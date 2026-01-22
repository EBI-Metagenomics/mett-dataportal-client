# Contributing to METT Data Portal Client

Thank you for your interest in contributing to the METT Data Portal client library!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/EBI-Metagenomics/mett-dataportal-client.git
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
# Check code style (using uv)
uv run ruff check mett_client/ scripts/ tests/

# Format code (using uv)
uv run ruff format mett_client/ scripts/ tests/
```

## Documentation

### Generating API Documentation

The API documentation is auto-generated from the OpenAPI specification:

```bash
# Generate documentation
python3 scripts/generate-api-docs.py

# Render to HTML
quarto render docs/reference/api-reference.qmd

# Preview in browser (watch mode)
quarto preview docs/reference/api-reference.qmd
```

### Documentation Standards

- Use Quarto (`.qmd`) format for all documentation
- Include examples in three formats: Friendly CLI, Generic CLI, and cURL
- Keep API descriptions synchronized with `openapi.json`
- Follow the existing documentation structure

## Testing

Run tests with:

```bash
# Using uv (recommended)
uv run pytest -v

# Or directly
pytest tests/
```

## Submitting Changes

1. Create a feature branch from `main`
2. Make your changes
3. Ensure tests pass: `uv run pytest -v`
4. Ensure code is formatted: `uv run ruff format mett_client/ scripts/ tests/`
5. Update documentation if needed: `python3 scripts/generate-api-docs.py`
6. Submit a pull request

## Project Structure

```
mett-dataportal-client/
├── mett_client/          # Main package
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
