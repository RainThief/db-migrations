#!/usr/bin/env bash
set -uo pipefail

# Assume this script is in the src directory and work from that location
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

source "$PROJECT_ROOT/scripts/include.sh"

exec_in_container python ./scripts/create_seeder.py "$@"
exitonfail $? "create seeder"
