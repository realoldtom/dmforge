#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path


def log_task() -> None:
    """Log a microtask with timestamp and optional tag."""
    print("\n📝 Log a Microtask")

    task = input("Describe what you completed: ").strip()
    if not task:
        print("⚠️  Task description is required.")
        return

    tag = input("Tag or module (e.g., phase1, spell_cards): ").strip() or "general"

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M")
    entry = f"- [{timestamp}] ({tag}) {task}\n"

    log_path = Path("task_log.md")
    if log_path.exists():
        log_path.write_text(
            log_path.read_text(encoding="utf-8") + entry, encoding="utf-8"
        )
    else:
        header = "# 🗂 Task Log – DMForge Microtasks\n\n"
        log_path.write_text(header + entry, encoding="utf-8")

    print("✅ Task logged.")


if __name__ == "__main__":
    log_task()
