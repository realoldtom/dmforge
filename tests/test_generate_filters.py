import json
import pytest
from pathlib import Path
from src.deck_forge.generate import generate_spell_deck


sample_spells = [
    {
        "index": "acid-arrow",
        "name": "Acid Arrow",
        "level": 2,
        "school": "Evocation",
        "classes": ["Wizard"],
        "components": ["V", "S", "M"],
        "range": "90 feet",
        "duration": "Instantaneous",
        "casting_time": "1 action",
        "desc": ["A green arrow streaks toward a target..."],
    },
    {
        "index": "bless",
        "name": "Bless",
        "level": 1,
        "school": "Enchantment",
        "classes": ["Cleric", "Paladin"],
        "components": ["V", "S", "M"],
        "range": "30 feet",
        "duration": "1 minute",
        "casting_time": "1 action",
        "desc": ["You bless up to three creatures..."],
    },
    {
        "index": "mage-hand",
        "name": "Mage Hand",
        "level": 0,
        "school": "Conjuration",
        "classes": ["Wizard", "Sorcerer"],
        "components": ["V", "S"],
        "range": "30 feet",
        "duration": "1 minute",
        "casting_time": "1 action",
        "desc": ["A spectral hand appears..."],
    },
]


@pytest.fixture
def spell_file(tmp_path):
    path = tmp_path / "spells.json"
    path.write_text(json.dumps(sample_spells), encoding="utf-8")
    return path


@pytest.fixture(autouse=True)
def patch_data_path(monkeypatch, spell_file):
    monkeypatch.setattr("src.deck_forge.generate.get_data_path", lambda _: spell_file)


def test_filter_by_class(tmp_path):
    result = generate_spell_deck(
        output_name=tmp_path / "deck.json",
        class_filter="cleric",
    )
    cards = json.loads(Path(result).read_text())["cards"]
    assert all("Cleric" in c["title"] or "Bless" in c["title"] for c in cards)
    assert len(cards) == 1


def test_filter_by_level(tmp_path):
    result = generate_spell_deck(
        output_name=tmp_path / "deck.json",
        level_filter="0",
    )
    cards = json.loads(Path(result).read_text())["cards"]
    assert any("Mage Hand" in c["title"] for c in cards)
    assert all(c["level"] == 0 for c in cards)
    assert len(cards) == 1


def test_filter_by_school(tmp_path):
    result = generate_spell_deck(
        output_name=tmp_path / "deck.json",
        school_filter="conjuration",
    )
    cards = json.loads(Path(result).read_text())["cards"]
    assert all(c["school"].lower() == "conjuration" for c in cards)
    assert len(cards) == 1


def test_combined_filters(tmp_path):
    result = generate_spell_deck(
        output_name=tmp_path / "deck.json",
        class_filter="wizard",
        level_filter="2",
        school_filter="evocation",
    )
    cards = json.loads(Path(result).read_text())["cards"]
    assert len(cards) == 1
    assert cards[0]["title"] == "Acid Arrow"
