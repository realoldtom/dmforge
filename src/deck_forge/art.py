import os
import json
import requests
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from src.utils.console import banner, success
from src.utils.formatting import spell_effect_snippet
from src.utils.prompt_utils import build_spell_prompt

API_URL = "https://api.openai.com/v1/images/generations"
MODEL = "dall-e-3"
DEFAULT_SIZE = "1024x1024"


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
        print(f"❌ Deck not found: {deck_path}", file=sys.stderr)
        return

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("❌ OPENAI_API_KEY not set.", file=sys.stderr)
        return

    raw = json.loads(deck_path.read_text(encoding="utf-8"))
    cards = (
        raw.get("cards")
        if isinstance(raw, dict)
        else raw if isinstance(raw, list) else []
    )

    if not cards:
        print("❌ No cards found in deck.", file=sys.stderr)
        return

    art_dir.mkdir(parents=True, exist_ok=True)

    for card in cards:
        title = card["title"]
        filename = f"{title.replace(' ', '_')}_{version}.png"
        out_path = art_dir / filename

        # 1)  Create a short, cinematic effect phrase from the raw SRD text
        effect = spell_effect_snippet(card.get("description", ""))

        # 2)  Build the final prompt with optional style / suffix
        prompt = build_spell_prompt(
            title=title,
            description=effect,
            character_style=character_style,
            prompt_suffix=prompt_suffix,
        )

        if out_path.exists():
            print(f"⏭️ Skipping existing: {filename}", file=sys.stderr)
            # IMPORTANT CHANGE: Make sure we're recording the versioned path even for skipped images
            relative_path = (Path("assets/art") / filename).as_posix()
            art_info = {
                "tag": version,
                "path": relative_path,
                "prompt": prompt,
            }
            card.setdefault("art_versions", []).append(art_info)
            card["art_url"] = relative_path  # Use versioned path
            continue

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
                print(f"❌ Failed to generate art for {title}", file=sys.stderr)
                print(f"   → Status: {response.status_code}", file=sys.stderr)
                print(f"   → Error: {response.text}", file=sys.stderr)
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                debug_path = (
                    art_dir / f"{title.replace(' ', '_')}_error_{timestamp}.json"
                )
                debug_path.write_text(response.text, encoding="utf-8")
                continue

            image_url = response.json()["data"][0]["url"]
            img_bytes = requests.get(image_url).content
            out_path.write_bytes(img_bytes)

            relative_path = (Path("assets/art") / filename).as_posix()
            art_info = {
                "tag": version,
                "path": relative_path,
                "prompt": prompt,
            }

            card.setdefault("art_versions", []).append(art_info)
            card["art_url"] = relative_path  # default image path

            print(f"✅ Updating art_url for {title}: {relative_path}")
            success(f"→ {title}: image saved to {filename}")

        except Exception as e:
            print(f"❌ {title}: Exception while generating art: {e}", file=sys.stderr)

    updated = {"cards": cards} if isinstance(raw, dict) else cards
    deck_path.write_text(json.dumps(updated, indent=2), encoding="utf-8")
    success(f"✅ All art generated and deck updated at {deck_path}")
