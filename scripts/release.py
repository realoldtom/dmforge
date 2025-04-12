#!/usr/bin/env python3

import subprocess
from datetime import datetime


def generate_version():
    return datetime.now().strftime("v%Y.%m.%d")


def commit_and_tag(version):
    print(f"\n📦 Releasing {version}...")
    subprocess.run(["git", "add", "."], check=False)
    subprocess.run(["git", "commit", "-m", f"release: {version}"], check=False)
    subprocess.run(["git", "tag", version], check=False)
    subprocess.run(["git", "push", "origin", "main", "--tags"], check=False)


def main():
    version = generate_version()
    commit_and_tag(version)
    print(f"\n✅ Release {version} created and pushed.")


if __name__ == "__main__":
    main()
