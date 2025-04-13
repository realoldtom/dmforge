"""Deck generation commands."""

import typer
from src.utils.console import banner

deck_app = typer.Typer(help="Generate spell cards and decks.")


@deck_app.command()
def create(ctx: typer.Context):
    """Create a new card deck."""
    env = ctx.obj["env"]
    banner("Creating Deck", f"Environment: {env}")
