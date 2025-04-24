import json
from pathlib import Path
import typer
from typing import Optional
from src.deck_forge.art import generate_art_for_deck
from src.deck_forge.generate import generate_spell_deck
from src.deck_forge.render_pdf import render_card_pdf, render_card_sheet_pdf
from src.deck_forge.render_html import render_card_html
from src.utils.console import banner, error, success
from src.utils.summarizer import summarize_text, MAX_CHAR_COUNT

deck_app = typer.Typer(name="deck", help="Create, render, and enrich spell card decks.")


def _load_deck(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("cards", "spells"):
            if key in data and isinstance(data[key], list):
                return data[key]
        return [data]
    raise ValueError("Unexpected deck JSON format: root must be list or dict")


def _summarize_cards(cards: list, max_length: int):
    for card in cards:
        raw = card.get("description") or card.get("desc") or ""
        if isinstance(raw, list):
            raw_text = " ".join(raw)
        else:
            raw_text = raw
        summary = summarize_text(raw_text, max_length=max_length)
        card["desc"] = [summary]
        card["description"] = summary


@deck_app.command(
    "build", help="Generate a spell deck from the SRD with optional filters."
)
def build(
    output: str = typer.Option(
        "deck.json", "--output", help="Output filename for the deck."
    ),
    limit: Optional[int] = typer.Option(
        None, "--limit", "-n", help="Limit the number of spells."
    ),
    summarize: bool = typer.Option(
        False, "--summarize/--no-summarize", help="Summarize spell descriptions."
    ),
    summary_length: int = typer.Option(
        MAX_CHAR_COUNT, "--summary-length", help="Max length of summary in characters."
    ),
    class_filter: Optional[str] = typer.Option(
        None, "--class", help="Comma-separated class filter (e.g. wizard,cleric)."
    ),
    level_filter: Optional[str] = typer.Option(
        None, "--level", help="Comma-separated spell level(s) (e.g. 1,2,3)."
    ),
    school_filter: Optional[str] = typer.Option(
        None, "--school", help="Comma-separated spell school(s)."
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        help="Select specific spells interactively after filtering.",
    ),
):
    """Generate a spell card deck from SRD spell data with optional filtering and summarization."""
    banner("🧱 Generating Spell Card Deck")
    deck_path_str = generate_spell_deck(
        output_name=output,
        limit=limit,
        class_filter=class_filter,
        level_filter=level_filter,
        school_filter=school_filter,
        interactive=interactive,
    )
    if not deck_path_str:
        error("❌ Deck generation failed.")
        raise typer.Exit(1)

    deck_path = Path(deck_path_str)

    if summarize:
        try:
            cards = _load_deck(deck_path)
            _summarize_cards(cards, summary_length)
            deck_path.write_text(
                json.dumps({"cards": cards}, indent=2), encoding="utf-8"
            )
            success(f"🔖 Summarized descriptions (≤{summary_length} chars)")
        except Exception as e:
            error(f"❌ Failed to summarize descriptions: {e}")
            raise typer.Exit(1)

    success(f"✅ Deck saved to {deck_path.resolve()}")


@deck_app.command("render", help="Render a deck to PDF or HTML.")
def render(
    deck_file: Path = typer.Argument(..., help="Deck JSON file to render."),
    format: str = typer.Option("pdf", "--format", help="Output format (pdf or html)."),
    layout: str = typer.Option(
        "sheet", "--layout", help="Layout: 'sheet' (6/page) or 'cards' (1/page)."
    ),
    output: Optional[str] = typer.Option(None, "--output", help="Output file path."),
    theme: str = typer.Option("default", "--theme", help="CSS theme to apply."),
    debug: bool = typer.Option(False, "--debug", help="Also save raw HTML output."),
    summarize: bool = typer.Option(
        False, "--summarize/--no-summarize", help="Summarize before rendering."
    ),
    summary_length: int = typer.Option(
        MAX_CHAR_COUNT, "--summary-length", help="Max summary length."
    ),
):
    """Render spell cards to a printable PDF or interactive HTML page."""
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
            temp_file.write_text(
                json.dumps({"cards": cards}, indent=2), encoding="utf-8"
            )
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
        elif format.lower() == "html":
            render_card_html(to_render, out_path, theme)
        else:
            error("❌ Unsupported format.")
            raise typer.Exit(1)

    except Exception as e:
        error(f"❌ Failed to render deck: {e}")
        raise typer.Exit(1)

    success("✅ Deck rendered successfully")


@deck_app.command("art", help="Generate DALL·E art for each spell card in a deck.")
def art(
    deck_file: Path = typer.Argument(..., help="Path to deck JSON to enrich with art."),
    art_dir: Path = typer.Option(
        Path("assets/art"), "--art-dir", help="Directory to store generated images."
    ),
    size: str = typer.Option("512x512", "--size", help="Size for generated images."),
    n: int = typer.Option(1, "--n", help="Number of images per card (uses first)."),
):
    """Attach AI-generated artwork to each card in the given deck."""
    generate_art_for_deck(deck_file, art_dir, size=size, n_per_card=n)
