#!/usr/bin/env bash
set -euo pipefail

pip install -r requirements.txt

echo -n "Migration name? " && read -e NAME

# trim whitespace
NAME="$(echo $NAME | xargs)"

STAMP="$(date +"%Y_%m_%dT%H_%M_%S")"
alembic revision --rev-id $STAMP -m "$NAME"
