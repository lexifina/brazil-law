"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch8.json (SCHEMA.md corpus part): the acts in ALL_ACTS
below (the two acts batch 7 deferred, money laundering and firearms, and further federal laws as they are verified).

    python -X utf8 scripts/brazil-law/batch8/parse_batch8.py [--stats] [--dry]

Imports ../batch7/parse_batch7.py (which configures batch 6, 5b, 5, 4, 3 and ../proc, the struck-text replay of
Planalto's annotated pages, plus batch 7's rules and the stale-wording rules) with no act of its own, and replaces only
the configuration: the acts, the in-force days, the hand tables for these acts, the pins and the output. Earlier parts
are not touched. No network.

BATCH8_ACTS=<slug,...> selects acts for trial runs (BATCH8_OUT=<file> writes elsewhere); by default VERIFIED is written.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH7_ACTS"] = "-"   # batch 7 configures no act of its own here
os.environ.pop("BATCH7_OUT", None)
sys.path.insert(0, str(FOLDER / "batch7"))
import parse_batch7 as B7  # noqa: E402

B6, B5, B4, B, P = B7.B6, B7.B5, B7.B4, B7.B, B7.P
PL = P.PL
B5.OUT = Path(os.environ.get("BATCH8_OUT") or FOLDER / "corpus.d" / "99-batch8.json")
B5.STAGE = HERE / ".tmp" / "stage.json"
P.RETRIEVED = "2026-10-31"

PAGES = {k: v for k, v in B7.PAGES.items() if k.split("-")[0] in ("edes", "llav")}
PAGES.update({
    "lch": "leis/l8072.htm",
    "lch-compilada": "leis/l8072compilada.htm",
    "lacp": "leis/l7347orig.htm",
    "lacp-compilada": "leis/l7347compilada.htm",
    "lindb": "decreto-lei/del4657.htm",
    "lindb-compilado": "decreto-lei/del4657compilado.htm",
    "lorcrim": "_ato2011-2014/2013/lei/l12850.htm",
    "lpi": "leis/l9279.htm",
    "lda": "leis/l9610.htm",
    "ejuv": "_ato2011-2014/2013/lei/l12852.htm",
    "ltur": "_ato2007-2010/2008/lei/l11771.htm",
    "lbi": "_ato2015-2018/2015/lei/l13146.htm",
})
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = B6.PAGES = B7.PAGES = PAGES


def _act(slug, short, page, consolidated, law, title, digits):
    return {"slug": slug, "short": short, "page": page, "consolidated": consolidated, "law": law, "title": title,
            "digits": digits, "url": PL + PAGES[page]}


ALL_ACTS: list[dict] = [a for a in B7.ALL_ACTS if a["page"] in PAGES] + [
    _act("lei-dos-crimes-hediondos", "LCH", "lch", "lch-compilada", "lei-8072-1990",
         "Lei dos Crimes Hediondos (Lei nº 8.072, de 25 de julho de 1990)", 2),
    _act("lei-da-acao-civil-publica", "LACP", "lacp", "lacp-compilada", "lei-7347-1985",
         "Lei da Ação Civil Pública (Lei nº 7.347, de 24 de julho de 1985)", 2),
    _act("lei-de-introducao-as-normas-do-direito-brasileiro", "LINDB", "lindb", "lindb-compilado", "dl-4657-1942",
         "Lei de Introdução às Normas do Direito Brasileiro (Decreto-Lei nº 4.657, de 4 de setembro de 1942)", 2),
    _act("lei-das-organizacoes-criminosas", "LOC", "lorcrim", "lorcrim", "lei-12850-2013",
         "Lei das Organizações Criminosas (Lei nº 12.850, de 2 de agosto de 2013)", 2),
    _act("lei-da-propriedade-industrial", "LPI", "lpi", "lpi", "lei-9279-1996",
         "Lei da Propriedade Industrial (Lei nº 9.279, de 14 de maio de 1996)", 3),
    _act("lei-de-direitos-autorais", "LDA", "lda", "lda", "lei-9610-1998",
         "Lei de Direitos Autorais (Lei nº 9.610, de 19 de fevereiro de 1998)", 3),
    _act("estatuto-da-juventude", "EJuv", "ejuv", "ejuv", "lei-12852-2013",
         "Estatuto da Juventude (Lei nº 12.852, de 5 de agosto de 2013)", 2),
    _act("lei-geral-do-turismo", "LGT", "ltur", "ltur", "lei-11771-2008",
         "Lei Geral do Turismo (Lei nº 11.771, de 17 de setembro de 2008)", 2),
    _act("estatuto-da-pessoa-com-deficiencia", "LBI", "lbi", "lbi", "lei-13146-2015",
         "Estatuto da Pessoa com Deficiência (Lei nº 13.146, de 6 de julho de 2015)", 3),
]
VERIFIED: list[str] = []
ENABLED = [s for s in os.environ.get("BATCH8_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
B7.ACTS[:] = ACTS          # batch 7's build_act wrapper names the act it fixes from this list

# In-force days of the acts, from each act's own closing clause and the DOU day Planalto prints under it (LC 95/1998 art.
# 8 § 1 counting from 26.4.2001; before that the day count of LINDB art. 1, as in batch 6)
ACT_DAY_ALL: dict[str, tuple[str, str]] = {k: v for k, v in B7.ACT_DAY_ALL.items() if k in ("lei-10826-2003", "lei-9613-1998")}
ACT_LAWS_ALL: dict[str, dict] = {k: v for k, v in B7.ACT_LAWS_ALL.items() if k in ACT_DAY_ALL}
ACT_DAY_NEW: dict[str, tuple[str, str]] = {}
ACT_LAWS_NEW: dict[str, dict] = {}
ACT_DAY_ALL.update(ACT_DAY_NEW)
ACT_LAWS_ALL.update(ACT_LAWS_NEW)
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

B.EXPLAINED.clear()
B.EXPLAINED.update({
    "estatuto-do-desarmamento": {
        "art-06": "the consolidated page prints the editorial note '(Expressões declaradas inconstitucionais pela ADIN "
                  "5538)' inside the line of inciso III; the history leaves the note out",
    },
})

SRC = HERE / "sources_batch8.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]
B6.CONTEXT[:] = []

# ---------------------------------------------------------------------------------------------------------------
# STF rulings (batch 3's COURTS format). Dates from the STF's own case records, read from archive copies (pinned as
# ctx:* in sources_batch8.json); see each 'why'.
P.COURTS = {
    "stf-adi-3964": {
        "label": "STF, ADI 3.964 (medida cautelar)", "kind": "court", "enacted": "2007-12-12", "published": "2007-12-12",
        "title": "Ação direta de inconstitucionalidade 3.964, medida cautelar: deferida para suspender a eficácia da "
                 "Medida Provisória nº 394, de 20 de setembro de 2007",
        "url": "https://portal.stf.jus.br/processos/detalhe.asp?incidente=2560579",
        "from": "2007-12-12", "case": r"3\.?964", "where": [],
        "why": "STF, ADI 3.964 MC (Plenário, 12.12.2007): 'O Tribunal, por maioria, nos termos do voto do Relator, deferiu "
               "a medida cautelar para suspender a eficácia da Medida Provisória nº 394, de 20 de setembro de 2007' (the "
               "STF's case summary, archived 18.7.2014; acórdão DJ 11.4.2008). MP 394 had rewritten only Estatuto do "
               "Desarmamento art. 5 § 3º (and the table of fees in its annex, not modelled); with its efficacy "
               "suspended the wording in force before it applies again (Lei 9.868/1999 art. 11 § 2). The STF summary "
               "gives the session day and the acórdão's DJ, not the DJ day of the session's ata, so the change is "
               "dated the session day, 12.12.2007; MP 417/2008 replaced the paragraph from 1.2.2008 either way. The "
               "Chamber of Deputies' record of MP 394 notes the suspension ('Suspensa a eficácia e a tramitação desta "
               "MPV, em face de liminar deferida pelo Supremo Tribunal Federal na Ação Direta de Inconstitucionalidade "
               "nº 3.964/2007') and that it was declared prejudicada on 7.2.2013 after Lei 11.706/2008"},
}

# ---------------------------------------------------------------------------------------------------------------
# Paragraph fixes before the replay
# (a) label slips: (act page, line start, corrected start, label, why)
LABEL_FIX: list[tuple[str, str, str, str, str]] = [
    ("llav", "2º Caberá recurso das decisões do COAF", "§ 2º Caberá recurso das decisões do COAF", "§ 2º",
     "Lei de Lavagem art. 16: the wording Medida Provisória nº 784/2017 gave § 2º is printed '2º Caberá recurso ...' "
     "(no '§'); read as '§ 2º', the paragraph it rewrote ('Art. 1º ... § 2º Caberá recurso das decisões do COAF', MP "
     "784's own text)"),
]
LABEL_USED: list[str] = []
# (b) a line with words struck by a court whose note is printed inside the text: (act page, unit, label, note) -> two
#     wordings, the full line (struck words kept) and the unstruck words, the note dropped from both; their days are
#     set in SPAN_FIX
COURT_SPLIT: list[tuple[str, str, str, str]] = [
    ("edes", "art-06", "III -", "(Expressões declaradas inconstitucionais pela ADIN 5538)"),
]
_paragraphs8 = P.paragraphs
_PAGE_OF_HTML: dict[int, str] = {}


def paragraphs(html: str, digits: int):
    out, rest = _paragraphs8(html, digits)
    page = CURRENT_PAGE[0]
    res = []
    for p in out:
        hit = next((c for c in COURT_SPLIT if c[0] == page and p["unit"] == c[1] and p["label"] == c[2]
                    and p["state"] == "mixed" and c[3] in p["text"]), None)
        if hit is None:
            res.append(p)
            continue
        base = {k: v for k, v in p.items() if k not in ("text", "state", "notes", "plain_text", "struck_text")}
        for state, t in (("struck", p["text"]), ("plain", p["plain_text"])):
            t = P.norm(t.replace(hit[3], " "))
            t = re.sub(r"\s+([,;.])", r"\1", t)
            res.append({**base, "text": t, "state": state, "notes": list(p["notes"]), "plain_text": "",
                        "struck_text": "", "court_split": state})
    out = res
    for i, p in enumerate(out):
        p["i"] = i
    for p in out:
        for pg, start, fixed, label, why in LABEL_FIX:
            if pg == page and p["text"].startswith(start):
                p["text"] = fixed + p["text"][len(start):]
                p["label"] = label
                LABEL_USED.append(why)
    return out, rest


CURRENT_PAGE = [""]
_raw8 = P.raw


def raw(ident: str):
    CURRENT_PAGE[0] = ident
    return _raw8(ident)


P.raw = raw
P.paragraphs = B.paragraphs = paragraphs

# ---------------------------------------------------------------------------------------------------------------
# Life spans set by hand where the replay cannot read them from the page: chains of Medidas Provisórias that were
# revoked, suspended by the STF or converted without the change. Each entry names one printed line: (act, unit, label,
# line start, n-th such line from the top, counting 0) -> fields, why. Lines set here are 'pinned' (the stale-wording
# rules leave them alone).
D = "2019-06-18"      # Lei 13.844/2019 (conversion of MP 870, its art. 72 on Lei 9.613 vetoed), DOU 18.6.2019 extra
SPAN_FIX: list[tuple[tuple[str, str, str, str, int], dict, str]] = []
_W870 = ("Medida Provisória nº 870/2019 (DOU 1.1.2019) art. 72 moved the COAF to the Ministério da Justiça e Segurança "
         "Pública, rewriting Lei 9.613 arts. 14 and 16; its conversion law, Lei 13.844/2019 (DOU 18.6.2019, edição extra; "
         "in force on publication), has 'Seção XI - Das Alterações no Conselho de Controle de Atividades Financeiras - "
         "Art. 72. (VETADO)', so MP 870's wording ended on 18.6.2019 and the earlier wording stood again until MP "
         "886/2019 (DOU 19.6.2019) rewrote the articles")
_W893 = ("Medida Provisória nº 893/2019 (DOU 20.8.2019, in force on publication) art. 15: 'Ficam revogados os seguintes "
         "dispositivos da Lei nº 9.613, de 1998: I - o art. 13; II - o art. 16; e III - o art. 17' (converted, Lei "
         "13.974/2020); MP 886's wording of art. 16 ended then. Planalto prints the Lei 12.683 wording once more under "
         "the revocation notes; it never stood again (MP 886's conversion law, Lei 13.901/2019, leaves out Lei 9.613)")
SPAN_FIX += [
    (("lei-de-lavagem-de-dinheiro", "art-14", "Art. 14", "Art. 14. Fica criado, no âmbito do Ministério da Justiça", 0),
     {"end": D, "end_law": "lei-13844-2019", "end_how": "conversion-without"}, _W870),
    (("lei-de-lavagem-de-dinheiro", "art-14", "Art. 14", "Art. 14. É criado, no âmbito do Ministério da Fazenda", 1),
     {"start": D, "start_law": "lei-13844-2019"}, _W870),
    (("lei-de-lavagem-de-dinheiro", "art-16", "Art. 16", "Art. 16. O COAF será composto por servidores públicos de "
      "reputação ilibada e reconhecida competência, designados em ato do Ministro de Estado da Justiça", 0),
     {"end": D, "end_law": "lei-13844-2019", "end_how": "conversion-without"}, _W870),
    (("lei-de-lavagem-de-dinheiro", "art-16", "Art. 16", "Art. 16. O Coaf será composto por servidores públicos de "
      "reputação ilibada e reconhecida competência, designados em ato do Ministro de Estado da Fazenda", 1),
     {"start": D, "start_law": "lei-13844-2019"}, _W870),
    (("lei-de-lavagem-de-dinheiro", "art-16", "§ 1º", "§ 1º O Presidente do COAF será indicado pelo Ministro de Estado da "
      "Justiça", 0), {"end": D, "end_law": "lei-13844-2019", "end_how": "conversion-without"}, _W870),
    (("lei-de-lavagem-de-dinheiro", "art-16", "§ 1º", "§ 1º O Presidente do Conselho será nomeado", 1),
     {"start": D, "start_law": "lei-13844-2019"}, _W870),
    (("lei-de-lavagem-de-dinheiro", "art-16", "Art. 16", "Art. 16. O Coaf será composto por servidores públicos de "
      "reputação ilibada e reconhecida competência, designados em ato do Ministro de Estado da Economia", 0),
     {"end": "2019-08-20", "end_law": "mp-893-2019", "end_how": "note"}, _W893),
    (("lei-de-lavagem-de-dinheiro", "art-16", "§ 1º", "§ 1º O Presidente do Coaf será indicado pelo Ministro de Estado da "
      "Economia", 0), {"end": "2019-08-20", "end_law": "mp-893-2019", "end_how": "note"}, _W893),
    (("lei-de-lavagem-de-dinheiro", "art-16", "Art. 16", "Art. 16. O Coaf será composto por servidores públicos de "
      "reputação ilibada e reconhecida competência, designados em ato do Ministro de Estado da Fazenda", 2),
     {"skip": True}, _W893),
    (("lei-de-lavagem-de-dinheiro", "art-16", "§ 1º", "§ 1º O Presidente do Conselho será nomeado", 2),
     {"skip": True}, _W893),
    (("lei-de-lavagem-de-dinheiro", "art-16", "§ 2º", "§ 2º Caberá recurso das decisões do Coaf", 0),
     {"end": "2019-08-20", "end_law": "mp-893-2019", "end_how": "note"},
     "Lei de Lavagem art. 16 § 2º in Lei 13.506/2017's wording is printed unstruck although its notes say '(Revogado "
     "pela Medida Provisória nº 893, de 2019)' and '(Revogado pela Lei nº 13.974, de 2020)': MP 893 art. 15 revoked the "
     "whole of art. 16, so it ends on 20.8.2019 (the consolidated page leaves art. 16 out)"),
]
_E = "estatuto-do-desarmamento"
F379 = {"end": "2007-09-18", "end_law": "mp-390-2007", "end_how": "revoked-mp"}
G379 = [("2007-06-29", "2007-09-18", "mp-379-2007", "mp-390-2007")]
_W379 = ("Medida Provisória nº 379/2007 (DOU 29.6.2007) rewrote Estatuto do Desarmamento arts. 5 § 3º, 6 §§ 1º-2º, 11 § 2º "
         "and 28 and added arts. 5 § 4º, 11 § 3º and 11-A; Medida Provisória nº 390/2007 (DOU 18.9.2007, edição extra; in "
         "force on publication; converted, Lei 11.579/2007) art. 1: 'Fica revogada a Medida Provisória nº 379, de 28 de "
         "junho de 2007'. MP 379's wordings end on 18.9.2007 and the wordings in force before it stand again (Planalto "
         "prints them once more with the note 'Vide Medida Provisória nº 390, de 2007', or, for art. 6 § 1º, unnoted "
         "under MP 379's wording)")
_W379b = ("Estatuto do Desarmamento art. 11 § 2º: under the note 'Vide Medida Provisória nº 390, de 2007' Planalto prints "
          "the wording Medida Provisória nº 417/2008 later gave the paragraph, not the 2003 wording that MP 390's "
          "revocation of MP 379 restored; the 2003 wording (printed first) stands from 18.9.2007 until MP 417, and the "
          "line under the MP 390 note is left out")
_W394 = ("Estatuto do Desarmamento art. 5 § 3º: Medida Provisória nº 394/2007 (DOU 21.9.2007) rewrote it; the STF "
         "suspended MP 394's efficacy (ADI 3.964 MC, 12.12.2007, see the ruling), so the wording in force before it (the "
         "2003 wording, restored by MP 390) stands again from 12.12.2007 until Medida Provisória nº 417/2008 (in force "
         "1.2.2008)")
_W5948 = ("Estatuto do Desarmamento art. 6 III and IV: STF, ADI 5.948 MC (decisão monocrática, Min. Alexandre de Moraes, "
          "29.6.2018, ad referendum do Plenário): 'CONCEDO A MEDIDA CAUTELAR PLEITEADA [...] DETERMINANDO A IMEDIATA "
          "SUSPENSÃO DA EFICÁCIA das expressões das capitais dos Estados e com mais de 500.000 (quinhentos mil) "
          "habitantes, no inciso III, bem como o inciso IV, ambos do art. 6º da Lei Federal nº 10.826/2003'; the "
          "Plenário made it final in ADI 5.538, ADI 5.948 and ADC 38 (virtual session ended 27.2.2021, Informativo STF "
          "1007), changing no further words. Planalto strikes the words noting ADIN 5538; the history drops them from "
          "29.6.2018, the decision's day (the DJe day of its publication is not in the records read), credited to the "
          "cautelar")
SPAN_FIX += [
    ((_E, "art-05", "§ 3º", "", 1), F379, _W379),
    ((_E, "art-05", "§ 3º", "", 2), {"start": "2007-09-18", "start_law": "mp-390-2007", "end": "2008-02-01",
                                     "end_law": "mp-417-2008", "end_how": "successor",
                                     "gaps": [("2007-09-21", "2007-12-12", "mp-394-2007", "stf-adi-3964")]}, _W394),
    ((_E, "art-05", "§ 3º", "", 3), {"end": "2007-12-12", "end_law": "stf-adi-3964", "end_how": "court"}, _W394),
    ((_E, "art-05", "§ 4º", "", 0), F379, _W379),
    ((_E, "art-06", "§ 1º", "", 0), F379, _W379),
    ((_E, "art-06", "§ 1º", "", 1), {"start": "2003-12-23", "start_law": None, "gaps": G379, "end": "2008-06-20",
                                     "end_law": "lei-11706-2008", "end_how": "successor"}, _W379),
    ((_E, "art-06", "§ 2º", "", 0), F379, _W379),
    ((_E, "art-06", "§ 2º", "", 1), {"start": "2003-12-23", "start_law": None, "gaps": G379, "end": "2008-02-01",
                                     "end_law": "mp-417-2008", "end_how": "successor"}, _W379),
    ((_E, "art-11", "§ 2º", "", 0), {"gaps": G379, "end": "2008-02-01", "end_law": "mp-417-2008",
                                     "end_how": "successor"}, _W379b),
    ((_E, "art-11", "§ 2º", "", 1), F379, _W379),
    ((_E, "art-11", "§ 2º", "", 2), {"skip": True}, _W379b),
    ((_E, "art-11", "§ 3º", "", 0), F379, _W379),
    ((_E, "art-11-a", "Art. 11-A", "", 0), F379, _W379),
    ((_E, "art-11-a", "§ 1º", "", 0), F379, _W379),
    ((_E, "art-11-a", "§ 2º", "", 0), F379, _W379),
    ((_E, "art-11-a", "§ 3º", "", 0), F379, _W379),
    ((_E, "art-28", "Art. 28", "", 1), F379, _W379),
    ((_E, "art-28", "Art. 28", "", 2), {"start": "2007-09-18", "start_law": "mp-390-2007"}, _W379),
    ((_E, "art-06", "III -", "III - os integrantes das guardas municipais das capitais", 0),
     {"end": "2018-06-29", "end_law": "stf-adi-5948", "end_how": "court"}, _W5948),
    ((_E, "art-06", "III -", "III - os integrantes das guardas municipais e dos Municípios", 0),
     {"start": "2018-06-29", "start_law": "stf-adi-5948", "end": None, "end_law": None, "end_how": None}, _W5948),
    ((_E, "art-06", "IV -", "IV - os integrantes das guardas municipais dos Municípios com mais de 50.000", 0),
     {"end": "2018-06-29", "end_law": "stf-adi-5948", "end_how": "court"}, _W5948),
]
P.COURTS["stf-adi-5948"] = {
    "label": "STF, ADI 5.948 (medida cautelar)", "kind": "court", "enacted": "2018-06-29", "published": "2018-06-29",
    "title": "Ação direta de inconstitucionalidade 5.948, medida cautelar: suspende a eficácia das expressões 'das capitais "
             "dos Estados' e 'com mais de 500.000 (quinhentos mil) habitantes', no inciso III, e do inciso IV do art. 6º da "
             "Lei nº 10.826, de 2003",
    "url": "https://www.stf.jus.br/arquivo/cms/noticiaNoticiaStf/anexo/ADI5948MCGuardasmunicipais.pdf",
    "from": "2018-06-29", "case": r"5\.?948", "where": [], "why": _W5948}
P.MP_PENDING.update({
    "mp-379-2007": "Medida Provisória nº 379, de 28.6.2007 (DOU 29.6.2007), 'Revogada pela Medida Provisória nº 390, de "
                   "2007' and 'Revogada pela Lei nº 11.579, de 2007' on its page: its wordings end on 18.9.2007 (set by "
                   "hand, see the life-span decisions)",
    "mp-394-2007": "Medida Provisória nº 394, de 20.9.2007 (DOU 21.9.2007): efficacy suspended by the STF (ADI 3.964 MC, "
                   "12.12.2007), declared prejudicada on 7.2.2013 (Chamber of Deputies' record); its wording ends on "
                   "12.12.2007 (set by hand)",
})
SPAN_USED: list[str] = []
SPAN_MISSED: list[str] = []
_lifespans8 = P.lifespans


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def apply_span_fix(paras: list[dict], act_slug: str, record: bool) -> None:
    for (act, unit, label, start, nth), fields, why in SPAN_FIX:
        if act != act_slug:
            continue
        hits = [p for p in paras if p["unit"] == unit and p["label"] == label and _norm(p["text"]).startswith(_norm(start))
                and not p["heading"]]
        if len(hits) <= nth:
            if record:
                SPAN_MISSED.append(f"{act} {unit} [{label}] #{nth} {start[:50]!r}")
            continue
        p = hits[nth]
        if "gaps" in fields:
            fields = dict(fields, gaps=[tuple(g) for g in fields["gaps"]])
        p.update(fields)
        p["pinned"] = True
        if record:
            SPAN_USED.append(why)


def lifespans(paras: list[dict], cx) -> list[str]:
    problems = _lifespans8(paras, cx)
    apply_span_fix(paras, cx.act, True)
    # an 'ends before it starts' problem on a line set aside here by hand is settled
    left_out = {f"{p['unit']} [{p['label']}] {p['start']}" for p in paras if p.get("pinned") and p.get("skip")}
    problems = [x for x in problems if not (x.startswith("ends before it starts: ")
                                            and x[len("ends before it starts: "):].split("..")[0] in left_out)]
    problems += [f"span fix not matched: {x}" for x in SPAN_MISSED if x.split()[0] == cx.act]
    return problems


_apply_rewrites8 = P.apply_rewrites


def apply_rewrites(paras, act, eff, problems):
    """parse_proc's rewrite rules (date-order chains, renumbered copies) run after the life spans; the hand-set spans
    are put back after them."""
    out = _apply_rewrites8(paras, act, eff, problems)
    apply_span_fix(paras, act["slug"], False)
    return out


P.apply_rewrites = B.apply_rewrites = apply_rewrites
P.lifespans = B.lifespans = lifespans

_inner8 = B6.PB5B._write_part5


def _inner(*a) -> int:
    if LABEL_USED:
        B5.EXTRA_DECISIONS.append("Label slips read as the label they stand for: " + "; ".join(dict.fromkeys(LABEL_USED)) + ".")
    if SPAN_USED:
        B5.EXTRA_DECISIONS.append("Life spans set by hand where Planalto's page cannot give them (Medidas Provisórias "
                                  "revoked, suspended by the STF or converted without the change): "
                                  + "; ".join(dict.fromkeys(SPAN_USED)) + ".")
    return _inner8(*a)


B6.PB5B._write_part5 = _inner

# batch 7's build_act wrapper (stale-wording rules) runs on these acts; it is reached through P.build_act
_build_act8 = B7._build_act7

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
