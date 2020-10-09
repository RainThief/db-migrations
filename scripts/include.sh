#!/usr/bin/env bash

IMAGE_NAME=${CI_IMAGE:-"migrations_ci_support_image"}
CI=${CI:-"false"}
PYTHONPATH="$(pwd)"
export PYTHONPATH

SEED="${SEED:-""}"

# init args
DB_USERNAME=""
DB_PASSWORD=""
DB_HOST=""
DB_NAME=""
DB_PORT=0
DB_DRIVER=""
ACTION=""
GENERATE=""
DIRECTION=""

_pushd(){
    command pushd "$@" > /dev/null
}

_popd(){
    command popd > /dev/null
}

db_usage() {
    echo "  -u | --user         databse username"
    echo "  -p | --password     database password"
    echo "  -h | --host         database host"
    echo "  -d | --database     database name"
    echo "  -D | --driver       database driver [postgresql|mysql|sqlite]"
    echo "  -P | --port        database port"
    echo ""
}


parse_args() {
    ARGS=()
    while [[ $# -gt 0 ]]; do
        case $1 in
            -u|--user)
            shift
            export DB_USERNAME="${1:-""}"
            shift
            ;;
            -p|--password)
            shift
            export DB_PASSWORD="${1:-""}"
            shift
            ;;
            -h|--host)
            shift
            export DB_HOST="${1:-""}"
            shift
            ;;
            -d|--database)
            shift
            export DB_NAME="${1:-""}"
            shift
            ;;
            -D|--driver)
            shift
            export DB_DRIVER="${1:-""}"
            shift
            ;;
            -P|--port)
            shift
            export DB_PORT="${1:-""}"
            shift
            ;;
            -g|--autogenerate)
            export GENERATE="--autogenerate"
            shift
            ;;
            migrate|seed)
            export ACTION="$1"
            shift
            ;;
            up|down)
            export DIRECTION="$1"
            shift
            ;;
            *)
            ARGS+=("$1")
            shift
            ;;
        esac
    done


    DEFAULT_PORT=0
    case $DB_DRIVER in
        postgresql)
        DEFAULT_PORT=5432
        ;;
        mysql)
        DEFAULT_PORT=3306
        ;;
        sqlite)
        ;;
        *)
        # if not known driver show usage
        usage
    esac
    if [ "$DB_PORT" -eq 0 ]; then
        DB_PORT=$DEFAULT_PORT
    fi
}

get_db_connection_details_from_env() {
    DB_URL="${DB_URL:-""}"

    # if database url is in env use it but allow cli args to take precedence
    if [ "$DB_URL" != "" ]; then
        DB="$(parse_db_url database)"
        exitonfail $? "parsing database url"
        DB_NAME=${DB_NAME:-"$DB"}
        DB_USERNAME=${DB_USERNAME:-"$(parse_db_url username)"}
        DB_PASSWORD=${DB_PASSWORD:-"$(parse_db_url password)"}
        DB_HOST=${DB_HOST:-"$(parse_db_url host)"}
        DB_DRIVER=${DB_DRIVER:-"$(parse_db_url drivername)"}
        DB_PORT=${DB_PORT:-"$(parse_db_url port)"}
        if [ "$DB_PORT" == "None" ]; then
            DB_PORT="5432"
        fi
    fi
}

parse_db_url() {
    python -c "from sqlalchemy.engine.url import make_url; print(make_url('$DB_URL').$1)"
    return $?
}

# driver dbname user password
prepare_connection(){

    get_db_connection_details_from_env

    if [ "$DB_USERNAME" == "" ] || [ "$DB_PASSWORD" == "" ] || [ "$DB_HOST" == "" ] || [ "$DB_NAME" == "" ] || [ "$DB_DRIVER" = "" ]; then
        usage
    fi

    INI_FILE="$(sed "s/driver/$DB_DRIVER/g" migrations/alembic.ini-dist)"
    INI_FILE="${INI_FILE//dbname/$DB_NAME}"
    INI_FILE="${INI_FILE//localhost/$DB_HOST}"
    INI_FILE="${INI_FILE//user/$DB_USERNAME}"
    INI_FILE="${INI_FILE//pass/$DB_PASSWORD}"
    INI_FILE="${INI_FILE//port/$DB_PORT}"
    echo "$INI_FILE" > './alembic.ini'
}

exec_in_container() {
    if ! docker pull "$IMAGE_NAME"; then
        _pushd "${PROJECT_ROOT}"
        docker build --pull -t "$IMAGE_NAME" -f ./scripts/Dockerfile .
        exitonfail $? "Docker build"
        _popd
    fi

    CONT_USER=$(id -u):$(id -g)
    OPTS="-it --init"

    if [ "$CI" == "true" ]; then
        CONT_USER=0
        OPTS="-t"
    fi

    docker run --rm $OPTS -u="$CONT_USER" --name "$IMAGE_NAME" \
        -v "$PROJECT_ROOT/:/usr/app/" \
        -e "CI=$CI" \
        -e "PYTHONPATH=/usr/app" \
        -e "SEED=$SEED" \
        --network=host \
        "$IMAGE_NAME" "$@"
}

exitonfail() {
    if [ "$1" -ne "0" ]
    then
        echo_danger "$2 failed"
        exit 1
    fi
}

warnonfail() {
    if [ "$1" -ne "0" ] && [ "$CI" != "true" ]
    then
        echo_warning "$2 warning"
    fi
}

echo_colour() {
    colour=$2
    no_colour='\033[0m'
    echo -e "${colour}$1${no_colour}"
}

echo_warning(){
    yellow='\033[0;33;1m'
    echo_colour "$1" "${yellow}"
}

echo_success(){
    green='\033[0;32;1m'
    echo_colour "$1" "${green}"
}

echo_danger(){
    red='\033[0;31;1m'
    echo_colour "$1" "${red}"
}

echo_info(){
  cyan='\033[0;36;1m'
  echo_colour "$1" "${cyan}"
}
