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

    # Use correct path relative to data directory
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

        # Step 3: Create parent directories if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Step 4: Save to local cache
        output_file.write_text(json.dumps(spells, indent=2), encoding="utf-8")
        success(f"✅ Saved {len(spells)} spells to {output_file}")

    except requests.RequestException as e:
        error(f"❌ Failed to fetch SRD spells: {e}")


def fetch_srd_traits(force: bool = False) -> None:
    """Fetch and cache racial traits from the 5e API.

    Args:
        force: If True, re-fetch even if local cache exists
    """
    banner("📥 Fetching SRD Traits")

    output_file = get_data_path("traits.json")

    if output_file.exists() and not force:
        warn("traits.json already exists — use --force to re-fetch.")
        return

    try:
        # Step 1: Get list of traits
        index_response = requests.get(f"{BASE_URL}/api/traits")
        index_response.raise_for_status()
        trait_list = index_response.json()["results"]

        # Step 2: Fetch individual trait details
        traits = []
        for trait in trait_list:
            trait_url = f"{BASE_URL}{trait['url']}"
            trait_response = requests.get(trait_url)
            trait_response.raise_for_status()
            traits.append(trait_response.json())

        # Step 3: Save to local cache
        output_file.write_text(json.dumps(traits, indent=2), encoding="utf-8")
        success(f"✅ Saved {len(traits)} traits to {output_file}")

    except requests.RequestException as e:
        error(f"❌ Failed to fetch SRD traits: {e}")


def fetch_srd_features(force: bool = False):
    """Fetch and cache class features from the 5e API."""
    banner("📥 Fetching SRD Features")

    output_file = get_data_path("features.json")

    if output_file.exists() and not force:
        warn("features.json already exists — use --force to re-fetch.")
        return

    try:
        # Step 1: Get feature list
        index_response = requests.get(f"{BASE_URL}/api/features")
        index_response.raise_for_status()
        feature_list = index_response.json()["results"]

        # Step 2: Fetch individual feature details
        features = []
        for feature in feature_list:
            feature_url = f"{BASE_URL}{feature['url']}"
            response = requests.get(feature_url)
            if response.status_code == 200:
                features.append(response.json())

        output_file.write_text(json.dumps(features, indent=2), encoding="utf-8")
        success(f"✅ Saved {len(features)} features to {output_file}")

    except requests.RequestException as e:
        error(f"❌ Failed to fetch SRD features: {e}")
