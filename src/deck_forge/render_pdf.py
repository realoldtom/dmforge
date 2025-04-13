# src/deck_forge/render_pdf.py

"""Render deck to PDF using WeasyPrint and the spell card HTML template."""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import json
from src.utils.console import banner, success, error

TEMPLATE_DIR = Path("templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def render_card_pdf(deck_path: Path, output_path: Path):
    """Render a JSON deck to PDF using HTML + WeasyPrint."""
    banner("🖨 Rendering Card Deck to PDF")

    if not deck_path.exists():
        error(f"❌ Deck not found: {deck_path}")
        return

    try:
        cards = json.loads(deck_path.read_text(encoding="utf-8"))
        template = env.get_template("spell_card.jinja")
        html_string = template.render(cards=cards)

        HTML(string=html_string).write_pdf(str(output_path))

        success(f"✅ PDF saved to {output_path.resolve()}")

    except Exception as e:
        error(f"❌ Failed to render PDF: {e}")
        raise


def render_card_sheet_pdf(deck_path: Path, output_path: Path):
    """Render a 6-card-per-page sheet for physical print."""
    banner("🖨 Rendering Grid Sheet (6 cards/page)")

    if not deck_path.exists():
        error(f"❌ Deck not found: {deck_path}")
        return

    try:
        cards = json.loads(deck_path.read_text(encoding="utf-8"))
        template = env.get_template("spell_sheet.jinja")
        html_string = template.render(cards=cards)

        HTML(string=html_string).write_pdf(str(output_path))
        success(f"✅ Sheet PDF saved to {output_path.resolve()}")

    except Exception as e:
        error(f"❌ Failed to render sheet: {e}")
        raise
