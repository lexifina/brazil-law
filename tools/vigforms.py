"""Misprinted or unusual forms of a law's own in-force clause, which the readers accept beside the standard ones
(corpus-wide audit of every law dated by the LINDB 45-day default, 2026-11-01).

Found on Planalto's pages (each checked against the page; all are the law's own closing article):
- 'Esta Lei entra vigor na data de sua publicação' ('em' missing): Leis 9.165/1995, 9.602/1998, 10.223/2001,
  10.408/2002, 12.720/2012; 'Esta Lei entra vigor após decorridos 90 (noventa) dias de sua publicação oficial': Lei
  14.310/2022;
- 'Esta lei entre em vigor na data de sua publicação' ('entre' for 'entra'): Lei 8.900/1994;
- 'O presente Decreto-Lei entra em vigor, na data de sua publicação' (subject 'O presente', comma before the day):
  Decreto-Lei 57/1966;
- 'Esta Lei, que será regulamentada no prazo de 180 (cento e oitenta) dias, entrará em vigor na data de sua publicação'
  (a relative clause between subject and verb): Lei 6.181/1974;
- 'O presente Decreto-lei entrará em vigor à data de sua publicação': read as 'na data', as the CLT reader already did
  (none of the laws so printed is dated by the other readers in any part).

clause_rx(rx) widens a reader's clause pattern by these forms (an alternation: everything the old pattern matched it
still matches); standard(clause) rewrites them to the standard wording before the day is read from the clause.
"""
from __future__ import annotations

import re

EXTRA = (r"(?:[EÊ]st[ae]|[OA]\s+presente)\s+(?:Lei|Medida\s+Provis[óo]ria|C[óo]digo|Decreto[-\s]?[LlI]ei)"
         r"(?:\s+Complementar)?(?:\s*,\s*que\s[^.;:]{1,160}?,)?\s*,?\s+(?:entra(?:r[áa])?|entre)\s+(?:em\s+)?vigor")


def clause_rx(rx: str) -> str:
    return f"(?:{rx})|(?:{EXTRA})"


def printed(clause: str) -> str:
    """The clause as printed, for a decision, when it is one of the misprinted or unusual forms above (not 'à data',
    which the CLT reader always read); else ''."""
    if not clause:
        return ""
    if (re.search(r"\bentre\s+em\s+vigor|\bentra(?:r[áa])?\s+vigor\b|\bem\s+vigor\s*,\s*na\s+data\b", clause, re.I)
            or re.match(r"[^,.]{0,60},\s*que\s", clause)):
        return clause
    return ""


def standard(clause: str) -> str:
    c = re.sub(r"\bentre(\s+em\s+vigor)", r"entra\1", clause, flags=re.I)
    c = re.sub(r"\b(entra(?:r[áa])?)\s+vigor\b", r"\1 em vigor", c, flags=re.I)
    c = re.sub(r"(\bem\s+vigor)\s+[àa]\s+(data\s+d[ae]\s+sua\s+publica)", r"\1 na \2", c, flags=re.I)
    return re.sub(r"(\bem\s+vigor)\s*,\s*(na\s+data\b)", r"\1 \2", c, flags=re.I)
