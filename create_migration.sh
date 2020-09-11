#!/usr/bin/env bash

# This script creates a migration file enforcing linear cronological ids

set -euo pipefail

INSTALL="false"
GENERATE=""


while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--install)
        INSTALL="true"
        shift
        ;;
        -g|--autogenerate)
        GENERATE="--autogenerate"
        shift
        ;;
        *)
        shift
        ;;
    esac
done


if [ "$INSTALL" == "true" ]; then
    pip install -r requirements.txt
fi

echo -n "Migration name? " && read -r -e NAME

# trim whitespace
NAME="$(echo "$NAME" | xargs)"

if [ "$NAME" == "" ]; then
    echo ""
    bash create_migration.sh
else
    STAMP="$(date +"%Y_%m_%dT%H_%M_%S")"
    alembic revision $GENERATE --rev-id "$STAMP" -m "$NAME"
fi


