from pathlib import Path
import json

p = Path("data/dev/spells.json")
data = json.loads(p.read_text(encoding="utf-8"))

# Fix if it's a list of strings
if isinstance(data, list) and isinstance(data[0], str):
    print("🔧 Fixing stringified spell data...")
    fixed = [json.loads(spell) for spell in data]
    p.write_text(json.dumps(fixed, indent=2), encoding="utf-8")
    print("✅ Repaired data/dev/spells.json")
else:
    print("✅ File is already in correct format.")
