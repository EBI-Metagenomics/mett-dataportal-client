# METT Data Portal Client Documentation

Python client and CLI for the **Microbial Ecosystems Transversal Themes (METT) Data Portal**.

- Portal: http://www.gut-microbes.org/
- Install: `pip install mett`
- Import package: `mett_client`

## Quick start

```bash
pip install mett
mett species list
```

```python
from mett_client import DataPortalClient

client = DataPortalClient()
print(len(client.list_species()))
```

## Docs map

| Doc | Contents |
|-----|----------|
| [CLI Guide](cli.md) | Commands, recipes, public surface |
| [Python API](python.md) | Client methods, pagination, errors |
| [Configuration](config.md) | Env vars, config file, JWT, releases |
| [Examples](examples.md) | Curated CLI / generic CLI / cURL (OpenAPI-only) |
| [API Reference](reference/api-reference.qmd) | Generated from `openapi.json` |
| [Troubleshooting](troubleshooting.md) | Common failures |
| [Changelog](changelog.md) | Release notes |
| [SDK codegen](dev/codegen.md) | Regenerating `mett_dataportal_sdk/` |

Examples document only endpoints that appear in the public OpenAPI schema. Internal/hidden routes are not listed here even if a CLI wrapper still exists.
