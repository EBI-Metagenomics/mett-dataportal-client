# Development Guide

This guide covers development setup, testing, and contribution workflows.

## Table of Contents

- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Regenerating the SDK](#regenerating-the-sdk)
- [Running Tests](#running-tests)
- [Code Quality](#code-quality)
- [Documentation](#documentation)
- [Release Process](#release-process)

## Development Setup

### Prerequisites

- Python 3.10 or higher
- `pip` and `setuptools`
- `openapi-generator-cli` (for SDK generation)

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/EBI-Metagenomics/mett-dataportal-client.git
cd mett-dataportal-client

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

### Using Conda

```bash
# Create conda environment
conda create -n mett-client python=3.12 -y
conda activate mett-client

# Install package + dev dependencies
pip install -e ".[dev]"
```

### Verify Installation

```bash
# Test CLI
mett --help

# Test Python import
python -c "from mett_dataportal import DataPortalClient; print('OK')"
```

## Project Structure

```
mett-dataportal-client/
├── mett_dataportal/          # Main package
│   ├── cli/                   # CLI commands
│   │   ├── core/              # Core APIs
│   │   │   ├── system.py
│   │   │   ├── species.py
│   │   │   ├── genomes.py
│   │   │   └── genes.py
│   │   ├── experimental/     # Experimental APIs
│   │   │   ├── drugs.py
│   │   │   ├── proteomics.py
│   │   │   └── ...
│   │   ├── interactions/      # Interaction APIs
│   │   │   ├── ppi.py
│   │   │   └── ttp.py
│   │   ├── main.py            # CLI entry point
│   │   ├── utils.py            # Shared utilities
│   │   └── output.py           # Output formatting
│   ├── client.py               # High-level API client
│   ├── config.py               # Configuration
│   ├── exceptions.py           # Custom exceptions
│   ├── utils.py                # General utilities
│   └── request_utils.py        # HTTP utilities
├── mett_dataportal_sdk/        # Auto-generated SDK
├── docs/                        # Documentation
│   ├── api-reference.qmd       # API reference (Quarto)
│   ├── USAGE.md                # Usage guide
│   ├── CONFIGURATION.md        # Configuration guide
│   └── DEVELOPMENT.md          # This file
├── scripts/                     # Utility scripts
│   ├── generate-sdk.sh         # SDK generation
│   ├── generate-api-docs.py    # Documentation generation
│   └── export-openapi-schema.sh # OpenAPI export
├── tests/                       # Test suite
├── pyproject.toml               # Project configuration
└── README.md                    # Main README
```

## Regenerating the SDK

When the API schema changes, regenerate the SDK:

### Step 1: Export OpenAPI Schema

```bash
# Export latest schema from API
./scripts/export-openapi-schema.sh

# Or manually set the base URL
METT_BASE_URL=http://localhost:8000 ./scripts/export-openapi-schema.sh
```

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
2. Update `mett_dataportal/client.py` if needed
3. Update CLI commands if API signatures changed
4. Run tests to verify compatibility

## Running Tests

### Run All Tests

```bash
# Using uv (recommended)
uv run pytest -v

# Or directly
pytest tests/
```

### Run Specific Tests

```bash
# Run tests in a specific file
pytest tests/test_client.py

# Run tests matching a pattern
pytest tests/ -k "test_search"

# Run with verbose output
pytest tests/ -v
```

### Test Coverage

```bash
# Install coverage tool
pip install pytest-cov

# Run with coverage
pytest --cov=mett_dataportal tests/
```

## Code Quality

### Linting

```bash
# Check code style (using uv)
uv run ruff check mett_dataportal/ scripts/ tests/

# Or directly
ruff check mett_dataportal/ scripts/ tests/
```

# Check specific files
ruff check mett_dataportal/client.py
```

### Formatting

```bash
# Format code (using uv)
uv run ruff format mett_dataportal/ scripts/ tests/

# Or directly
ruff format mett_dataportal/ scripts/ tests/
```

# Check formatting without changes
ruff format --check mett_dataportal/
```

### Type Checking

```bash
# Install mypy (if using)
pip install mypy

# Run type checker
mypy mett_dataportal/
```

## Documentation

### Generating API Documentation

```bash
# Generate API reference from OpenAPI spec
python3 scripts/generate-api-docs.py

# Render to HTML
quarto render docs/reference/api-reference.qmd

# Preview in browser (watch mode)
quarto preview docs/reference/api-reference.qmd
```

### Documentation Structure

- `docs/reference/api-reference.qmd` - Main API reference (auto-generated)
- `docs/guides/USAGE.md` - Usage examples (manual)
- `docs/guides/CONFIGURATION.md` - Configuration guide (manual)
- `docs/developers/DEVELOPMENT.md` - This file (manual)

### Updating Documentation

1. **API Reference**: Regenerate with `python3 scripts/generate-api-docs.py`
2. **Usage Examples**: Edit `docs/guides/USAGE.md`
3. **Configuration**: Edit `docs/guides/CONFIGURATION.md`
4. **Development**: Edit `docs/developers/DEVELOPMENT.md`

## Release Process

For detailed release instructions, see the **[Release Guide](RELEASE.md)**.

### Quick Release Steps

1. **Update version** in `pyproject.toml`
2. **Regenerate SDK** (if API changed): `./scripts/generate-sdk.sh`
3. **Run tests**: `uv run pytest -v && uv run ruff check mett_dataportal/ scripts/ tests/`
4. **Commit and push**: `git commit -m "Release v0.1.1" && git push`
5. **Create and push tag**: `git tag v0.1.1 && git push origin v0.1.1`
6. **GitHub Actions** - Manually trigger publish workflows:
   - **Publish to TestPyPI** - For testing
   - **Publish to PyPI** - For production

### Manual Publishing

If you prefer to publish manually:

```bash
# Build package
pip install build twine
python -m build

# Verify build
twine check dist/*

# Publish to PyPI
twine upload dist/*
```

See **[Release Guide](RELEASE.md)** for complete instructions, including:
- PyPI account setup
- GitHub Secrets configuration
- Automated vs manual publishing
- Troubleshooting
- Best practices

## Common Tasks

### Adding a New CLI Command

1. Identify the appropriate module (`core/`, `experimental/`, or `interactions/`)
2. Add command function to the module
3. Register in `cli/main.py`
4. Add examples to `docs/guides/USAGE.md`
5. Update API reference if needed

### Modifying Client API

1. Update `mett_dataportal/client.py`
2. Add/update tests in `tests/`
3. Update documentation
4. Ensure backward compatibility

### Debugging

```bash
# Enable debug logging
export METT_DEBUG=true

# Run with verbose output
mett --verbose species list

# Test specific endpoint
python -c "
from mett_dataportal import DataPortalClient
client = DataPortalClient()
print(client.list_species())
"
```

## See Also

- [Usage Guide](../guides/USAGE.md) - Usage examples
- [Configuration Guide](../guides/CONFIGURATION.md) - Configuration options
- [API Reference](../reference/api-reference.qmd) - Complete API documentation
- [Contributing Guide](../CONTRIBUTING.md) - Contribution guidelines
