"""Reads the cache and writes scripts/brazil-law/corpus.d/98-batch5.json (SCHEMA.md corpus part): batch 5 of the
Brazil corpus, the acts in ACTS below (public procurement, public registers, forest code).

    python -X utf8 scripts/brazil-law/batch5/parse_batch5.py [--stats] [--dry]

Imports ../batch4/parse_batch4.py (which configures ../batch3/parse_batch3.py and ../proc/parse_proc.py, the
struck-text replay of Planalto's annotated pages) and replaces only its configuration: the acts, the hand tables, the
pins and the output. Batch 4's machinery (lettered-article rule, MP wording dropped at conversion, promulgated vetoes)
is reused with this batch's own tables. The parts of batch 3, the RJU and batch 4 are not touched (their parsers, run on
their own, write the same bytes as before). No network.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
sys.path.insert(0, str(FOLDER / "batch4"))
import parse_batch4 as B4  # noqa: E402  (configures batch 3 / parse_proc for batch 4; reconfigured below)

B = B4.B
P = B4.P
PL = P.PL
OUT = FOLDER / "corpus.d" / "98-batch5.json"
STAGE = HERE / ".tmp" / "stage.json"   # batch 3's write_part writes here; the part is finished from it
P.RETRIEVED = "2026-10-29"

PAGES = {
    "lcc": "_ato2019-2022/2021/lei/l14133.htm",
    "l8666": "leis/l8666cons.htm",
    "lrp": "leis/l6015consolidado.htm",
    "lrp-compilada": "leis/l6015compilada.htm",
    "cflo": "_ato2011-2014/2012/lei/l12651.htm",
    "cflo-compilado": "_ato2011-2014/2012/lei/l12651compilado.htm",
}
B.PAGES.clear()
B.PAGES.update(PAGES)

ACTS: list[dict] = [
    {"slug": "lei-de-licitacoes-e-contratos", "short": "LLC", "page": "lcc", "consolidated": "lcc",
     "law": "lei-14133-2021",
     "title": "Lei de Licitações e Contratos Administrativos (Lei nº 14.133, de 1º de abril de 2021)",
     "digits": 3, "url": PL + "_ato2019-2022/2021/lei/l14133.htm"},
]
B.ACTS[:] = ACTS
B.ACT_DAY.clear()
B.ACT_DAY.update({
    "lei-14133-2021": ("2021-04-01", "Lei 14.133/2021 art. 194: 'Esta Lei entra em vigor na data de sua publicação' "
                                     "(published in the DOU of 1.4.2021, edição extra-F)"),
})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({
    "lei-14133-2021": B._act_law("Lei nº 14.133, de 2021", "Lei de Licitações e Contratos Administrativos.",
                                 "2021-04-01", "2021-04-01", "_ato2019-2022/2021/lei/l14133.htm"),
})
P.COURTS = {}
B.PROMULGATED.clear()
B.KEPT_BY_CONGRESS.clear()
B4.MP_DROPPED[:] = []
B4.PROMULGATED_UNITS.clear()
B.EXPLAINED.clear()

# ---------------------------------------------------------------------------------------------------------------
# pins: every Brazil pin file (a page already pinned elsewhere is read at that capture), then batch5's own, which win

SRC = HERE / "sources_batch5.json"
PIN_FILES = B4.PIN_FILES[:-1] + [B4.SRC, SRC]


def sources() -> dict[str, dict]:
    s: dict[str, dict] = {}
    for f in PIN_FILES:
        if f.exists():
            for i in json.loads(f.read_text(encoding="utf-8"))["fetch"]:
                if i.get("ts") or i.get("cc") or i.get("pt"):
                    s[i["id"]] = i
    return s


B.sources = P.sources = B4.sources = sources
PT_ARCHIVE = "https://arquivo.pt/wayback"
_raw = P.raw


def pt_url(s: dict) -> str:
    return f'{PT_ARCHIVE}/{s["pt"]["timestamp"]}id_/{s["pt"]["url"]}'


def raw(ident: str) -> tuple[bytes, str] | None:
    """batch 3's raw (Common Crawl, archive.org pins), plus Arquivo.pt pins ("pt": timestamp, url; cached by
    gitlaw_common/wayback.py pt_get under the sha256 of the replay URL). Cache only, no network."""
    s = sources().get(ident)
    if s and s.get("pt"):
        u = pt_url(s)
        p = B.CC_CACHE / P.hashlib.sha256(u.encode("utf-8")).hexdigest()
        return (p.read_bytes(), u) if p.exists() else None
    return _raw(ident)


P.raw = B.raw = raw

# ---------------------------------------------------------------------------------------------------------------
# the part file: batch 3's write_part (through batch 4's staging), then this part's own sources, notes and requests


def _requests(pins: dict[str, dict]) -> int:
    """Requests gitlaw_common/wayback.py logged for these pins: Common Crawl byte ranges, archive.org captures, CDX."""
    log = FOLDER / ".cache" / "cc" / "requests.jsonl"
    want = set()
    for i in pins.values():
        if i.get("cc"):
            c = i["cc"]
            want.add(f'cc:{c["filename"]}:{c["offset"]}:{c["length"]}')
        elif i.get("pt"):
            want.add(pt_url(i))
        elif i.get("via") == "wayback.py":
            want.add(B.fetch.wayback(i["url"], i["ts"]))
            want.add("cdx:" + i["url"].split("://", 1)[1].lower())
    n, seen = 0, set()
    for line in (log.read_text(encoding="utf-8").splitlines() if log.exists() else []):
        u = json.loads(line)["url"]
        key = u
        if "cdx/search" in u:
            m = re.search(r"[?&]url=([^&]+)", u)
            key = "cdx:" + (m.group(1).lower() if m else "")
        if key in want and key not in seen:
            seen.add(key)
            n += 1
    return n


EXTRA_DECISIONS: list[str] = []


def write_part(acts_out, laws, decisions, vig_notes, lindb, checks, problems, mpn) -> int:
    used = {a["first_law"] for a in acts_out}
    for act in acts_out:
        for v in act["versions"]:
            for ls in v["credits"].values():
                used |= set(ls)
    used |= {laws[k]["restores"] for k in used if laws.get(k, {}).get("restores")}
    allp = sources()
    pins = {k: v for k, v in allp.items() if k in PAGES or (k.startswith(("law:", "ato:")) and k.split(":", 1)[1] in used)}
    B.sources = lambda: pins
    try:
        decisions = decisions + EXTRA_DECISIONS + [
            f"A Medida Provisória's wording its conversion law left out: {why}." for (*_, why) in B4.MP_DROPPED
            if B4.MP_DROPPED_USED] + [
            f"{why} ({'; '.join(B4.PROMULGATED_USED)})." for (_, why, _) in B4.PROMULGATED_UNITS.values()
            if B4.PROMULGATED_USED] + (
            [f"A lettered article (inserted after enactment) whose 'Incluído' note Planalto prints only on its last "
             f"line: its unnoted lines take that note's law and day ({'; '.join(B4.ARTICLE_NOTE_USED)})."]
            if B4.ARTICLE_NOTE_USED else [])
        P.OUT = STAGE
        STAGE.parent.mkdir(exist_ok=True)
        B4._write_part(acts_out, laws, decisions, vig_notes, lindb, checks, problems, mpn)
    finally:
        B.sources = sources
    part = json.loads(STAGE.read_text(encoding="utf-8"))
    pl = part["sources"][0]
    n_cc = sum(1 for v in pins.values() if v.get("cc"))
    pl["name"] = ("Planalto (Presidência da República), Legislação: annotated and consolidated pages of "
                  + ", ".join(a["short"] for a in ACTS) + " and of every law their notes cite, read from Common Crawl "
                  "captures (and Internet Archive raw captures where Common Crawl has none)")
    pl["requests"] += _requests(pins)
    pl["notes"] = pl["notes"].replace(
        "Every page is the Internet Archive raw capture (web.archive.org/web/<ts>id_/<planalto url>), byte-identical to "
        "what Planalto served; the capture timestamps are pinned in batch3/sources_batch3.json.",
        f"{n_cc} of the {len(pins)} pages are Common Crawl captures (the WARC record's HTTP body, read by byte range "
        "from data.commoncrawl.org; crawl, timestamp, WARC file, offset and length pinned in batch5/sources_batch5.json), "
        "the rest Internet Archive raw captures (web.archive.org/web/<ts>id_/<planalto url>) pinned in "
        "batch5/sources_batch5.json or, for pages another Brazil part pinned first, that part's pin file.")
    part["sources"].insert(1, {
        "name": "Common Crawl (crawls CC-MAIN-2025-30 to CC-MAIN-2026-43): captures of the Planalto pages",
        "url": "https://commoncrawl.org/", "retrieved": P.RETRIEVED, "requests": 0,
        "licence": "Common Crawl Terms of Use (https://commoncrawl.org/terms-of-use); the page text is Planalto's",
        "notes": "Capture discovery from each crawl's own index files (cluster.idx and cdx blocks on data.commoncrawl.org); "
                 "page bodies by byte range; the requests are counted in the Planalto line above."})
    part["ai_use"] = ["Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote batch5/fetch_batch5.py and "
                      "batch5/parse_batch5.py (configuration of ../batch4, ../batch3 and ../proc, imported) and the "
                      "hand tables in them (in-force days, MP fates, explained differences) from the official pages. No "
                      "model wrote, summarised or changed legal text; no model runs at data-build or git-build time."]
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(part, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8",
                   newline="\n")
    os.replace(tmp, OUT)
    print("wrote", OUT, OUT.stat().st_size, "bytes;", sum(len(x["versions"]) for x in acts_out), "versions")
    return 0


B.write_part = P.write_part = write_part

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
