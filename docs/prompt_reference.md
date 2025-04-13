# 🧠 DMForge Prompt Reference

This document explains how DMForge generates AI-ready prompt text from SRD spells.

---

## 🎯 Prompt Generator Overview

Prompt generation is powered by `generate_spell_prompt()` and used in:

- `dmforge prompt generate`: Write all prompts to a file
- `dmforge prompt show [name]`: Preview a single prompt interactively

---

## 📄 Prompt Structure

A spell called 'Fireball', a level 3 Evocation spell. Used by: Wizard, Sorcerer. A bright streak flashes from your pointing finger...

yaml
Copy
Edit

Each prompt includes:

| Field      | Description                            |
|------------|----------------------------------------|
| `name`     | Spell name                             |
| `level`    | Spell level                            |
| `school`   | Spell school (Evocation, Conjuration)  |
| `classes`  | Usable classes                         |
| `desc`     | Short description (trimmed)            |
| `suffix`   | Optional style (e.g., "in anime style")|

---

## 📂 Output Formats

| Format | Output File                          | Description            |
|--------|--------------------------------------|------------------------|
| `txt`  | `prompts/{env}/spells.txt`           | Plain prompts          |
| `json` | `prompts/{env}/spells.json`          | Structured prompt list |

---

## 🛠 CLI Usage

```bash
# Generate all prompts
dmforge prompt generate

# With suffix and JSON format
dmforge prompt generate --format json --suffix "in anime style"

# Show a specific spell
dmforge prompt show fireball
🧪 Testing
Prompt features are tested via:

tests/test_generate_prompts.py

tests/test_prompt_show.py