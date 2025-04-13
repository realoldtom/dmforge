# src/cli/prompt.py

"""CLI commands for generating spell prompts."""

import typer
from src.prompts.generate import generate_spell_prompts

prompt_app = typer.Typer(help="Generate spell prompts for AI use.")


@prompt_app.command("generate")
def generate(
    suffix: str = typer.Option(
        "", "--suffix", help="Optional style/theme suffix (e.g., 'in anime style')"
    )
):
    """Generate spell prompts from spells.json."""
    generate_spell_prompts(suffix=suffix)
