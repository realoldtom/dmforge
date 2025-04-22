# tests/test_deck_interactive.py

import json
from src.deck_forge.generate import generate_spell_deck

sample_spells = [
    {
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
    },
    {
        "index": "cure-wounds",
        "name": "Cure Wounds",
        "level": 1,
        "school": "Evocation",
        "classes": ["Cleric", "Druid"],
        "components": ["V", "S"],
        "range": "Touch",
        "duration": "Instantaneous",
        "casting_time": "1 action",
        "desc": ["A creature you touch regains hit points..."],
    },
]


def test_generate_deck_with_class_and_level_filter(tmp_path, monkeypatch):
    # Write test data
    spell_file = tmp_path / "spells.json"
    spell_file.write_text(json.dumps(sample_spells), encoding="utf-8")

    # Patch data source and env
    monkeypatch.setattr("src.deck_forge.generate.get_data_path", lambda _: spell_file)
    monkeypatch.setattr("src.deck_forge.generate.get_env", lambda: "test")
    monkeypatch.chdir(tmp_path)

    # Run generator with filters
    output_file = tmp_path / "decks" / "test" / "filtered.json"
    result = generate_spell_deck(
        output_name=str(output_file),
        class_filter="Wizard",
        level_filter="3",
        school_filter=None,
        limit=None,
        interactive=False,
    )

    assert result is not None
    assert output_file.exists()

    data = json.loads(output_file.read_text())
    assert "cards" in data
    assert len(data["cards"]) == 1
    assert data["cards"][0]["title"] == "Fireball"
