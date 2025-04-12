#!/usr/bin/env python3

import subprocess
from datetime import datetime
from pathlib import Path
import argparse


def get_git_log() -> str:
    try:
        result = subprocess.check_output(
            [
                "git",
                "log",
                "--pretty=format:- %s",
                "--no-merges",
                "$(git describe --tags --abbrev=0)..HEAD",
            ],
            text=True,
            shell=True,
        )
        return result.strip()
    except subprocess.CalledProcessError:
        return ""


def get_default_version() -> str:
    return datetime.now().strftime("v%Y.%m.%d")


def append_to_changelog(version: str, log: str) -> None:
    changelog = Path("CHANGELOG.md")
    existing = changelog.read_text(encoding="utf-8") if changelog.exists() else ""

    entry = f"\n## {version} – {datetime.now().strftime('%Y-%m-%d')}\n\n{log}\n"
    updated = existing + entry

    changelog.write_text(updated, encoding="utf-8")
    print(f"📓 Changelog updated with version {version}.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate CHANGELOG.md from recent commits."
    )
    parser.add_argument(
        "--version", type=str, help="Override version tag", default=None
    )
    args = parser.parse_args()

    version = args.version or get_default_version()
    log = get_git_log()

    if not log:
        print("⚠️ No new commits found since last tag.")
        return

    append_to_changelog(version, log)


if __name__ == "__main__":
    main()
