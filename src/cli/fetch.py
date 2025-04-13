"""Data fetching commands."""

import typer

fetch_app = typer.Typer(help="Fetch D&D 5e content from sources.")


@fetch_app.command()
def srd(ctx: typer.Context):
    """Fetch core SRD content."""
    env = ctx.obj["env"]
    typer.echo(f"Fetching SRD data in {env} mode...")
