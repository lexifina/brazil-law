"""Fetch batch 3 of the Brazil corpus: the Código Tributário Nacional (Lei 5.172/1966), the Estatuto da Criança e do
Adolescente (Lei 8.069/1990), the Código Eleitoral (Lei 4.737/1965) and Lei 8.112/1990, and every law their notes cite.

    python -X utf8 scripts/brazil-law/batch3/fetch_batch3.py pages     # pin + fetch the annotated and compiled pages
    python -X utf8 scripts/brazil-law/batch3/fetch_batch3.py laws      # pin + fetch every amending law the notes link to
    python -X utf8 scripts/brazil-law/batch3/fetch_batch3.py missing   # cited laws with no link: try Planalto's paths
    python -X utf8 scripts/brazil-law/batch3/fetch_batch3.py lexml     # LexML record of every cited law (DOU day)
    python -X utf8 scripts/brazil-law/batch3/fetch_batch3.py plan      # fetch everything pinned in sources_batch3.json

This imports ../proc/fetch_proc.py (the CPP/CDC helper) and only changes its configuration: the pages, the pin file
(batch3/sources_batch3.json) and the politeness. A page another Brazil script already pinned is reused at the same
capture. Every Planalto page is an Internet Archive raw (`id_`) capture of the Planalto URL; Planalto itself is never
contacted.

Politeness: the first pages and laws were fetched through ../fetch.py with at most one archive.org request per 3 s
(coordinator, 2026-10-28, before 21:45Z). From 21:45Z (coordinator's FAST ARCHIVE ACCESS) gaps go through
scripts/gitlaw_common/wayback.py: Common Crawl first (cc_captures / cc_get; the pin keeps crawl, WARC file, offset and
length), archive.org only for what Common Crawl lacks (wayback.captures / wayback.get, one machine-wide adaptive rate).

    python -X utf8 scripts/brazil-law/batch3/fetch_batch3.py gap <id> <planalto url>   # pin + fetch one page
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "proc"))
sys.path.insert(0, str(HERE))
import fetch  # noqa: E402
import fetch_proc as F  # noqa: E402
import parse_batch3  # noqa: E402,F401  (configures parse_proc: ACTS, sources) before fetch_proc imports it

sys.path.insert(0, str(HERE.parent.parent / "gitlaw_common"))
import wayback  # noqa: E402

CC_CACHE = HERE.parent / ".cache" / "cc"   # .cache is gitignored ('*')

F.SRC = HERE / "sources_batch3.json"
F.OTHER_SRC = [HERE.parent / "proc" / "sources_proc.json", HERE.parent / "sources_phase2.json",
               HERE.parent / "codes" / "sources_codes.json", HERE.parent / "clt" / "sources_clt.json"]
F.PAGES = parse_batch3.PAGES


def _polite(host: str) -> None:
    """No own archive.org delay any more (coordinator, 21:45Z); 1 s per host as in ../fetch.py."""
    F._orig_polite(host)


fetch._polite = _polite


def good(b: bytes | None) -> bool:
    return bool(b) and len(b) > 1500 and not re.search(rb"Please enable JavaScript|Acesso Negado|TSPD", b[:6000])


def gap(ident: str, url: str) -> int:
    """Pin one page: the newest good Common Crawl capture, else the newest good archive.org capture."""
    plan = F.load()
    if any(i["id"] == ident and (i.get("ts") or i.get("cc")) for i in plan["fetch"]):
        print("already pinned", ident)
        return 0
    bare = url.split("://", 1)[1]
    recs = wayback.cc_captures(bare, crawls=wayback.cc_crawls(CC_CACHE)[:16], cache=CC_CACHE)
    recs = sorted((r for r in recs if str(r.get("status")) == "200"), key=lambda r: r["timestamp"], reverse=True)
    for r in recs:
        body = wayback.cc_get(r, cache=CC_CACHE)
        if good(body):
            item = {"id": ident, "url": url, "cc": {k: r[k] for k in ("crawl", "timestamp", "filename", "offset", "length")}}
            break
    else:
        caps = sorted(wayback.captures(bare, cache=CC_CACHE), key=lambda c: c["timestamp"], reverse=True)
        item = None
        for c in caps:
            body = wayback.get(url, ts=c["timestamp"], cache=CC_CACHE)
            if good(body):
                item = {"id": ident, "url": url, "ts": c["timestamp"], "via": "wayback.py"}
                break
        if item is None:
            print("NO CAPTURE", ident, url, "(Common Crawl:", len(recs), "captures; archive.org:", len(caps), ")")
            return 1
    plan = F.load()
    plan["fetch"] = [i for i in plan["fetch"] if i["id"] != ident] + [item]
    F.save(plan)
    print("pinned", ident, item.get("cc", {}).get("crawl") or item.get("ts"), len(body))
    return 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["gap"]:
        sys.exit(gap(sys.argv[2], sys.argv[3]))
    sys.exit(F.main(sys.argv[1:]))
