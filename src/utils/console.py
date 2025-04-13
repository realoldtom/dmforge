# src/utils/console.py

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()


def banner(title: str, subtitle: str = ""):
    """Print a nice header banner with title + optional subtitle."""
    text = Text(title, style="bold cyan")
    if subtitle:
        text.append(f"\n{subtitle}", style="dim")
    console.print(Panel(text, expand=False, box=box.ROUNDED))


def success(msg: str):
    console.print(f"✅ [green]{msg}[/]")


def warn(msg: str):
    console.print(f"⚠️  [yellow]{msg}[/]")


def error(msg: str):
    console.print(f"❌ [red]{msg}[/]")


def info(msg: str):
    console.print(f"💬 {msg}")
