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
VERIFIED: list[str] = []
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
    return out, rest


P.paragraphs = B.paragraphs = paragraphs

B.EXPLAINED.clear()
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

SRC = HERE / "sources_batch7.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
