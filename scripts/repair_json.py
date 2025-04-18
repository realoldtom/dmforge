import json
from pathlib import Path
from src.utils.console import banner, success, error, warn


def repair_spells_json():
    """Repair and validate the spells JSON file."""
    banner("🔧 Repairing Spells JSON")
    spells_file = Path("data/dev/spells.json")

    if not spells_file.exists():
        error("❌ Spells file not found")
        return

    try:
        # Load the corrupted JSON
        print("📖 Loading spell data...")
        with open(spells_file, encoding="utf-8") as f:
            data = f.read()

        # Parse full spell entries
        print("🔍 Parsing JSON structure...")
        raw_spells = json.loads(data)
        print(f"Found {len(raw_spells)} raw entries")

        # Filter out incomplete entries
        print("✨ Filtering valid spells...")
        spells = []
        required_fields = ["index", "name", "level", "school", "classes"]

        for i, spell in enumerate(raw_spells, 1):
            if isinstance(spell, dict) and all(key in spell for key in required_fields):
                spells.append(spell)
            else:
                warn(f"Skipping invalid spell at position {i}")

        if not spells:
            error("❌ No valid spells found!")
            return

        # Write back clean JSON
        print("💾 Saving cleaned data...")
        spells_file.write_text(json.dumps(spells, indent=2), encoding="utf-8")

        success(f"✅ Successfully repaired {len(spells)} spell entries")

    except json.JSONDecodeError as e:
        error(f"❌ JSON parsing error: {e}")
    except Exception as e:
        error(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    repair_spells_json()
