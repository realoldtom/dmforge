from typer.testing import CliRunner
from main import app
import json

runner = CliRunner()

sample_card = {
    "title": "Misty Step",
    "level": 2,
    "school": "Conjuration",
    "casting_time": "1 bonus action",
    "duration": "Instantaneous",
    "range": "30 feet",
    "components": ["V"],
    "description": "Briefly surrounded by silvery mist, you teleport up to 30 feet to an unoccupied space you can see.",
}


def test_render_html_with_theme(tmp_path):
    deck_path = tmp_path / "deck.json"
    output_path = tmp_path / "rendered.html"

    # Create a deck file
    deck_path.write_text(json.dumps([sample_card]), encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "deck",
            "render",
            str(deck_path),
            "--format",
            "html",
            "--theme",
            "default",
            "--output",
            str(output_path),
        ],
    )

    assert result.exit_code == 0
    assert output_path.exists()
    html = output_path.read_text(encoding="utf-8")
    assert "Misty Step" in html
