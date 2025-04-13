# 🚀 DMForge CLI Reference

This guide documents all available CLI commands and options for generating, rendering, and managing spell cards.

---

## 📦 Deck Commands

### `dmforge deck build`

Build a layout-ready JSON card deck from SRD data.

```bash
dmforge deck build --output test_deck.json --limit 20
Options:

Flag	Description
--output	Output JSON filename (default: full_spell_deck.json)
--limit	Limit number of spells included
🖨 Deck Rendering
dmforge deck render
Render a .json deck into PDF or HTML using layout templates.

bash
Copy
Edit
dmforge deck render decks/dev/full_spell_deck.json --format pdf --layout sheet
Options:

Flag	Description
--format	pdf or html
--output	Output file path (default: deck.pdf)
--layout	cards (1/page) or sheet (6/page)
🎨 Prompt Commands
dmforge prompt generate
Generate AI-ready prompt files from SRD spell data.

bash
Copy
Edit
dmforge prompt generate --format json --suffix "in anime style"
Options:

Flag	Description
--format	txt or json
--suffix	Append style to prompt (optional)
dmforge prompt show <spell-name>
Preview a single spell's AI prompt.

bash
Copy
Edit
dmforge prompt show fireball --suffix "high fantasy"
📥 Data Fetching
dmforge fetch srd
Fetch SRD spell, trait, and feature data from the API.

bash
Copy
Edit
dmforge fetch srd --spells --traits --force
Options:

Flag	Description
--spells	Fetch only spell data
--traits	Fetch racial traits
--features	Fetch class features
--force	Overwrite cached files
🧪 Misc
dmforge version
Show version and environment info.

dmforge help
Print CLI overview and dev docs.