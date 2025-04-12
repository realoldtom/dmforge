#!/usr/bin/env python3

import subprocess
from datetime import datetime
from src.utils.env import get_env


def main():
    env = get_env()
    if env != "prod":
        print(f"❌ Aborting: Releases are only allowed in prod mode (current: {env})")
        return

    version = generate_version()
    commit_and_tag(version)
    print(f"\n✅ Release {version} created and pushed.")


def generate_version():
    return datetime.now().strftime("v%Y.%m.%d")


def commit_and_tag(version):
    print(f"\n📦 Releasing {version}...")
    subprocess.run(["git", "add", "."], check=False)
    subprocess.run(["git", "commit", "-m", f"release: {version}"], check=False)
    subprocess.run(["git", "tag", version], check=False)
    subprocess.run(["git", "push", "origin", "main", "--tags"], check=False)


if __name__ == "__main__":
    main()
