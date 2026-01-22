# Configuration Guide

This guide covers all configuration options for the METT Data Portal client.

## Table of Contents

- [Authentication](#authentication)
- [Environment Variables](#environment-variables)
- [Config File](#config-file)
- [Python Configuration](#python-configuration)
- [CLI Options](#cli-options)

## Authentication

### Public vs. Protected Endpoints

**Public Endpoints** (no authentication required):
- Species listing and search
- Genome listing and search
- Gene listing and search
- System health and features

**Protected Endpoints** (authentication required):
- Drug MIC and metabolism data
- Proteomics data
- Essentiality data
- Fitness data
- Protein-protein interactions
- TTP interactions
- Most experimental endpoints

### Authentication Methods

The client supports multiple authentication methods, in order of precedence:

1. **JWT Token** (recommended for experimental endpoints)
2. **API Key** (if supported by the API)
3. **No authentication** (for public endpoints)

## Environment Variables

### Required for Protected Endpoints

```bash
export METT_JWT="your-jwt-token-here"
```

### Optional Configuration

```bash
# Base URL (defaults to https://www.gut-microbes.org)
export METT_BASE_URL="https://www.gut-microbes.org"

# Request timeout in seconds (default: 30)
export METT_TIMEOUT=60

# SSL verification (default: true)
export METT_VERIFY_SSL=true

# Custom user agent
export METT_USER_AGENT="my-app/1.0"
```

### Example Setup

```bash
# For production
export METT_BASE_URL="https://www.gut-microbes.org"
export METT_JWT="eyJhbGciOi..."
export METT_TIMEOUT=60
export METT_VERIFY_SSL=true

# For development (no SSL certificate)
export METT_BASE_URL="http://localhost:8000"
export METT_VERIFY_SSL=false
export METT_TIMEOUT=30
```

## Config File

Create a configuration file at `~/.mett/config.toml`:

```toml
# Base URL for the API
base_url = "https://www.gut-microbes.org"

# Authentication
jwt_token = "your-jwt-token-here"
# api_key = "alternative-api-key"  # If supported

# Request settings
timeout = 60
verify_ssl = true

# User agent
user_agent = "mett-client/{version}"  # Version is auto-detected from package
```

### Config File Location

The config file is located at:
- **Linux/macOS**: `~/.mett/config.toml`
- **Windows**: `%USERPROFILE%\.mett\config.toml`

### Config File Priority

Configuration is loaded in this order (later values override earlier ones):

1. Default values
2. Config file (`~/.mett/config.toml`)
3. Environment variables
4. Programmatic configuration (Python/CLI)

## Python Configuration

### Using Config Object

```python
from mett_client import DataPortalClient, Config

# Create custom config
config = Config(
    base_url="https://www.gut-microbes.org",
    jwt_token="your-token",
    timeout=60,
    verify_ssl=True
)

# Use config
client = DataPortalClient(config=config)
```

### Direct Initialization

```python
from mett_client import DataPortalClient

# Initialize with parameters
client = DataPortalClient(
    base_url="https://www.gut-microbes.org",
    jwt_token="your-token",
    timeout=60,
    verify_ssl=True
)
```

### Loading Config from File

```python
from mett_client import get_config, DataPortalClient
from pathlib import Path

# Load from custom path
config = get_config(config_path=Path("/path/to/config.toml"))
client = DataPortalClient(config=config)
```

## CLI Options

### Global Options

All CLI commands support these global options:

```bash
# Override base URL
mett --base-url http://localhost:8000 species list

# Override JWT token
mett --jwt "your-token" drugs mic --drug-name "amoxicillin"

# Override timeout
mett --timeout 120 genomes search --query "test"

# Disable SSL verification
mett --verify-ssl false species list
```

### Per-Command Configuration

```bash
# Use environment variables (recommended)
export METT_JWT="your-token"
mett drugs mic --drug-name "amoxicillin"

# Or use CLI flags
mett --jwt "your-token" drugs mic --drug-name "amoxicillin"
```

## Configuration Examples

### Development Setup

```bash
# .env file or shell profile
export METT_BASE_URL="http://localhost:8000"
export METT_VERIFY_SSL=false
export METT_TIMEOUT=30
```

### Production Setup

```bash
# .env file or shell profile
export METT_BASE_URL="https://www.gut-microbes.org"
export METT_JWT="production-jwt-token"
export METT_VERIFY_SSL=true
export METT_TIMEOUT=60
```

### CI/CD Setup

```yaml
# GitHub Actions example
env:
  METT_BASE_URL: ${{ secrets.METT_BASE_URL }}
  METT_JWT: ${{ secrets.METT_JWT }}
  METT_TIMEOUT: 60
```

## Troubleshooting

### Authentication Errors

```python
from mett_client.exceptions import AuthenticationError

try:
    client = DataPortalClient()
    result = client.search_drug_mic(drug_name="test")
except AuthenticationError as e:
    print(f"Check your JWT token: {e}")
```

### SSL Certificate Issues

For development environments without proper SSL certificates:

```bash
export METT_VERIFY_SSL=false
```

**Warning**: Only use this in development. Never disable SSL verification in production.

### Timeout Issues

If requests are timing out:

```python
# Increase timeout
client = DataPortalClient(timeout=120)
```

Or via environment variable:

```bash
export METT_TIMEOUT=120
```

## See Also

- [Usage Guide](USAGE.md) - Usage examples
- [API Reference](../reference/api-reference.qmd) - Complete API documentation
