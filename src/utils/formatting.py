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


def abbreviate_duration(raw: str) -> str:
    # Direct dictionary match
    if raw in _ABBREV:
        return _ABBREV[raw]

    # “Concentration, up to 10 minutes” → “Conc. 10 min”
    m = re.match(r"Concentration.*,.*?(\d+)\s*minute", raw, flags=re.I)
    if m:
        mins = int(m.group(1))
        return f"Conc. {_TIME.get(mins, f'{mins} min')}"

    # “1 hour” → “1 hr”
    m = re.match(r"(\d+)\s*hour", raw, flags=re.I)
    if m:
        hrs = int(m.group(1))
        return _TIME.get(hrs * 60, f"{hrs} hr")

    # --- NEW:  “Up to N minute(s) / hour(s)” ---
    m = re.match(r"Up to (\d+)\s*minute", raw, flags=re.I)
    if m:
        mins = int(m.group(1))
        return f"≤{mins} min"  # thin-space keeps it together

    m = re.match(r"Up to (\d+)\s*hour", raw, flags=re.I)
    if m:
        hrs = int(m.group(1))
        return f"≤{hrs} hr"

    # Fallback: keep first 9 chars + ellipsis
    return raw[:6] + "…"


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
    # remove dice, DCs, ranges, melee/ranged weapon text, etc.
    (\b\d+d\d+\b)|                       # 2d6, 8d8 ...
    (\bDC\s*\d+\b)|                     # DC 15
    (\b(range|duration|components):.*?$)|  # headers
    (\b(at\s+higher\s+levels?).*)       # scaling text
    """,
    flags=re.I | re.M | re.S | re.VERBOSE,
)


def spell_effect_snippet(desc: str, max_chars: int = 120) -> str:
    """
    Return a compact, cinematic phrase describing the spell's visual effect.

    Examples
    --------
    "A streak of flame whips from your finger..." -> "A streak of flame whips
    from a caster’s hand, erupting into a roaring fireball."

    Notes
    -----
    • Removes mechanics, dice numbers, section headers.
    • Rewrites 2nd-person (“you”) to 3rd-person (“the caster”).
    • Trims to `max_chars` without cutting mid-word.
    """
    if not desc:
        return ""

    # 1) strip line breaks
    text = " ".join(desc.splitlines())

    # 2) kill obvious mechanics
    text = _MECH_REGEX.sub("", text)

    # 3) first sentence (up to the first ‘.’ or 150 chars)
    m = re.match(r"(.{10,200}?\.)(\s|$)", text)
    text = m.group(1) if m else text[:200]

    # 4) 2nd-person ➜ 3rd-person
    text = re.sub(r"\b[Yy]ou\b", "the caster", text)

    # 5) collapse doubled spaces
    text = re.sub(r"\s{2,}", " ", text).strip()

    # 6) final safe truncate
    return shorten(text, width=max_chars, placeholder="…")
