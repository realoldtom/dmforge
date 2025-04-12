#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
from src.utils.env import get_env


def summarize_module(filepath: Path) -> str:
    lines = filepath.read_text(encoding="utf-8").splitlines()
    functions = [line.strip() for line in lines if line.strip().startswith("def ")]
    classes = [line.strip() for line in lines if line.strip().startswith("class ")]
    summary = ""
    if classes:
        summary += "\n  Classes:\n"
        for cls in classes:
            summary += f"    - {cls}\n"
    if functions:
        summary += "\n  Functions:\n"
        for fn in functions:
            summary += f"    - {fn}\n"
    return summary


def generate_module_overview(src_dir: Path = Path("src")) -> str:
    overview = "# 🧠 How DMForge Works (Auto-Generated)\n\n"
    overview += f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n"
    overview += "This file is auto-generated by `scripts/snapshot.py`.\n\n"
    overview += "## Modules\n\n"

    for py_file in sorted(src_dir.rglob("*.py")):
        rel_path = py_file.relative_to(src_dir)
        module_title = f"### `{rel_path}`"
        summary = summarize_module(py_file)
        overview += f"{module_title}\n{summary or '  (no functions or classes)'}\n\n"

    return overview


def write_snapshot(env: str) -> None:
    snapshot_dir = Path(f".snapshots/{env}")
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = snapshot_dir / f"snapshot_{timestamp}.txt"
    tracked_files = [str(p) for p in Path(".").rglob("*.py") if ".venv" not in str(p)]

    content = f"Snapshot taken at {timestamp}\n\n" + "\n".join(tracked_files)
    filename.write_text(content)
    print(f"📸 Snapshot saved: {filename}")


def write_how_it_works() -> None:
    output = generate_module_overview()
    output_path = Path("docs/how_it_works.md")
    output_path.write_text(output, encoding="utf-8")
    print("🧠 Module summary written to docs/how_it_works.md")


if __name__ == "__main__":
    env = get_env()
    write_snapshot(env)
    write_how_it_works()
    print("✅ Snapshot + module summary complete.\n")
