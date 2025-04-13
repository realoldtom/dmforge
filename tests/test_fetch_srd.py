# tests/test_fetch_srd.py

import json
from src.fetch.srd import fetch_srd_spells
from unittest.mock import patch, Mock


def mock_index_response():
    return {
        "results": [
            {"index": "fireball", "url": "/api/spells/fireball"},
            {"index": "mage-hand", "url": "/api/spells/mage-hand"},
        ]
    }


def mock_spell_detail(index):
    return {
        "index": index,
        "name": index.title(),
        "level": 3,
        "school": {"name": "Evocation"},
        "classes": [{"name": "Wizard"}],
        "desc": ["A blazing sphere..."],
        "range": "150 feet",
        "duration": "Instantaneous",
        "components": ["V", "S", "M"],
        "casting_time": "1 action",
    }


@patch("src.fetch.srd.requests.get")
def test_fetch_srd_creates_cache(mock_get, tmp_path, monkeypatch):
    # Setup mocked responses
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: mock_index_response()),
        Mock(status_code=200, json=lambda: mock_spell_detail("fireball")),
        Mock(status_code=200, json=lambda: mock_spell_detail("mage-hand")),
    ]

    monkeypatch.setenv("DMFORGE_ENV", "test")
    monkeypatch.setattr(
        "src.fetch.srd.get_data_path", lambda filename: tmp_path / filename
    )

    fetch_srd_spells(force=True)

    # Assert file was created
    output_file = tmp_path / "spells.json"
    assert output_file.exists()

    data = json.loads(output_file.read_text())
    assert isinstance(data, list)
    assert any(spell["index"] == "fireball" for spell in data)

    spell = data[0]
    assert "level" in spell and isinstance(spell["level"], int)
    assert "classes" in spell and isinstance(spell["classes"], list)
    assert "desc" in spell and isinstance(spell["desc"], list)


@patch("src.fetch.srd.requests.get")
def test_fetch_skips_if_not_forced(mock_get, tmp_path, monkeypatch):
    monkeypatch.setenv("DMFORGE_ENV", "test")
    test_file = tmp_path / "spells.json"
    test_file.write_text("[]")  # simulate existing cache

    monkeypatch.setattr("src.fetch.srd.get_data_path", lambda filename: test_file)

    fetch_srd_spells(force=False)

    # No API call should have been made if file exists and not forced
    mock_get.assert_not_called()
