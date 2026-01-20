# Contributing to METT Data Portal Client

Thank you for your interest in contributing to the METT Data Portal client library!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/mett-dataportal-client.git
   cd mett-dataportal-client
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

We use `ruff` for linting and formatting:

```bash
# Check code style
make lint

# Format code
make format
```

## Documentation

### Generating API Documentation

The API documentation is auto-generated from the OpenAPI specification:

```bash
# Generate documentation
make docs-generate

# Render to HTML
make docs-render

# Preview in browser (watch mode)
make docs-preview
```

### Documentation Standards

- Use Quarto (`.qmd`) format for all documentation
- Include examples in three formats: Friendly CLI, Generic CLI, and cURL
- Keep API descriptions synchronized with `openapi.json`
- Follow the existing documentation structure

## Testing

Run tests with:

```bash
make test
# or
pytest tests/
```

## Submitting Changes

1. Create a feature branch from `main`
2. Make your changes
3. Ensure tests pass: `make test`
4. Ensure code is formatted: `make format`
5. Update documentation if needed: `make docs-generate`
6. Submit a pull request

## Project Structure

```
mett-dataportal-client/
├── mett_dataportal/          # Main package
│   ├── cli/                  # CLI commands
│   │   ├── core/             # Core APIs
│   │   ├── experimental/     # Experimental APIs
│   │   └── interactions/     # Interaction APIs
│   ├── client.py             # High-level client
│   └── ...
├── mett_dataportal_sdk/      # Auto-generated SDK
├── docs/                     # Documentation
│   ├── guides/               # User guides
│   │   ├── USAGE.md
│   │   └── CONFIGURATION.md
│   ├── developers/           # Developer docs
│   │   ├── DEVELOPMENT.md
│   │   └── ARCHITECTURE.md
│   ├── reference/            # API reference
│   │   ├── api-reference.qmd
│   │   └── cli-examples*.md
│   └── assets/               # Static assets
├── scripts/                  # Utility scripts
│   └── generate-api-docs.py  # Documentation generator
└── tests/                    # Test suite
```

## Additional Resources

- **[Development Guide](docs/developers/DEVELOPMENT.md)** - Complete development setup and workflows
- **[Architecture Guide](docs/developers/ARCHITECTURE.md)** - Package architecture and design decisions

## Questions?

Feel free to open an issue for any questions or concerns.
