import json
from pathlib import Path
import typer
from typing import Optional
from src.deck_forge.art import generate_art_for_deck
from src.deck_forge.generate import generate_spell_deck
from src.deck_forge.render_pdf import render_card_pdf, render_card_sheet_pdf
from src.deck_forge.render_html import render_card_html
from src.cli.utils.deck_utils import load_deck, summarize_cards
from src.utils.console import banner, error, success
from src.utils.summarizer import MAX_CHAR_COUNT

deck_app = typer.Typer(name="deck", help="Create, render, and enrich spell card decks.")


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
            cards = load_deck(deck_path)
            summarize_cards(cards, summary_length)
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
            cards = load_deck(deck_file)
            summarize_cards(cards, summary_length)
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

            if debug:
                debug_file = to_render.parent / f"{to_render.stem}_debug.html"
                render_card_html(to_render, debug_file, theme)
                success(f"📝 Debug HTML saved to {debug_file.resolve()}")

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
    deck_file: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="Path to the deck JSON file to enrich with art.",
    ),
    art_dir: Path = typer.Option(
        Path("assets/art"),
        "--art-dir",
        "-a",
        file_okay=False,
        dir_okay=True,
        help="Directory to store generated images.",
    ),
    size: str = typer.Option(
        "1024x1024", "--size", "-s", help="Size for generated images."
    ),
    n_per_card: int = typer.Option(
        1, "--n", "-n", help="Number of images per card (uses the first)."
    ),
    prompt_suffix: Optional[str] = typer.Option(
        None,
        "--prompt-suffix",
        "-p",
        help="Additional text to append to the art prompt.",
    ),
    character_style: Optional[str] = typer.Option(
        None,
        "--character-style",
        "-c",
        help="Describe the character casting the spell.",
    ),
    version: str = typer.Option(
        "v1", "--version", help="Tag appended to generated art filenames."
    ),
    versioned: bool = typer.Option(
        False,
        "--versioned",
        help="If set, filenames become `<Slug>_<version>.png` and track `art_versions`.",
    ),
):
    """
    Attach AI-generated artwork to each card in the given deck.

    By default, files are named `<TitleSlug>.png`. If --versioned is set,
    filenames become `<TitleSlug>_<version>.png` and each card gets an
    `art_versions` list in addition to `art_url`.
    """
    # 1) Ensure output folder exists
    art_dir.mkdir(parents=True, exist_ok=True)

    # 2) Generate the images (single invocation)
    generate_art_for_deck(
        deck_path=deck_file,
        art_dir=art_dir,
        size=size,
        n_per_card=n_per_card,
        prompt_suffix=prompt_suffix,
        character_style=character_style,
        version=version,
    )

    # 3) Load & patch the deck JSON
    data = json.loads(deck_file.read_text(encoding="utf-8"))
    for card in data.get("cards", []):
        slug = card["title"].replace(" ", "_")
        if versioned:
            fname = f"{slug}_{version}.png"
            card["art_versions"] = [str(art_dir / fname)]
        else:
            fname = f"{slug}.png"
        card["art_url"] = str(art_dir / fname)

    # 4) Write enriched deck back to disk
    deck_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    # 5) Feedback
    typer.echo(
        f"✅ Art generated for {len(data.get('cards', []))} cards"
        + (" (versioned)" if versioned else "")
    )
