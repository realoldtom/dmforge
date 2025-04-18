"""Deck generation and rendering commands."""

from pathlib import Path
import typer
from src.utils.console import banner, error, success, warn
from src.deck_forge.render_pdf import render_card_pdf, render_card_sheet_pdf
from src.deck_forge.render_html import render_card_html
from src.deck_forge.generate import generate_spell_deck as build_deck

deck_app = typer.Typer(help="Generate and render spell card decks")


@deck_app.command()
def build(
    output: str = typer.Option("deck.json", "--output", help="Output file name"),
) -> None:
    """Build a full SRD spell deck and validate against schema."""
    try:
        deck_path = build_deck(output_name=output)  # alias for generate_spell_deck()
        if not deck_path:
            error("❌ Deck generation failed.")
            return

        success(f"✅ Deck saved to {deck_path.resolve()}")

        # Schema validation (auto-run)
        from jsonschema import Draft7Validator
        import json

        SCHEMA_PATH = Path("schemas/deck.schema.json")
        if not SCHEMA_PATH.exists():
            warn("⚠️  Skipped schema check – schema file missing.")
            return

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        data = json.loads(deck_path.read_text(encoding="utf-8"))

        validator = Draft7Validator(schema)
        errors = list(validator.iter_errors(data))

        if errors:
            for err in errors:
                loc = ".".join([str(x) for x in err.path])
                warn(f"❌ {loc}: {err.message}")
            error("❌ Deck failed schema validation.")
            return

        success("✅ Deck passed schema validation")

    except Exception as e:
        error(f"❌ Failed to build deck: {e}")


@deck_app.command()
def render(
    deck_file: Path = typer.Argument(..., help="Deck JSON file to render"),
    format: str = typer.Option("pdf", "--format", help="Output format (pdf or html)"),
    layout: str = typer.Option("sheet", "--layout", help="Layout type: sheet or cards"),
    output: str = typer.Option(None, "--output", help="Output file path"),
    theme: str = typer.Option("default", "--theme", help="Theme to use for layout"),
    debug: bool = typer.Option(
        False, "--debug", help="Also write raw HTML for inspection"
    ),
) -> None:
    """Render a deck to PDF or HTML."""
    banner("🎨 Rendering Deck")

    try:
        deck_path = Path(deck_file)
        output_path = Path(output) if output else Path(f"deck.{format}")

        if format == "pdf":
            if layout == "sheet":
                render_card_sheet_pdf(deck_path, output_path, theme, debug)
            else:
                render_card_pdf(deck_path, output_path, theme, debug)
        elif format == "html":
            render_card_html(deck_path, output_path, theme)
        else:
            error("❌ Unsupported format.")
            return

        success("✅ Deck rendered successfully")

    except Exception as e:
        error(f"❌ Failed to render deck: {e}")
