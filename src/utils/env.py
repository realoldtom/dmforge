"""Environment configuration utilities.

Handles loading and managing environment configuration from multiple sources:
1. Environment variables (highest priority)
2. config.yaml file
3. Default values (lowest priority)
"""

import os
from pathlib import Path
from typing import Dict, Any

import yaml
from dotenv import load_dotenv

load_dotenv()  # Load .env if it exists

DEFAULT_CONFIG: Dict[str, str] = {
    "environment": "dev",
    "data_dir": "data",
    "exports_dir": "exports",
}


def load_config() -> Dict[str, Any]:
    """Load configuration from config.yaml with defaults.

    Returns:
        Dict with config values, using defaults for missing keys

    Raises:
        RuntimeError: If config.yaml exists but cannot be parsed
    """
    config_path = Path("config.yaml")
    config: Dict[str, Any] = {}

    if config_path.exists():
        try:
            config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            if config is None:
                raise yaml.YAMLError("Empty or invalid YAML")
        except yaml.YAMLError as e:
            raise RuntimeError(f"❌ Failed to parse config.yaml: {e}")

    return {**DEFAULT_CONFIG, **(config or {})}


def get_env() -> str:
    """Get current environment from config or env vars.

    Checks sources in order:
    1. DMFORGE_ENV environment variable
    2. environment key in config.yaml
    3. Default 'dev' environment

    Returns:
        Lowercase environment name ('dev' or 'prod')
    """
    if env_override := os.getenv("DMFORGE_ENV"):
        return env_override.lower()

    return load_config()["environment"].lower()
