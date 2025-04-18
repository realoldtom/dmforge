import json
from pathlib import Path

from jsonschema import Draft7Validator

DECK_PATH = Path("decks/dev/full_deck.json")
SCHEMA_PATH = Path("schemas/deck.schema.json")


def test_deck_schema_valid():
    assert DECK_PATH.exists(), f"Missing deck file: {DECK_PATH}"
    assert SCHEMA_PATH.exists(), f"Missing schema file: {SCHEMA_PATH}"

    deck = json.loads(DECK_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(deck), key=lambda e: e.path)

    assert not errors, "Deck validation failed:\n" + "\n".join(
        f"{'.'.join(map(str, e.path))}: {e.message}" for e in errors
    )
