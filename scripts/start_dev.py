#!/usr/bin/env python3

import subprocess
from pathlib import Path
from src.utils.env import get_env


def print_header():
    print("\n🧠  Starting Dev Session")
    print("-" * 40)
    print(f"🌎  Environment: {get_env().upper()}")


def show_git_status():
    print("\n Git Branch & Status:")
    subprocess.run(["git", "status", "-sb"])


def show_last_log():
    print("\n Last Dev Log Entry:")
    dev_log = Path("dev-log.md")
    if dev_log.exists():
        lines = dev_log.read_test().split("---")
        print(lines[-1].strip() if lines else "(empty)")
    else:
        print("No dev-log.md found.")


def show_session_plan():
    print("\n Session Plan:")
    plan_file = Path("session_plan.md")
    if plan_file.exists():
        print(plan_file.read_text().strip())
    else:
        print("No session_plan.md found.")


if __name__ == "__main__":
    print_header()
    show_git_status()
    show_last_log()
    show_session_plan()
    print("\n ready to begin!\n")
