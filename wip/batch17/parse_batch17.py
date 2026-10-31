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
import re
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
    # part b
    "l9029": "leis/l9029.htm",
    "l9609": "leis/l9609.htm",
    "l9637": "leis/l9637.htm",
    "l9790": "leis/l9790.htm",
    # part c
    "l1060": "leis/l1060.htm",
    "l1060-compilada": "leis/l1060compilada.htm",
    "l9492": "leis/l9492.htm",
    "l6024": "leis/l6024.htm",
    "l12037": "_ato2007-2010/2009/lei/l12037.htm",
    # part d
    "l11105": "_ato2004-2006/2005/lei/l11105.htm",
    "l9263": "leis/l9263.htm",
    "l11419": "_ato2004-2006/2006/lei/l11419.htm",
    "l12587": "_ato2011-2014/2012/lei/l12587.htm",
    # part f
    "l6634": "leis/l6634.htm",
    "l9469": "leis/l9469.htm",
    "l9469-compilado": "leis/l9469compilado.htm",
    "l9537": "leis/l9537.htm",
    # part g
    "l13675": "_ato2015-2018/2018/lei/l13675.htm",
    "l4728": "leis/l4728.htm",
    "l4728-compilado": "leis/l4728compilado.htm",
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
    _act("lei-9029-de-1995", "LDisc", "l9029", "l9029", "lei-9029-1995",
         "Práticas discriminatórias na relação de trabalho (Lei nº 9.029, de 13 de abril de 1995)", 2),
    _act("lei-do-software", "LSoft", "l9609", "l9609", "lei-9609-1998",
         "Lei do Software (Lei nº 9.609, de 19 de fevereiro de 1998)", 2),
    _act("lei-das-organizacoes-sociais", "LOS", "l9637", "l9637", "lei-9637-1998",
         "Lei das Organizações Sociais (Lei nº 9.637, de 15 de maio de 1998)", 2),
    _act("lei-das-oscips", "LOSCIP", "l9790", "l9790", "lei-9790-1999",
         "Lei das OSCIPs (Lei nº 9.790, de 23 de março de 1999)", 2),
    _act("lei-da-assistencia-judiciaria", "LAJ", "l1060", "l1060-compilada", "lei-1060-1950",
         "Lei da Assistência Judiciária (Lei nº 1.060, de 5 de fevereiro de 1950)", 2),
    _act("lei-do-protesto-de-titulos", "LProt", "l9492", "l9492", "lei-9492-1997",
         "Lei do Protesto de Títulos (Lei nº 9.492, de 10 de setembro de 1997)", 2),
    _act("lei-da-intervencao-e-liquidacao-extrajudicial", "LILE", "l6024", "l6024", "lei-6024-1974",
         "Intervenção e liquidação extrajudicial de instituições financeiras (Lei nº 6.024, de 13 de março de 1974)", 2),
    _act("lei-da-identificacao-criminal", "LIdC", "l12037", "l12037", "lei-12037-2009",
         "Lei da Identificação Criminal (Lei nº 12.037, de 1º de outubro de 2009)", 2),
    _act("lei-de-biosseguranca", "LBio", "l11105", "l11105", "lei-11105-2005",
         "Lei de Biossegurança (Lei nº 11.105, de 24 de março de 2005)", 2),
    _act("lei-do-planejamento-familiar", "LPF", "l9263", "l9263", "lei-9263-1996",
         "Lei do Planejamento Familiar (Lei nº 9.263, de 12 de janeiro de 1996)", 2),
    _act("lei-do-processo-eletronico", "LPE", "l11419", "l11419", "lei-11419-2006",
         "Lei do Processo Judicial Eletrônico (Lei nº 11.419, de 19 de dezembro de 2006)", 2),
    _act("lei-da-mobilidade-urbana", "LMU", "l12587", "l12587", "lei-12587-2012",
         "Política Nacional de Mobilidade Urbana (Lei nº 12.587, de 3 de janeiro de 2012)", 2),
    _act("lei-da-faixa-de-fronteira", "LFF", "l6634", "l6634", "lei-6634-1979",
         "Lei da Faixa de Fronteira (Lei nº 6.634, de 2 de maio de 1979)", 2),
    _act("lei-9469-de-1997", "L9469", "l9469", "l9469-compilado", "lei-9469-1997",
         "Acordos e intervenção da União em causas judiciais (Lei nº 9.469, de 10 de julho de 1997)", 2),
    _act("lei-da-seguranca-do-trafego-aquaviario", "LESTA", "l9537", "l9537", "lei-9537-1997",
         "Lei de Segurança do Tráfego Aquaviário (Lei nº 9.537, de 11 de dezembro de 1997)", 2),
    _act("lei-do-susp", "LSUSP", "l13675", "l13675", "lei-13675-2018",
         "Lei do Sistema Único de Segurança Pública (Lei nº 13.675, de 11 de junho de 2018)", 2),
    _act("lei-do-mercado-de-capitais", "LMC", "l4728", "l4728-compilado", "lei-4728-1965",
         "Lei do Mercado de Capitais (Lei nº 4.728, de 14 de julho de 1965)", 2),
]
PARTS: dict[str, list[str]] = {
    "a": ["lei-do-trabalho-rural", "lei-do-decimo-terceiro-salario", "lei-do-repouso-semanal-remunerado",
          "lei-do-vale-transporte"],
    "b": ["lei-9029-de-1995", "lei-do-software", "lei-das-organizacoes-sociais", "lei-das-oscips"],
    "c": ["lei-da-assistencia-judiciaria", "lei-do-protesto-de-titulos", "lei-da-intervencao-e-liquidacao-extrajudicial",
          "lei-da-identificacao-criminal"],
    "d": ["lei-de-biosseguranca", "lei-do-planejamento-familiar", "lei-do-processo-eletronico"],
    "e": ["lei-da-mobilidade-urbana"],
    "f": ["lei-da-faixa-de-fronteira", "lei-9469-de-1997", "lei-da-seguranca-do-trafego-aquaviario"],
    "g": ["lei-do-susp", "lei-do-mercado-de-capitais"],
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
_PUB2 = "'Esta Lei entrará em vigor na data de sua publicação'"
ACT_DAY_ALL = {**B16.ACT_DAY_ALL,
    "lei-5889-1973": ("1973-06-11", f"Lei 5.889/1973 art. 21: {_PUB} (DOU 11.6.1973, rectified 30.10.1973)"),
    "lei-4090-1962": ("1962-07-26", f"Lei 4.090/1962 art. 4: {_PUB2} (DOU 26.7.1962)"),
    "lei-605-1949": ("1949-01-14", "Lei 605/1949 art. 15: 'A presente lei entrará em vigor na data de sua publicação' (DOU "
                                   "14.1.1949)"),
    "lei-7418-1985": ("1985-12-17", f"Lei 7.418/1985 art. 12 (art. 11 since Lei 7.619/1987): {_PUB} (DOU 17.12.1985)"),
    "lei-9029-1995": ("1995-04-17", "Lei 9.029/1995 art. 5: 'Esta lei entra em vigor na data de sua publicação' (DOU "
                                    "17.4.1995)"),
    "lei-9609-1998": ("1998-02-20", f"Lei 9.609/1998 art. 15: {_PUB} (DOU 20.2.1998, rectified 25.2.1998)"),
    "lei-9637-1998": ("1998-05-18", f"Lei 9.637/1998 art. 25: {_PUB} (DOU 18.5.1998, rectified 25.5.1998)"),
    "lei-9790-1999": ("1999-03-24", f"Lei 9.790/1999 art. 20: {_PUB} (DOU 24.3.1999)"),
    "lei-1060-1950": ("1950-03-15", "Lei 1.060/1950 art. 19: 'Esta Lei entrará em vigor trinta dias depois da sua publicação "
                                    "no Diário oficial da União' (DOU 13.2.1950)"),
    "lei-9492-1997": ("1997-09-11", f"Lei 9.492/1997 art. 42: {_PUB} (DOU 11.9.1997)"),
    "lei-6024-1974": ("1974-03-13", "Lei 6.024/1974 art. 57: 'Esta Lei entrará em vigor na data de sua publicação' (DOU "
                                    "13.3.1974, rectified 8.4.1974)"),
    "lei-12037-2009": ("2009-10-02", f"Lei 12.037/2009 art. 8: {_PUB} (DOU 2.10.2009)"),
    "lei-11105-2005": ("2005-03-28", f"Lei 11.105/2005 art. 41: {_PUB} (DOU 28.3.2005)"),
    "lei-9263-1996": ("1996-01-15", f"Lei 9.263/1996 art. 24: {_PUB} (DOU 15.1.1996)"),
    "lei-11419-2006": ("2007-03-20", "Lei 11.419/2006 art. 22: 'Esta Lei entra em vigor 90 (noventa) dias depois de sua "
                                     "publicação' (DOU 20.12.2006; the 90th day counted from publication is 19.3.2007, LC "
                                     "95/1998 art. 8 § 1)"),
    "lei-12587-2012": ("2012-04-13", "Lei 12.587/2012 art. 28: 'Esta Lei entra em vigor 100 (cem) dias após a data de sua "
                                     "publicação' (DOU 4.1.2012; the 100th day counted from publication is 12.4.2012, LC "
                                     "95/1998 art. 8 § 1)"),
    "lei-6634-1979": ("1979-05-03", "Lei 6.634/1979 art. 12: 'Esta Lei entrará em vigor na data de sua publicação' (DOU "
                                    "3.5.1979, rectified 11.5.1979)"),
    "lei-9469-1997": ("1997-07-11", f"Lei 9.469/1997 art. 13: {_PUB} (DOU 11.7.1997)"),
    "lei-9537-1997": ("1998-06-10", "Lei 9.537/1997 art. 41: 'Esta Lei entra em vigor cento e oitenta dias após a data de "
                                    "sua publicação' (DOU 12.12.1997; 180 days after 12.12.1997 is 10.6.1998)"),
    "lei-13675-2018": ("2018-07-12", "Lei 13.675/2018 art. 50: 'Esta Lei entra em vigor após decorridos 30 (trinta) dias de "
                                     "sua publicação oficial' (DOU 12.6.2018; LC 95/1998 art. 8 § 1)"),
    "lei-4728-1965": ("1965-07-16", "Lei 4.728/1965 art. 83: 'A presente Lei entra em vigor na data de sua publicação' (DOU "
                                    "16.7.1965, rectified 16.8.1965)"),
}
ACT_LAWS_ALL = {**B16.ACT_LAWS_ALL,
    "lei-5889-1973": _L("Lei nº 5.889, de 1973", "Estatui normas reguladoras do trabalho rural.", "1973-06-08", "1973-06-11",
                        PAGES["l5889"]),
    "lei-4090-1962": _L("Lei nº 4.090, de 1962", "Institui a Gratificação de Natal para os Trabalhadores.", "1962-07-13",
                        "1962-07-26", PAGES["l4090"]),
    "lei-605-1949": _L("Lei nº 605, de 1949", "Repouso semanal remunerado e o pagamento de salário nos dias feriados civis e "
                       "religiosos.", "1949-01-05", "1949-01-14", PAGES["l0605"]),
    "lei-7418-1985": _L("Lei nº 7.418, de 1985", "Institui o Vale-Transporte e dá outras providências.", "1985-12-16",
                        "1985-12-17", PAGES["l7418"]),
    "lei-9029-1995": _L("Lei nº 9.029, de 1995", "Proíbe a exigência de atestados de gravidez e esterilização, e outras "
                        "práticas discriminatórias, para efeitos admissionais ou de permanência da relação jurídica de "
                        "trabalho, e dá outras providências.", "1995-04-13", "1995-04-17", PAGES["l9029"]),
    "lei-9609-1998": _L("Lei nº 9.609, de 1998", "Dispõe sobre a proteção da propriedade intelectual de programa de "
                        "computador, sua comercialização no País, e dá outras providências.", "1998-02-19", "1998-02-20",
                        PAGES["l9609"]),
    "lei-9637-1998": _L("Lei nº 9.637, de 1998", "Dispõe sobre a qualificação de entidades como organizações sociais, a "
                        "criação do Programa Nacional de Publicização, a extinção dos órgãos e entidades que menciona e a "
                        "absorção de suas atividades por organizações sociais, e dá outras providências.", "1998-05-15",
                        "1998-05-18", PAGES["l9637"]),
    "lei-9790-1999": _L("Lei nº 9.790, de 1999", "Dispõe sobre a qualificação de pessoas jurídicas de direito privado, sem "
                        "fins lucrativos, como Organizações da Sociedade Civil de Interesse Público, institui e disciplina o "
                        "Termo de Parceria, e dá outras providências.", "1999-03-23", "1999-03-24", PAGES["l9790"]),
    "lei-1060-1950": _L("Lei nº 1.060, de 1950", "Estabelece normas para a concessão de assistência judiciária aos "
                        "necessitados.", "1950-02-05", "1950-02-13", PAGES["l1060"]),
    "lei-9492-1997": _L("Lei nº 9.492, de 1997", "Define competência, regulamenta os serviços concernentes ao protesto de "
                        "títulos e outros documentos de dívida e dá outras providências.", "1997-09-10", "1997-09-11",
                        PAGES["l9492"]),
    "lei-6024-1974": _L("Lei nº 6.024, de 1974", "Dispõe sobre a intervenção e a liquidação extrajudicial de instituições "
                        "financeiras, e dá outras providências.", "1974-03-13", "1974-03-13", PAGES["l6024"]),
    "lei-12037-2009": _L("Lei nº 12.037, de 2009", "Dispõe sobre a identificação criminal do civilmente identificado, "
                         "regulamentando o art. 5º, inciso LVIII, da Constituição Federal.", "2009-10-01", "2009-10-02",
                         PAGES["l12037"]),
    "lei-11105-2005": _L("Lei nº 11.105, de 2005", "Regulamenta os incisos II, IV e V do § 1º do art. 225 da Constituição "
                         "Federal, estabelece normas de segurança e mecanismos de fiscalização de atividades que envolvam "
                         "organismos geneticamente modificados – OGM e seus derivados, cria o Conselho Nacional de "
                         "Biossegurança – CNBS, reestrutura a Comissão Técnica Nacional de Biossegurança – CTNBio, dispõe "
                         "sobre a Política Nacional de Biossegurança – PNB, revoga a Lei nº 8.974, de 5 de janeiro de 1995, e "
                         "a Medida Provisória nº 2.191-9, de 23 de agosto de 2001, e os arts. 5º, 6º, 7º, 8º, 9º, 10 e 16 da "
                         "Lei nº 10.814, de 15 de dezembro de 2003, e dá outras providências.", "2005-03-24", "2005-03-28",
                         PAGES["l11105"]),
    "lei-9263-1996": _L("Lei nº 9.263, de 1996", "Regula o § 7º do art. 226 da Constituição Federal, que trata do "
                        "planejamento familiar, estabelece penalidades e dá outras providências.", "1996-01-12", "1996-01-15",
                        PAGES["l9263"]),
    "lei-11419-2006": _L("Lei nº 11.419, de 2006", "Dispõe sobre a informatização do processo judicial; altera a Lei nº "
                         "5.869, de 11 de janeiro de 1973 – Código de Processo Civil; e dá outras providências.", "2006-12-19",
                         "2006-12-20", PAGES["l11419"]),
    "lei-12587-2012": _L("Lei nº 12.587, de 2012", "Institui as diretrizes da Política Nacional de Mobilidade Urbana; revoga "
                         "dispositivos dos Decretos-Leis nºs 3.326, de 3 de junho de 1941, e 5.405, de 13 de abril de 1943, da "
                         "Consolidação das Leis do Trabalho (CLT), aprovada pelo Decreto-Lei nº 5.452, de 1º de maio de 1943, "
                         "e das Leis nºs 5.917, de 10 de setembro de 1973, e 6.261, de 14 de novembro de 1975; e dá outras "
                         "providências.", "2012-01-03", "2012-01-04", PAGES["l12587"]),
    "lei-6634-1979": _L("Lei nº 6.634, de 1979", "Dispõe sobre a Faixa de Fronteira, altera o Decreto-lei nº 1.135, de 3 de "
                        "dezembro de 1970, e dá outras providências.", "1979-05-02", "1979-05-03", PAGES["l6634"]),
    "lei-9469-1997": _L("Lei nº 9.469, de 1997", "Regulamenta o disposto no inciso VI do art. 4º da Lei Complementar nº 73, de "
                        "10 de fevereiro de 1993; dispõe sobre a intervenção da União nas causas em que figurarem, como autores "
                        "ou réus, entes da administração indireta; regula os pagamentos devidos pela Fazenda Pública em virtude "
                        "de sentença judiciária; revoga a Lei nº 8.197, de 27 de junho de 1991, e a Lei nº 9.081, de 19 de julho "
                        "de 1995, e dá outras providências.", "1997-07-10", "1997-07-11", PAGES["l9469"]),
    "lei-9537-1997": _L("Lei nº 9.537, de 1997", "Dispõe sobre a segurança do tráfego aquaviário em águas sob jurisdição "
                        "nacional e dá outras providências.", "1997-12-11", "1997-12-12", PAGES["l9537"]),
    "lei-13675-2018": _L("Lei nº 13.675, de 2018", "Disciplina a organização e o funcionamento dos órgãos responsáveis pela "
                         "segurança pública, nos termos do § 7º do art. 144 da Constituição Federal; cria a Política Nacional "
                         "de Segurança Pública e Defesa Social (PNSPDS); institui o Sistema Único de Segurança Pública (Susp); "
                         "altera a Lei Complementar nº 79, de 7 de janeiro de 1994, a Lei nº 10.201, de 14 de fevereiro de 2001, "
                         "e a Lei nº 11.530, de 24 de outubro de 2007; e revoga dispositivos da Lei nº 12.681, de 4 de julho de "
                         "2012.", "2018-06-11", "2018-06-12", PAGES["l13675"]),
    "lei-4728-1965": _L("Lei nº 4.728, de 1965", "Disciplina o mercado de capitais e estabelece medidas para o seu "
                        "desenvolvimento.", "1965-07-14", "1965-07-16", PAGES["l4728"]),
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
# part a: Lei 5.889/1973, Lei 4.090/1962, Lei 605/1949, Lei 7.418/1985
B7.CONVERTED_FIX["mp-410-2007"] = ("lei-11718-2008", "the MP page reads 'Convertida na Lei n 1 1.718, de 20.6.2008' (the "
                                                     "number broken by a space)")
P.MP_PENDING["mp-2164-2001"] = (
    "Medida Provisória nº 2.164-41, de 24.8.2001 (DOU 27.8.2001, in force on publication), kept in force by Emenda "
    "Constitucional 32/2001, art. 2. Planalto's notes name this edition only, so its changes are dated by its "
    "publication; earlier editions of the chain are not modelled")
P.MP_PENDING["mp-2165-2001"] = (
    "Medida Provisória nº 2.165-36, de 23.8.2001 (DOU 24.8.2001, art. 12: in force on publication), kept in force by "
    "Emenda Constitucional 32/2001, art. 2; its art. 13 revoked Lei 7.418 art. 1 § 1º. Planalto's note names this edition "
    "only, so the revocation is dated by its publication; earlier editions of the chain are not modelled")

# part b: Lei 9.029/1995, Lei 9.609/1998, Lei 9.637/1998, Lei 9.790/1999
P.MP_LAPSE["mp-850-2018"] = (
    "2019-02-12", "rejected: Ato do Presidente da Câmara dos Deputados de 13 de fevereiro de 2019 (DOU 14.2.2019) makes known "
                  "that 'em sessão realizada no dia 12 de fevereiro de 2019, o Plenário da Casa rejeitou, em apreciação "
                  "preliminar, o atendimento dos pressupostos constitucionais [...] da Medida Provisória nº 850, de 10 de "
                  "setembro de 2018 [...] e determinou o seu arquivamento' (MP DOU 11.9.2018; its art. 24, the change to Lei "
                  "9.637 art. 14 § 3º, in force on publication under its art. 29 II); the wording it had replaced is back "
                  "from 12.2.2019, as for Medida Provisória 446/2008")
P.MP_PENDING["mp-2216-2001"] = (
    "Medida Provisória nº 2.216-37, de 31.8.2001 (DOU 1.9.2001, art. 32: in force on publication), kept in force by Emenda "
    "Constitucional 32/2001, art. 2; its art. 18 gave Lei 9.790 art. 18 caput and § 1º their wording ('cinco anos'). "
    "Planalto's notes name this edition only (with 'Vide Medida Provisória nº 2.123-29, de 2001', an earlier edition of "
    "the chain), so the change is dated by its publication; earlier editions of the chain are not modelled")
B5.MP_REJECTED["mp-850-2018"] = ("Rejeição da Medida Provisória nº 850, de 2018",
                                 "Ato do Presidente da Câmara dos Deputados: rejeição da Medida Provisória nº 850, de 2018")

B13.OPEN_ITEMS["lei-das-organizacoes-sociais"] = (
    "Lei 9.637 (open items): Anexos I and II (the bodies extinguished and the entities authorised to be qualified as "
    "organizações sociais) are not part of the history; Medida Provisória 479/2009's art. 23-A, kept word for word by Lei "
    "12.269/2010, its conversion, is credited to the MP")
B13.OPEN_ITEMS["lei-das-oscips"] = (
    "Lei 9.790 (open items): Medida Provisória 2.216-37/2001's change to art. 18 is dated by that edition (Planalto also "
    "points to Medida Provisória 2.123-29/2001, an earlier edition of the chain, which is not modelled); 'Vide Lei nº "
    "13.800, de 2019' strikes no words")

# part c: Lei 1.060/1950, Lei 9.492/1997, Lei 6.024/1974, Lei 12.037/2009
P.MP_PENDING["mp-1894-1999"] = (
    "Medida Provisória nº 1.894-22, de 24.9.1999 (DOU 25.9.1999, art. 17: in force on publication), 'Reeditada pela MPv "
    "nº 1.894-23', one edition of a chain of monthly reissues; its art. 29 and 31 wordings of Lei 9.492 stand until Lei "
    "9.841/1999 (art. 40) gave both articles their wording (in force 20.11.1999: Lei 9.841 has no vigência clause, LINDB "
    "45 days after the DOU of 6.10.1999). Planalto's notes name this edition only; earlier and later editions of the "
    "chain are not modelled")
_LILE = "lei-da-intervencao-e-liquidacao-extrajudicial"
_W19 = ("Lei 6.024 art. 19: Medida Provisória 784/2017 (8.6.2017) rewrote the article (caput, incisos I-II with alíneas a)-f), "
        "§§ 1º-7º); it lapsed on 19.10.2017 and the 1974 article was in force again from 20.10.2017 until Lei 13.506/2017 "
        "(14.11.2017). Planalto prints the 1974 article a second time below MP 784's lines (struck, no note); its alíneas a) to "
        "d) start on 20.10.2017 with the restored caput, not in 1974")
_R784 = {"start": "2017-10-20", "start_law": "mp-784-2017-fim", "restored": True}
B8.SPAN_FIX += [
    ((_LILE, "art-19", "a)", "a) se os interessados", 1), _R784, _W19),
    ((_LILE, "art-19", "b)", "b) por transformação em liquidação ordinária", 1), _R784, _W19),
    ((_LILE, "art-19", "c)", "c) com a aprovação das contas finais", 1), _R784, _W19),
    ((_LILE, "art-19", "d)", "d) se decretada a falência", 1), _R784, _W19),
]
# Medida Provisória 955/2020 (DOU 20.4.2020) art. 1: 'Fica revogada a Medida Provisória nº 905, de 11 de novembro de 2019'.
# A page that notes only MP 905's change (Lei 12.037 art. 2 II) still falls under the CLT's MP 905/955 sequence: MP 955 is
# added to the laws such a page cites, so the shared model (batch 15's mp_pairs) dates it.
MP955_ADDED: list[str] = []
_note_laws17 = P.note_laws


def note_laws(paras):
    out = _note_laws17(paras)
    if "mp-905-2019" in out and "mp-955-2020" not in out:
        out.add("mp-955-2020")
        MP955_ADDED.append("x")
    return out


P.note_laws = note_laws
# On such a page the line MP 905 revoked is printed twice: struck with MP 905's note, then unstruck with no note. The struck
# copy stands until MP 955 lapsed (18.8.2020; absent while MP 905 stood, 12.11.2019 to 20.4.2020), and the unstruck copy is
# the line in force again from 19.8.2020, when MP 905 lapsed (absent on 18.8.2020, MP 905's last day).
MP955_ACTS = {"lei-da-identificacao-criminal"}
MP955_FIXED: list[str] = []


def mp955_two_copies(paras, act):
    if act["slug"] not in MP955_ACTS:
        return
    m_key, r_key = "mp-905-2019", "mp-955-2020"
    m_lapse, r_lapse = P.MP_LAPSE[m_key][0], P.MP_LAPSE[r_key][0]
    for i, p in enumerate(paras):
        if not p.get("mp_pair") or p["state"] == "plain" or p["end_law"] != m_key + "-fim":
            continue
        q = next((q for q in paras[i + 1:] if q["unit"] == p["unit"] and q["state"] == "plain" and q["label"] == p["label"]
                  and P.norm(q["text"]) == P.norm(p["text"]) and not q["notes"]), None)
        if q is None:
            continue
        p["end"], p["end_law"], p["end_how"] = r_lapse, r_key + "-fim", "mp-pair"
        q.update({"start": m_lapse, "start_law": m_key + "-fim", "end": None, "end_law": None, "end_how": None,
                  "skip": False, "restored": True, "pinned": True, "gaps": []})
        MP955_FIXED.append(f"{act['slug']} {p['unit']} [{p['label']}]")

# part e: Lei da Mobilidade Urbana (Lei 12.587/2012)
_LMU = "lei-da-mobilidade-urbana"
P.MP_LAPSE["mp-748-2016"] = (
    "2017-03-23", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 20, de 2017 (DOU 24.3.2017): 'teve seu "
                  "prazo de vigência encerrado no dia 22 de março do corrente ano'")
B13.OPEN_ITEMS[_LMU] = (
    "Lei 12.587 (open items): Planalto's 'Vide' pointers (Medida Provisória 1.179/2023 on art. 24 § 4º, Lei 15.432/2026 "
    "on the act) strike no words and are not modelled")
_W24 = ("Lei 12.587 art. 24 § 3º: Medida Provisória 818/2018 (12.1.2018) gave it a new wording ('sete anos'); Lei 13.683/2018, "
        "its conversion (20.6.2018), did not keep it, so Lei 13.406/2016's wording ('6 (seis) anos'), printed again unstruck "
        "below MP 818's, is in force from 20.6.2018 until Medida Provisória 906/2019 revoked the paragraph (20.11.2019); "
        "the placeholder '§ 3º (Revogado).' is Lei 14.000/2020's wording (MP 906's conversion, 20.5.2020), and the "
        "paragraph is absent from 20.11.2019 until then")
B8.SPAN_FIX += [
    ((_LMU, "art-24", "§ 3º", "§ 3º O Plano de Mobilidade Urbana será compatibilizado", 0),
     {"end": "2018-06-20", "end_law": "lei-13683-2018", "end_how": "conversion"}, _W24),
    ((_LMU, "art-24", "§ 3º", "§ 3º O Plano de Mobilidade Urbana deverá ser compatibilizado com o plano diretor municipal", 1),
     {"start": "2018-06-20", "start_law": "lei-13683-2018", "end": "2019-11-20", "end_law": "mp-906-2019",
      "end_how": "note", "restored": True, "skip": False, "gaps": []}, _W24),
    ((_LMU, "art-24", "§ 3º", "§ 3º (", 0), {"start": "2020-05-20", "start_law": "lei-14000-2020"}, _W24),
    ((_LMU, "art-24", "§ 5º", "§ 5º Encerrado o prazo", 0),
     {"end": "2017-03-23", "end_law": "mp-748-2016-fim", "end_how": "lapse"},
     "Lei 12.587 art. 24 § 5º as Medida Provisória 748/2016 added it: Lei 13.406/2016 (27.12.2016), a law of its own "
     "('Altera os §§ 3º e 4º do art. 24'), did not touch it, so it stands until MP 748 lapsed (22.3.2017; Ato Declaratório "
     "nº 20/2017)"),
]

# part f: Lei 6.634/1979, Lei 9.469/1997, Lei 9.537/1997
_LFF, _L9469, _LESTA = "lei-da-faixa-de-fronteira", "lei-9469-de-1997", "lei-da-seguranca-do-trafego-aquaviario"
if PART == "f":   # the text part b published stays as it is for part b
    P.MP_PENDING["mp-2216-2001"] = (
        "Medida Provisória nº 2.216-37, de 31.8.2001 (DOU 1.9.2001, art. 32: in force on publication), kept in force by "
        "Emenda Constitucional 32/2001, art. 2; its art. 33 revoked Lei 6.634 art. 9 § 1º. Planalto's note names this edition "
        "only, so the revocation is dated by its publication; earlier editions of the chain are not modelled")
P.MP_PENDING["mp-2226-2001"] = (
    "Medida Provisória nº 2.226, de 4.9.2001 (DOU 5.9.2001, edição extra; art. 4: in force on publication), kept in force by "
    "Emenda Constitucional 32/2001, art. 2; its art. 3 renumbered Lei 9.469 art. 6 parágrafo único "
    "as § 1º and added § 2º, which Lei 13.140/2015 revoked")
# Lei 14.004/2020 (DOU 27.5.2020) art. 1, the new wording of Lei 6.634 art. 4 caput and the new art. 8-A, was vetoed;
# Congress overrode the veto and the President of the Senate promulgated it in the DOU of 8.9.2020 (edição extra), printed on
# Lei 14.004's page ('Promulgação partes vetadas'). Lei 14.004 art. 3: in force on publication.
_W14004 = ("promulgated after the veto was overridden (Senado Federal, 8.9.2020; DOU 8.9.2020, edição extra; printed on Lei "
           "14.004's page as 'Promulgação partes vetadas'); Lei 14.004 art. 3: in force on publication")
P.VIGENCIA_PROVISION.update({("lei-14004-2020", _LFF, u): ("2020-09-08", "Lei 14.004/2020 art. 1 " + _W14004)
                             for u in ("art-04", "art-08-a")})
if any(a["slug"] == _LFF for a in ACTS):
    EXTRA.append("Lei 6.634 art. 4 caput and art. 8-A: Lei 14.004/2020 (DOU 27.5.2020) art. 1, which gave them their wording, "
                 "was vetoed; Congress overrode the veto and the President of the Senate promulgated the part (DOU 8.9.2020, "
                 "edição extra; printed on Lei 14.004's page, 'Promulgação partes vetadas'). Lei 14.004 art. 3: in force on "
                 "publication; the change is dated 8.9.2020, credited to Lei 14.004, and the 1979 caput of art. 4 stands to "
                 "then.")
B13.OPEN_ITEMS[_L9469] = (
    "Lei 9.469 (open items): Planalto's 'Vide ADIN Nº 2.527-9' on art. 6 (the § 2º Medida Provisória 2.226/2001 added, "
    "revoked by Lei 13.140/2015) and 'Vide Lei nº 14.057, de 2020' on art. 1 are pointers that strike no words on the page "
    "and are not modelled; the text before 11.7.1997 (the Medida Provisória 1.561 chain; this Lei is the conversion of "
    "its edition 1.561-6/1997) is not part of the history")
B13.OPEN_ITEMS[_LESTA] = (
    "Lei 9.537 (open items): the regulations it names (Decreto 2.596/1998, 'Vide Decreto nº 5.129, de 2004') are not part "
    "of the history")

# Lei 7.418/1985: Lei 7.619/1987 (DOU 1.10.1987, in force on publication) art. 1 gave art. 1 caput a new wording and
# revoked art. 1 § 2º and art. 2, 'renumerando-se os demais'. Planalto prints arts. 3 to 13 of 1985 only under their new
# numbers (2 to 12, each with '(Renumerado do art. N, pela Lei 7.619, de 30.9.1987)'). Lei 7.619 changed no other words,
# so each of them stood under its old number from 17.12.1985 to 1.10.1987, with the lines it had then.
_LVT = "lei-do-vale-transporte"
RENUM_ART = {_LVT: ("1987-10-01", "lei-7619-1987")}
RENUM_ART_USED: list[str] = []
_RENUM_RX = re.compile(r"Renumerad[oa]\s+do\s+art\s*\.\s*(\d+)", re.I)


def _ordinal(n: int) -> str:
    return f"{n}º" if n < 10 else str(n)


def renum_articles(paras, act):
    if act["slug"] not in RENUM_ART:
        return
    day, law = RENUM_ART[act["slug"]]
    act_day = B.ACT_DAY[act["law"]][0]
    old_of: dict[str, int] = {}
    for p in paras:
        if p["heading"] or not p["label"].startswith("Art"):
            continue
        for n in p["notes"]:
            m = _RENUM_RX.search(n)
            if m:
                old_of[p["unit"]] = int(m.group(1))
    if not old_of:
        return
    copies, first = [], None
    for i, p in enumerate(paras):
        if p["heading"] or p.get("skip") or p["unit"] not in old_of:
            continue
        if first is None and any(_RENUM_RX.search(n) for n in p["notes"]):
            first = i
        if p["start"] > day or (p["end"] is not None and p["end"] <= day):
            continue
        old = old_of[p["unit"]]
        c = dict(p, unit=f"art-{old:02d}", gaps=[], start=act_day, start_law=None, end=day, end_law=law,
                 end_how="renumbered", notes=[n for n in p["notes"] if not _RENUM_RX.search(n)])
        if p["label"].startswith("Art"):
            new_label = f"Art. {_ordinal(old)}"
            c["text"] = new_label + p["text"][len(p["label"]):]
            c["label"] = new_label
            RENUM_ART_USED.append(f"art. {old} -> {p['label'][5:]}")
        copies.append(c)
        if p["start"] < day:
            p["start"], p["start_law"] = day, law
    copies.sort(key=lambda c: int(c["unit"][4:]))
    paras[first:first] = copies
    for i, p in enumerate(paras):
        p["i"] = i


# Lei 605/1949: Planalto's page prints two lines with no note and no label, 'Descanso semanal' above art. 1 and
# 'Harmonização de multas trabalhistas constantes de legislações esparsas' above art. 12. They are the headings of
# Medida Provisória 905/2019's own articles (its art. 29 and the heading above it, read on the MP's page), copied onto the
# page with MP 905's wordings; they are not words of Lei 605 and are left out.
FOREIGN_RUBRICS = {"l0605": ("Descanso semanal", "Harmonização de multas trabalhistas constantes de legislações esparsas")}
FOREIGN_DROPPED: list[str] = []
QUOTED_HEADINGS: list[str] = []
_paragraphs17 = P.paragraphs


def paragraphs(html, digits):
    page = B8.CURRENT_PAGE[0]
    out, rest = _paragraphs17(html, digits)
    drop = FOREIGN_RUBRICS.get(page)
    if drop:
        keep = []
        for p in out:
            if p["label"] in ("", "rubrica") and not p["notes"] and P.norm(p["text"]) in drop:
                FOREIGN_DROPPED.append(f"{page}: {P.norm(p['text'])!r}")
                continue
            keep.append(p)
        out = keep
    if page == "l11105":
        # Lei 11.105 art. 37 quotes Lei 6.938's Anexo VIII ('"ANEXO VIII' and a table): the quoted annex title is a line
        # of art. 37, not a heading of Lei 11.105; an empty centred line after it is dropped
        cur, keep = None, []
        for p in out:
            if p["heading"] and not P.norm(p["text"]):
                QUOTED_HEADINGS.append(f"{page}: empty heading line")
                continue
            if p["heading"] and cur and P.norm(p["text"]).startswith('"ANEXO'):
                p.update({"heading": False, "unit": cur, "label": "", "center": False})
                QUOTED_HEADINGS.append(f"{page}: {P.norm(p['text'])!r} -> {cur}")
            elif not p["heading"] and p["unit"].startswith("art-"):
                cur = p["unit"]
            keep.append(p)
        out = keep
    return out, rest


P.paragraphs = B.paragraphs = paragraphs

# Lei 9.263/1996: arts. 10, 11 and 15 and art. 14 Parágrafo único were vetoed on 12.1.1996; Congress overrode the vetoes
# and the President promulgated them (Mensagem nº 928, de 19.8.1997, DOU 20.8.1997: 'acabo de promulgá-los'). Planalto
# prints them with '(Artigo vetado e mantido pelo Congresso Nacional)' / '(Parágrafo vetado e mantido ...)': they start on
# 20.8.1997, credited to Lei 9.263 (as 99-batch5's promulgated parts of Lei 14.133); the page prints no '(VETADO)' line
# for them, so they are absent before.
VETO_KEPT = {"lei-do-planejamento-familiar": ("1997-08-20", {("art-10", None), ("art-11", None), ("art-15", None),
                                                             ("art-14", "Parágrafo único")})}
VETO_KEPT_USED: list[str] = []


def veto_kept(paras, act):
    if act["slug"] not in VETO_KEPT:
        return
    day, where = VETO_KEPT[act["slug"]]
    for unit, label in sorted(where, key=str):
        hit = [p for p in paras if p["unit"] == unit and not p["heading"] and not p.get("skip")
               and (label is None or p["label"] == label) and p["start"] < day]
        for p in hit:
            p["start"], p["start_law"] = day, act["law"]
        VETO_KEPT_USED.append(f"art. {int(unit[4:])}" + (f" {label}" if label else "") + f" ({len(hit)} lines)")


# part g: Lei 13.675/2018 (Susp). Lei 14.531/2023 (DOU 11.1.2023) art. 2: its art. 9 § 2º XVII and art. 42-A § 7º were
# vetoed; Congress overrode the vetoes and the Vice-President, as acting President, promulgated them (DOU 19.7.2023, printed
# on Lei 14.531's page). Planalto prints them with Lei 14.531's other lines, '(Incluído pela Lei nº 14.531, de 2023)'.
_LSUSP = "lei-do-susp"
PROMULGATED = {_LSUSP: [("art-09", "XVII -", "XVII - polícia legislativa", "2023-07-19", "lei-14531-2023"),
                        ("art-42-a", "§ 7º", "§ 7º O disposto neste artigo aplica-se aos integrantes", "2023-07-19",
                         "lei-14531-2023")]}
PROMULGATED_USED: list[str] = []


def promulgated(paras, act):
    for unit, label, start, day, law in PROMULGATED.get(act["slug"], []):
        hit = [p for p in paras if p["unit"] == unit and p["label"] == label and not p["heading"] and not p.get("skip")
               and P.norm(p["text"]).startswith(start) and p["start"] < day]
        for p in hit:
            p["start"], p["start_law"] = day, law
        PROMULGATED_USED.append(f"art. {unit[4:].lstrip('0')} {label.rstrip(' -')} ({len(hit)} line)")


B.EXPLAINED[_LSUSP] = {
    "art-47": "check artefact: art. 47 quotes Lei 10.201/2001 art. 4 with the dotted line '§ 3º .....', which the history "
              "keeps as '§ 3º.' and the check, reading label-only lines as revoked dispositivos, drops",
}
B13.OPEN_ITEMS[_LSUSP] = (
    "Lei 13.675 (open items): 'Vide ADPF 995' on art. 9 (the STF's reading of the guardas municipais as part of the Susp) "
    "strikes no words and is not modelled")

_apply_rewrites17 = P.apply_rewrites


def apply_rewrites(paras, act, eff, problems):
    out = _apply_rewrites17(paras, act, eff, problems)
    renum_articles(paras, act)
    mp955_two_copies(paras, act)
    veto_kept(paras, act)
    promulgated(paras, act)
    return out


P.apply_rewrites = B.apply_rewrites = apply_rewrites

# ---------------------------------------------------------------------------------------------------------------
_inner17 = B6.PB5B._write_part5


def _inner(*a):
    dec = list(EXTRA)
    if RENUM_ART_USED:
        dec.append("Lei 7.418: Lei 7.619/1987 (DOU 1.10.1987) art. 1 rewrote art. 1 caput and revoked art. 1 § 2º and art. 2, "
                   "'renumerando-se os demais'; it changed no other words. Planalto prints the other 1985 articles only under "
                   "their new numbers, noted '(Renumerado do art. N, pela Lei 7.619, de 30.9.1987)'; each stands under its old "
                   "number, with the lines it had then, from 17.12.1985 to 1.10.1987: " + ", ".join(dict.fromkeys(RENUM_ART_USED))
                   + ".")
    if MP955_ADDED:
        dec.append("Medida Provisória 955/2020 (DOU 20.4.2020, art. 1: 'Fica revogada a Medida Provisória nº 905, de 11 de "
                   "novembro de 2019') is not noted on every page that notes Medida Provisória 905/2019; where it is not "
                   "(Lei 12.037 art. 2 II), the change MP 905 made is still dated by the CLT's MP 905/955 sequence: in force "
                   "12.11.2019, undone while MP 955 stood (20.4.2020 to its lapse on 18.8.2020), in force again on 18.8.2020, "
                   "MP 905's last day, and undone from 19.8.2020, when MP 905 lapsed. Planalto prints the line MP 905 "
                   "revoked twice, struck with MP 905's note and again unstruck; the unstruck copy is the line from "
                   "19.8.2020" + (" (" + ", ".join(MP955_FIXED) + ")" if MP955_FIXED else "") + ".")
    if any("ANEXO" in x for x in QUOTED_HEADINGS):
        dec.append("Lei 11.105 art. 37 gives Lei 6.938's Anexo VIII (Código 20) a new description and quotes the annex with its "
                   "title ('\"ANEXO VIII') and table; Planalto centres the quoted title, which is read as a line of art. 37, "
                   "not as a heading of Lei 11.105.")
    if VETO_KEPT_USED:
        dec.append("Lei 9.263: the parts vetoed on 12.1.1996 that Congress kept (Planalto: '(Artigo vetado e mantido pelo "
                   "Congresso Nacional)', '(Parágrafo vetado e mantido ...)') were promulgated by the President "
                   "(Mensagem nº 928, de 19.8.1997: 'acabo de promulgá-los'; DOU 20.8.1997) and start that day, credited "
                   "to Lei 9.263: " + ", ".join(VETO_KEPT_USED) + ".")
    if PROMULGATED_USED:
        dec.append("Lei 13.675: Lei 14.531/2023 (DOU 11.1.2023, in force on publication) added art. 9 § 2º XVII and art. 42-A "
                   "§ 7º, but they were vetoed; Congress overrode the vetoes and they were promulgated in the DOU of 19.7.2023 "
                   "(printed on Lei 14.531's page). Planalto notes them '(Incluído pela Lei nº 14.531, de 2023)' with the "
                   "law's other lines; they start on 19.7.2023, credited to Lei 14.531: " + ", ".join(PROMULGATED_USED) + ".")
    if FOREIGN_DROPPED:
        dec.append("Lei 605: two unlabelled lines Planalto prints with no note, 'Descanso semanal' (above art. 1) and "
                   "'Harmonização de multas trabalhistas constantes de legislações esparsas' (above art. 12), are the "
                   "headings of Medida Provisória 905/2019's own provisions (above its art. 29 and its new art. 12 wording, as "
                   "printed on the MP's page), copied onto the page with MP 905's wordings; they are not words of Lei 605 and "
                   "are left out.")
    B5.EXTRA_DECISIONS.extend(dec)
    return _inner17(*a)


B6.PB5B._write_part5 = _inner

SRC = HERE / "sources_batch17.json"
if not SRC.exists():
    SRC.write_text('{\n "fetch": []\n}\n', encoding="utf-8", newline="\n")
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
