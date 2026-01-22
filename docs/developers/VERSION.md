# Version Management

This document explains how version numbers are managed in the METT Data Portal client.

## Single Source of Truth

The version number is defined in **`pyproject.toml`** as the single source of truth:

```toml
[project]
version = "0.0.1a1"
```

## Automatic Version Detection

The package automatically reads the version from `pyproject.toml`:

1. **When installed**: Uses `importlib.metadata` to read the installed package version
2. **When not installed**: Reads directly from `pyproject.toml` using TOML parsing

## Files That Use Version

The following files automatically use the version from `pyproject.toml`:

- **`mett_client/__init__.py`**: Exports `__version__` for programmatic access
- **`mett_client/config.py`**: Uses version in default `user_agent` string
- **`scripts/generate-sdk.sh`**: Reads version from `pyproject.toml` for SDK generation

## Updating the Version

To update the version:

1. **Edit `pyproject.toml`**:
   ```toml
   [project]
   version = "0.2.0"  # Update this value
   ```

2. **No other files need to be updated** - they will automatically use the new version

3. **For SDK regeneration**: The `generate-sdk.sh` script will automatically use the new version

## Accessing Version Programmatically

```python
from mett_client import __version__
print(__version__)  # "0.1.0"

# Or directly
from mett_client.version import __version__
print(__version__)
```

## Version in User Agent

The default user agent string includes the version:

```python
from mett_client import DataPortalClient

client = DataPortalClient()
print(client.config.user_agent)  # "mett-dataportal-client/0.1.0"
```

## Version in Documentation

Documentation files may reference the version, but these are examples and don't need to be updated manually. The actual version used at runtime comes from `pyproject.toml`.
