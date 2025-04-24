# src/deck_forge/art.py

import typer
from typing import Optional
from src.deck_forge.art import generate_art_for_deck
from pathlib import Path
from src.cli.deck import deck_app

API_URL = "https://api.openai.com/v1/images/generations"
MODEL = "dall-e-3"
DEFAULT_SIZE = "512x512"


@deck_app.command("art", help="Generate DALL·E art for each spell card in a deck.")
def art(
    deck_file: Path = typer.Argument(..., help="Path to deck JSON to enrich with art."),
    art_dir: Path = typer.Option(
        Path("assets/art"), "--art-dir", help="Directory to store generated images."
    ),
    size: str = typer.Option("512x512", "--size", help="Size for generated images."),
    n: int = typer.Option(1, "--n", help="Number of images per card (uses first)."),
    prompt_suffix: Optional[str] = typer.Option(
        None, "--prompt-suffix", help="Append text to the generated prompt."
    ),
    character_style: Optional[str] = typer.Option(
        None, "--character-style", help="Describe the caster for the prompt."
    ),
):
    generate_art_for_deck(
        deck_path=deck_file,
        art_dir=art_dir,
        size=size,
        n_per_card=n,
        prompt_suffix=prompt_suffix,
        character_style=character_style,
    )
