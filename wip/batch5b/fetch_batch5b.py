"""Fetch the pages of batch 5b (see parse_batch5b.ALL_ACTS) and every law their notes cite: ../batch5/fetch_batch5.py's
commands with batch 5b's pages and pin file (batch5b/sources_batch5b.json).

    BATCH5B_ACTS=<slug,...> python -X utf8 scripts/brazil-law/batch5b/fetch_batch5b.py pages|laws|missing|gap|refetch|plan

`laws` and `missing` read the pages of the acts named in BATCH5B_ACTS (all five pages are pinned by `pages`).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import parse_batch5b as PB5B  # noqa: E402  (configures parse_batch5 for batch 5b first)

sys.path.insert(0, str(HERE.parent / "batch5"))
import fetch_batch5 as F5  # noqa: E402

F5.PB = PB5B.B5
F5.F.SRC = PB5B.SRC
F5.F.PAGES = PB5B.PAGES

if __name__ == "__main__":
    if sys.argv[1:2] == ["laws"] and len(sys.argv) == 2:
        sys.argv += [a["page"] for a in PB5B.ALL_ACTS if a["slug"] in PB5B.ENABLED]
    sys.exit(F5.main(sys.argv[1:]))
