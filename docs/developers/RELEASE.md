# Release Guide

This guide covers the complete process for building, tagging, releasing, and publishing the METT Data Portal client to PyPI.

## Overview

### What Can Be Automated with GitHub Actions ✅

- **Building the package** - Automated on every push/PR
- **Running tests** - Automated on every push/PR
- **Linting and code quality** - Automated on every push/PR
- **Publishing to TestPyPI** - Automated when you push a tag (optional)
- **Publishing to PyPI** - Automated when you push a release tag
- **Version validation** - Automated checks

### What Must Be Done Manually ⚠️

- **Updating the version** in `pyproject.toml` - You must do this
- **Creating a git tag** - You must create and push the tag
- **Writing release notes** - You should document what changed
- **Regenerating SDK** (if API changed) - You must run this before release
- **Creating GitHub Release** - Optional but recommended

## Prerequisites

### 1. PyPI Account Setup

1. **Create PyPI Account**
   - Go to https://pypi.org/account/register/
   - Verify your email

2. **Create TestPyPI Account** (Recommended)
   - Go to https://test.pypi.org/account/register/
   - Use a different username or email

3. **Generate API Tokens**

   **For PyPI:**
   ```bash
   # Go to: https://pypi.org/manage/account/token/
   # Click "Add API token"
   # Name: "mett-dataportal-pypi"
   # Scope: "Entire account" (or specific project)
   # Copy the token (starts with pypi-)
   ```

   **For TestPyPI:**
   ```bash
   # Go to: https://test.pypi.org/manage/account/token/
   # Click "Add API token"
   # Name: "mett-dataportal-testpypi"
   # Scope: "Entire account"
   # Copy the token (starts with pypi-)
   ```

### 2. Configure GitHub Secrets

Add these secrets to your GitHub repository:

**Settings → Secrets and variables → Actions → New repository secret**

1. **`PYPI_API_TOKEN`**
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI API token (starts with `pypi-`)

2. **`TEST_PYPI_API_TOKEN`** (Optional, for TestPyPI)
   - Name: `TEST_PYPI_API_TOKEN`
   - Value: Your TestPyPI API token (starts with `pypi-`)

## Release Process

### Step 1: Prepare for Release

#### 1.1 Update Version

Edit `pyproject.toml`:

```toml
[project]
version = "0.1.1"  # Bump version (patch, minor, or major)
```

**Version Numbering:**
- **Patch** (0.1.0 → 0.1.1): Bug fixes, no API changes
- **Minor** (0.1.0 → 0.2.0): New features, backward compatible
- **Major** (0.1.0 → 1.0.0): Breaking changes

#### 1.2 Regenerate SDK (If API Changed)

If the OpenAPI spec changed:

```bash
# Export latest OpenAPI schema
./scripts/export-openapi-schema.sh

# Regenerate SDK
./scripts/generate-sdk.sh
```

#### 1.3 Update Documentation

```bash
# Regenerate API documentation
python3 scripts/generate-api-docs.py
quarto render docs/reference/api-reference.qmd
```

#### 1.4 Run Tests Locally

```bash
# Run all tests (using uv)
uv run pytest -v

# Run linters (using uv)
uv run ruff check mett_dataportal/ scripts/ tests/

# Format code (using uv)
uv run ruff format mett_dataportal/ scripts/ tests/
```

#### 1.5 Update Changelog (Recommended)

Create or update `CHANGELOG.md`:

```markdown
## [0.1.1] - 2024-01-15

### Added
- New feature X
- New CLI command Y

### Changed
- Improved error messages

### Fixed
- Bug fix Z
```

### Step 2: Commit and Push Changes

```bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "Release v0.1.1"

# Push to main branch
git push origin main
```

### Step 3: Manually Trigger GitHub Actions

**Important:** The publish workflow is manual-only to ensure you always choose where to publish.

1. **Go to GitHub Actions**
   - Navigate to your repository on GitHub
   - Click the **Actions** tab

2. **Run CI Workflow** (optional, to verify before publishing)
   - Select **CI** workflow from the left sidebar
   - Click **Run workflow** button
   - Select branch (usually `main`)
   - Click **Run workflow**

3. **Run Publish Workflow**
   - Select **Publish to PyPI** workflow from the left sidebar
   - Click **Run workflow** button
   - **⚠️ CRITICAL: Select a BRANCH (not a tag) to see the dropdown**
     - In the "Use workflow from" dropdown, select: `main` (or your release branch)
     - **DO NOT select a tag** - the dropdown will disappear if you do
     - After selecting a branch, you'll see **"Where to publish"** dropdown
     - **Choose where to publish:**
       - `testpypi` - For testing (default, recommended first)
       - `pypi` - For production release
   - Click **Run workflow**

**⚠️ GitHub UI Limitation:**
- **If you select a TAG:** The "Where to publish" dropdown will NOT appear (GitHub limitation)
- **If you select a BRANCH:** The dropdown WILL appear and you can choose
- **The workflow will FAIL with a helpful error** if you select a tag, guiding you to select a branch instead

**Why this matters:**
- The workflow uses the version from `pyproject.toml`, not from the branch/tag you select
- Selecting a branch vs tag doesn't affect which version gets published
- You MUST select a branch to see and use the dropdown

### Step 4: Monitor GitHub Actions

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Watch the workflow run:
   - **CI workflow** runs manually (optional)
   - **Publish workflow** runs manually

### Step 5: Verify Publication

#### Check PyPI

1. Visit: https://pypi.org/project/mett-dataportal/
2. Verify the new version appears
3. Check the release date and files

#### Test Installation

```bash
# Install from PyPI
pip install mett-dataportal

# Verify version
pip show mett-dataportal

# Test CLI
mett --version
```

## Manual Publishing (Alternative)

If you prefer to publish manually instead of using GitHub Actions:

### Build Locally

```bash
# Install build tools
pip install build twine

# Build package (creates dist/ directory)
python -m build

# Verify build
twine check dist/*
```

### Publish to TestPyPI (Recommended First)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ mett-dataportal
```

### Publish to PyPI

```bash
# Upload to PyPI
twine upload dist/*
```

**Note:** You'll be prompted for credentials:
- Username: `__token__`
- Password: Your API token (starts with `pypi-`)

## GitHub Actions Workflows

### CI Workflow (`.github/workflows/ci.yml`)

**Triggers:**
- On push to any branch
- On pull requests

**Actions:**
- Runs tests
- Runs linters
- Checks code formatting
- Validates package build

**No secrets required** - This is public CI.

### Publish Workflow (`.github/workflows/publish.yml`)

**Triggers:**
- **Manual only** - Must be triggered via "Run workflow" button in GitHub Actions
- **No automatic triggers** - Tag pushes do NOT trigger publishing

**Actions:**
- Builds the package
- Validates the build
- Publishes to your chosen destination (TestPyPI or PyPI)
- You choose the destination via dropdown when triggering

**Secrets required:**
- `PYPI_API_TOKEN`
- `TEST_PYPI_API_TOKEN` (optional, but recommended for testing)

## Troubleshooting

### Tag Doesn't Trigger Workflow

1. **Check tag format:** Must start with `v` (e.g., `v0.1.1`)
2. **Check workflow file:** Ensure `.github/workflows/publish.yml` exists
3. **Check GitHub Actions:** Go to Actions tab and check for errors
4. **Check secrets:** Ensure `PYPI_API_TOKEN` is set

### Build Fails

1. **Check version:** Ensure version in `pyproject.toml` matches tag (without `v`)
2. **Check dependencies:** Ensure all dependencies are listed in `pyproject.toml`
3. **Check Python version:** Ensure `requires-python` is correct

### Publication Fails

1. **Check API token:** Ensure token is valid and has correct permissions
2. **Check version:** Ensure version doesn't already exist on PyPI
3. **Check package name:** Ensure `name` in `pyproject.toml` is correct

### Version Already Exists

If you try to publish a version that already exists:

1. **Bump version** in `pyproject.toml`
2. **Create new tag** with new version
3. **Push tag** to trigger workflow

## Best Practices

### 1. Always Test First

- Test locally before tagging
- Use TestPyPI for testing the publishing process
- Verify installation after publishing

### 2. Semantic Versioning

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR:** Breaking changes
- **MINOR:** New features, backward compatible
- **PATCH:** Bug fixes

### 3. Release Notes

Always document what changed:
- Create GitHub Release with notes
- Update CHANGELOG.md
- Include migration guide for breaking changes

### 4. Tag Management

- Use annotated tags: `git tag -a v0.1.1 -m "Release v0.1.1"`
- Push tags explicitly: `git push origin v0.1.1`
- Don't delete published tags

### 5. Security

- Never commit API tokens
- Use GitHub Secrets for sensitive data
- Rotate tokens periodically
- Use project-scoped tokens when possible

## Quick Reference

### Full Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Regenerate SDK (if API changed)
- [ ] Update documentation
- [ ] Run tests locally (`uv run pytest -v`)
- [ ] Run linters (`uv run ruff check mett_dataportal/ scripts/ tests/`)
- [ ] Update CHANGELOG.md
- [ ] Commit changes
- [ ] Push to main branch
- [ ] Create and push git tag (`git tag v0.1.1 && git push origin v0.1.1`)
- [ ] Monitor GitHub Actions
- [ ] Verify on PyPI
- [ ] Test installation
- [ ] Create GitHub Release (optional)

### Common Commands

```bash
# Build package
python -m build

# Check build
twine check dist/*

# Publish to TestPyPI
twine upload --repository testpypi dist/*

# Publish to PyPI
twine upload dist/*

# Create tag
git tag -a v0.1.1 -m "Release v0.1.1"
git push origin v0.1.1

# Check version
python -c "from mett_dataportal import __version__; print(__version__)"
```

## See Also

- [Development Guide](DEVELOPMENT.md) - Development setup
- [Version Management](VERSION.md) - Version management details
- [Architecture Guide](ARCHITECTURE.md) - Package architecture
- [PyPI Documentation](https://packaging.python.org/en/latest/) - Official packaging guide
