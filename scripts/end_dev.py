#!/usr/bin/env python3

import subprocess
from datetime import datetime
from pathlib import Path


def run_tests() -> None:
    """Run pytest suite."""
    print("\n🧪 Running tests...")
    subprocess.run(["pytest"], check=False)


def format_code() -> None:
    """Format all Python files with Black."""
    print("\n🎨 Formatting with Black...")
    subprocess.run(["black", "."], check=False)


def log_done_entry() -> None:
    """Log completed work to daily done_log file."""
    print("\n📝 Logging session to done_log...")
    now = datetime.now()
    log_dir = Path("done_log")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"{now.strftime('%Y-%m-%d')}.md"
    message = input("Describe what you completed today: ")
    entry = f"- {now.strftime('%H:%M')} – {message}\n"
    log_file.write_text(log_file.read_text() + entry if log_file.exists() else entry)


def git_commit() -> None:
    """Stage and commit all changes."""
    print("\n📦 Git commit...")
    msg = input("Enter commit message: ")
    subprocess.run(["git", "add", "."], check=False)
    subprocess.run(["git", "commit", "-m", msg], check=False)


def show_file_tree(root: str = ".", max_depth: int = 2) -> None:
    """Display project file tree up to specified depth."""

    def walk(path: Path, depth: int) -> None:
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


def log_session_end() -> None:
    """Log session end time to session_log.md."""
    log_path = Path("session_log.md")
    entry = f"- ✅ Session ended at {datetime.now().strftime('%H:%M')}\n"

    if log_path.exists():
        log_path.write_text(log_path.read_text() + entry)
        print("📘 Session end logged.")


def main() -> None:
    """Run end-of-session tasks and cleanup."""
    print("\n🔚 Ending Dev Session")
    print("-" * 40)
    run_tests()
    format_code()
    show_file_tree()
    log_done_entry()
    git_commit()
    log_session_end()
    print("\n✅ Dev session wrapped. Take a break!")


if __name__ == "__main__":
    main()
