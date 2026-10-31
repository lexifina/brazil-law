"""Fetch the pages of batch 14 (see parse_batch14.ALL_ACTS) and every law their notes cite: ../batch5/fetch_batch5.py's
commands with batch 14's pages and pin file (batch14/sources_batch14.json).

    BATCH14_ACTS=<slug,...> python -X utf8 scripts/brazil-law/batch14/fetch_batch14.py pages|laws|missing|gap|refetch|plan

`laws` and `missing` read the pages of the acts named in BATCH14_ACTS (default: every act in ALL_ACTS).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if not os.environ.get("BATCH14_ACTS"):
    os.environ["BATCH14_ACTS"] = "*"
sys.path.insert(0, str(HERE))
import parse_batch14 as PB6  # noqa: E402

sys.path.insert(0, str(HERE.parent / "batch5"))
import fetch_batch5 as F5  # noqa: E402

if os.environ["BATCH14_ACTS"] == "*":
    PB6.ACTS[:] = PB6.ALL_ACTS
_complete = F5.complete


def complete(b: bytes | None) -> bool:
    """fetch_batch5.complete, also for pages saved as UTF-16 (Lei 11.340's page: '</html>' is two bytes a letter)."""
    if _complete(b):
        return True
    if b and b[:2] in (bytes([0xFF, 0xFE]), bytes([0xFE, 0xFF])):
        import re
        t = b.decode("utf-16", "replace")
        return F5.FB.good(b) and re.search(r"</html\s*>", t, re.I) is not None
    return False


F5.complete = complete
F5.PB = PB6.B5
F5.PB.ACTS = PB6.ACTS
F5.F.SRC = PB6.SRC
F5.F.PAGES = PB6.PAGES

if __name__ == "__main__":
    if sys.argv[1:2] == ["laws"] and len(sys.argv) == 2:
        sys.argv += [a["page"] for a in PB6.ACTS]
    sys.exit(F5.main(sys.argv[1:]))
