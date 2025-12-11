# Quick Start Guide

## Generate and View Documentation

```bash
# Generate API reference from OpenAPI spec
make docs-generate

# Render to HTML
make docs-render

# Open in browser
open docs/reference/api-reference.html
```

## Preview While Editing

```bash
# Start preview server (auto-reloads on changes)
make docs-preview
```

## Update Documentation

1. Update `openapi.json` (via `scripts/export-openapi-schema.sh`)
2. Add examples to `cli-examples.md` or `curl-examples.md`
3. Regenerate: `make docs-generate`
4. Review and commit

