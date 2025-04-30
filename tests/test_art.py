import json
from pathlib import Path
import pytest

from src.deck_forge.art import generate_art_for_deck

DUMMY_CARD = {
    "title": "My Spell",
    "description": "A mighty blast of energy.",
    "desc": ["A mighty blast of energy."],
}


@pytest.fixture(autouse=True)
def clear_env(monkeypatch, tmp_path):
    # Ensure no stray API key
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    yield


def test_no_deck(tmp_path, capsys):
    # path does not exist
    deck = tmp_path / "does_not_exist.json"
    art_dir = tmp_path / "art"
    generate_art_for_deck(deck, art_dir)
    captured = capsys.readouterr()
    assert "Deck not found" in captured.err or "❌ Deck not found" in captured.err
    assert not art_dir.exists()


def test_no_api_key(tmp_path, capsys):
    # deck exists but no OPENAI_API_KEY
    deck = tmp_path / "deck.json"
    deck.write_text(json.dumps({"cards": [DUMMY_CARD]}), encoding="utf-8")
    art_dir = tmp_path / "art"
    generate_art_for_deck(deck, art_dir)
    captured = capsys.readouterr()
    assert "OPENAI_API_KEY not set" in captured.err
    assert not art_dir.exists()


def test_empty_cards(tmp_path, monkeypatch, capsys):
    # empty list / dict
    monkeypatch.setenv("OPENAI_API_KEY", "key")
    for raw in ([], {}, {"cards": []}):
        deck = tmp_path / "deck.json"
        deck.write_text(json.dumps(raw), encoding="utf-8")
        art_dir = tmp_path / "art"
        generate_art_for_deck(deck, art_dir)
        captured = capsys.readouterr()
        assert "No cards found in deck" in captured.err
        assert not art_dir.exists()


def test_skip_existing(tmp_path, monkeypatch, capsys):
    # file already exists → warn and skip
    monkeypatch.setenv("OPENAI_API_KEY", "key")
    deck = tmp_path / "deck.json"
    deck.write_text(json.dumps({"cards": [DUMMY_CARD]}), encoding="utf-8")
    art_dir = tmp_path / "art"
    art_dir.mkdir()
    # create the expected output file so it skips
    existing = art_dir / f"{DUMMY_CARD['title'].replace(' ', '_')}_v1.png"
    existing.write_bytes(b"")
    generate_art_for_deck(deck, art_dir, version="v1")
    captured = capsys.readouterr()
    assert "Skipping existing" in captured.err
    # deck file should be rewritten, but no new images
    data = json.loads(deck.read_text())
    # since we skipped, art_versions/key may not be added
    assert data["cards"][0]["art_versions"][0]["path"].endswith("_v1.png")
    assert Path(existing).exists()


def test_api_error_path(tmp_path, monkeypatch, capsys):
    # simulate non-200 response → writes a timestamped .json in art_dir
    monkeypatch.setenv("OPENAI_API_KEY", "key")
    deck = tmp_path / "deck.json"
    deck.write_text(json.dumps({"cards": [DUMMY_CARD]}), encoding="utf-8")
    art_dir = tmp_path / "art"

    # stub out requests.post
    class FakeResp:
        status_code = 500
        text = "server error"

        def json(self):
            return {}

    monkeypatch.setenv("OPENAI_API_KEY", "key")
    monkeypatch.setattr(
        "src.deck_forge.art.requests.post", lambda *args, **kwargs: FakeResp()
    )
    # run
    generate_art_for_deck(deck, art_dir, version="v1")
    # find the generated debug json
    files = list(art_dir.glob(f"{DUMMY_CARD['title'].replace(' ', '_')}_error_*.json"))
    assert files, "Expected an error JSON file"
    debug_txt = files[0].read_text()
    assert "server error" in debug_txt


def test_successful_generation(tmp_path, monkeypatch, capsys):
    # simulate happy path: post→200 with url, get→bytes
    monkeypatch.setenv("OPENAI_API_KEY", "key")
    deck = tmp_path / "deck.json"
    deck.write_text(json.dumps({"cards": [DUMMY_CARD]}), encoding="utf-8")
    art_dir = tmp_path / "art"
    # fake image URL and content
    fake_url = "https://example.com/image.png"

    class FakePost:
        status_code = 200

        def json(self):
            return {"data": [{"url": fake_url}]}

    monkeypatch.setattr(
        "src.deck_forge.art.requests.post", lambda *args, **kwargs: FakePost()
    )
    monkeypatch.setattr(
        "src.deck_forge.art.requests.get",
        lambda url: type("R", (object,), {"content": b"PNGDATA"}),
    )
    # run
    generate_art_for_deck(
        deck,
        art_dir,
        size="512x512",
        n_per_card=2,
        prompt_suffix="--test",
        character_style="heroic",
        version="v2",
    )
    out_file = art_dir / f"{DUMMY_CARD['title'].replace(' ','_')}_v2.png"
    assert out_file.exists() and out_file.read_bytes() == b"PNGDATA"
    # deck.json updated
    updated = json.loads(deck.read_text())
    card = updated["cards"][0]
    assert card["art_url"].endswith(f"/{out_file.name}")
    assert any(v["tag"] == "v2" for v in card["art_versions"])
    # ensure success banner at end
    captured = capsys.readouterr()
    assert "All art generated and deck updated" in captured.out


def test_exception_in_generation(tmp_path, monkeypatch, capsys):
    # simulate exception inside try
    monkeypatch.setenv("OPENAI_API_KEY", "key")
    deck = tmp_path / "deck.json"
    deck.write_text(json.dumps({"cards": [DUMMY_CARD]}), encoding="utf-8")
    art_dir = tmp_path / "art"

    def boom(*args, **kwargs):
        raise RuntimeError("oops")

    monkeypatch.setattr("src.deck_forge.art.requests.post", boom)
    # run
    generate_art_for_deck(deck, art_dir, version="v3")
    # should catch and log error, but still finish
    captured = capsys.readouterr()
    assert "Exception while generating art" in captured.err
    # deck.json still rewritten, even if no art_versions
    updated = json.loads(deck.read_text())
    assert "cards" in updated


def write_minimal_deck(path: Path):
    """Create a minimal deck JSON file for testing."""
    test_cards = [
        {
            "title": "Test Spell",  # Add title field to prevent KeyError
            "description": "This is a test spell description",
        }
    ]
    path.write_text(json.dumps({"cards": test_cards}, indent=2))
