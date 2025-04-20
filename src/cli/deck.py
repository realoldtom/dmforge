# src/cli/deck.py

import json
from pathlib import Path
from typing import Optional

import typer

from src.utils.console import banner, error, success
from src.deck_forge.generate import generate_spell_deck
from src.deck_forge.render_pdf import render_card_pdf, render_card_sheet_pdf
from src.deck_forge.render_html import render_card_html
from src.utils.summarizer import summarize_text, MAX_CHAR_COUNT

deck_app = typer.Typer(name="deck", help="Generate and render spell card decks")


def _load_deck(path: Path):
    """
    Load deck JSON, supporting either a list of card dicts or a single dict containing a list.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        # find a list under common keys
        for key in ("cards", "spells"):  # adapt if your structure differs
            if key in data and isinstance(data[key], list):
                return data[key]
        # otherwise wrap the single dict
        return [data]
    raise ValueError("Unexpected deck JSON format: root must be list or dict")


def _summarize_cards(cards: list, max_length: int):
    """
    Apply summarization to each card's description/desc field.
    """
    for card in cards:
        # extract raw text from 'description' or 'desc'
        raw = card.get("description") or card.get("desc") or ""
        if isinstance(raw, list):
            raw_text = " ".join(raw)
        else:
            raw_text = raw
        summary = summarize_text(raw_text, max_length=max_length)
        # override 'desc' with the summary (as a single-element list for consistency)
        card["desc"] = [summary]
        # also set 'description' in case downstream code references it
        card["description"] = summary


@deck_app.command("build")
def build(
    output: str = typer.Option("deck.json", "--output", help="Output file name"),
    limit: Optional[int] = typer.Option(
        None, "--limit", "-n", help="Only build the first N spells"
    ),
    summarize: bool = typer.Option(
        False, "--summarize/--no-summarize", help="Summarize spell descriptions"
    ),
    summary_length: int = typer.Option(
        MAX_CHAR_COUNT,
        "--summary-length",
        help=f"Max chars for summary (default {MAX_CHAR_COUNT})",
    ),
):
    """Build a full SRD spell deck, optionally summarizing descriptions."""
    banner("🧱 Generating Spell Card Deck")
    deck_path_str = generate_spell_deck(output_name=output, limit=limit)
    if not deck_path_str:
        error("❌ Deck generation failed.")
        raise typer.Exit(1)

    deck_path = Path(deck_path_str)

    if summarize:
        try:
            cards = _load_deck(deck_path)
            _summarize_cards(cards, summary_length)
            deck_path.write_text(json.dumps(cards, indent=2), encoding="utf-8")
            success(f"🔖 Summarized descriptions (≤{summary_length} chars)")
        except Exception as e:
            error(f"❌ Failed to summarize descriptions: {e}")
            raise typer.Exit(1)

    success(f"✅ Deck saved to {deck_path.resolve()}")


@deck_app.command("render")
def render(
    deck_file: Path = typer.Argument(..., help="Deck JSON file to render"),
    format: str = typer.Option("pdf", "--format", help="Output format (pdf or html)"),
    layout: str = typer.Option("sheet", "--layout", help="Layout: sheet or cards"),
    output: Optional[str] = typer.Option(None, "--output", help="Output file path"),
    theme: str = typer.Option("default", "--theme", help="Theme to use"),
    debug: bool = typer.Option(
        False, "--debug", help="Also write raw HTML for inspection"
    ),
    summarize: bool = typer.Option(
        False,
        "--summarize/--no-summarize",
        help="Summarize descriptions before rendering",
    ),
    summary_length: int = typer.Option(
        MAX_CHAR_COUNT,
        "--summary-length",
        help=f"Max chars for summary (default {MAX_CHAR_COUNT})",
    ),
):
    """Render a deck to PDF or HTML, optionally summarizing descriptions first."""
    banner("🎨 Rendering Deck")
    if not deck_file.exists():
        error(f"❌ Deck not found: {deck_file}")
        raise typer.Exit(1)

    to_render = deck_file
    if summarize:
        try:
            cards = _load_deck(deck_file)
            _summarize_cards(cards, summary_length)
            temp_file = deck_file.parent / f"{deck_file.stem}_summ.json"
            temp_file.write_text(json.dumps(cards, indent=2), encoding="utf-8")
            to_render = temp_file
            success(f"🔖 Using summarized deck (≤{summary_length} chars)")
        except Exception as e:
            error(f"❌ Failed to summarize before rendering: {e}")
            raise typer.Exit(1)

    out_path = Path(output) if output else Path(f"{deck_file.stem}.{format}")

    try:
        if format.lower() == "pdf":
            if layout == "sheet":
                render_card_sheet_pdf(to_render, out_path, theme, debug)
            else:
                render_card_pdf(to_render, out_path, theme, debug)
            if debug:
                dbg = to_render.parent / f"{to_render.stem}_debug.html"
                render_card_html(to_render, dbg, theme)

        elif format.lower() == "html":
            render_card_html(to_render, out_path, theme)
            if debug:
                dbg = to_render.parent / f"{to_render.stem}_debug.html"
                render_card_html(to_render, dbg, theme)

        else:
            error("❌ Unsupported format.")
            raise typer.Exit(1)

    except Exception as e:
        error(f"❌ Failed to render deck: {e}")
        raise typer.Exit(1)

    success("✅ Deck rendered successfully")
