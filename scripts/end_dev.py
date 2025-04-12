#!/usr/bin/env python3

import subprocess
from datetime import datetime
from pathlib import Path


def run_tests():
    print("\n🧪 Running tests...")
    subprocess.run(["pytest"], check=False)


def format_code():
    print("\n🎨 Formatting with Black...")
    subprocess.run(["black", "."], check=False)


def log_done_entry():
    print("\n📝 Logging session to done_log...")
    now = datetime.now()
    log_dir = Path("done_log")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"{now.strftime('%Y-%m-%d')}.md"
    message = input("Describe what you completed today: ")
    entry = f"- {now.strftime('%H:%M')} – {message}\n"
    log_file.write_text(log_file.read_text() + entry if log_file.exists() else entry)


def git_commit():
    print("\n📦 Git commit...")
    msg = input("Enter commit message: ")
    subprocess.run(["git", "add", "."], check=False)
    subprocess.run(["git", "commit", "-m", msg], check=False)


def main():
    print("\n🔚 Ending Dev Session")
    print("-" * 40)
    run_tests()
    format_code()
    log_done_entry()
    git_commit()
    print("\n✅ Dev session wrapped. Take a break!")


def show_file_tree(root=".", max_depth=2, prefix=""):
    from pathlib import Path

    def walk(path: Path, depth: int):
        if depth > max_depth:
            return
        for item in sorted(path.iterdir()):
            if item.name.startswith(".") and item.name not in {".vscode", ".snapshots"}:
                continue
            print(f"{'  ' * depth}├─ {item.name}")
            if item.is_dir():
                walk(item, depth + 1)

    print("\n📁 Project File Tree (depth ≤ 2):")
    walk(Path(root), 0)


if __name__ == "__main__":
    main()
