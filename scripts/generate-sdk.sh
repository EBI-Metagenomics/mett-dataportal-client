#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMA_PATH="${ROOT_DIR}/openapi.json"
OUTPUT_DIR="${ROOT_DIR}/generated"
PACKAGE_NAME="mett_dataportal_sdk"
PYPROJECT_PATH="${ROOT_DIR}/pyproject.toml"

if [[ ! -f "${SCHEMA_PATH}" ]]; then
  echo "OpenAPI schema not found at ${SCHEMA_PATH}. Run scripts/export-openapi-schema.sh first." >&2
  exit 1
fi

# Extract version from pyproject.toml
if [[ -f "${PYPROJECT_PATH}" ]]; then
  # Use Python to parse TOML (more reliable than grep/sed)
  PACKAGE_VERSION=$(python3 -c "
import sys
from pathlib import Path
try:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib
    pyproject_path = Path('${PYPROJECT_PATH}')
    with open(pyproject_path, 'rb') as f:
        data = tomllib.load(f)
        print(data['project']['version'])
except Exception as e:
    print('0.1.0', file=sys.stderr)
    sys.exit(1)
" 2>&1)

  # Check if extraction failed
  if [[ $? -ne 0 ]] || [[ -z "${PACKAGE_VERSION}" ]]; then
    echo "Warning: Could not parse version from pyproject.toml, using default 0.1.0" >&2
    PACKAGE_VERSION="0.1.0"
  fi
else
  echo "Warning: pyproject.toml not found, using default version 0.1.0" >&2
  PACKAGE_VERSION="0.1.0"
fi

echo "Using package version: ${PACKAGE_VERSION}"

rm -rf "${OUTPUT_DIR}"
openapi-generator-cli generate \
  --skip-validate-spec \
  -i "${SCHEMA_PATH}" \
  -g python \
  -o "${OUTPUT_DIR}" \
  --package-name "${PACKAGE_NAME}" \
  --additional-properties=packageVersion=${PACKAGE_VERSION},projectName=mett-dataportal-sdk

rm -rf "${ROOT_DIR}/${PACKAGE_NAME}" "${ROOT_DIR}/.openapi-generator"
mv "${OUTPUT_DIR}/${PACKAGE_NAME}" "${ROOT_DIR}/${PACKAGE_NAME}"
mv "${OUTPUT_DIR}/.openapi-generator" "${ROOT_DIR}/.openapi-generator"
rm -rf "${OUTPUT_DIR}"
