# 📁 DMForge Project Structure

A reference for understanding the folder and file layout of DMForge.

---

## Top-Level

| Path | Purpose |
|------|---------|
| `main.py` | CLI entry point using Typer |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Exclude files from version control |
| `.pre-commit-config.yaml` | Lint/test hooks before commit |
| `.vscode/` | Project-specific editor settings |
| `README.md` | Setup and usage instructions |
| `dev-log.md` | What was done and why (chronological) |
| `session_plan.md` | Intention for the current session |
| `reset_routine.md` | How to restart after a break |
| `done_log/` | Timestamped summaries of completed work |
| `.snapshots/` | Snapshots of file state and structure |

---

## Code

| Path | Purpose |
|------|---------|
| `src/` | All core logic modules (spell cards, prompts, etc.) |
| `src/utils/` | Reusable helper functions |
| `scripts/` | Developer automation scripts (start, end, test, etc.) |
| `tests/` | Unit tests |

---

## Outputs

| Path | Purpose |
|------|---------|
| `data/` | Cached or transformed data files (dev/prod separated) |
| `exports/` | Generated decks, PDFs, or prompts |

---

