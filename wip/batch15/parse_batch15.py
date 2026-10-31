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
EXTRA: list[str] = []   # decisions added to the part
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
P.COURTS.clear()      # batch 14's Estatuto da Terra record (its decision and law are printed wherever it is set)
P.NOTE_FIX = {}       # batch 14's note corrections are printed in every part

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
    # two notes fused in one parenthesis ('(Revogado pela Medida Provisória nº 905, de 2019 (Revogada pela Medida
    # Provisória nº 955, de 2020))', Lei 8.213 art. 21 IV d)) are read as two
    notes = []
    for n in p["notes"]:
        inner = re.split(r"\s*\((?=Revogad|Reda|Inclu)", n.strip()[1:-1]) if n.count("(") > 1 else []
        notes += [f"({x.strip(' )')})" for x in inner if x.strip()] if len(inner) > 1 else [n]
    for n in notes:
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
            elif e_m and e_r and first_copies.get(slot) != "revoked":   # wording MP 905 revoked, back while MP 955 stood
                p["end"], p["end_law"], p["end_how"] = r_lapse, r_fim, "mp-pair"
                p["gaps"] = [(min(e_m), r_eff, m_key, r_key)]
                first_copies[slot] = "revoked"
                p["mp_role"] = "revoked"
                how = "revoked by MP 905, back while MP 955 stood"
            else:                    # the same wording revoked again on 18.8.2020: never shown, restores after (a second
                # copy whose notes Planalto fused into one parenthesis also names MP 955: Lei 8.213 art. 21 IV d)
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
    "lei-13756-2018": ("2018-12-13", "art. 47: 'Esta Lei entra em vigor: I - após decorridos 180 (cento e oitenta dias) [...] "
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
P.VIGENCIA_FIXED.update({
    "lei-13202-2015": ("2015-12-09", "art. 16: 'Esta Lei entra em vigor: I - a partir de 1º de dezembro de 2015 quanto ao art. 15; "
                                     "II - na data de sua publicação quanto aos demais dispositivos' (DOU 9.12.2015): its "
                                     "changes to Lei 8.212 (arts. 12 and 17) fall under II"),
    "lei-13183-2015": ("2015-11-05", "art. 8: 'Esta Lei entra em vigor: I - em 3 de janeiro de 2016, quanto à redação do art. 16 "
                                     "e do inciso II do § 2º do art. 77 da Lei nº 8.213 [...]; II - em 1º de julho de 2016, "
                                     "quanto à redação do § 5º do art. 29-C da Lei nº 8.213 [...]; III - na data de sua "
                                     "publicação, para os demais dispositivos' (DOU 5.11.2015); the dispositivos of I and II "
                                     "are dated by provision"),
})
P.VIGENCIA_FIXED["lei-12873-2013"] = (
    "2013-10-25", "art. 63: 'Esta Lei entra em vigor: I - no 1º (primeiro) dia do sétimo mês subsequente à data de sua "
                  "publicação, em relação ao art. 32-C da Lei nº 8.212 [...]; II - 90 (noventa) dias após a data de sua "
                  "publicação, em relação: a) aos arts. 71-B e 71-C da Lei nº 8.213 [...]; e III - na data de sua publicação "
                  "quanto aos demais dispositivos, produzindo efeitos a partir de 1º de janeiro de 2014, em relação: a) ao "
                  "inciso VII do § 9º do art. 12, à alínea d do inciso I do § 11 do art. 12, e aos §§ 14 e 15 do art. 12 da Lei "
                  "nº 8.212 [...]; b) ao inciso VII do § 8º do art. 11, à alínea d do inciso I do § 10 do art. 11, aos §§ 12 e 13 "
                  "do art. 11 da Lei nº 8.213 [...]' (DOU 25.10.2013): I and II are dated by provision, III's effect days by "
                  "the effect-days step")
P.VIGENCIA_PROVISION.update({
    ("lei-12873-2013", _C, "art-032-c"): (
        "2014-05-01", "Lei 12.873/2013 art. 63 I: 'no 1º (primeiro) dia do sétimo mês subsequente à data de sua publicação, em "
                      "relação ao art. 32-C da Lei nº 8.212' (DOU 25.10.2013): 1.5.2014"),
})
# ---- Lei 8.213 (part b)
_MP664 = ("art. 5: 'Esta Medida Provisória entra em vigor: I - na data de sua publicação para os seguintes dispositivos: a) §§ 5º "
          "e 6º do art. 60 e § 1º do art. 74 da Lei nº 8.213, de 1991; e b) arts. 2º, 4º e alíneas \"a\" e \"d\" do inciso II "
          "do art. 6º desta Medida Provisória [the revocations of art. 17 § 2º and art. 151]; II - quinze dias a partir da sua "
          "publicação para o § 2º do art. 74 da Lei nº 8.213, de 1991; e III - no primeiro dia do terceiro mês subseqüente à "
          "data de publicação desta Medida Provisória quanto aos demais dispositivos' (DOU 30.12.2014)")
P.VIGENCIA_FIXED.update({
    "lei-10877-2004": ("2004-06-07", "art. 2: 'Esta Lei entra em vigor na data da sua publicação' (DOU 7.6.2004; the page "
                                     "breaks the clause after 'publi', so it is set here)"),
    "mp-664-2014": ("2015-03-01", _MP664 + ": its other changes to Lei 8.213 fall under III, 1.3.2015; I and II by "
                                           "provision"),
    "lei-13135-2015": ("2015-06-18", "art. 6: 'Esta Lei entra em vigor em: I - 180 (cento e oitenta) dias a partir de sua "
                                     "publicação, quanto à inclusão de pessoas com deficiência grave entre os dependentes dos "
                                     "segurados do [RGPS] e do [RPPS] previstos na Lei nº 8.112 [...]; II - 2 (dois) anos para a "
                                     "nova redação: a) do art. 16, incisos I e III, e do art. 77, § 2º, inciso IV, da Lei nº "
                                     "8.213 [...], em relação às pessoas com deficiência intelectual ou mental; [...] III - na "
                                     "data de sua publicação, para os demais dispositivos' (DOU 18.6.2015); II by provision"),
    "lei-13876-2019": ("2019-09-23", "art. 5: 'Esta Lei entra em vigor: I - quanto ao art. 3º, a partir do dia 1º de janeiro "
                                     "de 2020; II - quanto aos demais dispositivos, na data de sua publicação' (DOU 23.9.2019): "
                                     "its change to Lei 8.213 (art. 4, art. 126) falls under II"),
    "mp-1355-2026": ("2026-05-04", "art. 27: 'Esta Medida Provisória entra em vigor: I - quinze dias após a data de sua "
                                   "publicação, quanto aos art. 19 e art. 23; e II - na data de sua publicação, quanto aos "
                                   "demais dispositivos' (DOU 4.5.2026, edição extra): its change to Lei 8.213 (art. 22, art. "
                                   "115) falls under II"),
})
P.VIGENCIA_PROVISION.update({
    **{("mp-664-2014", _BN, u): ("2014-12-30", "Medida Provisória 664/2014 " + _MP664 + ": on publication for "
                                 + what) for u, what in (("art-017", "the revocation of art. 17 § 2º (art. 6 II a)"),
                                                         ("art-151", "the revocation of art. 151 (art. 6 II d)"))},
    ("lei-12873-2013", _BN, "art-071-b"): ("2014-01-23", "Lei 12.873/2013 art. 63 II: '90 (noventa) dias após a data de sua "
                                                         "publicação, em relação: a) aos arts. 71-B e 71-C da Lei nº 8.213' "
                                                         "(DOU 25.10.2013 + 90 days)"),
    ("lei-12873-2013", _BN, "art-071-c"): ("2014-01-23", "Lei 12.873/2013 art. 63 II (as for art. 71-B)"),
    ("lei-13183-2015", _BN, "art-016"): ("2016-01-03", "Lei 13.183/2015 art. 8 I: 'em 3 de janeiro de 2016, quanto à redação "
                                                       "do art. 16 [...] da Lei nº 8.213'"),
})
P.MP_LAPSE.update({
    "mp-739-2016": ("2016-11-05", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 58, de 2016 (DOU "
                                  "8.11.2016): 'teve seu prazo de vigência encerrado no dia 4 de novembro'"),
    "mp-891-2019": ("2019-12-04", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 67, de 2019 (DOU "
                                  "5.12.2019): 'teve seu prazo de vigência encerrado no dia 3 de dezembro'"),
    "mp-1355-2026": ("2026-09-01", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 89, de 2026 (DOU "
                                   "8.9.2026): 'teve seu prazo de vigência encerrado no dia 31 de agosto de 2026'"),
})
P.NOTE_FIX.update({} if _BN not in ENABLED else {
    f"({kind} pela MPv nº 404, de 2007)": (f"({kind} pela Medida Provisória nº 404, de 2007)",
                                         f"Lei 8.213: notes '({kind} pela MPv nº 404, de 2007)' read as Medida Provisória nº 404")
    for kind in ("Redação dada", "Incluído")})
P.NOTE_FIX.update({} if _BN not in ENABLED else {
    f"({kind} pela Lei nº 11,718, de 2008)": (f"({kind} pela Lei nº 11.718, de 2008)",
                                            f"Lei 8.213: notes '({kind} pela Lei nº 11,718, de 2008)' (comma) read as Lei nº "
                                            f"11.718")
    for kind in ("Redação dada", "Incluído")})
P.VIGENCIA_FIXED["lei-13137-2015"] = (
    "2015-06-22", "art. 26 VII: the provisions not named in its incisos I to VI, which include art. 7 (Lei 8.212 art. 22 § "
                  "14), in force 'na data de sua publicação' (DOU 22.6.2015, edição extra)")
P.VIGENCIA_FIXED["lei-11098-2005"] = (
    "2005-01-14", "art. 14: 'Esta Lei entra em vigor: I - a partir da data de publicação do ato referido no inciso I do art. "
                  "8º, para os arts. 1º, 2º, 3º e 4º; e II - a partir de 5 de outubro de 2004, para os demais artigos' (DOU "
                  "14.1.2005). The act of art. 8 I (creation of the Secretaria da Receita Previdenciária) is Decreto 5.256 of "
                  "27.10.2004 (DOU 28.10.2004, its Estrutura Regimental lists the Secretaria), published before the law, so "
                  "art. 4 (the new wording of Lei 8.212 art. 39 caput) is in force from the law's own publication. Medida "
                  "Provisória 222/2004, which the law converted and which had made the same change, is not noted on "
                  "Planalto's page and is not modelled")

# ---------------------------------------------------------------------------------------------------------------
# page fixes (paragraphs wrapper): footnote markers, misprints, a note's closing period left after the text
TEXT_FIX: list[tuple[str, str, str, str]] = [
    ("l8212", "Da Contribuição do Produtor Rural e do Pescado}", "Da Contribuição do Produtor Rural e do Pescador",
     "Lei 8.212 Capítulo VI heading (Lei 8.398/1992): Planalto's annotated page misprints 'Pescado}'; the consolidated page "
     "reads 'DO PESCADOR'"),
    ("l8212", "TÍTULO VII l", "TÍTULO VII",
     "Lei 8.212 Título VII heading: the annotated page prints a stray 'l' after 'TÍTULO VII' (the consolidated page does not)"),
    ("l8212", "V, X e XIII do caput, até o dia útil imediatamente anterior$",
     "V, X e XIII do caput, até o dia útil imediatamente anterior.",
     "Lei 8.212 art. 30 § 2º II (Lei 13.202/2015): the annotated page drops the closing period, which Lei 13.202's own text "
     "and the consolidated page print"),
]
TEXT_FIX_USED: list[str] = []
LETTER_ARTS: list[str] = []
CENTERED: dict[str, int] = {}
TABLES: dict[str, int] = {}
CELL = chr(0x2060)   # marks table cells while the page is read
CELLS_BACK: list[str] = []
FOOTNOTES_DROPPED: dict[str, int] = {}
NOTE_DOT: dict[str, int] = {}
_paragraphs15 = P.paragraphs
_SUPNUM = re.compile(r"<sup\b(?:(?!</sup>).)*?</sup>", re.S | re.I)


def _supnum(m):
    s = re.sub(r"<[^>]+>|&nbsp;|\s", "", m.group(0))
    return "" if re.fullmatch(r"\d{1,2}", s) else m.group(0)


# Lei 8.212 arts. 20, 26, 36, 68 and 94: the annotated page prints only later wordings, not the text of 1991; that text is
# read from Planalto's page of the act as enacted (L8212orig.htm, pinned ctx:l8212-original), which strikes the 1991
# wording above the later one, and placed struck above the first wording the annotated page prints. Art. 20 also: the
# rate table Lei 9.032/1995 gave (on the original page) stood until Lei 9.129/1995 gave the table printed today.
ORIGINAL_ARTS = ("art-020", "art-026", "art-036", "art-068", "art-094")
ORIGINAL_USED: list[str] = []


def _insert_original(out, digits):
    keep = B8.CURRENT_PAGE[0]
    B8.CURRENT_PAGE[0] = "l8212-original"
    orig, _ = paragraphs(P.decode(P.raw("ctx:l8212-original")[0]), digits)
    B8.CURRENT_PAGE[0] = keep
    # art. 6 § 10: the annotated page prints only '§ 10 . (Revogado pela Lei n° 9.032, de 28.4.95)'; its 1991 text is on the
    # original page
    for p in out:
        if p["unit"] == "art-006" and p["label"] == "§ 10" and re.fullmatch(r"§ 10\s*\.?", p["text"]):
            src = next(q for q in orig if q["unit"] == "art-006" and q["label"] == "§ 10")
            p["text"] = p["struck_text"] = src["text"]
            ORIGINAL_USED.append("art-006 § 10 (text of a line printed as its bare label)")
    for unit in ORIGINAL_ARTS:
        ou = [p for p in orig if p["unit"] == unit and not p["heading"]]
        if unit == "art-094":   # the original page prints the 1991 wording of art. 94 unstruck: its caput only
            first = [ou[0]]
        else:                   # the struck lines above the first unstruck caput
            k = next((i for i, p in enumerate(ou) if i and p["label"].startswith("Art.") and p["state"] == "plain"),
                     len(ou))
            first = [p for p in ou[:k] if p["state"] != "plain"]
            if unit == "art-020":   # and its 1991 parágrafo único, struck below Lei 9.032's caput and table
                first += [p for p in ou[k:] if p["label"] == "Parágrafo único" and p["state"] != "plain"]
        at = next(i for i, p in enumerate(out) if p["unit"] == unit and not p["heading"])
        new = []
        for p in first:
            q = {**p, "state": "struck", "plain_text": "", "struck_text": p["text"], "orig_insert": True,
                 "notes": [n for n in p["notes"] if unit == "art-036"]}
            new.append(q)
        out[at:at] = new
        ORIGINAL_USED.append(f"{unit} ({len(new)} lines)")
        if unit == "art-020":   # Lei 9.032's table after the caput it gave
            k = next(i for i, p in enumerate(ou) if i and p["label"].startswith("Art.") and p["state"] == "plain")
            t9032 = []
            for p in ou[k + 1:]:
                if p["label"]:
                    break
                t9032.append({**p, "state": "struck", "plain_text": "", "struck_text": p["text"], "orig_insert": True,
                              "t9032": True, "notes": []})
            cap = next(i for i, p in enumerate(out) if p["unit"] == unit and p["state"] == "plain"
                       and p["label"].startswith("Art."))
            out[cap + 1:cap + 1] = t9032


def paragraphs(html, digits):
    page = B8.CURRENT_PAGE[0]
    if "href=\"#ne" in html or page == "l8212":
        # l8212cons.htm keeps the numbered footnote markers of a 1998 edition ('e) as importâncias: <sup>14</sup>'); the
        # footnotes themselves (on Medidas Provisórias then pending) are printed after the signature, outside the act
        n0 = len(_SUPNUM.findall(html))
        html = _SUPNUM.sub(_supnum, html)
        FOOTNOTES_DROPPED[page] = n0 - len(_SUPNUM.findall(html))
    # l8212cons.htm sets each Título / Capítulo name as a bare <p> inside <center> (only the 'TÍTULO I' line itself is
    # centred text): give those paragraphs the centred alignment they are displayed with, so they are read as heading
    # lines, not as marginal headings of the next article
    n0 = len(re.findall(r"<center\b", html, re.I))
    def _centre(m):
        txt = re.sub(r"<[^>]+>|&nbsp;|\s", " ", m.group(0)).strip()
        if re.match(r"(TÍTULO|CAPÍTULO|Seção)\s", txt):
            return re.sub(r"<p(?=[\s>])(?![^>]*\balign=)", '<p align="center"', m.group(0), flags=re.I)

        def caps(q):   # in a centred block that also holds body text or a table, only all-capitals names
            body = re.sub(r"<[^>]+>|&nbsp;|\s", " ", q.group(0)).strip()
            if body and re.search(r"[A-ZÀ-Ý]{4}", body) and not re.search(r"[a-zß-ÿ]", body):
                return re.sub(r"^<p(?=[\s>])", '<p align="center"', q.group(0), flags=re.I)
            return q.group(0)
        return re.sub(r"<p(?=[\s>])(?![^>]*\balign=)[^>]*>.*?</p>", caps, m.group(0), flags=re.S | re.I)
    html = re.sub(r"<center\b.*?</center>", _centre, html, flags=re.S | re.I)
    # tables inside the act (Lei 8.212 arts. 20, 29, 32; Lei 8.213 arts. 77, 142): Planalto centres their cells, which the
    # shared reader takes for heading lines (filed under 'titulos'); their cells are lines of the article they are
    # printed in, one cell per line (as in the CLT's art. 580)
    body = re.search(r"Art\.\s*1[º°o]", html)
    if body:
        head, rest_html = html[:body.start()], html[body.start():]

        def _tab(m):
            if re.search(r"TÍTULO|CAPÍTULO|Seção|Brasília", re.sub(r"<[^>]+>", " ", m.group(0))):
                return m.group(0)
            TABLES[page] = TABLES.get(page, 0) + 1
            t = re.sub(r"(<(?:p|td|div|font|span)\b[^>]*?)\s+align=\"?center\"?", r"\1", m.group(0), flags=re.I)
            t = re.sub(r"</?center\b[^>]*>", " ", t, flags=re.I)
            t = re.sub(r"(<(?:p|td|div)\b[^>]*?)\bstyle=\"[^\"]*text-align:\s*center[^\"]*\"", r"\1", t, flags=re.I)
            return re.sub(r"(<(?:td|p)\b[^>]*>)", lambda c: c.group(1) + CELL, t, flags=re.I)   # cell marker, taken out below
        html = head + re.sub(r"<table\b.*?</table>", _tab, rest_html, flags=re.S | re.I)
    if n0:
        CENTERED[page] = n0
    out, rest = _paragraphs15(html, digits)
    # table cells: the marker comes out; a cell the marginal-heading rule moved into the next article (no label, no closing
    # punctuation: Lei 8.213 art. 142's table) goes back to the article it is printed in
    for i, p in enumerate(out):
        if any(CELL in (p.get(f) or "") for f in ("text", "struck_text", "plain_text")):
            for f in ("text", "struck_text", "plain_text"):
                if isinstance(p.get(f), str):
                    p[f] = P.norm(p[f].replace(CELL, ""))
            if p["label"] == "rubrica":
                prev = next((q for q in reversed(out[:i]) if not q["heading"] and q["label"] != "rubrica"), None)
                if prev is not None:
                    p["unit"], p["label"] = prev["unit"], ""
                    CELLS_BACK.append(f"{page} {p['unit']}")
    out[:] = [p for p in out if p["text"] or p["notes"] or p.get("label") not in ("", "rubrica")]
    for p in out:   # a cell of a struck table whose unstruck part is only spacing (Lei 8.213 art. 77, MP 664's table)
        if p["state"] == "mixed" and not (p.get("plain_text") or "").strip(" -–"):
            p["state"] = "struck"
    # 'Art. 22A.', 'Art. 22B.', 'Art. 25A.' (Leis 10.256/2001, 10.666/2003: Planalto prints the letter without a hyphen):
    # the shared reader keeps them in the files of arts. 22 and 25; each is its own article (art-022-a, ...)
    cur = None
    for p in out:
        m = re.match(r"^Art\.\s*(\d+)-?([A-Z])\.", p["text"]) if not p["heading"] else None
        if m and p["unit"] == f"art-{int(m.group(1)):0{digits}d}":
            cur = (p["unit"], f"{p['unit']}-{m.group(2).lower()}")
            p["label"] = f"Art. {m.group(1)}-{m.group(2)}"
            LETTER_ARTS.append(f"{page} {cur[1]}")
        elif p["heading"] or (cur and p["unit"] != cur[0]) or re.match(r"^Art\.\s*\d", p["text"]):
            cur = None
        if cur and p["unit"] == cur[0]:
            p["unit"] = cur[1]
    # Planalto's editorial line under Lei 8.212 art. 20's table ('(Valores e alíquotas dados pela Lei nº 9.129, de
    # 20.11.95)'), read as a heading line: it is a note (the table's dates are set in _art20)
    out[:] = [p for p in out if not (p["heading"] and re.fullmatch(r"\(Valores e alíquotas dados pela [^)]*\)", p["text"]))]
    if page == "l8212":
        _insert_original(out, digits)
    for p in out:
        for pg, wrong, right, why in TEXT_FIX:
            if pg != page:
                continue
            if wrong.endswith("$") and p["text"].endswith(wrong[:-1]):
                p["text"] = p["text"][:-len(wrong) + 1] + right
                TEXT_FIX_USED.append(why)
            elif not wrong.endswith("$") and wrong in p["text"]:
                p["text"] = p["text"].replace(wrong, right)
                if p.get("label") == wrong:
                    p["label"] = right
                TEXT_FIX_USED.append(why)
        # '(Revogado o caput pela Lei nº 9.639, de 25.5.98.)' (Lei 8.212 art. 93): the period inside the parenthesis kept the
        # note in the text; it is the caput's revocation note
        m = re.search(r"\.?\s*\((Revogad[oa]) o caput (pela [^()]*?)\.?\)$", p["text"])
        if m:
            p["text"] = p["text"][:m.start()].rstrip(".") + "."
            p["notes"] = p["notes"] + [f"({m.group(1)} {m.group(2)})"]
            TEXT_FIX_USED.append("Lei 8.212 art. 93: the note '(Revogado o caput pela Lei nº 9.639, de 25.5.98.)', whose "
                                 "inner period kept it in the text, is read as the caput's revocation note")
        # '...salário-maternidade; (Redação dada pela Lei nº 9.528, de 10.12.97).': the period closes the note, not the
        # text ('...;.' once the note is lifted out)
        if p["notes"] and re.search(r"[;:,]\s*\.$", p["text"]):
            p["text"] = re.sub(r"\s*\.$", "", p["text"])
            NOTE_DOT[page] = NOTE_DOT.get(page, 0) + 1
    return out, rest


P.paragraphs = B.paragraphs = paragraphs

# ---------------------------------------------------------------------------------------------------------------
# hand-set life spans (B8.SPAN_FIX: (act, unit, label, text start, n-th such line) -> fields, why)
_MP258_GAP = ("2005-08-15", "2005-11-19", "mp-258-2005", "mp-258-2005-fim")
_W26 = ("Lei 8.212 art. 26: Planalto prints the 1992 wording (Lei 8.436/1992) of the caput and §§ 1º-3º, then Medida "
        "Provisória 841/2018's wording (lapsed 23.10.2018), then the 1992 wording again (in force again from 24.10.2018 to "
        "Lei 13.756/2018, 13.12.2018); the second copy of §§ 1º-3º starts on 24.10.2018, like the caput's")
_W39 = ("Lei 8.212 art. 39 caput: Lei 8.620/1993's wording ends when Lei 11.098/2005's starts (14.1.2005, see its in-force "
        "day); Medida Provisória 258/2005 replaced that wording from 15.8.2005 until it lapsed (18.11.2005), so Lei "
        "11.098's wording stands from 14.1.2005 to Lei 11.457/2007 (2.5.2007) except from 15.8.2005 to 18.11.2005 "
        "(Planalto prints MP 258's wording above Lei 11.098's)")
_W44 = ("Lei 8.212 art. 44: Planalto prints the 1991 wording, Medida Provisória 258/2005's wording (lapsed 18.11.2005), "
        "the 1991 wording again and Lei 8.620/1993's wording (revoked by Lei 11.501/2007). The wording in force when MP 258 "
        "came and again after its lapse was Lei 8.620's, so it stands from 6.1.1993 to 12.7.2007 except from 15.8.2005 to "
        "18.11.2005, and the second copy of the 1991 wording (a reprint, no note) is left out")
_W50 = ("Lei 8.212 art. 50 caput: Planalto prints Lei 9.476/1997's wording struck (replaced by Medida Provisória 449/2008, "
        "4.12.2008), then MP 449's caput and §§ 1º-2º, then the 1991 wording, Lei 8.620/1993's, and Lei 9.476's wording "
        "again unstruck: Lei 11.941/2009, MP 449's conversion, did not take up MP 449's art. 50, so Lei 9.476's wording is "
        "in force again from 28.5.2009. Spans: 1991 wording 25.7.1991-6.1.1993; Lei 8.620's 6.1.1993-23.7.1997; Lei "
        "9.476's 23.7.1997-4.12.2008 and from 28.5.2009 (credited to Lei 11.941)")
_W32A = ("Lei 8.212 art. 32-A § 3º II (Lei 11.941/2009): Planalto strikes only the dash after the label ('II – R$ 500,00 "
         "...'), which made the line read as partly struck and undated; it is the inciso in force from 28.5.2009")
_C = "lei-de-custeio-da-seguridade-social"
B8.SPAN_FIX += [
    *[((_C, "art-026", lab, pre, 1), {"start": "2018-10-24", "start_law": "mp-841-2018-fim", "restored": True}, _W26)
      for lab, pre in [("§ 1º", "§ 1º Consideram-se concursos"), ("§ 2º", "§ 2º Para efeito do disposto"),
                       ("§ 3º", "§ 3º Durante a vigência dos contratos")]],
    ((_C, "art-039", "Art. 39", "Art. 39. O débito original atualizado monetariamente, a multa variável e os juros de mora "
                                "incidentes sobre o mesmo", 0),
     {"end": "2005-01-14", "end_law": "lei-11098-2005", "end_how": "successor"}, _W39),
    ((_C, "art-039", "Art. 39", "Art. 39. O débito original atualizado monetariamente, a multa variável e os juros de mora "
                                "sobre ele incidentes", 0),
     {"start": "2005-01-14", "start_law": "lei-11098-2005", "restored": False, "end": "2007-05-02",
      "end_law": "lei-11457-2007", "end_how": "successor", "gaps": [_MP258_GAP]}, _W39),
    ((_C, "art-044", "Art. 44", "Art. 44. A autoridade judiciária exigirá a comprovação", 0),
     {"end": "1993-01-06", "end_law": "lei-8620-1993", "end_how": "successor"}, _W44),
    ((_C, "art-044", "Art. 44", "Art. 44. A autoridade judiciária exigirá a comprovação", 1),
     {"skip": True, "end_how": "duplicate"}, _W44),
    ((_C, "art-044", "Art. 44", "Art. 44. A autoridade judiciária velará pelo fiel cumprimento", 0),
     {"start": "1993-01-06", "start_law": "lei-8620-1993", "end": "2007-07-12", "end_law": "lei-11501-2007",
      "end_how": "note", "gaps": [_MP258_GAP]}, _W44),
    ((_C, "art-050", "Art. 50", "Art. 50. Para fins de fiscalização do INSS", 0),
     {"start": "1997-07-23", "start_law": "lei-9476-1997", "end": "2008-12-04", "end_law": "mp-449-2008",
      "end_how": "successor"}, _W50),
    ((_C, "art-050", "Art. 50", "Art. 50. É obrigatória a apresentação", 0),
     {"start": "1991-07-25", "start_law": None, "end": "1993-01-06", "end_law": "lei-8620-1993", "end_how": "successor",
      "restored": False}, _W50),
    ((_C, "art-050", "Art. 50", "Art. 50. É obrigatória a apresentação", 1),
     {"start": "1993-01-06", "start_law": "lei-8620-1993", "end": "1997-07-23", "end_law": "lei-9476-1997",
      "end_how": "successor"}, _W50),
    ((_C, "art-050", "Art. 50", "Art. 50. Para fins de fiscalização do INSS", 1),
     {"start": "2009-05-28", "start_law": "lei-11941-2009", "restored": True}, _W50),
    ((_C, "art-032-a", "II -", "II - R$ 500,00", 1),
     {"start": "2009-05-28", "start_law": "lei-11941-2009", "end": None, "end_law": None, "end_how": None, "skip": False,
      "state": "plain"}, _W32A),
]
_W89 = ("Lei 8.212 art. 89: Planalto prints Lei 9.032/1995's caput and §§ 1º-7º, then Lei 9.129/1995's caput ('Redação dada "
        "ao caput e parágrafos pela Lei nº 9.129, de 20.11.95') followed by its §§ 1º-7º without notes; those second §§ 1º-7º "
        "are Lei 9.129's wording and start on 21.11.1995 (they had been read as the 1991 text)")
_W25 = ("Lei 8.212 art. 25 § 12: vetoed in Lei 13.606/2018 (DOU 10.1.2018); Congress overrode the veto and the part was "
        "promulgated on 17.4.2018 (DOU 18.4.2018, printed at the end of Lei 13.606's page: 'promulgo [...] as seguintes "
        "partes vetadas'), so the '§ 12. (VETADO).' line stands from 10.1.2018 to 18.4.2018 and the promulgated § 12 from "
        "18.4.2018, credited to Lei 13.606")
_W32C = ("Lei 8.212 art. 32-C § 3º I-III: Medidas Provisórias 1.107/2022 (DOU 18.3.2022, converted into Lei 14.438/2022, "
         "25.8.2022) and 1.110/2022 (DOU 28.3.2022, lapsed 7.8.2022) gave § 3º the same three incisos; Planalto prints MP "
         "1.107's, then MP 1.110's, then MP 1.107's again. MP 1.107's incisos stand from 18.3.2022 to 28.3.2022 and again "
         "from 8.8.2022 to Lei 14.438 (25.8.2022), MP 1.110's in between")
B8.SPAN_FIX += [
    *[((_C, "art-089", lab, lab, 1), {"start": "1995-11-21", "start_law": "lei-9129-1995", "restored": False}, _W89)
      for lab in ("§ 1º", "§ 2º", "§ 3º", "§ 4º", "§ 5º", "§ 6º", "§ 7º")],
    *[((_C, "art-032-c", lab, pre, n), f, _W32C) for lab, pre in [
        ("I -", "I - as contribuições previstas nos incisos X, XII e XIII do caput do art. 30;"),
        ("II -", "II - os valores referentes ao FGTS; e"),
        ("III -", "III - os encargos trabalhistas sob a sua responsabilidade.")]
      for n, f in [(0, {"end": "2022-03-28", "end_law": "mp-1110-2022", "end_how": "successor"}),
                   (2, {"start": "2022-08-08", "start_law": "mp-1110-2022-fim", "restored": True, "end": "2022-08-25",
                        "end_law": "lei-14438-2022", "end_how": "conversion"})]],
    *[((_C, "art-068", lab, lab, 0), {"start": "1994-04-16", "start_law": "lei-8870-1994"},
       "Lei 8.212 art. 68 §§ 1º-2º: printed without notes on the annotated page; Planalto's page of the act as enacted notes "
       "them 'Incluído pela Lei nº 8.870, de 1994' (the 1991 article had no paragraphs)") for lab in ("§ 1º", "§ 2º")],
    ((_C, "art-025", "§ 12", "§ 12. (VETADO)", 0),
     {"end": "2018-04-18", "end_law": "lei-13606-2018", "end_how": "promulgation"}, _W25),
    ((_C, "art-025", "§ 12", "§ 12. Não integra a base de cálculo", 0),
     {"start": "2018-04-18", "start_law": "lei-13606-2018", "promulgated": True}, _W25),
]
# Resoluções do Senado Federal suspending dispositivos the STF declared unconstitutional (CF art. 52 X): Planalto strikes
# the dispositivo and notes '(Execução suspensa pela Resolução do Senado Federal nº N, de AAAA)'; each page pinned ctx:rsf-*
if _C in ENABLED:
    P.COURTS.update({
        "rsf-26-2005": {
            "label": "Resolução do Senado Federal nº 26, de 2005", "kind": "law", "enacted": "2005-06-21",
            "published": "2005-06-22",
            "title": "Suspende a execução da alínea \"h\" do inciso I do art. 12 da Lei Federal nº 8.212, de 24 de julho de "
                     "1991, acrescentada pelo § 1º do art. 13 da Lei Federal nº 9.506, de 30 de outubro de 1997.",
            "url": PL + "_Ato2004-2006/2005/Congresso/ResSF26-05.htm", "from": "2005-06-22",
            "case": r"Resolu[çc][ãa]o\s+do\s+Senado\s+Federal\s+n[º°]\s*26,\s*de\s*2005",
            "where": [(_C, "art-012", "h)")],
            "why": "Resolução do Senado Federal nº 26, de 21.6.2005 (DOU 22.6.2005), art. 1: 'É suspensa a execução da alínea "
                   "\"h\" do inciso I do art. 12 da Lei Federal nº 8.212 [...] em virtude de declaração de "
                   "inconstitucionalidade em decisão definitiva do Supremo Tribunal Federal, nos autos do Recurso "
                   "Extraordinário nº 351.717-1'; art. 2: in force on publication. Lei 8.212 art. 12 I h) (added by Lei "
                   "9.506/1997) ends on 22.6.2005, credited to the resolution (kind law: a Senate act)"},
        "rsf-10-2016": {
            "label": "Resolução do Senado Federal nº 10, de 2016", "kind": "law", "enacted": "2016-03-30",
            "published": "2016-03-31",
            "title": "Suspende, nos termos do art. 52, inciso X, da Constituição Federal, a execução do inciso IV do art. 22 da "
                     "Lei nº 8.212, de 24 de julho de 1991.",
            "url": PL + "_Ato2015-2018/2016/Congresso/RSF%2010.htm", "from": "2016-03-31",
            "case": r"Resolu[çc][ãa]o\s+do\s+Senado\s+Federal\s+n[º°]\s*10,\s*de\s*2016",
            "where": [(_C, "art-022", "IV -")],
            "why": "Resolução do Senado Federal nº 10, de 30.3.2016 (DOU 31.3.2016), art. 1: 'É suspensa, nos termos do art. "
                   "52, inciso X, da Constituição Federal, a execução do inciso IV do art. 22 da Lei nº 8.212 [...] declarado "
                   "inconstitucional por decisão definitiva proferida pelo Supremo Tribunal Federal nos autos do Recurso "
                   "Extraordinário nº 595.838'; art. 2: in force on publication. Lei 8.212 art. 22 IV (added by Lei "
                   "9.876/1999) ends on 31.3.2016, credited to the resolution (kind law: a Senate act)"},
    })
    P.COURTS["rsf-15-2017"] = {
        "label": "Resolução do Senado Federal nº 15, de 2017", "kind": "law", "enacted": "2017-09-12",
        "published": "2017-09-13",
        "title": "Suspende, nos termos do art. 52, inciso X, da Constituição Federal, a execução do inciso VII do art. 12 da Lei "
                 "nº 8.212, de 24 de julho de 1991, e a execução do art. 1º da Lei nº 8.540, de 22 de dezembro de 1992, que deu "
                 "nova redação ao art. 12, inciso V, ao art. 25, incisos I e II, e ao art. 30, inciso IV, da Lei nº 8.212, de 24 "
                 "de julho de 1991, todos com a redação atualizada até a Lei nº 9.528, de 10 de dezembro de 1997.",
        "url": PL + "_Ato2015-2018/2017/Congresso/RSF15.htm", "from": "2017-09-13",
        "case": r"Resolu[çc][ãa]o\s+do\s+Senado\s+Federal\s+n[º°]\s*15,\s*de\s*2017",
        "where": [(_C, "art-025", "I -")],
        "why": "Resolução do Senado Federal nº 15, de 12.9.2017 (DOU 13.9.2017), art. 1: 'É suspensa [...] a execução do "
               "inciso VII do art. 12 da Lei nº 8.212 [...] e a execução do art. 1º da Lei nº 8.540 [...], que deu nova redação "
               "ao art. 12, inciso V, ao art. 25, incisos I e II, e ao art. 30, inciso IV, da Lei nº 8.212 [...], todos com a "
               "redação atualizada até a Lei nº 9.528, de 10 de dezembro de 1997, declarados inconstitucionais [...] nos autos "
               "do Recurso Extraordinário nº 363.852'; art. 2: in force on publication. Planalto notes the suspension beside "
               "the struck wordings of art. 12 V (and its alíneas), art. 12 VII and art. 25 I. Of these only art. 25 I (Lei "
               "9.528/1997's wording, '2% da receita bruta [...]') was still the text in 2017: it ends on 13.9.2017, credited "
               "to the resolution, and the inciso is absent until Lei 13.606/2018 gave it a new wording (10.1.2018); the "
               "others had been replaced by Leis 9.876/1999 and 11.718/2008 and are unchanged. Planalto prints no note at "
               "art. 25 II, which is kept. Medida Provisória 793/2017's wording of art. 25 I ('1,2%'; DOU 1.8.2017) was to "
               "produce effects from 1.1.2018 (its art. 14 I, for its art. 12) and the MP lapsed on 28.11.2017, so it never "
               "applied and is left out (as the effect-day rule requires)"}
    B8.SPAN_FIX.append(((_C, "art-025", "I -", "I - 1,2% (um inteiro e dois décimos por cento)", 0),
                        {"skip": True, "end_how": "never-in-effect"},
                        "Lei 8.212 art. 25 I: Medida Provisória 793/2017's wording never took effect (see the Resolução do "
                        "Senado Federal nº 15, de 2017 decision)"))
# ---- Lei 8.213 (part b)
_W664 = ("Lei 8.213: Medida Provisória 664/2014 (DOU 30.12.2014) put its changes in force on three days (art. 5): art. 60 "
         "§§ 5º-6º and art. 74 § 1º on publication (30.12.2014), art. 74 § 2º fifteen days after it (14.1.2015), the rest on "
         "1.3.2015; all of them ended with its conversion into Lei 13.135/2015 (18.6.2015)")
_PUB664 = {"start": "2014-12-30", "start_law": "mp-664-2014", "by_provision": True}
_W13135 = ("Lei 8.213: Lei 13.135/2015 art. 6 II gave '2 (dois) anos' (to 19.6.2017) to 'a nova redação: a) do art. 16, "
           "incisos I e III, e do art. 77, § 2º, inciso IV [...] em relação às pessoas com deficiência intelectual ou mental'. "
           "Art. 77 § 2º IV (its wording, still in force) starts on 19.6.2017; its wording of art. 16 III was replaced by Lei "
           "13.146/2015 (in force 3.1.2016) before that day and is left out (it never took effect)")
_W77II = ("Lei 8.213 art. 77 § 2º II: Lei 13.146/2015 (in force 3.1.2016) and Lei 13.183/2015 (its art. 8 I: 'em 3 de janeiro "
          "de 2016, quanto à redação [...] do inciso II do § 2º do art. 77') both gave the inciso a wording from 3.1.2016; "
          "the later law's wording (Lei 13.183's) is the one in force from that day, and Lei 13.146's never applied (left "
          "out)")
_BN = "lei-de-beneficios-da-previdencia-social"
B8.SPAN_FIX += [
    *[((_BN, "art-060", lab, pre, 0), _PUB664, _W664) for lab, pre in [
        ("§ 5º", "§ 5º O INSS a seu critério"), ("I -", "I - por convênio ou acordo de cooperação técnica"),
        ("II -", "II - por termo de cooperação técnica"), ("§ 6º", "§ 6º Não será devido auxílio-doença")]],
    ((_BN, "art-074", "§ 1º", "§ 1º Não terá direito à pensão por morte o condenado", 0), _PUB664, _W664),
    *[((_BN, "art-074", lab, pre, 0), {"start": "2015-01-14", "start_law": "mp-664-2014", "by_provision": True}, _W664) for lab, pre in [
        ("§ 2º", "§ 2º O cônjuge, companheiro ou companheira não terá direito"),
        ("I -", "I - o óbito do segurado seja decorrente de acidente"), ("II -", "II - o cônjuge, o companheiro ou a companheira for considerado incapa")]],
    ((_BN, "art-077", "IV -", "IV - para filho ou irmão que tenha deficiência intelectual", 0),
     {"start": "2017-06-19", "start_law": "lei-13135-2015"}, _W13135),
    ((_BN, "art-016", "III -", "III - o irmão de qualquer condição menor de 21", 0),
     {"skip": True, "end_how": "never-in-effect"}, _W13135),
    ((_BN, "art-077", "II -", "II - para filho, pessoa a ele equiparada ou irmão", 0),
     {"end": "2016-01-03", "end_law": "lei-13183-2015", "end_how": "successor"}, _W77II),
    ((_BN, "art-077", "II -", "II - para o filho, a pessoa a ele equiparada ou o irmão, de ambos os sexos, pela emancipação", 2),
     {"skip": True, "end_how": "never-in-effect"}, _W77II),
    ((_BN, "art-077", "II -", "II - para o filho, a pessoa a ele equiparada ou o irmão, de ambos os sexos, ao completar vinte", 0),
     {"start": "2016-01-03", "start_law": "lei-13183-2015", "restored": False}, _W77II),
    *[((_BN, "art-041", lab, pre, 0), {"start": "1991-07-25", "start_law": None, "end": "1992-07-21",
                                       "end_law": "lei-8444-1992", "end_how": "renumbered"},
       "Lei 8.213 art. 41 §§ 5º and 6º as enacted ('O primeiro pagamento de renda mensal [...]', 'O pagamento de parcelas "
       "[...]', no notes): renumbered §§ 6º and 7º by Lei 8.444/1992 (21.7.1992), which inserted a new § 5º; they had "
       "been dated by later rules") for lab, pre in [("§ 5º", "§ 5º O primeiro pagamento de renda mensal"),
                                                     ("§ 6º", "§ 6º O pagamento de parcelas relativas a benefício")]],
    ((_BN, "art-074", "§ 3º", "§ 3º", 0), {"skip": True, "end_how": "editorial"},
     "Lei 8.213 art. 74 § 3º: Planalto prints a struck bare label '§ 3º' with only '(Vide Medida Provisória nº 871, de "
     "2019)' (MP 871's wording of the paragraph, in force 120 days after 18.1.2019 under its art. 34 II, is not printed); "
     "the line is left out and that wording is not modelled"),
    ((_BN, "art-096", "§ 1º", "§ 1º O disposto no inciso V do caput deste artigo", 0),
     {"start": "2026-03-27", "start_law": "lei-15363-2026"},
     "Lei 8.213 art. 96: Lei 15.363/2026 (27.3.2026) added § 2º, so the parágrafo único (Lei 13.846/2019) became § 1º "
     "from then (the § 1º line carries only the 2019 note)"),
    ((_BN, "art-011", "VI -", "VI - a associação em cooperativa agropecuária ou de crédito rural; e", 0),
     {"end": "2024-12-27", "end_law": "lei-15072-2024", "end_how": "successor"},
     "Lei 8.213 art. 11 § 8º VI: Planalto leaves Lei 13.183/2015's wording unstruck above Lei 15.072/2024's ('Redação "
     "dada'); it ends on 27.12.2024"),
    ((_BN, "art-106", "I -", "I - contrato individual de trabalho ou Carteira de Trabalho", 2),
     {"skip": False, "end": None, "end_law": None, "end_how": None, "state": "plain"},
     "Lei 8.213 art. 106 I (Lei 11.718/2008's wording): Planalto strikes it with a style but gives no revocation note, and "
     "its consolidated page prints it as in force under Lei 13.846/2019's caput; it is kept"),
]
_NOTEIN = ("typesetting: the consolidated page keeps old amendment notes inside the text ('(Parágrafo acrescentado pela Lei "
           "nº 9.528, de 10.12.97).', '(Alínea acrescentada pela Lei nº 8.647, de 13.4.93)'), which the annotated page sets "
           "as notes")
B.EXPLAINED[_C] = {
    "art-012": _NOTEIN + "; it also prints the revoked incisos III and IV as bare labels ('III -.') and a stray period "
                         "after '§ 11 do art. 25 desta Lei; e'",
    "art-020": _NOTEIN, "art-030": _NOTEIN,
    "art-022": _NOTEIN + "; it prints the suspended inciso IV (Resolução do Senado Federal nº 10, de 2016) as a bare 'IV' "
                         "label, which the history leaves out from 31.3.2016",
    "art-097": _NOTEIN + "; '§ 2º (VETADO na Lei nº 9.528, de 10.12.97)' for the annotated page's '§ 2º (VETADO)'",
    "art-028": "typesetting: the consolidated page prints the revoked alínea c) as a bare label 'c).'",
    "art-032-a": "typesetting: Planalto prints '§ 3º II' as 'II – R$ 500,00 [...]' with the dash struck (annotated page) and "
                 "as 'II R$ 500,00 [...] casos..' (consolidated page); the history keeps 'II - R$ 500,00 [...] casos.'",
    "art-047": "the consolidated page misprints 'a verbação' (annotated: 'a averbação') and keeps a footnote number ('19')",
    "art-056": "typesetting: the annotated page prints '§ 1º (Revogado pela Medida Provisória nº 2187-13, de 2001). "
               "(Renumerado do parágrafo único e Incluído pela Lei nº 12.810, de 2013)', kept as the label '§ 1º.'; the "
               "consolidated page's revocation-note line is read as a revoked placeholder",
    "art-093": "typesetting: the consolidated page prints 'Art. 93. (Revogado o caput pela Lei nº 9.639, de 25.5.98.)'; the "
               "annotated page strikes both wordings of the caput and the parágrafo único (revoked by Lei 11.941/2009), so "
               "the article is not in today's text",
    "titulos": "typesetting: the consolidated page sets the Capítulo VI name in capitals ('DA CONTRIBUIÇÃO DO PRODUTOR RURAL E "
               "DO PESCADOR') with the note '(Alterado pela Lei nº 8.398, de 7.1.92)' as a line; the annotated page's "
               "heading (misprint 'Pescado}' corrected) is used",
}
B.EXPLAINED[_BN] = {
    "art-071-c": "the consolidated page drops the closing period ('... sob pena de suspensão do benefício'), which the "
                 "annotated page prints",
    "art-115": "the consolidated page (captured 15.10.2026) is out of date: it still prints Medida Provisória 1.355/2026's "
               "wording of inciso VI ('[...] observados os limites [...]'), which lost effect on 1.9.2026 (Ato Declaratório "
               "nº 89, de 2026), and lacks Lei 15.327/2026's change to inciso V; the annotated page has both",
    "art-124-g": "the consolidated page is out of date: it lacks art. 124-G (Lei 15.327/2026, DOU 7.1.2026), which the "
                 "annotated page prints",
    "art-096": "the consolidated page is out of date: it still prints the parágrafo único (Lei 13.846/2019), which Lei "
               "15.363/2026 (27.3.2026) made § 1º when it added § 2º; the annotated page prints §§ 1º and 2º",
}
B13.OPEN_ITEMS.update({
    _C: ("Lei 8.212 (open items): Planalto's 'Vide' pointers (ADIs 2.028, 2.036, 2.228, 4.395, 5.161, 7.633; Lei Complementar "
         "150/2015; Lei 15.371/2026) strike no words and are not modelled; the amounts of the art. 20 and art. 21 tables "
         "updated by ministerial portarias are not part of the act's text"),
    _BN: ("Lei 8.213 (open items): Planalto's 'Vide' pointers (ADIs 2.110, 2.111, 4.878, 5.083, 6.096, 6.327) "
          "strike no words and are not modelled; Medida Provisória 871/2019's wording of art. 74 § 3º (in force 120 days "
          "after 18.1.2019 under its art. 34 II) is not printed on the page and is not modelled"),
})
_anachronisms15 = P.anachronisms


def anachronisms(paras, cx):
    """lines dated by hand from a provision's own in-force day (MP 664/2014 art. 5 I and II) are not early"""
    return _anachronisms15([p for p in paras if not p.get("by_provision")], cx)


P.anachronisms = anachronisms
TEXT_FIX.append(("l8213", "a das demais deve ser comprovada$", "a das demais deve ser comprovada.",
                 "Lei 8.213 art. 16 § 4º: the annotated page drops the closing period, which the consolidated page prints"))
# heading lines (B8.SPAN_FIX leaves headings alone): act -> [(text, fields, why)]
HEAD_FIX: dict[str, list] = {
    _C: [(t, {"end_law": "lei-8398-1992", "end_how": "successor", "skip": False},
          "Lei 8.212 Capítulo VI heading: the 1991 heading 'CAPÍTULO VI / Da Contribuição do Produtor Rural, do Pescador e "
          "do Garimpeiro' (struck, no note) ends when Lei 8.398/1992's heading ('Da Contribuição do Produtor Rural e do "
          "Pescador', printed below it with its note) starts")
         for t in ("CAPÍTULO VI", "Da Contribuição do Produtor Rural, do Pescador e do Garimpeiro")],
}
SPAN15_USED: list[str] = []
_apply_rewrites15 = P.apply_rewrites


def apply_rewrites(paras, act, eff, problems):
    """the shared rewrite rules (and batch 3's 'undated' rule) run after the life spans: heading fixes come after them"""
    out = _apply_rewrites15(paras, act, eff, problems)
    for text, fields, why in HEAD_FIX.get(act["slug"], []):
        for p in paras:
            if p["heading"] and p["state"] != "plain" and p["text"] == text and p.get("end_how") == "undated":
                p.update(fields)
                if fields.get("end_law") and not fields.get("end"):
                    p["end"] = eff[fields["end_law"]]
                p["pinned"] = True
                SPAN15_USED.append(why)
    for fn in ARTICLE_FIX.get(act["slug"], []):
        fn(paras, eff)
    mp_pairs_restore(paras)
    return out


def mp_pairs_restore(paras):
    """a wording MP 905 revoked is printed a third time, unstruck and without notes, for the text in force again from
    19.8.2020 (the shared duplicate rules had set it aside as a copy of the struck ones): it starts when MP 905's term
    ended"""
    for m_key in MP_PAIRS:
        m_lapse = P.MP_LAPSE[m_key][0]
        for i, p in enumerate(paras):
            if p.get("mp_role") != "revoked":
                continue
            for q in paras[i + 1:]:
                if q["unit"] != p["unit"]:
                    break
                if (q["state"] == "plain" and not q.get("mp_pair") and q["label"] == p["label"] and q["text"] == p["text"]
                        and (q.get("skip") or q["start"] < m_lapse)):
                    q.update({"start": m_lapse, "start_law": m_key + "-fim", "skip": False, "restored": True,
                              "pinned": True})
                    if q.get("end_how") in ("duplicate", "twin", "undated"):
                        q["end"], q["end_law"], q["end_how"] = None, None, None
                    MP_PAIRS_USED.append(f"{p['unit']} [{p['label']}]: in force again from 19.8.2020 (unstruck copy)")
                    break


def _art55(paras, eff):
    """Lei 8.212 art. 55: Planalto prints the whole article twice, first with the caput's note 'Revogado pela Medida
    Provisória nº 446, de 2008' (MP 446, DOU 10.11.2008, rejected by the Chamber on 10.2.2009), then again with every line
    noted 'Revogado pela Lei nº 12.101, de 2009'. The first copy is the article: every line in force across MP 446's term
    has the caput's gap; the second copy is left out (its lines are the same wordings)."""
    lines = [p for p in paras if p["unit"] == "art-055" and not p["heading"]]
    cut = next((i for i, p in enumerate(lines) if i and p["label"] == "Art. 55"), None)
    if cut is None:
        return
    gap = next((g for g in lines[0].get("gaps") or [] if g[2] == "mp-446-2008"), None)
    if not gap:
        return
    for p in lines[1:cut]:
        if not p.get("skip") and p["start"] < gap[0] and (p["end"] is None or p["end"] > gap[1]) and not p["gaps"]:
            p["gaps"], p["pinned"] = [gap], True
    for p in lines[cut:]:
        p["skip"], p["end_how"], p["pinned"] = True, "duplicate", True
    SPAN15_USED.append("Lei 8.212 art. 55: Planalto prints the whole article twice, first with the caput's note 'Revogado "
                       "pela Medida Provisória nº 446, de 2008' (MP 446 was rejected on 10.2.2009), then again with every "
                       "line noted 'Revogado pela Lei nº 12.101, de 2009' (30.11.2009); the first copy is the article, all "
                       "of it out of force while MP 446 stood (10.11.2008 to 10.2.2009), and the second copy (the same "
                       "wordings) is left out")


def _art25_order(paras, eff):
    """Lei 8.212 art. 25 I as worded by Lei 9.528/1997 is printed above the caput Lei 10.256/2001 gave the article; it
    stood under that caput until 13.9.2017, so it is placed after it."""
    i = next((k for k, p in enumerate(paras) if p["unit"] == "art-025" and p["label"] == "I -"
              and p["text"].startswith("I - 2% da receita bruta")), None)
    j = next((k for k, p in enumerate(paras) if p["unit"] == "art-025" and p["label"] == "Art. 25" and p["state"] == "plain"),
             None)
    if i is None or j is None or i > j:
        return
    paras.insert(j, paras.pop(i))
    SPAN15_USED.append("Lei 8.212 art. 25 I (Lei 9.528/1997's wording, '2% da receita bruta [...]') is printed above the "
                       "caput Lei 10.256/2001 gave the article and is placed after that caput, under which it stood until "
                       "13.9.2017")


def _art20(paras, eff):
    """Lei 8.212 art. 20's tables: 1991 (original page) to Lei 9.032/1995; Lei 9.032's (original page) to Lei 9.129/1995;
    Lei 9.129's (the annotated page's, followed there by '(Valores e alíquotas dados pela Lei nº 9.129, de 20.11.95)')."""
    d9032, d9129 = eff["lei-9032-1995"], eff["lei-9129-1995"]
    for p in paras:
        if p["unit"] == "art-020" and p.get("orig_insert") and p["label"] == "Parágrafo único":
            # renumbered § 1º when Lei 8.620/1993 added § 2º (the § 1º printed with its note)
            p.update({"end": eff["lei-8620-1993"], "end_law": "lei-8620-1993", "end_how": "renumbered", "skip": False,
                      "pinned": True})
        if p["unit"] != "art-020" or p["label"] or p["heading"]:
            continue
        if p.get("t9032"):
            p.update({"start": d9032, "start_law": "lei-9032-1995", "end": d9129, "end_law": "lei-9129-1995",
                      "end_how": "successor", "skip": False, "gaps": [], "pinned": True})
        elif p.get("orig_insert"):
            p.update({"start": P.ACT_DAY["lei-8212-1991"][0], "start_law": None, "end": d9032, "end_law": "lei-9032-1995",
                      "end_how": "successor", "skip": False, "gaps": [], "pinned": True})
        elif p["state"] == "plain":
            p.update({"start": d9129, "start_law": "lei-9129-1995", "pinned": True})
    SPAN15_USED.append("Lei 8.212 art. 20's rate table: the 1991 table (original page) stands to Lei 9.032/1995 (29.4.1995), "
                       "Lei 9.032's table (original page; 'até R$ 249,80 [...] até R$ 836,90') to Lei 9.129/1995 (21.11.1995), "
                       "and the table the annotated page prints ('até 249,80 [...] até 832,66', followed there by "
                       "'(Valores e alíquotas dados pela Lei nº 9.129, de 20.11.95)', and in Lei 9.129's own text) from then")


ARTICLE_FIX: dict[str, list] = {_C: [_art55, _art25_order, _art20]}


P.apply_rewrites = B.apply_rewrites = apply_rewrites
_lifespans15 = P.lifespans


def lifespans(paras, cx):
    problems = _lifespans15(paras, cx)
    # 'ends before it starts' problems the hand-set spans above have settled
    bad = {f"{p['unit']} [{p['label']}]" for p in paras if p["end"] and not p.get("skip") and p["end"] < p["start"]}
    def settled(x):
        m = re.match(r"ends before it starts: (\S+ \[[^\]]*\]) ", x)
        return bool(m) and m.group(1) not in bad
    return [x for x in problems if not settled(x)]


P.lifespans = B.lifespans = lifespans

_inner15 = B6.PB5B._write_part5


def _inner(*a):
    dec = mp_pairs_decision() + EXTRA
    if FOOTNOTES_DROPPED.get("l8212"):
        dec.append(f"Lei 8.212: Planalto's annotated page keeps the numbered footnote markers of a 1998 edition "
                   f"({FOOTNOTES_DROPPED['l8212']} superscript numbers such as 'e) as importâncias: 14'); the footnotes "
                   "themselves (on Medidas Provisórias then pending, and updated amounts) are printed after the signature, "
                   "outside the act, so the markers are dropped from the text and the footnotes are not part of the history.")
    if CENTERED.get("l8212"):
        dec.append("Lei 8.212: Planalto's pages set each Título and Capítulo name as an unaligned paragraph inside a centred "
                   "block (only the 'TÍTULO I' line itself is centred text); these names are read as heading lines, as "
                   "displayed, not as marginal headings of the following article.")
    if ORIGINAL_USED:
        dec.append("Lei 8.212 arts. 20, 26, 36, 68 and 94: Planalto's annotated page prints only later wordings of these "
                   "articles, not their 1991 text; the 1991 wording is read from Planalto's page of the act as enacted "
                   "(L8212orig.htm, which strikes it above the later wording; for art. 94 it prints it unstruck) and "
                   "placed struck above the first wording the annotated page prints, which ends it (art. 36: revoked by "
                   "Lei 8.218/1991): " + ", ".join(ORIGINAL_USED) + ".")
    if TABLES:
        dec.append("Tables printed inside articles (" + ", ".join(f"{k} {v}" for k, v in sorted(TABLES.items())) + "): "
                   "Planalto centres their cells; each cell is a line of the article it is printed in (as in the CLT's "
                   "art. 580), not a heading line.")
    if LETTER_ARTS:
        dec.append("Articles Planalto prints with the letter but no hyphen ('Art. 22A.', 'Art. 22B.', 'Art. 25A.') are "
                   "articles of their own (art-022-a, ...), labelled 'Art. 22-A' like the rest of the corpus: "
                   + ", ".join(sorted(set(x.split()[1] for x in LETTER_ARTS))) + ".")
    if TEXT_FIX_USED:
        dec.append("Misprints corrected: " + "; ".join(dict.fromkeys(TEXT_FIX_USED)) + ".")
    if NOTE_DOT:
        dec.append("A period printed after an amendment note that follows a line already ending in ';', ':' or ',' ('... "
                   "salário-maternidade; (Redação dada pela Lei nº 9.528, de 10.12.97).') closes the note and is dropped "
                   "with it (lines: " + ", ".join(f"{k} {v}" for k, v in sorted(NOTE_DOT.items())) + ").")
    if SPAN15_USED:
        dec.append("Life spans set by hand for these acts: " + "; ".join(dict.fromkeys(SPAN15_USED)) + ".")
    B5.EXTRA_DECISIONS.extend(dec)
    return _inner15(*a)


B6.PB5B._write_part5 = _inner

SRC = HERE / "sources_batch15.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
