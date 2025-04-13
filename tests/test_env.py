# tests/test_env.py

from src.utils.env import load_config, get_env


def test_load_config_returns_dict():
    config = load_config()
    assert isinstance(config, dict)
    assert "environment" in config


def test_get_env_returns_string():
    env = get_env()
    assert isinstance(env, str)
    assert env in {"dev", "prod"}
