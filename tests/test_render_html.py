# tests/test_render_html.py

from src.deck_forge.render_html import render_card_html
import json

sample_card = {
    "title": "Fireball",
    "level": 3,
    "school": "Evocation",
    "casting_time": "1 action",
    "duration": "Instantaneous",
    "range": "150 feet",
    "components": ["V", "S", "M"],
    "description": "A bright streak flashes...",
}


def test_render_card_html(tmp_path):
    deck_path = tmp_path / "deck.json"
    output_path = tmp_path / "deck.html"

    # Write fake deck
    deck_path.write_text(json.dumps([sample_card]), encoding="utf-8")

    # Render
    render_card_html(deck_path, output_path)

    # Assertions
    assert output_path.exists()
    html = output_path.read_text(encoding="utf-8")
    assert "Fireball" in html
    assert "assets/css/default.css" in html or "file:///" in html  # CSS is injected
