"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch14<x>.json (SCHEMA.md corpus parts): more major federal
acts not yet in the corpus, published in small parts of 2-4 acts each (99-batch14a, 99-batch14b, ...).

    BATCH14_PART=a python -X utf8 scripts/brazil-law/batch14/parse_batch14.py [--stats] [--dry]

Imports ../batch13/parse_batch13.py (which configures batch 12 and everything below it, plus batch 13's hand tables) with
no act of its own, and replaces only the configuration: the acts, the in-force days, the hand tables for these acts, the
pins and the output. Earlier parts are not touched. No network.

BATCH14_PART selects the part (its acts are PARTS[part]); BATCH14_ACTS=<slug,...> selects acts for trial runs
(BATCH14_OUT=<file> writes elsewhere).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH13_ACTS"] = "-"   # batch 13 configures no act of its own here
os.environ.pop("BATCH13_OUT", None)
os.environ.pop("BATCH13_PART", None)
sys.path.insert(0, str(FOLDER / "batch13"))
import parse_batch13 as B13  # noqa: E402

B12, B11, B10, B9, B8, B7, B6, B5, B, P = (B13.B12, B13.B11, B13.B10, B13.B9, B13.B8, B13.B7, B13.B6, B13.B5, B13.B,
                                           B13.P)
PL = P.PL
PART = os.environ.get("BATCH14_PART", "a")
B5.OUT = Path(os.environ.get("BATCH14_OUT") or FOLDER / "corpus.d" / f"99-batch14{PART}.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = {
    # 14a
    "lc87": "leis/lcp/lcp87.htm",
    "lc116": "leis/lcp/lcp116.htm",
    # next parts
    "l8212": "leis/l8212cons.htm",
    "l8212-compilado": "leis/l8212compilado.htm",
    "l8213": "leis/l8213cons.htm",
    "l8213-compilado": "leis/l8213compilado.htm",
    "lc123": "leis/lcp/lcp123.htm",
    "l4504": "leis/l4504.htm",
    "l4504-compilada": "leis/l4504compilada.htm",
    "l9472": "leis/l9472.htm",
    "l9433": "leis/l9433.htm",
    "l9985": "leis/l9985.htm",
    "l13874": "_ato2019-2022/2019/lei/l13874.htm",
    "l7565": "leis/l7565.htm",
    "l7565-compilado": "leis/l7565compilado.htm",
    "l12288": "_ato2007-2010/2010/lei/l12288.htm",
    "l1521": "leis/l1521.htm",
    "dl201": "decreto-lei/del0201.htm",
}
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = B6.PAGES = B7.PAGES = B8.PAGES = B9.PAGES = B10.PAGES = B11.PAGES = B12.PAGES = B13.PAGES = PAGES


def _act(slug, short, page, consolidated, law, title, digits):
    return {"slug": slug, "short": short, "page": page, "consolidated": consolidated, "law": law, "title": title,
            "digits": digits, "url": PL + PAGES[page]}


ALL_ACTS: list[dict] = [
    _act("lei-kandir", "LC87", "lc87", "lc87", "lc-87-1996",
         "Lei Kandir - ICMS (Lei Complementar nº 87, de 13 de setembro de 1996)", 2),
    _act("lei-do-iss", "LC116", "lc116", "lc116", "lc-116-2003",
         "Lei do ISS (Lei Complementar nº 116, de 31 de julho de 2003)", 2),
    _act("lei-de-custeio-da-seguridade-social", "LOSS", "l8212", "l8212-compilado", "lei-8212-1991",
         "Lei Orgânica da Seguridade Social - custeio (Lei nº 8.212, de 24 de julho de 1991)", 3),
    _act("lei-de-beneficios-da-previdencia-social", "LBPS", "l8213", "l8213-compilado", "lei-8213-1991",
         "Lei de Benefícios da Previdência Social (Lei nº 8.213, de 24 de julho de 1991)", 3),
    _act("estatuto-da-microempresa", "LC123", "lc123", "lc123", "lc-123-2006",
         "Estatuto Nacional da Microempresa e da Empresa de Pequeno Porte - Simples Nacional (Lei Complementar nº 123, "
         "de 14 de dezembro de 2006)", 2),
    _act("estatuto-da-terra", "ET", "l4504", "l4504-compilada", "lei-4504-1964",
         "Estatuto da Terra (Lei nº 4.504, de 30 de novembro de 1964)", 3),
    _act("lei-geral-de-telecomunicacoes", "LGT", "l9472", "l9472", "lei-9472-1997",
         "Lei Geral de Telecomunicações (Lei nº 9.472, de 16 de julho de 1997)", 3),
    _act("lei-das-aguas", "LAg", "l9433", "l9433", "lei-9433-1997",
         "Política Nacional de Recursos Hídricos (Lei nº 9.433, de 8 de janeiro de 1997)", 2),
    _act("lei-do-snuc", "SNUC", "l9985", "l9985", "lei-9985-2000",
         "Sistema Nacional de Unidades de Conservação da Natureza (Lei nº 9.985, de 18 de julho de 2000)", 2),
    _act("lei-da-liberdade-economica", "LLE", "l13874", "l13874", "lei-13874-2019",
         "Lei da Liberdade Econômica (Lei nº 13.874, de 20 de setembro de 2019)", 2),
    _act("codigo-brasileiro-de-aeronautica", "CBA", "l7565", "l7565-compilado", "lei-7565-1986",
         "Código Brasileiro de Aeronáutica (Lei nº 7.565, de 19 de dezembro de 1986)", 3),
    _act("estatuto-da-igualdade-racial", "EIR", "l12288", "l12288", "lei-12288-2010",
         "Estatuto da Igualdade Racial (Lei nº 12.288, de 20 de julho de 2010)", 2),
    _act("lei-dos-crimes-contra-a-economia-popular", "LCEP", "l1521", "l1521", "lei-1521-1951",
         "Crimes contra a economia popular (Lei nº 1.521, de 26 de dezembro de 1951)", 2),
    _act("lei-dos-crimes-de-responsabilidade-dos-prefeitos", "DL201", "dl201", "dl201", "dl-201-1967",
         "Responsabilidade dos prefeitos e vereadores (Decreto-Lei nº 201, de 27 de fevereiro de 1967)", 2),
]
PARTS: dict[str, list[str]] = {
    "a": ["lei-kandir", "lei-do-iss"],
}
VERIFIED: list[str] = PARTS.get(PART, [])
ENABLED = [s for s in os.environ.get("BATCH14_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
for M in (B7, B8, B9, B10, B11, B12, B13):
    M.ACTS[:] = ACTS

_PUB = "'Esta Lei entra em vigor na data de sua publicação'"
ACT_DAY_ALL: dict[str, tuple[str, str]] = {
    "lc-87-1996": ("1996-11-01", "Lei Complementar 87/1996 art. 36: 'Esta Lei Complementar entra em vigor no primeiro dia do "
                                 "segundo mês seguinte ao da sua publicação, observado o disposto nos arts. 32 e 33 e no Anexo' "
                                 "(DOU 16.9.1996): 1.11.1996; art. 32 (exports, credits) and the Anexo applied from publication, "
                                 "16.9.1996, which the history does not separate (the act's first version is 1.11.1996)"),
    "lc-116-2003": ("2003-08-01", "Lei Complementar 116/2003 art. 9: 'Esta Lei Complementar entra em vigor na data de sua "
                                  "publicação' (DOU 1.8.2003)"),
}
_L = B._act_law
ACT_LAWS_ALL: dict[str, dict] = {
    "lc-87-1996": _L("Lei Complementar nº 87, de 1996", "Dispõe sobre o imposto dos Estados e do Distrito Federal sobre "
                     "operações relativas à circulação de mercadorias e sobre prestações de serviços de transporte "
                     "interestadual e intermunicipal e de comunicação, e dá outras providências. (LEI KANDIR)", "1996-09-13",
                     "1996-09-16", PAGES["lc87"]),
    "lc-116-2003": _L("Lei Complementar nº 116, de 2003", "Dispõe sobre o Imposto Sobre Serviços de Qualquer Natureza, de "
                      "competência dos Municípios e do Distrito Federal, e dá outras providências.", "2003-07-31", "2003-08-01",
                      PAGES["lc116"]),
}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# batch 13's act-specific tools emptied (law facts in VIGENCIA_FIXED, MP_LAPSE, ... are kept: printed only where used)
B.EXPLAINED.clear()
B8.SPAN_FIX.clear()
B8.LABEL_FIX.clear()
B9.WORD_FIX.clear()
P.VETO_PROMULGATION = {}
P.VETO_PROMULGATED_UNITS = {}
P.NOTE_FIX = {}
B13.OPEN_ITEMS.clear()

# ---------------------------------------------------------------------------------------------------------------
# hand tables for these acts, each read from the official pages named in the reason

OPEN_ITEMS = B13.OPEN_ITEMS

SRC = HERE / "sources_batch14.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
