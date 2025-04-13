"""Data fetching commands for D&D 5e content."""

from typer import Typer, Option
from src.fetch.srd import fetch_srd_spells, fetch_srd_traits, fetch_srd_features
from src.utils.console import banner, error, success

fetch_app = Typer(help="Data fetching commands")


@fetch_app.command("srd")
def fetch_srd(
    spells: bool = Option(False, "--spells", help="Fetch SRD spells"),
    traits: bool = Option(False, "--traits", help="Fetch racial traits"),
    features: bool = Option(False, "--features", help="Fetch class features"),
    all_data: bool = Option(False, "--all", help="Fetch all available SRD content"),
    force: bool = Option(False, "--force", help="Force re-download and overwrite"),
) -> None:
    """Download and cache SRD data from dnd5eapi.co."""
    if not (spells or traits or features or all_data):
        error("No data type selected. Use --spells, --traits, --features, or --all.")
        return

    banner("📥 Fetching SRD Content")

    try:
        if all_data or spells:
            fetch_srd_spells(force=force)

        if all_data or traits:
            fetch_srd_traits(force=force)

        if all_data or features:
            fetch_srd_features(force=force)

        success("✅ All requested content downloaded")

    except Exception as e:
        error(f"Failed to fetch content: {str(e)}")
        raise  # Re-raise to show full traceback in debug mode
