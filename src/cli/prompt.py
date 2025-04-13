import typer
import json
from src.prompts.generate import generate_spell_prompts
from src.utils.paths import get_data_path
from src.prompts.spells import generate_spell_prompt
from src.utils.console import banner, info, error

prompt_app = typer.Typer(help="Generate spell prompts for AI use.")


@prompt_app.command("generate")
def generate(
    suffix: str = typer.Option("", "--suffix", help="Optional style/theme suffix"),
    format: str = typer.Option("txt", "--format", help="Output format: txt or json"),
):
    """Generate spell prompts from spells.json."""
    generate_spell_prompts(suffix=suffix, format=format)


@prompt_app.command("show")
def show(
    name: str = typer.Argument(..., help="Spell name or index to preview"),
    suffix: str = typer.Option(
        "", "--suffix", help="Add style/theme/persona to prompt"
    ),
):
    """Show the generated prompt for a specific spell."""
    input_file = get_data_path("spells.json")
    if not input_file.exists():
        error(f"❌ No spell data found at {input_file}")
        raise typer.Exit(1)

    spells = json.loads(input_file.read_text(encoding="utf-8"))

    # Match by index or name (case insensitive)
    match = next(
        (
            s
            for s in spells
            if s.get("index", "").lower() == name.lower()
            or s.get("name", "").lower() == name.lower()
        ),
        None,
    )

    if not match:
        error(f"❌ No spell found for: {name}")
        raise typer.Exit(1)

    banner("🎯 Spell Prompt Preview")
    prompt = generate_spell_prompt(match, suffix)
    info(prompt)
