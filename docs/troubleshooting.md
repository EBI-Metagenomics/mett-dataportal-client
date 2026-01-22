# Troubleshooting

Common issues and solutions when using the METT Data Portal client.

## SSL Errors

### Problem

```
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed
```

### Solution

For development environments without proper SSL certificates:

```bash
export METT_VERIFY_SSL=false
```

Or in Python:

```python
from mett_client import DataPortalClient

client = DataPortalClient(verify_ssl=False)
```

**Warning**: Only disable SSL verification in development. Never use this in production.

## Command Not Found

### Problem

```
mett: command not found
```

### Solutions

1. **Check installation**:
   ```bash
   pip install mett
   ```

2. **Check PATH**: Ensure the Python scripts directory is in your PATH:
   ```bash
   # Find where pip installs scripts
   python -m site --user-base

   # Add to PATH (example for Linux/macOS)
   export PATH="$PATH:$(python -m site --user-base)/bin"
   ```

3. **Use Python module**:
   ```bash
   python -m mett_client.cli.main --help
   ```

4. **pyenv shim confusion**: If using pyenv, ensure the correct Python version is active:
   ```bash
   pyenv versions
   pyenv local 3.11.0  # or your version
   ```

## Authentication Failed

### Problem

```
AuthenticationError: Authentication required
```

### Solutions

1. **Check JWT token**:
   ```bash
   echo $METT_JWT
   ```

2. **Verify token is set**:
   ```python
   from mett_client import DataPortalClient

   client = DataPortalClient(jwt_token="your-token")
   # Test with a protected endpoint
   ```

3. **Check token expiration**: JWT tokens may expire. Contact administrators for a new token.

4. **Verify endpoint requires auth**: Some endpoints are public and don't require authentication.

## No Results / Filters Not Working

### Problem

Search queries return no results or filters don't work as expected.

### Solutions

1. **Check query syntax**:
   ```bash
   # Try a simple query first
   mett genomes search --query "BU" --format json
   ```

2. **Verify filter syntax**:
   ```bash
   # Correct filter format
   mett genes search-advanced --filter "essentiality:essential" --format json

   # Multiple filters
   mett genes search-advanced --filter "pfam:pf13715;essentiality:not_essential" --format json
   ```

3. **Check species acronyms**: Use correct species codes (e.g., `BU`, `PV`):
   ```bash
   mett species list --format json
   ```

4. **Try without filters first**: Narrow down the issue:
   ```bash
   # Without filters
   mett genes search --query "dnaA" --format json

   # Then add filters
   mett genes search-advanced --query "dnaA" --species BU --format json
   ```

## Connection Timeout

### Problem

```
TimeoutError: Request timed out
```

### Solutions

1. **Increase timeout**:
   ```bash
   export METT_TIMEOUT=120
   ```

   Or in Python:
   ```python
   client = DataPortalClient(timeout=120)
   ```

2. **Check network connectivity**:
   ```bash
   curl http://www.gut-microbes.org/api/health
   ```

3. **Check base URL**:
   ```bash
   echo $METT_BASE_URL
   ```

## Import Errors

### Problem

```
ImportError: cannot import name 'DataPortalClient' from 'mett_client'
```

### Solutions

1. **Reinstall package**:
   ```bash
   pip uninstall mett
   pip install mett
   ```

2. **Check Python version**: Requires Python 3.10+:
   ```bash
   python --version
   ```

3. **Check virtual environment**: Ensure you're in the correct virtual environment:
   ```bash
   which python
   pip list | grep mett
   ```

## Pagination Issues

### Problem

Not getting all results or pagination not working.

### Solutions

1. **Check pagination metadata**:
   ```python
   result = client.search_genomes(query="test", page=1, per_page=10)
   if result.pagination:
       print(f"Total pages: {result.pagination.total_pages}")
       print(f"Has next: {result.pagination.has_next}")
   ```

2. **Iterate through pages**:
   ```python
   page = 1
   while True:
       result = client.search_genomes(query="test", page=page, per_page=20)
       # Process results
       if not result.pagination or not result.pagination.has_next:
           break
       page += 1
   ```

## Rate Limiting

### Problem

Getting rate limit errors or requests being throttled.

### Solutions

1. **Add delays between requests**:
   ```python
   import time

   for page in range(1, 10):
       result = client.search_genomes(query="test", page=page)
       time.sleep(1)  # Wait 1 second between requests
   ```

2. **Reduce request frequency**: Use larger page sizes to reduce number of requests.

3. **Contact administrators**: If rate limits are too restrictive, contact the API administrators.

## Getting Help

If you're still experiencing issues:

1. **Check the documentation**: Review the [Configuration Guide](config/configuration.md) and [Python Quickstart](python/quickstart.md)

2. **Report issues**: [Open an issue on GitHub](https://github.com/EBI-Metagenomics/mett-dataportal-client/issues)

3. **Check API status**: Verify the API is operational:
   ```bash
   mett system health --format json
   ```

## See Also

- **[Configuration Guide](config/configuration.md)** - Configuration options
- **[Authentication Guide](config/authentication.md)** - Authentication setup
- **[CLI Overview](cli/overview.md)** - CLI usage
- **[Python Quickstart](python/quickstart.md)** - Python API usage
