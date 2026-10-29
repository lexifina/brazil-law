"""Fetch what Lei 8.112/1990 (Regime Jurídico dos Servidores Públicos Civis da União) needs beyond batch 3's pins.

    python -X utf8 scripts/brazil-law/rju/fetch_rju.py gap <id> <planalto url>   # pin + fetch one page
    python -X utf8 scripts/brazil-law/rju/fetch_rju.py plan                      # everything pinned (cached: no requests)

Batch 3 (../batch3/fetch_batch3.py) already pinned and fetched the annotated page l8112cons.htm, the consolidated page
l8112compilado.htm and every law their notes cite (../batch3/sources_batch3.json). This script imports it unchanged and
only points its pin file at rju/sources_rju.json, so batch 3's pins (and its part, 90-batch3.json) stay as they are.
It pins the pages batch 3 lacked: the Atos Declaratórios of the President of Congress that ended the lapsed Medidas
Provisórias (linked from the RJU page's '(Vigência encerrada)' notes), the right page for MP 765/2016 (batch 3 had
pinned L8270.htm by mistake) and the conversion laws the MP pages name.

Planalto is never contacted: Common Crawl first, then archive.org `id_` captures, both through
scripts/gitlaw_common/wayback.py (one machine-wide adaptive archive.org rate).
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "batch3"))
import fetch_batch3 as FB  # noqa: E402  (configures ../proc/fetch_proc.py for batch 3)

F = FB.F
F.SRC = HERE / "sources_rju.json"
F.OTHER_SRC = [HERE.parent / "batch3" / "sources_batch3.json", *F.OTHER_SRC]

def plan() -> int:
    """Fetch every page pinned in rju/sources_rju.json into ../.cache/cc (no request when already cached)."""
    bad = 0
    for item in F.load()["fetch"]:
        if item.get("cc"):
            body = FB.wayback.cc_get(dict(item["cc"]), cache=FB.CC_CACHE)
        else:
            body = FB.wayback.get(item["url"], ts=item["ts"], cache=FB.CC_CACHE)
        ok = FB.good(body)
        bad += not ok
        print("ok " if ok else "BAD", item["id"], len(body or b""))
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["gap"]:
        sys.exit(FB.gap(sys.argv[2], sys.argv[3]))
    if sys.argv[1:2] == ["plan"]:
        sys.exit(plan())
    sys.exit("usage: fetch_rju.py gap <id> <planalto url> | plan")
