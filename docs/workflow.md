🧠 docs/workflow.md
📦 DMForge Dev + Deck Creation Workflow
Last updated: 2025-04-13 (Post Phase 6.1)

🛠 Dev Session Lifecycle
🟢 Start Dev Session
bash
Copy
Edit
python scripts/start_dev.py
Logs session start

Displays file tree

Prepares session_log.md

🔚 End Dev Session
bash
Copy
Edit
python scripts/end_dev.py
Runs tests, formats code, prompts for summary

Logs to done_log/YYYY-MM-DD.md and session_log.md

Commits changes with message

📥 Data Ingestion
Fetch Spells, Traits, and Features
bash
Copy
Edit
python main.py fetch srd --spells --traits --features
Stores JSON in data/dev/

Requires internet connection

🧱 Deck Building
Build JSON Deck from Spell Data
bash
Copy
Edit
python main.py deck build --limit 20 --output test_deck.json
Outputs to decks/dev/

Schema: spell_to_card() format

🎨 Prompt Generation (Optional)
Generate Prompts for AI Art
bash
Copy
Edit
python main.py prompt generate --format txt --suffix "epic fantasy style"
Outputs to prompts/dev/spells.txt or .json

🖨 Rendering Decks
HTML Preview
bash
Copy
Edit
python main.py deck render decks/dev/test_deck.json --format html --output exports/dev/test_deck.html
Uses spell_card.jinja

Injects external CSS from assets/css/default.css

PDF Export: 1 Card per Page
bash
Copy
Edit
python main.py deck render decks/dev/test_deck.json --format pdf --layout cards --output exports/dev/cards.pdf
Great for individual cutting or digital view

PDF Export: 6 Cards per A4 Sheet
bash
Copy
Edit
python main.py deck render decks/dev/test_deck.json --format pdf --layout sheet --output exports/dev/sheet.pdf
Print-optimized layout

Uses spell_sheet.jinja

🧪 Testing Workflow
bash
Copy
Edit
pytest
pre-commit run --all-files
Coverage includes CLI, HTML renderers, schema conversion

HTML tests validate CSS injection and spell content

🧾 Snapshots & Documentation
Save Project Snapshot
bash
Copy
Edit
python scripts/snapshot.py
Updates docs/how_it_works.md

Creates .snapshots/dev/YYYY-MM-DD--HHMM.md

🔖 Releasing
Commit + Tag + Push
bash
Copy
Edit
git commit -am "release: Phase 5 complete – v0.6.0"
git tag v0.6.0
git push origin main --tags
✅ Output Paths Summary
Type	Location
Deck JSON	decks/dev/test_deck.json
Prompts	prompts/dev/spells.txt/.json
HTML View	exports/dev/test_deck.html
PDF Cards	exports/dev/cards.pdf
PDF Sheet	exports/dev/sheet.pdf
Snapshots	.snapshots/dev/*.md
Logs	done_log/, session_log.md