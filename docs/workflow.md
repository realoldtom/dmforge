# 🔄 DMForge Developer Workflow

This document describes the standard solo dev routine used to maintain code quality, track progress, and reduce mental fatigue.  
All tools here were built specifically for this solo developer environment.

---

## 🧠 Philosophy

> “Slow is smooth, smooth is fast.”

- Work in small, focused microtasks
- Log what you do so you don’t have to remember
- Automate repetitive or error-prone steps
- Use the environment safely (dev vs prod)

---

## 🏁 Daily Workflow

### ✅ Start of Session

Run:

```bash
python scripts/start_dev.py
```

This will:
- Show your current Git status
- Show your last `dev-log.md` and current `session_plan.md`
- Log the start of a new session in `session_log.md`
- Print the active environment (DEV or PROD)

---

### 🧱 During Development

Use:

```bash
python scripts/task_tracker.py
```

To:
- Log each microtask
- Include a short description and optional tag (e.g., `phase1`, `scene_forge`)

Also refer to:
- `session_plan.md` for your short-term plan
- `dev_log.md` for daily notes or decisions

---

### 📸 Snapshots (Optional Mid-Session or Pre-Release)

Run:

```bash
python scripts/snapshot.py
```

This will:
- Save a list of files to `.snapshots/{env}/`
- Auto-generate `docs/how_it_works.md` with module summaries

---

### 🚧 End of Session

Run:

```bash
python scripts/end_dev.py
```

This will:
- Run tests
- Auto-format code
- Log a description to `done_log/`
- Commit your changes
- Update `session_log.md` with the end time
- Print a 2-level folder tree to confirm file structure

---

### 📦 Releasing

When you're ready to release:

```bash
python scripts/release.py
```

> Releases are blocked if you’re in `dev` mode.

Tag your release, then run:

```bash
python scripts/generate_changelog.py
```

This will:
- Append recent commits to `CHANGELOG.md` using Git log
- Allow you to override the version (e.g., `--version v0.2.0`)

---

## 🧾 Files That Help You Stay on Track

| File | Purpose |
|------|---------|
| `dev-log.md` | Notes, decisions, observations |
| `task_log.md` | Microtask tracker (timestamp + tag) |
| `session_log.md` | Chronological dev sessions |
| `session_plan.md` | Sticky note: what you’re doing right now |
| `reset_routine.md` | Checklist for returning after a break |

---

## 🔁 Reset Routine (Post-Break)

1. Open VS Code
2. Run `scripts/start_dev.py`
3. Review `session_log.md`, `session_plan.md`, and `dev-log.md`
4. Pick your next microtask or run `task_tracker.py`

---

