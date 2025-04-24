# src/cli/utils/docs.py

from pathlib import Path
from typer import Typer
from typer.testing import CliRunner
from src.utils.console import banner, success


def generate_cli_docs(app: Typer, output: str = "docs/cli.md"):
    banner("📘 Generating CLI Docs")
    runner = CliRunner()
    lines = ["# DMForge CLI Reference\n"]

    # Get root help
    lines.append("## `dmforge`")
    lines.append("**Help:** DMForge CLI – Generate spell decks, scenes, and more.\n")

    result = runner.invoke(app, ["--help"])
    if result.exit_code == 0:
        lines.append("```shell")
        lines.append(result.stdout.strip())
        lines.append("```")

    lines.append("\n---\n")

    # Commands to document - add all your commands here
    commands = [
        "version",
        "help",
        "docs-cli",
        "fetch",
        "fetch srd",
        "deck",
        "deck build",
        "deck art",
        "deck render",
        "prompt",
        "prompt show",
    ]

    for cmd in commands:
        lines.append(f"## `dmforge {cmd}`")
        result = runner.invoke(app, cmd.split() + ["--help"])
        if result.exit_code == 0:
            lines.append("```shell")
            lines.append(result.stdout.strip())
            lines.append("```")
        else:
            lines.append(f"_Failed to generate help output for '{cmd}'._")

        lines.append("\n---\n")

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    success(f"✅ CLI documentation written to {output_path.resolve()}")
