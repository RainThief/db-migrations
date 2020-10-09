#!/usr/bin/env bash
set -uo pipefail

# Assume this script is in the src directory and work from that location
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

source "$PROJECT_ROOT/scripts/include.sh"


function usage {
    echo ""
    echo "usage: $0 [-guphdD]  migration_name"
    echo "  -g | --autogenerate     generate migration file from model changes"
    echo ""
    echo "options required when using autogeneration of versions"
    db_usage
    exit 1
}


parse_args "$@"
set -- "${ARGS[@]}"

if [ $# -ne 1 ]; then
    usage
fi

NAME="$*"

if [ "$NAME" == "" ]; then
    usage
fi

# if auto generate then we need a valid alembic config for connection
if [ "$GENERATE" != "" ]; then
    prepare_connection
fi


# allow command to fail if empty repo
COMMIT_HASH=$(git rev-parse --verify --short HEAD) || true
STAMP="$(date +"%Y_%m_%dT%H_%M_%S")"
# cannot quote generate var as if empty stops alembic parsing args
# shellcheck disable=SC2086
exec_in_container alembic revision $GENERATE --rev-id "${STAMP}__${COMMIT_HASH}_" -m "$NAME"
exitonfail $? "create migration"
