# Documentation Structure

This document describes the organization of the documentation directory.

## Directory Organization

```
docs/
├── README.md              # Main documentation overview
├── INDEX.md               # Documentation index/navigation
├── QUICK_START.md         # Quick reference for documentation commands
├── requirements.txt       # Documentation dependencies
│
├── guides/                # User-facing guides
│   ├── README.md         # Guides overview
│   ├── USAGE.md          # Comprehensive usage examples
│   └── CONFIGURATION.md  # Configuration and authentication
│
├── developers/            # Developer documentation
│   ├── README.md         # Developer docs overview
│   └── DEVELOPMENT.md    # Development setup and workflows
│
├── reference/             # API reference and examples
│   ├── README.md         # Reference overview
│   ├── api-reference.qmd # Main API reference (Quarto, auto-generated)
│   ├── cli-examples.md   # CLI command examples (friendly and generic)
│   └── curl-examples.md  # cURL/HTTP request examples
│
└── assets/                # Static assets
    ├── styles.css        # Custom CSS styling
    └── custom.scss        # SCSS customizations
```

## File Categories

### User Documentation (`guides/`)
- **USAGE.md**: How to use the CLI and Python API
- **CONFIGURATION.md**: Setting up authentication and configuration

### Developer Documentation (`developers/`)
- **DEVELOPMENT.md**: Development environment, testing, and release process

### API Reference (`reference/`)
- **api-reference.qmd**: Auto-generated from OpenAPI spec
- **cli-examples.md**: CLI examples source (friendly and generic CLI)
- **curl-examples.md**: cURL/HTTP examples source

### Assets (`assets/`)
- **styles.css**: Custom CSS for rendered documentation
- **custom.scss**: SCSS customizations for Quarto

## Navigation

- Start at [README.md](README.md) for overview
- Use [INDEX.md](INDEX.md) for quick navigation
- See [QUICK_START.md](QUICK_START.md) for common commands

## Maintenance

- **API Reference**: Auto-generated, don't edit manually
- **User Guides**: Manual edits in `guides/`
- **Developer Docs**: Manual edits in `developers/`
- **Examples**: Update in `reference/` for regeneration
