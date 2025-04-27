# src/utils/deck_utils.py

import json
from pathlib import Path
from src.utils.summarizer import summarize_text


def load_deck(path: Path) -> list:
    """Load deck JSON, returning a list of card dicts."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("cards", "spells"):
            if key in data and isinstance(data[key], list):
                return data[key]
        return [data]
    raise ValueError("Unexpected deck JSON format: root must be list or dict")


def summarize_cards(cards: list, max_length: int):
    """Rewrite each card’s description to a summarized form."""
    for card in cards:
        raw = card.get("description") or card.get("desc") or ""
        raw_text = " ".join(raw) if isinstance(raw, list) else raw
        summary = summarize_text(raw_text, max_length=max_length)
        card["desc"] = [summary]
        card["description"] = summary
