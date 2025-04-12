# 📦 DMForge Release Notes

---

## v0.1.0 – Phase 0 Complete: Environment & Developer Workflow
📅 Released: 2025-04-12

### ✅ Summary
Initial system foundation completed. DMForge now has a complete development environment, CLI entry, project structure, environment separation, and internal tooling.

---

### 🔧 Core Structure
- Created folder layout: `src/`, `tests/`, `scripts/`, `docs/`, `exports/`, `data/`
- Added `main.py` CLI entry point using Typer
- Initialized virtual environment and `requirements.txt`
- Added `.gitignore`, `.vscode/settings.json`, and `.pre-commit-config.yaml`

---

### 🧠 Developer Tools
- `start_dev.py` – Session launcher with Git and log summary
- `end_dev.py` – Tests, formats, logs, and commits session
- `lint.py`, `test.py`, `release.py`, `snapshot.py` – Core automation scripts
- `session_status.py` and `task_tracker.py` – Utility scripts for workflow tracking

---

### 🌍 Environment Separation
- Added `config.yaml`, `.env`, `get_env()` utility
- Dynamic output paths via `get_output_path()`
- Snapshot routing to `.snapshots/{env}/`
- Release protection in `dev` mode
- CLI override flag: `--env prod`

---

### 📚 Documentation
- `README.md` – Setup & usage
- `dev-log.md`, `session_plan.md`, `reset_routine.md`
- `docs/project_structure.md`, `cli_reference.md`, `how_it_works.md` (stub)
- `dev_hints.md` – Copilot strategies and hallucination defense

---

### 🏁 Status
✅ Phase 0 Complete  
🚧 Ready to begin Phase 1: Automation & Learning Support
