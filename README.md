# METT Data Portal Client

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/mett.svg)](https://badge.fury.io/py/mett)

Python client library and command-line interface (CLI) for the **Microbial Ecosystems Transversal Themes (METT) Data Portal**.

- Portal: http://www.gut-microbes.org/
- Install from PyPI: `pip install mett`
- Python import package: `mett_client`

## Features

- 🚀 **High-level Python API** - Clean, intuitive interface for programmatic access
- 💻 **Command-line Interface** - CLI with rich output and shell completion
- 📊 **Multiple Output Formats** - JSON, TSV, and formatted tables
- 🔒 **Flexible Configuration** - Environment variables and config file support
- 📚 **Documentation** - Usage examples and API details
- 🔄 **Auto-generated SDK** - Stays in sync with the API schema

## Quick Start

### Installation

```bash
pip install mett
```

### CLI Usage

```bash
# List all species
mett species list

# Search genomes
mett genomes search --query "Bacteroides" --per-page 5

# Get gene information
mett genes get BU_ATCC8492_00001
```

### Python API

```python
from mett_client import DataPortalClient

# Initialize client
client = DataPortalClient()

# List species
species = client.list_species()
print(f"Found {len(species)} species")

# List genomes (paginated)
result = client.list_genomes(per_page=5)
print(f"Found {len(result.items)} genomes")

# Search genomes by species
result = client.species_genomes("BU", per_page=5)
print(f"Found {len(result.items)} BU genomes")

# Search genomes with query
result = client.search_genomes(query="ATCC", per_page=5)
print(f"Found {len(result.items)} genomes matching 'ATCC'")

# Search genomes - check first genome
if result.items:
    print(f"First genome: {result.items[0].isolate_name}")
```

## Configuration

The client/CLI can be configured using **environment variables** (recommended for CI and local dev) or a config file (if supported by your implementation).

### Common environment variables
```bash
# Base URL for the METT Data Portal API (if your client supports overriding it)
export METT_BASE_URL="https://www.gut-microbes.org/"

# If the API requires authentication (token / key), set it here (adjust name to match your implementation)
# export METT_API_TOKEN="..."

# SSL verification (useful for dev environments without certificates)
export METT_VERIFY_SSL=false
```

## Documentation

Complete documentation is available in the [docs/](https://github.com/EBI-Metagenomics/mett-dataportal-client/tree/main/docs/) directory:

- **[Getting Started](https://github.com/EBI-Metagenomics/mett-dataportal-client/tree/main/docs/index.md)** - Overview and quick start
- **[CLI Guide](https://github.com/EBI-Metagenomics/mett-dataportal-client/tree/main/docs/cli/overview.md)** - Command-line interface
- **[Python API](https://github.com/EBI-Metagenomics/mett-dataportal-client/tree/main/docs/python/quickstart.md)** - Python client library
- **[Configuration](https://github.com/EBI-Metagenomics/mett-dataportal-client/tree/main/docs/config/configuration.md)** - Setup and authentication
- **[Troubleshooting](https://github.com/EBI-Metagenomics/mett-dataportal-client/tree/main/docs/troubleshooting.md)** - Common issues and solutions

## Source & Support

* **Source repository**: https://github.com/EBI-Metagenomics/mett-dataportal-client
* **Issues / feature requests**: https://github.com/EBI-Metagenomics/mett-dataportal-client/issues


### Development

#### From source (conda) — recommended

Use a single conda environment. You do **not** need a separate `.venv`.

```bash
git clone https://github.com/EBI-Metagenomics/mett-dataportal-client.git
cd mett-dataportal-client

# Create / activate a conda env (name is arbitrary; mett-client is conventional)
conda create -n mett-client python=3.12 -y
conda activate mett-client

# Editable install with dev tools (pytest, ruff, pre-commit, …)
pip install -e ".[dev]"

# Install git hooks once per clone (uses the active conda env)
pre-commit install

mett --help
```

#### Running tests and linting

With `mett-client` activated:

```bash
pytest -v

ruff check mett_client/ scripts/ tests/
ruff format --check mett_client/ scripts/ tests/

# Optional: run all pre-commit hooks
pre-commit run --all-files
```

If commits fail with ``pre-commit` not found`, activate the conda env and reinstall the hook:

```bash
conda activate mett-client
pip install -e ".[dev]"
pre-commit install
```

#### Alternative: `uv`

```bash
git clone https://github.com/EBI-Metagenomics/mett-dataportal-client.git
cd mett-dataportal-client

uv sync --all-extras --dev
uv run mett --help

uv run pytest -v
uv run ruff check mett_client/ scripts/ tests/
uv run pre-commit install
uv run pre-commit run --all-files
```

## Requirements

- Python 3.10+
- See `pyproject.toml` for full dependency list


## License

Apache-2.0 License - see LICENSE file for details.

---

**Note**: For development environments without SSL certificates, you may need to set:
```bash
export METT_VERIFY_SSL=false
```
