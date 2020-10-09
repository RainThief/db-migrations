#!/usr/bin/env bash
set -uo pipefail

source "scripts/include.sh"

# alembic needs config file even though connection is mocked
export DB_URL=postgresql://user:pass@localhost/dbname
prepare_connection "postgresql" "db" "localhost" "user" "pass"

coverage run -m unittest discover
exitonfail $? "Unit tests"

coverage report --fail-under=80 --skip-covered --show-missing --skip-empty
exitonfail $? "Coverage check"

echo_success "Unit tests passed"
