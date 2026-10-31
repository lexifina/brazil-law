"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch16<x>.json (SCHEMA.md corpus parts): more major federal
acts not yet in the corpus, in small parts of 2-4 acts each (99-batch16a, 99-batch16b, ...).

    BATCH16_PART=a python -X utf8 scripts/brazil-law/batch16/parse_batch16.py [--stats] [--dry]

Imports ../batch15/parse_batch15.py (which configures batch 14 and everything below it, plus batch 15's hand tables and
the Medida Provisória 905/955 model) with no act of its own, and replaces only the configuration: the acts, the in-force
days, the hand tables for these acts, the pins and the output. Earlier parts are not touched. No network.

BATCH16_PART selects the part (its acts are PARTS[part]); BATCH16_ACTS=<slug,...> selects acts for trial runs
(BATCH16_OUT=<file> writes elsewhere). After writing a part run ../effects_fix.py on it (effect days).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH15_PART"] = "-"   # batch 15 configures no act of its own here
os.environ.pop("BATCH15_ACTS", None)
os.environ.pop("BATCH15_OUT", None)
sys.path.insert(0, str(FOLDER / "batch15"))
import parse_batch15 as B15  # noqa: E402

B14, B13, B12, B11, B10, B9, B8, B7, B6, B5, B, P = (B15.B14, B15.B13, B15.B12, B15.B11, B15.B10, B15.B9, B15.B8, B15.B7,
                                                     B15.B6, B15.B5, B15.B, B15.P)
PL = P.PL
PART = os.environ.get("BATCH16_PART", "a")
B5.OUT = Path(os.environ.get("BATCH16_OUT") or FOLDER / "corpus.d" / f"99-batch16{PART}.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = dict(B15.PAGES)
PAGES.update({
    # batch 13's deferred acts (their page ids as pinned in batch13/sources_batch13.json)
    "l4320": "leis/l4320.htm",
    "l4320-compilado": "leis/l4320compilado.htm",
    "lfgts": "leis/l8036consol.htm",
    "lfgts-compilada": "leis/l8036compilada.htm",
})
B.PAGES.clear()
B.PAGES.update(PAGES)
for M in (B5, B6, B7, B8, B9, B10, B11, B12, B13, B14, B15):
    M.PAGES = PAGES

_CBA, _L4320, _FGTS = "codigo-brasileiro-de-aeronautica", "lei-4320-de-1964", "lei-do-fgts"
ALL_ACTS: list[dict] = ([a for a in B14.ALL_ACTS if a["slug"] == _CBA]
                        + [a for a in B13.ALL_ACTS if a["slug"] in (_L4320, _FGTS)])
PARTS: dict[str, list[str]] = {
    "a": [_CBA],
}
VERIFIED: list[str] = PARTS.get(PART, [])
ENABLED = [s for s in os.environ.get("BATCH16_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
for M in (B7, B8, B9, B10, B11, B12, B13, B14, B15):
    M.ACTS[:] = ACTS
ACT_DAY_ALL = {**B13.ACT_DAY_ALL, **B14.ACT_DAY_ALL}
ACT_LAWS_ALL = {**B13.ACT_LAWS_ALL, **B14.ACT_LAWS_ALL}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# earlier batches' printed-everywhere lists emptied (their act-keyed tables do nothing here)
P.COURTS.clear()
P.NOTE_FIX = {}
B9.REPEALS.clear()
EXTRA: list[str] = []   # decisions added to the part

# ---------------------------------------------------------------------------------------------------------------
# Código Brasileiro de Aeronáutica (Lei 7.565/1986), part a
P.VIGENCIA_FIXED["mp-1089-2021"] = (
    "2021-12-30", "art. 6: 'Esta Medida Provisória entra em vigor: I - após noventa dias da sua publicação, quanto ao Anexo; e "
                  "II - na data de sua publicação, quanto aos demais dispositivos' (DOU 30.12.2021): its changes to the Código "
                  "Brasileiro de Aeronáutica fall under II (the Anexo is Lei 11.182/2005's fee table)")
P.MP_LAPSE["mp-1240-2024"] = (
    "2024-11-07", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 112, de 2024 (DOU 14.11.2024): 'teve seu "
                  "prazo de vigência encerrado no dia 6 de novembro de 2024'")
_W181 = ("CBA arts. 181 and 182: Medida Provisória 714/2016 (2.3.2016) gave art. 181 a new caput, incisos I-II and §§ 3º-6º and "
         "revoked art. 181 III and art. 182; Lei 13.319/2016, its conversion (26.7.2016), vetoed its art. 181 ('Art. 181. "
         "(VETADO) [...] § 5º (VETADO). § 6º (VETADO).') and kept none of the revocations, so the 1986 text of both articles "
         "is in force again from 26.7.2016 until Medida Provisória 863/2018 (13.12.2018). Planalto prints these 1986 "
         "wordings a second time below MP 714's (struck, with MP 863's notes); they start on 26.7.2016, credited to Lei "
         "13.319, and the MP 714 caput ends then")
_W303 = ("CBA art. 303 § 2º: the 1986 wording ('§ 2º A autoridade mencionada no parágrafo anterior [...]') is printed struck "
         "below the § 2º Lei 9.614/1998 inserted, which renumbered it § 3º ('Renumerado do § 2º para § 3º com nova "
         "redação'); it stands from 1986 to 6.3.1998")
_RESTORE_181 = {"start": "2016-07-26", "start_law": "lei-13319-2016", "restored": True}
B8.SPAN_FIX += [
    ((_CBA, "art-181", "Art. 181", "Art. 181. A concessão ou autorização somente será dada", 0),
     {"end": "2016-07-26", "end_law": "lei-13319-2016", "end_how": "conversion"}, _W181),
    ((_CBA, "art-181", "Art. 181", "Art. 181. A concessão somente será dada", 1),
     dict(_RESTORE_181, end="2018-12-13", end_law="mp-863-2018", end_how="successor"), _W181),
    *[((_CBA, unit, lab, pre, 1), _RESTORE_181, _W181) for unit, lab, pre in [
        ("art-181", "I -", "I - sede no Brasil"), ("art-181", "II -", "II - pelo menos 4/5"),
        ("art-181", "III -", "III - direção confiada"), ("art-182", "Art. 182", "Art. 182. A autorização pode ser outorgada"),
        ("art-182", "I -", "I - às sociedades anônimas"), ("art-182", "II -", "II - às demais sociedades"),
        ("art-182", "Parágrafo único", "Parágrafo único. Em se tratando de serviços aéreos especializados")]],
    ((_CBA, "art-303", "§ 2º", "§ 2º A autoridade mencionada no parágrafo anterior", 0),
     {"start": "1986-12-23", "start_law": None, "end": "1998-03-06", "end_law": "lei-9614-1998", "end_how": "successor"},
     _W303),
]
B.EXPLAINED[_CBA] = {
    "art-184": "the consolidated page prints arts. 184 to 186 as one line ('Art. 184 a 186 (Revogado pela Lei nº 13.842, de "
               "2019) e (Revogado pela Lei nº 14.368, de 2022)'); the annotated page strikes each article (revoked by "
               "Medida Provisória 863/2018, 13.12.2018)",
    "art-197": "the consolidated page drops a word ('exames de proficiência de e aeroviários'); the annotated page reads "
               "'exames de proficiência de aeronautas e aeroviários'",
    "art-270": "the consolidated page drops the § sign of § 2º ('2° O saldo de 70% [...]'); the annotated page prints '§ 2°'",
    "titulos": "the consolidated page still prints the headings of divisions revoked by Medida Provisória 1.089/2021 and Lei "
               "14.368/2022 (Título III Capítulo V Seção II, Título IV Capítulo IV Seção IV, Título VI Capítulo II "
               "'Serviços Aéreos Privados', Título VI Capítulo III Seções I-III, Capítulo VI) with a '(Revogado pela Lei nº "
               "14.368, de 2022)' note; the annotated page strikes them, and a revoked division has no heading",
}

# A dispositivo whose caput (or enclosing §) a Medida Provisória revoked as a whole: Planalto notes the MP's revocation on
# that line only, and on its incisos, parágrafos and alíneas only the conversion law's revocation ('Revogado pela Lei nº
# 14.368, de 2022'). They fall with the line above them on the MP's day (MP 1.089/2021 art. 5 IV m): 'os art. 73 a art. 76',
# n) 'a Seção II do Capítulo V do Título III', u) 'os art. 116 e art. 117').
CONV_CHILD_ACTS = {_CBA}
CONV_CHILD_USED: list[str] = []


def conv_children(paras, cx, record=True):
    if cx.act not in CONV_CHILD_ACTS:
        return
    for i, p in enumerate(paras):
        if p["heading"] or p["state"] == "plain" or p.get("skip") or p.get("end_how") != "note" or not p["end_law"]:
            continue
        lv = P.level(p["label"])
        if lv == 0:
            continue
        par = None
        for q in reversed(paras[:i]):
            if q["unit"] != p["unit"]:
                break
            if q["heading"] or q.get("skip") or P.level(q["label"]) >= lv:
                continue
            if q["start"] <= p["start"] and (q["end"] is None or q["end"] > p["start"]):
                par = q
                break
        if par is None or par["state"] == "plain" or not par["end"] or par["end"] >= p["end"]:
            continue
        fate = cx.mp.get(par["end_law"]) or {}
        if fate.get("converted") != p["end_law"]:
            continue
        if any(P.law_key(n, cx.mp.get("_years")) == par["end_law"] for n in p["notes"]):
            continue
        p["end"], p["end_law"], p["end_how"] = par["end"], par["end_law"], "parent"
        if record:
            CONV_CHILD_USED.append(f"{p['unit']} [{p['label']}]")


_lifespans16 = P.lifespans


_CX: list = [None]


def lifespans(paras, cx):
    problems = _lifespans16(paras, cx)
    _CX[0] = cx
    conv_children(paras, cx)
    return problems


_apply_rewrites16 = P.apply_rewrites


def apply_rewrites(paras, act, eff, problems):
    out = _apply_rewrites16(paras, act, eff, problems)
    if _CX[0] is not None and _CX[0].act == act["slug"]:
        conv_children(paras, _CX[0], record=False)
    return out


P.lifespans = B.lifespans = lifespans
P.apply_rewrites = B.apply_rewrites = apply_rewrites

# ---------------------------------------------------------------------------------------------------------------
_inner16 = B6.PB5B._write_part5


def _inner(*a):
    dec = list(EXTRA)
    if CONV_CHILD_USED:
        dec.append("Código Brasileiro de Aeronáutica: where Medida Provisória 1.089/2021 revoked whole articles or sections (its "
                   "art. 5 IV: 'os art. 73 a art. 76', 'a Seção II do Capítulo V do Título III', 'os art. 116 e art. 117', "
                   "...), Planalto notes the MP's revocation on the caput only and on the lines under it only the revocation "
                   "by Lei 14.368/2022, its conversion; those lines fall with the caput on the MP's day (30.12.2021): "
                   + ", ".join(dict.fromkeys(CONV_CHILD_USED)) + ".")
    B5.EXTRA_DECISIONS.extend(dec)
    return _inner16(*a)


B6.PB5B._write_part5 = _inner

SRC = HERE / "sources_batch16.json"
if not SRC.exists():
    SRC.write_text('{\n "fetch": []\n}\n', encoding="utf-8", newline="\n")
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
