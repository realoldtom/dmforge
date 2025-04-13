"""Environment configuration utilities."""

import os
from pathlib import Path
import yaml
from dotenv import load_dotenv

load_dotenv()  # Load .env if it exists

DEFAULT_CONFIG = {"environment": "dev", "data_dir": "data", "exports_dir": "exports"}


def load_config() -> dict:
    """Load configuration from config.yaml with defaults."""
    config_path = Path("config.yaml")
    config = {}

    if config_path.exists():
        try:
            config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        except Exception as e:
            raise RuntimeError(f"❌ Failed to parse config.yaml: {e}")

    return {**DEFAULT_CONFIG, **config}


def get_env() -> str:
    """Get current environment from config or env vars."""
    if env_override := os.getenv("DMFORGE_ENV"):
        return env_override.lower()

    return load_config()["environment"].lower()
