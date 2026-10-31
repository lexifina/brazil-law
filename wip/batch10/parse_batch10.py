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
ACT_DAY_ALL: dict[str, tuple[str, str]] = {}
ACT_LAWS_ALL: dict[str, dict] = {}
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
