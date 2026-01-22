# Authentication

Authentication setup for accessing protected METT Data Portal endpoints.

## Public vs. Protected Endpoints

### Public Endpoints (No Authentication Required)

- Species listing and search
- Genome listing and search
- Gene listing and search
- System health and features

### Protected Endpoints (Authentication Required)

- Drug MIC and metabolism data
- Proteomics data
- Essentiality data
- Fitness data
- Protein-protein interactions
- TTP interactions
- Most experimental endpoints

## Authentication Methods

The client supports JWT token authentication for protected endpoints.

### Environment Variable (Recommended)

```bash
export METT_JWT="your-jwt-token-here"
```

### Config File

Create `~/.mett/config.toml`:

```toml
jwt_token = "your-jwt-token-here"
```

### Python

```python
from mett_client import DataPortalClient

# Initialize with JWT token
client = DataPortalClient(jwt_token="your-jwt-token-here")
```

### CLI

```bash
# Using environment variable
export METT_JWT="your-token"
mett drugs mic --drug-name "amoxicillin"

# Or using CLI flag
mett --jwt "your-token" drugs mic --drug-name "amoxicillin"
```

## Getting a JWT Token

Contact the METT Data Portal administrators to obtain a JWT token for accessing experimental endpoints.

## Authentication Priority

Authentication is loaded in this order (first found is used):

1. CLI argument (`--jwt`)
2. Environment variable (`METT_JWT`)
3. Config file (`~/.mett/config.toml`)
4. Python argument (`jwt_token=`)

## Testing Authentication

```python
from mett_client import DataPortalClient
from mett_client.exceptions import AuthenticationError

try:
    client = DataPortalClient(jwt_token="your-token")
    # Try accessing a protected endpoint
    result = client.search_drug_mic(drug_name="test")
    print("Authentication successful!")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
```

## Troubleshooting

### "Authentication required" Error

If you see this error when accessing protected endpoints:

1. Check that `METT_JWT` is set correctly
2. Verify the token is valid and not expired
3. Ensure the token has permissions for the endpoint

### Token Expired

JWT tokens may expire. Contact administrators for a new token.

## See Also

- **[Configuration](configuration.md)** - General configuration options
- **[Troubleshooting](../troubleshooting.md)** - Common authentication issues
