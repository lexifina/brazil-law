"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch11.json (SCHEMA.md corpus part): the acts in ALL_ACTS
below (more federal laws, as they are verified).

    python -X utf8 scripts/brazil-law/batch11/parse_batch11.py [--stats] [--dry]

Imports ../batch10/parse_batch10.py (which configures batch 9 and everything below it, plus batch 10's hand tools) with
no act of its own, and replaces only the configuration: the acts, the in-force days, the hand tables for these acts, the
pins and the output. Earlier parts are not touched. No network.

BATCH11_ACTS=<slug,...> selects acts for trial runs (BATCH11_OUT=<file> writes elsewhere); by default VERIFIED is
written.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH10_ACTS"] = "-"   # batch 10 configures no act of its own here
os.environ.pop("BATCH10_OUT", None)
sys.path.insert(0, str(FOLDER / "batch10"))
import parse_batch10 as B10  # noqa: E402

B9, B8, B7, B6, B5, B, P = B10.B9, B10.B8, B10.B7, B10.B6, B10.B5, B10.B, B10.P
PL = P.PL
B5.OUT = Path(os.environ.get("BATCH11_OUT") or FOLDER / "corpus.d" / "99-batch11.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = {
    "lef": "leis/l6830.htm",
    "lcade": "_ato2011-2014/2011/lei/l12529.htm",
    "eoab": "leis/l8906.htm",
    "ladi": "leis/l9868.htm",
    "ladpf": "leis/l9882.htm",
    "lcot": "leis/l8137.htm",
    "lit": "leis/l9296.htm",
    "lbf": "leis/l8009.htm",
    "lap": "leis/l4717.htm",
    "lcsf": "leis/l7492.htm",
    "lps": "leis/l9656.htm",
    "lps-compilado": "leis/l9656compilado.htm",
    "lcvm": "leis/l6385.htm",
    "lcvm-compilada": "leis/l6385compilada.htm",
    "lpsolo": "leis/l6766.htm",
    "lpsolo-compilado": "leis/l6766compilado.htm",
    "loas": "leis/l8742.htm",
    "loas-compilado": "leis/l8742compilado.htm",
}
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = B6.PAGES = B7.PAGES = B8.PAGES = B9.PAGES = B10.PAGES = PAGES


def _act(slug, short, page, consolidated, law, title, digits):
    return {"slug": slug, "short": short, "page": page, "consolidated": consolidated, "law": law, "title": title,
            "digits": digits, "url": PL + PAGES[page]}


ALL_ACTS: list[dict] = [
    _act("lei-de-execucao-fiscal", "LEF", "lef", "lef", "lei-6830-1980",
         "Lei de Execução Fiscal (Lei nº 6.830, de 22 de setembro de 1980)", 2),
    _act("lei-de-defesa-da-concorrencia", "LDC", "lcade", "lcade", "lei-12529-2011",
         "Lei de Defesa da Concorrência (Lei nº 12.529, de 30 de novembro de 2011)", 3),
    _act("estatuto-da-advocacia", "EOAB", "eoab", "eoab", "lei-8906-1994",
         "Estatuto da Advocacia e da OAB (Lei nº 8.906, de 4 de julho de 1994)", 2),
    _act("lei-da-adi-e-da-adc", "LADI", "ladi", "ladi", "lei-9868-1999",
         "Lei da ADI e da ADC (Lei nº 9.868, de 10 de novembro de 1999)", 2),
    _act("lei-da-adpf", "LADPF", "ladpf", "ladpf", "lei-9882-1999",
         "Lei da ADPF (Lei nº 9.882, de 3 de dezembro de 1999)", 2),
    _act("lei-dos-crimes-contra-a-ordem-tributaria", "LCOT", "lcot", "lcot", "lei-8137-1990",
         "Crimes contra a ordem tributária, econômica e as relações de consumo (Lei nº 8.137, de 27 de dezembro de 1990)", 2),
    _act("lei-de-interceptacao-telefonica", "LIT", "lit", "lit", "lei-9296-1996",
         "Lei de Interceptação Telefônica (Lei nº 9.296, de 24 de julho de 1996)", 2),
    _act("lei-do-bem-de-familia", "LBF", "lbf", "lbf", "lei-8009-1990",
         "Lei do Bem de Família (Lei nº 8.009, de 29 de março de 1990)", 2),
    _act("lei-da-acao-popular", "LAP", "lap", "lap", "lei-4717-1965",
         "Lei da Ação Popular (Lei nº 4.717, de 29 de junho de 1965)", 2),
    _act("lei-dos-crimes-contra-o-sistema-financeiro", "LCSF", "lcsf", "lcsf", "lei-7492-1986",
         "Crimes contra o Sistema Financeiro Nacional (Lei nº 7.492, de 16 de junho de 1986)", 2),
    _act("lei-dos-planos-de-saude", "LPS", "lps", "lps-compilado", "lei-9656-1998",
         "Lei dos Planos de Saúde (Lei nº 9.656, de 3 de junho de 1998)", 2),
    _act("lei-do-mercado-de-valores-mobiliarios", "LCVM", "lcvm", "lcvm-compilada", "lei-6385-1976",
         "Lei do Mercado de Valores Mobiliários (Lei nº 6.385, de 7 de dezembro de 1976)", 2),
    _act("lei-do-parcelamento-do-solo-urbano", "LPSU", "lpsolo", "lpsolo-compilado", "lei-6766-1979",
         "Lei do Parcelamento do Solo Urbano (Lei nº 6.766, de 19 de dezembro de 1979)", 2),
    _act("lei-organica-da-assistencia-social", "LOAS", "loas", "loas-compilado", "lei-8742-1993",
         "Lei Orgânica da Assistência Social (Lei nº 8.742, de 7 de dezembro de 1993)", 2),
]
VERIFIED: list[str] = []
ENABLED = [s for s in os.environ.get("BATCH11_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
B7.ACTS[:] = ACTS
B8.ACTS[:] = ACTS
B9.ACTS[:] = ACTS
B10.ACTS[:] = ACTS

# in-force day of each act as enacted, and its own law record (filled from each page as it is read)
ACT_DAY_ALL: dict[str, tuple[str, str]] = {}
ACT_LAWS_ALL: dict[str, dict] = {}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# batch 10's hand tools, emptied for these acts (law facts in VIGENCIA_FIXED, MP_LAPSE, ... are kept: they hold for every
# act and are printed in decisions only where a version uses them)
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

# ---------------------------------------------------------------------------------------------------------------
# hand tables for these acts, each read from the official pages named in the reason

SRC = HERE / "sources_batch11.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
