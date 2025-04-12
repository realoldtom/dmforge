#!/usr/bin/env python3

import subprocess
from pathlib import Path
from datetime import datetime
from src.utils.env import get_env


def log_session_start() -> None:
    """Log the start of a new development session if not already logged today."""
    log_path = Path("session_log.md")
    today = datetime.now().strftime("%Y-%m-%d")

    if log_path.exists() and today in log_path.read_text(encoding="utf-8"):
        return  # Already logged today

    entry = f"\n## 🚧 {today} – New Dev Session Started\n\n"
    if log_path.exists():
        log_path.write_text(
            log_path.read_text(encoding="utf-8") + entry, encoding="utf-8"
        )
    else:
        log_path.write_text(entry, encoding="utf-8")

    print(f"📝 Session log started for {today}")


def print_header() -> None:
    """Print the session header with environment information."""
    print("\n🧠  Starting Dev Session")
    print("-" * 40)
    print(f"🌎  Environment: {get_env().upper()}")


def show_git_status() -> None:
    """Display current git branch and status."""
    print("\n📌 Git Branch & Status:")
    subprocess.run(["git", "status", "-sb"])


def show_last_log() -> None:
    """Show the most recent dev log entry."""
    print("\n📓 Last Dev Log Entry:")
    dev_log = Path("dev-log.md")
    if dev_log.exists():
        lines = dev_log.read_text(encoding="utf-8").split("---")
        print(lines[-1].strip() if lines else "(empty)")
    else:
        print("No dev-log.md found.")


def show_session_plan() -> None:
    """Display today's session plan if available."""
    print("\n🗒️  Session Plan:")
    plan_file = Path("session_plan.md")
    if plan_file.exists():
        print(plan_file.read_text(encoding="utf-8").strip())
    else:
        print("No session_plan.md found.")


if __name__ == "__main__":
    print_header()
    show_git_status()
    show_last_log()
    show_session_plan()
    log_session_start()
    print("\n✅ Ready to begin!\n")
