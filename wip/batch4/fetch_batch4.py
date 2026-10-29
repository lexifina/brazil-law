"""Fetch batch 4 of the Brazil corpus (see parse_batch4.ACTS) and every law its notes cite.

    python -X utf8 scripts/brazil-law/batch4/fetch_batch4.py pages        # pin + fetch the acts' annotated/consolidated pages
    python -X utf8 scripts/brazil-law/batch4/fetch_batch4.py laws         # pin + fetch every law the notes link to
    python -X utf8 scripts/brazil-law/batch4/fetch_batch4.py gap <id> <planalto url>   # pin + fetch one page
    python -X utf8 scripts/brazil-law/batch4/fetch_batch4.py lexml        # LexML record of every cited law (DOU day)
    python -X utf8 scripts/brazil-law/batch4/fetch_batch4.py plan         # everything pinned (cached: no requests)

Reuses batch 3 and the RJU helper unchanged: ../batch3/fetch_batch3.py (which configures ../proc/fetch_proc.py) for
the note-link reader and the bot-page test. Pins go to batch4/sources_batch4.json; a page any other Brazil script
already pinned (sources.json, sources_phase2.json, codes/, clt/, proc/, batch3/, rju/) is reused at that capture and
not fetched again.

Planalto is never contacted. Common Crawl holds no Planalto captures of these pages (probed 2026-10-29: 0 captures in
the last 8 crawls), so every page is an Internet Archive raw (`id_`) capture fetched through
scripts/gitlaw_common/wayback.py (one machine-wide adaptive archive.org rate), cached in ../.cache/cc. A pin is the
newest capture that is not a bot-challenge or error page.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import parse_batch4 as PB  # noqa: E402  (configures batch 3 / parse_proc for batch 4 first)

sys.path.insert(0, str(HERE.parent / "batch3"))
import fetch_batch3 as FB  # noqa: E402

F = FB.F
F.SRC = HERE / "sources_batch4.json"
F.PAGES = PB.PAGES
wayback = FB.wayback
CACHE = FB.CC_CACHE


def load() -> dict:
    return json.loads(F.SRC.read_text(encoding="utf-8")) if F.SRC.exists() else {"fetch": []}


def save(plan: dict) -> None:
    tmp = F.SRC.with_suffix(".tmp")
    tmp.write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    tmp.replace(F.SRC)


def pin(ident: str, url: str, since: str = "2025") -> bool:
    """Pin ident to the newest good archive.org capture of url (one CDX request, then pages newest first)."""
    if ident in PB.sources():
        return True
    bare = url.split("://", 1)[1]
    caps = [c for c in wayback.captures(bare, cache=CACHE, since=since)]
    if not caps and since:
        caps = wayback.captures(bare, cache=CACHE)
    caps.sort(key=lambda c: c["timestamp"], reverse=True)
    for c in caps[:6]:
        if int(c.get("length") or 0) < 1500:   # CDX length is the compressed size; bot pages are tiny
            continue
        body = wayback.get(url, ts=c["timestamp"], cache=CACHE)
        if FB.good(body):
            plan = load()
            plan["fetch"] = [i for i in plan["fetch"] if i["id"] != ident] + [
                {"id": ident, "url": url, "ts": c["timestamp"], "via": "wayback.py"}]
            save(plan)
            print("pinned", ident, c["timestamp"], len(body), flush=True)
            return True
    print("NO CAPTURE", ident, url, len(caps), "captures", flush=True)
    return False


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else ""
    if cmd == "pages":
        bad = 0
        for ident, rel in PB.PAGES.items():
            bad += not pin(ident, PB.P.PL + rel, since="2026")
        return 1 if bad else 0
    if cmd == "gap":
        return 0 if pin(argv[1], argv[2]) else 1
    if cmd == "laws":
        found: dict[str, str] = {}
        for ident in (argv[1:] or [a["page"] for a in PB.ACTS]):
            r = PB.P.raw(ident)
            if not r:
                print("page not cached", ident)
                continue
            tmp = HERE / ".tmp" / "links.htm"
            tmp.parent.mkdir(exist_ok=True)
            tmp.write_bytes(r[0])
            for k, u in F.law_links(tmp, PB.sources()[ident]["url"]).items():
                found.setdefault(k, u)
        have = PB.sources()
        todo = {k: u for k, u in sorted(found.items()) if "law:" + k not in have}
        print(len(found), "acts linked from the notes;", len(todo), "not pinned by any Brazil script", flush=True)
        bad = 0
        for k, u in todo.items():
            bad += not pin("law:" + k, u)
        return 1 if bad else 0
    if cmd == "lexml":
        return F.main(["lexml"])
    if cmd == "plan":
        bad = 0
        for item in load()["fetch"]:
            body = wayback.get(item["url"], ts=item["ts"], cache=CACHE)
            ok = FB.good(body)
            bad += not ok
            print("ok " if ok else "BAD", item["id"], len(body or b""))
        return 1 if bad else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
