# Python API Quickstart

Get started with the METT Data Portal Python client.

## Installation

```bash
pip install mett
```

## First Steps

### Basic Usage

```python
from mett_client import DataPortalClient

# Initialize client (uses default base URL: http://www.gut-microbes.org)
client = DataPortalClient()

# List all species
species = client.list_species()
print(f"Found {len(species)} species")

# Search genomes
result = client.search_genomes(query="Bacteroides", per_page=5)
print(f"Found {len(result.items)} genomes")
```

### With Authentication

```python
from mett_client import DataPortalClient

# Initialize with JWT token for experimental endpoints
client = DataPortalClient(jwt_token="your-token-here")

# Now you can access protected endpoints
result = client.search_drug_mic(drug_name="amoxicillin", species_acronym="BU")
```

## Core Objects

### DataPortalClient

The main client class for interacting with the API.

```python
from mett_client import DataPortalClient

client = DataPortalClient(
    base_url="http://www.gut-microbes.org",  # Optional, defaults to production
    jwt_token="your-token",                   # Optional, for protected endpoints
    timeout=60                                 # Optional, default 30 seconds
)
```

## Common Methods

### Species

```python
# List all species
species = client.list_species()
for s in species:
    print(f"{s.species_acronym}: {s.species_scientific_name}")

# Get genomes for a species
result = client.species_genomes("BU", per_page=10)
```

### Genomes

```python
# List genomes (paginated)
result = client.list_genomes(page=1, per_page=10)

# Search genomes
result = client.search_genomes(query="Bacteroides", per_page=5)

# Get genomes by isolate names
result = client.get_genomes_by_isolates(["BU_909", "BU_61"])

# Get genes for a genome
result = client.get_genome_genes("BU_909")
```

### Genes

```python
# Search genes
result = client.search_genes(query="dnaA")

# Advanced search
result = client.search_genes_advanced(
    query="dnaA",
    species_acronym="BU",
    filter="essentiality:essential"
)

# Get gene by locus tag
gene = client.get_gene("BU_ATCC8492_00001")
print(gene.product)
```

### Experimental Data (Requires Authentication)

```python
client = DataPortalClient(jwt_token="your-token")

# Drug MIC
result = client.search_drug_mic(
    drug_name="amoxicillin",
    species_acronym="BU",
    min_mic_value=35.0,
    max_mic_value=45.0
)

# Proteomics
result = client.search_proteomics(locus_tags=["BU_ATCC8492_00002"])

# Essentiality
result = client.search_essentiality(essentiality_call="essential")

# Fitness
result = client.search_fitness(max_fdr=0.05, min_lfc=2.0)

# PPI interactions
result = client.search_ppi(
    locus_tag="BU_ATCC8492_01788",
    species_acronym="BU"
)
```

## Working with Results

### Paginated Results

Most search methods return `PaginatedResult` objects:

```python
result = client.search_genomes(query="Bacteroides", per_page=10)

# Access items
for genome in result.items:
    print(genome.isolate_name)

# Access pagination metadata
if result.pagination:
    print(f"Page {result.pagination.page} of {result.pagination.total_pages}")
    print(f"Total items: {result.pagination.total}")
    print(f"Has next: {result.pagination.has_next}")
```

### Iterating Through Pages

```python
page = 1
while True:
    result = client.search_genomes(query="Bacteroides", page=page, per_page=20)

    for genome in result.items:
        print(genome.isolate_name)

    if not result.pagination or not result.pagination.has_next:
        break

    page += 1
```

## Error Handling

```python
from mett_client import DataPortalClient
from mett_client.exceptions import APIError, AuthenticationError, ConfigurationError

client = DataPortalClient()

try:
    result = client.search_genomes(query="test")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except APIError as e:
    print(f"API error ({e.status_code}): {e}")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

## Configuration

### Using Environment Variables

```python
import os
from mett_client import DataPortalClient

# Environment variables are automatically used
# METT_BASE_URL, METT_JWT, METT_TIMEOUT, METT_VERIFY_SSL
client = DataPortalClient()
```

### Using Config File

Create `~/.mett/config.toml`:

```toml
base_url = "http://www.gut-microbes.org"
jwt_token = "your-token-here"
timeout = 60
verify_ssl = true
```

The client automatically reads this file.

### Programmatic Configuration

```python
from mett_client import DataPortalClient, Config

config = Config(
    base_url="https://custom-api.example.com",
    jwt_token="your-token",
    timeout=120,
    verify_ssl=False
)

client = DataPortalClient(config=config)
```

## Next Steps

- **[Pagination Patterns](pagination.md)** - Advanced pagination techniques
- **[Configuration Guide](../config/configuration.md)** - Detailed configuration options
- **[Troubleshooting](../troubleshooting.md)** - Common issues and solutions
