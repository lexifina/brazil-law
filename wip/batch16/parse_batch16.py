"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch16<x>.json (SCHEMA.md corpus parts): more major federal
acts not yet in the corpus, in small parts of 2-4 acts each (99-batch16a, 99-batch16b, ...).

    BATCH16_PART=a python -X utf8 scripts/brazil-law/batch16/parse_batch16.py [--stats] [--dry]

Imports ../batch15/parse_batch15.py (which configures batch 14 and everything below it, plus batch 15's hand tables and
the Medida Provisória 905/955 model) with no act of its own, and replaces only the configuration: the acts, the in-force
days, the hand tables for these acts, the pins and the output. Earlier parts are not touched. No network.

BATCH16_PART selects the part (its acts are PARTS[part]); BATCH16_ACTS=<slug,...> selects acts for trial runs
(BATCH16_OUT=<file> writes elsewhere). After writing a part run ../effects_fix.py on it (effect days).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH15_PART"] = "-"   # batch 15 configures no act of its own here
os.environ.pop("BATCH15_ACTS", None)
os.environ.pop("BATCH15_OUT", None)
sys.path.insert(0, str(FOLDER / "batch15"))
import parse_batch15 as B15  # noqa: E402

B14, B13, B12, B11, B10, B9, B8, B7, B6, B5, B, P = (B15.B14, B15.B13, B15.B12, B15.B11, B15.B10, B15.B9, B15.B8, B15.B7,
                                                     B15.B6, B15.B5, B15.B, B15.P)
PL = P.PL
PART = os.environ.get("BATCH16_PART", "a")
B5.OUT = Path(os.environ.get("BATCH16_OUT") or FOLDER / "corpus.d" / f"99-batch16{PART}.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = dict(B15.PAGES)
PAGES.update({
    # batch 13's deferred acts (their page ids as pinned in batch13/sources_batch13.json)
    "l4320": "leis/l4320.htm",
    "l4320-compilado": "leis/l4320compilado.htm",
    "lfgts": "leis/l8036consol.htm",
    "lfgts-compilada": "leis/l8036compilada.htm",
})
B.PAGES.clear()
B.PAGES.update(PAGES)
for M in (B5, B6, B7, B8, B9, B10, B11, B12, B13, B14, B15):
    M.PAGES = PAGES

_CBA, _L4320, _FGTS = "codigo-brasileiro-de-aeronautica", "lei-4320-de-1964", "lei-do-fgts"
ALL_ACTS: list[dict] = ([a for a in B14.ALL_ACTS if a["slug"] == _CBA]
                        + [a for a in B13.ALL_ACTS if a["slug"] in (_L4320, _FGTS)])
PARTS: dict[str, list[str]] = {
    "a": [_CBA],
}
VERIFIED: list[str] = PARTS.get(PART, [])
ENABLED = [s for s in os.environ.get("BATCH16_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
for M in (B7, B8, B9, B10, B11, B12, B13, B14, B15):
    M.ACTS[:] = ACTS
ACT_DAY_ALL = {**B13.ACT_DAY_ALL, **B14.ACT_DAY_ALL}
ACT_LAWS_ALL = {**B13.ACT_LAWS_ALL, **B14.ACT_LAWS_ALL}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# earlier batches' printed-everywhere lists emptied (their act-keyed tables do nothing here)
P.COURTS.clear()
P.NOTE_FIX = {}
B9.REPEALS.clear()
EXTRA: list[str] = []   # decisions added to the part

# ---------------------------------------------------------------------------------------------------------------
# Código Brasileiro de Aeronáutica (Lei 7.565/1986), part a
P.VIGENCIA_FIXED["mp-1089-2021"] = (
    "2021-12-30", "art. 6: 'Esta Medida Provisória entra em vigor: I - após noventa dias da sua publicação, quanto ao Anexo; e "
                  "II - na data de sua publicação, quanto aos demais dispositivos' (DOU 30.12.2021): its changes to the Código "
                  "Brasileiro de Aeronáutica fall under II (the Anexo is Lei 11.182/2005's fee table)")
P.MP_LAPSE["mp-1240-2024"] = (
    "2024-11-07", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 112, de 2024 (DOU 14.11.2024): 'teve seu "
                  "prazo de vigência encerrado no dia 6 de novembro de 2024'")

# ---------------------------------------------------------------------------------------------------------------
_inner16 = B6.PB5B._write_part5


def _inner(*a):
    B5.EXTRA_DECISIONS.extend(EXTRA)
    return _inner16(*a)


B6.PB5B._write_part5 = _inner

SRC = HERE / "sources_batch16.json"
if not SRC.exists():
    SRC.write_text('{\n "fetch": []\n}\n', encoding="utf-8", newline="\n")
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
