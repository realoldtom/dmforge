# tests/test_console.py

from src.utils import console


def test_banner_runs_without_crashing():
    console.banner("Test Title", "Test Subtitle")


def test_info_runs():
    console.info("This is an info message.")


def test_success_runs():
    console.success("This is a success message.")


def test_warn_runs():
    console.warn("This is a warning.")


def test_error_runs():
    console.error("This is an error.")


def test_info_output(capfd):
    console.info("Hello world!")
    out, _ = capfd.readouterr()
    assert "Hello world!" in out
