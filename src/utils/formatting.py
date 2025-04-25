# utils/formatting.py
import re

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
