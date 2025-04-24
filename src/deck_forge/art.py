import os
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional
from src.utils.console import banner, success, error, warn

API_URL = "https://api.openai.com/v1/images/generations"
MODEL = "dall-e-3"
DEFAULT_SIZE = "512x512"


def generate_art_for_deck(
    deck_path: Path,
    art_dir: Path,
    size: str = DEFAULT_SIZE,
    n_per_card: int = 1,
    prompt_suffix: Optional[str] = None,
    character_style: Optional[str] = None,
    version: str = "v1",
):
    banner("🎨 Generating Card Art with DALL·E (versioning enabled)")

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
        filename = f"{title.replace(' ', '_')}_{version}.png"
        out_path = art_dir / filename

        if out_path.exists():
            warn(f"⏭️ Skipping existing: {filename}")
            continue

        prompt = (
            f"Fantasy artwork of the spell '{title}', from a tabletop RPG. "
            f"Depict a magical scene representing a level {card['level']} {card['school']} spell. "
            f"Include dramatic lighting, detailed environment, and cinematic style. "
        )
        if character_style:
            prompt += f" Show a {character_style} casting the spell. "
        prompt += f"Focus on the spell's effects: {card['description']}. "
        if prompt_suffix:
            prompt += f"{prompt_suffix} "
        prompt += "Use a painterly look inspired by ArtStation and Wizards of the Coast illustrations."

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

            relative_path = (Path("../../assets/art") / filename).as_posix()
            art_info = {
                "tag": version,
                "path": relative_path,
                "prompt": prompt,
            }

            # Add or update art_versions field
            card.setdefault("art_versions", []).append(art_info)
            card["art_url"] = relative_path  # default image path

            print(f"✅ Updating art_url for {title}: {relative_path}")
            success(f"→ {title}: image saved to {filename}")

        except Exception as e:
            error(f"❌ {title}: Exception while generating art: {e}")

    updated = {"cards": cards} if isinstance(raw, dict) else cards
    deck_path.write_text(json.dumps(updated, indent=2), encoding="utf-8")
    success(f"✅ All art generated and deck updated at {deck_path}")
