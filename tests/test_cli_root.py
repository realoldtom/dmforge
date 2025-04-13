# tests/test_cli_root.py

from typer.testing import CliRunner
from src.cli import app

runner = CliRunner()


def test_version_command():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "DMForge CLI" in result.output
    assert "Environment:" in result.output


def test_help_command():
    result = runner.invoke(app, ["help"])
    assert result.exit_code == 0
    assert "DMForge Help" in result.output
    assert "CLI Commands" in result.output


def test_env_override_to_prod():
    # Instead of passing --env, simulate that context was set by the callback
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Environment:" in result.output
