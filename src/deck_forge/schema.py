# src/deck_forge/schema.py

import random
from typing import Dict, Any, Optional
from src.utils.console import warn
from src.utils.summarizer import summarize_text, MAX_CHAR_COUNT


def spell_to_card(
    spell: Dict[str, Any], summarize: bool = True
) -> Optional[Dict[str, Any]]:
    """Convert a raw spell dictionary to a card-ready format."""
    try:
        if not isinstance(spell, dict):
            return None

        required = ["name", "level", "school"]
        if not all(key in spell for key in required):
            return None

        # Handle long descriptions with summarization
        desc_raw = spell.get("desc", [])
        full_desc = " ".join(desc_raw) if isinstance(desc_raw, list) else str(desc_raw)
        was_summarized = len(full_desc) > MAX_CHAR_COUNT
        final_desc = summarize_text(full_desc)

        card = {
            "title": spell["name"].title(),
            "level": int(spell["level"]),
            "school": str(spell["school"]),
            "description": final_desc,
            "summary": was_summarized,
            "casting_time": str(spell.get("casting_time", "1 action")),
            "duration": str(spell.get("duration", "Instantaneous")),
            "range": str(spell.get("range", "Self")),
            "components": list(spell.get("components", [])),
            "source": "SRD",
            "art_url": random.choice(
                [
                    "https://placekitten.com/300/180",
                    "https://placebear.com/300/180",
                    "https://picsum.photos/300/180",
                ]
            ),
        }

        return card

    except Exception as e:
        warn(f"Failed to convert spell '{spell.get('name', 'UNKNOWN')}': {e}")
        return None
