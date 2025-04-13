# src/deck_forge/schema.py

"""Spell-to-card schema converter for layout rendering."""


def spell_to_card(spell: dict) -> dict:
    """Convert SRD spell dict to standardized card schema for layout/rendering."""
    return {
        "title": spell.get("name", "Unnamed Spell"),
        "level": spell.get("level", 0),
        "school": spell.get("school", "Unknown"),
        "classes": spell.get("classes", []),
        "components": spell.get("components", []),
        "range": spell.get("range", "Unknown"),
        "duration": spell.get("duration", "Unknown"),
        "casting_time": spell.get("casting_time", "Unknown"),
        "description": " ".join(spell.get("desc", [])),
        "tags": [],  # Reserved for later enhancements
        "source": "SRD",
    }
