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
