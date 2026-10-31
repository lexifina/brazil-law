"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch7.json (SCHEMA.md corpus part): the acts in ALL_ACTS
below (city statute, older persons, penal execution, corporations, startups, domestic violence, firearms, fiscal
responsibility, writ of mandamus, money laundering).

    python -X utf8 scripts/brazil-law/batch7/parse_batch7.py [--stats] [--dry]

Imports ../batch6/parse_batch6.py (which configures batch 5b, 5, 4, 3 and ../proc, the struck-text replay of Planalto's
annotated pages, plus batch 6's rules) and replaces only its configuration: the acts, the in-force days, the hand tables
for these acts, the pins and the output. Earlier parts are not touched. No network.

BATCH7_ACTS=<slug,...> selects acts for trial runs (BATCH7_OUT=<file> writes elsewhere); by default VERIFIED is written.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ.setdefault("BATCH6_ACTS", "-")   # batch 6 configures no act of its own here
sys.path.insert(0, str(FOLDER / "batch6"))
import parse_batch6 as B6  # noqa: E402

B5, B4, B, P = B6.B5, B6.B4, B6.B, B6.P
PL = P.PL
B5.OUT = Path(os.environ.get("BATCH7_OUT") or FOLDER / "corpus.d" / "99-batch7.json")
B5.STAGE = HERE / ".tmp" / "stage.json"
P.RETRIEVED = "2026-10-31"

PAGES = {
    "ecid": "leis/leis_2001/l10257.htm",
    "eido": "leis/2003/l10.741.htm",
    "eido-compilado": "leis/2003/l10.741compilado.htm",
    "lep": "leis/l7210.htm",
    "lep-compilado": "leis/l7210compilado.htm",
    "lsa": "leis/l6404consol.htm",
    "lsa-compilada": "leis/l6404compilada.htm",
    "lcp182": "leis/lcp/lcp182.htm",
    "lmp": "_ato2004-2006/2006/lei/l11340.htm",
    "edes": "leis/2003/l10.826.htm",
    "edes-compilado": "leis/2003/l10.826compilado.htm",
    "lcp101": "leis/lcp/lcp101.htm",
    "lms": "_ato2007-2010/2009/lei/l12016.htm",
    "llav": "leis/l9613.htm",
    "llav-compilado": "leis/l9613compilado.htm",
}
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = PAGES
B6.PAGES = PAGES


def _act(slug, short, page, consolidated, law, title, digits):
    return {"slug": slug, "short": short, "page": page, "consolidated": consolidated, "law": law, "title": title,
            "digits": digits, "url": PL + PAGES[page]}


ALL_ACTS: list[dict] = [
    _act("estatuto-da-cidade", "ECid", "ecid", "ecid", "lei-10257-2001",
         "Estatuto da Cidade (Lei nº 10.257, de 10 de julho de 2001)", 2),
    _act("estatuto-da-pessoa-idosa", "EIdo", "eido", "eido-compilado", "lei-10741-2003",
         "Estatuto da Pessoa Idosa (Lei nº 10.741, de 1º de outubro de 2003)", 3),
    _act("lei-de-execucao-penal", "LEP", "lep", "lep-compilado", "lei-7210-1984",
         "Lei de Execução Penal (Lei nº 7.210, de 11 de julho de 1984)", 3),
    _act("lei-das-sociedades-por-acoes", "LSA", "lsa", "lsa-compilada", "lei-6404-1976",
         "Lei das Sociedades por Ações (Lei nº 6.404, de 15 de dezembro de 1976)", 3),
    _act("marco-legal-das-startups", "MLS", "lcp182", "lcp182", "lc-182-2021",
         "Marco Legal das Startups (Lei Complementar nº 182, de 1º de junho de 2021)", 2),
    _act("lei-maria-da-penha", "LMP", "lmp", "lmp", "lei-11340-2006",
         "Lei Maria da Penha (Lei nº 11.340, de 7 de agosto de 2006)", 2),
    _act("estatuto-do-desarmamento", "EDes", "edes", "edes-compilado", "lei-10826-2003",
         "Estatuto do Desarmamento (Lei nº 10.826, de 22 de dezembro de 2003)", 2),
    _act("lei-de-responsabilidade-fiscal", "LRF", "lcp101", "lcp101", "lc-101-2000",
         "Lei de Responsabilidade Fiscal (Lei Complementar nº 101, de 4 de maio de 2000)", 2),
    _act("lei-do-mandado-de-seguranca", "LMS", "lms", "lms", "lei-12016-2009",
         "Lei do Mandado de Segurança (Lei nº 12.016, de 7 de agosto de 2009)", 2),
    _act("lei-de-lavagem-de-dinheiro", "LLav", "llav", "llav-compilado", "lei-9613-1998",
         "Lei de Lavagem de Dinheiro (Lei nº 9.613, de 3 de março de 1998)", 2),
]
VERIFIED: list[str] = ["estatuto-da-cidade", "estatuto-da-pessoa-idosa", "lei-de-execucao-penal",
                        "lei-das-sociedades-por-acoes", "marco-legal-das-startups", "lei-maria-da-penha",
                        "lei-de-responsabilidade-fiscal", "lei-do-mandado-de-seguranca"]
ENABLED = [s for s in os.environ.get("BATCH7_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = ACTS
B6.ACTS = ACTS

# In-force days of the acts, from each act's own closing clause and the DOU day Planalto prints under it (LC 95/1998 art.
# 8 § 1 counting from 26.4.2001; Lei 810/1949 before that)
ACT_DAY_ALL: dict[str, tuple[str, str]] = {
    "lei-10257-2001": ("2001-10-09", "Lei 10.257/2001 art. 58: 'Esta Lei entra em vigor após decorridos noventa dias de sua "
                                     "publicação' (DOU 11.7.2001): the 90th day counted from publication is 8.10.2001 (LC "
                                     "95/1998 art. 8 § 1). The retificação in the DOU of 17.7.2001 corrects only the "
                                     "signatures ('Na página 5, 1ª coluna, nas assinaturas, leia-se: ...', as the Chamber of "
                                     "Deputies' record of the law gives it), so it does not restart the period (LINDB art. 1 "
                                     "§ 3)"),
    "lei-10741-2003": ("2004-01-01", "Lei 10.741/2003 art. 118: 'Esta Lei entra em vigor decorridos 90 (noventa) dias da sua "
                                     "publicação, ressalvado o disposto no caput do art. 36, que vigorará a partir de 1º de "
                                     "janeiro de 2004' (DOU 3.10.2003): the 90th day counted from publication is 31.12.2003 "
                                     "(LC 95/1998 art. 8 § 1), so the whole law, art. 36 included, is in force from 1.1.2004"),
    "lei-7210-1984": ("1985-01-13", "Lei 7.210/1984 art. 204: 'Esta Lei entra em vigor concomitantemente com a lei de reforma "
                                    "da Parte Geral do Código Penal', Lei 7.209/1984 (DOU 13.7.1984), whose art. 5 puts it in "
                                    "force six months after publication, on 13.1.1985 (as in this corpus' Código Penal)"),
    "lei-6404-1976": ("1977-02-15", "Lei 6.404/1976 art. 300: 'A presente Lei entrará em vigor 60 (sessenta) dias após a sua "
                                    "publicação, aplicando-se, todavia, a partir da data da publicação, às companhias que se "
                                    "constituírem' (DOU 17.12.1976): in force 60 days after publication, on 15.2.1977; for "
                                    "companies formed from 17.12.1976 it applied from publication"),
    "lc-182-2021": ("2021-08-31", "Lei Complementar 182/2021 art. 18: 'Esta Lei Complementar entra em vigor após decorridos 90 "
                                  "(noventa) dias de sua publicação oficial' (DOU 2.6.2021): the 90th day counted from "
                                  "publication is 30.8.2021 (LC 95/1998 art. 8 § 1). The retificação in the DOU of 4.6.2021 "
                                  "corrects only the signatures, as the Chamber of Deputies' record of the law gives it"),
    "lei-11340-2006": ("2006-09-22", "Lei 11.340/2006 art. 46: 'Esta Lei entra em vigor 45 (quarenta e cinco) dias após sua "
                                     "publicação' (DOU 8.8.2006): the 45th day counted from publication is 21.9.2006 (LC "
                                     "95/1998 art. 8 § 1)"),
    "lei-10826-2003": ("2003-12-23", "Lei 10.826/2003 art. 37: 'Esta Lei entra em vigor na data de sua publicação' (DOU "
                                     "23.12.2003)"),
    "lc-101-2000": ("2000-05-05", "Lei Complementar 101/2000 art. 75: 'Esta Lei Complementar entra em vigor na data da sua "
                                  "publicação' (DOU 5.5.2000)"),
    "lei-12016-2009": ("2009-08-10", "Lei 12.016/2009 art. 29: 'Esta Lei entra em vigor na data de sua publicação' (DOU "
                                     "10.8.2009)"),
    "lei-9613-1998": ("1998-03-04", "Lei 9.613/1998 art. 18: 'Esta Lei entra em vigor na data de sua publicação' (DOU "
                                    "4.3.1998)"),
}
ACT_LAWS_ALL: dict[str, dict] = {
    "lei-10257-2001": B._act_law("Lei nº 10.257, de 2001", "Regulamenta os arts. 182 e 183 da Constituição Federal, "
                                 "estabelece diretrizes gerais da política urbana e dá outras providências.", "2001-07-10",
                                 "2001-07-11", PAGES["ecid"]),
    "lei-10741-2003": B._act_law("Lei nº 10.741, de 2003", "Dispõe sobre o Estatuto do Idoso e dá outras providências.",
                                 "2003-10-01", "2003-10-03", PAGES["eido"]),
    "lei-7210-1984": B._act_law("Lei nº 7.210, de 1984", "Institui a Lei de Execução Penal.", "1984-07-11", "1984-07-13",
                                PAGES["lep"]),
    "lei-6404-1976": B._act_law("Lei nº 6.404, de 1976", "Dispõe sobre as Sociedades por Ações.", "1976-12-15",
                                "1976-12-17", PAGES["lsa"]),
    "lc-182-2021": B._act_law("Lei Complementar nº 182, de 2021", "Institui o marco legal das startups e do empreendedorismo "
                              "inovador; e altera a Lei nº 6.404, de 15 de dezembro de 1976, e a Lei Complementar nº 123, "
                              "de 14 de dezembro de 2006.", "2021-06-01", "2021-06-02", PAGES["lcp182"]),
    "lei-11340-2006": B._act_law("Lei nº 11.340, de 2006", "Cria mecanismos para coibir a violência doméstica e familiar "
                                 "contra a mulher, nos termos do § 8º do art. 226 da Constituição Federal, da Convenção sobre "
                                 "a Eliminação de Todas as Formas de Discriminação contra as Mulheres e da Convenção "
                                 "Interamericana para Prevenir, Punir e Erradicar a Violência contra a Mulher; dispõe sobre a "
                                 "criação dos Juizados de Violência Doméstica e Familiar contra a Mulher; altera o Código de "
                                 "Processo Penal, o Código Penal e a Lei de Execução Penal; e dá outras providências.",
                                 "2006-08-07", "2006-08-08", PAGES["lmp"]),
    "lei-10826-2003": B._act_law("Lei nº 10.826, de 2003", "Dispõe sobre registro, posse e comercialização de armas de fogo "
                                 "e munição, sobre o Sistema Nacional de Armas – Sinarm, define crimes e dá outras "
                                 "providências.", "2003-12-22", "2003-12-23", PAGES["edes"]),
    "lc-101-2000": B._act_law("Lei Complementar nº 101, de 2000", "Estabelece normas de finanças públicas voltadas para a "
                              "responsabilidade na gestão fiscal e dá outras providências.", "2000-05-04", "2000-05-05",
                              PAGES["lcp101"]),
    "lei-12016-2009": B._act_law("Lei nº 12.016, de 2009", "Disciplina o mandado de segurança individual e coletivo e dá "
                                 "outras providências.", "2009-08-07", "2009-08-10", PAGES["lms"]),
    "lei-9613-1998": B._act_law("Lei nº 9.613, de 1998", "Dispõe sobre os crimes de \"lavagem\" ou ocultação de bens, "
                                "direitos e valores; a prevenção da utilização do sistema financeiro para os ilícitos "
                                "previstos nesta Lei; cria o Conselho de Controle de Atividades Financeiras - COAF, e dá "
                                "outras providências.", "1998-03-03", "1998-03-04", PAGES["llav"]),
}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# parse_proc starts an act at its 'LEI Nº' / 'DECRETO-LEI Nº' title line; a Lei Complementar's title ('LEI COMPLEMENTAR
# Nº 101, DE 4 DE MAIO DE 2000') is read as the same kind of line. The title line itself is not part of any unit.
_analyse7 = P.analyse
LC_TITLE = re.compile(r"^LEI\s+COMPLEMENTAR\s+(N.*)$")


def analyse(block: dict) -> dict:
    d = _analyse7(block)
    m = LC_TITLE.match(d["text"])
    if m:
        d = dict(d, text="LEI " + m.group(1))
    return d


P.analyse = analyse

# A paragraph or § printed centred (Lei 6.404 art. 221 Parágrafo único) is read by parse_proc as a heading line; a line
# that starts with a dispositivo label below an article belongs to that article.
LABELLED = re.compile(r"^(?:Parágrafo\s+único|§\s*\d+)")
HEADING_LABEL_FIX: list[str] = []
_paragraphs7 = P.paragraphs


def paragraphs(html: str, digits: int):
    out, rest = _paragraphs7(html, digits)
    for i, p in enumerate(out):
        if not (p["heading"] and LABELLED.match(p["text"])):
            continue
        prev = next((q for q in reversed(out[:i]) if not q["heading"]), None)
        if prev is None or not prev["unit"].startswith("art-"):
            continue
        p.update(heading=False, unit=prev["unit"], label=P.label_of(p["text"]))
        HEADING_LABEL_FIX.append(f"{prev['unit']} [{p['label']}]")
    for p in out:
        # notes with a typing slip (P.NOTE_FIX) are corrected in place, so the start/end patterns read them too
        p["notes"] = [P.NOTE_FIX.get(n, (n,))[0] for n in p["notes"]]
        for end, fixed, why in STRAY_LINKS:
            if p["text"].endswith(end):
                p["text"] = p["text"][: len(p["text"]) - len(end)] + fixed
                STRAY_USED.append(why)
    return out, rest


# Stray link text at the end of a line (a decree number printed as a bare link, left from a removed 'Vide' note):
# (line end, corrected end, why). Only the stray text is dropped.
STRAY_LINKS: list[tuple[str, str, str]] = [
    ("aos presos e às presas. 7.627", "aos presos e às presas.",
     "Lei de Execução Penal art. 18-A § 3º: the annotated page prints a bare link '7.627' (to Decreto nº 7.627, de 2011) "
     "after the full stop; the consolidated page does not"),
]
STRAY_USED: list[str] = []


P.paragraphs = B.paragraphs = paragraphs

B.EXPLAINED.clear()
_QUOTED = ("label-only lines inside the quoted text of an amendment to another law ('{x}', standing for a paragraph the "
           "amendment leaves unchanged); the check drops label-only lines from the consolidated page only")
B.EXPLAINED.update({
    "lei-das-sociedades-por-acoes": {
        "art-041": "typesetting: a line of art. 41 ends 'a instituição depositária' on the annotated page and with a full "
                   "stop on the consolidated page",
        "art-064": "the consolidated page (l6404compilada.htm) still prints the wording of art. 64 III before Lei "
                   "14.711/2023; the annotated page (l6404consol.htm) has Lei 14.711's wording, which the history follows",
        "art-250": "typesetting: in art. 250 III the annotated page strikes only the hyphen after 'III' (noted 'Redação "
                   "dada pela Lei nº 11.941, de 2009'); the consolidated page prints 'III as parcelas'",
        "art-255": "the consolidated page keeps the placeholder '§§ 1º e 2º (Revogados pela Lei nº 9.457, de 1997)'; the "
                   "history leaves revoked text out",
    },
    "estatuto-da-pessoa-idosa": {
        "art-045": "the consolidated page prints 'V - abrigo em entidade;' twice; the annotated page once",
        "art-110": _QUOTED.format(x="§ 3º. / § 1º."), "art-112": _QUOTED.format(x="§ 4º."),
        "titulos": "typesetting: one heading is printed on one line on the annotated page and on two on the consolidated "
                   "page ('Da Apuração Administrativa de Infração às Normas de Proteção à Pessoa Idosa')",
    },
    "marco-legal-das-startups": {"art-17": _QUOTED.format(x="§ 4º.")},
    "lei-de-execucao-penal": {
        "art-009-a": "the consolidated page leaves out § 1º (Incluído pela Lei nº 12.654, de 2012), which no law revoked: "
                     "Lei 15.295/2025 art. 1 rewrites only the caput and §§ 5, 6, 7, 9 and 10 of art. 9º-A",
        "art-016": "typesetting: 'Art. 16.' (annotated) / 'Art. 16 -' (consolidated)",
        "art-018-a": "the stray '7.627' link text after § 3º (see the stray-link decision) is dropped; the consolidated "
                     "page does not print it",
        "art-019": "typesetting: 'Art. 19 -' (annotated) / 'Art. 19.' (consolidated)", "art-035": "typesetting, as art. 19",
        "art-036": "typesetting, as art. 19", "art-038": "typesetting, as art. 19", "art-039": "typesetting, as art. 19",
        "titulos": "capitalisation of one heading: 'Do trabalho interno' (annotated) / 'Do Trabalho Interno' (consolidated)",
    },
})
B6.NEVER_IN_FORCE.clear()
B6.MP_CHAINS.clear()
B6.REISSUES.clear()

# ---------------------------------------------------------------------------------------------------------------
# hand tables for these acts, each read from the official pages named in the reason
P.NOTE_FIX = {
    "(Redação dada pela Lei nº 11.673, 2008)": (
        "(Redação dada pela Lei nº 11.673, de 2008)",
        "Estatuto da Cidade art. 50: the note reads 'Lei nº 11.673, 2008' (no 'de'); its link is "
        "_Ato2007-2010/2008/Lei/L11673.htm, Lei nº 11.673, de 8.5.2008, whose art. 1 gives art. 50 that wording"),
}
# laws whose vigência clause is staged or not machine-readable: key -> (day, reason)
P.VIGENCIA_FIXED.update({
    "lei-11638-2007": ("2008-01-01", "art. 10: 'Esta Lei entra em vigor no primeiro dia do exercício seguinte ao de sua "
                                     "publicação' (DOU 28.12.2007, edição extra): 1.1.2008"),
    "lei-14711-2023": ("2023-10-31", "art. 26: 'Esta Lei entra em vigor: I - (VETADO); II - na data de sua publicação, quanto "
                                     "aos demais dispositivos' (DOU 31.10.2023)"),
    "lc-178-2021": ("2021-01-14", "art. 32: 'Esta Lei Complementar entra em vigor: I - em relação a seu art. 16, "
                                  "especificamente no que altera o art. 51 da Lei Complementar nº 101 [...] a partir de 2022; "
                                  "II - em relação a seu art. 16, especificamente no que altera o art. 42 [...] a partir de "
                                  "2023; III - em relação às demais disposições, na data de sua publicação' (DOU 14.1.2021); "
                                  "its changes to LRF arts. 51 and 42 are dated 1.1.2022 and 1.1.2023"),
})
P.VIGENCIA_PROVISION.update({
    ("lc-178-2021", "lei-de-responsabilidade-fiscal", "art-51"): ("2022-01-01", "Lei Complementar 178/2021 art. 32, I"),
    ("lc-178-2021", "lei-de-responsabilidade-fiscal", "art-42"): ("2023-01-01", "Lei Complementar 178/2021 art. 32, II"),
    # Lei 13.818/2019 art. 3: 'Esta Lei entra em vigor na data de sua publicação, à exceção do art. 1º, que entra em vigor
    # em 1º de janeiro de 2022' (DOU 25.4.2019); its art. 1 is the new LSA art. 289, its art. 2 the new art. 294 caput
    ("lei-13818-2019", "lei-das-sociedades-por-acoes", "art-289"): (
        "2022-01-01", "Lei 13.818/2019 art. 3: in force on publication 'à exceção do art. 1º, que entra em vigor em 1º de "
                      "janeiro de 2022'; its art. 1 is the new wording of LSA art. 289"),
})
# Medidas Provisórias that lapsed: key -> (day the wording they replaced is back, reason), from the Ato Declaratório
# the MP page links ('Vigência encerrada'), pinned as ato:* in sources_batch7.json
P.MP_LAPSE.update({
    "mp-1065-2021": ("2022-02-07", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 5, de 2022 (DOU "
                                   "11.3.2022): 'teve seu prazo de vigência encerrado no dia 6 de fevereiro de 2022'"),
    "mp-1158-2023": ("2023-06-02", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 39, de 2023 (DOU "
                                   "16.6.2023): 'teve seu prazo de vigência encerrado no dia 1º de junho de 2023'"),
    "mp-784-2017": ("2017-10-20", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 56, de 2017 (DOU "
                                  "23.10.2017): 'teve seu prazo de vigência encerrado no dia 19 de outubro do corrente ano'"),
    "mp-892-2019": ("2019-12-04", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 68, de 2019 (DOU "
                                  "5.12.2019): 'teve seu prazo de vigência encerrado no dia 3 de dezembro do corrente ano'"),
})
# MP pages whose 'Convertida na Lei' line is mistyped, so parse_proc does not read it: key -> (conversion law, why)
CONVERTED_FIX: dict[str, tuple[str, str]] = {
    "mp-459-2009": ("lei-11977-2009", "the MP page reads 'Convertida na Lei nº 1 1.977, de 2009' (a space inside the "
                                      "number), linking ../Lei/L11977.htm, Lei nº 11.977, de 7.7.2009"),
}
CONVERTED_USED: list[str] = []
_page_info7 = P.page_info


def page_info(key: str) -> dict:
    info = _page_info7(key)
    if key in CONVERTED_FIX and info and not info.get("converted"):
        info["converted"] = CONVERTED_FIX[key][0]
        CONVERTED_USED.append(key)
    return info


P.page_info = B.page_info = page_info
P.NOTE_FIX["(Redação da pela Lei nº10.303, de 2001)"] = (
    "(Redação dada pela Lei nº 10.303, de 2001)",
    "Lei 6.404 art. 124 § 1º: the note reads 'Redação da pela Lei nº10.303, de 2001' ('da' for 'dada'); its link is Lei "
    "nº 10.303, de 31.10.2001, whose art. 2 gives § 1º that wording")

# ---------------------------------------------------------------------------------------------------------------
# Lines whose end parse_proc does not find:
# (1) a struck wording with no note and no later wording of the same label, printed above the lines that replaced it
#     with new labels (a list renumbered: Lei 6.404 art. 40 III became II; art. 178's alíneas became incisos): it ends
#     when the first later wording below it in the same article starts, credited to that wording's law;
# (2) an unstruck line a later law replaced, which Planalto left unstruck (PLAIN_ENDS, checked by hand).
NEXT_WORDING_USED: list[str] = []
LAPSE_EARLY_USED: list[str] = []
PLAIN_ENDS: dict[tuple[str, str, str, str], tuple[str, str]] = {
    ("lei-de-responsabilidade-fiscal", "art-51", "§ 1º", "§ 1º Os Estados e os Municípios encaminharão suas contas ao Poder "
     "Executivo da União nos seguintes prazos:"): (
        "lc-178-2021", "LRF art. 51 § 1º as enacted ('... nos seguintes prazos:', followed by incisos I and II, which are "
                       "struck) is printed unstruck above the wording 'Redação dada pela Lei Complementar nº 178, de 2021' "
                       "that replaced it from 1.1.2022"),
}
PLAIN_ENDS_USED: list[str] = []
_lifespans7 = P.lifespans


def lifespans(paras: list[dict], cx) -> list[str]:
    problems = _lifespans7(paras, cx)
    for p in paras:
        for (act, unit, label, start), (law, why) in PLAIN_ENDS.items():
            if cx.act == act and p["unit"] == unit and p["label"] == label and p["text"].startswith(start) and not p["end"]:
                p["end"], p["end_law"], p["end_how"] = cx.eff[law], law, "plain-end"
                PLAIN_ENDS_USED.append(why)
    # a lapsed MP's wording that a law replaced before the lapse ends with that law's wording (Estatuto da Cidade art.
    # 57-A: Lei 14.273/2021, in force 6.2.2022, while MP 1.065/2021's term ended at the close of 6.2.2022)
    for i, p in enumerate(paras):
        if p["end_how"] != "lapse" or not p["end"]:
            continue
        j = P.successor(paras, i)
        if j is not None and paras[j]["start"] < p["end"]:
            q = paras[j]
            LAPSE_EARLY_USED.append(f"{cx.act} {p['unit']} [{p['label']}] ends {q['start']} ({P.law_label(q['start_law'])}), "
                                    f"not {p['end']}")
            p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "successor-before-lapse"
    # ... and so do the other lines that MP wrote in the same article (its Parágrafo único under the replaced caput)
    for p in paras:
        if p["end_how"] != "lapse":
            continue
        e = [q for q in paras if q["unit"] == p["unit"] and q["start_law"] == p["start_law"]
             and q["end_how"] == "successor-before-lapse" and q["end"] < p["end"]]
        if e:
            p["end"], p["end_law"], p["end_how"] = e[0]["end"], e[0]["end_law"], "successor-before-lapse"
            LAPSE_EARLY_USED.append(f"{cx.act} {p['unit']} [{p['label']}] with its article")
    for i, p in enumerate(paras):
        if p["end_how"] != "undated" and not (p["state"] != "plain" and not p["end"] and not p["gaps"]):
            continue
        q = None
        seen = {p["label"]}
        for r in paras[i + 1:]:
            if r["unit"] != p["unit"] or r["heading"] != p["heading"]:
                break
            # a later wording of a label printed since p replaced that sibling, not p (Lei 11.638's alínea c) of art.
            # 178 § 1º, while alíneas a) and b) stood until MP 449/2008 recast the list)
            if p["heading"] and r["label"].split("-")[0] != p["label"].split("-")[0]:
                continue   # a heading line is replaced only within its own heading group
            if r["start"] > p["start"] and not r.get("skip") and (p["heading"] or r["label"] not in seen):
                q = r
                break
            seen.add(r["label"])
        if q is None:
            continue
        p["end"], p["end_law"], p["end_how"], p["skip"] = q["start"], q["start_law"], "next-wording", False
        NEXT_WORDING_USED.append(f"{cx.act} {p['unit']} [{p['label']}] {p['text'][:40]!r} ends {q['start']}")
    return problems


P.lifespans = B.lifespans = lifespans

SRC = HERE / "sources_batch7.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

# Chamber of Deputies records the in-force days rely on (pinned as ctx:* in sources_batch7.json)
B6.CONTEXT[:] = [
    {"when": lambda: any(a["law"] == "lei-10257-2001" for a in ACTS),
     "pins": ["ctx:camara-lei-10257-2001-norma", "ctx:camara-lei-10257-2001-retificacao"],
     "what": "the record and the retificação (DOU 17.7.2001) of Lei 10.257/2001"},
    {"when": lambda: any(a["law"] == "lc-182-2021" for a in ACTS),
     "pins": ["ctx:camara-lc-182-2021-norma", "ctx:camara-lc-182-2021-retificacao"],
     "what": "the record and the retificação (DOU 4.6.2021) of Lei Complementar 182/2021"},
]

_inner6 = B6.PB5B._write_part5


def _inner(*a) -> int:
    if CONVERTED_USED:
        B5.EXTRA_DECISIONS.append(
            "Medida Provisória pages whose 'Convertida na Lei' line is mistyped are read with the law their link names: "
            + "; ".join(f"{P.law_label(k)}: {CONVERTED_FIX[k][1]}" for k in dict.fromkeys(CONVERTED_USED)) + ".")
    if NEXT_WORDING_USED:
        B5.EXTRA_DECISIONS.append(
            "A struck wording with no note and no later wording of the same label, printed above the lines that replaced "
            "it under new labels (a list renumbered or recast), ends when the first later wording below it in the same "
            "article starts (skipping later wordings of the sibling labels printed between them), credited to that "
            "wording's law: " + "; ".join(dict.fromkeys(NEXT_WORDING_USED)) + ".")
    if LAPSE_EARLY_USED:
        B5.EXTRA_DECISIONS.append("A lapsed Medida Provisória's wording that a law replaced before the MP's term ended "
                                  "ends on that law's day: " + "; ".join(dict.fromkeys(LAPSE_EARLY_USED)) + ".")
    if PLAIN_ENDS_USED:
        B5.EXTRA_DECISIONS.append("Unstruck lines a later law replaced, which Planalto left unstruck, end on that law's "
                                  "day: " + "; ".join(dict.fromkeys(PLAIN_ENDS_USED)) + ".")
    if STRAY_USED:
        B5.EXTRA_DECISIONS.append("Stray link text at the end of a line is dropped: " + "; ".join(dict.fromkeys(STRAY_USED)) + ".")
    if HEADING_LABEL_FIX:
        B5.EXTRA_DECISIONS.append(
            "A dispositivo Planalto prints centred, like a heading, is kept in its article when its line starts with a "
            "dispositivo label: " + "; ".join(dict.fromkeys(HEADING_LABEL_FIX)) + ".")
    return _inner6(*a)


B6.PB5B._write_part5 = _inner

# Stale wordings (two wordings of one dispositivo at once): the rules of stale_fix.py, applied to each act's final life
# spans before its versions are built (as for the older parts, through oldparts.py); their uses go into the decisions.
import stale_fix  # noqa: E402

_build_act7 = P.build_act
_act_order: list[str] = []


def build_act(paras, *a, **k):
    slug = ACTS[len(_act_order)]["slug"] if len(_act_order) < len(ACTS) else "?"
    _act_order.append(slug)
    stale_fix.fix(P, paras, slug, set())
    return _build_act7(paras, *a, **k)


P.build_act = B.build_act = build_act
_inner_stale = B6.PB5B._write_part5


def _inner2(*a) -> int:
    B5.EXTRA_DECISIONS.extend(stale_fix.decisions())
    return _inner_stale(*a)


B6.PB5B._write_part5 = _inner2

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
