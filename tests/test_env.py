"""Test environment configuration utilities."""

from pathlib import Path

import pytest
from src.utils.env import get_env, load_config


def test_load_config_returns_dict():
    """Test that load_config returns a dictionary with required keys."""
    config = load_config()
    assert isinstance(config, dict), "Config should be a dictionary"
    assert "environment" in config, "Config missing 'environment' key"
    assert "data_dir" in config, "Config missing 'data_dir' key"
    assert "exports_dir" in config, "Config missing 'exports_dir' key"


def test_get_env_from_config(monkeypatch):
    """Test environment detection from config file when no env var set."""
    monkeypatch.delenv("DMFORGE_ENV", raising=False)
    env = get_env()
    assert env in ["dev", "prod"], f"Invalid environment: {env}"
    assert env.islower(), "Environment should be lowercase"


def test_get_env_from_env_var(monkeypatch):
    """Test environment override via environment variable."""
    monkeypatch.setenv("DMFORGE_ENV", "PROD")
    assert get_env() == "prod", "Environment should be normalized to lowercase"


def test_load_config_fallback(monkeypatch, tmp_path):
    """Test error handling with invalid config file."""
    bad_config = tmp_path / "config.yaml"
    # Cause a real YAML parse error
    bad_config.write_text("this: [unclosed-list", encoding="utf-8")

    monkeypatch.setattr(
        "src.utils.env.Path",
        lambda *args: bad_config if args[0] == "config.yaml" else Path(*args),
    )

    with pytest.raises(RuntimeError, match="Failed to parse config.yaml"):
        load_config()

    with pytest.raises(RuntimeError) as exc:
        load_config()
    assert "Failed to parse config.yaml" in str(exc.value)


def test_load_config_defaults():
    """Test default configuration values."""
    config = load_config()
    assert config["environment"] == "dev", "Default env should be 'dev'"
    assert config["data_dir"] == "data", "Default data dir incorrect"
    assert config["exports_dir"] == "exports", "Default exports dir incorrect"
