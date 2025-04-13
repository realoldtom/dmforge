import typer
from pathlib import Path
from src.deck_forge.generate import generate_spell_deck
from src.deck_forge.render_html import render_card_html  # <-- import this after typer

deck_app = typer.Typer(help="Generate and render spell decks.")  # ✅ define this first


@deck_app.command("build")
def build(
    output: str = typer.Option(
        "full_spell_deck.json", "--output", help="Output JSON filename"
    ),
    limit: int = typer.Option(None, "--limit", help="Limit number of cards"),
):
    """Build a full card deck from SRD spells."""
    generate_spell_deck(output_name=output, limit=limit)


@deck_app.command("render")
def render(
    deck_path: str = typer.Argument(..., help="Path to JSON deck file"),
    output: str = typer.Option("deck.html", "--output", help="Output HTML file"),
    format: str = typer.Option(
        "html", "--format", help="Render format: html (default)"
    ),
):
    """Render a deck into HTML or other formats (PDF/image coming soon)."""
    if format == "html":
        render_card_html(Path(deck_path), Path(output))
    else:
        typer.echo("❌ Only 'html' format is supported at this stage.")
