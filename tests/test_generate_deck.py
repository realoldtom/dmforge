# tests/test_generate_deck.py

import json
from src.deck_forge.generate import generate_spell_deck

sample_spell = {
    "index": "fireball",
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


def test_generate_spell_deck_writes_json(tmp_path, monkeypatch):
    # Setup fake input file
    spell_file = tmp_path / "spells.json"
    spell_file.write_text(json.dumps([sample_spell]), encoding="utf-8")

    monkeypatch.setattr("src.deck_forge.generate.get_data_path", lambda _: spell_file)
    monkeypatch.setattr("src.deck_forge.generate.get_env", lambda: "test")
    monkeypatch.chdir(tmp_path)

    generate_spell_deck(output_name="test_deck.json")

    output_file = tmp_path / "decks" / "test" / "test_deck.json"
    assert output_file.exists()

    deck = json.loads(output_file.read_text())
    assert isinstance(deck, list)
    assert deck[0]["title"] == "Fireball"
    assert deck[0]["description"].startswith("A bright streak")


def test_generate_spell_deck_limit(tmp_path, monkeypatch):
    spells = [
        dict(sample_spell, index=f"spell-{i}", name=f"Spell {i}") for i in range(10)
    ]
    spell_file = tmp_path / "spells.json"
    spell_file.write_text(json.dumps(spells), encoding="utf-8")

    monkeypatch.setattr("src.deck_forge.generate.get_data_path", lambda _: spell_file)
    monkeypatch.setattr("src.deck_forge.generate.get_env", lambda: "test")
    monkeypatch.chdir(tmp_path)

    generate_spell_deck(output_name="limited_deck.json", limit=5)

    deck_file = tmp_path / "decks" / "test" / "limited_deck.json"
    deck = json.loads(deck_file.read_text())
    assert len(deck) == 5
