"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch6.json (SCHEMA.md corpus part): the acts in ACTS
below (administrative improbity, environmental crimes, access to information, federal administrative procedure, and
further federal laws as they are verified).

    python -X utf8 scripts/brazil-law/batch6/parse_batch6.py [--stats] [--dry]

Imports ../batch5b/parse_batch5b.py (which configures ../batch5, ../batch4, ../batch3 and ../proc, the struck-text
replay of Planalto's annotated pages) and replaces only its configuration: the acts, the in-force days, the pins and
the output. Batch 5b's hand tables (MP fates, Senate resolutions, note fixes) stay in place; entries an act here does
not use are not printed. The parts of batch 5b and earlier are not touched (their parsers, run on their own, write the
same bytes as before). No network.

BATCH6_ACTS=<slug,...> selects acts for trial runs; by default the VERIFIED list is written.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
sys.path.insert(0, str(FOLDER / "batch5b"))
import parse_batch5b as PB5B  # noqa: E402  (configures batch 5 / 4 / 3 / parse_proc for batch 5b; reconfigured below)

B5, B4, B, P = PB5B.B5, PB5B.B4, PB5B.B, PB5B.P
PL = P.PL
B5.OUT = Path(os.environ.get("BATCH6_OUT") or FOLDER / "corpus.d" / "99-batch6.json")
B5.STAGE = HERE / ".tmp" / "stage.json"
P.RETRIEVED = "2026-10-29"

PAGES = {k: v for k, v in PB5B.PAGES.items() if k in ("lia", "lia-compilada", "lca", "lai", "lpa")}
PAGES.update(EXTRA_PAGES := {})
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = PAGES

ALL_ACTS: list[dict] = [a for a in PB5B.ALL_ACTS if a["page"] in PAGES]
VERIFIED: list[str] = ["lei-de-improbidade-administrativa", "lei-de-crimes-ambientais", "lei-de-acesso-a-informacao",
                        "lei-do-processo-administrativo"]
ENABLED = [s for s in os.environ.get("BATCH6_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = ACTS

# In-force days of the acts (their own closing clause and the DOU day; LC 95/1998 art. 8 § 1 counting).
ACT_DAY_ALL = dict(PB5B.ACT_DAY_ALL)
ACT_DAY_ALL.update({
    "lei-9605-1998": ("1998-03-30", "Lei 9.605/1998: its vigência article (art. 81) was vetoed, so LINDB art. 1 applies: in "
                                    "force 45 days after publication (DOU 13.2.1998), on 30.3.1998. The DOU of 17.2.1998 "
                                    "printed a retificação, but it corrects only the heading ('onde se lê: Nº 9.605, DE "
                                    "FEVEREIRO DE 1998 leia-se: LEI Nº 9.605, DE 12 DE FEVEREIRO DE 1998', as the Chamber of "
                                    "Deputies' record of the law gives it), not the law's text, so it is not a new "
                                    "publication of the text that would restart the period (LINDB art. 1 § 3)"),
    "lei-9784-1999": ("1999-02-01", "Lei 9.784/1999 art. 70: 'Esta Lei entra em vigor na data de sua publicação' (DOU "
                                    "1.2.1999). The retificação in the DOU of 11.3.1999 corrects only the signatures ('Na "
                                    "página 5, 1ª coluna, nas assinaturas, leia-se: Fernando Henrique Cardoso, Renan "
                                    "Calheiros e Paulo Paiva', as the Chamber of Deputies' record of the law gives it), not "
                                    "the law's text"),
})
ACT_LAWS_ALL = dict(PB5B.ACT_LAWS_ALL)
ACT_LAWS_ALL.update({
    "lei-9605-1998": B._act_law("Lei nº 9.605, de 1998", "Dispõe sobre as sanções penais e administrativas derivadas de "
                                "condutas e atividades lesivas ao meio ambiente, e dá outras providências.", "1998-02-12",
                                "1998-02-13", PAGES["lca"]),
    "lei-9784-1999": B._act_law("Lei nº 9.784, de 1999", "Regula o processo administrativo no âmbito da Administração "
                                "Pública Federal.", "1999-01-29", "1999-02-01", PAGES["lpa"]),
})
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# Amending laws whose own vigência is staged by level of government: dated by the first day the new wording was law
# (for the União, the States and the Distrito Federal); the later day for the other levels is given in the reason.
P.VIGENCIA_FIXED["lei-13019-2014"] = (
    "2016-01-23", "art. 88 as amended by Lei 13.204/2015: 'Esta Lei entra em vigor após decorridos quinhentos e quarenta "
                  "dias de sua publicação oficial' (DOU 1.8.2014: the 540th day counted from publication is 22.1.2016, "
                  "LC 95/1998 art. 8 § 1), and § 1: 'Para os Municípios, esta Lei entra em vigor a partir de 1º de janeiro "
                  "de 2017'. Its changes are dated 23.1.2016, the day they became law for the União, the States and the "
                  "Distrito Federal; for the Municípios they applied from 1.1.2017")
P.VIGENCIA_FIXED["lei-14129-2021"] = (
    "2021-06-28", "art. 55: 'Esta Lei entra em vigor após decorridos: I - 90 (noventa) dias de sua publicação oficial, "
                  "para a União; II - 120 (cento e vinte) dias [...] para os Estados e o Distrito Federal; III - 180 (cento "
                  "e oitenta) dias [...] para os Municípios' (DOU 30.3.2021: the 90th day counted from publication is "
                  "27.6.2021, LC 95/1998 art. 8 § 1). Its changes are dated 28.6.2021, the day they became law for the "
                  "União; for the States and the Distrito Federal they applied from 28.7.2021, for the Municípios from "
                  "26.9.2021")

# ---------------------------------------------------------------------------------------------------------------
# Medidas Provisórias reissued with a changed wording, where the act's page prints both wordings and credits each to
# its own reissue ('Incluído pela Medida Provisória nº 1.710, de 1998', then 'Redação dada pela Medida Provisória nº
# 1.710-1, de 1998'). parse_proc keys an MP by its base number, which would date both wordings by the first issue; a
# reissue listed here gets its own key (mp-<n>r<reissue>-<year>), page and day. Other reissues keep the base key.
REISSUES: set[tuple[str, str, str]] = {("1710", "1", "1998")}
REISSUE_KEY = re.compile(r"^mp-(\d+)r(\d+)-(\d{4})$")
REISSUE_REF = re.compile(r"Medida\s+Provis[óo]ria\s*(?:n\s*[º°o]?\s*\.?)?\s*(\d{1,2}(?:\.\d{3})+|\d+)-(\d{1,2})(?!\d)\s*,?\s*de\s+(\d{4})", re.I)
_law_key6, _law_label6, _lexml_url6, _page_info6 = P.law_key, P.law_label, P.lexml_url, P.page_info


def law_key(text: str, year_of: dict | None = None) -> str | None:
    m = REISSUE_REF.search(text)
    if m:
        n = m.group(1).replace(".", "")
        if (n, m.group(2), m.group(3)) in REISSUES and not P.LAW_REF.search(text[:m.start()]):
            return f"mp-{n}r{m.group(2)}-{m.group(3)}"
    return _law_key6(text, year_of)


def law_label(key: str) -> str:
    m = REISSUE_KEY.match(key)
    if m:
        num = f"{int(m.group(1)):,}".replace(",", ".")
        return f"Medida Provisória nº {num}-{m.group(2)}, de {m.group(3)}"
    return _law_label6(key)


def lexml_url(key: str, enacted: str | None) -> str | None:
    m = REISSUE_KEY.match(key)
    if m:
        return f"{P.LEXML}medida.provisoria:{enacted};{m.group(1)}-{m.group(2)}" if enacted else None
    return _lexml_url6(key, enacted)


# MP pages whose heading leaves out the 'DE' before the year ('MEDIDA PROVISÓRIA Nº 62, DE 22 DE AGOSTO 2002'): the
# heading is read with it put back (only for page_info's dates; the act pages are not touched)
HEAD_NO_DE = re.compile(r"(\bDE\s+\d{1,2}\s*[º°o]?\s+DE\s+(?:JANEIRO|FEVEREIRO|MAR[ÇC]O|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|"
                        r"OUTUBRO|NOVEMBRO|DEZEMBRO))\s+(\d{4})")
HEAD_FIXED: list[str] = []


def page_info(key: str) -> dict:
    """parse_proc/batch 3 page_info; a reissue key reads its own pinned page under the base key's number check, and a
    heading with no 'DE' before the year is read with it."""
    m = REISSUE_KEY.match(key)
    base = f"mp-{m.group(1)}-{m.group(3)}" if m else key
    raw0, dec0 = P.raw, P.decode

    def raw(ident: str):
        return raw0("law:" + key) if (m and ident == "law:" + base) else raw0(ident)

    def decode(b: bytes) -> str:
        t = dec0(b)
        t2 = HEAD_NO_DE.sub(r"\1 DE \2", t, count=1)
        if t2 != t:
            HEAD_FIXED.append(key)
        return t2
    P.raw, P.decode = raw, decode
    try:
        info = _page_info6(base)
    finally:
        P.raw, P.decode = raw0, dec0
    if m and info:
        P.LEXML_USED.discard(_lexml_url6(base, info.get("enacted")))
        P.LEXML_USED.add(lexml_url(key, info.get("enacted")))
    return info


P.law_key, P.law_label, P.lexml_url, P.page_info = law_key, law_label, lexml_url, page_info
B.law_key, B.law_label, B.lexml_url, B.page_info = law_key, law_label, lexml_url, page_info

# An MP the Senate declared 'prejudicada' after rejecting its conversion bill: Planalto prints 'Prejudicada' after the
# struck wording (Lei 9.605 art. 25 § 5º), read like '(Vigência encerrada)'
P.LAPSED_WORDS = re.compile(P.LAPSED_WORDS.pattern + r"|(?<=[.;:)])\s*(?-i:Prejudicad[ao])\s*$", re.I)

# Notes with a typing slip that hides them from parse_proc's note patterns: '(Renumerando do §2º para §3º pela Lei nº
# 13.052, de 2014)' (Lei 9.605 art. 25) is read as '(Renumerado do ...)'. Only the note's verb is corrected.
NOTE_VERB_TYPOS = [(re.compile(r"\(\s*Renumerando(\s+do)"), r"(Renumerado\1")]
NOTE_VERB_USED: list[str] = []
_decode6 = P.decode


def decode(b: bytes) -> str:
    t = _decode6(b)
    for rx, rep in NOTE_VERB_TYPOS:
        t, n = rx.subn(rep, t)
        if n:
            NOTE_VERB_USED.append(rx.pattern)
    return t


P.decode = B.decode = decode
P.MP_LAPSE["mp-62-2002"] = (
    "2002-11-20", "declared 'prejudicada': Ato Declaratório do Presidente do Senado Federal de 20.11.2002 (DOU 21.11.2002): "
                  "'em sessão realizada no dia 20 de novembro de 2002, o Plenário da Casa declarou prejudicada a Medida "
                  "Provisória nº 62, de 22 de agosto de 2002 [...] em virtude da rejeição do Projeto de Lei de Conversão nº "
                  "27, de 2002'; the Lei 9.605 wording of art. 25 it had replaced is back from that day")
B5.MP_REJECTED["mp-62-2002"] = (
    "Medida Provisória nº 62, de 2002: prejudicada",
    "Medida Provisória nº 62, de 2002, declared prejudicada by the Senate after its conversion bill was rejected (Ato "
    "Declaratório de 20 de novembro de 2002)")
P.MP_PENDING.update({
    "mp-1710-1998": "Medida Provisória nº 1.710, de 7.8.1998, 'Reeditada pela MPv nº 1.710-1, de 1998', whose changed "
                    "wording of Lei 9.605 art. 79-A Planalto prints and credits separately: the reissue's wording ends it",
    "mp-1710r1-1998": "Medida Provisória nº 1.710-1, de 8.9.1998, 'Reeditada pela MPv nº 1.710-2, de 1998', a chain of "
                      "reissues down to MP 2.163-41, de 23.8.2001; Planalto prints no wording of the reissues in between, "
                      "so its wording of Lei 9.605 art. 79-A stands until MP 2.163-41's",
    "mp-2163-2001": "Medida Provisória nº 2.163-41, de 23.8.2001 (DOU 24.8.2001) was in force on 11.9.2001, so it stays in "
                    "force until a later MP revokes it or Congress votes on it (Emenda Constitucional 32/2001, art. 2)",
})

# Differences left between the last version and Planalto's consolidated page, each checked by hand against both pages
B.EXPLAINED.clear()
B.EXPLAINED.update({
    "lei-de-improbidade-administrativa": {
        "art-17": "typesetting: § 6º-A ends '(Código de Processo Civil' with no closing parenthesis or full stop on both "
                  "pages; the consolidated page prints a comma after its '(Incluído pela Lei nº 14.230, de 2021)' note, "
                  "which is read into the text",
        "titulos": "the consolidated page keeps the revoked heading 'Seção II-A' with its '(Revogado pela Lei nº 14.230, de "
                   "2021)' note as a placeholder; the history leaves revoked text out",
    },
})

# batch 5b's tables for its own acts that would print decisions here whether used or not
P.NOTE_FIX = {}
P.COURTS = {}
PB5B.SPLIT_NOTES.clear()

# ---------------------------------------------------------------------------------------------------------------
# '(Incluído pela Lei X, com a redação dada pela Lei Y)': a dispositivo X inserted and Y reworded before or after it
# took effect. parse_proc credits the first law named; here the wording is credited to Y, the law that wrote it, from the
# later of the two in-force days (the wording cannot be law before X has put the dispositivo in force, nor before Y).
WITH_WORDING = re.compile(r"\(\s*(?:Inclu[ií]d[oa]|Acrescid[oa]|Acrescentad[oa])\s+pel[ao]\s+(.+?),?\s+com\s+a\s+reda[çc][ãa]o\s+"
                          r"dada\s+pel[ao]\s+(.+?)\)", re.I)
WITH_WORDING_USED: list[str] = []
# Struck wordings that never took effect: replaced (or dropped) by a later law before the law that wrote them came into
# force. (act, unit, label, text start) -> reason. The line is left out of every version.
NEVER_IN_FORCE: dict[tuple[str, str, str, str], str] = {
    ("lei-de-improbidade-administrativa", "art-10", "XIX -", "XIX - frustrar a licitude de processo seletivo"): "a",
    ("lei-de-improbidade-administrativa", "art-10", "XX -", "XX - agir negligentemente"): "a",
    ("lei-de-improbidade-administrativa", "art-10", "XXI -", "XXI - liberar recursos de parcerias"): "a",
}
NEVER_WHY = {
    "a": "Lei 8.429 art. 10 XIX to XXI as Lei 13.019/2014 art. 77 first inserted them (struck, noted only 'Incluído pela "
         "Lei nº 13.019, de 2014'): Lei 13.204/2015 (DOU 15.12.2015, in force on publication) rewrote that art. 77 before "
         "Lei 13.019 came into force on 23.1.2016, so art. 10 received the wording of XIX and XX that Planalto notes "
         "'Incluído pela Lei nº 13.019, de 2014, com a redação dada pela Lei nº 13.204, de 2015', and XXI never existed",
}
NEVER_USED: list[tuple[str, str]] = []
_lifespans6, _note_laws6 = P.lifespans, P.note_laws


def note_laws(paras: list[dict]) -> set[str]:
    out = _note_laws6(paras)
    for p in paras:
        for n in p["notes"]:
            m = WITH_WORDING.search(n)
            k = m and law_key(m.group(2))
            if k:
                out.add(k)
    return out


# A wording Planalto credits to the first and the last MP of one reissue chain ('Redação dada pela Medida Provisória nº
# 1.337, de 1996' and '... nº 1.472-31, de 1996'): parse_proc starts it with the later MP. Where the wording is printed
# in the first MP's own page too, it starts with the first MP (the chain kept it in force; CF art. 62 before EC 32/2001
# let a reissued MP carry its text on). (first, last) MP keys; the check reads both pages.
MP_CHAINS: set[tuple[str, str]] = {("mp-1337-1996", "mp-1472-1996"), ("mp-1984-2000", "mp-2180-2001")}
MP_CHAIN_USED: list[str] = []
_PAGE_TEXT: dict[str, str] = {}


def _alnum(s: str) -> str:
    return re.sub(r"[^0-9a-zà-ÿ]", "", s.lower())


def page_has(key: str, text: str) -> bool:
    if key not in _PAGE_TEXT:
        r = P.raw("law:" + key)
        _PAGE_TEXT[key] = _alnum(P.htmlmod.unescape(re.sub(r"<[^>]+>", " ", P.decode(r[0])))) if r else ""
    body = _alnum(text[len(text.split(" ", 2)[0]):])[:80] if text else ""
    return bool(body) and body[5:] in _PAGE_TEXT[key]


# Renumbered dispositivos ('Renumerado do § 3º para § 4º pela Lei nº 13.052, de 2014'): Planalto prints only the new
# label. (1) Where no wording under the old label is printed at all, the line stood under its old label (same words)
# until the renumbering: that wording is added, ended by the renumbered line. (2) Where the old-label wording is printed
# but was replaced by a Medida Provisória that lapsed before the renumbering, it is back from the lapse until the
# renumbering (Lei 9.605 art. 25 § 2º: MP 62/2002, prejudicada on 20.11.2002; renumbered § 3º by Lei 13.052/2014).
RENUM_ADDED: list[str] = []
RENUM_RESTORED: list[str] = []


def _renum_old(p: dict) -> str | None:
    for n in p["notes"]:
        if re.search(r"Renumerad", n, re.I):
            old = P.renum_label(n)
            if old and old != p["label"]:
                return old
    return None


def _body(p: dict) -> str:
    return p["text"][len(p["label"]):].strip() if p["label"] and p["text"].startswith(p["label"]) else p["text"]


def renum_pre(paras: list[dict], cx) -> None:
    for i in range(len(paras) - 1, -1, -1):
        p = paras[i]
        old = None if p["heading"] else _renum_old(p)
        if not old:
            continue
        if any(q["unit"] == p["unit"] and q["label"] == old and not _renum_old(q) for q in paras):
            continue   # an earlier wording under the old label is printed: parse_proc's renumbering rule applies
        v = dict(p, label=old, text=old + p["text"][len(p["label"]):], state="struck", plain_text="", struck_text="",
                 notes=[n for n in p["notes"] if not re.search(r"Renumerad", n, re.I)], renum_virtual=True)
        paras.insert(i, v)
        RENUM_ADDED.append(f"{cx.act} {p['unit']} [{old} -> {p['label']}]")
    for i, p in enumerate(paras):
        p["i"] = i


def renum_post(paras: list[dict], cx, problems: list[str]) -> None:
    for p in list(paras):
        old = None if p["heading"] else _renum_old(p)
        if not old or not p["start"]:
            continue
        day, law = p["start"], p["start_law"]
        r = next((q for q in paras if q["unit"] == p["unit"] and q["label"] == old and _body(q) == _body(p)
                  and q["state"] != "plain" and not q.get("renum_virtual")), None)
        if not r or not r["end"] or r["end"] >= day:
            continue
        m = next((q for q in paras if q["unit"] == p["unit"] and q["label"] == old and q["start"] == r["end"]
                  and q["end_how"] == "lapse" and q["end"] and q["end"] < day), None)
        if not m:
            continue
        c = dict(r, start=m["end"], start_law=m["end_law"], end=day, end_law=law, end_how="renumbered", gaps=[],
                 skip=False, restored=True)
        paras.insert(paras.index(m) + 1, c)
        RENUM_RESTORED.append(f"{cx.act} {p['unit']} [{old}] {m['end']}..{day}")
        # parse_proc reports the lapsed MP's later-numbered line as restored after the renumbered one: not a problem
    for i, p in enumerate(paras):
        p["i"] = i
    keep = []
    for pr in problems:
        mm = re.match(r"restored wording after an open one: (\S+) \[([^\]]+)\]", pr)
        if mm and any(q["unit"] == mm.group(1) and q["label"] == mm.group(2) and q["state"] == "plain" and _renum_old(q)
                      for q in paras):
            continue
        keep.append(pr)
    problems[:] = keep


def lifespans(paras: list[dict], cx) -> list[str]:
    problems: list[str] = []
    renum_pre(paras, cx)
    for p in paras:
        for (act, unit, label, start), why in NEVER_IN_FORCE.items():
            if cx.act == act and p["unit"] == unit and p["label"] == label and p["text"].startswith(start) and p["state"] != "plain":
                p["never"] = why
        keys = {law_key(n): n for n in p["notes"] if P.START_KIND.search(n) and law_key(n)}
        for first, last in MP_CHAINS:
            if first in keys and last in keys:
                if page_has(first, p["text"]) and page_has(last, p["text"]):
                    p["notes"] = [n for n in p["notes"] if n != keys[last]]
                    MP_CHAIN_USED.append(f"{cx.act} {p['unit']} [{p['label']}] from {P.law_label(first)} (also printed in "
                                         f"{P.law_label(last)})")
                else:
                    problems.append(f"MP chain {first}/{last}: wording not on both pages: {p['unit']} [{p['label']}]")
        for i, n in enumerate(p["notes"]):
            m = WITH_WORDING.search(n)
            if not m:
                continue
            x, y = law_key(m.group(1)), law_key(m.group(2))
            if not (x and y and x in cx.eff and y in cx.eff):
                problems.append(f"no in-force day for {x} or {y} (note {n!r})")
                continue
            p["notes"][i] = f"(Redação dada pela {P.law_label(y)})"
            p["with_wording"] = True
            day = max(cx.eff[x], cx.eff[y])
            if day != cx.eff[y]:
                k = (y, cx.act, p["unit"])
                if P.VIGENCIA_PROVISION.get(k, (day,))[0] != day:
                    problems.append(f"two in-force days for {y} in {cx.act} {p['unit']}")
                P.VIGENCIA_PROVISION[k] = (day, f"inserted by {P.law_label(x)} (in force {cx.eff[x]})")
                other = [q for q in paras if q["unit"] == p["unit"] and q is not p and not q.get("with_wording")
                         and not any(WITH_WORDING.search(z) for z in q["notes"])
                         and any(law_key(z) == y for z in q["notes"])]
                if other:
                    problems.append(f"{y} also named by other notes in {cx.act} {p['unit']}: its day would move")
            WITH_WORDING_USED.append(f"{cx.act} {p['unit']} [{p['label']}] ({P.law_label(x)}, wording {P.law_label(y)}, "
                                     f"from {day})")
    problems += _lifespans6(paras, cx)
    renum_post(paras, cx, problems)
    for p in paras:
        if p.get("never"):
            p["skip"], p["end"], p["end_law"], p["end_how"], p["gaps"] = True, p["start"], p["start_law"], "never-in-force", []
            NEVER_USED.append((p["never"], f"{cx.act} {p['unit']} [{p['label']}] {p['text'][:60]!r}"))
    return problems


P.lifespans = B.lifespans = lifespans
P.note_laws = B.note_laws = note_laws

SRC = HERE / "sources_batch6.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

_inner5 = PB5B._write_part5


def _inner(*a) -> int:
    if HEAD_FIXED:
        B5.EXTRA_DECISIONS.append(
            "Medida Provisória pages whose heading leaves out 'DE' before the year ('MEDIDA PROVISÓRIA Nº 62, DE 22 DE AGOSTO "
            "2002') are read with it, for their dates only: " + ", ".join(P.law_label(k) for k in dict.fromkeys(HEAD_FIXED))
            + ".")
    if WITH_WORDING_USED:
        B5.EXTRA_DECISIONS.append(
            "A dispositivo noted '(Incluído pela Lei X, com a redação dada pela Lei Y)' is credited to Y, the law that wrote "
            "its words, from the later of the two laws' in-force days: " + "; ".join(dict.fromkeys(WITH_WORDING_USED)) + ".")
    if NOTE_VERB_USED:
        B5.EXTRA_DECISIONS.append("Notes whose verb has a typing slip are read with the verb corrected, so the note is "
                                  "not taken for law text: '(Renumerando do ...)' is read as '(Renumerado do ...)' (Lei "
                                  "9.605 art. 25 §§ 3º to 5º, renumbered by Lei 13.052/2014).")
    if RENUM_ADDED:
        B5.EXTRA_DECISIONS.append(
            "A dispositivo Planalto prints only under its new number, with a 'Renumerado do ... para ...' note, stood "
            "under its old number with the same words until the renumbering; that wording is added: "
            + "; ".join(dict.fromkeys(RENUM_ADDED)) + ".")
    if RENUM_RESTORED:
        B5.EXTRA_DECISIONS.append(
            "A wording a lapsed Medida Provisória had replaced is back from the lapse until the law that renumbered it: "
            + "; ".join(dict.fromkeys(RENUM_RESTORED)) + ".")
    if MP_CHAIN_USED:
        B5.EXTRA_DECISIONS.append(
            "A wording Planalto credits to both the first and the last Medida Provisória of one reissue chain starts with the "
            "first, once its text is found on both MP pages (the reissues kept it in force): "
            + "; ".join(dict.fromkeys(MP_CHAIN_USED)) + ".")
    if NEVER_USED:
        for code, why in NEVER_WHY.items():
            used = [u for c, u in NEVER_USED if c == code]
            if used:
                B5.EXTRA_DECISIONS.append(f"Struck wordings that never took effect are left out of every version: {why} "
                                          f"({'; '.join(dict.fromkeys(used))}).")
    return _inner5(*a)


PB5B._write_part5 = _inner
_outer5 = B5.write_part
# Chamber of Deputies records the hand tables cite (pinned as ctx:* in sources_batch6.json), listed as a source when an
# act that relies on them is in the part
CONTEXT = [
    {"when": lambda: any(a["law"] == "lei-9605-1998" for a in ACTS),
     "pins": ["ctx:camara-lei-9605-1998-norma", "ctx:camara-lei-9605-1998-retificacao", "ctx:camara-ad-20-11-2002"],
     "what": "the record and the retificação (DOU 17.2.1998) of Lei 9.605/1998, and the Ato Declaratório of 20.11.2002 "
             "declaring Medida Provisória nº 62, de 2002 prejudicada"},
    {"when": lambda: any(a["law"] == "lei-9784-1999" for a in ACTS),
     "pins": ["ctx:camara-lei-9784-1999-norma", "ctx:camara-lei-9784-1999-retificacao"],
     "what": "the record and the retificação (DOU 11.3.1999) of Lei 9.784/1999"},
]


def write_part(*a) -> int:
    rc = _outer5(*a)
    # batch 5's writer words every act's replay check as against 'the unstruck text of Planalto's page of the act'; an
    # act with a separate consolidated page (compilada) is checked against that page, so say so
    import json as _json
    part = _json.loads(B5.OUT.read_text(encoding="utf-8"))
    no_page = ("the unstruck text of Planalto's page of the act (Planalto publishes no separate consolidated page for "
               "it)")
    for i, d in enumerate(part["decisions"]):
        for act in ACTS:
            if act["consolidated"] != act["page"] and act["slug"] in d and no_page in d:
                d = d.replace(no_page, f"Planalto's consolidated page ({PAGES[act['consolidated']].rsplit('/', 1)[-1]})")
        part["decisions"][i] = d
    ctx = [c for c in CONTEXT if c["when"]()]
    if ctx:
        part["sources"].append({
            "name": "Câmara dos Deputados, Legislação Informatizada: records of the publication of some acts",
            "url": "https://www2.camara.leg.br/legin/fed/", "retrieved": "2026-10-31",
            "requests": sum(len(c["pins"]) for c in ctx),
            "licence": "Official acts are not protected by copyright (Lei 9.610/1998 art. 8, IV)",
            "notes": "Read only for facts about publication, never for law text: " + "; ".join(c["what"] for c in ctx)
                     + f". Each page is pinned to a dated capture in {B5.SRC.parent.name}/{B5.SRC.name} (ids ctx:...)."})
    tmp = B5.OUT.with_suffix(".json.tmp")
    tmp.write_text(_json.dumps(part, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8",
                   newline="\n")
    os.replace(tmp, B5.OUT)
    return rc


B5.write_part = B.write_part = P.write_part = write_part

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
