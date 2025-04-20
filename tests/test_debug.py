import json
import pytest
from typer.testing import CliRunner  # Switch to Typer's CliRunner
from src.cli.deck import deck_app

# Sample card used across tests
sample_card = {
    "title": "Test Spell",
    "level": 1,
    "school": "Evocation",
    "description": "Test description",
    "casting_time": "1 action",
    "duration": "Instantaneous",
    "range": "Self",
    "components": ["V", "S"],
    "source": "SRD",
    "art_url": "https://example.com/image.png",
    "summary": False,
}


@pytest.fixture
def runner():
    return CliRunner()  # This will be Typer's CliRunner


def test_render_card_sheet_debug_output(tmp_path, runner):
    # Write a single-card deck
    deck_path = tmp_path / "deck.json"
    deck_path.write_text(json.dumps({"cards": [sample_card]}), encoding="utf-8")

    # Invoke with --debug flag
    output_path = tmp_path / "out.html"
    result = runner.invoke(
        deck_app,  # Keep using deck_app directly
        [
            "render",
            str(deck_path),
            "--format",
            "html",
            "--layout",
            "sheet",
            "--debug",
            "--output",
            str(output_path),
        ],
    )
    assert result.exit_code == 0

    # Debug should also write a raw HTML debug file
    debug_file = tmp_path / "deck_debug.html"
    assert debug_file.exists()
    # And the rendered output should exist and include the spell title
    assert output_path.exists()
    assert "Test Spell" in output_path.read_text(encoding="utf-8")
