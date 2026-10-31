"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch12.json (SCHEMA.md corpus part): the four acts batch 11
deferred (Lei 6.766/1979, Lei 9.656/1998, Lei 8.742/1993, Lei 6.385/1976), as they are verified.

    python -X utf8 scripts/brazil-law/batch12/parse_batch12.py [--stats] [--dry]

Imports ../batch11/parse_batch11.py (which configures batch 10 and everything below it, plus batch 11's hand tables) with
no act of its own, and replaces only the configuration: the acts, the hand tables for these acts, the pins and the output.
Earlier parts are not touched. No network.

BATCH12_ACTS=<slug,...> selects acts for trial runs (BATCH12_OUT=<file> writes elsewhere); by default VERIFIED is
written.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH11_ACTS"] = "-"   # batch 11 configures no act of its own here
os.environ.pop("BATCH11_OUT", None)
sys.path.insert(0, str(FOLDER / "batch11"))
import parse_batch11 as B11  # noqa: E402

B10, B9, B8, B7, B6, B5, B, P = B11.B10, B11.B9, B11.B8, B11.B7, B11.B6, B11.B5, B11.B, B11.P
PL = P.PL
B5.OUT = Path(os.environ.get("BATCH12_OUT") or FOLDER / "corpus.d" / "99-batch12.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

MINE = ["lei-do-parcelamento-do-solo-urbano", "lei-dos-planos-de-saude", "lei-organica-da-assistencia-social",
        "lei-do-mercado-de-valores-mobiliarios"]
ALL_ACTS: list[dict] = [a for s in MINE for a in B11.ALL_ACTS if a["slug"] == s]
PAGES = {k: v for k, v in B11.PAGES.items() if any(k in (a["page"], a["consolidated"]) for a in ALL_ACTS)}
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = B6.PAGES = B7.PAGES = B8.PAGES = B9.PAGES = B10.PAGES = B11.PAGES = PAGES

VERIFIED: list[str] = []
ENABLED = [s for s in os.environ.get("BATCH12_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
for M in (B7, B8, B9, B10, B11):
    M.ACTS[:] = ACTS
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in B11.ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in B11.ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# batch 11's act-specific tools emptied (its law facts in VIGENCIA_FIXED etc. are kept: printed only where used)
B.EXPLAINED.clear()
B8.SPAN_FIX.clear()
B8.LABEL_FIX.clear()
B9.WORD_FIX.clear()
P.VETO_PROMULGATION = {}
P.VETO_PROMULGATED_UNITS = {}

# ---------------------------------------------------------------------------------------------------------------
# hand tables for these acts, each read from the official pages named in the reason
_LPSU = "lei-do-parcelamento-do-solo-urbano"
B8.LABEL_FIX[:] = [
    ("lpsolo", "III-A. - ao longo das águas correntes", "III-A - ao longo das águas correntes", "III-A -",
     "Lei do Parcelamento do Solo Urbano art. 4 III-A: Lei 13.913/2019's wording is printed 'III-A. -'; read as 'III-A -', "
     "so Lei 14.285/2021's wording of III-A replaces it"),
]
B9.WORD_FIX[:] = [
    ("lpsolo", "§ 1º Parágrafo único. Na hipótese de parcelamento", "§ 1º Na hipótese de parcelamento",
     "Lei do Parcelamento do Solo Urbano art. 22 § 1º: Lei 14.620/2023 art. 24 keeps the former parágrafo único as § 1º "
     "('§ 1º .....', adding §§ 2º and 3º); both Planalto pages print '§ 1º Parágrafo único. Na hipótese ...', and the "
     "history drops the leftover words 'Parágrafo único.'"),
]
_TYPO = "typesetting: the annotated page prints 'Art. {n}º.' with a full stop after the number; the consolidated page has none"
B.EXPLAINED[_LPSU] = {
    **{f"art-{n:02d}": _TYPO.format(n=n) for n in (1, 2, 4, 5, 7)},
    "art-06": _TYPO.format(n=6) + "; inciso VI reads 'caracteristicas' on the annotated page, 'características' on the "
              "consolidated page",
    "art-43": "typesetting: the annotated page ends the parágrafo único with a full stop, the consolidated page without",
    "art-22": "both Planalto pages print '§ 1º Parágrafo único. Na hipótese ...'; the history drops the leftover 'Parágrafo "
              "único.' (see the word corrections)",
}

SRC = HERE / "sources_batch12.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
