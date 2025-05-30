# 📦 DMForge Changelog

This changelog documents the incremental, release-tagged development of DMForge — a solo-developer toolkit for modular D&D 5e content generation.

---

## v0.2.0 – Phase 1 Complete: Automation & Learning Support  
📅 Released: 2025-04-13

### ✅ Summary  
Developer support systems are now in place — including logs, microtask tracking, session automation, changelog generation, and CLI help integration.

---

### 🧠 Developer Logging & Support
- Added `dev_hints.md` for Copilot usage and hallucination defense
- Added `session_log.md` to track dev sessions by date
- Enhanced `scripts/start_dev.py` and `end_dev.py` to update `session_log.md` automatically
- Created `task_log.md` and upgraded `task_tracker.py` with tagging and timestamps
- Added `session_plan.md` and `reset_routine.md` for solo dev memory management

---

### 📘 Documentation Enhancements
- Added `docs/project_structure.md` to document folder roles
- Added `docs/cli_reference.md` for Typer-based CLI command reference
- Added `docs/workflow.md` outlining full start-to-end solo dev routine
- Stubbed and then auto-generated `docs/how_it_works.md` from `snapshot.py`

---

### ⚙️ Automation Tools
- Enhanced `snapshot.py` to generate module summaries and how_it_works.md
- Added `generate_changelog.py` to build changelogs from Git log
- Added `dmforge help` CLI command to print overview, usage, and links to docs

---

### 🏁 Status
✅ Phase 1 complete  
🚧 Ready to begin Phase 2: Core Infrastructure (modular CLI, testing, config)

---

## v0.1.0 – Phase 0 Complete: Environment & Developer Workflow  
📅 Released: 2025-04-12

### ✅ Summary  
Initial system foundation completed. DMForge now has a full project structure, CLI entry, dev/prod environment separation, and automation scaffolding.

---

### 🧱 Core Structure
- Created folder layout: `src/`, `tests/`, `scripts/`, `docs/`, `exports/`, `data/`
- Added `main.py` CLI entry point using Typer
- Initialized `.gitignore`, `.vscode/settings.json`, `.pre-commit-config.yaml`, and `requirements.txt`

---

### 🧰 Core Scripts
- `start_dev.py` – Start session, show logs and Git state
- `end_dev.py` – Run tests, format code, commit, and log session
- `lint.py`, `test.py`, `release.py`, `snapshot.py` – Core automation scripts
- `session_status.py` – Git diff/branch view
- `task_tracker.py` – CLI microtask logger

---

### 🌍 Environment Separation
- Added `config.yaml` and `.env` support
- Implemented `get_env()` and `get_output_path()` utilities
- Routed output by environment (e.g., `.snapshots/dev/`)
- Added `--env` CLI override and protected `release.py` from running in `dev`

---

### 🧠 Docs & Orientation
- Created `README.md`, `dev-log.md`, `reset_routine.md`
- Session management system enabled and tracked in `done_log/`

---

### 🏁 Status
✅ Phase 0 complete  
🚧 Began Phase 1: Logging, developer support tools, automation

---
## v0.3.0 – Phase 2 Complete: CLI & Test Infrastructure  
📅 Released: 2025-04-13

### ✅ Summary  
DMForge now has a modular CLI, full dev/prod environment support, internal helper utilities, and automated test coverage for all Phase 2 components.

---

### ⚙️ CLI Architecture
- Refactored CLI into `src/cli/` using Typer
- Added subcommands: `dmforge fetch`, `dmforge deck`
- CLI context supports `--env` override
- Rich-based CLI output with banners and styling

---

### 🧪 Test Infrastructure
- Integrated `pytest` with `tests/` structure
- Added coverage for:
  - `env.py`, `paths.py`, `console.py`
  - `snapshot.py`, `task_tracker.py`
  - CLI root (`version`, `help`)
- `pre-commit` with `black` + `ruff`

---

### 🧠 Utilities
- `src/utils/` now includes:
  - `env.py`: config.yaml + .env logic
  - `paths.py`: environment-based file routing
  - `console.py`: rich formatting helpers

---

### 🏁 Status
✅ Phase 2 complete  
🚧 Ready to begin Phase 3: SRD Fetching + Caching

## v0.4.0 – Phase 3 Complete: SRD Data Ingestion  
📅 Released: 2025-04-13

### ✅ Summary  
DMForge can now fetch and cache structured SRD content for downstream use in prompts, scenes, and card decks.

---

### 📥 SRD Fetching Features
- CLI: `dmforge fetch srd` now supports:
  - `--spells`, `--traits`, `--features`, `--all`
- Fetches from: https://www.dnd5eapi.co
- Output format: `data/{env}/{type}.json`
- Includes normalized structure (for spells)

---

### 🧪 Testing
- Added mock-based tests for:
  - `fetch_srd_spells`
  - `fetch_srd_traits`
  - `fetch_srd_features`
- Verifies output, re-fetching logic, error handling

---

### 🏁 Status
✅ Phase 3 complete  
🚧 Ready for Phase 4: Prompt Generator


---

### 📄 `CHANGELOG.md`

```markdown
## v0.5.0 – Phase 4 Complete: AI Prompt Generator  
📅 Released: 2025-04-13

### ✅ Summary  
DMForge can now generate AI-style text prompts for spell cards and previews.

---

### 🎨 Prompt Generator

- `generate_spell_prompt()` formats clean natural language prompt from spell data
- New CLI:
  - `dmforge prompt generate` (outputs `.txt` or `.json`)
  - `dmforge prompt show [name]` (preview a specific spell's prompt)

---

### 🧪 Testing

- Tests for:
  - Prompt formatting and suffixes
  - JSON output structure
  - CLI command `prompt show`

---

### 🏁 Status
✅ Phase 4 complete  
🚧 Next: Phase 5 – Card Layout System

## v0.6.0 – Phase 5 Complete: Card Layout System  
📅 Released: 2025-04-13

---

### ✅ Summary

DMForge now supports full spell card layout and rendering, including:

- 📄 Spell card schema with layout-ready fields
- 🖨 CLI rendering: `dmforge deck render --format pdf`
- 🧾 Print-ready grid sheets: `--layout sheet`
- 🎴 One-card-per-page layout: `--layout cards`
- 🌐 HTML preview with Jinja2 template
- ✅ WeasyPrint for high-fidelity PDF output

---

### 🖥 CLI Improvements

- `deck build`: generates JSON deck from spells
- `deck render`: renders to HTML or PDF
- `--layout sheet`: 6 cards per A4 page
- `--layout cards`: 1 card per page
- Templates stored in `templates/`
- Debug HTML support in dev mode (manual)

---

### 🧪 Testing

- `spell_to_card()` schema converter tested
- Deck generator and CLI tested
- HTML + PDF output tested for structure and layout

---

### 🏁 Status
✅ Phase 5 complete  
🎯 Next: Phase 6 – Layout Formatting Enhancements
