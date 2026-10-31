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
VERIFIED: list[str] = ["lei-de-execucao-fiscal", "lei-de-defesa-da-concorrencia", "estatuto-da-advocacia", "lei-da-adi-e-da-adc",
                        "lei-da-adpf", "lei-dos-crimes-contra-a-ordem-tributaria", "lei-de-interceptacao-telefonica",
                        "lei-do-bem-de-familia", "lei-da-acao-popular", "lei-dos-crimes-contra-o-sistema-financeiro"]
ENABLED = [s for s in os.environ.get("BATCH11_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
B7.ACTS[:] = ACTS
B8.ACTS[:] = ACTS
B9.ACTS[:] = ACTS
B10.ACTS[:] = ACTS

# in-force day of each act as enacted, and its own law record (filled from each page as it is read)
_PUB = "'Esta Lei entra em vigor na data de sua publicação'"
ACT_DAY_ALL: dict[str, tuple[str, str]] = {
    "lei-6830-1980": ("1980-12-23", "Lei 6.830/1980 art. 42: 'esta Lei entrará em vigor 90 (noventa) dias após a data de sua "
                                    "publicação' (DOU 24.9.1980): 24.9.1980 + 90 days"),
    "lei-12529-2011": ("2012-05-29", "Lei 12.529/2011 art. 128: 'Esta Lei entra em vigor após decorridos 180 (cento e oitenta) "
                                     "dias de sua publicação oficial' (DOU 1.12.2011, rectified 2.12.2011; Planalto's page "
                                     "misprints '1º.11.2011'): the 180th day counted from publication is 28.5.2012 (LC 95/1998 "
                                     "art. 8 § 1)"),
    "lei-8906-1994": ("1994-07-05", f"Lei 8.906/1994 art. 86: {_PUB} (DOU 5.7.1994)"),
    "lei-9868-1999": ("1999-11-11", f"Lei 9.868/1999 art. 31: {_PUB} (DOU 11.11.1999)"),
    "lei-9882-1999": ("1999-12-06", f"Lei 9.882/1999 art. 14: {_PUB} (DOU 6.12.1999)"),
    "lei-8137-1990": ("1990-12-28", f"Lei 8.137/1990 art. 22: {_PUB} (DOU 28.12.1990)"),
    "lei-9296-1996": ("1996-07-25", f"Lei 9.296/1996 art. 11: {_PUB} (DOU 25.7.1996)"),
    "lei-8009-1990": ("1990-03-30", f"Lei 8.009/1990 art. 7: {_PUB} (DOU 30.3.1990); the conversion of Medida Provisória nº "
                                    "143, de 8.3.1990, whose own text Planalto's page does not give"),
    "lei-4717-1965": ("1965-08-19", "Lei 4.717/1965 has no vigência clause: LINDB art. 1, 45 days after publication in the DOU "
                                    "of 5.7.1965 (republished 8.4.1974)"),
    "lei-7492-1986": ("1986-06-18", f"Lei 7.492/1986 art. 34: {_PUB} (DOU 18.6.1986)"),
    "lei-9656-1998": ("1998-09-02", "Lei 9.656/1998 art. 36: 'Esta Lei entra em vigor noventa dias após a data de sua "
                                    "publicação' (DOU 4.6.1998): 4.6.1998 + 90 days (LC 95/1998 art. 8 § 1)"),
    "lei-6385-1976": ("1976-12-09", f"Lei 6.385/1976 art. 34 (now 35): {_PUB} (DOU 9.12.1976)"),
    "lei-6766-1979": ("1979-12-20", f"Lei 6.766/1979 art. 54: {_PUB} (DOU 20.12.1979)"),
    "lei-8742-1993": ("1993-12-08", f"Lei 8.742/1993 art. 41: {_PUB} (DOU 8.12.1993)"),
}
_L = B._act_law
ACT_LAWS_ALL: dict[str, dict] = {
    "lei-6830-1980": _L("Lei nº 6.830, de 1980", "Dispõe sobre a cobrança judicial da Dívida Ativa da Fazenda Pública, e dá "
                        "outras providências.", "1980-09-22", "1980-09-24", PAGES["lef"]),
    "lei-12529-2011": _L("Lei nº 12.529, de 2011", "Estrutura o Sistema Brasileiro de Defesa da Concorrência; dispõe sobre a "
                         "prevenção e repressão às infrações contra a ordem econômica; altera a Lei nº 8.137, de 27 de dezembro "
                         "de 1990, o Decreto-Lei nº 3.689, de 3 de outubro de 1941 - Código de Processo Penal, e a Lei nº 7.347, "
                         "de 24 de julho de 1985; revoga dispositivos da Lei nº 8.884, de 11 de junho de 1994, e a Lei nº 9.781, "
                         "de 19 de janeiro de 1999; e dá outras providências.", "2011-11-30", "2011-12-01", PAGES["lcade"]),
    "lei-8906-1994": _L("Lei nº 8.906, de 1994", "Dispõe sobre o Estatuto da Advocacia e a Ordem dos Advogados do Brasil (OAB).",
                        "1994-07-04", "1994-07-05", PAGES["eoab"]),
    "lei-9868-1999": _L("Lei nº 9.868, de 1999", "Dispõe sobre o processo e julgamento da ação direta de inconstitucionalidade e "
                        "da ação declaratória de constitucionalidade perante o Supremo Tribunal Federal.", "1999-11-10",
                        "1999-11-11", PAGES["ladi"]),
    "lei-9882-1999": _L("Lei nº 9.882, de 1999", "Dispõe sobre o processo e julgamento da argüição de descumprimento de preceito "
                        "fundamental, nos termos do § 1º do art. 102 da Constituição Federal.", "1999-12-03", "1999-12-06",
                        PAGES["ladpf"]),
    "lei-8137-1990": _L("Lei nº 8.137, de 1990", "Define crimes contra a ordem tributária, econômica e contra as relações de "
                        "consumo, e dá outras providências.", "1990-12-27", "1990-12-28", PAGES["lcot"]),
    "lei-9296-1996": _L("Lei nº 9.296, de 1996", "Regulamenta o inciso XII, parte final, do art. 5º da Constituição Federal.",
                        "1996-07-24", "1996-07-25", PAGES["lit"]),
    "lei-8009-1990": _L("Lei nº 8.009, de 1990", "Dispõe sobre a impenhorabilidade do bem de família.", "1990-03-29",
                        "1990-03-30", PAGES["lbf"]),
    "lei-4717-1965": _L("Lei nº 4.717, de 1965", "Regula a ação popular.", "1965-06-29", "1965-07-05", PAGES["lap"]),
    "lei-7492-1986": _L("Lei nº 7.492, de 1986", "Define os crimes contra o sistema financeiro nacional, e dá outras "
                        "providências.", "1986-06-16", "1986-06-18", PAGES["lcsf"]),
    "lei-9656-1998": _L("Lei nº 9.656, de 1998", "Dispõe sobre os planos e seguros privados de assistência à saúde.",
                        "1998-06-03", "1998-06-04", PAGES["lps"]),
    "lei-6385-1976": _L("Lei nº 6.385, de 1976", "Dispõe sobre o mercado de valores mobiliários e cria a Comissão de Valores "
                        "Mobiliários.", "1976-12-07", "1976-12-09", PAGES["lcvm"]),
    "lei-6766-1979": _L("Lei nº 6.766, de 1979", "Dispõe sobre o Parcelamento do Solo Urbano e dá outras Providências.",
                        "1979-12-19", "1979-12-20", PAGES["lpsolo"]),
    "lei-8742-1993": _L("Lei nº 8.742, de 1993", "Dispõe sobre a organização da Assistência Social e dá outras providências.",
                        "1993-12-07", "1993-12-08", PAGES["loas"]),
}
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
P.VIGENCIA_FIXED.update({
    "lei-8176-1991": ("1991-02-18", "art. 6 (as printed): 'Esta lei entra em vigor cinco dias após a sua publicação' (DOU "
                                    "13.2.1991): 13.2.1991 + 5 days"),
    "mp-687-2015": ("2015-08-18", "art. 4 II: in force 'na data de sua publicação' (DOU 18.8.2015) for every provision but "
                                  "the new wording of Lei 12.529/2011 art. 23 caput (art. 4 I: 1.1.2016), which Planalto's page does not "
                                  "print; its wording of the parágrafo único is in force from publication"),
    "lei-13196-2015": ("2015-12-02", "art. 5 II: in force 'na data de sua publicação' (DOU 2.12.2015) for every provision but "
                                     "the wording its art. 2 gives Lei 12.529/2011 art. 23 (art. 5 I: 1.1.2016)"),
    "mp-871-2019": ("2019-01-18", "art. 34 III: in force 'na data de sua publicação' (DOU 18.1.2019, edição extra) for every "
                                  "provision but its change to Lei 8.742/1993 art. 20 § 13 (art. 34 I, 90 days) and to Lei "
                                  "8.213/1991 art. 74 § 3º (art. 34 II, 120 days)"),
})
P.VETO_PROMULGATION = {
    "lei-13964-2019": ("2021-04-30", "the parts of Lei 13.964/2019 vetoed on 24.12.2019 were promulgated after Congress "
                                     "overrode the veto (CF art. 66 § 5; DOU 30.4.2021, printed at the end of the Lei "
                                     "13.964 page): Lei de Interceptação Telefônica art. 8º-A §§ 2º and 4º read '(VETADO)' "
                                     "until then"),
}
P.VETO_PROMULGATED_UNITS = {"lei-13964-2019": {("lei-de-interceptacao-telefonica", "art-08-a", "§ 2º"),
                                                  ("lei-de-interceptacao-telefonica", "art-08-a", "§ 4º")}}
P.VIGENCIA_PROVISION.update({
    ("lei-13196-2015", "lei-de-defesa-da-concorrencia", "art-023"): (
        "2016-01-01", "Lei 13.196/2015 art. 5 I: its wording of art. 23 in force on 1.1.2016"),
    ("mp-871-2019", "lei-organica-da-assistencia-social", "art-20"): (
        "2019-04-18", "Medida Provisória nº 871/2019 art. 34 I: its change to art. 20 § 13 in force 90 days after publication "
                      "(DOU 18.1.2019)"),
})

SRC = HERE / "sources_batch11.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
