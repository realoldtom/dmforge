# tests/test_cli_deck_additional.py

import json
from pathlib import Path

from typer.testing import CliRunner

from src.cli.deck import deck_app

runner = CliRunner()


def write_minimal_deck(path: Path):
    payload = {"cards": [{"title": "TestSpell", "description": "A test spell."}]}
    path.write_text(json.dumps(payload), encoding="utf-8")


# ─── Unsupported format ───────────────────────────────────────────────────────


def test_render_unsupported_format(monkeypatch):
    with runner.isolated_filesystem():
        write_minimal_deck(Path("deck.json"))
        result = runner.invoke(deck_app, ["render", "deck.json", "--format", "txt"])
        assert result.exit_code == 1
        assert "❌ Unsupported format." in result.stdout


# ─── Render with summarization ────────────────────────────────────────────────


def test_render_with_summarize_success(monkeypatch):
    # Stub summarization helpers and renderers
    monkeypatch.setattr("src.cli.deck.load_deck", lambda p: [{"name": "A"}])
    monkeypatch.setattr("src.cli.deck.summarize_cards", lambda cards, max_length: None)
    monkeypatch.setattr(
        "src.cli.deck.render_card_sheet_pdf",
        lambda inp, out, theme, debug: Path(out).write_text("PDF"),
    )
    monkeypatch.setattr(
        "src.cli.deck.render_card_html",
        lambda inp, out, theme: Path(out).write_text("<html>"),
    )

    with runner.isolated_filesystem():
        write_minimal_deck(Path("deck.json"))
        # Summarize + debug branch
        result = runner.invoke(
            deck_app,
            [
                "render",
                "deck.json",
                "--summarize",
                "--summary-length",
                "5",
                "--debug",
            ],
        )
        assert result.exit_code == 0
        # Summarization writes deck_summ.json
        assert Path("deck_summ.json").exists()
        # PDF and debug HTML for the summarized deck
        assert Path("deck.pdf").exists()
        assert Path("deck_summ_debug.html").exists()
        assert "🔖 Using summarized deck" in result.stdout


def test_render_summarize_error(monkeypatch):
    # Make summarize_cards raise
    monkeypatch.setattr("src.cli.deck.load_deck", lambda p: [{"name": "B"}])

    def fail_summarize(cards, max_length):
        raise RuntimeError("boom")

    monkeypatch.setattr("src.cli.deck.summarize_cards", fail_summarize)

    with runner.isolated_filesystem():
        write_minimal_deck(Path("deck.json"))
        result = runner.invoke(deck_app, ["render", "deck.json", "--summarize"])
        assert result.exit_code == 1
        assert "❌ Failed to summarize before rendering: boom" in result.stdout


# ─── Render exception path ─────────────────────────────────────────────────────


def test_render_renderer_exception(monkeypatch):
    monkeypatch.setattr(
        "src.cli.deck.render_card_sheet_pdf",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("render fail")),
    )

    with runner.isolated_filesystem():
        write_minimal_deck(Path("deck.json"))
        result = runner.invoke(deck_app, ["render", "deck.json"])
        assert result.exit_code == 1
        assert "❌ Failed to render deck: render fail" in result.stdout


# ─── Art command default args ───────────────────────────────────────────────────


def test_art_default_parameters(monkeypatch):
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
        result = runner.invoke(deck_app, ["art", "deck.json"])
        assert result.exit_code == 0

    # Defaults from deck.py: art_dir=assets/art, size=1024x1024, n=1, no suffix/style, version v1
    assert captured["deck_path"] == Path("deck.json")
    assert captured["art_dir"] == Path("assets/art")
    assert captured["size"] == "1024x1024"
    assert captured["n"] == 1
    assert captured["suffix"] is None
    assert captured["style"] is None
    assert captured["version"] == "v1"
