#!/usr/bin/env bash

IMAGE_NAME=${CI_IMAGE:-"migrations_ci_support_image"}
CI=${CI:-"false"}

_pushd(){
    command pushd "$@" > /dev/null
}

_popd(){
    command popd > /dev/null
}

exec_in_container() {
    if ! docker pull "$IMAGE_NAME"; then
        _pushd "${PROJECT_ROOT}"
        docker build --pull -t "$IMAGE_NAME" -f ./scripts/Dockerfile .
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
        sleep 5
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