"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch12.json (SCHEMA.md corpus part): the four acts batch 11
deferred (Lei 6.766/1979, Lei 9.656/1998, Lei 8.742/1993, Lei 6.385/1976), as they are verified.

    python -X utf8 scripts/brazil-law/batch12/parse_batch12.py [--stats] [--dry]

Imports ../batch11/parse_batch11.py (which configures batch 10 and everything below it, plus batch 11's hand tables) with
no act of its own, and replaces only the configuration: the acts, the hand tables for these acts, the pins and the output.
Earlier parts are not touched. No network.

BATCH12_ACTS=<slug,...> selects acts for trial runs (BATCH12_OUT=<file> writes elsewhere); by default VERIFIED is
written.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH11_ACTS"] = "-"   # batch 11 configures no act of its own here
os.environ.pop("BATCH11_OUT", None)
sys.path.insert(0, str(FOLDER / "batch11"))
import parse_batch11 as B11  # noqa: E402

B10, B9, B8, B7, B6, B5, B, P = B11.B10, B11.B9, B11.B8, B11.B7, B11.B6, B11.B5, B11.B, B11.P
PL = P.PL
B5.OUT = Path(os.environ.get("BATCH12_OUT") or FOLDER / "corpus.d" / "99-batch12.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

MINE = ["lei-do-parcelamento-do-solo-urbano", "lei-dos-planos-de-saude", "lei-organica-da-assistencia-social",
        "lei-do-mercado-de-valores-mobiliarios"]
ALL_ACTS: list[dict] = [a for s in MINE for a in B11.ALL_ACTS if a["slug"] == s]
PAGES = {k: v for k, v in B11.PAGES.items() if any(k in (a["page"], a["consolidated"]) for a in ALL_ACTS)}
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = B6.PAGES = B7.PAGES = B8.PAGES = B9.PAGES = B10.PAGES = B11.PAGES = PAGES

VERIFIED: list[str] = ["lei-do-parcelamento-do-solo-urbano", "lei-dos-planos-de-saude", "lei-organica-da-assistencia-social",
                        "lei-do-mercado-de-valores-mobiliarios"]
ENABLED = [s for s in os.environ.get("BATCH12_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
for M in (B7, B8, B9, B10, B11):
    M.ACTS[:] = ACTS
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in B11.ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in B11.ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# batch 11's act-specific tools emptied (its law facts in VIGENCIA_FIXED etc. are kept: printed only where used)
B.EXPLAINED.clear()
B8.SPAN_FIX.clear()
B8.LABEL_FIX.clear()
B9.WORD_FIX.clear()
P.VETO_PROMULGATION = {}
P.VETO_PROMULGATED_UNITS = {}

# ---------------------------------------------------------------------------------------------------------------
# hand tables for these acts, each read from the official pages named in the reason
_LPSU = "lei-do-parcelamento-do-solo-urbano"
B8.LABEL_FIX[:] = [
    ("lpsolo", "III-A. - ao longo das águas correntes", "III-A - ao longo das águas correntes", "III-A -",
     "Lei do Parcelamento do Solo Urbano art. 4 III-A: Lei 13.913/2019's wording is printed 'III-A. -'; read as 'III-A -', "
     "so Lei 14.285/2021's wording of III-A replaces it"),
]
B9.WORD_FIX[:] = [
    ("lpsolo", "§ 1º Parágrafo único. Na hipótese de parcelamento", "§ 1º Na hipótese de parcelamento",
     "Lei do Parcelamento do Solo Urbano art. 22 § 1º: Lei 14.620/2023 art. 24 keeps the former parágrafo único as § 1º "
     "('§ 1º .....', adding §§ 2º and 3º); both Planalto pages print '§ 1º Parágrafo único. Na hipótese ...', and the "
     "history drops the leftover words 'Parágrafo único.'"),
]
# Lei Orgânica da Assistência Social
B7.CONVERTED_FIX["mp-1164-2023"] = ("lei-14601-2023", "the MP page reads 'Convertida na Lei 14.601, de 2023' (no 'nº'); "
                                                    "Lei nº 14.601, de 19.6.2023")
P.MP_LAPSE["mp-446-2008"] = (
    "2009-02-10", "rejected: Ato do Presidente da Câmara dos Deputados (DOU 12.2.2009) makes known that 'em sessão realizada "
                  "no dia 10 de fevereiro de 2009, o Plenário da Casa rejeitou a Medida Provisória nº 446' (DOU 10.11.2008, "
                  "in force on publication); the wording it had replaced is back from 10.2.2009 (CF art. 62 § 3 makes a "
                  "rejected MP lose effect from its edition; the history keeps its wording for the days Planalto shows it "
                  "standing)")
B5.MP_REJECTED["mp-446-2008"] = ("Rejeição da Medida Provisória nº 446, de 2008",
                                 "Ato do Presidente da Câmara dos Deputados: rejeição da Medida Provisória nº 446, de 2008")
_LOAS = "lei-organica-da-assistencia-social"
P.VIGENCIA_FIXED.update({
    "lei-14176-2021": ("2021-06-23", "art. 6: 'Esta Lei entra em vigor: I - em 1º de janeiro de 2022, quanto ao art. 1º, na "
                                     "parte que acrescenta o § 11-A no art. 20 e o art. 20-B na Lei nº 8.742 [...]; II - em 1º "
                                     "de outubro de 2021, quanto ao art. 2º, que institui o auxílio-inclusão [the new Seção VI, "
                                     "arts. 26-A to 26-H]; e III - na data de sua publicação, quanto aos demais dispositivos' "
                                     "(DOU 23.6.2021)"),
    "lei-14601-2023": ("2023-06-20", "art. 34: 'Esta Lei entra em vigor: I - em 1º de janeiro de 2024, quanto: a) aos arts. 30 e "
                                     "31 e ao inciso I do caput do art. 33; b) ao § 3º do art. 4º; e II - na data de sua "
                                     "publicação, quanto aos demais dispositivos' (DOU 20.6.2023); its changes to Lei 8.742 "
                                     "(art. 28) fall under II"),
})
P.VIGENCIA_PROVISION.update({
    ("lei-14176-2021", _LOAS, "art-20-b"): ("2022-01-01", "Lei 14.176/2021 art. 6 I: art. 20-B in force on 1.1.2022"),
    **{("lei-14176-2021", _LOAS, f"art-26-{c}"): ("2021-10-01", "Lei 14.176/2021 art. 6 II: the auxílio-inclusão (Seção "
                                                                 "VI, arts. 26-A to 26-H) in force on 1.10.2021")
       for c in "abcdefgh"},
})
B8.SPAN_FIX[:] = [
    ((_LOAS, "art-20", "§ 11-A", "§ 11-A. O regulamento", 0), {"start": "2022-01-01", "start_law": "lei-14176-2021"},
     "Lei Orgânica da Assistência Social art. 20 § 11-A: Lei 14.176/2021 art. 6 I puts it in force on 1.1.2022 (its other "
     "changes to art. 20 on publication, 23.6.2021)"),
    ((_LOAS, "art-09", "§ 3º", "§ 3º A inscrição da entidade no Conselho Municipal", 1),
     {"end": "2009-11-30", "end_law": "lei-12101-2009", "end_how": "note",
      "gaps": [("2008-11-10", "2009-02-10", "mp-446-2008", "mp-446-2008-fim")]},
     "Lei Orgânica da Assistência Social art. 9 § 3º: Medida Provisória nº 2.187-13/2001's wording stands from 27.8.2001 "
     "until Lei 12.101/2009 revoked it (30.11.2009), except while Medida Provisória nº 446/2008 (revoked it; rejected "
     "10.2.2009) stood"),
    ((_LOAS, "art-09", "§ 3º", "§ 3º A inscrição da entidade no Conselho Municipal", 2), {"skip": True, "end_how": "twin"},
     "Lei Orgânica da Assistência Social art. 9 § 3º: Planalto prints Medida Provisória nº 2.187-13/2001's wording twice, "
     "once noted as revoked by Medida Provisória nº 446/2008 (rejected 10.2.2009) and once as revoked by Lei 12.101/2009; "
     "the first copy carries the whole life span (2001 to 2009, absent while MP 446 stood) and the second is left out"),
    ((_LOAS, "art-20", "§ 7º", "§ 7º Na hipótese de não existirem serviços credenciados", 0),
     {"end": "1998-12-01", "end_law": "lei-9720-1998", "end_how": "successor"},
     "Lei Orgânica da Assistência Social art. 20 § 7º: the 1993 wording ends when Lei 9.720/1998 gave the paragraph its "
     "new wording (noted 'Incluído', printed below the struck 1993 text)"),
]
B9.WORD_FIX[:] = B9.WORD_FIX + [
    ("loas", "§ 3º deste artigo. '", "§ 3º deste artigo.",
     "Lei Orgânica da Assistência Social art. 20 § 14: the annotated page prints a stray apostrophe on its own line after the "
     "paragraph; it is dropped (the consolidated page and Lei 13.982/2020 have none)"),
]
P.NOTE_FIX.update({
    "(Redação dada pela Lei nº 9.720, de 26.4.1991)": (
        "(Redação dada pela Lei nº 9.720, de 1998)",
        "Lei Orgânica da Assistência Social art. 18 VI: the note reads 'Lei nº 9.720, de 26.4.1991'; Lei nº 9.720 is of "
        "30.11.1998 (the other notes of the page and the law's own page)"),
})
_TYPO = "typesetting: the annotated page prints 'Art. {n}º.' with a full stop after the number; the consolidated page has none"
B.EXPLAINED[_LPSU] = {
    **{f"art-{n:02d}": _TYPO.format(n=n) for n in (1, 2, 4, 5, 7)},
    "art-06": _TYPO.format(n=6) + "; inciso VI reads 'caracteristicas' on the annotated page, 'características' on the "
              "consolidated page",
    "art-43": "typesetting: the annotated page ends the parágrafo único with a full stop, the consolidated page without",
    "art-22": "both Planalto pages print '§ 1º Parágrafo único. Na hipótese ...'; the history drops the leftover 'Parágrafo "
              "único.' (see the word corrections)",
}

# ---------------------------------------------------------------------------------------------------------------
# Lei do Mercado de Valores Mobiliários: Decreto nº 3.995, de 31.10.2001 (DOU 1.11.2001), an autonomous decree (CF art. 84
# VI a, 'nas matérias reservadas a decreto') that rewrote and added provisions of Lei 6.385 on the day Lei 10.303/2001 was
# sanctioned with those provisions vetoed. Its notes ('Redação dada pelo Decreto nº 3.995, de 31.10.2001', 'Parágrafo
# incluído pelo Decreto ...') name a decree, which the shared law keys do not cover: key dec-<n>-<year>, kind "decree".
import re  # noqa: E402

_LCVM = "lei-do-mercado-de-valores-mobiliarios"
DEC_REF = re.compile(r"\bDecreto(?:\s+aut[ôo]nomo)?\s+n\s*[º°o]?\s*\.?\s*([\d.]+)\s*,?\s*de\s+(?:\d{1,2}\s*\.\s*\d{1,2}\s*\.\s*)?(\d{4})",
                     re.I)
DECREES = {
    "dec-3995-2001": {"enacted": "2001-10-31", "published": "2001-11-01",
                      "title": "Altera e acresce dispositivos à Lei nº 6.385, de 7 de dezembro de 1976, que dispõe sobre o "
                               "mercado de valores mobiliários, nas matérias reservadas a decreto."},
}
_law_key12, _law_label12, _page_info12, _lexml_url12 = P.law_key, P.law_label, P.page_info, P.lexml_url


def law_key(text, year_of=None):
    k = _law_key12(text, year_of)
    if k is None:
        t = P.NOTE_FIX.get(text, (text,))[0]
        m = DEC_REF.search(t)
        if m and not re.search(r"\bVide\b", t[:m.start()], re.I):
            k2 = f"dec-{int(m.group(1).replace('.', ''))}-{m.group(2)}"
            if k2 in DECREES:
                return k2
    return k


def law_label(key):
    if key.startswith("dec-"):
        _, n, y = key.split("-")
        return "Decreto nº " + f"{int(n):,}".replace(",", ".") + f", de {y}"
    return _law_label12(key)


def page_info(key):
    if key not in DECREES:
        return _page_info12(key)
    r = P.raw("law:" + key)
    if not r:
        return {}
    import hashlib
    return {"source_url": r[1], "sha256": hashlib.sha256(r[0]).hexdigest(), **DECREES[key],
            "clause": "Este Decreto entra em vigor na data de sua publicação"}


def lexml_url(key, enacted):
    return None if key.startswith("dec-") else _lexml_url12(key, enacted)


P.law_key = B.law_key = law_key
P.law_label = B.law_label = law_label
P.page_info = B.page_info = page_info
P.lexml_url = B.lexml_url = lexml_url
P.VIGENCIA_FIXED["dec-3995-2001"] = (
    "2001-11-01", "art. 3: 'Este Decreto entra em vigor na data de sua publicação, produzindo efeitos, em relação às "
                  "companhias já constituídas, após decorridos cento e vinte dias daquela data' (DOU 1.11.2001)")
P.NOTE_FIX.update({
    "(Redação pelo Decreto nº 3.995, de 31.10.2001)": (
        "(Redação dada pelo Decreto nº 3.995, de 31.10.2001)",
        "Lei do Mercado de Valores Mobiliários art. 11 § 10: the note reads 'Redação pelo Decreto' ('dada' missing)"),
})
_W10303 = ("Lei do Mercado de Valores Mobiliários art. 9 §§ 3º to 6º: Lei 10.303/2001 (in force 1.3.2002) added them as "
           "'(VETADO)', and Decreto nº 3.995/2001 (in force 1.11.2001) gave them their wording; Planalto prints the "
           "'(VETADO)' lines struck above the decree's wording. They never stood as text and are left out; the decree's "
           "wordings stand from 1.11.2001")
B8.SPAN_FIX += [
    *[((_LCVM, "art-09", lab, lab + " (VETADO)", 0), {"skip": True, "end_how": "twin"}, _W10303)
      for lab in ("§ 3º", "§ 4º", "§ 5º", "§ 6º")],
    ((_LCVM, "art-09", "§ 4º", "§ 4º Na apuração de infrações da legislação do mercado de valores mobiliários, a Comissão "
                               "deverá dar prioridade", 0),
     {"start": "2001-11-01", "start_law": "dec-3995-2001", "end": "2017-06-08", "end_law": "mp-784-2017",
      "end_how": "successor"},
     "Lei do Mercado de Valores Mobiliários art. 9 § 4º: Decreto nº 3.995/2001's wording stands from 1.11.2001 until "
     "Medida Provisória nº 784/2017 (8.6.2017), and again (Planalto's second copy) from the MP's lapse (20.10.2017) until "
     "Lei 13.506/2017 (14.11.2017)"),
    ((_LCVM, "art-18", "h)", "h) (VETADO)", 0), {"skip": True, "end_how": "twin"},
     "Lei do Mercado de Valores Mobiliários art. 18 II h): Lei 10.303/2001 (in force 1.3.2002) added it as '(VETADO)', and "
     "Lei 10.411/2002 (in force 27.2.2002) gave it its wording first; the '(VETADO)' line, which Planalto prints unstruck "
     "above that wording, never stood as text and is left out"),
]
# Lei 6.385 art. 9 caput: Planalto's annotated page prints only Decreto nº 3.995/2001's wording of the caput (noted
# 'Redação dada pelo Decreto'), not the 1976 wording it replaced; that wording is read from Planalto's page of the act as
# enacted (l6385original.htm, pinned as ctx:lcvm-original) and placed, struck, above the decree's, so it stands from
# 1976 to 1.11.2001 (without it the article rule would date the whole article from the decree)
LCVM_ORIGINAL_USED: list[str] = []
_paragraphs12 = P.paragraphs


def _original_caput9() -> str:
    import html as _h
    keep = B8.CURRENT_PAGE[0]
    r = P.raw("ctx:lcvm-original")
    B8.CURRENT_PAGE[0] = keep
    t = P.norm(_h.unescape(re.sub(r"<[^>]+>", " ", P.decode(r[0]))))
    m = re.search(r"Art\.?\s*9\s*[º°o]\s+(A Comissão de Valores Mobiliários terá jurisdição.*?poderá:)", t)
    return "Art. 9º " + m.group(1)


def paragraphs(html, digits):
    out, rest = _paragraphs12(html, digits)
    if B8.CURRENT_PAGE[0] == "lcvm":
        for i, p in enumerate(out):
            if p["unit"] == "art-09" and p["label"].startswith("Art. 9") and p["state"] == "plain" and any(
                    "3.995" in n for n in p["notes"]):
                old = {**p, "text": _original_caput9(), "state": "struck", "notes": [], "plain_text": "",
                       "struck_text": ""}
                old["struck_text"] = old["text"]
                out.insert(i, old)
                LCVM_ORIGINAL_USED.append(
                    "Lei do Mercado de Valores Mobiliários art. 9 caput: Planalto's annotated page prints only Decreto nº "
                    "3.995/2001's wording; the 1976 wording it replaced ('" + old["text"][:90] + "...') is read from "
                    "Planalto's page of the act as enacted (l6385original.htm) and stands from 9.12.1976 to 1.11.2001")
                break
    return out, rest


P.paragraphs = B.paragraphs = paragraphs

# replay problems on lines the hand spans above settle (the '(VETADO)' lines of Lei 10.303 art. 9 §§ 3º, 5º, 6º, left out)
LCVM_SETTLED = tuple(f"no end for struck art-09 [{x}] '{x} (VETADO)'" for x in ("§ 3º", "§ 5º", "§ 6º"))
_lifespans12 = P.lifespans


def lifespans(paras, cx):
    problems = _lifespans12(paras, cx)
    if cx.act == _LCVM:
        problems = [x for x in problems if not x.startswith(LCVM_SETTLED)]
    if cx.act == "lei-dos-planos-de-saude":   # art. 10 § 2º: settled by its hand span (see the life-span decisions)
        problems = [x for x in problems if not x.startswith("no end for struck art-10 [§ 2º] '§ 2º As pessoas jurídicas")]
    return problems


P.lifespans = B.lifespans = lifespans
B9.WORD_FIX[:] = B9.WORD_FIX + [
    ("lcvm", "Art. 17-A. (VETADO) (Artigo", "Art. 17-A. (VETADO)",
     "Lei do Mercado de Valores Mobiliários art. 17-A: the first word of the note '(Artigo incluído pela Lei nº 10.303, de "
     "31.10.2001)' is read into the line; it is dropped"),
]
B.EXPLAINED[_LCVM] = {
    "art-21": "the consolidated page ends § 5º with a stray closing quotation mark ('organizado ou não.\"'); the annotated "
              "page has none",
}

# ---------------------------------------------------------------------------------------------------------------
# Lei dos Planos de Saúde (Lei 9.656/1998). From 5.6.1998 (Medida Provisória nº 1.665, before the act took effect on
# 2.9.1998) to 27.8.2001 the act was rewritten by a chain of about 44 monthly Medidas Provisórias (1.665, 1.685, 1.730,
# 1.801, 1.908, 1.976, 2.097, 2.177), the last being MP 2.177-44 (DOU 27.8.2001), kept in force by EC 32/2001 art. 2.
# Planalto's page prints only the 1998 text and MP 2.177-44's wording, citing the earlier reissues with 'Vide' notes, so
# the text in force between 1998 and 2001 cannot be rebuilt from it: the history starts on 27.8.2001 with the oldest
# version available.
_LPS = "lei-dos-planos-de-saude"
LPS_START = "2001-08-27"
LPS_WHY = ("Lei dos Planos de Saúde: from 5.6.1998 (Medida Provisória nº 1.665, issued before the act took effect on "
           "2.9.1998) to 27.8.2001 the act was rewritten by a chain of about 44 monthly reissued Medidas Provisórias "
           "(1.665, 1.685, 1.730, 1.801, 1.908, 1.976, 2.097 and 2.177), the last being MP 2.177-44 (DOU 27.8.2001), kept "
           "in force by EC 32/2001 art. 2. Planalto's page prints only the 1998 text and MP 2.177-44's wording and cites the "
           "earlier reissues with 'Vide' notes, so the text in force from 1998 to 2001 cannot be rebuilt from it. The "
           "history therefore starts on 27.8.2001 with the oldest version available (the act as MP 2.177-44 worded it, "
           "including Lei 10.223/2001's change), credited to the publisher; the 1998 text and the monthly reissues are not "
           "modelled")
LPS_ADI = ("Lei dos Planos de Saúde, STF ADI 1.931 (open item): Planalto strikes art. 35-E and the words 'atuais e' in art. "
           "10 § 2º, noting only '(Vide ADI nº 1.931)' with no date. As for other struck text whose end the source does not "
           "date, art. 35-E and the struck words are left out of every version; the ruling (a 2003 interim suspension and "
           "the 2018 judgment) is not modelled, pending a dated official record")
P.MP_PENDING["mp-2177-2001"] = ("Medida Provisória nº 2.177-44, de 24.8.2001 (DOU 27.8.2001), the last reissue of the "
                                "MP 1.665/1998 chain, was in force on 11.9.2001, so it stays in force until a later MP "
                                "revokes it or Congress votes on it (Emenda Constitucional 32/2001, art. 2)")
B8.SPAN_FIX += [
    ((_LPS, "art-10", "§ 2º", "§ 2º As pessoas jurídicas que comercializam produtos", 0),
     {"end": None, "end_law": None, "end_how": None, "state": "plain",
      "text": "§ 2º As pessoas jurídicas que comercializam produtos de que tratam o inciso I e o § 1º do art. 1º desta Lei "
              "oferecerão, obrigatoriamente, a partir de 3 de dezembro de 1999, o plano-referência de que trata este artigo "
              "a todos os seus futuros consumidores."},
     "Lei dos Planos de Saúde art. 10 § 2º: Medida Provisória nº 2.177-44's wording, with the words 'atuais e' that Planalto "
     "strikes (ADI 1.931, undated) left out, stands from 27.8.2001 to today (no later law rewrote it; the next-wording "
     "rule had ended it with MP 1.067/2021's § 4º)"),
    ((_LPS, "art-32", "§ 10", "§ 10. A obrigação de ressarcimento de que trata este artigo poderá ser convertida em "
                               "prestação de serviços no âmbito do SUS, mediante", 0),
     {"end": "2025-10-08", "end_law": "lei-15233-2025", "end_how": "conversion"},
     "Lei dos Planos de Saúde art. 32 § 10: Medida Provisória nº 1.301/2025's wording ends when its conversion law, Lei "
     "15.233/2025, gave the paragraph its own wording (8.10.2025)"),
]
B9.WORD_FIX[:] = B9.WORD_FIX + [
    ("lps", "Ministros de Estado: (composição: vide Dec.4.044, de 2001)", "Ministros de Estado:",
     "Lei dos Planos de Saúde art. 35-B: Planalto's editorial pointer '(composição: vide Dec. 4.044, de 2001)' is printed "
     "inside the caput; it is dropped like the page's other 'Vide' notes"),
]
B.EXPLAINED[_LPS] = {
    "art-12": "typesetting: the annotated page prints 'g)cobertura' without a space",
    "art-32": "typesetting: the annotated page ends § 1º II without its full stop; the consolidated page cuts § 10 off "
              "after 'em depó' (the history's § 10 is word for word Lei 15.233/2025's text)",
    "art-35-b": "the consolidated page keeps the editorial pointer '(composiçaõ: vide Dec.4.044, de 6.12.2001)' in the caput",
    "art-35-e": "Planalto strikes art. 35-E (ADI 1.931, undated); it is left out of every version (see the ADI 1.931 decision)",
}
_build_act12 = P.build_act


def build_act(paras, act_day, *a, **k):
    slug = ACTS[len(B7._act_order)]["slug"] if len(B7._act_order) < len(ACTS) else "?"
    versions = _build_act12(paras, act_day, *a, **k)
    if slug == _LPS:
        versions = [v for v in versions if v["from"] >= LPS_START]
        assert versions[0]["from"] == LPS_START
        versions[0]["credits"] = {}
        versions[0]["note"] = ("Oldest version available: the act as Medida Provisória nº 2.177-44 (DOU 27.8.2001) left it; "
                               "the 1998 text and the monthly reissues of the MP 1.665 chain are not modelled.")
        versions[0].pop("same_day", None)
    return versions


P.build_act = B.build_act = build_act

_inner12 = B6.PB5B._write_part5


def _inner(*a):
    B5.EXTRA_DECISIONS.extend(x + "." for x in dict.fromkeys(LCVM_ORIGINAL_USED))
    for k, rec in a[1].items():
        if k.startswith("dec-"):
            rec["kind"] = "decree"
    keep = {}
    for act in a[0]:
        if act["slug"] == _LPS:
            keep = {k: a[1][k] for k in ("lei-9656-1998", "lei-10223-2001") if k in a[1]}
            B5.EXTRA_DECISIONS.extend([LPS_WHY + ".", LPS_ADI + "."])
    rc = _inner12(*a)
    if keep:   # laws named only in earlier_laws: the part writer keeps only credited laws
        import json as _json
        part = _json.loads(B5.OUT.read_text(encoding="utf-8"))
        for k, rec in keep.items():
            part["laws"].setdefault(k, rec)
        for act in part["acts"]:
            if act["slug"] == _LPS:
                act["first_law"], act["earlier_laws"] = None, list(keep)
        t = B5.OUT.with_suffix(".json.tmp")
        t.write_text(_json.dumps(part, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8",
                     newline="\n")
        t.replace(B5.OUT)
    return rc


B6.PB5B._write_part5 = _inner

SRC = HERE / "sources_batch12.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
