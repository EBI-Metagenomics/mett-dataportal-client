# Changelog

All notable changes to the METT Data Portal client will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release

## [0.0.1a4] - 2024-XX-XX

### Changed
- Renamed Python package from `mett_dataportal` to `mett_client`
- Updated documentation structure for better user experience

### Fixed
- Fixed `search_genomes` API call to correctly include `format=json` parameter

## [0.0.1a2] - 2024-XX-XX

### Added
- Initial alpha release
- CLI interface with friendly commands
- Python API client
- Support for core APIs (species, genomes, genes)
- Support for experimental APIs (drugs, proteomics, essentiality, fitness, etc.)
- Support for interaction APIs (PPI, TTP)
- Multiple output formats (JSON, TSV, table)
- Configuration via environment variables and config file
- Authentication support for protected endpoints

## Breaking Changes

### Version 0.0.1a4

- **Python import path changed**: `from mett_dataportal import ...` → `from mett_client import ...`
  - This is a breaking change requiring code updates
  - Update all imports in your codebase
  - See [Migration Guide](../RENAME_GUIDE.md) for details

## Deprecations

None currently.

## Migration Guides

### Migrating from `mett_dataportal` to `mett_client`

If you're using version 0.0.1a4 or later:

1. Update imports:
   ```python
   # Old
   from mett_dataportal import DataPortalClient

   # New
   from mett_client import DataPortalClient
   ```

2. Reinstall the package:
   ```bash
   pip install --upgrade mett
   ```

3. Update any scripts or documentation that reference the old import path.

For more details, see the [Migration Guide](../RENAME_GUIDE.md).

## See Also

- **[GitHub Releases](https://github.com/EBI-Metagenomics/mett-dataportal-client/releases)** - Detailed release notes
- **[Migration Guide](../RENAME_GUIDE.md)** - Guide for upgrading between versions
