# tests/test_summarizer.py

import os
import logging
import openai

from src.utils.summarizer import summarize_text, MAX_CHAR_COUNT
from src.deck_forge.schema import spell_to_card

# Configure logging capture
logging.getLogger().handlers.clear()
logging.basicConfig(level=logging.DEBUG)


def test_summarize_text_no_api_key_logs_and_truncates(caplog, monkeypatch):
    # make sure we really have *no* OPENAI_API_KEY for this test
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    caplog.set_level(logging.WARNING)
    long_text = "A" * (MAX_CHAR_COUNT + 50)
    result = summarize_text(long_text)
    # We should have ellipsis and be <= MAX_CHAR_COUNT
    assert result.endswith("...")
    assert len(result) <= MAX_CHAR_COUNT
    # And our warning must be exactly this
    assert "⚠️ falling back to truncation" in caplog.text


def test_summarize_text_with_api_key_invokes_openai(monkeypatch):
    # Simulate an API key present
    os.environ["OPENAI_API_KEY"] = "fake-key"

    # Prepare a fake response object
    class FakeChoice:
        message = type("M", (), {"content": "LLM generated summary"})

    class FakeResponse:
        choices = [FakeChoice()]

    called = {}

    def fake_create(*args, **kwargs):
        called["args"] = (args, kwargs)
        return FakeResponse()

    # Monkeypatch the correct method path
    monkeypatch.setattr(openai.chat.completions, "create", fake_create)

    # Short text (no summarization)
    short_text = "Hello!"
    assert summarize_text(short_text) == short_text

    # Long text triggers LLM path
    long_text = "B" * (MAX_CHAR_COUNT + 10)
    summary = summarize_text(long_text)
    assert summary == "LLM generated summary"
    # And ensure we actually called the OpenAI method
    assert "args" in called


def test_summarize_text_on_exception_truncates_and_logs_error(caplog, monkeypatch):
    # Simulate API key
    os.environ["OPENAI_API_KEY"] = "fake-key"
    caplog.set_level(logging.ERROR)

    # Cause the create call to raise
    def fake_create(*args, **kwargs):
        raise RuntimeError("API is down")

    monkeypatch.setattr(openai.chat.completions, "create", fake_create)

    long_text = "C" * (MAX_CHAR_COUNT + 20)
    result = summarize_text(long_text)
    assert result.endswith("...")  # fallback truncated
    assert "❌ OpenAI summarization failed" in caplog.text


def test_spell_to_card_summary_flag_and_description(monkeypatch):
    # Force a fake summarizer so we can observe it

    def fake_summarize(text, max_length=None):
        return "Fake summary."

    monkeypatch.setattr("src.utils.summarizer.summarize_text", fake_summarize)

    # Build a spell whose desc is definitely too long
    desc_list = ["word"] * ((MAX_CHAR_COUNT // 5) + 10)
    spell = {
        "name": "Test Spell",
        "level": 1,
        "school": "Evocation",
        "desc": desc_list,
        "casting_time": "1 action",
        "duration": "Instantaneous",
        "range": "Self",
        "components": ["V", "S"],
    }

    card = spell_to_card(spell, summarize=True)
    assert card["summary"] is True
    assert card["description"] == "Fake summary."
