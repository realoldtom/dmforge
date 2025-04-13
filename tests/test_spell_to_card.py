# tests/test_spell_to_card.py

from src.deck_forge.schema import spell_to_card

sample_spell = {
    "name": "Fireball",
    "level": 3,
    "school": "Evocation",
    "classes": ["Wizard", "Sorcerer"],
    "components": ["V", "S", "M"],
    "range": "150 feet",
    "duration": "Instantaneous",
    "casting_time": "1 action",
    "desc": ["A bright streak flashes from your pointing finger..."],
}


def test_spell_to_card_maps_fields():
    card = spell_to_card(sample_spell)
    assert card["title"] == "Fireball"
    assert card["level"] == 3
    assert card["school"] == "Evocation"
    assert "Wizard" in card["classes"]
    assert "V" in card["components"]
    assert "150 feet" in card["range"]
    assert "1 action" in card["casting_time"]
    assert "A bright streak" in card["description"]
    assert card["source"] == "SRD"
    assert isinstance(card["tags"], list)


def test_spell_to_card_handles_missing_fields():
    minimal_spell = {"name": "Magic Pebble", "desc": ["Throw a rock."]}
    card = spell_to_card(minimal_spell)
    assert card["level"] == 0
    assert card["school"] == "Unknown"
    assert card["classes"] == []
    assert card["components"] == []
    assert card["range"] == "Unknown"
    assert card["duration"] == "Unknown"
    assert card["casting_time"] == "Unknown"
    assert card["source"] == "SRD"
