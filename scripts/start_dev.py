#!/usr/bin/env python3

"""Development session startup utilities."""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional
from src.utils.env import get_env
from src.utils.console import banner, error, success, warn

if "VIRTUAL_ENV" not in os.environ:
    print("⚠️  Virtual environment not active. Please activate with:")
    print("    .venv\\Scripts\\Activate.ps1  (PowerShell)")
    print("    .venv\\Scripts\\activate.bat   (cmd.exe)")
    print("    source .venv/bin/activate     (Linux/macOS)")


def verify_python_environment() -> None:
    """Verify script is running with correct Python interpreter."""
    executable = Path(sys.executable).name.lower()
    if "devenv" in executable or "visualstudio" in executable:
        error("Script launched by Visual Studio instead of Python")
        print(f"\nCurrent executable: {sys.executable}")
        print("\nTo fix this:")
        print("1. Open Windows Settings")
        print("2. Go to Apps > Default Apps")
        print("3. Set .py files to open with Python")
        sys.exit(1)


def get_latest_log_entry() -> Optional[str]:
    """Get the most recent dev log entry or None if not found."""
    dev_log = Path("dev-log.md")
    if not dev_log.exists():
        return None

    try:
        content = dev_log.read_text(encoding="utf-8")
        entries = content.split("---")
        return entries[-1].strip() if entries else None
    except Exception as e:
        error(f"Failed to read dev log: {e}")
        return None


def log_session_start() -> None:
    """Log the start of a new development session if not already logged today."""
    log_path = Path("session_log.md")
    today = datetime.now().strftime("%Y-%m-%d")

    try:
        if log_path.exists():
            content = log_path.read_text(encoding="utf-8")
            if today in content:
                return  # Already logged today

            log_path.write_text(
                content + f"\n## 🚧 {today} – New Dev Session Started\n\n",
                encoding="utf-8",
            )
        else:
            log_path.write_text(
                f"## 🚧 {today} – New Dev Session Started\n\n", encoding="utf-8"
            )
        success(f"Session log started for {today}")
    except Exception as e:
        error(f"Failed to write session log: {e}")


if __name__ == "__main__":
    verify_python_environment()

    # Print session header
    banner("🧠 Starting Dev Session")
    print(f"🌎 Environment: {get_env().upper()}")

    # Show git status
    print("\n📌 Git Branch & Status:")
    try:
        subprocess.run(["git", "status", "-sb"], check=True)
    except subprocess.CalledProcessError:
        error("Git command failed")

    # Show latest log entry
    print("\n📓 Last Dev Log Entry:")
    if latest := get_latest_log_entry():
        print(latest)
    else:
        warn("No dev log entries found")

    # Show session plan
    print("\n🗒️ Session Plan:")
    plan = Path("session_plan.md")
    if plan.exists():
        print(plan.read_text(encoding="utf-8").strip())
    else:
        warn("No session plan found")

    # Log session start
    log_session_start()
    success("Ready to begin!")
