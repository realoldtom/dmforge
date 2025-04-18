"""Repair double-encoded JSON spell data."""

import json
from src.utils.paths import get_data_path
from src.utils.console import banner, success, error, warn


def repair_spell_data():
    """Fix double-encoded JSON in spells.json."""
    banner("🔧 Repairing Spell Data")

    spells_file = get_data_path("spells.json")
    if not spells_file.exists():
        error("❌ Spells file not found - run 'fetch srd --spells' first")
        return

    try:
        # Load potentially corrupted data
        data = json.loads(spells_file.read_text(encoding="utf-8"))

        # Check if we have string-encoded spells
        if isinstance(data, list) and any(isinstance(s, str) for s in data):
            warn("Found string-encoded spells, repairing...")

            # Decode each spell string back to dict
            fixed = []
            for i, spell in enumerate(data):
                try:
                    if isinstance(spell, str):
                        fixed.append(json.loads(spell))
                    else:
                        fixed.append(spell)
                except json.JSONDecodeError:
                    error(f"❌ Failed to decode spell at index {i}")
                    return

            # Save fixed data
            spells_file.write_text(json.dumps(fixed, indent=2), encoding="utf-8")
            success(f"✅ Repaired {len(fixed)} spells")
        else:
            success("✅ Spell data is in correct format")

    except Exception as e:
        error(f"❌ Failed to repair spell data: {e}")


if __name__ == "__main__":
    repair_spell_data()
