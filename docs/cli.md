# CLI Guide

Command-line interface for the METT Data Portal. Examples below cover **public OpenAPI endpoints** only. For the full HTTP contract, see [API Reference](reference/api-reference.qmd) or `openapi.json`.

## Install

```bash
pip install mett
# or, for local development (conda):
# conda activate mett-client && pip install -e ".[dev]"
```

## First command

```bash
mett species list
mett --help
mett genomes search --help
```

## Global options

```bash
mett --base-url <url> --jwt <token> --release <v1|current> \
  --timeout <seconds> --verify-ssl <true|false> \
  <group> <command> ...
```

Also: `METT_BASE_URL`, `METT_JWT`, `METT_RELEASE`, `METT_TIMEOUT`, `METT_VERIFY_SSL`. See [Configuration](config.md).

## Output formats

| Format | Flag | Use |
|--------|------|-----|
| Table | (default) | Human-readable |
| JSON | `--format json` | Pipelines / `jq` |
| TSV | `--format tsv` | Spreadsheets |

```bash
mett genomes search --query PV
mett genomes search --query PV --format json | jq '.'
mett genomes search --query PV --format tsv > genomes.tsv
```

## Command map

### Core

| Group | Commands |
|-------|----------|
| `mett species` | `list`, `genomes`, `search-genomes` |
| `mett genomes` | `list`, `search`, `type-strains`, `by-isolates`, `genes`, `release-history`, `essentiality`, `drug-mic`, `drug-metabolism`, `drug-data` |
| `mett genes` | `list`, `search`, `search-advanced`, `get`, `release-history`, plus gene-scoped experimental helpers (`proteomics`, `essentiality`, `fitness`, …) |
| `mett system` | `releases` |

### Experimental (JWT usually required)

`drugs`, `proteomics`, `essentiality`, `fitness`, `fitness-correlations`, `mutant-growth`, `reactions`, `operons`, `orthologs`

### Interactions

`ppi`, `ttp`

### Utilities

`pyhmmer` (search / result / domains / download), `api request` (any path)

## Recipes

### Genomes and genes

```bash
mett genomes search --query "BU" --format json
mett genomes search --query ATCC --species BU --format json
mett genomes by-isolates --isolate BU_909 --isolate BU_61 --format json
mett genomes type-strains --format json
mett genomes release-history BU_ATCC8492 --format json

mett genes search --query dnaA --format json
mett genes get BU_ATCC8492_00001 --format json
mett genes release-history BU_ATCC8492_00001 --format json
mett genes search-advanced --species BU --query dna --filter "essentiality:essential" --format json
mett genomes genes BU_909 --format json
```

### Releases

```bash
mett system releases --format json
mett --release v1 genomes search --query BU --format json
```

### Drugs / PPI (auth)

```bash
export METT_JWT="your-token"

mett drugs mic --drug-name amoxicillin --species BU --format json
mett drugs mic-by-drug amoxicillin --species BU --format json
mett drugs metabolism-search --query amoxapine --format json
mett genomes drug-data BU_ATCC8492 --format json

mett ppi interactions --locus-tag BU_ATCC8492_01788 --species BU --format json
mett ppi interaction 'bu:A0A0X1ABC1__B0ABC123' --format json
mett ppi neighbors --locus-tag BU_ATCC8492_01788 --species BU --format json
mett ppi scores --format json
```

### Essentiality

```bash
mett essentiality search --essentiality-call essential --format json
mett genes essentiality BU_ATCC8492_00002 --format json
```

### Generic HTTP (escape hatch)

```bash
mett api request GET /api/species/ --format json
mett api request GET /api/releases --format json
mett api request POST /api/pyhmmer/search \
  --format json \
  --header content-type:application/json \
  --body '{"database":"bu_all","input":">test\nMSEIDHVGLWNRCLEIIRDNVPEQTYKTWFLPIIPLKYEDKTLV"}'
```

## Command reference (public surface)

### Species

```bash
mett species list [--format json|tsv|table]
mett species genomes <species_acronym> [--query <q>] [--page <n>] [--per-page <n>]
mett species search-genomes <species_acronym> [--query <q>] ...
```

### Genomes

```bash
mett genomes list [--page <n>] [--per-page <n>] [--format ...]
mett genomes search [--query <q>] [--species <acronym>] [--page <n>] [--per-page <n>]
mett genomes type-strains [--format ...]
mett genomes by-isolates --isolate <name> [--isolate <name> ...]
mett genomes genes <isolate_name> [--filter <expr>] [--page <n>] ...
mett genomes release-history <isolate_name> [--format json]
mett genomes essentiality <isolate_name> <ref_name> [--format json]
mett genomes drug-mic|drug-metabolism|drug-data <isolate_name> ...
```

### Genes

```bash
mett genes list|search|search-advanced|get ...
mett genes release-history <locus_tag> [--format json]
mett genes proteomics|essentiality|fitness|mutant-growth|reactions|correlations|orthologs|operons <locus_tag> ...
```

### System

```bash
mett system releases [--format json]
```

### Drugs

```bash
mett drugs mic [...]
mett drugs mic-by-drug <drug_name> [--species <acronym>]
mett drugs metabolism-search [...]
mett drugs metabolism-by-drug <drug_name> [--species <acronym>]
```

### PPI

```bash
mett ppi scores|data-sources|string-network|interactions|interaction|neighbors|network|network-properties ...
```

### TTP

```bash
mett ttp metadata|search|gene-interactions|compound-interactions ...
```

### PyHMMER

```bash
mett pyhmmer search|result|domains|download ...
```

## See also

- [Examples](examples.md) — CLI + cURL side by side
- [Python API](python.md)
- [Configuration](config.md)
