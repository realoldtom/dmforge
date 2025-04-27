# utils/formatting.py
import re
from textwrap import shorten

_ABBREV = {
    "Instantaneous": "Inst.",
    "Until dispelled": "Disp.",
    "Concentration, up to": "Conc.",
    "Concentration,‎ up‎ to": "Conc.",  # non-breaking space variant
}

_TIME = {  # minutes → abbreviation
    1: "1 min",  # thin space keeps number + unit together
    10: "10 min",
    60: "1 hr",
    600: "10 hr",
    1440: "24 hr",
}


def components_short(raw) -> str:
    """
    Return spell components in the compact 'V, S, M' form.

    Accepts:
      • ['V', 'S', 'M']
      • "V,S,M" or "V, S, M"
      • None / empty

    Always returns a string joined by ', ' (comma + space).
    """
    if not raw:
        return ""

    # 1) If we already have a list/tuple → join with ', '
    if isinstance(raw, (list, tuple)):
        parts = [str(x).strip() for x in raw if x]
        return ", ".join(parts)

    # 2) If it's a string → strip spaces, split on ',', then re-join
    parts = [p.strip() for p in str(raw).split(",") if p.strip()]
    return ", ".join(parts)


_MECH_REGEX = re.compile(
    r"""
    (\b\d+d\d+\b)                                       # dice: 2d6, 8d8...
    |(\bDC\s*\d+\b)                                     # DC 15
    |(\b(?:range|duration|components):\s*[^.]*\.)       # headers up to the next period
    |(\bat\s+higher\s+levels?[^.]*\.)                   # scaling text up to the next period
    """,
    flags=re.I | re.M | re.VERBOSE,
)


def abbreviate_duration(raw: str) -> str:
    # 1) Direct dictionary match
    if raw in _ABBREV:
        return _ABBREV[raw]

    # 2) “Concentration … N minutes” → “Conc. N min” (always show minutes)
    m = re.search(r"Concentration.*?(\d+)\s*minute", raw, flags=re.I)
    if m:
        mins = int(m.group(1))
        return f"Conc. {mins} min"

    # 3) “Up to N minutes” → “≤N min”
    m = re.search(r"Up to\s+(\d+)\s*minute", raw, flags=re.I)
    if m:
        mins = int(m.group(1))
        return f"≤{mins} min"

    # 4) “Up to N hours” → “≤N hr”
    m = re.search(r"Up to\s+(\d+)\s*hour", raw, flags=re.I)
    if m:
        hrs = int(m.group(1))
        return f"≤{hrs} hr"

    # 5) “N hour(s)” → “N hr”
    m = re.search(r"^(\d+)\s*hour", raw, flags=re.I)
    if m:
        hrs = int(m.group(1))
        return _TIME.get(hrs * 60, f"{hrs} hr")

    # 6) Fallback: first 6 chars + ellipsis
    return raw[:6] + "…"


def spell_effect_snippet(desc: str, max_chars: int = 120) -> str:
    """
    Return a compact, cinematic phrase describing the spell's visual effect.

    - Strips mechanics (dice, DCs), headers (Range:/Duration:/Components:), and scaling text.
    - Chooses the sentence containing “you” (converted to “the caster”), else the first sentence.
    - Truncates safely to max_chars without cutting mid-word.
    """
    if not desc:
        return ""

    # collapse line breaks
    text = " ".join(desc.splitlines())

    # strip mechanics, headers, scaling text
    text = _MECH_REGEX.sub("", text)

    # split into sentences
    sentences = [s.strip() for s in re.split(r"(?<=[.])\s+", text) if s.strip()]

    # pick the sentence with “you”, else first
    you_idx = next(
        (i for i, s in enumerate(sentences) if re.search(r"\b[Yy]ou\b", s)), None
    )
    snippet = (
        sentences[you_idx]
        if you_idx is not None
        else (sentences[0] if sentences else "")
    )

    # replace “you” → “the caster”
    snippet = re.sub(r"\b[Yy]ou\b", "the caster", snippet)

    # collapse extra spaces
    snippet = re.sub(r"\s{2,}", " ", snippet).strip()

    # final safe truncate
    return shorten(snippet, width=max_chars, placeholder="…")
