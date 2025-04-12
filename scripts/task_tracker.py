#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path


def log_task():
    task = input("Describe the task you completed: ")
    tag = input("Tag or module (e.g., 'spell_cards'): ")

    now = datetime.now()
    log_file = Path("task_log.md")
    entry = f"- [{now.strftime('%Y-%m-%d %H:%M')}] ({tag}) {task}\n"

    log_file.write_text(log_file.read_text() + entry if log_file.exists() else entry)
    print("✅ Task logged.")


if __name__ == "__main__":
    log_task()
