# tests/test_cli_deck.py

import json
from pathlib import Path

from typer.testing import CliRunner

from src.cli.deck import deck_app

runner = CliRunner()


def write_minimal_deck(path: Path):
    """Writes a minimal deck JSON with one card."""
    payload = {"cards": [{"title": "TestSpell", "description": "A test spell."}]}
    path.write_text(json.dumps(payload), encoding="utf-8")


# ─── build command tests ─────────────────────────────────────────────────────


def test_build_success(monkeypatch):
    def fake_gen(
        output_name, limit, class_filter, level_filter, school_filter, interactive
    ):
        Path(output_name).write_text(
            json.dumps(
                {"cards": [{"name": "TestSpell", "description": "A test spell."}]}
            ),
            encoding="utf-8",
        )
        return output_name

    monkeypatch.setattr("src.cli.deck.generate_spell_deck", fake_gen)

    with runner.isolated_filesystem():
        result = runner.invoke(deck_app, ["build"])
        assert result.exit_code == 0
        assert Path("deck.json").exists()
        assert "✅ Deck saved to" in result.stdout


def test_build_failure(monkeypatch):
    monkeypatch.setattr("src.cli.deck.generate_spell_deck", lambda *args, **kwargs: "")
    result = runner.invoke(deck_app, ["build"])
    assert result.exit_code == 1
    assert "❌ Deck generation failed." in result.stdout


def test_build_with_summarize(monkeypatch):
    def fake_gen(output_name, *args, **kwargs):
        Path(output_name).write_text(
            json.dumps({"cards": [{"name": "S", "description": "ABCDEFGHIJK"}]}),
            encoding="utf-8",
        )
        return output_name

    monkeypatch.setattr("src.cli.deck.generate_spell_deck", fake_gen)
    monkeypatch.setattr("src.cli.deck.summarize_cards", lambda cards, max_length: cards)

    with runner.isolated_filesystem():
        result = runner.invoke(
            deck_app, ["build", "--summarize", "--summary-length", "5"]
        )
        assert result.exit_code == 0
        assert "🔖 Summarized descriptions" in result.stdout


# ─── render command tests ────────────────────────────────────────────────────


def test_render_missing_file():
    result = runner.invoke(deck_app, ["render", "nope.json"])
    assert result.exit_code == 1
    assert "❌ Deck not found" in result.stdout


def test_render_pdf_sheet(monkeypatch):
    # Stub PDF renderer & HTML debug renderer
    monkeypatch.setattr(
        "src.cli.deck.render_card_sheet_pdf",
        lambda inp, out, theme, debug: Path(out).write_text("PDF DATA"),
    )
    monkeypatch.setenv("G_MESSAGES_DEBUG", "none")
    monkeypatch.setattr(
        "src.cli.deck.render_card_html",
        lambda inp, out, theme: Path(out).write_text("<html>"),
    )

    with runner.isolated_filesystem():
        write_minimal_deck(Path("deck.json"))
        result = runner.invoke(deck_app, ["render", "deck.json", "--debug"])
        assert result.exit_code == 0
        assert Path("deck.pdf").exists()
        assert Path("deck_debug.html").exists()
        assert "✅ Deck rendered successfully" in result.stdout


def test_render_pdf_card(monkeypatch):
    # Stub single-card PDF renderer
    monkeypatch.setattr(
        "src.cli.deck.render_card_pdf",
        lambda inp, out, theme, debug: Path(out).write_text("ONE CARD PDF"),
    )

    with runner.isolated_filesystem():
        write_minimal_deck(Path("deck.json"))
        result = runner.invoke(deck_app, ["render", "deck.json", "--layout", "cards"])
        assert result.exit_code == 0
        assert Path("deck.pdf").exists()
        assert "✅ Deck rendered successfully" in result.stdout


def test_render_html(monkeypatch):
    # Stub HTML renderer
    monkeypatch.setattr(
        "src.cli.deck.render_card_html",
        lambda inp, out, theme: Path(out).write_text("<html>"),
    )

    with runner.isolated_filesystem():
        write_minimal_deck(Path("deck.json"))
        result = runner.invoke(
            deck_app,
            ["render", "deck.json", "--format", "html", "--output", "page.html"],
        )
        assert result.exit_code == 0
        assert Path("page.html").exists()
        assert "✅ Deck rendered successfully" in result.stdout


# ─── art command tests ───────────────────────────────────────────────────────


def test_art_invokes_generator(monkeypatch):
    captured = {}

    def fake_art(
        deck_path, art_dir, size, n_per_card, prompt_suffix, character_style, version
    ):
        captured.update(
            {
                "deck_path": deck_path,
                "art_dir": art_dir,
                "size": size,
                "n": n_per_card,
                "suffix": prompt_suffix,
                "style": character_style,
                "version": version,
            }
        )

    monkeypatch.setattr("src.cli.deck.generate_art_for_deck", fake_art)

    with runner.isolated_filesystem():
        write_minimal_deck(Path("deck.json"))
        result = runner.invoke(
            deck_app,
            [
                "art",
                "deck.json",
                "--art-dir",
                "images",
                "--size",
                "256x256",
                "--n",
                "3",
                "--prompt-suffix",
                "bonus",
                "--character-style",
                "elf",
                "--version",
                "v2",
            ],
        )
        assert result.exit_code == 0

    assert captured["deck_path"] == Path("deck.json")
    assert captured["art_dir"] == Path("images")
    assert captured["size"] == "256x256"
    assert captured["n"] == 3
    assert captured["suffix"] == "bonus"
    assert captured["style"] == "elf"
    assert captured["version"] == "v2"
