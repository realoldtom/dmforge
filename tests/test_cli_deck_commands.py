from typer.testing import CliRunner
from src.cli import app

runner = CliRunner()


def test_main_help_includes_deck_commands():
    result = runner.invoke(app, ["--help"])
    output = result.stdout
    assert result.exit_code == 0
    assert "deck" in output
    assert "build" in output
    assert "render" in output
    assert "art" in output


def test_deck_help_includes_build_options():
    result = runner.invoke(app, ["deck", "build", "--help"])
    output = result.stdout
    assert result.exit_code == 0
    assert "--class" in output
    assert "--level" in output
    assert "--interactive" in output
    assert "--summarize" in output
    assert "--summary-length" in output
