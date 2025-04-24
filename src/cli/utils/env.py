import os
import yaml
from pathlib import Path

DEFAULT_ENV = "dev"
DEFAULT_CONFIG = {
    "environment": DEFAULT_ENV,
    "data_dir": "data",
    "exports_dir": "exports",
}


def get_env() -> str:
    """Return the current environment, defaulting to 'dev'."""
    return os.getenv("DMFORGE_ENV", DEFAULT_ENV).lower()


def load_config(path: Path = Path("config.yaml")) -> dict:
    """
    Load configuration from config.yaml. If not present or invalid,
    fallback to default config. Raises RuntimeError on parse failure.
    """
    if not path.exists():
        return DEFAULT_CONFIG

    try:
        with path.open(encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    except Exception as e:
        raise RuntimeError(f"Failed to parse config.yaml: {e}")

    return {
        "environment": config.get("environment", DEFAULT_ENV),
        "data_dir": config.get("data_dir", "data"),
        "exports_dir": config.get("exports_dir", "exports"),
    }
