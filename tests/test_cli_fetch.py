# tests/test_cli_fetch.py

import pytest
from typer.testing import CliRunner

from src.cli import app  # main Typer application

runner = CliRunner()


def test_no_flags_shows_error():
    """
    Invoking `fetch srd` without any flags should print an error message and exit 0.
    """
    result = runner.invoke(app, ["fetch", "srd"])
    assert result.exit_code == 0
    assert (
        "No data type selected. Use --spells, --traits, --features, or --all."
        in result.stdout
    )


@pytest.mark.parametrize(
    "flags, expected_calls",
    [
        (["--spells"], [("spells", False)]),
        (["--traits"], [("traits", False)]),
        (["--features"], [("features", False)]),
    ],
)
def test_single_flag_calls_only_that(monkeypatch, flags, expected_calls):
    """
    Each single flag should only call its corresponding fetch function once with the correct `force` value.
    """
    calls = []
    # Patch the CLI-level imports in src.cli.fetch
    monkeypatch.setattr(
        "src.cli.fetch.fetch_srd_spells",
        lambda force=False: calls.append(("spells", force)),
    )
    monkeypatch.setattr(
        "src.cli.fetch.fetch_srd_traits",
        lambda force=False: calls.append(("traits", force)),
    )
    monkeypatch.setattr(
        "src.cli.fetch.fetch_srd_features",
        lambda force=False: calls.append(("features", force)),
    )

    result = runner.invoke(app, ["fetch", "srd"] + flags)
    assert result.exit_code == 0
    assert calls == expected_calls
    assert "✅ All requested content downloaded" in result.stdout


def test_force_flag_passed_to_generator(monkeypatch):
    """
    The --force flag should pass `force=True` to the selected fetch function only.
    """
    calls = []
    monkeypatch.setattr(
        "src.cli.fetch.fetch_srd_traits",
        lambda force=False: calls.append(("traits", force)),
    )
    monkeypatch.setattr(
        "src.cli.fetch.fetch_srd_spells",
        lambda force=False: calls.append(("spells", force)),
    )
    monkeypatch.setattr(
        "src.cli.fetch.fetch_srd_features",
        lambda force=False: calls.append(("features", force)),
    )

    result = runner.invoke(app, ["fetch", "srd", "--traits", "--force"])
    assert result.exit_code == 0
    assert calls == [("traits", True)]


def test_all_flag_calls_everything(monkeypatch):
    """
    The --all flag should invoke all three fetch functions with `force=True`.
    """
    calls = []
    monkeypatch.setattr(
        "src.cli.fetch.fetch_srd_spells",
        lambda force=False: calls.append(("spells", force)),
    )
    monkeypatch.setattr(
        "src.cli.fetch.fetch_srd_traits",
        lambda force=False: calls.append(("traits", force)),
    )
    monkeypatch.setattr(
        "src.cli.fetch.fetch_srd_features",
        lambda force=False: calls.append(("features", force)),
    )

    result = runner.invoke(app, ["fetch", "srd", "--all", "--force"])
    assert result.exit_code == 0
    assert calls == [("spells", True), ("traits", True), ("features", True)]
    assert "✅ All requested content downloaded" in result.stdout


def test_exception_propagates_and_logs(monkeypatch):
    """
    If a fetch function raises, the CLI should log an error and exit non-zero.
    """

    def boom(force=False):
        raise RuntimeError("boom")

    monkeypatch.setattr("src.cli.fetch.fetch_srd_spells", boom)
    monkeypatch.setattr("src.cli.fetch.fetch_srd_traits", lambda force=False: None)
    monkeypatch.setattr("src.cli.fetch.fetch_srd_features", lambda force=False: None)

    result = runner.invoke(app, ["fetch", "srd", "--spells"])
    assert result.exit_code != 0
    assert "Failed to fetch content: boom" in result.stdout
