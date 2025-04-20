# src/deck_forge/schema.py

import random
from typing import Dict, Any, Optional
from src.utils.console import warn
import src.utils.summarizer as summarizer
from src.utils.summarizer import MAX_CHAR_COUNT


def spell_to_card(
    spell: Dict[str, Any], summarize: bool = True
) -> Optional[Dict[str, Any]]:
    """Convert a raw spell dictionary to a card-ready format, summarizing if needed."""
    try:
        if not isinstance(spell, dict):
            return None

        # Required
        for key in ("name", "level", "school", "desc"):
            if key not in spell:
                return None

        full_desc = (
            " ".join(spell["desc"])
            if isinstance(spell["desc"], list)
            else str(spell["desc"])
        )
        was_summarized = len(full_desc) > MAX_CHAR_COUNT
        final_desc = summarizer.summarize_text(full_desc) if summarize else full_desc

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
