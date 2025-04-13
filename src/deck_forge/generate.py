# src/deck_forge/generate.py

"""Generate renderable card decks from spell data."""

import json
from pathlib import Path
from src.utils.paths import get_data_path
from src.utils.env import get_env
from src.utils.console import banner, success, error
from src.deck_forge.schema import spell_to_card


def generate_spell_deck(
    output_name: str = "full_spell_deck.json", limit: int = None
) -> None:
    """Convert SRD spells into layout-ready card deck (JSON format)."""
    banner("🧱 Generating Spell Card Deck")

    input_file = get_data_path("spells.json")
    if not input_file.exists():
        error(f"❌ Missing SRD spell data: {input_file}")
        return

    try:
        spells = json.loads(input_file.read_text(encoding="utf-8"))
        if limit:
            spells = spells[:limit]

        cards = [spell_to_card(spell) for spell in spells]

        env = get_env()
        output_dir = Path("decks") / env
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / output_name
        output_file.write_text(json.dumps(cards, indent=2), encoding="utf-8")

        success(f"✅ Wrote {len(cards)} cards to {output_file.resolve()}")

    except Exception as e:
        error(f"❌ Failed to generate deck: {e}")
        raise
