import logging
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import os
import base64
import mimetypes

# ——— Logging setup —————————————————————————————————————————————————————
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ——— Project root & placeholder ——————————————————————————————————————
PROJECT_ROOT = Path(__file__).parent.parent.parent
logger.info(f"🔎 Project root: {PROJECT_ROOT.resolve()}")


def _load_placeholder_data_uri(project_root: Path) -> str:
    ph = project_root / "assets" / "images" / "placeholder.png"
    if not ph.exists():
        logger.warning(f"Placeholder image not found at {ph}")
        return ""
    data = ph.read_bytes()
    mime = mimetypes.guess_type(str(ph))[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


PLACEHOLDER_DATA_URI = _load_placeholder_data_uri(PROJECT_ROOT)


# ——— Image‐path fixer ———————————————————————————————————————————————————
def _fix_image_paths(cards: list[dict], project_root: Path, output_dir: Path):
    for card in cards:
        url = card.get("art_url") or ""
        if not url:
            card["art_url"] = PLACEHOLDER_DATA_URI
            continue

        # normalize
        url = url.replace("\\", "/").lstrip("/")

        # skip external or data URIs
        if url.startswith(("http://", "https://", "data:", "file://")):
            if url.startswith("file://"):
                p = url.replace("file://", "")
                if os.name == "nt" and p.startswith("/"):
                    p = p[1:]
                card["art_url"] = Path(p).resolve().as_uri()
            continue

        # disk lookup
        image_path = (project_root / url).resolve()
        if not image_path.exists():
            logger.warning(f"Image not found: {image_path}")
            # try versioned fallback
            stem, ext = image_path.stem, image_path.suffix
            versions = sorted(image_path.parent.glob(f"{stem}_v*{ext}"))
            if versions:
                image_path = versions[0]
                logger.info(f"✓ Found versioned image: {image_path}")
            else:
                card["art_url"] = PLACEHOLDER_DATA_URI
                continue

        # embed small, else relative link
        try:
            size = image_path.stat().st_size
            if size < 100_000:
                mime = mimetypes.guess_type(str(image_path))[0] or "image/png"
                data = image_path.read_bytes()
                card["art_url"] = (
                    f"data:{mime};base64,{base64.b64encode(data).decode()}"
                )
                logger.info(f"✓ Embedded image as data URI: {image_path.name}")
            else:
                rel = os.path.relpath(image_path, output_dir).replace("\\", "/")
                card["art_url"] = rel
                logger.info(f"✓ Using relative path: {rel}")
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {e}")
            card["art_url"] = PLACEHOLDER_DATA_URI


# ——— HTML renderer —————————————————————————————————————————————————————
def render_card_html(deck_path: Path, output_path: Path, theme: str = "default"):
    logger.info("🖼 Rendering Card Deck to HTML")

    if not deck_path.exists():
        logger.error(f"❌ Deck file not found: {deck_path}")
        return

    try:
        data = json.loads(deck_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            if "cards" not in data:
                logger.error("❌ 'cards' key missing in JSON file.")
                return
            cards = data["cards"]
        elif isinstance(data, list):
            cards = data
        else:
            logger.error("❌ JSON root must be a dict with a 'cards' key or a list.")
            return

        if not cards:
            logger.warning("⚠️ No cards found in input.")
        else:
            logger.info(f"📦 Loaded {len(cards)} cards from {deck_path}")

        logger.info(f"Loaded {len(cards)} cards from {deck_path}")

        _fix_image_paths(cards, PROJECT_ROOT, output_path.parent)

        # CSS
        css_file = PROJECT_ROOT / "assets" / "css" / f"{theme}.css"
        if not css_file.exists():
            logger.warning(f"Theme not found: {theme}. Using default.css.")
            css_file = PROJECT_ROOT / "assets" / "css" / "default.css"
        css_path = os.path.relpath(css_file, output_path.parent).replace("\\", "/")

        # Jinja environment pointing at <project_root>/templates
        env = Environment(
            loader=FileSystemLoader(PROJECT_ROOT / "templates"),
            autoescape=select_autoescape(["html", "jinja"]),
        )
        template = env.get_template("spell_card.jinja")
        html = template.render(
            cards=cards,
            css_path=css_path,
            default_image=PLACEHOLDER_DATA_URI,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(html, encoding="utf-8")
        logger.info(f"✅ HTML output saved to {output_path.resolve()}")

    except Exception as e:
        logger.error(f"❌ Failed to render HTML: {e}")
        raise
