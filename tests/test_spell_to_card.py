"""Tests for spell-to-card schema conversion."""

from src.deck_forge.schema import spell_to_card

# Test data
valid_spell = {
    "index": "fireball",
    "name": "Fireball",
    "level": 3,
    "school": "Evocation",
    "classes": ["Wizard"],
    "desc": ["A bright streak flashes..."],
    "range": "150 feet",
    "duration": "Instantaneous",
    "components": ["V", "S", "M"],
    "casting_time": "1 action",
}


def test_spell_to_card_maps_fields():
    """Test that spell fields map correctly to card fields."""
    card = spell_to_card(valid_spell)
    assert card is not None

    # Check required fields
    assert card["title"] == "Fireball"
    assert card["level"] == 3
    assert card["school"] == "Evocation"
    assert card["description"].startswith("A bright streak")
    assert card["source"] == "SRD"

    # Check optional fields
    assert card["casting_time"] == "1 action"
    assert card["duration"] == "Instantaneous"
    assert card["range"] == "150 feet"
    assert card["components"] == ["V", "S", "M"]

    # Check art URL
    assert card["art_url"].startswith("https://")


def test_spell_to_card_handles_missing_fields():
    """Test that missing optional fields get defaults."""
    minimal_spell = {
        "name": "Magic Pebble",
        "level": 0,
        "school": "Transmutation",
        "desc": ["Throw a rock."],
    }

    card = spell_to_card(minimal_spell)
    assert card is not None
    assert card["title"] == "Magic Pebble"
    assert card["level"] == 0
    assert card["school"] == "Transmutation"
    assert card["description"] == "Throw a rock."
    assert card["casting_time"] == "1 action"
    assert card["duration"] == "Instantaneous"
    assert card["range"] == "Self"
    assert card["components"] == []
    assert card["source"] == "SRD"


def test_spell_to_card_invalid_input():
    """Test handling of invalid inputs."""
    assert spell_to_card(None) is None
    assert spell_to_card({}) is None
    assert spell_to_card("not a dict") is None

    # Missing required fields
    incomplete_spell = {"name": "Test"}
    assert spell_to_card(incomplete_spell) is None
