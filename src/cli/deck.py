"""Deck generation and rendering commands."""

from pathlib import Path
import typer
from src.utils.console import banner, error, success
from src.deck_forge.render_pdf import render_card_pdf, render_card_sheet_pdf
from src.deck_forge.render_html import render_card_html
from src.deck_forge.generate import generate_spell_deck as build_deck

deck_app = typer.Typer(help="Generate and render spell card decks")


@deck_app.command()
def build(
    spells: str = typer.Option(
        None, "--spells", help="Spells to include (comma-separated)"
    ),
    all_spells: bool = typer.Option(
        False, "--all", help="Include all available spells"
    ),
    output: str = typer.Option("deck.json", "--output", help="Output file name"),
) -> None:
    """Build a deck JSON file from selected spells."""
    if not (spells or all_spells):
        error("No spells selected. Use --spells or --all")
        return

    try:
        deck = build_deck(
            spell_list=spells.split(",") if spells else None, all_spells=all_spells
        )
        output_path = Path(output)
        output_path.write_text(deck, encoding="utf-8")
        success(f"✅ Deck saved to {output_path}")
    except Exception as e:
        error(f"Failed to build deck: {e}")


@deck_app.command()
def render(
    deck_file: Path = typer.Argument(..., help="Deck JSON file to render"),
    format: str = typer.Option("pdf", "--format", help="Output format (pdf or html)"),
    layout: str = typer.Option(
        "sheet", "--layout", help="Layout type: 'sheet' or 'cards'"
    ),
    output: str = typer.Option(None, "--output", help="Output file path"),
):
    """Render a deck to PDF or HTML."""
    banner("🎨 Rendering Deck")

    try:
        # Set default output filename
        if output is None:
            output = "deck.pdf" if format == "pdf" else "deck.html"

        deck_path = Path(deck_file)
        output_path = Path(output)

        if format == "pdf":
            if layout == "sheet":
                render_card_sheet_pdf(deck_path, output_path)
            else:
                render_card_pdf(deck_path, output_path)

        elif format == "html":
            render_card_html(deck_path, output_path)

        else:
            raise ValueError("Unsupported format. Use 'pdf' or 'html'.")

        success("✅ Deck rendered successfully")

    except Exception as e:
        error(f"❌ Failed to render deck: {e}")
