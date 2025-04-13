from pathlib import Path
from src.utils.env import get_env


def get_output_path(folder: str, filename: str = "") -> Path:
    """Get a path inside exports/{env}/."""
    env = get_env()
    base = Path("exports") / env / folder
    base.mkdir(parents=True, exist_ok=True)
    return base / filename if filename else base


def get_data_path(filename: str = "") -> Path:
    """Get a path inside data/{env}/ for SRD caching."""
    env = get_env()
    base = Path("data") / env
    base.mkdir(parents=True, exist_ok=True)
    return base / filename if filename else base
