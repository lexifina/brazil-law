"""Fetch the Phase 2 acts (Código Penal, Código de Processo Civil; the CLT is another agent's part, 70-clt.json) and every law their notes cite.

    python -X utf8 scripts/brazil-law/fetch_phase2.py pages     # pin + fetch the annotated and compiled pages
    python -X utf8 scripts/brazil-law/fetch_phase2.py laws      # pin + fetch every amending law the notes link to
    python -X utf8 scripts/brazil-law/fetch_phase2.py plan      # fetch everything pinned in sources_phase2.json

Adapted from codes/fetch_codes.py (the Código Civil/LGPD helper). A law page the helper already pinned in
codes/sources_codes.json is reused at the same capture.

Uses the main Brazil fetcher (../fetch.py: curl, sha256-named cache in ../.cache, requests.jsonl). Planalto blocks
non-browser clients, so every page is an Internet Archive raw (`id_`) capture of the Planalto URL; the capture
timestamps are pinned in sources_phase2.json so parse_phase2.py is reproducible.

Politeness: the main Brazil agent may fetch from web.archive.org at the same time, so besides fetch.py's own
1 request/second, this script waits until at least 1.5 s have passed since the last request either process logged
(the mtime of ../.cache/requests.jsonl).
"""
from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fetch  # noqa: E402

SRC = HERE / "sources_phase2.json"
HELPER_SRC = HERE / "codes" / "sources_codes.json"
PL = "https://www.planalto.gov.br/ccivil_03/"
PAGES = {
    "cp": "decreto-lei/del2848.htm",
    "cp-compilado": "decreto-lei/del2848compilado.htm",
    "cpc": "_ato2015-2018/2015/lei/l13105.htm",
}

_orig_polite = fetch._polite


def _shared_polite(host: str) -> None:
    while True:
        try:
            since = time.time() - fetch.LOG.stat().st_mtime
        except OSError:
            since = 99
        if since >= 1.5:
            break
        time.sleep(1.5 - since)
    _orig_polite(host)


fetch._polite = _shared_polite


def load() -> dict:
    return json.loads(SRC.read_text(encoding="utf-8")) if SRC.exists() else {"fetch": []}


def save(plan: dict) -> None:
    tmp = SRC.with_suffix(".tmp")
    tmp.write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(SRC)


def pin(plan: dict, ident: str, url: str, **extra) -> dict:
    have = {i["id"]: i for i in plan["fetch"]}
    if ident not in have and HELPER_SRC.exists():
        helper = {i["id"]: i for i in json.loads(HELPER_SRC.read_text(encoding="utf-8"))["fetch"]}
        if helper.get(ident, {}).get("ts"):
            have[ident] = dict(helper[ident])
            plan["fetch"] = list(have.values())
            save(plan)
            return have[ident]
    if ident in have and (have[ident].get("ts") or have[ident].get("url") == url and have[ident].get("tried")):
        return have[ident]
    try:
        ts = fetch.pick(url.split("://", 1)[1], min_len=1500)
    except RuntimeError as e:
        print("cdx error", ident, e)
        ts = None
    item = {"id": ident, "url": url, "ts": ts, **({} if ts else {"tried": True}), **extra}
    have[ident] = item
    plan["fetch"] = list(have.values())
    save(plan)
    print("pinned", ident, ts, flush=True)
    return item


def get(item: dict) -> Path | None:
    if not item.get("ts"):
        print("NO CAPTURE", item["id"], item["url"])
        return None
    u = fetch.wayback(item["url"], item["ts"])
    try:
        return fetch.get(u)
    except RuntimeError as e:
        print("FAIL", e)
        return None


NOTE_WORDS = re.compile(r"Reda|Inclu|Acresc|Revog|Renumer|Vide|Convert|Vig[êe]ncia|Produ", re.I)


def law_links(path: Path, base: str) -> dict[str, str]:
    """Planalto URL of every act a note in the page links to, keyed by a normalised id (lei-14905-2024 ...)."""
    import parse_phase2 as parse_codes  # the same id rules as the parser

    b = path.read_bytes()
    t = parse_codes.decode(b)
    out = {}
    for m in re.finditer(r'<a\b[^>]*href\s*=\s*"([^"]+)"[^>]*>(.*?)</a>', t, re.I | re.S):
        href, label = m.group(1), html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))
        key = parse_codes.law_key(label)
        if not key or not NOTE_WORDS.search(label) or "legislacao.planalto" in href:
            continue
        href = href.strip().split("#")[0]
        if "web.archive.org" in href:
            href = re.sub(r"^.*?/(https?://)", r"\1", href)
        url = urllib.parse.urljoin(base, href)
        url = re.sub(r"^http://", "https://", url)
        url = url.replace("://planalto.gov.br", "://www.planalto.gov.br")
        out.setdefault(key, url)
    return out


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else ""
    plan = load()
    if cmd == "pages":
        for ident, rel in PAGES.items():
            item = pin(plan, ident, PL + rel)
            p = get(item)
            print(ident, p and p.name, p and p.stat().st_size)
        return 0
    if cmd == "laws":
        sys.path.insert(0, str(HERE))
        found: dict[str, str] = {}
        for ident in (argv[1:] or list(PAGES)):
            item = next((i for i in plan["fetch"] if i["id"] == ident), None)
            if not item or not item.get("ts"):
                continue
            p = fetch.cached(fetch.wayback(item["url"], item["ts"]))
            if p:
                for k, u in law_links(p, item["url"]).items():
                    found.setdefault(k, u)
        print(len(found), "acts linked from the notes")
        for k, u in sorted(found.items()):
            it = pin(plan, "law:" + k, u)
            get(it)
        return 0
    if cmd == "plan":
        for item in plan["fetch"]:
            get(item)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
