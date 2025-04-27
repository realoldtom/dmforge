import re
import pytest
from src.utils.formatting import (
    abbreviate_duration,
    components_short,
    spell_effect_snippet,
)

# -- Tests for abbreviate_duration ------------------------------------------------


@pytest.mark.parametrize(
    "raw,expected",
    [
        # direct dictionary matches
        ("Instantaneous", "Inst."),
        ("Until dispelled", "Disp."),
        ("Concentration, up to", "Conc."),
        # concentration with minutes
        ("Concentration, up to 10 minutes", "Conc. 10 min"),
        ("Concentration while active for 600 minutes", "Conc. 600 min"),
        # hours
        ("1 hour", "1 hr"),
        ("10 hours", "10 hr"),
        # “Up to” variants
        ("Up to 5 minutes", "≤5 min"),
        ("Up to 2 hours", "≤2 hr"),
        # fallback (shorten to first 6 chars + ellipsis)
        ("Some very long duration string", "Some v…"),
    ],
)
def test_abbreviate_duration(raw, expected):
    assert abbreviate_duration(raw) == expected


# -- Tests for components_short --------------------------------------------------


@pytest.mark.parametrize(
    "raw,expected",
    [
        (None, ""),
        ("", ""),
        ([], ""),
        # list input
        (["V", "S", "M"], "V, S, M"),
        (("V", None, "M"), "V, M"),
        # string input
        ("V,S,M", "V, S, M"),
        ("V, S, M", "V, S, M"),
        (" V , S ,    M  ", "V, S, M"),
        ("V,,M", "V, M"),
    ],
)
def test_components_short(raw, expected):
    assert components_short(raw) == expected


# -- Tests for spell_effect_snippet ------------------------------------------------

SAMPLE_DESC = """
A bright ray of frost streaks toward a target.  
On hit, the target takes 1d8 cold damage.  
DC 15 to resist.  
At higher levels, this increases by 1d8.
Duration: Instantaneous.
Range: 60 feet.
You unleash the chill from your fingertips.
"""


def test_spell_effect_snippet_basic():
    snippet = spell_effect_snippet(SAMPLE_DESC, max_chars=100)
    # mechanics (dice, DC, headers) should be stripped
    assert "1d8" not in snippet
    assert "DC 15" not in snippet
    assert not re.search(r"\bRange:", snippet)
    # pronoun replacement
    assert "the caster" in snippet
    # ends with ellipsis or period, and <=100 chars
    assert len(snippet) <= 100
    assert snippet.endswith(("…", "."))


def test_spell_effect_snippet_empty():
    assert spell_effect_snippet("", max_chars=50) == ""
    assert spell_effect_snippet(None, max_chars=50) == ""


@pytest.mark.parametrize("max_chars", [20, 50, 120])
def test_spell_effect_snippet_truncation(max_chars):
    long_desc = "You conjure a massive wall of fire that burns everything in its path. It lasts for 1 minute."
    out = spell_effect_snippet(long_desc, max_chars=max_chars)
    assert len(out) <= max_chars
    # Should still contain "caster"
    assert "caster" in out
