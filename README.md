# mett-dataportal-client

Python client/CLI scaffolding for the METT Data Portal API.

## Regenerating the SDK

1. Ensure `openapi.json` is present (see `scripts/export-openapi-schema.sh`).
2. Run:
   ```bash
   ./scripts/generate-sdk.sh
   ```
   This refreshes the vendored `mett_dataportal_sdk/` package using `openapi-generator-cli`.

The high-level wrapper in `mett_dataportal/client.py` now delegates to the generated SDK, so the CLI and package stay in sync with the API schema.

---

## Local Environment (Conda)

If you prefer Conda, the following sets up a `mett-client` env driven by `pyproject.toml`:

```bash
# create env with Python 3.11 (matches workflows)
conda create -n mett-client python=3.12 -y
conda activate mett-client

# install package + dev deps defined in pyproject.toml
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

From here you can:

- Run the CLI: `mett --help`
- Execute scripts: `./scripts/generate-sdk.sh`
- Build the package locally: `python -m build`

When done, `conda deactivate`.

---

## Set the environment variable once per shell (till the time we don't have the SSL certificate procured):
   ```bash
   export METT_VERIFY_SSL=false
   ```

## CLI Usage (With & Without Auth)

1. **Install locally**
   ```bash
   pip install --upgrade pip
   pip install -e .
   ```

2. **Authentication (optional)**
   - Public endpoints (species, genomes search, etc.) work without credentials.
   - For JWT-protected experimental data, set an env var or config file:
     ```bash
     export METT_JWT="eyJhbGciOi..."        # preferred
     # optional: custom base URL
    export METT_BASE_URL="https://www.gut-microbes.org"
     ```
     You can also create `~/.mett/config.toml`:
     ```toml
     base_url = "https://www.gut-microbes.org"
     jwt_token = "eyJhbGciOi..."
     timeout = 60
     verify_ssl = true
     ```
     The canonical host lives in `mett_dataportal.constants.DEFAULT_BASE_URL`. Update that single constant if the default ever changes; the CLI and client pick up overrides via `METT_BASE_URL` or config files as shown above.

3. **Examples**
   - List species (no auth needed):
     ```bash
     mett species list
     ```
   - Search genomes (public):
     ```bash
     mett genomes search --query "Bacteroides" --per-page 5
     ```
   - Fetch experimental drug MIC data (requires JWT):
     ```bash
     METT_JWT=... mett drugs mic --drug-name "azithromycin" --species BU
     ```
   - JSON output for pipelines:
     ```bash
     mett genomes search --query PV --format json | jq '.'
     ```
   - TSV format (more efficient for large datasets):
     ```bash
     mett genomes search --query "Bacteroides" --format tsv
     mett species list --format tsv
     ```
   - Explore any API group (every endpoint now has a dedicated command):
     ```bash
     mett genes --help
     mett proteomics search --help
     mett pyhmmer search --help
     ```
   - Raw API access (full surface area):
     ```bash
     mett api request GET /api/health --format json
     mett api request GET /api/genomes/autocomplete --format json --query query=bu --query limit=5
     ```

4. **Output Formats**
   - **Table** (default, no `--format` specified): Requests JSON from API, displays results in a formatted table
   - **JSON** (`--format json`): Requests JSON from API, displays raw JSON output
   - **TSV** (`--format tsv`): Requests TSV from API, displays raw TSV output (ideal for bulk data export and spreadsheet tools)

5. **Non-interactive pipelines**
   - Combine with curl/jq/wget by using `--format json` or `--format tsv`.
   - See `docs/cli-examples-mett.md` for a catalog of `mett api request` examples covering every positive Postman scenario.
   - Use `METT_TIMEOUT` and `METT_VERIFY_SSL=false` when running against dev environments.

---

## Publishing & Consuming the PyPI Package

### Preparing a Release
1. Regenerate the SDK (if the API changed):
   ```bash
   ./scripts/export-openapi-schema.sh      # fetch latest schema
   ./scripts/generate-sdk.sh               # regenerate client
   ```
2. Bump the version in `pyproject.toml`.
3. Run tests / lint if applicable.

### Build & Publish
```bash
python -m build

# TestPyPI dry run
twine upload --repository testpypi dist/*

# Verify
pip install --index-url https://test.pypi.org/simple/ mett-dataportal

# Publish to PyPI
twine upload dist/*
```

### Automating with GitHub Actions
Two workflows live in `.github/workflows/`:

- `ci.yml` runs on pushes/PRs to `main`, installs `-e .[dev]`, and executes placeholder lint/test commands (replace with real checks as they’re added).
- `publish.yml` runs when a release is published (or via manual dispatch). It:
  1. Checks out the repo and sets up Python 3.11.
  2. Installs `build`, `twine`, and `openapi-generator-cli`.
  3. (Optionally) refreshes `openapi.json`, then runs `./scripts/generate-sdk.sh`.
  4. Builds the package with `python -m build`.
  5. Uploads artifacts with Twine using the `PYPI_API_TOKEN` repository secret.

To activate:
1. Store your PyPI API token as `PYPI_API_TOKEN` under **Settings → Secrets and variables → Actions**.
2. Tag a release (`git tag v0.1.0 && git push origin v0.1.0`) or manually trigger the workflow from the Actions tab.

TestPyPI support can be added by duplicating the publish step with another secret (e.g., `TEST_PYPI_API_TOKEN`) and pointing Twine’s `--repository` to `testpypi`.

### Consumers
```bash
pip install mett-dataportal

python - <<'PY'
from mett_dataportal import DataPortalClient
client = DataPortalClient(jwt_token="...optional...")

# JSON format (default)
species = client.list_species(format="json")
print(species[:3])

# TSV format (more efficient for large datasets)
genomes = client.search_genomes(format="tsv", query="Bacteroides")
print(f"Found {len(genomes.items)} genomes")
PY

# CLI
mett genomes search --query "PV"                # Table format (default)
mett genomes search --query "PV" --format json   # JSON format
mett genomes search --query "PV" --format tsv    # TSV format
```

Document these steps (README or internal wiki) before sharing publicly.
