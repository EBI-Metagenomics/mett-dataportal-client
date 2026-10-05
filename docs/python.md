# Python API

High-level client for the METT Data Portal (`mett_client.DataPortalClient`).

## Install

```bash
pip install mett
```

## Quick start

```python
from mett_client import DataPortalClient

client = DataPortalClient()

species = client.list_species()
print(f"Found {len(species)} species")

result = client.search_genomes(query="Bacteroides", per_page=5)
print(f"Found {len(result.items)} genomes")
```

### With authentication / release pinning

```python
client = DataPortalClient(jwt_token="your-token", release="v1")
result = client.search_drug_mic(drug_name="amoxicillin", species_acronym="BU")
```

## Core methods

### Species and genomes

```python
species = client.list_species()
result = client.species_genomes("BU", per_page=10)
result = client.list_genomes(page=1, per_page=10)
result = client.search_genomes(query="Bacteroides", per_page=5)
result = client.get_genome_genes("BU_909")
history = client.get_genome_release_history("BU_ATCC8492")
```

### Genes

```python
result = client.search_genes(query="dnaA")
result = client.search_genes_advanced(
    query="dnaA",
    species_acronym="BU",
    filter="essentiality:essential",
)
gene = client.get_gene("BU_ATCC8492_00001")
print(gene.product)

releases = client.list_releases()
gene_history = client.get_gene_release_history("BU_ATCC8492_00001")
```

### Experimental / interactions (JWT)

```python
client = DataPortalClient(jwt_token="your-token")

client.search_drug_mic(drug_name="amoxicillin", species_acronym="BU")
client.search_proteomics(locus_tags=["BU_ATCC8492_00002"])
client.search_essentiality(essentiality_call="essential")
client.search_fitness(max_fdr=0.05, min_lfc=2.0)
client.search_ppi(locus_tag="BU_ATCC8492_01788", species_acronym="BU")
client.get_ppi_interaction("bu:A0A0X1ABC1__B0ABC123")
```

## Pagination

Most search helpers return `PaginatedResult`:

```python
result = client.search_genomes(query="Bacteroides", page=1, per_page=10)

print(len(result.items))
if result.pagination:
    print(result.pagination.page, result.pagination.total_pages)
    print(result.pagination.total, result.pagination.has_next)
```

Walk all pages:

```python
page = 1
all_items = []
while True:
    result = client.search_genomes(query="Bacteroides", page=page, per_page=20)
    all_items.extend(result.items)
    if not result.pagination or not result.pagination.has_next:
        break
    page += 1
```

## Errors

```python
from mett_client import DataPortalClient
from mett_client.exceptions import APIError, AuthenticationError, ConfigurationError

client = DataPortalClient()
try:
    client.search_genomes(query="test")
except AuthenticationError as e:
    print("auth:", e)
except APIError as e:
    print(f"api ({e.status_code}):", e)
except ConfigurationError as e:
    print("config:", e)
```

## Configuration

Environment variables (`METT_BASE_URL`, `METT_JWT`, `METT_RELEASE`, …) and `~/.mett/config.toml` are loaded automatically. See [Configuration](config.md).

```python
from mett_client import DataPortalClient, Config

client = DataPortalClient(
    config=Config(base_url="http://www.gut-microbes.org", timeout=60, release="current")
)
```

## See also

- [CLI Guide](cli.md)
- [Examples](examples.md)
- [API Reference](reference/api-reference.qmd) (generated from OpenAPI)
