# tests/test_render_pdf.py

import json
from src.deck_forge.render_pdf import render_card_pdf
from src.deck_forge.render_pdf import render_card_sheet_pdf

sample_card = {
    "title": "Fireball",
    "level": 3,
    "school": "Evocation",
    "classes": ["Wizard", "Sorcerer"],
    "components": ["V", "S", "M"],
    "range": "150 feet",
    "duration": "Instantaneous",
    "casting_time": "1 action",
    "description": "A bright streak flashes from your pointing finger...",
    "tags": [],
    "source": "SRD",
}


def test_render_card_pdf_creates_file(tmp_path):
    deck_path = tmp_path / "deck.json"
    pdf_path = tmp_path / "output.pdf"

    deck_path.write_text(json.dumps([sample_card]), encoding="utf-8")

    render_card_pdf(deck_path, pdf_path)

    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000  # File exists and isn't empty


def test_render_card_sheet_pdf(tmp_path):
    deck_path = tmp_path / "deck.json"
    pdf_path = tmp_path / "sheet.pdf"

    deck_path.write_text(json.dumps([sample_card] * 6), encoding="utf-8")

    render_card_sheet_pdf(deck_path, pdf_path)

    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000
