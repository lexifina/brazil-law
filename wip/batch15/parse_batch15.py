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
P.VIGENCIA_FIXED.update({
    "lei-13202-2015": ("2015-12-09", "art. 16: 'Esta Lei entra em vigor: I - a partir de 1º de dezembro de 2015 quanto ao art. 15; "
                                     "II - na data de sua publicação quanto aos demais dispositivos' (DOU 9.12.2015): its "
                                     "changes to Lei 8.212 (arts. 12 and 17) fall under II"),
    "lei-13183-2015": ("2015-11-05", "art. 7: 'Esta Lei entra em vigor: I - em 3 de janeiro de 2016, quanto à redação do art. 16 "
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
FOOTNOTES_DROPPED: dict[str, int] = {}
NOTE_DOT: dict[str, int] = {}
_paragraphs15 = P.paragraphs
_SUPNUM = re.compile(r"<sup\b(?:(?!</sup>).)*?</sup>", re.S | re.I)


def _supnum(m):
    s = re.sub(r"<[^>]+>|&nbsp;|\s", "", m.group(0))
    return "" if re.fullmatch(r"\d{1,2}", s) else m.group(0)


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
    html = re.sub(r"<center\b.*?</center>", lambda m: re.sub(r"<p(?=[\s>])(?![^>]*\balign=)", '<p align="center"', m.group(0),
                                                             flags=re.I), html, flags=re.S | re.I)
    if n0:
        CENTERED[page] = n0
    out, rest = _paragraphs15(html, digits)
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
    return out


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
