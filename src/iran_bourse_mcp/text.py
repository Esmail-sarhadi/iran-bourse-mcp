"""Persian/Arabic text normalisation.

TSETMC stores text with Arabic letters (ي ك) while users type Persian ones (ی ک).
We normalise everything we *return* to Persian letters and everything we *compare*
to a canonical key.
"""

from __future__ import annotations

import re

_LETTERS = str.maketrans(
    {
        "ي": "ی",
        "ى": "ی",
        "ك": "ک",
        "ـ": "",  # tatweel
        "‏": "",  # RLM
        "‎": "",  # LRM
        " ": " ",
    }
)
_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
_WS = re.compile(r"\s+")


def clean(value: object) -> str | None:
    """Normalise a display string (Persian letters, single spaces). ``None`` stays ``None``."""
    if value is None:
        return None
    text = str(value).translate(_LETTERS)
    text = _WS.sub(" ", text).strip()
    return text


def ascii_digits(value: str) -> str:
    return value.translate(_DIGITS)


def match_key(value: object) -> str:
    """Canonical key for comparing symbols and names (ignores spaces, ZWNJ, digit script)."""
    text = clean(value) or ""
    text = ascii_digits(text).replace("‌", "").replace(" ", "")
    return text.casefold()
