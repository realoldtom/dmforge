# src/deck_forge/generate.py

"""Generate renderable card decks from spell data."""

import json
from pathlib import Path
from typing import Optional, List, Dict, Any

from src.utils.paths import get_data_path
from src.utils.env import get_env
from src.utils.console import banner, success, error, warn
from src.deck_forge.schema import spell_to_card


def validate_and_repair_spells(data: Any) -> List[Dict[str, Any]]:
    """Clean and validate spell data during import."""
    required_fields = ["index", "name", "level", "school", "classes"]
    valid_spells = []

    # Handle potential string-encoded JSON
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            warn("Invalid JSON string in data")
            return []

    # Ensure we have a list of spells
    if not isinstance(data, list):
        warn(f"Expected list of spells, got {type(data)}")
        return []

    # Process each spell
    for spell in data:
        try:
            # Handle string-encoded spells
            if isinstance(spell, str):
                spell = json.loads(spell)

            # Validate and normalize
            if isinstance(spell, dict):
                # Ensure all required fields exist
                if not all(key in spell for key in required_fields):
                    warn(
                        f"Skipping spell missing required fields: {spell.get('name', 'UNKNOWN')}"
                    )
                    continue

                # Normalize the spell data
                normalized = {
                    "index": str(spell["index"]),
                    "name": str(spell["name"]),
                    "level": int(spell["level"]),
                    "school": (
                        spell["school"]
                        if isinstance(spell["school"], str)
                        else spell["school"].get("name", "Unknown")
                    ),
                    "classes": (
                        [str(c) for c in spell["classes"]]
                        if isinstance(spell["classes"], list)
                        else [spell["classes"]]
                    ),
                    "desc": (
                        spell.get("desc", [])
                        if isinstance(spell.get("desc"), list)
                        else [str(spell.get("desc", "No description"))]
                    ),
                    "range": str(spell.get("range", "Self")),
                    "duration": str(spell.get("duration", "Instantaneous")),
                    "components": spell.get("components", []),
                    "casting_time": str(spell.get("casting_time", "1 action")),
                }
                valid_spells.append(normalized)

        except (json.JSONDecodeError, TypeError, ValueError) as e:
            warn(f"Failed to process spell: {e}")
            continue

    if not valid_spells:
        warn("No valid spells found after validation")
    else:
        success(f"Validated {len(valid_spells)} spells")

    return valid_spells


def generate_spell_deck(
    output_name: str = "full_deck.json", limit: Optional[int] = None
) -> Optional[Path]:
    """Generate a deck of spell cards from SRD data."""
    banner("🧱 Generating Spell Card Deck")

    input_file = get_data_path("spells.json")
    if not input_file.exists():
        error("❌ Missing SRD data - run 'fetch srd --spells' first")
        return None

    try:
        # Load and repair data
        raw_data = json.loads(input_file.read_text(encoding="utf-8"))
        spells = validate_and_repair_spells(raw_data)

        if not spells:
            error("❌ No valid spells found")
            return None

        # Apply optional limit
        if limit:
            spells = spells[:limit]
            warn(f"Limited to first {limit} spells")

        # Generate cards with error handling
        cards = []
        for spell in spells:
            if card := spell_to_card(spell):
                cards.append(card)
            else:
                warn(f"Skipped invalid spell: {spell.get('name', 'UNKNOWN')}")

        if not cards:
            error("❌ No valid cards generated")
            return None

        # Save deck file
        env = get_env()
        output_dir = Path("decks") / env
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / output_name

        output_file.write_text(json.dumps({"cards": cards}, indent=2), encoding="utf-8")
        success(f"✅ Generated {len(cards)} cards in {output_file.resolve()}")
        return output_file

    except Exception as e:
        error(f"❌ Failed to generate deck: {str(e)}")
        return None
