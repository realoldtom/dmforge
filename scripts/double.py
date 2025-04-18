# scripts/debug_deck.py
import json
from pathlib import Path

path = Path("decks/dev/full_deck.json")
print("Inspecting:", path)

try:
    text = path.read_text(encoding="utf-8")
    print("Raw preview:", text[:150])
    data = json.loads(text)
    print("✅ JSON loaded")
    print("Top keys:", list(data.keys()))
    print("First card:", data["cards"][0])
except Exception as e:
    print("❌ Error loading JSON:", e)
