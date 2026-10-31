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
    # part h, ...: tax laws
    "l7689": "leis/l7689.htm",
    "l9249": "leis/l9249.htm",
    "l9250": "leis/l9250.htm",
    "l9250-compilado": "leis/l9250compilado.htm",
    "l7713": "leis/l7713.htm",
    "l7713-compilada": "leis/l7713compilada.htm",
    "l9430": "leis/l9430.htm",
    "l9430-compilada": "leis/l9430compilada.htm",
    # parts l, m
    "l13465": "_ato2015-2018/2017/lei/l13465.htm",
    "l11977": "_ato2007-2010/2009/lei/l11977.htm",
    "l11977-compilado": "_ato2007-2010/2009/lei/l11977compilado.htm",
    # part n
    "l11788": "_ato2007-2010/2008/lei/l11788.htm",
    "l12318": "_ato2007-2010/2010/lei/l12318.htm",
    "l10048": "leis/l10048.htm",
    "l11804": "_ato2007-2010/2008/lei/l11804.htm",
    # part o
    "l11107": "_ato2004-2006/2005/lei/l11107.htm",
    "l10098": "leis/l10098.htm",
    # part p
    "l11096": "_ato2004-2006/2005/lei/l11096.htm",
    "l11096-compilado": "_ato2004-2006/2005/lei/l11096compilado.htm",
    "l12711": "_ato2011-2014/2012/lei/l12711.htm",
    "l13431": "_ato2015-2018/2017/lei/l13431.htm",
    # part q: Lei 10.522/2002
    "l10522": "leis/2002/l10522.htm",
    "l10522-compilado": "leis/2002/l10522compilado.htm",
    # parts r, ...: next candidates
    "l12462": "_ato2011-2014/2011/lei/l12462.htm",
    "l12462-compilado": "_ato2011-2014/2011/lei/l12462compilado.htm",
    "l10520": "leis/2002/l10520.htm",
    "l10520-2023": "leis/2002/l10520.htm",
    "l9873": "leis/l9873.htm",
    "l10233": "leis/leis_2001/l10233.htm",
    "l9074": "leis/l9074cons.htm",
    "l9074-compilada": "leis/l9074compilada.htm",
    "l12815": "_ato2011-2014/2013/lei/l12815.htm",
    "l12783": "_ato2011-2014/2013/lei/l12783.htm",
    # part x
    "l13848": "_ato2019-2022/2019/lei/l13848.htm",
    "l9986": "leis/l9986.htm",
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
    _act("lei-da-csll", "LCSLL", "l7689", "l7689", "lei-7689-1988",
         "Contribuição Social sobre o Lucro Líquido - CSLL (Lei nº 7.689, de 15 de dezembro de 1988)", 2),
    _act("lei-9249-de-1995", "L9249", "l9249", "l9249", "lei-9249-1995",
         "Imposto de renda das pessoas jurídicas e CSLL (Lei nº 9.249, de 26 de dezembro de 1995)", 2),
    _act("lei-9250-de-1995", "L9250", "l9250", "l9250-compilado", "lei-9250-1995",
         "Imposto de renda das pessoas físicas (Lei nº 9.250, de 26 de dezembro de 1995)", 2),
    _act("lei-7713-de-1988", "L7713", "l7713", "l7713-compilada", "lei-7713-1988",
         "Imposto de renda (Lei nº 7.713, de 22 de dezembro de 1988)", 2),
    _act("lei-9430-de-1996", "L9430", "l9430", "l9430-compilada", "lei-9430-1996",
         "Legislação tributária federal (Lei nº 9.430, de 27 de dezembro de 1996)", 2),
    _act("lei-da-regularizacao-fundiaria", "LREURB", "l13465", "l13465", "lei-13465-2017",
         "Lei da Regularização Fundiária Rural e Urbana (Lei nº 13.465, de 11 de julho de 2017)", 2),
    _act("lei-minha-casa-minha-vida", "LMCMV", "l11977", "l11977-compilado", "lei-11977-2009",
         "Programa Minha Casa, Minha Vida (Lei nº 11.977, de 7 de julho de 2009)", 2),
    _act("lei-do-estagio", "LEst", "l11788", "l11788", "lei-11788-2008",
         "Lei do Estágio (Lei nº 11.788, de 25 de setembro de 2008)", 2),
    _act("lei-da-alienacao-parental", "LAP", "l12318", "l12318", "lei-12318-2010",
         "Lei da Alienação Parental (Lei nº 12.318, de 26 de agosto de 2010)", 2),
    _act("lei-do-atendimento-prioritario", "LAPr", "l10048", "l10048", "lei-10048-2000",
         "Atendimento prioritário (Lei nº 10.048, de 8 de novembro de 2000)", 2),
    _act("lei-dos-alimentos-gravidicos", "LAG", "l11804", "l11804", "lei-11804-2008",
         "Lei dos Alimentos Gravídicos (Lei nº 11.804, de 5 de novembro de 2008)", 2),
    _act("lei-dos-consorcios-publicos", "LCP", "l11107", "l11107", "lei-11107-2005",
         "Lei dos Consórcios Públicos (Lei nº 11.107, de 6 de abril de 2005)", 2),
    _act("lei-da-acessibilidade", "LAc", "l10098", "l10098", "lei-10098-2000",
         "Lei da Acessibilidade (Lei nº 10.098, de 19 de dezembro de 2000)", 2),
    _act("lei-do-prouni", "LProUni", "l11096", "l11096-compilado", "lei-11096-2005",
         "Programa Universidade para Todos - ProUni (Lei nº 11.096, de 13 de janeiro de 2005)", 2),
    _act("lei-de-cotas", "LCotas", "l12711", "l12711", "lei-12711-2012",
         "Lei de Cotas (Lei nº 12.711, de 29 de agosto de 2012)", 2),
    _act("lei-da-escuta-protegida", "LEP17", "l13431", "l13431", "lei-13431-2017",
         "Lei da Escuta Protegida (Lei nº 13.431, de 4 de abril de 2017)", 2),
    _act("lei-do-cadin", "LCadin", "l10522", "l10522-compilado", "lei-10522-2002",
         "Lei do Cadin (Lei nº 10.522, de 19 de julho de 2002)", 2),
    _act("lei-da-prescricao-da-acao-punitiva", "LPAP", "l9873", "l9873", "lei-9873-1999",
         "Prescrição da ação punitiva da Administração Pública Federal (Lei nº 9.873, de 23 de novembro de 1999)", 2),
    _act("lei-do-pregao", "LPreg", "l10520-2023", "l10520-2023", "lei-10520-2002",
         "Lei do Pregão (Lei nº 10.520, de 17 de julho de 2002)", 2),
    _act("lei-das-concessoes-do-setor-eletrico", "LCSE", "l12783", "l12783", "lei-12783-2013",
         "Concessões de energia elétrica e modicidade tarifária (Lei nº 12.783, de 11 de janeiro de 2013)", 2),
    _act("lei-dos-portos", "LPortos", "l12815", "l12815", "lei-12815-2013",
         "Lei dos Portos (Lei nº 12.815, de 5 de junho de 2013)", 2),
    _act("lei-9074-de-1995", "L9074", "l9074", "l9074-compilada", "lei-9074-1995",
         "Outorga e prorrogação de concessões e permissões de serviços públicos (Lei nº 9.074, de 7 de julho de 1995)", 2),
    _act("lei-do-rdc", "LRDC", "l12462", "l12462-compilado", "lei-12462-2011",
         "Regime Diferenciado de Contratações Públicas - RDC (Lei nº 12.462, de 4 de agosto de 2011)", 2),
    _act("lei-da-antt-e-antaq", "L10233", "l10233", "l10233", "lei-10233-2001",
         "Reestruturação dos transportes aquaviário e terrestre, ANTT e ANTAQ (Lei nº 10.233, de 5 de junho de 2001)", 2),
    _act("lei-geral-das-agencias-reguladoras", "LAR", "l13848", "l13848", "lei-13848-2019",
         "Lei Geral das Agências Reguladoras (Lei nº 13.848, de 25 de junho de 2019)", 2),
    _act("lei-9986-de-2000", "L9986", "l9986", "l9986", "lei-9986-2000",
         "Gestão de recursos humanos das agências reguladoras (Lei nº 9.986, de 18 de julho de 2000)", 2),
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
    "h": ["lei-da-csll", "lei-9249-de-1995"],
    "i": ["lei-9250-de-1995"],
    "j": ["lei-7713-de-1988"],
    "k": ["lei-9430-de-1996"],
    "l": ["lei-da-regularizacao-fundiaria"],
    "m": ["lei-minha-casa-minha-vida"],
    "n": ["lei-do-estagio", "lei-da-alienacao-parental", "lei-do-atendimento-prioritario", "lei-dos-alimentos-gravidicos"],
    "o": ["lei-dos-consorcios-publicos", "lei-da-acessibilidade"],
    "p": ["lei-do-prouni", "lei-de-cotas", "lei-da-escuta-protegida"],
    "q": ["lei-do-cadin"],
    "r": ["lei-da-prescricao-da-acao-punitiva", "lei-do-pregao"],
    "s": ["lei-das-concessoes-do-setor-eletrico"],
    "t": ["lei-dos-portos"],
    "u": ["lei-9074-de-1995"],
    "v": ["lei-do-rdc"],
    "w": ["lei-da-antt-e-antaq"],
    "x": ["lei-geral-das-agencias-reguladoras", "lei-9986-de-2000"],
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
    "lei-7689-1988": ("1988-12-16", f"Lei 7.689/1988 art. 12: {_PUB} (DOU 16.12.1988)"),
    "lei-9249-1995": ("1996-01-01", "Lei 9.249/1995 art. 35: 'Esta Lei entra em vigor na data de sua publicação, produzindo "
                                    "efeitos a partir de 1º de janeiro de 1996' (DOU 27.12.1995): dated by the day it takes "
                                    "effect"),
    "lei-9250-1995": ("1995-12-27", f"Lei 9.250/1995 art. 41: {_PUB} (DOU 27.12.1995)"),
    "lei-7713-1988": ("1989-01-01", "Lei 7.713/1988 art. 57: 'Esta Lei entra em vigor em 1º de janeiro de 1989' (DOU "
                                    "23.12.1988, the day LexML gives; the page footer misprints 23.12.1998)"),
    "lei-9430-1996": ("1996-12-30", "Lei 9.430/1996 art. 87: 'Esta Lei entra em vigor na data da sua publicação, produzindo "
                                    "efeitos financeiros a partir de 1º de janeiro de 1997' (DOU 30.12.1996): financial "
                                    "effects only, so the in-force day"),
    "lei-13465-2017": ("2017-07-12", f"Lei 13.465/2017 art. 108: {_PUB} (DOU 12.7.2017, rectified 6.9.2017; the "
                                     "consolidated text republished in the DOU of 8.9.2017)"),
    "lei-11977-2009": ("2009-07-08", f"Lei 11.977/2009 art. 83: {_PUB} (DOU 8.7.2009)"),
    "lei-11788-2008": ("2008-09-26", f"Lei 11.788/2008 art. 21: {_PUB} (DOU 26.9.2008)"),
    "lei-12318-2010": ("2010-08-27", f"Lei 12.318/2010 art. 11: {_PUB} (DOU 27.8.2010, rectified 31.8.2010)"),
    "lei-10048-2000": ("2000-11-09", f"Lei 10.048/2000 art. 8: {_PUB} (DOU 9.11.2000)"),
    "lei-11804-2008": ("2008-11-06", f"Lei 11.804/2008 art. 12: {_PUB} (DOU 6.11.2008)"),
    "lei-11107-2005": ("2005-04-07", f"Lei 11.107/2005 art. 21: {_PUB} (DOU 7.4.2005)"),
    "lei-10098-2000": ("2000-12-20", f"Lei 10.098/2000 art. 27: {_PUB} (DOU 20.12.2000)"),
    "lei-11096-2005": ("2005-01-14", f"Lei 11.096/2005 art. 23: {_PUB} (DOU 14.1.2005)"),
    "lei-12711-2012": ("2012-08-30", f"Lei 12.711/2012 art. 9: {_PUB} (DOU 30.8.2012)"),
    "lei-13431-2017": ("2018-04-05", "Lei 13.431/2017 art. 29: 'Esta Lei entra em vigor após decorrido 1 (um) ano de sua "
                                     "publicação oficial' (DOU 5.4.2017): one year after publication, 5.4.2018"),
    "lei-10522-2002": ("2002-07-22", f"Lei 10.522/2002 art. 40: {_PUB} (DOU 22.7.2002)"),
    "lei-9873-1999": ("1999-11-24", f"Lei 9.873/1999 art. 7: {_PUB} (DOU 24.11.1999, edição extra)"),
    "lei-10520-2002": ("2002-07-18", f"Lei 10.520/2002 art. 13: {_PUB} (DOU 18.7.2002, rectified 30.7.2002)"),
    "lei-12783-2013": ("2013-01-14", f"Lei 12.783/2013 art. 32: {_PUB} (DOU 14.1.2013)"),
    "lei-12815-2013": ("2013-06-05", f"Lei 12.815/2013 art. 75: {_PUB} (DOU 5.6.2013, edição extra)"),
    "lei-9074-1995": ("1995-07-08", f"Lei 9.074/1995 art. 39: {_PUB} (DOU 8.7.1995, edição extra; republished 28.9.1998)"),
    "lei-12462-2011": ("2011-08-05", "Lei 12.462/2011 art. 70: 'Esta Lei entra em vigor na data de sua publicação, produzindo "
                                     "efeitos financeiros, no tocante ao art. 52 desta Lei, a contar da transferência dos órgãos "
                                     "ali referidos' (DOU 5.8.2011, edição extra, rectified 10.8.2011): financial effects only, so "
                                     "the in-force day"),
    "lei-10233-2001": ("2001-06-06", f"Lei 10.233/2001 art. 124: {_PUB} (DOU 6.6.2001)"),
    "lei-13848-2019": ("2019-09-24", "Lei 13.848/2019 art. 53: 'Esta Lei entra em vigor após decorridos 90 (noventa) dias de "
                                     "sua publicação oficial' (DOU 26.6.2019)"),
    "lei-9986-2000": ("2000-07-19", f"Lei 9.986/2000 art. 38: {_PUB} (DOU 19.7.2000)"),
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
    "lei-7689-1988": _L("Lei nº 7.689, de 1988", "Institui contribuição social sobre o lucro das pessoas jurídicas e dá "
                        "outras providências.", "1988-12-15", "1988-12-16", PAGES["l7689"]),
    "lei-9249-1995": _L("Lei nº 9.249, de 1995", "Altera a legislação do imposto de renda das pessoas jurídicas, bem como da "
                        "contribuição social sobre o lucro líquido, e dá outras providências.", "1995-12-26", "1995-12-27",
                        PAGES["l9249"]),
    "lei-9250-1995": _L("Lei nº 9.250, de 1995", "Altera a legislação do imposto de renda das pessoas físicas e dá outras "
                        "providências.", "1995-12-26", "1995-12-27", PAGES["l9250"]),
    "lei-7713-1988": _L("Lei nº 7.713, de 1988", "Altera a legislação do imposto de renda e dá outras providências.",
                        "1988-12-22", "1988-12-23", PAGES["l7713"]),
    "lei-9430-1996": _L("Lei nº 9.430, de 1996", "Dispõe sobre a legislação tributária federal, as contribuições para a "
                        "seguridade social, o processo administrativo de consulta e dá outras providências.", "1996-12-27",
                        "1996-12-30", PAGES["l9430"]),
    "lei-13465-2017": _L("Lei nº 13.465, de 2017", "Dispõe sobre a regularização fundiária rural e urbana, sobre a liquidação "
                         "de créditos concedidos aos assentados da reforma agrária e sobre a regularização fundiária no âmbito "
                         "da Amazônia Legal; institui mecanismos para aprimorar a eficiência dos procedimentos de alienação de "
                         "imóveis da União; e dá outras providências.", "2017-07-11", "2017-07-12", PAGES["l13465"]),
    "lei-11977-2009": _L("Lei nº 11.977, de 2009", "Dispõe sobre o Programa Minha Casa, Minha Vida – PMCMV e a regularização "
                         "fundiária de assentamentos localizados em áreas urbanas; altera o Decreto-Lei nº 3.365, de 21 de junho "
                         "de 1941, as Leis nºs 4.380, de 21 de agosto de 1964, 6.015, de 31 de dezembro de 1973, 8.036, de 11 de "
                         "maio de 1990, e 10.257, de 10 de julho de 2001, e a Medida Provisória nº 2.197-43, de 24 de agosto de "
                         "2001; e dá outras providências.", "2009-07-07", "2009-07-08", PAGES["l11977"]),
    "lei-11788-2008": _L("Lei nº 11.788, de 2008", "Dispõe sobre o estágio de estudantes; altera a redação do art. 428 da "
                         "Consolidação das Leis do Trabalho – CLT, aprovada pelo Decreto-Lei nº 5.452, de 1º de maio de 1943, e a "
                         "Lei nº 9.394, de 20 de dezembro de 1996; revoga as Leis nºs 6.494, de 7 de dezembro de 1977, e 8.859, de "
                         "23 de março de 1994, o parágrafo único do art. 82 da Lei nº 9.394, de 20 de dezembro de 1996, e o art. 6º "
                         "da Medida Provisória nº 2.164-41, de 24 de agosto de 2001; e dá outras providências.", "2008-09-25",
                         "2008-09-26", PAGES["l11788"]),
    "lei-12318-2010": _L("Lei nº 12.318, de 2010", "Dispõe sobre a alienação parental e altera o art. 236 da Lei nº 8.069, de 13 "
                         "de julho de 1990.", "2010-08-26", "2010-08-27", PAGES["l12318"]),
    "lei-10048-2000": _L("Lei nº 10.048, de 2000", "Dá prioridade de atendimento às pessoas que especifica, e dá outras "
                         "providências.", "2000-11-08", "2000-11-09", PAGES["l10048"]),
    "lei-11804-2008": _L("Lei nº 11.804, de 2008", "Disciplina o direito a alimentos gravídicos e a forma como ele será exercido "
                         "e dá outras providências.", "2008-11-05", "2008-11-06", PAGES["l11804"]),
    "lei-11107-2005": _L("Lei nº 11.107, de 2005", "Dispõe sobre normas gerais de contratação de consórcios públicos e dá outras "
                         "providências.", "2005-04-06", "2005-04-07", PAGES["l11107"]),
    "lei-10098-2000": _L("Lei nº 10.098, de 2000", "Estabelece normas gerais e critérios básicos para a promoção da "
                         "acessibilidade das pessoas portadoras de deficiência ou com mobilidade reduzida, e dá outras "
                         "providências.", "2000-12-19", "2000-12-20", PAGES["l10098"]),
    "lei-11096-2005": _L("Lei nº 11.096, de 2005", "Institui o Programa Universidade para Todos - PROUNI, regula a atuação de "
                         "entidades beneficentes de assistência social no ensino superior; altera a Lei nº 10.891, de 9 de julho "
                         "de 2004, e dá outras providências.", "2005-01-13", "2005-01-14", PAGES["l11096"]),
    "lei-12711-2012": _L("Lei nº 12.711, de 2012", "Dispõe sobre o ingresso nas universidades federais e nas instituições "
                         "federais de ensino técnico de nível médio e dá outras providências.", "2012-08-29", "2012-08-30",
                         PAGES["l12711"]),
    "lei-13431-2017": _L("Lei nº 13.431, de 2017", "Estabelece o sistema de garantia de direitos da criança e do adolescente "
                         "vítima ou testemunha de violência e altera a Lei nº 8.069, de 13 de julho de 1990 (Estatuto da Criança "
                         "e do Adolescente).", "2017-04-04", "2017-04-05", PAGES["l13431"]),
    "lei-10522-2002": _L("Lei nº 10.522, de 2002", "Dispõe sobre o Cadastro Informativo dos créditos não quitados de órgãos e "
                         "entidades federais e dá outras providências.", "2002-07-19", "2002-07-22", PAGES["l10522"]),
    "lei-9873-1999": _L("Lei nº 9.873, de 1999", "Estabelece prazo de prescrição para o exercício de ação punitiva pela "
                        "Administração Pública Federal, direta e indireta, e dá outras providências.", "1999-11-23", "1999-11-24",
                        PAGES["l9873"]),
    "lei-10520-2002": _L("Lei nº 10.520, de 2002", "Institui, no âmbito da União, Estados, Distrito Federal e Municípios, nos "
                         "termos do art. 37, inciso XXI, da Constituição Federal, modalidade de licitação denominada pregão, para "
                         "aquisição de bens e serviços comuns, e dá outras providências.", "2002-07-17", "2002-07-18",
                         PAGES["l10520"]),
    "lei-12783-2013": _L("Lei nº 12.783, de 2013", "Dispõe sobre as concessões de geração, transmissão e distribuição de energia "
                         "elétrica, sobre a redução dos encargos setoriais e sobre a modicidade tarifária; altera as Leis nºs "
                         "10.438, de 26 de abril de 2002, 12.111, de 9 de dezembro de 2009, 9.648, de 27 de maio de 1998, 9.427, de "
                         "26 de dezembro de 1996, e 10.848, de 15 de março de 2004; revoga dispositivo da Lei nº 8.631, de 4 de "
                         "março de 1993; e dá outras providências.", "2013-01-11", "2013-01-14", PAGES["l12783"]),
    "lei-12815-2013": _L("Lei nº 12.815, de 2013", "Dispõe sobre a exploração direta e indireta pela União de portos e "
                         "instalações portuárias e sobre as atividades desempenhadas pelos operadores portuários; altera as Leis "
                         "nºs 5.025, de 10 de junho de 1966, 10.233, de 5 de junho de 2001, 10.683, de 28 de maio de 2003, 9.719, de "
                         "27 de novembro de 1998, e 8.213, de 24 de julho de 1991; revoga as Leis nºs 8.630, de 25 de fevereiro de "
                         "1993, e 11.610, de 12 de dezembro de 2007, e dispositivos das Leis nºs 11.314, de 3 de julho de 2006, e "
                         "11.518, de 5 de setembro de 2007; e dá outras providências.", "2013-06-05", "2013-06-05",
                         PAGES["l12815"]),
    "lei-9074-1995": _L("Lei nº 9.074, de 1995", "Estabelece normas para outorga e prorrogações das concessões e permissões de "
                        "serviços públicos e dá outras providências.", "1995-07-07", "1995-07-08", PAGES["l9074"]),
    "lei-12462-2011": _L("Lei nº 12.462, de 2011", "Institui o Regime Diferenciado de Contratações Públicas - RDC; altera a Lei "
                         "nº 10.683, de 28 de maio de 2003, que dispõe sobre a organização da Presidência da República e dos "
                         "Ministérios, a legislação da Agência Nacional de Aviação Civil (Anac) e a legislação da Empresa Brasileira "
                         "de Infraestrutura Aeroportuária (Infraero); cria a Secretaria de Aviação Civil, cargos de Ministro de "
                         "Estado, cargos em comissão e cargos de Controlador de Tráfego Aéreo; autoriza a contratação de "
                         "controladores de tráfego aéreo temporários; altera as Leis nºs 11.182, de 27 de setembro de 2005, 5.862, "
                         "de 12 de dezembro de 1972, 8.399, de 7 de janeiro de 1992, 11.526, de 4 de outubro de 2007, 11.458, de 19 "
                         "de março de 2007, e 12.350, de 20 de dezembro de 2010, e a Medida Provisória nº 2.185-35, de 24 de agosto "
                         "de 2001; e revoga dispositivos da Lei nº 9.649, de 27 de maio de 1998.", "2011-08-04", "2011-08-05",
                         PAGES["l12462"]),
    "lei-10233-2001": _L("Lei nº 10.233, de 2001", "Dispõe sobre a reestruturação dos transportes aquaviário e terrestre, cria o "
                         "Conselho Nacional de Integração de Políticas de Transporte, a Agência Nacional de Transportes Terrestres, "
                         "a Agência Nacional de Transportes Aquaviários e o Departamento Nacional de Infra-Estrutura de Transportes, "
                         "e dá outras providências.", "2001-06-05", "2001-06-06", PAGES["l10233"]),
    "lei-13848-2019": _L("Lei nº 13.848, de 2019", "Dispõe sobre a gestão, a organização, o processo decisório e o controle social "
                         "das agências reguladoras [...].", "2019-06-25", "2019-06-26", PAGES["l13848"]),
    "lei-9986-2000": _L("Lei nº 9.986, de 2000", "Dispõe sobre a gestão de recursos humanos das Agências Reguladoras e dá outras "
                        "providências.", "2000-07-18", "2000-07-19", PAGES["l9986"]),
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
# Lei 7.689 art. 11 and Lei 9.249 art. 14 end '[...], com a redação dada pelo Decreto-Lei nº N, de d de m de aaaa.': words of
# the article (which wording of another act it refers to), not an amendment note; the reader takes them for a bare note.
BARE_TEXT = {"l7689": "art-11", "l9249": "art-14", "l9430": "art-88", "l9873": ("art-03", "art-08")}
BARE_TEXT_USED: list[str] = []
QUOTE_DROPPED: list[str] = []
_BARE_RX = re.compile(r"\(?\s*(reda[çc][ãa]o dada pel[oa] (?:Decreto-Lei|Lei) n[º°.]?\s*[\d.]+, de \d{1,2} de \w+ de \d{4}[.;]?)\s*\)?",
                      re.I)
_BARE_RX9873 = re.compile(r"\(?\s*(reda[çc][ãa]o dada pela Lei n[º°.]?\s*9\.457, de 1997, o art\. 28 da Lei n[º°.]?\s*8\.884, de 1994, e "
                          r"demais disposições em contrário, ainda que constantes de lei especial\.)\s*\)?")
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
    if page in BARE_TEXT:
        units = BARE_TEXT[page] if isinstance(BARE_TEXT[page], tuple) else (BARE_TEXT[page],)
        for p in out:
            if p["unit"] not in units or not p["text"].rstrip().endswith("com a"):
                continue
            hit = [(n, m) for n in p["notes"] for m in [_BARE_RX.fullmatch(n.strip())] if m]
            if not hit and page == "l9873":
                # Lei 9.873 art. 8: '[...] o art. 33 da Lei nº 6.385, de 1976, com a redação dada pela Lei nº 9.457, de 1997, o
                # art. 28 da Lei nº 8.884, de 1994, e demais disposições em contrário, ainda que constantes de lei especial.'
                hit = [(n, m) for n in p["notes"] for m in [_BARE_RX9873.fullmatch(n.strip())] if m]
            if hit:
                n, m = hit[0]
                p["text"] = p["text"].rstrip() + " " + m.group(1)
                p["notes"] = [x for x in p["notes"] if x != n]
                BARE_TEXT_USED.append(f"{page} {p['unit']}")
    if page == "l9430":
        # Lei 9.430: Planalto's markers '(Sem eficácia)' after struck lines whose change never took effect or lapsed (Medidas
        # Provisórias 252/2005, 303/2006, 478/2009) and 'Rejeitada' after Medida Provisória 75/2002's lines are not part of
        # the text; a line of the marker alone is dropped
        keep = []
        for p in out:
            t = re.sub(r"\s*(?:\(\s*Sem efic[áa]cia\s*\)|(?<![\w,])Rejeitada)\s*$", "", p["text"])
            if t != p["text"]:
                L9430_FIXED.append(p["unit"])
                p["text"] = t
                if not P.norm(t):
                    continue
            keep.append(p)
        out = keep
    if page == "l13465":
        # Lei 13.465: Planalto's link '(Partes vetadas)' (to the promulgated parts printed at the foot of the page) is not
        # text; art. 4 quotes Lei 11.952 art. 16 ('Art. 16. As condições resolutivas [...]') with no opening quotation mark,
        # which the reader takes for Lei 13.465's own art. 16: those lines belong to art. 4
        keep, seen5 = [], False
        for p in out:
            t = re.sub(r"\s*\(Partes vetadas\)\s*", " ", p["text"]).strip()
            if t != p["text"].strip():
                L13465_FIXED.append(f"{p['unit']} '(Partes vetadas)' marker left out")
                p["text"] = t
                if not t:
                    continue
            if p["unit"] == "art-05":
                seen5 = True
            if p["unit"] == "art-16" and not seen5 and not p["heading"]:
                p["unit"] = "art-04"
                if p["label"].startswith("Art"):
                    p["label"] = ""
                L13465_FIXED.append(f"quoted Lei 11.952 art. 16 line -> art-04: {P.norm(t)[:40]!r}")
            keep.append(p)
        out = keep
    if page == "l9249":
        # Lei 9.249 art. 9 caput as Medida Provisória 694/2015 worded it: the page leaves the opening quotation mark of the
        # MP's quoted text before the line ('“ Art. 9º [...]'), so the line had no label
        for p in out:
            m = re.match(r"^[\"'“”]\s*(Art\. 9º)\s", p["text"]) if p["unit"] == "art-09" else None
            if m:
                p["text"] = p["text"][m.start(1):]
                p["label"] = "Art. 9º"
                QUOTE_DROPPED.append("Lei 9.249 art. 9")
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
    if page == "l10233":
        # Lei 10.233 art. 118 § 1º: Planalto prints one struck line, the 2001 wording ('[...] conforme estabelece o art. 114.'),
        # noted 'Redação dada pela Medida Provisória nº 2.217-3, de 4.9.2001 e 246, de 4.9.2005'; the MP's art. 1 gave the
        # paragraph the wording '[...] conforme estabelece o art. 114-A.' (read on its page): the 2001 line loses the note and
        # the MP's wording follows it
        # art. 102-A (added by the same MP) is printed after an opening quotation mark copied from the MP ('"Art. 102-A.'),
        # so the reader filed it and its §§ 1º-4º under art. 102 with no label
        a102 = False
        for p in out:
            if p["unit"] == "art-102" and not p["heading"] and re.match(r'^\s*["“]\s*Art\.\s*102-A', p["text"]):
                p["text"] = re.sub(r'^\s*["“]\s*', "", p["text"])
                p["unit"], p["label"], a102 = "art-102-a", "Art. 102-A", True
                L10233_FIXED.append("art-102-a")
            elif a102 and p["unit"] == "art-102" and not p["heading"]:
                p["unit"] = "art-102-a"
            else:
                a102 = False
        keep = []
        for p in out:
            keep.append(p)
            if p["unit"] == "art-118" and p["label"] == "§ 1º" and P.norm(p["text"]).endswith("conforme estabelece o art. 114.")                     and any("2.217-3" in n for n in p["notes"]):
                q = dict(p)
                q["text"] = re.sub(r"art\.\s*114\.\s*$", "art. 114-A.", p["text"].rstrip())
                q["notes"] = ["(Redação dada pela Medida Provisória nº 2.217-3, de 4.9.2001)"] + [n for n in p["notes"]
                                                                                                if "2.217-3" not in n]
                p["notes"] = [n for n in p["notes"] if "2.217-3" not in n]
                keep.append(q)
                L10233_FIXED.append("art-118 § 1º")
        out = keep
    if page == "l12462":
        # Lei 12.462 art. 63 § 17 (Medida Provisória 1.349/2026, 'Vigência encerrada', day not read): left out
        n0 = len(out)
        out = [p for p in out if not (p["unit"] == "art-63" and P.norm(p["text"]).startswith("§ 17. O apoio financeiro "
                                                                                        "reembolsável"))]
        if len(out) != n0:
            LRDC_FIXED.append("x")
    if page == "l9873":
        # Lei 9.873: the conversion law was promulgated by the President of the Senate; its closing line 'Congresso Nacional,
        # em 23 de novembro de 1999; [...]' is not a line of art. 8
        n0 = len(out)
        out = [p for p in out if not re.match(r"Congresso Nacional, em \d", P.norm(p["text"]))]
        if len(out) != n0:
            L9873_FIXED.append("closing line 'Congresso Nacional, em 23 de novembro de 1999' left out of art. 8")
        # art. 2º-A (Lei 11.941/2009) is printed after a stray full stop ('. Art. 2º-A. Interrompe-se o prazo prescricional da
        # ação executória:'), so the reader kept it and its incisos in art. 2
        cur = None
        for p in out:
            m = re.match(r"^\.\s*Art\.\s*2º\s*-\s*A\.\s*", P.norm(p["text"])) if p["unit"] == "art-02" else None
            if m:
                p["text"] = "Art. 2º-A. " + P.norm(p["text"])[m.end():]
                p["label"], p["unit"], cur = "Art. 2º-A", "art-02-a", "art-02-a"
                L9873_FIXED.append("art. 2º-A, printed after a stray full stop ('. Art. 2º-A.'), read as its own article with "
                                   "its incisos I to V (they had been read as lines of art. 2)")
            elif cur and p["unit"] == "art-02" and not p["heading"]:
                p["unit"] = cur
            elif p["unit"] != "art-02":
                cur = None
    if page in ("l10522", "l10522-compilado"):
        # Lei 10.522 art. 37-B § 10 (Lei 11.941/2009): both Planalto pages (and Lei 11.941's own page) strike only the dash in
        # 'Custódia – SELIC'; a typesetting slip in a line in force: the line is read as unstruck, dash kept
        for p in out:
            if p["state"] == "mixed" and P.norm(p.get("struck_text", "")) in ("–", "-"):
                p.update({"state": "plain", "plain_text": "", "struck_text": ""})
                MIXED_PLAIN.append(f"{page} {p['unit']} {p['label']}")
    if page in EMPTY_ITEM_PAGES:
        # Lei 9.250 art. 4 III and VI, Lei 7.713 art. 6 XV: struck 'a) (Vide Medida nº 340, de 2006).' ... 'd)': a label
        # and a pointer, no words
        keep = []
        for p in out:
            if (not p["heading"] and p["state"] != "plain" and re.fullmatch(r"[a-z]\)\s*\.?", P.norm(p["text"]))
                    and all("Vide" in n for n in p["notes"])):
                EMPTY_ITEMS.append(f"{page} {p['unit']} {P.norm(p['text'])!r}")
                continue
            keep.append(p)
        out = keep
    if page == "l9250":
        # Lei 9.250: Lei 15.270/2025 added arts. 3º-A and 11-A, each with a table whose centred title ('Tabela de redução
        # do imposto mensal' / '... do ajuste anual') and an empty centred line come before the table rows; they are lines
        # of the article, not headings. The name lines of Capítulos II-A and III-A carry no note of their own: they come
        # with the 'CAPÍTULO II-A (Incluído pela Lei nº 15.270, de 2025)' line above them.
        cur, prev, keep = None, None, []
        for p in out:
            t = re.sub(r"(?:^|\s+)Sem efic[áa]cia\s*$", "", p["text"])
            if t != p["text"]:
                # art. 22: Planalto's marker 'Sem eficácia' after each struck line of Medida Provisória 252/2005 (lapsed)
                p["text"] = t
                L9250_FIXED.append(f"{p['unit']} marker 'Sem eficácia' left out of the text")
            if p["heading"] and not P.norm(p["text"]):
                L9250_FIXED.append("empty centred line dropped")
                continue
            if p["heading"] and cur and P.norm(p["text"]).startswith("Tabela de redução"):
                p.update({"heading": False, "unit": cur, "label": "", "center": False})
                L9250_FIXED.append(f"{P.norm(p['text'])!r} -> {cur}")
            elif (p["heading"] and not p["notes"] and prev is not None and prev["heading"]
                  and any("Incluíd" in n for n in prev["notes"]) and P.norm(prev["text"]).startswith("CAPÍTULO")):
                p["notes"] = list(prev["notes"])
                L9250_FIXED.append(f"{P.norm(p['text'])!r} dated with {P.norm(prev['text'])!r}")
            elif not p["heading"] and p["unit"].startswith("art-"):
                cur = p["unit"]
            keep.append(p)
            prev = p
        out = keep
    return out, rest


L9250_FIXED: list[str] = []
L9430_FIXED: list[str] = []
L13465_FIXED: list[str] = []
EMPTY_ITEM_PAGES = {"l9250", "l7713"}
MIXED_PLAIN: list[str] = []
L9873_FIXED: list[str] = []
LRDC_FIXED: list[str] = []
L10233_FIXED: list[str] = []
EMPTY_ITEMS: list[str] = []
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

# part g: Lei 4.728/1965 (mercado de capitais). Planalto abbreviates Decreto-Lei as 'Del' or 'Decreto' in some notes; the
# links behind them go to Del1338-74.htm, Del2287.htm and Del0911.htm. Set only when the act runs (NOTE_FIX entries are
# listed in every part's decisions).
_LMC = "lei-do-mercado-de-capitais"
if any(a["slug"] == _LMC for a in ACTS):
    for _how, _n, _d, _y in (("Redação dada", "1.338", "23.7.1974", "1974"), ("Revogado", "1.338", "23.7.1974", "1974")):
        P.NOTE_FIX[f"({_how} pelo Del {_n}, de {_d})"] = (
            f"({_how} pelo Decreto-Lei nº {_n}, de {_y})",
            f"Lei 4.728: the note reads '{_how} pelo Del {_n}, de {_d}', Planalto's abbreviation of Decreto-Lei (the link "
            f"goes to the Decreto-Lei's page)")
    P.NOTE_FIX["(Redação dada pelo Decreto nº 911, de 1º.10.1969)"] = (
        "(Redação dada pelo Decreto-Lei nº 911, de 1969)",
        "Lei 4.728: the note reads 'Decreto nº 911, de 1º.10.1969'; the link goes to Decreto-Lei 911/1969, which rewrote art. 66")
    P.NOTE_FIX["(Redação dada pelo Decreto nº 2.287, 23.7.1986)"] = (
        "(Redação dada pelo Decreto-Lei nº 2.287, de 1986)",
        "Lei 4.728: the note reads 'Decreto nº 2.287, 23.7.1986'; the link goes to Decreto-Lei 2.287/1986 (art. 24)")

P.MP_PENDING["mp-2160-2001"] = (
    "Medida Provisória nº 2.160-25, de 23.8.2001 (DOU 24.8.2001, art. 24: in force on publication), kept in force by "
    "Emenda Constitucional 32/2001, art. 2, until Lei 10.931/2004 revoked it; its art. 22 added Lei 4.728 art. 66-A. "
    "Planalto's notes name this edition only, so the change is dated by its publication; earlier editions of the chain are "
    "not modelled")
if any(a["slug"] == _LMC for a in ACTS):
    P.VIGENCIA_FIXED["dl-614-1969"] = (
        "1969-06-06", "art. 6: 'O presente Decreto-lei entrará em vigor na data de sua publicação' (DOU 6.6.1969, rectified "
                      "10.6.1969; the page writes 'Art . 6º', so the clause was not found by the reader)")
    P.VIGENCIA_FIXED["dl-911-1969"] = (
        "1969-10-03", "art. 9: 'O presente Decreto-lei entrará em vigor na data de sua publicação, aplicando-se desde logo, "
                      "aos processos em curso' (DOU 3.10.1969), as for Decreto-Lei 911 itself in this corpus")
B13.OPEN_ITEMS[_LMC] = (
    "Lei 4.728 (open items): Planalto's 'Vide' pointers (Decretos-Leis 1.089/1970, 1.338/1974, 1.401/1975, 1.980/1982, "
    "1.986/1982, 2.072/1983, 2.285/1986, 2.469/1988, Leis 5.409/1968, 6.404/1976, 14.286/2021, Medida Provisória "
    "1.184/2023) strike no words on the page and are not modelled; the 1965 text is the text as published on 16.7.1965 "
    "(rectified 16.8.1965), as Planalto prints it")
B.EXPLAINED[_LMC] = {
    "art-29": "the consolidated page runs incisos IV and V together on one line; the annotated page prints them as two",
    "art-80": "the consolidated page prints 'Cr$1.000' with no space; the annotated page prints 'Cr$ 1.000'",
}

# part h: Lei 7.689/1988 (CSLL), Lei 9.249/1995. Staggered MP days entered by hand (set only when these acts run).
_LCSLL, _L9249 = "lei-da-csll", "lei-9249-de-1995"
if any(a["slug"] in (_LCSLL, _L9249) for a in ACTS):
    P.VIGENCIA_FIXED["mp-675-2015"] = (
        "2015-09-01", "last article: 'Esta Medida Provisória entra em vigor a partir do primeiro dia do quarto mês "
                      "subsequente ao de sua publicação' (DOU 22.5.2015): 1.9.2015")
    P.VIGENCIA_FIXED["mp-1034-2021"] = (
        "2021-07-01", "art. 5: 'Esta Medida Provisória entra em vigor: I - na data de sua publicação, quanto ao art. 2º; e II "
                      "- no primeiro dia do quarto mês subsequente ao de sua publicação, quanto aos demais dispositivos' (DOU "
                      "1.3.2021): its art. 1, the change to Lei 7.689 art. 3, falls under II, 1.7.2021")
    P.VIGENCIA_FIXED["mp-694-2015"] = (
        "2016-01-01", "art. 4: 'Esta Medida Provisória entra em vigor na data de sua publicação, produzindo efeitos a "
                      "partir: I - de 1º de janeiro de 2016, em relação ao art. 1º' (DOU 30.9.2015, edição extra): its art. "
                      "1, the change to Lei 9.249 art. 9, is dated by the day it takes effect, 1.1.2016")
B13.OPEN_ITEMS[_LCSLL] = (
    "Lei 7.689 (open items): art. 8 ('A contribuição social será devida a partir do resultado apurado no período-base a ser "
    "encerrado em 31 de dezembro de 1988'), which Planalto strikes with '(Execução suspensa pela RSF nº 11, de 1995)' and "
    "'Vide ADIN nº 15-2', is left out of every version: no official copy of the Senate resolution is available to date the "
    "suspension; 'Vide' pointers (Leis 7.787/1989, 8.383/1991, 9.249/1995, Lei Complementar 224/2025, Medida Provisória "
    "1.303/2025, ADIN 5485) are not modelled; the text before 16.12.1988 (Medida Provisória 22/1988, of which this Lei is the "
    "conversion) is not part of the history")
B13.OPEN_ITEMS[_L9249] = (
    "Lei 9.249 (open items): Lei 9.430/1996's changes are dated by its in-force day (30.12.1996): its 'efeitos financeiros a "
    "partir de 1º de janeiro de 1997' are financial effects only; 'Vide' pointers (Decreto 6.306/2007, Lei 11.119/2005, "
    "Medida Provisória 1.303/2025) are not modelled")
_W9 = ("Lei 9.249 art. 9 caput and § 2º: Medida Provisória 694/2015 gave them new wordings with effect from 1.1.2016 and lapsed on "
       "8.3.2016 (Ato Declaratório nº 5/2016); Planalto prints the 1995 caput again, unstruck, below the MP's struck wording: "
       "that copy is the caput in force again from 9.3.2016, not from 1996")
B8.SPAN_FIX += [
    ((_L9249, "art-09", "Art. 9º", "Art. 9º A pessoa jurídica poderá deduzir", 2),
     {"start": "2016-03-09", "start_law": "mp-694-2015-fim", "restored": True}, _W9),
]
P.MP_LAPSE["mp-694-2015"] = (
    "2016-03-09", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 5, de 2016 (DOU 10.3.2016): 'teve seu prazo "
                  "de vigência encerrado no dia 8 de março do corrente ano'; the wording it had replaced is back from 9.3.2016")

# part i: Lei 9.250/1995 (imposto de renda das pessoas físicas). Hand days set only when the act runs.
_L9250 = "lei-9250-de-1995"
if any(a["slug"] == _L9250 for a in ACTS):
    P.VIGENCIA_FIXED["lei-12213-2010"] = (
        "2011-01-01", "art. 5: 'Esta Lei entra em vigor em 1º de janeiro do ano seguinte ao de sua publicação oficial' (DOU "
                      "21.1.2010): 1.1.2011")
    P.VIGENCIA_FIXED["lei-13498-2017"] = (
        "2018-01-01", "art. 2: 'Esta Lei entra em vigor no primeiro dia do ano seguinte ao de sua publicação' (DOU "
                      "27.10.2017): 1.1.2018")
if any(a["slug"] in (_L9250, "lei-7713-de-1988") for a in ACTS):
    P.MP_LAPSE["mp-644-2014"] = (
        "2014-08-30", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 35, de 2014 (DOU 4.9.2014): 'teve seu "
                      "prazo de vigência encerrado no dia 29 de agosto do corrente ano'; the wordings it had replaced are back "
                      "from 30.8.2014")
if any(a["slug"] == _L9250 for a in ACTS):
    P.MP_LAPSE["mp-1171-2023"] = (
        "2023-08-28", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 62, de 2023 (DOU 31.8.2023): 'teve seu "
                      "prazo de vigência encerrado no dia 27 de agosto de 2023'; the wordings it had replaced are back from "
                      "28.8.2023")
_W1171 = ("Lei 9.250 art. 4: Medida Provisória 1.171/2023 (in force 1.5.2023) revoked the parágrafo único (art. 15 II) and added "
          "§§ 1º and 2º (art. 14); it lapsed on 27.8.2023 (Ato Declaratório nº 62/2023), and Lei 14.663/2023 (DOU 28.8.2023, "
          "edição extra, in force on publication) art. 6 numbered the parágrafo único as § 1º, with new wordings of § 1º and "
          "its incisos and a § 2º, the same day the parágrafo único would have come back. So the parágrafo único and its "
          "incisos I and II (Lei 13.202/2015) end on 1.5.2023 and do not come back (Planalto leaves inciso I unstruck); the "
          "struck § 2º with no note is MP 1.171's (read on the MP's page), 1.5.2023 to the lapse")
B8.SPAN_FIX += [
    ((_L9250, "art-04", "I -", "I - do trabalho com vínculo empregatício ou de administradores", 0),
     {"end": "2023-05-01", "end_law": "mp-1171-2023", "end_how": "note", "gaps": []}, _W1171),
    ((_L9250, "art-04", "II -", "II - proventos de aposentados e pensionistas, quando a fonte pagadora for responsável pelo "
      "desconto e respectivo", 0),
     {"end": "2023-05-01", "end_law": "mp-1171-2023", "end_how": "note", "gaps": []}, _W1171),
    ((_L9250, "art-04", "§ 2º", "§ 2º Alternativamente às deduções de que trata o caput, poderá", 0),
     {"start": "2023-05-01", "start_law": "mp-1171-2023", "end": "2023-08-28", "end_law": "mp-1171-2023-fim",
      "end_how": "lapse"}, _W1171),
    ((_L9250, "art-22", "Art. 22", "Art. 22. Fica isento do imposto de renda o ganho de capital auferido na alienação de bens "
      "e direitos de pequeno valor, cujo preço unitário de alienação, no mês em que esta se realizar, seja igual ou inferior a "
      "R$ 20.000,00", 0),
     {"end": "2005-11-22", "end_law": "lei-11196-2005", "end_how": "successor", "gaps": [("2005-06-16", "2005-10-14", "mp-252-2005", "mp-252-2005-fim")]},
     "Lei 9.250 art. 22 caput: Medida Provisória 252/2005 (in force 16.6.2005) gave it a new wording and lapsed on 13.10.2005; "
     "the 1995 wording stands again from 14.10.2005 until Lei 11.196/2005 (in force 22.11.2005; its art. 38 has effects from "
     "14.10.2005, a retroactive effect: the change keeps its in-force day). Planalto prints the 1995 caput once, struck"),
    ((_L9250, "art-08", "", "9. R$ 3.375,83", 4),
     {"end": "2015-07-22", "end_law": "lei-13149-2015", "end_how": "successor"},
     "Lei 9.250 art. 8 II c) item 9: Planalto prints Medida Provisória 670/2015's wording unstruck above Lei 13.149/2015's "
     "(its conversion law, same words); MP 670's line ends on 22.7.2015"),
]
B.EXPLAINED[_L9250] = {
    "art-04": "the consolidated page prints inciso VI d) twice, in Medida Provisória 528/2011's wording (struck on the annotated "
              "page) and in Lei 12.469/2011's (same words)",
    "art-03-a": "the table title 'Tabela de redução do imposto mensal' is a centred line, which the consolidated page's reading "
                "takes for a heading; it is a line of art. 3º-A",
    "art-11-a": "the table title 'Tabela de redução do ajuste anual' is a centred line, which the consolidated page's reading "
                "takes for a heading; it is a line of art. 11-A",
    "titulos": "the two table titles of arts. 3º-A and 11-A, read as headings on the consolidated page, are lines of those "
               "articles",
}
B13.OPEN_ITEMS[_L9250] = (
    "Lei 9.250 (open items): changes whose effects reach back before their in-force day keep that day (Medida Provisória "
    "2.189-49/2001 art. 12, Medida Provisória 22/2002 and Leis 10.451/2002, 11.119/2005, 11.196/2005 art. 38, 11.311/2006, "
    "11.324/2006, 11.482/2007, 11.727/2008 art. 21, 12.469/2011 and 12.832/2013); 'Vide' pointers (Medidas Provisórias "
    "340/2006 and 1.303/2025, Leis 9.532/1997, 13.043/2014 and others) strike no words and are not modelled; earlier "
    "editions of Medida Provisória 2.189-49 are not modelled")
P.MP_PENDING["mp-2189-2001"] = (
    "Medida Provisória nº 2.189-49, de 23.8.2001 (DOU 24.8.2001; in force on publication), kept in force by Emenda "
    "Constitucional 32/2001, art. 2; its art. 11 gave Lei 9.250 arts. 10 and 25 new wordings (its art. 12 applies the art. 10 "
    "wording to taxable events from 1.1.1998, a retroactive application: the change keeps its in-force day). Planalto's notes "
    "name this edition only, so the change is dated by its publication; earlier editions of the chain are not modelled")

# part j: Lei 7.713/1988 (imposto de renda). Hand days set only when the act runs.
_L7713 = "lei-7713-de-1988"
if any(a["slug"] == _L7713 for a in ACTS):
    P.VIGENCIA_FIXED["lei-11052-2004"] = (
        "2005-01-01", "art. 2: 'Esta Lei entra em vigor em 1º de janeiro do ano subseqüente à data de sua publicação' (DOU "
                      "30.12.2004): 1.1.2005")
    P.VIGENCIA_FIXED["lei-7975-1989"] = (
        "1990-03-01", "art. 2: 'Esta Lei entra em vigor a partir do primeiro dia do terceiro mês seguinte ao de sua "
                      "publicação' (DOU 27.12.1989, the day LexML gives; the page footer prints 22.12.1989): 1.3.1990")
    P.VIGENCIA_FIXED["mp-582-2012"] = (
        "2013-01-01", "art. 20: 'Esta Medida Provisória entra em vigor: [...] II - a partir de 1º de janeiro de "
                      "2013, em relação ao art. 18' (DOU 21.9.2012): its art. 18, the change to Lei 7.713, from 1.1.2013")
    P.MP_LAPSE["mp-1251-2024"] = (
        "2024-12-06", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 125, de 2024 (DOU 11.12.2024): 'teve seu "
                      "prazo de vigência encerrado no dia 5 de dezembro de 2024'; the wordings it had replaced are back from "
                      "6.12.2024")
    P.VIGENCIA_FIXED["lei-12794-2013"] = (
        "2013-04-03", "art. 21: 'Esta Lei entra em vigor: I - a partir de 1º de janeiro de 2013, em relação aos arts. 1º a 3º, "
                      "14, 15, 17, 18 e 20 desta Lei [...]; e II - na data de sua publicação para os demais dispositivos' (DOU "
                      "3.4.2013): its art. 18 (Lei 7.713 art. 9), the conversion of Medida Provisória 582/2012 art. 18 (in "
                      "force 1.1.2013), reaches back to 1.1.2013; a retroactive start keeps the day of publication, 3.4.2013")
    P.NOTE_FIX["(Revogada pela Lei nº 7.759, de 1989)"] = (
        "(Revogada pela Lei nº 7.959, de 1989)",
        "Lei 7.713: the note reads 'Revogada pela Lei nº 7.759, de 1989'; its link goes to Lei 7.959/1989 (L7959.htm#art9), "
        "whose art. 9 made the revocation")

# part k: Lei 9.430/1996 (IN PROGRESS, not published; see batch17/PROGRESS.md 'Part k status'). Hand days read so far.
_L9430 = "lei-9430-de-1996"
if any(a["slug"] == _L9430 for a in ACTS):
    P.VIGENCIA_FIXED["lei-12382-2011"] = (
        "2011-03-01", "art. 7: 'Esta Lei entra em vigor no primeiro dia do mês subsequente à data de sua publicação' (DOU "
                      "28.2.2011): 1.3.2011")
    P.VIGENCIA_FIXED["lei-12844-2013"] = (
        "2013-07-19", "art. 49: 'Esta Lei entra em vigor: [...] V - na data de sua publicação para os demais dispositivos' "
                      "(DOU 19.7.2013, edição extra): its art. 20 (Lei 9.430 arts. 6, 73 and 74) falls under V")
    P.VIGENCIA_FIXED["mp-472-2009"] = (
        "2009-12-16", "art. 60: 'Esta Medida Provisória entra em vigor: I - na data de sua publicação, produzindo efeitos: "
                      "[...] d) a partir da data de sua publicação, em relação aos demais dispositivos' (DOU 16.12.2009): its "
                      "art. 23 (Lei 9.430 art. 44 § 5º) falls under I d)")
    P.VIGENCIA_FIXED["mp-668-2015"] = (
        "2015-01-30", "art. 3: 'Esta Medida Provisória entra em vigor: [...] II - em relação ao art. 2º e aos incisos I a IV do "
                      "caput do art. 4º, na data de sua publicação' (DOU 30.1.2015, edição extra): its art. 4 II (revocation "
                      "of Lei 9.430 art. 74 §§ 15 and 16) on publication")
    for _k, _d, _a, _end in (("mp-303-2006", "2006-10-28", "Ato do Presidente da Mesa do Congresso Nacional nº 57, de 2006 "
                              "(DOU 1.11.2006)", "27 de outubro do corrente ano"),
                             ("mp-478-2009", "2010-06-02", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº "
                              "18, de 2010 (DOU 15.6.2010)", "1º de junho do corrente ano"),
                             ("mp-822-2018", "2018-06-30", "Ato Declaratório nº 35, de 3 de julho de 2018 (DOU 4.7.2018)",
                              "29 de junho do corrente ano"),
                             ("mp-877-2019", "2019-07-24", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº "
                              "48, de 2019 (DOU 29.7.2019)", "23 de julho do corrente ano"),
                             ("mp-1262-2024", "2025-03-13", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº "
                              "10, de 2025 (DOU 14.3.2025)", "12 de março de 2025")):
        P.MP_LAPSE[_k] = (_d, f"{_a}: 'teve seu prazo de vigência encerrado no dia {_end}'; the wordings it had replaced "
                              f"are back from the next day")
    # Medida Provisória 1.227/2024 art. 5 (Lei 9.430 art. 74 § 3º XI): rejected outright and 'considerados não escritos'
    # by the President of Congress, 'encerramento da vigência e eficácia, desde a data de sua edição' (Ato Declaratório nº
    # 36, de 2024, DOU 12.6.2024): never in force. The rest of the MP lapsed on 1.10.2024 (Ato Declaratório nº 95/2024).
    P.MP_LAPSE["mp-1227-2024"] = (
        "2024-06-04", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 36, de 2024 (DOU 12.6.2024): its art. "
                      "5 (Lei 9.430 art. 74 § 3º XI) rejected outright, 'considera não escritos [...] e declara o "
                      "encerramento da vigência e eficácia, desde a data de sua edição': never in force")
    P.MP_PENDING["mp-2158-2001"] = (
        "Medida Provisória nº 2.158-35, de 24.8.2001 (DOU 27.8.2001), kept in force by Emenda Constitucional 32/2001, art. 2; "
        "its art. 92 ('entra em vigor na data de sua publicação, produzindo efeitos: I - a partir de 1º de abril de 2000 [...] "
        "IV [...]') dates only other articles, so its art. 70, the new caput of Lei 9.430 art. 63, is in force on publication. "
        "Planalto's note names this edition only; earlier editions of the chain are not modelled")
    P.NOTE_FIX["(Redação dada pela nº 12.715, de 2012)"] = (
        "(Redação dada pela Lei nº 12.715, de 2012)", "Lei 9.430: the note reads 'Redação dada pela nº 12.715, de 2012' (the "
                                                      "word 'Lei' is missing)")
    P.VIGENCIA_FIXED["lei-14596-2023"] = (
        "2024-01-01", "art. 47: 'Esta Lei entra em vigor em 1º de janeiro de 2024, exceto o art. 45, que entra em vigor na data "
                      "de sua publicação' (DOU 15.6.2023): its art. 40 (Lei 9.430 arts. 24 and 24-A) and art. 46 VI ('Ficam "
                      "revogados, a partir de 1º de janeiro de 2024 [...] arts. 18 a 23; e [...] § 2º do art. 24') from "
                      "1.1.2024; the option of art. 45 (the rules applied from 1.1.2023 to taxpayers who chose them) is a "
                      "taxpayer's choice, not a day of the law")
    _W12715 = ("Lei 12.715/2012 art. 78 § 1º: 'Os arts. 48 e 50 entram em vigor em 1º de janeiro de 2013' (DOU 18.9.2012): "
               "art. 48 (Lei 9.430 arts. 12, 18, 19 and 22) and art. 50 (arts. 18-A and 19-A); its arts. 49 and 51 (arts. 20, "
               "20-A, 20-B and 28) are in force on publication")
    _W12766 = ("Lei 12.766/2012 art. 13: 'produzindo efeitos: [...] II - a partir de 1º de janeiro de 2013, em relação aos arts. "
               "2º, 3º e 5º' (DOU 28.12.2012): its art. 5 (Lei 9.430 art. 22) from 1.1.2013")
    _W11727 = ("Lei 11.727/2008 art. 41: 'produzindo efeitos em relação: [...] VI - aos arts. 22, 23, 29 e 31, a partir do "
               "primeiro dia do ano seguinte ao da publicação desta Lei' (DOU 24.6.2008): its arts. 22 and 23 (Lei 9.430 art. 24 "
               "§ 4º, arts. 24-A and 24-B) from 1.1.2009")
    _W449 = ("Medida Provisória 449/2008 (DOU 4.12.2008, in force on publication) art. 29 gave art. 24-A's parágrafo único a new "
             "wording before the article took effect (1.1.2009, Lei 11.727 art. 41 VI): the article takes effect on 1.1.2009 "
             "with the MP's wording, and the 2008 wording of the parágrafo único never took effect")
    P.VIGENCIA_PROVISION.update({("lei-12715-2012", _L9430, u): ("2013-01-01", _W12715)
                                 for u in ("art-12", "art-18", "art-18-a", "art-19", "art-19-a", "art-22")})
    P.VIGENCIA_PROVISION[("lei-12766-2012", _L9430, "art-22")] = ("2013-01-01", _W12766)
    P.VIGENCIA_PROVISION.update({("lei-11727-2008", _L9430, u): ("2009-01-01", _W11727)
                                 for u in ("art-24", "art-24-a", "art-24-b")})
    P.VIGENCIA_PROVISION[("mp-449-2008", _L9430, "art-24-a")] = ("2009-01-01", _W449)
    _W1602 = ("Medida Provisória 1.602/1997 (DOU 17.11.1997) art. 65, the new wordings of Lei 9.430 art. 44 § 2º and art. 47, "
              "with effects from 1.1.1998 (art. 72 II: 'a partir de 1º de janeiro de 1998, em relação aos demais dispositivos'); "
              "Lei 9.532/1997 (DOU 11.12.1997), its conversion, kept them in its art. 70, also with effects from 1.1.1998 (art. "
              "81 II): the wordings apply from 1.1.1998, credited to Lei 9.532, and the MP's never took effect")
    P.VIGENCIA_PROVISION.update({(k, _L9430, u): ("1998-01-01", _W1602) for k in ("mp-1602-1997", "lei-9532-1997")
                                 for u in ("art-44", "art-47")})
    B13.OPEN_ITEMS[_L9430] = (
        "Lei 9.430 (open items): art. 87's 'efeitos financeiros a partir de 1º de janeiro de 1997' are financial effects only "
        "(the in-force day, 30.12.1996, is kept); changes whose effects reach back before their in-force day keep that day "
        "(Leis 9.959/2000, 10.637/2002 art. 49, 12.249/2010); Medida Provisória 2.158-35/2001 is dated by that edition; 'Vide' "
        "pointers (Medidas Provisórias 563/2012 on art. 22 and 1.152/2022 on arts. 18 to 24-B, Decreto 7.212/2010, Lei "
        "Complementar 214/2025 and others) strike no words and are not modelled")
    B.EXPLAINED[_L9430] = {
        "art-74": "the consolidated page prints 'Lei no 5.172' where the annotated page prints 'Lei nº 5.172' (typography)",
        "art-88": "inciso XXV ends 'com a redação dada pela Lei nº 9.065, de 20 de junho de 1995;', words of the text that the "
                  "consolidated page's reading takes for an amendment note and cuts",
        "titulos": "the consolidated page still prints the headings of arts. 18 to 22 ('Seção V', 'Preços de Transferência', "
                   "'Bens, Serviços e Direitos Adquiridos no Exterior', 'Receitas Oriundas de Exportações para o Exterior', "
                   "'Apuração dos Preços Médios', 'Juros'); the annotated page strikes them with the articles under them, "
                   "which Lei 14.596/2023 revoked",
    }
_W70 = ("Lei 9.430 art. 70 § 2º: Medida Provisória 252/2005 (DOU 16.6.2005) art. 50 gave it a new wording with effects from "
        "1.1.2006 (art. 73 IV: 'arts. 17 a 27 e 47 a 51'); the MP lapsed on 13.10.2005, so its wording never took effect, and "
        "Lei 11.196/2005 (DOU 21.11.2005) art. 73, also with effects from 1.1.2006 (art. 132 IV b: 'arts. [...] 70 a 75'), gave "
        "the paragraph its present wording: the 1996 wording stands until 1.1.2006; Planalto's second, struck copy of it "
        "(after the MP's lapse) is the same line")
_W478 = ("Lei 9.430 arts. 19-A and 19-B as Medida Provisória 478/2009 (DOU 29.12.2009, effects from 1.1.2010 for its arts. 9 and "
         "10) added them: Planalto notes them only 'Vide Medida Provisória nº 478, de 2009'; they are the MP's wordings and "
         "stand from its day until it lapsed on 1.6.2010 (Ato Declaratório nº 18/2010); art. 19-A's later wording is Lei "
         "12.715/2012's")
_R478 = {"start": "2009-12-29", "start_law": "mp-478-2009", "end": "2010-06-02", "end_law": "mp-478-2009-fim",
         "end_how": "lapse", "skip": False, "gaps": []}
B8.SPAN_FIX += [
    ((_L9430, "art-70", "§ 2º", "§ 2º O imposto deverá ser retido na data do pagamento ou crédito da multa ou vantagem e será", 0),
     {"end": "2006-01-01", "end_law": "lei-11196-2005", "end_how": "successor", "gaps": []}, _W70),
    ((_L9430, "art-70", "§ 2º", "§ 2º O imposto deverá ser retido na data do pagamento ou crédito da multa ou vantagem.", 0),
     {"skip": True, "end_how": "never-in-force"}, _W70),
    ((_L9430, "art-70", "§ 2º", "§ 2º O imposto deverá ser retido na data do pagamento ou crédito da multa ou vantagem e será", 1),
     {"skip": True, "end_how": "duplicate"}, _W70),
    ((_L9430, "art-70", "§ 2º", "§ 2º O imposto será retido", 0), {"start": "2006-01-01", "start_law": "lei-11196-2005"}, _W70),
    ((_L9430, "art-19-a", "Art. 19-A", "Art. 19-A. O Ministro de Estado da Fazenda poderá fixar margens", 0), _R478, _W478),
    ((_L9430, "art-19-b", "Art. 19-B", "Art. 19-B. A opção por um dos métodos", 0), _R478, _W478),
    ((_L9430, "art-19-b", "I -", "I - não indicar, precedentemente", 0), _R478, _W478),
    ((_L9430, "art-19-b", "II -", "II - não apresentar os documentos", 0), _R478, _W478),
    ((_L9430, "art-19-b", "III -", "III - apresentar documentos imprestáveis", 0), _R478, _W478),
    ((_L9430, "art-19-b", "§ 2º", "§ 2º A utilização do método", 0), _R478, _W478),
]
_W22 = ("Lei 9.430 art. 22: Lei 12.715/2012 art. 48 gave the caput a new wording and added § 5º, and its art. 79 I revoked § 4º, "
        "all from 1.1.2013 (art. 78 § 1º, art. 79 I); before that day Lei 12.766/2012 (DOU 28.12.2012) art. 5 gave the article "
        "its next wording with effects from 1.1.2013 and its art. 14 revoked § 5º. So Lei 12.715's caput and § 5º never took "
        "effect: the 1996 caput and § 4º stand until 1.1.2013, when Lei 12.766's wording applies")
_W63 = ("Lei 9.430 art. 63 § 3º: added by Medida Provisória 75/2002 (DOU 25.10.2002), which the Chamber rejected (in force "
        "to 18.12.2002); Planalto notes it only 'Vide Medida Provisória nº 75, de 2002', followed by 'Rejeitada'")
B8.SPAN_FIX += [
    ((_L9430, "art-22", "Art. 22", "Art. 22. Os juros pagos ou creditados a pessoa vinculada, quando decorrentes de contrato de "
      "mútuo", 0), {"skip": True, "end_how": "never-in-force"}, _W22),
    ((_L9430, "art-22", "§ 5º", "§ 5º O Ministro de Estado da Fazenda poderá reduzir", 0),
     {"skip": True, "end_how": "never-in-force"}, _W22),
    ((_L9430, "art-63", "§ 3º", "§ 3º O disposto nos §§ 1º e 2º aplica-se aos lançamentos de ofício", 0),
     {"start": "2002-10-25", "start_law": "mp-75-2002", "end": "2002-12-19", "end_law": "mp-75-2002-fim", "end_how": "lapse",
      "skip": False, "gaps": []}, _W63),
]
_W45 = ("Lei 9.430 arts. 45 and 46: Medida Provisória 303/2006 (in force 30.6.2006) revoked both; it lapsed on 27.10.2006 and they "
        "stood again from 28.10.2006 until Medida Provisória 351/2007 (22.1.2007) revoked them. Art. 45's quoted lines and "
        "incisos fall with the caput while the MP stood; Planalto prints both articles a second time (struck, 'Vide Medida "
        "Provisória nº 303, de 2006', revoked by Medida Provisória 351 and Lei 11.488), the same lines as the first copy")
_G303 = [("2006-06-30", "2006-10-28", "mp-303-2006", "mp-303-2006-fim")]
B8.SPAN_FIX += [
    ((_L9430, "art-45", "", '"Art. 80. A falta de lançamento', 0), {"gaps": _G303}, _W45),
    ((_L9430, "art-45", "I -", "I - setenta e cinco por cento do valor do imposto", 0), {"gaps": _G303}, _W45),
    ((_L9430, "art-45", "II -", "II - cento e cinqüenta por cento do valor do imposto", 0), {"gaps": _G303}, _W45),
    ((_L9430, "art-45", "", '.....', 0), {"gaps": _G303}, _W45),
    *[((_L9430, "art-45", lab, pre, 1), {"skip": True, "end_how": "duplicate"}, _W45) for lab, pre in (
        ("", '"Art. 80. A falta de lançamento'), ("I -", "I - setenta e cinco por cento do valor do imposto"),
        ("II -", "II - cento e cinqüenta por cento do valor do imposto"), ("", "....."))],
    *[((_L9430, "art-46", lab, pre, 1), {"skip": True, "end_how": "duplicate"}, _W45) for lab, pre in (
        ("§ 1º", "§ 1º As multas de que trata este artigo"), ("I -", "I - juntamente com o imposto"),
        ("II -", "II - isoladamente, nos demais casos"), ("§ 2º", "§ 2º Aplicam-se às multas"))],
    ((_L9430, "art-24-a", "Parágrafo único", "Parágrafo único. Para efeitos deste artigo, considera-se regime fiscal", 0),
     {"skip": True, "end_how": "never-in-force"},
     "Lei 9.430 art. 24-A parágrafo único: Lei 11.727/2008's wording never took effect: Medida Provisória 449/2008 (in force "
     "4.12.2008) replaced it before the article took effect on 1.1.2009 (Lei 11.727 art. 41 VI)"),
    ((_L9430, "art-09", "a)", "a) até R$ 15.000,00", 1), {"start": "2015-01-20", "start_law": "lei-13097-2015"},
     "Lei 9.430 art. 9 § 7º II a): Lei 13.097/2015's line (the conversion of Medida Provisória 656/2014's § 7º) is printed "
     "with no note of its own; it starts with Lei 13.097's other lines of § 7º (20.1.2015)"),
]
_W44 = ("Lei 9.430 art. 44 §§ 1º and 2º: Planalto prints the 1996 § 1º with its incisos I to V, and the 1997 alíneas a) to c) of § "
        "2º, a second time below Medida Provisória 303/2006's wordings (MP in force 30.6.2006, lapsed 27.10.2006): that copy is "
        "the text in force again from 28.10.2006 until Medida Provisória 351/2007 (22.1.2007); inciso V, revoked in 1998, is "
        "the same line twice")
_W18 = ("Lei 9.430 art. 18 II: Planalto prints its alíneas a) to d) (and d)'s items 1 and 2) a second time below Medida "
        "Provisória 478/2009's wording of the article ('Vide Medida Provisória nº 563, de 2012'): that copy is the text in force "
        "again from 2.6.2010, after the MP lapsed, until Lei 12.715/2012 (1.1.2013); the first copy ends with the MP")
_R303 = {"start": "2006-10-28", "start_law": "mp-303-2006-fim", "restored": True}
_R478b = {"start": "2010-06-02", "start_law": "mp-478-2009-fim", "restored": True}
B8.SPAN_FIX += [
    *[((_L9430, "art-44", lab, pre, 1), dict(_R303), _W44) for lab, pre in (
        ("I -", "I - juntamente com o tributo"), ("II -", "II - isoladamente, quando o tributo"),
        ("III -", "III - isoladamente, no caso de pessoa física"), ("IV -", "IV - isoladamente, no caso de pessoa jurídica"))],
    ((_L9430, "art-44", "V -", "V - isoladamente, no caso de tributo", 1), {"skip": True, "end_how": "duplicate"}, _W44),
    *[((_L9430, unit, lab, pre, 0), {"skip": True, "end_how": "never-in-force"},
       "Lei 9.430 art. 44 § 2º and art. 47: Medida Provisória 1.602/1997's wordings (effects from 1.1.1998) never took effect: "
       "Lei 9.532/1997, its conversion (11.12.1997), gave the same words before that day, also with effects from 1.1.1998")
      for unit, lab, pre in (("art-44", "§ 2º", "§ 2º As multas a que se referem os incisos I e II do caput passarão"),
                             ("art-44", "a)", "a) prestar esclarecimentos"), ("art-44", "b)", "b) apresentar os arquivos"),
                             ("art-44", "c)", "c) apresentar a documentação técnica"),
                             ("art-47", "Art. 47", "Art. 47. A pessoa física ou jurídica submetida a ação fiscal por parte da "
                              "Secretaria da Receita Federal poderá pagar, até o vigésimo dia subseqüente à data de recebimento "
                              "do termo de início de fiscalização, os tributos e contribuições já declarados"))],
    *[((_L9430, "art-44", lab, pre, 2), dict(_R303), _W44) for lab, pre in (
        ("a)", "a) prestar esclarecimentos"), ("b)", "b) apresentar os arquivos"), ("c)", "c) apresentar a documentação técnica"))],
    *[((_L9430, "art-18", "", pre, 1), {"end": "2009-12-29", "end_law": "mp-478-2009", "end_how": "parent"}, _W18)
      for pre in ("1. sessenta por cento", "2. vinte por cento")],
    *[((_L9430, "art-18", lab, pre, n), dict(_R478b), _W18) for lab, pre, n in (
        ("a)", "a) dos descontos incondicionais", 1), ("b)", "b) dos impostos e contribuições incidentes", 1),
        ("c)", "c) das comissões e corretagens", 1), ("d)", "d) da margem de lucro de:", 2),
        ("", "1. sessenta por cento", 2), ("", "2. vinte por cento", 2))],
]
# part l: Lei 13.465/2017. Parts vetoed on 11.7.2017 that Congress kept were promulgated by the President on 6.9.2017 (DOU
# 8.9.2017; the promulgation is printed at the foot of the page): in art. 3 the new wording of Lei 13.001 art. 3 caput, art.
# 3-A (an article of Lei 13.465), and in art. 4 Lei 11.952 art. 16 § 2º. They start on 8.9.2017, credited to Lei 13.465.
_LREURB = "lei-da-regularizacao-fundiaria"
_WPROM = ("Lei 13.465: parts vetoed on 11.7.2017 and kept by Congress were promulgated by the President on 6.9.2017 ('Faço saber "
          "que o Congresso Nacional decreta e eu promulgo, nos termos do parágrafo 5º do art. 66 da Constituição Federal, as "
          "seguintes partes vetadas da Lei nº 13.465'; DOU 8.9.2017, printed at the foot of Planalto's page): in art. 3 the "
          "quoted new caput of Lei 13.001 art. 3 ('Ficam remitidos [...] R$ 10.000,00') and its closing line, art. 3-A (an "
          "article of Lei 13.465: caput and incisos I to IV) and in art. 4 the quoted Lei 11.952 art. 16 § 2º; they start on "
          "8.9.2017, credited to Lei 13.465, and are absent before (the page prints no '(VETADO)' line for them)")
_P13465 = {"start": "2017-09-08", "start_law": "lei-13465-2017"}
B8.SPAN_FIX += [
    *[((_LREURB, unit, lab, pre, n), dict(_P13465), _WPROM) for unit, lab, pre, n in (
        ("art-03", "", '" Art. 3º Ficam remitidos', 0), ("art-03", "", ".....", 0),
        ("art-03-a", "Art. 3º-A", "Art. 3º-A O financiamento", 0),
        ("art-03-a", "I -", "I - o limite de crédito será de até R$ 140.000,00", 0),
        ("art-03-a", "II -", "II - o prazo de financiamento", 0), ("art-03-a", "III -", "III - o tomador do crédito", 0),
        ("art-03-a", "IV -", "IV - os valores limites estabelecidos", 0),
        ("art-04", "§ 2º", "§ 2º Caso a análise de que trata o § 1º", 0))],
    *[((_LREURB, "art-33", lab, pre, 2), {"start": "2021-01-13", "start_law": "lei-14118-2021"},
       "Lei 13.465 art. 33: Medida Provisória 996/2020 (26.8.2020) revoked the parágrafo único and added § 1º with the same "
       "incisos II and III; Lei 14.118/2021 (13.1.2021), its conversion, kept § 1º as the former parágrafo único (its art. 26 "
       "II: '§ 1º (antigo parágrafo único)'). Planalto prints II and III three times: struck with the 2017 parágrafo único, "
       "struck as the MP's, and unstruck with no note under Lei 14.118's § 1º: the last copy starts with Lei 14.118")
      for lab, pre in (("II -", "II - na Reurb-E, a regularização fundiária será contratada"),
                       ("III -", "III - na Reurb-E sobre áreas públicas, se houver interesse público"))],
]
B.EXPLAINED[_LREURB] = {u: "check artefact: the article quotes another law with dotted lines ('§ 1º .....'), which the history "
                           "keeps as a label-only line and the check, reading label-only lines as revoked dispositivos, drops"
                        for u in ("art-02", "art-03", "art-06", "art-92")}
B13.OPEN_ITEMS[_LREURB] = (
    "Lei 13.465 (open items): the text before 12.7.2017 (Medida Provisória 759/2016, of which this Lei is the conversion) is "
    "not part of the history; the rectification published on 6.9.2017 and the consolidated text republished on 8.9.2017 are "
    "read as Planalto prints the Lei (words as corrected); Planalto has no consolidated page for this Lei, so the check "
    "compares the annotated page's present text with itself")
# part m: Lei 11.977/2009 (Minha Casa, Minha Vida). Hand days set only when the act runs.
_LMCMV = "lei-minha-casa-minha-vida"
if any(a["slug"] == _LMCMV for a in ACTS):
    P.VIGENCIA_FIXED["mp-472-2009"] = (
        "2009-12-16", "art. 60: 'Esta Medida Provisória entra em vigor: I - na data de sua publicação, produzindo efeitos: "
                      "[...] d) a partir da data de sua publicação, em relação aos demais dispositivos' (DOU 16.12.2009): its "
                      "art. 46 (Lei 11.977 arts. 6, 11, 13, 20 and 30) falls under I d)")
    P.VIGENCIA_FIXED["lei-13161-2015"] = (
        "2015-08-31", "art. 7: 'Esta Lei entra em vigor: I - a partir do primeiro dia do quarto mês subsequente ao de sua "
                      "publicação quanto aos arts. 1º e 2º; II - na data de sua publicação, quanto aos demais dispositivos' "
                      "(DOU 31.8.2015): its art. 4 (Lei 11.977 art. 6º-A) falls under II")
    P.MP_LAPSE["mp-478-2009"] = (
        "2010-06-02", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 18, de 2010 (DOU 15.6.2010): 'teve seu "
                      "prazo de vigência encerrado no dia 1º de junho do corrente ano'; the wordings it had replaced are back "
                      "from 2.6.2010")
    P.MP_PENDING["mp-1382-2026"] = (
        "published 1.8.2026 (DOU), in force on publication (art. 10); on the retrieval day (31.10.2026) it was neither "
        "converted nor lapsed (CF art. 62 § 3: 60 days, extendable once by 60, the count suspended in the July recess), so its "
        "wordings and revocations of Lei 11.977 (art. 6: arts. 8º-A, 20 and 24; art. 9 I: art. 20 I to IV and §§ 1º and 1º-A, "
        "arts. 21, 27, 27-A, 28, 30 and 30-A) stand open")
    P.MP_PENDING["mp-1350-2026"] = (
        "published 15.4.2026 (DOU), in force on publication; its art. 1 gave Lei 11.977 art. 20 IV a new wording. Medida "
        "Provisória 1.382/2026 (1.8.2026, pending) revoked art. 20 IV (art. 9 I a) 1) and revoked Medida Provisória 1.350 "
        "itself (art. 9 II) before its term ran out, so the wording stands from 15.4.2026 to 1.8.2026 and its later fate "
        "changes no words of Lei 11.977")
    for _n in ("Redação dada", "Incluído"):
        P.NOTE_FIX[f"({_n} pela Mediada Provisória nº 561, de 2012)"] = (
            f"({_n} pela Medida Provisória nº 561, de 2012)",
            f"Lei 11.977: notes read '{_n} pela Mediada Provisória nº 561, de 2012'; their links go to Medida Provisória "
            f"561/2012 (_Ato2011-2014/2012/Mpv/561.htm)")

# Lei 11.977 Capítulo III (arts. 46 to 71-A, regularização fundiária) was revoked whole by Medida Provisória 759/2016 (art.
# 75 VI, DOU 23.12.2016) and again by Lei 13.465/2017 (art. 109 IV), its conversion. Planalto adds both revocation notes to
# every struck line of the chapter, also to wordings that Medidas Provisórias 514/2010 and Lei 12.424/2011 had already
# replaced: those end with the next wording of the same dispositivo, not on 23.12.2016.
_W_CH3 = ("Lei 11.977 Capítulo III (arts. 46 to 71-A): Medida Provisória 759/2016 (DOU 23.12.2016, art. 75 VI) and Lei "
          "13.465/2017 (art. 109 IV) revoked the whole chapter; Planalto prints both revocation notes after every struck line "
          "of the chapter, also after wordings that Medida Provisória 514/2010 (2.12.2010) or Lei 12.424/2011 (17.6.2011) had "
          "already replaced: each of those ends with the next wording of the same dispositivo, and only the wordings in force "
          "on 22.12.2016 end on 23.12.2016. Lei 12.424/2011 (17.6.2011), the conversion of Medida Provisória 514/2010, "
          "restated arts. 47 IX, 56 § 2º I to III (its § 5º taking the place of the MP's §§ 5º and 6º), 59, 60-A and 71-A, "
          "so the MP's wordings of those, and the 2009 lines of art. 59, end on 17.6.2011; art. 60 § 1º I and § 2º, which "
          "Lei 12.424 left as dotted lines, keep the MP's wording, as Planalto prints them, until 23.12.2016")
CH3_REVOKERS = {"mp-759-2016", "lei-13465-2017"}
CH3_USED: list[str] = []


def ch3_successors(paras, act):
    if act["slug"] != _LMCMV:
        return
    for i, p in enumerate(paras):
        if p.get("pinned") or p["state"] == "plain" or p.get("end_how") != "note" or p.get("end_law") not in CH3_REVOKERS:
            continue
        j = P.successor(paras, i)
        if j is not None and paras[j]["start"] < p["end"]:
            q = paras[j]
            p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "successor"
            CH3_USED.append(f"{p['unit']} {p['label'] or '(line)'} {p['start']}")
    # Lei 12.424/2011 (17.6.2011), the conversion of Medida Provisória 514/2010, restated arts. 47 IX, 56 (§ 2º I-III; its
    # § 5º replaced the MP's §§ 5º and 6º), 59 (whole), 60-A and 71-A: the MP's wordings, and the 2009 lines of art. 59,
    # end that day. Art. 60 § 1º I and § 2º, which Lei 12.424 left as dotted lines, keep MP 514's wording until 2016.
    # Lines noted only 'Revogado pela Lei nº 13.465' end with the chapter, on 23.12.2016.
    for p in paras:
        m = re.match(r"art-(\d+)", p["unit"])
        if not m or not 46 <= int(m.group(1)) <= 71 or p.get("pinned") or p["heading"]:
            continue
        if p.get("end_law") == "lei-13465-2017" and p["end"] > "2016-12-23":
            p["end"], p["end_law"], p["end_how"] = "2016-12-23", "mp-759-2016", "note"
            CH3_USED.append(f"{p['unit']} {p['label'] or '(line)'} {p['start']} (chapter)")
        kept = (p["start_law"] == "mp-514-2010" and p["unit"] != "art-60") or (
            p["unit"] == "art-59" and p["start_law"] is None and p["label"] in ("Parágrafo único", "I -", "II -"))
        if kept and p["state"] != "plain" and (p["end"] or "9999") > "2011-06-17":
            p["end"], p["end_law"], p["end_how"] = "2011-06-17", "lei-12424-2011", "conversion"
            CH3_USED.append(f"{p['unit']} {p['label'] or '(line)'} {p['start']} (Lei 12.424)")
    # lines that fall with their parent follow the parent's corrected end
    for i, p in enumerate(paras):
        if p.get("pinned") or p.get("end_how") != "parent" or p["heading"]:
            continue
        lv = P.level(p["label"])
        for q in reversed(paras[:i]):
            if q["unit"] != p["unit"]:
                break
            if P.level(q["label"]) < lv and not q["heading"]:
                if q["state"] != "plain" and q["end"] and p["start"] < q["end"] < p["end"]:
                    p["end"], p["end_law"] = q["end"], q["end_law"]
                    CH3_USED.append(f"{p['unit']} {p['label'] or '(line)'} {p['start']} (parent)")
                break


_W79 = ("Lei 11.977 art. 79: Medida Provisória 478/2009 (29.12.2009) rewrote the article; it lapsed on 1.6.2010 (Ato "
        "Declaratório nº 18/2010) and the 2009 article (the new wording of Medida Provisória 2.197-43 art. 2) was in force "
        "again from 2.6.2010 until Medida Provisória 514/2010 (2.12.2010). Planalto prints the 2009 article a second time "
        "below the MP's lines (struck, no note): that copy starts on 2.6.2010; art. 11's parágrafo único likewise (MP 478 "
        "had made it § 1º and added § 2º)")
_R478m = {"start": "2010-06-02", "start_law": "mp-478-2009-fim", "restored": True}
B8.SPAN_FIX += [
    *[((_LMCMV, "art-79", lab, pre, n), dict(_R478m), _W79) for lab, pre, n in (
        ("", '"Art. 2º Os agentes financeiros do SFH', 1), ("§ 1º", "§ 1º Para o cumprimento do disposto no caput", 2),
        ("I -", "I - disponibilizar, na qualidade de estipulante e beneficiário, uma quantidade", 2),
        ("II -", "II - aceitar apólices individuais", 2), ("§ 2º", "§ 2º Sem prejuízo da regulamentação", 2))],
    ((_LMCMV, "art-11", "Parágrafo único", "Parágrafo único. A assistência técnica deve fazer parte", 1), dict(_R478m), _W79),
    ((_LMCMV, "art-13", "I -", "I - facilitar a produção do imóvel residencial", 1),
     {"start": "2010-06-14", "start_law": "lei-12249-2010", "end": "2010-12-02", "end_law": "mp-514-2010",
      "end_how": "successor", "skip": False},
     "Lei 11.977 art. 13 I: Lei 12.249/2010 (14.6.2010), the conversion of Medida Provisória 472/2009, kept the MP's wording "
     "('facilitar a produção do imóvel residencial'); Planalto prints that line, noted 'Redação dada pela Lei nº 12.249, de "
     "2010', after Medida Provisória 514/2010's line: it stands from 14.6.2010 until MP 514 (2.12.2010)"),
    ((_LMCMV, "art-04", "II -", "II - (VETADO)", 0), {"skip": True, "end_how": "duplicate"},
     "Lei 11.977 art. 4 § 1º II: '(VETADO)' is printed twice, struck with the 2009 § 1º and unstruck under the present § 1º; "
     "the inciso was vetoed in 2009 and never had words: one line, from 8.7.2009"),
    ((_LMCMV, "art-59", "III -", "III - (revogado)", 0), {"start": "2011-06-17", "start_law": "lei-12424-2011"},
     "Lei 11.977 art. 59 § 1º III: the placeholder '(revogado)' (no note) stands for the revocation by Lei 12.424/2011 "
     "(17.6.2011); it starts that day"),
    ((_LMCMV, "art-63", "Art. 63", "Art. 63. (VETADO)", 0),
     {"end": "2016-12-23", "end_law": "mp-759-2016", "end_how": "note", "skip": False}, _W_CH3),
]
for _lab, _rest in (("§ 1º", "A demarcação urbanística e a legitimação"), ("§ 2º", "Sem prejuízo de outros meios de prova")):
    B15.TEXT_FIX.append(("l11977", f"{_lab} {_lab} {_rest}", f"{_lab} {_rest}",
                         f"Lei 11.977 art. 47 {_lab} in Lei 12.424/2011's wording: the annotated page prints the label twice "
                         f"('{_lab} {_lab} {_rest[:20]}...'); Lei 12.424 art. 47 prints it once"))
_W2011 = ("Lei 11.977 arts. 5, 12, 18 (caput and § 2º) and 19 (caput): Medida Provisória 514/2010 art. 9 IV and Lei 12.424/2011 "
          "art. 13 III, its conversion, revoke them 'a partir de 31 de dezembro de 2011'; they end on 31.12.2011, credited to "
          "Lei 12.424 (Planalto notes only 'Revogado pela Lei nº 12.424, de 2011', which would date them 17.6.2011). Art. 12's "
          "parágrafo único falls with the article, although both Planalto pages print it unstruck")
_E2011 = {"end": "2011-12-31", "end_law": "lei-12424-2011", "end_how": "note", "skip": False}
B8.SPAN_FIX += [((_LMCMV, unit, lab, pre, n), dict(_E2011), _W2011) for unit, lab, pre, n in (
    ("art-05", "Art. 5º", "Art. 5º Fica a União autorizada", 0),
    ("art-05", "Parágrafo único", "Parágrafo único. Enquanto não efetivado", 0),
    ("art-12", "Art. 12", "Art", 0), ("art-12", "Parágrafo único", "Parágrafo único. Enquanto não efetivado", 0),
    ("art-18", "Art. 18", "Art. 18. Fica a União autorizada a transferir recursos para o Fundo de Arrendamento Residencial - "
     "FAR, até o limite de R$ 16.500", 1),
    ("art-18", "§ 2º", "§ 2º Enquanto não efetivado", 0),
    ("art-19", "Art. 19", "Art. 19. Fica a União autorizada", 0))]
_W41 = ("Lei 11.977 art. 41: Medida Provisória 656/2014 art. 16 (DOU 8.10.2014) gave it a new wording and added its parágrafo "
        "único, in force 'trinta dias após a sua publicação em relação aos arts. 9º a 17' (art. 55 II): from 7.11.2014; Lei "
        "13.097/2015 art. 60 (DOU 20.1.2015), its conversion, likewise 30 days after publication for arts. 54 to 62 (art. 168 "
        "II): from 19.2.2015 (LC 95/1998 art. 8 § 1)")
if any(a["slug"] == _LMCMV for a in ACTS):
    P.VIGENCIA_PROVISION[("mp-656-2014", _LMCMV, "art-41")] = ("2014-11-07", _W41)
    P.VIGENCIA_PROVISION[("lei-13097-2015", _LMCMV, "art-41")] = ("2015-02-19", _W41)
B8.SPAN_FIX.append(((_LMCMV, "art-41", "Parágrafo único", "Parágrafo único. O descumprimento do disposto no caput", 0),
                    {"end": "2015-02-19", "end_law": "lei-13097-2015", "end_how": "successor"}, _W41))
B13.OPEN_ITEMS[_LMCMV] = (
    "Lei 11.977 (open items): the text before 8.7.2009 (Medida Provisória 459/2009, of which this Lei is the conversion) is "
    "not part of the history; Medida Provisória 1.382/2026 was pending on the retrieval day: if it lapses, the wordings it "
    "replaced or revoked (and Medida Provisória 1.350/2026, which it revoked) come back, which the history does not show yet; "
    "Lei 12.249/2010's effects reaching back to 16.12.2009 keep its in-force day; 'Vide' pointers (Medidas Provisórias "
    "514/2010 and 1.382/2026 on art. 8º-A § 4º's term, Leis 12.424/2011 and 14.620/2023, decrees) strike no words and are "
    "not modelled")
B8.SPAN_FIX.append((("lei-do-prouni", "art-02", "§ 1º", "§ 1º", 0), {"skip": True, "end_how": "pointer"},
                    "Lei 11.096 art. 2: Planalto prints a struck line holding only the label '§ 1º' and the note '(Vide "
                    "Medida Provisória nº 1.075, de 2021)' among the 2005 lines; the 2005 article had a parágrafo único, no § 1º; "
                    "the line is a pointer, not a wording, and is left out (§ 1º starts with Lei 14.350/2022)"))
_WPU = ("Lei 11.096 arts. 2 and 7: Lei 14.350/2022 art. 6 (DOU 26.5.2022, in force on publication): 'produzirá efeitos: I - a "
        "partir de 1º de julho de 2022, quanto à parte do art. 1º que altera [...] a) o inciso I do caput e o § 1º do art. 2º; e "
        "b) o inciso II do caput e os §§ 1º, 1º-A e 2º do art. 7º': those wordings (with their alíneas and incisos) start, and "
        "the wordings they replace end, on 1.7.2022; its other changes on 26.5.2022. Medida Provisória 1.075/2021 had the same "
        "clause (art. 5 I); Planalto prints none of its wordings of those dispositivos (only 'Vide' notes)")
_S1 = {"start": "2022-07-01", "start_law": "lei-14350-2022"}
_E1 = {"end": "2022-07-01", "end_law": "lei-14350-2022", "end_how": "successor"}
B8.SPAN_FIX += [(("lei-do-prouni", u, lab, pre, 0), dict(f), _WPU) for u, lab, pre, f in (
    ("art-02", "I -", "I - a estudante que tenha cursado o ensino médio completo", _E1),
    ("art-02", "I -", "I - a estudante que tenha cursado:", _S1),
    *[("art-02", x + ")", x + ") o ensino médio", _S1) for x in "abcde"],
    ("art-02", "§ 1º", "§ 1º A sequência de classificação", _S1),
    ("art-02", "I -", "I - professor da rede pública", _S1),
    ("art-02", "II -", "II - estudante que tenha cursado", _S1),
    ("art-02", "III -", "III - estudante que tenha cursado", _S1),
    ("art-02", "IV -", "IV - estudante que tenha cursado", _S1),
    ("art-02", "V -", "V - estudante que tenha cursado", _S1),
    ("art-02", "VI -", "VI - estudante que tenha cursado", _S1),
    ("art-07", "II -", "II - percentual de bolsas de estudo destinado à implementação de políticas afirmativas de acesso ao "
                       "ensino superior de portadores", _E1),
    ("art-07", "II -", "II - percentual de bolsas de estudo destinado à implementação de políticas afirmativas de acesso ao "
                       "ensino superior de:", _S1),
    ("art-07", "a)", "a) pessoas com deficiência", _S1), ("art-07", "b)", "b) autodeclarados", _S1),
    ("art-07", "c)", "c) estudantes egressos", _S1),
    ("art-07", "§ 1º", "§ 1º O percentual de que trata o inciso II do caput deste artigo deverá ser", _E1),
    ("art-07", "§ 1º", "§ 1º O percentual de que trata o inciso II do caput deste artigo será", _S1),
    ("art-07", "§ 1º-A", "§ 1º-A Para o percentual", _S1),
    ("art-07", "§ 2º", "§ 2º No caso de não-preenchimento", _E1),
    ("art-07", "§ 2º", "§ 2º Na hipótese de não preenchimento", _S1),
    ("art-07", "I -", "I - estudantes que atendam", _S1), ("art-07", "II -", "II - candidatos aos cursos", _S1))]
B.EXPLAINED[_LMCMV] = {
    "titulos": "the consolidated page still prints the heading 'CAPÍTULO III' of the chapter Medida Provisória 759/2016 and "
               "Lei 13.465/2017 revoked; the annotated page strikes it with the chapter",
    "art-12": "the consolidated page prints art. 12's parágrafo único under 'Art. 12 (Revogado pela Lei nº 12.424, de 2011)'; "
              "Lei 12.424 art. 13 III revokes the whole article ('os arts. 5º e 12') from 31.12.2011, so the history ends it then",
}

# part q: Lei 10.522/2002 (Cadin). Hand days set only when the act runs.
_LCADIN = "lei-do-cadin"
if any(a["slug"] == _LCADIN for a in ACTS):
    P.VIGENCIA_FIXED["lei-12844-2013"] = (
        "2013-07-19", "art. 49: 'Esta Lei entra em vigor: [...] V - na data de sua publicação para os demais dispositivos' "
                      "(DOU 19.7.2013, edição extra): its art. 21 (Lei 10.522 art. 19) falls under V")
_LCSE, _L9074 = "lei-das-concessoes-do-setor-eletrico", "lei-9074-de-1995"
if any(a["slug"] == _L9074 for a in ACTS):
    P.VIGENCIA_FIXED["mp-1300-2025"] = (
        "2025-05-21", "'Esta Medida Provisória entra em vigor: I - quarenta e cinco dias [...] quanto ao art. 6º; II - em 1º de "
                      "janeiro de 2026, quanto ao art. 8º; e III - na data de sua publicação, quanto aos demais dispositivos' (DOU "
                      "21.5.2025, edição extra): its art. 1 (Lei 9.074) falls under III")
    P.VIGENCIA_FIXED["lei-15235-2025"] = (
        "2025-10-09", "'Esta Lei entra em vigor: I - em 1º de janeiro de 2026, quanto ao inciso III do caput do art. 5º; e II - "
                      "na data de sua publicação, quanto aos demais dispositivos' (DOU 9.10.2025): the conversion of Medida "
                      "Provisória 1.300/2025, which does not keep the MP's art. 1 (its changes to Lei 9.074), takes effect on "
                      "publication, so those changes end on 9.10.2025 and the wordings they replaced are back")
if any(a["slug"] in (_LCSE, _L9074) for a in ACTS):
    P.VIGENCIA_FIXED["mp-612-2013"] = (
        "2013-04-04", "art. 28: 'Esta Medida Provisória entra em vigor: [...] III - na data de sua publicação para os demais "
                      "dispositivos, produzindo efeitos quanto ao art. 22 a partir da entrada em vigor da Lei nº 12.783' (DOU "
                      "4.4.2013): its arts. 21 and 22 (Lei 12.783) fall under III; art. 22's effects reach back to 14.1.2013, so "
                      "the in-force day is kept" if not any(a["slug"] == _L9074 for a in ACTS) else
                      "4.4.2013): its art. 29 (the revocation of Lei 9.074 art. 1 VI, 'na data de publicação desta Medida "
                      "Provisória') falls under III")
    P.MP_LAPSE["mp-612-2013"] = (
        "2013-08-02", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 49, de 2013 (DOU 7.8.2013): 'teve seu "
                      "prazo de vigência encerrado no dia 1º de agosto do corrente ano'")
if any(a["slug"] == _LCSE for a in ACTS):
    P.VIGENCIA_FIXED["lei-12844-2013"] = (
        "2013-07-19", "art. 49: 'Esta Lei entra em vigor: [...] V - na data de sua publicação para os demais dispositivos, "
                      "produzindo efeitos quanto ao art. 27 a partir da entrada em vigor da Lei nº 12.783, de 11 de janeiro de "
                      "2013' (DOU 19.7.2013, edição extra): its arts. 26 and 27 (Lei 12.783 arts. 8, 15 and 26-A) fall under V; "
                      "art. 27's effects reach back to 14.1.2013, so the in-force day is kept")
    P.MP_LAPSE["mp-1232-2024"] = (
        "2024-10-11", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 101, de 2024 (DOU 31.10.2024): 'teve "
                      "seu prazo de vigência encerrado no dia 10 de outubro de 2024'; the wordings it replaced or revoked are "
                      "back from 11.10.2024")
    P.VIGENCIA_FIXED["lei-13988-2020"] = (
        "2020-04-14", "'Esta Lei entra em vigor: I - em 120 (cento e vinte) dias [...] em relação ao inciso I do caput e ao "
                      "parágrafo único do art. 23; e II - na data de sua publicação, em relação aos demais dispositivos' (DOU "
                      "14.4.2020, edição extra): its art. 28 (Lei 10.522 art. 19-E) falls under II")
    P.MP_LAPSE["mp-1160-2023"] = (
        "2023-06-02", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 41, de 2023 (DOU 16.6.2023): 'teve seu "
                      "prazo de vigência encerrado no dia 1º de junho de 2023'; the provision it had revoked is back from "
                      "2.6.2023")
for _w, _r in (("Lei no 8.981", "Lei nº 8.981"), ("Decreto no 70.235", "Decreto nº 70.235"), ("Lei no 10.480", "Lei nº 10.480"),
               ("Lei no 11.457", "Lei nº 11.457")):
    B15.TEXT_FIX.append(("l10522", _w, _r, "Lei 10.522 arts. 17, 32 and 37-B: the annotated page prints the ordinal sign of "
                         "'nº' as a plain 'o' ('Lei no 8.981') where the consolidated page prints 'nº'"))
B15.TEXT_FIX.append(("l10522", "a critério exclusivo da autoridade fazendária$", "a critério exclusivo da autoridade fazendária:",
                     "Lei 10.522 art. 20-D caput: the annotated page drops the closing colon before incisos I-III, which Lei "
                     "13.606's own text and the consolidated page print"))
B.EXPLAINED[_LCADIN] = {
    "art-20-b": "the annotated page ends the caput with a full stop ('nela indicados.'); the consolidated page and Lei 13.606's "
                "own page print none; the annotated page's text is kept",
}
_W20D = ("Lei 10.522 art. 20-D: added by Lei 13.606/2018 (art. 25, DOU 10.1.2018) but vetoed ('Art. 20-D. (VETADO).'); "
         "Congress overrode the veto and the article was promulgated on 17.4.2018 (DOU 18.4.2018, printed on Lei 13.606's "
         "page, as for Lei 8.212 art. 25 § 12 in 99-batch15a). The '(VETADO)' line (the page prints it struck and without "
         "its closing parenthesis) stands from 10.1.2018 to 18.4.2018, the promulgated caput and incisos I-III from "
         "18.4.2018, credited to Lei 13.606")
_P20D = {"start": "2018-04-18", "start_law": "lei-13606-2018", "promulgated": True}
B8.SPAN_FIX += [
    ((_LCADIN, "art-20-d", "Art. 20-D", "Art. 20-D. (VETADO", 0),
     {"text": "Art. 20-D. (VETADO).", "skip": False, "start": "2018-01-10", "start_law": "lei-13606-2018",
      "end": "2018-04-18", "end_law": "lei-13606-2018", "end_how": "promulgation"}, _W20D),
    ((_LCADIN, "art-20-d", "Art. 20-D", "Art. 20-D. Sem prejuízo", 0), dict(_P20D), _W20D),
    ((_LCADIN, "art-20-d", "I -", "I - notificar as pessoas", 0), dict(_P20D), _W20D),
    ((_LCADIN, "art-20-d", "II -", "II - requisitar informações", 0), dict(_P20D), _W20D),
    ((_LCADIN, "art-20-d", "III -", "III - instaurar procedimento", 0), dict(_P20D), _W20D),
    ((_LCADIN, "art-10", "Art. 10", "Art. 10.", 1), {"skip": True, "end_how": "pointer"},
     "Lei 10.522 art. 10: Planalto prints a struck line holding only 'Art. 10.' and the note '(Vide Mpv nº 75, de 2002)' (a "
     "Medida Provisória the Chamber rejected); it is a pointer, not a wording, and is left out"),
    ((_LCADIN, "art-13-a", "Art. 13-A", "Art. 13-A -", 0), {"skip": True, "end_how": "pointer"},
     "Lei 10.522 art. 13-A: Planalto prints a struck line holding only 'Art. 13-A -' and the note '(Vide Medida Provisória nº "
     "249, de 2005)'; it is a pointer, not a wording, and is left out (art. 13-A starts with Lei 11.345/2006, 15.9.2006)"),
]
_W11 = ("Lei 10.522 art. 11 §§ 1º to 3º: Medida Provisória 449/2008 (4.12.2008) rewrote art. 11 (a caput with incisos I and "
        "II, new §§ 1º to 3º, §§ 4º to 9º revoked); Lei 11.941/2009, its conversion (28.5.2009), gave a new wording only to the "
        "caput and kept the revocations, so MP 449's incisos and §§ 1º to 3º end on 28.5.2009 and the 2002 §§ 1º to 3º are "
        "in force again from that day: Planalto prints them a second time, unstruck and without notes, below Lei 11.941's "
        "caput (they had been read as in force from 2002 next to their struck copies)")
_R11 = {"start": "2009-05-28", "start_law": "lei-11941-2009", "restored": True}
B8.SPAN_FIX += [((_LCADIN, "art-11", lab, pre, 1), dict(_R11), _W11) for lab, pre in (
    ("§ 1º", "§ 1º Observados os limites"), ("§ 2º", "§ 2º Enquanto não deferido"), ("§ 3º", "§ 3º O não-cumprimento"))]
# part r: Lei 9.873/1999, Lei 10.520/2002 (pregão; repealed as a whole on 30.12.2023, read from a capture of 10.12.2023)
_LPREG = "lei-do-pregao"
B9.REPEALS[_LPREG] = (
    "2023-12-30", "lei-14133-2021",
    "Lei 10.520/2002 was repealed as a whole by Lei 14.133/2021 art. 193 II, in the wording Lei Complementar 198/2023 gave it "
    "('Revogam-se: [...] II - em 30 de dezembro de 2023: [...] b) a Lei nº 10.520, de 17 de julho de 2002'; the first "
    "wording set two years from 1.4.2021, Medida Provisória 1.167/2023 and then LC 198/2023 moved it), so its last version, "
    "on 30.12.2023, removes every provision, credited to Lei 14.133/2021. After the repeal Planalto strikes the whole page, "
    "so the page is read from a capture of 10.12.2023, before the repeal, and the history up to 29.12.2023 is checked "
    "against that capture's text")

_DOTTED = ("check artefact: the article quotes another law with dotted lines ('§ 1º .....'), which the history keeps as a "
           "label-only line and the check, reading label-only lines as revoked dispositivos, drops")
B.EXPLAINED[_LCSE] = {"art-30": _DOTTED}
B.EXPLAINED["lei-dos-portos"] = {"art-71": _DOTTED}
B13.OPEN_ITEMS[_LCSE] = (
    "Lei 12.783 (open items): the text before 14.1.2013 (Medida Provisória 579/2012, of which this Lei is the conversion) is "
    "not part of the history; the retroactive effects of Medida Provisória 612/2013 art. 22 and Lei 12.844/2013 art. 27 "
    "(from 14.1.2013) keep their in-force days; 'Vide' pointers (Medida Provisória 615/2013, decrees) strike no words and "
    "are not modelled")
B13.OPEN_ITEMS["lei-dos-portos"] = (
    "Lei 12.815 (open items): the text before 5.6.2013 (Medida Provisória 595/2012, of which this Lei is the conversion) is "
    "not part of the history; 'Vide' pointers and regulations strike no words and are not modelled")
_W27 = ("Lei 12.783 art. 27 (its new wording of Lei 12.111 art. 3 § 16): Medida Provisória 1.232/2024 (DOU 13.6.2024, art. 3 "
         "II) revoked the whole article and lapsed on 10.10.2024 (Ato Declaratório 101/2024); Planalto notes the revocation on "
         "the article's first line only, so the quoted lines below it get the same gap, 13.6.2024 to 11.10.2024")
_G1232 = {"gaps": [("2024-06-13", "2024-10-11", "mp-1232-2024", "mp-1232-2024-fim")]}
B8.SPAN_FIX += [((_LCSE, "art-27", lab, pre, 0), dict(_G1232), _W27) for lab, pre in (("", '"Art. 3'), ("§ 16", "§ 16."))]
B13.OPEN_ITEMS[_L9074] = (
    "Lei 9.074 (open items): the text before 8.7.1995 (Medida Provisória 1.017/1995, of which this Lei is the conversion) is "
    "not part of the history; the republication of 28.9.1998 is read as Planalto prints the Lei; 'Vide' pointers (decrees, "
    "Lei 12.783/2013) strike no words and are not modelled")
# part v: Lei 12.462/2011 (RDC). Hand days set only when the act runs.
_LRDC = "lei-do-rdc"
if any(a["slug"] == _LRDC for a in ACTS):
    P.VIGENCIA_FIXED["lei-14133-2021"] = (
        "2023-12-30", "art. 193, as Lei Complementar 198/2023 worded it: 'Revogam-se: [...] II - em 30 de dezembro de 2023: "
                      "[...] c) os arts. 1º a 47-A da Lei nº 12.462, de 4 de agosto de 2011' (the first wording set two years "
                      "from 1.4.2021; Medida Provisória 1.167/2023 and then LC 198/2023 moved it): every note of Lei 14.133 on "
                      "Lei 12.462's page is that revocation, so it is dated 30.12.2023, not by Lei 14.133's own entry into force")
    P.VIGENCIA_FIXED["mp-551-2011"] = (
        "2012-01-10", "'Esta Medida Provisória entra em vigor na data de sua publicação, produzindo efeitos: I - em relação aos "
                      "arts. 1º, 2º, 3º, 4º, 5º e 10, a partir do dia 10 de janeiro de 2012' (DOU 23.11.2011): its art. 4 (Lei "
                      "12.462 art. 63) takes effect on 10.1.2012")
    P.VIGENCIA_FIXED["lei-12688-2012"] = (
        "2012-07-19", "art. 34: 'Esta Lei entra em vigor: [...] III - a partir de 1º de junho de 2012, quanto ao disposto no art. "
                      "30; IV - na data de sua publicação, em relação aos demais artigos' (DOU 19.7.2012): its art. 28 (Lei "
                      "12.462 arts. 1 and 43) falls under IV")
    for _n in ("Incluído", "Redação dada"):
        P.NOTE_FIX[f"({_n} pela Lei nº 1.4002, de 2020)"] = (
            f"({_n} pela Lei nº 14.002, de 2020)",
            f"Lei 12.462: notes read '{_n} pela Lei nº 1.4002, de 2020'; their links go to Lei 14.002/2020 (L14002.htm)")
B.EXPLAINED[_LRDC] = {
    "art-48": _DOTTED, "art-68": _DOTTED,
    "titulos": "the consolidated page still prints the headings of Capítulo I's Seções II to V and their Subseções, which the "
               "annotated page strikes with arts. 1 to 47-A (revoked by Lei 14.133/2021 from 30.12.2023)",
    "art-63": "the consolidated page prints § 17 (Medida Provisória 1.349/2026), which lapsed on a day not read here and is "
              "left out of the history",
}
_W14034 = ("Lei 12.462 art. 63: Lei 14.034/2020 (DOU 6.8.2020) art. 13: 'produzirá efeitos, quanto ao § 5º do art. 63 da Lei nº "
           "12.462 [...] alterado pelo art. 7º desta Lei, e quanto aos incisos II e III do caput do art. 12 desta Lei, em 1º de "
           "janeiro de 2021': its § 5º (caput and incisos I and II) and the revocation of § 1º II (art. 12 III) take effect on "
           "1.1.2021; its other changes to art. 63 on 6.8.2020")
_S21 = {"start": "2021-01-01", "start_law": "lei-14034-2020"}
_E21 = {"end": "2021-01-01", "end_law": "lei-14034-2020"}
B8.SPAN_FIX += [((_LRDC, "art-63", lab, pre, 0), dict(f), _W14034) for lab, pre, f in (
    ("§ 5º", "§ 5º Os recursos do FNAC também poderão ser aplicados no desenvolvimento", _E21),
    ("§ 5º", "§ 5º Os recursos do FNAC também poderão ser aplicados:", _S21),
    ("I -", "I - no desenvolvimento, na ampliação e na reestruturação de aeroportos concedidos", _S21),
    ("II -", "II - no custeio de eventuais despesas decorrentes de responsabilidade civil", _S21),
    ("II -", "II - os referidos no art. 1º da Lei nº 9.825", _E21))]
B8.SPAN_FIX[-1] = ((_LRDC, "art-63", "II -", "II - os referidos no art. 1º da Lei nº 9.825", 1), dict(_E21), _W14034)   # Lei 12.648's copy
_W63B = ("Lei 12.462 art. 63-B (caput and parágrafo único), added by Lei 14.901/2024 art. 3 (DOU 26.6.2024, in force on "
         "publication): its art. 5 reads '[...] nos termos do art. 140 da Lei nº 14.791, de 29 de dezembro de 2023, o art. "
         "63-B acrescido à Lei nº 12.462 [...] pelo art. 3º desta Lei terá vigência por 5 (cinco) anos'. The term runs from "
         "26.6.2024, the first day counted, to 25.6.2029, so the article is in force to that day and leaves the text on "
         "26.6.2029 (on the futuro branch while that day is ahead), credited to Lei 14.901. No later law that extends the "
         "term is noted on Planalto's page (capture of 23.10.2026)")
_T63B = {"end": "2029-06-26", "end_law": "lei-14901-2024", "end_how": "term"}
B8.SPAN_FIX += [((_LRDC, "art-63-b", lab, pre, 0), dict(_T63B), _W63B) for lab, pre in (
    ("Art. 63-B", "Art. 63-B. Da arrecadação total do FNAC"), ("Parágrafo único", "Parágrafo único. Ato conjunto dos Ministros"))]
B13.OPEN_ITEMS[_LRDC] = (
    "Lei 12.462 (open items): the text before 5.8.2011 (Medida Provisória 527/2011, of which this Lei is the conversion) is "
    "not part of the history; the STF's ADIs 4.645 and 4.655 (Planalto prints only 'Vide' notes) are not modelled; art. 63 "
    "§ 17 (Medida Provisória 1.349/2026, lapsed on a day not read here) is left out; 'Vide' pointers (Decreto 8.024/2013, "
    "Lei 14.034/2020, Lei 14.133/2021) strike no words and are not modelled")

# part w: Lei 10.233/2001 (ANTT, ANTAQ, DNIT). Hand days set only when the act runs.
_LANTT = "lei-da-antt-e-antaq"
if any(a["slug"] == _LANTT for a in ACTS):
    P.MP_LAPSE["mp-800-2017"] = (
        "2018-02-27", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 6, de 2018 (DOU 28.2.2018): 'teve seu "
                      "prazo de vigência encerrado no dia 26 de fevereiro do corrente ano'; the lines it added to Lei 10.233 "
                      "end on 27.2.2018")
    P.MP_PENDING["mp-2217-2001"] = (
        "Medida Provisória nº 2.217-3, de 4.9.2001 (DOU 5.9.2001, art. 7: in force on publication), kept in force by Emenda "
        "Constitucional 32/2001, art. 2; its art. 1 gave Lei 10.233 the wordings Planalto notes with this edition (its art. "
        "6 confirms the acts done under Medida Provisória 2.201-2/2001, the edition before it). Planalto's notes name this "
        "edition only, so its changes are dated by its publication; earlier editions of the chain are not modelled")
    B7.CONVERTED_FIX["mp-155-2003"] = ("lei-10871-2004", "Lei 10.871/2004's page reads 'Conversão da MPv nº 155, de 2003' "
                                                         "(DOU 21.5.2004, art. 38: in force on publication)")
_W1065 = ("Lei 10.233: Medida Provisória 1.065/2021 (DOU 30.8.2021) lapsed at the close of 6.2.2022 (Ato Declaratório 5/2022), "
          "and Lei 14.273/2021 (DOU 23.12.2021, edição extra; no vigência clause, so in force 45 days later, on 6.2.2022) "
          "gave new wordings to arts. 24 IX, 25 I, V, VII to IX and parágrafo único, 38 and 82 § 1º and revoked art. 13 "
          "parágrafo único (its art. 78 II c). Where Lei 14.273 replaced or revoked a line MP 1.065 had changed, the MP's "
          "wording ends on 6.2.2022 and the wording the MP had replaced is not back (Planalto prints it a second time, below "
          "the MP's struck line: that copy is left out). Where Lei 14.273 left the line alone (art. 24 IV, added by the MP; "
          "art. 25 III), the MP's wording ends with its lapse, on 7.2.2022, and the wording it replaced is back from that day")
_E14273 = {"end": "2022-02-06", "end_law": "lei-14273-2021", "end_how": "successor-before-lapse"}
_ELAPSE = {"end": "2022-02-07", "end_law": "mp-1065-2021-fim", "end_how": "lapse"}
_SKIP = {"skip": True, "end_how": "never-restored"}
B8.SPAN_FIX += [((_LANTT, u, lab, pre, n), dict(f), _W1065) for u, lab, pre, n, f in (
    ("art-13", "Parágrafo único", "Parágrafo único. A exploração de ferrovias será disciplinada", 0, _E14273),
    ("art-13", "Parágrafo único", "Parágrafo único. Considera-se, para os fins da alínea d do inciso V", 1, _SKIP),
    ("art-38", "Art. 38", "Art. 38. As permissões a serem outorgadas pela ANTT para o transporte rodoviário interestadual "
                          "semiurbano e pela Antaq serão aplicadas", 0, _E14273),
    ("art-38", "Art. 38", "Art. 38. As permissões a serem outorgadas pela ANTT para o transporte rodoviário interestadual "
                          "semiurbano e para o transporte ferroviário", 0, _SKIP),
    ("art-82", "§ 1º", "§ 1º As atribuições a que se refere o caput não se aplicam aos elementos da infraestrutura autorizados", 0,
     _E14273),
    ("art-82", "§ 1º", "§ 1º As atribuições a que se refere o caput não se aplicam aos elementos da infra-estrutura concedidos ou "
                       "arrendados pela ANTT e pela ANTAQ.", 1, _SKIP),
    ("art-24", "IV -", "IV - adotar, no todo ou em parte, normas e regulações", 0, _ELAPSE),
    ("art-25", "III -", "III - publicar editais, julgar as licitações e celebrar contratos de concessão e de permissão", 0,
     _ELAPSE))]
_W7A = ("Lei 10.233 art. 7º-A: Planalto prints Lei 10.683/2003's wording (DOU 29.5.2003, in force on publication) as 'Art. 7 o A' "
        "(no hyphen), which was read as a line of art. 7; it is the article's second wording, from 29.5.2003 to Medida "
        "Provisória 369/2007's wording (8.5.2007), and Medida Provisória 2.217-3/2001's wording ends on 29.5.2003 (Planalto "
        "notes it 'Revogado pela Medida Provisória nº 369, de 2007', the MP that replaced the next wording)")
_W115 = ("Lei 10.233 art. 115: Medida Provisória 2.217-3/2001 (DOU 5.9.2001, in force on publication) gave the caput a new wording "
         "and its art. 8 revoked § 1º ('Ficam revogados o inciso IV do art. 44 e o § 1º do art. 115'); Planalto notes § 1º "
         "'Revogado pela Medida Provisória nº 353, de 2007' and strikes the 2001 caput with only Lei 11.483's note, so both end "
         "on 5.9.2001")
B8.SPAN_FIX += [
    ((_LANTT, "art-07", "Art. 7º", "Art. 7º A O CONIT", 0),
     {"unit": "art-07-a", "label": "Art. 7º-A", "moved_from": ("art-07", "Art. 7º"), "skip": False, "end": "2007-05-08", "end_law": "mp-369-2007",
      "end_how": "successor", "text": "Art. 7º-A O CONIT será presidido pelo Ministro de Estado dos Transportes e terá como "
      "membros os Ministros de Estado da Defesa, da Justiça, da Fazenda, do Planejamento, Orçamento e Gestão, do "
      "Desenvolvimento, Indústria e Comércio Exterior e das Cidades."}, _W7A),
    ((_LANTT, "art-07-a", "Art. 7º-A", "Art. 7º-A. O CONIT será presidido pelo Ministro de Estado dos Transportes e terá como "
                                       "membros os Ministros de Estado da Defesa", 0),
     {"end": "2003-05-29", "end_law": "lei-10683-2003", "end_how": "successor"}, _W7A),
    ((_LANTT, "art-88", "Parágrafo único", "Parágrafo único. As nomeações dos Diretores do DNIT", 0),
     {"skip": False, "end": "2019-01-01", "end_law": "mp-870-2019", "end_how": "note"},
     "Lei 10.233 art. 88 parágrafo único (added by Medida Provisória 2.217-3/2001): Planalto leaves the 'Incluído' note "
     "unclosed, so the notes after it ('Revogado pela Medida Provisória nº 870, de 2019', 'Revogado pela Lei nº 13.844, de "
     "2019') were not read; it ends with MP 870's revocation on 1.1.2019, as the other lines MP 870 revoked"),
    ((_LANTT, "art-115", "Art. 115", "Art. 115. Os quadros de Pessoal Específico e em Extinção, de que tratam os arts. 113 e "
                                     "114,", 0),
     {"end": "2001-09-05", "end_law": "mp-2217-2001", "end_how": "successor"}, _W115),
    ((_LANTT, "art-88-a", "Art. 88-A", "Art. 88-A. As nomeações dos Diretores", 0),
     {"start": "2019-12-11", "start_law": "lei-13901-2019", "promulgated": True},
     "Lei 10.233 art. 88-A: Lei 13.901/2019 (DOU 12.11.2019) art. 5, which added it, was vetoed; Congress overrode the veto and "
     "the President promulgated the part on 10.12.2019 (DOU 11.12.2019; printed on Lei 13.901's page as 'Promulgação partes "
     "vetadas'), so the article starts on 11.12.2019, credited to Lei 13.901"),
    ((_LANTT, "art-115", "§ 1º", "§ 1º À medida que forem extintos", 0),
     {"end": "2001-09-05", "end_law": "mp-2217-2001", "end_how": "note"}, _W115),
]
# part x: Lei 13.848/2019 (agências reguladoras), Lei 9.986/2000. Hand days set only when the acts run.
_LAR, _L9986 = "lei-geral-das-agencias-reguladoras", "lei-9986-de-2000"
if any(a["slug"] == _L9986 for a in ACTS):
    B7.CONVERTED_FIX["mp-155-2003"] = ("lei-10871-2004", "Lei 10.871/2004's page reads 'Conversão da MPv nº 155, de 2003' "
                                                         "(DOU 21.5.2004, art. 38: in force on publication)")
    P.MP_LAPSE["mp-1181-2023"] = (
        "2023-11-15", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 79, de 2023: 'teve seu prazo de vigência "
                      "encerrado no dia 14 de novembro de 2023'; its art. 24 I had revoked Lei 9.986 art. 32 from 18.7.2023, and Lei "
                      "14.724/2023 (DOU 14.11.2023, in force on publication) revoked it again")
    P.MP_PENDING["mp-2229-2001"] = (
        "Medida Provisória nº 2.229-43, de 6.9.2001 (DOU 10.9.2001, in force on publication), kept in force by Emenda "
        "Constitucional 32/2001, art. 2; it gave Lei 9.986 art. 22 its wording. Planalto's note names this edition only, so the "
        "change is dated by its publication; earlier editions of the chain are not modelled")
    P.MP_PENDING["mp-2216-2001"] = (
        "Medida Provisória nº 2.216-37, de 31.8.2001 (DOU 1.9.2001, art. 32: in force on publication), kept in force by Emenda "
        "Constitucional 32/2001, art. 2; it gave Lei 9.986 art. 8 its wording ('quatro meses'). Planalto's notes name this "
        "edition only, so the change is dated by its publication; earlier editions of the chain are not modelled")
_W32 = ("Lei 9.986 art. 32 parágrafo único: Medida Provisória 1.181/2023 (DOU 18.7.2023) art. 24 I and Lei 14.724/2023 (DOU "
        "14.11.2023, in force on publication) art. 36 III revoke 'o art. 32 da Lei nº 9.986', the whole article; Planalto strikes "
        "only the caput and leaves the parágrafo único unstruck, so it falls with the caput: absent from 18.7.2023 while the MP "
        "stood, and revoked by Lei 14.724 on 14.11.2023, before the MP's lapse (14.11.2023) could restore it")
B8.SPAN_FIX += [((_L9986, "art-32", "Parágrafo único", "Parágrafo único. Os Cargos Comissionados", 0),
                 {"end": "2023-11-14", "end_law": "lei-14724-2023", "end_how": "note",
                  "gaps": [("2023-07-18", "2023-11-15", "mp-1181-2023", "mp-1181-2023-fim")]}, _W32)]
B.EXPLAINED[_L9986] = {"art-32": "the page leaves art. 32's parágrafo único unstruck, though Lei 14.724/2023 revoked the whole "
                                 "article (art. 32 caput is struck); it is left out from 14.11.2023"}
B13.OPEN_ITEMS[_L9986] = (
    "Lei 9.986 (open items): the Anexos (posts of each agency) are not part of the history; the STF's ADI 2.310 (Planalto prints "
    "only 'Vide ADIN 2310' on the struck lines of the employment regime, which Lei 10.871/2004 revoked) is not modelled; "
    "Medidas Provisórias 2.216-37/2001 and 2.229-43/2001 are dated by those editions; 'Vide' pointers (Medidas Provisórias "
    "155/2003, 269/2005, 304/2006, 2.048-28/2000 and 2.049-24/2000, Lei 10.871/2004) strike no words and are not modelled")
B13.OPEN_ITEMS[_LAR] = (
    "Lei 13.848 (open items): its own changes to other laws (arts. 39 to 51) are recorded in those laws' histories where the "
    "corpus holds them; Lei 15.352/2026 restated art. 2 XII (added by Medida Provisória 1.317/2025) without changing its words")
B13.OPEN_ITEMS[_LANTT] = (
    "Lei 10.233 (open items): the Anexos (tables of posts and salaries, including Tabela IV as Medida Provisória 1.120/2022 and "
    "Lei 14.465/2022 replaced it) are not part of the history; Medida Provisória 2.217-3/2001's changes are dated by that "
    "edition (earlier editions of the chain, among them Medida Provisória 2.201-2/2001, are not modelled); the 'Medida "
    "Provisória 246' that one note of art. 118 § 1º also names has no printed wording and is not modelled; financial effects "
    "of Lei 10.470/2002 (1.3.2002) and Medida Provisória 375/2007 (1.6.2007) keep the in-force days; 'Vide' pointers "
    "(Medidas Provisórias 155/2003, 353/2007 and 2.217-3/2001, Decreto 6.550/2008) strike no words and are not modelled")
B13.OPEN_ITEMS[_LCADIN] = (
    "Lei 10.522 (open items): the text before 22.7.2002 (Medida Provisória 2.176-79/2001 and its earlier editions, of which "
    "this Lei is the conversion) is not part of the history; the STF's judgment in ADIs 5.881, 5.886, 5.890, 5.925, 5.931 and "
    "5.932 on arts. 20-B to 20-E (Planalto prints only 'Vide' notes and strikes no words) is not modelled; 'Vide' pointers "
    "(Medidas Provisórias 75/2002, 249/2005, 526/2011, 766/2017, 958/2020, 975/2020, 1.028/2021, 1.176/2023 and 1.259/2024, "
    "Leis 12.453/2011, 12.973/2014, 13.340/2016, 13.999/2020, 14.057/2020, 14.179/2021 and 14.690/2023 on art. 6, ADI "
    "1.976-7) strike no words and are not modelled. LEFT OUT: art. 32's quoted § 2º of Decreto 70.235 art. 33 (the "
    "arrolamento of 30% of the debt as a condition of the recurso voluntário), in the act as enacted: Planalto strikes it "
    "with only '(Vide Adin nº 1.976-7)' and no date; the STF ruling cannot be read here (the STF's case pages are closed to "
    "this project's reader), so the line's end cannot be dated and it is not in any version")

# Lei 9.430 arts. 18 to 22: the headings above them (Seção V 'Preços de Transferência' and the article headings) are struck
# with no note; they fall with the articles, revoked by Lei 14.596/2023 (the 'heads' rule would end each with the first
# change of the article under it)
HEADS_14596 = {_L9430: ("lei-14596-2023", {"Seção V", "Preços de Transferência", "Bens, Serviços e Direitos Adquiridos no "
                                           "Exterior", "Receitas Oriundas de Exportações para o Exterior",
                                           "Apuração dos Preços Médios", "Juros"})}
HEADS_USED: list[str] = []


def heads_14596(paras, act, eff):
    if act["slug"] not in HEADS_14596:
        return
    law, names = HEADS_14596[act["slug"]]
    for p in paras:
        if p["heading"] and p["state"] != "plain" and p.get("end_how") == "heads" and P.norm(p["text"]) in names:
            p["end"], p["end_law"], p["end_how"] = eff[law], law, "note"
            HEADS_USED.append(P.norm(p["text"]))

B15.TEXT_FIX.append(("l7713","calculado de acordo com o disposto no art. 25 desta Lei:)$",
                     "calculado de acordo com o disposto no art. 25 desta Lei:",
                     "Lei 7.713 art. 7 caput: the annotated page leaves a stray closing parenthesis after the 'Vide' notes "
                     "('(Vide Lei nº 9.250, de 1995) )'); the consolidated page has none"))
B.EXPLAINED[_L7713] = {
    "art-30": "the consolidated page prints 'Arts. 28 e 29 (Revogados pela Lei nº 8.134, de 1990)' as one line before art. 30, "
              "which its reading files under art. 30; the annotated page prints both articles, struck",
}
B13.OPEN_ITEMS[_L7713] = (
    "Lei 7.713 (open items): changes whose effects reach back before their in-force day keep that day (Leis 7.799/1989, "
    "11.119/2005, 11.311/2006, 11.482/2007, 11.945/2009, 12.794/2013); Lei 9.430/1996's 'efeitos financeiros a partir de 1º de "
    "janeiro de 1997' are financial effects only (in-force day kept); 'Vide' pointers (Leis 8.134/1990, 8.383/1991, "
    "8.848/1994, 9.250/1995, Medidas Provisórias 582/2012 and 1.303/2025 and others) strike no words and are not modelled")

_lifespans17 = P.lifespans


def lifespans(paras, cx):
    problems = _lifespans17(paras, cx)
    # a struck line a SPAN_FIX entry gave an end (Lei 10.522 art. 20-D's '(VETADO' line): the reader's 'no end' is settled
    dated = {f"no end for struck {u} [{lab}] " for p in paras
             if p.get("pinned") and p["state"] != "plain" and p.get("end") and not p.get("skip")
             for u, lab in ((p["unit"], p["label"]), p.get("moved_from") or (p["unit"], p["label"]))}
    return [x for x in problems if not any(x.startswith(t) for t in dated)]


P.lifespans = B.lifespans = lifespans
_apply_rewrites17 = P.apply_rewrites


def apply_rewrites(paras, act, eff, problems):
    out = _apply_rewrites17(paras, act, eff, problems)
    renum_articles(paras, act)
    mp955_two_copies(paras, act)
    veto_kept(paras, act)
    promulgated(paras, act)
    heads_14596(paras, act, eff)
    ch3_successors(paras, act)
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
    if any(x.startswith("l9430") for x in BARE_TEXT_USED):
        dec.append("Lei 9.430 art. 88 XXV ends '[...] o art. 89 da Lei nº 8.981, de 20 de janeiro de 1995, com a redação dada "
                   "pela Lei nº 9.065, de 20 de junho de 1995;': these words name the wording of the article it revokes; they are "
                   "part of the text, not an amendment note (l9430 art-88).")
    if any(x.startswith("l9873") for x in BARE_TEXT_USED):
        dec.append("Lei 9.873 art. 3 II and art. 8 name the act they refer to or revoke '[...] da Lei nº 6.385, de [...] 1976, com "
                   "a redação dada pela Lei nº 9.457, de [...] 1997[...]': these words are part of the text, not an amendment "
                   "note (" + ", ".join(dict.fromkeys(x for x in BARE_TEXT_USED if x.startswith("l9873"))) + ").")
    if LRDC_FIXED:
        dec.append("Lei 12.462 art. 63 § 17 was added by Medida Provisória 1.349/2026 (DOU 7.4.2026); Planalto's page of the MP "
                   "reads 'Vigência encerrada' and links Ato Declaratório nº 77 of 2026, which could not be read, so the day "
                   "the paragraph lapsed is not known: it is LEFT OUT of every version (the consolidated page, not updated, "
                   "still prints it).")
    if "art-102-a" in L10233_FIXED:
        dec.append("Lei 10.233 art. 102-A (added by Medida Provisória 2.217-3/2001): Planalto prints it after an opening "
                   "quotation mark copied from the MP ('\"Art. 102-A.'); the mark is left out and the article and its §§ 1º to "
                   "4º are read as art. 102-A, not as unlabelled lines of art. 102.")
    if "art-118 § 1º" in L10233_FIXED:
        dec.append("Lei 10.233 art. 118 § 1º: Planalto prints a single struck line, the 2001 wording ('[...] percebidos pelos "
                   "empregados da RFFSA que vierem a ser absorvidos pela ANTT, conforme estabelece o art. 114.'), with the note "
                   "'Redação dada pela Medida Provisória nº 2.217-3, de 4.9.2001 e 246, de 4.9.2005'. Medida Provisória "
                   "2.217-3/2001 (DOU 5.9.2001) art. 1 gave the paragraph the wording '[...] conforme estabelece o art. 114-A.' "
                   "(read on the MP's page): the printed line stands from 6.6.2001 to 5.9.2001 and the MP's wording from "
                   "5.9.2001 until Lei 11.483/2007 rewrote art. 118 (31.5.2007). No wording of the 'Medida Provisória 246' the "
                   "note also names is printed, and none is modelled.")
    if L9873_FIXED:
        dec.append("Lei 9.873: " + "; ".join(dict.fromkeys(L9873_FIXED)) + " (the Lei, the conversion of Medida Provisória "
                   "1.859-17/1999, was promulgated by the President of the Senate).")
    if MIXED_PLAIN:
        dec.append("Lei 10.522 art. 37-B § 10 (Lei 11.941/2009): Planalto strikes only the dash in 'Custódia – SELIC' (also on "
                   "Lei 11.941's own page) in a line in force; the strike is read as a typesetting slip and the line as unstruck, "
                   "dash kept (" + ", ".join(dict.fromkeys(MIXED_PLAIN)) + ").")
    if any(not x.startswith(("l9430", "l9873")) for x in BARE_TEXT_USED):
        dec.append("Lei 7.689 art. 11 and Lei 9.249 art. 14 end '[...], com a redação dada pelo Decreto-Lei nº [...]' (Decretos-"
                   "Leis 2.449/1988 and 1.730/1979): these words name the wording of the other act the article refers to; they "
                   "are part of the article's text, not an amendment note (" + ", ".join(x for x in BARE_TEXT_USED if not x.startswith(("l9430", "l9873"))) + ").")
    if QUOTE_DROPPED:
        dec.append("Lei 9.249 art. 9: the caput as Medida Provisória 694/2015 worded it (1.1.2016 to its lapse on 8.3.2016) is "
                   "printed after the opening quotation mark of the MP's quoted text; the mark is left out.")
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
    if L9250_FIXED:
        dec.append("Lei 9.250: the centred titles of the tables Lei 15.270/2025 added in arts. 3º-A and 11-A ('Tabela de redução "
                   "do imposto mensal', '... do ajuste anual') are lines of those articles, not headings; empty centred lines "
                   "are left out; the name lines of Capítulos II-A and III-A start with the 'CAPÍTULO' line above them, which "
                   "carries Lei 15.270's note; Planalto's marker 'Sem eficácia' after the struck lines of "
                   "Medida Provisória 252/2005 in art. 22 is not part of the text (" + "; ".join(dict.fromkeys(L9250_FIXED)) + ").")
    if L9430_FIXED:
        dec.append("Lei 9.430: Planalto's markers '(Sem eficácia)' after struck lines (wordings of Medidas Provisórias "
                   "252/2005, 303/2006 and 478/2009 that lapsed or never took effect, and the 1996 lines they touched) and "
                   "'Rejeitada' after the lines of Medida Provisória 75/2002 (rejected) are not part of the text and are left out (" + ", ".join(dict.fromkeys(L9430_FIXED)) + ").")
    if L13465_FIXED:
        dec.append("Lei 13.465: Planalto's link '(Partes vetadas)' after the parts promulgated on 8.9.2017 is not text and is "
                   "left out; art. 4 quotes Lei 11.952 art. 16 ('Art. 16. As condições resolutivas [...]', §§ 1º to 3º) with no "
                   "opening quotation mark, and those lines are read as lines of art. 4, not as Lei 13.465's own art. 16.")
    if CH3_USED:
        dec.append(_W_CH3 + " (" + ", ".join(dict.fromkeys(CH3_USED)) + ").")
    if HEADS_USED:
        dec.append("Lei 9.430: the headings above arts. 18 to 22 (" + "; ".join(f"'{x}'" for x in dict.fromkeys(HEADS_USED))
                   + "), struck with no note, fall with the articles under them, revoked by Lei 14.596/2023 from 1.1.2024 "
                   "(its art. 46 VI), not with the first change of the article each heads.")
    if EMPTY_ITEMS:
        dec.append("Struck items printed with a label and only the note '(Vide Medida nº 340, de 2006)', and no words, are "
                   "pointers, not wordings, and are left out (" + ", ".join(dict.fromkeys(EMPTY_ITEMS)) + ").")
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
