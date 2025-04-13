# tests/test_prompt_spells.py

from src.prompts.spells import generate_spell_prompt

sample_spell = {
    "name": "Fireball",
    "level": 3,
    "school": "Evocation",
    "classes": ["Wizard", "Sorcerer"],
    "desc": [
        "A bright streak flashes from your pointing finger to a point you choose..."
    ],
}


def test_generate_spell_prompt_basic():
    prompt = generate_spell_prompt(sample_spell)
    assert "Fireball" in prompt
    assert "level 3" in prompt
    assert "Evocation" in prompt
    assert "Wizard" in prompt
    assert "bright streak" in prompt


def test_generate_spell_prompt_with_suffix():
    prompt = generate_spell_prompt(
        sample_spell, suffix="in the style of a medieval woodcut"
    )
    assert "medieval woodcut" in prompt
    assert prompt.endswith("medieval woodcut")
