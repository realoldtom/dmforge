from main import app as dmforge_app
from src.cli.utils.docs import generate_cli_docs


def test_generate_cli_docs_creates_file(tmp_path, capsys):
    output_file = tmp_path / "cli.md"
    generate_cli_docs(dmforge_app, str(output_file))

    captured = capsys.readouterr().out
    assert "📘 Generating CLI Docs" in captured
    assert "✅ CLI documentation written to" in captured
    assert output_file.exists()

    content = output_file.read_text(encoding="utf-8")
    # top‐level header
    assert content.startswith("# DMForge CLI Reference")
    # root command section
    assert "## `dmforge`" in content
    # at least one subcommand documented
    assert "## `dmforge version`" in content
    # help blocks use ```shell fences
    assert "```shell" in content


def test_generate_cli_docs_subcommand_failures(tmp_path):
    # Use an empty Typer app so all subcommands fail
    from typer import Typer

    dummy_app = Typer()
    output_file = tmp_path / "cli_failed.md"
    generate_cli_docs(dummy_app, str(output_file))

    content = output_file.read_text(encoding="utf-8")
    # Even though root help exists, each listed cmd should fall back to failure message
    assert "_Failed to generate help output for 'version'._" in content
    assert "_Failed to generate help output for 'deck build'._" in content
