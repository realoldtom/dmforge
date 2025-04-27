import json
from typer.testing import CliRunner
from unittest.mock import patch
from src.cli.deck import deck_app

runner = CliRunner()

sample_card = {
    "title": "Test Spell",
    "level": 2,
    "school": "Evocation",
    "description": "A magical fire bursts forth.",
}


@patch("src.deck_forge.art.requests.post")
@patch("src.deck_forge.art.requests.get")
@patch.dict("os.environ", {"OPENAI_API_KEY": "fake-key"})
def test_versioned_art_adds_versions(mock_get, mock_post, tmp_path):
    # Setup mock responses
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "data": [{"url": "https://fakeimage.com/test.png"}]
    }
    mock_get.return_value.content = b"fake-image-bytes"

    deck_path = tmp_path / "deck.json"
    art_dir = tmp_path / "assets" / "art"
    deck_path.write_text(json.dumps({"cards": [sample_card]}), encoding="utf-8")

    result = runner.invoke(
        deck_app,
        [
            "art",
            str(deck_path),
            "--art-dir",
            str(art_dir),
            "--versioned",
        ],
    )

    assert result.exit_code == 0

    # Reload and validate deck contents
    updated = json.loads(deck_path.read_text(encoding="utf-8"))
    card = updated["cards"][0]
    assert "art_versions" in card
    assert card["art_url"].endswith("_v1.png")
    assert any("Test_Spell_v1.png" in url for url in card["art_versions"])
    assert (art_dir / "Test_Spell_v1.png").exists()
