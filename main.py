# main.py

import typer
from src.utils.env import get_env

app = typer.Typer(help="DMForge CLI – Generate spell decks, prompts, and more.")


# Shared CLI context
class CLIContext:
    def __init__(self):
        self.env_override = None


pass_context = typer.ContextVar("cli_ctx")


@app.callback()
def main(
    ctx: typer.Context,
    env: str = typer.Option(None, "--env", help="Override environment"),
):
    """Initialize CLI context and environment override."""
    context = CLIContext()
    context.env_override = env
    ctx.obj = context


@app.command()
def version(ctx: typer.Context):
    """Print DMForge version and environment mode."""
    env = ctx.obj.env_override or get_env()
    typer.echo(f"DMForge v0.1.0 – Environment: {env}")


if __name__ == "__main__":
    app()
