"""Fetch the Código de Processo Penal (Decreto-Lei 3.689/1941), the Código de Defesa do Consumidor (Lei 8.078/1990)
and every law their notes cite.

    python -X utf8 scripts/brazil-law/proc/fetch_proc.py pages     # pin + fetch the annotated and compiled pages
    python -X utf8 scripts/brazil-law/proc/fetch_proc.py laws      # pin + fetch every amending law the notes link to
    python -X utf8 scripts/brazil-law/proc/fetch_proc.py plan      # fetch everything pinned in proc/sources_proc.json

Adapted from codes/fetch_codes.py (the Código Civil/LGPD helper). A page already pinned by another Brazil script
(codes/sources_codes.json, sources_phase2.json) is reused at the same capture.

Uses the main Brazil fetcher (../fetch.py: curl, sha256-named cache in ../.cache, requests.jsonl). Planalto blocks
non-browser clients, so every page is an Internet Archive raw (`id_`) capture of the Planalto URL; the capture
timestamps are pinned in proc/sources_proc.json so proc/parse_proc.py is reproducible.

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
sys.path.insert(0, str(HERE.parent))
import fetch  # noqa: E402

SRC = HERE / "sources_proc.json"
OTHER_SRC = [HERE.parent / "sources_phase2.json", HERE.parent / "codes" / "sources_codes.json",
             HERE.parent / "clt" / "sources_clt.json"]
PL = "https://www.planalto.gov.br/ccivil_03/"
PAGES = {
    "cpp": "decreto-lei/del3689.htm",
    "cpp-compilado": "decreto-lei/del3689compilado.htm",
    "cdc": "leis/l8078.htm",
    "cdc-compilado": "leis/l8078compilado.htm",
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
    for other in OTHER_SRC:
        if ident in have or not other.exists():
            break
        try:
            helper = {i["id"]: i for i in json.loads(other.read_text(encoding="utf-8"))["fetch"]}
        except (OSError, ValueError):
            continue
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
    import parse_proc as parse_codes  # the same id rules as the parser

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


def candidates(key: str) -> list[str]:
    pre, n, y = key.split("-")
    y = int(y)
    num = n.rstrip("abcdefghijklmnopqrstuvwxyz")
    suf = n[len(num):].upper()
    out = []
    if pre == "dl":
        for d in ("decreto-lei/1937-1946/", "decreto-lei/", "decreto-lei/1965-1988/"):
            for nn in (num, f"{int(num):04d}"):
                for sx in ([suf, "-" + suf] if suf else [""]):
                    out.append(f"{d}Del{nn}{sx}.htm")
    elif pre in ("lei", "lc"):
        stem = "Lcp" if pre == "lc" else "L"
        if y >= 2004:
            a = 2004 + (y - 2004) // 3 * 3 if y < 2007 else 2007 + (y - 2007) // 4 * 4
            rng = f"_ato{a}-{a + (2 if a == 2004 else 3)}"
            out.append(f"{rng}/{y}/lei/{stem.lower()}{num}.htm")
            out.append(f"{rng}/{y}/lei/{stem}{num}.htm")
        if pre == "lc":
            out.append(f"leis/lcp/Lcp{num}.htm")
        else:
            for d in ("leis/", "leis/1950-1969/", "leis/1930-1949/", f"leis/{y}/", f"leis/leis_{y}/"):
                out.append(f"{d}L{num}.htm")
    seen, uniq = set(), []
    for u in out:  # the Wayback index lowercases URLs: one probe per case-folded path
        if u.lower() not in seen:
            seen.add(u.lower())
            uniq.append(u)
    return uniq


def pin_guess(key: str) -> None:
    plan = load()
    for rel in candidates(key):
        url = PL + rel
        try:
            ts = fetch.pick(url.split("://", 1)[1], min_len=1500)
        except RuntimeError as e:
            print("cdx error", key, e)
            continue
        if ts:
            item = {"id": "law:" + key, "url": url, "ts": ts, "guessed_path": True}
            plan = load()
            plan["fetch"] = [i for i in plan["fetch"] if i["id"] != item["id"]] + [item]
            save(plan)
            print("pinned", key, rel, ts, flush=True)
            get(item)
            return
    print("NOT FOUND", key, flush=True)


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
    if cmd == "missing":
        # every law a start/end note names (parse_clt's own key rules) that has no pinned page yet: try Planalto's
        # usual paths for it, newest good capture first
        import warnings
        warnings.filterwarnings("ignore")
        import parse_proc as P
        keys = set(argv[1:])
        for act in P.ACTS:
            b, _ = P.raw(act["page"])
            P.CENTER_HEADINGS = act.get("center_headings", True)
            paras, _ = P.paragraphs(P.decode(b), act["digits"])
            keys |= P.note_laws(paras)
        keys = sorted(keys)
        have = {i["id"] for i in plan["fetch"] if i.get("ts")}
        for k in keys:
            if "law:" + k in have:
                continue
            pin_guess(k)
        return 0
    if cmd == "lexml":
        # LexML (Senado Federal / PRODASEN) record of every cited law: its "Publicação Original" line checks the DOU
        # date printed on the Planalto page (some pages print a wrong year or day)
        import warnings
        warnings.filterwarnings("ignore")
        import parse_proc as P
        keys = set()
        for act in P.ACTS:
            b, _ = P.raw(act["page"])
            P.CENTER_HEADINGS = act.get("center_headings", True)
            paras, _ = P.paragraphs(P.decode(b), act["digits"])
            keys |= P.note_laws(paras)
        for k in sorted(keys):
            u = P.lexml_url(k, P.page_info(k).get("enacted"))
            if not u:
                print("no urn", k)
                continue
            try:
                print(k, fetch.get(u).name, flush=True)
            except RuntimeError as e:
                print("FAIL", k, e, flush=True)
        return 0
    if cmd == "plan":
        for item in plan["fetch"]:
            get(item)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
