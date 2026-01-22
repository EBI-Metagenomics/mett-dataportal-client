# API Reference

This directory contains the API reference documentation and example files.

## Contents

- **[API Reference](api-reference.qmd)** - Complete API reference (Quarto format)
  - Auto-generated from OpenAPI specification
  - Includes tabbed examples (Friendly CLI, Generic CLI, cURL)
  - Render with: `quarto render docs/reference/api-reference.qmd`

- **[CLI Examples](cli-examples.md)** - Comprehensive CLI command examples (friendly and generic CLI)
- **[cURL Examples](curl-examples.md)** - Raw HTTP request examples

## Generating the API Reference

The API reference is automatically generated:

```bash
# Generate from OpenAPI spec and examples
python3 scripts/generate-api-docs.py

# Render to HTML
quarto render docs/reference/api-reference.qmd
```

## See Also

- [CLI Guide](../cli/overview.md) - How to use the CLI
- [Python API Guide](../python/quickstart.md) - How to use the Python client
- [Configuration Guide](../config/configuration.md) - Setup and configuration
