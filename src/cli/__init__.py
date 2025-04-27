import os
import warnings
import typer
from typing import Optional
from pathlib import Path
from src.utils.console import banner, info
from .fetch import fetch_app
from .deck import deck_app
from .prompt import prompt_app
from .utils.docs import generate_cli_docs

__version__ = "0.2.0"

# Suppress GLib and GTK warnings
os.environ["G_MESSAGES_DEBUG"] = "none"
warnings.filterwarnings("ignore")

__version__ = "0.2.0"

app = typer.Typer(
    name="dmforge",
    help="🚀 DMForge CLI – Generate spell decks, scenes, and more.",
    no_args_is_help=True,
)

# Register subcommands
app.add_typer(fetch_app, name="fetch")
app.add_typer(deck_app, name="deck")
app.add_typer(prompt_app, name="prompt")


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    env: Optional[str] = typer.Option(None, "--env", "-e", help="Override environment"),
):
    """
    Initialize CLI context.
    """
    ctx.obj = {"env": env or "dev"}


@app.command(
    "docs-cli",
    help="Generate CLI reference documentation for all dmforge commands, including subcommands.",
)
def docs_cli_command(
    output: Path = typer.Option(
        Path("docs/cli_reference.md"),
        "--output",
        "-o",
        file_okay=True,
        dir_okay=False,
        help="Output path for generated CLI reference markdown.",
    )
):
    """
    Generate CLI reference documentation covering all commands and subcommands.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    generate_cli_docs(app, output)
    typer.echo(f"✅ CLI documentation generated at {output}")


@app.command("version", help="Show DMForge version and active environment.")
def version(
    env: Optional[str] = typer.Option(None, "--env", "-e", help="Override environment")
):
    """
    Print the current DMForge CLI version and environment.
    """
    env_val = env or "dev"
    banner("DMForge CLI", f"Version {__version__} – Environment: {env_val}")


@app.command("help", help="Show system overview, CLI usage, and developer docs.")
def help_cmd(
    env: Optional[str] = typer.Option(None, "--env", "-e", help="Override environment")
):
    """
    Show a quick high-level help, including available commands and docs.
    """
    env_val = env or "dev"
    banner("DMForge Help", f"Environment: {env_val}")
    info("📘 Overview:")
    info("  - Solo dev content generator for D&D 5e")
    info("\n📂 CLI Commands:")
    info("  dmforge version")
    info("  dmforge help")
    info("  dmforge docs-cli")
    info("  dmforge fetch srd")
    info("  dmforge deck build")
    info("  dmforge deck render")
    info("  dmforge deck art")
    info("  dmforge prompt show")
    info("\n📄 Developer Docs:")
    info("  - dev-log.md")
    info("  - docs/cli_reference.md")
    info("  - docs/how_it_works.md")
