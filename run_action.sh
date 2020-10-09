#!/usr/bin/env bash
set -uo pipefail

# Assume this script is in the src directory and work from that location
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

source "$PROJECT_ROOT/scripts/include.sh"


function usage {
    echo ""
    echo "usage: $0 -uphdD command [direction] [version]"
    echo "  command             migrate | seed    migrate or seed db"
    echo ""
    echo "options required when using migrate command"
    echo "  direction           up | down         direction to migrate db"
    echo "  version             alembic version id"
    db_usage
    exit 1
}

parse_args "$@"
set -- "${ARGS[@]}"

if [ "$ACTION" != "seed" ] && [ "$ACTION" != "migrate" ]; then
    usage
fi

prepare_connection



if [ "$ACTION" == "migrate" ]; then
    VERSION="$*"

    if [ $# -ne 1 ] || [ "$DIRECTION" == "" ] || [ "$VERSION" == "" ]; then
        usage
    fi

    exec_in_container alembic "${DIRECTION}grade" "$VERSION"
    exitonfail $? "migrate action"
    exit 0
fi

if [ $# -ne 0 ]; then
    usage
fi

if [ "$SEED" != "true" ]; then
    echo_warning 'cannot seed as SEED env is not set to "true"'
    exit 0
fi
exec_in_container python ./scripts/run_seeders.py
exitonfail $? "seed action"
