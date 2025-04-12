from pathlib import Path
from .env import get_env


def get_output_path(base_dir: str, filename: str) -> Path:
    env = get_env()
    return Path(base_dir) / env / filename
