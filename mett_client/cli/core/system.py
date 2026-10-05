"""System and metadata CLI commands."""

from __future__ import annotations

from typing import Optional

import typer  # type: ignore[import]

from ..utils import ensure_client, handle_raw_response

system_app = typer.Typer(help="System / metadata endpoints")


@system_app.command("releases")
def system_releases(
    ctx: typer.Context,
    format: Optional[str] = typer.Option(None, "--format", "-f", help="json|tsv"),
) -> None:
    """List scientist-visible METT data releases."""
    client = ensure_client(ctx)
    response = client.raw_request("GET", "/api/releases", format=format)
    handle_raw_response(response, format, title="Releases")
