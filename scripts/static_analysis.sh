#!/usr/bin/env bash
set -uo pipefail


source "scripts/include.sh"


export PYLINTHOME="/tmp"


echo_info "linting python"
FILES=$(find util seeds scripts migrations -iname "*.py")
while IFS= read -r FILE; do
    # echo_info "linting $FILE"
    if ! RESULT=$(pylint "$@" "$FILE"); then
        echo "$RESULT"
        exitonfail 1 "pylint"
    fi
done < <(printf '%s\n' "$FILES")


echo_info "linting bash"
shellcheck ./*.sh
exitonfail $? "shellcheck"


echo_info "linting dockerfile"
FILES=$(find . -iname "Dockerfile*")
while IFS= read -r FILE; do
    if ! RESULT=$(hadolint "$@" "$FILE"); then
        EXIT=$?
        echo "$RESULT"
        exitonfail $EXIT "hadolint"
    fi
done < <(printf '%s\n' "$FILES")


echo_success "Static analysis passed"
