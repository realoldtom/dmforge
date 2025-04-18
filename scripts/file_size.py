from pathlib import Path

print(Path("data/dev/spells.json").stat().st_size, "bytes")
