#!/usr/bin/env python3

import subprocess


def run_tests():
    print("\n🧪 Running Pytest...")
    result = subprocess.run(["pytest"], text=True)
    if result.returncode == 0:
        print("✅ All tests passed.")
    else:
        print("❗ Some tests failed.")


if __name__ == "__main__":
    run_tests()
