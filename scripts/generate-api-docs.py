#!/usr/bin/env python3
"""
Generate Quarto API reference from openapi.json only.

Examples are synthesized from the public OpenAPI paths (generic CLI + cURL).
Hidden/internal routes that are not in the schema are never documented here.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

CATEGORY_MAP = {
    "System": ["Health", "Features", "Metadata", "Releases"],
    "Species": ["Species"],
    "Genomes": ["Genomes"],
    "Genes": ["Genes"],
    "Drugs": ["Drugs"],
    "Proteomics": ["Proteomics"],
    "Essentiality": ["Essentiality"],
    "Fitness": ["Fitness", "FitnessCorrelations"],
    "Mutant Growth": ["MutantGrowth"],
    "Reactions": ["Reactions"],
    "Operons": ["Operons"],
    "Orthologs": ["Orthologs"],
    "PPI": ["PPI", "ProteinProteinInteractions"],
    "TTP": ["TTP", "PooledTTP"],
    "PyHMMER": ["PyHMMER", "Pyhmmer"],
}

CATEGORY_ORDER = [
    "System",
    "Species",
    "Genomes",
    "Genes",
    "Drugs",
    "Proteomics",
    "Essentiality",
    "Fitness",
    "Mutant Growth",
    "Reactions",
    "Operons",
    "Orthologs",
    "PPI",
    "TTP",
    "PyHMMER",
    "Other",
]

BASE = "${METT_BASE_URL:-https://www.gut-microbes.org}"


def load_openapi_spec(openapi_path: Path) -> Dict[str, Any]:
    with openapi_path.open() as fh:
        return json.load(fh)


def extract_endpoint_info(spec: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    endpoints: Dict[str, Dict[str, Any]] = {}
    for path, methods in spec["paths"].items():
        for method, details in methods.items():
            if method not in {"get", "post", "put", "delete", "patch"}:
                continue
            if not isinstance(details, dict):
                continue
            endpoints[path] = {
                "method": method.upper(),
                "summary": details.get("summary", ""),
                "description": details.get("description", ""),
                "tags": details.get("tags", []),
                "operationId": details.get("operationId", ""),
                "parameters": details.get("parameters", []),
            }
    return endpoints


def categorize_endpoint(path: str, tags: List[str]) -> str:
    for category, tag_list in CATEGORY_MAP.items():
        if any(tag in tags for tag in tag_list):
            return category
    if "/releases" in path:
        return "System"
    if "/species" in path:
        return "Species"
    if "/genomes" in path:
        return "Genomes"
    if "/genes" in path:
        return "Genes"
    if "/drugs" in path:
        return "Drugs"
    if "/proteomics" in path:
        return "Proteomics"
    if "/essentiality" in path:
        return "Essentiality"
    if "/fitness" in path:
        return "Fitness"
    if "/mutant-growth" in path:
        return "Mutant Growth"
    if "/reactions" in path:
        return "Reactions"
    if "/operons" in path:
        return "Operons"
    if "/orthologs" in path:
        return "Orthologs"
    if "/ppi" in path:
        return "PPI"
    if "/ttp" in path:
        return "TTP"
    if "/pyhmmer" in path:
        return "PyHMMER"
    return "Other"


def _sample_path(path: str) -> str:
    """Replace path templates with placeholder values for copy-paste examples."""
    samples = {
        "locus_tag": "BU_ATCC8492_00001",
        "isolate_name": "BU_ATCC8492",
        "species_acronym": "BU",
        "drug_name": "amoxicillin",
        "pair_id": "bu:A0A0X1ABC1__B0ABC123",
        "score_type": "ds_score",
        "ref_name": "contig_1",
        "operon_id": "operon_1",
        "compound": "compound_1",
        "id": "JOB_ID",
    }

    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        return samples.get(name, f"{{{name}}}")

    return re.sub(r"\{([^}]+)\}", repl, path)


def synthesize_examples(path: str, info: Dict[str, Any]) -> List[Dict[str, str]]:
    method = info["method"]
    sample = _sample_path(path)
    generic = f"mett api request {method} {sample} \\\n" f"  --format json"
    curl = f'curl -X {method} "{BASE}{sample}"'
    if method != "GET":
        curl += " \\\n  -H 'Content-Type: application/json'"
    return [
        {
            "title": info.get("summary") or path,
            "friendly_cli": "",
            "generic_cli": generic,
            "curl": curl,
        }
    ]


def generate_endpoint_section(
    path: str, endpoint_info: Dict[str, Any], examples: List[Dict[str, str]]
) -> str:
    summary = endpoint_info.get("summary") or path
    description = endpoint_info.get("description", "")
    section = f"### {summary}\n\n"
    section += f"`{endpoint_info.get('method', 'GET')} {path}`\n\n"
    if description:
        section += f"{description}\n\n"

    example = examples[0] if examples else {}
    section += "::: {.panel-tabset}\n\n"
    if example.get("generic_cli"):
        section += "#### Generic CLI\n\n```bash\n"
        section += example["generic_cli"] + "\n```\n\n"
    section += "#### cURL\n\n```bash\n"
    section += example.get(
        "curl",
        f'curl -X {endpoint_info.get("method", "GET")} "{BASE}{path}"',
    )
    section += "\n```\n\n:::\n\n"
    return section


def generate_quarto_document(
    endpoints: Dict[str, Dict[str, Any]],
    endpoint_examples: Dict[str, List[Dict[str, str]]],
    output_path: Path,
) -> None:
    categorized: Dict[str, List[Tuple[str, Dict[str, Any]]]] = defaultdict(list)
    for path, info in endpoints.items():
        categorized[categorize_endpoint(path, info.get("tags", []))].append(
            (path, info)
        )

    doc = f"""---
title: "METT Data Portal API Reference"
format:
  html:
    toc: true
    toc-depth: 3
    code-fold: show
    code-tools: true
    code-copy: true
    theme: cosmo
---

# Introduction

Auto-generated from `openapi.json`. Only **public OpenAPI** paths are listed.

- **Generic CLI**: `mett api request …`
- **cURL**: raw HTTP

Environment: `METT_BASE_URL` (default `{BASE}`), `METT_JWT` for protected routes, optional `METT_RELEASE`.

::: {{.callout-note}}
## Friendly CLI

Curated high-level commands live in [Examples](../examples.md) and the [CLI Guide](../cli.md).
:::

"""

    for category in CATEGORY_ORDER:
        if category not in categorized:
            continue
        if category == "System":
            doc += "# Core APIs\n\n"
        elif category == "Drugs":
            doc += "\n# Experimental APIs\n\n"
        elif category == "PPI":
            doc += "\n# Interactions APIs\n\n"
        elif category == "PyHMMER":
            doc += "\n# PyHMMER\n\n"
        doc += f"## {category}\n\n"

        for path, info in sorted(categorized[category], key=lambda x: x[0]):
            doc += generate_endpoint_section(
                path, info, endpoint_examples.get(path, [])
            )

    doc += """
::: {.callout-tip}
## Additional resources

- [Examples](../examples.md)
- [CLI Guide](../cli.md)
- [Python API](../python.md)
- Schema: `openapi.json`
:::
"""
    output_path.write_text(doc)
    print(f"Generated {output_path} ({len(endpoints)} endpoints)")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    openapi_path = root / "openapi.json"
    output_path = root / "docs" / "reference" / "api-reference.qmd"

    print("Loading OpenAPI…")
    endpoints = extract_endpoint_info(load_openapi_spec(openapi_path))
    print(f"  {len(endpoints)} public paths")

    endpoint_examples = {
        path: synthesize_examples(path, info) for path, info in endpoints.items()
    }
    generate_quarto_document(endpoints, endpoint_examples, output_path)


if __name__ == "__main__":
    main()
