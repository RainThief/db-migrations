#!/usr/bin/env bash

# This script creates a migration file enforcing linear cronological ids

set -euo pipefail

PIP=${1:-"true"}

if [ "$PIP" == "true" ]; then
    pip install -r requirements.txt
fi

echo -n "Migration name? " && read -e NAME

# trim whitespace
NAME="$(echo "$NAME" | xargs)"

if [ "$NAME" == "" ]; then
    echo ""
    bash create_migration.sh "false"
else
    STAMP="$(date +"%Y_%m_%dT%H_%M_%S")"
    alembic revision --rev-id "$STAMP" -m "$NAME"
fi


