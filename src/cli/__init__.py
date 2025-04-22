# src/cli/__init__.py

import os
import warnings
import typer
from typing import Optional
from src.utils.console import banner, info
from .fetch import fetch_app
from .deck import deck_app
from .prompt import prompt_app

# Suppress GLib and GTK warnings
os.environ["G_MESSAGES_DEBUG"] = "none"

# Optional: suppress all warnings
warnings.filterwarnings("ignore")


app = typer.Typer(
    name="dmforge", help="DMForge CLI – Generate spell decks, scenes, and more."
)

app.add_typer(fetch_app, name="fetch")
app.add_typer(deck_app, name="deck")
app.add_typer(prompt_app, name="prompt")


@app.callback()
def main(
    ctx: typer.Context,
    env: Optional[str] = typer.Option(None, "--env", help="Override environment"),
):
    """Initialize CLI context and override environment."""
    ctx.obj = {"env": env}


@app.command("version")
def version(ctx: typer.Context):
    """Show DMForge version and active environment."""
    env = ctx.obj.get("env") or "dev"
    banner("DMForge CLI", f"Version 0.2.0 – Environment: {env}")


@app.command("help")
def help_cmd(ctx: typer.Context):
    """Show system overview, CLI usage, and dev docs."""
    env = ctx.obj.get("env") or "dev"
    banner("DMForge Help", f"Environment: {env}")
    info("📘 Overview:")
    info("  - Solo dev content generator for D&D 5e")
    info("\n📂 CLI Commands:")
    info("  dmforge version")
    info("  dmforge help")
    info("  dmforge fetch srd")
    info("  dmforge deck build")
    info("  dmforge deck render")
    info("  dmforge prompt show")
    info("\n📄 Developer Docs:")
    info("  - dev-log.md")
    info("  - docs/cli_reference.md")
    info("  - docs/how_it_works.md")
