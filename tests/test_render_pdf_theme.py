from src.deck_forge.render_pdf import render_card_pdf, render_card_sheet_pdf
import json
from tests.utils.mocks import HTMLCapture

sample_card = {
    "title": "Mage Armor",
    "level": 1,
    "school": "Abjuration",
    "casting_time": "1 action",
    "duration": "8 hours",
    "range": "Touch",
    "components": ["V", "S", "M"],
    "description": "You touch a willing creature who isn't wearing armor...",
}


def test_render_card_pdf_with_theme(tmp_path):
    deck_path = tmp_path / "deck.json"
    pdf_path = tmp_path / "out_card.pdf"

    deck_path.write_text(json.dumps([sample_card]), encoding="utf-8")

    with HTMLCapture() as capture:
        render_card_pdf(deck_path, pdf_path, theme="default")

    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000
    assert "assets/css/default.css" in capture.captured["html"]


def test_render_card_sheet_pdf_with_theme(tmp_path):
    deck_path = tmp_path / "deck.json"
    pdf_path = tmp_path / "out_sheet.pdf"

    deck_path.write_text(json.dumps([sample_card]), encoding="utf-8")

    with HTMLCapture() as capture:
        render_card_sheet_pdf(deck_path, pdf_path, theme="default")

    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000
    assert "assets/css/default.css" in capture.captured["html"]
