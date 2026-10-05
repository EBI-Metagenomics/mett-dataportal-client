# Examples

Curated examples for **endpoints present in `openapi.json`**. Hidden or internal routes (for example `/api/features`, `/api/health`, gene autocomplete) are omitted on purpose.

Environment:

```bash
export METT_BASE_URL="${METT_BASE_URL:-https://www.gut-microbes.org}"
# export METT_JWT=...          # for experimental / interactions
# export METT_RELEASE=v1       # optional release pin
```

## Core

### List releases

```bash
mett system releases --format json
mett api request GET /api/releases --format json
curl -X GET "${METT_BASE_URL}/api/releases"
```

### Species list

```bash
mett species list --format json
mett api request GET /api/species/ --format json
curl -X GET "${METT_BASE_URL}/api/species/"
```

### Search genomes

```bash
mett genomes search --query Bacteroides --per-page 5 --format json
mett api request GET /api/genomes/search --query query=Bacteroides --query per_page=5 --format json
curl -X GET "${METT_BASE_URL}/api/genomes/search?query=Bacteroides&per_page=5"
```

### Genome release history

```bash
mett genomes release-history BU_ATCC8492 --format json
mett api request GET /api/genomes/BU_ATCC8492/release-history --format json
curl -X GET "${METT_BASE_URL}/api/genomes/BU_ATCC8492/release-history"
```

### Get gene

```bash
mett genes get BU_ATCC8492_00001 --format json
mett api request GET /api/genes/BU_ATCC8492_00001 --format json
curl -X GET "${METT_BASE_URL}/api/genes/BU_ATCC8492_00001"
```

### Gene release history

```bash
mett genes release-history BU_ATCC8492_00001 --format json
mett api request GET /api/genes/BU_ATCC8492_00001/release-history --format json
curl -X GET "${METT_BASE_URL}/api/genes/BU_ATCC8492_00001/release-history"
```

## Experimental (JWT)

```bash
export METT_JWT="your-token"

mett drugs mic --drug-name amoxicillin --species BU --format json
curl -X GET "${METT_BASE_URL}/api/drugs/mic/search?drug_name=amoxicillin&species_acronym=BU" \
  -H "Authorization: Bearer ${METT_JWT}"

mett genes essentiality BU_ATCC8492_00002 --format json
curl -X GET "${METT_BASE_URL}/api/genes/BU_ATCC8492_00002/essentiality" \
  -H "Authorization: Bearer ${METT_JWT}"
```

## Interactions (JWT)

```bash
mett ppi interactions --locus-tag BU_ATCC8492_01788 --species BU --format json
mett ppi interaction 'bu:A0A0X1ABC1__B0ABC123' --format json
curl -X GET "${METT_BASE_URL}/api/ppi/interactions/bu:A0A0X1ABC1__B0ABC123" \
  -H "Authorization: Bearer ${METT_JWT}"
```

## More detail

- Working recipes: [CLI Guide](cli.md)
- Generated per-endpoint tabs: [API Reference](reference/api-reference.qmd) (`python scripts/generate-api-docs.py`)
- Schema: `openapi.json` at the repo root
