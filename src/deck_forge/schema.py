# src/deck_forge/schema.py

"""Spell-to-card schema converter for layout rendering."""

import random
from typing import Dict, Any, Optional
from src.utils.console import warn


def spell_to_card(spell: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Convert a raw spell dictionary to a card-ready format."""
    try:
        # Validate required fields
        if not isinstance(spell, dict):
            return None

        required = ["name", "level", "school"]
        if not all(key in spell for key in required):
            return None

        # Required fields with type conversion
        card = {
            "title": spell["name"].title(),  # Call the method
            "level": int(spell["level"]),
            "school": str(spell["school"]),
            "description": (
                " ".join(spell["desc"])
                if isinstance(spell["desc"], list)
                else str(spell.get("desc", "No description"))
            ),
            "source": "SRD",
        }

        # Optional fields with defaults
        card.update(
            {
                "casting_time": str(spell.get("casting_time", "1 action")),
                "duration": str(spell.get("duration", "Instantaneous")),
                "range": str(spell.get("range", "Self")),
                "components": list(spell.get("components", [])),
            }
        )

        # Random placeholder art
        card["art_url"] = random.choice(
            [
                "https://placekitten.com/300/180",
                "https://placebear.com/300/180",
                "https://picsum.photos/300/180",
            ]
        )

        return card

    except Exception as e:
        warn(f"Failed to convert spell '{spell.get('name', 'UNKNOWN')}': {e}")
        return None
