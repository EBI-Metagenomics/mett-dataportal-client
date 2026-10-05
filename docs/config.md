# Configuration and authentication

## Environment variables

```bash
export METT_BASE_URL="http://www.gut-microbes.org"   # default
export METT_JWT="your-jwt-token"                      # experimental endpoints
export METT_RELEASE=v1                                # optional; sent as X-METT-Release
export METT_TIMEOUT=60
export METT_VERIFY_SSL=true                           # set false only for local/dev TLS
export METT_USER_AGENT="my-app/1.0"
```

## Config file

`~/.mett/config.toml` (Windows: `%USERPROFILE%\.mett\config.toml`):

```toml
base_url = "http://www.gut-microbes.org"
# jwt_token = "..."
# release = "v1"
timeout = 60
verify_ssl = true
```

### Priority (later wins)

1. Defaults
2. Config file
3. Environment variables
4. Constructor / CLI flags (`--base-url`, `--jwt`, `--release`, …)

## Authentication

**Public** (no JWT): species, genomes, genes search/get, releases, orthologs/operons that are exposed publicly in OpenAPI.

**Protected** (JWT): drugs, proteomics, essentiality, fitness, PPI, TTP, and most experimental routes.

```bash
export METT_JWT="your-token"
mett drugs mic --drug-name amoxicillin --species BU --format json
# or
mett --jwt "your-token" drugs mic --drug-name amoxicillin --format json
```

```python
from mett_client import DataPortalClient

client = DataPortalClient(jwt_token="your-token")
```

Obtain a token from METT Data Portal administrators.

### Auth troubleshooting

- Confirm `echo $METT_JWT` is set and non-empty
- Token may be expired — request a new one
- Catch `AuthenticationError` from `mett_client.exceptions`

## Python / CLI examples

```python
from mett_client import DataPortalClient, Config, get_config
from pathlib import Path

client = DataPortalClient(base_url="http://localhost:8000", verify_ssl=False, release="v1")
client = DataPortalClient(config=get_config(config_path=Path("/path/to/config.toml")))
```

```bash
mett --base-url http://localhost:8000 --verify-ssl false species list
mett --release v1 genomes search --query BU --format json
```

## Proxies

`HTTP_PROXY` / `HTTPS_PROXY` are honored by `requests`.

## See also

- [CLI Guide](cli.md)
- [Python API](python.md)
- [Troubleshooting](troubleshooting.md)
