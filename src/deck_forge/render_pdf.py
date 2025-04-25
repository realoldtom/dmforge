from pathlib import Path
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from src.utils.console import banner, success, error, warn
from src.utils.formatting import abbreviate_duration

TEMPLATE_DIR = Path("templates")
ASSETS_DIR = Path("assets")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def resolve_image_path(path_str, base_dir):
    """Convert relative paths to absolute file URIs."""
    if not path_str or path_str.startswith(("http://", "https://", "file://")):
        return path_str

    # Handle relative paths
    path = Path(path_str)
    if not path.is_absolute():
        # Try multiple resolution strategies
        potential_paths = [(base_dir / path).resolve(), (Path.cwd() / path).resolve()]

        # Use the first path that exists
        for potential_path in potential_paths:
            if potential_path.exists():
                print(f"✓ Found image at: {potential_path}")
                return potential_path.as_uri()

        # If we got here, no path worked
        warn(f"⚠️ Image not found: {path} (tried {len(potential_paths)} locations)")
        return None

    # Handle absolute paths
    if not path.exists():
        warn(f"⚠️ Image not found: {path}")
        return None

    # Return as file URI
    return path.as_uri()


def process_cards(cards, base_dir):
    """Process all cards to ensure image paths are properly resolved."""
    print(f"Base directory for image resolution: {base_dir.absolute()}")
    print(f"Current working directory: {Path.cwd().absolute()}")

    for card in cards:
        if "art_url" in card:
            original_path = card["art_url"]
            card["art_url"] = resolve_image_path(card["art_url"], base_dir)

            # Enhanced debugging
            print(f"Card '{card.get('title', 'Untitled')}':")
            print(f"  → Original path: {original_path}")
            print(f"  → Resolved to: {card['art_url'] or 'FAILED'}")

        # Process art versions if present
        if "art_versions" in card:
            for version in card["art_versions"]:
                if "path" in version:
                    original_path = version["path"]
                    version["path"] = resolve_image_path(version["path"], base_dir)
                    print(f"  → Art version '{version.get('tag', 'Unknown')}':")
                    print(f"    → Original path: {original_path}")
                    print(f"    → Resolved to: {version['path'] or 'FAILED'}")


def load_deck(deck_path):
    """Load and parse the deck file, handling both list and dict formats."""
    if not deck_path.exists():
        error(f"❌ Deck not found: {deck_path}")
        return None

    try:
        content = deck_path.read_text(encoding="utf-8")
        data = json.loads(content)

        # Handle both formats: {"cards": [...]} or just [...]
        if isinstance(data, dict) and "cards" in data:
            return data["cards"]
        elif isinstance(data, list):
            return data
        else:
            error(
                "❌ Invalid deck format: expected list of cards or object with 'cards' property"
            )
            return None
    except Exception as e:
        error(f"❌ Failed to load deck: {e}")
        return None


def get_css_path(theme):
    """Get the absolute URI path to the CSS file."""
    css_file = ASSETS_DIR / "css" / f"{theme}.css"
    if not css_file.exists():
        warn(f"⚠️ Theme not found: {theme}. Using default.css.")
        css_file = ASSETS_DIR / "css" / "default.css"

    return css_file.absolute().as_uri()


def render_card_pdf(
    deck_path: Path, output_path: Path, theme: str = "default", debug: bool = False
):
    """Render a JSON deck to PDF using HTML + WeasyPrint (one card per page)."""
    banner("🖨 Rendering Card Deck (1 card/page)")

    # Load deck
    cards = load_deck(deck_path)
    if not cards:
        return

    try:
        # Process cards to resolve image paths
        process_cards(cards, base_dir=deck_path.parent)

        for c in cards:
            # ---- Title fallback ----
            c["title"] = c.get("title") or c.get("name", "Untitled")

            # ---- Level / school one-liner (optional) ----
            lvl = "Cantrip" if c.get("level", 0) == 0 else f"L{c['level']}"
            sch = c.get("school", "")[:3].upper()  # EVO, ABJ, etc.
            c["level_school"] = f"{lvl}·{sch}"

            # ---- Duration abbreviation ----
            if "duration" in c:
                c["duration_short"] = abbreviate_duration(c["duration"])

                # --- Clean components ---
                if isinstance(c.get("components"), list):
                    # ['V', 'S', 'M']  ->  "V,S,M"
                    c["components_short"] = ",".join(c["components"])
                else:
                    c["components_short"] = c.get("components", "")

        # Get CSS path
        css_path = get_css_path(theme)

        # Generate HTML
        template = env.get_template("spell_card.jinja")
        html_string = template.render(
            cards=cards,
            css_path=css_path,
            default_image="assets/images/placeholder.png",
        )

        # Save debug HTML if requested
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if debug:
            debug_path = output_path.with_suffix(".html")
            debug_path.write_text(html_string, encoding="utf-8")
            success(f"📝 Debug HTML saved to {debug_path.resolve()}")

            # Also save a paths debug file
            paths_debug = "\n".join(
                [
                    f"{card.get('title', 'Untitled')}: {card.get('art_url', 'No image')}"
                    for card in cards
                ]
            )
            path_debug_file = output_path.with_name(
                f"{output_path.stem}_paths_debug.txt"
            )
            path_debug_file.write_text(paths_debug, encoding="utf-8")
            success(f"📝 Paths debug saved to {path_debug_file.resolve()}")

        # Render PDF
        HTML(string=html_string, base_url=str(ASSETS_DIR)).write_pdf(
            str(output_path), stylesheets=[CSS(css_path)]
        )
        success(f"✅ PDF saved to {output_path.resolve()}")

    except Exception as e:
        error(f"❌ Failed to render PDF: {e}")
        if debug:
            import traceback

            error(traceback.format_exc())


def render_card_sheet_pdf(
    deck_path: Path, output_path: Path, theme: str = "default", debug: bool = False
):
    """Render cards as a sheet/grid in PDF format."""
    banner("📄 Rendering Sheet PDF")

    # Load deck
    cards = load_deck(deck_path)
    if not cards:
        return

    try:
        # Process cards to resolve image paths
        process_cards(cards, base_dir=deck_path.parent)

        for c in cards:
            # ---- Title fallback ----
            c["title"] = c.get("title") or c.get("name", "Untitled")

            # ---- Level / school one-liner (optional) ----
            lvl = "Cantrip" if c.get("level", 0) == 0 else f"L{c['level']}"
            sch = c.get("school", "")[:3].upper()  # EVO, ABJ, etc.
            c["level_school"] = f"{lvl}·{sch}"

            # ---- Duration abbreviation ----
            if "duration" in c:
                c["duration_short"] = abbreviate_duration(c["duration"])

            # --- Clean components ---
            if isinstance(c.get("components"), list):
                # ['V', 'S', 'M']  ->  "V,S,M"
                c["components_short"] = ",".join(c["components"])
            else:
                c["components_short"] = c.get("components", "")

        # Get CSS path
        css_path = get_css_path(theme)

        # Generate HTML
        template = env.get_template("spell_sheet.jinja")
        html_string = template.render(
            cards=cards,
            css_path=css_path,
            default_image="assets/images/placeholder.png",
        )

        # Save debug HTML if requested
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if debug:
            debug_path = output_path.with_suffix(".html")
            debug_path.write_text(html_string, encoding="utf-8")
            success(f"📝 Debug HTML saved to {debug_path.resolve()}")

            # Also save a paths debug file
            paths_debug = "\n".join(
                [
                    f"{card.get('title', 'Untitled')}: {card.get('art_url', 'No image')}"
                    for card in cards
                ]
            )
            path_debug_file = output_path.with_name(
                f"{output_path.stem}_paths_debug.txt"
            )
            path_debug_file.write_text(paths_debug, encoding="utf-8")
            success(f"📝 Paths debug saved to {path_debug_file.resolve()}")

        # Render PDF
        HTML(string=html_string).write_pdf(
            str(output_path), stylesheets=[CSS(css_path)]
        )
        success(f"✅ Sheet PDF saved to {output_path.resolve()}")

    except Exception as e:
        error(f"❌ Failed to render sheet PDF: {e}")
        if debug:
            import traceback

            error(traceback.format_exc())


def render_all(
    deck_path: Path, output_dir: Path, theme: str = "default", debug: bool = False
):
    """Render both card PDF and sheet PDF from a single deck."""
    banner("🎴 Rendering All PDF Formats")

    output_dir.mkdir(parents=True, exist_ok=True)
    deck_name = deck_path.stem

    card_pdf = output_dir / f"{deck_name}_cards.pdf"
    sheet_pdf = output_dir / f"{deck_name}_sheet.pdf"

    render_card_pdf(deck_path, card_pdf, theme, debug)
    render_card_sheet_pdf(deck_path, sheet_pdf, theme, debug)

    success(f"✅ All PDFs rendered to {output_dir.resolve()}")


def diagnose_image_paths(deck_path):
    """Just check all image paths in a deck without rendering."""
    banner("🔍 Diagnosing Image Paths")

    cards = load_deck(deck_path)
    if not cards:
        return

    print(f"Found {len(cards)} cards in {deck_path}")
    base_dir = deck_path.parent

    for card in cards:
        title = card.get("title", "Untitled")
        print(f"\n--- Card: {title} ---")

        if "art_url" in card:
            path_str = card["art_url"]
            print(f"Original path: {path_str}")

            # Try resolving with different base directories
            test_bases = [
                ("Deck directory", base_dir),
                ("Current directory", Path.cwd()),
                ("Parent of current", Path.cwd().parent),
                ("Root of project", Path.cwd().resolve().parents[1]),
            ]

            for name, test_base in test_bases:
                if not path_str.startswith(("http://", "https://", "file://")):
                    path = Path(path_str)
                    if not path.is_absolute():
                        test_path = (test_base / path).resolve()
                        exists = test_path.exists()
                        print(f"  {name}: {test_path} {'✓' if exists else '✗'}")


if __name__ == "__main__":
    # Command-line parsing would go here if this is used as a standalone script
    pass
