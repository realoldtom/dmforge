#!/usr/bin/env python3

import subprocess


def run_linter():
    print("\n🔍 Running Ruff linter...")
    result = subprocess.run(["ruff", "."], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("❗ Linting completed with issues.")
    else:
        print("✅ Code is clean.")


if __name__ == "__main__":
    run_linter()
