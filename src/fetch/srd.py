# src/fetch/srd.py

"""Fetch and cache D&D 5e SRD content from the official API."""

import json
import requests
from src.utils.paths import get_data_path
from src.utils.console import banner, success, warn, error

BASE_URL = "https://www.dnd5eapi.co"


def normalize_spell(raw: dict) -> dict:
    """Extract relevant fields from raw API spell data."""
    return {
        "index": raw.get("index"),
        "name": raw.get("name"),
        "level": raw.get("level"),
        "school": raw.get("school", {}).get("name"),
        "classes": [cls["name"] for cls in raw.get("classes", [])],
        "desc": raw.get("desc", []),
        "range": raw.get("range"),
        "duration": raw.get("duration"),
        "components": raw.get("components", []),
        "casting_time": raw.get("casting_time"),
    }


def fetch_srd_spells(force: bool = False) -> None:
    """Fetch and cache SRD spell data from the 5e API.

    Args:
        force: If True, re-fetch even if local cache exists
    """
    banner("📥 Fetching SRD Spells")

    output_file = get_data_path("spells.json")

    if output_file.exists() and not force:
        warn("spells.json already exists — use --force to re-fetch.")
        return

    try:
        # Step 1: Fetch list of spells
        index_response = requests.get(f"{BASE_URL}/api/spells")
        index_response.raise_for_status()
        spell_list = index_response.json()["results"]

        # Step 2: Fetch full data for each spell
        spells = []
        for spell in spell_list:
            spell_url = f"{BASE_URL}{spell['url']}"
            spell_response = requests.get(spell_url)
            spell_response.raise_for_status()
            spells.append(normalize_spell(spell_response.json()))

        # Step 3: Save to local cache
        output_file.write_text(json.dumps(spells, indent=2), encoding="utf-8")
        success(f"✅ Saved {len(spells)} spells to {output_file}")

    except requests.RequestException as e:
        error(f"❌ Failed to fetch SRD spells: {e}")
