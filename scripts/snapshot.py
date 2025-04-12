#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path


def take_snapshot():
    print("\n📸 Taking project snapshot...")

    snapshot_dir = Path(".snapshots")
    snapshot_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = snapshot_dir / f"snapshot_{timestamp}.txt"

    files = [str(p) for p in Path(".").rglob("*.py") if ".venv" not in str(p)]
    content = f"Snapshot taken at {timestamp}\n\n" + "\n".join(files)

    filename.write_text(content)
    print(f"✅ Snapshot saved to {filename}")


if __name__ == "__main__":
    take_snapshot()
