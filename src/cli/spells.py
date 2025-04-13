# src/cli/deck.py

import typer

deck_app = typer.Typer(help="Deck building commands")


@deck_app.command("build")
def build_deck():
    """Build a deck from class, level, or custom input (placeholder)."""
    typer.echo("🃏 Building deck (placeholder)...")
