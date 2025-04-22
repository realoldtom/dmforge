# src/deck_forge/generate.py

"""Generate renderable card decks from spell data."""

import json
import typer
from pathlib import Path
from src.utils.paths import get_data_path
from src.utils.console import success, error
from src.deck_forge.schema import spell_to_card


def fetch_srd_spells():
    """Load SRD spells from JSON file."""
    path = get_data_path("spells.json")
    if not path.exists():
        error(f"❌ spells.json not found at {path}")
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def generate_spell_deck(
    output_name="deck.json",
    limit=None,
    class_filter=None,
    level_filter=None,
    school_filter=None,
    interactive=False,
):
    """Generate a full or filtered spell deck and save as a JSON file."""
    spells = fetch_srd_spells()
    if not spells:
        return None

    class_set = (
        {c.strip().lower() for c in class_filter.split(",")} if class_filter else set()
    )
    level_set = (
        {int(level.strip()) for level in level_filter.split(",")}
        if level_filter
        else set()
    )
    school_set = (
        {school.strip().lower() for school in school_filter.split(",")}
        if school_filter
        else set()
    )

    def matches_filters(spell):
        spell_classes = [c.lower() for c in spell.get("classes", [])]
        spell_level = spell.get("level")
        spell_school = spell.get("school", "").lower()
        return (
            (not class_set or any(c in class_set for c in spell_classes))
            and (not level_set or spell_level in level_set)
            and (not school_set or spell_school in school_set)
        )

    filtered = [s for s in spells if matches_filters(s)]
    if not filtered:
        error("❌ No matching spells found.")
        return None

    if limit:
        filtered = filtered[:limit]

    if interactive:
        typer.echo("📜 Available Spells (filtered):\n")
        for i, s in enumerate(filtered, 1):
            typer.echo(f"{i:2}. {s['name']} (Level {s['level']}, {s['school']})")

        selected_input = typer.prompt(
            "\nEnter the numbers of spells to include (comma-separated), or leave blank to include all"
        ).strip()

        if selected_input:
            try:
                selected_indices = {int(x.strip()) for x in selected_input.split(",")}
                filtered = [
                    s for i, s in enumerate(filtered, 1) if i in selected_indices
                ]
            except Exception as e:
                error(f"❌ Invalid input: {e}")
                return None

    cards = []
    for spell in filtered:
        card = spell_to_card(spell)
        if card:
            cards.append(card)

    output_path = Path(output_name)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps({"cards": cards}, indent=2), encoding="utf-8")

    success(f"✅ Deck written to {output_path.resolve()} with {len(cards)} card(s).")
    return output_path
