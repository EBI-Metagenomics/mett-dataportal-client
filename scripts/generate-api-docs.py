#!/usr/bin/env python3
"""
Generate comprehensive Quarto-compatible API documentation from OpenAPI spec and examples.

This script:
1. Extracts API endpoint information from openapi.json
2. Parses CLI examples from cli-examples.md
3. Maps cURL examples from curl-examples.md
4. Generates a complete api-reference.qmd file with tabbed examples
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

# API category mapping based on tags and paths
CATEGORY_MAP = {
    'System': ['Health', 'Features', 'Metadata'],
    'Species': ['Species'],
    'Genomes': ['Genomes'],
    'Genes': ['Genes'],
    'Drugs': ['Drugs'],
    'Proteomics': ['Proteomics'],
    'Essentiality': ['Essentiality'],
    'Fitness': ['Fitness'],
    'Mutant Growth': ['MutantGrowth'],
    'Reactions': ['Reactions'],
    'Operons': ['Operons'],
    'Orthologs': ['Orthologs'],
    'PPI': ['PPI', 'ProteinProteinInteractions'],
    'TTP': ['TTP', 'PooledTTP'],
    'PyHMMER': ['PyHMMER', 'Pyhmmer'],
}


def load_openapi_spec(openapi_path: Path) -> Dict:
    """Load and parse OpenAPI specification."""
    with open(openapi_path) as f:
        return json.load(f)


def extract_endpoint_info(spec: Dict) -> Dict[str, Dict]:
    """Extract endpoint information from OpenAPI spec."""
    endpoints = {}
    for path, methods in spec['paths'].items():
        for method, details in methods.items():
            if method in ['get', 'post', 'put', 'delete', 'patch']:
                endpoints[path] = {
                    'method': method.upper(),
                    'summary': details.get('summary', ''),
                    'description': details.get('description', ''),
                    'tags': details.get('tags', []),
                    'operationId': details.get('operationId', ''),
                }
    return endpoints


def parse_cli_examples(examples_path: Path) -> List[Dict]:
    """Parse CLI examples from cli-examples.md."""
    with open(examples_path) as f:
        content = f.read()
    
    examples = []
    # Pattern to match example blocks with title, friendly CLI, and generic CLI
    pattern = r'####\s+(.+?)\n\nFriendly CLI:\n```bash\n(.*?)\n```\n\nGeneric CLI:\n```bash\n(.*?)\n```'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        title = match.group(1).strip()
        friendly_cli = match.group(2).strip()
        generic_cli = match.group(3).strip()
        
        examples.append({
            'title': title,
            'friendly_cli': friendly_cli,
            'generic_cli': generic_cli,
        })
    
    return examples


def parse_curl_examples(curl_path: Path) -> Dict[str, str]:
    """Parse cURL examples from curl-examples.md and map to endpoints."""
    with open(curl_path) as f:
        content = f.read()
    
    curl_examples = {}
    # Pattern to match cURL examples with title
    pattern = r'####\s+(.+?)\n\n```bash\n(.*?)\n```'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        title = match.group(1).strip()
        curl_cmd = match.group(2).strip()
        
        # Extract endpoint path from cURL command
        path_match = re.search(r'/(api/[^\s"\']+)', curl_cmd)
        if path_match:
            path = '/' + path_match.group(1).split('?')[0].split('"')[0]
            if path not in curl_examples:
                curl_examples[path] = []
            curl_examples[path].append({
                'title': title,
                'curl': curl_cmd,
            })
    
    return curl_examples


def map_examples_to_endpoints(
    cli_examples: List[Dict],
    curl_examples: Dict[str, List[Dict]],
    endpoints: Dict[str, Dict]
) -> Dict[str, List[Dict]]:
    """Map CLI and cURL examples to their corresponding endpoints."""
    endpoint_examples = defaultdict(list)
    
    # Map CLI examples
    for example in cli_examples:
        generic = example['generic_cli']
        path_match = re.search(r'/(api/[^\s\']+)', generic)
        if path_match:
            path = '/' + path_match.group(1).split()[0].split('?')[0]
            if path in endpoints:
                endpoint_examples[path].append({
                    'title': example['title'],
                    'friendly_cli': example['friendly_cli'],
                    'generic_cli': example['generic_cli'],
                    'curl': None,
                })
    
    # Add cURL examples
    for path, curl_list in curl_examples.items():
        if path in endpoint_examples:
            for i, example in enumerate(endpoint_examples[path]):
                if i < len(curl_list):
                    example['curl'] = curl_list[i]['curl']
        elif path in endpoints:
            # Add cURL-only examples
            for curl_item in curl_list:
                endpoint_examples[path].append({
                    'title': curl_item['title'],
                    'friendly_cli': None,
                    'generic_cli': None,
                    'curl': curl_item['curl'],
                })
    
    return dict(endpoint_examples)


def categorize_endpoint(path: str, tags: List[str]) -> str:
    """Categorize endpoint based on path and tags."""
    path_lower = path.lower()
    
    # Check tags first
    for category, tag_list in CATEGORY_MAP.items():
        if any(tag in tags for tag in tag_list):
            return category
    
    # Check path
    if '/health' in path or '/features' in path or '/metadata' in path:
        return 'System'
    elif '/species' in path:
        return 'Species'
    elif '/genomes' in path:
        return 'Genomes'
    elif '/genes' in path:
        return 'Genes'
    elif '/drugs' in path:
        return 'Drugs'
    elif '/proteomics' in path:
        return 'Proteomics'
    elif '/essentiality' in path:
        return 'Essentiality'
    elif '/fitness' in path:
        return 'Fitness'
    elif '/mutant-growth' in path:
        return 'Mutant Growth'
    elif '/reactions' in path:
        return 'Reactions'
    elif '/operons' in path:
        return 'Operons'
    elif '/orthologs' in path:
        return 'Orthologs'
    elif '/ppi' in path:
        return 'PPI'
    elif '/ttp' in path:
        return 'TTP'
    elif '/pyhmmer' in path:
        return 'PyHMMER'
    
    return 'Other'


def generate_curl_from_generic(generic_cli: str) -> str:
    """Generate cURL command from generic CLI command."""
    # Extract method and path
    method_match = re.search(r'(GET|POST|PUT|DELETE|PATCH)\s+(/api/[^\s\']+)', generic_cli)
    if not method_match:
        return f'curl -X GET "${{METT_BASE_URL:-https://www.gut-microbes.org}}/api/..."'
    
    method = method_match.group(1)
    path = method_match.group(2).split()[0]
    
    # Extract query parameters
    query_params = []
    for match in re.finditer(r'--query\s+([^\\\n]+)', generic_cli):
        param = match.group(1).strip()
        query_params.append(param)
    
    # Extract headers
    headers = []
    for match in re.finditer(r'--header\s+([^\\\n]+)', generic_cli):
        header = match.group(1).strip()
        headers.append(header)
    
    # Build cURL command
    base_url = "${METT_BASE_URL:-https://www.gut-microbes.org}"
    url = f"{base_url}{path}"
    
    if query_params:
        query_string = "&".join(query_params)
        url += f"?{query_string}"
    
    curl = f'curl -X {method} "{url}"'
    
    for header in headers:
        curl += f" \\\n    -H '{header}'"
    
    return curl


def generate_endpoint_section(
    path: str,
    endpoint_info: Dict,
    examples: List[Dict]
) -> str:
    """Generate Quarto markdown section for an endpoint."""
    summary = endpoint_info.get('summary', '')
    description = endpoint_info.get('description', '')
    
    # Use summary as heading, fallback to path-based heading
    if not summary:
        summary = path.replace('/api/', '').replace('/', ' ').title()
        summary = summary.replace('_', ' ').title()
    
    section = f"### {summary}\n\n"
    
    if description:
        section += f"{description}\n\n"
    
    if examples:
        # Use first example (or best match)
        example = examples[0]
        
        section += "::: {.panel-tabset}\n\n"
        
        # Friendly CLI tab
        if example.get('friendly_cli'):
            section += "#### Friendly CLI\n\n"
            section += "```bash\n"
            section += example['friendly_cli'] + "\n"
            section += "```\n\n"
        
        # Generic CLI tab
        if example.get('generic_cli'):
            section += "#### Generic CLI\n\n"
            section += "```bash\n"
            section += example['generic_cli'] + "\n"
            section += "```\n\n"
        
        # cURL tab
        section += "#### cURL\n\n"
        if example.get('curl'):
            section += "```bash\n"
            section += example['curl'] + "\n"
            section += "```\n\n"
        elif example.get('generic_cli'):
            # Generate cURL from generic CLI
            curl_cmd = generate_curl_from_generic(example['generic_cli'])
            section += "```bash\n"
            section += curl_cmd + "\n"
            section += "```\n\n"
        else:
            section += "```bash\n"
            section += f'curl -X {endpoint_info.get("method", "GET")} "${{METT_BASE_URL:-https://www.gut-microbes.org}}{path}"\n'
            section += "```\n\n"
        
        section += ":::\n\n"
    else:
        # No examples, just show basic cURL
        section += "::: {.panel-tabset}\n\n"
        section += "#### cURL\n\n"
        section += "```bash\n"
        section += f'curl -X {endpoint_info.get("method", "GET")} "${{METT_BASE_URL:-https://www.gut-microbes.org}}{path}"\n'
        section += "```\n\n"
        section += ":::\n\n"
    
    return section


def generate_quarto_document(
    endpoints: Dict[str, Dict],
    endpoint_examples: Dict[str, List[Dict]],
    output_path: Path
):
    """Generate complete Quarto document."""
    
    # Organize endpoints by category
    categorized = defaultdict(list)
    for path, info in endpoints.items():
        category = categorize_endpoint(path, info.get('tags', []))
        categorized[category].append((path, info))
    
    # Category order
    category_order = [
        'System', 'Species', 'Genomes', 'Genes',
        'Drugs', 'Proteomics', 'Essentiality', 'Fitness',
        'Mutant Growth', 'Reactions', 'Operons', 'Orthologs',
        'PPI', 'TTP', 'PyHMMER', 'Other'
    ]
    
    # Generate document
    doc = """---
title: "METT Data Portal API Reference"
format:
  html:
    toc: true
    toc-depth: 3
    code-fold: show
    code-tools: true
    code-copy: true
    theme: cosmo
    css: styles.css
---

# Introduction

This document provides comprehensive API reference documentation for the METT Data Portal, including examples in three formats:

- **Friendly CLI**: High-level `mett` commands with intuitive syntax
- **Generic CLI**: Lower-level `mett api request` commands for direct API access
- **cURL**: Raw HTTP requests for integration with any HTTP client

All examples assume the following environment variables:

- `METT_BASE_URL` (defaults to `https://www.gut-microbes.org` if unset)
- `METT_JWT` for endpoints that require experimental access

::: {.callout-note}
## Authentication

- **Public endpoints** (species, genomes search, etc.) work without credentials
- **Experimental endpoints** (drugs, proteomics, fitness, etc.) require a JWT token set via `METT_JWT` environment variable or `~/.mett/config.toml`
:::

"""
    
    # Generate sections by category
    for category in category_order:
        if category not in categorized:
            continue
        
        # Category header
        if category == 'System':
            doc += "# Core APIs\n\n"
            doc += f"## {category} & Health\n\n"
        elif category in ['Drugs', 'Proteomics', 'Essentiality', 'Fitness', 
                         'Mutant Growth', 'Reactions', 'Operons', 'Orthologs']:
            if category == 'Drugs':
                doc += "\n# Experimental APIs\n\n"
            doc += f"## {category}\n\n"
        elif category in ['PPI', 'TTP']:
            if category == 'PPI':
                doc += "\n# Interactions APIs\n\n"
            doc += f"## {category}\n\n"
        elif category == 'PyHMMER':
            doc += "\n# PyHMMER\n\n"
        else:
            if category == 'Species':
                doc += "## Species\n\n"
            elif category == 'Genomes':
                doc += "## Genomes\n\n"
            elif category == 'Genes':
                doc += "## Genes\n\n"
        
        # Sort endpoints within category
        category_endpoints = sorted(categorized[category], key=lambda x: x[0])
        
        for path, info in category_endpoints:
            examples = endpoint_examples.get(path, [])
            doc += generate_endpoint_section(path, info, examples)
    
    doc += """---

::: {.callout-tip}
## Additional Resources

- For more examples, see `docs/reference/cli-examples.md` and `docs/reference/curl-examples.md`
- API schema: `openapi.json`
- Python client documentation: `README.md`
- PyPI package: [mett-dataportal](https://pypi.org/project/mett-dataportal)
:::
"""
    
    # Write document
    with open(output_path, 'w') as f:
        f.write(doc)
    
    print(f"✅ Generated documentation: {output_path}")
    print(f"   - {len(endpoints)} endpoints documented")
    print(f"   - {len(endpoint_examples)} endpoints with examples")


if __name__ == '__main__':
    project_root = Path(__file__).parent.parent
    openapi_path = project_root / 'openapi.json'
    cli_examples_path = project_root / 'docs' / 'reference' / 'cli-examples.md'
    curl_examples_path = project_root / 'docs' / 'reference' / 'curl-examples.md'
    output_path = project_root / 'docs' / 'reference' / 'api-reference.qmd'
    
    print("📚 Generating API Documentation")
    print("=" * 50)
    
    print("\n1. Loading OpenAPI spec...")
    spec = load_openapi_spec(openapi_path)
    endpoints = extract_endpoint_info(spec)
    print(f"   ✅ Found {len(endpoints)} endpoints")
    
    print("\n2. Parsing CLI examples...")
    cli_examples = parse_cli_examples(cli_examples_path)
    print(f"   ✅ Found {len(cli_examples)} CLI examples")
    
    print("\n3. Parsing cURL examples...")
    curl_examples = parse_curl_examples(curl_examples_path)
    print(f"   ✅ Found {sum(len(v) for v in curl_examples.values())} cURL examples")
    
    print("\n4. Mapping examples to endpoints...")
    endpoint_examples = map_examples_to_endpoints(cli_examples, curl_examples, endpoints)
    print(f"   ✅ Mapped examples to {len(endpoint_examples)} endpoints")
    
    print("\n5. Generating Quarto document...")
    generate_quarto_document(endpoints, endpoint_examples, output_path)
    
    print("\n" + "=" * 50)
    print("✅ Documentation generation complete!")
    print(f"\nTo render the documentation, run:")
    print(f"  quarto render {output_path}")
