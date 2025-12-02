"""Typer-based CLI wired into the high-level DataPortalClient."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import typer  # type: ignore[import]

from ..client import DataPortalClient
from ..config import Config, get_config
from .output import print_full_table, print_json, print_tsv

app = typer.Typer(help="METT Data Portal CLI")
system_app = typer.Typer(help="System / metadata endpoints")
species_app = typer.Typer(help="Species endpoints")
genomes_app = typer.Typer(help="Genome endpoints")
genes_app = typer.Typer(help="Gene endpoints")
drugs_app = typer.Typer(help="Drug endpoints")
proteomics_app = typer.Typer(help="Proteomics endpoints")
essentiality_app = typer.Typer(help="Essentiality endpoints")
fitness_app = typer.Typer(help="Fitness endpoints")
fitness_corr_app = typer.Typer(help="Fitness correlation endpoints")
mutant_app = typer.Typer(help="Mutant growth endpoints")
reactions_app = typer.Typer(help="Reaction endpoints")
operons_app = typer.Typer(help="Operon endpoints")
orthologs_app = typer.Typer(help="Ortholog endpoints")
ttp_app = typer.Typer(help="Pooled TTP interaction endpoints")
ppi_app = typer.Typer(help="PPI endpoints")
pyhmmer_app = typer.Typer(help="PyHMMER endpoints")
api_app = typer.Typer(help="Low-level raw API access")

app.add_typer(system_app, name="system")
app.add_typer(species_app, name="species")
app.add_typer(genomes_app, name="genomes")
app.add_typer(genes_app, name="genes")
app.add_typer(drugs_app, name="drugs")
app.add_typer(proteomics_app, name="proteomics")
app.add_typer(essentiality_app, name="essentiality")
app.add_typer(fitness_app, name="fitness")
app.add_typer(fitness_corr_app, name="fitness-correlations")
app.add_typer(mutant_app, name="mutant-growth")
app.add_typer(reactions_app, name="reactions")
app.add_typer(operons_app, name="operons")
app.add_typer(orthologs_app, name="orthologs")
app.add_typer(ttp_app, name="ttp")
app.add_typer(ppi_app, name="ppi")
app.add_typer(pyhmmer_app, name="pyhmmer")
app.add_typer(api_app, name="api")


def _build_client(
    *,
    base_url: Optional[str],
    api_key: Optional[str],
    jwt: Optional[str],
    timeout: Optional[int],
    verify_ssl: Optional[bool],
) -> DataPortalClient:
    config = get_config()
    if base_url:
        config.base_url = base_url.rstrip("/")
    if api_key:
        config.api_key = api_key
    if jwt:
        config.jwt_token = jwt
    if timeout is not None:
        config.timeout = timeout
    if verify_ssl is not None:
        config.verify_ssl = verify_ssl
    return DataPortalClient(config=config)


@app.callback()
def main(
    ctx: typer.Context,
    base_url: Optional[str] = typer.Option(None, help="Override the API base URL"),
    api_key: Optional[str] = typer.Option(None, help="API key for RoleBased auth"),
    jwt: Optional[str] = typer.Option(None, help="JWT token for experimental endpoints"),
    timeout: Optional[int] = typer.Option(None, help="HTTP timeout (seconds)"),
    verify_ssl: Optional[bool] = typer.Option(None, help="Set false to skip TLS verification"),
) -> None:
    """Initialize shared client and stash in Typer context."""

    ctx.obj = _build_client(
        base_url=base_url,
        api_key=api_key,
        jwt=jwt,
        timeout=timeout,
        verify_ssl=verify_ssl,
    )


def _ensure_client(ctx: typer.Context) -> DataPortalClient:
    if ctx.obj is None:
        ctx.obj = DataPortalClient(config=get_config())
    return ctx.obj


def _parse_key_value_pairs(
    pairs: Optional[Sequence[str]],
    *,
    separator: str = "=",
    error_message: str = "Expected KEY=VALUE",
) -> Dict[str, str]:
    parsed: Dict[str, str] = {}
    if not pairs:
        return parsed
    for pair in pairs:
        if separator not in pair:
            raise typer.BadParameter(error_message)
        key, value = pair.split(separator, 1)
        parsed[key.strip()] = value.strip()
    return parsed


def _merge_params(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for mapping in dicts:
        for key, value in mapping.items():
            if value is None:
                continue
            merged[key] = value
    return merged


def _extract_table_rows(payload: Any) -> Optional[List[Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("data", "results", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return None


def _handle_raw_response(response, format: Optional[str], *, title: str) -> None:
    content_type = (response.headers.get("Content-Type") or "").lower()
    if (format or "").lower() == "tsv":
        # If TSV format requested, check if response is already TSV
        if "text/tab-separated" in content_type:
            typer.echo(response.text)
            return
        
        # Otherwise, parse JSON and convert to TSV
        try:
            payload = response.json()
        except ValueError:
            # If not JSON, just output as-is
            typer.echo(response.text)
            return
        
        # Extract rows from JSON payload
        rows = _extract_table_rows(payload)
        if rows:
            print_tsv(rows)
        else:
            # If we can't extract rows, output as JSON (fallback)
            print_json(payload)
        return

    try:
        payload = response.json()
    except ValueError:
        typer.echo(response.text)
        return

    if (format or "").lower() == "json":
        print_json(payload)
        return

    rows = _extract_table_rows(payload)
    if rows:
        print_full_table(rows, title=title)
    else:
        print_json(payload)


def _comma_join(values: Optional[Sequence[str]]) -> Optional[str]:
    if not values:
        return None
    return ",".join(values)


def _print_paginated_result(result: Any, format: Optional[str], *, title: str) -> None:
    if format == "tsv":
        print_tsv(result.items)
        return
    if format == "json":
        print_json(result.raw)
        return
    print_full_table(result.items, title=title)


# ---------------------------------------------------------------------------
# System & metadata
# ---------------------------------------------------------------------------


@system_app.command("health")
def system_health(
    ctx: typer.Context,
    format: Optional[str] = typer.Option(None, "--format", "-f", help="json|tsv"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", "/api/health", format=format)
    _handle_raw_response(response, format, title="Health Check")


@system_app.command("features")
def system_features(
    ctx: typer.Context,
    format: Optional[str] = typer.Option(None, "--format", "-f", help="json|tsv"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", "/api/features", format=format)
    _handle_raw_response(response, format, title="Feature Flags")


@system_app.command("cog-categories")
def system_cog_categories(
    ctx: typer.Context,
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", "/api/metadata/cog-categories", format=format)
    _handle_raw_response(response, format, title="COG Categories")


@api_app.command("request")
def api_request(
    ctx: typer.Context,
    method: str = typer.Argument(..., help="HTTP method (GET, POST, etc.)"),
    path: str = typer.Argument(..., help="API path, e.g. /api/species/"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Response format: json|tsv"),
    query: Optional[List[str]] = typer.Option(None, "--query", "-q", help="Query parameter KEY=VALUE"),
    header: Optional[List[str]] = typer.Option(None, "--header", "-H", help="Extra header KEY:VALUE"),
    data: Optional[str] = typer.Option(None, "--data", "-d", help="Raw request payload"),
    json_body: Optional[str] = typer.Option(None, "--json", help="JSON request payload"),
) -> None:
    """Invoke any METT API endpoint while reusing client configuration."""

    client = _ensure_client(ctx)

    if data and json_body:
        raise typer.BadParameter("Use either --data or --json, not both")

    query_params = _parse_key_value_pairs(query)
    header_params = _parse_key_value_pairs(
        header,
        separator=":",
        error_message="Expected header format KEY:VALUE",
    )

    json_payload: Any = None
    if json_body:
        try:
            json_payload = json.loads(json_body)
        except json.JSONDecodeError as exc:
            raise typer.BadParameter(f"Invalid JSON payload: {exc}") from exc

    response = client.raw_request(
        method=method,
        path=path,
        params=query_params,
        headers=header_params,
        data=data,
        json_body=json_payload,
        format=format,
    )

    _handle_raw_response(response, format, title=f"{method.upper()} {path}")


@species_app.command("list")
def list_species(
    ctx: typer.Context,
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format: json|tsv (default: table)"),
) -> None:
    client = _ensure_client(ctx)
    api_format = format or "json"  # Default to JSON for API request
    species = client.list_species(format=api_format)
    
    if format == "tsv":
        print_tsv(species)
    elif format == "json":
        print_json(species)
    else:
        # No format specified - display as table
        print_full_table(species, title="Species")


@species_app.command("genomes")
def species_genomes_list(
    ctx: typer.Context,
    species_acronym: str = typer.Argument(..., help="Species acronym, e.g. BU"),
    query: Optional[str] = typer.Option(None, "--query", "-q", help="Optional search term"),
    isolates: Optional[List[str]] = typer.Option(None, "--isolate", "-i", help="Filter by isolate(s)"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    sort_field: Optional[str] = typer.Option(None, "--sort-field"),
    sort_order: Optional[str] = typer.Option(None, "--sort-order"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="json|tsv"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "query": query,
            "page": page,
            "per_page": per_page,
            "sortField": sort_field,
            "sortOrder": sort_order,
            "isolates": _comma_join(isolates),
        }
    )
    response = client.raw_request(
        "GET",
        f"/api/species/{species_acronym}/genomes",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"Genomes ({species_acronym})")


@species_app.command("search-genomes")
def species_search_genomes(
    ctx: typer.Context,
    species_acronym: str = typer.Argument(..., help="Species acronym, e.g. BU"),
    query: Optional[str] = typer.Option(None, "--query", "-q"),
    isolates: Optional[List[str]] = typer.Option(None, "--isolate", "-i"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    sort_field: Optional[str] = typer.Option(None, "--sort-field"),
    sort_order: Optional[str] = typer.Option(None, "--sort-order"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="json|tsv"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "query": query,
            "page": page,
            "per_page": per_page,
            "sortField": sort_field,
            "sortOrder": sort_order,
            "isolates": _comma_join(isolates),
        }
    )
    response = client.raw_request(
        "GET",
        f"/api/species/{species_acronym}/genomes/search",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"Genomes search ({species_acronym})")


@genomes_app.command("list")
def list_genomes_command(
    ctx: typer.Context,
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    sort_field: Optional[str] = typer.Option(None, "--sort-field"),
    sort_order: Optional[str] = typer.Option(None, "--sort-order"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="json|tsv"),
) -> None:
    client = _ensure_client(ctx)
    result = client.list_genomes(
        format=format or "json",
        page=page,
        per_page=per_page,
        sortField=sort_field,
        sortOrder=sort_order,
    )
    _print_paginated_result(result, format, title="Genomes")


@genomes_app.command("search")
def search_genomes(
    ctx: typer.Context,
    query: Optional[str] = typer.Option(None, "--query", "-q", help="Search term"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    page: int = typer.Option(1, "--page", "-p"),
    per_page: int = typer.Option(10, "--per-page"),
    sort_field: Optional[str] = typer.Option(None, "--sort-field"),
    sort_order: Optional[str] = typer.Option(None, "--sort-order"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format: json|tsv (default: table)"),
) -> None:
    client = _ensure_client(ctx)
    api_format = format or "json"  # Default to JSON for API request
    result = client.search_genomes(
        format=api_format,
        query=query,
        page=page,
        per_page=per_page,
        sort_field=sort_field,
        sort_order=sort_order,
        species_acronym=species_acronym,
    )
    
    if format == "tsv":
        print_tsv(result.items)
    elif format == "json":
        print_json(result.raw)
    else:
        # No format specified - display as table
        print_full_table(result.items, title="Genomes")


@genomes_app.command("type-strains")
def genomes_type_strains(
    ctx: typer.Context,
    format: Optional[str] = typer.Option(None, "--format", "-f", help="json|tsv"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", "/api/genomes/type-strains", format=format)
    _handle_raw_response(response, format, title="Type Strains")


@genomes_app.command("autocomplete")
def genomes_autocomplete(
    ctx: typer.Context,
    query: str = typer.Option(..., "--query", "-q", help="Search term"),
    limit: Optional[int] = typer.Option(5, "--limit"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="json|tsv"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "query": query,
            "limit": limit,
            "species_acronym": species_acronym,
        }
    )
    response = client.raw_request("GET", "/api/genomes/autocomplete", params=params, format=format)
    _handle_raw_response(response, format, title="Genome Autocomplete")


@genomes_app.command("download")
def genomes_download_tsv(
    ctx: typer.Context,
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Destination file (defaults to stdout)"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", "/api/genomes/download/tsv", format="tsv")
    content = response.text
    if output:
        output.write_text(content)
        typer.echo(f"Wrote {output}")
    else:
        typer.echo(content)


@genomes_app.command("by-isolates")
def genomes_by_isolates(
    ctx: typer.Context,
    isolate: List[str] = typer.Option(..., "--isolate", "-i", help="Isolate name(s)"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="json|tsv"),
) -> None:
    client = _ensure_client(ctx)
    params = {"isolates": _comma_join(isolate)}
    response = client.raw_request("GET", "/api/genomes/by-isolate-names", params=params, format=format)
    _handle_raw_response(response, format, title="Genomes by isolate")


@genomes_app.command("genes")
def genomes_genes(
    ctx: typer.Context,
    isolate_name: str = typer.Argument(..., help="Genome isolate name"),
    filter: Optional[str] = typer.Option(None, "--filter", help="Filter expression"),
    filter_operators: Optional[str] = typer.Option(None, "--filter-operators"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    sort_field: Optional[str] = typer.Option(None, "--sort-field"),
    sort_order: Optional[str] = typer.Option(None, "--sort-order"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "filter": filter,
            "filter_operators": filter_operators,
            "page": page,
            "per_page": per_page,
            "sort_field": sort_field,
            "sort_order": sort_order,
        }
    )
    response = client.raw_request(
        "GET",
        f"/api/genomes/{isolate_name}/genes",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"Genes for {isolate_name}")


@genomes_app.command("essentiality")
def genomes_essentiality(
    ctx: typer.Context,
    isolate_name: str = typer.Argument(..., help="Genome isolate name"),
    ref_name: str = typer.Argument(..., help="Reference/contig name"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request(
        "GET",
        f"/api/genomes/{isolate_name}/essentiality/{ref_name}",
        format=format,
    )
    _handle_raw_response(response, format, title=f"Essentiality {isolate_name}:{ref_name}")


@genomes_app.command("drug-mic")
def genomes_drug_mic(
    ctx: typer.Context,
    isolate_name: str = typer.Argument(...),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params({"page": page, "per_page": per_page})
    response = client.raw_request(
        "GET",
        f"/api/genomes/{isolate_name}/drug-mic",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"Drug MIC ({isolate_name})")


@genomes_app.command("drug-metabolism")
def genomes_drug_metabolism(
    ctx: typer.Context,
    isolate_name: str = typer.Argument(...),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params({"page": page, "per_page": per_page})
    response = client.raw_request(
        "GET",
        f"/api/genomes/{isolate_name}/drug-metabolism",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"Drug metabolism ({isolate_name})")


@genomes_app.command("drug-data")
def genomes_drug_data(
    ctx: typer.Context,
    isolate_name: str = typer.Argument(...),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request(
        "GET",
        f"/api/genomes/{isolate_name}/drug-data",
        format=format,
    )
    _handle_raw_response(response, format, title=f"Drug data ({isolate_name})")


# ---------------------------------------------------------------------------
# Genes
# ---------------------------------------------------------------------------


@genes_app.command("list")
def genes_list(
    ctx: typer.Context,
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    sort_field: Optional[str] = typer.Option(None, "--sort-field"),
    sort_order: Optional[str] = typer.Option(None, "--sort-order"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "page": page,
            "per_page": per_page,
            "sort_field": sort_field,
            "sort_order": sort_order,
        }
    )
    response = client.raw_request("GET", "/api/genes/", params=params, format=format)
    _handle_raw_response(response, format, title="Genes")


@genes_app.command("search")
def genes_search(
    ctx: typer.Context,
    query: Optional[str] = typer.Option(None, "--query", "-q"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    sort_field: Optional[str] = typer.Option(None, "--sort-field"),
    sort_order: Optional[str] = typer.Option(None, "--sort-order"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "query": query,
            "page": page,
            "per_page": per_page,
            "sort_field": sort_field,
            "sort_order": sort_order,
        }
    )
    response = client.raw_request("GET", "/api/genes/search", params=params, format=format)
    _handle_raw_response(response, format, title="Gene search")


@genes_app.command("search-advanced")
def genes_search_advanced(
    ctx: typer.Context,
    isolates: Optional[List[str]] = typer.Option(None, "--isolate", "-i"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    locus_tag: Optional[str] = typer.Option(None, "--locus-tag"),
    query: Optional[str] = typer.Option(None, "--query", "-q"),
    filter: Optional[str] = typer.Option(None, "--filter"),
    filter_operators: Optional[str] = typer.Option(None, "--filter-operators"),
    seq_id: Optional[str] = typer.Option(None, "--seq-id"),
    start_position: Optional[int] = typer.Option(None, "--start-position"),
    end_position: Optional[int] = typer.Option(None, "--end-position"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    sort_field: Optional[str] = typer.Option(None, "--sort-field"),
    sort_order: Optional[str] = typer.Option(None, "--sort-order"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "isolates": _comma_join(isolates),
            "species_acronym": species_acronym,
            "locus_tag": locus_tag,
            "query": query,
            "filter": filter,
            "filter_operators": filter_operators,
            "seq_id": seq_id,
            "start_position": start_position,
            "end_position": end_position,
            "page": page,
            "per_page": per_page,
            "sort_field": sort_field,
            "sort_order": sort_order,
        }
    )
    response = client.raw_request("GET", "/api/genes/search/advanced", params=params, format=format)
    _handle_raw_response(response, format, title="Advanced gene search")


@genes_app.command("get")
def genes_get(
    ctx: typer.Context,
    locus_tag: str = typer.Argument(..., help="Locus tag"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", f"/api/genes/{locus_tag}", format=format)
    _handle_raw_response(response, format, title=f"Gene {locus_tag}")


@genes_app.command("proteomics")
def genes_proteomics(
    ctx: typer.Context,
    locus_tag: str = typer.Argument(...),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", f"/api/genes/{locus_tag}/proteomics", format=format)
    _handle_raw_response(response, format, title=f"Proteomics ({locus_tag})")


@genes_app.command("essentiality")
def genes_essentiality(
    ctx: typer.Context,
    locus_tag: str = typer.Argument(...),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", f"/api/genes/{locus_tag}/essentiality", format=format)
    _handle_raw_response(response, format, title=f"Essentiality ({locus_tag})")


@genes_app.command("fitness")
def genes_fitness(
    ctx: typer.Context,
    locus_tag: str = typer.Argument(...),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", f"/api/genes/{locus_tag}/fitness", format=format)
    _handle_raw_response(response, format, title=f"Fitness ({locus_tag})")


@genes_app.command("mutant-growth")
def genes_mutant_growth(
    ctx: typer.Context,
    locus_tag: str = typer.Argument(...),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", f"/api/genes/{locus_tag}/mutant-growth", format=format)
    _handle_raw_response(response, format, title=f"Mutant growth ({locus_tag})")


@genes_app.command("reactions")
def genes_reactions(
    ctx: typer.Context,
    locus_tag: str = typer.Argument(...),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", f"/api/genes/{locus_tag}/reactions", format=format)
    _handle_raw_response(response, format, title=f"Reactions ({locus_tag})")


@genes_app.command("correlations")
def genes_correlations(
    ctx: typer.Context,
    locus_tag: str = typer.Argument(...),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    min_correlation: Optional[float] = typer.Option(None, "--min"),
    max_results: Optional[int] = typer.Option(None, "--max-results"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "species_acronym": species_acronym,
            "min_correlation": min_correlation,
            "max_results": max_results,
        }
    )
    response = client.raw_request(
        "GET",
        f"/api/genes/{locus_tag}/correlations",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"Correlations ({locus_tag})")


@genes_app.command("orthologs")
def genes_orthologs(
    ctx: typer.Context,
    locus_tag: str = typer.Argument(...),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    orthology_type: Optional[str] = typer.Option(None, "--orthology-type"),
    one_to_one_only: Optional[bool] = typer.Option(None, "--one-to-one-only"),
    cross_species_only: Optional[bool] = typer.Option(None, "--cross-species-only"),
    max_results: Optional[int] = typer.Option(None, "--max-results"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "species_acronym": species_acronym,
            "orthology_type": orthology_type,
            "one_to_one_only": one_to_one_only,
            "cross_species_only": cross_species_only,
            "max_results": max_results,
        }
    )
    response = client.raw_request(
        "GET",
        f"/api/genes/{locus_tag}/orthologs",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"Orthologs ({locus_tag})")


@genes_app.command("operons")
def genes_operons(
    ctx: typer.Context,
    locus_tag: str = typer.Argument(...),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params({"species_acronym": species_acronym})
    response = client.raw_request(
        "GET",
        f"/api/genes/{locus_tag}/operons",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"Operons ({locus_tag})")


@genes_app.command("autocomplete")
def genes_autocomplete(
    ctx: typer.Context,
    query: str = typer.Option(..., "--query", "-q"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    isolates: Optional[List[str]] = typer.Option(None, "--isolates", "-i"),
    filter: Optional[str] = typer.Option(None, "--filter", help="Filter expression (e.g., 'essentiality:essential')"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "query": query,
            "species_acronym": species_acronym,
            "isolates": _comma_join(isolates),
            "filter": filter,
            "page": page,
            "per_page": per_page,
        }
    )
    response = client.raw_request("GET", "/api/genes/autocomplete", params=params, format=format)
    _handle_raw_response(response, format, title="Gene autocomplete")


@genes_app.command("faceted-search")
def genes_faceted_search(
    ctx: typer.Context,
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    limit: Optional[int] = typer.Option(None, "--limit"),
    pfam: Optional[str] = typer.Option(None, "--pfam"),
    interpro: Optional[str] = typer.Option(None, "--interpro"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "species_acronym": species_acronym,
            "limit": limit,
            "pfam": pfam,
            "interpro": interpro,
        }
    )
    response = client.raw_request("GET", "/api/genes/faceted-search", params=params, format=format)
    _handle_raw_response(response, format, title="Gene facets")


@genes_app.command("protein")
def genes_protein(
    ctx: typer.Context,
    protein_id: str = typer.Argument(..., help="Protein ID"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", f"/api/genes/protein/{protein_id}", format=format)
    _handle_raw_response(response, format, title=f"Protein {protein_id}")


# ---------------------------------------------------------------------------
# Proteomics & other experimental datasets
# ---------------------------------------------------------------------------


@proteomics_app.command("search")
def proteomics_search(
    ctx: typer.Context,
    locus_tags: Optional[List[str]] = typer.Option(None, "--locus-tag"),
    uniprot_ids: Optional[List[str]] = typer.Option(None, "--uniprot"),
    min_coverage: Optional[float] = typer.Option(None, "--min-coverage"),
    min_unique_peptides: Optional[int] = typer.Option(None, "--min-unique-peptides"),
    has_evidence: Optional[bool] = typer.Option(None, "--has-evidence"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "locus_tags": _comma_join(locus_tags),
            "uniprot_ids": _comma_join(uniprot_ids),
            "min_coverage": min_coverage,
            "min_unique_peptides": min_unique_peptides,
            "has_evidence": has_evidence,
        }
    )
    response = client.raw_request("GET", "/api/proteomics/search", params=params, format=format)
    _handle_raw_response(response, format, title="Proteomics search")


@essentiality_app.command("search")
def essentiality_search(
    ctx: typer.Context,
    locus_tags: Optional[List[str]] = typer.Option(None, "--locus-tag"),
    uniprot_ids: Optional[List[str]] = typer.Option(None, "--uniprot"),
    essentiality_call: Optional[str] = typer.Option(None, "--call"),
    experimental_condition: Optional[str] = typer.Option(None, "--condition"),
    min_tas_in_locus: Optional[int] = typer.Option(None, "--min-tas-in-locus"),
    min_tas_hit: Optional[float] = typer.Option(None, "--min-tas-hit"),
    element: Optional[str] = typer.Option(None, "--element"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "locus_tags": _comma_join(locus_tags),
            "uniprot_ids": _comma_join(uniprot_ids),
            "essentiality_call": essentiality_call,
            "experimental_condition": experimental_condition,
            "min_tas_in_locus": min_tas_in_locus,
            "min_tas_hit": min_tas_hit,
            "element": element,
        }
    )
    response = client.raw_request("GET", "/api/essentiality/search", params=params, format=format)
    _handle_raw_response(response, format, title="Essentiality search")


@fitness_app.command("search")
def fitness_search(
    ctx: typer.Context,
    locus_tags: Optional[List[str]] = typer.Option(None, "--locus-tag"),
    uniprot_ids: Optional[List[str]] = typer.Option(None, "--uniprot"),
    contrast: Optional[str] = typer.Option(None, "--contrast"),
    min_lfc: Optional[float] = typer.Option(None, "--min-lfc"),
    max_fdr: Optional[float] = typer.Option(None, "--max-fdr"),
    min_barcodes: Optional[int] = typer.Option(None, "--min-barcodes"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "locus_tags": _comma_join(locus_tags),
            "uniprot_ids": _comma_join(uniprot_ids),
            "contrast": contrast,
            "min_lfc": min_lfc,
            "max_fdr": max_fdr,
            "min_barcodes": min_barcodes,
        }
    )
    response = client.raw_request("GET", "/api/fitness/search", params=params, format=format)
    _handle_raw_response(response, format, title="Fitness search")


@fitness_corr_app.command("search")
def fitness_correlations_search(
    ctx: typer.Context,
    query: str = typer.Option(..., "--query", "-q"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "query": query,
            "species_acronym": species_acronym,
            "page": page,
            "per_page": per_page,
        }
    )
    response = client.raw_request("GET", "/api/fitness-correlations/search", params=params, format=format)
    _handle_raw_response(response, format, title="Fitness correlations search")


@fitness_corr_app.command("pair")
def fitness_correlations_pair(
    ctx: typer.Context,
    locus_tag_a: str = typer.Option(..., "--gene-a"),
    locus_tag_b: str = typer.Option(..., "--gene-b"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "locus_tag_a": locus_tag_a,
            "locus_tag_b": locus_tag_b,
            "species_acronym": species_acronym,
        }
    )
    response = client.raw_request("GET", "/api/fitness-correlations/correlation", params=params, format=format)
    _handle_raw_response(response, format, title="Gene fitness correlation")


@mutant_app.command("search")
def mutant_growth_search(
    ctx: typer.Context,
    locus_tags: Optional[List[str]] = typer.Option(None, "--locus-tag"),
    uniprot_ids: Optional[List[str]] = typer.Option(None, "--uniprot"),
    media: Optional[str] = typer.Option(None, "--media"),
    experimental_condition: Optional[str] = typer.Option(None, "--condition"),
    min_doubling_time: Optional[float] = typer.Option(None, "--min-doubling-time"),
    max_doubling_time: Optional[float] = typer.Option(None, "--max-doubling-time"),
    exclude_double_picked: Optional[bool] = typer.Option(None, "--exclude-double-picked"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "locus_tags": _comma_join(locus_tags),
            "uniprot_ids": _comma_join(uniprot_ids),
            "media": media,
            "experimental_condition": experimental_condition,
            "min_doubling_time": min_doubling_time,
            "max_doubling_time": max_doubling_time,
            "exclude_double_picked": exclude_double_picked,
        }
    )
    response = client.raw_request("GET", "/api/mutant-growth/search", params=params, format=format)
    _handle_raw_response(response, format, title="Mutant growth search")


@reactions_app.command("search")
def reactions_search(
    ctx: typer.Context,
    locus_tags: Optional[List[str]] = typer.Option(None, "--locus-tag"),
    uniprot_ids: Optional[List[str]] = typer.Option(None, "--uniprot"),
    reaction_id: Optional[str] = typer.Option(None, "--reaction-id"),
    metabolite: Optional[str] = typer.Option(None, "--metabolite"),
    substrate: Optional[str] = typer.Option(None, "--substrate"),
    product: Optional[str] = typer.Option(None, "--product"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "locus_tags": _comma_join(locus_tags),
            "uniprot_ids": _comma_join(uniprot_ids),
            "reaction_id": reaction_id,
            "metabolite": metabolite,
            "substrate": substrate,
            "product": product,
        }
    )
    response = client.raw_request("GET", "/api/reactions/search", params=params, format=format)
    _handle_raw_response(response, format, title="Reaction search")


@orthologs_app.command("search")
def orthologs_search(
    ctx: typer.Context,
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    orthology_type: Optional[str] = typer.Option(None, "--orthology-type"),
    one_to_one_only: Optional[bool] = typer.Option(None, "--one-to-one-only"),
    cross_species_only: Optional[bool] = typer.Option(None, "--cross-species-only"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "species_acronym": species_acronym,
            "orthology_type": orthology_type,
            "one_to_one_only": one_to_one_only,
            "cross_species_only": cross_species_only,
            "page": page,
            "per_page": per_page,
        }
    )
    response = client.raw_request("GET", "/api/orthologs/search", params=params, format=format)
    _handle_raw_response(response, format, title="Ortholog search")


@orthologs_app.command("pair")
def orthologs_pair(
    ctx: typer.Context,
    locus_tag_a: str = typer.Option(..., "--gene-a"),
    locus_tag_b: str = typer.Option(..., "--gene-b"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = {
        "locus_tag_a": locus_tag_a,
        "locus_tag_b": locus_tag_b,
    }
    response = client.raw_request("GET", "/api/orthologs/pair", params=params, format=format)
    _handle_raw_response(response, format, title="Ortholog pair")


@operons_app.command("search")
def operons_search(
    ctx: typer.Context,
    locus_tag: Optional[str] = typer.Option(None, "--locus-tag"),
    operon_id: Optional[str] = typer.Option(None, "--operon-id"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    isolate_name: Optional[str] = typer.Option(None, "--isolate"),
    has_tss: Optional[bool] = typer.Option(None, "--has-tss"),
    has_terminator: Optional[bool] = typer.Option(None, "--has-terminator"),
    min_gene_count: Optional[int] = typer.Option(None, "--min-genes"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "locus_tag": locus_tag,
            "operon_id": operon_id,
            "species_acronym": species_acronym,
            "isolate_name": isolate_name,
            "has_tss": has_tss,
            "has_terminator": has_terminator,
            "min_gene_count": min_gene_count,
            "page": page,
            "per_page": per_page,
        }
    )
    response = client.raw_request("GET", "/api/operons/search", params=params, format=format)
    _handle_raw_response(response, format, title="Operon search")


@operons_app.command("get")
def operons_get(
    ctx: typer.Context,
    operon_id: str = typer.Argument(...),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", f"/api/operons/{operon_id}", format=format)
    _handle_raw_response(response, format, title=f"Operon {operon_id}")


@operons_app.command("statistics")
def operons_statistics(
    ctx: typer.Context,
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params({"species_acronym": species_acronym})
    response = client.raw_request("GET", "/api/operons/statistics", params=params, format=format)
    _handle_raw_response(response, format, title="Operon statistics")


@ttp_app.command("metadata")
def ttp_metadata(
    ctx: typer.Context,
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", "/api/ttp/metadata", format=format)
    _handle_raw_response(response, format, title="TTP metadata")


@ttp_app.command("search")
def ttp_search(
    ctx: typer.Context,
    query: Optional[str] = typer.Option(None, "--query", "-q"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    sort_field: Optional[str] = typer.Option(None, "--sort-field"),
    sort_order: Optional[str] = typer.Option(None, "--sort-order"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "query": query,
            "page": page,
            "per_page": per_page,
            "sort_field": sort_field,
            "sort_order": sort_order,
        }
    )
    response = client.raw_request("GET", "/api/ttp/search", params=params, format=format)
    _handle_raw_response(response, format, title="TTP search")


@ttp_app.command("gene-interactions")
def ttp_gene_interactions(
    ctx: typer.Context,
    locus_tag: str = typer.Argument(...),
    hit_calling: Optional[bool] = typer.Option(None, "--hit-calling"),
    pool_a: Optional[str] = typer.Option(None, "--pool-a"),
    pool_b: Optional[str] = typer.Option(None, "--pool-b"),
    min_ttp_score: Optional[float] = typer.Option(None, "--min-ttp-score"),
    sort_field: Optional[str] = typer.Option(None, "--sort-field"),
    sort_order: Optional[str] = typer.Option(None, "--sort-order"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "locus_tag": locus_tag,
            "hit_calling": hit_calling,
            "poolA": pool_a,
            "poolB": pool_b,
            "min_ttp_score": min_ttp_score,
            "sort_field": sort_field,
            "sort_order": sort_order,
        }
    )
    response = client.raw_request(
        "GET",
        f"/api/ttp/gene/{locus_tag}/interactions",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"TTP interactions ({locus_tag})")


@ttp_app.command("compound-interactions")
def ttp_compound_interactions(
    ctx: typer.Context,
    compound: str = typer.Argument(...),
    hit_calling: Optional[bool] = typer.Option(None, "--hit-calling"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    isolate_name: Optional[str] = typer.Option(None, "--isolate"),
    min_ttp_score: Optional[float] = typer.Option(None, "--min-ttp-score"),
    sort_field: Optional[str] = typer.Option(None, "--sort-field"),
    sort_order: Optional[str] = typer.Option(None, "--sort-order"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "compound": compound,
            "hit_calling": hit_calling,
            "species_acronym": species_acronym,
            "isolate_name": isolate_name,
            "min_ttp_score": min_ttp_score,
            "sort_field": sort_field,
            "sort_order": sort_order,
        }
    )
    response = client.raw_request(
        "GET",
        f"/api/ttp/compound/{compound}/interactions",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"TTP interactions ({compound})")


@ttp_app.command("hits")
def ttp_hits(
    ctx: typer.Context,
    min_ttp_score: Optional[float] = typer.Option(None, "--min-ttp-score"),
    max_fdr: Optional[float] = typer.Option(None, "--max-fdr"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params({"min_ttp_score": min_ttp_score, "max_fdr": max_fdr})
    response = client.raw_request("GET", "/api/ttp/hits", params=params, format=format)
    _handle_raw_response(response, format, title="TTP hits")


@ttp_app.command("pools-analysis")
def ttp_pools_analysis(
    ctx: typer.Context,
    pool_a: str = typer.Option(..., "--pool-a"),
    pool_b: str = typer.Option(..., "--pool-b"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = {"poolA": pool_a, "poolB": pool_b}
    response = client.raw_request("GET", "/api/ttp/pools/analysis", params=params, format=format)
    _handle_raw_response(response, format, title="TTP pools analysis")


@ppi_app.command("scores")
def ppi_scores(
    ctx: typer.Context,
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", "/api/ppi/scores/available", format=format)
    _handle_raw_response(response, format, title="PPI score types")


@ppi_app.command("interactions")
def ppi_interactions(
    ctx: typer.Context,
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    isolate_name: Optional[str] = typer.Option(None, "--isolate"),
    score_type: Optional[str] = typer.Option(None, "--score-type"),
    score_threshold: Optional[float] = typer.Option(None, "--score-threshold"),
    has_xlms: Optional[bool] = typer.Option(None, "--has-xlms"),
    has_string: Optional[bool] = typer.Option(None, "--has-string"),
    has_operon: Optional[bool] = typer.Option(None, "--has-operon"),
    has_ecocyc: Optional[bool] = typer.Option(None, "--has-ecocyc"),
    protein_id: Optional[str] = typer.Option(None, "--protein-id"),
    locus_tag: Optional[str] = typer.Option(None, "--locus-tag"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "species_acronym": species_acronym,
            "isolate_name": isolate_name,
            "score_type": score_type,
            "score_threshold": score_threshold,
            "has_xlms": has_xlms,
            "has_string": has_string,
            "has_operon": has_operon,
            "has_ecocyc": has_ecocyc,
            "protein_id": protein_id,
            "locus_tag": locus_tag,
            "page": page,
            "per_page": per_page,
        }
    )
    response = client.raw_request("GET", "/api/ppi/interactions", params=params, format=format)
    _handle_raw_response(response, format, title="PPI interactions")


@ppi_app.command("neighbors")
def ppi_neighbors(
    ctx: typer.Context,
    protein_id: Optional[str] = typer.Option(None, "--protein-id"),
    locus_tag: Optional[str] = typer.Option(None, "--locus-tag"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "protein_id": protein_id,
            "locus_tag": locus_tag,
            "species_acronym": species_acronym,
        }
    )
    response = client.raw_request("GET", "/api/ppi/neighbors", params=params, format=format)
    _handle_raw_response(response, format, title="PPI neighbors")


@ppi_app.command("neighborhood")
def ppi_neighborhood(
    ctx: typer.Context,
    protein_id: Optional[str] = typer.Option(None, "--protein-id"),
    locus_tag: Optional[str] = typer.Option(None, "--locus-tag"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    n: Optional[int] = typer.Option(None, "--n"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "protein_id": protein_id,
            "locus_tag": locus_tag,
            "species_acronym": species_acronym,
            "n": n,
        }
    )
    response = client.raw_request("GET", "/api/ppi/neighborhood", params=params, format=format)
    _handle_raw_response(response, format, title="PPI neighborhood")


@ppi_app.command("network")
def ppi_network(
    ctx: typer.Context,
    score_type: str = typer.Argument(...),
    score_threshold: Optional[float] = typer.Option(None, "--score-threshold"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    include_properties: Optional[bool] = typer.Option(None, "--include-properties"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "score_threshold": score_threshold,
            "species_acronym": species_acronym,
            "include_properties": include_properties,
        }
    )
    response = client.raw_request(
        "GET",
        f"/api/ppi/network/{score_type}",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"PPI network ({score_type})")


@ppi_app.command("network-properties")
def ppi_network_properties(
    ctx: typer.Context,
    score_type: str = typer.Option(..., "--score-type"),
    score_threshold: Optional[float] = typer.Option(None, "--score-threshold"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "score_type": score_type,
            "score_threshold": score_threshold,
            "species_acronym": species_acronym,
        }
    )
    response = client.raw_request("GET", "/api/ppi/network-properties", params=params, format=format)
    _handle_raw_response(response, format, title="PPI network properties")


# ---------------------------------------------------------------------------
# PyHMMER
# ---------------------------------------------------------------------------


def _load_body_json(body: Optional[str], body_file: Optional[Path]) -> Optional[Any]:
    if body and body_file:
        raise typer.BadParameter("Use either --body-json or --body-file, not both")
    if body:
        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise typer.BadParameter(f"Invalid JSON payload: {exc}") from exc
    if body_file:
        return json.loads(body_file.read_text())
    return None


@pyhmmer_app.command("databases")
def pyhmmer_databases(
    ctx: typer.Context,
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", "/api/pyhmmer/search/databases", format=format)
    _handle_raw_response(response, format, title="PyHMMER databases")


@pyhmmer_app.command("mx-choices")
def pyhmmer_mx_choices(
    ctx: typer.Context,
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", "/api/pyhmmer/search/mx-choices", format=format)
    _handle_raw_response(response, format, title="PyHMMER mx choices")


@pyhmmer_app.command("search")
def pyhmmer_search(
    ctx: typer.Context,
    body_json: Optional[str] = typer.Option(None, "--body-json", help="Inline JSON payload"),
    body_file: Optional[Path] = typer.Option(None, "--body-file", exists=True, readable=True, help="Path to JSON body"),
    format: Optional[str] = typer.Option("json", "--format", "-f", help="json|tsv"),
) -> None:
    client = _ensure_client(ctx)
    payload = _load_body_json(body_json, body_file)
    if payload is None:
        raise typer.BadParameter("Provide --body-json or --body-file")
    response = client.raw_request(
        "POST",
        "/api/pyhmmer/search",
        json_body=payload,
        format=format,
    )
    _handle_raw_response(response, format, title="PyHMMER search")


@pyhmmer_app.command("result")
def pyhmmer_result(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="PyHMMER job ID"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    page_size: Optional[int] = typer.Option(None, "--page-size"),
    taxonomy_ids: Optional[List[str]] = typer.Option(None, "--taxonomy-id"),
    architecture: Optional[str] = typer.Option(None, "--architecture"),
    with_domains: Optional[bool] = typer.Option(None, "--with-domains"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "page": page,
            "page_size": page_size,
            "taxonomy_ids": _comma_join(taxonomy_ids),
            "architecture": architecture,
            "with_domains": with_domains,
        }
    )
    response = client.raw_request(
        "GET",
        f"/api/pyhmmer/result/{job_id}",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"PyHMMER result ({job_id})")


@pyhmmer_app.command("domains")
def pyhmmer_domains(
    ctx: typer.Context,
    job_id: str = typer.Argument(...),
    target: str = typer.Option(..., "--target"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = {"target": target}
    response = client.raw_request(
        "GET",
        f"/api/pyhmmer/result/{job_id}/domains",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"PyHMMER domains ({job_id})")


@pyhmmer_app.command("download")
def pyhmmer_download(
    ctx: typer.Context,
    job_id: str = typer.Argument(...),
    download_format: str = typer.Option(..., "--download-format", help="aligned_fasta|fasta|csv|tab"),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
) -> None:
    client = _ensure_client(ctx)
    params = {"format": download_format}
    response = client.raw_request(
        "GET",
        f"/api/pyhmmer/result/{job_id}/download",
        params=params,
        format="tsv" if download_format == "tab" else None,
    )
    content = response.text
    if output:
        output.write_text(content)
        typer.echo(f"Wrote {output}")
    else:
        typer.echo(content)


@pyhmmer_app.command("debug-msa")
def pyhmmer_debug_msa(
    ctx: typer.Context,
    job_id: str = typer.Argument(...),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request(
        "GET",
        f"/api/pyhmmer/result/{job_id}/debug-pyhmmer-msa",
        format=format,
    )
    _handle_raw_response(response, format, title=f"PyHMMER MSA ({job_id})")


@pyhmmer_app.command("debug-fasta")
def pyhmmer_debug_fasta(
    ctx: typer.Context,
    job_id: str = typer.Argument(...),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request(
        "GET",
        f"/api/pyhmmer/result/{job_id}/debug-fasta",
        format=format,
    )
    _handle_raw_response(response, format, title=f"PyHMMER FASTA ({job_id})")


@pyhmmer_app.command("debug-task")
def pyhmmer_debug_task(
    ctx: typer.Context,
    task_id: str = typer.Argument(...),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    response = client.raw_request("GET", f"/api/pyhmmer/debug/task/{task_id}", format=format)
    _handle_raw_response(response, format, title=f"PyHMMER task ({task_id})")


@pyhmmer_app.command("testtask")
def pyhmmer_testtask(
    ctx: typer.Context,
    body_json: Optional[str] = typer.Option(None, "--body-json"),
    body_file: Optional[Path] = typer.Option(None, "--body-file", exists=True, readable=True),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    payload = _load_body_json(body_json, body_file)
    response = client.raw_request("POST", "/api/pyhmmer/testtask", json_body=payload, format=format)
    _handle_raw_response(response, format, title="PyHMMER test task")


@drugs_app.command("mic")
def drug_mic_search(
    ctx: typer.Context,
    query: Optional[str] = typer.Option(None, "--query", "-q"),
    drug_name: Optional[str] = typer.Option(None, "--drug-name"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    page: int = typer.Option(1, "--page", "-p"),
    per_page: int = typer.Option(20, "--per-page"),
    format: Optional[str] = typer.Option(None, "--format", "-f", help="Output format: json|tsv (default: table)"),
) -> None:
    client = _ensure_client(ctx)
    api_format = format or "json"  # Default to JSON for API request
    result = client.search_drug_mic(
        format=api_format,
        query=query,
        drug_name=drug_name,
        species_acronym=species_acronym,
        page=page,
        per_page=per_page,
    )
    
    if format == "tsv":
        print_tsv(result.items)
    elif format == "json":
        print_json(result.raw)
    else:
        # No format specified - display as table
        print_full_table(result.items, title="Drug MIC")


@drugs_app.command("mic-by-drug")
def drug_mic_by_drug(
    ctx: typer.Context,
    drug_name: str = typer.Argument(..., help="Drug name"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params({"species_acronym": species_acronym})
    response = client.raw_request(
        "GET",
        f"/api/drugs/mic/by-drug/{drug_name}",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"Drug MIC ({drug_name})")


@drugs_app.command("metabolism-search")
def drug_metabolism_search(
    ctx: typer.Context,
    query: Optional[str] = typer.Option(None, "--query", "-q"),
    drug_name: Optional[str] = typer.Option(None, "--drug-name"),
    drug_class: Optional[str] = typer.Option(None, "--drug-class"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    min_fdr: Optional[float] = typer.Option(None, "--min-fdr"),
    min_degr_percent: Optional[float] = typer.Option(None, "--min-degr-percent"),
    metabolizer_classification: Optional[str] = typer.Option(None, "--classification"),
    is_significant: Optional[bool] = typer.Option(None, "--significant"),
    experimental_condition: Optional[str] = typer.Option(None, "--condition"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    sort_by: Optional[str] = typer.Option(None, "--sort-by"),
    sort_order: Optional[str] = typer.Option(None, "--sort-order"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "query": query,
            "drug_name": drug_name,
            "drug_class": drug_class,
            "species_acronym": species_acronym,
            "min_fdr": min_fdr,
            "min_degr_percent": min_degr_percent,
            "metabolizer_classification": metabolizer_classification,
            "is_significant": is_significant,
            "experimental_condition": experimental_condition,
            "page": page,
            "per_page": per_page,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }
    )
    response = client.raw_request("GET", "/api/drugs/metabolism/search", params=params, format=format)
    _handle_raw_response(response, format, title="Drug metabolism search")


@drugs_app.command("metabolism-by-drug")
def drug_metabolism_by_drug(
    ctx: typer.Context,
    drug_name: str = typer.Argument(..., help="Drug name"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params({"species_acronym": species_acronym})
    response = client.raw_request(
        "GET",
        f"/api/drugs/metabolism/by-drug/{drug_name}",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"Drug metabolism ({drug_name})")


@drugs_app.command("mic-by-class")
def drug_mic_by_class(
    ctx: typer.Context,
    drug_class: str = typer.Argument(...),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "species_acronym": species_acronym,
            "page": page,
            "per_page": per_page,
        }
    )
    response = client.raw_request(
        "GET",
        f"/api/drugs/mic/by-class/{drug_class}",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"Drug MIC class ({drug_class})")


@drugs_app.command("metabolism-by-class")
def drug_metabolism_by_class(
    ctx: typer.Context,
    drug_class: str = typer.Argument(...),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    page: Optional[int] = typer.Option(None, "--page", "-p"),
    per_page: Optional[int] = typer.Option(None, "--per-page"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = _ensure_client(ctx)
    params = _merge_params(
        {
            "species_acronym": species_acronym,
            "page": page,
            "per_page": per_page,
        }
    )
    response = client.raw_request(
        "GET",
        f"/api/drugs/metabolism/by-class/{drug_class}",
        params=params,
        format=format,
    )
    _handle_raw_response(response, format, title=f"Drug metabolism class ({drug_class})")


if __name__ == "__main__":
    app()
