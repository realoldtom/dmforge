from src.deck_forge.render_pdf import render_card_pdf, render_card_sheet_pdf
import json

sample_card = {
    "title": "Shield",
    "level": 1,
    "school": "Abjuration",
    "casting_time": "1 reaction",
    "duration": "1 round",
    "range": "Self",
    "components": ["V", "S"],
    "description": "An invisible barrier of magical force appears and protects you...",
}


def test_render_card_pdf_debug_output(tmp_path):
    deck_path = tmp_path / "deck.json"
    pdf_path = tmp_path / "cards.pdf"
    debug_path = tmp_path / "DEBUG_cards.html"

    deck_path.write_text(json.dumps([sample_card]), encoding="utf-8")

    render_card_pdf(deck_path, pdf_path, theme="default", debug=True)

    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000
    assert debug_path.exists()
    assert "Shield" in debug_path.read_text(encoding="utf-8")


def test_render_card_sheet_debug_output(tmp_path):
    deck_path = tmp_path / "deck.json"
    pdf_path = tmp_path / "sheet.pdf"
    debug_path = tmp_path / "DEBUG_sheet.html"

    deck_path.write_text(json.dumps([sample_card]), encoding="utf-8")

    render_card_sheet_pdf(deck_path, pdf_path, theme="default", debug=True)

    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000
    assert debug_path.exists()
    assert "Shield" in debug_path.read_text(encoding="utf-8")
