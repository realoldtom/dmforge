import json
import pytest
import typer
from pathlib import Path

import src.deck_forge.generate as G


# A simple stub for spell_to_card to ensure cards always generate
@pytest.fixture(autouse=True)
def patch_spell_to_card(monkeypatch):
    def stub_spell_to_card(spell):
        return {
            "title": spell.get("name", spell.get("index")),
            "level": spell.get("level"),
            "school": spell.get("school"),
        }

    monkeypatch.setattr(G, "spell_to_card", stub_spell_to_card)


@pytest.fixture
def spell_file(tmp_path):
    path = tmp_path / "spells.json"
    path.write_text(json.dumps([]), encoding="utf-8")
    return path


@pytest.fixture(autouse=True)
def patch_data_path_and_cwd(monkeypatch, spell_file, tmp_path):
    # Point get_data_path to our fixture, and work in tmp_path
    monkeypatch.setattr(G, "get_data_path", lambda _: spell_file)
    monkeypatch.chdir(tmp_path)


def test_fetch_srd_spells_no_file(tmp_path, monkeypatch, capsys):
    missing = tmp_path / "nope.json"
    monkeypatch.setattr(G, "get_data_path", lambda _: missing)
    spells = G.fetch_srd_spells()
    assert spells == []
    out = capsys.readouterr().out
    assert "❌ spells.json not found" in out


def test_generate_spell_deck_empty(monkeypatch):
    monkeypatch.setattr(G, "fetch_srd_spells", lambda: [])
    assert G.generate_spell_deck(output_name="deck.json") is None


def test_generate_spell_deck_no_match(spell_file, capsys):
    spells = [{"index": "x", "name": "X", "level": 1, "school": "S", "classes": ["A"]}]
    spell_file.write_text(json.dumps(spells), encoding="utf-8")
    result = G.generate_spell_deck(output_name="deck.json", class_filter="nope")
    assert result is None
    out = capsys.readouterr().out
    assert "❌ No matching spells found." in out


def test_generate_spell_deck_limit(spell_file):
    spells = [
        {"index": f"i{i}", "name": f"N{i}", "level": 0, "school": "S", "classes": []}
        for i in range(5)
    ]
    spell_file.write_text(json.dumps(spells), encoding="utf-8")
    path = G.generate_spell_deck(output_name="deck.json", limit=2)
    deck = json.loads(Path(path).read_text())
    assert len(deck["cards"]) == 2


def test_generate_spell_deck_filters(spell_file):
    spells = [
        {"index": "a", "name": "A", "level": 1, "school": "X", "classes": ["C"]},
        {"index": "b", "name": "B", "level": 2, "school": "Y", "classes": ["D"]},
    ]
    spell_file.write_text(json.dumps(spells), encoding="utf-8")
    path = G.generate_spell_deck(
        output_name="deck.json", class_filter="C", level_filter="1", school_filter="X"
    )
    deck = json.loads(Path(path).read_text())
    assert len(deck["cards"]) == 1
    assert deck["cards"][0]["title"] == "A"


def test_generate_spell_deck_interactive_good(spell_file, monkeypatch):
    spells = [
        {"index": "a", "name": "A", "level": 0, "school": "S", "classes": []},
        {"index": "b", "name": "B", "level": 0, "school": "S", "classes": []},
    ]
    spell_file.write_text(json.dumps(spells), encoding="utf-8")
    monkeypatch.setattr(typer, "prompt", lambda msg: "2")
    path = G.generate_spell_deck(output_name="deck.json", interactive=True)
    deck = json.loads(Path(path).read_text())
    assert len(deck["cards"]) == 1
    assert deck["cards"][0]["title"] == "B"


def test_generate_spell_deck_interactive_bad(spell_file, monkeypatch, capsys):
    spells = [
        {"index": "a", "name": "A", "level": 0, "school": "S", "classes": []},
        {"index": "b", "name": "B", "level": 0, "school": "S", "classes": []},
    ]
    spell_file.write_text(json.dumps(spells), encoding="utf-8")
    monkeypatch.setattr(typer, "prompt", lambda msg: "foo")
    result = G.generate_spell_deck(output_name="deck.json", interactive=True)
    assert result is None
    out = capsys.readouterr().out
    assert "❌ Invalid input" in out


def test_deck_json_structure(spell_file):
    spells = [{"index": "x", "name": "X", "level": 0, "school": "S", "classes": []}]
    spell_file.write_text(json.dumps(spells), encoding="utf-8")
    path = G.generate_spell_deck(output_name="deck.json")
    deck = json.loads(Path(path).read_text())
    assert set(deck.keys()) == {"cards"}
    card = deck["cards"][0]
    assert {"title", "level", "school"}.issubset(card.keys())
