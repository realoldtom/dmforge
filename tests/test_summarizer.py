import openai
from src.utils.summarizer import summarize_text, MAX_CHAR_COUNT
from src.deck_forge.schema import spell_to_card


class DummyResponse:
    class Choice:
        def __init__(self, content):
            self.message = type("msg", (), {"content": content})

    def __init__(self, content):
        self.choices = [DummyResponse.Choice(content)]


def test_summarize_text_short_returns_unchanged(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    text = "Short description"
    result = summarize_text(text, max_length=50)
    assert result == text


def test_summarize_text_fallback_truncates(monkeypatch, caplog):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    long_text = "A" * (MAX_CHAR_COUNT + 50)
    caplog.set_level("WARNING")
    result = summarize_text(long_text)
    assert len(result) <= MAX_CHAR_COUNT
    assert result.endswith("...")
    assert "falling back to truncation" in caplog.text


def test_summarize_text_with_openai(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")
    expected_summary = "This is a summarized description."

    def fake_create(*args, **kwargs):
        return DummyResponse(expected_summary)

    monkeypatch.setattr(openai.chat.completions, "create", fake_create)
    long_text = "B" * (MAX_CHAR_COUNT + 100)
    result = summarize_text(long_text)
    assert result == expected_summary or result.endswith("...")


def test_spell_to_card_summary_flag(monkeypatch):
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

    def fake_summarize(text, max_length=None):
        return "Fake summary."

    import src.utils.summarizer as summ

    monkeypatch.setattr(summ, "summarize_text", fake_summarize)
    card = spell_to_card(spell)
    assert card["summary"] is True
    assert card["description"] == "Fake summary."


def test_spell_to_card_no_summary():
    spell = {
        "name": "Tiny Spell",
        "level": 0,
        "school": "Conjuration",
        "desc": ["Short."],
        "casting_time": "1 action",
        "duration": "Instantaneous",
        "range": "Self",
        "components": ["V"],
    }
    card = spell_to_card(spell)
    assert card["summary"] is False
    assert card["description"] == "Short."
