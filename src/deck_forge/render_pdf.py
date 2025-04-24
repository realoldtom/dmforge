# src/deck_forge/render_pdf.py

from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
import json
from src.utils.console import banner, success, error, warn

TEMPLATE_DIR = Path("templates")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def render_card_pdf(
    deck_path: Path, output_path: Path, theme: str = "default", debug: bool = False
):
    """Render a JSON deck to PDF using HTML + WeasyPrint."""
    banner("🖨 Rendering Card Deck (1 card/page)")

    if not deck_path.exists():
        error(f"❌ Deck not found: {deck_path}")
        return

    try:
        cards = json.loads(deck_path.read_text(encoding="utf-8"))

        css_file = Path(f"assets/css/{theme}.css")
        if not css_file.exists():
            warn(f"⚠️ Theme not found: {theme}. Using default.css.")
            css_file = Path("assets/css/default.css")
        css_path = css_file.absolute().as_uri()

        template = env.get_template("spell_card.jinja")
        html_string = template.render(cards=cards, css_path=css_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        if debug:
            debug_path = output_path.with_name(f"{output_path.stem}_debug.html")
            debug_path.write_text(html_string, encoding="utf-8")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            success(f"📝 Debug HTML saved to {debug_path.resolve()}")

        HTML(string=html_string).write_pdf(
            str(output_path), stylesheets=[CSS(css_path)]
        )
        success(f"✅ PDF saved to {output_path.resolve()}")

    except Exception as e:
        error(f"❌ Failed to render PDF: {e}")
        raise


def render_card_sheet_pdf(
    deck_path: Path, output_path: Path, theme: str = "default", debug: bool = False
):
    """Render a 6-card-per-page sheet for physical print."""
    banner("🖨 Rendering Card Grid Sheet")

    if not deck_path.exists():
        error(f"❌ Deck not found: {deck_path}")
        return

    try:
        cards = json.loads(deck_path.read_text(encoding="utf-8"))

        css_file = Path(f"assets/css/{theme}.css")
        if not css_file.exists():
            warn(f"⚠️ Theme not found: {theme}. Using default.css.")
            css_file = Path("assets/css/default.css")
        css_path = css_file.absolute().as_uri()

        template = env.get_template("spell_sheet.jinja")
        html_string = template.render(cards=cards, css_path=css_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        if debug:
            debug_path = output_path.with_name(f"{output_path.stem}_debug.html")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            debug_path.write_text(html_string, encoding="utf-8")
            success(f"📝 Debug HTML saved to {debug_path.resolve()}")

        HTML(string=html_string).write_pdf(
            str(output_path), stylesheets=[CSS(css_path)]
        )
        success(f"✅ Sheet PDF saved to {output_path.resolve()}")

    except Exception as e:
        error(f"❌ Failed to render sheet: {e}")
        raise
