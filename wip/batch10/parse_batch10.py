"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch10.json (SCHEMA.md corpus part): the acts in ALL_ACTS
below (more federal laws, as they are verified).

    python -X utf8 scripts/brazil-law/batch10/parse_batch10.py [--stats] [--dry]

Imports ../batch9/parse_batch9.py (which configures batch 8 and everything below it, plus batch 9's hand tools:
REPEALS, FOLD_EARLY, NOTE_INTO_TEXT, WORD_FIX) with no act of its own, and replaces only the configuration: the acts,
the in-force days, the hand tables for these acts, the pins and the output. Earlier parts are not touched. No network.

BATCH10_ACTS=<slug,...> selects acts for trial runs (BATCH10_OUT=<file> writes elsewhere); by default VERIFIED is
written.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH9_ACTS"] = "-"   # batch 9 configures no act of its own here
os.environ.pop("BATCH9_OUT", None)
sys.path.insert(0, str(FOLDER / "batch9"))
import parse_batch9 as B9  # noqa: E402

B8, B7, B6, B5, B, P = B9.B8, B9.B7, B9.B6, B9.B5, B9.B, B9.P
PL = P.PL
B5.OUT = Path(os.environ.get("BATCH10_OUT") or FOLDER / "corpus.d" / "99-batch10.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = {
    "lconc": "leis/l8987cons.htm",
    "lconc-compilada": "leis/l8987compilada.htm",
    "lppp": "_ato2004-2006/2004/lei/l11079.htm",
    "lppp-compilado": "_ato2004-2006/2004/lei/l11079compilado.htm",
    "lsan": "_ato2007-2010/2007/lei/l11445.htm",
    "lsan-compilado": "_ato2007-2010/2007/lei/l11445compilado.htm",
    "lpet": "leis/l9478.htm",
    "lpet-compilado": "leis/l9478compilado.htm",
    "labus": "_ato2019-2022/2019/lei/l13869.htm",
    "labus-compilado": "_ato2019-2022/2019/lei/l13869compilado.htm",
    "emil": "leis/l6880.htm",
    "emil-compilada": "leis/l6880compilada.htm",
    "linel": "leis/lcp/lcp64.htm",
    "linel-compilado": "leis/lcp/lcp64compilado.htm",
    "l8142": "leis/l8142.htm",
    "lgesp": "_ato2023-2026/2023/lei/l14597.htm",
    "etorc": "leis/2003/l10.671.htm",
    "etorc-compilado": "leis/2003/l10.671compilado.htm",
    "pnma": "leis/l6938.htm",
    "pnma-compilada": "leis/l6938compilada.htm",
}
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = B6.PAGES = B7.PAGES = B8.PAGES = B9.PAGES = PAGES


def _act(slug, short, page, consolidated, law, title, digits):
    return {"slug": slug, "short": short, "page": page, "consolidated": consolidated, "law": law, "title": title,
            "digits": digits, "url": PL + PAGES[page]}


ALL_ACTS: list[dict] = [
    _act("lei-de-concessoes", "LConc", "lconc", "lconc-compilada", "lei-8987-1995",
         "Lei de Concessões (Lei nº 8.987, de 13 de fevereiro de 1995)", 2),
    _act("lei-das-parcerias-publico-privadas", "LPPP", "lppp", "lppp-compilado", "lei-11079-2004",
         "Lei das Parcerias Público-Privadas (Lei nº 11.079, de 30 de dezembro de 2004)", 2),
    _act("lei-do-saneamento-basico", "LSB", "lsan", "lsan-compilado", "lei-11445-2007",
         "Lei do Saneamento Básico (Lei nº 11.445, de 5 de janeiro de 2007)", 2),
    _act("lei-do-petroleo", "LPet", "lpet", "lpet-compilado", "lei-9478-1997",
         "Lei do Petróleo (Lei nº 9.478, de 6 de agosto de 1997)", 2),
    _act("lei-de-abuso-de-autoridade", "LAA", "labus", "labus-compilado", "lei-13869-2019",
         "Lei de Abuso de Autoridade (Lei nº 13.869, de 5 de setembro de 2019)", 2),
    _act("estatuto-dos-militares", "EMil", "emil", "emil-compilada", "lei-6880-1980",
         "Estatuto dos Militares (Lei nº 6.880, de 9 de dezembro de 1980)", 3),
    _act("lei-das-inelegibilidades", "LInel", "linel", "linel-compilado", "lcp-64-1990",
         "Lei das Inelegibilidades (Lei Complementar nº 64, de 18 de maio de 1990)", 2),
    _act("lei-8142-de-1990", "L8142", "l8142", "l8142", "lei-8142-1990",
         "Participação da comunidade e financiamento do SUS (Lei nº 8.142, de 28 de dezembro de 1990)", 2),
    _act("lei-geral-do-esporte", "LGE", "lgesp", "lgesp", "lei-14597-2023",
         "Lei Geral do Esporte (Lei nº 14.597, de 14 de junho de 2023)", 3),
    _act("estatuto-do-torcedor", "ETor", "etorc", "etorc-compilado", "lei-10671-2003",
         "Estatuto de Defesa do Torcedor (Lei nº 10.671, de 15 de maio de 2003)", 2),
    _act("politica-nacional-do-meio-ambiente", "PNMA", "pnma", "pnma-compilada", "lei-6938-1981",
         "Política Nacional do Meio Ambiente (Lei nº 6.938, de 31 de agosto de 1981)", 2),
]
VERIFIED: list[str] = []
ENABLED = [s for s in os.environ.get("BATCH10_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
B7.ACTS[:] = ACTS
B8.ACTS[:] = ACTS
B9.ACTS[:] = ACTS

# in-force day of each act as enacted, and its own law record (filled from each page as it is read)
_PUB = "'Esta Lei entra em vigor na data de sua publicação'"
ACT_DAY_ALL: dict[str, tuple[str, str]] = {
    "lei-8987-1995": ("1995-02-14", f"Lei 8.987/1995 art. 46: {_PUB} (DOU 14.2.1995)"),
    "lei-11079-2004": ("2004-12-31", f"Lei 11.079/2004 art. 30: {_PUB} (DOU 31.12.2004)"),
    "lei-11445-2007": ("2007-01-08", "Lei 11.445/2007 art. 60 (as enacted): 'Esta Lei entra em vigor na data de sua "
                                     "publicação' (DOU 8.1.2007)"),
    "lei-9478-1997": ("1997-08-07", f"Lei 9.478/1997 art. 82: {_PUB} (DOU 7.8.1997)"),
    "lei-13869-2019": ("2020-01-03", "Lei 13.869/2019 art. 45: 'Esta Lei entra em vigor após decorridos 120 (cento e vinte) "
                                     "dias de sua publicação oficial' (DOU 5.9.2019, edição extra): the 120th day counted "
                                     "from publication is 2.1.2020 (LC 95/1998 art. 8 § 1)"),
    "lei-6880-1980": ("1981-01-01", "Lei 6.880/1980 art. 159: 'O presente Estatuto entrará em vigor a partir de 1º de "
                                    "janeiro de 1981, salvo quanto ao disposto no item IV do artigo 98, que terá vigência 1 "
                                    "(um) ano após a data da publicação desta Lei' (DOU 11.12.1980)"),
    "lcp-64-1990": ("1990-05-21", "Lei Complementar 64/1990 art. 27: 'Esta lei complementar entra em vigor na data de sua "
                                  "publicação' (DOU 21.5.1990)"),
    "lei-8142-1990": ("1990-12-31", "Lei 8.142/1990 art. 6: 'Esta lei entra em vigor na data de sua publicação' (DOU "
                                    "31.12.1990)"),
    "lei-14597-2023": ("2023-06-15", f"Lei 14.597/2023 art. 218: {_PUB} (DOU 15.6.2023)"),
    "lei-10671-2003": ("2003-05-16", f"Lei 10.671/2003 art. 45: {_PUB} (DOU 16.5.2003)"),
    "lei-6938-1981": ("1981-09-02", "Lei 6.938/1981 art. 20: 'Esta Lei entrará em vigor na data de sua publicação' (DOU "
                                    "2.9.1981)"),
}
ACT_LAWS_ALL: dict[str, dict] = {
    "lei-8987-1995": B._act_law("Lei nº 8.987, de 1995", "Dispõe sobre o regime de concessão e permissão da prestação de "
                                "serviços públicos previsto no art. 175 da Constituição Federal, e dá outras providências.",
                                "1995-02-13", "1995-02-14", PAGES["lconc"]),
    "lei-11079-2004": B._act_law("Lei nº 11.079, de 2004", "Institui normas gerais para licitação e contratação de parceria "
                                 "público-privada no âmbito da administração pública.", "2004-12-30", "2004-12-31",
                                 PAGES["lppp"]),
    "lei-11445-2007": B._act_law("Lei nº 11.445, de 2007", "Estabelece diretrizes nacionais para o saneamento básico; altera "
                                 "as Leis nos 6.766, de 19 de dezembro de 1979, 8.036, de 11 de maio de 1990, 8.666, de 21 "
                                 "de junho de 1993, 8.987, de 13 de fevereiro de 1995; revoga a Lei no 6.528, de 11 de maio "
                                 "de 1978; e dá outras providências.", "2007-01-05", "2007-01-08", PAGES["lsan"]),
    "lei-9478-1997": B._act_law("Lei nº 9.478, de 1997", "Dispõe sobre a política energética nacional, as atividades "
                                "relativas ao monopólio do petróleo, institui o Conselho Nacional de Política Energética e "
                                "a Agência Nacional do Petróleo e dá outras providências.", "1997-08-06", "1997-08-07",
                                PAGES["lpet"]),
    "lei-13869-2019": B._act_law("Lei nº 13.869, de 2019", "Dispõe sobre os crimes de abuso de autoridade; altera a Lei nº "
                                 "7.960, de 21 de dezembro de 1989, a Lei nº 9.296, de 24 de julho de 1996, a Lei nº 8.069, "
                                 "de 13 de julho de 1990, e a Lei nº 8.906, de 4 de julho de 1994; e revoga a Lei nº 4.898, "
                                 "de 9 de dezembro de 1965, e dispositivos do Decreto-Lei nº 2.848, de 7 de dezembro de 1940 "
                                 "(Código Penal).", "2019-09-05", "2019-09-05", PAGES["labus"]),
    "lei-6880-1980": B._act_law("Lei nº 6.880, de 1980", "Dispõe sobre o Estatuto dos Militares.", "1980-12-09",
                                "1980-12-11", PAGES["emil"]),
    "lcp-64-1990": B._act_law("Lei Complementar nº 64, de 1990", "Estabelece, de acordo com o art. 14, § 9º da Constituição "
                              "Federal, casos de inelegibilidade, prazos de cessação, e determina outras providências.",
                              "1990-05-18", "1990-05-21", PAGES["linel"]),
    "lei-8142-1990": B._act_law("Lei nº 8.142, de 1990", "Dispõe sobre a participação da comunidade na gestão do Sistema "
                                "Único de Saúde (SUS) e sobre as transferências intergovernamentais de recursos financeiros "
                                "na área da saúde e dá outras providências.", "1990-12-28", "1990-12-31", PAGES["l8142"]),
    "lei-14597-2023": B._act_law("Lei nº 14.597, de 2023", "Institui a Lei Geral do Esporte.", "2023-06-14", "2023-06-15",
                                 PAGES["lgesp"]),
    "lei-10671-2003": B._act_law("Lei nº 10.671, de 2003", "Dispõe sobre o Estatuto de Defesa do Torcedor e dá outras "
                                 "providências.", "2003-05-15", "2003-05-16", PAGES["etorc"]),
    "lei-6938-1981": B._act_law("Lei nº 6.938, de 1981", "Dispõe sobre a Política Nacional do Meio Ambiente, seus fins e "
                                "mecanismos de formulação e aplicação, e dá outras providências.", "1981-08-31",
                                "1981-09-02", PAGES["pnma"]),
}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# batch 9's hand tools, emptied for these acts (the law facts in VIGENCIA_FIXED, MP_LAPSE, ... are kept: they hold for
# every act and are printed in decisions only where a version uses them)
B.EXPLAINED.clear()
B8.SPAN_FIX.clear()
B8.COURT_SPLIT.clear()
B8.LABEL_FIX.clear()
B8.UNIT_FIX.clear()
B8.NAV_LINES.clear()
B8.EXTRA_LAWS.clear()
B9.NOTE_INTO_TEXT.clear()
B9.WORD_FIX.clear()
B9.REPEALS.clear()
B9.FOLD_EARLY.clear()
P.COURTS = {}
P.NOTE_FIX = {}

SRC = HERE / "sources_batch10.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
