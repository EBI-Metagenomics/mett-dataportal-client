# CLI Recipes

Common workflows and examples for using the METT CLI.

## Basic Workflows

### Search Genomes

```bash
# Search by query
mett genomes search --query "Bacteroides" --format json

# Search by species
mett genomes search --query "ATCC" --species BU --format json

# Get specific genomes by isolate names
mett genomes by-isolates --isolate BU_909 --isolate BU_61 --format json

# Get type strains
mett genomes type-strains --format json
```

### Fetch Genes

```bash
# Search genes by name
mett genes search --query "dnaA" --format json

# Get gene by locus tag
mett genes get BU_ATCC8492_00001 --format json

# Advanced search with filters
mett genes search-advanced --species BU --query "dna" --filter "essentiality:essential" --format json

# Get genes for a genome
mett genomes genes BU_909 --format json
```

### Download Results

```bash
# Download all genomes as TSV
mett genomes download > genomes.tsv

# Export search results as JSON
mett genomes search --query "PV" --format json > results.json

# Export as TSV for analysis
mett genes search --query "dnaA" --format tsv > genes.tsv
```

## Experimental Data Workflows

### Drug Data (Requires Authentication)

```bash
# Set authentication token
export METT_JWT="your-token-here"

# Search drug MIC values
mett drugs mic --drug-name "amoxicillin" --species BU --format json

# Get drug MIC by drug class
mett drugs mic-by-class beta_lactam --species BU --format json

# Search drug metabolism
mett drugs metabolism-search --query "amoxapine" --format json

# Get drug data for a specific genome
mett genomes drug-data BU_ATCC8492 --format json
```

### Protein-Protein Interactions (Requires Authentication)

```bash
# Search PPI interactions for a gene
mett ppi interactions --locus-tag BU_ATCC8492_01788 --species BU --format json

# Get neighbors
mett ppi neighbors --locus-tag BU_ATCC8492_01788 --species BU --format json

# Search with score filters
mett ppi interactions --species BU --score-type ds_score --score-threshold 0.8 --format json
```

### Gene Essentiality (Requires Authentication)

```bash
# Search essential genes
mett essentiality search --essentiality-call essential --format json

# Get essentiality for a specific gene
mett genes essentiality BU_ATCC8492_00002 --format json

# Search with quality filters
mett essentiality search --min-tas-in-locus 25 --min-tas-hit 0.8 --format json
```

## Advanced Workflows

### Pagination

```bash
# Get first page
mett genomes list --page 1 --per-page 10 --format json

# Get second page
mett genomes list --page 2 --per-page 10 --format json
```

### Filtering and Sorting

```bash
# Search with multiple filters
mett genes search-advanced --species BU --filter "pfam:pf13715;essentiality:not_essential" --format json

# Sort results
mett genes search-advanced --sort-field locus_tag --sort-order asc --format json
```

### Combining Commands

```bash
# Get genomes for a species, then get genes for each
mett species genomes bu --format json | jq -r '.items[].isolate_name' | while read genome; do
  echo "Genes for $genome:"
  mett genomes genes "$genome" --format json | jq '.items | length'
done
```

## Output Format Examples

### JSON (for pipelines)

```bash
# Pipe to jq for filtering
mett genomes search --query "PV" --format json | jq '.items[].isolate_name'

# Save to file
mett genes search --query "dnaA" --format json > results.json
```

### TSV (for analysis)

```bash
# Export to TSV for spreadsheet analysis
mett genomes search --query "Bacteroides" --format tsv > genomes.tsv

# Import into Python/R
# pandas.read_csv('genomes.tsv', sep='\t')
```

### Table (default, human-readable)

```bash
# Pretty formatted output
mett genomes search --query "PV"

# No --format needed, table is default
mett species list
```

## Using the Generic API Command

For endpoints without dedicated commands:

```bash
# Health check
mett api request GET /api/health --format json

# Custom endpoint with query parameters
mett api request GET /api/genomes/autocomplete \
  --format json \
  --query query=bu \
  --query limit=5

# POST request with JSON body
mett api request POST /api/pyhmmer/search \
  --format json \
  --header content-type:application/json \
  --body '{"database": "bu_all", "input": ">test\nMSEIDHVGLWNRCLEIIRDNVPEQTYKTWFLPIIPLKYEDKTLV"}'
```

## See Also

- **[CLI Overview](overview.md)** - Introduction to the CLI
- **[Command Reference](commands.md)** - Complete command list
- **[Configuration](../config/configuration.md)** - Authentication setup
