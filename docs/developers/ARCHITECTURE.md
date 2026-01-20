# Package Architecture & Design Guide

> **Note:** This document is intended for developers and contributors. For user documentation, see the [Usage Guide](../guides/USAGE.md) and [API Reference](../reference/api-reference.qmd).

## Executive Summary

This guide outlines the architecture and design decisions for the METT Data Portal Python client package. It covers repository structure, code generation approaches, technology stack choices, and PyPI publishing strategies. This document is useful for:
- Contributors understanding the project structure
- Developers making architectural decisions
- Maintainers planning future improvements

---

## 1. Repository Structure Decision

### Option A: Separate Repository (Recommended for Public Packages)

**Pros:**
- ✅ Clean separation of concerns
- ✅ Independent versioning and release cycles
- ✅ Easier to maintain different access controls
- ✅ Standard practice for public PyPI packages
- ✅ Simpler CI/CD pipelines
- ✅ Better for open-source distribution

**Cons:**
- ❌ Requires syncing API changes manually or via automation
- ❌ Two repositories to maintain

**When to use:** When publishing to PyPI for public/community use

### Option B: Monorepo (Recommended for Internal/Private Packages)

**Pros:**
- ✅ Single source of truth
- ✅ Easier to keep client in sync with API changes
- ✅ Shared schemas and types
- ✅ Atomic commits across API and client

**Cons:**
- ❌ More complex CI/CD
- ❌ Versioning can be tricky
- ❌ Less common for public PyPI packages

**When to use:** Internal tools, private packages, or when tight coupling is desired

### Recommendation

**For PyPI publication:** Use a **separate repository** named `mett-dataportal-client` or `mett-dataportal-python`.

**Structure:**
```
mett-dataportal-client/
├── mett_dataportal/
│   ├── __init__.py
│   ├── client.py          # Main API client
│   ├── models/            # Pydantic models
│   ├── api/               # API endpoint modules
│   │   ├── genes.py
│   │   ├── genomes.py
│   │   ├── species.py
│   │   └── ...
│   └── cli/               # CLI commands
│       ├── __init__.py
│       └── commands.py
├── tests/
├── docs/
├── pyproject.toml
├── README.md
└── setup.py (optional, if not using pyproject.toml)
```

---

## 2. Code Generation Approaches

### Approach 1: OpenAPI Generator / Swagger Codegen (Recommended for Large APIs)

**Tools:**
- [openapi-generator](https://openapi-generator.tech/) (actively maintained, recommended)
- [swagger-codegen](https://swagger.io/tools/swagger-codegen/) (legacy, less maintained)

**How it works:**
1. Export OpenAPI schema from Django Ninja (`/api/openapi.json`)
2. Generate Python client using openapi-generator
3. Customize generated code for CLI and additional features

**Pros:**
- ✅ Automatically generates client from OpenAPI spec
- ✅ Stays in sync with API changes
- ✅ Type-safe models
- ✅ Handles authentication, error handling
- ✅ Industry standard approach

**Cons:**
- ❌ Generated code can be verbose
- ❌ May need customization for CLI
- ❌ Requires maintaining OpenAPI spec accuracy

**Implementation Steps:**

```bash
# 1. Install openapi-generator
brew install openapi-generator  # macOS
# or
npm install -g @openapi-generator/cli

# 2. Export OpenAPI schema from your API
curl http://localhost:8000/api/openapi.json > openapi.json

# 3. Generate Python client
openapi-generator generate \
  -i openapi.json \
  -g python \
  -o ./mett-dataportal-client \
  --package-name mett_dataportal \
  --additional-properties=packageVersion={version}

# 4. Customize for CLI and add features
```

**Customization needed:**
- Add CLI wrapper using `click` or `argparse`
- Add convenience methods
- Add retry logic, rate limiting
- Add better error messages

### Approach 2: Manual Implementation (Recommended for Control)

**Pros:**
- ✅ Full control over API and design
- ✅ Can optimize for specific use cases
- ✅ Cleaner, more Pythonic code
- ✅ Easier to add CLI-specific features
- ✅ Better documentation

**Cons:**
- ❌ More initial development time
- ❌ Manual updates when API changes
- ❌ Need to maintain models manually

**When to use:** When you want full control, have a well-defined API, or need custom features

**Implementation Structure:**

```python
# mett_dataportal/client.py
import requests
from typing import Optional, Dict, Any
from mett_dataportal.models import Genome, Gene, Species

class DataPortalClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})

    def get_genomes(self, **params) -> List[Genome]:
        response = self.session.get(f'{self.base_url}/api/genomes/', params=params)
        response.raise_for_status()
        return [Genome(**item) for item in response.json()['results']]

    # ... more methods
```

### Approach 3: Hybrid (Recommended Best Practice)

**Strategy:**
1. Use OpenAPI generator to create base models and API structure
2. Manually create a high-level client wrapper
3. Add CLI layer on top

**Benefits:**
- ✅ Auto-generated models stay in sync
- ✅ Custom client provides better UX
- ✅ CLI can use both layers

---

## 3. Recommended Stack

### Core Dependencies

```toml
[project]
name = "mett-dataportal"
version = "0.1.1"  # Update this value - it's the single source of truth
description = "Python client and CLI for METT Data Portal API"
requires-python = ">=3.10"

dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",        # For models (if not using generated)
    "click>=8.0.0",           # For CLI
    "rich>=13.0.0",           # For beautiful CLI output
    "typer>=0.9.0",           # Alternative to click (modern, type-safe)
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov",
    "black",
    "ruff",
    "mypy",
]
```

### CLI Framework Options

1. **Click** (Traditional, widely used)
   ```python
   import click

   @click.group()
   def cli():
       pass

   @cli.command()
   @click.option('--genome-id', required=True)
   def get_genome(genome_id):
       client = DataPortalClient()
       genome = client.get_genome(genome_id)
       click.echo(genome)
   ```

2. **Typer** (Modern, type-safe, recommended)
   ```python
   import typer

   app = typer.Typer()

   @app.command()
   def get_genome(genome_id: str):
       client = DataPortalClient()
       genome = client.get_genome(genome_id)
       typer.echo(genome)
   ```

3. **Rich + Click/Typer** (Beautiful output)
   ```python
   from rich.console import Console
   from rich.table import Table

   console = Console()
   table = Table()
   # Add columns and rows
   console.print(table)
   ```

---

## 4. Project Structure (Recommended)

```
mett-dataportal-client/
├── mett_dataportal/
│   ├── __init__.py                 # Package exports
│   ├── client.py                   # Main API client
│   ├── config.py                   # Configuration management
│   ├── exceptions.py               # Custom exceptions
│   ├── models/                     # Data models
│   │   ├── __init__.py
│   │   ├── genome.py
│   │   ├── gene.py
│   │   └── species.py
│   ├── api/                        # API endpoint modules
│   │   ├── __init__.py
│   │   ├── base.py                 # Base API class
│   │   ├── genes.py
│   │   ├── genomes.py
│   │   └── species.py
│   └── cli/                        # CLI commands
│       ├── __init__.py
│       ├── main.py                 # CLI entry point
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── genomes.py
│       │   ├── genes.py
│       │   └── species.py
│       └── utils.py                # CLI utilities
├── tests/
│   ├── test_client.py
│   ├── test_cli.py
│   └── fixtures/
├── docs/
│   ├── cli.md
│   └── api.md
├── pyproject.toml
├── README.md
├── LICENSE
└── .github/
    └── workflows/
        ├── ci.yml
        └── publish.yml
```

---

## 5. Implementation Example

### Client Implementation

```python
# mett_dataportal/client.py
from typing import Optional, List, Dict, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from mett_dataportal.models import Genome, Gene, Species
from mett_dataportal.exceptions import APIError, AuthenticationError

class DataPortalClient:
    """Main client for METT Data Portal API."""

    def __init__(
        self,
        base_url: str = "http://www.gut-microbes.org",
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout

        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })

        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}'
            })

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling."""
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            raise APIError(f"API request failed: {e}")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {e}")

    def get_genomes(
        self,
        query: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
        **kwargs
    ) -> List[Genome]:
        """Get genomes with optional filtering."""
        params = {
            'query': query,
            'page': page,
            'per_page': per_page,
            **kwargs
        }
        params = {k: v for k, v in params.items() if v is not None}

        response = self._request('GET', '/api/genomes/', params=params)
        return [Genome(**item) for item in response.get('results', [])]

    def get_genome(self, isolate_name: str) -> Genome:
        """Get a specific genome by isolate name."""
        genomes = self.get_genomes(query=isolate_name, per_page=1)
        if not genomes:
            raise APIError(f"Genome not found: {isolate_name}")
        return genomes[0]

    # ... more methods
```

### CLI Implementation

```python
# mett_dataportal/cli/main.py
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table

from mett_dataportal.client import DataPortalClient
from mett_dataportal.config import get_config

app = typer.Typer(help="METT Data Portal CLI")
console = Console()

@app.command()
def genomes(
    query: Optional[str] = typer.Option(None, "--query", "-q", help="Search query"),
    page: int = typer.Option(1, "--page", "-p", help="Page number"),
    per_page: int = typer.Option(20, "--per-page", help="Results per page"),
    output: str = typer.Option("table", "--output", "-o", help="Output format: table, json, csv"),
):
    """List genomes."""
    config = get_config()
    client = DataPortalClient(
        base_url=config.base_url,
        api_key=config.api_key,
    )

    genomes = client.get_genomes(query=query, page=page, per_page=per_page)

    if output == "json":
        import json
        console.print(json.dumps([g.dict() for g in genomes], indent=2))
    elif output == "csv":
        # CSV output
        pass
    else:
        # Table output
        table = Table(title="Genomes")
        table.add_column("Isolate Name")
        table.add_column("Species")
        table.add_column("Type Strain")

        for genome in genomes:
            table.add_row(
                genome.isolate_name,
                genome.species_scientific_name,
                "Yes" if genome.type_strain else "No"
            )
        console.print(table)

@app.command()
def genome(
    isolate_name: str = typer.Argument(..., help="Isolate name"),
):
    """Get details for a specific genome."""
    config = get_config()
    client = DataPortalClient(
        base_url=config.base_url,
        api_key=config.api_key,
    )

    genome = client.get_genome(isolate_name)
    console.print(genome)

if __name__ == "__main__":
    app()
```

### Configuration

```python
# mett_dataportal/config.py
import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

@dataclass
class Config:
    base_url: str = "http://www.gut-microbes.org"
    api_key: Optional[str] = None

def get_config() -> Config:
    """Load configuration from environment or config file."""
    # Check environment variables
    api_key = os.getenv("METT_API_KEY")
    base_url = os.getenv("METT_BASE_URL", "http://www.gut-microbes.org")

    # Check config file (~/.mett/config.toml)
    config_path = Path.home() / ".mett" / "config.toml"
    if config_path.exists():
        # Load from file
        import tomli
        with open(config_path, "rb") as f:
            config_data = tomli.load(f)
            api_key = api_key or config_data.get("api_key")
            base_url = config_data.get("base_url", base_url)

    return Config(base_url=base_url, api_key=api_key)
```

---

## 6. PyPI Publishing

### Setup for PyPI

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "mett-dataportal"
version = "0.1.1"  # Update this value - it's the single source of truth
description = "Python client and CLI for METT Data Portal API"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["genomics", "microbiome", "api", "cli"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
    "typer>=0.9.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov",
    "black",
    "ruff",
    "mypy",
]

[project.scripts]
mett = "mett_dataportal.cli.main:app"

[tool.setuptools]
packages = ["mett_dataportal"]

[tool.setuptools.package-data]
"*" = ["*.json", "*.yaml"]
```

### Publishing Steps

```bash
# 1. Install build tools
pip install build twine

# 2. Build package
python -m build

# 3. Test on TestPyPI
twine upload --repository testpypi dist/*

# 4. Install from TestPyPI to test
pip install --index-url https://test.pypi.org/simple/ mett-dataportal

# 5. Publish to PyPI
twine upload dist/*

# 6. Verify installation
pip install mett-dataportal
mett --help
```

### GitHub Actions for Auto-Publishing

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install build twine
      - name: Build package
        run: python -m build
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

---

## 7. Keeping Client in Sync with API

### Option 1: Automated Sync (Recommended)

Create a GitHub Action that:
1. Fetches OpenAPI schema from API
2. Generates/updates client code
3. Creates PR if changes detected

```yaml
# .github/workflows/sync-api.yml
name: Sync API Schema

on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Fetch OpenAPI schema
        run: |
          curl http://www.gut-microbes.org/api/openapi.json > openapi.json
      - name: Generate client
        run: |
          # Run code generation
      - name: Create PR
        # Create PR if changes
```

### Option 2: Manual Sync

Document the process in README:
1. Export schema: `curl http://www.gut-microbes.org/api/openapi.json > openapi.json`
2. Regenerate client
3. Test and commit

---

## 8. Recommended Approach Summary

### For Your Use Case:

1. **Repository:** Separate repository (`mett-dataportal-client`)
2. **Code Generation:** Hybrid approach
   - Use OpenAPI generator for base models
   - Manual high-level client wrapper
   - Manual CLI layer
3. **CLI Framework:** Typer (modern, type-safe)
4. **Output:** Rich for beautiful tables
5. **Publishing:** PyPI with GitHub Actions automation

### Next Steps:

1. Create new repository `mett-dataportal-client`
2. Export OpenAPI schema from your API
3. Set up project structure
4. Generate base models using openapi-generator
5. Implement high-level client
6. Implement CLI with Typer
7. Add tests
8. Set up CI/CD
9. Publish to PyPI

---

## 9. Example Usage

### Python Package Usage

```python
from mett_dataportal import DataPortalClient

client = DataPortalClient(
    base_url="http://www.gut-microbes.org",
    api_key="your-api-key"
)

# Get genomes
genomes = client.get_genomes(query="Bacteroides", per_page=10)
for genome in genomes:
    print(f"{genome.isolate_name}: {genome.species_scientific_name}")

# Get specific genome
genome = client.get_genome("BU_ATCC8492")
print(genome)
```

### CLI Usage

```bash
# Install
pip install mett-dataportal

# List genomes
mett genomes --query "Bacteroides" --per-page 10

# Get specific genome
mett genome BU_ATCC8492

# JSON output
mett genomes --output json

# In data pipeline
mett genomes --query "PV" --output csv > genomes.csv
```

---

## 10. Additional Considerations

### Authentication
- Support API keys via environment variable or config file
- Support JWT tokens if needed
- Document authentication clearly

### Error Handling
- Custom exceptions for different error types
- Retry logic for transient failures
- Rate limiting awareness

### Documentation
- Comprehensive README
- API documentation (Sphinx or MkDocs)
- CLI help text
- Examples and tutorials

### Testing
- Unit tests for client
- Integration tests against test API
- CLI tests
- Mock API responses

### Versioning
- Follow semantic versioning
- Keep client version independent of API version
- Document API version compatibility

---

## References

- [OpenAPI Generator](https://openapi-generator.tech/)
- [Typer Documentation](https://typer.tiangolo.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Publishing Guide](https://packaging.python.org/guides/distributing-packages-using-setuptools/)
