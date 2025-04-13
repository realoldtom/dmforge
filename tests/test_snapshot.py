# tests/test_snapshot.py

from pathlib import Path
from scripts import snapshot


def test_snapshot_file_created(tmp_path, monkeypatch):
    # Simulate environment
    monkeypatch.setattr(snapshot, "get_env", lambda: "test")

    # Point snapshot directory to tmp_path
    monkeypatch.setattr(
        snapshot,
        "Path",
        lambda *args: tmp_path if args[0] == ".snapshots/test" else Path(*args),
    )

    # Run snapshot
    snapshot.write_snapshot("test")

    # Check if file exists
    snapshot_files = list((tmp_path).glob("snapshot_*.txt"))
    assert snapshot_files, "No snapshot file created"


def test_how_it_works_created(tmp_path, monkeypatch):
    # Redirect output path
    monkeypatch.setattr(
        snapshot,
        "Path",
        lambda *args: (
            tmp_path / "how_it_works.md"
            if args[0] == "docs/how_it_works.md"
            else Path(*args)
        ),
    )

    # Generate how_it_works.md
    snapshot.write_how_it_works()

    # Confirm file was written
    output = tmp_path / "how_it_works.md"
    assert output.exists(), "how_it_works.md was not created"
    assert (
        "DMForge" in output.read_text()
    ), "Output file doesn't contain expected content"
