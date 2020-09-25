#!/usr/bin/env bash
set -euo pipefail

# This script creates a migration file enforcing linear cronological ids

source ./scripts/include.sh


function usage {
    echo ""
    echo "usage: $0 [-g]  migration_name"
    echo "  -g | --autogenerate     generate migration file from model changes"
    echo ""
    exit 1
}

# no args passed display usage
if [ $# -eq 0 ]; then
    usage
fi


GENERATE=""
NAME=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -g|--autogenerate)
        GENERATE="--autogenerate"
        shift
        ;;
        *)
        NAME="$1"
        shift
        ;;
    esac
done


# trim whitespace
NAME="$(echo "$NAME" | xargs)"

if [ "$NAME" == "" ]; then
    echo "please provide a migration name [--name]"
    exit 1
fi


# allow command to fail if empty repo
COMMIT_HASH=$(git rev-parse --verify --short HEAD) || true
STAMP="$(date +"%Y_%m_%dT%H_%M_%S")"
alembic revision $GENERATE --rev-id "${STAMP}__${COMMIT_HASH}_" -m "$NAME"

