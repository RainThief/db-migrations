#!/usr/bin/env bash
set -uo pipefail

source "scripts/include.sh"

pip freeze | safety check --stdin
exitonfail $? "dependency audit"

LICENSE_LIST="$(curl -L https://raw.githubusercontent.com/rainthief/react-lint-config/master/licenses.json | jq -c -r '.[]')"
exitonfail $? "obtaining license list"

LICENSES_USED="$(pip-licenses)"

# check what licenses are used in pip packages and remove ones that are allowed
IFS=$'\n'
for LICENSE in $LICENSE_LIST; do
    LICENSES_USED="$(sed "/$LICENSE/d" <<< "$LICENSES_USED")"
done

# if results contain more than just heading row we have license violations
# disable word splitting warning as wc produces number
# shellcheck disable=SC2046
if [ $(echo "$LICENSES_USED" | wc -l) -gt 1 ]; then
    echo "$LICENSES_USED"
    warnonfail 1 "licence checker"
    echo "PLEASE REVIEW LICENSES LISTED ABOVE"
fi

echo_success "Security audit passed"
