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
    "b": ["lei-das-aguas", "lei-dos-crimes-de-responsabilidade-dos-prefeitos", "lei-geral-de-telecomunicacoes",
          "lei-dos-crimes-contra-a-economia-popular"],
    "c": ["lei-do-snuc", "lei-da-liberdade-economica", "estatuto-da-igualdade-racial"],
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
    "lei-8212-1991": ("1991-07-25", "Lei 8.212/1991 art. 104: 'Esta Lei entrará em vigor na data de sua publicação' (DOU "
                                    "25.7.1991, republished 11.4.1996 and 14.8.1998)"),
    "lei-8213-1991": ("1991-07-25", f"Lei 8.213/1991 art. 155: {_PUB} (DOU 25.7.1991, republished 11.4.1996 and 14.8.1998)"),
    "lc-123-2006": ("2006-12-15", "Lei Complementar 123/2006 art. 88: 'Esta Lei Complementar entra em vigor na data de sua "
                                  "publicação, ressalvado o regime de tributação das microempresas e empresas de pequeno porte, "
                                  "que entra em vigor em 1º de julho de 2007' (DOU 15.12.2006)"),
    "lei-4504-1964": ("1964-11-30", "Lei 4.504/1964 art. 128: 'entrará em vigor na data de sua publicação' (DOU 30.11.1964, "
                                    "rectified 17.12.1964)"),
    "lei-9472-1997": ("1997-07-17", f"Lei 9.472/1997 art. 216: {_PUB} (DOU 17.7.1997)"),
    "lei-9433-1997": ("1997-01-09", f"Lei 9.433/1997 art. 56: {_PUB} (DOU 9.1.1997)"),
    "lei-9985-2000": ("2000-07-19", f"Lei 9.985/2000 art. 59: {_PUB} (DOU 19.7.2000)"),
    "lei-13874-2019": ("2019-09-20", "Lei 13.874/2019 art. 20: 'Esta Lei entra em vigor: I - (VETADO); II - na data de sua "
                                     "publicação, para os demais artigos' (DOU 20.9.2019, edição extra-B); the conversion of "
                                     "Medida Provisória nº 881/2019"),
    "lei-7565-1986": ("1986-12-23", "Lei 7.565/1986 art. 323: 'Este Código entra em vigor na data de sua publicação' (DOU "
                                    "23.12.1986, rectified 30.12.1986)"),
    "lei-12288-2010": ("2010-10-19", "Lei 12.288/2010 art. 65: 'Esta Lei entra em vigor 90 (noventa) dias após a data de sua "
                                     "publicação' (DOU 21.7.2010): 21.7.2010 + 90 days, counted as for the other acts of this "
                                     "corpus (LC 95/1998 art. 8 § 1: the day of publication and the last day counted, in force "
                                     "the day after)"),
    "lei-1521-1951": ("1952-02-25", "Lei 1.521/1951 art. 33: 'Esta Lei entrará em vigor sessenta dias depois de sua publicação' "
                                    "(DOU 27.12.1951): 27.12.1951 + 60 days"),
    "dl-201-1967": ("1967-02-27", "Decreto-Lei 201/1967 art. 9: 'O presente decreto-lei entrará em vigor na data de sua "
                                  "publicação' (DOU 27.2.1967, rectified 14.3.1967)"),
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
    "lei-8212-1991": _L("Lei nº 8.212, de 1991", "Dispõe sobre a organização da Seguridade Social, institui Plano de "
                        "Custeio, e dá outras providências.", "1991-07-24", "1991-07-25", PAGES["l8212"]),
    "lei-8213-1991": _L("Lei nº 8.213, de 1991", "Dispõe sobre os Planos de Benefícios da Previdência Social e dá outras "
                        "providências.", "1991-07-24", "1991-07-25", PAGES["l8213"]),
    "lc-123-2006": _L("Lei Complementar nº 123, de 2006", "Institui o Estatuto Nacional da Microempresa e da Empresa de "
                      "Pequeno Porte; altera dispositivos das Leis nº 8.212 e 8.213, ambas de 24 de julho de 1991, da "
                      "Consolidação das Leis do Trabalho - CLT, aprovada pelo Decreto-Lei nº 5.452, de 1º de maio de 1943, da "
                      "Lei nº 10.189, de 14 de fevereiro de 2001, da Lei Complementar nº 63, de 11 de janeiro de 1990; e revoga "
                      "as Leis nº 9.317, de 5 de dezembro de 1996, e 9.841, de 5 de outubro de 1999.", "2006-12-14",
                      "2006-12-15", PAGES["lc123"]),
    "lei-4504-1964": _L("Lei nº 4.504, de 1964", "Dispõe sobre o Estatuto da Terra, e dá outras providências.", "1964-11-30",
                        "1964-11-30", PAGES["l4504"]),
    "lei-9472-1997": _L("Lei nº 9.472, de 1997", "Dispõe sobre a organização dos serviços de telecomunicações, a criação e "
                        "funcionamento de um órgão regulador e outros aspectos institucionais, nos termos da Emenda "
                        "Constitucional nº 8, de 1995.", "1997-07-16", "1997-07-17", PAGES["l9472"]),
    "lei-9433-1997": _L("Lei nº 9.433, de 1997", "Institui a Política Nacional de Recursos Hídricos, cria o Sistema Nacional "
                        "de Gerenciamento de Recursos Hídricos, regulamenta o inciso XIX do art. 21 da Constituição Federal, e "
                        "altera o art. 1º da Lei nº 8.001, de 13 de março de 1990, que modificou a Lei nº 7.990, de 28 de "
                        "dezembro de 1989.", "1997-01-08", "1997-01-09", PAGES["l9433"]),
    "lei-9985-2000": _L("Lei nº 9.985, de 2000", "Regulamenta o art. 225, § 1º, incisos I, II, III e VII da Constituição "
                        "Federal, institui o Sistema Nacional de Unidades de Conservação da Natureza e dá outras providências.",
                        "2000-07-18", "2000-07-19", PAGES["l9985"]),
    "lei-13874-2019": _L("Lei nº 13.874, de 2019", "Institui a Declaração de Direitos de Liberdade Econômica; estabelece "
                         "garantias de livre mercado; altera as Leis nºs 10.406, de 10 de janeiro de 2002 (Código Civil), 6.404, "
                         "de 15 de dezembro de 1976, 11.598, de 3 de dezembro de 2007, 12.682, de 9 de julho de 2012, 6.015, de 31 "
                         "de dezembro de 1973, 10.522, de 19 de julho de 2002, 8.934, de 18 de novembro 1994, o Decreto-Lei nº "
                         "9.760, de 5 de setembro de 1946 e a Consolidação das Leis do Trabalho, aprovada pelo Decreto-Lei nº "
                         "5.452, de 1º de maio de 1943; revoga a Lei Delegada nº 4, de 26 de setembro de 1962, a Lei nº 11.887, de "
                         "24 de dezembro de 2008, e dispositivos do Decreto-Lei nº 73, de 21 de novembro de 1966; e dá outras "
                         "providências.", "2019-09-20", "2019-09-20", PAGES["l13874"]),
    "lei-7565-1986": _L("Lei nº 7.565, de 1986", "Dispõe sobre o Código Brasileiro de Aeronáutica.", "1986-12-19",
                        "1986-12-23", PAGES["l7565"]),
    "lei-12288-2010": _L("Lei nº 12.288, de 2010", "Institui o Estatuto da Igualdade Racial; altera as Leis nºs 7.716, de 5 de "
                         "janeiro de 1989, 9.029, de 13 de abril de 1995, 7.347, de 24 de julho de 1985, e 10.778, de 24 de "
                         "novembro de 2003.", "2010-07-20", "2010-07-21", PAGES["l12288"]),
    "lei-1521-1951": _L("Lei nº 1.521, de 1951", "Altera dispositivos da legislação vigente sobre crimes contra a economia "
                        "popular.", "1951-12-26", "1951-12-27", PAGES["l1521"]),
    "dl-201-1967": _L("Decreto-Lei nº 201, de 1967", "Dispõe sobre a responsabilidade dos Prefeitos e Vereadores, e dá outras "
                      "providências.", "1967-02-27", "1967-02-27", PAGES["dl201"]),
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
P.COURTS.clear()                  # batch 13's Resolução do Senado 16/2006 (TCU): its decision is printed wherever it is set
B6.PB5B.SPLIT_NOTES.pop("rsf-16-2006", None)

# ---------------------------------------------------------------------------------------------------------------
# hand tables for these acts, each read from the official pages named in the reason

P.VIGENCIA_FIXED.update({
    "lc-102-2000": ("2000-08-01", "art. 7: 'Esta Lei Complementar entra em vigor no primeiro dia do mês subseqüente ao da sua "
                                  "publicação' (DOU 12.7.2000)"),
    "lc-190-2022": ("2022-01-05", "art. 3: 'Esta Lei Complementar entra em vigor na data de sua publicação, observado, quanto à "
                                  "produção de efeitos, o disposto na alínea \"c\" do inciso III do caput do art. 150 da "
                                  "Constituição Federal' (DOU 5.1.2022); as for other deferred effects, its wording is dated by "
                                  "the in-force day"),
    "lc-122-2006": ("2006-12-13", "art. 2: 'Esta Lei Complementar entra em vigor na data de sua publicação' (DOU 13.12.2006)"),
})
_LK = "lei-kandir"
B8.LABEL_FIX += [
    ("lc87", "2º Não integra a base de cálculo", "§ 2º Não integra a base de cálculo", "§ 2º",
     "Lei Kandir art. 13 § 2º: Planalto's page prints the paragraph as '2º Não integra ...', its '§' lost in an empty "
     "struck span above it; read as § 2º"),
]
_LC204 = ("Lei Kandir art. 12 § 5º (with its incisos I and II): vetoed in Lei Complementar 204/2023 (DOU 29.12.2023, in "
          "force 1.1.2024), the veto overridden by Congress and the part promulgated on 12.6.2024 (DOU 13.6.2024, printed at "
          "the end of LC 204's page); it starts on 13.6.2024, not with the rest of LC 204")
B8.SPAN_FIX += [
    ((_LK, "art-12", lab, pre, 0), {"start": "2024-06-13", "start_law": "lc-204-2023"}, _LC204) for lab, pre in [
        ("§ 5º", "§ 5º Alternativamente ao disposto no § 4º"),
        ("I -", "I - nas operações internas, as alíquotas estabelecidas"),
        ("II -", "II - nas operações interestaduais, as alíquotas fixadas")]
]
B8.SPAN_FIX += [
    ((_LK, "art-31", "§ 4º-A", "§ 4º-A. A partir de 1º de janeiro de 2003 volta a vigorar", 0),
     {"end": "2002-12-27", "end_law": "lc-115-2002", "end_how": "note", "skip": False},
     "Lei Kandir art. 31 § 4º-A (added by Lei Complementar 102/2000): Planalto's note '(Parágrafo Revogado pela LCP nº 115, "
     "de 26.12.2002' lacks its closing parenthesis and is not read as a note; LC 115/2002 art. 5 revoked the paragraph "
     "(DOU 27.12.2002, in force on publication)"),
]
# a repeal on a future day: today's text is still checked against Planalto's page (batch 9's rule returns no page for
# repealed acts, whose page is struck after the repeal)
_cons14 = P.consolidated


def consolidated(ident: str, digits: int):
    if any(a["consolidated"] == ident and a["slug"] in B9.REPEALS and B9.REPEALS[a["slug"]][0] > "2026-10-31" for a in ACTS):
        return B9._consolidated9(ident, digits)
    return _cons14(ident, digits)


P.consolidated = B.consolidated = consolidated
# LC 214/2025 art. 543: 'Ficam revogados a partir de 1º de janeiro de 2033: [...] III - a Lei Complementar nº 87 [...]; IV -
# a Lei Complementar nº 116' (art. 544 V: effects of art. 543 from 1.1.2033): both acts end on 1.1.2033 (futuro branch)
_R2033 = ("{act} is repealed as a whole from 1.1.2033 by Lei Complementar 214/2025 art. 543 ('Ficam revogados a partir de 1º "
          "de janeiro de 2033: [...] {item}'; art. 544 V: art. 543 takes effect on 1.1.2033), part of the transition to the "
          "IBS/CBS of Emenda Constitucional 132/2023: its last version, on 1.1.2033, removes every provision, credited to LC "
          "214/2025, and is on the future branch; the replay check is the usual one, today's text against Planalto's page")
B9.REPEALS.clear()
B9.REPEALS.update({
    "lei-kandir": ("2033-01-01", "lc-214-2025", _R2033.format(act="Lei Complementar 87/1996 (Lei Kandir)",
                                                             item="III - a Lei Complementar nº 87, de 13 de setembro de 1996")),
    "lei-do-iss": ("2033-01-01", "lc-214-2025", _R2033.format(act="Lei Complementar 116/2003 (ISS)",
                                                             item="IV - a Lei Complementar nº 116, de 31 de julho de 2003")),
})

# 14b
P.VIGENCIA_FIXED["lei-14173-2021"] = (
    "2021-06-16", "art. 13: 'Esta Lei entra em vigor: I - quanto aos arts. 1º, 2º e 4º, na data de sua publicação e produz "
                  "efeitos a partir de 1º de janeiro de 2021 [...]; II - (VETADO); III - quanto aos arts. 5º, 6º, 7º, 8º, 9º, "
                  "10 e 11 e ao inciso II do caput do art. 12, na data de sua publicação' (DOU 16.6.2021); its change to the "
                  "Lei Geral de Telecomunicações (art. 7: art. 2 VII) falls under III")
P.NOTE_FIX["(Incluído pela Lei º 14.108, de 2020)"] = (
    "(Incluído pela Lei nº 14.108, de 2020)",
    "Lei Geral de Telecomunicações: the note reads 'Lei º 14.108', 'nº' misprinted")
P.MP_PENDING["mp-2172-2001"] = (
    "Medida Provisória nº 2.172-32, de 23.8.2001 (DOU 24.8.2001, in force on publication), art. 7: 'Fica revogado o § 3º do "
    "art. 4º da Lei nº 1.521, de 26 de dezembro de 1951'; a reissue (its art. 5 validates acts under MP 2.172-31), kept in "
    "force by Emenda Constitucional 32/2001, art. 2, and never converted or revoked. Planalto's note names this edition "
    "only, so the revocation is dated by its publication; earlier editions of the chain are not modelled")
_LGT = "lei-geral-de-telecomunicacoes"
_LGT172 = ("Lei Geral de Telecomunicações art. 172 caput: Planalto strikes the 1997 wording and prints Lei 13.879/2019's new "
           "wording below it without a note (the note is on § 2º only); Lei 13.879/2019 art. 1 gives art. 172 caput that "
           "wording (its own page; DOU 4.10.2019, in force on publication), so the 1997 wording ends and the new one starts "
           "on 4.10.2019, credited to it")
B8.SPAN_FIX += [
    ((_LGT, "art-172", "Art. 172", "Art. 172. O direito de exploração de satélite brasileiro para transporte de sinais de "
                                   "telecomunicações assegura a ocupação da órbita e o uso das radiofreqüências", 0),
     {"end": "2019-10-04", "end_law": "lei-13879-2019", "end_how": "successor", "skip": False}, _LGT172),
    ((_LGT, "art-172", "Art. 172", "Art. 172. O direito de exploração de satélite brasileiro para transporte de sinais de "
                                   "telecomunicações assegura a ocupação da órbita e o uso das radiofrequências", 0),
     {"start": "2019-10-04", "start_law": "lei-13879-2019"}, _LGT172),
]
B9.WORD_FIX[:] = B9.WORD_FIX + [
    (pg, q + "Art. 90. Não poderão participar", "Art. 90. Não poderão participar",
     "Lei Geral de Telecomunicações art. 90: Planalto prints Lei 15.324/2026's wording with the opening quotation mark of "
     "the amending law ('“Art. 90.'); the mark is dropped")
    for pg in ("l9472",) for q in ('"', "“")
]
# 14c
P.NOTE_FIX["(Redação dada pela Lei nº 11.516, 2007)"] = (
    "(Redação dada pela Lei nº 11.516, de 2007)", "Lei do SNUC art. 6 III: the note reads 'Lei nº 11.516, 2007', 'de' missing")
_DOTTED = ("check artefact: the article quotes another law's provisions with dotted lines ('{lab} ....'), which the history "
           "keeps as '{lab}.' and the check, reading label-only lines as revoked dispositivos, drops")
B.EXPLAINED["lei-da-liberdade-economica"] = {"art-14": _DOTTED.format(lab="§ 1º")}
B.EXPLAINED["estatuto-da-igualdade-racial"] = {"art-62": _DOTTED.format(lab="§ 1º"), "art-64": _DOTTED.format(lab="§ 3º")}
# a quoted amendment closed by a line in single quotation marks ('Art. 1.368-F. ...'"), which the shared rubrica rule
# (closes_quote knows double quotes only) moved into the next article as its marginal heading: put back where printed
_paragraphs14 = P.paragraphs
SQUOTE_KEPT: list[str] = []


def paragraphs(html, digits):
    out, rest = _paragraphs14(html, digits)
    for i, p in enumerate(out):
        if p["label"] == "rubrica" and p["text"].lstrip().startswith(("'", "\u2018")) and i > 0 and not out[i - 1]["heading"]:
            SQUOTE_KEPT.append(f"{B8.CURRENT_PAGE[0]} {p['unit']} -> {out[i - 1]['unit']}: {p['text'][:40]!r}")
            p["unit"], p["label"] = out[i - 1]["unit"], ""
    return out, rest


P.paragraphs = B.paragraphs = paragraphs
OPEN_ITEMS = B13.OPEN_ITEMS
OPEN_ITEMS.update({
    "lei-do-iss": (
        "Lei do ISS (open item): the 'Lista de serviços anexa' (the list of taxable services, printed after the signature, "
        "with its own amendment notes) is not included; the history holds the articles only"),
    "lei-kandir": (
        "Lei Kandir: its Anexo (the União's transfers to the States, art. 31), printed struck after the signature, is not "
        "included; the history holds the articles only. Planalto's 'Vide' pointers (Decreto de 26.10.1996, ADC 49 at art. 12 "
        "I and art. 13 § 4º) strike no words and are not modelled"),
})
_inner14 = B6.PB5B._write_part5


def _inner(*a):
    # batch 9's wording is for acts repealed in the past; for a future repeal the page is today's
    if SQUOTE_KEPT:
        B5.EXTRA_DECISIONS.append(
            "A line that closes a quoted amendment with single quotation marks (\"'Art. 1.368-F. [...] Capítulo.'\"\"), "
            "which the marginal-heading rule would move into the next article, is kept in the article that quotes it: "
            + "; ".join(dict.fromkeys(SQUOTE_KEPT)) + ".")
    B9.REPEAL_CHECK[:] = [x.replace("the unstruck text of the pre-repeal capture of Planalto's page",
                                    "the unstruck text of Planalto's page (the repeal is in the future)")
                          for x in B9.REPEAL_CHECK]
    return _inner14(*a)


B6.PB5B._write_part5 = _inner

SRC = HERE / "sources_batch14.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
