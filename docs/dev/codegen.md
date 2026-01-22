# SDK Code Generation

How to regenerate the SDK from the OpenAPI schema.

## Overview

The METT client uses an auto-generated SDK (`mett_dataportal_sdk/`) that is built from the OpenAPI specification. When the API schema changes, you need to regenerate the SDK.

## Prerequisites

- `openapi-generator-cli` installed
- Access to the METT API (for exporting the schema)

## Regenerating the SDK

### Step 1: Export OpenAPI Schema

```bash
# Export latest schema from API
./scripts/export-openapi-schema.sh

# Or manually set the base URL
METT_BASE_URL=http://localhost:8000 ./scripts/export-openapi-schema.sh
```

This creates/updates `openapi.json` in the repository root.

### Step 2: Generate SDK

```bash
# Regenerate SDK from openapi.json
./scripts/generate-sdk.sh
```

This will:
1. Use `openapi-generator-cli` to generate the SDK
2. Update `mett_dataportal_sdk/` with new models and API classes
3. Preserve any manual modifications (if any)

### Step 3: Update Client Code

After SDK regeneration:

1. Review changes in `mett_dataportal_sdk/`
2. Update `mett_client/client.py` if needed
3. Update CLI commands if API signatures changed
4. Run tests to verify compatibility

## SDK Structure

The generated SDK is located in `mett_dataportal_sdk/`:

```
mett_dataportal_sdk/
├── __init__.py
├── api/              # API client classes
│   ├── genes_api.py
│   ├── genomes_api.py
│   └── ...
├── models/           # Data models
│   ├── gene_response_schema.py
│   ├── genome_response_schema.py
│   └── ...
├── api_client.py     # Base API client
├── configuration.py  # Configuration
└── rest.py           # REST client
```

## Manual Modifications

If you need to make manual modifications to the generated SDK:

1. Document the changes clearly
2. Consider if the changes should be upstreamed to the API schema
3. Be aware that regeneration will overwrite manual changes

## Version Management

The SDK version is read from `pyproject.toml`:

```bash
# Extract version for SDK generation
version=$(python -c "import tomllib; f=open('pyproject.toml','rb'); print(tomllib.load(f)['project']['version'])")
```

## Troubleshooting

### SDK Generation Fails

- Check that `openapi-generator-cli` is installed and in PATH
- Verify `openapi.json` is valid JSON
- Check OpenAPI generator version compatibility

### Import Errors After Regeneration

- Ensure all generated files are present
- Check that package structure matches `pyproject.toml`
- Run `pip install -e .` to reinstall the package

## See Also

- **[Architecture](architecture.md)** - Overall project architecture
- **[Releasing](releasing.md)** - Release process including SDK updates
