# src/cli/__init__.py

"""DMForge CLI."""
from src.utils.env import get_env
from .fetch import fetch_app
from .deck import deck_app
import typer


app = typer.Typer(help="DMForge CLI – Generate spell decks, scenes, and more.")
app.add_typer(fetch_app, name="fetch")
app.add_typer(deck_app, name="deck")


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
    typer.echo(f"DMForge v0.2.0 – Environment: {env}")


@app.command()
def help(ctx: typer.Context):
    """Show system overview, CLI usage, and dev docs."""
    env = ctx.obj["env"]
    typer.echo("\n🧰 DMForge Help\n" + "-" * 40)
    typer.echo(f"🌍 Environment: {env}\n")
    typer.echo("📘 Overview:")
    typer.echo("  - Solo dev content generator for D&D 5e")
    typer.echo("  - Modular CLI, logs, and automation")
    typer.echo("\n📂 CLI Commands:")
    typer.echo("  dmforge version")
    typer.echo("  dmforge help")
    typer.echo("\n📄 Developer Docs:")
    typer.echo("  - dev-log.md")
    typer.echo("  - docs/cli_reference.md")
    typer.echo("  - docs/how_it_works.md")
