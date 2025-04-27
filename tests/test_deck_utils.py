import json
import pytest
from src.cli.utils.deck_utils import load_deck, summarize_cards


@pytest.fixture
def tmp_json(tmp_path):
    def _make(data):
        p = tmp_path / "deck.json"
        p.write_text(json.dumps(data), encoding="utf-8")
        return p

    return _make


def test_load_deck_list(tmp_json):
    raw = [{"name": "A"}]
    path = tmp_json(raw)
    assert load_deck(path) == raw


def test_load_deck_with_cards(tmp_json):
    raw = {"cards": [{"name": "X"}]}
    path = tmp_json(raw)
    assert load_deck(path) == raw["cards"]


def test_load_deck_with_spells(tmp_json):
    raw = {"spells": [{"name": "Y"}]}
    path = tmp_json(raw)
    assert load_deck(path) == raw["spells"]


def test_load_deck_single_object(tmp_json):
    raw = {"name": "Solo"}
    path = tmp_json(raw)
    assert load_deck(path) == [raw]


def test_load_deck_invalid(tmp_json):
    path = tmp_json(123)
    with pytest.raises(ValueError):
        load_deck(path)


def test_summarize_cards_truncates(tmp_json):
    cards = [{"description": "abcdefghijKLMNOP"}]
    summarize_cards(cards, max_length=10)
    desc = cards[0]["description"]
    assert len(desc) <= 10
    assert cards[0]["desc"] == [desc]
