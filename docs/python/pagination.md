# Pagination Patterns

How to work with paginated results in the METT Python client.

## Basic Pagination

Most search methods return `PaginatedResult` objects:

```python
from mett_client import DataPortalClient

client = DataPortalClient()
result = client.search_genomes(query="Bacteroides", page=1, per_page=10)

# Access items
print(f"Found {len(result.items)} genomes on this page")

# Access pagination metadata
if result.pagination:
    print(f"Page {result.pagination.page} of {result.pagination.total_pages}")
    print(f"Total items: {result.pagination.total}")
    print(f"Per page: {result.pagination.per_page}")
    print(f"Has next: {result.pagination.has_next}")
    print(f"Has previous: {result.pagination.has_previous}")
```

## Iterating Through All Pages

### Simple Loop

```python
from mett_client import DataPortalClient

client = DataPortalClient()
page = 1
all_genomes = []

while True:
    result = client.search_genomes(query="Bacteroides", page=page, per_page=20)
    all_genomes.extend(result.items)

    if not result.pagination or not result.pagination.has_next:
        break

    page += 1

print(f"Total genomes found: {len(all_genomes)}")
```

### Using a Generator

```python
from mett_client import DataPortalClient

def get_all_genomes(client, query, per_page=20):
    """Generator that yields all genomes across all pages."""
    page = 1
    while True:
        result = client.search_genomes(query=query, page=page, per_page=per_page)
        yield from result.items

        if not result.pagination or not result.pagination.has_next:
            break

        page += 1

# Usage
client = DataPortalClient()
for genome in get_all_genomes(client, "Bacteroides"):
    print(genome.isolate_name)
```

## Processing Large Result Sets

### With Progress Tracking

```python
from mett_client import DataPortalClient

client = DataPortalClient()
page = 1
total_processed = 0

while True:
    result = client.search_genomes(query="Bacteroides", page=page, per_page=50)

    # Process items
    for genome in result.items:
        # Your processing logic here
        total_processed += 1

    # Show progress
    if result.pagination:
        print(f"Processed {total_processed} / {result.pagination.total} genomes")

    if not result.pagination or not result.pagination.has_next:
        break

    page += 1
```

### With Error Handling

```python
from mett_client import DataPortalClient
from mett_client.exceptions import APIError

client = DataPortalClient()
page = 1
all_items = []

while True:
    try:
        result = client.search_genomes(query="Bacteroides", page=page, per_page=20)
        all_items.extend(result.items)

        if not result.pagination or not result.pagination.has_next:
            break

        page += 1
    except APIError as e:
        print(f"Error on page {page}: {e}")
        # Decide whether to retry or break
        break
```

## Parallel Processing

For large result sets, you can fetch multiple pages in parallel:

```python
from concurrent.futures import ThreadPoolExecutor
from mett_client import DataPortalClient

def fetch_page(client, query, page, per_page):
    """Fetch a single page."""
    return client.search_genomes(query=query, page=page, per_page=per_page)

# First, get total pages
client = DataPortalClient()
first_result = client.search_genomes(query="Bacteroides", page=1, per_page=20)
total_pages = first_result.pagination.total_pages if first_result.pagination else 1

# Fetch all pages in parallel
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [
        executor.submit(fetch_page, client, "Bacteroides", page, 20)
        for page in range(1, total_pages + 1)
    ]

    all_items = []
    for future in futures:
        result = future.result()
        all_items.extend(result.items)

print(f"Fetched {len(all_items)} genomes")
```

## Best Practices

1. **Use appropriate page sizes**: Larger pages (50-100) reduce API calls but increase memory usage
2. **Handle rate limits**: Add delays between requests if needed
3. **Cache results**: Store results locally to avoid repeated API calls
4. **Use filters**: Narrow your search to reduce pagination needs

## See Also

- **[Python Quickstart](quickstart.md)** - Basic usage examples
- **[Configuration Guide](../config/configuration.md)** - Client configuration
