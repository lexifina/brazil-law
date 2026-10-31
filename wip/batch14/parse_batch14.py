"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch14<x>.json (SCHEMA.md corpus parts): more major federal
acts not yet in the corpus, published in small parts of 2-4 acts each (99-batch14a, 99-batch14b, ...).

    BATCH14_PART=a python -X utf8 scripts/brazil-law/batch14/parse_batch14.py [--stats] [--dry]

Imports ../batch13/parse_batch13.py (which configures batch 12 and everything below it, plus batch 13's hand tables) with
no act of its own, and replaces only the configuration: the acts, the in-force days, the hand tables for these acts, the
pins and the output. Earlier parts are not touched. No network.

BATCH14_PART selects the part (its acts are PARTS[part]); BATCH14_ACTS=<slug,...> selects acts for trial runs
(BATCH14_OUT=<file> writes elsewhere).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH13_ACTS"] = "-"   # batch 13 configures no act of its own here
os.environ.pop("BATCH13_OUT", None)
os.environ.pop("BATCH13_PART", None)
sys.path.insert(0, str(FOLDER / "batch13"))
import parse_batch13 as B13  # noqa: E402

B12, B11, B10, B9, B8, B7, B6, B5, B, P = (B13.B12, B13.B11, B13.B10, B13.B9, B13.B8, B13.B7, B13.B6, B13.B5, B13.B,
                                           B13.P)
PL = P.PL
PART = os.environ.get("BATCH14_PART", "a")
B5.OUT = Path(os.environ.get("BATCH14_OUT") or FOLDER / "corpus.d" / f"99-batch14{PART}.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = {
    # 14a
    "lc87": "leis/lcp/lcp87.htm",
    "lc116": "leis/lcp/lcp116.htm",
}
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = B6.PAGES = B7.PAGES = B8.PAGES = B9.PAGES = B10.PAGES = B11.PAGES = B12.PAGES = B13.PAGES = PAGES


def _act(slug, short, page, consolidated, law, title, digits):
    return {"slug": slug, "short": short, "page": page, "consolidated": consolidated, "law": law, "title": title,
            "digits": digits, "url": PL + PAGES[page]}


ALL_ACTS: list[dict] = [
    _act("lei-kandir", "LC87", "lc87", "lc87", "lc-87-1996",
         "Lei Kandir - ICMS (Lei Complementar nº 87, de 13 de setembro de 1996)", 2),
    _act("lei-do-iss", "LC116", "lc116", "lc116", "lc-116-2003",
         "Lei do ISS (Lei Complementar nº 116, de 31 de julho de 2003)", 2),
]
PARTS: dict[str, list[str]] = {
    "a": ["lei-kandir", "lei-do-iss"],
}
VERIFIED: list[str] = PARTS.get(PART, [])
ENABLED = [s for s in os.environ.get("BATCH14_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
for M in (B7, B8, B9, B10, B11, B12, B13):
    M.ACTS[:] = ACTS

_PUB = "'Esta Lei entra em vigor na data de sua publicação'"
ACT_DAY_ALL: dict[str, tuple[str, str]] = {
}
_L = B._act_law
ACT_LAWS_ALL: dict[str, dict] = {
}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# batch 13's act-specific tools emptied (law facts in VIGENCIA_FIXED, MP_LAPSE, ... are kept: printed only where used)
B.EXPLAINED.clear()
B8.SPAN_FIX.clear()
B8.LABEL_FIX.clear()
B9.WORD_FIX.clear()
P.VETO_PROMULGATION = {}
P.VETO_PROMULGATED_UNITS = {}
P.NOTE_FIX = {}
B13.OPEN_ITEMS.clear()

# ---------------------------------------------------------------------------------------------------------------
# hand tables for these acts, each read from the official pages named in the reason

OPEN_ITEMS = B13.OPEN_ITEMS

SRC = HERE / "sources_batch14.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
