# src/cli/__init__.py

"""DMForge CLI."""

import typer
from src.utils.env import get_env
from src.utils.console import banner, info

# Register subcommands
from .deck import deck_app
from .fetch import fetch_app
from .prompt import prompt_app

# Main CLI app
app = typer.Typer(help="DMForge CLI – Generate spell decks, scenes, and more.")

app.add_typer(fetch_app, name="fetch")
app.add_typer(deck_app, name="deck")
app.add_typer(prompt_app, name="prompt")


@app.callback()
def main(
    ctx: typer.Context,
    env: str = typer.Option(None, "--env", help="Override environment"),
):
    """Initialize CLI context and override environment."""
    ctx.obj = {"env": env or get_env()}


@app.command()
def version(ctx: typer.Context):
    """Show DMForge version and active environment."""
    env = ctx.obj["env"]
    banner("DMForge CLI", f"Version 0.2.0 – Environment: {env}")


@app.command()
def help(ctx: typer.Context):
    """Show system overview, CLI usage, and dev docs."""
    env = ctx.obj["env"]
    banner("DMForge Help", f"Environment: {env}")

    info("📘 Overview:")
    info("  - Solo dev content generator for D&D 5e")
    info("  - Modular CLI, logs, and automation")

    info("\n📂 CLI Commands:")
    info("  dmforge version")
    info("  dmforge help")
    info("  dmforge fetch srd")
    info("  dmforge deck create")

    info("\n📄 Developer Docs:")
    info("  - dev-log.md")
    info("  - docs/cli_reference.md")
    info("  - docs/how_it_works.md")
