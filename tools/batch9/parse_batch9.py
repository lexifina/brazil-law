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
    "l8666-2023": "leis/l8666cons.htm",
    "lacp": "leis/l7347orig.htm",
    "lacp-compilada": "leis/l7347compilada.htm",
}
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = B6.PAGES = B7.PAGES = B8.PAGES = PAGES


def _act(slug, short, page, consolidated, law, title, digits):
    return {"slug": slug, "short": short, "page": page, "consolidated": consolidated, "law": law, "title": title,
            "digits": digits, "url": PL + PAGES[page]}


ALL_ACTS: list[dict] = [a for a in B8.ALL_ACTS if a["slug"] == "lei-da-acao-civil-publica"] + [
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
    _act("lei-de-licitacoes-de-1993", "L8666", "l8666-2023", "l8666-2023", "lei-8666-1993",
         "Lei de Licitações e Contratos (Lei nº 8.666, de 21 de junho de 1993)", 3),
]
VERIFIED: list[str] = ["lei-de-diretrizes-e-bases-da-educacao", "lei-organica-da-saude", "lei-das-eleicoes",
                        "lei-de-licitacoes-de-1993", "lei-da-acao-civil-publica", "codigo-de-transito-brasileiro",
                        "codigo-florestal", "lei-de-registros-publicos"]
ENABLED = [s for s in os.environ.get("BATCH9_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
B7.ACTS[:] = ACTS
B8.ACTS[:] = ACTS

ACT_DAY_ALL: dict[str, tuple[str, str]] = {
    "lei-6015-1973": ("1976-01-01", "Lei 6.015/1973 art. 310 as enacted put it in force on 1.7.1974; Lei 6.064/1974 moved "
                                    "that to 1.7.1975 ('Redação dada pela Lei nº 6.064, de 1974'), and Lei 6.216/1975, "
                                    "published in the DOU of 1.7.1975, rewrote the article (renumbered art. 295, later art. "
                                    "298): 'Esta Lei entrará em vigor no dia 1º de janeiro 1976'. The act was never in force "
                                    "before 1.1.1976; Lei 6.216 art. 2 had it republished with its changes (DOU 16.9.1975), "
                                    "the text Planalto's page follows ('Atualizada a partir da republicação')"),
    "lei-7347-1985": B8.ACT_DAY_ALL["lei-7347-1985"],
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
    "lei-8666-1993": ("1993-06-22", "Lei 8.666/1993 art. 125 (art. 124 before Lei 8.883/1994 renumbered it): 'Esta Lei entra "
                                    "em vigor na data de sua publicação' (DOU 22.6.1993)"),
}
ACT_LAWS_ALL: dict[str, dict] = {
    "lei-6015-1973": B._act_law("Lei nº 6.015, de 1973", "Dispõe sobre os registros públicos, e dá outras providências.",
                                "1973-12-31", "1973-12-31", PAGES["lrp"]),
    "lei-7347-1985": B8.ACT_LAWS_ALL["lei-7347-1985"],
    "lei-8666-1993": B._act_law("Lei nº 8.666, de 1993", "Regulamenta o art. 37, inciso XXI, da Constituição Federal, institui "
                                "normas para licitações e contratos da Administração Pública e dá outras providências.",
                                "1993-06-21", "1993-06-22", PAGES["l8666-2023"]),
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
B8_NOTE_LACP = P.NOTE_FIX["(Incluído pela Lei nª 8.078, de 11.9.1990)"]
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
P.NOTE_FIX.update({
    "(Incluído pela Lei nº 13.495, 2017)": (
        "(Incluído pela Lei nº 13.495, de 2017)",
        "Código de Trânsito: notes read 'Lei nº 13.495, 2017' (no 'de'); Lei nº 13.495, de 24.10.2017 gives that wording"),
    "(Redação dada pela Lei nº 13.495, 2017)": (
        "(Redação dada pela Lei nº 13.495, de 2017)", "as the 'Incluído' notes of Lei 13.495"),
    "(Revogado pela Lei nº 13 281, de 2016)": (
        "(Revogado pela Lei nº 13.281, de 2016)", "Código de Trânsito: a note reads 'Lei nº 13 281' (a space for the point)"),
    "(Incluído pela Lei nª 8.078, de 11.9.1990)": B8_NOTE_LACP,
    "(Redação dada pela Lei nº 13.465, 2017)": (
        "(Redação dada pela Lei nº 13.465, de 2017)",
        "Lei 8.666 art. 17: the note reads 'Lei nº 13.465, 2017' (no 'de'); Lei nº 13.465, de 11.7.2017 gives that wording"),
    "(Incluído pela Lei nº 12.188, de 2.010)": (
        "(Incluído pela Lei nº 12.188, de 2010)",
        "Lei 8.666 art. 24 XXX: the note reads 'Lei nº 12.188, de 2.010'; its link is Lei nº 12.188, de 11.1.2010"),
})
_CTB = "codigo-de-transito-brasileiro"
P.VIGENCIA_FIXED.update({
    "lei-13160-2015": ("2016-01-23", "art. 4: 'Esta Lei entra em vigor após decorridos cento e cinquenta dias de sua "
                                     "publicação oficial' (DOU 26.8.2015): the 150th day counted from publication is "
                                     "22.1.2016 (LC 95/1998 art. 8 § 1)"),
    "lei-12971-2014": ("2014-11-01", "'Esta Lei entra em vigor no 1º (primeiro) dia do 6º (sexto) mês após a sua "
                                     "publicação' (DOU 12.5.2014): 1.11.2014"),
    "lei-12865-2013": ("2013-10-10", "'Esta Lei entra em vigor: I - a partir do primeiro dia do quarto mês subsequente ao de "
                                     "sua publicação, em relação ao disposto no art. 34 desta Lei; II - na data de sua "
                                     "publicação, para os demais dispositivos' (DOU 10.10.2013); its change to the Código de "
                                     "Trânsito (art. 10) is in its art. 22, so in force on publication"),
    "lei-14229-2021": ("2022-04-20", "art. 7: 'Esta Lei entra em vigor: I - na data de sua publicação, quanto aos arts. 1º, "
                                     "3º, 4º e 5º, ao inciso I do art. 6º, às alterações do art. 2º aos arts. 131, 271 e 282 "
                                     "e, também no art. 2º, à inclusão do art. 338-A na Lei nº 9.503 [...]; II - em 1º de "
                                     "janeiro de 2024, quanto às alterações ao caput do art. 289 [...] e quanto aos "
                                     "acréscimos do § 6º ao art. 285 e do art. 289-A [...]; III - após decorridos 180 "
                                     "(cento e oitenta) dias de sua publicação oficial, quanto aos demais dispositivos' "
                                     "(DOU 22.10.2021): the rest from 20.4.2022 (the 180th day counted from publication is "
                                     "19.4.2022, LC 95/1998 art. 8 § 1); the per-article days are set below"),
    "lei-12249-2010": ("2010-06-14", "art. 139: 'Esta Lei entra em vigor: I - na data de sua publicação, produzindo efeitos "
                                     "[...] d) a partir de 16 de dezembro de 2009, em relação aos demais dispositivos' (DOU "
                                     "14.6.2010); its revocation of Código de Trânsito art. 288 § 2º is dated the day it "
                                     "entered into force, 14.6.2010 (the clause gives it effect from 16.12.2009, before the "
                                     "law existed)"),
    "lei-14440-2022": ("2022-09-05", "'Esta Lei entra em vigor: I - a partir de 1º de janeiro de 2027, para as alterações do "
                                     "art. 15 referentes ao caput e § 5º do art. 282-A da Lei nº 9.503 [...]; e II - na data "
                                     "de sua publicação, para os demais dispositivos' (DOU 5.9.2022); its changes to art. "
                                     "282-A caput and § 5º are dated 1.1.2027 below"),
})

for _u in ("art-131", "art-271", "art-282", "art-338-a"):
    P.VIGENCIA_PROVISION[("lei-14229-2021", _CTB, _u)] = ("2021-10-22", "Lei 14.229/2021 art. 7 I (on publication)")
for _u in ("art-289", "art-285", "art-289-a"):
    P.VIGENCIA_PROVISION[("lei-14229-2021", _CTB, _u)] = ("2024-01-01", "Lei 14.229/2021 art. 7 II (1.1.2024)")
P.PUBLISHED_FIXED.update({
    "mp-75-2002": ("2002-10-25", "the Chamber of Deputies' record of Medida Provisória nº 75, de 24.10.2002: 'Diário "
                                 "Oficial da União - Seção 1 - 25/10/2002, Página 1 (Publicação Original)', republished "
                                 "28.10.2002"),
})
P.MP_LAPSE.update({
    "mp-75-2002": ("2002-12-19", "rejected: the Chamber of Deputies' record of the MP: 'Esta Medida Provisória foi "
                                 "rejeitada pelo Ato da Câmara dos Deputados, em sessão realizada em 18/12/2002 (DOU de "
                                 "19/12/2002)'; its wording of Código de Trânsito arts. 285 and 288 stands until the "
                                 "rejection was published"),
    "mp-1360-2026": ("2026-09-16", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 96, de 2026 (DOU "
                                   "17.9.2026): 'teve seu prazo de vigência encerrado no dia 15 de setembro de 2026'"),
    "mp-646-2014": ("2014-09-24", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 38, de 2014 (DOU "
                                  "26.9.2014): 'teve seu prazo de vigência encerrado no dia 23 de setembro do corrente "
                                  "ano'"),
    "mp-882-2019": ("2019-08-31", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 55, de 2019 (DOU "
                                  "3.9.2019): 'teve seu prazo de vigência encerrado no dia 30 de agosto do corrente ano'"),
    "mp-896-2019": ("2020-02-17", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 6, de 2020 (DOU "
                                  "18.2.2020): 'teve seu prazo de vigência encerrado no dia 16 de fevereiro de 2020'"),
    "mp-910-2019": ("2020-05-20", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 36, de 2020 (DOU "
                                  "21.5.2020): 'teve seu prazo de vigência encerrado no dia 19 de maio de 2020'"),
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
_A = "lei-da-acao-civil-publica"
_W53 = ("Lei da Ação Civil Pública art. 1: Lei 10.257/2001 (Estatuto da Cidade, DOU 11.7.2001, in force 9.10.2001) art. 53 "
        "would have added 'III - à ordem urbanística' and renumbered III-V as IV-VI, but Medida Provisória nº 2.180-35/2001 "
        "(DOU 27.8.2001; in force on 11.9.2001, so it stays in force under Emenda Constitucional 32/2001 art. 2) revoked "
        "that art. 53 before it took effect (Lei 10.257's page: '(Revogado pela Medida Provisória nº 2.180-35, de "
        "24.8.2001)'), and itself added 'VI - à ordem urbanística', reworded V and added the Parágrafo único. The lines "
        "Planalto prints for Lei 10.257's numbering never stood and are left out; incisos III and IV keep their wording "
        "throughout (Planalto prints them twice)")
B8.LABEL_FIX[:] = [
    ("ctb", "3º Os equipamentos fixos ou móveis", "§ 3º Os equipamentos fixos ou móveis", "§ 3º",
     "Código de Trânsito art. 99 § 3º is printed '3º Os equipamentos ...' (no '§'); the consolidated page prints '§ 3º'"),
    ("ctb", "'VI - em de", "VI - em de", "VI -",
     "Código de Trânsito art. 231 VI is printed with a stray apostrophe before the numeral; the consolidated page has none"),
    ("lacp", "l - ao meio-ambiente;", "I - ao meio-ambiente;", "I -",
     "Lei da Ação Civil Pública art. 1 I and II and art. 5 I (1985 wording): the roman numerals are printed with the letter "
     "l ('l - ao meio-ambiente;', 'll - ao consumidor;', 'l - esteja constituída'); read as I and II"),
    ("lacp", "ll - ao consumidor;", "II - ao consumidor;", "II -", "as art. 1 I"),
    ("lacp", "l - esteja constituída", "I - esteja constituída", "I -", "as art. 1 I"),
]
B8.SPAN_FIX[:] = [
    ((_CTB, "art-282-a", "§ 5º", "", 0), {"skip": True},
     "Código de Trânsito art. 282-A: Planalto prints a bare label line '§ 5º (Vide Lei nº 14.440, de 2022) (Vigência)' "
     "where Lei 14.440/2022 adds a § 5º from 1.1.2027 (its art. 7 I, with the new caput); the label line is left out, "
     "and Lei 14.440's 2027 wording of art. 282-A caput and § 5º, which Planalto's page does not print, is not in the "
     "history"),
    ((_CTB, "art-312-a", "IV -", "IV - outras atividades relacionadas ao resgate", 0),
     {"end": "2023-06-20", "end_law": "lei-14599-2023", "end_how": "successor"},
     "Código de Trânsito art. 312-A IV in Lei 13.281/2016's wording is printed unstruck above the wording 'Redação dada "
     "pela Lei nº 14.599, de 2023' that replaced it; it ends with that law (as II and III above it)"),

    ((_A, "art-01", "III -", "III - a bens e direitos", 0), {"skip": True}, _W53),
    ((_A, "art-01", "III -", "III - a bens e direitos", 1), {"start": "1985-07-25", "start_law": None}, _W53),
    ((_A, "art-01", "III -", "III - à ordem urbanística", 0), {"skip": True}, _W53),
    ((_A, "art-01", "IV -", "IV - a qualquer outro", 0), {"skip": True}, _W53),
    ((_A, "art-01", "IV -", "IV - a qualquer outro", 1), {"start": "1991-03-11", "start_law": "lei-8078-1990"}, _W53),
    ((_A, "art-01", "IV -", "IV - a bens e direitos", 0), {"skip": True}, _W53),
    ((_A, "art-01", "V -", "V - por infração da ordem econômica.", 0),
     {"end": "2001-08-27", "end_law": "mp-2180-2001", "end_how": "successor"}, _W53),
    ((_A, "art-01", "V -", "V - a qualquer outro", 0), {"skip": True}, _W53),
    ((_A, "art-01", "V -", "V - por infração da ordem econômica e da economia popular", 0),
     {"start": "2001-08-27", "start_law": "mp-2180-2001"}, _W53),
    ((_A, "art-01", "VI -", "VI - por infração da ordem econômica", 0), {"skip": True}, _W53),

    (("lei-de-licitacoes-de-1993", "art-021", "V -", "V - 5 (cinco) dias úteis para o convite.", 0),
     {"end": "1994-06-09", "end_law": "lei-8883-1994", "end_how": "recast"},
     "Lei 8.666 art. 21 § 2º V as enacted ('V - 5 (cinco) dias úteis para o convite.') is printed struck with no note; Lei "
     "8.883/1994 recast § 2º into incisos I to IV, the convite's period becoming inciso IV ('IV - cinco dias úteis para "
     "convite.'), so it ends with that law (in force 9.6.1994)"),
]
_W36B = ("LDB art. 36-B: Lei 14.645/2023 (in force 3.8.2023) renumbered the Parágrafo único as § 1º and added §§ 2º and "
         "3º; Planalto prints the struck Parágrafo único with its incisos I to III and then the § 1º with the same incisos, "
         "unstruck and with Lei 11.741/2008's note, so these start with the renumbering, when the struck copies end")
B8.SPAN_FIX += [
    (("lei-de-diretrizes-e-bases-da-educacao", "art-36-b", lab, start, 1),
     {"start": "2023-08-03", "start_law": "lei-14645-2023"}, _W36B)
    for lab, start in (("I -", "I - os objetivos e definições"), ("II -", "II - as normas complementares"),
                       ("III -", "III - as exigências de cada instituição"))
]
# Código Florestal
_CF = "codigo-florestal"
B8.COURT_SPLIT[:] = [("cflo", "art-03", "b)", "")]
_WADC42 = ("Código Florestal art. 3 VIII b): STF, ADC 42, ADI 4.903 and ADI 4.937 (Plenário, judgment concluded 28.2.2018, "
           "Informativo STF 892) declared unconstitutional the expressions 'gestão de resíduos' and 'instalações "
           "necessárias à realização de competições esportivas estaduais, nacionais ou internacionais'; Planalto strikes "
           "them inside the line. The history drops them from 28.2.2018, the judgment day (the DJe day of the session's ata "
           "is not in the records read), credited to the ruling")
P.COURTS = {
    "stf-adc-42": {
        "label": "STF, ADC 42 (with ADI 4.903 and 4.937)", "kind": "court", "enacted": "2018-02-28",
        "published": "2018-02-28",
        "title": "Ação declaratória de constitucionalidade 42 (julgada com as ADI 4.901, 4.902, 4.903 e 4.937): declara "
                 "inconstitucionais as expressões 'gestão de resíduos' e 'instalações necessárias à realização de "
                 "competições esportivas estaduais, nacionais ou internacionais' do art. 3º, VIII, b, da Lei nº 12.651, de "
                 "2012",
        "url": "https://www.stf.jus.br/arquivo/informativo/documento/informativo892.htm",
        "from": "2018-02-28", "case": r"ADC\s*N?º?\s*42", "where": [], "why": _WADC42},
}
_LRP = "lei-de-registros-publicos"
_W2220 = ("Lei de Registros Públicos art. 167 I items 28 and 37: Lei 10.257/2001 (enacted 10.7.2001, in force 9.10.2001) "
          "arts. 55 and 56 gave item 28 and added item 37 with the words 'independente da regularidade do parcelamento do "
          "solo ou da edificação'; Medida Provisória nº 2.220/2001 (DOU 5.9.2001, edição extra, in force on publication; "
          "kept in force by Emenda Constitucional 32/2001 art. 2), the later act, gave both items their wording without "
          "those words, which Planalto prints as today's. Lei 10.257's wordings never stood and are left out")
B8.SPAN_FIX += [
    ((_LRP, "art-167", "28)", "28) das sentenças declaratórias de usucapião;", 0),
     {"end": "2001-09-05", "end_law": "mp-2220-2001", "end_how": "successor"}, _W2220),
    ((_LRP, "art-167", "28)", "28) das sentenças declaratórias de usucapião, independente", 0), {"skip": True}, _W2220),
    ((_LRP, "art-167", "37)", "37) dos termos administrativos ou das sentenças declaratórias da concessão de uso especial "
                              "para fins de moradia, independente", 0), {"skip": True}, _W2220),
    ((_LRP, "art-288-a", "§ 2º", "§ 2º As matrículas das áreas destinadas a uso público", 1),
     {"start": "2011-06-17", "start_law": "lei-12424-2011"},
     "Lei de Registros Públicos art. 288-A § 2º: Planalto prints the paragraph twice, once with Medida Provisória nº "
     "514/2010's wording and again, word for word, inside the article as its conversion law Lei 12.424/2011 worded it, "
     "with the MP's note; the second copy starts with the conversion law, when the first ends"),
    ((_CF, "art-03", "b)", "b) as obras de infraestrutura destinadas às concessões", 0),
     {"end": "2018-02-28", "end_law": "stf-adc-42", "end_how": "court"}, _WADC42),
    ((_CF, "art-03", "b)", "b) as obras de infraestrutura destinadas às concessões", 1),
     {"start": "2018-02-28", "start_law": "stf-adc-42"}, _WADC42),
]
# Lei de Registros Públicos
P.VIGENCIA_FIXED.update({
    "mp-1085-2021": ("2021-12-28", "'Esta Medida Provisória entra em vigor: I - em 1º de janeiro de 2024, quanto ao art. 11 "
                                   "na parte em que altera o art. 130 da Lei nº 6.015, de 1973; e II - na data de sua "
                                   "publicação, quanto aos demais dispositivos' (DOU 28.12.2021); inciso I is printed "
                                   "struck (its conversion law, Lei 14.382/2022, did not keep it), so its changes to the "
                                   "Lei de Registros Públicos are dated 28.12.2021"),
    "lei-14382-2022": ("2022-06-28", "art. 21: 'Esta Lei entra em vigor: I - em 1º de janeiro de 2024, quanto ao art. 11, na "
                                     "parte em que altera o art. 130 da Lei nº 6.015, de 31 de dezembro de 1973 (Lei de "
                                     "Registros Públicos); e II - na data de sua publicação, quanto aos demais dispositivos' "
                                     "(DOU 28.6.2022); only its new wording of Lei 6.015 art. 130 is dated 1.1.2024"),
    "lei-9534-1997": ("1998-03-11", "'Esta Lei entra em vigor no prazo de noventa dias, contado da data de sua publicação' "
                                    "(DOU 11.12.1997): 11.3.1998"),
    "lei-6140-1974": ("1975-07-01", "art. 2: 'A presente Lei entrará em vigor a 1º de julho de 1975' (DOU 29.11.1974); "
                                    "before the Lei de Registros Públicos itself was in force, so its changes are part of "
                                    "the act's first day"),
})
P.VIGENCIA_PROVISION[("lei-14382-2022", _LRP, "art-130")] = (
    "2024-01-01", "Lei 14.382/2022 art. 21 I: its art. 11's change to Lei 6.015 art. 130 in force on 1.1.2024")
P.MP_LAPSE.update({
    "mp-922-2020": ("2020-06-30", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 72, de 2020 (DOU "
                                  "1.7.2020): 'teve seu prazo de vigência encerrado no dia 29 de junho de 2020'"),
    "mp-700-2015": ("2016-05-18", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 23, de 2016 (DOU "
                                  "19.5.2016): 'teve seu prazo de vigência encerrado no dia 17 de maio'"),
})
P.MP_PENDING.update({
    "mp-2220-2001": "Medida Provisória nº 2.220, de 4.9.2001 (DOU 5.9.2001, edição extra) was in force on 11.9.2001, so it "
                    "stays in force until a later MP revokes it or Congress votes on it (Emenda Constitucional 32/2001, "
                    "art. 2)",
    "mp-2187-2001": "Medida Provisória nº 2.187-13, de 24.8.2001 (DOU 27.8.2001) was in force on 11.9.2001, so it stays in "
                    "force until a later MP revokes it or Congress votes on it (Emenda Constitucional 32/2001, art. 2)",
})
P.MP_LAPSE["mp-867-2018"] = ("2019-06-04", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 35, de 2019 (DOU "
                                           "5.6.2019): 'teve seu prazo de vigência encerrado no dia 3 de junho do corrente "
                                           "ano'")
# a parenthesis inside the text read as a note (Código Florestal art. 74: '... com a redação dada pela Medida Provisória nº
# 2.216-37 ...' is law text): (pages, line start, note start) -> the note is put back into the line
NOTE_INTO_TEXT: list[tuple[tuple[str, ...], str, str, str]] = [
    (("cflo", "cflo-compilado"), "Art. 74. A Câmara de Comércio Exterior", "(redação dada pela Medida Provisória nº 2.216-37",
     "Código Florestal art. 74: the words '(redação dada pela Medida Provisória nº 2.216-37, de 31 de agosto de 2001, é "
     "autorizada a adotar medidas [...])' are the article's own text ('... da Lei nº 9.649, de 27 de maio de 1998, com a "
     "redação dada pela Medida Provisória nº 2.216-37 [...], é autorizada a adotar ...'); the page sets them in a way "
     "the parser read as a note, so they are put back into the line"),
]
NOTE_INTO_USED: list[str] = []
# words the annotated page misprints in an unstruck line, corrected from the amending law's own text (and Planalto's
# consolidated page): (page, wrong words, right words, why)
WORD_FIX: list[tuple[str, str, str, str]] = [
    ("lrp", "inclusive para as terras devolutas a ele transferidas em razão de legislação",
     "inclusive para as terras devolutas transferidas ao Município em razão de legislação",
     "Lei de Registros Públicos art. 195-A § 7º: the annotated page prints, under the note 'Incluído pela Lei nº 13.465, de "
     "2017', 'as terras devolutas a ele transferidas em razão de legislação'; Lei 13.465/2017's own text (and Planalto's "
     "consolidated page, and the wording of Medida Provisória nº 759/2016 it converted) reads 'as terras devolutas "
     "transferidas ao Município em razão de legislação', which the history uses"),
]
_paragraphs9 = P.paragraphs


def paragraphs(html, digits):
    out, rest = _paragraphs9(html, digits)
    page = B8.CURRENT_PAGE[0]
    for p in out:
        for pg, wrong, right, why in WORD_FIX:
            if pg == page and p["state"] == "plain" and wrong in p["text"]:
                p["text"] = p["text"].replace(wrong, right)
                NOTE_INTO_USED.append(why)
        for pages, start, note, why in NOTE_INTO_TEXT:
            if page in pages and p["text"].startswith(start):
                hit = [n for n in p["notes"] if n.startswith(note)]
                if hit:
                    p["text"] = P.norm(p["text"] + " " + hit[0][1:-1].rstrip())
                    if p.get("plain_text"):
                        p["plain_text"] = p["text"]
                    p["notes"] = [n for n in p["notes"] if n != hit[0]]
                    NOTE_INTO_USED.append(why)
    return out, rest


P.paragraphs = B.paragraphs = paragraphs
_Q = B7._QUOTED
B8.LAW_FIELD_FIX.update({
    "lei-12529-2011": ({"published": "2011-12-01"},
                       "Lei 12.529/2011: its page prints 'publicado no DOU de 1º.11.2011' for a law of 30.11.2011; it was "
                       "published in the DOU of 1.12.2011 (retificado 2.12.2011), so its own art. 128 ('Esta Lei entra em "
                       "vigor após decorridos 180 (cento e oitenta) dias de sua publicação oficial') puts it in force on "
                       "29.5.2012 (LC 95/1998 art. 8 § 1)"),
})
P.VIGENCIA_FIXED["lei-12529-2011"] = ("2012-05-29", "art. 128: 180 days after publication in the DOU of 1.12.2011 (the page "
                                                    "prints 1º.11.2011 by mistake): 29.5.2012")
B.EXPLAINED.update({
    "codigo-florestal": {"art-80": _Q.format(x="§ 1º.")},
    "lei-de-registros-publicos": {
        "art-054": "typesetting: '7º Os nomes' (annotated) / '7º) Os nomes' (consolidated), a line inside the quoted text of "
                   "an amendment",
        "art-066": "the annotated page prints 'residênci a' (a stray space inside the word), kept as printed; the "
                   "consolidated page 'residência'",
        "art-167": "the consolidated page keeps the placeholders '13)', '22)', '25.' and '33.' for items revoked or of a "
                   "lapsed Medida Provisória, and a full stop after 'regime fiduciário'; the history leaves revoked text out",
        "art-213": "typesetting: a full stop at the end of a line on the consolidated page only",
        "art-216-a": "typesetting: '(Código de Processo Civil);' (annotated) / '(Código de Processo Civil;' (consolidated)",
        "art-265": "typesetting: 'nº 3.200' (annotated) / 'n. 3.200' (consolidated)",
        "art-289": "the consolidated page prints the heading 'Das Disposições Finais e Transitórias' inside art. 289",
        "art-290": "typesetting: 'Art. 290..' (consolidated) / 'Art. 290.' (annotated)",
    },
    "lei-da-acao-civil-publica": {
        "art-01": "the consolidated page prints the numerals of incisos I and II with the letter l ('l -', 'll -') too; the "
                  "history reads them as I and II (see the label decision)",
        "art-05": "typesetting: the consolidated page prints 'ação cautelar:.' (colon and full stop); the annotated page "
                  "'ação cautelar:'",
    },
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

# ---------------------------------------------------------------------------------------------------------------
# Acts repealed as a whole: the act's last version removes every unit, on the repeal day, credited to the repealing law.
# Their page is read from a capture before the repeal (Planalto strikes the whole page afterwards), and the replay check
# compares the last version before the repeal with that capture's unstruck text.
REPEALS: dict[str, tuple[str, str, str]] = {
    "lei-de-licitacoes-de-1993": (
        "2023-12-30", "lei-14133-2021",
        "Lei 8.666/1993 was repealed as a whole by Lei 14.133/2021 art. 193 II, in the wording Lei Complementar 198/2023 "
        "gave it ('Revogam-se: [...] II - em 30 de dezembro de 2023: a) a Lei nº 8.666, de 21 de junho de 1993'; the "
        "first wording set two years from 1.4.2021, Medida Provisória 1.167/2023 and then LC 198/2023 moved it), so its "
        "last version, on 30.12.2023, removes every provision, credited to Lei 14.133/2021. Its arts. 89 to 108 had been "
        "revoked on 1.4.2021 (art. 193 I). After the repeal Planalto strikes the whole page, so the page is read from a "
        "capture of 20.11.2023, before the repeal, and the history up to 29.12.2023 is checked against that capture's "
        "unstruck text"),
}
REPEAL_CHECK: list[str] = []
# acts never in force as enacted, whose first day carries the changes of laws made before it: (version note, decision)
FOLD_EARLY: dict[str, tuple[str, str]] = {
    "lei-de-registros-publicos": (
        "The text in force on 1 January 1976, as republished in the DOU of 16 September 1975 with the changes of Leis "
        "6.064/1974, 6.140/1974 and 6.216/1975; the 1973 text never took effect.",
        "Lei de Registros Públicos: the act as enacted (DOU 31.12.1973) never took effect: its start was moved from "
        "1.7.1974 to 1.7.1975 (Lei 6.064/1974) and then to 1.1.1976 (Lei 6.216/1975, published 1.7.1975), and Lei 6.216 "
        "art. 2 had the act republished with its changes (DOU 16.9.1975, Suplemento). Its first version is the text in "
        "force on 1.1.1976, as republished, credited to Lei 6.015/1973 and noted as including the changes of Leis "
        "6.064/1974, 6.140/1974 and 6.216/1975 (Planalto's page prints those changes over the 1973 text); there is no "
        "version of the 1973 text"),
}
FOLD_USED: list[str] = []
_lifespans9 = P.lifespans


def lifespans(paras, cx):
    problems = _lifespans9(paras, cx)
    if cx.act in REPEALS:
        day, law, _ = REPEALS[cx.act]
        for p in paras:
            if not p.get("skip") and (p["end"] is None or p["end"] > day) and p["start"] < day and not (
                    p["state"] != "plain" and p["end"] is None and not p.get("pinned")):
                p["end"], p["end_law"], p["end_how"], p["pinned"] = day, law, "act-repealed", True
    return problems


P.lifespans = B.lifespans = lifespans
_build_act9 = P.build_act
_consolidated9 = P.consolidated


def build_act(paras, act_day, gate, gate_law, unit_label):
    slug = ACTS[len(B7._act_order)]["slug"] if len(B7._act_order) < len(ACTS) else "?"
    versions = _build_act9(paras, act_day, gate, gate_law, unit_label)
    if slug in FOLD_EARLY and len(versions) > 1 and versions[1].get("same_day"):
        # the act as enacted never took effect: its first version is the text in force on its first day
        versions = versions[1:]
        versions[0].pop("same_day", None)
        versions[0]["credits"] = {}
        versions[0]["note"] = FOLD_EARLY[slug][0]
        FOLD_USED.append(FOLD_EARLY[slug][1])
    if slug in REPEALS:
        act = next(a for a in ACTS if a["slug"] == slug)
        before = [v for v in versions if v["from"] < REPEALS[slug][0]][-1]["units"]
        diffs = P.compare({u: x["text"] for u, x in before.items()}, _consolidated9(act["consolidated"], act["digits"]))
        REPEAL_CHECK.append(f"{act['short']}: the last version before the repeal ({[v for v in versions if v['from'] < REPEALS[slug][0]][-1]['from']}) "
                            f"differs from the unstruck text of the pre-repeal capture of Planalto's page in {len(diffs)} "
                            f"articles" + (": " + "; ".join(diffs) if diffs else ""))
        print("REPEAL CHECK", REPEAL_CHECK[-1][:300])
    return versions


def consolidated(ident: str, digits: int):
    # a repealed act has no text today: its replay check is the pre-repeal one above
    if any(a["consolidated"] == ident and a["slug"] in REPEALS for a in ACTS):
        return {}
    return _consolidated9(ident, digits)


P.build_act = B.build_act = build_act
P.consolidated = B.consolidated = consolidated
_inner9 = B6.PB5B._write_part5


def _inner(*a) -> int:
    if NOTE_INTO_USED:
        B5.EXTRA_DECISIONS.append("Text corrections (a note read into its line; misprinted words corrected from the "
                                  "amending law): " + "; ".join(dict.fromkeys(NOTE_INTO_USED)) + ".")
    for slug, (_, _, why) in REPEALS.items():
        if any(x["slug"] == slug for x in ACTS):
            B5.EXTRA_DECISIONS.append(why + ".")
    B5.EXTRA_DECISIONS.extend(x + "." for x in REPEAL_CHECK)
    B5.EXTRA_DECISIONS.extend(x + "." for x in dict.fromkeys(FOLD_USED))
    return _inner9(*a)


B6.PB5B._write_part5 = _inner

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
