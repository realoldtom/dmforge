# src/deck_forge/render_html.py

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.utils.console import banner, success, error, warn
import json

TEMPLATE_DIR = Path("templates")
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "jinja"]),
)


def render_card_html(deck_path: Path, output_path: Path, theme: str = "default"):
    """Render cards from JSON deck to a single HTML page."""
    banner("🖼 Rendering Card Deck to HTML")

    if not deck_path.exists():
        error(f"❌ Deck file not found: {deck_path}")
        return

    try:
        cards_data = json.loads(deck_path.read_text(encoding="utf-8"))

        if isinstance(cards_data, dict) and "cards" in cards_data:
            cards = cards_data["cards"]
        else:
            cards = cards_data  # fallback if already a list

        css_file = Path(f"assets/css/{theme}.css")
        if not css_file.exists():
            warn(f"⚠️ Theme not found: {theme}. Using default.css.")
            css_file = Path("assets/css/default.css")

        css_path = css_file.absolute().as_uri()

        # Adjust image paths relative to output HTML file
        for card in cards:
            if "art_url" in card:
                try:
                    art_path = Path(card["art_url"])
                    if not art_path.is_absolute():
                        art_path = Path.cwd() / art_path
                    relative_path = art_path.relative_to(output_path.parent)
                    card["art_url"] = relative_path.as_posix()
                except Exception:
                    warn(f"⚠️ Could not adjust path for {card.get('title')}")

        template = env.get_template("spell_card.jinja")
        default_image = "https://placebear.com/300/180"

        html_string = template.render(
            cards=cards, css_path=css_path, default_image=default_image
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html_string, encoding="utf-8")

        success(f"✅ HTML output saved to {output_path.resolve()}")

    except Exception as e:
        error(f"❌ Failed to render HTML: {e}")
        raise
