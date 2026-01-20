#!/bin/bash
# Script to export OpenAPI schema from METT Data Portal API

# Default values
BASE_URL="${METT_API_URL:-http://localhost:8000}"
OUTPUT_FILE="${1:-openapi.json}"

echo "Exporting OpenAPI schema from ${BASE_URL}/api/openapi.json"
echo "Output file: ${OUTPUT_FILE}"

# Fetch the OpenAPI schema
curl -s "${BASE_URL}/api/openapi.json" -o "${OUTPUT_FILE}"

if [ $? -eq 0 ]; then
    echo "✅ Successfully exported OpenAPI schema to ${OUTPUT_FILE}"
    echo "📄 File size: $(wc -c < ${OUTPUT_FILE}) bytes"

    # Validate JSON
    if command -v jq &> /dev/null; then
        echo "✅ JSON is valid"
        echo "📊 API Info:"
        jq -r '.info | "Title: \(.title)\nVersion: \(.version)\nDescription: \(.description)"' "${OUTPUT_FILE}"
        echo ""
        echo "📈 Endpoints:"
        jq -r '.paths | keys | length | "Total endpoints: \(.)"' "${OUTPUT_FILE}"
    else
        echo "ℹ️  Install 'jq' for JSON validation and stats"
    fi
else
    echo "❌ Failed to export OpenAPI schema"
    exit 1
fi
