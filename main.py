# main.py

import typer
from src.utils.env import get_env

app = typer.Typer(help="DMForge CLI – Generate spell decks, prompts, and more.")


class CLIContext:
    """Shared CLI context for environment overrides."""

    def __init__(self):
        self.env_override = None


@app.callback()
def main(
    ctx: typer.Context,
    env: str = typer.Option(None, "--env", help="Override environment"),
) -> None:
    """Initialize CLI context and environment override."""
    context = CLIContext()
    context.env_override = env
    ctx.obj = context


@app.command()
def version(ctx: typer.Context) -> None:
    """Print DMForge version and environment mode."""
    env = ctx.obj.env_override or get_env()
    typer.echo(f"DMForge v0.1.0 – Environment: {env}")


@app.command()
def help(ctx: typer.Context) -> None:
    """Display system overview, usage examples, and links to docs."""
    env = ctx.obj.env_override or get_env()
    print("\n🧰 DMForge Help")
    print("─" * 40)
    print(f"🌍 Environment: {env}")
    print("\n📘 System Overview:")
    print("  - Solo dev assistant and content generator for D&D 5e")
    print("  - Supports card layout, scene generation, prompt output")
    print("  - Modular, testable, environment-aware")

    print("\n📂 CLI Commands:")
    print("  python main.py version")
    print("  python main.py help")
    print("  # (More commands coming in Phases 3–6)")

    print("\n📄 Developer Docs:")
    print("  - dev-log.md")
    print("  - docs/project_structure.md")
    print("  - docs/cli_reference.md")
    print("  - docs/how_it_works.md")
    print("  - dev_hints.md")

    print(
        "\n✅ Use `scripts/start_dev.py` and `scripts/end_dev.py` for session management.\n"
    )


if __name__ == "__main__":
    app()
