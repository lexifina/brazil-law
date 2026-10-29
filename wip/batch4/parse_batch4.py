"""Reads the cache and writes scripts/brazil-law/corpus.d/97-batch4.json (SCHEMA.md corpus part): batch 4 of the
Brazil corpus, the acts in ACTS below.

    python -X utf8 scripts/brazil-law/batch4/parse_batch4.py [--stats] [--dry]

Imports ../batch3/parse_batch3.py (which configures ../proc/parse_proc.py, the struck-text replay of Planalto's
annotated pages) and replaces only its configuration: the acts, the hand tables, the pins and the output, as
../rju/parse_rju.py does for Lei 8.112. Batch 3's and the RJU's parts are not touched (their parsers, run on their
own, write the same bytes as before). No network.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

os.environ.pop("BATCH3_RJU", None)
HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
sys.path.insert(0, str(FOLDER / "batch3"))
import parse_batch3 as B  # noqa: E402

P = B.P
PL = P.PL
OUT = FOLDER / "corpus.d" / "97-batch4.json"
STAGE = HERE / ".tmp" / "stage.json"   # batch 3's write_part writes here; the part is finished from it

PAGES = {
    "lrf": "_ato2004-2006/2005/lei/l11101.htm",
    "lrf-compilado": "_ato2004-2006/2005/lei/l11101compilado.htm",
    "jec": "leis/l9099.htm",
}
B.PAGES.clear()
B.PAGES.update(PAGES)

ACTS: list[dict] = [
    {"slug": "lei-de-recuperacao-e-falencia", "short": "LRF", "page": "lrf", "consolidated": "lrf-compilado",
     "law": "lei-11101-2005",
     "title": "Lei de Recuperação Judicial, Extrajudicial e Falência (Lei nº 11.101, de 9 de fevereiro de 2005)",
     "digits": 3, "url": PL + "_ato2004-2006/2005/lei/l11101compilado.htm"},
    {"slug": "juizados-especiais", "short": "JEC", "page": "jec", "consolidated": "jec",
     "law": "lei-9099-1995",
     "title": "Lei dos Juizados Especiais Cíveis e Criminais (Lei nº 9.099, de 26 de setembro de 1995)",
     "digits": 3, "url": PL + "leis/l9099.htm"},
]
B.ACTS[:] = ACTS
B.ACT_DAY.clear()
B.ACT_DAY.update({
    "lei-11101-2005": ("2005-06-09", "Lei 11.101/2005 art. 201: 'Esta Lei entra em vigor 120 (cento e vinte) dias após sua "
                                     "publicação' (published in the DOU of 9.2.2005, edição extra): counted with the "
                                     "publication day and the last day included, in force the day after (LC 95/1998 art. "
                                     "8 § 1º): 9.6.2005"),
    "lei-9099-1995": ("1995-11-26", "Lei 9.099/1995 art. 96: 'Esta Lei entra em vigor no prazo de sessenta dias após a sua "
                                    "publicação' (published in the DOU of 27.9.1995): 27.9.1995 + 60 days = 26.11.1995"),
})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({
    "lei-11101-2005": B._act_law("Lei nº 11.101, de 2005", "Regula a recuperação judicial, a extrajudicial e a falência do "
                                 "empresário e da sociedade empresária.", "2005-02-09", "2005-02-09",
                                 "_Ato2004-2006/2005/Lei/L11101.htm"),   # the record proc/ (CPP part) already gives it
    "lei-9099-1995": B._act_law("Lei nº 9.099, de 1995", "Dispõe sobre os Juizados Especiais Cíveis e Criminais e dá outras "
                                "providências.", "1995-09-26", "1995-09-27", "leis/l9099.htm"),
})
# batch 3's rulings, promulgations and Congress-kept vetoes concern the CTN, ECA and RJU only
P.COURTS = {}
B.PROMULGATED.clear()
B.KEPT_BY_CONGRESS.clear()

# ---------------------------------------------------------------------------------------------------------------
# pins: every Brazil pin file (a page already pinned elsewhere is read at that capture), then batch4's own, which win

SRC = HERE / "sources_batch4.json"
PIN_FILES = [FOLDER / "sources.json", FOLDER / "sources_phase2.json", FOLDER / "codes" / "sources_codes.json",
             FOLDER / "clt" / "sources_clt.json", FOLDER / "proc" / "sources_proc.json",
             FOLDER / "batch3" / "sources_batch3.json", FOLDER / "rju" / "sources_rju.json", SRC]


def sources() -> dict[str, dict]:
    s: dict[str, dict] = {}
    for f in PIN_FILES:
        if f.exists():
            for i in json.loads(f.read_text(encoding="utf-8"))["fetch"]:
                if i.get("ts") or i.get("cc"):
                    s[i["id"]] = i
    return s


B.sources = P.sources = sources

# ---------------------------------------------------------------------------------------------------------------
# hand tables (same meaning as in parse_proc / batch 3 / rju), filled for these acts

B.EXPLAINED.clear()

# Staged vigência clauses, read from each law's own page (the same days as the codes and CLT parts give them)
P.VIGENCIA_FIXED.update({
    "lei-12873-2013": ("2013-10-25", "art. 72: 'Esta Lei entra em vigor: I - [...] art. 32-C da Lei nº 8.212 [...]; II - "
                                     "90 (noventa) dias após [...] arts. 71-B e 71-C da Lei nº 8.213 [...] art. 392-B da "
                                     "Consolidação das Leis do Trabalho; e III - na data de sua publicação quanto aos "
                                     "demais dispositivos' (DOU 25.10.2013); its change to Lei 11.101 (art. 22: art. 48 § "
                                     "2º, the Parágrafo único renumbered § 1º) is among the 'demais dispositivos' and is "
                                     "not in III's list of deferred effects, so it took effect on publication"),
    "lei-13874-2019": ("2019-09-20", "art. 20: 'Esta Lei entra em vigor: I - (VETADO); II - na data de sua publicação, "
                                     "para os demais artigos' (DOU 20.9.2019, edição extra)"),
})

# Typing slip in the label (batch 3's TYPOS rule: only the label words are corrected)
B.TYPOS.append(("Parágrafo-único. O objeto da alienação", "Parágrafo único. O objeto da alienação", "Parágrafo único",
                "Lei 11.101 art. 60: Lei 14.112/2020's wording of the Parágrafo único is printed 'Parágrafo-único.' on "
                "both Planalto pages; read as 'Parágrafo único', so it replaces the struck 2005 wording on 23.1.2021"))

# A Medida Provisória's wording that its conversion law left out: it ends on the conversion law's in-force day (CF art.
# 62: what the conversion law does not keep loses effect), even where a later law wrote the same dispositivo anew.
# (act, unit, label, MP, conversion law, reason); each checked on both acts' pages.
MP_DROPPED = [
    ("lei-de-recuperacao-e-falencia", "art-082-a", "Art. 82-A", "mp-881-2019", "lei-13874-2019",
     "Lei 11.101 art. 82-A as MP 881/2019 art. 9 wrote it ('A extensão dos efeitos da falência somente será admitida "
     "quando estiverem presentes os requisitos da desconsideração da personalidade jurídica [...]'), in force from "
     "30.4.2019: its conversion law, Lei 13.874/2019 (in force 20.9.2019), has no article on Lei 11.101 (its page names "
     "neither the law nor art. 82-A), so that wording ends on 20.9.2019, credited to Lei 13.874; art. 82-A is absent "
     "until Lei 14.112/2020 wrote a new one (in force 23.1.2021). Planalto's annotated page strikes the MP wording above "
     "Lei 14.112's with only its '(Incluído pela Medida Provisória nº 881, de 2019)' note"),
]
MP_DROPPED_USED: list[str] = []

# Vetoed parts of an amending law promulgated after Congress overrode the veto (CF art. 66 § 5), read from the
# promulgation printed at the end of the law's own page (as batch 3's PROMULGATED and the Código Penal part's Lei
# 13.964): law -> (day, reason, {(act, unit, label or None for every line of the unit)}). The law's wording of each
# listed dispositivo starts that day, not on the law's own day; the wording it was to replace stands until then.
LRF = "lei-de-recuperacao-e-falencia"
PROMULGATED_UNITS: dict[str, tuple[str, str, set]] = {
    "lei-14112-2020": ("2021-03-26",
                       "Lei 14.112/2020 (in force 23.1.2021): the parts vetoed on 24.12.2020 were promulgated after "
                       "Congress overrode the veto ('Brasília, 26 de março de 2021 [...] Este texto não substitui o "
                       "publicado no DOU de 26.3.2021 - Edição extra D e republicado em 30.3.2021', printed at the end "
                       "of the Lei 14.112 page, which marks each such part '(VETADO)' followed by '(Promulgação partes "
                       "vetadas)'). In Lei 11.101 they are art. 6 § 13, art. 6-B (whole article), art. 50-A (whole "
                       "article), art. 60 Parágrafo único and art. 66 § 3º; Planalto's 11.101 page credits them to Lei "
                       "14.112 with no mark of the veto. Their wording starts on 26.3.2021; until then art. 60 keeps its "
                       "2005 Parágrafo único, and the others are absent (the page does not print their '(VETADO)' lines)",
                       {(LRF, "art-006", "§ 13"), (LRF, "art-060", "Parágrafo único"), (LRF, "art-066", "§ 3º"),
                        (LRF, "art-006-b", None), (LRF, "art-050-a", None)}),
}
PROMULGATED_USED: list[str] = []
_lifespans = B.lifespans


INSERTED_ARTICLE = re.compile(r"Inclu[íi]d[oa]|Acrescid|Acrescentad", re.I)
ARTICLE_NOTE_USED: list[str] = []


def lifespans(paras: list[dict], cx) -> list[str]:
    problems = _lifespans(paras, cx)
    # A lettered article (art. 6º-B) cannot be in the act as enacted: where Planalto prints its 'Incluído' note only
    # on its last line, every unnoted line of the article dated to the act's own day takes that note's law and day.
    for unit in dict.fromkeys(p["unit"] for p in paras):
        if not re.fullmatch(r"art-\d+-[a-z]+", unit):
            continue
        lines = [p for p in paras if p["unit"] == unit and p["state"] == "plain"]
        laws = {P.law_key(n, cx.mp.get("_years")) for p in lines for n in p["notes"] if INSERTED_ARTICLE.search(n)}
        bare = [p for p in lines if not p["notes"] and p["start"] == cx.act_day]
        if len(laws) == 1 and bare and None not in laws:
            law = laws.pop()
            for p in bare:
                p["start"], p["start_law"] = cx.eff[law], law
            ARTICLE_NOTE_USED.append(f"{unit}: {len(bare)} lines by {P.law_label(law)}")
    for law, (day, _, where) in PROMULGATED_UNITS.items():
        old = cx.eff.get(law)
        if not old:
            continue
        for slug, unit, label in sorted(where, key=str):
            if slug != cx.act:
                continue
            hit = [p for p in paras if p["unit"] == unit and (label is None or p["label"] == label)
                   and p["state"] == "plain" and p["start_law"] == law and p["start"] == old]
            if not hit:
                problems.append(f"PROMULGATED {unit} [{label}]: no line")
                continue
            for p in hit:
                p["start"], p["promulgated"] = day, True
                for q in paras:
                    if (q is not p and q["unit"] == p["unit"] and q["label"] == p["label"] and q["state"] != "plain"
                            and q["end"] == old and q["end_law"] == law):
                        q["end"], q["end_how"] = day, "promulgation"
            PROMULGATED_USED.append(f"{unit} [{label or 'whole article'}]: {len(hit)} lines")
    return problems


B.lifespans = P.lifespans = lifespans
_apply_rewrites = B.apply_rewrites


def apply_rewrites(paras: list[dict], act: dict, eff: dict, problems: list[str]) -> list[str]:
    out = _apply_rewrites(paras, act, eff, problems)
    for slug, unit, label, mp, conv, _ in MP_DROPPED:
        if slug != act["slug"]:
            continue
        hit = [p for p in paras if p["unit"] == unit and p["label"] == label and p["state"] != "plain"
               and p["start_law"] == mp]
        if len(hit) != 1 or conv not in eff:
            out.append(f"MP_DROPPED {unit} [{label}]: {len(hit)} lines")
            continue
        p = hit[0]
        p["end"], p["end_law"], p["end_how"], p["skip"] = eff[conv], conv, "mp-dropped", False
        MP_DROPPED_USED.append(f"{unit} [{label}] ends {eff[conv]}")
    return out


B.apply_rewrites = P.apply_rewrites = apply_rewrites

# ---------------------------------------------------------------------------------------------------------------
# the part file: batch 3's write_part, then this part's own sources, notes and requests

_write_part = B.write_part


def _cc_requests(pins: dict[str, dict]) -> int:
    """Requests gitlaw_common/wayback.py logged for these pins (archive.org captures + CDX), as rju/parse_rju.py."""
    log = FOLDER / ".cache" / "cc" / "requests.jsonl"
    want = set()
    for i in pins.values():
        if i.get("via") == "wayback.py":
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


def write_part(acts_out, laws, decisions, vig_notes, lindb, checks, problems, mpn) -> int:
    used = {a["first_law"] for a in acts_out}
    for act in acts_out:
        for v in act["versions"]:
            for ls in v["credits"].values():
                used |= set(ls)
    used |= {laws[k]["restores"] for k in used if laws.get(k, {}).get("restores")}
    allp = sources()
    pins = {k: v for k, v in allp.items() if k in PAGES or (k.startswith(("law:", "ato:")) and k.split(":", 1)[1] in used)}
    B.sources = lambda: pins          # batch 3's request count and page names: only the pins this part uses
    try:
        decisions = decisions + [
            "Lei 9.099/1995: Planalto publishes one page of the act (l9099.htm), with superseded wording struck through "
            "in place and no separate consolidated page, so its replay check compares the last version with that "
            "page's unstruck text (a check of the replay, not an independent second page)."] + [
            f"A Medida Provisória's wording its conversion law left out: {why}." for (*_, why) in MP_DROPPED
            if MP_DROPPED_USED] + [
            f"{why} ({'; '.join(PROMULGATED_USED)})." for (_, why, _) in PROMULGATED_UNITS.values() if PROMULGATED_USED] + (
            [f"A lettered article (inserted after enactment) whose 'Incluído' note Planalto prints only on its last "
             f"line: its unnoted lines take that note's law and day ({'; '.join(ARTICLE_NOTE_USED)})."]
            if ARTICLE_NOTE_USED else [])
        P.OUT = STAGE
        STAGE.parent.mkdir(exist_ok=True)
        _write_part(acts_out, laws, decisions, vig_notes, lindb, checks, problems, mpn)
    finally:
        B.sources = sources
    part = json.loads(STAGE.read_text(encoding="utf-8"))
    pl = part["sources"][0]
    pl["name"] = ("Planalto (Presidência da República), Legislação: annotated and consolidated pages of Lei 11.101/2005 "
                  "and Lei 9.099/1995 and of every law their notes cite, read as Internet Archive raw captures")
    pl["requests"] += _cc_requests(pins)
    pl["notes"] = pl["notes"].replace(
        "batch3/sources_batch3.json.",
        "batch4/sources_batch4.json (fetched through scripts/gitlaw_common/wayback.py) and, for pages another Brazil "
        "part pinned first, that part's pin file (proc/, batch3/, rju/, ...).")
    part["ai_use"] = ["Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote batch4/fetch_batch4.py and "
                      "batch4/parse_batch4.py (configuration of ../batch3 and ../proc, imported) and the hand tables in "
                      "them (in-force days, MP fates, explained differences) from the official pages. No model wrote, "
                      "summarised or changed legal text; no model runs at data-build or git-build time."]
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(part, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8",
                   newline="\n")
    os.replace(tmp, OUT)
    print("wrote", OUT, OUT.stat().st_size, "bytes;", sum(len(x["versions"]) for x in acts_out), "versions")
    return 0


B.write_part = P.write_part = write_part

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
