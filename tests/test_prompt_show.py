import json
from typer.testing import CliRunner
from src.cli import app

runner = CliRunner()

sample_spell = {
    "index": "fireball",
    "name": "Fireball",
    "level": 3,
    "school": "Evocation",
    "classes": ["Wizard", "Sorcerer"],
    "desc": ["A bright streak flashes from your pointing finger..."],
}


def test_prompt_show_by_index(tmp_path, monkeypatch):
    path = tmp_path / "spells.json"
    path.write_text(json.dumps([sample_spell]), encoding="utf-8")

    monkeypatch.setattr("src.cli.prompt.get_data_path", lambda _: path)
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["prompt", "show", "fireball"])
    assert result.exit_code == 0
    assert "Fireball" in result.output
    assert "Evocation" in result.output


def test_prompt_show_with_suffix(tmp_path, monkeypatch):
    path = tmp_path / "spells.json"
    path.write_text(json.dumps([sample_spell]), encoding="utf-8")

    monkeypatch.setattr("src.cli.prompt.get_data_path", lambda _: path)
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(
        app, ["prompt", "show", "fireball", "--suffix", "in anime style"]
    )
    assert result.exit_code == 0
    assert "anime style" in result.output


def test_prompt_show_spell_not_found(tmp_path, monkeypatch):
    path = tmp_path / "spells.json"
    path.write_text(json.dumps([sample_spell]), encoding="utf-8")

    monkeypatch.setattr("src.cli.prompt.get_data_path", lambda _: path)
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, ["prompt", "show", "unknown-spell"])
    assert result.exit_code != 0
    assert "No spell found" in result.output
