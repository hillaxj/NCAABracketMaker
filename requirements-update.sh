#!/usr/bin/env bash
set -eux

HERE="$(dirname "$0")"
REQUIREMENTS_FILE="${HERE}/requirements.txt"
REQUIREMENTS_VE="/tmp/requirements_update_ve"

rm -rf "${REQUIREMENTS_VE}"
/usr/bin/python3 -m venv --prompt tmp "${REQUIREMENTS_VE}"
set +eux
. "${REQUIREMENTS_VE}/bin/activate"
set -eux
pip install -U 'pip-tools'

pip-compile --allow-unsafe --generate-hashes --upgrade --rebuild --verbose --annotate --output-file="${REQUIREMENTS_FILE}" requirements.in

# fix the path of the `-e` req
sed -i -r 's|file:///.*$|.|' "${REQUIREMENTS_FILE}"

rm -rf "${REQUIREMENTS_VE}"
