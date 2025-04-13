# src/cli/prompt.py

"""CLI commands for prompt generation and management."""

from typer import Typer, Option
from src.prompts.generate import generate_spell_prompts
from src.utils.console import error

prompt_app = Typer(help="Generate and manage image prompts")


@prompt_app.command()
def create(
    spells: bool = Option(False, "--spells", help="Generate spell card prompts"),
    style: str = Option("", "--style", help="Optional style suffix for prompts"),
    json_format: bool = Option(False, "--json", help="Output in JSON format"),
) -> None:
    """Create image generation prompts from SRD data."""
    if not spells:
        error("No content type selected. Use --spells")
        return

    generate_spell_prompts(suffix=style, format="json" if json_format else "txt")
