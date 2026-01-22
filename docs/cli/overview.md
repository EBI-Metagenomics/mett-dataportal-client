# CLI Overview

The METT CLI provides a command-line interface for accessing the METT Data Portal API. It supports both "friendly" commands (like `mett species list`) and a generic API request command for any endpoint.

## Installation

```bash
pip install mett
```

## First Command

```bash
# List all species
mett species list
```

## Command Map

The CLI is organized into command groups:

### Core Commands
- `mett species` - Species operations
- `mett genomes` - Genome operations
- `mett genes` - Gene operations
- `mett system` - System health and metadata

### Experimental Commands
- `mett drugs` - Drug MIC and metabolism data
- `mett proteomics` - Proteomics data
- `mett essentiality` - Gene essentiality data
- `mett fitness` - Fitness data
- `mett reactions` - Metabolic reactions
- `mett operons` - Operon data
- `mett orthologs` - Ortholog relationships

### Interaction Commands
- `mett ppi` - Protein-protein interactions
- `mett ttp` - TTP (pooled) interactions

### Utility Commands
- `mett pyhmmer` - HMMER search operations
- `mett api` - Generic API request command

## Output Formats

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

## Getting Help

```bash
# General help
mett --help

# Command group help
mett species --help

# Command help
mett genomes search --help
```

## Configuration

The CLI uses the same configuration as the Python client:

- Environment variables (e.g., `METT_BASE_URL`, `METT_JWT`)
- Config file at `~/.mett/config.toml`
- Command-line options (e.g., `--base-url`, `--jwt`)

See the [Configuration Guide](../config/configuration.md) for details.

## Next Steps

- **[Command Reference](commands.md)** - Complete list of all commands
- **[Common Recipes](recipes.md)** - Workflow examples
- **[Configuration](../config/configuration.md)** - Set up authentication
