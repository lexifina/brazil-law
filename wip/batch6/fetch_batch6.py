"""Fetch the pages of batch 6 (see parse_batch6.ALL_ACTS) and every law their notes cite: ../batch5/fetch_batch5.py's
commands with batch 6's pages and pin file (batch6/sources_batch6.json).

    BATCH6_ACTS=<slug,...> python -X utf8 scripts/brazil-law/batch6/fetch_batch6.py pages|laws|missing|gap|refetch|plan

`laws` and `missing` read the pages of the acts named in BATCH6_ACTS (default: every act in ALL_ACTS).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if not os.environ.get("BATCH6_ACTS"):
    os.environ["BATCH6_ACTS"] = "*"
sys.path.insert(0, str(HERE))
import parse_batch6 as PB6  # noqa: E402

sys.path.insert(0, str(HERE.parent / "batch5"))
import fetch_batch5 as F5  # noqa: E402

if os.environ["BATCH6_ACTS"] == "*":
    PB6.ACTS[:] = PB6.ALL_ACTS
F5.PB = PB6.B5
F5.PB.ACTS = PB6.ACTS
F5.F.SRC = PB6.SRC
F5.F.PAGES = PB6.PAGES

if __name__ == "__main__":
    if sys.argv[1:2] == ["laws"] and len(sys.argv) == 2:
        sys.argv += [a["page"] for a in PB6.ACTS]
    sys.exit(F5.main(sys.argv[1:]))
