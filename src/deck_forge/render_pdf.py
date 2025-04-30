from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS
from src.utils.console import banner, success, error, warn
from src.utils.formatting import abbreviate_duration
from src.deck_forge.render_html import PLACEHOLDER_DATA_URI

# Directories
PROJECT_ROOT = Path(__file__).parent.parent.parent
TEMPLATE_DIR = PROJECT_ROOT / "templates"
ASSETS_DIR = PROJECT_ROOT / "assets"

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "jinja"]),
)


def resolve_image_path(path_str: str, base_dir: Path) -> str:
    """Convert relative or versioned paths to file URIs or data URIs."""
    if not path_str:
        return PLACEHOLDER_DATA_URI
    if path_str.startswith(("http://", "https://", "data:", "file://")):
        return path_str

    # Try relative to deck folder then to assets
    candidates = [
        (base_dir / path_str).resolve(),
        (ASSETS_DIR / path_str).resolve(),
    ]
    for p in candidates:
        if p.exists():
            return p.as_uri()

    warn(f"⚠️ Image not found: {path_str} (tried {len(candidates)} locations)")
    return PLACEHOLDER_DATA_URI


def load_deck(deck_path: Path) -> list[dict]:
    """Load JSON deck, supporting both list and dict formats."""
    if not deck_path.exists():
        error(f"❌ Deck not found: {deck_path}")
        return []
    data = json.loads(deck_path.read_text(encoding="utf-8"))
    return (
        data.get("cards")
        if isinstance(data, dict)
        else (data if isinstance(data, list) else [])
    )


def get_css_path(theme: str) -> str:
    """Return the CSS file URI for a given theme."""
    css_file = ASSETS_DIR / "css" / f"{theme}.css"
    if not css_file.exists():
        warn(f"⚠️ Theme '{theme}' not found; using default.css")
        css_file = ASSETS_DIR / "css" / "default.css"
    return css_file.as_uri()


def process_cards(cards: list[dict], base_dir: Path):
    """Resolve all art_url entries to URIs."""
    for card in cards:
        original = card.get("art_url", "")
        card["art_url"] = resolve_image_path(original, base_dir)
        # log troubleshooting
        if card["art_url"] == PLACEHOLDER_DATA_URI:
            warn(
                f"Card '{card.get('name','')}': art_url '{original}' resolved to placeholder"
            )


def render_card_pdf(
    deck_path: Path,
    output_path: Path,
    theme: str = "default",
    debug: bool = False,
):
    banner("🖨 Rendering Card Deck (1 per page)")
    cards = load_deck(deck_path)
    if not cards:
        return

    from src.deck_forge.render_html import (
        _fix_image_paths,
        PROJECT_ROOT,
        PLACEHOLDER_DATA_URI,
    )

    # After loading `cards` from JSON:
    _fix_image_paths(cards, PROJECT_ROOT, output_path.parent)

    # Prepare data
    process_cards(cards, base_dir=deck_path.parent)
    for c in cards:
        c["title"] = c.get("title") or c.get("name", "Untitled")
        lvl = "Cantrip" if c.get("level", 0) == 0 else f"L{c['level']}"
        sch = c.get("school", "").upper()[:3]
        c["level_school"] = f"{lvl}·{sch}"
        if "duration" in c:
            c["duration_short"] = abbreviate_duration(c["duration"])
        c["components_short"] = (
            ",".join(c.get("components", []))
            if isinstance(c.get("components"), list)
            else c.get("components", "")
        )

    # Load template
    template = env.get_template("spell_card.jinja")
    html_string = template.render(
        cards=cards,
        css_path=get_css_path(theme),
        default_image=PLACEHOLDER_DATA_URI,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if debug:
        dbg = output_path.with_suffix(".html")
        dbg.write_text(html_string, encoding="utf-8")
        success(f"📝 Debug HTML: {dbg.resolve()}")

    # Render PDF with correct base_url for assets
    base = str(output_path.parent.resolve())
    HTML(string=html_string, base_url=base).write_pdf(
        str(output_path), stylesheets=[CSS(get_css_path(theme))]
    )
    success(f"✅ PDF saved: {output_path.resolve()}")


def render_card_sheet_pdf(
    deck_path: Path,
    output_path: Path,
    theme: str = "default",
    debug: bool = False,
):
    banner("📄 Rendering Sheet PDF (6 per page)")
    cards = load_deck(deck_path)
    if not cards:
        return

    from src.deck_forge.render_html import (
        _fix_image_paths,
        PROJECT_ROOT,
        PLACEHOLDER_DATA_URI,
    )

    # After loading `cards` from JSON:
    _fix_image_paths(cards, PROJECT_ROOT, output_path.parent)

    process_cards(cards, base_dir=deck_path.parent)
    for c in cards:
        c["title"] = c.get("title") or c.get("name", "Untitled")
        lvl = "Cantrip" if c.get("level", 0) == 0 else f"L{c['level']}"
        sch = c.get("school", "").upper()[:3]
        c["level_school"] = f"{lvl}·{sch}"
        if "duration" in c:
            c["duration_short"] = abbreviate_duration(c["duration"])
        c["components_short"] = (
            ",".join(c.get("components", []))
            if isinstance(c.get("components"), list)
            else c.get("components", "")
        )

    template = env.get_template("spell_sheet.jinja")
    html_string = template.render(
        cards=cards,
        css_path=get_css_path(theme),
        default_image=PLACEHOLDER_DATA_URI,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if debug:
        dbg = output_path.with_suffix(".html")
        dbg.write_text(html_string, encoding="utf-8")
        success(f"📝 Debug HTML: {dbg.resolve()}")

    base = str(output_path.parent.resolve())
    HTML(string=html_string, base_url=base).write_pdf(
        str(output_path), stylesheets=[CSS(get_css_path(theme))]
    )
    success(f"✅ Sheet PDF saved: {output_path.resolve()}")
