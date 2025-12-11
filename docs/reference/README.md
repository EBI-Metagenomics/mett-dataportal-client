# API Reference

This directory contains the API reference documentation and example files.

## Contents

- **[API Reference](api-reference.qmd)** - Complete API reference (Quarto format)
  - Auto-generated from OpenAPI specification
  - Includes tabbed examples (Friendly CLI, Generic CLI, cURL)
  - Render with: `make docs-render`

- **[CLI Examples](cli-examples.md)** - Comprehensive CLI command examples (friendly and generic CLI)
- **[cURL Examples](curl-examples.md)** - Raw HTTP request examples

## Generating the API Reference

The API reference is automatically generated:

```bash
# Generate from OpenAPI spec and examples
make docs-generate

# Render to HTML
make docs-render
```

## See Also

- [Usage Guide](../guides/USAGE.md) - How to use the client
- [Configuration Guide](../guides/CONFIGURATION.md) - Setup and configuration
- [Development Guide](../developers/DEVELOPMENT.md) - Development workflows
