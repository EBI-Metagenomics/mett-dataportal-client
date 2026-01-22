# Usage Guide

This guide provides detailed examples for using the METT Data Portal client via CLI and Python API.

## Table of Contents

- [CLI Usage](#cli-usage)
- [Python API](#python-api)
- [Output Formats](#output-formats)
- [Examples by Category](#examples-by-category)

## CLI Usage

### Basic Commands

```bash
# Get help
mett --help
mett species --help
mett genomes search --help

# List all available commands
mett --help
```

### Output Formats

The CLI supports three output formats:

- **Table** (default): Formatted table with Rich
- **JSON**: Raw JSON output for pipelines
- **TSV**: Tab-separated values for bulk export

```bash
# Table format (default)
mett genomes search --query "PV"

# JSON format
mett genomes search --query "PV" --format json | jq '.'

# TSV format
mett genomes search --query "PV" --format tsv > genomes.tsv
```

## Python API

### Basic Usage

```python
from mett_client import DataPortalClient

# Initialize client
client = DataPortalClient()

# Or with authentication
client = DataPortalClient(jwt_token="your-token")

# Or with custom configuration
client = DataPortalClient(
    base_url="https://www.gut-microbes.org",
    jwt_token="your-token",
    timeout=60
)
```

### Working with Results

```python
from mett_client import DataPortalClient

client = DataPortalClient()

# Paginated results
result = client.search_genomes(query="Bacteroides", per_page=10)
print(f"Total items: {len(result.items)}")
print(f"Page: {result.pagination.page if result.pagination else 'N/A'}")

# Iterate through results
for genome in result.items:
    print(genome.isolate_name)

# Access raw response
raw_data = result.raw
```

## Examples by Category

### Core APIs

#### Species

```bash
# List all species
mett species list
mett species list --format json

# Get genomes by species
mett species genomes bu
mett species genomes bu --query "ATCC" --page 1

# Search genomes by species
mett species genomes bu --query "BU_ATCC" --page 1
```

```python
# Python API
client = DataPortalClient()

# List species
species = client.list_species()
for s in species:
    print(s.species_acronym, s.species_scientific_name)

# Get genomes by species
result = client.species_genomes("BU", per_page=10)
```

#### Genomes

```bash
# List all genomes
mett genomes list --page 1 --per-page 10

# Search genomes
mett genomes search --query "Bacteroides"
mett genomes search --query "PV_H4" --format json

# Get type strains
mett genomes type-strains

# Get genomes by isolate names
mett genomes by-isolates --isolate BU_909 --isolate BU_61

# Autocomplete
mett genomes autocomplete --query cc --limit 5

# Download all genomes (TSV)
mett genomes download > genomes.tsv

# Get genes for a genome
mett genomes genes BU_909
```

```python
# Python API
client = DataPortalClient()

# List genomes
result = client.list_genomes(page=1, per_page=10)

# Search genomes
result = client.search_genomes(query="Bacteroides", per_page=5)

# Get genes for a genome
result = client.get_genome_genes("BU_909")
```

#### Genes

```bash
# List all genes
mett genes list --page 1 --per-page 10

# Search genes
mett genes search --query "dnaA"

# Advanced search
mett genes search-advanced --query "dnaA" --species BU

# Get gene by locus tag
mett genes get BU_ATCC8492_00001

# Autocomplete
mett genes autocomplete --species BU --query "dnaA"

# Faceted search
mett genes faceted-search --species BU --limit 10 --pfam PF07660

# Get protein sequence
mett genes protein BU_2243B_00003
```

```python
# Python API
client = DataPortalClient()

# Search genes
result = client.search_genes(query="dnaA")

# Advanced search
result = client.search_genes_advanced(query="dnaA", species_acronym="BU")

# Get gene
gene = client.get_gene("BU_ATCC8492_00001")
print(gene.locus_tag, gene.product)
```

### Experimental APIs

#### Drugs

```bash
# Search drug MIC
mett drugs mic --drug-name "amoxicillin" --species BU
mett drugs mic --drug-name "amoxicillin" --species BU \
  --min-mic-value 150.0 --max-mic-value 160.0

# Get MIC by drug name
mett drugs mic-by-drug azithromycin
mett drugs mic-by-drug azithromycin --species BU

# Get MIC by drug class
mett drugs mic-by-class beta_lactam
mett drugs mic-by-class beta_lactam --species BU

# Search drug metabolism
mett drugs metabolism-search --query "amoxapine"
mett drugs metabolism-search --min-degr-percent 50.0 --species BU

# Get metabolism by drug
mett drugs metabolism-by-drug amoxapine
mett drugs metabolism-by-drug amoxapine --species BU

# Get metabolism by class
mett drugs metabolism-by-class beta_lactam
```

```python
# Python API
client = DataPortalClient(jwt_token="your-token")

# Search drug MIC
result = client.search_drug_mic(
    drug_name="amoxicillin",
    species_acronym="BU",
    min_mic_value=150.0,
    max_mic_value=160.0
)

# Search drug metabolism
result = client.search_drug_metabolism(query="amoxapine")
```

#### Proteomics

```bash
# Search proteomics
mett proteomics search --locus-tag BU_ATCC8492_00002
mett proteomics search --locus-tag BU_ATCC8492_00002 \
  --min-coverage 50 --min-unique-peptides 10

# Get proteomics by gene
mett genes proteomics BU_ATCC8492_00002
```

```python
# Python API
client = DataPortalClient(jwt_token="your-token")

# Search proteomics
result = client.search_proteomics(locus_tags=["BU_ATCC8492_00002"])
```

#### Essentiality

```bash
# Search essentiality
mett essentiality search --essentiality-call essential
mett essentiality search --locus-tag BU_ATCC8492_00002

# Get essentiality by gene
mett genes essentiality BU_ATCC8492_00002
```

```python
# Python API
client = DataPortalClient(jwt_token="your-token")

# Search essentiality
result = client.search_essentiality(essentiality_call="essential")

# Get essentiality by gene (via genomes endpoint)
# See API reference for details
```

#### Fitness

```bash
# Search fitness data
mett fitness search --max-fdr 0.05 --min-lfc 2.0
mett fitness search --locus-tag BU_ATCC8492_00002

# Get fitness by gene
mett genes fitness BU_ATCC8492_00002
```

```python
# Python API
client = DataPortalClient(jwt_token="your-token")

# Search fitness
result = client.search_fitness(max_fdr=0.05, min_lfc=2.0)
```

### Interactions

#### Protein-Protein Interactions (PPI)

```bash
# Search PPI interactions
mett ppi interactions --locus-tag BU_ATCC8492_01788 --species BU
mett ppi interactions --species BU --score-type ds_score --score-threshold 0.8

# Get neighbors
mett ppi neighbors --locus-tag BU_ATCC8492_01788 --species BU

# Get network
mett ppi network ds_score --score-threshold 0.8 --species PV

# Get available score types
mett ppi scores-available
```

```python
# Python API
client = DataPortalClient(jwt_token="your-token")

# Search PPI
result = client.search_ppi(
    locus_tag="BU_ATCC8492_01788",
    species_acronym="BU"
)

# Get neighbors
result = client.get_ppi_neighbors(
    locus_tag="BU_ATCC8492_01788",
    species_acronym="BU"
)
```

#### TTP Interactions

```bash
# Search TTP interactions
mett ttp search --query BU_ATCC8492
mett ttp search --query myo-inositol

# Get gene interactions
mett ttp gene-interactions PV_ATCC8482_00051

# Get compound interactions
mett ttp compound-interactions myo-inositol

# Get metadata
mett ttp metadata
```

```python
# Python API
client = DataPortalClient(jwt_token="your-token")

# Search TTP
result = client.search_ttp(query="BU_ATCC8492")

# Get gene interactions
result = client.get_ttp_gene_interactions("PV_ATCC8482_00051")
```

### Raw API Access

For endpoints without dedicated commands:

```bash
# Health check
mett api request GET /api/health --format json

# Autocomplete
mett api request GET /api/genomes/autocomplete \
  --format json \
  --query query=bu \
  --query limit=5

# POST request
mett api request POST /api/pyhmmer/search \
  --format json \
  --header content-type:application/json \
  --body @request.json
```

## Advanced Usage

### Pagination

```python
from mett_client import DataPortalClient

client = DataPortalClient()

# Iterate through all pages
page = 1
while True:
    result = client.search_genomes(query="Bacteroides", page=page, per_page=20)

    for genome in result.items:
        print(genome.isolate_name)

    if not result.pagination or not result.pagination.has_next:
        break

    page += 1
```

### Error Handling

```python
from mett_client import DataPortalClient
from mett_client.exceptions import APIError, AuthenticationError

client = DataPortalClient()

try:
    result = client.search_genomes(query="test")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except APIError as e:
    print(f"API error ({e.status_code}): {e}")
```

### Custom Configuration

```python
from mett_client import DataPortalClient, Config

# Create custom config
config = Config(
    base_url="https://custom-api.example.com",
    jwt_token="your-token",
    timeout=120,
    verify_ssl=False
)

client = DataPortalClient(config=config)
```

## See Also

- [API Reference](../reference/api-reference.qmd) - Complete API documentation
- [Configuration Guide](CONFIGURATION.md) - Authentication and configuration
