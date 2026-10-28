"""placeholder: replaced below"""
from __future__ import annotations

import re

MONTHS = {"janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7,
          "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}


def decode(b: bytes) -> str:
    m = re.search(rb'charset=["\']?([\w-]+)', b[:4000], re.I)
    enc = (m.group(1).decode() if m else "windows-1252").lower()
    if enc in ("iso-8859-1", "latin1", "latin-1"):
        enc = "windows-1252"
    try:
        return b.decode(enc)
    except (UnicodeDecodeError, LookupError):
        return b.decode("windows-1252", errors="replace")


LAW_REF = re.compile(
    r"(Lei\s+Complementar|Lei|Medida\s+Provis[óo]ria|Decreto[-\s]?[Ll]ei)\s*(?:n[º°o]?\s*\.?|n\.)?\s*"
    r"(\d{1,2}(?:\.\d{3})+|\d+)(?:[-\s]*[A-Z](?![a-z]))?(?:\s*\.)?(?:\s*,)?(?:\s*de\s+(\d{1,2}\s*[./]\s*\d{1,2}\s*[./]\s*(\d{4})|"
    r"\d{1,2}º?\s+de\s+\w+\s+de\s+(\d{4})|(\d{4})))?", re.I)


def law_key(text: str, year_of: dict | None = None) -> str | None:
    """lei-14905-2024, lc-128-2008, mp-1085-2021, dl-4037-1942 for the first act named in text."""
    m = LAW_REF.search(text)
    if not m:
        return None
    kind = m.group(1).lower()
    pre = "lc" if "complementar" in kind else "mp" if kind.startswith("medida") else "dl" if kind.startswith("decreto") else "lei"
    n = int(m.group(2).replace(".", ""))
    y = m.group(4) or m.group(5) or m.group(6)
    if not y and year_of:
        y = year_of.get(f"{pre}-{n}")
    if not y:
        return None
    return f"{pre}-{n}-{y}"
