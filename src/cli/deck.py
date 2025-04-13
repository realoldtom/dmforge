"""Deck generation commands."""

import typer

deck_app = typer.Typer(help="Generate spell cards and decks.")


@deck_app.command()
def create(ctx: typer.Context):
    """Create a new card deck."""
    env = ctx.obj["env"]
    typer.echo(f"Creating deck in {env} mode...")
