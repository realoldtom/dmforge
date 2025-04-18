import json
from pathlib import Path

import pytest

DECK_PATH = Path("decks/dev/full_deck.json")


@pytest.fixture
def deck_data():
    """Load and parse the full deck file."""
    assert DECK_PATH.exists(), f"Deck not found: {DECK_PATH}"
    raw = json.loads(DECK_PATH.read_text(encoding="utf-8"))

    cards = raw["cards"] if isinstance(raw, dict) and "cards" in raw else raw
    assert isinstance(cards, list) and len(cards) > 0, "Deck has no cards"
    return cards


def test_deck_card_structure(deck_data):
    required_fields = ["title", "level", "school", "description"]

    for card in deck_data:
        for field in required_fields:
            assert field in card, f"Missing field: {field}"
            assert card[field] not in (None, "", []), f"{field} is empty"

        assert isinstance(card["level"], int), "Level must be an integer"
        assert isinstance(card["title"], str), "Title must be a string"


def test_deck_card_count(deck_data):
    assert len(deck_data) >= 50, "Expected at least 50 cards in full deck"
