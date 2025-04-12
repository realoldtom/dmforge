# 🧠 Dev Hints & AI Copilot Tips

A working reference for how to use GitHub Copilot, ChatGPT, and other LLM tools safely while building DMForge.

---

## 🛡️ Hallucination Defense Strategies

- ✅ Always **read** Copilot's output — don’t accept blindly
- ✅ Break tasks into **small steps** to get better suggestions
- ✅ Ask Copilot **why it suggests something** if unsure
- ✅ Prefer **standard libraries** unless there's a good reason
- ❌ Don’t let Copilot generate full files or config from scratch — build those incrementally

---

## 💡 Copilot Usage Tips

- Start with **comment-based scaffolds**:

```python
# Generate a prompt for Fireball with character class and race
```

- Use **docstring summaries** to explain function behavior
- Try typing **“def ”** and wait for helpful completion
- Use it to generate **test scaffolds**, then fill in logic yourself

---

## 🛠️ CLI Example Patterns

```bash
# Check project status
python scripts/session_status.py

# Start dev session
python scripts/start_dev.py

# Run tests
python scripts/test.py

# Build and tag release
python scripts/release.py
```

---

## 🧰 Building Safely with AI

- Use **asserts** even before full test coverage
- Document why something exists in dev-log.md
- Let future-you know which parts were Copilot-assisted

---
