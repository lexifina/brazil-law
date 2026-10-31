"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch17<x>.json (SCHEMA.md corpus parts): more major federal
acts not yet in the corpus, in small parts of 2-4 acts each (99-batch17a, 99-batch17b, ...).

    BATCH17_PART=a python -X utf8 scripts/brazil-law/batch17/parse_batch17.py [--stats] [--dry]

Imports ../batch16/parse_batch16.py (which configures batch 15 and everything below it, with their hand tables and the
Medida Provisória 905/955 model) with no act of its own, and replaces only the configuration: the acts, the in-force
days, the hand tables for these acts, the pins and the output. Earlier parts are not touched. No network.

BATCH17_PART selects the part (its acts are PARTS[part]); BATCH17_ACTS=<slug,...> selects acts for trial runs
(BATCH17_OUT=<file> writes elsewhere). After writing a part run ../effects_fix.py on it (effect days).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH16_PART"] = "-"   # batch 16 configures no act of its own here
os.environ.pop("BATCH16_ACTS", None)
os.environ.pop("BATCH16_OUT", None)
sys.path.insert(0, str(FOLDER / "batch16"))
import parse_batch16 as B16  # noqa: E402

B15, B14, B13, B12, B11, B10, B9, B8, B7, B6, B5, B, P = (B16.B15, B16.B14, B16.B13, B16.B12, B16.B11, B16.B10, B16.B9,
                                                          B16.B8, B16.B7, B16.B6, B16.B5, B16.B, B16.P)
PL = P.PL
PART = os.environ.get("BATCH17_PART", "a")
B5.OUT = Path(os.environ.get("BATCH17_OUT") or FOLDER / "corpus.d" / f"99-batch17{PART}.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = B16.PAGES   # the dict every earlier module shares; batch 17's pages are added to it
PAGES.update({
    # part a: labour laws
    "l5889": "leis/l5889.htm",
    "l4090": "leis/l4090.htm",
    "l0605": "leis/l0605.htm",
    "l7418": "leis/l7418.htm",
    "l7418-compilado": "leis/l7418compilado.htm",
})
B.PAGES.clear()
B.PAGES.update(PAGES)
for M in (B5, B6, B7, B8, B9, B10, B11, B12, B13, B14, B15, B16):
    M.PAGES = PAGES

_act = B14._act
ALL_ACTS: list[dict] = [
    _act("lei-do-trabalho-rural", "LTR", "l5889", "l5889", "lei-5889-1973",
         "Lei do Trabalho Rural (Lei nº 5.889, de 8 de junho de 1973)", 2),
    _act("lei-do-decimo-terceiro-salario", "L13S", "l4090", "l4090", "lei-4090-1962",
         "Gratificação de Natal - décimo terceiro salário (Lei nº 4.090, de 13 de julho de 1962)", 2),
    _act("lei-do-repouso-semanal-remunerado", "LRSR", "l0605", "l0605", "lei-605-1949",
         "Repouso semanal remunerado (Lei nº 605, de 5 de janeiro de 1949)", 2),
    _act("lei-do-vale-transporte", "LVT", "l7418", "l7418-compilado", "lei-7418-1985",
         "Lei do Vale-Transporte (Lei nº 7.418, de 16 de dezembro de 1985)", 2),
]
PARTS: dict[str, list[str]] = {
    "a": ["lei-do-trabalho-rural", "lei-do-decimo-terceiro-salario", "lei-do-repouso-semanal-remunerado",
          "lei-do-vale-transporte"],
}
VERIFIED: list[str] = PARTS.get(PART, [])
ENABLED = [s for s in os.environ.get("BATCH17_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
for M in (B7, B8, B9, B10, B11, B12, B13, B14, B15, B16):
    M.ACTS[:] = ACTS
_PUB = "'Esta Lei entra em vigor na data de sua publicação'"
_L = B._act_law
ACT_DAY_ALL = {**B16.ACT_DAY_ALL,
}
ACT_LAWS_ALL = {**B16.ACT_LAWS_ALL,
}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

P.COURTS.clear()
P.NOTE_FIX = {}
B9.REPEALS.clear()
EXTRA: list[str] = []   # decisions added to the part

# ---------------------------------------------------------------------------------------------------------------
_inner17 = B6.PB5B._write_part5


def _inner(*a):
    B5.EXTRA_DECISIONS.extend(EXTRA)
    return _inner17(*a)


B6.PB5B._write_part5 = _inner

SRC = HERE / "sources_batch17.json"
if not SRC.exists():
    SRC.write_text('{\n "fetch": []\n}\n', encoding="utf-8", newline="\n")
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
