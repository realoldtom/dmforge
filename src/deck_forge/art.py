import os
import json
import requests
from pathlib import Path
from datetime import datetime
from src.utils.console import banner, success, error, warn

API_URL = "https://api.openai.com/v1/images/generations"
MODEL = "dall-e-3"
DEFAULT_SIZE = "512x512"


def generate_art_for_deck(
    deck_path: Path,
    art_dir: Path,
    size: str = DEFAULT_SIZE,
    n_per_card: int = 1,
):
    banner("🎨 Generating Card Art with DALL·E (API fallback)")

    if not deck_path.exists():
        error(f"❌ Deck not found: {deck_path}")
        return

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        error("❌ OPENAI_API_KEY not set.")
        return

    raw = json.loads(deck_path.read_text(encoding="utf-8"))
    cards = (
        raw.get("cards")
        if isinstance(raw, dict)
        else raw if isinstance(raw, list) else []
    )
    if not cards:
        error("❌ No cards found in deck.")
        return

    art_dir.mkdir(parents=True, exist_ok=True)

    for card in cards:
        title = card["title"]
        filename = f"{title.replace(' ', '_')}.png"
        out_path = art_dir / filename

        if out_path.exists():
            warn(f"⏭️ Skipping existing: {filename}")
            continue

        prompt = (
            f"Fantasy artwork of the spell '{title}', from a tabletop RPG. "
            f"Depict a magical scene representing a level {card['level']} {card['school']} spell. "
            f"Include dramatic lighting, detailed environment, and cinematic style. "
            f"Focus on the spell's effects {card['description']} and the character casting it. "
            f"Use a painterly look inspired by ArtStation and Wizards of the Coast illustrations."
        )

        try:
            response = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "n": n_per_card,
                    "size": size,
                },
                timeout=60,
            )

            if response.status_code != 200:
                warn(f"❌ Failed to generate art for {title}")
                warn(f"   → Status: {response.status_code}")
                warn(f"   → Error: {response.text}")

                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                debug_path = (
                    art_dir / f"{title.replace(' ', '_')}_error_{timestamp}.json"
                )
                debug_path.write_text(response.text, encoding="utf-8")
                continue

            image_url = response.json()["data"][0]["url"]
            img_bytes = requests.get(image_url).content
            out_path.write_bytes(img_bytes)

            card["art_url"] = str(out_path.resolve())
            success(f"→ {title}: image saved to {out_path.name}")

        except Exception as e:
            error(f"❌ {title}: Exception while generating art: {e}")

    updated = {"cards": cards} if isinstance(raw, dict) else cards
    deck_path.write_text(json.dumps(updated, indent=2), encoding="utf-8")
    success(f"✅ All art generated and deck updated at {deck_path}")
