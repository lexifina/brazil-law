"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch10.json (SCHEMA.md corpus part): the acts in ALL_ACTS
below (more federal laws, as they are verified).

    python -X utf8 scripts/brazil-law/batch10/parse_batch10.py [--stats] [--dry]

Imports ../batch9/parse_batch9.py (which configures batch 8 and everything below it, plus batch 9's hand tools:
REPEALS, FOLD_EARLY, NOTE_INTO_TEXT, WORD_FIX) with no act of its own, and replaces only the configuration: the acts,
the in-force days, the hand tables for these acts, the pins and the output. Earlier parts are not touched. No network.

BATCH10_ACTS=<slug,...> selects acts for trial runs (BATCH10_OUT=<file> writes elsewhere); by default VERIFIED is
written.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH9_ACTS"] = "-"   # batch 9 configures no act of its own here
os.environ.pop("BATCH9_OUT", None)
sys.path.insert(0, str(FOLDER / "batch9"))
import parse_batch9 as B9  # noqa: E402

B8, B7, B6, B5, B, P = B9.B8, B9.B7, B9.B6, B9.B5, B9.B, B9.P
PL = P.PL
B5.OUT = Path(os.environ.get("BATCH10_OUT") or FOLDER / "corpus.d" / "99-batch10.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = {
    "lconc": "leis/l8987cons.htm",
    "lconc-compilada": "leis/l8987compilada.htm",
    "lppp": "_ato2004-2006/2004/lei/l11079.htm",
    "lppp-compilado": "_ato2004-2006/2004/lei/l11079compilado.htm",
    "lsan": "_ato2007-2010/2007/lei/l11445.htm",
    "lsan-compilado": "_ato2007-2010/2007/lei/l11445compilado.htm",
    "lpet": "leis/l9478.htm",
    "lpet-compilado": "leis/l9478compilado.htm",
    "labus": "_ato2019-2022/2019/lei/l13869.htm",
    "labus-compilado": "_ato2019-2022/2019/lei/l13869compilado.htm",
    "emil": "leis/l6880.htm",
    "emil-compilada": "leis/l6880compilada.htm",
    "linel": "leis/lcp/lcp64.htm",
    "linel-compilado": "leis/lcp/lcp64compilado.htm",
    "l8142": "leis/l8142.htm",
    "lgesp": "_ato2023-2026/2023/lei/l14597.htm",
    "etorc": "leis/2003/l10.671.htm",
    "etorc-2023": "leis/2003/l10.671.htm",
    "etorc-compilado": "leis/2003/l10.671compilado.htm",
    "pnma": "leis/l6938.htm",
    "pnma-compilada": "leis/l6938compilada.htm",
}
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = B6.PAGES = B7.PAGES = B8.PAGES = B9.PAGES = PAGES


def _act(slug, short, page, consolidated, law, title, digits):
    return {"slug": slug, "short": short, "page": page, "consolidated": consolidated, "law": law, "title": title,
            "digits": digits, "url": PL + PAGES[page]}


ALL_ACTS: list[dict] = [
    _act("lei-de-concessoes", "LConc", "lconc", "lconc-compilada", "lei-8987-1995",
         "Lei de Concessões (Lei nº 8.987, de 13 de fevereiro de 1995)", 2),
    _act("lei-das-parcerias-publico-privadas", "LPPP", "lppp", "lppp-compilado", "lei-11079-2004",
         "Lei das Parcerias Público-Privadas (Lei nº 11.079, de 30 de dezembro de 2004)", 2),
    _act("lei-do-saneamento-basico", "LSB", "lsan", "lsan-compilado", "lei-11445-2007",
         "Lei do Saneamento Básico (Lei nº 11.445, de 5 de janeiro de 2007)", 2),
    _act("lei-do-petroleo", "LPet", "lpet", "lpet-compilado", "lei-9478-1997",
         "Lei do Petróleo (Lei nº 9.478, de 6 de agosto de 1997)", 2),
    _act("lei-de-abuso-de-autoridade", "LAA", "labus", "labus-compilado", "lei-13869-2019",
         "Lei de Abuso de Autoridade (Lei nº 13.869, de 5 de setembro de 2019)", 2),
    _act("estatuto-dos-militares", "EMil", "emil", "emil-compilada", "lei-6880-1980",
         "Estatuto dos Militares (Lei nº 6.880, de 9 de dezembro de 1980)", 3),
    _act("lei-das-inelegibilidades", "LInel", "linel", "linel-compilado", "lcp-64-1990",
         "Lei das Inelegibilidades (Lei Complementar nº 64, de 18 de maio de 1990)", 2),
    _act("lei-8142-de-1990", "L8142", "l8142", "l8142", "lei-8142-1990",
         "Participação da comunidade e financiamento do SUS (Lei nº 8.142, de 28 de dezembro de 1990)", 2),
    _act("lei-geral-do-esporte", "LGE", "lgesp", "lgesp", "lei-14597-2023",
         "Lei Geral do Esporte (Lei nº 14.597, de 14 de junho de 2023)", 3),
    _act("estatuto-do-torcedor", "ETor", "etorc-2023", "etorc-2023", "lei-10671-2003",
         "Estatuto de Defesa do Torcedor (Lei nº 10.671, de 15 de maio de 2003)", 2),
    _act("politica-nacional-do-meio-ambiente", "PNMA", "pnma", "pnma-compilada", "lei-6938-1981",
         "Política Nacional do Meio Ambiente (Lei nº 6.938, de 31 de agosto de 1981)", 2),
]
VERIFIED: list[str] = ["lei-de-concessoes", "lei-das-parcerias-publico-privadas", "lei-de-abuso-de-autoridade",
                        "lei-das-inelegibilidades", "lei-8142-de-1990", "lei-geral-do-esporte",
                        "estatuto-dos-militares", "estatuto-do-torcedor", "lei-do-saneamento-basico",
                        "politica-nacional-do-meio-ambiente", "lei-do-petroleo"]
ENABLED = [s for s in os.environ.get("BATCH10_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
B7.ACTS[:] = ACTS
B8.ACTS[:] = ACTS
B9.ACTS[:] = ACTS

# in-force day of each act as enacted, and its own law record (filled from each page as it is read)
_PUB = "'Esta Lei entra em vigor na data de sua publicação'"
ACT_DAY_ALL: dict[str, tuple[str, str]] = {
    "lei-8987-1995": ("1995-02-14", f"Lei 8.987/1995 art. 46: {_PUB} (DOU 14.2.1995)"),
    "lei-11079-2004": ("2004-12-31", f"Lei 11.079/2004 art. 30: {_PUB} (DOU 31.12.2004)"),
    "lei-11445-2007": ("2007-02-22", "Lei 11.445/2007 has no vigência clause (its art. 59 was vetoed; art. 60 revokes Lei "
                                     "6.528/1978): LINDB art. 1, 45 days after publication in the DOU of 8.1.2007"),
    "lei-9478-1997": ("1997-08-07", f"Lei 9.478/1997 art. 82: {_PUB} (DOU 7.8.1997)"),
    "lei-13869-2019": ("2020-01-03", "Lei 13.869/2019 art. 45: 'Esta Lei entra em vigor após decorridos 120 (cento e vinte) "
                                     "dias de sua publicação oficial' (DOU 5.9.2019, edição extra): the 120th day counted "
                                     "from publication is 2.1.2020 (LC 95/1998 art. 8 § 1)"),
    "lei-6880-1980": ("1981-01-01", "Lei 6.880/1980 art. 159: 'O presente Estatuto entrará em vigor a partir de 1º de "
                                    "janeiro de 1981, salvo quanto ao disposto no item IV do artigo 98, que terá vigência 1 "
                                    "(um) ano após a data da publicação desta Lei' (DOU 11.12.1980)"),
    "lcp-64-1990": ("1990-05-21", "Lei Complementar 64/1990 art. 27: 'Esta lei complementar entra em vigor na data de sua "
                                  "publicação' (DOU 21.5.1990)"),
    "lei-8142-1990": ("1990-12-31", "Lei 8.142/1990 art. 6: 'Esta lei entra em vigor na data de sua publicação' (DOU "
                                    "31.12.1990)"),
    "lei-14597-2023": ("2023-06-15", f"Lei 14.597/2023 art. 218: {_PUB} (DOU 15.6.2023)"),
    "lei-10671-2003": ("2003-05-16", f"Lei 10.671/2003 art. 45: {_PUB} (DOU 16.5.2003)"),
    "lei-6938-1981": ("1981-09-02", "Lei 6.938/1981 art. 20: 'Esta Lei entrará em vigor na data de sua publicação' (DOU "
                                    "2.9.1981)"),
}
ACT_LAWS_ALL: dict[str, dict] = {
    "lei-8987-1995": B._act_law("Lei nº 8.987, de 1995", "Dispõe sobre o regime de concessão e permissão da prestação de "
                                "serviços públicos previsto no art. 175 da Constituição Federal, e dá outras providências.",
                                "1995-02-13", "1995-02-14", PAGES["lconc"]),
    "lei-11079-2004": B._act_law("Lei nº 11.079, de 2004", "Institui normas gerais para licitação e contratação de parceria "
                                 "público-privada no âmbito da administração pública.", "2004-12-30", "2004-12-31",
                                 PAGES["lppp"]),
    "lei-11445-2007": B._act_law("Lei nº 11.445, de 2007", "Estabelece diretrizes nacionais para o saneamento básico; altera "
                                 "as Leis nos 6.766, de 19 de dezembro de 1979, 8.036, de 11 de maio de 1990, 8.666, de 21 "
                                 "de junho de 1993, 8.987, de 13 de fevereiro de 1995; revoga a Lei no 6.528, de 11 de maio "
                                 "de 1978; e dá outras providências.", "2007-01-05", "2007-01-08", PAGES["lsan"]),
    "lei-9478-1997": B._act_law("Lei nº 9.478, de 1997", "Dispõe sobre a política energética nacional, as atividades "
                                "relativas ao monopólio do petróleo, institui o Conselho Nacional de Política Energética e "
                                "a Agência Nacional do Petróleo e dá outras providências.", "1997-08-06", "1997-08-07",
                                PAGES["lpet"]),
    "lei-13869-2019": B._act_law("Lei nº 13.869, de 2019", "Dispõe sobre os crimes de abuso de autoridade; altera a Lei nº "
                                 "7.960, de 21 de dezembro de 1989, a Lei nº 9.296, de 24 de julho de 1996, a Lei nº 8.069, "
                                 "de 13 de julho de 1990, e a Lei nº 8.906, de 4 de julho de 1994; e revoga a Lei nº 4.898, "
                                 "de 9 de dezembro de 1965, e dispositivos do Decreto-Lei nº 2.848, de 7 de dezembro de 1940 "
                                 "(Código Penal).", "2019-09-05", "2019-09-05", PAGES["labus"]),
    "lei-6880-1980": B._act_law("Lei nº 6.880, de 1980", "Dispõe sobre o Estatuto dos Militares.", "1980-12-09",
                                "1980-12-11", PAGES["emil"]),
    "lcp-64-1990": B._act_law("Lei Complementar nº 64, de 1990", "Estabelece, de acordo com o art. 14, § 9º da Constituição "
                              "Federal, casos de inelegibilidade, prazos de cessação, e determina outras providências.",
                              "1990-05-18", "1990-05-21", PAGES["linel"]),
    "lei-8142-1990": B._act_law("Lei nº 8.142, de 1990", "Dispõe sobre a participação da comunidade na gestão do Sistema "
                                "Único de Saúde (SUS) e sobre as transferências intergovernamentais de recursos financeiros "
                                "na área da saúde e dá outras providências.", "1990-12-28", "1990-12-31", PAGES["l8142"]),
    "lei-14597-2023": B._act_law("Lei nº 14.597, de 2023", "Institui a Lei Geral do Esporte.", "2023-06-14", "2023-06-15",
                                 PAGES["lgesp"]),
    "lei-10671-2003": B._act_law("Lei nº 10.671, de 2003", "Dispõe sobre o Estatuto de Defesa do Torcedor e dá outras "
                                 "providências.", "2003-05-15", "2003-05-16", PAGES["etorc"]),
    "lei-6938-1981": B._act_law("Lei nº 6.938, de 1981", "Dispõe sobre a Política Nacional do Meio Ambiente, seus fins e "
                                "mecanismos de formulação e aplicação, e dá outras providências.", "1981-08-31",
                                "1981-09-02", PAGES["pnma"]),
}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# batch 9's hand tools, emptied for these acts (the law facts in VIGENCIA_FIXED, MP_LAPSE, ... are kept: they hold for
# every act and are printed in decisions only where a version uses them)
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
P.PUBLISHED_FIXED.pop("mp-75-2002", None)   # batch 9's (Código de Trânsito); every entry left there is printed

# ---------------------------------------------------------------------------------------------------------------
# hand tables for these acts, each read from the official pages named in the reason
B7.CONVERTED_FIX.update({
    "mp-577-2012": ("lei-12767-2012", "the MP page reads 'Convertida pela Lei nº 12.767, de 2012' ('pela' for 'na'), "
                                      "Lei nº 12.767, de 27.12.2012"),
})
_W27 = ("Lei de Concessões art. 27: Lei 11.196/2005 (in force 22.11.2005) renumbered the Parágrafo único as § 1º and "
        "added §§ 2º to 4º; Planalto prints the struck Parágrafo único with its incisos I and II and then the § 1º with "
        "the same incisos, unstruck and with no note, so these start with the renumbering, when the struck copies end")
B8.SPAN_FIX[:] = [
    (("lei-de-concessoes", "art-27", "I -", "I - atender às exigências", 1),
     {"start": "2005-11-22", "start_law": "lei-11196-2005"}, _W27),
    (("lei-de-concessoes", "art-27", "II -", "II - comprometer-se", 1),
     {"start": "2005-11-22", "start_law": "lei-11196-2005"}, _W27),
    (("lei-geral-do-esporte", "art-099", "IV -", "", 0), {"skip": True},
     "Lei Geral do Esporte art. 99 § 1º IV: Planalto prints a bare label line 'IV - (Vide Lei nº 15.522, de 2026)' where "
     "Lei 15.522/2026 rewords the inciso 180 days after its publication (DOU 29.9.2026; its art. 11), a day after the "
     "data's retrieval; the label line is left out and that future wording, which Planalto's page does not print, is "
     "not in the history"),
]
B7.CONVERTED_FIX["mp-575-2012"] = ("lei-12766-2012", "the MP page reads 'Convertida pela Lei nº 12.766, de 2012' ('pela' "
                                                    "for 'na'), Lei nº 12.766, de 27.12.2012")
P.VIGENCIA_FIXED.update({
    "lei-13137-2015": ("2015-06-22", "art. 26 VII: the provisions not named in its incisos I to VI, which include art. 3 "
                                     "(the changes to Lei 11.079/2004), in force 'na data de sua publicação' (DOU 22.6.2015, "
                                     "edição extra)"),
})
P.VIGENCIA_FIXED["lei-11447-2007"] = ("2007-01-08", "art. 3: 'Esta Lei entra em vigor a partir da data de sua publicação' "
                                                    "(DOU 8.1.2007)")
P.MP_PENDING.update({
    "mp-2215-2001": "Medida Provisória nº 2.215-10, de 31.8.2001 (DOU 1.9.2001) was in force on 11.9.2001, so it stays in "
                    "force until a later MP revokes it or Congress votes on it (Emenda Constitucional 32/2001, art. 2)",
})
P.MP_LAPSE.update({
    "mp-592-2012": ("2013-05-13", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 31, de 2013 (DOU "
                                  "3.6.2013): 'teve seu prazo de vigência encerrado no dia 12 de maio do corrente ano'"),
    "mp-844-2018": ("2018-11-20", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 70, de 2018 (DOU "
                                  "21.11.2018): 'teve seu prazo de vigência encerrado no dia 19 de novembro do corrente "
                                  "ano'"),
    "mp-868-2018": ("2019-06-04", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 36, de 2019 (DOU "
                                  "5.6.2019): 'teve seu prazo de vigência encerrado no dia 3 de junho do corrente ano'"),
})
B7.CONVERTED_FIX["mp-532-2011"] = ("lei-12490-2011", "the MP page reads 'Convertida pela Lei nº 12.490, de 2011' ('pela' for "
                                                    "'na'), Lei nº 12.490, de 16.9.2011")
P.VIGENCIA_FIXED.update({
    "lc-225-2026": ("2026-01-09", "art. 58 II: in force 'na data de sua publicação' (DOU 9.1.2026) for every provision but "
                                  "the programmes and seals of its own arts. 19 to 32 and 40 to 47 (art. 58 I, 90 days)"),
    "mp-844-2018": ("2018-07-09", "art. 8 II: in force 'na data de sua publicação' (DOU 9.7.2018) for every provision but "
                                  "the art. 10-A it adds to Lei 11.445/2007 (art. 8 I: three years after publication; the MP "
                                  "lapsed on 20.11.2018, so that art. 10-A never took effect)"),
    "mp-868-2018": ("2018-12-28", "art. 9 II: in force 'na data de sua publicação' (DOU 28.12.2018) for every provision but "
                                  "the art. 10-C it adds to Lei 11.445/2007 (art. 9 I: twelve months after publication; the "
                                  "MP lapsed on 4.6.2019, so that art. 10-C never took effect)"),
    "lei-13312-2016": ("2021-07-13", "art. 3: 'Esta Lei entra em vigor após decorridos cinco anos de sua publicação oficial' "
                                     "(DOU 12.7.2016, edição extra): the period ends on 12.7.2021 and the law is in force the "
                                     "day after (LC 95/1998 art. 8 § 1)"),
    "lei-15082-2024": ("2024-12-31", "art. 4 II: in force 'na data de sua publicação' (DOU 31.12.2024) for every provision "
                                     "but the §§ 5º and 6º of art. 7º and art. 9º-B it adds to Lei 13.576/2017 (art. 4 I, "
                                     "90 days)"),
})
P.NOTE_FIX.update({
    "(Redação dada pela Lei nº 9.990, 2000)": (
        "(Redação dada pela Lei nº 9.990, de 2000)",
        "Lei do Petróleo: a note reads 'Lei nº 9.990, 2000' (no 'de'); Lei nº 9.990, de 21.7.2000"),
})
P.NOTE_FIX.update({
    "(Redação dada pela Medida provisória nº 513, de 2.010)": (
        "(Redação dada pela Medida Provisória nº 513, de 2010)",
        "Lei das PPPs: notes read 'Medida provisória nº 513, de 2.010'; Medida Provisória nº 513, de 26.11.2010"),
    "(Incluído pela Medida provisória nº 513, de 2.010)": (
        "(Incluído pela Medida Provisória nº 513, de 2010)", "as the 'Redação dada' notes of MP 513/2010"),
})
_E = "estatuto-dos-militares"
SAN_ACT = "lei-do-saneamento-basico"
B8.LABEL_FIX[:] = [
    ("emil", "lll - os da reserva remunerada", "III - os da reserva remunerada", "III -",
     "Estatuto dos Militares art. 3 § 1º b) III in Lei 9.442/1997's wording is printed with the letter l for the numeral "
     "('lll -'); read as III"),
    ("emil", "u§ 2º O oficial na inatividade", "§ 2º O oficial na inatividade", "§ 2º",
     "Estatuto dos Militares art. 77 § 2º is printed with a stray 'u' before the '§'; the consolidated page has none"),
    ("emil", "u § 2º O oficial na inatividade", "§ 2º O oficial na inatividade", "§ 2º", "as the line above"),
]
B8.SPAN_FIX += [
    ((_E, "art-003", "II -", "II - os reformados", 0), {"keep": True},
     "Estatuto dos Militares art. 3 § 1º b) II ('os reformados ...') is printed once, unstruck and with no note, under "
     "alínea b), below the struck a) II; it is the act's own wording, in force throughout (the twin-wording rule, which "
     "would take it for a copy of a) II, does not apply)"),
    ((_E, "art-098", "IV -", "IV - ultrapassar o oficial 5 (cinco) anos", 0),
     {"start": "1981-12-11", "start_law": "lei-6880-1980"},
     "Estatuto dos Militares art. 98 IV: art. 159 gives it 'vigência 1 (um) ano após a data da publicação desta Lei' "
     "(DOU 11.12.1980), the rest of the act being in force from 1.1.1981; it enters the history on 11.12.1981, "
     "credited to Lei 6.880/1980"),
]
B8.SPAN_FIX += [
    (("estatuto-do-torcedor", "art-13", "Parágrafo único", "", 0), {"start": "2003-11-17", "start_law": "lei-10671-2003"},
     "Estatuto do Torcedor art. 13 parágrafo único and arts. 18, 22, 25 and 33: art. 44 puts them in force 'após seis "
     "meses da publicação desta Lei' (DOU 16.5.2003), so they enter the history on 17.11.2003, credited to Lei 10.671/2003"),
]
_LP = "lei-do-petroleo"
_W68 = ("Lei do Petróleo arts. 68-B and 68-C: Medida Provisória nº 1.063/2021 inserted them; Medida Provisória nº 1.069/2021 "
        "(13.9.2021) reworded art. 68-B caput and art. 68-C I; Lei 14.292/2022, the conversion of MP 1.063 (in force "
        "4.1.2022), gives both articles as '(VETADO)', so MP 1.069's wordings end with it (MP 1.069 itself was revoked by "
        "MP 1.100/2022, converted into Lei 14.367/2022). Planalto prints MP 1.069's wordings unstruck above the '(VETADO)' "
        "lines, and its consolidated page keeps them as today's text; the history follows Lei 14.292")
B8.SPAN_FIX += [
    ((_LP, "art-68-b", "Art. 68-B", "Art. 68-B. Sem prejuízo das demais hipóteses previstas na regulação, o agente produtor, a "
                                    "cooperativa", 0),
     {"end": "2022-01-04", "end_law": "lei-14292-2022", "end_how": "successor"}, _W68),
    ((_LP, "art-68-c", "I -", "I - agente produtor, cooperativa", 0),
     {"end": "2022-01-04", "end_law": "lei-14292-2022", "end_how": "successor"}, _W68),
]
P.MP_PENDING.update({
    "mp-1069-2021": "Medida Provisória nº 1.069, de 13.9.2021: revoked by Medida Provisória nº 1.100, de 14.2.2022 (art. 4), "
                    "converted into Lei 14.367/2022; its wordings of the Lei do Petróleo had ended earlier, with Lei "
                    "14.292/2022 (see the life-span decisions)",
    "mp-1255-2024": "Medida Provisória nº 1.255, de 26.8.2024: 'Revogada pela Lei nº 15.075, de 2024' on its page; its "
                    "wordings of the Lei do Petróleo end with Lei 15.075/2024, which gave those provisions their wording",
})
# STF, ADI 4.917: the rapporteur's cautelar of 18.3.2013 (DJe 21.3.2013), 'suspender os efeitos dos arts. 42-B; 42-C; 48,
# II; 49, II; 49-A; 49-B; 49-C; § 2º do art. 50; 50-A; 50-B; 50-C; 50-D; e 50-E da Lei Federal n. 9.478/97, com as
# alterações promovidas pela Lei n. 12.734/2012, ad referendum do Plenário [...] até o julgamento final' (the case's
# andamentos, archived copy pinned as ctx:stf-adi-4917-andamentos); the Plenário had not ruled when the data was read.
# Planalto keeps the 2012 wordings in its annotated page, each with '(Vide ADI 4917)', so the wording is not changed:
# the ruling is a no-words event credited to the provisions it names.
ADI4917_DAY = "2013-03-18"
ADI4917_UNITS = ["art-48", "art-49", "art-49-a", "art-49-b", "art-49-c", "art-50", "art-50-a", "art-50-b", "art-50-c",
                 "art-50-d", "art-50-e"]
B8.EXTRA_LAWS["stf-adi-4917"] = {
    "label": "STF, ADI 4.917 (medida cautelar)", "kind": "court", "enacted": ADI4917_DAY, "published": "2013-03-21",
    "title": "Ação direta de inconstitucionalidade 4.917, medida cautelar (decisão monocrática, ad referendum do Plenário): "
             "suspende os efeitos dos arts. 42-B, 42-C, 48, II, 49, II, 49-A, 49-B, 49-C, § 2º do art. 50, 50-A, 50-B, "
             "50-C, 50-D e 50-E da Lei nº 9.478, de 1997, com as alterações promovidas pela Lei nº 12.734, de 2012",
    "url": "https://portal.stf.jus.br/processos/detalhe.asp?incidente=4379376", "temporary_until": None,
    "restores": None,
    "note": "A rapporteur's interim ruling (ADI 4.917, 18 March 2013) suspended the effects of the royalty rules Lei "
            "12.734/2012 wrote into these provisions until the court's final judgment; the words are unchanged on "
            "Planalto's page, so they are unchanged here."}
ADI4917_WHY = ("Lei do Petróleo: STF, ADI 4.917, medida cautelar of 18.3.2013 (Min. Cármen Lúcia, ad referendum; DJe "
               "21.3.2013; read from the case's record of proceedings) suspended the effects of arts. 48 II, 49 II, 49-A to "
               "49-C, 50 § 2º and 50-A to 50-E as worded by Lei 12.734/2012 until the final judgment, still pending when the "
               "data was read. Planalto's annotated page keeps those wordings (with '(Vide ADI 4917)'), and its consolidated "
               "page shows art. 49 in the wording before Lei 12.734 but arts. 48 and 50 in Lei 12.734's; the history keeps "
               "the annotated page's wordings and records the ruling as a version on 18.3.2013 that changes no words, "
               "credited to the provisions it names that stood then")
ADI4917_USED: list[str] = []
# Lei do Saneamento Básico art. 52 § 1º I, set after the copy model (san_model): the 2007 wording, replaced by Lei
# 13.308/2016 (7.7.2016), was given again word for word by Lei 14.026/2020 (16.7.2020), which Planalto prints unnoted
SAN_FINAL: list[tuple[tuple[str, str, str, int], dict]] = [
    (("art-52", "I -", "I - abranger o abastecimento de água, o esgotamento sanitário, o manejo de resíduos sólidos e o "
                       "manejo de águas pluviais e outras", -1),
     {"start": "2007-02-22", "start_law": None, "end": None, "end_law": None,
      "gaps": [("2016-07-07", "2020-07-16", "lei-13308-2016", "lei-14026-2020")]}),
    (("art-52", "I -", "I - abranger o abastecimento de água, o esgotamento sanitário, o manejo de resíduos sólidos e o "
                       "manejo de águas pluviais, com limpeza", 0),
     {"start": "2016-07-07", "start_law": "lei-13308-2016", "end": "2020-07-16", "end_law": "lei-14026-2020",
      "end_how": "successor", "gaps": [("2018-07-09", "2018-11-20", "mp-844-2018", "mp-844-2018-fim"),
                                       ("2018-12-28", "2019-06-04", "mp-868-2018", "mp-868-2018-fim")]}),
]
SAN_FINAL_WHY = ("Lei do Saneamento Básico art. 52 § 1º I: the 2007 wording stands until Lei 13.308/2016 (7.7.2016) and again "
                 "from Lei 14.026/2020 (16.7.2020), which gave the same words (Planalto prints them once, unnoted); Lei "
                 "13.308's wording stands in between, except while MP 844/2018 and MP 868/2018 were in force")
B8.SPAN_FIX += [
    ((SAN_ACT, "art-35", lab, start, 0), {"end": "2018-11-20", "end_law": "mp-844-2018-fim", "end_how": "lapse"},
     "Lei do Saneamento Básico art. 35: MP 844/2018's incisos I to III ('Vigência encerrada') end when it lapsed, "
     "20.11.2018 (the date-order rule had carried them to 4.6.2019)")
    for lab, start in (("I -", "I - a destinação adequada"), ("II -", "II - o nível de renda"),
                       ("III -", "III - as características dos lotes e"))
] + [
    ((SAN_ACT, "art-11", "§ 5º-A", "§ 5º-A Na hipótese de não existência", 0),
     {"start": "2018-12-28", "start_law": "mp-868-2018", "end": "2019-06-04", "end_law": "mp-868-2018-fim",
      "end_how": "lapse"},
     "Lei do Saneamento Básico art. 11 § 5º-A: Planalto prints it struck with only the note '(Vigência encerrada)'; it is "
     "MP 868/2018's (its text adds this § 5º-A), in force from 28.12.2018 until the MP lapsed, 4.6.2019"),
]
B9.WORD_FIX[:] = [
    ("pnma", "condicional, e a perda ou suspensão de participação em linhas de financiamento",
     "condicional, e a perda ou suspensão de participação em linhas de fiananciamento",
     "Política Nacional do Meio Ambiente art. 8 V: the annotated page prints 'linhas de financiamento'; the act as published "
     "(DOU 2.9.1981, the Chamber of Deputies' reproduction of the original publication) reads 'linhas de fiananciamento', "
     "and Lei 7.804/1989 changed only the body named in the inciso ('da SEMA' to 'do IBAMA'); the history keeps the "
     "published words, as Planalto's consolidated page does"),
    ("pnma", "O PRESIDENTE DA REPÚBLICA, faço saber", "O PRESIDENTE DA REPÚBLICA, Faço saber",
     "Política Nacional do Meio Ambiente, preamble: 'Faço saber' as in the act as published (the annotated page prints 'faço')"),
]
_RETYPED = ("Planalto's consolidated page of this act (l6938compilada.htm) is a retyped edition: it differs from the "
            "annotated page in punctuation after article numbers ('Art. 2º.' / 'Art. 2º -'), capital letters and some "
            "words; every line of the history was checked against its own source, the act as published (the Chamber of "
            "Deputies' reproduction of the DOU of 2.9.1981) or the amending law's text, and matches it (batch10/.tmp/"
            "pnma_adj.py); the consolidated page's variants are not in those texts")
B8.SPAN_FIX += [
    (("politica-nacional-do-meio-ambiente", "art-19", "Art. 19", "Art. 19 - (VETADO)", 0),
     {"end": "1989-07-20", "end_law": "lei-7804-1989", "end_how": "successor"},
     "Política Nacional do Meio Ambiente art. 19: the 1981 article was vetoed; Lei 7.804/1989 gave art. 19 a text "
     "('Incluído pela Lei nº 7.804, de 1989'), so the '(VETADO)' line, which Planalto still prints above it, ends then"),
]
B.EXPLAINED.update({"politica-nacional-do-meio-ambiente": {u: _RETYPED for u in (
    "art-02", "art-04", "art-05", "art-06", "art-09", "art-11", "art-12", "art-13", "art-14", "art-19", "art-20", "art-21",
    "preambulo")}})
B.EXPLAINED["politica-nacional-do-meio-ambiente"]["art-19"] = (
    "the consolidated page keeps the 1981 '(VETADO)' line above the art. 19 Lei 7.804/1989 gave the article; the history "
    "ends that line then (see the life-span decisions)")
B.EXPLAINED.update({
    _E: {"art-098": "the consolidated page keeps the placeholder 'XIV -;' for the inciso Lei 9.297/1996 revoked; the history "
                    "leaves revoked text out",
         "art-101": "the consolidated page leaves out item 4 of art. 101 II a) ('4. 20 (vinte) anos, se Capitão de "
                    "Corveta ou Major;', Redação dada pela Lei nº 13.954, de 2019), which the annotated page prints"},
    "lei-das-parcerias-publico-privadas": {
        "art-10": "the consolidated page prints incisos VI and VII of the caput in one paragraph; the annotated page and "
                  "the history give them a line each",
        "art-26": B7._QUOTED.format(x="§ 1º."),
    },
    "lei-de-concessoes": {"art-15": "typesetting: the annotated page prints § 3º without its closing full stop; the "
                                    "consolidated page has it"},
    "lei-de-abuso-de-autoridade": {"art-15-a": "the annotated page prints the heading 'Violência Institucional' (Incluído "
                                               "pela Lei nº 14.321, de 2022) above art. 15-A, kept in that article; the "
                                               "consolidated page sets it as a heading the replay check does not read"},
})

# ---------------------------------------------------------------------------------------------------------------
# An act's own vetoed parts promulgated after Congress overrode the veto (CF art. 66 §§ 5 and 7). Planalto prints the
# '(VETADO)' line (struck, or not) and then the promulgated wording with the note '(Promulgação partes vetadas)', and the
# promulgation text itself after the act's signature. A printed line is promulgated when its words are in that text (in
# a dispositivo that carries the note); it starts on the promulgation's DOU day, credited to the act's own law, and the
# '(VETADO)' line it replaces stands until then. act slug -> (DOU day, the act's law, why)
OWN_PROMULGATION: dict[str, tuple[str, str, str]] = {
    "lei-geral-do-esporte": (
        "2024-05-22", "lei-14597-2023",
        "Lei Geral do Esporte: Congress overrode vetoes of Lei 14.597/2023 and the President promulgated those parts on "
        "21.5.2024 (DOU 22.5.2024; the text is printed at the end of Planalto's page): each promulgated dispositivo "
        "(arts. 15, 27 parágrafo único, 34 parágrafo único, 36 § 1º, 37, 40 to 49 with the headings of Seções II and III "
        "of their chapter, 86 § 12, 153, 160 § 1º, 212 and the others the promulgation text names) takes effect on "
        "22.5.2024, credited to Lei 14.597/2023, and its '(VETADO)' line stands until then"),
    "lei-de-abuso-de-autoridade": (
        "2019-09-27", "lei-13869-2019",
        "Lei de Abuso de Autoridade: the parts of Lei 13.869/2019 vetoed on 5.9.2019 were promulgated after Congress "
        "overrode the veto (DOU 27.9.2019, edição extra), before the act took effect on 3.1.2020, so they are part of its "
        "first version and the '(VETADO)' lines never stood"),
}
OWN_PROMULGATION_USED: list[str] = []
_lifespans10 = P.lifespans


def _flat(s: str) -> str:
    import re as _re
    s = s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    return _re.sub(r"[\s\"']+", " ", s).strip()


def _promulgation_text(page: str) -> str:
    import html as _h
    import re as _re
    keep = B8.CURRENT_PAGE[0]
    raw = P.raw(page)
    B8.CURRENT_PAGE[0] = keep
    t = P.decode(raw[0])
    t = _re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", t)
    t = _h.unescape(_re.sub(r"<[^>]+>", " ", t))
    m = _re.search(r"Brasília,\s+\d", t)   # the act's own signature; the promulgation text follows it
    return _flat(t[m.end():]) if m else ""


# replay problems on Lei do Saneamento Básico lines that san_model (below) sets afresh: the 2018-2020 copies; checked
# after the model by the lapse-day invariant (batch10/.tmp/lsbinv.py) and the duplicate-line check
SAN_SETTLED = ("art-23 [XIII -]", "art-35 [I -]", "art-35 [II -]", "art-35 [III -]", "art-52 [I -]")


# Política Nacional do Meio Ambiente: Planalto's annotated page prints 'IBAMA' in lines Leis 9.960/2000 and 10.165/2000
# wrote with 'Ibama'; a line is corrected only where the corrected words, and not the printed ones, are in the law's text
PNMA_CASE: list[str] = []
_LAWTEXT: dict[str, str] = {}


def _loose(t: str) -> str:
    """Words only, for finding a line in an act's text: case kept, punctuation, dashes and 'nº'/'n o' spacing dropped."""
    t = t.replace("nº", "no").replace("n o ", "no ").replace("n º", "no")
    return re.sub(r"[^0-9A-Za-zÀ-ÿ]+", "", t)


def _law_text(law: str) -> str:
    import html as _h
    if law not in _LAWTEXT:
        keep = B8.CURRENT_PAGE[0]
        r = P.raw("law:" + law)
        B8.CURRENT_PAGE[0] = keep
        t = P.decode(r[0]) if r else ""
        t = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", t)
        _LAWTEXT[law] = _flat(_h.unescape(re.sub(r"<[^>]+>", " ", t)))
    return _LAWTEXT[law]


def lifespans(paras, cx):
    problems = _lifespans10(paras, cx)
    if cx.act == "politica-nacional-do-meio-ambiente":
        for p in paras:
            if p["start_law"] in ("lei-9960-2000", "lei-10165-2000") and "IBAMA" in p["text"]:
                src = _loose(_law_text(p["start_law"]))
                body = lambda x: _loose(re.sub(r"^(Art\.\s*\S+|§\s*\S+|Parágrafo único|[IVXL]+\s*-)\s*", "", P.norm(x)))
                fixed = p["text"].replace("IBAMA", "Ibama")
                if body(fixed) in src and body(p["text"]) not in src:
                    p["text"] = fixed
                    PNMA_CASE.append(p["unit"])
    if cx.act == "lei-do-saneamento-basico":
        problems = [x for x in problems if not (x.startswith(("restored wording after an open one: ", "ends before it starts: "))
                                                and x.split(": ", 1)[1].startswith(SAN_SETTLED))]
    hit = OWN_PROMULGATION.get(cx.act)
    if not hit:
        return problems
    day, law, why = hit
    act = next(a for a in ACTS if a["slug"] == cx.act)
    text = _promulgation_text(act["page"])
    promulgated = set()
    block = None   # the unit of the promulgated block being read: it starts at a line carrying the note
    for p in paras:
        body = _flat(P.norm(p["text"]))
        inside = (not p.get("skip") and "(VETADO)" not in p["text"] and len(body) >= 8 and body in text)
        if inside and any("Promulgação partes vetadas" in n for n in p["notes"]):
            block = p["unit"]
        elif not (inside and block == p["unit"] and p["unit"] != "titulos"):
            block = None
            continue
        promulgated.add((p["unit"], p["label"]))
        if day > cx.act_day:
            p["start"], p["start_law"], p["start_how"], p["pinned"] = day, law, "promulgation", True
    for p in paras:
        if (p["unit"], p["label"]) in promulgated and "(VETADO)" in p["text"] and p["state"] != "plain" and day > cx.act_day:
            p["skip"] = False
            p["start"], p["start_law"] = cx.act_day, None
            p["end"], p["end_law"], p["end_how"], p["pinned"] = day, law, "promulgation", True
    if promulgated:
        OWN_PROMULGATION_USED.append(why)
    return problems


P.lifespans = B.lifespans = lifespans

# Lei do Saneamento Básico, 2018-2020: MP 844/2018 (in force 9.7.2018, lapsed 20.11.2018) and MP 868/2018 (28.12.2018,
# lapsed 4.6.2019) rewrote articles, and Planalto prints such an article as a run of copies: the 2007 wording (struck),
# the MP's, the 2007 wording again after the lapse, ... The replay dates each copy from its notes, so copies overlap or
# leave holes. Here each 2007-era wording of an article an MP touched is one line: the last copy Planalto prints (its
# place in today's text), standing from its first day to its last, except while an MP that replaced it was in force:
# every wording of the article if the MP rewrote its caput, else the wordings with the same label as the MP's lines.
SAN_MPS = {"mp-844-2018": ("2018-07-09", "2018-11-20"), "mp-868-2018": ("2018-12-28", "2019-06-04")}
SAN_USED: list[str] = []


def san_model(paras):
    for unit in dict.fromkeys(p["unit"] for p in paras):
        rows = [p for p in paras if p["unit"] == unit and not p.get("heading")]

        def own(p, mp):   # a line in the MP's own wording (not a 2007 wording the replay dated from the MP)
            n = mp.split("-")[1]
            return p["start_law"] == mp and any(re.search(r"(Redação dada|Incluíd|Acrescid)[^)]*Medida Provisória nº " + n, x)
                                                for x in p["notes"])
        mps = {mp: [p for p in rows if own(p, mp)] for mp in SAN_MPS}
        mps = {mp: ls for mp, ls in mps.items() if ls}
        if not mps:
            continue
        whole = {mp: any((p["label"] or "").startswith("Art.") for p in ls) for mp, ls in mps.items()}
        mine = {id(p) for ls in mps.values() for p in ls}
        old = [p for p in rows if id(p) not in mine and p["start"] < "2020-07-16" and (
            (p["start_law"] or "").endswith("-fim") or p["start"] < "2018-07-09" or p["start_law"] in SAN_MPS)]
        groups: dict = {}
        for p in old:
            # copies are the same wording up to typesetting (punctuation, 'nº'/'no', spacing)
            k = re.sub(r"[^0-9a-zà-ü]+", "", P.norm(p["text"]).lower().replace("nº", "no"))
            groups.setdefault((p["label"], k), []).append(p)
        for (label, _), cs in groups.items():
            keep = cs[-1]
            noted = [c["start"] for c in cs if c["start_law"] and not c["start_law"].endswith("-fim")
                     and c["start_law"] not in SAN_MPS]
            firm = noted or [c["start"] for c in cs if not (c["start_law"] or "").endswith("-fim")]
            start = min(firm) if firm else min(c["start"] for c in cs)
            end, end_law0 = keep["end"], keep.get("end_law")   # the last copy, in today's place, ends the wording
            gaps = [(a, b, mp, mp + "-fim") for mp, (a, b) in SAN_MPS.items() if mp in mps and (
                whole[mp] or any(q["label"] == label for q in mps[mp])) and start < a and (end is None or end > a)]
            for c in cs:
                if c is not keep and not c.get("skip"):
                    c["skip"], c["end_how"], c["pinned"] = True, "san-copy", True
            law = next((c["start_law"] for c in cs if c["start"] == start), keep["start_law"])
            keep.update({"start": start, "start_law": law, "end": end, "gaps": gaps, "skip": False, "pinned": True})
            keep["end_law"] = end_law0
        SAN_USED.append(unit)

# Lei do Petróleo, 2012-2013 (hand model, read from the pages of Lei 12.734/2012 and MP 592/2012, both pinned):
# - Lei 12.734/2012 (DOU 30.11.2012, edição extra; art. 5: in force on publication) was sanctioned with its art. 3 (the
#   new wordings of arts. 48, 49 and 50 and the new arts. 49-A to 49-C and 50-A to 50-F of Lei 9.478) and its art. 4
#   (revoking art. 49 §§ 1º to 3º and art. 50 § 4º) vetoed whole. Congress overrode the veto and the President promulgated
#   those parts on 14.3.2013 (DOU 15.3.2013; the promulgation text is printed on Lei 12.734's page). Every Lei 12.734
#   wording of this act therefore takes effect on 15.3.2013, and the wordings it replaced stand until then. Planalto's
#   annotated page of Lei 9.478 dates none of this: it prints the 12.734 wordings with the note 'Redação dada / Incluído
#   pela Lei nº 12.734, de 2012'.
# - MP 592/2012 (DOU 3.12.2012, edição extra; in force on publication; lapsed, Ato Declaratório 31/2013) added arts. 48-A,
#   49-A, 50 § 5º, 50-A, 50-B and 81-A and revoked art. 49 § 3º and art. 50 § 4º (its art. 3 I and II; Planalto's page
#   gives those two paragraphs only '(Vide Medida Provisória nº 592, 2012)'). Its arts. 49-A, 50 § 5º, 50-A and 50-B are
#   replaced by Lei 12.734's on 15.3.2013 (same dispositivos, later law); its arts. 48-A and 81-A stand until the lapse.
B.EXPLAINED[_LP] = {
    "art-08": "the consolidated page prints the two wordings of inciso XI in one paragraph, keeps inciso XVIII as Lei "
              "14.993/2024 worded it (the annotated page gives Lei 15.103/2025's wording, 'dos biocombustíveis e do "
              "hidrogênio'), leaves out the '(revogado)' lines of incisos XX to XXII, XXIV and XXV, and ends inciso XXVIII "
              "with a full stop the annotated page does not print",
    "art-10": "the consolidated page ends the parágrafo único with the start of its note, '(Parágrafo único'",
    "art-48": "typesetting: the annotated page prints 'Lei no 12.351' in § 1º and no semicolon after § 1º I ('em 2011'); "
              "the consolidated page and the promulgation text of Lei 12.734/2012 read 'Lei nº 12.351' and 'em 2011;'",
    "art-49": "the consolidated page prints art. 49 as it read before Lei 12.734/2012 (incisos I d) and II, §§ 1º to 3º), "
              "while it prints arts. 48 and 50 in Lei 12.734's wording; the annotated page, and the promulgation text of "
              "Lei 12.734 (DOU 15.3.2013), give art. 49 the wording the history has (see the ADI 4.917 decision)",
    "art-68-b": _W68 + " (the '(VETADO)' line is Lei 14.292/2022's)",
    "art-68-c": _W68,
}
LPET_DAY = "2013-03-15"
LPET_LAW = "lei-12734-2012"
LPET_MP = "mp-592-2012"
LPET_MP_DAY = "2012-12-03"
LPET_MP_REVOKED = {("art-49", "§ 3º"), ("art-50", "§ 4º")}
LPET_MP_REPLACED = {"art-49-a", "art-50-a", "art-50-b"}   # whole articles; plus art. 50 § 5º below
LPET_WHY = ("Lei do Petróleo, Lei 12.734/2012: its art. 3 (the new wordings of arts. 48, 49 and 50 and the new arts. 49-A "
            "to 49-C and 50-A to 50-F) and its art. 4 (revoking art. 49 §§ 1º to 3º and art. 50 § 4º) were vetoed when the "
            "law was sanctioned (DOU 30.11.2012); Congress overrode the veto and the parts were promulgated on 14.3.2013 "
            "(DOU 15.3.2013; promulgation text on Lei 12.734's page), so every Lei 12.734 wording of this act takes effect "
            "on 15.3.2013 (art. 5: in force on publication), credited to Lei 12.734/2012, and the wordings it replaced "
            "stand until then; Planalto's annotated page of Lei 9.478 does not give that day. Lei 12.734's page notes a "
            "partial republication on 25.3.2013; the history uses the wordings Planalto prints")
LPET_MP_WHY = ("Lei do Petróleo, Medida Provisória nº 592/2012 (in force 3.12.2012, lapsed 13.5.2013): its art. 3 I and II "
               "revoked art. 49 § 3º and art. 50 § 4º (Planalto's page gives them only '(Vide Medida Provisória nº 592, "
               "2012)'), so those paragraphs end on 3.12.2012, credited to it (Lei 12.734 revoked them again from "
               "15.3.2013, so the lapse does not restore them); the MP's arts. 49-A, 50 § 5º, 50-A and 50-B end on "
               "15.3.2013, when Lei 12.734's wordings of the same dispositivos take effect; its arts. 48-A and 81-A stand "
               "until the lapse")
LPET_USED: list[str] = []
_RX12734 = re.compile(r"(Redação dada|Incluíd[oa]|Acrescid[oa]) pela Lei nº 12\.734")


def lpet_model(paras):
    for p in paras:
        if p.get("heading") or p.get("skip"):
            continue
        noted = any(_RX12734.search(n) for n in p["notes"])
        mp_own = p["start_law"] == LPET_MP or any("Medida Provisória nº 592" in n and "Vide" not in n for n in p["notes"])
        if noted and p["start"] != LPET_DAY and p["start"] <= "2013-05-13":
            p["start"], p["start_law"], p["pinned"] = LPET_DAY, LPET_LAW, True
        elif (p["unit"], p["label"]) in LPET_MP_REVOKED and p["end_law"] == LPET_LAW and p["start"] < LPET_MP_DAY:
            p["end"], p["end_law"], p["end_how"], p["pinned"] = LPET_MP_DAY, LPET_MP, "note", True
        elif p["end_law"] == LPET_LAW and p["end"] and p["end"] < LPET_DAY:
            p["end"], p["pinned"] = LPET_DAY, True
        elif mp_own and (p["unit"] in LPET_MP_REPLACED or (p["unit"], p["label"]) == ("art-50", "§ 5º")):
            p["end"], p["end_law"], p["end_how"], p["pinned"] = LPET_DAY, LPET_LAW, "successor", True
    LPET_USED[:] = [LPET_WHY, LPET_MP_WHY]


_build_act10 = P.build_act
B9.REPEALS["estatuto-do-torcedor"] = (
    "2023-06-15", "lei-14597-2023",
    "The Estatuto de Defesa do Torcedor (Lei 10.671/2003) was repealed as a whole by the Lei Geral do Esporte (Lei "
    "14.597/2023 art. 217 III), in force on its publication (DOU 15.6.2023), so its last version, on 15.6.2023, removes "
    "every provision, credited to Lei 14.597/2023. After the repeal Planalto strikes the whole page, so the page is read "
    "from a capture of 21.3.2023, before the repeal, and the history up to 14.6.2023 is checked against that capture's "
    "unstruck text")
# Lei 10.671/2003 art. 44: 'O disposto no parágrafo único do art. 13, e nos arts. 18, 22, 25 e 33 entrará em vigor após
# seis meses da publicação desta Lei' (DOU 16.5.2003): the period ends on 16.11.2003, in force from 17.11.2003
ETOR_LATE = {"art-18", "art-22", "art-25", "art-33"}
ETOR_DAY = "2003-11-17"


def build_act(paras, act_day, gate, gate_law, unit_label):
    slug = ACTS[len(B7._act_order)]["slug"] if len(B7._act_order) < len(ACTS) else "?"
    if slug == "estatuto-do-torcedor":
        gate = dict(gate, **{u: ETOR_DAY for u in ETOR_LATE})
        gate_law = dict(gate_law, **{u: "lei-10671-2003" for u in ETOR_LATE})
    versions = _build_act10(paras, act_day, gate, gate_law, unit_label)
    if slug == "lei-do-petroleo":
        before = [v for v in versions if v["from"] <= ADI4917_DAY]
        units = before[-1]["units"]
        cred = {u: ["stf-adi-4917"] for u in ADI4917_UNITS if u in units}
        assert not any(v["from"] == ADI4917_DAY for v in versions)
        versions.insert(len(before), {"from": ADI4917_DAY, "source_url": before[-1].get("source_url"),
                                      "sha256": before[-1].get("sha256"), "units": units, "credits": cred})
        ADI4917_USED.append(ADI4917_WHY)
        for v in versions:
            if v["from"] == LPET_DAY:
                v["note"] = ("Parts of Lei 12.734/2012 that the President vetoed and Congress restored by overriding the "
                             "veto, promulgated and published in the DOU of 15.3.2013: the new royalty and special-"
                             "participation rules of arts. 48 to 50-F.")
    hit = OWN_PROMULGATION.get(slug)
    if hit and hit[0] > act_day:
        for v in versions:
            if v["from"] == hit[0]:
                v["note"] = ("Parts of the act that the President vetoed and Congress restored by overriding the veto, "
                             "promulgated and published in the DOU of " + ".".join(str(int(x)) for x in hit[0].split("-")[::-1])
                             + "; until then each read '(VETADO)'.")
    return versions


P.build_act = B.build_act = build_act
_inner10 = B6.PB5B._write_part5


def _inner(*a) -> int:
    B5.EXTRA_DECISIONS.extend(x + "." for x in dict.fromkeys(OWN_PROMULGATION_USED + LPET_USED + ADI4917_USED))
    if PNMA_CASE:
        B5.EXTRA_DECISIONS.append(
            "Política Nacional do Meio Ambiente: Planalto's annotated page prints 'IBAMA' in lines that Leis 9.960/2000 and "
            "10.165/2000 wrote with 'Ibama'; those lines read as the laws' own texts (checked line by line against them): "
            + ", ".join(dict.fromkeys(PNMA_CASE)) + ".")
    if SAN_USED:
        B5.EXTRA_DECISIONS.append(
            "Lei do Saneamento Básico, 9.7.2018 to 15.7.2020: Medida Provisória nº 844/2018 (in force 9.7.2018, lapsed "
            "20.11.2018, Ato Declaratório 70/2018) and nº 868/2018 (in force 28.12.2018, lapsed 4.6.2019, Ato Declaratório "
            "36/2019) each rewrote whole articles; Planalto prints such an article as the 2007 text, MP 844's text, the "
            "2007 text again, MP 868's text and the 2007 text once more (with Lei 14.026/2020's changes). Each 2007-era "
            "wording is kept once, in the place of its last copy, standing from its first day to its last except while "
            "an MP that replaced it was in force (every wording of the article if the MP rewrote the caput, else those "
            "with the label of an MP line), so the act reads as before each MP once it lapsed: " + ", ".join(
                u for u in dict.fromkeys(SAN_USED) if u.startswith(("art-", "pre"))) + ".")
        B5.EXTRA_DECISIONS.extend(u + "." for u in dict.fromkeys(SAN_USED) if not u.startswith(("art-", "pre")))
    return _inner10(*a)
    return _inner10(*a)


B6.PB5B._write_part5 = _inner

# SPAN_FIX entries with {"keep": True}: a line the stale-wording rules would leave out stands as the replay read it
_stale_fix = B7.stale_fix.fix


def _fix(core, paras, slug, same_day):
    keep = [(p, p.get("skip"), p.get("end_how"), p["start"], p["start_law"]) for p in paras if p.get("keep")]
    res = _stale_fix(core, paras, slug, same_day)
    if slug == SAN_ACT and not os.environ.get("NOSAN"):
        san_model(paras)   # after every other rule (the date-order and stale-wording rules rewrite spans)
        for (unit, label, start, nth), fields in SAN_FINAL:
            hits = [p for p in paras if p["unit"] == unit and p["label"] == label and P.norm(p["text"]).startswith(start)
                    and not p.get("heading")]
            p = hits[nth]
            p.update(fields)
            p["skip"] = False
            SAN_USED.append(SAN_FINAL_WHY)
    if slug == _LP:
        lpet_model(paras)   # after every other rule, as san_model
    for p, skip, how, start, law in keep:
        p["skip"], p["end_how"], p["start"], p["start_law"] = skip, how, start, law
    return res


B7.stale_fix.fix = _fix

# Lines closing a quoted amendment ('....." (NR)') stay in their article: now in the shared parsers' move_rubricas
# (parse_proc.closes_quote, with its decision), where this batch's wrapper first did it.

SRC = HERE / "sources_batch10.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
