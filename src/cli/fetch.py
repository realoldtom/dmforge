"""Data fetching commands."""

from typer import Typer, Option
from src.fetch.srd import fetch_srd_spells

fetch_app = Typer(help="Data fetching commands")


@fetch_app.command("srd")
def fetch_srd(force: bool = Option(False, "--force", help="Force re-download")):
    """Download and cache SRD spells from dnd5eapi.co"""
    fetch_srd_spells(force=force)
