# src/prompts/spells.py

"""Spell prompt generator for AI art and text models."""


def generate_spell_prompt(spell: dict, suffix: str = "") -> str:
    """Create a natural language prompt from a spell object.

    Args:
        spell: Dict containing spell data from SRD.
        suffix: Optional additional description (e.g., art style or persona).

    Returns:
        str: A formatted prompt string.
    """
    name = spell.get("name", "Unnamed Spell")
    level = spell.get("level", "Unknown level")
    school = spell.get("school", "Unknown school")
    classes = ", ".join(spell.get("classes", []))
    desc = " ".join(spell.get("desc", []))[:200]  # Trim for short prompts

    base = f"A spell called '{name}', a level {level} {school} spell. Used by: {classes}. {desc}"
    return f"{base.strip()} {suffix.strip()}".strip()
