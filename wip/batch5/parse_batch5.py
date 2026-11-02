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
OUT = Path(os.environ.get("BATCH5_OUT") or FOLDER / "corpus.d" / "98-batch5.json")
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
# The day a lapsed Medida Provisória stopped having effect, from the Ato Declaratório of the President of Congress
# (CF art. 62 §§ 3, 4, 7 and 11), linked from the notes on the Lei 14.133 page: key -> (day the wording it replaced
# is back, reason).
P.MP_LAPSE = {
    "mp-1166-2023": ("2023-07-21", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 50, de 2023 (DOU "
                                   "4.8.2023): 'teve seu prazo de vigência encerrado no dia 20 de julho de 2023'; its "
                                   "wording of Lei 14.133 art. 75 ends then"),
    "mp-1167-2023": ("2023-07-29", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 51, de 2023 (DOU "
                                   "4.8.2023): 'teve seu prazo de vigência encerrado no dia 28 de julho de 2023'; the "
                                   "wording of Lei 14.133 art. 191 it had replaced is back from 29.7.2023 (its art. 193 "
                                   "II wording was replaced by Lei Complementar 198/2023 before that)"),
}
B.PROMULGATED.clear()
B.KEPT_BY_CONGRESS.clear()
B4.MP_DROPPED[:] = []
B4.PROMULGATED_UNITS.clear()
B.EXPLAINED.clear()

# ---------------------------------------------------------------------------------------------------------------
# Vetoed parts of an act promulgated after Congress overrode the veto (CF art. 66 §§ 5 and 7), printed on the act's own
# page as a struck '(VETADO)' line followed by the promulgated wording noted '(Promulgação partes vetadas)': act law ->
# (day, reason). The promulgated dispositivo (with its unnoted incisos) starts on that day, credited to the act's law;
# the '(VETADO)' line stands until then.
PROMULGATED_PARTS: dict[str, tuple[str, str]] = {
    "lei-14133-2021": ("2021-06-11", "Lei 14.133/2021: the parts vetoed on 1.4.2021 were promulgated after Congress "
                                     "overrode the veto (promulgation signed 10.6.2021 and printed at the end of the Lei "
                                     "14.133 page; published in the DOU of 11.6.2021, Seção 1, p. 2, as LexML's record of "
                                     "the law gives it, 'Publicação de Veto Parcialmente Rejeitado'), in force on "
                                     "publication (art. 194). They are art. 37 § 2º (with its incisos I and II), art. 54 "
                                     "§ 1º, art. 115 § 4º and art. 175 § 2º; Planalto marks each '(Promulgação partes "
                                     "vetadas)' below the struck '(VETADO)' line, which stands until then"),
}
PROMULGATED_PARTS_USED: list[str] = []
PROMULGATION_NOTE = re.compile(r"Promulga[çc][ãa]o\s+(?:das\s+)?partes\s+vetadas", re.I)
_lifespans5 = P.lifespans


def lifespans(paras: list[dict], cx) -> list[str]:
    problems = _lifespans5(paras, cx)
    act = next(a for a in ACTS if a["slug"] == cx.act)
    if act["law"] not in PROMULGATED_PARTS:
        return problems
    day = PROMULGATED_PARTS[act["law"]][0]
    for i, p in enumerate(paras):
        if p["state"] != "plain" or not any(PROMULGATION_NOTE.search(n) for n in p["notes"]):
            continue
        group = [p]
        # unnoted sub-items (incisos, alíneas) printed under the promulgated paragraph, up to the next § / article
        for q in paras[i + 1:]:
            if q["unit"] != p["unit"] or q["notes"] or q["state"] != "plain" or re.match(r"(?:§|Art\.|Parágrafo)", q["label"] or ""):
                break
            group.append(q)
        for q in group:
            q["start"], q["start_law"] = day, act["law"]
        hit = [q for q in paras[:i] if q["unit"] == p["unit"] and q["label"] == p["label"] and q["state"] != "plain"
               and re.search(r"\(VETADO\)", q["text"]) and not q["end"]]
        for q in hit:
            q["end"], q["end_law"], q["end_how"] = day, act["law"], "promulgation"
        PROMULGATED_PARTS_USED.append(f"{p['unit']} [{p['label']}]: {len(group)} lines, {len(hit)} '(VETADO)' line ended")
    return problems


P.lifespans = B.lifespans = lifespans

# A line a lapsed Medida Provisória revoked, printed twice: struck (with the MP's 'Revogado' note, 'Vigência encerrada')
# and again unstruck with no note below the MP's own lines (Lei 14.133 art. 191 Parágrafo único). The struck copy
# ends the day the MP took effect; the unstruck copy is back the day the MP lapsed, credited to its lapse, exactly as the
# caput above it.
LAPSE_RESTORED: list[str] = []
_apply_rewrites5 = P.apply_rewrites


def apply_rewrites(paras: list[dict], act: dict, eff: dict, problems: list[str]) -> list[str]:
    out = _apply_rewrites5(paras, act, eff, problems)
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end"] or len(p["gaps"]) != 1:
            continue
        g_start, g_end, g_law, g_fim = p["gaps"][0]
        q = next((q for q in paras[i + 1:] if q["unit"] == p["unit"] and q["label"] == p["label"] and q["state"] == "plain"
                  and q["text"] == p["text"] and not q["notes"] and q["start"] <= p["start"]), None)
        if q is None:
            continue
        p["end"], p["end_law"], p["end_how"], p["gaps"] = g_start, g_law, "lapse-restored", []
        q["start"], q["start_law"], q["skip"] = g_end, g_fim, None
        LAPSE_RESTORED.append(f"{act['short']} {p['unit']} [{p['label']}]")
    return out


P.apply_rewrites = B.apply_rewrites = apply_rewrites

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
        return (p.read_bytes(), s["url"]) if p.exists() else None
    r = _raw(ident)
    if r and s and s.get("cc"):
        # the version's source_url is the official page; the capture it was read from is pinned in the pin file
        return r[0], s["url"]
    return r


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
# Medidas Provisórias Congress rejected (CF art. 62 § 3), modelled through MP_LAPSE (the wording they replaced is back
# from the given day); their end is relabelled: MP key -> (label, title) of the '<key>-fim' law.
MP_REJECTED: dict[str, tuple[str, str]] = {}
# In-force days set per provision (P.VIGENCIA_PROVISION: (law, act, unit) -> (day, reason)) are printed as decisions for
# every act of the part whose versions credit that law on that unit. Skipped: keys the reader sets itself (batch 6's
# 'com a redação dada' rule, which prints its own decision) and (law, act) pairs another decision already explains.
PROVISION_AUTO: set[tuple[str, str, str]] = set()
PROVISION_REPORTED: set[tuple[str, str]] = set()


def provision_decisions(acts_out) -> list[str]:
    groups: dict[tuple, list[str]] = {}
    acts = {a["slug"]: a for a in acts_out}
    for (law, slug, unit), (day, why) in sorted(P.VIGENCIA_PROVISION.items()):
        act = acts.get(slug)
        if not act or (law, slug, unit) in PROVISION_AUTO or (law, slug) in PROVISION_REPORTED:
            continue
        label, used = None, False
        for v in act["versions"]:
            u = (v.get("changes") or v.get("units") or {}).get(unit)
            label = label or (u or {}).get("label")
            used = used or law in v["credits"].get(unit, [])
        if used:
            groups.setdefault((act["short"], law, day, why), []).append(label or unit)
    merged: dict[tuple, list[str]] = {}   # one line for laws sharing the articles, day and reason (an MP and its conversion)
    for (short, law, day, why), labels in groups.items():
        merged.setdefault((short, tuple(labels), day, why), []).append(P.law_label(law))
    return [f"{short} {', '.join(labels)}: {' and '.join(laws)} take{'s' if len(laws) == 1 else ''} effect for "
            f"{'this article' if len(labels) == 1 else 'these articles'} on {day}, by a provision of "
            f"{'its' if len(laws) == 1 else 'their'} own ({why})." for (short, labels, day, why), laws in merged.items()]


def write_part(acts_out, laws, decisions, vig_notes, lindb, checks, problems, mpn) -> int:
    used = {a["first_law"] for a in acts_out}
    for act in acts_out:
        for v in act["versions"]:
            for ls in v["credits"].values():
                used |= set(ls)
    used |= {laws[k]["restores"] for k in used if laws.get(k, {}).get("restores")}
    allp = sources()
    pins = {k: v for k, v in allp.items() if k in B.PAGES or (k.startswith(("law:", "ato:")) and k.split(":", 1)[1] in used)}
    B.sources = lambda: pins
    try:
        decisions = decisions + EXTRA_DECISIONS + provision_decisions(acts_out) + [
            f"{why} ({'; '.join(PROMULGATED_PARTS_USED)})." for (_, why) in PROMULGATED_PARTS.values()
            if PROMULGATED_PARTS_USED] + (
            ["A line a lapsed Medida Provisória revoked is printed twice, struck with the MP's note and again unstruck "
             "below the MP's lines: the struck copy ends the day the MP took effect and the unstruck copy is back the day "
             f"the MP lapsed, credited to the lapse ({'; '.join(LAPSE_RESTORED)})."] if LAPSE_RESTORED else []) + [
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
    pl["name"] = ("Planalto (Presidência da República), Legislação: annotated and consolidated pages of "
                  + ", ".join(a["title"] for a in ACTS) + " and of every law their notes cite")
    pl["requests"] += _requests(pins)
    # published text: what the pages are and where they are pinned, never how they were fetched (PUSH RULES 3)
    notes = re.sub(r"Every page is .*$", "", pl["notes"])
    notes = re.sub(r"\s*\(Wayback captures of /robots\.txt[^)]*\)", "", notes)
    notes = re.sub(r"\s*Planalto answers non-browser clients[^.]*\.", "", notes)
    pl["notes"] = notes.rstrip() + (
        f" Each of the {len(pins)} pages is Planalto's page as it stood on the dated capture pinned in "
        f"{SRC.parent.name}/{SRC.name} (or, for a page another Brazil part pinned first, that part's pin file); its sha256 "
        "is recorded in each version.")
    for d_i, d in enumerate(part["decisions"]):
        # a line that already reads 'the unstruck text of Planalto's consolidated page' names a consolidated page the act
        # has (CPC 1973's pre-repeal check in 99-batch17zzzza): it is left as it is, so the phrase is not doubled
        if re.search(r"(?<!the unstruck text of )Planalto's consolidated page", d):
            part["decisions"][d_i] = re.sub(r"(?<!the unstruck text of )Planalto's consolidated page",
                                            "the unstruck text of Planalto's page of the act (Planalto publishes no "
                                            "separate consolidated page for it)", d)
    for k, (label, title) in MP_REJECTED.items():
        if k + "-fim" in part["laws"]:
            part["laws"][k + "-fim"].update(label=label, title=title)
    part["ai_use"] = ["Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote Lexifina's code and the hand tables in it "
                      "(in-force days, MP fates, explained differences) from the official pages. No model wrote, "
                      "summarised or changed legal text; no model runs at data-build or git-build time."]
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(part, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8",
                   newline="\n")
    os.replace(tmp, OUT)
    print("wrote", OUT, OUT.stat().st_size, "bytes;", sum(len(x["versions"]) for x in acts_out), "versions")
    return 0


B.write_part = P.write_part = write_part

if __name__ == "__main__":
    # stale-wording rules (../batch7/stale_fix.py), applied only when this part is written (not when imported)
    sys.path.insert(0, str(FOLDER / "batch7"))
    import stale_fix
    _build_plain = P.build_act
    _n: list[int] = []

    def _build_act_stale(paras, *a, **k):
        stale_fix.fix(P, paras, ACTS[len(_n)]["slug"] if len(_n) < len(ACTS) else "?", set())
        _n.append(1)
        return _build_plain(paras, *a, **k)
    P.build_act = B.build_act = _build_act_stale
    _write_plain = write_part

    def _write_part_stale(*a) -> int:
        EXTRA_DECISIONS.extend(stale_fix.decisions())
        return _write_plain(*a)
    B.write_part = P.write_part = _write_part_stale
    sys.exit(P.main(sys.argv[1:]))
