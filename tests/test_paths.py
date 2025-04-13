# tests/test_paths.py

from src.utils.paths import get_output_path


def test_get_output_path_returns_path():
    output = get_output_path("exports", "test.pdf")
    assert "exports" in str(output)
    assert "test.pdf" in str(output)
