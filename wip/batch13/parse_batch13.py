"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch13<x>.json (SCHEMA.md corpus parts): more major federal
acts not yet in the corpus, published in small parts of 2-4 acts each (99-batch13a, 99-batch13b, ...).

    BATCH13_PART=a python -X utf8 scripts/brazil-law/batch13/parse_batch13.py [--stats] [--dry]

Imports ../batch12/parse_batch12.py (which configures batch 11 and everything below it, plus batch 12's hand tables) with
no act of its own, and replaces only the configuration: the acts, the in-force days, the hand tables for these acts, the
pins and the output. Earlier parts are not touched. No network.

BATCH13_PART selects the part (its acts are PARTS[part]); BATCH13_ACTS=<slug,...> selects acts for trial runs
(BATCH13_OUT=<file> writes elsewhere).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH12_ACTS"] = "-"   # batch 12 configures no act of its own here
os.environ.pop("BATCH12_OUT", None)
sys.path.insert(0, str(FOLDER / "batch12"))
import parse_batch12 as B12  # noqa: E402

B11, B10, B9, B8, B7, B6, B5, B, P = B12.B11, B12.B10, B12.B9, B12.B8, B12.B7, B12.B6, B12.B5, B12.B, B12.P
PL = P.PL
PART = os.environ.get("BATCH13_PART", "a")
B5.OUT = Path(os.environ.get("BATCH13_OUT") or FOLDER / "corpus.d" / f"99-batch13{PART}.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = {
    # 13a
    "lcp": "decreto-lei/del3688.htm",
    "lcr": "leis/l1079.htm",
    "lrac": "leis/l7716.htm",
    "lrac-compilado": "leis/l7716compilado.htm",
}
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = B6.PAGES = B7.PAGES = B8.PAGES = B9.PAGES = B10.PAGES = B11.PAGES = B12.PAGES = PAGES


def _act(slug, short, page, consolidated, law, title, digits):
    return {"slug": slug, "short": short, "page": page, "consolidated": consolidated, "law": law, "title": title,
            "digits": digits, "url": PL + PAGES[page]}


ALL_ACTS: list[dict] = [
    _act("lei-das-contravencoes-penais", "LCP", "lcp", "lcp", "dl-3688-1941",
         "Lei das Contravenções Penais (Decreto-Lei nº 3.688, de 3 de outubro de 1941)", 2),
    _act("lei-dos-crimes-de-responsabilidade", "LCR", "lcr", "lcr", "lei-1079-1950",
         "Lei dos Crimes de Responsabilidade (Lei nº 1.079, de 10 de abril de 1950)", 2),
    _act("lei-do-crime-racial", "LCRac", "lrac", "lrac-compilado", "lei-7716-1989",
         "Crimes resultantes de preconceito de raça ou de cor (Lei nº 7.716, de 5 de janeiro de 1989)", 2),
]
PARTS: dict[str, list[str]] = {
    "a": ["lei-das-contravencoes-penais", "lei-dos-crimes-de-responsabilidade", "lei-do-crime-racial"],
}
VERIFIED: list[str] = PARTS.get(PART, [])
ENABLED = [s for s in os.environ.get("BATCH13_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
for M in (B7, B8, B9, B10, B11, B12):
    M.ACTS[:] = ACTS

_PUB = "'Esta Lei entra em vigor na data de sua publicação'"
ACT_DAY_ALL: dict[str, tuple[str, str]] = {
    "dl-3688-1941": ("1942-01-01", "Decreto-Lei 3.688/1941 art. 72: 'Esta lei entrará em vigor no dia 1º de janeiro de 1942'"),
    "lei-1079-1950": ("1950-05-27", "Lei 1.079/1950 has no vigência clause (its last article, art. 82, sets the time limit "
                                    "for the trial): LINDB art. 1, 45 days after publication in the DOU of 12.4.1950"),
    "lei-7716-1989": ("1989-01-06", f"Lei 7.716/1989 art. 21: {_PUB} (DOU 6.1.1989)"),
}
_L = B._act_law
ACT_LAWS_ALL: dict[str, dict] = {
    "dl-3688-1941": _L("Decreto-Lei nº 3.688, de 1941", "Lei das Contravenções Penais.", "1941-10-03", "1941-10-13",
                       PAGES["lcp"]),
    "lei-1079-1950": _L("Lei nº 1.079, de 1950", "Define os crimes de responsabilidade e regula o respectivo processo de "
                        "julgamento.", "1950-04-10", "1950-04-12", PAGES["lcr"]),
    "lei-7716-1989": _L("Lei nº 7.716, de 1989", "Define os crimes resultantes de preconceito de raça ou de cor.",
                        "1989-01-05", "1989-01-06", PAGES["lrac"]),
}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# batch 12's act-specific tools emptied (law facts in VIGENCIA_FIXED, MP_LAPSE, ... are kept: printed only where used)
B.EXPLAINED.clear()
B8.SPAN_FIX.clear()
B8.LABEL_FIX.clear()
B9.WORD_FIX.clear()
P.VETO_PROMULGATION = {}
P.VETO_PROMULGATED_UNITS = {}
P.NOTE_FIX = {}

# ---------------------------------------------------------------------------------------------------------------
# hand tables for these acts, each read from the official pages named in the reason
P.VIGENCIA_FIXED.update({
    "dl-6916-1944": ("1944-10-02", "artigo único: art. 46 of the Lei das Contravenções Penais 'passa a vigorar, a partir da "
                                   "publicação da presente lei, com a seguinte redação' (DOU 2.10.1944)"),
})

# court and other open items named in decisions (Planalto's 'Vide' notes are dropped from the text, so nothing is modelled)
OPEN_ITEMS = {
    "lei-dos-crimes-de-responsabilidade": (
        "Lei dos Crimes de Responsabilidade (open item): Planalto's page marks arts. 39, 41, 47, 54, 57 and 70 (crimes and "
        "procedure for Ministers of the Supremo Tribunal Federal and the Procurador-Geral da República) with '(Vide ADPF 1259)' and "
        "'(Vide ADPF 1260)', with no date and no struck text; the STF decisions in those cases are not modelled, and the "
        "text is the law's own wording"),
    "lei-do-crime-racial": (
        "Crimes resultantes de preconceito de raça ou de cor (open item): Planalto's page heads the act with '(Vide ADO Nº 26)', a Supremo Tribunal Federal "
        "ruling that changes no words of the act; it changes no words and is not modelled"),
    "lei-das-contravencoes-penais": (
        "Lei das Contravenções Penais: Planalto's 'Vide' pointers at the head of the act (Lei 1.390/1951, Lei 7.437/1985) and "
        "at art. 50 (Decretos-Leis 4.866/1942 and 9.215/1946) name acts that changed no words of it; they are not "
        "modelled"),
}
_inner13 = B6.PB5B._write_part5


def _inner(*a):
    B5.EXTRA_DECISIONS.extend(OPEN_ITEMS[act["slug"]] + "." for act in a[0] if act["slug"] in OPEN_ITEMS)
    return _inner13(*a)


B6.PB5B._write_part5 = _inner

SRC = HERE / "sources_batch13.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
