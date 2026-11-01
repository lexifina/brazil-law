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
    # part y
    "l9961": "leis/l9961.htm",
    "l9717": "leis/l9717.htm",
    "l9717-compilado": "leis/l9717compilado.htm",
    # parts z, ...: Leis 9.427/1996 (ANEEL), 9.782/1999 (Anvisa), 8.745/1993 (contratação temporária)
    "l9427": "leis/l9427cons.htm",
    "l9427-compilada": "leis/l9427compilada.htm",
    "l9782": "leis/l9782.htm",
    "l9782-compilado": "leis/l9782compilado.htm",
    "l8745": "leis/l8745cons.htm",
    "l8745-compilada": "leis/l8745compilada.htm",
    # parts zc, zd
    "l10101": "leis/l10101.htm",
    "l10101-compilado": "leis/l10101compilado.htm",
    "l9608": "leis/l9608.htm",
    "l9608-compilado": "leis/l9608compilado.htm",
    "l12506": "_ato2011-2014/2011/lei/l12506.htm",
    "l9984": "leis/l9984.htm",
    "l9984-compilado": "leis/l9984compilado.htm",
    "l12334": "_ato2007-2010/2010/lei/l12334.htm",
    "lcp105": "leis/lcp/lcp105.htm",
    # parts zg, zh
    "l11182": "_ato2004-2006/2005/lei/l11182.htm",
    "l13575": "_ato2015-2018/2017/lei/l13575.htm",
    "l11428": "_ato2004-2006/2006/lei/l11428.htm",
    "l4886": "leis/l4886.htm",
    "l8397": "leis/l8397.htm",
    "l9795": "leis/l9795.htm",
    # parts zi, zj
    "l11417": "_ato2004-2006/2006/lei/l11417.htm",
    "l11418": "_ato2004-2006/2006/lei/l11418.htm",
    "l13460": "_ato2015-2018/2017/lei/l13460.htm",
    "l12187": "_ato2007-2010/2009/lei/l12187.htm",
    "l13123": "_ato2015-2018/2015/lei/l13123.htm",
    # parts zj (published), zk, zl (pinned, not configured): PIS/COFINS (Leis 9.718/1998, 10.637/2002, 10.833/2003), one act per part
    "l9718": "leis/l9718.htm",
    "l9718-compilada": "leis/l9718compilada.htm",
    "l10637": "leis/2002/l10637.htm",
    "l10637-compilado": "leis/2002/l10637compilado.htm",
    "l10833": "leis/2003/l10.833.htm",
    "l10833-compilado": "leis/2003/l10.833compilado.htm",
    # parts zm, ...: thin areas (SUS, education, public finance, transport, forests, consumer, electoral)
    "lcp141": "leis/lcp/lcp141.htm",
    "l14113": "_ato2019-2022/2020/lei/l14113.htm",
    "l12414": "_ato2011-2014/2011/lei/l12414.htm",
    "l11442": "_ato2007-2010/2007/lei/l11442.htm",
    "lcp200": "leis/lcp/lcp200.htm",
    "l11284": "_ato2004-2006/2006/lei/l11284.htm",
    "l6091": "leis/l6091.htm",
    "l9611": "leis/l9611.htm",
    "l10209": "leis/leis_2001/l10209.htm",
    "l14119": "_ato2019-2022/2021/lei/l14119.htm",
    "l9434": "leis/l9434.htm",
    "l10216": "leis/leis_2001/l10216.htm",
    "l9434-compilado": "leis/l9434compilado.htm",
    # parts zr, ...: education, transport, health surveillance, electoral, fiscal federalism
    "l11738": "_ato2007-2010/2008/lei/l11738.htm",
    "l12009": "_ato2007-2010/2009/lei/l12009.htm",
    "l6996": "leis/1980-1988/l6996.htm",
    "l9870": "leis/l9870.htm",
    "l12379": "_ato2011-2014/2011/lei/l12379.htm",
    "l6437": "leis/l6437.htm",
    "l6437-compilado": "leis/l6437compilado.htm",
    "l13005": "_ato2011-2014/2014/lei/l13005.htm",
    "lcp159": "leis/lcp/lcp159.htm",
    "lcp178": "leis/lcp/lcp178.htm",
    # parts zv, zw (nineteenth session)
    "l7853": "leis/l7853.htm",
    "l7853-compilado": "leis/l7853compilado.htm",
    "l9807": "leis/l9807.htm",
    "l10861": "_ato2004-2006/2004/lei/l10.861.htm",
    "l10973": "_ato2004-2006/2004/lei/l10.973.htm",
    "l9456": "leis/l9456.htm",
    # parts zx, ... (twentieth session)
    "l7802-2023": "leis/l7802.htm",   # capture of 18.12.2023, before Lei 14.785/2023 repealed it
    "l14785": "_ato2023-2026/2023/lei/l14785.htm",
    "l11947": "_ato2007-2010/2009/lei/l11947.htm",
    "l10820": "leis/2003/l10.820.htm",
    "l9612": "leis/l9612.htm",
    # twenty-first session
    "l13979": "_ato2019-2022/2020/lei/l13979.htm",
    "l6360": "leis/l6360.htm",
    "l11494": "_ato2007-2010/2007/lei/l11494.htm",
    "l11494-2020": "_ato2007-2010/2007/lei/l11494.htm",   # capture of 15.12.2020, before Lei 14.113/2020 repealed it
    "l9424": "leis/l9424.htm",
    # twenty-second session: fresh ranked list (social security, environment, electoral, banking)
    "lcp109": "leis/lcp/lcp109.htm",
    "lcp108": "leis/lcp/lcp108.htm",
    "lcp140": "leis/lcp/lcp140.htm",
    "l9709": "leis/l9709.htm",
    "lcp179": "leis/lcp/lcp179.htm",
    "l14286": "_ato2019-2022/2021/lei/l14286.htm",
    "l12351": "_ato2007-2010/2010/lei/l12351.htm",
    "l14134": "_ato2019-2022/2021/lei/l14134.htm",
    "del0200": "decreto-lei/del0200.htm",
    "lcp80": "leis/lcp/lcp80.htm",
    "lcp75": "leis/lcp/lcp75.htm",
    "l8437": "leis/l8437.htm",
    "l9494": "leis/l9494.htm",
    "l12813": "_ato2011-2014/2013/lei/l12813.htm",
    "l14129": "_ato2019-2022/2021/lei/l14129.htm",
    # twenty-third session: next on the ranked list
    "l8625": "leis/l8625.htm",
    "l12618": "_ato2011-2014/2012/lei/l12618.htm",
    "l12865": "_ato2011-2014/2013/lei/l12865.htm",
    "l14601": "_ato2023-2026/2023/lei/l14601.htm",
    # twenty-fourth session
    "l10848": "_ato2004-2006/2004/lei/l10.848.htm",
    # twenty-fifth session: environment laws
    "l9966": "leis/l9966.htm",
    "l7661": "leis/l7661.htm",
    "l11959": "_ato2007-2010/2009/lei/l11959.htm",
    "l5197": "leis/l5197.htm",
    "l7735": "leis/l7735.htm",
    "l11516": "_ato2007-2010/2007/lei/l11516.htm",
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
    _act("lei-da-ans", "LANS", "l9961", "l9961", "lei-9961-2000",
         "Agência Nacional de Saúde Suplementar - ANS (Lei nº 9.961, de 28 de janeiro de 2000)", 2),
    _act("lei-9717-de-1998", "L9717", "l9717", "l9717-compilado", "lei-9717-1998",
         "Regimes próprios de previdência social dos servidores públicos (Lei nº 9.717, de 27 de novembro de 1998)", 2),
    _act("lei-da-aneel", "LANEEL", "l9427", "l9427-compilada", "lei-9427-1996",
         "Agência Nacional de Energia Elétrica - ANEEL (Lei nº 9.427, de 26 de dezembro de 1996)", 2),
    _act("lei-da-anvisa", "LAnvisa", "l9782", "l9782-compilado", "lei-9782-1999",
         "Sistema Nacional de Vigilância Sanitária e Anvisa (Lei nº 9.782, de 26 de janeiro de 1999)", 2),
    _act("lei-da-contratacao-temporaria", "LCTemp", "l8745", "l8745-compilada", "lei-8745-1993",
         "Contratação por tempo determinado na Administração Pública Federal (Lei nº 8.745, de 9 de dezembro de 1993)", 2),
    _act("lei-da-participacao-nos-lucros", "LPLR", "l10101", "l10101-compilado", "lei-10101-2000",
         "Participação dos trabalhadores nos lucros ou resultados (Lei nº 10.101, de 19 de dezembro de 2000)", 2),
    _act("lei-do-servico-voluntario", "LVol", "l9608", "l9608-compilado", "lei-9608-1998",
         "Lei do Serviço Voluntário (Lei nº 9.608, de 18 de fevereiro de 1998)", 2),
    _act("lei-do-aviso-previo", "LAPrev", "l12506", "l12506", "lei-12506-2011",
         "Aviso prévio proporcional (Lei nº 12.506, de 11 de outubro de 2011)", 2),
    _act("lei-da-ana", "LANA", "l9984", "l9984-compilado", "lei-9984-2000",
         "Agência Nacional de Águas e Saneamento Básico - ANA (Lei nº 9.984, de 17 de julho de 2000)", 2),
    _act("lei-de-seguranca-de-barragens", "LSB", "l12334", "l12334", "lei-12334-2010",
         "Política Nacional de Segurança de Barragens (Lei nº 12.334, de 20 de setembro de 2010)", 2),
    _act("lei-do-sigilo-bancario", "LC105", "lcp105", "lcp105", "lc-105-2001",
         "Sigilo das operações de instituições financeiras (Lei Complementar nº 105, de 10 de janeiro de 2001)", 2),
    _act("lei-da-anac", "LANAC", "l11182", "l11182", "lei-11182-2005",
         "Agência Nacional de Aviação Civil - ANAC (Lei nº 11.182, de 27 de setembro de 2005)", 2),
    _act("lei-da-anm", "LANM", "l13575", "l13575", "lei-13575-2017",
         "Agência Nacional de Mineração - ANM (Lei nº 13.575, de 26 de dezembro de 2017)", 2),
    _act("lei-da-mata-atlantica", "LMA", "l11428", "l11428", "lei-11428-2006",
         "Lei da Mata Atlântica (Lei nº 11.428, de 22 de dezembro de 2006)", 2),
    _act("lei-dos-representantes-comerciais", "LRC", "l4886", "l4886", "lei-4886-1965",
         "Representantes comerciais autônomos (Lei nº 4.886, de 9 de dezembro de 1965)", 2),
    _act("lei-da-medida-cautelar-fiscal", "LMCF", "l8397", "l8397", "lei-8397-1992",
         "Medida cautelar fiscal (Lei nº 8.397, de 6 de janeiro de 1992)", 2),
    _act("lei-da-educacao-ambiental", "LPNEA", "l9795", "l9795", "lei-9795-1999",
         "Política Nacional de Educação Ambiental (Lei nº 9.795, de 27 de abril de 1999)", 2),
    _act("lei-da-sumula-vinculante", "LSV", "l11417", "l11417", "lei-11417-2006",
         "Súmula vinculante (Lei nº 11.417, de 19 de dezembro de 2006)", 2),
    _act("lei-dos-usuarios-de-servicos-publicos", "LUSP", "l13460", "l13460", "lei-13460-2017",
         "Código de Defesa dos Usuários de Serviços Públicos (Lei nº 13.460, de 26 de junho de 2017)", 2),
    _act("lei-da-politica-nacional-sobre-mudanca-do-clima", "PNMC", "l12187", "l12187", "lei-12187-2009",
         "Política Nacional sobre Mudança do Clima (Lei nº 12.187, de 29 de dezembro de 2009)", 2),
    _act("lei-da-biodiversidade", "LBio", "l13123", "l13123", "lei-13123-2015",
         "Lei da Biodiversidade (Lei nº 13.123, de 20 de maio de 2015)", 2),
    _act("lei-9718-de-1998", "L9718", "l9718", "l9718-compilada", "lei-9718-1998",
         "PIS/Pasep e Cofins (Lei nº 9.718, de 27 de novembro de 1998)", 2),
    _act("lei-10637-de-2002", "L10637", "l10637", "l10637-compilado", "lei-10637-2002",
         "PIS/Pasep não cumulativo (Lei nº 10.637, de 30 de dezembro de 2002)", 2),
    _act("lei-10833-de-2003", "L10833", "l10833", "l10833-compilado", "lei-10833-2003",
         "Cofins não cumulativa (Lei nº 10.833, de 29 de dezembro de 2003)", 2),
    _act("lei-do-financiamento-da-saude", "LC141", "lcp141", "lcp141", "lc-141-2012",
         "Aplicação mínima em ações e serviços públicos de saúde (Lei Complementar nº 141, de 13 de janeiro de 2012)", 2),
    {**_act("lei-do-fundeb", "LFundeb", "l14113", "l14113", "lei-14113-2020",
            "Fundo de Manutenção e Desenvolvimento da Educação Básica - Fundeb (Lei nº 14.113, de 25 de dezembro de 2020)", 2),
     "center_headings": False},   # headings are <h4> blocks, not centred: the name line after a Capítulo/Seção line is a heading
    _act("lei-do-cadastro-positivo", "LCadPos", "l12414", "l12414", "lei-12414-2011",
         "Lei do Cadastro Positivo (Lei nº 12.414, de 9 de junho de 2011)", 2),
    _act("lei-do-regime-fiscal-sustentavel", "LC200", "lcp200", "lcp200", "lc-200-2023",
         "Regime Fiscal Sustentável (Lei Complementar nº 200, de 30 de agosto de 2023)", 2),
    _act("lei-do-transporte-rodoviario-de-cargas", "LTRC", "l11442", "l11442", "lei-11442-2007",
         "Transporte Rodoviário de Cargas (Lei nº 11.442, de 5 de janeiro de 2007)", 2),
    _act("lei-do-vale-pedagio", "LVP", "l10209", "l10209", "lei-10209-2001",
         "Vale-Pedágio obrigatório (Lei nº 10.209, de 23 de março de 2001)", 2),
    _act("lei-do-transporte-multimodal", "LTM", "l9611", "l9611", "lei-9611-1998",
         "Transporte Multimodal de Cargas (Lei nº 9.611, de 19 de fevereiro de 1998)", 2),
    _act("lei-de-gestao-de-florestas-publicas", "LGFP", "l11284", "l11284", "lei-11284-2006",
         "Gestão de florestas públicas e Serviço Florestal Brasileiro (Lei nº 11.284, de 2 de março de 2006)", 2),
    _act("lei-do-pagamento-por-servicos-ambientais", "LPSA", "l14119", "l14119", "lei-14119-2021",
         "Política Nacional de Pagamento por Serviços Ambientais (Lei nº 14.119, de 13 de janeiro de 2021)", 2),
    _act("lei-do-transporte-de-eleitores", "LTE", "l6091", "l6091", "lei-6091-1974",
         "Transporte gratuito de eleitores das zonas rurais (Lei nº 6.091, de 15 de agosto de 1974)", 2),
    _act("lei-da-saude-mental", "LSM", "l10216", "l10216", "lei-10216-2001",
         "Lei da Saúde Mental (Lei nº 10.216, de 6 de abril de 2001)", 2),
    _act("lei-dos-transplantes", "LTx", "l9434", "l9434-compilado", "lei-9434-1997",
         "Lei dos Transplantes (Lei nº 9.434, de 4 de fevereiro de 1997)", 2),
    _act("lei-do-piso-do-magisterio", "LPSPN", "l11738", "l11738", "lei-11738-2008",
         "Piso salarial profissional nacional do magistério público da educação básica (Lei nº 11.738, de 16 de julho de 2008)", 2),
    _act("lei-dos-mototaxistas", "LMoto", "l12009", "l12009", "lei-12009-2009",
         "Mototaxistas, motofretistas e motoboys (Lei nº 12.009, de 29 de julho de 2009)", 2),
    _act("lei-do-processamento-eletronico-eleitoral", "LPEE", "l6996", "l6996", "lei-6996-1982",
         "Processamento eletrônico de dados nos serviços eleitorais (Lei nº 6.996, de 7 de junho de 1982)", 2),
    _act("lei-das-mensalidades-escolares", "LMEsc", "l9870", "l9870", "lei-9870-1999",
         "Lei das Mensalidades Escolares (Lei nº 9.870, de 23 de novembro de 1999)", 2),
    _act("lei-do-plano-nacional-de-educacao", "PNE", "l13005", "l13005", "lei-13005-2014",
         "Plano Nacional de Educação - PNE (Lei nº 13.005, de 25 de junho de 2014)", 2),
    _act("lei-do-sistema-nacional-de-viacao", "LSNV", "l12379", "l12379", "lei-12379-2011",
         "Sistema Nacional de Viação - SNV (Lei nº 12.379, de 6 de janeiro de 2011)", 2),
    _act("lei-das-infracoes-sanitarias", "LIS", "l6437", "l6437-compilado", "lei-6437-1977",
         "Infrações à legislação sanitária federal (Lei nº 6.437, de 20 de agosto de 1977)", 2),
    _act("lei-do-regime-de-recuperacao-fiscal", "LC159", "lcp159", "lcp159", "lc-159-2017",
         "Regime de Recuperação Fiscal dos Estados e do Distrito Federal (Lei Complementar nº 159, de 19 de maio de 2017)", 2),
    _act("lei-do-plano-de-equilibrio-fiscal", "LC178", "lcp178", "lcp178", "lc-178-2021",
         "Programa de Acompanhamento e Transparência Fiscal e Plano de Promoção do Equilíbrio Fiscal (Lei Complementar nº 178, "
         "de 13 de janeiro de 2021)", 2),
    _act("lei-da-pessoa-com-deficiencia-de-1989", "L7853", "l7853", "l7853-compilado", "lei-7853-1989",
         "Apoio às pessoas portadoras de deficiência e Corde (Lei nº 7.853, de 24 de outubro de 1989)", 2),
    _act("lei-de-protecao-a-testemunhas", "LPT", "l9807", "l9807", "lei-9807-1999",
         "Proteção a vítimas e testemunhas ameaçadas (Lei nº 9.807, de 13 de julho de 1999)", 2),
    _act("lei-do-sinaes", "SINAES", "l10861", "l10861", "lei-10861-2004",
         "Sistema Nacional de Avaliação da Educação Superior - SINAES (Lei nº 10.861, de 14 de abril de 2004)", 2),
    {**_act("lei-de-inovacao", "LInov", "l10973", "l10973", "lei-10973-2004",
            "Lei de Inovação (Lei nº 10.973, de 2 de dezembro de 2004)", 2),
     "center_headings": False},   # chapter name lines are not centred: they were read as rubricas of the next article
    _act("lei-de-protecao-de-cultivares", "LPC", "l9456", "l9456", "lei-9456-1997",
         "Lei de Proteção de Cultivares (Lei nº 9.456, de 25 de abril de 1997)", 2),
    _act("lei-dos-agrotoxicos-de-1989", "LAgro", "l7802-2023", "l7802-2023", "lei-7802-1989",
         "Lei dos Agrotóxicos (Lei nº 7.802, de 11 de julho de 1989)", 2),
    _act("lei-da-radiodifusao-comunitaria", "LRC", "l9612", "l9612", "lei-9612-1998",
         "Serviço de Radiodifusão Comunitária (Lei nº 9.612, de 19 de fevereiro de 1998)", 2),
    _act("lei-da-alimentacao-escolar", "PNAE", "l11947", "l11947", "lei-11947-2009",
         "Alimentação escolar e Programa Dinheiro Direto na Escola (Lei nº 11.947, de 16 de junho de 2009)", 2),
    _act("lei-dos-agrotoxicos", "LAgro23", "l14785", "l14785", "lei-14785-2023",
         "Lei dos Agrotóxicos (Lei nº 14.785, de 27 de dezembro de 2023)", 2),
    _act("lei-do-credito-consignado", "LCons", "l10820", "l10820", "lei-10820-2003",
         "Desconto de prestações em folha de pagamento - crédito consignado (Lei nº 10.820, de 17 de dezembro de 2003)", 2),
    _act("lei-da-vigilancia-sanitaria-de-medicamentos", "LVSM", "l6360", "l6360", "lei-6360-1976",
         "Vigilância sanitária de medicamentos, drogas, insumos farmacêuticos, cosméticos e saneantes (Lei nº 6.360, de 23 de "
         "setembro de 1976)", 2),
    # read from the capture of 15.12.2020 (before the repeal); its consolidated check is the page as it is today
    _act("lei-do-fundeb-de-2007", "Fundeb07", "l11494-2020", "l11494", "lei-11494-2007",
         "Fundeb 2007-2020 (Lei nº 11.494, de 20 de junho de 2007)", 2),
    _act("lei-do-fundef", "Fundef", "l9424", "l9424", "lei-9424-1996",
         "Fundef e salário-educação (Lei nº 9.424, de 24 de dezembro de 1996)", 2),
    # twenty-second session
    _act("lei-da-previdencia-complementar", "LC109", "lcp109", "lcp109", "lc-109-2001",
         "Lei da Previdência Complementar (Lei Complementar nº 109, de 29 de maio de 2001)", 2),
    _act("lei-da-previdencia-complementar-do-setor-publico", "LC108", "lcp108", "lcp108", "lc-108-2001",
         "Previdência complementar patrocinada pelo setor público (Lei Complementar nº 108, de 29 de maio de 2001)", 2),
    _act("lei-da-cooperacao-ambiental", "LC140", "lcp140", "lcp140", "lc-140-2011",
         "Cooperação federativa em matéria ambiental (Lei Complementar nº 140, de 8 de dezembro de 2011)", 2),
    _act("lei-do-plebiscito-e-do-referendo", "LPR", "l9709", "l9709", "lei-9709-1998",
         "Plebiscito, referendo e iniciativa popular (Lei nº 9.709, de 18 de novembro de 1998)", 2),
    _act("lei-da-autonomia-do-banco-central", "LC179", "lcp179", "lcp179", "lc-179-2021",
         "Autonomia do Banco Central do Brasil (Lei Complementar nº 179, de 24 de fevereiro de 2021)", 2),
    _act("lei-do-mercado-de-cambio", "LCambio", "l14286", "l14286", "lei-14286-2021",
         "Lei do Mercado de Câmbio (Lei nº 14.286, de 29 de dezembro de 2021)", 2),
    _act("lei-do-gas", "LGas", "l14134", "l14134", "lei-14134-2021",
         "Lei do Gás (Lei nº 14.134, de 8 de abril de 2021)", 2),
    _act("estatuto-do-ministerio-publico-da-uniao", "LOMPU", "lcp75", "lcp75", "lc-75-1993",
         "Estatuto do Ministério Público da União (Lei Complementar nº 75, de 20 de maio de 1993)", 2),
    _act("lei-organica-da-defensoria-publica", "LODP", "lcp80", "lcp80", "lc-80-1994",
         "Lei Orgânica da Defensoria Pública (Lei Complementar nº 80, de 12 de janeiro de 1994)", 2),
    _act("lei-de-conflito-de-interesses", "LCI", "l12813", "l12813", "lei-12813-2013",
         "Lei de Conflito de Interesses (Lei nº 12.813, de 16 de maio de 2013)", 2),
    _act("lei-das-cautelares-contra-o-poder-publico", "LCPP", "l8437", "l8437", "lei-8437-1992",
         "Medidas cautelares contra atos do Poder Público (Lei nº 8.437, de 30 de junho de 1992)", 2),
    _act("lei-da-tutela-antecipada-contra-a-fazenda-publica", "LTAFP", "l9494", "l9494", "lei-9494-1997",
         "Tutela antecipada contra a Fazenda Pública (Lei nº 9.494, de 10 de setembro de 1997)", 2),
    _act("lei-do-governo-digital", "LGD", "l14129", "l14129", "lei-14129-2021",
         "Lei do Governo Digital (Lei nº 14.129, de 29 de março de 2021)", 2),
    # twenty-third session
    _act("decreto-lei-200-de-1967", "DL200", "del0200", "del0200", "dl-200-1967",
         "Organização da Administração Federal e Reforma Administrativa (Decreto-Lei nº 200, de 25 de fevereiro de 1967)", 3)
    | {"center_headings": False},   # headings are <h4>/<h5> blocks, not centred: a Título's name line went into the article above
    _act("lei-da-partilha-de-producao", "LPartilha", "l12351", "l12351", "lei-12351-2010",
         "Partilha de produção do pré-sal e Fundo Social (Lei nº 12.351, de 22 de dezembro de 2010)", 2),
    _act("lei-organica-nacional-do-ministerio-publico", "LONMP", "l8625", "l8625", "lei-8625-1993",
         "Lei Orgânica Nacional do Ministério Público (Lei nº 8.625, de 12 de fevereiro de 1993)", 2),
    _act("lei-do-programa-bolsa-familia", "LPBF", "l14601", "l14601", "lei-14601-2023",
         "Programa Bolsa Família (Lei nº 14.601, de 19 de junho de 2023)", 2),
    # twenty-fourth session
    _act("lei-da-previdencia-complementar-dos-servidores-federais", "LFunpresp", "l12618", "l12618", "lei-12618-2012",
         "Previdência complementar dos servidores públicos federais - Funpresp (Lei nº 12.618, de 30 de abril de 2012)", 2),
    _act("lei-12865-de-2013", "L12865", "l12865", "l12865", "lei-12865-2013",
         "Arranjos e instituições de pagamento, e outras matérias (Lei nº 12.865, de 9 de outubro de 2013)", 2),
    # twenty-fifth session
    _act("lei-da-poluicao-por-oleo", "LOleo", "l9966", "l9966", "lei-9966-2000",
         "Poluição por óleo e substâncias nocivas em águas sob jurisdição nacional (Lei nº 9.966, de 28 de abril de 2000)", 2),
    _act("lei-da-pesca", "LPesca", "l11959", "l11959", "lei-11959-2009",
         "Política Nacional de Desenvolvimento Sustentável da Aquicultura e da Pesca (Lei nº 11.959, de 29 de junho de 2009)", 2),
    _act("lei-da-comercializacao-de-energia-eletrica", "LCEE", "l10848", "l10848", "lei-10848-2004",
         "Comercialização de energia elétrica (Lei nº 10.848, de 15 de março de 2004)", 2),
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
    "y": ["lei-da-ans", "lei-9717-de-1998"],   # MP reissue editions keyed per edition (batch 18 reader, batch6)
    "z": ["lei-da-aneel"],
    "za": ["lei-da-contratacao-temporaria"],
    "zb": ["lei-da-anvisa"],
    "zc": ["lei-da-participacao-nos-lucros", "lei-do-servico-voluntario", "lei-do-aviso-previo"],
    "zd": ["lei-de-seguranca-de-barragens", "lei-do-sigilo-bancario"],
    "zf": ["lei-da-ana"],   # configured, not published (MP 844/868 chain, MP 437 fate): see PROGRESS
    "zg": ["lei-da-anac", "lei-da-anm"],
    "zh": ["lei-da-mata-atlantica", "lei-dos-representantes-comerciais", "lei-da-medida-cautelar-fiscal",
           "lei-da-educacao-ambiental"],
    "zi": ["lei-da-sumula-vinculante", "lei-dos-usuarios-de-servicos-publicos", "lei-da-politica-nacional-sobre-mudanca-do-clima",
           "lei-da-biodiversidade"],
    "zj": ["lei-9718-de-1998"],
    "zk": ["lei-10637-de-2002"],
    "zl": ["lei-10833-de-2003"],
    "zm": ["lei-do-financiamento-da-saude", "lei-do-fundeb"],
    "zn": ["lei-do-cadastro-positivo", "lei-do-regime-fiscal-sustentavel"],
    "zo": ["lei-do-transporte-rodoviario-de-cargas", "lei-do-vale-pedagio", "lei-do-transporte-multimodal"],
    "zp": ["lei-de-gestao-de-florestas-publicas", "lei-do-pagamento-por-servicos-ambientais"],
    "zq": ["lei-do-transporte-de-eleitores", "lei-da-saude-mental", "lei-dos-transplantes"],
    # lei-do-piso-do-magisterio (Lei 11.738/2008) configured but in no part: Lei 15.437/2026 (31 notes) has no archive.org capture
    # lei-dos-mototaxistas (Lei 12.009/2009) configured but in no part: Medida Provisória 1.360/2026 (art. 2) lapsed ('Vigência
    # encerrada', Ato adc-96-mpv1.360): the Ato has no archive.org capture, so the lapse day cannot be read
    "zr": ["lei-do-processamento-eletronico-eleitoral", "lei-das-mensalidades-escolares"],
    "zs": ["lei-do-plano-nacional-de-educacao", "lei-do-sistema-nacional-de-viacao"],
    "zt": ["lei-das-infracoes-sanitarias"],
    "zu": ["lei-do-regime-de-recuperacao-fiscal", "lei-do-plano-de-equilibrio-fiscal"],
    "zv": ["lei-da-pessoa-com-deficiencia-de-1989", "lei-de-protecao-a-testemunhas", "lei-do-sinaes"],
    "zw": ["lei-de-inovacao", "lei-de-protecao-de-cultivares"],
    "zx": ["lei-dos-agrotoxicos-de-1989"],
    "zy": ["lei-da-radiodifusao-comunitaria", "lei-da-alimentacao-escolar"],
    "zz": ["lei-dos-agrotoxicos"],
    "zza": ["lei-do-credito-consignado"],
    "zzb": ["lei-da-vigilancia-sanitaria-de-medicamentos"],
    "zzc": ["lei-do-fundeb-de-2007"],
    "zzd": ["lei-do-fundef"],
    # twenty-second session (fresh ranked list)
    "zze": ["lei-da-previdencia-complementar", "lei-da-previdencia-complementar-do-setor-publico"],
    "zzf": ["lei-da-cooperacao-ambiental", "lei-do-plebiscito-e-do-referendo"],
    "zzg": ["lei-da-autonomia-do-banco-central", "lei-do-mercado-de-cambio"],
    "zzh": ["lei-do-gas", "estatuto-do-ministerio-publico-da-uniao"],
    "zzi": ["lei-organica-da-defensoria-publica"],
    "zzj": ["lei-de-conflito-de-interesses", "lei-das-cautelares-contra-o-poder-publico"],
    "zzk": ["lei-da-tutela-antecipada-contra-a-fazenda-publica"],
    "zzl": ["lei-do-governo-digital"],
    # twenty-third session
    "zzm": ["decreto-lei-200-de-1967"],
    "zzn": ["lei-da-partilha-de-producao"],
    "zzo": ["lei-organica-nacional-do-ministerio-publico", "lei-do-programa-bolsa-familia"],
    # twenty-fourth session
    "zzp": ["lei-da-previdencia-complementar-dos-servidores-federais"],
    "zzq": ["lei-12865-de-2013"],
    "zzr": ["lei-da-comercializacao-de-energia-eletrica"],
    "zzs": ["lei-da-poluicao-por-oleo", "lei-da-pesca"],
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
# Lei 14.785/2023's ementa: the law entry of part zx (EXTRA_LAWS) and of part zz (its own act) must be identical
_T14785 = ("Dispõe sobre a pesquisa, a experimentação, a produção, a embalagem, a rotulagem, o transporte, o armazenamento, a "
           "comercialização, a utilização, a importação, a exportação, o destino final dos resíduos e das embalagens, o registro, a "
           "classificação, o controle, a inspeção e a fiscalização de agrotóxicos, de produtos de controle ambiental, de seus "
           "produtos técnicos e afins; revoga as Leis nºs 7.802, de 11 de julho de 1989, e 9.974, de 6 de junho de 2000, e partes "
           "de anexos das Leis nºs 6.938, de 31 de agosto de 1981, e 9.782, de 26 de janeiro de 1999.")
# Lei 14.286/2021's ementa: as 99-batch13f and 99-batch17g have the law record
_T14286 = 'Dispõe sobre o mercado de câmbio brasileiro, o capital brasileiro no exterior, o capital estrangeiro no País e a prestação de informações ao Banco Central do Brasil; altera as Leis n os 4.131, de 3 de setembro de 1962, 4.728, de 14 de julho de 1965, 8.383, de 30 de dezembro de 1991, 10.192, de 14 de fevereiro de 2001, e 11.371, de 28 de novembro de 2006, e o Decreto nº 23.258, de 19 de outubro de 1933; e revoga as Leis n os 156, de 27 de novembro de 1947, 1.383, de 13 de junho de 1951, 1.807, de 7 de janeiro de 1953, 2.145, de 29 de dezembro de 1953, 2.698, de 27 de dezembro de 1955, 4.390, de 29 de agosto de 1964, 5.331, de 11 de outubro de 1967, 9.813, de 23 de agosto de 1999, e 13.017, de 21 de julho de 2014, os Decretos-Leis n os 1.201, de 8 de abril de 1939, 9.025, de 27 de fevereiro de 1946, 9.602, de 16 de agosto de 1946, 9.863, de 13 de setembro de 1946, e 857, de 11 de setembro de 1969, a Medida Provisória nº 2.224, de 4 de setembro de 2001, e dispositivos das Leis n os 4.182, de 13 de novembro de 1920, 3.244, de 14 de agosto de 1957, 4.595, de 31 de dezembro de 1964, 5.409, de 9 de abril de 1968, 6.099, de 12 de setembro de 1974, 7.738, de 9 de março de 1989, 8.021, de 12 de abril de 1990, 8.880, de 27 de maio de 1994, 9.069, de 29 de junho de 1995, 9.529, de 10 de dezembro de 1997, 11.803, de 5 de novembro de 2008, 12.865, de 9 de outubro de 2013, 13.292, de 31 de maio de 2016, e 13.506, de 13 de novembro de 2017, e dos Decretos-Leis n os 2.440, de 23 de julho de 1940, 1.060, de 21 de outubro de 1969, 1.986, de 28 de dezembro de 1982, e 2.285, de 23 de julho de 1986.'
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
    "lei-9961-2000": ("2000-01-29", f"Lei 9.961/2000 art. 41: {_PUB} (DOU 29.1.2000)"),
    "lei-9717-1998": ("1998-11-28", f"Lei 9.717/1998 art. 11: {_PUB} (DOU 28.11.1998)"),
    "lei-9427-1996": ("1996-12-27", f"Lei 9.427/1996 art. 35: {_PUB} (DOU 27.12.1996, republished 28.9.1998)"),
    "lei-9782-1999": ("1999-01-27", f"Lei 9.782/1999 art. 45: {_PUB} (DOU 27.1.1999)"),
    "lei-8745-1993": ("1993-12-10", f"Lei 8.745/1993 art. 17: {_PUB} (DOU 10.12.1993)"),
    "lei-10101-2000": ("2000-12-20", f"Lei 10.101/2000 art. 8: {_PUB} (DOU 20.12.2000)"),
    "lei-9608-1998": ("1998-02-19", f"Lei 9.608/1998 art. 4: {_PUB} (DOU 19.2.1998)"),
    "lei-12506-2011": ("2011-10-13", f"Lei 12.506/2011 art. 2: {_PUB} (DOU 13.10.2011)"),
    "lei-9984-2000": ("2000-07-18", f"Lei 9.984/2000 art. 33: {_PUB} (DOU 18.7.2000)"),
    "lei-12334-2010": ("2010-09-21", f"Lei 12.334/2010 art. 23: {_PUB} (DOU 21.9.2010)"),
    "lc-105-2001": ("2001-01-11", "Lei Complementar 105/2001 art. 12: 'Esta Lei Complementar entra em vigor na data de sua "
                                  "publicação' (DOU 11.1.2001)"),
    "lei-11182-2005": ("2005-09-28", f"Lei 11.182/2005 art. 51: {_PUB} (DOU 28.9.2005)"),
    "lei-13575-2017": ("2017-12-27", "Lei 13.575/2017 art. 38: 'Esta Lei entra em vigor: I - (VETADO); II - quanto aos demais "
                                     "dispositivos, na data de sua publicação' (DOU 27.12.2017)"),
    "lei-11428-2006": ("2006-12-26", f"Lei 11.428/2006 art. 51: {_PUB} (DOU 26.12.2006)"),
    "lei-4886-1965": ("1965-12-10", "Lei 4.886/1965 art. 48: 'Esta lei entra em vigor na data de sua publicação' (DOU 10.12.1965)"),
    "lei-8397-1992": ("1992-01-07", "Lei 8.397/1992 art. 19: 'Esta lei entra em vigor na data de sua publicação' (DOU 7.1.1992)"),
    "lei-9795-1999": ("1999-04-28", f"Lei 9.795/1999 art. 21: {_PUB} (DOU 28.4.1999)"),
    "lei-11417-2006": ("2007-03-20", "Lei 11.417/2006 art. 11: 'Esta Lei entra em vigor 3 (três) meses após a sua publicação' (DOU "
                                     "20.12.2006): in force on 20.3.2007"),
    "lei-13460-2017": ("2018-06-22", "Lei 13.460/2017 art. 25: 'Esta Lei entra em vigor, a contar da sua publicação, em: I - trezentos "
                                     "e sessenta dias para a União, os Estados, o Distrito Federal e os Municípios com mais de quinhentos "
                                     "mil habitantes; II - quinhentos e quarenta dias para os Municípios entre cem mil e quinhentos mil "
                                     "habitantes; e III - setecentos e vinte dias para os Municípios com menos de cem mil habitantes' (DOU "
                                     "27.6.2017): dated by I, the federal stage, 360 days counted from the day of publication (LC 95 art. 8 "
                                     "§ 1º), in force on 22.6.2018"),
    "lei-12187-2009": ("2009-12-30", f"Lei 12.187/2009 art. 13: {_PUB} (DOU 30.12.2009, edição extra)"),
    "lei-13123-2015": ("2015-11-17", "Lei 13.123/2015 art. 49: 'Esta Lei entra em vigor após decorridos 180 (cento e oitenta) dias da "
                                     "data de sua publicação oficial' (DOU 21.5.2015, from LexML; Planalto's footer misprints '14.5.2015'): "
                                     "in force on 17.11.2015"),
    "lei-9718-1998": ("1998-11-28", "Lei 9.718/1998 art. 17: 'Esta Lei entra em vigor na data de sua publicação, produzindo efeitos: "
                                    "I - em relação aos arts. 2º a 8º, para os fatos geradores ocorridos a partir de 1º de fevereiro "
                                    "de 1999; II - em relação aos arts. 9º e 12 a 15, a partir de 1º de janeiro de 1999' (DOU "
                                    "28.11.1998): the other articles from publication; arts. 9 and 12 to 15 from 1.1.1999 and arts. 2 "
                                    "to 8 from 1.2.1999, the days they take effect"),
    "lei-10637-2002": ("2002-12-31", "Lei 10.637/2002 art. 68: 'Esta Lei entra em vigor na data de sua publicação, produzindo efeitos: "
                                     "I - a partir de 1º de outubro de 2002, em relação aos arts. 29 e 49; II - a partir de 1º de dezembro "
                                     "de 2002, em relação aos arts. 1º a 6º e 8º a 11; III - a partir de 1º de janeiro de 2003, em relação "
                                     "aos arts. 34, 37 a 44, 46 e 48; IV - a partir da data da publicação desta Lei, em relação aos demais "
                                     "artigos' (DOU 31.12.2002, edição extra): every article from publication (the effects under I and II "
                                     "reach back before it), arts. 34, 37 to 44, 46 and 48 from 1.1.2003, the day they take effect"),
    "lei-10833-2003": ("2003-12-30", "Lei 10.833/2003 art. 93: 'Esta Lei entra em vigor na data de sua publicação, produzindo efeitos, "
                                     "em relação: I - aos arts. 1º a 15 e 25, a partir de 1º de fevereiro de 2004; II - aos arts. 26, 27, "
                                     "29, 30 e 34 desta Lei, a partir de 1º de fevereiro de 2004; [...] IV - aos arts. 49 a 51 e 53 a 58 "
                                     "desta Lei, a partir do 1º dia do quarto mês subseqüente ao de sua publicação; V - ao art. 52 desta "
                                     "Lei, a partir do 1º dia do segundo mês subseqüente ao de publicação desta Lei; VI - aos demais "
                                     "artigos, a partir da data da publicação desta Lei' (DOU 30.12.2003, edição extra-A): the other "
                                     "articles from publication; arts. 1 to 15, 25 to 27, 29, 30, 34 and 52 from 1.2.2004 and arts. 49 to "
                                     "51 and 53 to 58 from 1.4.2004, the days they take effect"),
    "lc-141-2012": ("2012-01-16", "Lei Complementar 141/2012 art. 48: 'Esta Lei Complementar entra em vigor na data de sua "
                                  "publicação' (DOU 16.1.2012)"),
    "lei-14113-2020": ("2020-12-25", "Lei 14.113/2020 art. 54: 'Esta Lei entra em vigor na data da sua publicação' (DOU 25.12.2020, "
                                     "edição extra)"),
    "lei-12414-2011": ("2011-06-10", f"Lei 12.414/2011 art. 18: {_PUB} (DOU 10.6.2011)"),
    "lc-200-2023": ("2023-08-31", "Lei Complementar 200/2023 art. 15: 'Esta Lei Complementar entra em vigor: I - em 1º de janeiro de "
                                  "2024, quanto ao art. 11; e II - na data de sua publicação, quanto aos demais dispositivos' (DOU "
                                  "31.8.2023): every article from publication, art. 11 from 1.1.2024, the day it takes effect"),
    "lei-11442-2007": ("2007-01-08", "Lei 11.442/2007 art. 23: 'Esta Lei entra em vigor na data de sua publicação [...]' (DOU 8.1.2007)"),
    "lei-10209-2001": ("2001-03-24", f"Lei 10.209/2001 art. 11: {_PUB} (DOU 24.3.2001, edição extra)"),
    "lei-9611-1998": ("1998-02-20", f"Lei 9.611/1998 art. 34: {_PUB} (DOU 20.2.1998)"),
    "lei-11284-2006": ("2006-03-03", f"Lei 11.284/2006 art. 86: {_PUB} (DOU 3.3.2006)"),
    "lei-14119-2021": ("2021-01-14", f"Lei 14.119/2021 art. 26: {_PUB} (DOU 14.1.2021, rectified 15.1.2021)"),
    "lei-6091-1974": ("1974-08-15", "Lei 6.091/1974 art. 28: 'Esta Lei entra em vigor na data de sua publicação, revogadas as disposições "
                                    "em contrário' (DOU 15.8.1974)"),
    "lei-10216-2001": ("2001-04-09", f"Lei 10.216/2001 art. 13: {_PUB} (DOU 9.4.2001)"),
    "lei-9434-1997": ("1997-03-22", "Lei 9.434/1997 has no in-force clause (art. 25 only revokes): in force 45 days after its publication "
                                    "(LINDB art. 1; DOU 5.2.1997), on 22.3.1997"),
    "lei-11738-2008": ("2008-07-17", f"Lei 11.738/2008 art. 8: {_PUB} (DOU 17.7.2008)"),
    "lei-12009-2009": ("2009-07-30", f"Lei 12.009/2009 art. 9: {_PUB} (DOU 30.7.2009)"),
    "lei-6996-1982": ("1982-06-08", f"Lei 6.996/1982 art. 19: {_PUB} (DOU 8.6.1982)"),
    "lei-9870-1999": ("1999-11-24", f"Lei 9.870/1999 art. 11: {_PUB} (DOU 24.11.1999, edição extra)"),
    "lei-13005-2014": ("2014-06-26", f"Lei 13.005/2014 art. 14: {_PUB} (DOU 26.6.2014, edição extra)"),
    "lei-12379-2011": ("2011-01-07", f"Lei 12.379/2011 art. 44: {_PUB} (DOU 7.1.2011)"),
    "lei-6437-1977": ("1977-08-24", "Lei 6.437/1977 art. 39: 'Esta Lei entrará em vigor na data de sua publicação' (DOU 24.8.1977)"),
    "lc-159-2017": ("2017-05-22", "Lei Complementar 159/2017 art. 18: 'Esta Lei Complementar entra em vigor na data de sua "
                                  "publicação' (DOU 22.5.2017)"),
    "lc-178-2021": ("2021-01-14", "Lei Complementar 178/2021 art. 32: 'Esta Lei Complementar entra em vigor: I - em relação a seu "
                                  "art. 16, especificamente no que altera o art. 51 da Lei Complementar nº 101 [...] a partir de 2022; "
                                  "II - [...] no que altera o art. 42 [...] a partir de 2023; III - em relação às demais disposições, "
                                  "na data de sua publicação' (DOU 14.1.2021): its own articles from publication (the staged items "
                                  "concern Lei Complementar 101's text)"),
    "lei-7853-1989": ("1989-10-25", f"Lei 7.853/1989 art. 19: {_PUB} (DOU 25.10.1989)"),
    "lei-9807-1999": ("1999-07-14", f"Lei 9.807/1999 art. 21: {_PUB} (DOU 14.7.1999)"),
    "lei-10861-2004": ("2004-04-15", f"Lei 10.861/2004 art. 15: {_PUB} (DOU 15.4.2004)"),
    "lei-10973-2004": ("2004-12-03", f"Lei 10.973/2004 art. 29: {_PUB} (DOU 3.12.2004, rectified 16.5.2005)"),
    "lei-9456-1997": ("1997-04-28", f"Lei 9.456/1997 art. 55: {_PUB} (DOU 28.4.1997, as LexML's record of the original "
                                    "publication gives it; Planalto's page misprints '8.4.1997', before the Lei's own date; "
                                    "rectified 26.8.1997 and 25.9.1997)"),
    "lei-7802-1989": ("1989-07-12", f"Lei 7.802/1989 art. 22: {_PUB} (DOU 12.7.1989)"),
    "lei-9612-1998": ("1998-02-20", f"Lei 9.612/1998 art. 26: {_PUB} (DOU 20.2.1998)"),
    "lei-11947-2009": ("2009-06-17", f"Lei 11.947/2009 art. 35: {_PUB} (DOU 17.6.2009)"),
    "lei-14785-2023": ("2023-12-28", f"Lei 14.785/2023 art. 66: {_PUB} (DOU 28.12.2023, rectified 16.4.2024)"),
    "lei-10820-2003": ("2003-12-18", f"Lei 10.820/2003 art. 9: {_PUB} (DOU 18.12.2003)"),
    "lei-6360-1976": ("1976-12-28", "Lei 6.360/1976 art. 88: 'Esta Lei entrará em vigor 95 (noventa e cinco) dias depois de sua "
                                    "publicação' (DOU 24.9.1976; 95 days after 24.9.1976 is 28.12.1976)"),
    "lei-11494-2007": ("2007-06-21", "Lei 11.494/2007 art. 49: 'Esta Lei entra em vigor na data da sua publicação' (DOU "
                                     "21.6.2007, rectified 22.6.2007)"),
    "lei-9424-1996": ("1997-01-01", "Lei 9.424/1996 art. 16: 'Esta Lei entra em vigor em 1º de janeiro de 1997' (DOU 26.12.1996)"),
    "lc-109-2001": ("2001-05-30", "Lei Complementar 109/2001 art. 78: 'Esta Lei Complementar entra em vigor na data de sua "
                                  "publicação' (DOU 30.5.2001)"),
    "lc-108-2001": ("2001-05-30", "Lei Complementar 108/2001 art. 31: 'Esta Lei Complementar entra em vigor na data de sua "
                                  "publicação' (DOU 30.5.2001)"),
    "lc-140-2011": ("2011-12-09", "Lei Complementar 140/2011 art. 22: 'Esta Lei Complementar entra em vigor na data de sua "
                                  "publicação' (DOU 9.12.2011, rectified 12.12.2011)"),
    "lei-9709-1998": ("1998-11-19", f"Lei 9.709/1998 art. 15: {_PUB} (DOU 19.11.1998)"),
    "lc-179-2021": ("2021-02-25", "Lei Complementar 179/2021 art. 14: 'Esta Lei Complementar entra em vigor na data de sua "
                                  "publicação' (DOU 25.2.2021)"),
    "lei-14286-2021": ("2022-12-30", "Lei 14.286/2021 art. 29: 'Esta Lei entra em vigor após decorrido 1 (um) ano de sua "
                                     "publicação oficial' (DOU 30.12.2021): one year after publication, 30.12.2022 (as Lei "
                                     "13.431/2017, same clause)"),
    "lei-14134-2021": ("2021-04-09", f"Lei 14.134/2021 art. 49: {_PUB} (DOU 9.4.2021)"),
    "lc-75-1993": ("1993-05-21", "Lei Complementar 75/1993 art. 294: 'Esta lei complementar entra em vigor na data de sua "
                                 "publicação' (DOU 21.5.1993)"),
    "lc-80-1994": ("1994-01-13", "Lei Complementar 80/1994 art. 148: 'Esta Lei Complementar entra em vigor na data de sua "
                                 "publicação' (DOU 13.1.1994)"),
    "lei-12813-2013": ("2013-07-01", "Lei 12.813/2013: its arts. 14 and 15 (the closing articles) were vetoed, so it has no "
                                     "vigência clause: LINDB art. 1, 45 days after DOU 17.5.2013 (rectified 20.5.2013): "
                                     "1.7.2013"),
    "lei-8437-1992": ("1992-07-01", "Lei 8.437/1992 art. 5: 'Esta lei entra em vigor na data de sua publicação' (DOU 1.7.1992)"),
    "lei-9494-1997": ("1997-09-11", f"Lei 9.494/1997 art. 4: {_PUB} (DOU 11.9.1997, as LexML's record of the publication gives "
                                    "it; Planalto's footer misprints 'D.O.U. de 24.12.1997')"),
    "lei-14129-2021": ("2021-06-28", "Lei 14.129/2021 art. 55: 'Esta Lei entra em vigor após decorridos: I - 90 (noventa) dias de "
                                     "sua publicação oficial, para a União; II - 120 (cento e vinte) dias [...] para os Estados e o "
                                     "Distrito Federal; III - 180 (cento e oitenta) dias [...] para os Municípios' (DOU 30.3.2021, "
                                     "republished 14.4.2021): dated by its federal stage, 90 days, 28.6.2021 (as for Lei 13.460 in "
                                     "part zi); the later stages are an open item"),
    "dl-200-1967": ("1967-03-15", "Decreto-Lei 200/1967 art. 214: 'Esta Lei entrará em vigor em 15 de março de 1967, observado o "
                                  "disposto nos parágrafos do presente artigo e ressalvadas as disposições cuja vigência, na data da "
                                  "publicação, seja por ela expressamente determinada' (DOU 27.2.1967, rectified 8.3.1967, 30.3.1967 "
                                  "and 17.7.1967)"),
    "lei-12351-2010": ("2010-12-23", f"Lei 12.351/2010 art. 68: {_PUB} (DOU 23.12.2010)"),
    "lei-8625-1993": ("1993-02-15", "Lei 8.625/1993 art. 83: 'Esta lei entra em vigor na data de sua publicação' (DOU 15.2.1993)"),
    "lei-14601-2023": ("2023-06-20", "Lei 14.601/2023 art. 34: 'Esta Lei entra em vigor: I - em 1º de janeiro de 2024, quanto: a) aos "
                                     "arts. 30 e 31 e ao inciso I do caput do art. 33; b) ao § 3º do art. 4º; e II - na data de sua "
                                     "publicação, quanto aos demais dispositivos' (DOU 20.6.2023)"),
    "lei-12618-2012": ("2012-05-02", "Lei 12.618/2012 art. 33: 'Esta Lei entra em vigor: I - quanto ao disposto no Capítulo I, na "
                                     "data em que forem criadas quaisquer das entidades de que trata o art. 4º, observado o disposto "
                                     "no art. 31; e II - quanto aos demais dispositivos, na data de sua publicação' (DOU 2.5.2012); "
                                     "Capítulo I (arts. 1 to 3) from 21.9.2012, the day the first of those entities was created "
                                     "(Decreto 7.808/2012)"),
    "lei-12865-2013": ("2013-10-10", "Lei 12.865/2013 art. 43: 'Esta Lei entra em vigor: I - a partir do primeiro dia do quarto mês "
                                     "subsequente ao de sua publicação, em relação ao disposto no art. 34 desta Lei; II - na data de "
                                     "sua publicação, para os demais dispositivos' (DOU 10.10.2013): art. 34 from 1.2.2014"),
    "lei-10848-2004": ("2004-03-16", f"Lei 10.848/2004 art. 33: {_PUB} (DOU 16.3.2004)"),
    "lei-9966-2000": ("2000-07-28", "Lei 9.966/2000 art. 34: 'Esta Lei entra em vigor noventa dias da data de sua publicação' (DOU "
                                    "29.4.2000): 90 days after 29.4.2000, 28.7.2000"),
    "lei-11959-2009": ("2009-08-29", "Lei 11.959/2009 art. 37: 'Esta Lei entra em vigor após decorridos 60 (sessenta) dias de sua "
                                     "publicação oficial' (DOU 30.6.2009): 60 days after 30.6.2009, 29.8.2009"),
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
    "lei-13465-2017": _L("Lei nº 13.465, de 2017", "Dispõe sobre a regularização fundiária rural e urbana, sobre a liquidação de créditos concedidos aos"
                         " assentados da reforma agrária e sobre a regularização fundiária no âmbito da Amazônia Legal; "
                         "institui mecanismos para aprimorar a eficiência dos procedimentos de alienação de imóveis da União; "
                         "altera as Leis n os 8.629, de 25 de fevereiro de 1993, 13.001, de 20 de junho de 2014, 11.952, de 25"
                         " de junho de 2009, 13.340, de 28 de setembro de 2016, 8.666, de 21 de junho de 1993, 6.015, de 31 de"
                         " dezembro de 1973, 12.512, de 14 de outubro de 2011, 10.406, de 10 de janeiro de 2002 (Código "
                         "Civil), 13.105, de 16 de março de 2015 (Código de Processo Civil), 11.977, de 7 de julho de 2009, "
                         "9.514, de 20 de novembro de 1997, 11.124, de 16 de junho de 2005, 6.766, de 19 de dezembro de 1979, "
                         "10.257, de 10 de julho de 2001, 12.651, de 25 de maio de 2012, 13.240, de 30 de dezembro de 2015, "
                         "9.636, de 15 de maio de 1998, 8.036, de 11 de maio de 1990, 13.139, de 26 de junho de 2015, 11.483, "
                         "de 31 de maio de 2007, e a 12.712, de 30 de agosto de 2012, a Medida Provisória nº 2.220, de 4 de "
                         "setembro de 2001, e os Decretos-Leis nº 2.398, de 21 de dezembro de 1987, 1.876, de 15 de julho de "
                         "1981, 9.760, de 5 de setembro de 1946, e 3.365, de 21 de junho de 1941; revoga dispositivos da Lei "
                         "Complementar nº 76, de 6 de julho de 1993, e da Lei nº 13.347, de 10 de outubro de 2016; e dá outras"
                         " providências.", "2017-07-11", "2017-07-12", PAGES["l13465"]),
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
    "lei-9961-2000": _L("Lei nº 9.961, de 2000", "Cria a Agência Nacional de Saúde Suplementar – ANS e dá outras providências.",
                        "2000-01-28", "2000-01-29", PAGES["l9961"]),
    "lei-9717-1998": _L("Lei nº 9.717, de 1998", "Dispõe sobre regras gerais para a organização e o funcionamento dos regimes "
                        "próprios de previdência social dos servidores públicos [...] e dá outras providências.", "1998-11-27",
                        "1998-11-28", PAGES["l9717"]),
    "lei-9427-1996": _L("Lei nº 9.427, de 1996", "Institui a Agência Nacional de Energia Elétrica - ANEEL, disciplina o regime das "
                        "concessões de serviços públicos de energia elétrica e dá outras providências.", "1996-12-26",
                        "1996-12-27", PAGES["l9427"]),
    "lei-9782-1999": _L("Lei nº 9.782, de 1999", "Define o Sistema Nacional de Vigilância Sanitária, cria a Agência Nacional de "
                        "Vigilância Sanitária, e dá outras providências.", "1999-01-26", "1999-01-27", PAGES["l9782"]),
    "lei-8745-1993": _L("Lei nº 8.745, de 1993", "Dispõe sobre a contratação por tempo determinado para atender a necessidade "
                        "temporária de excepcional interesse público, nos termos do inciso IX do art. 37 da Constituição Federal, "
                        "e dá outras providências.", "1993-12-09", "1993-12-10", PAGES["l8745"]),
    "lei-10101-2000": _L("Lei nº 10.101, de 2000", "Dispõe sobre a participação dos trabalhadores nos lucros ou resultados da "
                         "empresa e dá outras providências.", "2000-12-19", "2000-12-20", PAGES["l10101"]),
    "lei-9608-1998": _L("Lei nº 9.608, de 1998", "Dispõe sobre o serviço voluntário e dá outras providências.", "1998-02-18",
                        "1998-02-19", PAGES["l9608"]),
    "lei-12506-2011": _L("Lei nº 12.506, de 2011", "Dispõe sobre o aviso prévio e dá outras providências.", "2011-10-11",
                         "2011-10-13", PAGES["l12506"]),
    "lei-9984-2000": _L("Lei nº 9.984, de 2000", "Dispõe sobre a criação da Agência Nacional de Águas - ANA, entidade federal de implementação da "
                        "Política Nacional de Recursos Hídricos e de coordenação do Sistema Nacional de Gerenciamento de "
                        "Recursos Hídricos, e dá outras providências.", "2000-07-17", "2000-07-18", PAGES["l9984"]),
    "lei-12334-2010": _L("Lei nº 12.334, de 2010", "Estabelece a Política Nacional de Segurança de Barragens [...].", "2010-09-20",
                         "2010-09-21", PAGES["l12334"]),
    "lc-105-2001": _L("Lei Complementar nº 105, de 2001", "Dispõe sobre o sigilo das operações de instituições financeiras e dá "
                      "outras providências.", "2001-01-10", "2001-01-11", PAGES["lcp105"]),
    "lei-11182-2005": _L("Lei nº 11.182, de 2005", "Cria a Agência Nacional de Aviação Civil – ANAC, e dá outras providências.",
                         "2005-09-27", "2005-09-28", PAGES["l11182"]),
    "lei-13575-2017": _L("Lei nº 13.575, de 2017", "Cria a Agência Nacional de Mineração (ANM); extingue o Departamento Nacional de "
                         "Produção Mineral (DNPM) [...].", "2017-12-26", "2017-12-27", PAGES["l13575"]),
    "lei-11428-2006": _L("Lei nº 11.428, de 2006", "Dispõe sobre a utilização e proteção da vegetação nativa do Bioma Mata "
                         "Atlântica, e dá outras providências.", "2006-12-22", "2006-12-26", PAGES["l11428"]),
    "lei-4886-1965": _L("Lei nº 4.886, de 1965", "Regula as atividades dos representantes comerciais autônomos.", "1965-12-09",
                        "1965-12-10", PAGES["l4886"]),
    "lei-8397-1992": _L("Lei nº 8.397, de 1992", "Institui medida cautelar fiscal e dá outras providências.", "1992-01-06",
                        "1992-01-07", PAGES["l8397"]),
    "lei-9795-1999": _L("Lei nº 9.795, de 1999", "Dispõe sobre a educação ambiental, institui a Política Nacional de Educação "
                        "Ambiental e dá outras providências.", "1999-04-27", "1999-04-28", PAGES["l9795"]),
    "lei-11417-2006": _L("Lei nº 11.417, de 2006", "Regulamenta o art. 103-A da Constituição Federal e altera a Lei nº 9.784, de 29 "
                         "de janeiro de 1999, disciplinando a edição, a revisão e o cancelamento de enunciado de súmula vinculante "
                         "pelo Supremo Tribunal Federal, e dá outras providências.", "2006-12-19", "2006-12-20", PAGES["l11417"]),
    "lei-13460-2017": _L("Lei nº 13.460, de 2017", "Dispõe sobre participação, proteção e defesa dos direitos do usuário dos serviços "
                         "públicos da administração pública.", "2017-06-26", "2017-06-27", PAGES["l13460"]),
    "lei-12187-2009": _L("Lei nº 12.187, de 2009", "Institui a Política Nacional sobre Mudança do Clima - PNMC e dá outras "
                         "providências.", "2009-12-29", "2009-12-30", PAGES["l12187"]),
    "lei-13123-2015": _L("Lei nº 13.123, de 2015", "Regulamenta o inciso II do § 1º e o § 4º do art. 225 da Constituição Federal [...] "
                         "e dá outras providências.", "2015-05-20", "2015-05-21", PAGES["l13123"]),
    "lei-9718-1998": _L("Lei nº 9.718, de 1998", "Altera a Legislação Tributária Federal.", "1998-11-27", "1998-11-28",
                        PAGES["l9718"]),
    "lei-10637-2002": _L("Lei nº 10.637, de 2002", "Dispõe sobre a não-cumulatividade na cobrança da contribuição para os Programas "
                         "de Integração Social (PIS) e de Formação do Patrimônio do Servidor Público (Pasep), nos casos que "
                         "especifica; sobre o pagamento e o parcelamento de débitos tributários federais, a compensação de créditos "
                         "fiscais, a declaração de inaptidão de inscrição de pessoas jurídicas, a legislação aduaneira, e dá outras "
                         "providências.", "2002-12-30", "2002-12-31", PAGES["l10637"]),
    "lei-10833-2003": _L("Lei nº 10.833, de 2003", "Altera a Legislação Tributária Federal e dá outras providências.", "2003-12-29",
                         "2003-12-30", PAGES["l10833"]),
    "lc-141-2012": _L("Lei Complementar nº 141, de 2012", "Regulamenta o § 3º do art. 198 da Constituição Federal para dispor sobre os "
                      "valores mínimos a serem aplicados anualmente pela União, Estados, Distrito Federal e Municípios em ações e "
                      "serviços públicos de saúde [...] e dá outras providências.", "2012-01-13", "2012-01-16", PAGES["lcp141"]),
    "lei-14113-2020": _L("Lei nº 14.113, de 2020", "Regulamenta o Fundo de Manutenção e Desenvolvimento da Educação Básica e de "
                         "Valorização dos Profissionais da Educação (Fundeb), de que trata o art. 212-A da Constituição Federal; revoga "
                         "dispositivos da Lei nº 11.494, de 20 de junho de 2007; e dá outras providências.", "2020-12-25", "2020-12-25",
                         PAGES["l14113"]),
    "lei-12414-2011": _L("Lei nº 12.414, de 2011", "Disciplina a formação e consulta a bancos de dados com informações de adimplemento, "
                         "de pessoas naturais ou de pessoas jurídicas, para formação de histórico de crédito.", "2011-06-09",
                         "2011-06-10", PAGES["l12414"]),
    "lc-200-2023": _L("Lei Complementar nº 200, de 2023", "Institui regime fiscal sustentável para garantir a estabilidade "
                      "macroeconômica do País e criar as condições adequadas ao crescimento socioeconômico, com fundamento no art. 6º "
                      "da Emenda Constitucional nº 126, de 21 de dezembro de 2022, e no inciso VIII do caput e no parágrafo único do "
                      "art. 163 da Constituição Federal; e altera a Lei Complementar nº 101, de 4 de maio de 2000 (Lei de "
                      "Responsabilidade Fiscal).", "2023-08-30", "2023-08-31", PAGES["lcp200"]),
    "lei-11442-2007": _L("Lei nº 11.442, de 2007", "Dispõe sobre o transporte rodoviário de cargas por conta de terceiros e mediante "
                         "remuneração e revoga a Lei nº 6.813, de 10 de julho de 1980.", "2007-01-05", "2007-01-08", PAGES["l11442"]),
    "lei-10209-2001": _L("Lei nº 10.209, de 2001", "Institui o Vale-Pedágio obrigatório sobre o transporte rodoviário de carga e dá "
                         "outras providências.", "2001-03-23", "2001-03-24", PAGES["l10209"]),
    "lei-9611-1998": _L("Lei nº 9.611, de 1998", "Dispõe sobre o Transporte Multimodal de Cargas e dá outras providências.",
                        "1998-02-19", "1998-02-20", PAGES["l9611"]),
    "lei-11284-2006": _L("Lei nº 11.284, de 2006", "Dispõe sobre a gestão de florestas públicas para a produção sustentável; institui, "
                         "na estrutura do Ministério do Meio Ambiente, o Serviço Florestal Brasileiro - SFB; cria o Fundo Nacional de "
                         "Desenvolvimento Florestal - FNDF; altera as Leis nºs 10.683, de 28 de maio de 2003, 5.868, de 12 de dezembro de "
                         "1972, 9.605, de 12 de fevereiro de 1998, 4.771, de 15 de setembro de 1965, 6.938, de 31 de agosto de 1981, e "
                         "6.015, de 31 de dezembro de 1973; e dá outras providências.", "2006-03-02", "2006-03-03", PAGES["l11284"]),
    "lei-14119-2021": _L("Lei nº 14.119, de 2021", "Institui a Política Nacional de Pagamento por Serviços Ambientais; e altera as Leis "
                         "nºs 8.212, de 24 de julho de 1991, 8.629, de 25 de fevereiro de 1993, e 6.015, de 31 de dezembro de 1973, para "
                         "adequá-las à nova política.", "2021-01-13", "2021-01-14", PAGES["l14119"]),
    "lei-6091-1974": _L("Lei nº 6.091, de 1974", "Dispõe sobre o fornecimento gratuito de transporte, em dias de eleição, a eleitores "
                        "residentes nas zonas rurais, e dá outras providências.", "1974-08-15", "1974-08-15", PAGES["l6091"]),
    "lei-10216-2001": _L("Lei nº 10.216, de 2001", "Dispõe sobre a proteção e os direitos das pessoas portadoras de transtornos mentais e "
                         "redireciona o modelo assistencial em saúde mental.", "2001-04-06", "2001-04-09", PAGES["l10216"]),
    "lei-9434-1997": _L("Lei nº 9.434, de 1997", "Dispõe sobre a remoção de órgãos, tecidos e partes do corpo humano para fins de "
                        "transplante e tratamento e dá outras providências.", "1997-02-04", "1997-02-05", PAGES["l9434"]),
    "lei-11738-2008": _L("Lei nº 11.738, de 2008", "Regulamenta a alínea “e” do inciso III do caput do art. 60 do Ato das Disposições "
                         "Constitucionais Transitórias, para instituir o piso salarial profissional nacional para os profissionais do "
                         "magistério público da educação básica.", "2008-07-16", "2008-07-17", PAGES["l11738"]),
    "lei-12009-2009": _L("Lei nº 12.009, de 2009", "Regulamenta o exercício das atividades dos profissionais em transporte de "
                         "passageiros, “mototaxista”, em entrega de mercadorias e em serviço comunitário de rua, e “motoboy”, com o uso "
                         "de motocicleta, altera a Lei nº 9.503, de 23 de setembro de 1997, para dispor sobre regras de segurança dos "
                         "serviços de transporte remunerado de mercadorias em motocicletas e motonetas – moto-frete –, estabelece regras "
                         "gerais para a regulação deste serviço e dá outras providências.", "2009-07-29", "2009-07-30", PAGES["l12009"]),
    "lei-6996-1982": _L("Lei nº 6.996, de 1982", "Dispõe sobre a utilização de processamento eletrônico de dados nos serviços "
                        "eleitorais e dá outras providências.", "1982-06-07", "1982-06-08", PAGES["l6996"]),
    "lei-9870-1999": _L("Lei nº 9.870, de 1999", "Dispõe sobre o valor total das anuidades escolares e dá outras providências.",
                        "1999-11-23", "1999-11-24", PAGES["l9870"]),
    "lei-13005-2014": _L("Lei nº 13.005, de 2014", "Aprova o Plano Nacional de Educação - PNE e dá outras providências.",
                         "2014-06-25", "2014-06-26", PAGES["l13005"]),
    "lei-12379-2011": _L("Lei nº 12.379, de 2011", "Dispõe sobre o Sistema Nacional de Viação - SNV; altera a Lei nº 9.432, de 8 de "
                         "janeiro de 1997; revoga as Leis nºs 5.917, de 10 de setembro de 1973, 6.346, de 6 de julho de 1976, 6.504, "
                         "de 13 de dezembro de 1977, 6.555, de 22 de agosto de 1978, 6.574, de 30 de setembro de 1978, 6.630, de 16 de "
                         "abril de 1979, 6.648, de 16 de maio de 1979, 6.671, de 4 de julho de 1979, 6.776, de 30 de abril de 1980, "
                         "6.933, de 13 de julho de 1980, 6.976, de 14 de dezembro de 1980, 7.003, de 24 de junho de 1982, 7.436, de 20 "
                         "de dezembro de 1985, 7.581, de 24 de dezembro de 1986, 9.060, de 14 de junho de 1995, 9.078, de 11 de julho "
                         "de 1995, 9.830, de 2 de setembro de 1999, 9.852, de 27 de outubro de 1999, 10.030, de 20 de outubro de 2000, "
                         "10.031, de 20 de outubro de 2000, 10.540, de 1º de outubro de 2002, 10.606, de 19 de dezembro de 2002, "
                         "10.680, de 23 de maio de 2003, 10.739, de 24 de setembro de 2003, 10.789, de 28 de novembro de 2003, 10.960, "
                         "de 7 de outubro de 2004, 11.003, de 16 de dezembro de 2004, 11.122, de 31 de maio de 2005, 11.475, de 29 de "
                         "maio de 2007, 11.550, de 19 de novembro de 2007, 11.701, de 18 de junho de 2008, 11.729, de 24 de junho de "
                         "2008, e 11.731, de 24 de junho de 2008; revoga dispositivos das Leis nºs 6.261, de 14 de novembro de 1975, "
                         "6.406, de 21 de março de 1977, 11.297, de 9 de maio de 2006, 11.314, de 3 de julho de 2006, 11.482, de 31 de "
                         "maio de 2007, 11.518, de 5 de setembro de 2007, e 11.772, de 17 de setembro de 2008; e dá outras "
                         "providências.", "2011-01-06", "2011-01-07", PAGES["l12379"]),
    "lei-6437-1977": _L("Lei nº 6.437, de 1977", "Configura infrações à legislação sanitária federal, estabelece as sanções "
                        "respectivas, e dá outras providências.", "1977-08-20", "1977-08-24", PAGES["l6437"]),
    # LC 159 and LC 178: the same entries as 99-batch7's (title and URL), so the merged commit messages do not change
    "lc-159-2017": _L("Lei Complementar nº 159, de 2017", "Institui o Regime de Recuperação Fiscal dos Estados e do Distrito Federal "
                      "e altera as Leis Complementares n o 101, de 4 de maio de 2000, e n o 156, de 28 de dezembro de 2016.",
                      "2017-05-19", "2017-05-22", "leis/lcp/Lcp159.htm"),
    "lc-178-2021": _L("Lei Complementar nº 178, de 2021", "Estabelece o Programa de Acompanhamento e Transparência Fiscal e o Plano "
                      "de Promoção do Equilíbrio Fiscal; altera a Lei Complementar nº 101, de 4 de maio de 2000, a Lei Complementar nº "
                      "156, de 28 de dezembro de 2016, a Lei Complementar nº 159, de 19 de maio de 2017, a Lei Complementar nº 173, de "
                      "27 de maio de 2020, a Lei nº 9.496, de 11 de setembro de 1997, a Lei nº 12.348, de 15 de dezembro de 2010, a Lei "
                      "nº 12.649, de 17 de maio de 2012, e a Medida Provisória nº 2.185-35, de 24 de agosto de 2001; e dá outras "
                      "providências.", "2021-01-13", "2021-01-14", "leis/lcp/Lcp178.htm"),
    "lei-7853-1989": _L("Lei nº 7.853, de 1989", "Dispõe sobre o apoio às pessoas portadoras de deficiência, sua integração social, "
                        "sobre a Coordenadoria Nacional para Integração da Pessoa Portadora de Deficiência - Corde, institui a tutela "
                        "jurisdicional de interesses coletivos ou difusos dessas pessoas, disciplina a atuação do Ministério Público, "
                        "define crimes, e dá outras providências.", "1989-10-24", "1989-10-25", PAGES["l7853"]),
    "lei-9807-1999": _L("Lei nº 9.807, de 1999", "Estabelece normas para a organização e a manutenção de programas especiais de "
                        "proteção a vítimas e a testemunhas ameaçadas, institui o Programa Federal de Assistência a Vítimas e a "
                        "Testemunhas Ameaçadas e dispõe sobre a proteção de acusados ou condenados que tenham voluntariamente prestado "
                        "efetiva colaboração à investigação policial e ao processo criminal.", "1999-07-13", "1999-07-14",
                        PAGES["l9807"]),
    "lei-10861-2004": _L("Lei nº 10.861, de 2004", "Institui o Sistema Nacional de Avaliação da Educação Superior – SINAES e dá outras "
                         "providências", "2004-04-14", "2004-04-15", PAGES["l10861"]),
    "lei-10973-2004": _L("Lei nº 10.973, de 2004", "Dispõe sobre incentivos à inovação e à pesquisa científica e tecnológica no "
                         "ambiente produtivo e dá outras providências.", "2004-12-02", "2004-12-03", PAGES["l10973"]),
    "lei-9456-1997": _L("Lei nº 9.456, de 1997", "Institui a Lei de Proteção de Cultivares e dá outras providências.", "1997-04-25",
                        "1997-04-28", PAGES["l9456"]),
    "lei-7802-1989": _L("Lei nº 7.802, de 1989", "Dispõe sobre a pesquisa, a experimentação, a produção, a embalagem e rotulagem, o "
                        "transporte, o armazenamento, a comercialização, a propaganda comercial, a utilização, a importação, a "
                        "exportação, o destino final dos resíduos e embalagens, o registro, a classificação, o controle, a inspeção "
                        "e a fiscalização de agrotóxicos, seus componentes e afins, e dá outras providências.", "1989-07-11",
                        "1989-07-12", PAGES["l7802-2023"]),
    "lei-9612-1998": _L("Lei nº 9.612, de 1998", "Institui o Serviço de Radiodifusão Comunitária e dá outras providências.",
                        "1998-02-19", "1998-02-20", PAGES["l9612"]),
    "lei-11947-2009": _L("Lei nº 11.947, de 2009", "Dispõe sobre o atendimento da alimentação escolar e do Programa Dinheiro "
                         "Direto na Escola aos alunos da educação básica; altera as Leis nºs 10.880, de 9 de junho de 2004, 11.273, "
                         "de 6 de fevereiro de 2006, 11.507, de 20 de julho de 2007; revoga dispositivos da Medida Provisória nº "
                         "2.178-36, de 24 de agosto de 2001, e a Lei nº 8.913, de 12 de julho de 1994; e dá outras providências.",
                         "2009-06-16", "2009-06-17", PAGES["l11947"]),
    "lei-14785-2023": _L("Lei nº 14.785, de 2023", _T14785, "2023-12-27", "2023-12-28", PAGES["l14785"]),
    # url as in 99-batch15b's entry (capital L), so the merged law entry does not change
    "lei-10820-2003": _L("Lei nº 10.820, de 2003", "Dispõe sobre a autorização para desconto de prestações em folha de "
                         "pagamento, e dá outras providências.", "2003-12-17", "2003-12-18", "leis/2003/L10.820.htm"),
    "lei-6360-1976": _L("Lei nº 6.360, de 1976", "Dispõe sobre a vigilância sanitária a que ficam sujeitos os medicamentos, as "
                        "drogas, os insumos farmacêuticos e correlatos, cosméticos, saneantes e outros produtos, e dá outras "
                        "providências.", "1976-09-23", "1976-09-24", PAGES["l6360"]),
    "lei-11494-2007": _L("Lei nº 11.494, de 2007", "Regulamenta o Fundo de Manutenção e Desenvolvimento da Educação Básica e de "
                         "Valorização dos Profissionais da Educação - FUNDEB, de que trata o art. 60 do Ato das Disposições "
                         "Constitucionais Transitórias; altera a Lei nº 10.195, de 14 de fevereiro de 2001; revoga dispositivos "
                         "das Leis nºs 9.424, de 24 de dezembro de 1996, 10.880, de 9 de junho de 2004, e 10.845, de 5 de março "
                         "de 2004; e dá outras providências.", "2007-06-20", "2007-06-21", PAGES["l11494"]),
    "lei-9424-1996": _L("Lei nº 9.424, de 1996", "Dispõe sobre o Fundo de Manutenção e Desenvolvimento do Ensino Fundamental e de "
                        "Valorização do Magistério, na forma prevista no art. 60, § 7º, do Ato das Disposições Constitucionais "
                        "Transitórias, e dá outras providências.", "1996-12-24", "1996-12-26", PAGES["l9424"]),
    "lc-109-2001": _L("Lei Complementar nº 109, de 2001", "Dispõe sobre o Regime de Previdência Complementar e dá outras "
                      "providências.", "2001-05-29", "2001-05-30", PAGES["lcp109"]),
    "lc-108-2001": _L("Lei Complementar nº 108, de 2001", "Dispõe sobre a relação entre a União, os Estados, o Distrito Federal e "
                      "os Municípios, suas autarquias, fundações, sociedades de economia mista e outras entidades públicas e "
                      "suas respectivas entidades fechadas de previdência complementar, e dá outras providências.",
                      "2001-05-29", "2001-05-30", PAGES["lcp108"]),
    # the three below: records as earlier parts have them (99-batch10, 99-batch13f, 99-batch17g), so merged messages stay
    "lc-140-2011": _L("Lei Complementar nº 140, de 2011", "Fixa normas, nos termos dos incisos III, VI e VII do caput e do "
                      "parágrafo único do art. 23 da Constituição Federal, para a cooperação entre a União, os Estados, o "
                      "Distrito Federal e os Municípios nas ações administrativas decorrentes do exercício da competência comum "
                      "relativas à proteção das paisagens naturais notáveis, à proteção do meio ambiente, ao combate à poluição "
                      "em qualquer de suas formas e à preservação das florestas, da fauna e da flora; e altera a Lei n o 6.938, "
                      "de 31 de agosto de 1981.", "2011-12-08", "2011-12-09", "leis/LCP/Lcp140.htm"),
    "lei-9709-1998": _L("Lei nº 9.709, de 1998", "Regulamenta a execução do disposto nos incisos I, II e III do art. 14 da "
                        "Constituição Federal.", "1998-11-18", "1998-11-19", PAGES["l9709"]),
    "lc-179-2021": _L("Lei Complementar nº 179, de 2021", "Define os objetivos do Banco Central do Brasil e dispõe sobre sua "
                      "autonomia e sobre a nomeação e a exoneração de seu Presidente e de seus Diretores; e altera artigo da Lei "
                      "nº 4.595, de 31 de dezembro de 1964.", "2021-02-24", "2021-02-25", "leis/LCP/Lcp179.htm"),
    "lei-14286-2021": _L("Lei nº 14.286, de 2021", _T14286, "2021-12-29", "2021-12-30", "_Ato2019-2022/2021/Lei/L14286.htm"),
    # as 99-batch10 has the record
    "lei-14134-2021": _L("Lei nº 14.134, de 2021", "Dispõe sobre as atividades relativas ao transporte de gás natural, de que "
                         "trata o art. 177 da Constituição Federal, e sobre as atividades de escoamento, tratamento, "
                         "processamento, estocagem subterrânea, acondicionamento, liquefação, regaseificação e comercialização de "
                         "gás natural; altera as Leis nºs 9.478, de 6 de agosto de 1997, e 9.847, de 26 de outubro de 1999; e "
                         "revoga a Lei nº 11.909, de 4 de março de 2009, e dispositivo da Lei nº 10.438, de 26 de abril de 2002.",
                         "2021-04-08", "2021-04-09", "_Ato2019-2022/2021/Lei/L14134.htm"),
    "lc-75-1993": _L("Lei Complementar nº 75, de 1993", "Dispõe sobre a organização, as atribuições e o estatuto do Ministério "
                     "Público da União.", "1993-05-20", "1993-05-21", PAGES["lcp75"]),
    "lc-80-1994": _L("Lei Complementar nº 80, de 1994", "Organiza a Defensoria Pública da União, do Distrito Federal e dos "
                     "Territórios e prescreve normas gerais para sua organização nos Estados, e dá outras providências.",
                     "1994-01-12", "1994-01-13", PAGES["lcp80"]),
    "lei-12813-2013": _L("Lei nº 12.813, de 2013", "Dispõe sobre o conflito de interesses no exercício de cargo ou emprego do "
                         "Poder Executivo federal e impedimentos posteriores ao exercício do cargo ou emprego; e revoga "
                         "dispositivos da Lei nº 9.986, de 18 de julho de 2000, e das Medidas Provisórias nºs 2.216-37, de 31 de "
                         "agosto de 2001, e 2.225-45, de 4 de setembro de 2001.", "2013-05-16", "2013-05-17", PAGES["l12813"]),
    "lei-8437-1992": _L("Lei nº 8.437, de 1992", "Dispõe sobre a concessão de medidas cautelares contra atos do Poder Público e dá "
                        "outras providências.", "1992-06-30", "1992-07-01", PAGES["l8437"]),
    # as 99-batch9 has the record (title, url); published from LexML (Planalto's footer misprints 24.12.1997)
    "lei-9494-1997": _L("Lei nº 9.494, de 1997", "Disciplina a aplicação da tutela antecipada contra a Fazenda Pública, altera a "
                        "Lei nº 7.347, de 24 de julho de 1985, e dá outras providências.", "1997-09-10", "1997-09-11",
                        "leis/L9494.htm"),
    # as 99-batch6 and 99-batch17zi have the record
    "lei-14129-2021": _L("Lei nº 14.129, de 2021", "Dispõe sobre princípios, regras e instrumentos para o Governo Digital e para o "
                         "aumento da eficiência pública e altera a Lei nº 7.116, de 29 de agosto de 1983, a Lei nº 12.527, de 18 "
                         "de novembro de 2011 (Lei de Acesso à Informação), a Lei nº 12.682, de 9 de julho de 2012, e a Lei nº "
                         "13.460, de 26 de junho de 2017.", "2021-03-29", "2021-03-30", "_Ato2019-2022/2021/Lei/L14129.htm"),
    "dl-200-1967": _L("Decreto-Lei nº 200, de 1967", "Dispõe sôbre a organização da Administração Federal, estabelece diretrizes "
                      "para a Reforma Administrativa e dá outras providências.", "1967-02-25", "1967-02-27", PAGES["del0200"]),
    # as 99-batch10 has the record (title, url)
    "lei-12351-2010": _L("Lei nº 12.351, de 2010", "Dispõe sobre a exploração e a produção de petróleo, de gás natural e de outros "
                         "hidrocarbonetos fluidos, sob o regime de partilha de produção, em áreas do pré-sal e em áreas "
                         "estratégicas; cria o Fundo Social - FS e dispõe sobre sua estrutura e fontes de recursos; altera "
                         "dispositivos da Lei n o 9.478, de 6 de agosto de 1997; e dá outras providências.", "2010-12-22",
                         "2010-12-23", "_Ato2007-2010/2010/Lei/L12351.htm"),
    "lei-8625-1993": _L("Lei nº 8.625, de 1993", "Institui a Lei Orgânica Nacional do Ministério Público, dispõe sobre normas gerais "
                        "para a organização do Ministério Público dos Estados e dá outras providências.", "1993-02-12", "1993-02-15",
                        PAGES["l8625"]),
    # as 99-batch12 and 99-batch17zza have the record
    "lei-14601-2023": _L("Lei nº 14.601, de 2023", "Institui o Programa Bolsa Família; altera a Lei nº 8.742, de 7 de dezembro de 1993 "
                         "(Lei Orgânica da Assistência Social), a Lei nº 10.820, de 17 de dezembro de 2003, que dispõe sobre a "
                         "autorização para desconto em folha de pagamento, e a Lei nº 10.779, de 25 de novembro de 2003; e revoga "
                         "dispositivos das Leis nºs 14.284, de 29 de dezembro de 2021, e 14.342, de 18 de maio de 2022, e a Medida "
                         "Provisória nº 1.155, de 1º de janeiro de 2023.", "2023-06-19", "2023-06-20",
                         "_Ato2023-2026/2023/Lei/L14601.htm"),
    "lei-12618-2012": _L("Lei nº 12.618, de 2012", "Institui o regime de previdência complementar para os servidores públicos federais "
                         "titulares de cargo efetivo, inclusive os membros dos órgãos que menciona; fixa o limite máximo para a "
                         "concessão de aposentadorias e pensões pelo regime de previdência de que trata o art. 40 da Constituição "
                         "Federal; autoriza a criação de 3 (três) entidades fechadas de previdência complementar, denominadas "
                         "Fundação de Previdência Complementar do Servidor Público Federal do Poder Executivo (Funpresp-Exe), "
                         "Fundação de Previdência Complementar do Servidor Público Federal do Poder Legislativo (Funpresp-Leg) e "
                         "Fundação de Previdência Complementar do Servidor Público Federal do Poder Judiciário (Funpresp-Jud); "
                         "altera dispositivos da Lei nº 10.887, de 18 de junho de 2004; e dá outras providências.", "2012-04-30",
                         "2012-05-02", PAGES["l12618"]),
    # as 99-batch17e has the record
    "lei-12865-2013": _L("Lei nº 12.865, de 2013", "Autoriza o pagamento de subvenção econômica aos produtores da safra 2011/2012 de "
                         "cana-de-açúcar e de etanol que especifica e o financiamento da renovação e implantação de canaviais com "
                         "equalização da taxa de juros; dispõe sobre os arranjos de pagamento e as instituições de pagamento "
                         "integrantes do Sistema de Pagamentos Brasileiro (SPB); autoriza a União a emitir, sob a forma de colocação "
                         "direta, em favor da Conta de Desenvolvimento Energético (CDE), títulos da dívida pública mobiliária "
                         "federal; estabelece novas condições para as operações de crédito rural oriundas de, ou contratadas com, "
                         "recursos do Fundo Constitucional de Financiamento do Nordeste (FNE); altera os prazos previstos nas Leis nº "
                         "11.941, de 27 de maio de 2009, e nº 12.249, de 11 de junho de 2010; autoriza a União a contratar o Banco do "
                         "Brasil S.A. ou suas subsidiárias para atuar na gestão de recursos, obras e serviços de engenharia "
                         "relacionados ao desenvolvimento de projetos, modernização, ampliação, construção ou reforma da rede "
                         "integrada e especializada para atendimento da mulher em situação de violência; disciplina o documento "
                         "digital no Sistema Financeiro Nacional; disciplina a transferência, no caso de falecimento, do direito de "
                         "utilização privada de área pública por equipamentos urbanos do tipo quiosque, trailer, feira e banca de "
                         "venda de jornais e de revistas; altera a incidência da Contribuição para o PIS/Pasep e da Cofins na cadeia "
                         "de produção e comercialização da soja e de seus subprodutos; altera as Leis nºs 12.666, de 14 de junho de "
                         "2012, 5.991, de 17 de dezembro de 1973, 11.508, de 20 de julho de 2007, 9.503, de 23 de setembro de 1997, "
                         "9.069, de 29 de junho de 1995, 10.865, de 30 de abril de 2004, 12.587, de 3 de janeiro de 2012, 10.826, de "
                         "22 de dezembro de 2003, 10.925, de 23 de julho de 2004, 12.350, de 20 de dezembro de 2010, 4.870, de 1º de "
                         "dezembro de 1965 e 11.196, de 21 de novembro de 2005, e o Decreto nº 70.235, de 6 de março de 1972; revoga "
                         "dispositivos das Leis nºs 10.865, de 30 de abril de 2004, 10.925, de 23 de julho de 2004, 12.546, de 14 de "
                         "dezembro de 2011, e 4.870, de 1º de dezembro de 1965; e dá outras providências.", "2013-10-09", "2013-10-10",
                         "_Ato2011-2014/2013/Lei/L12865.htm"),
    # as 99-batch10 has the record
    "lei-9966-2000": _L("Lei nº 9.966, de 2000", "Dispõe sobre a prevenção, o controle e a fiscalização da poluição causada por "
                        "lançamento de óleo e outras substâncias nocivas ou perigosas em águas sob jurisdição nacional e dá outras "
                        "providências.", "2000-04-28", "2000-04-29", "leis/L9966.htm"),
    "lei-11959-2009": _L("Lei nº 11.959, de 2009", "Dispõe sobre a Política Nacional de Desenvolvimento Sustentável da Aquicultura "
                         "e da Pesca, regula as atividades pesqueiras, revoga a Lei n o 7.679, de 23 de novembro de 1988, e "
                         "dispositivos do Decreto-Lei n o 221, de 28 de fevereiro de 1967, e dá outras providências.",
                         "2009-06-29", "2009-06-30", "_Ato2007-2010/2009/Lei/L11959.htm"),
    # as 99-batch10, 17u and 17z have the record
    "lei-10848-2004": _L("Lei nº 10.848, de 2004", "Dispõe sobre a comercialização de energia elétrica, altera as Leis nºs 5.655, "
                         "de 20 de maio de 1971, 8.631, de 4 de março de 1993, 9.074, de 7 de julho de 1995, 9.427, de 26 de "
                         "dezembro de 1996, 9.478, de 6 de agosto de 1997, 9.648, de 27 de maio de 1998, 9.991, de 24 de julho de "
                         "2000, 10.438, de 26 de abril de 2002, e dá outras providências.", "2004-03-15", "2004-03-16",
                         "_Ato2004-2006/2004/Lei/L10.848.htm"),
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

# Lei 10.101 (part zc): (a) art. 6, 6-A and 6-B, which Medida Provisória 905/2019 revoked, are printed struck with MP 905's
# note and again unstruck with Lei 11.603's note: the unstruck copy is the line in force again from 19.8.2020 (MP 905
# lapsed), the struck copy stands until MP 955 lapsed (18.8.2020) - the mp955_two_copies model, with the note kept;
# (b) art. 2 §§ 3º-A and 5º to 10 (with their incisos): MP 905 added them and Lei 14.020/2020 (DOU 7.7.2020, in force on
# publication) added them again; MP 905's wordings end when MP 955 revoked the MP (20.4.2020) and do not come back on
# 18.8.2020, MP 905's last day, because by then Lei 14.020 had given these paragraphs their wording.
LPLR_905: list[str] = []


def _lplr_lab(x):
    return x.replace("º", "").replace(" ", "")


def _lplr_alnum(x):
    return re.sub(r"[\W_]+", "", P.norm(x))[:40]


def lplr_905(paras, act):
    if act["slug"] != "lei-da-participacao-nos-lucros":
        return
    m_key, r_key = "mp-905-2019", "mp-955-2020"
    m_lapse, r_lapse = P.MP_LAPSE[m_key][0], P.MP_LAPSE[r_key][0]
    for i, p in enumerate(paras):
        if p["unit"] not in ("art-06", "art-06-a", "art-06-b") or p["state"] == "plain" or not p.get("mp_pair") \
                or p.get("skip") or p.get("end") not in (r_lapse, m_lapse):
            continue
        q = next((q for q in paras[i + 1:] if q["unit"] == p["unit"] and q["state"] == "plain" and q["label"] == p["label"]
                  and P.norm(q["text"]) == P.norm(p["text"])
                  and all(any(x.startswith(n.rstrip(") ")) for x in p["notes"]) for n in q["notes"])), None)
        if q is None:
            continue
        p["end"], p["end_law"], p["end_how"] = r_lapse, r_key + "-fim", "mp-pair"
        q.update({"start": m_lapse, "start_law": m_key + "-fim", "end": None, "end_law": None, "end_how": None,
                  "skip": False, "restored": True, "pinned": True, "gaps": []})
        LPLR_905.append(f"{p['unit']} [{p['label']}]")
    # Planalto prints Medida Provisória 388/2007's arts. 6º-A and 6º-B a second time, struck, in the second block of these
    # articles; the second copies are the same wordings over the same days and are left out
    seen = set()
    for p in paras:
        if p["unit"] in ("art-06-a", "art-06-b") and p["state"] != "plain" and p.get("start_law") == "mp-388-2007":
            k = (p["unit"], p["label"], P.norm(p["text"]), p.get("end"))
            if k in seen and not p.get("skip"):
                p.update({"skip": True, "end_how": "duplicate", "pinned": True})
                LPLR_905.append(f"{p['unit']} [{p['label']}] Medida Provisória 388 wording printed twice, second copy left out")
            seen.add(k)
    later = [q for q in paras if q["unit"] == "art-02" and q["state"] == "plain"
             and any("14.020" in n for n in q["notes"])]
    for p in paras:
        if p["unit"] != "art-02" or p["state"] == "plain" or not any("905" in n for n in p["notes"]):
            continue
        hit = [q for q in later if _lplr_lab(q["label"]) == _lplr_lab(p["label"]) and (
            p["label"].startswith("§") or _lplr_alnum(q["text"]) == _lplr_alnum(p["text"]))]
        if not hit or p.get("start", "") > "2020-04-20":
            if hit and not p.get("skip"):
                p.update({"skip": True, "end_how": "superseded-by-lei-14020", "pinned": True})
                LPLR_905.append(f"art-02 [{p['label']}] {P.norm(p['text'])[:25]!r} 18.8.2020 copy left out")
            continue
        if p.get("end") != "2020-04-20" or p.get("gaps"):
            p.update({"end": "2020-04-20", "end_law": r_key, "end_how": "mp-pair", "gaps": [], "pinned": True})
            LPLR_905.append(f"art-02 [{p['label']}] {P.norm(p['text'])[:25]!r} ends 20.4.2020")


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
    B5.PROVISION_REPORTED.add(("lei-14004-2020", _LFF))   # explained by the line above
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
FOREIGN_RUBRICS = {"l0605": ("Descanso semanal", "Harmonização de multas trabalhistas constantes de legislações esparsas"),
                   "l10101": ("Participação nos lucros e prêmios",),
                   "l10101-compilado": ("Participação nos lucros e prêmios",)}
FOREIGN_DROPPED: list[str] = []
QUOTED_HEADINGS: list[str] = []
# Lei 7.689 art. 11 and Lei 9.249 art. 14 end '[...], com a redação dada pelo Decreto-Lei nº N, de d de m de aaaa.': words of
# the article (which wording of another act it refers to), not an amendment note; the reader takes them for a bare note.
BARE_TEXT = {"l7689": "art-11", "l9249": "art-14", "l9430": "art-88", "l9873": ("art-03", "art-08"), "l9984": "art-29",
             "l9984-compilado": "art-29", "l10637": ("art-47", "art-54"), "l10637-compilado": ("art-47", "art-54"),
             "l10833": ("art-23", "art-25", "art-40"), "l10833-compilado": ("art-23", "art-40"), "l9807": "art-17"}
BARE_TEXT_USED: list[str] = []
QUOTE_DROPPED: list[str] = []
_BARE_RX = re.compile(r"\(?\s*(reda[çc][ãa]o dada pel[oa] (?:Decreto-Lei|Lei) n[º°.]?\s*[\d.]+, de \d{1,2} de \w+ de \d{4}[.;]?)\s*\)?",
                      re.I)
_BARE_RX9807 = re.compile(r"\(?\s*(reda[çc][ãa]o dada pela Lei n[º°.]?\s*9\.708, de 18 de novembro de 1998, passa a ter a seguinte "
                          r"reda[çc][ãa]o:)\s*\)?", re.I)
_BARE_RX9873 = re.compile(r"\(?\s*(reda[çc][ãa]o dada pela Lei n[º°.]?\s*9\.457, de 1997, o art\. 28 da Lei n[º°.]?\s*8\.884, de 1994, e "
                          r"demais disposições em contrário, ainda que constantes de lei especial\.)\s*\)?")
_BARE_RX9984 = re.compile(r"\(?\s*(reda[çc][ãa]o dada pela Lei n[º°.]?\s*9\.433, de 1997, passa a vigorar com a seguinte "
                          r"reda[çc][ãa]o:)\s*\)?")
# Lei 10.637 art. 47 § 2º ('[...] o art. 14 da Lei nº 9.648, de 27 de maio de 1998, com a redação dada pela Lei nº 10.433, de
# 24 de abril de 2002, para efeitos de incidência [...]') and the 2002 art. 54 ('[...] do Decreto-Lei nº 1.593, de 21 de dezembro
# de 1977, com a redação dada pela Medida Provisória nº 2.158-35, de 24 de agosto de 2001.')
_BARE_RX10637 = re.compile(r"\(?\s*(reda[çc][ãa]o dada pel[oa] (?:Lei n[º°.]?\s*10\.433, de 24 de abril de 2002, para efeitos de "
                           r"incid[êe]ncia .*?|Medida Provis[óo]ria n[º°.]?\s*2\.158-35, de 24 de agosto de 2001\.))\s*\)?")
# Lei 10.833 art. 23 ('[...] art. 6º, caput, da Lei nº 9.718, de 27 de novembro de 1998, com a redação dada pela Lei nº 9.990, de
# 21 de julho de 2000, sobre os gases liquefeitos de petróleo [...]') and art. 40 ('O caput do art. 1º do Decreto-Lei nº 1.593, de
# 21 de dezembro de 1977, com a redação dada pela Medida Provisória nº 2.158-35, de 24 de agosto de 2001, e o art. 18 do mesmo
# Decreto-Lei passam a vigorar com a seguinte redação:')
_BARE_RX10833 = re.compile(r"\(?\s*(reda[çc][ãa]o dada pela (?:Lei n[º°.]?\s*9\.990, de 21 de julho de 2000, sobre os gases .*?"
                           r"|Medida Provis[óo]ria n[º°.]?\s*2\.158-35, de 24 de agosto de 2001, e o art\. 18 do mesmo Decreto-Lei passam "
                           r"a vigorar com a seguinte reda[çc][ãa]o:))\s*\)?")
_paragraphs17 = P.paragraphs


def paragraphs(html, digits):
    page = B8.CURRENT_PAGE[0]
    if page == "l14113":
        # Lei 14.113 art. 26: Lei 14.276/2021 art. 1 made the parágrafo único § 1º (and added § 2º); Planalto notes the new § 1º
        # '(Transformado em § 1º pela Lei nº 14.276, de 2021)', a form the reader does not take for a note: read as the
        # renumbering it describes. The struck parágrafo único lacks the space after its label ('Parágrafo único.Para').
        html, n1 = re.subn(r"\(\s*Transformado\s+em\s+(§\s*1º)\s+pela\s+", r"(Renumerado do parágrafo único para \1 pela ", html)
        html, n2 = re.subn(r"(Parágrafo único\.)(</font>\s*<font[^>]*>)(Para)", r"\1\2 \3", html)
        LFUNDEB_FIXED.extend(["art-26 note"] * n1 + ["art-26 space"] * n2)
    out, rest = _paragraphs17(html, digits)
    if page in ("l9434", "l9434-compilado"):
        # Lei 9.434 art. 10: Planalto prints Lei 10.211/2001's § 1º as '1º Nos casos em que o receptor [...]', the '§' sign missing
        for p in out:
            if p["unit"] == "art-10" and p["label"] == "" and p["text"].startswith("1º Nos casos em que o receptor"):
                p["text"], p["label"] = "§ " + p["text"], "§ 1º"
                L9434_FIXED.append(f"{page} art-10 § 1º")
    if page == "l11442":
        # Lei 11.442 art. 13: Planalto prints the placeholder 'Parágrafo único. (Revogado).' (Lei 14.599/2023) right after the
        # struck parágrafo único of 2007, above the caput Lei 14.599 gave the article: it is the article's last line
        pu = [p for p in out if p["unit"] == "art-13" and p["state"] == "plain" and p["text"].startswith("Parágrafo único. (Revogado)")]
        if len(pu) == 1:
            out.remove(pu[0])
            last = max(i for i, q in enumerate(out) if q["unit"] == "art-13")
            out.insert(last + 1, pu[0])
            for i, q in enumerate(out):
                q["i"] = i
            L11442_FIXED.append("art-13 parágrafo único placeholder after § 9º")
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
            if not hit and page in ("l9984", "l9984-compilado"):
                # Lei 9.984 art. 29: 'O art. 1º da Lei nº 8.001, de 13 de março de 1990, com a redação dada pela Lei nº 9.433, de
                # 1997, passa a vigorar com a seguinte redação:'
                hit = [(n, m) for n in p["notes"] for m in [_BARE_RX9984.fullmatch(n.strip())] if m]
            if not hit and page == "l9807":
                # Lei 9.807 art. 17: 'O parágrafo único do art. 58 da Lei nº 6.015 [...], com a redação dada pela Lei nº 9.708, de 18
                # de novembro de 1998, passa a ter a seguinte redação:'
                hit = [(n, m) for n in p["notes"] for m in [_BARE_RX9807.fullmatch(n.strip())] if m]
            if not hit and page in ("l10637", "l10637-compilado"):
                hit = [(n, m) for n in p["notes"] for m in [_BARE_RX10637.fullmatch(n.strip())] if m]
            if not hit and page in ("l10833", "l10833-compilado"):
                hit = [(n, m) for n in p["notes"] for m in [_BARE_RX10833.fullmatch(n.strip())] if m]
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
    if page in ("l9718", "l9718-compilada"):
        # Lei 9.718: Planalto's marker 'Sem eficácia' after the struck line of Medida Provisória 252/2005 (art. 3 § 8 III,
        # lapsed) is not part of the text
        for p in out:
            t = re.sub(r"(?:^|\s+)\(?Sem efic[áa]cia\)?\s*$", "", p["text"])
            if t != p["text"]:
                p["text"] = t
                L9718_FIXED.append(p["unit"])
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
    if page in ("l8745", "l8745-compilada"):
        # Lei 8.745 art. 2 VI d) and art. 4 caput (2003): Planalto's pointers '(Prorrogação de prazo).' (Medida Provisória
        # 431/2008 art. 173, struck) and '(Prorrogação de prazo pela Lei nº 11.784, de 2008' (its closing parenthesis missing)
        # name a law that extended contracts, not a change of words; they and the stray full stops left by the pointers
        # around them are not text
        for p in out:
            t = re.sub(r"\s*\(Prorroga[çc][ãa]o de prazo(?: pela\s+Lei n[º°]\s*11\.784, de 2008)?\)?\.?", "", p["text"])
            if t != p["text"]:
                t = re.sub(r"([;:])\s*\.+\s*$", r"\1", t.rstrip())
                L8745_FIXED.append(f"{p['unit']} [{p['label']}]")
                p["text"] = t
    if page == "l12462":
        # Lei 12.462 art. 63 § 17 (Medida Provisória 1.349/2026, 'Vigência encerrada', day not read): left out
        n0 = len(out)
        out = [p for p in out if not (p["unit"] == "art-63" and P.norm(p["text"]).startswith("§ 17. O apoio financeiro "
                                                                                        "reembolsável"))]
        if len(out) != n0:
            LRDC_FIXED.append("x")
    if page in ("l9782", "l9782-compilado"):
        # Lei 9.782: the lines Lei 15.524/2026 added (no archived copy of the Lei, so its in-force day cannot be read): left out
        n0 = len(out)
        out = [p for p in out if not any(re.search(r"Lei\s+n[º°]\s*15\.524", n) for n in p["notes"])]
        if len(out) != n0:
            L9782_LEFT_OUT.append(f"{page}: {n0 - len(out)} lines")
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
    if page == "l9984":
        # Lei 9.984: Planalto prints Medida Provisória 868/2018's inciso XXIII-A, inciso XXIV-A, § 9º-A and § 10-A of art. 4 as
        # 'XXIIIA', 'XXIVA -', '§ 9º A' and '§ 10A.', and Medida Provisória 844/2018's art. 4º-A as 'Art. 4ºA.' (the MPs' own
        # pages: 'XXIII-A', 'XXIV -A', '§ 9º-A', '§ 10-A.', 'Art. 4º-A'); the reader took the last three for the lower label (§ 9º,
        # § 10) or for lines of art. 4. They keep the MPs' labels; MP 844's art. 4º-A and its lines are read as art. 4º-A.
        fix = ((r"^XXIIIA\s*-?\s*", "XXIII-A - ", "XXIII-A -"), (r"^XXIVA\s*-\s*", "XXIV-A - ", "XXIV-A -"),
               (r"^§\s*9º\s*A\s+", "§ 9º-A ", "§ 9º-A"), (r"^§\s*10\s*A\.\s*", "§ 10-A. ", "§ 10-A"))
        a4a = False
        for p in out:
            if p["heading"]:
                continue
            if p["unit"] == "art-04" and re.match(r"Art\.\s*4º\s*A\.\s", P.norm(p["text"])):
                p["text"] = re.sub(r"^\s*Art\.\s*4º\s*A\.\s*", "Art. 4º-A. ", p["text"])
                p["unit"], p["label"], a4a = "art-04-a", "Art. 4º-A", True
                L9984_FIXED.append("art-04-a")
                continue
            if a4a and p["unit"] == "art-04":
                p["unit"] = "art-04-a"
                continue
            a4a = False
            if p["unit"] != "art-04":
                continue
            for rx, new, lab in fix:
                if re.match(rx, P.norm(p["text"])):
                    p["text"], p["label"] = re.sub(rx, new, P.norm(p["text"])), lab
                    L9984_FIXED.append(lab)
    if page == "l4886":
        # Lei 4.886: Lei 8.420/1992 art. 3 'São suprimidos o parágrafo único do art. 10, o parágrafo único do art. 17 e o art.
        # 41'; Planalto marks the struck lines '(Suprimido)', naming no law: the mark is read as that revocation. Lei 12.246/2010
        # (art. 10 '§ 1º (Suprimido)') prints the word as part of its text: there it stays in the line.
        for p in out:
            if not any(n.strip() == "(Suprimido)" for n in p["notes"]):
                continue
            if p["state"] == "plain":
                p["text"] = P.norm(p["text"]).rstrip(". ") + " (Suprimido)."
                p["notes"] = [n for n in p["notes"] if n.strip() != "(Suprimido)"]
                L4886_FIXED.append(f"{p['unit']} [{p['label']}] text")
            else:
                p["notes"] = [("(Revogado pela Lei nº 8.420, de 1992)" if n.strip() == "(Suprimido)" else n) for n in p["notes"]]
                L4886_FIXED.append(f"{p['unit']} [{p['label']}]")
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
    if page == "l10833":
        efeitos_fix(out)
    if page == "l10973":
        # Lei 10.973 is read without centred headings (its chapter names are not centred); the dotted closing lines of the
        # amendments arts. 24 and 25 quote ('..... " (NR)') have no lower-case letter, so the capitals rule took them for
        # headings: they are lines of the article that quotes them
        last = None
        for p in out:
            if p["heading"] and re.search(r"\(NR\)\s*$", p["text"]) and last:
                p["unit"], p["heading"], p["label"] = last, False, ""
                LINOV_FIXED.append(f"{last} closing line")
            elif not p["heading"] and p["unit"].startswith("art-"):
                last = p["unit"]
    if page == "l13005":
        B15.TABLES.pop(page, None)   # the page's tables are in the Anexo (Meta 7), read below: own decision
        # Lei 13.005: the Anexo (the plan's 20 metas and their estratégias) is printed after the signature, where the reader
        # stops; it is part of the Lei (art. 1 'na forma do Anexo') and is read here: one unit per meta
        ann = pne_annex(html)
        out = out + ann
        for i, q in enumerate(out):
            q["i"] = i
        PNE_ANNEX.append(f"{page}: {len(ann)} lines")
    return out, rest


PNE_ANNEX: list[str] = []
LINOV_FIXED: list[str] = []


def pne_annex(html):
    """The Anexo of Lei 13.005 as paragraphs: the 'ANEXO' / 'METAS E ESTRATÉGIAS' lines in unit anexo, then each 'Meta N:'
    line with its 'Estratégias:' line and its items 'N.M)' in unit anexo-meta-NN (labels 'Meta N' and 'N.M)')."""
    res, unit = [], None
    for b in [P.analyse(x) for x in P.blocks_of(html)]:
        t = b["text"]
        if unit is None:
            if t == "ANEXO" and b["center"]:
                unit = "anexo"
            else:
                continue
        if not t or re.fullmatch(r"[.;,:\s*]+", t):
            if b["notes"] and res:
                res[-1]["notes"] = list(res[-1]["notes"]) + list(b["notes"])
            continue
        lab = ""
        m = re.match(r"Meta (\d+):", t)
        if m:
            unit, lab = f"anexo-meta-{int(m.group(1)):02d}", f"Meta {m.group(1)}"
        else:
            m = re.match(r"(\d+\.\d+)\)", t)
            if m:
                lab = m.group(1) + ")"
        res.append({**b, "unit": unit, "label": lab, "heading": False})
    return res


_unit_kind17, _unit_label17 = P.unit_kind, P.unit_label


def unit_kind(u):
    return "annex" if u.startswith("anexo") else _unit_kind17(u)


def unit_label(u, ps):
    if u == "anexo":
        return "Anexo"
    if u.startswith("anexo-meta-"):
        return f"Meta {int(u[11:])} do Anexo"
    return _unit_label17(u, ps)


P.unit_kind, P.unit_label = unit_kind, unit_label


# Lei 10.833: Planalto's annotated page prints 'efeito' where the Lei says 'efeitos' (art. 23 'gases liquefeito', art. 93
# 'produzindo efeito', art. 94 VI 'dos efeito'); its consolidated page and the Chamber of Deputies' copy of the original
# publication (DOU 30.12.2003) print 'efeitos'. A line of the annotated page whose words are not found in the consolidated
# page, the original publication or the page of the act its note names, but are found there with one set of its 'efeito'
# made 'efeitos', takes those words (Lei 11.727/2008's page too: art. 58-M's struck caput has only a revocation note).
# Comparison on letters and digits only ('nº' and 'n o' alike).
EFX_REFS = ("l10833-compilado", "ctx:camara-lei-10833-2003-original", "law:lei-11727-2008")
_EFX_CACHE: dict[str, str] = {}
EFX_FIXED: list[str] = []
EFX_OPEN: list[str] = []


def _efx_key(s):
    s = s.replace("º", "o").replace("°", "o").replace("ª", "a").lower()
    return "".join(c for c in s if c.isalnum())


def _efx_ref(k):
    if k not in _EFX_CACHE:
        import html as _h
        r = P.raw(k)
        t = ""
        if r:
            t = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", P.decode(r[0]))
            t = _h.unescape(re.sub(r"<[^>]+>", " ", t))
        _EFX_CACHE[k] = _efx_key(t)
    return _EFX_CACHE[k]


def efeitos_fix(out):
    for p in out:
        occ = [m.end() for m in re.finditer(r"efeito\b", p["text"])]
        if not occ:
            continue
        refs = list(EFX_REFS) + ["law:" + k for n in p["notes"] for k in [B6.law_key(n)] if k]
        keys = [_efx_ref(r) for r in dict.fromkeys(refs)]

        def found(t):
            kt = _efx_key(t)
            return any(kt in k for k in keys)
        if found(p["text"]):
            continue
        hits = []
        for mask in range(1, 2 ** len(occ)):
            t = p["text"]
            for i in reversed(range(len(occ))):
                if mask >> i & 1:
                    t = t[:occ[i]] + "s" + t[occ[i]:]
            if found(t):
                hits.append(t)
        where = f"{p['unit']} {p['label'] or p['text'][:30]!r}"
        if len(hits) == 1:
            p["text"] = hits[0]
            EFX_FIXED.append(where)
        elif re.search(r"(?:\bos|\bdos|\bgases liqu|\bproduzindo|\bproduzirá|\bpara|\bcom|\bde) efeito\b", p["text"]):
            EFX_OPEN.append(where + f" ({len(hits)} matches)")


L9250_FIXED: list[str] = []
L9430_FIXED: list[str] = []
L9718_FIXED: list[str] = []
L13465_FIXED: list[str] = []
L8745_FIXED: list[str] = []
L9782_LEFT_OUT: list[str] = []
L9984_FIXED: list[str] = []
L4886_FIXED: list[str] = []
LFUNDEB_FIXED: list[str] = []
L11442_FIXED: list[str] = []
L9434_FIXED: list[str] = []
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


# part zh: Lei 4.886/1965 art. 10. Lei 12.246/2010 art. 1 'renumerando-se as atuais alíneas a a g para incisos I a VII';
# Planalto prints only the incisos, each noted 'Renumerado pela Lei nº 12.246, de 2010'. The alíneas a) to g), with the same
# words, stand from the act's first day to 28.5.2010, after the caput.
LRC_RENUM: list[str] = []
LRC_RENUM92: list[str] = []
_ROMAN7 = {"I -": "a)", "II -": "b)", "III -": "c)", "IV -": "d)", "V -": "e)", "VI -": "f)", "VII -": "g)"}


def lrc_renum(paras, act):
    if act["slug"] != "lei-dos-representantes-comerciais":
        return
    day, law = "2010-05-28", "lei-12246-2010"
    act_day = B.ACT_DAY[act["law"]][0]
    cap = next((i for i, p in enumerate(paras) if p["unit"] == "art-10" and p["label"] == "Art. 10" and not p["heading"]), None)
    if cap is None:
        return
    copies = []
    for p in paras:
        if (p["unit"] != "art-10" or p["label"] not in _ROMAN7 or p.get("skip")
                or not any("Renumerado pela Lei nº 12.246" in n for n in p["notes"])):
            continue
        lab = _ROMAN7[p["label"]]
        c = dict(p, label=lab, text=lab + p["text"][len(p["label"]):], gaps=[], start=act_day, start_law=None, end=day,
                 end_law=law, end_how="renumbered", notes=[n for n in p["notes"] if "Renumerado" not in n])
        copies.append(c)
        LRC_RENUM.append(f"{lab} -> {p['label'].rstrip(' -')}")
    paras[cap + 1:cap + 1] = copies
    # Lei 8.420/1992 (DOU 11.5.1992) art. 2 added articles 'que passarão a ter os números 41, 42, 43, 44, 45, 46 e 47': the 1965
    # arts. 42 ('Esta lei entra em vigor na data de sua publicação') and 43 ('Revogam-se as disposições em contrário') became
    # arts. 48 and 49 (the Chamber's copy of the original publication; Planalto prints only the new numbers, with no note)
    d92, l92 = "1992-05-11", "lei-8420-1992"
    for new, old in (("art-48", 42), ("art-49", 43)):
        src = [p for p in paras if p["unit"] == new and not p["heading"] and not p.get("skip")]
        at = next((i for i, p in enumerate(paras) if p["unit"] == f"art-{old}"), None)
        if not src or at is None or src[0]["start"] != act_day:
            continue
        cs = []
        for p in src:
            c = dict(p, unit=f"art-{old}", gaps=[], start=act_day, start_law=None, end=d92, end_law=l92, end_how="renumbered")
            if p["label"].startswith("Art"):
                c["label"] = f"Art. {old}"
                c["text"] = c["label"] + p["text"][len(p["label"]):]
            cs.append(c)
            p["start"], p["start_law"] = d92, l92
        paras[at:at] = cs
        LRC_RENUM92.append(f"art. {old} -> art. {int(new[4:])}")
    for i, p in enumerate(paras):
        p["i"] = i


# part zf: Lei 9.984/2000 (ANA). Medida Provisória 437/2008 (DOU 30.7.2008, in force on publication) art. 13 added art. 4 XIX
# and § 8º, art. 19-A and art. 20 XI and parágrafo único; Medida Provisória 439/2008 (DOU 29.8.2008, edição extra, in force on
# publication; converted, Lei 11.805/2008, which repeats it in its art. 4) art. 4: 'Fica revogada a Medida Provisória nº 437,
# de 29 de julho de 2008'. Every line MP 437 gave Lei 9.984 ends on 29.8.2008 (Lei 12.058/2009 later added art. 4 XIX and § 8º
# again, from 14.10.2009).
_LANA = "lei-da-ana"
ANA_437: list[str] = []


def ana_437(paras, act):
    if act["slug"] != _LANA:
        return
    for p in paras:
        if p["state"] == "plain" or p.get("start_law") != "mp-437-2008":
            continue
        p.update({"end": "2008-08-29", "end_law": "mp-439-2008", "end_how": "revoked-mp", "skip": False, "gaps": [],
                  "pinned": True})
        ANA_437.append(f"{p['unit']} [{p['label']}]")
        # the earlier passes listed these lines as undated or as ended by the next wording: they are dated here
        und = f"{act['short']} {p['unit']} [{p['label'] or 'line'}] {p['text'][:60]!r}"
        B.UNDATED[:] = [u for u in B.UNDATED if not u.startswith(und)]
        nxt = f"{act['slug']} {p['unit']} [{p['label']}] {p['text'][:40]!r} ends "
        B7.NEXT_WORDING_USED[:] = [u for u in B7.NEXT_WORDING_USED if not u.startswith(nxt)]


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
    # (these two were inside part s's block below since the sixth session, so a fresh parse of part q lost them)
    P.VIGENCIA_FIXED["lei-13988-2020"] = (
        "2020-04-14", "'Esta Lei entra em vigor: I - em 120 (cento e vinte) dias [...] em relação ao inciso I do caput e ao "
                      "parágrafo único do art. 23; e II - na data de sua publicação, em relação aos demais dispositivos' (DOU "
                      "14.4.2020, edição extra): its art. 28 (Lei 10.522 art. 19-E) falls under II")
    P.MP_LAPSE["mp-1160-2023"] = (
        "2023-06-02", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 41, de 2023 (DOU 16.6.2023): 'teve seu "
                      "prazo de vigência encerrado no dia 1º de junho de 2023'; the provision it had revoked is back from "
                      "2.6.2023")
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
    # ... and so is a struck line SPAN_FIX leaves out (a duplicate copy): matched by unit, label and text
    dated |= {f"no end for struck {p['unit']} [{p['label']}] {p['text'][:90]!r}" for p in paras
              if p.get("pinned") and p["state"] != "plain" and p.get("skip") and p.get("end_how") == "duplicate"}
    problems = [x for x in problems if not any(x.startswith(t) for t in dated)]
    # Leis 10.637 and 10.833: Planalto prints the wordings Medida Provisória 1.159/2023 replaced a second time, struck, as
    # restored when it lapsed (1.6.2023); Lei 14.592/2023 (DOU 30.5.2023, in force on publication) had already given those
    # dispositivos their wording, so the restored copies never were in force and are left out
    if cx.act in (_L10637, _L10833):
        for p in paras:
            if p["start_law"] == "mp-1159-2023-fim" and p.get("end") and p["end"] < p["start"] and not p.get("skip"):
                p["skip"], p["pinned"], p["end_how"] = True, True, "never-in-effect"
                MP1159_SKIPPED.append(f"{p['unit']} {p['label']}")
                key = f"ends before it starts: {p['unit']} [{p['label']}] {p['start']}.."
                problems = [x for x in problems if not x.startswith(key)]
    return problems


MP1159_SKIPPED: list[str] = []
P.lifespans = B.lifespans = lifespans
_apply_rewrites17 = P.apply_rewrites


# Lei 9.870 (part zr): Medida Provisória 2.173-24 (DOU 24.8.2001) art. 1 added art. 1 §§ 3º and 4º 'renumerando-se os atuais
# §§ 3º e 4º para §§ 5º e 6º' and art. 2 added art. 6 § 1º 'renumerando-se os atuais §§ 1º, 2º e 3º para §§ 2º, 3º e 4º' (read
# on the MP page), changing no words. Planalto prints only the new numbers, noted 'Renumerado'; the paragraphs stand under
# their old numbers, with the same words, from the act's first day to 24.8.2001.
MESC_RENUM: list[str] = []
_MESC_RENUM = {"art-01": ("§ 2º", {"§ 5º": "§ 3º", "§ 6º": "§ 4º"}),
               "art-06": ("Art. 6º", {"§ 2º": "§ 1º", "§ 3º": "§ 2º", "§ 4º": "§ 3º"})}


def mesc_renum(paras, act):
    if act["slug"] != "lei-das-mensalidades-escolares":
        return
    day, law = "2001-08-24", "mp-2173-2001"
    act_day = B.ACT_DAY[act["law"]][0]
    for unit, (after, olds) in _MESC_RENUM.items():
        at = next((i for i, p in enumerate(paras) if p["unit"] == unit and p["label"] == after and not p["heading"]), None)
        if at is None:
            continue
        copies = []
        for p in paras:
            if (p["unit"] != unit or p["label"] not in olds or p.get("skip")
                    or not any("Renumerado pela Medida Provisória nº 2.173-24" in n for n in p["notes"])):
                continue
            old = olds[p["label"]]
            copies.append(dict(p, label=old, text=old + p["text"][len(p["label"]):], gaps=[], start=act_day, start_law=None,
                               end=day, end_law=law, end_how="renumbered",
                               notes=[n for n in p["notes"] if "Renumerado" not in n]))
            MESC_RENUM.append(f"art. {int(unit[4:])} {old} -> {p['label']}")
        paras[at + 1:at + 1] = copies
    for i, p in enumerate(paras):
        p["i"] = i


def apply_rewrites(paras, act, eff, problems):
    out = _apply_rewrites17(paras, act, eff, problems)
    renum_articles(paras, act)
    mp955_two_copies(paras, act)
    lplr_905(paras, act)
    veto_kept(paras, act)
    promulgated(paras, act)
    heads_14596(paras, act, eff)
    ch3_successors(paras, act)
    ana_437(paras, act)
    lrc_renum(paras, act)
    prom_14119(paras, act)
    mesc_renum(paras, act)
    return out


# Lei 14.119/2021 (part zp): parts vetoed on 13.1.2021 that Congress kept were promulgated by the President in two acts printed
# at the foot of the page: on 26.3.2021 (DOU 26.3.2021, edição extra-D) art. 6 § 8º, art. 8 § 1º and arts. 13, 15 and 16; on
# 10.6.2021 (DOU 11.6.2021; the page's footer misprints '11.1.2021') art. 17 and its parágrafo único (days read on the Chamber
# of Deputies' records of the two promulgations, archive.org copies). Planalto prints each '(VETADO)' line struck before the
# promulgated text: the '(VETADO)' line stands from the Lei's first day to the promulgation, the promulgated lines from then,
# credited to Lei 14.119. The promulgated art. 6 § 8º, art. 15 § 4º and art. 16 § 2º keep the quotation marks of the
# promulgation's own text, which are dropped.
PROM14119 = {"art-13": ("2021-03-26", None), "art-15": ("2021-03-26", None), "art-16": ("2021-03-26", None),
             "art-17": ("2021-06-11", None), "art-06": ("2021-03-26", "§ 8º"), "art-08": ("2021-03-26", "§ 1º")}
PROM14119_USED: list[str] = []


def prom_14119(paras, act):
    if act["slug"] != "lei-do-pagamento-por-servicos-ambientais":
        return
    first = B.ACT_DAY[act["law"]][0]
    for p in paras:
        if p["heading"] or p["unit"] not in PROM14119:
            continue
        day, lab = PROM14119[p["unit"]]
        t = p["text"]
        if lab and p["label"] == "" and t.startswith("'" + lab + " "):
            p["label"] = lab
        if lab and p["label"] != lab:
            continue
        if p["state"] == "struck" and re.fullmatch(r"(?:Art\. \d+\.|§ \d+º) \(VETADO\)\.", P.norm(t)):
            p.update(skip=False, start=first, start_law=None, end=day, end_law="lei-14119-2021", end_how="promulgated")
            PROM14119_USED.append(f"{p['unit']} {p['label']} (VETADO) to {day}")
        elif p["state"] == "plain" and p["start"] == first and not p.get("skip"):
            t2 = t.strip()
            if t2.startswith("'"):
                t2 = t2[1:]
            if t2.endswith('"'):
                t2 = t2[:-1]
            p["text"] = t2
            p.update(start=day, start_law="lei-14119-2021")
            PROM14119_USED.append(f"{p['unit']} {p['label']} from {day}")


P.apply_rewrites = B.apply_rewrites = apply_rewrites

# ---------------------------------------------------------------------------------------------------------------
_inner17 = B6.PB5B._write_part5


def _inner(*a):
    dec = list(EXTRA)
    if LINOV_FIXED:
        dec.append("Lei 10.973: its chapter names are not centred, so headings are read by the Capítulo line and the name line "
                   "after it; the dotted closing lines of the amendments arts. 24 and 25 quote ('..... \" (NR)'), which have no "
                   "lower-case letter, are kept as lines of those articles, not headings (" + ", ".join(dict.fromkeys(LINOV_FIXED)) + ").")
    if PNE_ANNEX:
        dec.append("Lei 13.005: Planalto prints the Anexo (art. 1: the plan 'na forma do Anexo'; its 20 metas and their "
                   "estratégias) after the signature; it is part of the Lei and is read as units of its own: 'anexo' (the lines "
                   "'ANEXO' and 'METAS E ESTRATÉGIAS') and one unit per meta, anexo-meta-01 to anexo-meta-20, holding the "
                   "meta, the line 'Estratégias:' and the numbered estratégias (labels 'Meta N' and 'N.M)'); the tables of "
                   "Meta 7 (IDEB and PISA targets) are one cell per line, as in the CLT's art. 580.")
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
    if any(x.startswith("l9984") for x in BARE_TEXT_USED):
        dec.append("Lei 9.984 art. 29 begins 'O art. 1º da Lei nº 8.001, de 13 de março de 1990, com a redação dada pela Lei nº "
                   "9.433, de 1997, passa a vigorar com a seguinte redação:': these words name the wording of the article it "
                   "rewrites; they are part of the text, not an amendment note (l9984 art-29).")
    if L9984_FIXED:
        dec.append("Lei 9.984 art. 4: Planalto prints Medida Provisória 868/2018's incisos XXIII-A and XXIV-A and §§ 9º-A and "
                   "10-A as 'XXIIIA', 'XXIVA -', '§ 9º A' and '§ 10A.', and Medida Provisória 844/2018's art. 4º-A as 'Art. "
                   "4ºA.'; the MPs' own pages read 'XXIII-A', 'XXIV -A', '§ 9º-A', '§ 10-A.' and 'Art. 4º-A'. The lines keep the "
                   "MPs' labels, and MP 844's art. 4º-A with its paragraphs and incisos is read as art. 4º-A, not as lines of "
                   "art. 4 (" + ", ".join(dict.fromkeys(L9984_FIXED)) + ").")
    if PROM14119_USED:
        dec.append("Lei 14.119/2021: parts vetoed on 13.1.2021 and kept by Congress were promulgated by the President on 26.3.2021 "
                   "(DOU 26.3.2021, edição extra-D: art. 6 § 8º, art. 8 § 1º, arts. 13, 15 and 16) and on 10.6.2021 (DOU 11.6.2021, "
                   "though the footer of the promulgation on Planalto's page prints '11.1.2021': art. 17 and its parágrafo único); "
                   "the days are read on the Chamber of Deputies' records of the two promulgations. Each '(VETADO)' line Planalto "
                   "prints stands from 14.1.2021 to the promulgation; the promulgated text starts on the day of its DOU, credited to "
                   "Lei 14.119, without the quotation marks of the promulgation's own text (" + "; ".join(PROM14119_USED) + ").")
    if L9434_FIXED:
        dec.append("Lei 9.434 art. 10: Planalto prints Lei 10.211/2001's § 1º without its '§' sign ('1º Nos casos em que o receptor "
                   "[...]'); read as '§ 1º' (" + ", ".join(dict.fromkeys(L9434_FIXED)) + ").")
    if L11442_FIXED:
        dec.append("Lei 11.442 art. 13: Planalto prints the placeholder 'Parágrafo único. (Revogado).' (Lei 14.599/2023) above the "
                   "caput Lei 14.599 gave the article, right after the struck parágrafo único of 2007; it is kept as the article's "
                   "last line, after § 9º (" + ", ".join(dict.fromkeys(L11442_FIXED)) + ").")
    if LFUNDEB_FIXED:
        dec.append("Lei 14.113 art. 26: Lei 14.276/2021 (DOU 28.12.2021) art. 1 made the parágrafo único § 1º, with the same words; "
                   "Planalto notes the new § 1º '(Transformado em § 1º pela Lei nº 14.276, de 2021)', which is read as that "
                   "renumbering (the parágrafo único stands to 28.12.2021, § 1º from then, credited to Lei 14.276), and the space "
                   "missing after the struck 'Parágrafo único.' is restored (" + ", ".join(dict.fromkeys(LFUNDEB_FIXED)) + ").")
    if L4886_FIXED:
        dec.append("Lei 4.886: Lei 8.420/1992 (DOU 11.5.1992, in force on publication) art. 3: 'São suprimidos o parágrafo único "
                   "do art. 10, o parágrafo único do art. 17 e o art. 41'; Planalto marks those struck lines '(Suprimido)', "
                   "naming no law, and they end on 11.5.1992, credited to Lei 8.420. Lei 12.246/2010 art. 1 gave art. 10 a '§ 1º "
                   "(Suprimido)' (its own words): that line reads '§ 1º (Suprimido).' (" + ", ".join(dict.fromkeys(L4886_FIXED))
                   + ").")
    if LRC_RENUM:
        dec.append("Lei 4.886 art. 10: Lei 12.246/2010 (DOU 28.5.2010) art. 1 renumbered 'as atuais alíneas a a g para incisos I "
                   "a VII' and changed no words; Planalto prints only the incisos, noted 'Renumerado pela Lei nº 12.246, de 2010'. "
                   "The alíneas stand under their letters, with the same words, from 10.12.1965 to 28.5.2010 ("
                   + ", ".join(dict.fromkeys(LRC_RENUM)) + ").")
    if MESC_RENUM:
        dec.append("Lei 9.870: Medida Provisória 2.173-24/2001 (DOU 24.8.2001) arts. 1 and 2 added art. 1 §§ 3º-4º and art. 6 § 1º "
                   "and renumbered the paragraphs after them ('renumerando-se os atuais §§ 3º e 4º para §§ 5º e 6º'; 'os atuais "
                   "§§ 1º, 2º e 3º para §§ 2º, 3º e 4º'), changing no words; Planalto prints only the new numbers, noted "
                   "'Renumerado'. The paragraphs stand under their old numbers, with the same words, from 24.11.1999 to 24.8.2001 ("
                   + ", ".join(dict.fromkeys(MESC_RENUM)) + ").")
    if LRC_RENUM92:
        dec.append("Lei 4.886: Lei 8.420/1992 (DOU 11.5.1992) art. 2 added articles 'que passarão a ter os números 41, 42, 43, 44, "
                   "45, 46 e 47'; the 1965 arts. 42 and 43 (in-force and revocation clauses; the Chamber's copy of the original "
                   "publication of 10.12.1965) became arts. 48 and 49 with the same words. Planalto prints only the new numbers, "
                   "with no note: each stands under its 1965 number to 11.5.1992 (" + ", ".join(dict.fromkeys(LRC_RENUM92)) + ").")
    if ANA_437:
        dec.append("Lei 9.984: Medida Provisória 437/2008 (DOU 30.7.2008, in force on publication) added art. 4 XIX and § 8º, "
                   "art. 19-A and art. 20 XI and parágrafo único. Medida Provisória 439/2008 (DOU 29.8.2008, edição extra, in "
                   "force on publication) art. 4: 'Fica revogada a Medida Provisória nº 437, de 29 de julho de 2008'; MP 439 was "
                   "converted into Lei 11.805/2008, whose art. 4 says the same. Every line MP 437 gave Lei 9.984 ends on "
                   "29.8.2008, credited to MP 439 (Planalto's note 'Vide Medida Provisória nº 439, de 1998' misprints the year); "
                   "Lei 12.058/2009 added art. 4 XIX and § 8º again from 14.10.2009 (" + ", ".join(dict.fromkeys(ANA_437)) + ").")
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
    _BX = ("l9430", "l9873", "l9984", "l10637", "l10833", "l9807")
    if any(x.startswith("l9807") for x in BARE_TEXT_USED):
        dec.append("Lei 9.807 art. 17 begins 'O parágrafo único do art. 58 da Lei nº 6.015, de 31 de dezembro de 1973, com a redação "
                   "dada pela Lei nº 9.708, de 18 de novembro de 1998, passa a ter a seguinte redação:': these words name the wording "
                   "of the article it rewrites; they are part of the text, not an amendment note (l9807 art-17).")
    if any(not x.startswith(_BX) for x in BARE_TEXT_USED):
        dec.append("Lei 7.689 art. 11 and Lei 9.249 art. 14 end '[...], com a redação dada pelo Decreto-Lei nº [...]' (Decretos-"
                   "Leis 2.449/1988 and 1.730/1979): these words name the wording of the other act the article refers to; they "
                   "are part of the article's text, not an amendment note (" + ", ".join(x for x in BARE_TEXT_USED if not x.startswith(_BX)) + ").")
    if any(x.startswith("l10637") for x in BARE_TEXT_USED):
        dec.append("Lei 10.637 art. 47 § 2º ('[...] o art. 14 da Lei nº 9.648, de 27 de maio de 1998, com a redação dada pela Lei nº "
                   "10.433, de 24 de abril de 2002, para efeitos de incidência [...]') and the 2002 wording of art. 54 ('[...] o art. "
                   "1º do Decreto-Lei nº 1.593, de 21 de dezembro de 1977, com a redação dada pela Medida Provisória nº 2.158-35, de 24 "
                   "de agosto de 2001.'): these words name the wording of the other act the article refers to; they are part of the "
                   "text, not an amendment note (" + ", ".join(dict.fromkeys(x for x in BARE_TEXT_USED if x.startswith("l10637"))) + ").")
    if any(x.startswith("l10833") for x in BARE_TEXT_USED):
        dec.append("Lei 10.833 art. 23 ('[...] da Lei nº 9.718, de 27 de novembro de 1998, com a redação dada pela Lei nº 9.990, de "
                   "21 de julho de 2000, sobre os gases [...]'), the 2003 wording of art. 25 ('[...] com a redação dada pela Lei "
                   "nº 10.548, de 13 de novembro de 2002.') and art. 40 ('O caput do art. 1º do Decreto-Lei nº 1.593, de 21 de "
                   "dezembro de 1977, com a redação dada pela Medida Provisória nº 2.158-35, de 24 de agosto de 2001, e o art. 18 do "
                   "mesmo Decreto-Lei passam a vigorar [...]'): these words name the wording of the other act the article refers to; "
                   "they are part of the text, not an amendment note (" + ", ".join(dict.fromkeys(x for x in BARE_TEXT_USED
                                                                                                  if x.startswith("l10833"))) + ").")
    if QUOTE_DROPPED:
        dec.append("Lei 9.249 art. 9: the caput as Medida Provisória 694/2015 worded it (1.1.2016 to its lapse on 8.3.2016) is "
                   "printed after the opening quotation mark of the MP's quoted text; the mark is left out.")
    if PROMULGATED_USED:
        dec.append("Lei 13.675: Lei 14.531/2023 (DOU 11.1.2023, in force on publication) added art. 9 § 2º XVII and art. 42-A "
                   "§ 7º, but they were vetoed; Congress overrode the vetoes and they were promulgated in the DOU of 19.7.2023 "
                   "(printed on Lei 14.531's page). Planalto notes them '(Incluído pela Lei nº 14.531, de 2023)' with the "
                   "law's other lines; they start on 19.7.2023, credited to Lei 14.531: " + ", ".join(PROMULGATED_USED) + ".")
    if LPLR_905:
        dec.append("Lei 10.101 and Medida Provisória 905/2019: arts. 6, 6º-A and 6º-B, which MP 905 revoked, are printed struck "
                   "with MP 905's note and again unstruck with Lei 11.603's note; the unstruck copy is the article in force again "
                   "from 19.8.2020, when MP 905 lapsed, and the struck copy stands until Medida Provisória 955/2020 lapsed "
                   "(18.8.2020; absent while MP 905 stood). Art. 2 §§ 3º-A and 5º to 10 and their incisos: MP 905 added them "
                   "and Lei 14.020/2020 (DOU 7.7.2020, in force on publication) added them again; MP 905's wordings end when MP "
                   "955 revoked the MP (20.4.2020) and do not come back on 18.8.2020, MP 905's last day, because by then Lei "
                   "14.020 had given those paragraphs their wording; Medida Provisória 388/2007's wordings of arts. 6º-A and 6º-B, "
                   "printed twice, are read once (" + "; ".join(dict.fromkeys(LPLR_905)) + ").")
    if any(x.startswith("l10101") for x in FOREIGN_DROPPED):
        dec.append("Lei 10.101: the unlabelled line 'Participação nos lucros e prêmios' Planalto prints above art. 2 with no note "
                   "is the heading of Medida Provisória 905/2019's own art. 48 (as printed on the MP's page), copied onto the page "
                   "with MP 905's wordings; it is not a word of Lei 10.101 and is left out.")
    if any(x.startswith("l0605") for x in FOREIGN_DROPPED):
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
    if any(a["slug"] == _L9718 for a in ACTS):
        dec.append("Lei 9.718: art. 17 ('Esta Lei entra em vigor na data de sua publicação, produzindo efeitos: I - em relação aos "
                   "arts. 2º a 8º, para os fatos geradores ocorridos a partir de 1º de fevereiro de 1999; II - em relação aos arts. "
                   "9º e 12 a 15, a partir de 1º de janeiro de 1999'; DOU 28.11.1998): arts. 2 to 8 start on 1.2.1999, arts. 9 and "
                   "12 to 15 on 1.1.1999, the other articles on 28.11.1998" + (
                       "; changes made to those articles before their day start on that day (" + "; ".join(dict.fromkeys(G9718_USED))
                       + ")" if G9718_USED else "") + ".")
    if any(a["slug"] == _L10637 for a in ACTS):
        dec.append("Lei 10.637: art. 68 ('Esta Lei entra em vigor na data de sua publicação, produzindo efeitos: I - a partir de "
                   "1º de outubro de 2002, em relação aos arts. 29 e 49; II - a partir de 1º de dezembro de 2002, em relação aos "
                   "arts. 1º a 6º e 8º a 11; III - a partir de 1º de janeiro de 2003, em relação aos arts. 34, 37 a 44, 46 e 48; "
                   "IV - a partir da data da publicação desta Lei, em relação aos demais artigos'; DOU 31.12.2002): arts. 34, 37 "
                   "to 44, 46 and 48 start on 1.1.2003; the other articles on 31.12.2002 (the effects under I and II reach back "
                   "before the publication, which is the first day of the record)" + (
                       "; changes made to those articles before their day start on that day (" + "; ".join(dict.fromkeys(G10637_USED))
                       + ")" if G10637_USED else "") + ".")
    if any(a["slug"] == "lei-do-regime-fiscal-sustentavel" for a in ACTS):
        dec.append("Lei Complementar 200/2023: art. 15 ('Esta Lei Complementar entra em vigor: I - em 1º de janeiro de 2024, quanto "
                   "ao art. 11; e II - na data de sua publicação, quanto aos demais dispositivos'; DOU 31.8.2023): art. 11 (its "
                   "changes to Lei Complementar 101/2000) starts on 1.1.2024, the other articles on 31.8.2023" + (
                       "; changes made to art. 11 before that day start on it (" + "; ".join(dict.fromkeys(GLC200_USED)) + ")"
                       if GLC200_USED else "") + ".")
    if any(a["slug"] == _L10833 for a in ACTS):
        dec.append("Lei 10.833: art. 93 ('Esta Lei entra em vigor na data de sua publicação, produzindo efeitos, em relação: I - "
                   "aos arts. 1º a 15 e 25, a partir de 1º de fevereiro de 2004; II - aos arts. 26, 27, 29, 30 e 34 desta Lei, a "
                   "partir de 1º de fevereiro de 2004; [...] IV - aos arts. 49 a 51 e 53 a 58 desta Lei, a partir do 1º dia do "
                   "quarto mês subseqüente ao de sua publicação; V - ao art. 52 desta Lei, a partir do 1º dia do segundo mês "
                   "subseqüente ao de publicação desta Lei; VI - aos demais artigos, a partir da data da publicação desta Lei'; "
                   "DOU 30.12.2003): arts. 1 to 15, 25 to 27, 29, 30, 34 and 52 start on 1.2.2004, arts. 49 to 51 and 53 to 58 "
                   "on 1.4.2004, the other articles on 30.12.2003" + (
                       "; changes made to those articles before their day start on that day (" + "; ".join(
                           dict.fromkeys(x for x in G10833_USED if not x.startswith("art-58-"))) + ")"
                       if any(not x.startswith("art-58-") for x in G10833_USED) else "") + ".")
        bev = list(dict.fromkeys(x.split()[0] for x in G10833_USED if x.startswith("art-58-")))
        if bev:
            dec.append("Lei 10.833 arts. 58-A to 58-V (special regime for water, soft drinks and beer): Lei 11.727/2008 (DOU "
                       "24.6.2008) art. 32 added arts. 58-A to 58-U; its art. 41 ('Esta Lei entra em vigor na data de sua "
                       "publicação, produzindo efeitos em relação: [...] VII - aos arts. 32 a 39, a partir de 1º de janeiro de "
                       "2009', VII as Medida Provisória 436/2008 and Lei 11.827/2008 worded it) gives them effect from 1.1.2009, "
                       "and Medida Provisória 451/2008 art. 10 added art. 58-V to the same regime. The articles start on "
                       "1.1.2009; wordings Medida Provisória 436 and Lei 11.827 gave them before that day start on it, and "
                       "wordings replaced before it never show (" + ", ".join(bev) + ").")
    if L10833_FIXED:
        dec.append("Lei 10.833 art. 43: item 1 of the quoted alínea c) ('1. em relação aos fatos geradores que ocorrerem no período "
                   "de 1º de janeiro de 2004 até 31 de dezembro de 2004: [...]; e') ends without a full stop, like a heading, and "
                   "would be read as the heading of art. 44; it is a line of art. 43's quoted text and stays there.")
    if REV2009_USED:
        dec.append("Lei 10.833 arts. 49, 50, 52, 55, 57 and 58: Lei 11.727/2008 art. 42 ('Ficam revogados: [...] IV - a partir de "
                   "1º de janeiro de 2009: a) os arts. 49, 50, 52, 55, 57 e 58 da Lei nº 10.833, de 29 de dezembro de 2003, não "
                   "havendo, após essa data, outra forma de tributação além dos 2 (dois) regimes previstos nos arts. 58-A a 58-U "
                   "[...]', IV as Lei 11.827/2008 worded it, read on Lei 11.727's page) revokes them from 1.1.2009. Planalto "
                   "prints them unstruck, with only a 'Vide Lei nº 11.727, de 2008' pointer; the law's text governs, so they "
                   "end on 1.1.2009, credited to Lei 11.727 (" + ", ".join(dict.fromkeys(REV2009_USED)) + "). Art. 58 caput "
                   "incisos I and II, which Planalto prints struck with no note: Lei 11.051/2004 art. 25 rewrote only § 1º of "
                   "art. 58 (the caput and its incisos are dotted lines in its text), so they stand until 1.1.2009 with the "
                   "article.")
    if EFX_FIXED:
        dec.append("Lei 10.833: Planalto's annotated page prints 'efeito' where the Lei says 'efeitos' (for example art. 23 'gases "
                   "liquefeito de petróleo', art. 93 'produzindo efeito', art. 94 VI 'dos efeito desta Lei'); Planalto's "
                   "page of the consolidated text (l10.833compilado.htm) and the Chamber of Deputies' copy of the original publication (DOU 30.12.2003, edição "
                   "extra-A) print 'efeitos'. A line whose words are found in none of those texts, the page of the act its note "
                   "names or the page of Lei 11.727/2008 (which added arts. 58-A to 58-U), but are found there with 'efeitos' in place of 'efeito', takes those words (comparison of "
                   "letters and digits only; " + str(len(dict.fromkeys(EFX_FIXED))) + " lines: " + ", ".join(dict.fromkeys(EFX_FIXED)) + ").")
    if EFX_OPEN:
        dec.append("Lei 10.833: lines with 'efeito' that no other text settles, kept as the annotated page prints them ("
                   + ", ".join(dict.fromkeys(EFX_OPEN)) + ").")
    if MP1159_SKIPPED:
        dec.append("Leis 10.637 and 10.833: Medida Provisória 1.159/2023 (DOU 12.1.2023) lapsed on 1.6.2023 (Ato Declaratório do "
                   "Presidente da Mesa do Congresso Nacional nº 40, de 2023); Planalto prints the wordings it had replaced a second "
                   "time, struck, as restored on its lapse, but Lei 14.592/2023 (DOU 30.5.2023, in force on publication) had given "
                   "those dispositivos their wording before that day, so the restored copies never were in force and are left out ("
                   + ", ".join(dict.fromkeys(MP1159_SKIPPED)) + ").")
    for _slug, _used in FUT2027_USED.items():
        if _used:
            dec.append(_FUT2027[_slug][2] + " (" + ", ".join(dict.fromkeys(_used)) + ").")
    if L2027_USED:
        dec.append("Lei 9.718: Lei Complementar 214/2025 art. 542 ('Ficam revogados a partir de 1º de janeiro de 2027: [...] X - os "
                   "arts. 2º a 8º-B da Lei nº 9.718, de 27 de novembro de 1998') and art. 504 (new wording of art. 9, without 'da "
                   "contribuição PIS/PASEP e da COFINS'), both in effect from 1.1.2027 (art. 544 III, as Lei Complementar 227/2026 "
                   "worded it), read on LC 214's page (Planalto's page of Lei 9.718 does not print them): arts. 2 to 8-B end and "
                   "art. 9 takes the new wording on 1.1.2027, on the future branch (" + ", ".join(dict.fromkeys(L2027_USED)) + ").")
    if R_PUB_USED:
        dec.append("Medida Provisória editions whose Planalto page ends 'Este texto não substitui o publicado no DO de ...' ('DO', "
                   "not 'DOU'): their DOU day is read from that line (" + "; ".join(
                       f"{P.law_label(k)}: {_R_PUB[k][1]}" for k in sorted(dict.fromkeys(R_PUB_USED))) + ").")
    if L9718_FIXED:
        dec.append("Lei 9.718: Planalto's marker 'Sem eficácia' after the struck line of Medida Provisória 252/2005 (lapsed) is "
                   "not part of the text and is left out (" + ", ".join(dict.fromkeys(L9718_FIXED)) + ").")
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
    if L9782_LEFT_OUT:
        dec.append("Lei 9.782: Lei 15.524/2026 added art. 8º-A (Planalto: 'Incluído pela Lei nº 15.524, de 2026'); no copy "
                   "of that Lei could be read, so the day it took effect is not known: the article is LEFT OUT of every "
                   "version (" + "; ".join(dict.fromkeys(L9782_LEFT_OUT)) + ").")
    if L8745_FIXED:
        dec.append("Lei 8.745 art. 2 VI d) and art. 4 caput: Planalto's pointers '(Prorrogação de prazo).' (to Medida Provisória "
                   "431/2008 art. 173, struck) and '(Prorrogação de prazo pela Lei nº 11.784, de 2008' (to Lei 11.784/2008 art. "
                   "173, closing parenthesis missing) name the law that extended contracts already in force; they change no "
                   "words and are left out of the text, with the stray full stops between them (" + ", ".join(dict.fromkeys(
                       x for x in L8745_FIXED)) + ").")
    if EMPTY_ITEMS:
        dec.append("Struck items printed with a label and only the note '(Vide Medida nº 340, de 2006)', and no words, are "
                   "pointers, not wordings, and are left out (" + ", ".join(dict.fromkeys(EMPTY_ITEMS)) + ").")
    B5.EXTRA_DECISIONS.extend(dec)
    return _inner17(*a)


B6.PB5B._write_part5 = _inner

# part y: Lei 9.961/2000 (ANS) and Lei 9.717/1998 (RPPS); their MP editions are read by batch 6's edition reader
B13.OPEN_ITEMS["lei-da-ans"] = (
    "Lei 9.961 (open items): the editions of the Medida Provisória 1.976 / 2.097 / 2.177 chain that Planalto's notes do not "
    "name are not modelled (each named edition is dated by its own DOU day); wordings credited to two editions whose text "
    "is not on the earlier edition's own page keep the later edition's day (listed in the decisions); 'Vide' pointers "
    "strike no words")
B13.OPEN_ITEMS["lei-9717-de-1998"] = (
    "Lei 9.717 (open items): the editions of the Medida Provisória 1.891 / 2.043 / 2.187 chain that Planalto's notes do "
    "not name (before 1.891-8 of 24.9.1999 and between the named ones) are not modelled; each named edition is dated by its "
    "own DOU day; 'Vide' pointers strike no words")

# part z: Lei 9.427/1996 (ANEEL). Hand days set only when the act runs.
_LANEEL = "lei-da-aneel"
if any(a["slug"] == _LANEEL for a in ACTS):
    P.VIGENCIA_FIXED["mp-1300-2025"] = (
        "2025-05-21", "'Esta Medida Provisória entra em vigor: I - quarenta e cinco dias [...] quanto ao art. 6º; II - em 1º de "
                      "janeiro de 2026, quanto ao art. 8º; e III - na data de sua publicação, quanto aos demais dispositivos' (DOU "
                      "21.5.2025, edição extra): its art. 2 (Lei 9.427) and art. 9 I a) (the revocation of Lei 9.427 art. 20 § 1º I "
                      "and II) fall under III")
    P.VIGENCIA_FIXED["lei-15235-2025"] = (
        "2025-10-09", "'Esta Lei entra em vigor: I - em 1º de janeiro de 2026, quanto ao inciso III do caput do art. 5º; e II - "
                      "na data de sua publicação, quanto aos demais dispositivos' (DOU 9.10.2025): the conversion of Medida "
                      "Provisória 1.300/2025; of the MP's changes to Lei 9.427 it keeps only the revocation of art. 20 § 1º I and "
                      "II (its art. 5 I, under II)")
    P.MP_LAPSE["mp-1212-2024"] = (
        "2024-08-08", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 62, de 2024 (DOU 16.8.2024): 'teve seu "
                      "prazo de vigência encerrado no dia 7 de agosto de 2024'; the wordings it replaced or revoked are back from "
                      "8.8.2024")
_W1300 = ("Lei 9.427 art. 3 XVII and art. 20 § 1º: Medida Provisória 1.300/2025 (DOU 21.5.2025, in force on publication for its "
          "art. 2) gave both new wordings; Lei 15.235/2025, its conversion (DOU 9.10.2025, in force on publication), does not keep "
          "the MP's art. 2 (it keeps only the revocation of art. 20 § 1º I and II, its art. 5 I), so the MP's wordings end on "
          "9.10.2025 and the earlier wordings are in force again from that day until Lei 15.269/2025 (DOU 25.11.2025) rewrote "
          "them: Planalto prints each earlier wording a second time, struck, between the MP's wording and Lei 15.269's")
_E1300 = {"end": "2025-10-09", "end_law": "lei-15235-2025", "end_how": "conversion"}
_R1300 = {"start": "2025-10-09", "start_law": "lei-15235-2025", "restored": True,
          "end": "2025-11-25", "end_law": "lei-15269-2025", "end_how": "successor"}
_W12 = ("Lei 9.427 art. 26 § 12: added by Lei 14.120/2021 (DOU 2.3.2021) but vetoed ('§ 12. (VETADO).'); Congress overrode "
        "the veto and the paragraph was promulgated on 10.6.2021 (DOU 11.6.2021, printed on Lei 14.120's page). The '(VETADO)' "
        "line stands from 2.3.2021 to 11.6.2021, the promulgated paragraph from 11.6.2021, credited to Lei 14.120")
B8.SPAN_FIX += [
    ((_LANEEL, "art-03", "XVII -", "XVII - estabelecer mecanismos de regulação e fiscalização para garantir o atendimento ao "
      "mercado", 0), dict(_E1300), _W1300),
    ((_LANEEL, "art-03", "XVII -", "XVII - estabelecer mecanismos de regulação e fiscalização para garantir o atendimento à "
      "totalidade", 1), dict(_R1300), _W1300),
    ((_LANEEL, "art-20", "§ 1º", "§ 1º A descentralização abrangerá os serviços e as instalações", 0), dict(_E1300), _W1300),
    ((_LANEEL, "art-20", "§ 1º", "§ 1º A descentralização abrangerá os serviços e instalações", 1), dict(_R1300), _W1300),
    ((_LANEEL, "art-26", "§ 12", "§ 12. (VETADO", 0),
     {"end": "2021-06-11", "end_law": "lei-14120-2021", "end_how": "promulgation"}, _W12),
    ((_LANEEL, "art-26", "§ 12", "§ 12. O agente titular", 0),
     {"start": "2021-06-11", "start_law": "lei-14120-2021", "promulgated": True}, _W12),
]
B13.OPEN_ITEMS[_LANEEL] = (
    "Lei 9.427 (open items): the republication of 28.9.1998 (Lei 9.648/1998 art. 22) is read as Planalto prints the Lei; 'Vide' "
    "pointers and regulations strike no words and are not modelled")

# part za: Lei 8.745/1993 (contratação temporária). Hand days set only when the act runs.
_LCTEMP = "lei-da-contratacao-temporaria"
if any(a["slug"] == _LCTEMP for a in ACTS):
    P.MP_LAPSE["mp-1181-2023"] = (
        "2023-11-15", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 79, de 2023: 'teve seu prazo de vigência "
                      "encerrado no dia 14 de novembro de 2023'; the wordings it gave Lei 8.745 end on 15.11.2023 unless a law "
                      "replaced them earlier")
    P.MP_LAPSE["mp-1186-2023"] = (
        "2024-02-20", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 7, de 2024 (DOU 1.3.2024): 'teve seu "
                      "prazo de vigência encerrado no dia 19 de fevereiro de 2024'; the wordings it gave Lei 8.745 end on 20.2.2024")
    P.MP_PENDING["mp-2229-2001"] = (
        "Medida Provisória nº 2.229-43, de 6.9.2001 (DOU 10.9.2001, in force on publication), kept in force by Emenda "
        "Constitucional 32/2001, art. 2; it added Lei 8.745 art. 4 § 7º. Planalto's note names this edition only, so the change "
        "is dated by its publication; earlier editions of the chain are not modelled")
    P.NOTE_FIX["(Incluído pela MPV nº 2.229-43, de 6.9.2001)"] = (
        "(Incluído pela Medida Provisória nº 2.229-43, de 6.9.2001)",
        "Lei 8.745 art. 4 § 7º: the note abbreviates 'Medida Provisória' as 'MPV'")
_W922PU = ("Lei 8.745 art. 4 parágrafo único ('É admitida a prorrogação dos contratos:', Lei 10.667/2003): Medida Provisória "
           "922/2020 (DOU 2.3.2020) made it § 1º with new incisos and added a § 2º; the MP lapsed on 29.6.2020 (Ato Declaratório "
           "72/2020) and the parágrafo único is in force again from 30.6.2020, as its incisos (it was read as renumbered for good)")
_W5PU = ("Lei 8.745 art. 5 parágrafo único (1993): revoked by Lei 9.849/1999; Planalto prints it a second time, unstruck and "
         "with the same revocation note, below the article's restored caput; that copy is not in force and is left out")
B8.SPAN_FIX += [
    ((_LCTEMP, "art-04", "Parágrafo único", "Parágrafo único. É admitida a prorrogação dos contratos", 0),
     {"end": None, "end_law": None, "end_how": None}, _W922PU),
    ((_LCTEMP, "art-05", "Parágrafo único", "Parágrafo único. Os órgãos ou entidades contratantes", 1),
     {"skip": True, "end_how": "revoked-copy"}, _W5PU),
    ((_LCTEMP, "art-04", "§ 8º", "§ 8º", 0), {"skip": True, "end_how": "pointer"},
     "Lei 8.745 art. 4: Planalto prints a struck line holding only '§ 8º' and the note '(Vide Medida Provisória nº 86, de "
     "18.12.2002)'; it is a pointer, not a wording, and is left out"),
]
B.EXPLAINED[_LCTEMP] = {"art-05": "the consolidated page prints art. 5's parágrafo único (1993), revoked by Lei 9.849/1999, "
                                  "unstruck with its revocation note; it is not in force and is left out"}
B13.OPEN_ITEMS[_LCTEMP] = (
    "Lei 8.745 (open items): the STF's ADI 2.380 (Planalto prints only 'Vide ADIN 2380') is not modelled; Medida Provisória "
    "2.229-43/2001 is dated by that edition (earlier editions of the chain are not modelled); 'Vide' pointers (Medidas "
    "Provisórias 86/2002, 319/2006, 341/2006 and 2.216-37/2001, Lei 11.204/2005, decrees) and the 'Prorrogação de prazo' "
    "pointers to Medida Provisória 431/2008 and Lei 11.784/2008 (art. 173) strike no words and are not modelled")

# part zb: Lei 9.782/1999 (Anvisa). Hand days set only when the act runs.
_LANVISA = "lei-da-anvisa"
if any(a["slug"] == _LANVISA for a in ACTS):
    P.MP_PENDING["mp-2190-2001"] = (
        "Medida Provisória nº 2.190-34, de 23.8.2001 (DOU 24.8.2001, in force on publication), kept in force by Emenda "
        "Constitucional 32/2001, art. 2; it gave Lei 9.782 the wordings Planalto notes with this edition. Earlier editions of "
        "the chain (1.814, 1.912, 2.000, 2.039, 2.134) are named only in 'Vide' notes, except 2.039-24 (art. 3 caput)")
    P.MP_PENDING["mp-2039-2000"] = (
        "Medida Provisória nº 2.039-24, de 21.12.2000: Planalto's page reads 'Revogada e Reeditada pela Medida Provisória nº "
        "2.134-25'; its wording of Lei 9.782 art. 3 caput is on the pages of 2.039-24 and 2.190-34 (both named in the note) "
        "and stayed in force through the reissues to 2.190-34, which Emenda Constitucional 32/2001 kept in force")
    for _how in ("Incluído", "Redação dada"):
        P.NOTE_FIX[f"({_how} pela Lei nº 13.411, de 2017)"] = (
            f"({_how} pela Lei nº 13.411, de 2016)",
            f"Lei 9.782: the notes read '{_how} pela Lei nº 13.411, de 2017'; the link goes to Lei 13.411 of 28.12.2016 (L13411.htm, DOU "
            "29.12.2016, in force 90 days after publication)")
    P.MP_LAPSE["mp-557-2011"] = (
        "2012-06-01", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 26, de 2012 (DOU 14.6.2012): 'teve seu "
                      "prazo de vigência encerrado no dia 31 de maio do corrente ano'; its changes to Lei 9.782 end on 1.6.2012")
B.EXPLAINED[_LANVISA] = {"titulos": "the annotated page prints 'CAPÍTULO I' without the chapter's name ('DO SISTEMA NACIONAL "
                                    "DE VIGILÂNCIA SANITÁRIA'), which the consolidated page has; the history follows the "
                                    "annotated page"}
B13.OPEN_ITEMS[_LANVISA] = (
    "Lei 9.782 (open items): the text before 27.1.1999 (Medida Provisória 1.791/1998, of which this Lei is the conversion) is "
    "not part of the history; the Anexos (tables of posts and of the Taxa de Fiscalização de Vigilância Sanitária) are not "
    "part of the history; the editions of the Medida Provisória 1.814 / 1.912 / 2.000 / 2.039 / 2.134 / 2.190 chain that "
    "Planalto names only in 'Vide' notes are not modelled; wordings noted with Medida Provisória 2.190-34/2001 are dated by "
    "that edition. LEFT OUT: art. 8º-A, which Lei 15.524/2026 added (caput, parágrafo único and incisos I-II, noted "
    "'Incluído pela Lei nº 15.524, de 2026'): no copy of the Lei could be read, so its in-force day is not known and they are in no version")

# part zc: Leis 10.101/2000 (PLR), 9.608/1998 (serviço voluntário), 12.506/2011 (aviso prévio)
_LVOL = "lei-do-servico-voluntario"
if any(a["slug"] == _LVOL for a in ACTS):
    P.VIGENCIA_PROVISION[("mp-411-2007", _LVOL, "art-03-a")] = (
        "2008-01-01", "Medida Provisória 411/2007 (DOU 28.12.2007, in force on publication) art. 24: 'Ficam revogados, a partir "
                      "de 1º de janeiro de 2008: I - o art. 3º-A da Lei nº 9.608, de 18 de fevereiro de 1998'; Lei 11.692/2008, its "
                      "conversion, repeats the revocation (art. 24 I): art. 3º-A ends on 1.1.2008")

# part zd: Lei 12.334/2010 (barragens), Lei Complementar 105/2001 (sigilo bancário)
_LC105 = "lei-do-sigilo-bancario"
if any(a["slug"] == _LC105 for a in ACTS):
    P.VIGENCIA_FIXED["lc-166-2019"] = (
        "2019-07-09", "art. 7: 'Esta Lei Complementar entra em vigor: I - na data de sua publicação, quanto ao disposto: a) no "
                      "caput e no § 6º do art. 12 da Lei nº 12.414 [...]; e b) nos arts. 3º e 5º; II - após decorridos 91 (noventa e "
                      "um) dias de sua publicação oficial, quanto aos demais dispositivos' (DOU 9.4.2019): its art. 1 (Lei "
                      "Complementar 105 art. 1) falls under II; 91 days counted from the day of publication, in force on 9.7.2019")
    P.VIGENCIA_PROVISION[("lc-224-2025", _LC105, "art-01")] = (
        "2026-01-01", "Lei Complementar 224/2025 (DOU 26.12.2025, in force on publication) 'produzirá efeitos: [...] III - a "
                      "partir de 1º de janeiro de 2026, em relação aos demais dispositivos': its art. 3 (Lei Complementar 105 art. "
                      "1 § 3º VIII) takes effect on 1.1.2026")
B13.OPEN_ITEMS[_LC105] = (
    "Lei Complementar 105 (open items): the STF's rulings on the access of the tax authorities to bank data (ADIs 2.390, "
    "2.386, 2.397, 2.859) changed no words and are not modelled; 'Vide' pointers and regulations strike no words")

# part zf: Lei 9.984/2000 (ANA). Hand days set only when the act runs.
if any(a["slug"] == _LANA for a in ACTS):
    P.MP_PENDING["mp-437-2008"] = (
        "Medida Provisória nº 437, de 29.7.2008 (DOU 30.7.2008, in force on publication): revoked by Medida Provisória nº 439, "
        "de 29.8.2008 (DOU 29.8.2008, edição extra, art. 4), converted into Lei 11.805/2008 (art. 4); its lines in Lei 9.984 end "
        "on 29.8.2008")
    P.MP_PENDING["mp-2216-2001"] = (
        "Medida Provisória nº 2.216-37, de 31.8.2001 (DOU 1.9.2001, art. 32: in force on publication), kept in force by Emenda "
        "Constitucional 32/2001, art. 2; it added Lei 9.984 art. 4 XVIII and art. 18-A and revoked arts. 17 and 18. "
        "Planalto's notes name this edition only (Medida Provisória 2.049-21 and 2.049-23/2000 appear in 'Vide' notes), so the "
        "changes are dated by its publication; earlier editions of the chain are not modelled")
    B8.EXTRA_LAWS["mp-439-2008"] = {
        "label": "Medida Provisória nº 439, de 2008", "kind": "law",
        "title": "Constitui fonte de recursos adicional para ampliação de limites operacionais do Banco Nacional de "
                 "Desenvolvimento Econômico e Social - BNDES.",
        "enacted": "2008-08-29", "published": "2008-08-29",
        "url": PL + "_Ato2007-2010/2008/Mpv/439.htm", "temporary_until": None, "restores": None, "note": None}
_W4B = ("Lei 9.984 art. 4º-B: Planalto prints Medida Provisória 844/2018's art. 4º-B (in force 9.7.2018, lapsed 19.11.2018) "
        "after the art. 4º-B Lei 14.026/2020 gave it; the MP's wording stands from 9.7.2018 to 20.11.2018 only, before Lei "
        "14.026's, and is not a restored wording")
_W42 = ("Lei 9.984 art. 4 § 2º (2000): revoked by Medida Provisória 844/2018 (9.7.2018, lapsed 19.11.2018) and again by Medida "
        "Provisória 868/2018 (28.12.2018, lapsed 3.6.2019), then by Lei 14.026/2020 (16.7.2020). Planalto prints the 2000 "
        "wording three times, struck, one copy per revocation; it is one wording, absent while each MP stood and in force "
        "again from each lapse to 16.7.2020; the second and third copies are left out")
B8.SPAN_FIX += [
    ((_LANA, "art-04-b", "Art. 4º-B", "Art. 4º-B. O acesso aos recursos públicos federais", 0),
     {"start": "2018-07-09", "start_law": "mp-844-2018", "end": "2018-11-20", "end_law": "mp-844-2018-fim", "end_how": "lapse"},
     _W4B),
    ((_LANA, "art-04", "§ 2º", "§ 2º As ações a que se refere o inciso X deste artigo", 0),
     {"end": "2020-07-16", "end_law": "lei-14026-2020", "end_how": "successor",
      "gaps": [("2018-07-09", "2018-11-20", "mp-844-2018", "mp-844-2018-fim"),
               ("2018-12-28", "2019-06-04", "mp-868-2018", "mp-868-2018-fim")]}, _W42),
    ((_LANA, "art-04", "§ 2º", "§ 2º As ações a que se refere o inciso X deste artigo", 1),
     {"skip": True, "end_how": "duplicate"}, _W42),
    ((_LANA, "art-04", "§ 2º", "§ 2º As ações a que se refere o inciso X deste artigo", 2),
     {"skip": True, "end_how": "duplicate"}, _W42),
]
B13.OPEN_ITEMS[_LANA] = (
    "Lei 9.984 (open items): art. 4 XVIII, art. 18-A and the revocations of arts. 17 and 18 are dated by Medida "
    "Provisória 2.216-37/2001, the edition Planalto names (2.049-21 and 2.049-23/2000 appear only in 'Vide' notes; earlier "
    "editions of the chain are not modelled); 'Vide' pointers and regulations strike no words")

# part zg: Lei 11.182/2005 (ANAC), Lei 13.575/2017 (ANM). Hand days set only when the act runs.
_LANAC, _LANM = "lei-da-anac", "lei-da-anm"
if any(a["slug"] == _LANM for a in ACTS):
    B7.CONVERTED_FIX["mp-1133-2022"] = (
        "lei-14514-2022", "Medida Provisória 1.133/2022: its page reads 'Convertida na Lei nº 14 514, de 2022' (the full stop of "
                          "the number missing); Lei 14.514/2022 reads 'Conversão da Medida Provisória nº 1.133, de 2022'")
    P.VIGENCIA_FIXED["lei-14514-2022"] = (
        "2022-12-30", "art. 25: 'Esta Lei entra em vigor: I - (VETADO); II - na data de sua publicação, com produção de efeitos "
                      "[...] (Lei 8.001/1990); e III - na data de sua publicação, quanto aos demais dispositivos' (DOU 30.12.2022): its "
                      "art. 13 (Lei 13.575 art. 2 XXXVII-XL) falls under III")
    P.VIGENCIA_PROVISION[("lei-14514-2022", _LANM, "art-21")] = (
        "2024-05-22", "Lei 14.514/2022 art. 13, in the part that rewrote Lei 13.575 art. 21 (II-A, III, III-A, V, VII-IX, XI, XIII, "
                      "XIII-A, XV), art. 24 V b) (revocation of art. 21 X and XII) and art. 25 I ('em 1º de fevereiro de 2023, quanto "
                      "às alterações efetuadas pelo art. 13 no art. 21 da Lei nº 13.575') were vetoed; Congress overrode the vetoes "
                      "and the President promulgated them on 21.5.2024 (DOU 22.5.2024, printed at the foot of Lei 14.514's page). "
                      "A promulgated part is law only from its publication: the changes to art. 21 take effect on 22.5.2024")
_W34 = ("Lei 11.182 art. 34 quotes the wording it gave Lei 6.009/1973 art. 2 parágrafo único a); Medida Provisória 1.089/2021 "
        "revoked that alínea of Lei 6.009, not words of Lei 11.182. Planalto prints the quoted lines twice, struck with the MP's "
        "note and again unstruck; the struck copy is not a wording of Lei 11.182 and is left out")
B8.SPAN_FIX += [((_LANAC, "art-34", lab, pre, 0), {"skip": True, "end_how": "duplicate"}, _W34) for lab, pre in (
    ("", '"Art. 2º.'), ("Parágrafo único", "Parágrafo único."), ("a)", "a) por tarifas aeroportuárias"), ("", "....."))]
B.EXPLAINED[_LANAC] = {"art-34": "art. 34 quotes Lei 6.009's 'Parágrafo único.' (a label with dotted text, the quoted alínea a) "
                                  "below it); the check reads a line holding only a label as a revoked dispositivo and leaves "
                                  "it out of the page's side"}
B13.OPEN_ITEMS[_LANAC] = (
    "Lei 11.182 (open items): the Anexos (tables of posts and of the TFAC values) are not part of the history; Lei 11.292/2006 "
    "(in force on publication, 27.4.2006) gave art. 29 the wording that institutes the Taxa de Fiscalização da Aviação Civil "
    "'respeitando-se [...] o disposto nas alíneas b e c do inciso III do art. 150 da Constituição Federal': the tax could be "
    "charged only from 1.1.2007, but the wording replaced the 2005 one on publication and is dated by that day; 'Vide' pointers "
    "(Medida Provisória 269/2005) and regulations strike no words")
B13.OPEN_ITEMS[_LANM] = (
    "Lei 13.575 (open items): the text before 27.12.2017 (Medida Provisória 791/2017, of which this Lei is the conversion) is "
    "not part of the history; 'Vide' pointers and regulations strike no words")

# part zh: Leis 11.428/2006 (Mata Atlântica), 4.886/1965 (representantes comerciais), 8.397/1992 (cautelar fiscal), 9.795/1999
# (educação ambiental)
B.EXPLAINED["lei-da-mata-atlantica"] = {
    "art-48": "art. 48 quotes Lei 9.393's '§ 1º' with dotted text (a label-only line); the check reads a line holding only a "
              "label as a revoked dispositivo and leaves it out of the page's side"}
B13.OPEN_ITEMS["lei-da-mata-atlantica"] = (
    "Lei 11.428 (open items): the DOU of 26.12.2006 was rectified on 9.1.2007; Planalto prints the rectified text, which is "
    "read from the act's first day; Lei 15.190/2025's revocation of art. 14 §§ 1º and 2º (vetoed, then promulgated on 5.12.2025, "
    "DOU 8.12.2025, before the Lei's in-force day) takes effect with the Lei on 4.2.2026; 'Vide' pointers and regulations strike "
    "no words")
B13.OPEN_ITEMS["lei-dos-representantes-comerciais"] = (
    "Lei 4.886 (open items): the retificação of 20.12.1965 (art. 13: '2º' to be read '§ 2º') changes no words and is read from "
    "the act's first day; 'Vide' pointers strike no words")
if any(a["slug"] == "lei-dos-representantes-comerciais" for a in ACTS):
    B6.CONTEXT.append({
        "when": lambda: True,
        "pins": ["ctx:camara-lei-4886-1965-original", "ctx:camara-lei-4886-1965-retificacao"],
        "what": "the original publication of Lei 4.886/1965 (DOU 10.12.1965: the numbers of its last articles, 42 and 43) and "
                "its retificação (DOU 20.12.1965)"})
B13.OPEN_ITEMS["lei-da-medida-cautelar-fiscal"] = (
    "Lei 8.397 (open items): the DOU of 7.1.1992 was rectified on 16.1.1992; Planalto prints the rectified text, which is read "
    "from the act's first day")

# part zi: Leis 11.417/2006 (súmula vinculante), 13.460/2017 (usuários de serviços públicos), 12.187/2009 (PNMC), 13.123/2015
# (biodiversidade)
B13.OPEN_ITEMS["lei-dos-usuarios-de-servicos-publicos"] = (
    "Lei 13.460 (open items): the Lei and Lei 14.129/2021 (its amender) take effect in stages by level of government (Lei "
    "13.460 art. 25: 360 days for the União, the States, the Distrito Federal and Municipalities above 500,000 inhabitants, "
    "540 and 720 days for smaller Municipalities; Lei 14.129's in-force clause: 90 days for the União, 120 for States and the Distrito "
    "Federal, 180 for Municipalities); the history is dated by the federal stage (22.6.2018 and 28.6.2021), the later stages "
    "are not separate versions")
B13.OPEN_ITEMS["lei-da-biodiversidade"] = (
    "Lei 13.123 (open items): its text before the in-force day (17.11.2015) is the same as on that day (no change in between); "
    "Medida Provisória 2.186-16/2001, which it revokes (art. 50), is not part of the history; 'Vide' pointers and regulations strike no words")

# MP editions of 2000 whose pages end 'Este texto não substitui o publicado no DO de d.m.aaaa' ('DO', not 'DOU', which the
# reader does not take): their day is read from that line, keyed by the edition (batch 6 reads an edition's page under its
# base key, so the base key's PUBLISHED_FIXED would also date every other edition)
_R_PUB: dict[str, tuple[str, str]] = {}
R_PUB_USED: list[str] = []


def _with_pub(f):
    def g(key):
        if key not in _R_PUB:
            return f(key)
        d0 = P.decode
        P.decode = lambda b: re.sub(r"(publicado\s+no\s+DO)(\s+de\s)", r"\1U\2", d0(b))
        try:
            info = f(key)
        finally:
            P.decode = d0
        if info and info.get("published") == _R_PUB[key][0]:
            R_PUB_USED.append(key)
        return info
    return g


B6.page_info = _with_pub(B6.page_info)
P.page_info = B.page_info = _with_pub(P.page_info)

# part zj: Lei 9.718/1998 (PIS/Pasep and Cofins). Hand days set only when the act runs.
_L9718 = "lei-9718-de-1998"
if any(a["slug"] == _L9718 for a in ACTS):
    P.VIGENCIA_FIXED["lei-12844-2013"] = (
        "2013-07-19", "art. 49: 'Esta Lei entra em vigor: [...] V - na data de sua publicação para os demais dispositivos' "
                      "(DOU 19.7.2013, edição extra): its art. 36 (Lei 9.718 arts. 3 and 5) falls under V")
    P.VIGENCIA_FIXED["mp-472-2009"] = (
        "2009-12-16", "art. 60: 'Esta Medida Provisória entra em vigor: I - na data de sua publicação, produzindo efeitos: "
                      "[...] d) a partir da data de sua publicação, em relação aos demais dispositivos' (DOU 16.12.2009): its "
                      "art. 22 (Lei 9.718 art. 14 VII) falls under I d)")
    P.VIGENCIA_FIXED["mp-601-2012"] = (
        "2012-12-28", "art. 7: 'Esta Medida Provisória entra em vigor: [...] II - na data de sua publicação, produzindo efeitos a "
                      "partir de 1º de janeiro de 2013, em relação aos arts. 4º e 6º' (DOU 28.12.2012): its art. 6 (Lei 9.718 art. "
                      "3 §§ 10 to 12) is in force on publication, with effect from 1.1.2013 (effect day: effects_fix)")
    P.MP_LAPSE["mp-601-2012"] = (
        "2013-06-04", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 36, de 2013 (DOU 6.6.2013): 'teve seu "
                      "prazo de vigência encerrado no dia 3 de junho do corrente ano'; the wordings it gave Lei 9.718 end on "
                      "4.6.2013")
    P.MP_PENDING["mp-2158-2001"] = (
        "Medida Provisória nº 2.158-35, de 24.8.2001 (DOU 27.8.2001), kept in force by Emenda Constitucional 32/2001, art. 2; "
        "its art. 92 ('entra em vigor na data de sua publicação, produzindo efeitos: [...] IV - relativamente aos fatos "
        "geradores ocorridos a partir de: a) 1º de dezembro de 2001, relativamente ao disposto no § 9º do art. 3º da Lei nº "
        "9.718, de 1998') dates Lei 9.718 art. 3 § 9 from 1.12.2001 (effect day: effects_fix); its other changes to Lei 9.718 "
        "are in force on publication. Planalto's notes name this edition only; the editions before it are modelled only where "
        "a note names them (1.807/1999, 1.858-6/1999, 1.991-15 and 1.991-18/2000)")
    _R_PUB.update({"mp-1991-2000": ("2000-03-13", "13.3.2000"), "mp-1991r16-2000": ("2000-04-12", "12.4.2000"),
                   "mp-1991r18-2000": ("2000-06-10", "10.6.2000 (Edição extra)"), "mp-2037-2000": ("2000-06-29", "29.6.2000")})

    P.VIGENCIA_FIXED["lei-13043-2014"] = (
        "2015-01-01", "art. 113: 'Esta Lei entra em vigor na data de sua publicação, exceto: [...] II - os arts. 1º a 15, 30 a 32, "
                      "97, 106 e os artigos da Seção XXI do Capítulo I, que entram em vigor a partir de 1º de janeiro de 2015' (DOU "
                      "14.11.2014): its art. 30 (Lei 9.718 art. 3) falls under II")
    for _pg in ("l9718", "l9718-compilada"):
        B15.TEXT_FIX.append((_pg, 'Parágrafo único. Revogado. "$', "Parágrafo único. Revogado.",
                             "Lei 9.718 art. 4 parágrafo único (Lei 9.990/2000's wording): both Planalto pages print the closing "
                             "quotation mark of the amending text in the line"))
    B15.TEXT_FIX.append(("l9718", "observada regulamentação editada pelo Conselho Monetário Nacional.)$",
                         "observada regulamentação editada pelo Conselho Monetário Nacional.",
                         "Lei 9.718 art. 3 § 8 II (Medida Provisória 1.858-6/1999's wording): the annotated page prints a stray closing "
                         "parenthesis after the final full stop (the closing quotation mark of the MP's text); the MP's page has none"))
_W6 = ("Lei 9.718 art. 3 § 6 I and II: Medida Provisória 1.807/1999 added § 6 with incisos I to IV; its next editions, 1.858-6/1999 "
       "among them (read on its page), kept the same words, and Medida Provisória 2.158-35/2001 gave § 6 its present wording. The "
       "reader had ended I and II on 30.6.1999 at § 8's incisos I and II (added by 1.858-6), which are other provisions; "
       "they end with 2.158-35 (27.8.2001), as the rest of § 6")
_E2158 = {"end": "2001-08-27", "end_law": "mp-2158-2001", "end_how": "successor"}
_W1063 = ("Lei 9.718 art. 5: Medida Provisória 1.063/2021 (DOU 12.8.2021) art. 6: 'produz efeitos: I - na data da sua publicação, "
          "quanto ao: a) art. 1º, na parte que acresce o art. 68-D à Lei nº 9.478, de 1997; e b) art. 3º; e II - no primeiro dia do "
          "quarto mês subsequente ao de sua publicação, quanto aos demais dispositivos': its arts. 2 and 4 (Lei 9.718 art. 5) take "
          "effect on 1.12.2021, so its new lines start, and the lines it revoked or replaced end, on that day (effects_fix cannot "
          "move them: Medida Provisória 1.069/2021, in force on publication, 13.9.2021, changed the article in between). Its own "
          "wording of § 4º-A never took effect: Medida Provisória 1.069 replaced it on 13.9.2021, before that day")
_S1063 = {"start": "2021-12-01", "start_law": "mp-1063-2021"}
_E1063 = {"end": "2021-12-01", "end_law": "mp-1063-2021"}
B8.SPAN_FIX += [
    ((_L9718, "art-03", "I -", "I - no caso de bancos comerciais", 0), dict(_E2158), _W6),
    ((_L9718, "art-03", "II -", "II - no caso de empresas de seguros privados, os rendimentos", 0), dict(_E2158), _W6),
    ((_L9718, "art-05", "I -", "I - por distribuidor, no caso de venda de álcool anidro", 0), dict(_E1063, end_how="note"), _W1063),
    ((_L9718, "art-05", "II -", "II - por comerciante varejista, em qualquer caso", 0), dict(_E1063, end_how="successor"), _W1063),
    ((_L9718, "art-05", "II -", "II - por comerciante varejista, exceto na hipótese", 0), dict(_S1063), _W1063),
    ((_L9718, "art-05", "§ 3º", "§ 3º As demais pessoas jurídicas que comerciem álcool", 0), dict(_E1063, end_how="note"), _W1063),
    ((_L9718, "art-05", "§ 19", "§ 19. O disposto no § 3º não se aplica", 0), dict(_E1063, end_how="note"), _W1063),
    ((_L9718, "art-05", "§ 4º-A", "§ 4º-A Na hipótese de venda efetuada diretamente do produtor ou do importador", 0),
     {"skip": True, "end_how": "never-in-effect"}, _W1063),
    ((_L9718, "art-05", "I -", "I - nos incisos I e II do caput; ou", 0), dict(_S1063), _W1063),
    ((_L9718, "art-05", "II -", "II - nos incisos I e II do § 4º, observado", 0), dict(_S1063), _W1063),
    ((_L9718, "art-05", "§ 4º-B", "§ 4º-B As alíquotas de que trata o § 4º-A aplicam-se", 0), dict(_S1063), _W1063),
    ((_L9718, "art-05", "I -", "I - de o importador exercer também a função de distribuidor", 0), dict(_S1063), _W1063),
    ((_L9718, "art-05", "II -", "II - de as vendas serem efetuadas pelas pessoas jurídicas de que trata o inciso II ou III", 0),
     dict(_S1063), _W1063),
    ((_L9718, "art-05", "III -", "III - de as vendas serem efetuadas pelas demais pessoas jurídicas", 0), dict(_S1063), _W1063),
    ((_L9718, "art-05", "§ 4º-C", "§ 4º-C Na hipótese de venda de gasolina pelo distribuidor", 0), dict(_S1063), _W1063),
    ((_L9718, "art-05", "I -", "I - no inciso I do caput; ou", 0), dict(_S1063), _W1063),
    ((_L9718, "art-05", "II -", "II - no inciso I do § 4º, observado", 0), dict(_S1063), _W1063),
    ((_L9718, "art-05", "§ 13-A", "§ 13-A. O distribuidor sujeito ao regime", 0), dict(_S1063), _W1063),
    ((_L9718, "art-05", "§ 14-A", "§ 14-A. Os créditos de que trata o § 13-A", 0), dict(_S1063), _W1063),
]
B.EXPLAINED[_L9718] = {"art-05": "the consolidated page prints the end of a note ('. Vide Medida Provisória nº 497, de 2010)') inside "
                                  "the text of a paragraph of art. 5; the annotated page prints it as a note"}
B13.OPEN_ITEMS[_L9718] = (
    "Lei 9.718 (open items): the Lei's own articles take effect in stages (art. 17): arts. 2 to 8 for fatos geradores from "
    "1.2.1999, arts. 9 and 12 to 15 from 1.1.1999, the rest on publication (28.11.1998); each article starts on its day. Medidas "
    "Provisórias of the reissue chain 1.807/1999 to 2.158-35/2001 are modelled only where Planalto's notes name an edition "
    "(1.807, 1.858-6, 1.991-15, 1.991-18, 2.158-35); the other editions are not read. Medida Provisória 413/2008 (art. 5): its "
    "art. 18, as Medida Provisória 425/2008 worded it before the first fixed day arrived, tied the effect of its art. 7 to an act "
    "of the Receita Federal; Lei 11.727/2008, the conversion, fixed 1.10.2008; the MP's wording of art. 5 is not shown as in "
    "effect. Medida Provisória 1.069/2021 art. 6 § 1º (the 'noventena' for taxpayers who did not opt) is not modelled. 'Vide' "
    "pointers (Decretos 3.048/1999 and 6.573/2008, Lei Complementar 214/2025) are not modelled")

# Lei 9.718 art. 17: 'Esta Lei entra em vigor na data de sua publicação, produzindo efeitos: I - em relação aos arts. 2º a 8º,
# para os fatos geradores ocorridos a partir de 1º de fevereiro de 1999; II - em relação aos arts. 9º e 12 a 15, a partir de
# 1º de janeiro de 1999'. Those articles start on their day (gates, as Lei 9.279 in batch 8); a change made to a gated
# article before its day (Medida Provisória 1.807/1999, DOU 29.1.1999, art. 3 §§ 6 and 7) is dated by that day too.
_G9718 = {**{f"art-0{n}": ("1999-02-01", "arts. 2 to 8: I") for n in range(2, 9)},
          **{u: ("1999-01-01", "arts. 9 and 12 to 15: II") for u in ("art-09", "art-12", "art-13", "art-14", "art-15")}}
G9718_USED: list[str] = []
_build_act17 = P.build_act
# Date-by-article gates of acts whose own effect clause stages their articles: slug -> (unit -> (day, clause item), act law
# key, list of the changes moved to a gate). Lei 10.637 art. 68 III: arts. 34, 37 to 44, 46 and 48 from 1.1.2003 (I and II
# reach back before the publication, 31.12.2002, so those articles start on it). Lei 10.833 art. 93: I/II arts. 1 to 15, 25,
# 26, 27, 29, 30 and 34 from 1.2.2004; IV arts. 49 to 51 and 53 to 58 from the first day of the fourth month after
# publication (DOU 30.12.2003: 1.4.2004); V art. 52 from the first day of the second month after it (1.2.2004).
_L10637 = "lei-10637-de-2002"
_L10833 = "lei-10833-de-2003"


def _u(n):
    return f"art-{n:02d}"


_G10637 = {_u(n): ("2003-01-01", "III") for n in (34, 37, 38, 39, 40, 41, 42, 43, 44, 46, 48)}
_G10833 = {**{_u(n): ("2004-02-01", "I") for n in (*range(1, 16), 25)},
           **{_u(n): ("2004-02-01", "II") for n in (26, 27, 29, 30, 34)},
           **{_u(n): ("2004-04-01", "IV") for n in (49, 50, 51, 53, 54, 55, 56, 57, 58)},
           _u(52): ("2004-02-01", "V")}
# Lei 10.833 arts. 58-A to 58-V (beverage regime): Lei 11.727/2008 art. 32 added arts. 58-A to 58-U, whose effects art. 41 VII
# (as Medida Provisória 436/2008 and Lei 11.827/2008 worded it) sets from 1.1.2009; Medida Provisória 451/2008 art. 10 added
# art. 58-V to the same regime. Gate entries with a third item name the law credited when the article first shows.
_BEV = [f"art-58-{c}" for c in "abcdefghijlmnopqrstuv"]
_G10833.update({u: ("2009-01-01", "Lei 11.727 art. 41 VII", "mp-451-2008" if u == "art-58-v" else "lei-11727-2008")
                for u in _BEV})
G10637_USED: list[str] = []
G10833_USED: list[str] = []
# Lei Complementar 200/2023 art. 15: 'I - em 1º de janeiro de 2024, quanto ao art. 11' (its changes to Lei Complementar 101)
_GLC200 = {"art-11": ("2024-01-01", "I")}
GLC200_USED: list[str] = []
# Lei 14.601/2023 art. 34 I a): arts. 30 and 31 from 1.1.2024 (art. 4 § 3º and art. 33 I are single lines: SPAN_FIX)
_G14601 = {"art-30": ("2024-01-01", "I a"), "art-31": ("2024-01-01", "I a")}
G14601_USED: list[str] = []
_GATES = {_L9718: (_G9718, "lei-9718-1998", G9718_USED), _L10637: (_G10637, "lei-10637-2002", G10637_USED),
          _L10833: (_G10833, "lei-10833-2003", G10833_USED), "lei-do-regime-fiscal-sustentavel": (_GLC200, "lc-200-2023", GLC200_USED),
          "lei-do-programa-bolsa-familia": (_G14601, "lei-14601-2023", G14601_USED)}
# Lei 11.727/2008 art. 42: 'Ficam revogados: [...] IV - a partir de 1º de janeiro de 2009: a) os arts. 49, 50, 52, 55, 57 e
# 58 da Lei nº 10.833 [...]' (IV as Lei 11.827/2008 worded it; Planalto prints those articles unstruck)
_REV2009 = {"art-49", "art-50", "art-52", "art-55", "art-57", "art-58"}
REV2009_USED: list[str] = []
L10833_FIXED: list[str] = []


def build_act(paras, act_day, gate, gate_law, unit_label):
    slug = ACTS[len(B7._act_order)]["slug"] if len(B7._act_order) < len(ACTS) else "?"
    if slug in _GATES:
        tbl, law, used = _GATES[slug]
        gate, gate_law = dict(gate), dict(gate_law)
        for u, (day, *rest) in tbl.items():
            gate[u], gate_law[u] = day, (rest[1] if len(rest) > 1 else law)
        for p in paras:
            g = tbl.get(p["unit"])
            # a line that ended on or before its article's day never shows, and keeps its days
            if (g and p["start_law"] and act_day <= p["start"] < g[0] and not p.get("skip")
                    and not (p["end"] and p["end"] <= g[0])):
                used.append(f"{p['unit']} {p['label']} ({p['start_law']}, {p['start']})")
                p["start"] = g[0]
    if slug == _L10833:
        for p in paras:
            # art. 43's quoted alínea c) item 1 ('[...] fatos geradores; e') ends without a full stop, so the reader took it
            # for a heading of art. 44; it is a line of art. 43
            if p["unit"] == "art-44" and p["label"] == "rubrica" and p["text"].startswith("1. em relação aos fatos geradores"):
                p["unit"], p["label"] = "art-43", ""
                L10833_FIXED.append("art. 43 item 1 of the quoted alínea c)")
            if p["unit"] in _REV2009 and not p.get("skip") and not p["heading"] and (p["end"] is None or p["end"] > "2009-01-01"):
                p["end"], p["end_law"], p["end_how"] = "2009-01-01", "lei-11727-2008", "repealed"
                REV2009_USED.append(p["unit"])
    if slug in _FUT2027:
        fut_2027(paras, slug)
    if slug == _L9718:
        lc214_2027(paras)
        # art. 5 § 4º-A: Planalto prints Medida Provisória 1.063's § 4º-A with its incisos I and II, then Medida Provisória
        # 1.069's new § 4º-A caput; the MP 1.063 caput never took effect (skipped), so its incisos go under MP 1.069's caput
        cap = [p for p in paras if p["unit"] == "art-05" and p["label"] == "§ 4º-A" and p["start_law"] == "mp-1069-2021"]
        inc = [p for p in paras if p["unit"] == "art-05" and p["start_law"] == "mp-1063-2021"
               and p["text"].startswith(("I - nos incisos I e II do caput; ou", "II - nos incisos I e II do § 4º, observado"))]
        if cap and len(inc) == 2 and paras.index(inc[0]) < paras.index(cap[0]):
            for p in inc:
                paras.remove(p)
            at = paras.index(cap[0]) + 1
            paras[at:at] = inc
            G9718_USED.append("art-05 § 4º-A incisos I and II (Medida Provisória 1.063) placed under Medida Provisória 1.069's "
                              "caput")
    if slug == _LPNE:
        n = len(B9.REPEAL_CHECK)
        versions = _build_act17(paras, act_day, gate, gate_law, unit_label)
        # the plan's term ended (it was not repealed), and Planalto does not strike a lapsed plan: the check reads today's page
        for i in range(n, len(B9.REPEAL_CHECK)):
            x = B9.REPEAL_CHECK[i]
            x = x.replace("the last version before the repeal", "the last version before the end of its term")
            x = x.replace("the unstruck text of the pre-repeal capture of Planalto's page",
                          "the text of Planalto's page (capture of 20.10.2026)")
            x = x.replace("anexo: only in replay", "anexo: only in replay (the check sets aside a unit made only of lines with "
                          "no label and no closing punctuation, taken for the marginal heading of a revoked article; this unit "
                          "holds the Anexo's title lines 'ANEXO' and 'METAS E ESTRATÉGIAS', which the page prints)")
            B9.REPEAL_CHECK[i] = x
        return pne_term_gap(versions)
    return _build_act17(paras, act_day, gate, gate_law, unit_label)


# Lei 13.005 art. 1: ten years from publication (DOU 26.6.2014), so the plan's term ended on 25.6.2024; Lei 14.934/2024
# (DOU 26.7.2024, in force on publication) extended it to 31.12.2025. Fixed-term lapse rule: the text leaves the record on
# 26.6.2024 (the day after the term), credited to Lei 13.005 (its art. 1 set the term), and is back, word for word, on
# 26.7.2024, credited to Lei 14.934; it leaves again on 1.1.2026 (B9.REPEALS).
_PNE_LAPSE, _PNE_BACK = "2024-06-26", "2024-07-26"
PNE_GAP_USED: list[str] = []


def pne_term_gap(versions):
    before = [v for v in versions if v["from"] < _PNE_LAPSE]
    after = [v for v in versions if v["from"] >= _PNE_LAPSE]
    if not before or not after or after[0]["from"] <= _PNE_BACK or any(v["from"] < "2026-01-01" for v in after):
        raise SystemExit(f"PNE term gap: unexpected versions {[v['from'] for v in versions]}")
    last = before[-1]["units"]
    lapse = {"from": _PNE_LAPSE, "units": {}, "credits": {u: ["lei-13005-2014"] for u in sorted(last)},
             "note": "The plan's ten-year term (Lei 13.005/2014 art. 1, from its publication on 26.6.2014) ended on "
                     "25.6.2024, so its text leaves the record from the day after, until Lei 14.934/2024 extended the term."}
    back = {"from": _PNE_BACK, "units": {u: dict(x) for u, x in last.items()},
            "credits": {u: ["lei-14934-2024"] for u in sorted(last)}}
    PNE_GAP_USED.append(f"PNE: {len(last)} units removed on {_PNE_LAPSE} and back on {_PNE_BACK}, as in force on "
                        f"{before[-1]['from']}")
    return before + [lapse, back] + after


# Lei Complementar 214/2025 (IBS/CBS transition; Planalto's page of Lei 9.718 does not print these future changes, read on LC
# 214's page): art. 542 'Ficam revogados a partir de 1º de janeiro de 2027: [...] X - os arts. 2º a 8º-B da Lei nº 9.718, de
# 27 de novembro de 1998' and art. 504, the new wording of art. 9 (dropping 'da contribuição PIS/PASEP e da COFINS'); art.
# 544 III: both from 1.1.2027 (futuro branch).
_U2027 = {"art-02", "art-03", "art-04", "art-05", "art-06", "art-07", "art-08", "art-08-a", "art-08-b"}
_OLD9 = "da legislação do imposto de renda, da contribuição social sobre o lucro líquido, da contribuição PIS/PASEP e da COFINS,"
_NEW9 = "da legislação do imposto sobre a renda e da Contribuição Social sobre o Lucro Líquido,"
L2027_USED: list[str] = []


def lc214_2027(paras):
    D, L = "2027-01-01", "lc-214-2025"
    for i, p in enumerate(list(paras)):
        if p.get("skip") or p["heading"] or (p["end"] is not None and p["end"] <= D):
            continue
        if p["unit"] in _U2027:
            p["end"], p["end_law"], p["end_how"] = D, L, "repealed"
            L2027_USED.append(p["unit"])
        elif p["unit"] == "art-09" and _OLD9 in p["text"]:
            q = dict(p, text=p["text"].replace(_OLD9, _NEW9), start=D, start_law=L, end=None, end_law=None, end_how=None,
                     notes=["(Redação dada pela Lei Complementar nº 214, de 2025)"], state="plain")
            p["end"], p["end_law"], p["end_how"] = D, L, "successor"
            paras.insert(paras.index(p) + 1, q)
            L2027_USED.append("art-09")


# Lei Complementar 214/2025 changes from 1.1.2027 (art. 544 III, as Lei Complementar 227/2026 worded it) to Leis 10.637 and
# 10.833, read on LC 214's page (Planalto's pages of the two Leis do not print them): art. 542 revocations and new wordings.
# slug -> (units ended, {unit: (start of the old caput, new caput)}, the LC 214 items, for the decision).
_FUT2027 = {
    _L10637: ({"art-01", "art-02", "art-03", "art-04", "art-05", "art-05-a", "art-07", "art-08", "art-10", "art-11", "art-12",
               "art-32", "art-47"},
              {"art-35": ("Art. 35. A receita decorrente da avaliação de títulos",
                          "Art. 35. A receita decorrente da avaliação de títulos e valores mobiliários, instrumentos financeiros, "
                          "derivativos e itens objeto de hedge, registrada pelas instituições financeiras e demais entidades "
                          "autorizadas a funcionar pelo Banco Central do Brasil, instituições autorizadas a operar pela "
                          "Superintendência de Seguros Privados - Susep e sociedades autorizadas a operar em seguros ou resseguros "
                          "em decorrência da valoração a preço de mercado no que exceder ao rendimento produzido até a referida "
                          "data será computada na base de cálculo do Imposto sobre a Renda das Pessoas Jurídicas e da Contribuição "
                          "Social sobre o Lucro Líquido somente quando da alienação dos respectivos ativos.")},
              "Lei 10.637: Lei Complementar 214/2025 art. 542 ('Ficam revogados a partir de 1º de janeiro de 2027: [...] XVIII - "
              "os seguintes dispositivos da Lei nº 10.637, de 30 de dezembro de 2002: a) os arts. 1º a 5º-A; b) os arts. 7º e "
              "8º; c) os arts. 10 a 12; d) o art. 32; e e) o art. 47') and art. 507 (new caput of art. 35, which no longer "
              "names the Cofins and the contribuição para o PIS/Pasep), both in effect from 1.1.2027 (art. 544 III, as Lei "
              "Complementar 227/2026 worded it), read on LC 214's page (Planalto's page of Lei 10.637 does not print them): "
              "those articles end and art. 35 takes the new caput on 1.1.2027, on the future branch"),
    _L10833: ({*(f"art-{n:02d}" for n in range(1, 17)), "art-25", "art-91", ("art-31", "§ 1º")},
              {"art-23": ("Art. 23. A incidência da CIDE",
                          "Art. 23. A incidência da CIDE, nos termos do inciso V do art. 3º da Lei nº 10.336, de 19 de dezembro de "
                          "2001, sobre os gases liquefeitos de petróleo, classificados na subposição 2711.1 da Nomenclatura Comum "
                          "do Mercosul - NCM, não alcança os produtos classificados no código 2711.11.00."),
               "art-30": ("Art. 30. Os pagamentos efetuados pelas pessoas jurídicas",
                          "Art. 30. Os pagamentos efetuados pelas pessoas jurídicas a outras pessoas jurídicas de direito privado, "
                          "pela prestação de serviços de limpeza, conservação, manutenção, segurança, vigilância, transporte de "
                          "valores e locação de mão de obra, pela prestação de serviços de assessoria creditícia, mercadológica, "
                          "gestão de crédito, seleção e riscos, administração de contas a pagar e a receber, bem como pela "
                          "remuneração de serviços profissionais, estão sujeitos à retenção na fonte da Contribuição Social sobre "
                          "o Lucro Líquido - CSLL."),
               "art-31": ("Art. 31. O valor da CSLL",
                          "Art. 31. O valor da CSLL de que trata o art. 30 será determinado mediante a aplicação, sobre o montante "
                          "a ser pago, do percentual de 1% (um por cento)."),
               "art-32": [("Parágrafo único", "Parágrafo único. A retenção da COFINS",
                           "Parágrafo único. Será exigida a retenção da CSLL nos pagamentos:")],
               "art-33": ("Art. 33. A União",
                          "Art. 33. A União, por intermédio da Secretaria da Receita Federal, poderá celebrar convênios com os "
                          "Estados, Distrito Federal e Municípios, para estabelecer a responsabilidade pela retenção na fonte da "
                          "CSLL, mediante a aplicação da alíquota prevista no art. 31, nos pagamentos efetuados por órgãos, "
                          "autarquias e fundações dessas administrações públicas às pessoas jurídicas de direito privado, pelo "
                          "fornecimento de bens ou pela prestação de serviços em geral."),
               "art-34": ("Art. 34. Ficam obrigadas",
                          "Art. 34. Ficam obrigadas a efetuar as retenções na fonte do imposto sobre a renda e da CSLL, a que se "
                          "refere o art. 64 da Lei nº 9.430, de 27 de dezembro de 1996, as seguintes entidades da administração "
                          "pública federal:"),
               "art-67": ("Art. 67. Na impossibilidade",
                          "Art. 67. Na impossibilidade de identificação da mercadoria importada, em razão de seu extravio ou "
                          "consumo, e de descrição genérica nos documentos comerciais e de transporte disponíveis, será aplicada, "
                          "para fins de determinação dos impostos incidentes na importação, alíquota única de 70% (setenta por "
                          "cento) relativa ao Imposto de Importação e ao Imposto sobre Produtos Industrializados - IPI.")},
              "Lei 10.833: Lei Complementar 214/2025 art. 542 ('Ficam revogados a partir de 1º de janeiro de 2027: [...] XXI - "
              "os seguintes dispositivos da Lei nº 10.833, de 29 de dezembro de 2003: a) os arts. 1º a 16; b) o art. 25; c) o § "
              "1º do art. 31; d) os arts. 49 e 50; e) o art. 52; f) o art. 55; g) os arts. 57 e 58; e h) o art. 91'; arts. 49, 50, "
              "52, 55, 57 and 58 had already ended on 1.1.2009, under Lei 11.727/2008 art. 42 IV a)) and art. "
              "509 (new capita of arts. 23, 30, 31, 33, 34 and 67, a new caput of art. 32's parágrafo único, and art. 67 § 3º "
              "with incisos I and II; none of them names the Cofins or the contribuição para o PIS/Pasep any more), all in "
              "effect from 1.1.2027 (art. 544 III, as Lei Complementar 227/2026 worded it), read on LC 214's page (Planalto's "
              "page of Lei 10.833 does not print them): on 1.1.2027, on the future branch",
              {"art-67": ("§ 2º", [("§ 3º", "§ 3º A alíquota de que trata o caput será distribuída nos seguintes percentuais:"),
                                    ("I -", "I - 35% (trinta e cinco por cento), a título de alíquota do Imposto de Importação; e"),
                                    ("II -", "II - 35% (trinta e cinco por cento), a título de alíquota do IPI.")])}),
}
FUT2027_USED: dict[str, list[str]] = {}


def _is_caput(p):
    return p["label"] == "caput" or p["label"].startswith("Art.") or p["text"].startswith("Art. ")


def fut_2027(paras, slug):
    # entry: (ends, rewrites, decision[, inserts]). ends: unit keys (whole article) or (unit, label) (that dispositivo and
    # the incisos/alíneas under it). rewrites: {unit: (start of the old caput, new caput)} or {unit: [(label or 'caput',
    # start of the old line, new line), ...]}. inserts: {unit: (label of the line to insert after, [(label, text), ...])}.
    D, L = "2027-01-01", "lc-214-2025"
    entry = _FUT2027[slug]
    ends, rew, _ = entry[:3]
    ins = entry[3] if len(entry) > 3 else {}
    used = FUT2027_USED.setdefault(slug, [])
    sub_end = None   # unit whose incisos/alíneas follow an ended dispositivo
    for p in list(paras):
        if p.get("skip") or p["heading"] or (p["end"] is not None and p["end"] <= D):
            continue
        if sub_end and p["unit"] == sub_end and p["label"] and not p["label"].startswith(("§", "Parágrafo", "Art.")):
            p["end"], p["end_law"], p["end_how"] = D, L, "repealed"
            continue
        sub_end = None
        if p["unit"] in ends:
            p["end"], p["end_law"], p["end_how"] = D, L, "repealed"
            used.append(p["unit"])
            continue
        if (p["unit"], p["label"]) in ends:
            p["end"], p["end_law"], p["end_how"] = D, L, "repealed"
            used.append(f"{p['unit']} {p['label']}")
            sub_end = p["unit"]
            continue
        r = rew.get(p["unit"])
        if r is None:
            continue
        rows = [("caput",) + tuple(r)] if isinstance(r, tuple) else r
        for lab, prefix, new in rows:
            if (_is_caput(p) if lab == "caput" else p["label"] == lab) and p["text"].startswith(prefix):
                q = dict(p, text=new, start=D, start_law=L, end=None, end_law=None, end_how=None,
                         notes=["(Redação dada pela Lei Complementar nº 214, de 2025)"], state="plain")
                p["end"], p["end_law"], p["end_how"] = D, L, "successor"
                paras.insert(paras.index(p) + 1, q)
                used.append(p["unit"] if lab == "caput" else f"{p['unit']} {lab}")
                break
    for unit, (after, rows) in ins.items():
        cur = [p for p in paras if p["unit"] == unit and p["label"] == after and not p.get("skip") and p["end"] is None]
        if len(cur) != 1:
            continue
        at = paras.index(cur[0]) + 1
        for lab, text in rows:
            paras.insert(at, dict(cur[0], label=lab, text=text, start=D, start_law=L, end=None, end_law=None, end_how=None,
                                  notes=["(Incluído pela Lei Complementar nº 214, de 2025)"], state="plain"))
            at += 1
        used.append(f"{unit} {rows[0][0]} (new)")


# parts zk/zl: hand days, set only when the acts run
if any(a["slug"] in (_L10637, _L10833) for a in ACTS):
    P.MP_LAPSE["mp-1159-2023"] = (
        "2023-06-02", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 40, de 2023 (DOU 16.6.2023): 'teve seu "
                      "prazo de vigência encerrado no dia 1º de junho de 2023'; the wordings it gave end on 2.6.2023")
    P.VIGENCIA_FIXED["lei-14596-2023"] = (
        "2024-01-01", "art. 47: 'Esta Lei entra em vigor em 1º de janeiro de 2024, exceto o art. 45, que entra em vigor na data de "
                      "sua publicação' (DOU 15.6.2023): its art. 46 (revocations; VII: Lei 10.637 art. 45; VIII: Lei 10.833 art. "
                      "45) from 1.1.2024")
    P.VIGENCIA_FIXED["lei-13043-2014"] = (
        "2015-01-01", "art. 113: 'Esta Lei entra em vigor na data de sua publicação, exceto: [...] II - os arts. 1º a 15, 30 a 32, "
                      "97, 106 e os artigos da Seção XXI do Capítulo I, que entram em vigor a partir de 1º de janeiro de 2015' (DOU "
                      "14.11.2014): its arts. 31 (Lei 10.637 art. 8) and 32 (Lei 10.833 art. 10) fall under II")
    P.MP_PENDING["mp-382-2007"] = (
        "Medida Provisória nº 382, de 24.7.2007 (DOU 25.7.2007, in force on publication), revoked by Medida Provisória nº 392, "
        "de 18.9.2007 (DOU 19.9.2007, art. 1: 'Fica revogada a Medida Provisória nº 382, de 24 de julho de 2007'), whose "
        "conversion, Lei 11.604/2007 (DOU 6.12.2007), repeats the revocation; the wordings Medida Provisória 382 gave end on "
        "19.9.2007")
    P.NOTE_FIX["(Incluído pela Medida Provisória nº 382, 2007)"] = (
        "(Incluído pela Medida Provisória nº 382, de 2007)", "the note reads 'Medida Provisória nº 382, 2007' (no 'de'); its link "
                                                             "is to Medida Provisória 382/2007")
    P.NOTE_FIX["(Revogado pela Medida Provisória nº 392)"] = (
        "(Revogado pela Medida Provisória nº 392, de 2007)", "the note gives no year; its link is to Medida Provisória 392/2007, "
                                                             "which revoked Medida Provisória 382/2007")
    for _how in ("Redação dada", "Incluído"):
        P.NOTE_FIX[f"({_how} pela Medida Provisória nº 11.488, de 2007)"] = (
            f"({_how} pela Medida Provisória nº 447, de 2008)",
            f"Lei 10.637 art. 10 ('{_how}'): the note names 'Medida Provisória nº 11.488, de 2007' (no such MP; Lei 11.488/2007 is a "
            "Lei); its link is to Medida Provisória 447/2008, whose art. 2 gave art. 10 these words (read on its page)")

_W413 = ("Lei 10.637 arts. 2 and 3: Medida Provisória 413/2008 (DOU 3.1.2008) art. 14 changed them (art. 2 XI and XII, art. 3 I "
         "a)); its art. 18 II gave its arts. 3, 7 and 9 to 17 effect from the first day of the fourth month after publication, "
         "and Medida Provisória 425/2008, before that day came, moved art. 14 to III ('a partir do 1º dia do mês subseqüente ao "
         "da publicação do ato da Secretaria da Receita Federal do Brasil'); Lei 11.727/2008, its conversion, set the effect of "
         "its own art. 14 from 1.10.2008: the MP's wordings are not shown as in effect (judgement call, as for Lei 9.718)")
_W11727 = ("Lei 10.637 arts. 1, 2, 3 and 8: Lei 11.727/2008 (DOU 24.6.2008) art. 41: 'produzindo efeitos em relação: [...] IV - aos "
           "arts. 7º, 9º a 12 e 14 a 16, a partir do primeiro dia do quarto mês subseqüente ao da publicação desta Lei; [...] VII - "
           "aos arts. 32 a 39, a partir de 1º de janeiro de 2009' (IV and VII as Medida Provisória 436/2008 and Lei 11.827/2008, "
           "its conversion, worded them before either day came) and art. 42 III c) (revocation of art. 1 § 3º IV and art. 8 VII "
           "a) 'a partir do primeiro dia do quarto mês subseqüente ao da publicação desta Lei'): its art. 14 (art. 2 § 1º-A, art. "
           "3 I a)) and the revocations from 1.10.2008, its art. 35 (art. 2 VIII and IX) from 1.1.2009, the wordings they replaced "
           "until then (set by hand: Leis 11.787/2008 and Medida Provisória 451/2008 changed arts. 3 and 2 in between, so "
           "effects_fix cannot move them); its art. 42 II a) (revocation of art. 37 from 1.5.2008) reaches back before the "
           "publication, which is kept")
_W451 = ("Lei 10.637 art. 3 § 15: Medida Provisória 451/2008 (DOU 16.12.2008) art. 22: 'produzindo efeitos: [...] II - a partir "
         "do primeiro dia do quarto mês subseqüente ao da publicação desta Medida Provisória, em relação ao disposto: a) no art. "
         "8º, relativamente ao § 15 do art. 3º da Lei nº 10.637': the § 15 it added from 1.4.2009 (set by hand: Lei 11.898/2009 "
         "changed art. 3 in between, so effects_fix cannot move it); its § 16 on publication")
_E1010 = {"end": "2008-10-01", "end_law": "lei-11727-2008"}
_S1010 = {"start": "2008-10-01", "start_law": "lei-11727-2008"}
_E0101 = {"end": "2009-01-01", "end_law": "lei-11727-2008"}
_S0101 = {"start": "2009-01-01", "start_law": "lei-11727-2008"}
B8.SPAN_FIX += [
    ((_L10637, "art-03", "a)", "a) no inciso III do § 3º do art. 1º; e", 0), {"skip": True, "end_how": "never-in-effect"}, _W413),
    ((_L10637, "art-02", "XI -", "XI no caput do art. 5º da Lei nº 9.718", 0), {"skip": True, "end_how": "never-in-effect"}, _W413),
    ((_L10637, "art-02", "XII -", "XII - no § 2º do art. 5º da Lei nº 9.718", 0), {"skip": True, "end_how": "never-in-effect"},
     _W413),
    ((_L10637, "art-03", "a)", "a) nos incisos III e IV do § 3º do art. 1º desta Lei; e", 0), dict(_E1010, end_how="successor"),
     _W11727),
    ((_L10637, "art-03", "a)", "a) no inciso III do § 3º do art. 1º desta Lei; e.", 0), dict(_S1010), _W11727),
    ((_L10637, "art-02", "§ 1º-A", "§ 1º-A. Excetua-se do disposto no caput deste artigo a receita bruta auferida pelos produtores",
      0), dict(_S1010), _W11727),
    ((_L10637, "art-02", "VIII -", "VIII - no art. 49 da Lei nº 10.833, de 29 de dezembro de 2003, e alterações posteriores, no caso de venda de água", 0), dict(_E0101, end_how="successor"), _W11727),
    ((_L10637, "art-02", "IX -", "IX - no art. 52 da Lei nº 10.833", 0), dict(_E0101, end_how="successor"), _W11727),
    ((_L10637, "art-02", "VIII -", "VIII - no art. 58-I da Lei nº 10.833", 0), dict(_S0101), _W11727),
    ((_L10637, "art-02", "IX -", "IX - no inciso II do art. 58-M da Lei nº 10.833", 0), dict(_S0101), _W11727),
    ((_L10637, "art-01", "IV -", "IV - de venda de álcool para fins carburantes", 0), dict(_E1010, end_how="note"), _W11727),
    ((_L10637, "art-08", "a)", "a) referidas no inciso IV do § 3º do art. 1º", 0), dict(_E1010, end_how="note"), _W11727),
    ((_L10637, "art-03", "§ 15", "§ 15. Sem prejuízo da vedação", 0), {"start": "2009-04-01", "start_law": "mp-451-2008"}, _W451),
]
_X10637 = ("the consolidated page prints a revoked or vetoed dispositivo as a placeholder line ('VII - a IX - (Revogado ...)', "
           "'§§ 10 e 11. (Revogados ...)', 'Art. 38. (Revogado ...)', 'Arts. 42 e 43. (Revogados ...)'), which the history "
           "leaves out")
_N10637 = "the annotated page prints 'nº' as 'n' with a raised 'o' ('no' in the text), the consolidated page as 'nº'"
B.EXPLAINED[_L10637] = {"art-01": _N10637, "art-02": _X10637, "art-03": _X10637 + "; " + _N10637, "art-38": _X10637,
                        "art-41": _X10637, "art-52": _N10637}
B13.OPEN_ITEMS[_L10637] = (
    "Lei 10.637 (open items): Medida Provisória 66/2002 (DOU 30.8.2002), which the Lei converted, is not part of the history; "
    "the record starts with the Lei (31.12.2002), so the effects art. 68 I and II give from 1.10.2002 and 1.12.2002 start on "
    "that day. Effects that reach back before an amending act's publication are dated by the publication (Lei 10.684/2003 "
    "art. 29 II, Medida Provisória 447/2008 art. 8, Lei 11.933/2009 art. 11 I, Lei 11.945/2009 art. 33 I c) and IV b), Lei "
    "11.727/2008 art. 42 II a)). Medida Provisória 413/2008's wordings are not shown as in effect (its effect tied to an act "
    "of the Receita Federal by Medida Provisória 425/2008; Lei 11.727 fixed 1.10.2008). Medida Provisória 451/2008: Planalto's "
    "page of the MP prints the items of art. 22 I struck; they are read as published (as for Lei 9.718). Lei 10.833/2003 art. "
    "94 VI ('a partir da data de início dos efeitos desta Lei') is read as 1.2.2004, the day its arts. 1 to 15 take effect. "
    "Lei 12.973/2014 art. 119 § 1º (its rules from 1.1.2014 for taxpayers who opted) is not modelled. 'Vide' pointers "
    "(Decretos 5.057/2004 and 6.842/2009, Medida Provisória 413/2008) are not modelled")
if any(a["slug"] == _L10637 for a in ACTS):
    P.VIGENCIA_PROVISION[("lei-12973-2014", _L10637, "art-55")] = (
        "2014-05-14", "Lei 12.973/2014 art. 119: 'Esta Lei entra em vigor em 1º de janeiro de 2015, exceto os arts. 3º, 72 a 75 e "
                      "93 a 119, que entram em vigor na data de sua publicação' (DOU 14.5.2014); its art. 118 ('Revoga-se o art. "
                      "55 da Lei nº 10.637 [...], a partir da data de publicação desta Lei') falls under the exception")

# part zl: Lei 10.833/2003. Hand days set only when the act runs (each text names the article that touches Lei 10.833).
if any(a["slug"] == _L10833 for a in ACTS):
    P.VIGENCIA_FIXED["mp-472-2009"] = (
        "2009-12-16", "art. 60: 'Esta Medida Provisória entra em vigor: I - na data de sua publicação, produzindo efeitos: "
                      "[...] d) a partir da data de sua publicação, em relação aos demais dispositivos' (DOU 16.12.2009): its "
                      "art. 27 (Lei 10.833 art. 18) falls under I d)")
    P.VIGENCIA_FIXED["lei-12844-2013"] = (
        "2013-07-19", "art. 49: 'Esta Lei entra em vigor: [...] V - na data de sua publicação para os demais dispositivos' "
                      "(DOU 19.7.2013, edição extra): its art. 23 (Lei 10.833 art. 62) falls under V")
    for _how in ("Redação dada", "Incluído"):
        P.NOTE_FIX[f"({_how} pela Lei nº 11.933, de 2007)"] = (
            f"({_how} pela Lei nº 11.933, de 2009)",
            f"Lei 10.833 art. 11 ('{_how}'): the note names 'Lei nº 11.933, de 2007'; its link is to Lei 11.933/2009 (L11933.htm#art3), "
            "whose art. 3 gave art. 11 these words (read on its page)")
    P.NOTE_FIX["(Incluído pela Lei nº 12.767, de 20212)"] = (
        "(Incluído pela Lei nº 12.767, de 2012)",
        "Lei 10.833 art. 61 VIII and IX: the note reads 'Lei nº 12.767, de 20212'; its link is to Lei 12.767/2012 (L12767.htm#art28), "
        "whose art. 28 added them (read on its page)")
    B6.CONTEXT.append({
        "when": lambda: bool(EFX_FIXED),
        "pins": ["ctx:camara-lei-10833-2003-original"],
        "what": "the original publication of Lei 10.833/2003 (DOU 30.12.2003, edição extra-A), to settle which of Planalto's two "
                "printings ('efeito' or 'efeitos') is the published word"})
B8.SPAN_FIX += [
    ((_L10833, "art-03", "§ 22", "§ 22.", 0), {"skip": True, "end_how": "pointer"},
     "Lei 10.833 art. 3 § 22: both Planalto pages print a line holding only '§ 22.' and the note '(Vide Medida Provisória nº 413, "
     "de 2008)'; it is a pointer, not a wording, and is left out"),
    ((_L10833, "art-30", "§ 4º", "§ 4º", 0), {"skip": True, "end_how": "pointer"},
     "Lei 10.833 art. 30 § 4º: Planalto prints a line holding only '§ 4º' and the note '(Vide Medida Provisória nº 232, 2004)'; "
     "it is a pointer, not a wording, and is left out"),
    ((_L10833, "art-69", "§ 3º", "§ 3º", 0), {"skip": True, "end_how": "pointer"},
     "Lei 10.833 art. 69 § 3º: Planalto prints a struck line holding only '§ 3º' and the note '(Vide Medida Provisória nº 320, "
     "2006)' above the § 3º Lei 13.043/2014 added; it is a pointer, not a wording, and is left out"),
]
# Lei 11.727/2008 (DOU 24.6.2008) art. 41: 'produzindo efeitos em relação: [...] IV - aos arts. 7º, 9º a 12 e 14 a 16, a partir
# do primeiro dia do quarto mês subseqüente ao da publicação desta Lei; [...] VII - aos arts. 32 a 39, a partir de 1º de janeiro
# de 2009' (IV and VII as Lei 11.827/2008 worded them) and art. 42 III d) (revocation of art. 1 § 3º IV and art. 10 VII a) 'a
# partir do primeiro dia do quarto mês subseqüente ao da publicação desta Lei'): its art. 15 (art. 2 § 1º-A, art. 3 I a) and §
# 18) and those revocations from 1.10.2008, its art. 36 (art. 2 § 1º VIII and IX, art. 3 § 1º and § 16, arts. 51 and 53) from
# 1.1.2009; its art. 19 (art. 34) on publication. Lei 11.787/2008 and Medida Provisória 451/2008 changed arts. 2 and 3 in
# between, so effects_fix cannot move these: set by hand.
_W11727Z = ("Lei 10.833: Lei 11.727/2008 (DOU 24.6.2008) art. 41 ('produzindo efeitos em relação: [...] IV - aos arts. 7º, 9º a "
            "12 e 14 a 16, a partir do primeiro dia do quarto mês subseqüente ao da publicação desta Lei; [...] VII - aos arts. 32 a "
            "39, a partir de 1º de janeiro de 2009', IV and VII as Medida Provisória 436/2008 and Lei 11.827/2008 worded them) and "
            "art. 42 III d) (revocation of art. 1 § 3º IV and art. 10 VII a) 'a partir do primeiro dia do quarto mês subseqüente ao "
            "da publicação desta Lei'): its art. 15 (art. 2 § 1º-A, art. 3 I a) and § 18) and those revocations from 1.10.2008; its "
            "art. 36 (art. 2 § 1º VIII and IX, art. 3 § 1º and § 16, arts. 51 and 53) from 1.1.2009; the wordings they replaced "
            "until then (set by hand: Lei 11.787/2008 and Medida Provisória 451/2008 changed arts. 2 and 3 in between, so "
            "effects_fix cannot move them); its art. 19 (art. 34) on publication. Art. 10 VII a) ('referidas no inciso IV do § 3º "
            "do art. 1º'), which Planalto prints unstruck with only a 'Vide Lei nº 11.727, de 2008' pointer, ends on 1.10.2008: the "
            "law's text governs")
_W451Z = ("Lei 10.833 art. 3 § 23: Medida Provisória 451/2008 (DOU 16.12.2008) art. 22: 'produzindo efeitos: [...] II - a partir do "
          "primeiro dia do quarto mês subseqüente ao da publicação desta Medida Provisória, em relação ao disposto: [...] b) no art. "
          "9º, relativamente ao § 23 do art. 3º da Lei nº 10.833' (printed struck on the MP's page, read as published): the § 23 it "
          "added from 1.4.2009 (set by hand: Lei 11.898/2009 changed art. 3 in between, so effects_fix cannot move it)")
_W58M = ("Lei 10.833 art. 58-M: the caput, added by Lei 11.727/2008 art. 32 with the article, carries only Lei 13.097's revocation "
         "note and starts with Lei 11.727; incisos I and II: Lei 11.727's wording until Medida Provisória 436/2008 (27.6.2008), "
         "the MP's until Lei 11.827/2008 (21.11.2008), and Lei 11.827's, which repeats the MP's words, until Lei 13.097 revoked "
         "the article (the reader had taken Lei 11.827's lines for duplicates of the MP's)")
_W58Z = ("Lei 10.833 art. 58 caput incisos I and II: Planalto prints them struck with no note (the consolidated page leaves them "
         "out); Lei 11.051/2004 art. 25 rewrote only § 1º of art. 58 (the caput and its incisos are dotted lines in its text), so "
         "they stand with the article until Lei 11.727/2008 art. 42 IV a) revoked it (1.1.2009)")
_E1010Z = {"end": "2008-10-01", "end_law": "lei-11727-2008", "end_how": "successor"}
_S1010Z = {"start": "2008-10-01", "start_law": "lei-11727-2008"}
_E0101Z = {"end": "2009-01-01", "end_law": "lei-11727-2008", "end_how": "successor"}
_S0101Z = {"start": "2009-01-01", "start_law": "lei-11727-2008"}
_R0101Z = {"end": "2009-01-01", "end_law": "lei-11727-2008", "end_how": "repealed"}
_I13097 = {"skip": False, "end": "2015-01-20", "end_law": "lei-13097-2015", "end_how": "parent"}
B8.SPAN_FIX += [((_L10833, u, lab, pre, n), dict(f), w) for u, lab, pre, n, f, w in (
    ("art-02", "VIII -", "VIII - no art. 49 desta Lei", 0, _E0101Z, _W11727Z),
    ("art-02", "VIII -", "VIII - no art. 58-I desta Lei", 0, _S0101Z, _W11727Z),
    ("art-02", "IX -", "IX - no art. 52 desta Lei", 0, _E0101Z, _W11727Z),
    ("art-02", "IX -", "IX - no inciso II do art. 58-M desta Lei", 0, _S0101Z, _W11727Z),
    ("art-02", "§ 1º-A", "§ 1º-A. Excetua-se do disposto no caput deste artigo a receita bruta auferida pelos produtores", 0,
     _S1010Z, _W11727Z),
    ("art-03", "a)", "a) nos incisos III e IV do § 3º do art. 1º desta Lei", 0, _E1010Z, _W11727Z),
    ("art-03", "a)", "a) no inciso III do § 3º do art. 1º desta Lei", 0, _S1010Z, _W11727Z),
    ("art-03", "§ 1º", "§ 1º Observado o disposto no § 15 deste artigo e no § 1º do art. 52", 0, _E0101Z, _W11727Z),
    ("art-03", "§ 1º", "§ 1º Observado o disposto no § 15 deste artigo, o crédito", 1, _S0101Z, _W11727Z),
    ("art-03", "§ 16", "§ 16. Opcionalmente", 0, _E0101Z, _W11727Z),
    ("art-03", "§ 16", "§ 16. Opcionalmente", 1, _S0101Z, _W11727Z),
    ("art-03", "I -", "I - no prazo de 12 (doze) meses, à razão de 1/12", 0, _S0101Z, _W11727Z),
    ("art-03", "II -", "II - na hipótese de opção pelo regime especial instituído pelo art. 58-J", 0, _S0101Z, _W11727Z),
    ("art-03", "§ 18", "§ 18. O crédito, na hipótese de devolução", 0, _E1010Z, _W11727Z),
    ("art-03", "§ 18", "§ 18. No caso de devolução de vendas", 0, _S1010Z, _W11727Z),
    ("art-10", "a)", "a) referidas no inciso IV do § 3º do art. 1º", 0, dict(_E1010Z, end_how="repealed"), _W11727Z),
    ("art-03", "§ 23", "§ 23. Sem prejuízo da vedação", 0, {"start": "2009-04-01", "start_law": "mp-451-2008"}, _W451Z),
    ("art-58-m", "Art. 58-M", "Art. 58-M. Para os efeitos do regime especial", 0,
     {"start": "2008-06-24", "start_law": "lei-11727-2008"}, _W58M),
    ("art-58-m", "I -", "I - o Poder Executivo estabelecerá as alíquotas do IPI", 0,
     {"end": "2008-06-27", "end_law": "mp-436-2008", "end_how": "successor"}, _W58M),
    ("art-58-m", "II -", "II - as alíquotas da Contribuição para o PIS/Pasep e da Cofins serão de 2,5%", 0,
     {"end": "2008-06-27", "end_law": "mp-436-2008", "end_how": "successor"}, _W58M),
    ("art-58-m", "I -", "I - o Poder Executivo estabelecerá as alíquotas do IPI", 2, _I13097, _W58M),
    ("art-58-m", "II -", "II - as alíquotas da Contribuição para o PIS/Pasep e da Cofins serão de 2,5%", 2, _I13097, _W58M),
    ("art-58", "I -", "I - contribuição para o PIS/PASEP, do saldo dos créditos", 0, dict(_R0101Z, skip=False), _W58Z),
    ("art-58", "II -", "II - COFINS, do valor equivalente a 3%", 0, _R0101Z, _W58Z),
)]
if any(a["slug"] == _L10833 for a in ACTS):
    _W1727P = ("Lei 11.727/2008 (DOU 24.6.2008): art. 42 III d) revokes art. 1 § 3º IV of Lei 10.833 'a partir do primeiro dia do "
               "quarto mês subseqüente ao da publicação desta Lei' (1.10.2008); art. 36 (arts. 51 and 53) takes effect from "
               "1.1.2009 (art. 41 VII, as Lei 11.827/2008 worded it)")
    P.VIGENCIA_PROVISION.update({("lei-11727-2008", _L10833, "art-01"): ("2008-10-01", _W1727P),
                                 ("lei-11727-2008", _L10833, "art-51"): ("2009-01-01", _W1727P),
                                 ("lei-11727-2008", _L10833, "art-53"): ("2009-01-01", _W1727P)})
    _W13043P = ("Lei 13.043/2014 art. 113 ('Esta Lei entra em vigor na data de sua publicação, exceto: [...] II - os arts. 1º a 15, "
                "30 a 32, 97, 106 e os artigos da Seção XXI do Capítulo I, que entram em vigor a partir de 1º de janeiro de 2015; "
                "[...] IV - [...] b) o art. 98 e os artigos das Seções XVI, XVII, XIX e XX do Capítulo I', DOU 14.11.2014): its "
                "art. 56 (Lei 10.833 arts. 67 and 69, Seção XI) and art. 114 III (art. 76 alíneas) fall under the general rule, in "
                "force on publication; its art. 32 (art. 10 XXX) under II (1.1.2015); its art. 79 (art. 10 XX, Seção XX) under IV "
                "b) (1.3.2015, moved by effects_fix)")
    P.VIGENCIA_PROVISION.update({("lei-13043-2014", _L10833, u): ("2014-11-14", _W13043P) for u in ("art-67", "art-69", "art-76")})
B13.OPEN_ITEMS[_L10833] = (
    "Lei 10.833 (open items): Medida Provisória 135/2003 (DOU 31.10.2003), which the Lei converted, is not part of the history; "
    "the record starts with the Lei (30.12.2003). The Anexo Único (the list of goods, by TIPI code, named in arts. 50 and 58, "
    "revoked by Lei 10.925/2004) is not modelled. Effects that reach back before an amending act's publication are dated by "
    "the publication (Lei 11.196/2005 art. 132 II b), Lei 11.933/2009 art. 11 I, Lei 11.945/2009 art. 33 I d) and IV c), Lei "
    "12.249/2010 art. 139 I d)). "
    "Lei 11.051/2004 art. 24 gives art. 3 § 20 effect from 1.4.2005 only 'no que se refere ao inciso II do § 19': its words "
    "apply to § 19 I from publication, so the paragraph is dated by the publication (30.12.2004). Medida Provisória 451/2008: "
    "Planalto's page of the MP prints the items of art. 22 I and II b) struck; they are read as published (as for Leis 9.718 "
    "and 10.637). Lei 12.995/2014 art. 27 I e) revokes art. 58-T § 2º 'a partir da entrada em vigor do art. 13', whose effects "
    "its art. 26 sets from the first day of the following year: read as 1.1.2015 (judgement call). Art. 1 § 3º IX: Planalto "
    "notes the revocation by Medida Provisória 1.185/2023 and 'Revogado Lei nº 14.789, de 2023' (its conversion), both from "
    "1.1.2024; the MP is credited. Lei Complementar 214/2025's changes from 1.1.2027 are on the future branch. 'Vide' "
    "pointers (Medidas Provisórias 164/2004, 232/2004, 320/2006, 413/2008 and 497/2010, Decretos 5.062/2004 and 5.162/2004, "
    "Lei 10.685/2004) are not modelled")
_N10833 = "the annotated page prints 'nº' as 'n' with a raised 'o' ('no' in the text), the consolidated page as 'nº'"
_REV10833 = ("Planalto prints the article unstruck with only a 'Vide Lei nº 11.727, de 2008' pointer, though Lei 11.727/2008 art. 42 "
             "IV a) (as Lei 11.827/2008 worded it) revoked it from 1.1.2009; the law's text governs and the article ends then")
B.EXPLAINED[_L10833] = {
    "art-02": _N10833 + "; the consolidated page also prints a stray line 'IX - n' (the start of a revoked inciso IX)",
    "art-03": "the annotated page ends § 15 with a full stop ('desta Lei.'), the consolidated page without",
    "art-18": _N10833, "art-62": _N10833, "art-70": _N10833, "art-77": _DOTTED,
    "art-10": ("Planalto prints inciso VII a) ('referidas no inciso IV do § 3º do art. 1º') unstruck with only a 'Vide Lei nº "
               "11.727, de 2008' pointer, though Lei 11.727/2008 art. 42 III d) revoked it from 1.10.2008; the law's text governs "
               "and the alínea ends then"),
    **{u: _REV10833 for u in ("art-49", "art-50", "art-52", "art-55", "art-57", "art-58")},
    **{u: ("item 1 of art. 43's quoted alínea c) ends without a full stop; read from the consolidated page it is taken for a "
           "heading of art. 44, while the history keeps it in art. 43, where both pages print it") for u in ("art-43", "art-44")},
}

# part zm: Lei Complementar 141/2012 (aplicação mínima em saúde), Lei 14.113/2020 (Fundeb). Hand days set only when the act runs.
_LC141, _LFUNDEB = "lei-do-financiamento-da-saude", "lei-do-fundeb"
if any(a["slug"] == _LFUNDEB for a in ACTS):
    P.MP_LAPSE["mp-1074-2021"] = (
        "2022-04-22", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 35, de 2022: 'teve seu prazo de vigência "
                      "encerrado no dia 21 de abril de 2022'; the wording it gave Lei 14.113 art. 41 § 3º I (DOU 12.11.2021) had "
                      "already been replaced by Lei 14.276/2021 (DOU 28.12.2021, in force on publication), so nothing returns")
    P.VIGENCIA_PROVISION[("lei-14276-2021", _LFUNDEB, "art-21")] = (
        "2022-03-25", "Lei 14.276/2021 art. 1, in the part that added art. 21 § 9º, was vetoed; Congress overrode the veto and the "
                      "President promulgated it on 24.3.2022 (DOU 25.3.2022, printed on Lei 14.276's page as 'Promulgação partes "
                      "vetadas'). A promulgated part is law only from its publication: § 9º takes effect on 25.3.2022 (Planalto "
                      "prints no '(VETADO)' line for it, so it is absent before)")
    EXTRA.append("Lei 14.113 art. 21 § 9º: " + P.VIGENCIA_PROVISION[("lei-14276-2021", _LFUNDEB, "art-21")][1]
                 + "; it is credited to Lei 14.276/2021 on 25.3.2022.")
    B5.PROVISION_REPORTED.add(("lei-14276-2021", _LFUNDEB))
# part zn: Lei 12.414/2011 (cadastro positivo), Lei Complementar 200/2023 (regime fiscal sustentável). Hand days set only when the
# act runs.
_LCADPOS, _LC200 = "lei-do-cadastro-positivo", "lei-do-regime-fiscal-sustentavel"
if any(a["slug"] == _LCADPOS for a in ACTS):
    P.VIGENCIA_FIXED["lc-166-2019"] = (
        "2019-07-09", "art. 7: 'Esta Lei Complementar entra em vigor: I - na data de sua publicação, quanto ao disposto: a) no "
                      "caput e no § 6º do art. 12 da Lei nº 12.414, de 9 de junho de 2011, com redação dada pelo art. 2º desta Lei "
                      "Complementar; e b) nos arts. 3º e 5º; II - após decorridos 91 (noventa e um) dias de sua publicação oficial, "
                      "quanto aos demais dispositivos' (DOU 9.4.2019): its changes to Lei 12.414 fall under II (91 days counted from "
                      "the day of publication, in force on 9.7.2019), except art. 12 caput and § 6º (I a), in force on 9.4.2019")
if any(a["slug"] == _LC200 for a in ACTS):
    EXTRA.append("Lei Complementar 200/2023 art. 11 (its changes to Lei Complementar 101/2000): the new Lei Complementar 101 art. 4 "
                 "§ 7º was vetoed ('§ 7º (VETADO).'); Congress overrode the veto and the President promulgated it on 22.12.2023 (DOU "
                 "22.12.2023, edição extra; printed on Lei Complementar 200's page). Both fall before art. 11's own day (1.1.2024, "
                 "art. 15 I), so art. 11 first shows on 1.1.2024 with the promulgated § 7º and the '(VETADO)' line never shows.")
B.EXPLAINED[_LC200] = {"art-11": _DOTTED}
B13.OPEN_ITEMS[_LCADPOS] = (
    "Lei 12.414 (open items): the Lei converted Medida Provisória 518/2010, which is not part of the history (the record starts "
    "with the Lei, 10.6.2011); 'Vide' pointers and the regulations ('Regulamento' links) strike no words and are not modelled")
B13.OPEN_ITEMS[_LC200] = (
    "Lei Complementar 200 (open items): 'Vide ADI' pointers (ADIs 7.064, 7.641, 7.922 and 8.010) strike no words and are not "
    "modelled; the transitional rules for the financial years 2023 and 2024 (arts. 12 to 14) set no term of their own and stay in "
    "the text as Planalto prints them; its changes to Lei Complementar 101/2000 (art. 11) are words of this act, and Lei "
    "Complementar 101's own history is a separate act of the record")
_W12414 = ("Lei 12.414 art. 12: Lei Complementar 166/2019 art. 7 I a) puts its new caput and § 6º in force on publication (DOU "
           "9.4.2019); its other changes to the Lei take effect 91 days after publication (art. 7 II, 9.7.2019)")
_S0409 = {"start": "2019-04-09", "start_law": "lc-166-2019", "by_provision": True}
B8.SPAN_FIX += [
    ((_LCADPOS, "art-12", "Art. 12", "Art. 12. Quando solicitado pelo cliente", 0),
     {"end": "2019-04-09", "end_law": "lc-166-2019", "end_how": "successor"}, _W12414),
    ((_LCADPOS, "art-12", "Art. 12", "Art. 12. As instituições autorizadas", 0), dict(_S0409), _W12414),
    ((_LCADPOS, "art-12", "§ 6º", "§ 6º O órgão administrativo competente", 0), dict(_S0409), _W12414),
]
# part zo: Leis 11.442/2007 (transporte rodoviário de cargas), 10.209/2001 (vale-pedágio), 9.611/1998 (transporte multimodal)
_LTRC, _LVP, _LTM = "lei-do-transporte-rodoviario-de-cargas", "lei-do-vale-pedagio", "lei-do-transporte-multimodal"
if any(a["slug"] == _LVP for a in ACTS):
    P.VIGENCIA_PROVISION[("lei-14229-2021", _LVP, "art-08")] = (
        "2021-10-22", "Lei 14.229/2021 art. 7 I: in force on publication 'quanto aos arts. 1º, 3º, 4º e 5º' (DOU 22.10.2021); its art. "
                      "4 added Lei 10.209 art. 8 parágrafo único (the 180 days of art. 7 III are for its other provisions)")
    EXTRA.append("Lei 10.209 art. 8 parágrafo único: " + P.VIGENCIA_PROVISION[("lei-14229-2021", _LVP, "art-08")][1]
                 + "; it starts on 22.10.2021.")
    B5.PROVISION_REPORTED.add(("lei-14229-2021", _LVP))
_W5TRC = ("Lei 11.442 art. 5: Lei 14.206/2021 (DOU 28.9.2021) art. 18 numbered the parágrafo único as § 1º and, in the same "
          "article, gave § 1º the wording '§ 1º (Revogado).'; Planalto prints the renumbered wording struck with a 'Renumerado' "
          "note, but it never stood as § 1º: the parágrafo único ends on 28.9.2021 and '§ 1º (Revogado).' starts then (Lei "
          "14.440/2022 later put the same words back as § 3º)")
_W4VP = ("Lei 10.209 art. 4: Lei 10.561/2002 (DOU 14.11.2002, in force on publication) art. 4 'Fica revogado o art. 4º da Lei nº "
         "10.209', the whole article; Planalto strikes only the caput and prints the parágrafo único unstruck. The law's text "
         "governs: the parágrafo único ends on 14.11.2002 with the caput")
_W7VP = ("Lei 10.209 art. 7: Planalto prints the 2001 wording ('as atividades inerentes ao Ministério dos Transportes', with the "
         "typing slip 'exerçer') struck, then the note '(Redação dada pela Lei nº 10.561, de 13.11.2002)' outside the strike, then "
         "the new wording ('inerentes à ANTT') with the same note; the note belongs to the new wording (Lei 10.561 made the same "
         "change in art. 6), so the struck line is the article as enacted, from 24.3.2001 to 14.11.2002, in Planalto's words")
B8.SPAN_FIX += [
    ((_LTRC, "art-05", "§ 1º", "§ 1º Compete à Justiça Comum", 0), {"skip": True, "end_how": "renumbered-and-revoked"}, _W5TRC),
    ((_LVP, "art-04", "Parágrafo único", "Parágrafo único. A dedução de que trata", 0),
     {"end": "2002-11-14", "end_law": "lei-10561-2002", "end_how": "repealed"}, _W4VP),
    ((_LVP, "art-07", "Art. 7º", "Art. 7º Caso o Ministério do Trabalho e Emprego venha a exerçer", 0),
     {"start": "2001-03-24", "start_law": None, "notes": [], "skip": False, "end": "2002-11-14", "end_law": "lei-10561-2002",
      "end_how": "successor"}, _W7VP),
]
B.EXPLAINED[_LVP] = {"art-04": "Planalto prints art. 4's parágrafo único unstruck, though Lei 10.561/2002 art. 4 revoked the whole "
                                "article; the law's text governs and it ends on 14.11.2002"}
B13.OPEN_ITEMS[_LTRC] = (
    "Lei 11.442 (open items): Lei 12.249/2010 art. 128 (art. 5º-A) has effects from 16.12.2009 (its art. 139 I d), the day of "
    "Medida Provisória 472/2009, which it converted); the page credits the Lei, so art. 5º-A is dated by the Lei's publication "
    "(14.6.2010). Lei 13.103/2015 has no in-force clause: in force 45 days after publication (LINDB art. 1; DOU 3.3.2015, "
    "17.4.2015). Lei 15.485/2026 converted Medida Provisória 1.343/2026; the page credits no wording to the MP. Medidas "
    "Provisórias 1.051/2021 and 1.153/2022 were converted (Leis 14.206/2021 and 14.599/2023). 'Vide' pointers (Lei 13.103/2015, "
    "ADC 48) strike no words and are not modelled")
B13.OPEN_ITEMS[_LVP] = (
    "Lei 10.209 (open items): the Lei converted Medida Provisória 2.107-12/2001 (its art. 10 validates acts under 2.107-11); "
    "the earlier editions of the MP chain are not part of the history (the record starts with the Lei, 24.3.2001). Planalto "
    "prints art. 7 in Lei 10.561/2002's wording twice, once struck with a typing slip ('exerçer') and once unstruck: the "
    "unstruck copy is the wording. 'Vide ADIN 6031' strikes no words and is not modelled")
B13.OPEN_ITEMS[_LTM] = (
    "Lei 9.611 (open items): no amendment notes on the page; the regulation ('Regulamento' link) is not modelled")
# part zp: Leis 11.284/2006 (gestão de florestas públicas), 14.119/2021 (pagamento por serviços ambientais)
_LGFP, _LPSA = "lei-de-gestao-de-florestas-publicas", "lei-do-pagamento-por-servicos-ambientais"
if any(a["slug"] == _LGFP for a in ACTS):
    P.NOTE_FIX["(Redação dada pela Lei nº 11.516, 2007)"] = (
        "(Redação dada pela Lei nº 11.516, de 2007)",
        "Lei 11.284 art. 39: the note reads 'Lei nº 11.516, 2007' (the 'de' missing; its link goes to Lei 11.516/2007's page)")
_Q14119 = ("the promulgated text keeps the quotation marks of the promulgation's own wording on Planalto's page; the history drops "
           "them (they are not words of the article)")
B.EXPLAINED[_LPSA] = {"art-23": _DOTTED, "art-06": _Q14119, "art-15": _Q14119, "art-16": _Q14119}
B13.OPEN_ITEMS[_LGFP] = (
    "Lei 11.284 (open items): Medida Provisória 1.151/2022 was converted (Lei 14.590/2023); 'Vide' pointers (Medida Provisória "
    "366/2007, Decreto 10.347/2020, ADI 7.394) strike no words and are not modelled; the regulations are not modelled")
B13.OPEN_ITEMS[_LPSA] = (
    "Lei 14.119 (open items): the Lei was rectified in the DOU of 15.1.2021; the record follows Planalto's text. The regulation "
    "is not modelled")
# part zq: Leis 6.091/1974 (transporte de eleitores), 10.216/2001 (saúde mental), 9.434/1997 (transplantes)
B13.OPEN_ITEMS["lei-do-transporte-de-eleitores"] = (
    "Lei 6.091 (open items): arts. 17 to 25 end on 18.6.1986, revoked by Lei 7.493/1986 art. 26 (a law for the 1986 elections "
    "whose revocation is not limited to them); Lei 6.961/1981, which had given art. 17 its 1981 wording, was revoked by the same "
    "article (no words of Lei 6.091 change by that)")
B13.OPEN_ITEMS["lei-da-saude-mental"] = (
    "Lei 10.216 (open items): no amendment notes on the page; regulations are not modelled")
B.EXPLAINED["lei-dos-transplantes"] = {
    "art-10": ("the compiled page still prints the 1997 parágrafo único after §§ 1º and 2º; the annotated page strikes it: Lei "
               "10.211/2001 (as Medida Provisória 2.083-32 before it) replaced it with § 1º, which has the same words")}
B13.OPEN_ITEMS["lei-dos-transplantes"] = (
    "Lei 9.434 (open items): the Medida Provisória chain that Lei 10.211/2001 converted began in 1998; Planalto's page names "
    "only its last edition, 2.083-32 (DOU 23.2.2001), so the earlier editions' wordings are not part of the history and the "
    "changes start with 2.083-32. Regulations ('Regulamento' links) are not modelled")
B13.OPEN_ITEMS[_LC141] = (
    "Lei Complementar 141 (open items): Lei Complementar 227/2026's new wordings of arts. 6 and 7 and art. 3 X (the IBS share) "
    "take effect on its publication (its art. 182 III; DOU 14.1.2026, republished 15.1.2026 and rectified 23.1.2026: dated by the "
    "first publication, with the words Planalto prints), though the IBS is collected in full only from later years; "
    "'Vide' pointers (Decreto 7.827/2012, the regulation; ADI 5.897 on art. 11) strike no words and are not modelled")
B13.OPEN_ITEMS[_LFUNDEB] = (
    "Lei 14.113 (open items): the transitional rules of arts. 43 to 43-B name the financial years they apply to (2021 to 2024); "
    "they set no term of their own and stay in the text as Planalto prints them. Medida Provisória 1.074/2021's wording of art. "
    "41 § 3º I stood from 12.11.2021 until Lei 14.276/2021 replaced it on 28.12.2021 (the MP lapsed on 21.4.2022). The "
    "regulation ('Regulamento' link) is not modelled")

# part zr: Leis 6.996/1982 (processamento eletrônico eleitoral), 9.870/1999 (mensalidades escolares)
_LPEE, _LMESC = "lei-do-processamento-eletronico-eleitoral", "lei-das-mensalidades-escolares"
if any(a["slug"] == _LPEE for a in ACTS):
    B8.LAW_FIELD_FIX["lei-7663-1988"] = (
        {"enacted": "1988-05-27"},
        "Lei 7.663/1988: Planalto's page heads it 'DE 27 DE JUNHO DE 1988', but it closes 'Brasília, 27 de maio de 1988' and was "
        "published in the DOU of 31.5.1988: enacted 27.5.1988 (its in-force day, the day of publication, is unchanged)")
    B8.LAW_FIELD_FIX["lei-7444-1985"] = (
        {"title": "Dispõe sobre a implantarão do processamento eletrônico de dados no alistamento eleitoral e a revisão do "
                  "eleitorado e dá outras providências"},
        "Lei 7.444/1985: its ementa ends without a full stop, so the title reader found none; the title is the ementa as printed")
_W16PEE = ("Lei 6.996 art. 16: Lei 9.096/1995 (DOU 20.9.1995, in force on publication) art. 63 revokes 'o art. 16 da Lei nº 6.996, "
           "de 7 de junho de 1982', the whole article; Planalto strikes only its caput and prints §§ 1º and 2º unstruck. The law's "
           "text governs: §§ 1º and 2º end on 20.9.1995 with the caput")
B8.SPAN_FIX += [
    ((_LPEE, "art-16", "§ 1º", "§ 1º - Deferida a filiação", 0),
     {"end": "1995-09-20", "end_law": "lei-9096-1995", "end_how": "repealed"}, _W16PEE),
    ((_LPEE, "art-16", "§ 2º", "§ 2º - Estando em vigor a inscrição", 0),
     {"end": "1995-09-20", "end_law": "lei-9096-1995", "end_how": "repealed"}, _W16PEE),
]
B.EXPLAINED[_LPEE] = {"art-16": "Planalto prints art. 16 §§ 1º and 2º unstruck, though Lei 9.096/1995 art. 63 revoked the whole "
                                "article; the law's text governs and they end on 20.9.1995"}
B13.OPEN_ITEMS[_LPEE] = (
    "Lei 6.996 (open items): Lei 7.444/1985 art. 12 revokes art. 2 § 2º, citing 'Lei nº 6.996, de 7 de junho de 1932' (a slip "
    "for 1982); Lei 7.663/1988 art. 5 revokes art. 9 (caput, parágrafo único and its incisos), which art. 17 "
    "still names ('o parágrafo único do art. 9º'): art. 17 keeps its words as Planalto prints them")
if any(a["slug"] == _LMESC for a in ACTS):
    P.MP_PENDING["mp-2173-2001"] = (
        "Medida Provisória nº 2.173-24, de 23.8.2001 (DOU 24.8.2001, art. 4: in force on publication), kept in force by Emenda "
        "Constitucional 32/2001, art. 2; it added Lei 9.870 art. 1 §§ 3º and 4º and art. 6 § 1º and renumbered the paragraphs "
        "after them. Planalto's notes name this edition only, so the changes are dated by its publication; earlier editions of "
        "the chain are not modelled")
B13.OPEN_ITEMS[_LMESC] = (
    "Lei 9.870 (open items): the Lei converted Medida Provisória 1.890-67/1999 (its art. 10 keeps the acts done under 1.890-66 "
    "and the earlier editions in effect); the MP chain before the Lei is not part of the history (the record starts with the "
    "Lei, 24.11.1999). The changes Medida Provisória 1.930/1999 and its editions made before 2.173-24 are not modelled: "
    "Planalto prints them only as 'Vide' pointers. Regulations ('Regulamento' links) are not modelled")

# part zs: Leis 13.005/2014 (Plano Nacional de Educação), 12.379/2011 (Sistema Nacional de Viação)
_LPNE, _LSNV = "lei-do-plano-nacional-de-educacao", "lei-do-sistema-nacional-de-viacao"
_N14934 = ("Extended to 31 December 2025 the term of the Plano Nacional de Educação that Lei 13.005/2014 approved for ten years "
           "from its publication in the DOU of 26.6.2014, a term that had ended on 25.6.2024. It changed none of the plan's words: "
           "the plan's text, which left the record on 26.6.2024, is back from 26.7.2024, the day this law was published, and "
           "leaves it again on 1.1.2026, the day after the extended term.")
if any(a["slug"] == _LPNE for a in ACTS):
    B8.EXTRA_LAWS["lei-14934-2024"] = {
        "label": "Lei nº 14.934, de 2024", "kind": "law",
        "title": "Prorroga, até 31 de dezembro de 2025, a vigência do Plano Nacional de Educação, aprovado por meio da Lei nº "
                 "13.005, de 25 de junho de 2014.",
        "enacted": "2024-07-25", "published": "2024-07-26",
        "url": PL + "_ato2023-2026/2024/lei/l14934.htm", "temporary_until": None, "restores": None, "note": _N14934}
    B9.REPEALS[_LPNE] = (
        "2026-01-01", "lei-14934-2024",
        "Lei 13.005/2014 (Plano Nacional de Educação) art. 1 approves the plan 'com vigência por 10 (dez) anos, a contar da "
        "publicação desta Lei' (DOU 26.6.2014, so to 25.6.2024); Lei 14.934/2024 art. 1 (DOU 26.7.2024, in force on publication) "
        "'Fica prorrogada, até 31 de dezembro de 2025, a vigência do Plano Nacional de Educação'. The plan is an act with a "
        "fixed term, so a version on the day after the term ends removes every provision: on 26.6.2024, credited to Lei "
        "13.005/2014, whose art. 1 set the ten-year term (the extension came a month after the term had ended, and it does not "
        "say it reaches back). On 26.7.2024 every provision is back, word for word as in force on 25.6.2024, credited to Lei "
        "14.934/2024, which changed none of the plan's words (its note says so); the act's last version, on 1.1.2026 (the day "
        "after the extended term), removes every provision again, credited to Lei 14.934/2024, which set that day. Planalto's "
        "page (capture of 20.10.2026) names no later law that extends "
        "the term again, and Planalto does not strike a lapsed plan, so the replay check compares the last version before the "
        "end of the term with the page's text")
# part zw: Leis 10.973/2004 (inovação), 9.456/1997 (proteção de cultivares)
_LINOV, _LPC = "lei-de-inovacao", "lei-de-protecao-de-cultivares"
if any(a["slug"] == _LINOV for a in ACTS):
    P.NOTE_FIX["(Redação pela Lei nº 13.243, de 2016)"] = (
        "(Redação dada pela Lei nº 13.243, de 2016)",
        "Lei 10.973: 40 notes read '(Redação pela Lei nº 13.243, de 2016)', the word 'dada' missing (the other notes of the page "
        "and Lei 13.243's art. 2 give these wordings): read as 'Redação dada pela'")
_W9456 = ("Lei 9.456 art. 10 V and art. 14-A: added by Lei 13.606/2018 art. 27 (DOU 10.1.2018), which the President vetoed whole "
          "('Art. 27. (VETADO).'); Congress overrode the veto and the article was promulgated on 17.4.2018 (DOU 18.4.2018, printed "
          "on Lei 13.606's page, '(Promulgação)'), so both start on 18.4.2018, credited to Lei 13.606, as its art. 20-D of Lei "
          "10.522 (part q); Planalto's page of Lei 9.456 prints no '(VETADO)' line for them, so they are absent before")
_P9456 = {"start": "2018-04-18", "start_law": "lei-13606-2018", "promulgated": True}
B8.SPAN_FIX += [
    ((_LPC, "art-10", "V -", "V - multiplica, distribui, troca ou comercializa sementes", 0), dict(_P9456), _W9456),
    ((_LPC, "art-14-a", "Art. 14-A", "Art. 14-A. Ficam isentos de pagamento", 0), dict(_P9456), _W9456),
]
B.EXPLAINED[_LINOV] = {"art-24": _DOTTED}
B13.OPEN_ITEMS[_LINOV] = (
    "Lei 10.973 (open items): Medida Provisória 495/2010 (converted by Lei 12.349/2010) and 718/2016 (converted by Lei "
    "13.322/2016) are dated by their publication and their conversions; the page was rectified on 16.5.2005 (DOU), the record "
    "follows Planalto's text; 'Vide' pointers (Medida Provisória 497/2010, Decreto 9.841/2019) strike no words and are not "
    "modelled; the regulations are not modelled")
B13.OPEN_ITEMS[_LPC] = (
    "Lei 9.456 (open items): Planalto's page dates the DOU '8.4.1997' (a slip: the Lei is of 25.4.1997; LexML's record of the "
    "original publication gives 28.4.1997, used here); the rectifications of 26.8.1997 and 25.9.1997 are followed as Planalto "
    "prints the text; the regulations are not modelled")
# part zv: Leis 7.853/1989 (pessoas com deficiência, Corde), 9.807/1999 (proteção a testemunhas), 10.861/2004 (SINAES)
_L7853, _LPT, _LSINAES = "lei-da-pessoa-com-deficiencia-de-1989", "lei-de-protecao-a-testemunhas", "lei-do-sinaes"
if any(a["slug"] == _L7853 for a in ACTS):
    P.MP_PENDING["mp-437-2008"] = (
        "Medida Provisória nº 437, de 29.7.2008 (DOU 30.7.2008, in force on publication): revoked by Medida Provisória nº 439, "
        "de 29.8.2008 (DOU 29.8.2008, edição extra, art. 4), converted into Lei 11.805/2008 (art. 4); its wording of Lei 7.853 "
        "art. 10 caput ends on 29.8.2008 and Lei 8.028/1990's wording is back from that day")
    B8.EXTRA_LAWS["mp-439-2008"] = {
        "label": "Medida Provisória nº 439, de 2008", "kind": "law",
        "title": "Constitui fonte de recursos adicional para ampliação de limites operacionais do Banco Nacional de "
                 "Desenvolvimento Econômico e Social - BNDES.",
        "enacted": "2008-08-29", "published": "2008-08-29",
        "url": PL + "_Ato2007-2010/2008/Mpv/439.htm", "temporary_until": None, "restores": None, "note": None}
_W7853 = ("Lei 7.853 art. 10 caput: Medida Provisória 437/2008 (DOU 30.7.2008) gave it a new wording and was revoked by Medida "
          "Provisória 439/2008 (art. 4; DOU 29.8.2008, edição extra), so its wording ends on 29.8.2008 and Lei 8.028/1990's wording, "
          "which Planalto prints again below the MP's line, stands from that day, credited to Medida Provisória 439, until Lei "
          "11.958/2009 (DOU 29.6.2009) gave the caput the words MP 437 had used")
B8.SPAN_FIX += [
    ((_L7853, "art-10", "Art. 10", "Art. 10. A coordenação superior dos assuntos, ações governamentais e medidas referentes a pessoas "
                                   "portadoras de deficiência caberá", 0),
     {"end": "2008-08-29", "end_law": "mp-439-2008", "end_how": "revoked-mp"}, _W7853),
    ((_L7853, "art-10", "Art. 10", "Art. 10. A coordenação superior dos assuntos, ações governamentais e medidas, referentes a pessoas", 1),
     {"start": "2008-08-29", "start_law": "mp-439-2008"}, _W7853),
]
if any(a["slug"] == _LSINAES for a in ACTS):
    P.MP_PENDING["mp-1370-2026"] = (
        "Medida Provisória nº 1.370, de 19.6.2026 (DOU 19.6.2026, edição extra), in force on publication; on the day of the last "
        "copy of its page read here (22.10.2026) it was neither converted nor lapsed. Its term (CF art. 62 §§ 3 and 4: 60 days, "
        "extendable once by 60, the count suspended in the July recess) ends about 30.10.2026, so its fate is not yet in the record "
        "and its addition of Lei 10.861 art. 5 § 12 stands open")
B13.OPEN_ITEMS[_L7853] = (
    "Lei 7.853 (open items): 'Vide' pointers (Medida Provisória 150/1990, which Lei 8.028/1990 converted; Medida Provisória "
    "1.799-6/1999, an earlier edition of the chain that Medida Provisória 2.216-37/2001 ended) strike no words and are not "
    "modelled; the regulations are not modelled")
B13.OPEN_ITEMS[_LPT] = (
    "Lei 9.807 (open items): art. 17 rewrites Lei 6.015 art. 58 parágrafo único (quoted, kept as the article's text); the "
    "regulations are not modelled")
B13.OPEN_ITEMS[_LSINAES] = (
    "Lei 10.861 (open items): the Lei converted Medida Provisória 147/2003; the MP's own text before the Lei is not part of the "
    "history (the record starts with the Lei, 15.4.2004). Medida Provisória 1.370/2026 (art. 5 § 12) was pending on the last "
    "copy of Planalto's pages read here (22.10.2026): its fate is to be read once a later copy is available")
# part zu: Leis Complementares 159/2017 (Regime de Recuperação Fiscal) and 178/2021 (Plano de Promoção do Equilíbrio Fiscal)
_LC159, _LC178 = "lei-do-regime-de-recuperacao-fiscal", "lei-do-plano-de-equilibrio-fiscal"
if any(a["slug"] == _LC159 for a in ACTS):
    P.NOTE_FIX["(Incluído pela Lei Complementar nº 189, de 2021)"] = (
        "(Incluído pela Lei Complementar nº 189, de 2022)",
        "Lei Complementar 159 art. 2: the note reads 'Lei Complementar nº 189, de 2021'; its link goes to Lcp189.htm#art2, Lei "
        "Complementar 189 of 4 January 2022 (DOU 5.1.2022), which the other notes of the same article name 'de 2022'")
B.EXPLAINED[_LC178] = {"art-12": _DOTTED, "art-13": _DOTTED, "art-16": _DOTTED}
B13.OPEN_ITEMS[_LC159] = (
    "Lei Complementar 159 (open items): the Regime's own periods (each State's plan, its extensions) are acts of execution, not "
    "terms of the text; the regulations ('Regulamento' link) are not modelled")
B13.OPEN_ITEMS[_LC178] = (
    "Lei Complementar 178 (open items): its art. 16's changes of Lei Complementar 101 arts. 51 and 42 'a partir de 2022' and "
    "'a partir de 2023' (art. 32 I and II) concern that law's text, not this act's; the dates in its articles (deadlines for "
    "contract amendments and lawsuits) are not terms of the text; Lei Complementar 212/2025's promulgated vetoed parts (DOU 4.12.2025) do not "
    "touch this act; the regulations are not modelled")
# part zt: Lei 6.437/1977 (infrações sanitárias)
_LIS = "lei-das-infracoes-sanitarias"
if any(a["slug"] == _LIS for a in ACTS):
    P.MP_PENDING["mp-2190-2001"] = (
        "Medida Provisória nº 2.190-34, de 23.8.2001 (DOU 24.8.2001, art. 14: in force on publication), kept in force by Emenda "
        "Constitucional 32/2001, art. 2; its art. 12 gave Lei 6.437 art. 2 incisos XII and XIII and §§ 1º to 3º and the art. 10 "
        "wordings Planalto notes with this edition (incisos XXXII to XLI added). Planalto's notes name this edition only, so the "
        "changes are dated by its publication; earlier editions of the chain are not modelled")
    P.PUBLISHED_FIXED["lei-9695-1998"] = (
        "1998-08-21", "Lei 9.695/1998: its page closes 'Este texto não substitui o publicado pelo D.O.U. de 21.8.1998' ('pelo', a "
                      "form the publication reader does not take); in force on publication (art. 3)")
B13.OPEN_ITEMS[_LIS] = (
    "Lei 6.437 (open items): Medida Provisória 116/1989's wording of art. 5 (DOU 30.11.1989) was kept word for word by its "
    "conversion, Lei 7.967/1989 (DOU 26.12.1989), so that law changes no words; Lei 9.005/1995 converted Medida Provisória "
    "834/1995 (its art. 4 keeps the acts done under it), whose change of art. 10 XXX is dated by the Lei, the only act Planalto "
    "names; the regulations are not modelled")
B13.OPEN_ITEMS[_LPNE] = (
    "Lei 13.005 (open items): 'Vide ADI 5668' (art. 2 III) and 'Vide Decreto 11.713/2023' strike no words and are not modelled; the "
    "plans of the States and Municipalities (art. 8) are not part of the history")
B13.OPEN_ITEMS[_LSNV] = (
    "Lei 12.379 (open items): Anexos I to VII were vetoed (Planalto prints '(VETADO)' for each, after the signature) and are not "
    "part of the history; the relações descritivas that Lei 14.273/2021's art. 41-A leaves to acts of the Executive are not "
    "modelled; the vetoed art. 45 stays as Planalto prints it")
_W1065S = ("Lei 12.379: Medida Provisória 1.065/2021 (DOU 30.8.2021) lapsed at the close of 6.2.2022 (Ato Declaratório 5/2022), and "
           "Lei 14.273/2021 (DOU 23.12.2021, edição extra; no vigência clause, so in force 45 days later, on 6.2.2022) art. 76 gave "
           "new wordings to arts. 2, 20 IV and parágrafo único, 21 IV to VI, 22 (caput, § 1º caput, I caput, c) to f), II, § 2º), "
           "23-A, 24 and 41-A, and its art. 78 III revoked arts. 10, 15, 17, 23, 26, 27, 28, 35 and 43. Where Lei 14.273 replaced "
           "or revoked a line MP 1.065 had changed (art. 10 I, art. 24 caput), the MP's wording ends on 6.2.2022 and the wording "
           "the MP had replaced is not back (Planalto prints it a second time, struck, below the MP's line: that copy is left out, "
           "as are the second copies of the 2011 art. 22 caput, c), d) and § 2º). Where Lei 14.273 left the line alone (art. 22 § "
           "1º I a) and b), kept by its dotted line), the MP's wording ends with its lapse, on 7.2.2022, and the 2011 wording is "
           "back from that day, as Planalto prints it (as for Lei 10.233 in part w)")
_E14273S = {"end": "2022-02-06", "end_law": "lei-14273-2021", "end_how": "successor-before-lapse"}
_E14273R = {"end": "2022-02-06", "end_law": "lei-14273-2021", "end_how": "repealed"}
_ELAPSES = {"end": "2022-02-07", "end_law": "mp-1065-2021-fim", "end_how": "lapse"}
_SKIPS = {"skip": True, "end_how": "never-restored"}
B8.SPAN_FIX += [((_LSNV, u, lab, pre, n), dict(f), _W1065S) for u, lab, pre, n, f in (
    ("art-10", "I -", "I - aprovação de lei específica, no caso do transporte rodoviário e aquaviário", 0, _E14273R),
    ("art-10", "I -", "I - aprovação de lei específica, no caso do transporte terrestre e aquaviário", 1, _SKIPS),
    ("art-22", "Art. 22", "Art. 22. As ferrovias integrantes do Subsistema Ferroviário Federal são designadas pelo símbolo \"EF\" ou",
     1, _SKIPS),
    ("art-22", "a)", "a) 1 (um) para as Ferrovias Longitudinais;", 0, _ELAPSES),
    ("art-22", "b)", "b) 2 (dois) para as Ferrovias Transversais;", 0, _ELAPSES),
    ("art-22", "c)", "c) 3 (três) para as diagonais; e", 1, _SKIPS),
    ("art-22", "d)", "d) 4 (quatro) para as ligações;", 1, _SKIPS),
    ("art-22", "§ 2º", "§ 2º O símbolo \"AF\"", 1, _SKIPS),
    ("art-24", "Art. 24", "Art. 24. Fica a União autorizada a desativar ou erradicar", 1, _E14273S),
    ("art-24", "Art. 24", "Art. 24. Fica a União autorizada a desativar ou erradicar", 2, _SKIPS))]

# part zx: Lei 7.802/1989 (agrotóxicos; repealed as a whole on 28.12.2023, read from a capture of 18.12.2023)
_LAGRO = "lei-dos-agrotoxicos-de-1989"
if any(a["slug"] == _LAGRO for a in ACTS):
    B8.EXTRA_LAWS["lei-14785-2023"] = {
        "label": "Lei nº 14.785, de 2023", "kind": "law", "title": _T14785, "enacted": "2023-12-27", "published": "2023-12-28",
        "url": PL + PAGES["l14785"], "temporary_until": None, "restores": None, "note": None}
    B9.REPEALS[_LAGRO] = (
        "2023-12-28", "lei-14785-2023",
        "Lei 7.802/1989 was repealed as a whole by Lei 14.785/2023 art. 65 I ('Revogam-se: I - as Leis nºs 7.802, de 11 de julho "
        "de 1989, e 9.974, de 6 de junho de 2000'; not vetoed), in force on publication (art. 66; DOU 28.12.2023), so its last "
        "version, on 28.12.2023, removes every provision, credited to Lei 14.785/2023 (its art. 64 validates the acts done under "
        "Lei 7.802). After the repeal Planalto strikes the whole page, so the page is read from a capture of 18.12.2023, before "
        "the repeal, and the history up to 27.12.2023 is checked against that capture's text")
# part zy: Leis 9.612/1998 (radiodifusão comunitária), 11.947/2009 (alimentação escolar)
_LRC, _LPNAE = "lei-da-radiodifusao-comunitaria", "lei-da-alimentacao-escolar"
if any(a["slug"] in (_LRC, _LPNAE) for a in ACTS):
    P.MP_PENDING["mp-2143-2001"] = (
        "Medida Provisória nº 2.143-32, de 2.5.2001 (DOU 3.5.2001, in force on publication), an edition of the chain that "
        "Medida Provisória nº 2.216-37, de 31.8.2001 (same ementa, the numbering continued) closed; its wording of Lei 9.612 "
        "art. 2 is dated by its publication and ends with 2.216-37's wording (DOU 1.9.2001), kept in force by Emenda "
        "Constitucional 32/2001, art. 2. Planalto's notes name these two editions only; the editions between are not modelled")
    P.VIGENCIA_FIXED["lei-15255-2025"] = (
        "2026-01-01", "art. 3: 'Esta Lei entra em vigor no primeiro exercício financeiro subsequente ao de sua publicação "
                      "oficial' (DOU 11.11.2025): the financial year 2026, from 1.1.2026")
_W14734 = ("Lei 11.947 art. 17 XI (with alíneas a) to i)) and art. 20 IV: added by Lei 14.734/2023 (DOU 23.11.2023, edição extra; "
           "no vigência clause, so in force 45 days later, on 7.1.2024) but vetoed ('XI - (VETADO).', 'IV - (VETADO).'); "
           "Congress overrode the veto and the parts were promulgated on 21.5.2024 (DOU 22.5.2024, printed on Lei 14.734's "
           "page, '(Promulgação partes vetadas)'). The '(VETADO)' lines stand from 7.1.2024 to 22.5.2024 (Planalto prints "
           "them struck with no note, read at first as the 2009 text), the promulgated words from 22.5.2024, credited to Lei "
           "14.734, as for Lei 9.427 art. 26 § 12 in part z")
_V14734 = {"start": "2024-01-07", "start_law": "lei-14734-2023", "end": "2024-05-22", "end_law": "lei-14734-2023",
           "end_how": "promulgation"}
_P14734 = {"start": "2024-05-22", "start_law": "lei-14734-2023", "promulgated": True}
B8.SPAN_FIX += [
    ((_LPNAE, "art-17", "XI -", "XI - (VETADO", 0), dict(_V14734), _W14734),
    ((_LPNAE, "art-17", "XI -", "XI - complementar, por meio de lei local", 0), dict(_P14734), _W14734),
    *[((_LPNAE, "art-17", f"{x})", f"{x}) {w}", 0), dict(_P14734), _W14734) for x, w in (
        ("a", "objetivos;"), ("b", "beneficiários;"), ("c", "forma de gestão;"), ("d", "ações de educação alimentar"),
        ("e", "procedimentos de aquisição"), ("f", "estrutura e funcionamento do CAE"), ("g", "procedimentos de execução"),
        ("h", "prestação de contas"), ("i", "monitoramento, avaliação"))],
    ((_LPNAE, "art-20", "IV -", "IV - (VETADO", 0), dict(_V14734), _W14734),
    ((_LPNAE, "art-20", "IV -", "IV - não implementarem o disposto no inciso XI", 0), dict(_P14734), _W14734),
]
B13.OPEN_ITEMS[_LRC] = (
    "Lei 9.612 (open items): Planalto prints 'Vide ADIN Nº 2566' beside art. 4 § 1º and leaves its words unstruck, so the "
    "ruling is not modelled; the regulations ('Regulamento' link) strike no words and are not modelled")
B13.OPEN_ITEMS[_LPNAE] = (
    "Lei 11.947 (open items): the text before 17.6.2009 (Medida Provisória 455/2008, of which this Lei is the conversion) is "
    "not part of the history; Lei 14.734/2023 art. 2 (promulgated 22.5.2024: the FNDE may apply art. 20 IV only three years "
    "after 23.11.2023) is that law's own rule and changes no words of this Lei; 'Vide' pointers (Leis 14.734/2023 and "
    "15.255/2025) strike no words and are not modelled")
B8.SPAN_FIX += [
    ((_LAGRO, "art-07", "d)", "d) declarações de propriedade relativas à inocuidade", 0), {"keep": True},
     "Lei 7.802 art. 7 § 2º II d) ('declarações de propriedade relativas à inocuidade [...]') is printed once, unstruck and "
     "with no note, in § 2º; it is the act's own wording, in force until the repeal (the twin-wording rule, which would take "
     "it for a copy of the caput's inciso II d), struck and rewritten by Lei 9.974/2000, does not apply)")]
B13.OPEN_ITEMS[_LAGRO] = (
    "Lei 7.802 (open items): the regulations ('Regulamento' links, Decreto 4.074/2002) strike no words and are not modelled")

# part zz: Lei 14.785/2023 (agrotóxicos). Vetoed parts promulgated in two acts printed on its page.
_LAG23 = "lei-dos-agrotoxicos"
_W14785 = ("Lei 14.785/2023 (DOU 28.12.2023, in force on publication) was sanctioned with parts vetoed; Congress overrode the vetoes "
           "and the President promulgated them in two acts printed on Planalto's page ('(Promulgação partes vetadas)'): on "
           "21.5.2024 (DOU 22.5.2024) art. 4 § 5º V, art. 27 I to III, art. 28 (caput and parágrafo único), art. 29 § 2º and art. "
           "30 § 2º; on 1.7.2025 (DOU 2.7.2025) arts. 59 (caput, §§ 1º and 2º), 60 and 61 and art. 62 I (the Taxa de Avaliação e "
           "de Registro). Each '(VETADO)' line stands from 28.12.2023 to its promulgation (Planalto prints it struck with no "
           "note); the promulgated words are law from the DOU of the promulgation, credited to Lei 14.785, as for Lei 9.427 art. "
           "26 § 12 in part z")
_PR1, _PR2 = "2024-05-22", "2025-07-02"


def _v14785(day):
    return {"skip": False, "end": day, "end_law": "lei-14785-2023", "end_how": "promulgation"}


def _p14785(day):
    return {"start": day, "start_law": "lei-14785-2023", "promulgated": True}


B8.SPAN_FIX += [((_LAG23, u, lab, pre, 0), f, _W14785) for u, lab, pre, f in (
    ("art-04", "V -", "V - (VETADO", _v14785(_PR1)), ("art-04", "V -", "V - coordenar as reanálises", _p14785(_PR1)),
    ("art-27", "I -", "I - (VETADO", _v14785(_PR1)), ("art-27", "I -", "I - processo produtivo", _p14785(_PR1)),
    ("art-27", "II -", "II - (VETADO", _v14785(_PR1)), ("art-27", "II -", "II - especificações do produto", _p14785(_PR1)),
    ("art-27", "III -", "III - (VETADO", _v14785(_PR1)), ("art-27", "III -", "III - alteração de matérias-primas", _p14785(_PR1)),
    ("art-28", "Art. 28", "Art. 28. (VETADO", _v14785(_PR1)), ("art-28", "Art. 28", "Art. 28. O órgão federal", _p14785(_PR1)),
    ("art-28", "Parágrafo único", "Parágrafo único. O órgão federal", _p14785(_PR1)),
    ("art-29", "§ 2º", "§ 2º (VETADO", _v14785(_PR1)), ("art-29", "§ 2º", "§ 2º Os pedidos de registro", _p14785(_PR1)),
    ("art-30", "§ 2º", "§ 2º (VETADO", _v14785(_PR1)), ("art-30", "§ 2º", "§ 2º Os pedidos de registro", _p14785(_PR1)),
    ("art-59", "Art. 59", "Art. 59. (VETADO", _v14785(_PR2)), ("art-59", "Art. 59", "Art. 59. É criada a Taxa", _p14785(_PR2)),
    ("art-59", "§ 1º", "§ 1º São sujeitos passivos", _p14785(_PR2)), ("art-59", "§ 2º", "§ 2º A taxa a que se refere", _p14785(_PR2)),
    ("art-60", "Art. 60", "Art. 60. (VETADO", _v14785(_PR2)), ("art-60", "Art. 60", "Art. 60. O produto da arrecadação", _p14785(_PR2)),
    ("art-61", "Art. 61", "Art. 61. (VETADO", _v14785(_PR2)), ("art-61", "Art. 61", "Art. 61. Os recursos arrecadados", _p14785(_PR2)),
    ("art-62", "I -", "I - (VETADO", _v14785(_PR2)), ("art-62", "I -", "I - valores da arrecadação", _p14785(_PR2)))]
B13.OPEN_ITEMS[_LAG23] = (
    "Lei 14.785 (open items): the regulations strike no words and are not modelled; its art. 65's repeal of parts of the "
    "Anexos of Leis 6.938/1981 and 9.782/1999 concerns those laws, not this one")

# part zza: Lei 10.820/2003 (crédito consignado). Hand days set only when the act runs.
_LCONS = "lei-do-credito-consignado"
_W656C = ("Lei 10.820 arts. 1 to 5: Medida Provisória 656/2014 (DOU 8.10.2014) changed them in its art. 9, in force 'trinta dias "
          "após a sua publicação em relação aos arts. 9º a 17' (art. 55 II): from 7.11.2014, as for Lei 11.977 art. 41 in part m; "
          "Lei 13.097/2015 art. 52, its conversion, falls under art. 168 V (on publication, DOU 20.1.2015)")
if any(a["slug"] == _LCONS for a in ACTS):
    B7.CONVERTED_FIX["mp-719-2016"] = ("lei-13313-2016", "the MP page reads 'Convertida na Lei 13.313, de 2016' (no 'nº'); "
                                                        "Lei nº 13.313, de 14.7.2016")
    B7.CONVERTED_FIX["mp-1292-2025"] = ("lei-15179-2025", "the MP page captured on 11.6.2026 carries no conversion link; Lei nº "
                                                         "15.179, de 24.7.2025 (DOU 25.7.2025) is headed 'Conversão da Medida "
                                                         "Provisória nº 1.292, de 2025'")
    for _u in ("art-01", "art-02", "art-03", "art-04", "art-05"):
        P.VIGENCIA_PROVISION[("mp-656-2014", _LCONS, _u)] = ("2014-11-07", _W656C)
_W4P1 = ("Lei 10.820 art. 4 § 1º: Medida Provisória 656/2014 gave it a new wording (from 7.11.2014); Lei 13.097/2015, its "
         "conversion (DOU 20.1.2015), vetoed that change ('§ 1º (VETADO)' in its art. 52), so the MP's wording ends on 20.1.2015 "
         "and the 2003 wording, which Planalto prints a second time with '(Vide Medida Provisória nº 656, de 2014)', is back "
         "from that day until Medida Provisória 681/2015 (DOU 13.7.2015) rewrote it")
_W2IV = ("Lei 10.820 art. 2 IV: Planalto prints Medida Provisória 681/2015's wording unstruck above the same words given by Lei "
         "13.172/2015, its conversion (DOU 22.10.2015); the MP's wording ends on 22.10.2015")
_W6P7 = ("Lei 10.820 art. 6 § 7º: Planalto prints Lei 14.431/2022's wording unstruck above Lei 14.601/2023's (DOU 20.6.2023, art. "
         "29, in force on publication, art. 34 II), which rewrote it; Lei 14.431's wording ends on 20.6.2023")
B8.SPAN_FIX += [
    ((_LCONS, "art-04", "§ 1º", "§ 1º Poderá o empregador firmar com instituições consignatárias", 0),
     {"end": "2015-01-20", "end_law": "lei-13097-2015", "end_how": "conversion"}, _W4P1),
    ((_LCONS, "art-04", "§ 1º", "§ 1º Poderá o empregador, com a anuência", 1),
     {"start": "2015-01-20", "start_law": "lei-13097-2015", "restored": True,
      "end": "2015-07-13", "end_law": "mp-681-2015", "end_how": "successor"}, _W4P1),
    ((_LCONS, "art-02", "IV -", "IV - mutuário, empregado que firma com instituição consignatária contrato de empréstimo, "
      "financiamento, cartão de crédito", 0),
     {"end": "2015-10-22", "end_law": "lei-13172-2015", "end_how": "conversion"}, _W2IV),
    ((_LCONS, "art-06", "§ 7º", "§ 7º Aplica-se o previsto no caput e no § 5º deste artigo também", 0),
     {"end": "2023-06-20", "end_law": "lei-14601-2023", "end_how": "successor"}, _W6P7),
]
B.EXPLAINED[_LCONS] = {"art-02": "Planalto prints art. 2 IV twice unstruck, Medida Provisória 681/2015's wording above Lei "
                                 "13.172/2015's (the same words); the MP's ends on 22.10.2015",
                       "art-06": "Planalto prints art. 6 § 7º twice unstruck, Lei 14.431/2022's wording above Lei 14.601/2023's, "
                                 "which rewrote it; Lei 14.431's ends on 20.6.2023"}
B13.OPEN_ITEMS[_LCONS] = (
    "Lei 10.820 (open items): the text before 18.12.2003 (Medida Provisória 130/2003, of which this Lei is the conversion) is "
    "not part of the history; 'Vide' pointers (Medidas Provisórias 656/2014, 1.006/2020 and 1.355/2026, Lei 14.131/2021, whose "
    "temporary margins are that law's own rules) strike no words and are not modelled; the regulations strike no words")

# part zzb: Lei 6.360/1976 (vigilância sanitária de medicamentos). Hand items set only when the act runs.
_LVSM = "lei-da-vigilancia-sanitaria-de-medicamentos"
if any(a["slug"] == _LVSM for a in ACTS):
    P.MP_PENDING["mp-2190-2001"] = (
        "Medida Provisória nº 2.190-34, de 23.8.2001 (DOU 24.8.2001, art. 14: in force on publication), kept in force by Emenda "
        "Constitucional 32/2001, art. 2; its art. 9 gave arts. 3, 18 and 57 of Lei 6.360 the wordings Planalto notes "
        "with this edition and its art. 15 revoked art. 82 (noted 'Medida Provisória nº 2.190, de 2001'). Planalto's notes name this edition only, so the changes are dated by its publication; earlier editions of the "
        "chain are not modelled")
    for _k in ("Redação dada", "Incluído"):
        P.NOTE_FIX[f"({_k} pelo Decreto nº 6.480, de 1.12.1977)"] = (
            f"({_k} pela Lei nº 6.480, de 1.12.1977)",
            "Lei 6.360: two notes name 'Decreto nº 6.480, de 1.12.1977'; the act of that number and day is Lei nº 6.480, de "
            "1º de dezembro de 1977, which amends Lei 6.360 (read on its page)")
    B8.LAW_FIELD_FIX["lei-9782-1999"] = (
        {"url": PL + PAGES["l9782"]},
        "Lei 9.782/1999's law record takes the address of its page as part zb has it ('leis/l9782.htm'; Lei 6.360's notes link "
        "'L9782.htm', the same page), so the two parts' records are equal")
    B8.LABEL_FIX.append(
        ("l6360", "I - benefícios clínicos, econômicos e sociais", "II - benefícios clínicos, econômicos e sociais", "II -",
         "Lei 6.360 art. 17-A: Planalto prints the second inciso as 'I - benefícios clínicos [...]'; Lei 13.411/2016 (art. 1, "
         "read on its page) numbers it 'II -'"))

# part zzc: Lei 11.494/2007 (Fundeb 2007-2020). Repealed from 1.1.2021 by Lei 14.113/2020 art. 53 except art. 12; Lei
# 14.276/2021 (DOU 28.12.2021, in force on publication) narrowed the exception to the caput of art. 12 (its incisos stay).
_LF07 = "lei-do-fundeb-de-2007"
_W53 = ("Lei 11.494/2007: Lei 14.113/2020 (DOU 25.12.2020, in force on publication, art. 54) art. 53, as enacted: 'Fica "
        "revogada, a partir de 1º de janeiro de 2021, a Lei nº 11.494, de 20 de junho de 2007, ressalvado o art. 12 e mantidos "
        "seus efeitos financeiros no que se refere à execução dos Fundos relativa ao exercício de 2020' (the Lei's art. 48 had "
        "set the Funds' term to 31.12.2020). On 1.1.2021 every provision but art. 12 (and the heading of its Seção II) is "
        "removed, credited to Lei 14.113. Lei 14.276/2021 (DOU 28.12.2021, in force on publication, art. 2) gave art. 53 a new "
        "wording, 'ressalvado o caput do art. 12': art. 12 §§ 1º to 3º are removed on 28.12.2021, the day that wording took "
        "effect (its 'a partir de 1º de janeiro de 2021' reaches back, so the publication day is kept), credited to Lei "
        "14.276; the caput with its incisos I to III stays, as Planalto's page prints it today. The page is read from a "
        "capture of 15.12.2020, before the repeal (Planalto strikes the rest of the page afterwards); the history up to "
        "31.12.2020 is checked against that capture's text, the last version against the page as it is today")
_F07_CHECK: list[str] = []
_lifespansF07 = P.lifespans


def lifespans(paras, cx):
    problems = _lifespansF07(paras, cx)
    if cx.act == _LF07:
        # the heading kept is art. 12's own (its Seção II and name line), found by the name line's heading group
        grp = {p["label"].rsplit("-", 1)[0] for p in paras if p["unit"] == "titulos" and re.sub(r"\s+", " ", p["text"]).strip()
               == "Da Comissão Intergovernamental de Financiamento para a Educação Básica de Qualidade"}
        assert len(grp) == 1, grp
        for p in paras:
            if p.get("skip") or not (p["end"] is None or p["end"] > "2021-01-01") or p["start"] >= "2021-01-01":
                continue
            if p["unit"] == "preambulo":
                continue
            if p["unit"] == "titulos" and p["label"].rsplit("-", 1)[0] in grp:
                continue
            if p["unit"] == "art-12":
                if p["label"].startswith("§"):
                    p["end"], p["end_law"], p["end_how"], p["pinned"] = "2021-12-28", "lei-14276-2021", "act-repealed", True
                continue
            p["end"], p["end_law"], p["end_how"], p["pinned"] = "2021-01-01", "lei-14113-2020", "act-repealed", True
    return problems


P.lifespans = B.lifespans = lifespans
if any(a["slug"] == _LF07 for a in ACTS):
    EXTRA.append(_W53 + ".")
    # the two repealing laws no note of the 2020 capture names: records as part zm has them
    B8.EXTRA_LAWS["lei-14113-2020"] = dict(ACT_LAWS_ALL["lei-14113-2020"])
    B8.EXTRA_LAWS["lei-14276-2021"] = {
        "label": "Lei nº 14.276, de 2021", "kind": "law",
        "title": "Altera a Lei nº 14.113, de 25 de dezembro de 2020, que regulamenta o Fundo de Manutenção e Desenvolvimento da "
                 "Educação Básica e de Valorização dos Profissionais da Educação (Fundeb).",
        "enacted": "2021-12-27", "published": "2021-12-28", "url": PL + "_ato2019-2022/2021/Lei/L14276.htm",
        "temporary_until": None, "restores": None, "note": None}
B13.OPEN_ITEMS[_LF07] = (
    "Lei 11.494 (open items): the text before 21.6.2007 (Medida Provisória 339/2006, of which this Lei is the conversion) is "
    "not part of the history; its Anexo (the distribution formulas, printed as images after the signature) is not read; the "
    "financial effects for 2020 that Lei 14.113 art. 53 keeps change no words; 'Vide' pointers and regulations strike no "
    "words")

# part zzd: Lei 9.424/1996 (Fundef). Its arts. 1 to 8 and 13 were revoked 'a partir de 1º de janeiro de 2007' by Medida
# Provisória 339/2006 art. 48 (DOU 29.12.2006, in force on publication, art. 50); Lei 11.494/2007, its conversion (DOU
# 21.6.2007), repeats the revocation in its art. 46. Planalto notes 'Revogado pela Lei nº 11.494, de 2007' with '(Vide Medida
# Provisória nº 339, de 2006)': the lines go on 1.1.2007, the day the revocation took effect, credited to MP 339.
_LFUNDEF = "lei-do-fundef"
_W339 = ("Lei 9.424 arts. 1 to 8 and 13: Medida Provisória 339/2006 (DOU 29.12.2006, in force on publication, art. 50) art. 48: "
         "'Ficam revogados, a partir de 1º de janeiro de 2007, os arts. 1º a 8º e 13 da Lei nº 9.424, de 24 de dezembro de 1996' "
         "(read on the MP's page); Lei 11.494/2007, its conversion (DOU 21.6.2007), repeats it in its art. 46. Planalto notes "
         "the lines 'Revogado pela Lei nº 11.494, de 2007' with '(Vide Medida Provisória nº 339, de 2006)'; they are removed on "
         "1.1.2007, the day the revocation took effect, credited to MP 339 (Lei 11.494's own 'a partir de 1º de janeiro de 2007' "
         "reaches back before its publication and continues the MP's revocation)")
_F339_USED: list[str] = []
_lifespansFD = P.lifespans


def lifespans(paras, cx):
    problems = _lifespansFD(paras, cx)
    if cx.act == _LFUNDEF:
        for p in paras:
            if p.get("end_law") == "lei-11494-2007" and p.get("end") == "2007-06-21" and not p.get("skip"):
                p["end"], p["end_law"], p["end_how"], p["pinned"] = "2007-01-01", "mp-339-2006", "note", True
                _F339_USED.append(f"{p['unit']} {p['label']}")
    return problems


P.lifespans = B.lifespans = lifespans
if any(a["slug"] == _LFUNDEF for a in ACTS):
    EXTRA.append(_W339 + ".")
    B8.EXTRA_LAWS["mp-173-2004"] = {
        "label": "Medida Provisória nº 173, de 2004", "kind": "law",
        "title": "Institui o Programa Nacional de Apoio ao Transporte do Escolar - PNATE e o Programa de Apoio aos Sistemas de "
                 "Ensino para Atendimento à Educação de Jovens e Adultos, dispõe sobre o repasse de recursos financeiros do "
                 "Programa Brasil Alfabetizado, altera o art. 4º da Lei nº 9.424, de 24 de dezembro de 1996, e dá outras "
                 "providências.",
        "enacted": "2004-03-16", "published": "2004-03-17",
        "url": PL + "_Ato2004-2006/2004/Mpv/173.htm", "temporary_until": None, "restores": None, "note": None}
    # the MP the revocation is credited to: Planalto's notes name it only in 'Vide' pointers
    B8.EXTRA_LAWS["mp-339-2006"] = {
        "label": "Medida Provisória nº 339, de 2006", "kind": "law",
        "title": "Regulamenta o art. 60 do Ato das Disposições Constitucionais Transitórias e dá outras providências.",
        "enacted": "2006-12-28", "published": "2006-12-29",
        "url": PL + "_Ato2004-2006/2006/Mpv/339.htm", "temporary_until": None, "restores": None, "note": None}
    P.VIGENCIA_FIXED["lei-10832-2003"] = (
        "2004-01-01", "art. 3: 'Esta Lei entra em vigor no 1º (primeiro) dia do exercício financeiro seguinte ao de sua "
                      "publicação' (DOU 30.12.2003): 1.1.2004")
B8.SPAN_FIX.append(
    ((_LFUNDEF, "art-04", "§ 5º", "§ 5º Aos Conselhos incumbe acompanhar", 0),
     {"start": "2004-03-17", "start_law": "mp-173-2004", "by_provision": True},
     "Lei 9.424 art. 4 § 5º: Planalto notes it '(Incluído pela Lei nº 10.880, de 2004)' (DOU 11.6.2004); Lei 10.880 is the "
     "conversion of Medida Provisória 173/2004 (DOU 17.3.2004, in force on publication, art. 11), whose art. 10 added the same § "
     "5º word for word (read on the MP's page), so the paragraph is in force from 17.3.2004, credited to MP 173; the conversion "
     "keeps it"))
B13.OPEN_ITEMS[_LFUNDEF] = (
    "Lei 9.424 (open items): 'Vide' pointers (ADI 1.627 at art. 9 and art. 10 II, ADPF 188 at art. 15, Decretos 5.299/2004 "
    "and 5.374/2005, Medida Provisória 339/2006 beside lines it did not revoke) strike no words and are not modelled; the "
    "regulations strike no words")

# part zze: Leis Complementares 109/2001 and 108/2001 (previdência complementar). Hand items set only when the act runs.
_LC109 = "lei-da-previdencia-complementar"
if any(a["slug"] == _LC109 for a in ACTS):
    P.VIGENCIA_FIXED["lc-213-2025"] = (
        "2025-01-16", "art. 13: 'Esta Lei Complementar entra em vigor: I - quanto ao art. 3º, na parte em que altera o Capítulo X "
                      "do Decreto-Lei nº 73 [...], após decorrido 1 (um) ano [...]; II - quanto ao art. 3º, na parte em que acresce "
                      "o § 4º ao art. 88-E do Decreto-Lei nº 73 [...], após decorridos 4 (quatro) anos [...]; III - quanto aos "
                      "demais dispositivos, na data de sua publicação' (DOU 16.1.2025): its art. 6, which gives Lei Complementar "
                      "109 art. 38 III its wording, falls under III, in force on 16.1.2025")
B13.OPEN_ITEMS[_LC109] = (
    "Lei Complementar 109 (open items): 'Vide' pointers (Decreto 7.123/2010) and the regulations strike no words and are not "
    "modelled")

# part zzg: Lei Complementar 179/2021 and Lei 14.286/2021 (mercado de câmbio). Hand items set only when the act runs.
_LCAMBIO = "lei-do-mercado-de-cambio"
_W24C = ("Lei 14.286 art. 24 (which gave Lei 8.383 art. 50 a new caput and revoked its parágrafo único): Lei 14.596/2023 art. "
         "46 XI revokes 'a partir de 1º de janeiro de 2024 [...] art. 24 da Lei nº 14.286, de 29 de dezembro de 2021, na parte em "
         "que altera o art. 50 da Lei nº 8.383' (art. 47: in force 1.1.2024; read on its page). Planalto strikes both quoted "
         "lines (the caput noted 'Revogado pela Lei nº 14.596, de 2023', the 'Parágrafo único. (Revogado).\" (NR)' line struck "
         "with it); both end on 1.1.2024, credited to Lei 14.596. Medida Provisória 1.152/2022 (DOU 29.12.2022), whose art. 47 XI "
         "made the same revocation from 1.1.2024 (art. 48), was converted into Lei 14.596 (DOU 15.6.2023) before that day; "
         "Planalto names it in a 'Vide' pointer only. Art. 24's opening words stay, as Planalto prints them")
if any(a["slug"] == _LCAMBIO for a in ACTS):
    P.VIGENCIA_FIXED["lei-14596-2023"] = (
        "2024-01-01", "art. 47: 'Esta Lei entra em vigor em 1º de janeiro de 2024, exceto o art. 45, que entra em vigor na data de "
                      "sua publicação' (DOU 15.6.2023): its art. 46 XI (Lei 14.286 art. 24, in the part that amends Lei 8.383 "
                      "art. 50) from 1.1.2024")
B8.SPAN_FIX += [
    ((_LCAMBIO, "art-24", "Parágrafo único", "Parágrafo único. (Revogado).", 0),
     {"skip": False, "end": "2024-01-01", "end_law": "lei-14596-2023", "end_how": "note", "pinned": True}, _W24C),
]
B.EXPLAINED[_LCAMBIO] = {"art-25": _DOTTED}
B13.OPEN_ITEMS[_LCAMBIO] = (
    "Lei 14.286 (open items): its regulations (Resoluções of the Conselho Monetário Nacional and the Banco Central) strike no "
    "words and are not modelled")

# part zzh: Lei 14.134/2021 (Lei do Gás) and Lei Complementar 75/1993 (Estatuto do MPU).
_LGAS = "lei-do-gas"
L14134_FIXED: list[str] = []
LODP_FIXED: list[int] = []
_paragraphsGAS = P.paragraphs


def paragraphs(html, digits):
    if B8.CURRENT_PAGE[0] == "lcp80":
        # Lei Complementar 80: Planalto codes the ordinal signs 'º' and 'ª' with a strike tag ('9<s>º</s>', '2<s>ª</s>
        # Categoria'), 56 times, as on Lei Complementar 132's own page: read as plain text
        html, n = re.subn(r"<s>\s*([ºª])\s*</s>", r"\1", html)
        LODP_FIXED.append(n)
    out, rest = _paragraphsGAS(html, digits)
    if B8.CURRENT_PAGE[0] == "l14134":
        # Lei 14.134 art. 46 quotes Lei 9.478 arts. 2, 8, 8-A, 23 and 58; the first quoted line 'Art. 2º ......' has no opening
        # quotation mark, so the reader files it and the quoted lines after it under Lei 14.134's own art. 2: they belong to
        # art. 46 (lines after art. 46's caput and before art. 47)
        seen46 = seen47 = False
        for p in out:
            if p["unit"] == "art-46":
                seen46 = True
            elif p["unit"] == "art-47":
                seen47 = True
            elif p["unit"] == "art-02" and seen46 and not seen47 and not p["heading"]:
                p["unit"] = "art-46"
                if p["label"].startswith("Art"):
                    p["label"] = ""
                L14134_FIXED.append(P.norm(p["text"])[:40])
    return out, rest


P.paragraphs = B.paragraphs = paragraphs
if any(a["slug"] == _LGAS for a in ACTS):
    EXTRA.append("Lei 14.134: art. 46 quotes Lei 9.478 arts. 2, 8, 8-A, 23 and 58; Planalto prints the first quoted line "
                 "('Art. 2º ......') with no opening quotation mark, and the quoted lines are read as lines of art. 46, not as "
                 "Lei 14.134's own art. 2.")
B.EXPLAINED[_LGAS] = {"art-46": _DOTTED}
_LODP = "lei-organica-da-defensoria-publica"
if any(a["slug"] == _LODP for a in ACTS):
    EXTRA.append("Lei Complementar 80: Planalto codes the ordinal signs 'º' and 'ª' with a strike tag in 56 places ('Art. "
                 "9<s>º</s>', '2<s>ª</s> Categoria'), as on Lei Complementar 132's own page; the signs are read as plain text, "
                 "not as struck words.")
B13.OPEN_ITEMS[_LGAS] = (
    "Lei 14.134 (open items): its regulations (Decreto 10.712/2021, ANP resolutions) strike no words and are not modelled")
B13.OPEN_ITEMS["estatuto-do-ministerio-publico-da-uniao"] = (
    "Lei Complementar 75 (open items): Planalto's page (capture of 11.10.2026) carries no amendment note, so the history is the "
    "text as enacted; 'Mensagem de veto' (the vetoed parts) and the regulations strike no words")

# part zzj: Lei 12.813/2013 (conflito de interesses) and Lei 8.437/1992 (cautelares contra o Poder Público). Hand items set
# only when the act runs.
_LCI = "lei-de-conflito-de-interesses"
_LCPP = "lei-das-cautelares-contra-o-poder-publico"
if any(a["slug"] == _LCI for a in ACTS):
    P.MP_LAPSE["mp-792-2017"] = (
        "2017-11-29", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 65, de 2017 (DOU 7.12.2017): 'teve seu prazo "
                      "de vigência encerrado no dia 28 de novembro do corrente ano'; the replaced wording is back from 29.11.2017")
    # (the text is part 95-rju's, word for word: the lapse record built from it must be equal in both parts)
if any(a["slug"] == _LCPP for a in ACTS):
    for _k in ("Incluído", "Redação dada"):
        P.NOTE_FIX[f"({_k} pela Medida Provisória nº 2,180-35, de 2001)"] = (
            f"({_k} pela Medida Provisória nº 2.180-35, de 2001)",
            "Lei 8.437: Planalto's notes print the number of Medida Provisória 2.180-35/2001 with a comma ('2,180-35')")
    P.MP_PENDING["mp-2180-2001"] = (
        "Medida Provisória nº 2.180-35, de 24.8.2001 (DOU 27.8.2001, in force on publication), kept in force by Emenda "
        "Constitucional 32/2001, art. 2; its art. 1 gave Lei 8.437 the wordings Planalto notes with this edition. Planalto's "
        "notes name this edition only, so the changes are dated by its publication; earlier editions of the chain are not "
        "modelled")
B13.OPEN_ITEMS[_LCI] = (
    "Lei 12.813 (open items): 'Vide' pointers and the regulations strike no words and are not modelled")
B13.OPEN_ITEMS[_LCPP] = (
    "Lei 8.437 (open items): the earlier editions of Medida Provisória 2.180 (from 1.570/1997 on) are not modelled; 'Vide' "
    "pointers (ADIs) strike no words")

# parts zzk (Lei 9.494/1997) and zzl (Lei 14.129/2021)
if any(a["slug"] == "lei-do-governo-digital" for a in ACTS):
    EXTRA.append("Lei 14.129: arts. 32 and 35 (with its parágrafo único), vetoed on enactment, were promulgated after the veto "
                 "was overridden (DOU 11.6.2021, '(Promulgação partes vetadas)'); that day falls before the Lei's federal stage "
                 "(28.6.2021), so the promulgated text stands from the first version and the '(VETADO)' lines Planalto strikes "
                 "were never in force.")
B13.OPEN_ITEMS["lei-da-tutela-antecipada-contra-a-fazenda-publica"] = (
    "Lei 9.494 (open items): the text before 11.9.1997 (Medida Provisória 1.570/1997 and its editions, of which this Lei is the "
    "conversion) is not part of the history; earlier editions of Medida Provisória 2.180 are not modelled; 'Vide' pointers (ADC "
    "4, ADIs) strike no words")
B13.OPEN_ITEMS["lei-do-governo-digital"] = (
    "Lei 14.129 (open items): art. 55 staggers its entry into force by level of government (90 days for the União, 28.6.2021; "
    "120 days for the States and the Distrito Federal, 28.7.2021; 180 days for the Municipalities, 26.9.2021); the history is "
    "dated by the federal stage and the later stages change no words; the regulations strike no words")

# part zzm: Decreto-Lei 200/1967 (organização da Administração Federal). Hand items set only when the act runs.
_DL200 = "decreto-lei-200-de-1967"
if any(a["slug"] == _DL200 for a in ACTS):
    P.NOTE_FIX["(Revogado pelo Decreto-Lei nº 900, de 1968)"] = (
        "(Revogado pelo Decreto-Lei nº 900, de 1969)",
        "Decreto-Lei 200: 35 notes read 'Decreto-Lei nº 900, de 1968'; their links go to Decreto-Lei 900 of 29.9.1969 "
        "(Del0900.htm#art8), the only Decreto-Lei of that number")
    P.VIGENCIA_FIXED["dl-991-1969"] = (
        "1969-10-30", "art. 2: 'Êste Decreto-lei entra em vigor a 30 de outubro de 1969' (DOU 21.10.1969)")
# art. 39 lists each Ministry's matters under its own heading, numbering the items anew (I, II, ...) under each one: the
# items VI of the Ministérios da Agricultura, da Indústria e do Comércio, do Interior and do Trabalho are the 1967 text, not
# copies of the Ministério da Fazenda's item VI (rewritten by Lei 6.228/1975) that the twin-wording rule would leave out
_W39 = ("Decreto-Lei 200 art. 39 numbers the items anew under each Ministry's heading, so the label 'VI -' occurs six times: "
        "the items VI of the Ministérios da Agricultura, da Indústria e do Comércio, do Interior and do Trabalho e Previdência "
        "Social are the 1967 text, in force from 15.3.1967 with no end, and not copies of the Ministério da Fazenda's item VI "
        "(struck 'Serviços Gerais', rewritten by Lei 6.228/1975 as 'Administração patrimonial')")
B8.SPAN_FIX += [((_DL200, "art-039", "VI -", _t, 0), {"keep": True}, _W39) for _t in (
    "VI - Pesquisa e experimentação.", "VI - Pesquisa e experimentação tecnológica.",
    "VI - Assistência às populações atingidas", "VI - Colaboração com o Ministério Público")]
B15.TEXT_FIX.append(("del0200", "especificados:,$", "especificados:",
                     "Decreto-Lei 200 art. 39 caput: Planalto prints a comma between the two 'Vide' links after the caput "
                     "('especificados: (Vide ...) , (Vide ...)'); the links are dropped and the comma with them"))
# paragraphs wrapper (page del0200): (1) the struck 'SETOR ...' lines of arts. 35 and 39 (Ministries grouped by sector,
# 'Suprimido pelo Decreto-Lei 900, de 1969') and art. 39's Ministry names ('MINISTÉRIO DA JUSTIÇA', each above its list of
# matters) are printed as heading blocks like the Títulos; they are lines of their article.
# (2) Planalto prints 'Vide' links without parentheses after three lines (arts. 32 and 35 capita, art. 95): dropped, as the
# reader drops parenthesised 'Vide' notes.
DL200_FIXED: list[str] = []
_VIDE_TAIL = re.compile(r"(?:\s*,?\s*Vide (?:Lei|Decreto) nº [\d.]+, de [\d.]+)+\s*,?\s*$")
_paragraphsDL200 = P.paragraphs
_DL200_SWAP = {"art-097": ("nas condições previstas neste artigo.", "nos têrmos da legislação trabalhista."),
               "art-161": ("serão regulados em lei.", "serão regulados em decreto.")}


def paragraphs(html, digits):
    if B8.CURRENT_PAGE[0] == "del0200":
        # five Seção headings are typed 'SEçãO I' (lower-case 'çã'), which the heading reader does not know: read 'SEÇÃO'
        html, n = re.subn(r"SE(?:ç|&ccedil;)(?:ã|&atilde;)O", "SEÇÃO", html)
        DL200_FIXED.extend(["Seção"] * n)
    out, rest = _paragraphsDL200(html, digits)
    if B8.CURRENT_PAGE[0] == "del0200":
        prev = None
        for p in out:
            if p["heading"] and p["text"].startswith(("SETOR ", "MINISTÉRIO ")) and prev:
                p["heading"], p["unit"], p["label"] = False, prev, ""
                DL200_FIXED.append(f"{prev} {p['text']}")
            elif not p["heading"] and p["unit"] != "titulos":
                prev = p["unit"]
            m = _VIDE_TAIL.search(p["text"])
            if m and not p["heading"]:
                p["text"] = p["text"][:m.start()].rstrip()
                DL200_FIXED.append(f"{p['unit']} Vide links")
        # arts. 97 and 161: Planalto prints only the wording after Decreto-Lei 900/1969 art. 7 ('Ficam substituídas: I - no
        # artigo 97 [...] as expressões "nas condições previstas neste artigo" por "nos têrmos da legislação trabalhista";
        # II - no artigo 161 [...] a palavra "lei" por "decreto"'), noted '(Expressão substituída pelo Decreto-Lei nº 900, de
        # 1969)': the 1967 wording is read back from that article, as a struck line above the printed one
        res = []
        for p in out:
            sw = _DL200_SWAP.get(p["unit"])
            if (sw and p["state"] == "plain" and not p["heading"] and p["text"].endswith(sw[1])
                    and "(Expressão substituída pelo Decreto-Lei nº 900, de 1969)" in p["notes"]):
                notes = [n for n in p["notes"] if not n.startswith("(Expressão substituída")]
                res.append({**p, "text": p["text"][:-len(sw[1])] + sw[0], "state": "struck", "notes": notes})
                res.append({**p, "notes": notes + ["(Redação dada pelo Decreto-Lei nº 900, de 1969)"]})
                DL200_FIXED.append(f"{p['unit']} 1967 wording")
            else:
                res.append(p)
        out[:] = res
    return out, rest


P.paragraphs = B.paragraphs = paragraphs
if any(a["slug"] == _DL200 for a in ACTS):
    EXTRA.append("Decreto-Lei 200: the struck sector lines of arts. 35 and 39 ('SETOR POLÍTICO', 'SETOR ECONÔMICO', ...; "
                 "'Suprimido pelo Decreto-Lei 900, de 1969') and art. 39's Ministry names ('MINISTÉRIO DA JUSTIÇA', ...), "
                 "which Planalto prints as heading blocks, are read as lines of their article; the 'Vide' links Planalto prints without parentheses after the capita of arts. 32 and 35 "
                 "and after art. 95 are dropped, as parenthesised 'Vide' notes are. Arts. 97 and 161: Planalto prints only "
                 "the wording after Decreto-Lei 900/1969 art. 7 ('Ficam substituídas: I - no artigo 97 [...] as expressões "
                 "\"nas condições previstas neste artigo\" por \"nos têrmos da legislação trabalhista\"; II - no artigo 161 "
                 "[...] a palavra \"lei\" por \"decreto\"'), noted 'Expressão substituída'; the 1967 wording is read back "
                 "from that article and stands until 30.9.1969 (DOU of Decreto-Lei 900, in force on publication). Five Seção "
                 "headings typed 'SEçãO' are read as 'SEÇÃO'.")
B13.OPEN_ITEMS[_DL200] = (
    "Decreto-Lei 200 (open items): art. 214 puts the Decreto-Lei in force on 15.3.1967 'ressalvadas as disposições cuja "
    "vigência, na data da publicação, seja por ela expressamente determinada': only art. 113 (revocation of Lei 1.711/1952 "
    "arts. 62-63 'na data da publicação') is such a provision, and its effect falls on another law, so the history starts on "
    "15.3.1967; the rectifications of 8.3.1967, 30.3.1967 and 17.7.1967 are read as already in Planalto's text (the DOU pages "
    "are not part of the record); 'Vide' pointers (Leis 6.036/1974, 6.228/1975, 7.739/1989, 7.995/1990, 8.028/1990, "
    "10.683/2003 and decrees) strike no words; the history holds the changes Planalto notes on this page")

# part zzn: Lei 12.351/2010 (partilha de produção, Fundo Social). Hand items set only when the act runs (except the tables,
# which are keyed to the act).
_LPART = "lei-da-partilha-de-producao"
_P734 = ("2013-03-15", "lei-12734-2012")   # Lei 12.734/2012's vetoed parts, promulgated 14.3.2013 (DOU 15.3.2013)
if any(a["slug"] == _LPART for a in ACTS):
    P.NOTE_FIX["(Redação pela Medida Provisória nº 592, de 2012)"] = (
        "(Redação dada pela Medida Provisória nº 592, de 2012)",
        "Lei 12.351 art. 42-B II f): the note of Medida Provisória 592's wording reads 'Redação pela' (the word 'dada' missing)")
    P.MP_PENDING["mp-1226-2024"] = (
        "Medida Provisória nº 1.226, de 29.5.2024 (DOU 29.5.2024, in force on publication), was not converted: Lei 14.981/2024 "
        "art. 29 III revoked it (DOU 23.9.2024, in force on publication) and gave arts. 47 § 4º and 47-A their own wordings, so "
        "the MP's wordings end on 23.9.2024")
    EXTRA.append(
        "Lei 12.351: Lei 12.734/2012 (DOU 30.11.2012, edição extra) was sanctioned in part; the parts the President vetoed and "
        "Congress restored, promulgated on 14.3.2013 (DOU 15.3.2013; marked '(Promulgado em 14.03.2013)' on Lei 12.734's page), "
        "start on 15.3.2013: in art. 42-B the items 1, 3, 4 and 5 of alíneas d) and e) of incisos I and II and §§ 1º (with its "
        "incisos) to 4º, the whole art. 42-C, and the revocation of art. 49 IV and § 1º (Lei 12.734 art. 4 II), so those two "
        "dispositivos (and the Lei 9.478 text § 1º quotes) stand until 15.3.2013. Before that day the vetoed items read only "
        "'(VETADO)' in Lei 12.734 and are absent here.")
    EXTRA.append(
        "Lei 12.351 art. 60-A (tax exemption of the Fundo Social's operations, added by Lei 15.164/2025): art. 65-A, parágrafo "
        "único, added by the same Lei, says the renúncia fiscal of art. 60-A 'vigorará de 1º de janeiro de 2026 a 31 de dezembro "
        "de 2030', so art. 60-A stands from 1.1.2026 and leaves the record on 1.1.2031, the day after its term (on futuro), "
        "both credited to Lei 15.164.")
    # the ruling's record exactly as 99-batch10 has it (Lei do Petróleo)
    B8.EXTRA_LAWS["stf-adi-4917"] = {
        "label": "STF, ADI 4.917 (medida cautelar)", "kind": "court", "enacted": "2013-03-18", "published": "2013-03-21",
        "title": "Ação direta de inconstitucionalidade 4.917, medida cautelar (decisão monocrática, ad referendum do Plenário): "
                 "suspende os efeitos dos arts. 42-B, 42-C, 48, II, 49, II, 49-A, 49-B, 49-C, § 2º do art. 50, 50-A, 50-B, "
                 "50-C, 50-D e 50-E da Lei nº 9.478, de 1997, com as alterações promovidas pela Lei nº 12.734, de 2012",
        "url": "https://portal.stf.jus.br/processos/detalhe.asp?incidente=4379376", "temporary_until": None,
        "restores": None,
        "note": "A rapporteur's interim ruling (ADI 4.917, 18 March 2013) suspended the effects of the royalty rules Lei "
                "12.734/2012 wrote into these provisions until the court's final judgment; the words are unchanged on "
                "Planalto's page, so they are unchanged here."}
    EXTRA.append(
        "Lei 12.351 Anexo (the pre-salt polygon, Lei art. 2 IV): printed after the signature, where the reader stops; read here "
        "as unit 'anexo', one line per table row (the cells of a row separated by a space, as the page's text runs).")
PROMULGATED[_LPART] = [("art-42-b", "", f"{_n}. {_t}", *_P734) for _n, _t in (
    ("1", "os recursos serão distribuídos somente para"), ("3", "o percentual que o FP"), ("4", "o "), ("5", "os recursos que"))] + [
    ("art-42-b", "§ 1º", "§ 1º A soma dos valores referentes aos royalties", *_P734),
    ("art-42-b", "I -", "I - os valores que o Município recebeu", *_P734),
    ("art-42-b", "II -", "II - 2 (duas) vezes o valor per capita", *_P734),
    ("art-42-b", "§ 2º", "§ 2º A parcela dos royalties de que trata este artigo", *_P734),
    ("art-42-b", "§ 3º", "§ 3º Os pontos de entrega", *_P734),
    ("art-42-b", "§ 4º", "§ 4º A opção dos Estados", *_P734),
    ("art-42-c", "Art. 42-C", "Art. 42-C. Os recursos do fundo especial", *_P734)]
_W49 = ("Lei 12.351 art. 49 IV and § 1º (with the text of Lei 9.478 arts. 49 § 3º and 50 § 4º that § 1º quotes): revoked by Lei "
        "12.734/2012 art. 4 II, a part vetoed on enactment and promulgated on 14.3.2013 (DOU 15.3.2013); they stand until that day")
_E49 = {"end": _P734[0], "end_law": _P734[1], "end_how": "note", "skip": False}
B8.SPAN_FIX += [((_LPART, "art-49", _l, _t, 0), dict(_E49), _W49) for _l, _t in (
    ("IV -", "IV - os royalties"), ("§ 1º", "§ 1º A Lei nº 9.478"), ("", '"Art. 49.'), ("§ 3º", "§ 3º Nas áreas localizadas no pré-sal"),
    ("", '"Art. 50.'), ("§ 4º", "§ 4º Nas áreas localizadas no pré-sal"))]
_W58 = ("Lei 12.351 art. 58 § 5º: Lei 15.164/2025 art. 1 gave it a new wording ('[...] desta Lei deverão observar critérios de redução "
        "das desigualdades sociais e regionais', read on its page); Planalto prints the new wording under the 2010 one with no note: "
        "the 2010 wording ends and the new one starts on 15.7.2025, credited to Lei 15.164")
B8.SPAN_FIX += [
    ((_LPART, "art-58", "§ 5º", "§ 5º Os recursos do FS destinados aos programas e projetos de que trata o art. 47 devem", 0),
     {"end": "2025-07-15", "end_law": "lei-15164-2025", "end_how": "successor", "skip": False}, _W58),
    ((_LPART, "art-58", "§ 5º", "§ 5º Os recursos do FS destinados aos programas e projetos de que trata o art. 47 desta Lei", 0),
     {"start": "2025-07-15", "start_law": "lei-15164-2025", "by_provision": True}, _W58)]
_W42F = ("Lei 12.351 art. 42-B II f): Lei 12.734/2012's wording (30.11.2012) was replaced by Medida Provisória 592/2012 (3.12.2012) "
        "and is back when the MP lapsed (13.5.2013); Planalto prints it after the MP's struck wording, so the reader started it "
        "only at the lapse: it stands from 30.11.2012 with the MP's months as a gap")
B8.SPAN_FIX += [((_LPART, "art-42-b", "f)", "f) 22% (vinte e dois por cento) para a União", 0),
                 {"start": "2012-11-30", "start_law": "lei-12734-2012", "restored": False,
                  "gaps": [["2012-12-03", "2013-05-13", "mp-592-2012", "mp-592-2012-fim"]]}, _W42F)]
_W60A = ("Lei 12.351 art. 60-A: in effect from 1.1.2026 to 31.12.2030 (art. 65-A, parágrafo único, Lei 15.164/2025); it stands from "
         "1.1.2026 and leaves on 1.1.2031, credited to Lei 15.164")
B8.SPAN_FIX += [((_LPART, "art-60-a", _l, _t, 0), {"start": "2026-01-01", "start_law": "lei-15164-2025", "by_provision": True,
                                                   "end": "2031-01-01", "end_law": "lei-15164-2025", "end_how": "term"}, _W60A)
                for _l, _t in (("Art. 60-A", "Art. 60-A."), ("§ 1º", "§ 1º Ficam reduzidas"), ("§ 2º", "§ 2º Fica a Casa Civil"))]
B13.OPEN_ITEMS[_LPART] = (
    "Lei 12.351 (open items): the text before Lei 12.734/2012's vetoed items were promulgated reads '(VETADO)' in that Lei and is "
    "not printed on Lei 12.351's page (the items are absent until 15.3.2013); STF, ADI 4.917 (medida cautelar of 18.3.2013, "
    "pending) suspended the effects of arts. 42-B and 42-C: recorded as a version that changes no words; Lei 15.269/2025's vetoed "
    "art. 47 § 4º III reads '(VETADO)'; 'Vide' pointers and the regulations strike no words")
B.EXPLAINED[_LPART] = {
    "anexo": "check artefact: the check sets aside a unit made only of lines with no label and no closing punctuation (taken for "
             "the marginal heading of a revoked article); this unit holds the Anexo's title lines and its polygon table, which "
             "Planalto's page prints after the signature"}
L12351_ANNEX: list[str] = []
_paragraphsLP = P.paragraphs


def paragraphs(html, digits):
    out, rest = _paragraphsLP(html, digits)
    if B8.CURRENT_PAGE[0] == "l12351":
        # the Anexo (pre-salt polygon) after the signature: 'ANEXO', two title rows, a header row and 12 vertex rows
        ann, row, unit = [], [], None
        for b in [P.analyse(x) for x in P.blocks_of(html)]:
            t = b["text"]
            if unit is None:
                if t == "ANEXO":
                    unit = "anexo"
                    ann.append({**b, "unit": unit, "label": "", "heading": False})
                continue
            if not t or t == "*" or re.fullmatch(r"[.;,:\s*]+", t):
                continue
            if t in ("POLÍGONO PRÉ-SAL", "COORDENADAS POLICÔNICA/SAD69/MC54"):
                ann.append({**b, "unit": unit, "label": "", "heading": False})
                continue
            row.append(b)
            if len(row) == 3:
                ann.append({**row[0], "text": " ".join(x["text"] for x in row), "unit": unit, "label": "", "heading": False})
                row = []
        if row:
            L12351_ANNEX.append(f"unfinished row {[x['text'] for x in row]}")
        out = out + ann
        for i, q in enumerate(out):
            q["i"] = i
        L12351_ANNEX.append(f"{len(ann)} lines")
    return out, rest


P.paragraphs = B.paragraphs = paragraphs
_ADI4917_12351 = ("Lei 12.351: STF, ADI 4.917, medida cautelar of 18.3.2013 (the ruling 99-batch10 records for the Lei do Petróleo) "
                  "names arts. 42-B and 42-C among the provisions whose effects it suspends; those two articles are the ones Lei "
                  "12.734/2012 added to this Lei (Planalto prints '(Vide ADI 4917)' on art. 42-B). The words are unchanged, so the "
                  "ruling is recorded as a version on 18.3.2013 that changes no words, credited to those two articles")
ADI4917_12351_USED: list[str] = []

# part zzo: Lei 8.625/1993 (LONMP) and Lei 14.601/2023 (Bolsa Família)
_LPBF = "lei-do-programa-bolsa-familia"
if any(a["slug"] == _LPBF for a in ACTS):
    EXTRA.append("Lei 14.601: its art. 34 puts arts. 30 and 31, art. 33 I and art. 4 § 3º in force on 1.1.2024 and the rest on "
                 "publication (20.6.2023): arts. 30 and 31 first show on 1.1.2024, and the § 3º of art. 4 and inciso I of art. 33 "
                 "start that day, credited to Lei 14.601 (Planalto marks each with a 'Vigência' link).")
_W14601 = "Lei 14.601 art. 34 I: in force on 1.1.2024"
B8.SPAN_FIX += [((_LPBF, _u, _l, _t, 0), {"start": "2024-01-01", "start_law": "lei-14601-2023", "by_provision": True}, _W14601)
                for _u, _l, _t in (("art-04", "§ 3º", "§ 3º O Poder Executivo poderá autorizar o desconto"),
                                   ("art-33", "I -", "I - os §§ 8º, 9º e 10 do art. 2º da Lei nº 10.779"))]
B13.OPEN_ITEMS["lei-organica-nacional-do-ministerio-publico"] = (
    "Lei 8.625 (open items): Planalto's page (capture pinned) carries no amendment note, so the history is the text as enacted; "
    "'Mensagem de veto' (the vetoed parts) and the regulations strike no words")
B13.OPEN_ITEMS[_LPBF] = (
    "Lei 14.601 (open items): the text before 20.6.2023 (Medida Provisória 1.164/2023, of which this Lei is the conversion) is "
    "not part of the history; the regulations strike no words")

# part zzp: Lei 12.618/2012 (Funpresp). Hand days set only when the act runs.
_LFUNP = "lei-da-previdencia-complementar-dos-servidores-federais"
# Lei 12.618 art. 33 I: Capítulo I (arts. 1 to 3) in force 'na data em que forem criadas quaisquer das entidades de que trata o
# art. 4º, observado o disposto no art. 31'. Decreto 7.808/2012 art. 1 created the Funpresp-Exe; its art. 12 puts it in force on
# publication (DOU 21.9.2012). Planalto prints '(Vide Decreto nº 7.808, de 2012)' on art. 33 I.
_G12618 = {u: ("2012-09-21", "I") for u in ("art-01", "art-02", "art-03")}
G12618_USED: list[str] = []
_GATES[_LFUNP] = (_G12618, "lei-12618-2012", G12618_USED)
# part zzq: Lei 12.865/2013 art. 43 I: art. 34 (its changes to Lei 12.350/2010 arts. 54 and 55) from 1.2.2014
_L12865 = "lei-12865-de-2013"
_G12865 = {"art-34": ("2014-02-01", "I")}
G12865_USED: list[str] = []
_GATES[_L12865] = (_G12865, "lei-12865-2013", G12865_USED)
if any(a["slug"] == _LFUNP for a in ACTS):
    B7.CONVERTED_FIX["mp-1119-2022"] = ("lei-14463-2022", "the MP page reads 'Convertida na Lei nº Lei nº 14.463, de 2022' (the "
                                                          "words 'Lei nº' printed twice); Lei 14.463's page reads 'Conversão da "
                                                          "Medida Provisória nº 1.119, de 2022'")
    P.MP_LAPSE["mp-1286-2024"] = (
        "2025-06-03", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 46, de 2025 (DOU 12.6.2025): 'teve seu prazo "
                      "de vigência encerrado no dia 2 de junho de 2025'; the wording it gave ends on 3.6.2025, the day Lei 15.141/2025 "
                      "(DOU 3.6.2025, in force on publication; its art. 217 XXXIX also revokes the Medida Provisória) gives the same "
                      "words")
    EXTRA.append("Lei 12.618: art. 33 ('Esta Lei entra em vigor: I - quanto ao disposto no Capítulo I, na data em que forem criadas "
                 "quaisquer das entidades de que trata o art. 4º, observado o disposto no art. 31; e II - quanto aos demais "
                 "dispositivos, na data de sua publicação'; DOU 2.5.2012). The first of those entities, the Fundação de Previdência "
                 "Complementar do Servidor Público Federal do Poder Executivo (Funpresp-Exe), was created by Decreto 7.808, de 20 de "
                 "setembro de 2012 (art. 1: 'Fica criada a Fundação de Previdência Complementar do Servidor Público Federal do Poder "
                 "Executivo - Funpresp-Exe'; art. 12: 'Este Decreto entra em vigor na data de sua publicação'; DOU 21.9.2012), the "
                 "act Planalto names on art. 33 I ('Vide Decreto nº 7.808, de 2012'), within art. 31's 180 days from publication. "
                 "Capítulo I (its heading and arts. 1 to 3) therefore starts on 21.9.2012, credited to Lei 12.618; the other provisions on "
                 "2.5.2012. The acts that created "
                 "the Funpresp-Jud and the Funpresp-Leg are not read; neither precedes the Decreto on Planalto's page.")
if any(a["slug"] == _L12865 for a in ACTS):
    P.VIGENCIA_FIXED["mp-627-2013"] = (
        "2013-11-12", "art. 98: 'Esta Medida Provisória entra em vigor em 1º de janeiro de 2015, exceto os arts. 67 a 71 e 92 a "
                      "100, que entram em vigor na data de sua publicação' (DOU 12.11.2013): its art. 92, the changes to Lei "
                      "12.865 arts. 39 and 40, in force on publication")
    P.VIGENCIA_FIXED["lei-12973-2014"] = (
        "2014-05-14", "art. 119: 'Esta Lei entra em vigor em 1º de janeiro de 2015, exceto os arts. 3º, 72 a 75 e 93 a 119, que "
                      "entram em vigor na data de sua publicação' (DOU 14.5.2014): its art. 93, the changes to Lei 12.865 arts. "
                      "17, 39 and 40, in force on publication")
    P.MP_LAPSE["mp-1227-2024"] = (
        "2024-06-04", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 36, de 2024 (DOU 12.6.2024): its art. 6, "
                      "whose inciso VIII revoked Lei 12.865 art. 31 § 6º and art. 32, rejected outright, 'considera não escritos "
                      "[...] e declara o encerramento da vigência e eficácia, desde a data de sua edição': the revocation never "
                      "took effect")
    _W1227 = ("Lei 12.865 art. 31 § 6º and art. 32: Planalto prints them unstruck under a struck note '(Revogado pela Medida "
              "Provisória nº 1.227, de 2024) (Vide Ato Declaratório nº 36, de 2024)' and the marker 'Vigência encerrada'; the "
              "revocation (Medida Provisória 1.227 art. 6 VIII) was rejected outright and declared without effect since the "
              "MP's edition (Ato Declaratório nº 36, de 2024), so these lines are the 2013 text, in force throughout")
    B8.SPAN_FIX += [((_L12865, _u, _l, _t, 0), {"start": "2013-10-10", "start_law": None, "end": None, "end_law": None,
                                                 "end_how": None, "skip": False}, _W1227)
                    for _u, _l, _t in (("art-31", "§ 6º", "§ 6º A pessoa jurídica que até o final de cada trimestre"),
                                       ("art-31", "I -", "I - efetuar sua compensação com débitos próprios"),
                                       ("art-31", "II -", "II - solicitar seu ressarcimento em espécie"),
                                       ("art-32", "Art. 32", "Art. 32. Os créditos presumidos de que trata o art. 31"),
                                       ("art-32", "Parágrafo único", "Parágrafo único. O procedimento específico de "
                                                                     "ressarcimento"))]
    EXTRA.append(_W1227 + ".")
    B.EXPLAINED[_L12865] = {"art-20": _DOTTED, "art-33": _DOTTED}
    _FUT2027[_L12865] = (
        {"art-29", "art-30", "art-31", "art-32"}, {},
        "Lei 12.865: Lei Complementar 214/2025 art. 542 ('Ficam revogados a partir de 1º de janeiro de 2027: [...] LIX - os arts. "
        "29 a 32 da Lei nº 12.865, de 9 de outubro de 2013'), in effect from 1.1.2027 (art. 544 III, as Lei Complementar "
        "227/2026 worded it), read on LC 214's page (Planalto's page of Lei 12.865 prints only '(Vide Lei Complementar nº 214, "
        "de 2025)'): arts. 29 to 32 end on 1.1.2027, on the future branch")
    # the law record as 99-batch14a/17zj/17zk have it (Planalto's page of Lei 12.865 names LC 214 only in a 'Vide' note)
    B8.EXTRA_LAWS["lc-214-2025"] = {
        "label": "Lei Complementar nº 214, de 2025", "title": "Institui o Imposto sobre Bens e Serviços (IBS), a Contribuição "
        "Social sobre Bens e Serviços (CBS) e o Imposto Seletivo (IS); cria o Comitê Gestor do IBS e altera a legislação "
        "tributária.", "kind": "law", "enacted": "2025-01-16", "published": "2025-01-16",
        "url": "https://www.planalto.gov.br/ccivil_03/leis/LCP/Lcp214.htm", "temporary_until": None, "restores": None,
        "note": None}
    EXTRA.append("Lei 12.865: art. 43 ('Esta Lei entra em vigor: I - a partir do primeiro dia do quarto mês subsequente ao de sua "
                 "publicação, em relação ao disposto no art. 34 desta Lei; II - na data de sua publicação, para os demais "
                 "dispositivos'; DOU 10.10.2013): art. 34 (its changes to Lei 12.350/2010 arts. 54 and 55) first shows on "
                 "1.2.2014, credited to Lei 12.865 (Planalto marks it with a 'Vigência' link); the other articles start on "
                 "10.10.2013.")
B13.OPEN_ITEMS[_L12865] = (
    "Lei 12.865 (open items): art. 40 (Lei 12.973's '(Vide)' pointer) and the regulations change no words and are not "
    "modelled; the text before 10.10.2013 (Medida Provisória 615/2013, of which this Lei is the conversion) is not part of the "
    "history")
B13.OPEN_ITEMS[_LFUNP] = (
    "Lei 12.618 (open items): 'Vide' pointers (Lei 13.328/2016 and Medida Provisória 1.119/2022 on art. 3 § 7º, the reopened "
    "option periods) change no words and are not modelled; the regulations strike no words")

# part zzr: Lei 10.848/2004 (comercialização de energia elétrica). Hand days set only when the act runs.
_LCEE = "lei-da-comercializacao-de-energia-eletrica"
if any(a["slug"] == _LCEE for a in ACTS):
    P.VIGENCIA_FIXED["mp-1300-2025"] = (
        "2025-05-21", "'Esta Medida Provisória entra em vigor: I - quarenta e cinco dias [...] quanto ao art. 6º; II - em 1º de "
                      "janeiro de 2026, quanto ao art. 8º; e III - na data de sua publicação, quanto aos demais dispositivos' (DOU "
                      "21.5.2025, edição extra): its art. 4 (Lei 10.848) falls under III")
    P.VIGENCIA_FIXED["lei-15235-2025"] = (
        "2025-10-09", "'Esta Lei entra em vigor: I - em 1º de janeiro de 2026, quanto ao inciso III do caput do art. 5º; e II - "
                      "na data de sua publicação, quanto aos demais dispositivos' (DOU 9.10.2025): the conversion of Medida "
                      "Provisória 1.300/2025, which keeps none of the MP's art. 4 (its changes to Lei 10.848), takes effect on "
                      "publication, so those changes end on 9.10.2025 and the wordings they replaced are back")
    P.MP_LAPSE["mp-641-2014"] = (
        "2014-07-22", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 30, de 2014 (DOU 24.7.2014): Medida "
                      "Provisória 641/2014 'teve seu prazo de vigência encerrado no dia 21 de julho do corrente ano'; the wording "
                      "it replaced is back from 22.7.2014")
    P.MP_LAPSE["mp-814-2017"] = (
        "2018-06-02", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 30, de 2018 (DOU 6.6.2018): Medida "
                      "Provisória 814/2017 'teve seu prazo de vigência encerrado no dia 1º de junho do corrente ano'; the "
                      "provision it had revoked is back from 2.6.2018")
    B.EXPLAINED[_LCEE] = {
        "art-10": _DOTTED, "art-11": _DOTTED, "art-13": _DOTTED,
    }
    B13.OPEN_ITEMS[_LCEE] = (
        "Lei 10.848 (open items): the text before 16.3.2004 (Medida Provisória 144/2003, of which this Lei is the conversion) "
        "is not part of the history; 'Vide' pointers and regulations strike no words and are not modelled")
# page l10848: art. 3º-D (Lei 15.269/2025 art. 9) is printed as its label only; its text is read from Lei 15.269's page
# (the quoted article in art. 9, from '"Art. 3º-D. A contratação' to the line before '"Art. 3º-E.')
L3D_READ: list[str] = []
_paragraphsLCEE = P.paragraphs


def html_text(raw: bytes) -> str:
    import html as _h
    return _h.unescape(re.sub(r"<[^>]+>", " ", P.decode(raw)))


def paragraphs(html, digits):
    out, rest = _paragraphsLCEE(html, digits)
    if B8.CURRENT_PAGE[0] == "l10848":
        at = [i for i, p in enumerate(out) if p["label"] == "Art. 3º-D" and p["text"] == "Art. 3º-D." and not p["heading"]]
        assert len(at) == 1, at
        page = B8.CURRENT_PAGE[0]
        src, _ = _paragraphsLCEE(P.decode(P.raw("law:lei-15269-2025")[0]), digits)
        B8.CURRENT_PAGE[0] = page
        i = [k for k, q in enumerate(src) if q["text"].startswith('"Art. 3º-D. A contratação')]
        j = [k for k, q in enumerate(src) if q["text"].startswith('"Art. 3º-E.')]
        assert len(i) == 1 and len(j) == 1 and i[0] < j[0], (i, j)
        lines = [q["text"] for q in src[i[0]:j[0]]]
        assert len({q["unit"] for q in src[i[0]:j[0]]}) == 1 and all(q["state"] == "plain" and not q["notes"]
                                                                     for q in src[i[0]:j[0]])
        lines[0] = lines[0][1:]
        lines[-1] = lines[-1].rstrip('"').rstrip()
        assert not any('"' in x for x in lines), lines
        tmpl = out[at[0]]
        new = [{**tmpl, "text": x, "label": (tmpl["label"] if k == 0 else q["label"]), "notes": list(tmpl["notes"])}
               for k, (x, q) in enumerate(zip(lines, src[i[0]:j[0]]))]
        out[at[0]:at[0] + 1] = new
        L3D_READ.append(str(len(new)))
        # art. 2 § 6º: Planalto prints only Lei 11.943/2009's wording of the caput; the 2004 wording is read from the
        # Chamber's copy of the original publication and set above it, struck (ended by Lei 11.943's)
        k6 = [i for i, p in enumerate(out) if p["label"] == "§ 6º" and not p["heading"]
              and p["text"].startswith("§ 6º Entendem-se como novos empreendimentos de geração aqueles que até o início de "
                                       "processo público licitatório")]
        assert len(k6) == 1 and out[k6[0]]["notes"] == ["(Redação dada pela Lei nº 11.943, de 2009)"], k6
        ref = re.sub(r"\s+", " ", html_text(P.raw("ctx:camara-lei-10848-2004-original")[0]))
        w6 = ("§ 6º Entendem-se como novos empreendimentos de geração aqueles que até o início do processo licitatório para a "
              "expansão em curso:")
        assert w6 in ref and w6 + " I - não sejam detentores de outorga" in ref
        out.insert(k6[0], {**out[k6[0]], "text": w6, "state": "struck", "notes": []})
        L3D_READ.append("art-02 § 6º 2004")
    return out, rest


P.paragraphs = B.paragraphs = paragraphs
if any(a["slug"] == _LCEE for a in ACTS):
    EXTRA.append("Lei 10.848 art. 3º-D: Planalto's page prints the article as its label only ('Art. 3º-D.', 'Incluído pela Lei nº "
                 "15.269, de 2025', 'Produção de efeitos'); its text (caput, incisos I-II, §§ 1º-5º) is read from Lei 15.269/2025's "
                 "own page (art. 9, the quoted article; the check page is read the same way), credited to Lei 15.269; it takes effect 90 days after publication "
                 "(art. 24 II: 'em 90 (noventa) dias da data de sua publicação, quanto ao art. 9º, na parte que inclui o art. "
                 "3º-D'; DOU 25.11.2025), 23.2.2026 (effects_fix). Art. 2 § 6º: Planalto prints only Lei 11.943/2009's "
                 "wording of the caput ('Redação dada'), not the one it replaced; the 2004 wording ('... aqueles que até o "
                 "início do processo licitatório para a expansão em curso:') is read from the Chamber of Deputies' copy of the "
                 "original publication (DOU 16.3.2004) and stands until 29.5.2009.")
    B6.CONTEXT.append({
        "when": lambda: any("2004" in x for x in L3D_READ),
        "pins": ["ctx:camara-lei-10848-2004-original"],
        "what": "the original publication of Lei 10.848/2004 (DOU 16.3.2004), for the 2004 wording of art. 2 § 6º, which "
                "Planalto's page does not print"})

# A Medida Provisória's wording that its conversion law does not keep: Planalto prints, after the MP's (struck) wording, the
# wording the MP replaced a second time, struck, and then the wording of a later law. The reader ends the MP's wording at that
# later law (the repeated copy is its successor) and gives the copy no days. Rule (acts in CONV_RESTORE, with the MP and its
# conversion law read and named): the MP's wording ends on the conversion law's in-force day, and the copy (same words as the
# wording before the MP's) stands from that day to the later law. Checked against the hand entries of parts z (Lei 9.427)
# and u (Lei 9.074): BATCH17_CONV_REPORT=1 prints, for any act, every place the rule finds and the days it would give.
CONV_RESTORE: dict[str, dict[str, str]] = {_LCEE: {"mp-1300-2025": "lei-15235-2025"}, _L9074: {"mp-1300-2025": "lei-15235-2025"}}
_WCONV = ("Wordings of a Medida Provisória its conversion law did not keep (rule, not hand dates): where Planalto prints, "
          "after the MP's struck wording, the wording the MP replaced a second time, struck, before a later law's wording, the "
          "MP's wording ends on the conversion law's in-force day and the earlier wording is in force again from that day "
          "until the later law; here Medida Provisória 1.300/2025, converted into Lei 15.235/2025 (in force on publication, "
          "9.10.2025), which keeps none of the MP's changes to this Lei (its art. 4 for Lei 10.848, its art. 1 for Lei 9.074)")
CONV_RESTORED: list[str] = []
_lifespans17r = P.lifespans


def _conv_restore(paras, cx):
    """(MP line, copy line, line before the MP's, conversion day, conversion law) for each place the rule finds."""
    out = []
    for i, m in enumerate(paras):
        if m["heading"] or m["state"] == "plain" or m.get("skip") or not (m["start_law"] or "").startswith("mp-"):
            continue
        fate = cx.mp.get(m["start_law"]) or {}
        c_day, c_law = fate.get("converted_on"), fate.get("converted")
        a, r = P.predecessor(paras, i), P.successor(paras, i)
        if not c_day or a is None or r is None:
            continue
        A, R = paras[a], paras[r]
        if R["state"] == "plain" or R.get("skip") or R["text"] != A["text"] or not R.get("end") or not c_day < R["end"]:
            continue
        out.append((m, R, A, c_day, c_law))
    return out


def lifespans(paras, cx):
    problems = _lifespans17r(paras, cx)
    if os.environ.get("BATCH17_CONV_REPORT"):
        for m, R, A, c_day, c_law in _conv_restore(paras, cx):
            print(f"CONV-RULE {cx.act} {m['unit']} [{m['label']}] MP {m['start']}..{m['end']} ({m['end_law']}, "
                  f"{m['end_how']}) copy {R['start']}..{R['end']} ({R['start_law']}) | rule: MP ..{c_day} ({c_law}), copy "
                  f"{c_day}..{R['end']} | pinned {bool(m.get('pinned'))}/{bool(R.get('pinned'))}", file=sys.stderr)
    want = CONV_RESTORE.get(cx.act)
    if want:
        found = _conv_restore(paras, cx)
        assert {m["start_law"] for m, *_ in found} <= set(want), found
        for m, R, A, c_day, c_law in found:
            assert want[m["start_law"]] == c_law and A.get("end") == m["start"], (m, A)
            for p, fields in ((m, {"end": c_day, "end_law": c_law, "end_how": "conversion"}),
                              (R, {"start": c_day, "start_law": c_law, "restored": True})):
                hits = [q for q in paras if q["unit"] == p["unit"] and q["label"] == p["label"] and not q["heading"]
                        and B8._norm(q["text"]).startswith(B8._norm(p["text"]))]
                p.update(fields)
                p["pinned"] = True
                B8.SPAN_FIX.append(((cx.act, p["unit"], p["label"], p["text"], hits.index(p)), fields,
                                    "the conversion rule (CONV_RESTORE)"))
            CONV_RESTORED.append(f"{m['unit']} [{m['label']}]")
            key = f"ends before it starts: {R['unit']} [{R['label']}] "
            problems = [x for x in problems if not x.startswith(key)]
        if found:
            EXTRA.append(_WCONV + ": " + "; ".join(f"{m['unit']} [{m['label']}] ({m['start_law']}, ends {c_day}, "
                                                      f"{c_law}; the earlier wording again until {R['end']}, {R['end_law']})"
                                                      for m, R, A, c_day, c_law in found) + ".")
    return problems


P.lifespans = B.lifespans = lifespans

P.build_act = B.build_act = build_act
_build_actLP = build_act


def build_act_lp(paras, act_day, gate, gate_law, unit_label):
    """Lei 12.351: the ADI 4.917 ruling as a version of 18.3.2013 that changes no words (as 99-batch10 records it for the Lei
    do Petróleo)."""
    slug = ACTS[len(B7._act_order)]["slug"] if len(B7._act_order) < len(ACTS) else "?"
    versions = _build_actLP(paras, act_day, gate, gate_law, unit_label)
    if slug == _LPART:
        day = B10.ADI4917_DAY
        before = [v for v in versions if v["from"] <= day]
        assert before and before[-1]["from"] < day and not any(v["from"] == day for v in versions)
        units = before[-1]["units"]
        cred = {u: ["stf-adi-4917"] for u in ("art-42-b", "art-42-c") if u in units}
        assert len(cred) == 2
        versions.insert(len(before), {"from": day, "source_url": before[-1].get("source_url"),
                                      "sha256": before[-1].get("sha256"), "units": units, "credits": cred})
        EXTRA.append(_ADI4917_12351 + ".")
    return versions


P.build_act = B.build_act = build_act_lp
_build_actFP = build_act_lp
L12618_HEAD: list[str] = []


def build_act_fp(paras, act_day, gate, gate_law, unit_label):
    """Lei 12.618: the heading of Capítulo I ('CAPÍTULO I' and its name line) starts with the chapter (art. 33 I), on
    21.9.2012, credited to the Lei, like arts. 1 to 3 (_G12618)."""
    slug = ACTS[len(B7._act_order)]["slug"] if len(B7._act_order) < len(ACTS) else "?"
    if slug == _LFUNP:
        for p in paras:
            if (p["unit"] == "titulos" and p["text"] in ("CAPÍTULO I", "DO REGIME DE PREVIDÊNCIA COMPLEMENTAR")
                    and p["start"] == act_day and not p.get("skip") and p["end"] is None):
                p["start"], p["start_law"] = _G12618["art-01"][0], "lei-12618-2012"
                L12618_HEAD.append(p["text"])
        assert len(L12618_HEAD) == 2, L12618_HEAD
    return _build_actFP(paras, act_day, gate, gate_law, unit_label)


P.build_act = B.build_act = build_act_fp

SRC = HERE / "sources_batch17.json"
if not SRC.exists():
    SRC.write_text('{\n "fetch": []\n}\n', encoding="utf-8", newline="\n")
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
