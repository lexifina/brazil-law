"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch6.json (SCHEMA.md corpus part): the acts in ACTS
below (administrative improbity, environmental crimes, access to information, federal administrative procedure, and
further federal laws as they are verified).

    python -X utf8 scripts/brazil-law/batch6/parse_batch6.py [--stats] [--dry]

Imports ../batch5b/parse_batch5b.py (which configures ../batch5, ../batch4, ../batch3 and ../proc, the struck-text
replay of Planalto's annotated pages) and replaces only its configuration: the acts, the in-force days, the pins and
the output. Batch 5b's hand tables (MP fates, Senate resolutions, note fixes) stay in place; entries an act here does
not use are not printed. The parts of batch 5b and earlier are not touched (their parsers, run on their own, write the
same bytes as before). No network.

BATCH6_ACTS=<slug,...> selects acts for trial runs; by default the VERIFIED list is written.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
sys.path.insert(0, str(FOLDER / "batch5b"))
import parse_batch5b as PB5B  # noqa: E402  (configures batch 5 / 4 / 3 / parse_proc for batch 5b; reconfigured below)

B5, B4, B, P = PB5B.B5, PB5B.B4, PB5B.B, PB5B.P
PL = P.PL
B5.OUT = FOLDER / "corpus.d" / "99-batch6.json"
B5.STAGE = HERE / ".tmp" / "stage.json"
P.RETRIEVED = "2026-10-29"

PAGES = {k: v for k, v in PB5B.PAGES.items() if k in ("lia", "lia-compilada", "lca", "lai", "lpa")}
PAGES.update(EXTRA_PAGES := {})
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = PAGES

ALL_ACTS: list[dict] = [a for a in PB5B.ALL_ACTS if a["page"] in PAGES]
VERIFIED: list[str] = []
ENABLED = [s for s in os.environ.get("BATCH6_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = ACTS

# In-force days of the acts (their own closing clause and the DOU day; LC 95/1998 art. 8 § 1 counting).
ACT_DAY_ALL = dict(PB5B.ACT_DAY_ALL)
ACT_DAY_ALL.update({
    "lei-9605-1998": ("1998-03-30", "Lei 9.605/1998: its vigência article (art. 81) was vetoed, so LINDB art. 1 applies: in "
                                    "force 45 days after publication (DOU 13.2.1998), on 30.3.1998. The DOU of 17.2.1998 "
                                    "printed a retificação, but it corrects only the heading ('onde se lê: Nº 9.605, DE "
                                    "FEVEREIRO DE 1998 leia-se: LEI Nº 9.605, DE 12 DE FEVEREIRO DE 1998', as the Chamber of "
                                    "Deputies' record of the law gives it), not the law's text, so it is not a new "
                                    "publication of the text that would restart the period (LINDB art. 1 § 3)"),
    "lei-9784-1999": ("1999-02-01", "Lei 9.784/1999 art. 70: 'Esta Lei entra em vigor na data de sua publicação' (DOU "
                                    "1.2.1999). The retificação in the DOU of 11.3.1999 corrects only the signatures ('Na "
                                    "página 5, 1ª coluna, nas assinaturas, leia-se: Fernando Henrique Cardoso, Renan "
                                    "Calheiros e Paulo Paiva', as the Chamber of Deputies' record of the law gives it), not "
                                    "the law's text"),
})
ACT_LAWS_ALL = dict(PB5B.ACT_LAWS_ALL)
ACT_LAWS_ALL.update({
    "lei-9605-1998": B._act_law("Lei nº 9.605, de 1998", "Dispõe sobre as sanções penais e administrativas derivadas de "
                                "condutas e atividades lesivas ao meio ambiente, e dá outras providências.", "1998-02-12",
                                "1998-02-13", PAGES["lca"]),
    "lei-9784-1999": B._act_law("Lei nº 9.784, de 1999", "Regula o processo administrativo no âmbito da Administração "
                                "Pública Federal.", "1999-01-29", "1999-02-01", PAGES["lpa"]),
})
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# Amending laws whose own vigência is staged by level of government: dated by the first day the new wording was law
# (for the União, the States and the Distrito Federal); the later day for the other levels is given in the reason.
P.VIGENCIA_FIXED["lei-13019-2014"] = (
    "2016-01-23", "art. 88 as amended by Lei 13.204/2015: 'Esta Lei entra em vigor após decorridos quinhentos e quarenta "
                  "dias de sua publicação oficial' (DOU 1.8.2014: the 540th day counted from publication is 22.1.2016, "
                  "LC 95/1998 art. 8 § 1), and § 1: 'Para os Municípios, esta Lei entra em vigor a partir de 1º de janeiro "
                  "de 2017'. Its changes are dated 23.1.2016, the day they became law for the União, the States and the "
                  "Distrito Federal; for the Municípios they applied from 1.1.2017")
P.VIGENCIA_FIXED["lei-14129-2021"] = (
    "2021-06-28", "art. 55: 'Esta Lei entra em vigor após decorridos: I - 90 (noventa) dias de sua publicação oficial, "
                  "para a União; II - 120 (cento e vinte) dias [...] para os Estados e o Distrito Federal; III - 180 (cento "
                  "e oitenta) dias [...] para os Municípios' (DOU 30.3.2021: the 90th day counted from publication is "
                  "27.6.2021, LC 95/1998 art. 8 § 1). Its changes are dated 28.6.2021, the day they became law for the "
                  "União; for the States and the Distrito Federal they applied from 28.7.2021, for the Municípios from "
                  "26.9.2021")

SRC = HERE / "sources_batch6.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
