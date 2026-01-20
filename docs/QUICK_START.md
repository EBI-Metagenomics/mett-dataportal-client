# Quick Start Guide

## Generate and View Documentation

```bash
# Generate API reference from OpenAPI spec
python3 scripts/generate-api-docs.py

# Render to HTML
quarto render docs/reference/api-reference.qmd

# Open in browser
open docs/reference/api-reference.html
```

## Preview While Editing

```bash
# Start preview server (auto-reloads on changes)
quarto preview docs/reference/api-reference.qmd
```

## Update Documentation

1. Update `openapi.json` (via `scripts/export-openapi-schema.sh`)
2. Add examples to `cli-examples.md` or `curl-examples.md`
3. Regenerate: `python3 scripts/generate-api-docs.py`
4. Review and commit
