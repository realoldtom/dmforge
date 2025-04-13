# src/prompts/generate.py

"""Generate prompt file from cached SRD spells."""

import json
from pathlib import Path
from src.utils.env import get_env
from src.utils.paths import get_data_path
from src.prompts.spells import generate_spell_prompt
from src.utils.console import banner, success, error


def generate_spell_prompts(suffix: str = "", format: str = "txt"):
    """Generate prompt file from spells.json and save to prompts/{env}/spells.{txt,json}."""
    banner("🎨 Generating Spell Prompts")

    env = get_env()
    input_file = get_data_path("spells.json")
    output_dir = Path("prompts") / env
    output_file = output_dir / "spells.txt"

    if not input_file.exists():
        error(f"❌ Missing SRD data: {input_file}")
        return

    try:
        spells = json.loads(input_file.read_text(encoding="utf-8"))
        output_dir.mkdir(parents=True, exist_ok=True)

        if format == "json":
            structured = [
                {
                    "index": spell.get("index"),
                    "prompt": generate_spell_prompt(spell, suffix),
                }
                for spell in spells
            ]
            json_path = output_dir / "spells.json"
            json_path.write_text(json.dumps(structured, indent=2), encoding="utf-8")
            success(f"✅ Wrote {len(structured)} prompts to {json_path.resolve()}")

        else:
            prompts = [generate_spell_prompt(spell, suffix) for spell in spells]
            txt_path = output_file
            txt_path.write_text("\n\n".join(prompts), encoding="utf-8")
            success(f"✅ Wrote {len(prompts)} prompts to {txt_path.resolve()}")

    except Exception as e:
        error(f"❌ Failed to generate prompts: {e}")
        raise
