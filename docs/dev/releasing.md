# Releasing to PyPI

How to publish a new `mett` version to TestPyPI / PyPI.

Package name on PyPI: **[mett](https://pypi.org/project/mett/)**
Version source of truth: **`pyproject.toml`** → `[project].version`
Runtime version (`mett --version`) is read from the installed package metadata (falls back to `pyproject.toml`).

Publishing is done via **GitHub Actions** (`workflow_dispatch`), not from a laptop with long-lived tokens in shell history.

| Workflow | File | Secret |
|----------|------|--------|
| TestPyPI | `.github/workflows/publish-testpypi.yml` | `TEST_PYPI_API_TOKEN` |
| PyPI | `.github/workflows/publish-pypi.yml` | `PYPI_API_TOKEN` |

## Prerequisites

- [ ] Changes merged (or on the branch you intend to publish)
- [ ] CI green on that commit
- [ ] Repo secrets set: `PYPI_API_TOKEN` and/or `TEST_PYPI_API_TOKEN` (PyPI API tokens with upload scope for project `mett`)
- [ ] You can run Actions on the repo (`workflow_dispatch`)

## Checklist

### 1. Bump the version

Edit `pyproject.toml`:

```toml
[project]
version = "0.0.1a9"   # example — next unused version
```

PyPI **never** allows re-uploading an existing version. Always bump.

Optional: if you regenerated the SDK, re-run `./scripts/generate-sdk.sh` so generated `__version__` strings match `pyproject.toml` (see [codegen](codegen.md)).

### 2. Update the changelog

Edit `docs/changelog.md`:

1. Move items under `## [Unreleased]` into a new section, e.g. `## [0.0.1a9] - 2026-04-06`
2. Summarize user-facing changes (Added / Changed / Fixed / Removed)
3. Leave a fresh empty `## [Unreleased]` section at the top
4. **Run tests locally**
  ```bash
  uv run pytest -v
  ```
### 3. Commit and push

```bash
git status
git add pyproject.toml docs/changelog.md
# include other release-ready files as needed
git commit -m "$(cat <<'EOF'
Release 0.0.1a9

EOF
)"
git push
```

Optional but recommended: tag after the version commit is on the remote:

```bash
git tag -a v0.0.1a9 -m "mett 0.0.1a9"
git push origin v0.0.1a9
```

The publish workflows read the version from **`pyproject.toml`**, not from the tag. Tags are for GitHub Releases / humans.

### 4. Dry-run on TestPyPI (recommended)

1. GitHub → **Actions** → **Publish to TestPyPI** → **Run workflow**
2. Choose the branch that contains the bumped version
3. Wait for tests + `twine upload` to finish
4. Verify: https://test.pypi.org/project/mett/

Install check:

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ "mett==0.0.1a9"
mett --version
mett species list --format json
```

(`--extra-index-url` is needed so dependencies resolve from real PyPI.)

### 5. Publish to PyPI

1. GitHub → **Actions** → **Publish to PyPI** → **Run workflow**
2. Same branch / commit as TestPyPI
3. Verify: https://pypi.org/project/mett/

Install check:

```bash
pip install --upgrade "mett==0.0.1a9"
mett --version
```

### 6. GitHub Release (optional)

Create a release from the `v0.0.1a9` tag and paste the changelog section. Point users at:

```bash
pip install -U mett
```

## What the workflow does

1. Checkout
2. Read version from `pyproject.toml`
3. `pip install ".[dev]"`
4. `pytest -v`
5. `python -m build`
6. `twine check dist/*`
7. `twine upload` (TestPyPI or PyPI)

If step 7 fails with “File already exists”, bump the version and re-run — do not try to overwrite.

## Manual local publish (emergency only)

Prefer Actions. If you must upload locally:

```bash
conda activate mett-client   # or your env
pip install -e ".[dev]"
pytest -v
rm -rf dist/ build/
python -m build
twine check dist/*
# TestPyPI:
twine upload --repository testpypi dist/*
# PyPI:
twine upload dist/*
```

Use a PyPI API token as the password (`TWINE_USERNAME=__token__`).

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Version already exists | Bump `pyproject.toml`, commit, re-run workflow |
| `403` / invalid token | Rotate token; ensure secret name matches workflow |
| Tests fail in workflow | Fix on the branch; do not skip tests |
| Wrong version published | Confirm `pyproject.toml` on the selected branch; Actions does not use local uncommitted edits |
| `mett --version` stale after upgrade | Reinstall into the active env; check `which mett` |

## See also

- [SDK codegen](codegen.md) — regenerate before a release when the API changed
- [Changelog](../changelog.md)
- Workflows: `.github/workflows/publish-pypi.yml`, `publish-testpypi.yml`
