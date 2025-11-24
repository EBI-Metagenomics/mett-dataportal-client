#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMA_PATH="${ROOT_DIR}/openapi.json"
OUTPUT_DIR="${ROOT_DIR}/generated"
PACKAGE_NAME="mett_dataportal_sdk"

if [[ ! -f "${SCHEMA_PATH}" ]]; then
  echo "OpenAPI schema not found at ${SCHEMA_PATH}. Run scripts/export-openapi-schema.sh first." >&2
  exit 1
fi

rm -rf "${OUTPUT_DIR}"
openapi-generator-cli generate \
  --skip-validate-spec \
  -i "${SCHEMA_PATH}" \
  -g python \
  -o "${OUTPUT_DIR}" \
  --package-name "${PACKAGE_NAME}" \
  --additional-properties=packageVersion=0.1.0,projectName=mett-dataportal-sdk

rm -rf "${ROOT_DIR}/${PACKAGE_NAME}" "${ROOT_DIR}/.openapi-generator"
mv "${OUTPUT_DIR}/${PACKAGE_NAME}" "${ROOT_DIR}/${PACKAGE_NAME}"
mv "${OUTPUT_DIR}/.openapi-generator" "${ROOT_DIR}/.openapi-generator"
rm -rf "${OUTPUT_DIR}"
