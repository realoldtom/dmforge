#!/usr/bin/env python3

import argparse
import subprocess
from datetime import datetime
from pathlib import Path


def get_latest_tag() -> str:
    """Get the most recent tag, or return None if no tags exist."""
    try:
        return subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return None


def get_git_log(since_tag: str = None) -> str:
    """Get formatted git log since the specified tag or all commits if no tag."""
    cmd = ["git", "log", "--pretty=format:- %s", "--no-merges"]
    if since_tag:
        cmd.append(f"{since_tag}..HEAD")

    try:
        return subprocess.check_output(cmd, text=True).strip()
    except subprocess.CalledProcessError:
        return ""


def append_to_changelog(version: str, log: str) -> None:
    """Update CHANGELOG.md with new version entry."""
    changelog = Path("CHANGELOG.md")
    timestamp = datetime.now().strftime("%Y-%m-%d")

    header = "# Changelog\n\n" if not changelog.exists() else ""
    entry = f"\n## {version} ({timestamp})\n\n{log}\n"

    content = header + entry
    if changelog.exists():
        content = changelog.read_text(encoding="utf-8") + entry

    changelog.write_text(content, encoding="utf-8")
    print(f"📝 Changelog updated with version {version}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate changelog from git commits")
    parser.add_argument(
        "--version", required=True, help="Version to tag the changelog with"
    )
    args = parser.parse_args()

    latest_tag = get_latest_tag()
    log = get_git_log(latest_tag)

    if not log:
        print("⚠️ No new commits found" + (f" since {latest_tag}" if latest_tag else ""))
        return

    append_to_changelog(args.version, log)


if __name__ == "__main__":
    main()
