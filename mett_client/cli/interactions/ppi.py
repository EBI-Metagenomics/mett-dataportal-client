"""PPI (Protein-Protein Interactions) CLI commands."""

from __future__ import annotations

from typing import Optional

import typer  # type: ignore[import]

from ..utils import ensure_client, handle_raw_response, merge_params

ppi_app = typer.Typer(help="PPI endpoints")


@ppi_app.command("scores")
def ppi_scores(
    ctx: typer.Context,
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = ensure_client(ctx)
    response = client.raw_request("GET", "/api/ppi/scores/available", format=format)
    handle_raw_response(response, format, title="PPI score types")


@ppi_app.command("data-sources")
def ppi_data_sources(
    ctx: typer.Context,
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = ensure_client(ctx)
    response = client.raw_request("GET", "/api/ppi/data-sources", format=format)
    handle_raw_response(response, format, title="PPI data sources")


@ppi_app.command("string-network")
def ppi_string_network(
    ctx: typer.Context,
    locus_tag: Optional[str] = typer.Option(None, "--locus-tag"),
    pair_id: Optional[str] = typer.Option(None, "--pair-id"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    required_score: Optional[int] = typer.Option(None, "--required-score"),
    add_nodes: Optional[int] = typer.Option(None, "--add-nodes"),
    network_type: Optional[str] = typer.Option(None, "--network-type"),
    evidence_channels: Optional[str] = typer.Option(
        None,
        "--evidence-channels",
        help="Comma-separated STRING channels (e.g. experimental,database)",
    ),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = ensure_client(ctx)
    params = merge_params(
        {
            "locus_tag": locus_tag,
            "pair_id": pair_id,
            "species_acronym": species_acronym,
            "required_score": required_score,
            "add_nodes": add_nodes,
            "network_type": network_type,
            "evidence_channels": [
                c.strip() for c in evidence_channels.split(",") if c.strip()
            ]
            if evidence_channels
            else None,
        }
    )
    response = client.raw_request(
        "GET", "/api/ppi/string-network", params=params, format=format
    )
    handle_raw_response(response, format, title="STRING PPI network")


@ppi_app.command("interaction")
def ppi_interaction(
    ctx: typer.Context,
    pair_id: str = typer.Argument(
        ..., help="PPI pair ID (e.g. bu:A0A0X1ABC1__B0ABC123)"
    ),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    """Get a single PPI interaction by pair ID."""
    client = ensure_client(ctx)
    response = client.raw_request(
        "GET", f"/api/ppi/interactions/{pair_id}", format=format
    )
    handle_raw_response(response, format, title=f"PPI interaction ({pair_id})")


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
    client = ensure_client(ctx)
    params = merge_params(
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
    response = client.raw_request(
        "GET", "/api/ppi/interactions", params=params, format=format
    )
    handle_raw_response(response, format, title="PPI interactions")


@ppi_app.command("neighbors")
def ppi_neighbors(
    ctx: typer.Context,
    protein_id: Optional[str] = typer.Option(None, "--protein-id"),
    locus_tag: Optional[str] = typer.Option(None, "--locus-tag"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = ensure_client(ctx)
    params = merge_params(
        {
            "protein_id": protein_id,
            "locus_tag": locus_tag,
            "species_acronym": species_acronym,
        }
    )
    response = client.raw_request(
        "GET", "/api/ppi/neighbors", params=params, format=format
    )
    handle_raw_response(response, format, title="PPI neighbors")


@ppi_app.command("neighborhood")
def ppi_neighborhood(
    ctx: typer.Context,
    protein_id: Optional[str] = typer.Option(None, "--protein-id"),
    locus_tag: Optional[str] = typer.Option(None, "--locus-tag"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    n: Optional[int] = typer.Option(None, "--n"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = ensure_client(ctx)
    params = merge_params(
        {
            "protein_id": protein_id,
            "locus_tag": locus_tag,
            "species_acronym": species_acronym,
            "n": n,
        }
    )
    response = client.raw_request(
        "GET", "/api/ppi/neighborhood", params=params, format=format
    )
    handle_raw_response(response, format, title="PPI neighborhood")


@ppi_app.command("network")
def ppi_network(
    ctx: typer.Context,
    score_type: str = typer.Argument(...),
    score_threshold: Optional[float] = typer.Option(None, "--score-threshold"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    include_properties: Optional[bool] = typer.Option(None, "--include-properties"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = ensure_client(ctx)
    params = merge_params(
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
    handle_raw_response(response, format, title=f"PPI network ({score_type})")


@ppi_app.command("network-properties")
def ppi_network_properties(
    ctx: typer.Context,
    score_type: str = typer.Option(..., "--score-type"),
    score_threshold: Optional[float] = typer.Option(None, "--score-threshold"),
    species_acronym: Optional[str] = typer.Option(None, "--species", "-s"),
    format: Optional[str] = typer.Option(None, "--format", "-f"),
) -> None:
    client = ensure_client(ctx)
    params = merge_params(
        {
            "score_type": score_type,
            "score_threshold": score_threshold,
            "species_acronym": species_acronym,
        }
    )
    response = client.raw_request(
        "GET", "/api/ppi/network-properties", params=params, format=format
    )
    handle_raw_response(response, format, title="PPI network properties")
