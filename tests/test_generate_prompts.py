"""Test prompt generation functionality."""

import json
from unittest.mock import patch
from src.prompts.generate import generate_spell_prompts

# Shared test data
sample_spell = {
    "index": "fireball",
    "name": "Fireball",
    "level": 3,
    "school": "Evocation",
    "classes": ["Wizard", "Sorcerer"],
    "desc": ["A bright streak flashes from your pointing finger..."],
}


@patch("src.prompts.generate.get_env", return_value="test")
def test_generate_spell_prompts_basic(mock_env, tmp_path, monkeypatch):
    """Test basic prompt generation without suffix."""
    # Setup input file
    input_file = tmp_path / "spells.json"
    input_file.write_text(json.dumps([sample_spell]), encoding="utf-8")

    # Redirect only get_data_path()
    monkeypatch.setattr("src.prompts.generate.get_data_path", lambda _: input_file)
    monkeypatch.chdir(tmp_path)

    generate_spell_prompts()

    # Verify output
    output_file = tmp_path / "prompts" / "test" / "spells.txt"
    assert output_file.exists(), "Output file not created"
    content = output_file.read_text(encoding="utf-8")
    assert "Fireball" in content, "Spell name missing from prompt"


@patch("src.prompts.generate.get_env", return_value="test")
def test_generate_spell_prompts_with_suffix(mock_env, tmp_path, monkeypatch):
    """Test prompt generation with style suffix."""
    input_file = tmp_path / "spells.json"
    input_file.write_text(json.dumps([sample_spell]), encoding="utf-8")
    monkeypatch.setattr("src.prompts.generate.get_data_path", lambda _: input_file)
    monkeypatch.chdir(tmp_path)

    generate_spell_prompts(suffix="in pixel art")

    # Verify output
    output_file = tmp_path / "prompts" / "test" / "spells.txt"
    assert output_file.exists(), "Output file not created"
    content = output_file.read_text(encoding="utf-8")
    assert "in pixel art" in content, "Style suffix missing from prompt"


@patch("src.prompts.generate.get_env", return_value="test")
def test_generate_spell_prompts_json_format(mock_env, tmp_path, monkeypatch):
    """Test JSON format prompt generation."""
    # Setup input file
    input_file = tmp_path / "spells.json"
    input_file.write_text(json.dumps([sample_spell]), encoding="utf-8")
    monkeypatch.setattr("src.prompts.generate.get_data_path", lambda _: input_file)
    monkeypatch.chdir(tmp_path)

    # Run generator
    generate_spell_prompts(suffix="in pixel art", format="json")

    # Verify output
    output_file = tmp_path / "prompts" / "test" / "spells.json"
    assert output_file.exists(), "JSON output file not created"

    data = json.loads(output_file.read_text(encoding="utf-8"))
    assert isinstance(data, list), "JSON output should be a list"
    assert len(data) == 1, "Expected one spell prompt"

    prompt_data = data[0]
    assert prompt_data["index"] == "fireball", "Wrong spell index"
    assert (
        "in pixel art" in prompt_data["prompt"]
    ), "Style suffix missing from JSON prompt"
