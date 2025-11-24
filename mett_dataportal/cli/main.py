"""Typer-based CLI wired into the high-level DataPortalClient."""

from __future__ import annotations

from typing import Any, Optional

import typer  # type: ignore[import]

from ..client import DataPortalClient
from ..config import Config, get_config
from .output import print_full_table, print_json, print_tsv

app = typer.Typer(help="METT Data Portal CLI")
species_app = typer.Typer(help="Species endpoints")
genomes_app = typer.Typer(help="Genome endpoints")
drugs_app = typer.Typer(help="Drug experimental data endpoints")

app.add_typer(species_app, name="species")
app.add_typer(genomes_app, name="genomes")
app.add_typer(drugs_app, name="drugs")


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


if __name__ == "__main__":
    app()
