"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch15<x>.json (SCHEMA.md corpus parts): Lei 8.212/1991
(custeio da Seguridade Social, part 99-batch15a) and Lei 8.213/1991 (benefícios da Previdência Social, part 99-batch15b).

    BATCH15_PART=a python -X utf8 scripts/brazil-law/batch15/parse_batch15.py [--stats] [--dry]

Imports ../batch14/parse_batch14.py (which configures batch 13 and everything below it, plus batch 14's hand tables)
with no act of its own, and replaces only the configuration: the acts, the in-force days, the hand tables for these acts,
the pins and the output. Earlier parts are not touched. No network.

New here: the Medida Provisória 905/2019 -> 955/2020 sequence (MP_PAIRS, ported from clt/parse_clt.py) for the proc
pipeline, and footnote numbers on Lei 8.212's page (l8212cons.htm prints numbered footnotes and their markers).

After writing a part run ../effects_fix.py on it (effect days).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH14_PART"] = "-"   # batch 14 configures no act of its own here
os.environ.pop("BATCH14_ACTS", None)
os.environ.pop("BATCH14_OUT", None)
sys.path.insert(0, str(FOLDER / "batch14"))
import parse_batch14 as B14  # noqa: E402

B13, B12, B11, B10, B9, B8, B7, B6, B5, B, P = (B14.B13, B14.B12, B14.B11, B14.B10, B14.B9, B14.B8, B14.B7, B14.B6,
                                                B14.B5, B14.B, B14.P)
PL = P.PL
PART = os.environ.get("BATCH15_PART", "a")
B5.OUT = Path(os.environ.get("BATCH15_OUT") or FOLDER / "corpus.d" / f"99-batch15{PART}.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = dict(B14.PAGES)
B.PAGES.clear()
B.PAGES.update(PAGES)
for M in (B5, B6, B7, B8, B9, B10, B11, B12, B13, B14):
    M.PAGES = PAGES

ALL_ACTS = [a for a in B14.ALL_ACTS if a["slug"] in ("lei-de-custeio-da-seguridade-social",
                                                     "lei-de-beneficios-da-previdencia-social")]
_C, _BN = "lei-de-custeio-da-seguridade-social", "lei-de-beneficios-da-previdencia-social"
PARTS: dict[str, list[str]] = {"a": [_C], "b": [_BN]}
VERIFIED: list[str] = PARTS.get(PART, [])
ENABLED = [s for s in os.environ.get("BATCH15_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
for M in (B7, B8, B9, B10, B11, B12, B13, B14):
    M.ACTS[:] = ACTS
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in B14.ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in B14.ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# batch 14's act-specific tables are keyed by act slug or page and do nothing here; its printed-everywhere lists emptied
B.EXPLAINED.clear()
B13.OPEN_ITEMS.clear()
B9.REPEALS.clear()

SRC = HERE / "sources_batch15.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
