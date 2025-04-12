#!/usr/bin/env python3

from src.utils.env import get_env
from pathlib import Path
from datetime import datetime


def take_snapshot():
    print("\n📸 Taking project snapshot...")

    env = get_env()
    snapshot_dir = Path(f".snapshots/{env}")
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = snapshot_dir / f"snapshot_{timestamp}.txt"

    files = [str(p) for p in Path(".").rglob("*.py") if ".venv" not in str(p)]
    content = f"Snapshot taken at {timestamp}\n\n" + "\n".join(files)

    filename.write_text(content)
    print(f"✅ Snapshot saved to {filename}")


if __name__ == "__main__":
    take_snapshot()
