# src/prompts/generate.py

"""Generate prompt file from cached SRD spells."""

import json
from pathlib import Path
from src.utils.env import get_env
from src.utils.paths import get_data_path
from src.prompts.spells import generate_spell_prompt
from src.utils.console import banner, success, error


def generate_spell_prompts(suffix: str = "") -> None:
    """Generate prompt file from spells.json and save to prompts/{env}/spells.txt."""
    banner("🎨 Generating Spell Prompts")

    env = get_env()
    input_file = get_data_path("spells.json")
    output_dir = Path("prompts") / env
    output_file = output_dir / "spells.txt"

    if not input_file.exists():
        error(f"❌ Missing SRD data: {input_file}")
        return

    try:
        # Load spells from JSON cache
        spells = json.loads(input_file.read_text(encoding="utf-8"))
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate prompts for each spell
        prompts = [generate_spell_prompt(spell, suffix=suffix) for spell in spells]

        # Write prompts to file
        output_file.write_text("\n\n".join(prompts), encoding="utf-8")

        success(f"✅ Wrote {len(prompts)} prompts to {output_file.resolve()}")

    except Exception as e:
        error(f"❌ Failed to generate prompts: {e}")
