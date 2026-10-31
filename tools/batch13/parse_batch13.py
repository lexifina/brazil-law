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
    # 13b
    "lgreve": "leis/l7783.htm",
    "lcp150": "leis/lcp/lcp150.htm",
    "ltemp": "leis/l6019.htm",
    "ltemp-compilado": "leis/l6019compilado.htm",
    # 13c
    "lcondo": "leis/l4591.htm",
    "lcondo-compilado": "leis/l4591compilado.htm",
    "lsfi": "leis/l9514.htm",
    "dl911": "decreto-lei/1965-1988/del0911.htm",
    "dl911-compilado": "decreto-lei/1965-1988/del0911compilado.htm",
    # 13d
    "l4320": "leis/l4320.htm",
    "l4320-compilado": "leis/l4320compilado.htm",
    "lestatais": "_ato2015-2018/2016/lei/l13303.htm",
    "lpp": "leis/l9096.htm",
    "lpp-compilado": "leis/l9096compilado.htm",
    # 13e
    "lmig": "_ato2015-2018/2017/lei/l13445.htm",
    "lref": "leis/l9474.htm",
    "lterr": "_ato2015-2018/2016/lei/l13260.htm",
    "lpt": "leis/l7960.htm",
    # 13f
    "lfgts": "leis/l8036consol.htm",
    "lfgts-compilada": "leis/l8036compilada.htm",
    "lsfn": "leis/l4595.htm",
    "lsfn-compilado": "leis/l4595compilado.htm",
    "lcheque": "leis/l7357.htm",
    # 13g
    "ldup": "leis/l5474.htm",
    "ldup-compilado": "leis/l5474compilado.htm",
    "lcart": "leis/l8935.htm",
    "ltcu": "leis/l8443.htm",
    "ljef": "leis/leis_2001/l10259.htm",
    # 13h
    "ljefp": "_ato2007-2010/2009/lei/l12153.htm",
    "l8038": "leis/l8038.htm",
    "lalim": "leis/l5478.htm",
    "lpnrs": "_ato2007-2010/2010/lei/l12305.htm",
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
    _act("lei-de-greve", "LG", "lgreve", "lgreve", "lei-7783-1989",
         "Lei de Greve (Lei nº 7.783, de 28 de junho de 1989)", 2),
    _act("lei-do-trabalho-domestico", "LCTD", "lcp150", "lcp150", "lc-150-2015",
         "Lei do Trabalho Doméstico (Lei Complementar nº 150, de 1º de junho de 2015)", 2),
    _act("lei-do-trabalho-temporario", "LTT", "ltemp", "ltemp-compilado", "lei-6019-1974",
         "Lei do Trabalho Temporário e da Terceirização (Lei nº 6.019, de 3 de janeiro de 1974)", 2),
    _act("lei-de-condominios-e-incorporacoes", "LCI", "lcondo", "lcondo-compilado", "lei-4591-1964",
         "Lei de Condomínios e Incorporações (Lei nº 4.591, de 16 de dezembro de 1964)", 2),
    _act("lei-da-alienacao-fiduciaria-de-imoveis", "LSFI", "lsfi", "lsfi", "lei-9514-1997",
         "Sistema de Financiamento Imobiliário e alienação fiduciária de imóvel (Lei nº 9.514, de 20 de novembro de 1997)", 2),
    _act("lei-da-alienacao-fiduciaria", "DL911", "dl911", "dl911-compilado", "dl-911-1969",
         "Alienação fiduciária em garantia (Decreto-Lei nº 911, de 1º de outubro de 1969)", 2),
    _act("lei-4320-de-1964", "L4320", "l4320", "l4320-compilado", "lei-4320-1964",
         "Normas gerais de direito financeiro (Lei nº 4.320, de 17 de março de 1964)", 3),
    _act("lei-das-estatais", "LEst", "lestatais", "lestatais", "lei-13303-2016",
         "Lei das Estatais (Lei nº 13.303, de 30 de junho de 2016)", 2),
    _act("lei-dos-partidos-politicos", "LPP", "lpp", "lpp-compilado", "lei-9096-1995",
         "Lei dos Partidos Políticos (Lei nº 9.096, de 19 de setembro de 1995)", 2),
    _act("lei-de-migracao", "LMig", "lmig", "lmig", "lei-13445-2017",
         "Lei de Migração (Lei nº 13.445, de 24 de maio de 2017)", 3),
    _act("estatuto-dos-refugiados", "LRef", "lref", "lref", "lei-9474-1997",
         "Estatuto dos Refugiados (Lei nº 9.474, de 22 de julho de 1997)", 2),
    _act("lei-antiterrorismo", "LAT", "lterr", "lterr", "lei-13260-2016",
         "Lei Antiterrorismo (Lei nº 13.260, de 16 de março de 2016)", 2),
    _act("lei-da-prisao-temporaria", "LPT", "lpt", "lpt", "lei-7960-1989",
         "Lei da Prisão Temporária (Lei nº 7.960, de 21 de dezembro de 1989)", 2),
    _act("lei-do-fgts", "LFGTS", "lfgts", "lfgts-compilada", "lei-8036-1990",
         "Lei do FGTS (Lei nº 8.036, de 11 de maio de 1990)", 2),
    _act("lei-do-sistema-financeiro-nacional", "LSFN", "lsfn", "lsfn-compilado", "lei-4595-1964",
         "Lei do Sistema Financeiro Nacional (Lei nº 4.595, de 31 de dezembro de 1964)", 2),
    _act("lei-do-cheque", "LCh", "lcheque", "lcheque", "lei-7357-1985",
         "Lei do Cheque (Lei nº 7.357, de 2 de setembro de 1985)", 2),
    _act("lei-das-duplicatas", "LDup", "ldup", "ldup-compilado", "lei-5474-1968",
         "Lei das Duplicatas (Lei nº 5.474, de 18 de julho de 1968)", 2),
    _act("lei-dos-cartorios", "LNR", "lcart", "lcart", "lei-8935-1994",
         "Lei dos Cartórios (Lei nº 8.935, de 18 de novembro de 1994)", 2),
    _act("lei-organica-do-tcu", "LOTCU", "ltcu", "ltcu", "lei-8443-1992",
         "Lei Orgânica do Tribunal de Contas da União (Lei nº 8.443, de 16 de julho de 1992)", 3),
    _act("lei-dos-juizados-especiais-federais", "LJEF", "ljef", "ljef", "lei-10259-2001",
         "Lei dos Juizados Especiais Federais (Lei nº 10.259, de 12 de julho de 2001)", 2),
    _act("lei-dos-juizados-da-fazenda-publica", "LJEFP", "ljefp", "ljefp", "lei-12153-2009",
         "Lei dos Juizados Especiais da Fazenda Pública (Lei nº 12.153, de 22 de dezembro de 2009)", 2),
    _act("lei-8038-de-1990", "L8038", "l8038", "l8038", "lei-8038-1990",
         "Processos perante o STJ e o STF (Lei nº 8.038, de 28 de maio de 1990)", 2),
    _act("lei-de-alimentos", "LAlim", "lalim", "lalim", "lei-5478-1968",
         "Lei de Alimentos (Lei nº 5.478, de 25 de julho de 1968)", 2),
    _act("politica-nacional-de-residuos-solidos", "PNRS", "lpnrs", "lpnrs", "lei-12305-2010",
         "Política Nacional de Resíduos Sólidos (Lei nº 12.305, de 2 de agosto de 2010)", 2),
]
PARTS: dict[str, list[str]] = {
    "a": ["lei-das-contravencoes-penais", "lei-dos-crimes-de-responsabilidade", "lei-do-crime-racial"],
    "b": ["lei-de-greve", "lei-do-trabalho-domestico", "lei-do-trabalho-temporario"],
    "d": ["lei-das-estatais", "lei-dos-partidos-politicos"],
    "f": ["lei-do-sistema-financeiro-nacional", "lei-do-cheque"],
    "g": ["lei-das-duplicatas", "lei-dos-cartorios", "lei-organica-do-tcu", "lei-dos-juizados-especiais-federais"],
    "h": ["lei-dos-juizados-da-fazenda-publica", "lei-8038-de-1990", "lei-de-alimentos",
          "politica-nacional-de-residuos-solidos"],
    "e": ["lei-de-migracao", "estatuto-dos-refugiados", "lei-antiterrorismo", "lei-da-prisao-temporaria"],
    "c": ["lei-de-condominios-e-incorporacoes", "lei-da-alienacao-fiduciaria-de-imoveis", "lei-da-alienacao-fiduciaria"],
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
    "lei-7783-1989": ("1989-06-29", f"Lei 7.783/1989 art. 19: {_PUB} (DOU 29.6.1989)"),
    "lc-150-2015": ("2015-06-02", f"Lei Complementar 150/2015 art. 47: 'Esta Lei entra em vigor na data de sua publicação' "
                                  "(DOU 2.6.2015)"),
    "lei-6019-1974": ("1974-03-05", "Lei 6.019/1974 art. 20: 'Esta Lei entrará em vigor sessenta dias após sua publicação' "
                                    "(DOU 4.1.1974): 4.1.1974 + 60 days"),
    "lei-4591-1964": ("1964-12-21", "Lei 4.591/1964 art. 70: 'A presente lei entrará em vigor na data de sua publicação' (DOU "
                                    "21.12.1964, rectified 1.2.1965)"),
    "lei-9514-1997": ("1997-11-21", f"Lei 9.514/1997 art. 42: {_PUB} (DOU 21.11.1997, rectified 24.11.1997)"),
    "dl-911-1969": ("1969-10-03", "Decreto-Lei 911/1969 art. 9: 'O presente Decreto-lei entrará em vigor na data de sua "
                                  "publicação' (DOU 3.10.1969)"),
    "lei-4320-1964": ("1964-05-07", "Lei 4.320/1964 has no vigência clause (its art. 114 counts its effects from 1.1.1964 for "
                                    "the budgets and from 1.1.1965 for the rest): LINDB art. 1, 45 days after publication in "
                                    "the DOU of 23.3.1964 (rectified 9.4.1964 and 3.6.1964); the vetoed parts Congress kept "
                                    "were promulgated in the DOU of 5.5.1964, before that day"),
    "lei-13303-2016": ("2016-07-01", f"Lei 13.303/2016 art. 97: {_PUB} (DOU 1.7.2016)"),
    "lei-9096-1995": ("1995-09-20", f"Lei 9.096/1995 art. 62: {_PUB} (DOU 20.9.1995)"),
    "lei-13445-2017": ("2017-11-21", "Lei 13.445/2017 art. 125: 'Esta Lei entra em vigor após decorridos 180 (cento e oitenta) "
                                     "dias de sua publicação oficial' (DOU 25.5.2017): in force on the day after the 180th "
                                     "day counted from publication (LC 95/1998 art. 8 § 1)"),
    "lei-9474-1997": ("1997-07-23", f"Lei 9.474/1997 art. 49: {_PUB} (DOU 23.7.1997)"),
    "lei-13260-2016": ("2016-03-17", f"Lei 13.260/2016 art. 20: {_PUB} (DOU 17.3.2016, edição extra; rectified 18.3.2016)"),
    "lei-7960-1989": ("1989-12-22", f"Lei 7.960/1989 art. 6: {_PUB} (DOU 22.12.1989); the conversion of Medida Provisória nº "
                                    "111, de 1989, whose own text Planalto's page does not give"),
    "lei-8036-1990": ("1990-05-14", f"Lei 8.036/1990 art. 32: 'Esta lei entra em vigor na data de sua publicação' (DOU 14.5.1990, "
                                    "rectified 15.5.1990); the conversion of Medida Provisória nº 177/1990"),
    "lei-4595-1964": ("1965-03-31", "Lei 4.595/1964 art. 65: 'Esta lei entrará em vigor 90 (noventa) dias após data de sua "
                                    "publicação' (DOU 31.12.1964, supplement): 31.12.1964 + 90 days"),
    "lei-7357-1985": ("1985-09-03", "Lei 7.357/1985 art. 70: 'Esta Lei entra em vigor na data de sua publicação' (DOU 3.9.1985; "
                                    "the footer of Planalto's page misprints '3.9.1986')"),
    "lei-5474-1968": ("1968-08-18", "Lei 5.474/1968 art. 28: 'Esta Lei entrará em vigor 30 (trinta) dias após a data de sua "
                                    "publicação' (DOU 19.7.1968, rectified 25.7.1968): 19.7.1968 + 30 days"),
    "lei-8935-1994": ("1994-11-21", "Lei 8.935/1994 art. 54: 'Esta Lei entra em vigor na data da sua publicação' (DOU "
                                    "21.11.1994)"),
    "lei-8443-1992": ("1992-07-17", f"Lei 8.443/1992 art. 112: {_PUB} (DOU 17.7.1992, rectified 22.4.1993)"),
    "lei-10259-2001": ("2002-01-14", "Lei 10.259/2001 art. 27: 'Esta Lei entra em vigor seis meses após a data de sua "
                                     "publicação' (DOU 13.7.2001): the period ends on 13.1.2002 and the law is in force the day "
                                     "after (LC 95/1998 art. 8 § 1, as amended by LC 107/2001)"),
    "lei-12153-2009": ("2010-06-24", "Lei 12.153/2009 art. 28: 'Esta Lei entra em vigor após decorridos 6 (seis) meses de sua "
                                     "publicação oficial' (DOU 23.12.2009): the period ends on 23.6.2010 and the law is in "
                                     "force the day after (LC 95/1998 art. 8 § 1)"),
    "lei-8038-1990": ("1990-05-29", f"Lei 8.038/1990 art. 44: {_PUB} (DOU 29.5.1990)"),
    "lei-5478-1968": ("1968-08-25", "Lei 5.478/1968 art. 28: 'Esta lei entrará em vigor 30 (trinta) dias depois de sua "
                                    "publicação' (DOU 26.7.1968; rectified 14.8.1968, republished 8.4.1974): 26.7.1968 + 30 "
                                    "days"),
    "lei-12305-2010": ("2010-08-03", f"Lei 12.305/2010 art. 57: {_PUB} (DOU 3.8.2010)"),
}
_L = B._act_law
ACT_LAWS_ALL: dict[str, dict] = {
    "dl-3688-1941": _L("Decreto-Lei nº 3.688, de 1941", "Lei das Contravenções Penais.", "1941-10-03", "1941-10-13",
                       PAGES["lcp"]),
    "lei-1079-1950": _L("Lei nº 1.079, de 1950", "Define os crimes de responsabilidade e regula o respectivo processo de "
                        "julgamento.", "1950-04-10", "1950-04-12", PAGES["lcr"]),
    "lei-7716-1989": _L("Lei nº 7.716, de 1989", "Define os crimes resultantes de preconceito de raça ou de cor.",
                        "1989-01-05", "1989-01-06", PAGES["lrac"]),
    "lei-7783-1989": _L("Lei nº 7.783, de 1989", "Dispõe sobre o exercício do direito de greve, define as atividades "
                        "essenciais, regula o atendimento das necessidades inadiáveis da comunidade, e dá outras providências.",
                        "1989-06-28", "1989-06-29", PAGES["lgreve"]),
    "lc-150-2015": _L("Lei Complementar nº 150, de 2015", "Dispõe sobre o contrato de trabalho doméstico; altera as Leis nº "
                      "8.212, de 24 de julho de 1991, nº 8.213, de 24 de julho de 1991, e nº 11.196, de 21 de novembro de 2005; "
                      "revoga o inciso I do art. 3º da Lei nº 8.009, de 29 de março de 1990, o art. 36 da Lei nº 8.213, de 24 de "
                      "julho de 1991, a Lei nº 5.859, de 11 de dezembro de 1972, e o inciso VII do art. 12 da Lei nº 9.250, de 26 "
                      "de dezembro 1995; e dá outras providências.", "2015-06-01", "2015-06-02", PAGES["lcp150"]),
    "lei-6019-1974": _L("Lei nº 6.019, de 1974", "Dispõe sobre o Trabalho Temporário nas Empresas Urbanas, e dá outras "
                        "Providências.", "1974-01-03", "1974-01-04", PAGES["ltemp"]),
    "lei-4591-1964": _L("Lei nº 4.591, de 1964", "Dispõe sôbre o condomínio em edificações e as incorporações imobiliárias.",
                        "1964-12-16", "1964-12-21", PAGES["lcondo"]),
    "lei-9514-1997": _L("Lei nº 9.514, de 1997", "Dispõe sobre o Sistema de Financiamento Imobiliário, institui a alienação "
                        "fiduciária de coisa imóvel e dá outras providências.", "1997-11-20", "1997-11-21", PAGES["lsfi"]),
    "dl-911-1969": _L("Decreto-Lei nº 911, de 1969", "Altera a redação do art. 66, da Lei nº 4.728, de 14 de julho de 1965, "
                      "estabelece normas de processo sôbre alienação fiduciária e dá outras providências.", "1969-10-01",
                      "1969-10-03", PAGES["dl911"]),
    "lei-4320-1964": _L("Lei nº 4.320, de 1964", "Estatui Normas Gerais de Direito Financeiro para elaboração e contrôle dos "
                        "orçamentos e balanços da União, dos Estados, dos Municípios e do Distrito Federal.", "1964-03-17",
                        "1964-03-23", PAGES["l4320"]),
    "lei-13303-2016": _L("Lei nº 13.303, de 2016", "Dispõe sobre o estatuto jurídico da empresa pública, da sociedade de "
                         "economia mista e de suas subsidiárias, no âmbito da União, dos Estados, do Distrito Federal e dos "
                         "Municípios.", "2016-06-30", "2016-07-01", PAGES["lestatais"]),
    "lei-9096-1995": _L("Lei nº 9.096, de 1995", "Dispõe sobre partidos políticos, regulamenta os arts. 17 e 14, § 3º, inciso "
                        "V, da Constituição Federal.", "1995-09-19", "1995-09-20", PAGES["lpp"]),
    "lei-13445-2017": _L("Lei nº 13.445, de 2017", "Institui a Lei de Migração.", "2017-05-24", "2017-05-25", PAGES["lmig"]),
    "lei-9474-1997": _L("Lei nº 9.474, de 1997", "Define mecanismos para a implementação do Estatuto dos Refugiados de 1951, e "
                        "determina outras providências.", "1997-07-22", "1997-07-23", PAGES["lref"]),
    "lei-13260-2016": _L("Lei nº 13.260, de 2016", "Regulamenta o disposto no inciso XLIII do art. 5º da Constituição Federal, "
                         "disciplinando o terrorismo, tratando de disposições investigatórias e processuais e reformulando o "
                         "conceito de organização terrorista; e altera as Leis nºs 7.960, de 21 de dezembro de 1989, e 12.850, de "
                         "2 de agosto de 2013.", "2016-03-16", "2016-03-17", PAGES["lterr"]),
    "lei-7960-1989": _L("Lei nº 7.960, de 1989", "Dispõe sobre prisão temporária.", "1989-12-21", "1989-12-22", PAGES["lpt"]),
    "lei-8036-1990": _L("Lei nº 8.036, de 1990", "Dispõe sobre o Fundo de Garantia do Tempo de Serviço, e dá outras "
                        "providências.", "1990-05-11", "1990-05-14", PAGES["lfgts"]),
    "lei-4595-1964": _L("Lei nº 4.595, de 1964", "Dispõe sobre a Política e as Instituições Monetárias, Bancárias e "
                        "Creditícias, Cria o Conselho Monetário Nacional e dá outras providências.", "1964-12-31", "1964-12-31",
                        PAGES["lsfn"]),
    "lei-7357-1985": _L("Lei nº 7.357, de 1985", "Dispõe sobre o cheque e dá outras providências.", "1985-09-02", "1985-09-03",
                        PAGES["lcheque"]),
    "lei-5474-1968": _L("Lei nº 5.474, de 1968", "Dispõe sôbre as Duplicatas, e dá outras providências.", "1968-07-18",
                        "1968-07-19", PAGES["ldup"]),
    "lei-8935-1994": _L("Lei nº 8.935, de 1994", "Regulamenta o art. 236 da Constituição Federal, dispondo sobre serviços "
                        "notariais e de registro. (Lei dos cartórios)", "1994-11-18", "1994-11-21", PAGES["lcart"]),
    "lei-8443-1992": _L("Lei nº 8.443, de 1992", "Dispõe sobre a Lei Orgânica do Tribunal de Contas da União e dá outras "
                        "providências.", "1992-07-16", "1992-07-17", PAGES["ltcu"]),
    "lei-10259-2001": _L("Lei nº 10.259, de 2001", "Dispõe sobre a instituição dos Juizados Especiais Cíveis e Criminais no "
                         "âmbito da Justiça Federal.", "2001-07-12", "2001-07-13", PAGES["ljef"]),
    "lei-12153-2009": _L("Lei nº 12.153, de 2009", "Dispõe sobre os Juizados Especiais da Fazenda Pública no âmbito dos "
                         "Estados, do Distrito Federal, dos Territórios e dos Municípios.", "2009-12-22", "2009-12-23",
                         PAGES["ljefp"]),
    "lei-8038-1990": _L("Lei nº 8.038, de 1990", "Institui normas procedimentais para os processos que especifica, perante o "
                        "Superior Tribunal de Justiça e o Supremo Tribunal Federal.", "1990-05-28", "1990-05-29",
                        PAGES["l8038"]),
    "lei-5478-1968": _L("Lei nº 5.478, de 1968", "Dispõe sobre ação de alimentos e dá outras providências.", "1968-07-25",
                        "1968-07-26", PAGES["lalim"]),
    "lei-12305-2010": _L("Lei nº 12.305, de 2010", "Institui a Política Nacional de Resíduos Sólidos; altera a Lei nº 9.605, de "
                         "12 de fevereiro de 1998; e dá outras providências.", "2010-08-02", "2010-08-03", PAGES["lpnrs"]),
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

# Lei de Greve art. 10 X: Medida Provisória nº 866/2018 (NAV Brasil) gave it a new wording; MP 883/2019 revoked MP 866 and
# lapsed; MP 866 was converted into Lei 13.903/2019
P.MP_LAPSE["mp-883-2019"] = ("2019-09-19", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 58, de 2019 (DOU "
                                           "20.9.2019): MP 883 'teve seu prazo de vigência encerrado no dia 18 de setembro do "
                                           "corrente ano'")
_LG = "lei-de-greve"
_LG_WHY = ("Lei de Greve art. 10 X: the 1989 wording stands until Medida Provisória nº 866/2018 (21.12.2018) and again while "
           "MP 883/2019, which revoked MP 866, was in force (22.5.2019 to its lapse, 19.9.2019: Ato Declaratório nº 58/2019); "
           "MP 866's wording stands from 21.12.2018 to its conversion law, Lei 13.903/2019 (20.11.2019), except while MP 883 "
           "was in force. Planalto prints both wordings twice around the MP 883 note; the second copy of MP 866's is left out")
B8.SPAN_FIX += [
    ((_LG, "art-10", "X -", "X - controle de tráfego aéreo;", 0),
     {"start": "1989-06-29", "start_law": None, "end": "2018-12-21", "end_law": "mp-866-2018", "end_how": "successor"},
     _LG_WHY),
    ((_LG, "art-10", "X -", "X - controle de tráfego aéreo;", 1),
     {"start": "2019-05-22", "start_law": "mp-883-2019", "end": "2019-09-19", "end_law": "mp-883-2019-fim",
      "end_how": "lapse", "state": "struck"}, _LG_WHY),
    ((_LG, "art-10", "X -", "X - controle de tráfego aéreo e navegação aérea; e", 0),
     {"start": "2018-12-21", "start_law": "mp-866-2018", "end": "2019-11-20", "end_law": "lei-13903-2019",
      "end_how": "successor", "gaps": [("2019-05-22", "2019-09-19", "mp-883-2019", "mp-883-2019-fim")]}, _LG_WHY),
    ((_LG, "art-10", "X -", "X - controle de tráfego aéreo e navegação aérea; e", 1), {"skip": True, "end_how": "twin"},
     _LG_WHY),
]
P.MP_PENDING["mp-2221-2001"] = ("Medida Provisória nº 2.221, de 4.9.2001 (DOU 5.9.2001), in force on 11.9.2001, stayed in force "
                                "(Emenda Constitucional 32/2001, art. 2) until Lei 10.931/2004 revoked it (its page: 'Revogada "
                                "pela Lei nº 10.931, de 2004'); its wordings in the Lei de Condomínios e Incorporações end with "
                                "Lei 10.931's notes")
B.EXPLAINED["lei-de-condominios-e-incorporacoes"] = {
    "art-33": "the consolidated page keeps Medida Provisória nº 1.085/2021's parágrafo único ('... a cada cento e oitenta "
              "dias') above Lei 14.382/2022's ('... a cada 180 (cento e oitenta) dias'), which replaced it on the "
              "conversion; the annotated page strikes the MP's wording",
}
B.EXPLAINED["lei-da-alienacao-fiduciaria"] = {
    "preambulo": "layout: the consolidated page sets the ementa ('Altera a redação do art. 66 ...') as a centred heading, "
                 "the annotated page as the preamble's first line",
    "titulos": "layout: the ementa, see preambulo",
}
P.VIGENCIA_FIXED["mp-656-2014"] = (
    "2014-10-08", "art. 55: in force 'I - a partir de 1º de janeiro de 2015, em relação ao art. 3º; II - trinta dias após a "
                  "sua publicação em relação aos arts. 9º a 17; e III - a partir da data de sua publicação, em relação aos "
                  "demais artigos' (DOU 8.10.2014); its change to Lei 9.514/1997 (art. 53) falls under III")
B8.SPAN_FIX += [
    (("lei-da-alienacao-fiduciaria", "art-05", "Parágrafo único", "Parágrafo único. Não se aplica à alienação fiduciária o "
                                                                  "disposto nos incisos IX", 0),
     {"end": "1974-07-04", "end_law": "lei-6071-1974", "end_how": "successor"},
     "Decreto-Lei 911/1969 art. 5 parágrafo único: the 1969 wording ends when Lei 6.071/1974 gave the paragraph its new "
     "wording (4.7.1974); Planalto strikes it with the 1969 caput, which stood until Lei 13.043/2014"),
]
B.EXPLAINED["lei-dos-partidos-politicos"] = {
    "art-44": "Planalto's annotated page strikes §§ 5º-A and 7º (Lei 13.165/2015) with only '(Vide ADIN Nº 5.617)', no "
              "date; as for other struck text whose end the source does not date, they are left out of every version (see "
              "the ADI 5.617 decision); the consolidated page still prints them",
}
B.EXPLAINED["lei-antiterrorismo"] = {
    "art-19": "check artefact: art. 19 quotes Lei 12.850/2013 art. 1 with the dotted line '§ 2º .....', which the history "
              "keeps as '§ 2º.' and the check, reading label-only lines as revoked dispositivos, drops",
}
# Lei do Sistema Financeiro Nacional: Planalto abbreviates Decreto-Lei as 'Del' in some notes
_DEL_NOTES = [("Incluído", "2.321", "25/02/87", "1987"), ("Redação dada", "1.959", "14/09/82", "1982"),
              ("Redação dada", "2.376", "25/11/87", "1987"), ("Redação dada", "278", "28/02/67", "1967"),
              ("Redação dada", "581", "14/05/69", "1969"), ("Renumerado", "2.321", "25/02/87", "1987"),
              ("Revogado", "48", "18/11/66", "1966")]
for _how, _n, _d, _y in _DEL_NOTES:
    P.NOTE_FIX[f"({_how} pelo Del nº {_n}, de {_d})"] = (
        f"({_how} pelo Decreto-Lei nº {_n}, de {_y})",
        f"Lei do Sistema Financeiro Nacional: the note reads 'Del nº {_n}, de {_d}', Planalto's abbreviation of Decreto-Lei")
P.VIGENCIA_FIXED["dl-581-1969"] = (
    "1969-05-21", "art. 6: 'Êste Decreto-lei entrará em vigor na data de sua publicação' (DOU 21.5.1969; Planalto's footer "
                  "misprints '21.5.196e'). Its art. 4 parágrafo único leaves the date on which its new wording of Lei 4.595 "
                  "arts. 4 V, 10 VII and 11 III becomes effective to a decree, after the IMF amendment it approves; as for "
                  "other deferred effects, the wording is dated by the in-force day")
B9.WORD_FIX[:] = B9.WORD_FIX + [
    ("lsfn", "Banco Central da República do Brasil. Vide Lei nº 6.419, de 1944", "Banco Central da República do Brasil.",
     "Lei do Sistema Financeiro Nacional art. 56: Planalto's editorial pointer 'Vide Lei nº 6.419, de 1944', printed without "
     "parentheses below the caput, is read into the caput; it is dropped like the page's other 'Vide' notes"),
]
_LSFN = "lei-do-sistema-financeiro-nacional"
_LSFN42 = ("Lei do Sistema Financeiro Nacional art. 42: Medida Provisória nº 784/2017 revoked the whole article (8.6.2017 to "
           "its lapse, 20.10.2017) before Lei 13.506/2017 did (14.11.2017); Planalto notes the MP only on the caput, so the "
           "quoted wording of Lei 1.808/1953 art. 2 the article carries is absent with it while the MP stood")
B8.SPAN_FIX += [
    ((_LSFN, "art-10", "IV -", "IV - receber os recolhimentos compulsórios de que trata o inciso XIV", 0),
     {"skip": True, "end_how": "twin"},
     "Lei do Sistema Financeiro Nacional art. 10 IV: Planalto prints the former inciso III struck as inciso IV, noted "
     "'Renumerado pela Lei nº 7.730'; Medida Provisória nº 32/1989 (16.1.1989) and Lei 7.730/1989, its conversion, gave "
     "inciso IV a new wording in the same act, so the renumbered words never stood as inciso IV and are left out"),
    ((_LSFN, "art-42", "", '"Art. 2º Os diretores e gerentes', 0),
     {"gaps": [("2017-06-08", "2017-10-20", "mp-784-2017", "mp-784-2017-fim")]}, _LSFN42),
    ((_LSFN, "art-42", "Parágrafo único", "Parágrafo único. Havendo prejuízos", 0),
     {"gaps": [("2017-06-08", "2017-10-20", "mp-784-2017", "mp-784-2017-fim")]}, _LSFN42),
]
B.EXPLAINED["lei-do-sistema-financeiro-nacional"] = {
    "art-04": "the annotated page prints '( Vetado )' after Lei 6.045/1974's note on the caput, which the history keeps at "
              "the end of the caput and the consolidated page leaves out; it prints 'Lei nº 1.059, de 10.4.1950' where the "
              "consolidated page has 'Lei nº 1059, de 10/04/1950'",
    "art-05": "the consolidated page misprints 'Constituição Federa'",
    "art-10": "the annotated page prints inciso I as '... Conselho Monetário Nacional ( Vetado )).'; the consolidated page "
              "keeps the note '(Renumerado pela Lei nº 7.730, de 31/01/89)' in inciso V's text",
    "art-19": "typesetting: the annotated page ends inciso II with '(Vetado).', the consolidated page without the full stop",
}
P.VIGENCIA_FIXED["lei-14206-2021"] = (
    "2021-09-28", "art. 22: 'Esta Lei entra em vigor: I - (VETADO); e II - na data de sua publicação, para os demais "
                  "dispositivos' (DOU 28.9.2021)")
# Lei das Duplicatas, Capítulo V (arts. 15-18): Decreto-Lei 436/1969 (27.1.1969) gave arts. 15 (caput), 16 and 17 new
# wordings and added art. 15 §§ 12-13, keeping art. 15 §§ 1-11 ('.....' in its text); Lei 6.458/1977 rewrote the whole
# chapter. Planalto strikes the earlier lines without notes: each ends on Lei 6.458's day.
_LDUP = "lei-das-duplicatas"
_LDUP_WHY = ("Lei das Duplicatas arts. 15 to 18: Lei 6.458/1977 rewrote Capítulo V ('Redação dada pela Lei nº 6.458'); the "
             "earlier lines Planalto strikes without a note (the 1968 text and Decreto-Lei 436/1969's wordings of arts. 15 to "
             "17 and §§ 12-13; Decreto-Lei 436 kept art. 15 §§ 1 to 11, which its text gives as '.....') end on Lei 6.458's "
             "in-force day")
_L6458 = {"end": "1977-11-03", "end_law": "lei-6458-1977", "end_how": "successor", "skip": False}
B8.SPAN_FIX += [((_LDUP, u, lab, pre, n), _L6458, _LDUP_WHY) for u, lab, pre, n in [
    *[("art-15", f"§ {k}" + ("º" if k < 10 else ""), f"§ {k}" + ("º" if k < 10 else "."), 0) for k in range(1, 14)],
    ("art-15", "Art. 15", "Art. 15. Será processada pela forma executiva a ação do credor por duplicata ou triplicata", 0),
    ("art-16", "Art. 16", "Art. 16. Será processada pela forma ordinária a ação do credor contra", 0),
    ("art-16", "§ 1º", "§ 1º A apresentação e a distribuição", 0),
    ("art-16", "§ 2º", "§ 2º Não contestada, será a ação", 0),
    ("art-17", "Art. 17", "Art. 17. O fôro competente para a ação de cobrança da duplicata ou da", 0),
    ("art-18", "Art. 18", "Art. 18. A ação de cobrança da duplicata prescreve", 0),
    ("art-18", "I -", "I - contra o sacado e respectivos avalistas, em 3 (três) anos, contados da data do vencimento", 0),
    ("art-18", "II -", "Il - contra endossante", 0),
    ("art-18", "III -", "III - de qualquer dos coobrigados contra os demais, em um (1) ano", 0),
    ("art-18", "§ 1º", "§ 1º A ação de cobrança poderá ser", 0),
    ("art-18", "§ 2º", "§ 2º Os coobrigados da duplicata respondem solidàriamente", 0),
]]
# Lei Orgânica do TCU: Planalto's page heads the act 'Lei Nº 8.443, DE 16 DE JULHO DE 1992.' in mixed case, which the
# shared parser's start-of-act test (an upper-case 'LEI N') misses; the heading is read in upper case for that test only
_paragraphs13 = P.paragraphs


LALIM_QUOTED: list[str] = []


def paragraphs(html, digits):
    if B8.CURRENT_PAGE[0] == "ltcu":
        html = html.replace("Lei Nº 8.443, DE 16 DE JULHO DE 1992.", "LEI Nº 8.443, DE 16 DE JULHO DE 1992.", 1)
    out, rest = _paragraphs13(html, digits)
    if B8.CURRENT_PAGE[0] == "lalim":
        # Lei de Alimentos art. 19 § 1º as enacted quotes Código de Processo Civil (1939) art. 921 without quotation
        # marks; its 'Art. 921.' line and the lines after it, up to art. 20, are art. 19's own text
        for p in out:
            if p["unit"] == "art-921":
                p["unit"] = "art-19"
                LALIM_QUOTED.append(p["label"])
    return out, rest


P.paragraphs = B.paragraphs = paragraphs
# Lei Orgânica do TCU art. 55 § 1º: an expression suspended by a Senate resolution (CF art. 52 X), batch 5b's split rule
import re as _re  # noqa: E402
P.COURTS["rsf-16-2006"] = {
    "label": "Resolução do Senado Federal nº 16, de 2006", "kind": "law", "enacted": "2006-03-14", "published": "2006-03-15",
    "title": "Suspende a execução da expressão \"manter ou não o sigilo quanto ao objeto e à autoria da denúncia\", constante "
             "do § 1º do art. 55 da Lei Federal nº 8.443, de 16 de julho de 1992, e do contido no disposto no Regimento "
             "Interno do Tribunal de Contas da União, que, quanto à autoria da denúncia, estabelece a manutenção do sigilo.",
    "url": PL + "_Ato2004-2006/2006/Congresso/ResSF16-06.htm",
    "from": "2006-03-15", "case": r"Resolu[çc][ãa]o\s+SF\s+n[º°]?\s*16\s*,\s*de\s*2006", "where": [],
    "why": "Resolução do Senado Federal nº 16, de 14.3.2006 (DOU 15.3.2006; Planalto page ResSF16-06.htm), art. 1: 'É "
           "suspensa a execução da expressão \"manter ou não o sigilo quanto ao objeto e à autoria da denúncia\" constante "
           "do § 1º do art. 55 da Lei Federal nº 8.443 [...] em virtude de declaração de inconstitucionalidade em decisão "
           "definitiva do Supremo Tribunal Federal, nos autos do Mandado de Segurança nº 24.405-4'; art. 2: in force on "
           "publication. Planalto strikes the expression inside the paragraph; the history drops it on 15.3.2006, credited "
           "to the resolution (kind law: a Senate act)"}
B6.PB5B.SPLIT_NOTES["rsf-16-2006"] = _re.compile(r"\(\s*Express[ãa]o\s+suspensa\s+pela\s+Resolu[çc][ãa]o\s+SF\s+n[º°]?\s*16\s*,"
                                               r"\s*de\s*2006\s*\)", _re.I)
B.EXPLAINED["lei-das-duplicatas"] = {
    "preambulo": "layout: the consolidated page sets the ementa ('Dispõe sôbre as Duplicatas ...') as a centred heading, the "
                 "annotated page as the preamble's first line",
    "titulos": "layout: the ementa, see preambulo",
}
_LALIM_WHY = ("Lei de Alimentos art. 19 §§ 1º to 3º as enacted (§ 1º and § 3º amending the 1939 Código de Processo Civil arts. "
              "921 and 843, with the quoted text) end when Lei 6.014/1973 gave art. 19 its §§ 1º to 3º; Planalto strikes "
              "§ 1º's opening words without a note")
B8.SPAN_FIX += [
    (("lei-de-alimentos", "art-19", "§ 1º", "§ 1º O artigo 921 do Código de Processo Civil", 0),
     {"end": "1973-12-31", "end_law": "lei-6014-1973", "end_how": "successor", "skip": False}, _LALIM_WHY),
    (("lei-de-alimentos", "art-19", "§ 2º", "§ 2º Nos casos previstos nos nº VI", 0),
     {"end": "1973-12-31", "end_law": "lei-6014-1973", "end_how": "successor"}, _LALIM_WHY),
]
_PNRS19 = ("Política Nacional de Resíduos Sólidos art. 19 XIX: Planalto leaves the 2010 wording ('... observado "
           "prioritariamente o período de vigência do plano plurianual municipal') unstruck above Lei 14.026/2020's "
           "('... observado o período máximo de 10 (dez) anos'), which it notes 'Incluído'; Lei 14.026 gave inciso XIX that "
           "new wording, so the 2010 wording ends on 16.7.2020")
B8.SPAN_FIX += [
    (("politica-nacional-de-residuos-solidos", "art-19", "XIX -", "XIX - periodicidade de sua revisão, observado "
                                                                   "prioritariamente", 0),
     {"end": "2020-07-16", "end_law": "lei-14026-2020", "end_how": "successor"}, _PNRS19),
]
B.EXPLAINED["politica-nacional-de-residuos-solidos"] = {
    "art-19": "the annotated page (the act's only page) leaves inciso XIX's 2010 wording unstruck above Lei 14.026/2020's; "
              "the history ends it on 16.7.2020 (see the life-span decisions), so today's text has one inciso XIX",
}

# court and other open items named in decisions (Planalto's 'Vide' notes are dropped from the text, so nothing is modelled)
OPEN_ITEMS = {
    "lei-dos-crimes-de-responsabilidade": (
        "Lei dos Crimes de Responsabilidade (open item): Planalto's page marks arts. 39, 41, 47, 54, 57 and 70 (crimes and "
        "procedure for Ministers of the Supremo Tribunal Federal and the Procurador-Geral da República) with '(Vide ADPF 1259)' and "
        "'(Vide ADPF 1260)', with no date and no struck text; the STF decisions in those cases are not modelled, and the "
        "text is the law's own wording"),
    "lei-do-crime-racial": (
        "Crimes resultantes de preconceito de raça ou de cor (open item): Planalto's page heads the act with '(Vide ADO Nº 26)', a Supremo Tribunal Federal "
        "ruling that changes no words of the act; it is not modelled"),
    "lei-dos-partidos-politicos": (
        "Lei dos Partidos Políticos, STF ADI 5.617 (open item): Planalto strikes art. 44 §§ 5º-A and 7º (both added by Lei "
        "13.165/2015) noting only '(Vide ADIN Nº 5.617)', with no date; as for other struck text the source does not date, "
        "both are left out of every version, and the ruling is not modelled. The other 'Vide ADI' notes (5.105, 5.398, "
        "6.230, 7.021) strike no text"),
    "lei-das-estatais": (
        "Lei das Estatais: the 'Vide ADIN' notes (5.624, 5.846, 5.924, 6.029; ADI 7.331 at art. 17 § 2º) strike no text; "
        "the rulings are not modelled"),
    "lei-de-migracao": (
        "Lei de Migração: the act's annex (Tabela de Taxas e Emolumentos Consulares, art. 113), a table printed after the "
        "signature, is not included; the history holds the articles only"),
    "lei-da-prisao-temporaria": (
        "Lei da Prisão Temporária: Planalto heads the act with '(Vide ADI 3360)' and '(Vide ADI 4109)', Supremo Tribunal "
        "Federal rulings that strike no words of it; they are not modelled"),
    "lei-das-contravencoes-penais": (
        "Lei das Contravenções Penais: Planalto's 'Vide' pointers at the head of the act (Lei 1.390/1951, Lei 7.437/1985) and "
        "at art. 50 (Decretos-Leis 4.866/1942 and 9.215/1946) name acts that changed no words of it; they are not "
        "modelled"),
}
_inner13 = B6.PB5B._write_part5


def _inner(*a):
    B5.EXTRA_DECISIONS.extend(OPEN_ITEMS[act["slug"]] + "." for act in a[0] if act["slug"] in OPEN_ITEMS)
    if LALIM_QUOTED:
        B5.EXTRA_DECISIONS.append(
            "Lei de Alimentos art. 19: the 1968 text of § 1º quotes the 1939 Código de Processo Civil art. 921 (and § 3º its "
            "art. 843 § 2º) without quotation marks; the quoted 'Art. 921.' line and the lines after it, up to art. 20, are "
            f"kept in art. 19 ({len(LALIM_QUOTED)} lines), not read as an article of the act.")
    return _inner13(*a)


B6.PB5B._write_part5 = _inner

SRC = HERE / "sources_batch13.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
