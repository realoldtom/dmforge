# src/cli/prompt.py

import typer
import json
from src.utils.paths import get_data_path
from src.utils.console import banner, error
from src.prompts.spells import generate_spell_prompt

prompt_app = typer.Typer(name="prompt", help="Generate individual prompts")


@prompt_app.command("show")
def show(
    identifier: str = typer.Argument(..., help="Spell index or name"),
    suffix: str = typer.Option("", "--suffix", "-s", help="Suffix for prompt"),
):
    """Show AI art prompt for a single spell by index or name."""
    banner("🎨 Generating Spell Prompt")

    input_file = get_data_path("spells.json")
    if not input_file.exists():
        error(f"❌ Missing SRD data: {input_file}")
        raise typer.Exit(1)

    spells = json.loads(input_file.read_text(encoding="utf-8"))
    spell = next(
        (
            s
            for s in spells
            if s.get("index") == identifier
            or s.get("name", "").lower() == identifier.lower()
        ),
        None,
    )
    if not spell:
        error("❌ No spell found")
        raise typer.Exit(1)

    prompt = generate_spell_prompt(spell, suffix=suffix)
    typer.echo(prompt)
