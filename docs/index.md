# METT Data Portal Client Documentation

Welcome to the METT Data Portal Client documentation! This client provides both a command-line interface (CLI) and a Python API for accessing the **Microbial Ecosystems Transversal Themes (METT) Data Portal**.

## What is METT?

The METT Data Portal provides access to genomic data, experimental results, and protein interactions for gut microbiome research. This client library makes it easy to:

- Search and retrieve species, genomes, and genes
- Access experimental data (drugs, proteomics, fitness, etc.)
- Query protein-protein interactions
- Download results in multiple formats

## Quick Start

### Installation

```bash
pip install mett
```

### First Command

```bash
# List all species
mett species list
```

### First Python Snippet

```python
from mett_client import DataPortalClient

client = DataPortalClient()
species = client.list_species()
print(f"Found {len(species)} species")
```

### Default Configuration

The client connects to **http://www.gut-microbes.org** by default. You can override this using environment variables or configuration files.

## Documentation Sections

### For End Users

- **[CLI Guide](cli/overview.md)** - Learn how to use the command-line interface
- **[Python API Guide](python/quickstart.md)** - Get started with the Python client
- **[Configuration](config/configuration.md)** - Set up authentication and configuration
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions

### Reference

- **[CLI Commands](cli/commands.md)** - Complete command reference
- **[CLI Recipes](cli/recipes.md)** - Common workflows and examples
- **[Python API Reference](python/quickstart.md)** - Core objects and methods
- **[Changelog](changelog.md)** - Release notes and breaking changes

## Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/EBI-Metagenomics/mett-dataportal-client/issues)
- **Source Code**: [View on GitHub](https://github.com/EBI-Metagenomics/mett-dataportal-client)
- **Portal**: [Visit the METT Data Portal](http://www.gut-microbes.org/)

## Next Steps

1. **[Install the client](../README.md#installation)** if you haven't already
2. **[Configure authentication](config/authentication.md)** for experimental endpoints
3. **[Try the CLI](cli/overview.md)** with some example commands
4. **[Explore the Python API](python/quickstart.md)** for programmatic access
