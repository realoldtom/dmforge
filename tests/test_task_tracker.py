"""Test task tracking functionality."""

from scripts import task_tracker


def test_task_log_written(tmp_path, monkeypatch):
    """Test that task logging works with proper file creation and content."""
    log_path = tmp_path / "task_log.md"

    # Patch log path to use tmp_path
    monkeypatch.setattr(task_tracker, "Path", lambda *_: log_path)

    # Simulate user input
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "Test task" if "Describe" in prompt else "testing",
    )

    # Run task logger
    task_tracker.log_task()

    # Assert file is created
    assert log_path.exists(), "task_log.md not created"

    # Check content format with proper encoding
    contents = log_path.read_text(encoding="utf-8")
    assert "Test task" in contents, "Task description not found in log"
    assert "(testing)" in contents, "Task tag not found in log"
    assert any(
        [contents.startswith("# 🗂 Task Log"), contents.startswith("- [")]
    ), "Log has improper format"
