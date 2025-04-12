from pathlib import Path
import yaml
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file


def load_config():
    config_path = Path("config.yaml")
    if not config_path.exists():
        raise FileNotFoundError("Missing config.yaml")
    return yaml.safe_load(config_path.read_text())


def get_env():
    config = load_config()
    override = os.getenv("ENVIRONMENT")
    return override if override else config.get("environment", "dev")
