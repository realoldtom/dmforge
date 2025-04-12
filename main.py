# main.py
# Entry point for the DMForge CLI

import typer

app = typer.Typer(help="DMForge CLI – Generate spell decks, prompts, and more.")


@app.command()
def version():
    """Show DMForge version info."""
    print("DMForge v0.1.0 – CLI initialized.")


if __name__ == "__main__":
    app()
