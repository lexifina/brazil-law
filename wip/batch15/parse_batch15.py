"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch15<x>.json (SCHEMA.md corpus parts): Lei 8.212/1991
(custeio da Seguridade Social, part 99-batch15a) and Lei 8.213/1991 (benefícios da Previdência Social, part 99-batch15b).

    BATCH15_PART=a python -X utf8 scripts/brazil-law/batch15/parse_batch15.py [--stats] [--dry]

Imports ../batch14/parse_batch14.py (which configures batch 13 and everything below it, plus batch 14's hand tables)
with no act of its own, and replaces only the configuration: the acts, the in-force days, the hand tables for these acts,
the pins and the output. Earlier parts are not touched. No network.

New here: the Medida Provisória 905/2019 -> 955/2020 sequence (MP_PAIRS, ported from clt/parse_clt.py) for the proc
pipeline, and footnote numbers on Lei 8.212's page (l8212cons.htm prints numbered footnotes and their markers).

After writing a part run ../effects_fix.py on it (effect days).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH14_PART"] = "-"   # batch 14 configures no act of its own here
os.environ.pop("BATCH14_ACTS", None)
os.environ.pop("BATCH14_OUT", None)
sys.path.insert(0, str(FOLDER / "batch14"))
import parse_batch14 as B14  # noqa: E402

B13, B12, B11, B10, B9, B8, B7, B6, B5, B, P = (B14.B13, B14.B12, B14.B11, B14.B10, B14.B9, B14.B8, B14.B7, B14.B6,
                                                B14.B5, B14.B, B14.P)
PL = P.PL
PART = os.environ.get("BATCH15_PART", "a")
B5.OUT = Path(os.environ.get("BATCH15_OUT") or FOLDER / "corpus.d" / f"99-batch15{PART}.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = dict(B14.PAGES)
B.PAGES.clear()
B.PAGES.update(PAGES)
for M in (B5, B6, B7, B8, B9, B10, B11, B12, B13, B14):
    M.PAGES = PAGES

ALL_ACTS = [a for a in B14.ALL_ACTS if a["slug"] in ("lei-de-custeio-da-seguridade-social",
                                                     "lei-de-beneficios-da-previdencia-social")]
_C, _BN = "lei-de-custeio-da-seguridade-social", "lei-de-beneficios-da-previdencia-social"
PARTS: dict[str, list[str]] = {"a": [_C], "b": [_BN]}
VERIFIED: list[str] = PARTS.get(PART, [])
ENABLED = [s for s in os.environ.get("BATCH15_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
for M in (B7, B8, B9, B10, B11, B12, B13, B14):
    M.ACTS[:] = ACTS
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in B14.ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in B14.ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# batch 14's act-specific tables are keyed by act slug or page and do nothing here; its printed-everywhere lists emptied
B.EXPLAINED.clear()
B13.OPEN_ITEMS.clear()
B9.REPEALS.clear()

# ---------------------------------------------------------------------------------------------------------------
# Medidas Provisórias 905/2019 and 955/2020 (the CLT part's model, clt/parse_clt.py MP_PAIRS / mp_pairs, ported to the
# proc pipeline). MP 905/2019 (DOU 12.11.2019; art. 53 III: its changes to Leis 8.212 and 8.213 in force on publication)
# was revoked by MP 955/2020 (DOU 20.4.2020, in force on publication); MP 955 lapsed on 17.8.2020 (Ato Declaratório 113/
# 2020), so MP 905 had effect again until its own term ended on 18.8.2020 (Ato Declaratório 127/2020). Planalto prints each
# MP 905 wording twice: struck '(Revogada pela Medida Provisória nº 955, de 2020)' + 'Vigência encerrada' for the first
# period, struck '(Vigência encerrada)' for 18.8.2020; each wording MP 905 replaced comes back while MP 955 stood.
P.VIGENCIA_FIXED["mp-905-2019"] = (
    "2019-11-12", "art. 53: 'Esta Medida Provisória entra em vigor: I - noventa dias após a data de sua publicação, quanto "
                  "às alterações promovidas pelo art. 28 nos art. 161, art. 634 e art. 634-A da Consolidação das Leis do "
                  "Trabalho [...]; II - no primeiro dia do quarto mês subsequente [...] quanto à inclusão do art. 4º-B na Lei "
                  "nº 7.998, de 1990 [...]; e III - na data de sua publicação, quanto aos demais dispositivos' (DOU "
                  "12.11.2019); its changes to Leis 8.212 and 8.213 fall under III (its § 1º III: effects 'nas datas "
                  "estabelecidas no caput')")
P.MP_LAPSE.update({
    "mp-955-2020": ("2020-08-18", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 113, de 2020 (DOU "
                                  "20.8.2020): 'teve seu prazo de vigência encerrado no dia 17 de agosto de 2020'; MP "
                                  "905/2019, which it had revoked, had effect again from 18.8.2020"),
    "mp-905-2019": ("2020-08-19", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 127, de 2020 (DOU "
                                  "29.9.2020): 'teve seu prazo de vigência encerrado no dia 18 de agosto de 2020'; the "
                                  "wording it had replaced is back from 19.8.2020"),
})
MP_PAIRS = {"mp-905-2019": "mp-955-2020"}
MP_PAIRS_USED: list[str] = []
_SKIPNOTE = re.compile(r"\(\s*(?:Vide|Vig[êe]ncia|Produ|Regulament|Declarad|Suspens|Execu|Express|Promulga|Convers|Convertid|"
                       r"Mensagem|Texto)", re.I)


def _note_events(p: dict, cx) -> None:
    """the start and end notes of a line with their days (as parse_proc.lifespans reads them; clt keeps them as
    _starts/_ends)"""
    starts, ends = [], []
    for n in p["notes"]:
        if _SKIPNOTE.match(n):
            continue
        law = P.law_key(n, cx.mp.get("_years"))
        if not law:
            continue
        d = P.VIGENCIA_PROVISION.get((law, cx.act, p["unit"]), (None,))[0] or cx.eff.get(law)
        if not d:
            continue
        if P.START_KIND.search(n):
            starts.append((d, law))
        elif P.END_KIND.search(n):
            ends.append((d, law))
    p["_starts"], p["_ends"] = starts, ends


def mp_pairs(paras: list[dict], cx) -> list[str]:
    problems = []
    for m_key, r_key in MP_PAIRS.items():
        if not any(law == m_key for p in paras for _, law in p.get("_starts", []) + p.get("_ends", [])):
            continue
        if m_key not in cx.eff or r_key not in cx.eff or m_key not in cx.lapse_key or r_key not in cx.lapse_key:
            problems.append(f"MP pair {m_key}/{r_key}: dates missing")
            continue
        r_eff = cx.eff[r_key]
        r_lapse, r_fim = P.MP_LAPSE[r_key][0], cx.lapse_key[r_key]
        m_lapse, m_fim = P.MP_LAPSE[m_key][0], cx.lapse_key[m_key]
        first_copies: dict[tuple, str] = {}
        for p in paras:
            s_m = [d for d, law in p["_starts"] if law == m_key]
            e_m = [d for d, law in p["_ends"] if law == m_key]
            e_r = any(law == r_key for _, law in p["_ends"])
            if not (s_m or e_m) or p["state"] == "plain":
                continue
            slot = (p["unit"], p["label"], p["text"])
            p["pinned"], p["mp_pair"] = True, True
            p["gaps"], p["skip"], p["restored"] = [], False, False
            if s_m and e_r:          # MP 905 wording, first period
                p["start"], p["start_law"] = max(s_m), m_key
                p["end"], p["end_law"], p["end_how"] = r_eff, r_key, "mp-pair"
                first_copies[slot] = "made"
                how = "MP 905 wording, to MP 955"
            elif s_m:                # MP 905 wording again on 18.8.2020 (or a single copy: both periods)
                if first_copies.get(slot) == "made":
                    p["start"], p["start_law"] = r_lapse, r_fim
                    how = "MP 905 wording again, 18.8.2020"
                else:
                    p["start"], p["start_law"] = max(s_m), m_key
                    p["gaps"] = [(r_eff, r_lapse, r_key, r_fim)]
                    how = "MP 905 wording, gap while MP 955 stood"
                p["end"], p["end_law"], p["end_how"] = m_lapse, m_fim, "mp-pair"
            elif e_m and e_r:        # wording MP 905 revoked, back while MP 955 stood
                p["end"], p["end_law"], p["end_how"] = r_lapse, r_fim, "mp-pair"
                p["gaps"] = [(min(e_m), r_eff, m_key, r_key)]
                first_copies[slot] = "revoked"
                how = "revoked by MP 905, back while MP 955 stood"
            else:                    # the same wording revoked again on 18.8.2020: never shown, restores after
                if first_copies.get(slot) == "revoked":
                    p["start"], p["start_law"] = r_lapse, r_fim
                    p["end"], p["end_law"], p["end_how"] = m_lapse, m_fim, "mp-pair"
                    p["skip"] = True
                    how = "second copy of a wording MP 905 revoked (left out)"
                else:
                    p["end"], p["end_law"], p["end_how"] = m_lapse, m_fim, "mp-pair"
                    p["gaps"] = [(min(e_m), r_eff, m_key, r_key)]
                    how = "revoked by MP 905, gap while MP 955 stood"
            MP_PAIRS_USED.append(f"{cx.act} {p['unit']} [{p['label']}]: {how}")
        # a wording MP 905 replaced came back while MP 955 stood (parse_proc's successor rule had ended it when MP 905's
        # wording started)
        for i, p in enumerate(paras):
            if p.get("pinned") or p["state"] == "plain" or (p["end"] and p["end_how"] != "successor"):
                continue
            j = P.successor(paras, i)
            if j is None:
                continue
            q = paras[j]
            if q.get("mp_pair") and q["start_law"] == m_key and q["end_law"] == r_key:
                p["end"], p["end_law"], p["end_how"] = r_lapse, r_fim, "mp-pair"
                p["gaps"] = [(q["start"], r_eff, m_key, r_key)]
                p["pinned"] = True
                MP_PAIRS_USED.append(f"{cx.act} {p['unit']} [{p['label']}]: replaced by MP 905, back while MP 955 stood")
    return problems


_lifespans_proc = B._lifespans


def _lifespans_pairs(paras, cx):
    problems = _lifespans_proc(paras, cx)
    for p in paras:
        _note_events(p, cx)
    problems += mp_pairs(paras, cx)
    pinned = {f"{p['unit']} [{p['label']}]" for p in paras if p.get("mp_pair")}
    problems = [x for x in problems if not any(x.startswith(t) and x[len(t):].split(" '")[0] in pinned for t in (
        "restored wording after an open one: ", "no end for struck "))]
    return problems


B._lifespans = _lifespans_pairs


def mp_pairs_decision() -> list[str]:
    if not MP_PAIRS_USED:
        return []
    return ["Medidas Provisórias 905/2019 and 955/2020: MP 905/2019 (DOU 12.11.2019, its changes to this act in force on "
            "publication, art. 53 III) was revoked by MP 955/2020 (DOU 20.4.2020, in force on publication); MP 955 lapsed "
            "on 17.8.2020 (Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 113, de 2020), so MP 905 had "
            "effect again on 18.8.2020, the last day of its own term (Ato Declaratório nº 127, de 2020). Planalto prints "
            "each MP 905 wording twice (struck 'Revogada pela Medida Provisória nº 955, de 2020' for the first period, "
            "struck 'Vigência encerrada' for the second): each stands from 12.11.2019 to 20.4.2020 and again on "
            "18.8.2020, credited to MP 905 and to the end of MP 955's term; the wordings MP 905 replaced or revoked "
            "stand again from 20.4.2020 to 18.8.2020 and from 19.8.2020 (as in the CLT): "
            + "; ".join(dict.fromkeys(MP_PAIRS_USED)) + "."]


# ---------------------------------------------------------------------------------------------------------------
# in-force days and MP fates for the laws these acts' notes cite (each read from the law's own cached page; lapse days
# from the Atos Declaratórios pinned in batch14/sources_batch14.json as ato:*)
P.VIGENCIA_FIXED.update({
    "lei-11457-2007": ("2007-05-02", "art. 51: 'Esta Lei entra em vigor: I - na data de sua publicação, para o disposto nos "
                                     "arts. 40, 41, 47, 48, 49 e 50 desta Lei; II - no primeiro dia útil do segundo mês "
                                     "subseqüente à data de sua publicação, em relação aos demais dispositivos' (DOU "
                                     "19.3.2007): its changes to Leis 8.212 and 8.213 (arts. 2, 17, 32) fall under II, the "
                                     "first business day of May 2007 (1 May is a public holiday): 2.5.2007"),
    "lei-13670-2018": ("2018-05-30", "art. 11: 'Esta Lei entra em vigor: I - no primeiro dia do quarto mês subsequente ao de "
                                     "sua publicação, quanto aos arts. 1º e 2º, e ao inciso II do caput do art. 12; e II - na "
                                     "data de sua publicação, quanto aos demais dispositivos' (DOU 30.5.2018): its changes to "
                                     "Lei 8.212 (arts. 3 and 5) fall under II"),
    "lei-13756-2018": ("2018-12-13", "art. 39: 'Esta Lei entra em vigor: I - após decorridos 180 (cento e oitenta dias) [...] "
                                     "em relação à alteração do art. 18-A da Lei nº 9.615 [...]; e II - na data de sua "
                                     "publicação, em relação aos demais dispositivos' (DOU 13.12.2018): its change to Lei "
                                     "8.212 (art. 36) falls under II"),
    "lei-14784-2023": ("2023-12-28", "art. 7: 'Esta Lei entra em vigor: I - na data de sua publicação, quanto aos arts. 1º, "
                                     "2º, 4º e 5º; e II - no primeiro dia do quarto mês subsequente ao de sua publicação, "
                                     "quanto aos arts. 3º e 6º' (DOU 28.12.2023): its changes to Lei 8.212 (arts. 2 and 4) "
                                     "fall under I"),
    "mp-258-2005": ("2005-08-15", "art. 38: 'Esta Medida Provisória entra em vigor: I - na data de sua publicação, em relação "
                                  "aos arts. 32 e 37; e II - em 15 de agosto de 2005, os demais artigos' (DOU 22.7.2005): its "
                                  "changes to Lei 8.212 (arts. 3, 27 and 39) fall under II"),
})
P.MP_LAPSE.update({
    "mp-252-2005": ("2005-10-14", "Ato Declaratório do Presidente da Mesa do Congresso Nacional of 14.10.2005: 'teve seu "
                                  "prazo de vigência encerrado no dia 13 de outubro do corrente ano'"),
    "mp-258-2005": ("2005-11-19", "Ato Declaratório do Presidente da Mesa do Congresso Nacional of 21.11.2005: 'teve seu "
                                  "prazo de vigência encerrado no dia 18 de novembro do corrente ano'"),
    "mp-793-2017": ("2017-11-29", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 66, de 2017 (DOU "
                                  "7.12.2017): 'teve seu prazo de vigência encerrado no dia 28 de novembro'"),
    "mp-841-2018": ("2018-10-24", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 64, de 2018 (DOU "
                                  "25.10.2018): 'teve seu prazo de vigência encerrado no dia 23 de outubro'"),
    "mp-927-2020": ("2020-07-20", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 92, de 2020 (DOU "
                                  "31.7.2020): 'teve seu prazo de vigência encerrado no dia 19 de julho'"),
    "mp-1110-2022": ("2022-08-08", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 65, de 2022 (DOU "
                                   "19.8.2022): 'teve seu prazo de vigência encerrado no dia 7 de agosto'"),
})
P.MP_PENDING.update({
    "mp-2170-2001": ("Medida Provisória nº 2.170-36, de 23.8.2001 (DOU 24.8.2001, in force on publication; its effects from "
                     "1.1.1999 are retroactive, so its changes are dated by publication), kept in force by Emenda "
                     "Constitucional 32/2001, art. 2; its art. 8 revoked Lei 8.212 art. 60 parágrafo único"),
    "mp-2216-2001": ("Medida Provisória nº 2.216-37, de 31.8.2001 (DOU 1.9.2001, in force on publication), kept in force by "
                     "Emenda Constitucional 32/2001, art. 2; its art. 33 revoked Lei 8.212 arts. 6, 7, 63 to 66, 77, 84 and "
                     "86 and Lei 8.213 arts. 7 and 8. Planalto's notes name this edition only, so the revocations are "
                     "dated by its publication; earlier editions of the chain are not modelled"),
})
EXTRA: list[str] = []
_inner15 = B6.PB5B._write_part5


def _inner(*a):
    B5.EXTRA_DECISIONS.extend(mp_pairs_decision() + EXTRA)
    return _inner15(*a)


B6.PB5B._write_part5 = _inner

SRC = HERE / "sources_batch15.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
