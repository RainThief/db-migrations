#!/usr/bin/env bash
set -uo pipefail

source "scripts/include.sh"

coverage run -m unittest discover
exitonfail $? "Unit tests"

coverage report --fail-under=80 --skip-covered --show-missing --skip-empty
exitonfail $? "Coverage check"

echo_success "Unit tests passed"
