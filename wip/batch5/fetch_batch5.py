"""Fetch batch 5 of the Brazil corpus (see parse_batch5.ACTS) and every law its notes cite.

    python -X utf8 scripts/brazil-law/batch5/fetch_batch5.py ccindex [N]   # Common Crawl index of planalto.gov.br/ccivil_03/ (newest N crawls)
    python -X utf8 scripts/brazil-law/batch5/fetch_batch5.py pages         # pin + fetch the acts' annotated/consolidated pages
    python -X utf8 scripts/brazil-law/batch5/fetch_batch5.py laws [ids]    # pin + fetch every law the notes link to
                                                                    # (laws and missing skip the keys in ../bad_pins.json)
    python -X utf8 scripts/brazil-law/batch5/fetch_batch5.py missing       # cited laws with no link: Planalto's usual paths
    python -X utf8 scripts/brazil-law/batch5/fetch_batch5.py gap <id> <planalto url>   # pin + fetch one page
    python -X utf8 scripts/brazil-law/batch5/fetch_batch5.py lexml         # LexML record of every cited law (DOU day)
    python -X utf8 scripts/brazil-law/batch5/fetch_batch5.py plan          # everything pinned (cached: no requests)

Planalto (www.planalto.gov.br) is never contacted: it answers non-browser clients with a bot challenge. Every page is
read from Common Crawl first: `ccindex` lists every capture under planalto.gov.br/ccivil_03/ in the newest crawls from
Common Crawl's own index files (gitlaw_common/wayback.py cc_captures, which reads cluster.idx + cdx blocks from
data.commoncrawl.org while the index server is down), and a page is pinned to its newest complete capture (crawl,
timestamp, WARC file, offset, length), its body read by byte range with 16 threads. A page Common Crawl lacks is read
from Arquivo.pt (wayback.pt_captures / pt_get, user-approved 2026-10-29), and only then from an Internet Archive raw
(`id_`) capture through wayback.py (one machine-wide adaptive archive.org rate). A page
any other Brazil script already pinned is reused at that capture and not fetched again. Pins go to
batch5/sources_batch5.json; the cache is ../.cache/cc (gitignored).
"""
from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import parse_batch5 as PB  # noqa: E402  (configures batch 4 / batch 3 / parse_proc for batch 5 first)

sys.path.insert(0, str(HERE.parent / "batch3"))
import fetch_batch3 as FB  # noqa: E402

F = FB.F
F.SRC = PB.SRC
F.PAGES = PB.PAGES
wayback = FB.wayback
CACHE = FB.CC_CACHE
INDEX = CACHE / "planalto-ccivil03-cc-index.jsonl"
THREADS = 16


def load() -> dict:
    return json.loads(PB.SRC.read_text(encoding="utf-8")) if PB.SRC.exists() else {"fetch": []}


def save_items(items: list[dict]) -> None:
    plan = load()
    ids = {i["id"] for i in items}
    plan["fetch"] = [i for i in plan["fetch"] if i["id"] not in ids] + items
    plan["fetch"].sort(key=lambda i: (not i["id"].startswith(("law:", "ato:")) and 0 or 1, i["id"]))
    tmp = PB.SRC.with_suffix(".tmp")
    tmp.write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    tmp.replace(PB.SRC)


def path_key(url: str) -> str:
    u = url.split("://", 1)[-1].split("?", 1)[0].split("#", 1)[0].lower()
    return re.sub(r"^(?:www\.)?planalto\.gov\.br/", "", u)


def ccindex(n: int) -> int:
    crawls = wayback.cc_crawls(CACHE)[:n]

    def q(c):
        r = wayback.cc_captures("planalto.gov.br/ccivil_03/", crawls=[c], match="prefix", cache=CACHE)
        print(c, len(r), flush=True)
        return r
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(q, crawls))
    tmp = INDEX.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as f:
        for recs in res:
            for r in recs:
                f.write(json.dumps({k: r.get(k) for k in ("url", "timestamp", "status", "length", "offset", "filename",
                                                          "crawl", "digest")}) + "\n")
    tmp.replace(INDEX)
    return 0


_IDX: dict[str, list[dict]] = {}


def index() -> dict[str, list[dict]]:
    if not _IDX:
        for line in INDEX.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if str(r.get("status")) != "200" or "?" in r["url"]:
                continue
            _IDX.setdefault(path_key(r["url"]), []).append(r)
        for v in _IDX.values():
            v.sort(key=lambda r: r["timestamp"], reverse=True)
    return _IDX


def complete(b: bytes | None) -> bool:
    """A whole page: not a bot page, and its </html> is there (Planalto's F5 appends a script of up to ~12 KB after it;
    a capture cut short has none; the Lei 11.343 page carries ~90 KB of it, so the whole body is searched)."""
    return FB.good(b) and re.search(rb"</html\s*>", b, re.I) is not None


def pin_cc(ident: str, url: str) -> dict | None:
    for r in index().get(path_key(url), [])[:5]:
        body = wayback.cc_get(r, cache=CACHE)
        if complete(body):
            return {"id": ident, "url": url, "cc": {k: r[k] for k in ("crawl", "timestamp", "filename", "offset", "length")}}
    return None


def pin_pt(ident: str, url: str) -> dict | None:
    """Arquivo.pt (user-approved 2026-10-29), after Common Crawl and before archive.org."""
    caps = wayback.pt_captures(url.split("://", 1)[1], cache=CACHE)
    caps.sort(key=lambda c: c["timestamp"], reverse=True)
    for c in caps[:5]:
        body = wayback.pt_get(c, cache=CACHE)
        if complete(body):
            return {"id": ident, "url": url, "pt": {"timestamp": c["timestamp"], "url": c["url"]}, "via": "arquivo.pt"}
    return None


def pin_ia(ident: str, url: str) -> dict | None:
    bare = url.split("://", 1)[1]
    caps = sorted(wayback.captures(bare, cache=CACHE), key=lambda c: c["timestamp"], reverse=True)
    for c in caps[:6]:
        if int(c.get("length") or 0) < 1500:
            continue
        body = wayback.get(url, ts=c["timestamp"], cache=CACHE)
        if complete(body):
            return {"id": ident, "url": url, "ts": c["timestamp"], "via": "wayback.py"}
    return None


def pin_many(todo: dict[str, str]) -> int:
    """Pin each id -> url: Common Crawl (16 threads), then archive.org for the rest."""
    have = PB.sources()
    todo = {k: u for k, u in todo.items() if k not in have}
    index()   # built once, before the threads read it
    with ThreadPoolExecutor(THREADS) as ex:
        got = list(ex.map(lambda kv: pin_cc(*kv), todo.items()))
    items = [g for g in got if g]
    save_items(items)
    print(len(items), "pinned from Common Crawl", flush=True)
    rest = {k: u for k, u in todo.items() if k not in {i["id"] for i in items}}
    with ThreadPoolExecutor(12) as ex:
        got = list(ex.map(lambda kv: pin_pt(*kv), rest.items()))
    pt = [g for g in got if g]
    save_items(pt)
    print(len(pt), "pinned from Arquivo.pt", flush=True)
    rest = {k: u for k, u in rest.items() if k not in {i["id"] for i in pt}}
    bad = []
    with ThreadPoolExecutor(4) as ex:
        got = list(ex.map(lambda kv: pin_ia(*kv), rest.items()))
    ia = [g for g in got if g]
    save_items(ia)
    print(len(ia), "pinned from archive.org", flush=True)
    for k, u in rest.items():
        if k not in {i["id"] for i in ia}:
            bad.append(k)
            print("NO CAPTURE", k, u, flush=True)
    return 1 if bad else 0


BAD_PINS = HERE.parent / "bad_pins.json"


def drop_bad(todo: dict[str, str]) -> dict[str, str]:
    """Leave out every key in ../bad_pins.json (pins headyear.py showed to be a different act's page)."""
    bad = json.loads(BAD_PINS.read_text(encoding="utf-8"))["keys"] if BAD_PINS.exists() else {}
    for k in sorted(set(todo) & set(bad)):
        print("skipped (bad_pins.json):", k, "-", bad[k], flush=True)
    return {k: u for k, u in todo.items() if k not in bad}


def linked_laws(idents: list[str]) -> dict[str, str]:
    found: dict[str, str] = {}
    for ident in idents:
        r = PB.P.raw(ident)
        if not r:
            print("page not cached", ident)
            continue
        tmp = HERE / ".tmp" / "links.htm"
        tmp.parent.mkdir(exist_ok=True)
        tmp.write_bytes(r[0])
        for k, u in F.law_links(tmp, PB.sources()[ident]["url"]).items():
            found.setdefault(k, u)
    return found


def fetch_pin(item: dict) -> bool:
    """Fetch one pinned capture into the cache path the parsers read (refetch after the cache was lost)."""
    if PB.P.raw(item["id"]):
        return True
    if item.get("cc"):
        body = wayback.cc_get(dict(item["cc"], status=200), cache=CACHE)
    elif item.get("pt"):
        body = wayback.pt_get(item["pt"], cache=CACHE)
    elif item.get("via") == "wayback.py":
        body = wayback.get(item["url"], ts=item["ts"], cache=CACHE)
    elif item.get("ts"):
        # pins made through ../fetch.py: same capture, read through the shared archive.org rate, cached where
        # parse_proc.raw looks (../.cache/<sha256 of the id_ URL>.bin)
        u = FB.fetch.wayback(item["url"], item["ts"])
        p = FB.fetch.CACHE / (FB.fetch.key(u) + ".bin")
        body = wayback.fetch(u, None)
        if body:
            FB.fetch.CACHE.mkdir(exist_ok=True)
            (FB.fetch.CACHE / ".gitignore").write_text("*\n", encoding="utf-8")
            tmp = p.with_suffix(".part")
            tmp.write_bytes(body)
            tmp.replace(p)
            with (FB.fetch.CACHE / "requests.jsonl").open("a", encoding="utf-8") as f:
                f.write(json.dumps({"url": u, "status": 200, "bytes": len(body), "via": "wayback.fetch (refetch)"}) + "\n")
    else:
        return False
    return bool(body)


def fetch_urls(urls: list[str]) -> int:
    """Direct records the parsers read through ../fetch.py's cache (LexML URN pages, STF case pages): host_get, then
    stored at ../.cache/<sha256 of the URL>.bin. robots.txt allows /urn/ on lexml.gov.br."""
    def one(u):
        p = FB.fetch.CACHE / (FB.fetch.key(u) + ".bin")
        if p.exists() and p.stat().st_size:
            return True
        body = wayback.host_get(u, CACHE)
        if body:
            FB.fetch.CACHE.mkdir(exist_ok=True)
            tmp = p.with_suffix(".part")
            tmp.write_bytes(body)
            tmp.replace(p)
        return bool(body)
    with ThreadPoolExecutor(8) as ex:
        ok = list(ex.map(one, urls))
    print(sum(ok), "of", len(urls), "cached; failed:", [u for u, o in zip(urls, ok) if not o], flush=True)
    return 0 if all(ok) else 1


def refetch(idents: list[str]) -> int:
    srcs = PB.sources()
    items = [srcs[i] for i in idents if i in srcs]
    for i in idents:
        if i not in srcs:
            print("not pinned", i)
    with ThreadPoolExecutor(12) as ex:
        ok = list(ex.map(fetch_pin, items))
    bad = [i["id"] for i, o in zip(items, ok) if not o]
    print(len(items) - len(bad), "of", len(items), "cached;", "failed:", bad, flush=True)
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else ""
    if cmd == "refetch":   # refetch <ids...> | refetch --need (batch5/.tmp/need.json) | refetch --all-batch5
        if argv[1:2] == ["--need"]:
            need = json.loads((PB.SRC.parent / ".tmp" / "need.json").read_text())
            return refetch(need["pinned_missing"]) | (fetch_urls(need["urls"]) if need["urls"] else 0)
        if argv[1:2] == ["--all-batch5"]:
            return refetch([i["id"] for i in load()["fetch"]])
        return refetch(argv[1:])
    if cmd == "ccindex":
        return ccindex(int(argv[1]) if len(argv) > 1 else 16)
    if cmd == "pages":
        return pin_many({ident: PB.PL + rel for ident, rel in PB.PAGES.items()})
    if cmd == "gap":
        return pin_many({argv[1]: argv[2]})
    if cmd == "laws":
        found = linked_laws(argv[1:] or [a["page"] for a in PB.ACTS])
        print(len(found), "acts linked from the notes", flush=True)
        return pin_many(drop_bad({"law:" + k: u for k, u in sorted(found.items())}))
    if cmd == "missing":
        import warnings
        warnings.filterwarnings("ignore")
        P = PB.P
        keys = set(argv[1:])
        for act in PB.ACTS:
            b, _ = P.raw(act["page"])
            P.CENTER_HEADINGS = act.get("center_headings", True)
            paras, _ = P.paragraphs(P.decode(b), act["digits"])
            keys |= P.note_laws(paras)
        have = PB.sources()
        todo = {}
        for k in sorted(keys):
            if "law:" + k in have or k in PB.B.ACT_LAWS:
                continue
            for rel in F.candidates(k):
                if index().get(path_key(PB.PL + rel)):
                    todo["law:" + k] = PB.PL + rel
                    break
            else:
                print("no Common Crawl path for", k)
        return pin_many(drop_bad(todo))
    if cmd == "lexml":
        return F.main(["lexml"])
    if cmd == "plan":
        bad = 0
        for item in load()["fetch"]:
            r = PB.P.raw(item["id"])
            ok = bool(r) and complete(r[0])
            bad += not ok
            print("ok " if ok else "BAD", item["id"], len(r[0]) if r else 0)
        return 1 if bad else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
