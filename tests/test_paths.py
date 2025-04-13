from src.utils.paths import get_data_path


def test_get_data_path_returns_path(monkeypatch):
    monkeypatch.setenv("DMFORGE_ENV", "test")
    path = get_data_path("spells.json")
    assert "data" in str(path)
    assert "test" in str(path)
    assert "spells.json" in str(path)
