"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch9.json (SCHEMA.md corpus part): the acts in ALL_ACTS
below (more federal laws, as they are verified).

    python -X utf8 scripts/brazil-law/batch9/parse_batch9.py [--stats] [--dry]

Imports ../batch8/parse_batch8.py (which configures batch 7 and everything below it, plus batch 8's hand tools:
SPAN_FIX, COURT_SPLIT, LABEL_FIX, UNIT_FIX, NAV_LINES, EXTRA_LAWS) with no act of its own, and replaces only the
configuration: the acts, the in-force days, the hand tables for these acts, the pins and the output. Earlier parts are
not touched. No network.

BATCH9_ACTS=<slug,...> selects acts for trial runs (BATCH9_OUT=<file> writes elsewhere); by default VERIFIED is written.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH8_ACTS"] = "-"   # batch 8 configures no act of its own here
os.environ.pop("BATCH8_OUT", None)
sys.path.insert(0, str(FOLDER / "batch8"))
import parse_batch8 as B8  # noqa: E402

B7, B6, B5, B, P = B8.B7, B8.B6, B8.B5, B8.B, B8.P
PL = P.PL
B5.OUT = Path(os.environ.get("BATCH9_OUT") or FOLDER / "corpus.d" / "99-batch9.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = {
    "ctb": "leis/l9503.htm",
    "ctb-compilado": "leis/l9503compilado.htm",
    "ldb": "leis/l9394.htm",
    "ldb-compilado": "leis/l9394compilado.htm",
    "lsus": "leis/l8080.htm",
    "lel": "leis/l9504.htm",
    "lel-compilado": "leis/l9504compilado.htm",
    "cflo": "_ato2011-2014/2012/lei/l12651.htm",
    "cflo-compilado": "_ato2011-2014/2012/lei/l12651compilado.htm",
    "lrp": "leis/l6015consolidado.htm",
    "lrp-compilada": "leis/l6015compilada.htm",
    "l8666": "leis/l8666cons.htm",
}
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = B6.PAGES = B7.PAGES = B8.PAGES = PAGES


def _act(slug, short, page, consolidated, law, title, digits):
    return {"slug": slug, "short": short, "page": page, "consolidated": consolidated, "law": law, "title": title,
            "digits": digits, "url": PL + PAGES[page]}


ALL_ACTS: list[dict] = [
    _act("codigo-de-transito-brasileiro", "CTB", "ctb", "ctb-compilado", "lei-9503-1997",
         "Código de Trânsito Brasileiro (Lei nº 9.503, de 23 de setembro de 1997)", 3),
    _act("lei-de-diretrizes-e-bases-da-educacao", "LDB", "ldb", "ldb-compilado", "lei-9394-1996",
         "Lei de Diretrizes e Bases da Educação Nacional (Lei nº 9.394, de 20 de dezembro de 1996)", 2),
    _act("lei-organica-da-saude", "LOS", "lsus", "lsus", "lei-8080-1990",
         "Lei Orgânica da Saúde (Lei nº 8.080, de 19 de setembro de 1990)", 2),
    _act("lei-das-eleicoes", "LE", "lel", "lel-compilado", "lei-9504-1997",
         "Lei das Eleições (Lei nº 9.504, de 30 de setembro de 1997)", 3),
    _act("codigo-florestal", "CFlo", "cflo", "cflo-compilado", "lei-12651-2012",
         "Código Florestal (Lei nº 12.651, de 25 de maio de 2012)", 2),
    _act("lei-de-registros-publicos", "LRP", "lrp", "lrp-compilada", "lei-6015-1973",
         "Lei de Registros Públicos (Lei nº 6.015, de 31 de dezembro de 1973)", 3),
    _act("lei-de-licitacoes-de-1993", "L8666", "l8666", "l8666", "lei-8666-1993",
         "Lei de Licitações e Contratos (Lei nº 8.666, de 21 de junho de 1993)", 3),
]
VERIFIED: list[str] = ["lei-de-diretrizes-e-bases-da-educacao", "lei-organica-da-saude", "lei-das-eleicoes"]
ENABLED = [s for s in os.environ.get("BATCH9_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
B7.ACTS[:] = ACTS
B8.ACTS[:] = ACTS

ACT_DAY_ALL: dict[str, tuple[str, str]] = {
    "lei-9503-1997": ("1998-01-22", "Lei 9.503/1997 art. 340: 'Este Código entra em vigor cento e vinte dias após a data de "
                                    "sua publicação' (DOU 24.9.1997): 22.1.1998"),
    "lei-9394-1996": ("1996-12-23", "Lei 9.394/1996 art. 91: 'Esta Lei entra em vigor na data de sua publicação' (DOU "
                                    "23.12.1996)"),
    "lei-8080-1990": ("1990-09-20", "Lei 8.080/1990 art. 54: 'Esta lei entra em vigor na data de sua publicação' (DOU "
                                    "20.9.1990)"),
    "lei-9504-1997": ("1997-10-01", "Lei 9.504/1997 art. 106: 'Esta Lei entra em vigor na data de sua publicação' (DOU "
                                    "1.10.1997)"),
    "lei-12651-2012": ("2012-05-28", "Lei 12.651/2012 art. 84: 'Esta Lei entra em vigor na data de sua publicação' (DOU "
                                     "28.5.2012)"),
}
ACT_LAWS_ALL: dict[str, dict] = {
    "lei-9503-1997": B._act_law("Lei nº 9.503, de 1997", "Institui o Código de Trânsito Brasileiro.", "1997-09-23",
                                "1997-09-24", PAGES["ctb"]),
    "lei-9394-1996": B._act_law("Lei nº 9.394, de 1996", "Estabelece as diretrizes e bases da educação nacional.",
                                "1996-12-20", "1996-12-23", PAGES["ldb"]),
    "lei-8080-1990": B._act_law("Lei nº 8.080, de 1990", "Dispõe sobre as condições para a promoção, proteção e recuperação "
                                "da saúde, a organização e o funcionamento dos serviços correspondentes e dá outras "
                                "providências.", "1990-09-19", "1990-09-20", PAGES["lsus"]),
    "lei-9504-1997": B._act_law("Lei nº 9.504, de 1997", "Estabelece normas para as eleições.", "1997-09-30", "1997-10-01",
                                PAGES["lel"]),
    "lei-12651-2012": B._act_law("Lei nº 12.651, de 2012", "Dispõe sobre a proteção da vegetação nativa; altera as Leis nºs "
                                 "6.938, de 31 de agosto de 1981, 9.393, de 19 de dezembro de 1996, e 11.428, de 22 de "
                                 "dezembro de 2006; revoga as Leis nºs 4.771, de 15 de setembro de 1965, e 7.754, de 14 de "
                                 "abril de 1989, e a Medida Provisória nº 2.166-67, de 24 de agosto de 2001; e dá outras "
                                 "providências.", "2012-05-25", "2012-05-28", PAGES["cflo"]),
}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

B.EXPLAINED.clear()
B8.SPAN_FIX.clear()
B8.COURT_SPLIT.clear()
B8.LABEL_FIX.clear()
B8.UNIT_FIX.clear()
B8.NAV_LINES.clear()
B8.EXTRA_LAWS.clear()
P.COURTS = {}
P.NOTE_FIX = {}

# ---------------------------------------------------------------------------------------------------------------
# hand tables for these acts, each read from the official pages named in the reason
P.VIGENCIA_FIXED.update({
    "lei-10793-2003": ("2004-01-01", "art. 3: 'Esta Lei entra em vigor no ano letivo seguinte à data de sua publicação' "
                                     "(DOU 2.12.2003): the school year after publication is that of 2004; school years "
                                     "start on days each education system sets, so the change is dated 1.1.2004, the first "
                                     "day of that year"),
    "lei-11700-2008": ("2009-01-01", "art. 2: 'Esta Lei entra em vigor em 1º de janeiro do ano subseqüente ao de sua "
                                     "publicação' (DOU 16.6.2008)"),
    "lei-12061-2009": ("2010-01-01", "art. 3: 'Esta Lei entra em vigor em 1º de janeiro do ano subsequente ao de sua "
                                     "publicação oficial' (DOU 28.10.2009)"),
    "lei-14986-2024": ("2025-01-01", "art. 3: 'Esta Lei entra em vigor no ano subsequente ao de sua publicação' (DOU "
                                     "26.9.2024): 1.1.2025"),
})
P.MP_LAPSE.update({
    "mp-1303-2025": ("2025-10-09", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 67, de 2025 (DOU "
                                   "15.10.2025): 'teve seu prazo de vigência encerrado no dia 8 de outubro de 2025'"),
})
B8.UNIT_FIX[:] = [
    ("lel", "Art. 61A.", "art-061-a", "Art. 61-A",
     "Lei das Eleições: 'Art. 61A.' (Incluído pela Lei nº 10.408, de 2002) is filed as art. 61-A, not as a line of art. 61"),
    ("lsus", "Art. 6º A.", "art-06-a", "Art. 6º-A",
     "Lei Orgânica da Saúde: 'Art. 6º A.' (Incluído pela Lei nº 14.654, de 2023) is filed as art. 6º-A, not as a line of "
     "art. 6º"),
]
_Q = B7._QUOTED
B.EXPLAINED.update({
    "lei-das-eleicoes": {
        "art-037": "typesetting: a line of art. 37 ends without a full stop on the annotated page and with one on the "
                   "consolidated page",
        "art-051": "the consolidated page prints the note '(Inclçuído pela Lei nº 13.488, de 2017)' with a typing slip its "
                   "parser does not read as a note; the annotated page's note is read as a note",
        "art-057-a": "typesetting, as art. 37",
        "art-061": "the consolidated page keeps the placeholder 'Art. 61A. (Revogada pela Lei nº 10.740, de 2003)' under "
                   "art. 61; the history files art. 61-A on its own and leaves revoked text out",
        "art-102": _Q.format(x="Parágrafo único."),
    },
})

SRC = HERE / "sources_batch9.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
