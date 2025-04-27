# tests/test_debug.py

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from src.cli.deck import deck_app

runner = CliRunner()

sample_card = {
    "name": "TestSpell",
    "title": "TestSpell",
    "level": 1,
    "school": "Evocation",
    "description": "Desc",
    "desc": ["Desc"],
}


@pytest.fixture(autouse=True)
def patch_render_html(monkeypatch):
    """Stub out render_card_html so the debug HTML file is created."""
    # Import the correct module where render_card_html lives
    import src.deck_forge.render_html as html_mod

    monkeypatch.setattr(
        html_mod,  # Use html_mod instead of pdf_mod
        "render_card_html",
        lambda inp, out, theme: Path(out).write_text("<html>"),
    )


def test_render_card_sheet_debug_output(tmp_path):
    # Write a single-card deck
    deck_path = tmp_path / "deck.json"
    deck_path.write_text(json.dumps({"cards": [sample_card]}), encoding="utf-8")

    # Invoke with --debug on PDF path
    output_path = tmp_path / "out.pdf"
    result = runner.invoke(
        deck_app,
        [
            "render",
            str(deck_path),
            "--format",
            "pdf",
            "--layout",
            "sheet",
            "--debug",
            "--output",
            str(output_path),
        ],
    )
    assert result.exit_code == 0

    # The PDF itself and a debug HTML should exist
    assert Path(tmp_path / "out.pdf").exists()
    debug_file = tmp_path / f"{output_path.stem}_debug.html"
    assert debug_file.exists()
