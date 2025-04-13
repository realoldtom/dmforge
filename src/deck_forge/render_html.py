# src/deck_forge/render_html.py

"""Render card layout to HTML using Jinja2 templates."""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.utils.console import banner, success, error
import json

TEMPLATE_DIR = Path("templates")

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "jinja"]),
)


def render_card_html(deck_path: Path, output_path: Path):
    """Render cards from JSON deck to a single HTML page."""
    banner("🖼 Rendering Card Deck to HTML")

    if not deck_path.exists():
        error(f"❌ Deck file not found: {deck_path}")
        return

    try:
        cards = json.loads(deck_path.read_text(encoding="utf-8"))
        css_path = Path("assets/css/default.css").absolute().as_uri()
        template = env.get_template("spell_card.jinja")

        html_string = template.render(cards=cards, css_path=css_path)
        output_path.write_text(html_string, encoding="utf-8")

        success(f"✅ HTML output saved to {output_path.resolve()}")

    except Exception as e:
        error(f"❌ Failed to render HTML: {e}")
        raise
