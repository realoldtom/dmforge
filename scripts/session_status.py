#!/usr/bin/env python3

import subprocess


def print_git_branch():
    subprocess.run(["git", "branch", "--show-current"])


def print_diff_count():
    result = subprocess.run(
        ["git", "diff", "--shortstat"], capture_output=True, text=True
    )
    print("\n🔧 Uncommitted Changes:")
    print(result.stdout.strip() or "No uncommitted changes.")


def print_status():
    print("\n📍 Session Status")
    print("-" * 40)
    print("📂 Current Git Branch:")
    print_git_branch()
    print_diff_count()


if __name__ == "__main__":
    print_status()
