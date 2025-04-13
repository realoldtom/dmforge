# tests/test_fetch_srd.py

import json
from src.fetch.srd import fetch_srd_spells
from src.fetch.srd import fetch_srd_traits
from src.fetch.srd import fetch_srd_features
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


def mock_trait_index():
    return {
        "results": [
            {"index": "darkvision", "url": "/api/traits/darkvision"},
            {"index": "dwarven-toughness", "url": "/api/traits/dwarven-toughness"},
        ]
    }


def mock_trait_detail(index):
    return {
        "index": index,
        "name": index.replace("-", " ").title(),
        "desc": [f"This is the {index} trait."],
    }


@patch("src.fetch.srd.requests.get")
def test_fetch_traits_creates_file(mock_get, tmp_path, monkeypatch):
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: mock_trait_index()),
        Mock(status_code=200, json=lambda: mock_trait_detail("darkvision")),
        Mock(status_code=200, json=lambda: mock_trait_detail("dwarven-toughness")),
    ]

    monkeypatch.setenv("DMFORGE_ENV", "test")
    monkeypatch.setattr(
        "src.fetch.srd.get_data_path", lambda filename: tmp_path / filename
    )

    fetch_srd_traits(force=True)

    traits_file = tmp_path / "traits.json"
    assert traits_file.exists()
    data = json.loads(traits_file.read_text())
    assert isinstance(data, list)
    assert data[0]["index"] == "darkvision"


@patch("src.fetch.srd.requests.get")
def test_traits_skipped_if_not_forced(mock_get, tmp_path, monkeypatch):
    monkeypatch.setenv("DMFORGE_ENV", "test")
    test_file = tmp_path / "traits.json"
    test_file.write_text("[]")  # simulate existing file

    monkeypatch.setattr("src.fetch.srd.get_data_path", lambda filename: test_file)

    fetch_srd_traits(force=False)

    mock_get.assert_not_called()


def mock_feature_index():
    return {
        "results": [
            {"index": "channel-divinity", "url": "/api/features/channel-divinity"},
            {"index": "rage", "url": "/api/features/rage"},
        ]
    }


def mock_feature_detail(index):
    return {
        "index": index,
        "name": index.replace("-", " ").title(),
        "desc": [f"This is the {index} feature."],
        "level": 1,
    }


@patch("src.fetch.srd.requests.get")
def test_fetch_features_creates_file(mock_get, tmp_path, monkeypatch):
    mock_get.side_effect = [
        Mock(status_code=200, json=lambda: mock_feature_index()),
        Mock(status_code=200, json=lambda: mock_feature_detail("channel-divinity")),
        Mock(status_code=200, json=lambda: mock_feature_detail("rage")),
    ]

    monkeypatch.setenv("DMFORGE_ENV", "test")
    monkeypatch.setattr(
        "src.fetch.srd.get_data_path", lambda filename: tmp_path / filename
    )

    fetch_srd_features(force=True)

    output_file = tmp_path / "features.json"
    assert output_file.exists()
    data = json.loads(output_file.read_text())
    assert len(data) == 2
    assert data[0]["index"] == "channel-divinity"
    assert data[0]["level"] == 1


@patch("src.fetch.srd.requests.get")
def test_features_skipped_if_not_forced(mock_get, tmp_path, monkeypatch):
    monkeypatch.setenv("DMFORGE_ENV", "test")
    output_file = tmp_path / "features.json"
    output_file.write_text("[]")  # simulate existing cache

    monkeypatch.setattr("src.fetch.srd.get_data_path", lambda filename: output_file)

    fetch_srd_features(force=False)

    mock_get.assert_not_called()
