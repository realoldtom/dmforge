# src/cli/deck.py

import typer
from pathlib import Path
from typing import Optional
from src.utils.console import banner, error, success
from src.deck_forge.generate import generate_spell_deck
from src.deck_forge.render_pdf import render_card_pdf, render_card_sheet_pdf
from src.deck_forge.render_html import render_card_html

deck_app = typer.Typer(name="deck", help="Generate and render spell card decks")


@deck_app.command("build")
def build(
    output: str = typer.Option("deck.json", "--output", help="Output file name"),
    limit: Optional[int] = typer.Option(
        None, "--limit", "-n", help="Only build the first N spells"
    ),
):
    """Build a full SRD spell deck."""
    banner("🧱 Generating Spell Card Deck")
    deck_path = generate_spell_deck(output_name=output, limit=limit)
    if not deck_path:
        error("❌ Deck generation failed.")
        raise typer.Exit(1)
    success(f"✅ Deck saved to {deck_path.resolve()}")


@deck_app.command("render")
def render(
    deck_file: Path = typer.Argument(..., help="Deck JSON file to render"),
    format: str = typer.Option("pdf", "--format", help="Output format (pdf or html)"),
    layout: str = typer.Option("sheet", "--layout", help="Layout: sheet or cards"),
    output: Optional[str] = typer.Option(None, "--output", help="Output file path"),
    theme: str = typer.Option("default", "--theme", help="Theme to use"),
    debug: bool = typer.Option(
        False, "--debug", help="Also write raw HTML for inspection"
    ),
):
    """Render a deck to PDF or HTML."""
    banner("🎨 Rendering Deck")
    deck_path = Path(deck_file)
    if not deck_path.exists():
        error(f"❌ Deck not found: {deck_path}")
        raise typer.Exit(1)

    out_path = Path(output) if output else Path(f"deck.{format}")

    try:
        if format == "pdf":
            if layout == "sheet":
                render_card_sheet_pdf(deck_path, out_path, theme, debug)
            else:
                render_card_pdf(deck_path, out_path, theme, debug)
            # for PDFs, we still want the raw HTML if debug
            if debug:
                dbg = deck_path.parent / f"{deck_path.stem}_debug.html"
                render_card_html(deck_path, dbg, theme)

        elif format == "html":
            render_card_html(deck_path, out_path, theme)
            if debug:
                dbg = deck_path.parent / f"{deck_path.stem}_debug.html"
                render_card_html(deck_path, dbg, theme)

        else:
            error("❌ Unsupported format.")
            raise typer.Exit(1)

    except Exception as e:
        error(f"❌ Failed to render deck: {e}")
        raise typer.Exit(1)

    success("✅ Deck rendered successfully")
