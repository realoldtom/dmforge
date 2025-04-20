import json
import pytest
from typer.testing import CliRunner  # Change to Typer's CliRunner
from src.cli.deck import deck_app

sample_card = {
    "title": "Thematic Spell",
    "level": 2,
    "school": "Transmutation",
    "description": "Testing theme integration.",
    "casting_time": "1 action",
    "duration": "Instantaneous",
    "range": "Touch",
    "components": ["V"],
    "source": "SRD",
    "art_url": "https://example.com/image.png",
    "summary": False,
}


@pytest.fixture
def runner():
    return CliRunner()  # This will now return Typer's CliRunner


def test_render_card_sheet_pdf_with_theme(tmp_path, runner):
    deck_path = tmp_path / "deck.json"
    deck_path.write_text(json.dumps({"cards": [sample_card]}), encoding="utf-8")

    out_theme = tmp_path / "themed_sheet.pdf"
    result = runner.invoke(
        deck_app,  # Keep using deck_app directly with Typer's CliRunner
        [
            "render",
            str(deck_path),
            "--format",
            "pdf",
            "--layout",
            "sheet",
            "--theme",
            "default",
            "--output",
            str(out_theme),
        ],
    )
    assert result.exit_code == 0
    assert out_theme.exists()
