from typer.testing import CliRunner
from src.cli import app

runner = CliRunner()


def test_main_help_includes_deck_commands():
    result = runner.invoke(app, ["--help"])
    output = result.stdout
    assert result.exit_code == 0
    assert "deck" in output  # top-level command is present

    deck_result = runner.invoke(app, ["deck", "--help"])
    deck_output = deck_result.stdout
    assert deck_result.exit_code == 0
    assert "build" in deck_output  # subcommand should appear here


def test_deck_help_includes_build_options():
    result = runner.invoke(app, ["deck", "build", "--help"])
    output = result.stdout
    assert result.exit_code == 0
    assert "--class" in output
    assert "--level" in output
    assert "--interactive" in output
    assert "--summarize" in output
    assert "--summary-length" in output
