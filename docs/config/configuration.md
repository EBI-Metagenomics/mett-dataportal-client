# Configuration

Configuration options for the METT Data Portal client.

## Environment Variables

The client supports the following environment variables:

### Base URL

```bash
# Default: http://www.gut-microbes.org
export METT_BASE_URL="http://www.gut-microbes.org"
```

### Timeout

```bash
# Default: 30 seconds
export METT_TIMEOUT=60
```

### SSL Verification

```bash
# Default: true
export METT_VERIFY_SSL=true

# For development (no SSL certificate)
export METT_VERIFY_SSL=false
```

**Warning**: Only disable SSL verification in development. Never use this in production.

### User Agent

```bash
# Default: mett-client/{version}
export METT_USER_AGENT="my-app/1.0"
```

## Config File

Create a configuration file at `~/.mett/config.toml`:

```toml
# Base URL for the API
base_url = "http://www.gut-microbes.org"

# Request settings
timeout = 60
verify_ssl = true

# User agent
user_agent = "mett-client/{version}"  # Version is auto-detected
```

### Config File Location

- **Linux/macOS**: `~/.mett/config.toml`
- **Windows**: `%USERPROFILE%\.mett\config.toml`

### Configuration Priority

Configuration is loaded in this order (later values override earlier ones):

1. Default values
2. Config file (`~/.mett/config.toml`)
3. Environment variables
4. Programmatic configuration (Python/CLI arguments)

## Python Configuration

### Using Config Object

```python
from mett_client import DataPortalClient, Config

config = Config(
    base_url="http://www.gut-microbes.org",
    timeout=60,
    verify_ssl=True
)

client = DataPortalClient(config=config)
```

### Direct Initialization

```python
from mett_client import DataPortalClient

client = DataPortalClient(
    base_url="http://www.gut-microbes.org",
    timeout=60,
    verify_ssl=True
)
```

### Loading from Custom Path

```python
from mett_client import get_config, DataPortalClient
from pathlib import Path

config = get_config(config_path=Path("/path/to/config.toml"))
client = DataPortalClient(config=config)
```

## CLI Configuration

### Global Options

All CLI commands support these global options:

```bash
# Override base URL
mett --base-url http://localhost:8000 species list

# Override timeout
mett --timeout 120 genomes search --query "test"

# Disable SSL verification
mett --verify-ssl false species list
```

## Common Setups

### Development

```bash
export METT_BASE_URL="http://localhost:8000"
export METT_VERIFY_SSL=false
export METT_TIMEOUT=30
```

### Production

```bash
export METT_BASE_URL="http://www.gut-microbes.org"
export METT_VERIFY_SSL=true
export METT_TIMEOUT=60
```

### CI/CD

```yaml
# GitHub Actions example
env:
  METT_BASE_URL: ${{ secrets.METT_BASE_URL }}
  METT_TIMEOUT: 60
```

## Proxies

If you need to use a proxy, set the standard `HTTP_PROXY` and `HTTPS_PROXY` environment variables:

```bash
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
```

The `requests` library (used by the client) will automatically use these.

## See Also

- **[Authentication](authentication.md)** - Setting up authentication
- **[Troubleshooting](../troubleshooting.md)** - Common configuration issues
