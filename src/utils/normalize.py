from pathlib import Path
import json


def normalize_art_urls(deck_path: Path) -> None:
    if not deck_path.exists():
        print(f"❌ File not found: {deck_path}")
        return

    try:
        text = deck_path.read_text(encoding="utf-8")
        data = json.loads(text)

        cards = data.get("cards", data)  # support list or dict format
        if not isinstance(cards, list):
            print(f"❌ Unexpected deck format in {deck_path}")
            return

        modified = False
        for card in cards:
            if "art_url" in card and isinstance(card["art_url"], str):
                original = card["art_url"]
                fixed = original.replace("\\", "/")
                if fixed != original:
                    card["art_url"] = fixed
                    modified = True

        if modified:
            # Write back with formatting
            if isinstance(data, dict):
                data["cards"] = cards
            else:
                data = cards
            deck_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            print(f"✅ Normalized art_url paths in: {deck_path}")
        else:
            print(f"ℹ️ No changes needed in: {deck_path}")

    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON in {deck_path}: {e}")


# Run on a sample path
sample_deck_path = Path("C:/Games/Hobbies/DnD/dmforge/decks/dev/wizard_0.json")
normalize_art_urls(sample_deck_path)
