# CLI Command Reference

Complete reference for all METT CLI commands.

## Core Commands

### Species

```bash
# List all species
mett species list [--format json|tsv|table]

# Get genomes for a species
mett species genomes <species_acronym> [--query <query>] [--page <n>] [--per-page <n>]

# Search genomes by species
mett species genomes <species_acronym> --query <query> [--page <n>]
```

### Genomes

```bash
# List all genomes
mett genomes list [--page <n>] [--per-page <n>] [--format json|tsv|table]

# Search genomes
mett genomes search [--query <query>] [--species <acronym>] [--page <n>] [--per-page <n>]

# Get type strains
mett genomes type-strains [--format json|tsv|table]

# Get genomes by isolate names
mett genomes by-isolates --isolate <name> [--isolate <name> ...]

# Autocomplete
mett genomes autocomplete --query <query> [--species <acronym>] [--limit <n>]

# Download all genomes (TSV)
mett genomes download

# Get genes for a genome
mett genomes genes <genome_id> [--format json|tsv|table]

# Get essentiality for a genome contig
mett genomes essentiality <genome_id> <contig_id> [--format json]
```

### Genes

```bash
# List all genes
mett genes list [--page <n>] [--per-page <n>] [--format json|tsv|table]

# Search genes
mett genes search --query <query> [--format json|tsv|table]

# Advanced search
mett genes search-advanced [--query <query>] [--species <acronym>] [--isolate <name> ...] [--filter <filter>] [--sort-field <field>] [--sort-order asc|desc]

# Get gene by locus tag
mett genes get <locus_tag> [--format json]

# Autocomplete
mett genes autocomplete --query <query> [--species <acronym>] [--isolate <name> ...] [--filter <filter>]

# Faceted search
mett genes faceted-search [--species <acronym>] [--limit <n>] [--interpro <id>] [--pfam <id>]

# Get protein sequence
mett genes protein <locus_tag> [--format json]
```

### System

```bash
# Health check
mett system health [--format json]

# Get features
mett system features [--format json]

# Get COG categories
mett system cog-categories [--format json]
```

## Experimental Commands

### Drugs

```bash
# Search drug MIC
mett drugs mic [--drug-name <name>] [--drug-class <class>] [--species <acronym>] [--min-mic-value <n>] [--max-mic-value <n>] [--page <n>] [--per-page <n>] [--sort-by <field>] [--sort-order asc|desc]

# Get MIC by drug name
mett drugs mic-by-drug <drug_name> [--species <acronym>] [--format json]

# Get MIC by drug class
mett drugs mic-by-class <drug_class> [--species <acronym>] [--page <n>] [--per-page <n>]

# Search drug metabolism
mett drugs metabolism-search [--query <query>] [--drug-class <class>] [--species <acronym>] [--is-significant <true|false>] [--min-degr-percent <n>] [--page <n>] [--per-page <n>]

# Get metabolism by drug
mett drugs metabolism-by-drug <drug_name> [--species <acronym>] [--format json]

# Get metabolism by class
mett drugs metabolism-by-class <drug_class> [--species <acronym>] [--page <n>] [--per-page <n>]

# Get drug data for a genome
mett genomes drug-data <genome_id> [--format json]

# Get drug MIC for a genome
mett genomes drug-mic <genome_id> [--format json]

# Get drug metabolism for a genome
mett genomes drug-metabolism <genome_id> [--format json]
```

### Proteomics

```bash
# Search proteomics
mett proteomics search [--locus-tag <tag> ...] [--uniprot <id> ...] [--min-coverage <n>] [--min-unique-peptides <n>] [--has-evidence <true|false>] [--format json]

# Get proteomics by gene
mett genes proteomics <locus_tag> [--format json]
```

### Essentiality

```bash
# Search essentiality
mett essentiality search [--locus-tag <tag> ...] [--uniprot <id> ...] [--essentiality-call <call>] [--condition <condition>] [--min-tas-in-locus <n>] [--min-tas-hit <n>] [--format json]

# Get essentiality by gene
mett genes essentiality <locus_tag> [--format json]
```

### Fitness

```bash
# Search fitness data
mett fitness search [--locus-tag <tag> ...] [--contrast <contrast>] [--min-barcodes <n>] [--max-fdr <n>] [--min-lfc <n>] [--format json]

# Get fitness by gene
mett genes fitness <locus_tag> [--format json]
```

### Reactions

```bash
# Search reactions
mett reactions search [--locus-tag <tag> ...] [--uniprot <id> ...] [--reaction-id <id>] [--substrate <id>] [--product <id>] [--format json]

# Get reactions by gene
mett genes reactions <locus_tag> [--format json]
```

### Operons

```bash
# Search operons
mett operons search [--species <acronym>] [--min-gene-count <n>] [--has-tss <true|false>] [--has-terminator <true|false>] [--format json]

# Get operon statistics
mett operons get statistics --species <acronym> [--format json]

# Get operon by ID
mett operons get <operon_id> [--format json]

# Get operons for a gene
mett genes operons <locus_tag> [--format json]
```

### Orthologs

```bash
# Check if two genes are orthologs
mett orthologs pair --locus-tag-a <tag> --locus-tag-b <tag> [--format json]

# Get orthologs for a gene
mett genes orthologs <locus_tag> [--one-to-one-only <true|false>] [--format json]
```

### Mutant Growth

```bash
# Search mutant growth data
mett mutant-growth search [--locus-tag <tag> ...] [--exclude-double-picked <true|false>] [--media <media>] [--max-doubling-time <n>] [--format json]

# Get mutant growth by gene
mett genes mutant-growth <locus_tag> [--format json]
```

### Fitness Correlations

```bash
# Search fitness correlations
mett fitness-correlations search [--query <query>] [--format json]

# Get correlation between two genes
mett fitness-correlations correlation --locus-tag-a <tag> --locus-tag-b <tag> [--format json]

# Get correlations for a gene
mett genes correlations <locus_tag> [--format json]
```

## Interaction Commands

### Protein-Protein Interactions (PPI)

```bash
# Search PPI interactions
mett ppi interactions [--locus-tag <tag>] [--protein-id <id>] [--species <acronym>] [--score-type <type>] [--score-threshold <n>] [--has-string <true|false>] [--has-xlms <true|false>] [--page <n>] [--per-page <n>] [--format json]

# Get neighbors
mett ppi neighbors [--locus-tag <tag>] [--protein-id <id>] [--species <acronym>] [--n <n>] [--format json]

# Get neighborhood
mett ppi neighborhood [--locus-tag <tag>] [--protein-id <id>] [--species <acronym>] [--n <n>] [--format json]

# Get network
mett ppi network <score_type> [--score-threshold <n>] [--species <acronym>] [--include-properties <true|false>] [--format json]

# Get network properties
mett ppi network-properties [--score-type <type>] [--score-threshold <n>] [--species <acronym>] [--format json]

# Get available score types
mett ppi scores-available [--format json]
```

### TTP Interactions

```bash
# Search TTP interactions
mett ttp search [--query <query>] [--format json]

# Get gene interactions
mett ttp gene-interactions <locus_tag> [--hit-calling <true|false>] [--format json]

# Get compound interactions
mett ttp compound-interactions <compound_name> [--format json]

# Get pools analysis
mett ttp pools-analysis --pool-a <pool> --pool-b <pool> [--format json]

# Get significant hits
mett ttp hits [--max-fdr <n>] [--min-ttp-score <n>] [--format json]

# Get metadata
mett ttp metadata [--format json]
```

## Utility Commands

### PyHMMER

```bash
# List databases
mett pyhmmer databases [--format json]

# Search
mett pyhmmer search [--format json]  # Requires JSON body via stdin or file

# Get result
mett pyhmmer result <job_id> [--format json]

# Get result domains
mett pyhmmer result-domains <job_id> --target <target> [--format json]

# Download result
mett pyhmmer result-download <job_id> --format <fasta|aligned_fasta|tab> [--format json]

# Debug commands
mett pyhmmer debug-task <task_id> [--format json]
mett pyhmmer debug-msa <job_id> [--format json]
mett pyhmmer debug-fasta <job_id> [--format json]
mett pyhmmer testtask [--format json]  # Requires JSON body
```

### Generic API Request

```bash
# GET request
mett api request GET <path> [--format json|tsv|table] [--query <key=value> ...] [--header <key:value> ...]

# POST request
mett api request POST <path> [--format json|tsv|table] [--query <key=value> ...] [--header <key:value> ...] [--body <json_string>] [--body-file <file>]

# PUT request
mett api request PUT <path> [--format json|tsv|table] [--query <key=value> ...] [--header <key:value> ...] [--body <json_string>] [--body-file <file>]

# DELETE request
mett api request DELETE <path> [--format json|tsv|table] [--query <key=value> ...] [--header <key:value> ...]
```

## Global Options

All commands support these global options:

```bash
--base-url <url>        # Override API base URL
--jwt <token>           # JWT token for authentication
--timeout <seconds>     # HTTP timeout
--verify-ssl <true|false>  # SSL verification
--format <json|tsv|table>  # Output format
--version              # Show version
--help                 # Show help
```

## See Also

- **[CLI Overview](overview.md)** - Introduction to the CLI
- **[Common Recipes](recipes.md)** - Workflow examples
- **[Configuration](../config/configuration.md)** - Authentication setup
