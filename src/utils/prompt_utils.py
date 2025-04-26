def build_spell_prompt(
    title: str,
    description: str | None = None,
    character_style: str | None = None,
    prompt_suffix: str | None = None,
) -> str:
    """
    Return an image-generation prompt for a DMForge spell card.

    • title            – spell name
    • description      – full spell text (optional, short phrases are best)
    • character_style  – e.g. "robed elf wizard", "dragonborn sorcerer" (optional)
    • prompt_suffix    – any extra style tags you want appended (optional)
    """
    # 1) core
    parts = [
        f"High-fantasy illustration of the spell **{title}**.",
        "Painterly, ArtStation / Wizards-of-the-Coast style.",
        "Dramatic, cinematic lighting; rich, detailed environment.",
    ]

    # 2) subject
    if character_style:
        parts.append(f"Depict a **{character_style}** in mid-cast.")
    else:
        parts.append("No characters; focus on the spell’s visual effects.")

    # 3) spell effect (optional but helps the model)
    if description:
        parts.append(f"Visualise the core effect: {description.strip()}.")

    # 4) any caller-supplied suffix
    if prompt_suffix:
        parts.append(prompt_suffix.strip())

    # 5) final touch – keep camera direction consistent
    parts.append("Sharp focus, dynamic composition, aspect 3:4.")

    return " ".join(parts)
