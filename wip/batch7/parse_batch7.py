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
    "lrf": "leis/lcp/lcp101.htm",
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
    _act("lei-de-responsabilidade-fiscal", "LRF", "lrf", "lrf", "lc-101-2000",
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
ACT_DAY_ALL: dict[str, tuple[str, str]] = {}
ACT_LAWS_ALL: dict[str, dict] = {}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

B.EXPLAINED.clear()
B6.NEVER_IN_FORCE.clear()
B6.MP_CHAINS.clear()
B6.REISSUES.clear()

SRC = HERE / "sources_batch7.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
