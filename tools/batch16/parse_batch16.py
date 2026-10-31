"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch16<x>.json (SCHEMA.md corpus parts): more major federal
acts not yet in the corpus, in small parts of 2-4 acts each (99-batch16a, 99-batch16b, ...).

    BATCH16_PART=a python -X utf8 scripts/brazil-law/batch16/parse_batch16.py [--stats] [--dry]

Imports ../batch15/parse_batch15.py (which configures batch 14 and everything below it, plus batch 15's hand tables and
the Medida Provisória 905/955 model) with no act of its own, and replaces only the configuration: the acts, the in-force
days, the hand tables for these acts, the pins and the output. Earlier parts are not touched. No network.

BATCH16_PART selects the part (its acts are PARTS[part]); BATCH16_ACTS=<slug,...> selects acts for trial runs
(BATCH16_OUT=<file> writes elsewhere). After writing a part run ../effects_fix.py on it (effect days).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
os.environ["BATCH15_PART"] = "-"   # batch 15 configures no act of its own here
os.environ.pop("BATCH15_ACTS", None)
os.environ.pop("BATCH15_OUT", None)
sys.path.insert(0, str(FOLDER / "batch15"))
import parse_batch15 as B15  # noqa: E402

B14, B13, B12, B11, B10, B9, B8, B7, B6, B5, B, P = (B15.B14, B15.B13, B15.B12, B15.B11, B15.B10, B15.B9, B15.B8, B15.B7,
                                                     B15.B6, B15.B5, B15.B, B15.P)
PL = P.PL
PART = os.environ.get("BATCH16_PART", "a")
B5.OUT = Path(os.environ.get("BATCH16_OUT") or FOLDER / "corpus.d" / f"99-batch16{PART}.json")
B5.STAGE = HERE / ".tmp" / "stage.json"

PAGES = dict(B15.PAGES)
PAGES.update({
    # batch 13's deferred acts (their page ids as pinned in batch13/sources_batch13.json)
    "l4320": "leis/l4320.htm",
    "l4320-compilado": "leis/l4320compilado.htm",
    "lfgts": "leis/l8036consol.htm",
    "lfgts-compilada": "leis/l8036compilada.htm",
    # part d
    "l9455": "leis/l9455.htm",
    "l2889": "leis/l2889.htm",
    "l13300": "_ato2015-2018/2016/lei/l13300.htm",
    "l9507": "leis/l9507.htm",
    # part e
    "l6001": "leis/l6001.htm",
    "l5764": "leis/l5764.htm",
    "l8629": "leis/l8629.htm",
    # part f
    "l8629-compilado": "leis/l8629compilado.htm",
    # part f
    "l7998": "leis/l7998.htm",
    "l7998-compilado": "leis/l7998compilado.htm",
    "l13019": "_ato2011-2014/2014/lei/l13019.htm",
    "l13019-compilado": "_ato2011-2014/2014/lei/l13019compilado.htm",
})
B.PAGES.clear()
B.PAGES.update(PAGES)
for M in (B5, B6, B7, B8, B9, B10, B11, B12, B13, B14, B15):
    M.PAGES = PAGES

_CBA, _L4320, _FGTS = "codigo-brasileiro-de-aeronautica", "lei-4320-de-1964", "lei-do-fgts"
_act = B14._act
ALL_ACTS: list[dict] = ([a for a in B14.ALL_ACTS if a["slug"] == _CBA]
                        + [a for a in B13.ALL_ACTS if a["slug"] in (_L4320, _FGTS)] + [
    _act("lei-de-tortura", "LTort", "l9455", "l9455", "lei-9455-1997",
         "Lei de Tortura (Lei nº 9.455, de 7 de abril de 1997)", 2),
    _act("lei-do-genocidio", "LGen", "l2889", "l2889", "lei-2889-1956",
         "Crime de genocídio (Lei nº 2.889, de 1º de outubro de 1956)", 2),
    _act("lei-do-mandado-de-injuncao", "LMI", "l13300", "l13300", "lei-13300-2016",
         "Lei do Mandado de Injunção (Lei nº 13.300, de 23 de junho de 2016)", 2),
    _act("lei-do-habeas-data", "LHD", "l9507", "l9507", "lei-9507-1997",
         "Lei do Habeas Data (Lei nº 9.507, de 12 de novembro de 1997)", 2),
    _act("estatuto-do-indio", "EInd", "l6001", "l6001", "lei-6001-1973",
         "Estatuto do Índio (Lei nº 6.001, de 19 de dezembro de 1973)", 2),
    _act("lei-das-cooperativas", "LCoop", "l5764", "l5764", "lei-5764-1971",
         "Lei das Cooperativas (Lei nº 5.764, de 16 de dezembro de 1971)", 3),
    _act("lei-da-reforma-agraria", "LRA", "l8629", "l8629-compilado", "lei-8629-1993",
         "Lei da Reforma Agrária (Lei nº 8.629, de 25 de fevereiro de 1993)", 2),
    _act("lei-do-seguro-desemprego", "LSD", "l7998", "l7998-compilado", "lei-7998-1990",
         "Lei do Seguro-Desemprego e do FAT (Lei nº 7.998, de 11 de janeiro de 1990)", 2),
    _act("marco-regulatorio-das-oscs", "MROSC", "l13019", "l13019-compilado", "lei-13019-2014",
         "Marco Regulatório das Organizações da Sociedade Civil (Lei nº 13.019, de 31 de julho de 2014)", 2),
])
PARTS: dict[str, list[str]] = {
    "a": [_CBA],
    "b": [_FGTS],
    "c": [_L4320],
    "d": ["lei-de-tortura", "lei-do-genocidio", "lei-do-mandado-de-injuncao", "lei-do-habeas-data"],
    "e": ["estatuto-do-indio", "lei-das-cooperativas", "lei-da-reforma-agraria"],
    "f": ["lei-do-seguro-desemprego"],
    "g": ["marco-regulatorio-das-oscs"],
}
VERIFIED: list[str] = PARTS.get(PART, [])
ENABLED = [s for s in os.environ.get("BATCH16_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
for M in (B7, B8, B9, B10, B11, B12, B13, B14, B15):
    M.ACTS[:] = ACTS
_PUB = "'Esta Lei entra em vigor na data de sua publicação'"
_L = B._act_law
ACT_DAY_ALL = {**B13.ACT_DAY_ALL, **B14.ACT_DAY_ALL,
    "lei-9455-1997": ("1997-04-08", f"Lei 9.455/1997 art. 3: {_PUB} (DOU 8.4.1997)"),
    "lei-2889-1956": ("1956-11-16", "Lei 2.889/1956 has no vigência clause: LINDB art. 1, 45 days after publication in the "
                                    "DOU of 2.10.1956"),
    "lei-13300-2016": ("2016-06-24", f"Lei 13.300/2016 art. 15: {_PUB} (DOU 24.6.2016)"),
    "lei-9507-1997": ("1997-11-13", f"Lei 9.507/1997 art. 22: {_PUB} (DOU 13.11.1997)"),
    "lei-6001-1973": ("1973-12-21", "Lei 6.001/1973 art. 68: 'Esta Lei entrará em vigor na data de sua publicação' (DOU "
                                    "21.12.1973)"),
    "lei-5764-1971": ("1971-12-16", "Lei 5.764/1971 art. 117: 'Esta Lei entrará em vigor na data de sua publicação' (DOU "
                                    "16.12.1971)"),
    "lei-8629-1993": ("1993-02-26", f"Lei 8.629/1993 art. 27: {_PUB} (DOU 26.2.1993)"),
    "lei-7998-1990": ("1990-01-12", f"Lei 7.998/1990 art. 31: {_PUB} (DOU 12.1.1990)"),
    "lei-13019-2014": ("2016-01-23", "Lei 13.019/2014 art. 88 as worded by Lei 13.204/2015: 'Esta Lei entra em vigor após "
                                     "decorridos quinhentos e quarenta dias de sua publicação oficial, observado o disposto "
                                     "nos §§ 1º e 2º deste artigo' (DOU 1.8.2014; the 540th day counted from publication is "
                                     "22.1.2016, LC 95/1998 art. 8 § 1); its § 1º: 'Para os Municípios, esta Lei entra em "
                                     "vigor a partir de 1º de janeiro de 2017' (§ 2º: earlier by local act). The original "
                                     "term (90 days) was extended by MP 658/2014 and Lei 13.102/2015 (360 days) and MP "
                                     "684/2015 (540 days) before it ran out"),
}
ACT_LAWS_ALL = {**B13.ACT_LAWS_ALL, **B14.ACT_LAWS_ALL,
    "lei-9455-1997": _L("Lei nº 9.455, de 1997", "Define os crimes de tortura e dá outras providências.", "1997-04-07",
                        "1997-04-08", PAGES["l9455"]),
    "lei-2889-1956": _L("Lei nº 2.889, de 1956", "Define e pune o crime de genocídio.", "1956-10-01", "1956-10-02",
                        PAGES["l2889"]),
    "lei-13300-2016": _L("Lei nº 13.300, de 2016", "Disciplina o processo e o julgamento dos mandados de injunção "
                         "individual e coletivo e dá outras providências.", "2016-06-23", "2016-06-24", PAGES["l13300"]),
    "lei-9507-1997": _L("Lei nº 9.507, de 1997", "Regula o direito de acesso a informações e disciplina o rito processual "
                        "do habeas data.", "1997-11-12", "1997-11-13", PAGES["l9507"]),
    "lei-6001-1973": _L("Lei nº 6.001, de 1973", "Dispõe sobre o Estatuto do Índio.", "1973-12-19", "1973-12-21",
                        PAGES["l6001"]),
    "lei-5764-1971": _L("Lei nº 5.764, de 1971", "Define a Política Nacional de Cooperativismo, institui o regime jurídico "
                        "das sociedades cooperativas, e dá outras providências.", "1971-12-16", "1971-12-16",
                        PAGES["l5764"]),
    "lei-8629-1993": _L("Lei nº 8.629, de 1993", "Dispõe sobre a regulamentação dos dispositivos constitucionais relativos à "
                        "reforma agrária, previstos no Capítulo III, Título VII, da Constituição Federal.", "1993-02-25",
                        "1993-02-26", PAGES["l8629"]),
    "lei-7998-1990": _L("Lei nº 7.998, de 1990", "Regula o Programa do Seguro-Desemprego, o Abono Salarial, institui o Fundo de "
                        "Amparo ao Trabalhador (FAT), e dá outras providências.", "1990-01-11", "1990-01-12", PAGES["l7998"]),
    "lei-13019-2014": _L("Lei nº 13.019, de 2014", "Estabelece o regime jurídico das parcerias voluntárias, envolvendo ou não "
                         "transferências de recursos financeiros, entre a administração pública e as organizações da "
                         "sociedade civil, em regime de mútua cooperação, para a consecução de finalidades de interesse "
                         "público; define diretrizes para a política de fomento e de colaboração com organizações da "
                         "sociedade civil; institui o termo de colaboração e o termo de fomento; e altera as Leis nºs 8.429, "
                         "de 2 de junho de 1992, e 9.790, de 23 de março de 1999.", "2014-07-31", "2014-08-01",
                         PAGES["l13019"]),
}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# earlier batches' printed-everywhere lists emptied (their act-keyed tables do nothing here)
P.COURTS.clear()
P.NOTE_FIX = {}
B9.REPEALS.clear()
EXTRA: list[str] = []   # decisions added to the part

# ---------------------------------------------------------------------------------------------------------------
# Código Brasileiro de Aeronáutica (Lei 7.565/1986), part a
P.VIGENCIA_FIXED["mp-1089-2021"] = (
    "2021-12-30", "art. 6: 'Esta Medida Provisória entra em vigor: I - após noventa dias da sua publicação, quanto ao Anexo; e "
                  "II - na data de sua publicação, quanto aos demais dispositivos' (DOU 30.12.2021): its changes to the Código "
                  "Brasileiro de Aeronáutica fall under II (the Anexo is Lei 11.182/2005's fee table)")
P.MP_LAPSE["mp-1240-2024"] = (
    "2024-11-07", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 112, de 2024 (DOU 14.11.2024): 'teve seu "
                  "prazo de vigência encerrado no dia 6 de novembro de 2024'")
_W181 = ("CBA arts. 181 and 182: Medida Provisória 714/2016 (2.3.2016) gave art. 181 a new caput, incisos I-II and §§ 3º-6º and "
         "revoked art. 181 III and art. 182; Lei 13.319/2016, its conversion (26.7.2016), vetoed its art. 181 ('Art. 181. "
         "(VETADO) [...] § 5º (VETADO). § 6º (VETADO).') and kept none of the revocations, so the 1986 text of both articles "
         "is in force again from 26.7.2016 until Medida Provisória 863/2018 (13.12.2018). Planalto prints these 1986 "
         "wordings a second time below MP 714's (struck, with MP 863's notes); they start on 26.7.2016, credited to Lei "
         "13.319, and the MP 714 caput ends then")
_W303 = ("CBA art. 303 § 2º: the 1986 wording ('§ 2º A autoridade mencionada no parágrafo anterior [...]') is printed struck "
         "below the § 2º Lei 9.614/1998 inserted, which renumbered it § 3º ('Renumerado do § 2º para § 3º com nova "
         "redação'); it stands from 1986 to 6.3.1998")
_RESTORE_181 = {"start": "2016-07-26", "start_law": "lei-13319-2016", "restored": True}
B8.SPAN_FIX += [
    ((_CBA, "art-181", "Art. 181", "Art. 181. A concessão ou autorização somente será dada", 0),
     {"end": "2016-07-26", "end_law": "lei-13319-2016", "end_how": "conversion"}, _W181),
    ((_CBA, "art-181", "Art. 181", "Art. 181. A concessão somente será dada", 1),
     dict(_RESTORE_181, end="2018-12-13", end_law="mp-863-2018", end_how="successor"), _W181),
    *[((_CBA, unit, lab, pre, 1), _RESTORE_181, _W181) for unit, lab, pre in [
        ("art-181", "I -", "I - sede no Brasil"), ("art-181", "II -", "II - pelo menos 4/5"),
        ("art-181", "III -", "III - direção confiada"), ("art-182", "Art. 182", "Art. 182. A autorização pode ser outorgada"),
        ("art-182", "I -", "I - às sociedades anônimas"), ("art-182", "II -", "II - às demais sociedades"),
        ("art-182", "Parágrafo único", "Parágrafo único. Em se tratando de serviços aéreos especializados")]],
    ((_CBA, "art-303", "§ 2º", "§ 2º A autoridade mencionada no parágrafo anterior", 0),
     {"start": "1986-12-23", "start_law": None, "end": "1998-03-06", "end_law": "lei-9614-1998", "end_how": "successor"},
     _W303),
]
B.EXPLAINED[_CBA] = {
    "art-184": "the consolidated page prints arts. 184 to 186 as one line ('Art. 184 a 186 (Revogado pela Lei nº 13.842, de "
               "2019) e (Revogado pela Lei nº 14.368, de 2022)'); the annotated page strikes each article (revoked by "
               "Medida Provisória 863/2018, 13.12.2018)",
    "art-197": "the consolidated page drops a word ('exames de proficiência de e aeroviários'); the annotated page reads "
               "'exames de proficiência de aeronautas e aeroviários'",
    "art-270": "the consolidated page drops the § sign of § 2º ('2° O saldo de 70% [...]'); the annotated page prints '§ 2°'",
    "titulos": "the consolidated page still prints the headings of divisions revoked by Medida Provisória 1.089/2021 and Lei "
               "14.368/2022 (Título III Capítulo V Seção II, Título IV Capítulo IV Seção IV, Título VI Capítulo II "
               "'Serviços Aéreos Privados', Título VI Capítulo III Seções I-III, Capítulo VI) with a '(Revogado pela Lei nº "
               "14.368, de 2022)' note; the annotated page strikes them, and a revoked division has no heading",
}

# A dispositivo whose caput (or enclosing §) a Medida Provisória revoked as a whole: Planalto notes the MP's revocation on
# that line only, and on its incisos, parágrafos and alíneas only the conversion law's revocation ('Revogado pela Lei nº
# 14.368, de 2022'). They fall with the line above them on the MP's day (MP 1.089/2021 art. 4 IV m): 'os art. 73 a art. 76',
# n) 'a Seção II do Capítulo V do Título III', u) 'os art. 116 e art. 117').
CONV_CHILD_ACTS = {_CBA}
CONV_CHILD_USED: list[str] = []


def conv_children(paras, cx, record=True):
    if cx.act not in CONV_CHILD_ACTS:
        return
    for i, p in enumerate(paras):
        if p["heading"] or p["state"] == "plain" or p.get("skip") or p.get("end_how") != "note" or not p["end_law"]:
            continue
        lv = P.level(p["label"])
        if lv == 0:
            continue
        par = None
        for q in reversed(paras[:i]):
            if q["unit"] != p["unit"]:
                break
            if q["heading"] or q.get("skip") or P.level(q["label"]) >= lv:
                continue
            if q["start"] <= p["start"] and (q["end"] is None or q["end"] > p["start"]):
                par = q
                break
        if par is None or par["state"] == "plain" or not par["end"] or par["end"] >= p["end"]:
            continue
        fate = cx.mp.get(par["end_law"]) or {}
        if fate.get("converted") != p["end_law"]:
            continue
        if any(P.law_key(n, cx.mp.get("_years")) == par["end_law"] for n in p["notes"]):
            continue
        p["end"], p["end_law"], p["end_how"] = par["end"], par["end_law"], "parent"
        if record:
            CONV_CHILD_USED.append(f"{p['unit']} [{p['label']}]")


_lifespans16 = P.lifespans


_CX: list = [None]


def lifespans(paras, cx):
    problems = _lifespans16(paras, cx)
    _CX[0] = cx
    conv_children(paras, cx)
    return problems


_apply_rewrites16 = P.apply_rewrites


def apply_rewrites(paras, act, eff, problems):
    out = _apply_rewrites16(paras, act, eff, problems)
    if _CX[0] is not None and _CX[0].act == act["slug"]:
        conv_children(paras, _CX[0], record=False)
    if act["slug"] == _L4320:
        scheme_lines(paras)
    return out


P.lifespans = B.lifespans = lifespans
P.apply_rewrites = B.apply_rewrites = apply_rewrites

# ---------------------------------------------------------------------------------------------------------------
# Lei do FGTS (Lei 8.036/1990), part b
P.VIGENCIA_FIXED["lei-13932-2019"] = (
    "2019-12-12", "art. 15: 'Esta Lei entra em vigor: I - quanto aos §§ 8º e 9º do art. 5º e ao inciso I do § 6º-A do art. 9º "
                  "incluídos pelo art. 2º à Lei nº 8.036, de 11 de maio de 1990, a partir do dia 1º de janeiro de 2020; II - "
                  "quanto aos incisos XXI e XXII do caput do art. 20 incluídos pelo art. 2º à Lei nº 8.036 [...], após "
                  "decorridos 180 (cento e oitenta) dias de sua publicação; III - quanto aos demais dispositivos, na data de "
                  "sua publicação' (DOU 12.12.2019): I and II are dated by provision (1.1.2020; 9.6.2020, the day after the "
                  "180th day counted from publication, LC 95/1998 art. 8 § 1)")
_W13932 = ("Lei 13.932/2019 art. 15 I and II: art. 5 §§ 8º-9º (taxa de administração) are in force from 1.1.2020, and art. "
           "20 XXI-XXII from 9.6.2020 (180 days after publication on 12.12.2019); art. 20 XXI as Medida Provisória "
           "889/2019 had worded it (24.7.2019) ends when the conversion law gives the inciso its own wording (12.12.2019), so "
           "the inciso is absent from 12.12.2019 to 9.6.2020, as the clause defers it; art. 9 § 6º-A, also named in I, was "
           "vetoed")
B8.SPAN_FIX += [
    *[((_FGTS, "art-05", lab, pre, 0), {"start": "2020-01-01", "start_law": "lei-13932-2019", "by_provision": True}, _W13932)
      for lab, pre in [("§ 8º", "§ 8º A taxa de administração do FGTS"), ("§ 9º", "§ 9º A taxa de administração de que trata")]],
    *[((_FGTS, "art-20", lab, pre, n), {"start": "2020-06-09", "start_law": "lei-13932-2019", "by_provision": True}, _W13932)
      for lab, pre, n in [("XXI -", "XXI - a qualquer tempo, quando seu saldo for inferior a R$ 80,00 (oitenta reais) e não "
                                    "houver", 0),
                          ("XXII -", "XXII - quando o trabalhador ou qualquer de seus dependentes for", 0)]],
]
_W3 = ("Lei 8.036 art. 3: Planalto notes both later wordings of the caput 'Redação dada pela Lei nº 9.649, de 1998'; Lei "
       "9.649's own page shows that its art. 49 as enacted (27.5.1998) gave the caput with incisos I-VI ('integrado por três "
       "representantes da categoria dos trabalhadores [...]') and § 2º, and that Medida Provisória 2.216-37/2001 (DOU "
       "1.9.2001) rewrote art. 49 to give the caput its present wording ('composto por representação de trabalhadores, "
       "empregadores e órgãos e entidades governamentais') and § 5º ('maioria simples'), and revoked § 2º (noted on this "
       "page). So the 1998 caput and its incisos stand from 28.5.1998 to 1.9.2001, the present caput and § 5º from 1.9.2001 "
       "(credited to MP 2.216-37; earlier editions of that MP chain are not modelled), and the 1990 § 5º to 1.9.2001")
_W13 = ("Lei 8.036 art. 13 § 5º I: Lei 13.446/2017's wording is replaced by Medida Provisória 889/2019's (24.7.2019); Lei "
        "13.932/2019, the conversion, did not take up MP 889's § 5º and inciso I, and Planalto prints Lei 13.446's wording as "
        "today's text: it is out of force from 24.7.2019 to 12.12.2019")
_W23 = ("Lei 8.036 art. 23 § 2º: the 1990 caput and alíneas a)-b) give way to Medida Provisória 905/2019's § 2º (12.11.2019 to "
        "20.4.2020, and again on 18.8.2020) and stand again from 20.4.2020 to 18.8.2020 and from 19.8.2020 to Medida "
        "Provisória 1.107/2022 (18.3.2022). Alínea c) as Medida Provisória 889/2019 added it (24.7.2019) ends when MP 905's § 2º "
        "starts (12.11.2019); its wording by Lei 13.932/2019 (MP 889's conversion, 12.12.2019) belongs to the 1990 § 2º and "
        "stands while that paragraph is in force (from 20.4.2020 to 18.8.2020 and from 19.8.2020 to 18.3.2022). Planalto "
        "prints the 1990 alíneas, MP 889's c) and Lei 13.932's c) twice, before and after MP 905's text; the second copy of "
        "MP 889's c) is left out")
_MP905_GAP = ("2019-11-12", "2020-04-20", "mp-905-2019", "mp-955-2020")
B8.SPAN_FIX += [
    ((_FGTS, "art-03", "Art. 3º", "Art. 3º O FGTS será regido segundo normas e diretrizes estabelecidas por um Conselho "
                                  "Curador, integrado por três representantes da categoria dos trabalhadores", 0),
     {"end": "2001-09-01", "end_law": "mp-2216-2001", "end_how": "successor"}, _W3),
    *[((_FGTS, "art-03", lab, pre, 0), {"end": "2001-09-01", "end_law": "mp-2216-2001", "end_how": "parent"}, _W3)
      for lab, pre in [("I -", "I - Ministério do Trabalho"), ("II -", "II - Ministério do Planejamento"),
                       ("III -", "III - Ministério da Fazenda"), ("IV -", "IV - Ministério da Indústria"),
                       ("V -", "V - Caixa Econômica Federal"), ("VI -", "VI - Banco Central do Brasil")]],
    ((_FGTS, "art-03", "Art. 3º", "Art. 3º O FGTS será regido por normas e diretrizes", 0),
     {"start": "2001-09-01", "start_law": "mp-2216-2001"}, _W3),
    ((_FGTS, "art-03", "§ 5º", "§ 5º As decisões do Conselho serão tomadas com a presença, no mínimo", 0),
     {"end": "2001-09-01", "end_law": "mp-2216-2001", "end_how": "successor"}, _W3),
    ((_FGTS, "art-03", "§ 5º", "§ 5º As decisões do Conselho serão tomadas com a presença da maioria simples", 0),
     {"start": "2001-09-01", "start_law": "mp-2216-2001"}, _W3),
    ((_FGTS, "art-13", "I -", "I - a distribuição alcançará todas as contas vinculadas que apresentarem saldo positivo em 31 "
                              "de dezembro do exercício-base", 0),
     {"gaps": [("2019-07-24", "2019-12-12", "mp-889-2019", "lei-13932-2019")]}, _W13),
    *[((_FGTS, "art-23", lab, pre, 0), {"end": "2020-08-18", "end_law": "mp-955-2020-fim", "end_how": "mp-pair",
                                        "gaps": [_MP905_GAP], "skip": False}, _W23)
      for lab, pre in [("a)", "a) de 2 (dois) a 5 (cinco) BTN"), ("b)", "b) de 10 (dez) a 100 (cem) BTN")]],
    *[((_FGTS, "art-23", lab, pre, 1), {"start": "2020-08-19", "start_law": "mp-905-2019-fim", "restored": True}, _W23)
      for lab, pre in [("a)", "a) de 2 (dois) a 5 (cinco) BTN"), ("b)", "b) de 10 (dez) a 100 (cem) BTN")]],
    ((_FGTS, "art-23", "c)", "c) de R$100,00 (cem reais) a R$300,00 (trezentos reais) por trabalhador prejudicado na", 0),
     {"end": "2019-11-12", "end_law": "mp-905-2019", "end_how": "mp-pair"}, _W23),
    ((_FGTS, "art-23", "c)", "c) de R$100,00 (cem reais) a R$300,00 (trezentos reais) por trabalhador prejudicado na", 1),
     {"skip": True, "end_how": "duplicate"}, _W23),
    ((_FGTS, "art-23", "c)", "c) de R$ 100,00 (cem reais) a R$ 300,00 (trezentos reais) por trabalhador prejudicado, na "
                             "hipótese", 0),
     {"start": "2020-04-20", "start_law": "mp-955-2020", "end": "2020-08-18", "end_law": "mp-955-2020-fim",
      "end_how": "mp-pair", "gaps": [], "skip": False}, _W23),
    ((_FGTS, "art-23", "c)", "c) de R$ 100,00 (cem reais) a R$ 300,00 (trezentos reais) por trabalhador prejudicado, na "
                             "hipótese", 1),
     {"start": "2020-08-19", "start_law": "mp-905-2019-fim", "end": "2022-03-18", "end_law": "mp-1107-2022",
      "end_how": "successor", "gaps": [], "skip": False}, _W23),
]
B.EXPLAINED[_FGTS] = {
    "art-05": "the consolidated page drops the semicolon after alínea f) ('[...] por classe de ativo, observados os "
              "requisitos técnicos aplicáveis'; the annotated page prints ';'), reads the line 'XIV - (revogado);' (Lei 13.932/2019) as a "
              "note, and leaves the tail of a note in § 7º ('[...] final daquele exercício. 07, de 2022)')",
    "art-09": "the consolidated page is out of date for § 9º: it prints Medida Provisória 848/2018's wording ('Banco Nacional "
              "de Desenvolvimento Econômico e Social - BNDES [...] entidades hospitalares filantrópicas e sem fins "
              "lucrativos'), which Lei 13.778/2018, its conversion, replaced (the annotated page strikes MP 848's wording "
              "and prints Lei 13.778's); it also drops the semicolon after alínea f) ('hipoteca sobre imóvel de propriedade de "
              "terceiros')",
    "art-23": "the consolidated page prints stray characters before alínea c) of § 2º ('eee9c) de R$ 100,00 [...]') and reads "
              "the lines 'II - (revogado);', 'III - (revogado);' and 'a) (revogada);' (Lei 14.438/2022) as notes",
}
B13.OPEN_ITEMS[_FGTS] = (
    "Lei 8.036 (open items): Medidas Provisórias reissued before Emenda Constitucional 32/2001 (MP 2.164-41, 2.196-3, "
    "2.197-43, 2.216-37 and the chains before them) are dated by the edition Planalto's notes name, so changes their "
    "earlier editions made from 1998 are dated 2001; Medida Provisória 1.107/2022 and Lei 14.438/2022 defer the effects of "
    "their changes to arts. 13, 15 and 23 to the start of collection through the digital guide service (an event set by "
    "regulation, not a fixed day), so those changes are dated by the in-force day; the Anexo Lei 13.932/2019 added (the "
    "saque-aniversário table) is not part of the history; Planalto's 'Vide' pointers (ADI 2.736, RE 522.897, Lei "
    "Complementar 150/2015, later laws, MPs and decrees) strike no words and are not modelled")
P.MP_PENDING["mp-2216-2001"] = (
    "Medida Provisória nº 2.216-37, de 31.8.2001 (DOU 1.9.2001, in force on publication), kept in force by Emenda "
    "Constitucional 32/2001, art. 2; its art. 1 rewrote Lei 9.649/1998 art. 49, which gives Lei 8.036 art. 3 caput and § 5º "
    "their present wording, and revoked art. 3 § 2º. Earlier editions of the chain are not modelled")
B15.TEXT_FIX.append(("lfgts", "§ 9º § 9º A taxa", "§ 9º A taxa",
                     "Lei 8.036 art. 5 § 9º (Lei 13.932/2019): the annotated page prints the label twice ('§ 9º § 9º A taxa "
                     "de administração [...]'); Lei 13.932's own text and the consolidated page print it once"))
P.MP_LAPSE["mp-1336-2026"] = (
    "2026-06-06", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 48, de 2026 (DOU 9.6.2026): 'teve seu "
                  "prazo de vigência encerrado no dia 5 de junho de 2026'")
B7.CONVERTED_FIX["mp-996-2020"] = ("lei-14118-2021", "the MP page reads 'Convertida Lei nº 14.118, de 2021' (no 'na'), "
                                                    "linking ../../2021/Lei/L14118.htm, Lei nº 14.118, de 12.1.2021 "
                                                    "('Conversão da Medida Provisória nº 996, de 2020')")
P.MP_PENDING.update({
    "mp-2164-2001": ("Medida Provisória nº 2.164-41, de 24.8.2001 (DOU 27.8.2001, in force on publication), kept in force by "
                     "Emenda Constitucional 32/2001, art. 2; its art. 9 gave Lei 8.036 arts. 19-A, 20 VIII and XIII and 29-A "
                     "to 29-D their wording. Planalto's notes name this edition only, so the changes are dated by its "
                     "publication; earlier editions of the chain are not modelled"),
    "mp-2196-2001": ("Medida Provisória nº 2.196-3, de 24.8.2001 (DOU 25.8.2001, in force on publication), kept in force by "
                     "Emenda Constitucional 32/2001, art. 2; its art. 12 added Lei 8.036 art. 9 § 8º. Earlier editions of the "
                     "chain are not modelled"),
    "mp-2197-2001": ("Medida Provisória nº 2.197-43, de 24.8.2001 (DOU 27.8.2001, in force on publication), kept in force by "
                     "Emenda Constitucional 32/2001, art. 2; its art. 5 gave Lei 8.036 art. 9 § 6º and art. 20 its wording. "
                     "Earlier editions of the chain are not modelled"),
})

# ---------------------------------------------------------------------------------------------------------------
# part e: Estatuto do Índio, Lei das Cooperativas, Lei da Reforma Agrária
_EIND, _LCOOP, _LRA = "estatuto-do-indio", "lei-das-cooperativas", "lei-da-reforma-agraria"
P.MP_PENDING["mp-2168-2001"] = (
    "Medida Provisória nº 2.168-40, de 24.8.2001 (DOU 27.8.2001, in force on publication), kept in force by Emenda "
    "Constitucional 32/2001, art. 2; its art. 13 gave Lei 5.764 art. 88 its wording. Planalto's note names this edition "
    "only, so the change is dated by its publication; earlier editions of the chain are not modelled")
_W14701 = ("Estatuto do Índio art. 2 IX: Lei 14.701/2023 (DOU 20.10.2023) art. 32, which rewrote the inciso, was vetoed; "
           "Congress overrode the veto and the part was promulgated in the DOU of 28.12.2023 (printed on Lei 14.701's page; "
           "Planalto marks the note 'Promulgação partes vetadas'): the 1973 wording stands to 28.12.2023")
_W14757 = ("Lei 8.629 art. 6 § 9º: Lei 14.757/2023 (DOU 20.12.2023) added it, but the President vetoed it ('§ 9º (VETADO).'); "
           "Congress overrode the veto and the paragraph was promulgated in the DOU of 13.6.2024 (printed on Lei 14.757's page): "
           "the '(VETADO)' line stands to 13.6.2024 and the text from then")
_W20 = ("Lei 8.629 art. 20 §§ 1º to 4º: Planalto prints Lei 13.465/2017's §§ 1º, 2º (later replaced), 3º and 4º with no note; "
        "they come after Lei 13.465's caput and incisos (Medida Provisória 759/2016's §§, which they continue, are printed "
        "struck above them) and the 1993 article had no parágrafos, so they start with Lei 13.465 (12.7.2017)")
_L13465 = {"start": "2017-07-12", "start_law": "lei-13465-2017"}
B8.SPAN_FIX += [
    ((_EIND, "art-02", "IX -", "IX - garantir aos índios e comunidades indígenas, nos termos da Constituição, a posse", 0),
     {"end": "2023-12-28", "end_law": "lei-14701-2023", "end_how": "promulgation"}, _W14701),
    ((_EIND, "art-02", "IX -", "IX - garantir aos índios e comunidades indígenas, nos termos da Constituição Federal", 0),
     {"start": "2023-12-28", "start_law": "lei-14701-2023", "by_provision": True}, _W14701),
    ((_LRA, "art-06", "§ 9º", "§ 9º (VETADO)", 0),
     {"start": "2023-12-20", "start_law": "lei-14757-2023", "end": "2024-06-13", "end_law": "lei-14757-2023",
      "end_how": "promulgation", "skip": False}, _W14757),
    ((_LRA, "art-06", "§ 9º", "§ 9º Os laudos que indiquem o grau de utilização", 0),
     {"start": "2024-06-13", "start_law": "lei-14757-2023", "by_provision": True}, _W14757),
    ((_LRA, "art-20", "§ 1º", "§ 1º As disposições constantes dos incisos I, II, III, IV e VI do caput deste artigo", 0),
     _L13465, _W20),
    ((_LRA, "art-20", "§ 2º", "§ 2º A vedação de que trata o inciso I do caput deste artigo não se aplica", 0), _L13465, _W20),
    ((_LRA, "art-20", "§ 3º", "§ 3º São considerados serviços de interesse comunitário", 1), _L13465, _W20),
    ((_LRA, "art-20", "§ 4º", "§ 4º Não perderá a condição de beneficiário aquele que passe a se enquadrar nos incisos I, "
                              "III, IV e VI do caput deste artigo", 0), _L13465, _W20),
]
B.EXPLAINED[_LRA] = {
    "art-05": "the consolidated page prints incisos II and III of § 3º as one line ('[...] cento e cinqüenta módulos fiscais; e "
              "III - do segundo ao vigésimo ano [...]'); the annotated page prints them as two",
    "art-17": "the consolidated page prints '§ 1º (Vetado).', the annotated page '§ 1º (Vetado.)'",
}
B13.OPEN_ITEMS[_LRA] = (
    "Lei 8.629 (open items): its changes by Medida Provisória 2.183-56/2001 (arts. 2, 2-A, 5, 6, 7, 11, 12, 17, 18, 26-A) "
    "are dated by that edition's publication (27.8.2001), as Planalto's notes name it; the earlier editions of the chain "
    "(from Medida Provisória 1.577/1997) that first made most of them are not modelled; Planalto's 'Vide' pointers (ADIs "
    "2.213 and 2.411) strike no words and are not modelled")
B13.OPEN_ITEMS[_EIND] = (
    "Estatuto do Índio (open items): Lei 14.701/2023 art. 32's wording of art. 2 IX is the subject of ADC 87 and ADIs 7.582, "
    "7.583 and 7.586 (pending: 'Vide' pointers on Planalto's page, no words struck); it is shown as promulgated")

# ---------------------------------------------------------------------------------------------------------------
# part f: Lei do Seguro-Desemprego (Lei 7.998/1990)
_LSD = "lei-do-seguro-desemprego"
_MP665 = ("art. 3: 'Esta Medida Provisória entra em vigor: I - sessenta dias após sua publicação quanto às alterações dos "
          "art. 3º e art. 4º da Lei nº 7.998, de 11 de janeiro de 1990, estabelecidas no art. 1º e ao inciso III do caput do "
          "art. 4º; II - no primeiro dia do quarto mês subsequente à data de sua publicação quanto ao art. 2º e ao inciso IV "
          "do caput do art. 4º; III - na data de sua publicação, para os demais dispositivos' (DOU 30.12.2014, edição extra)")
P.VIGENCIA_FIXED["mp-665-2014"] = (
    "2014-12-30", _MP665 + ": its other changes to Lei 7.998 (and its art. 4 II, which revoked art. 2º-B, art. 3 II and art. "
                           "9 parágrafo único) fall under III; arts. 3 and 4 by provision (28.2.2015)")
P.VIGENCIA_PROVISION.update({
    ("mp-665-2014", _LSD, u): ("2015-02-28", "Medida Provisória 665/2014 " + _MP665 + ": 60 days after publication, "
                               "counted from the day of publication (LC 95/1998 art. 8 § 1): 28.2.2015")
    for u in ("art-03", "art-04")})
B8.SPAN_FIX.append(((_LSD, "art-03", "II -", "II - ter sido empregado de pessoa jurídica", 0),
                    {"end": "2014-12-30", "end_law": "mp-665-2014", "end_how": "note"},
                    "Lei 7.998 art. 3 II: revoked by Medida Provisória 665/2014 art. 4 II, which falls under its art. 3 III (in "
                    "force on publication, 30.12.2014), not under art. 3 I (the 60-day term for its new wording of arts. 3 and "
                    "4)"))
_W25 = ("Lei 7.998 art. 25: Medida Provisória 905/2019 replaced the whole article (caput only, '[...] art. 634-A da "
        "Consolidação das Leis do Trabalho [...].' (NR)); Planalto prints its wording twice in the reverse of the usual order "
        "(first the copy noted only 'Vigência encerrada', for 18.8.2020, then the copy noted 'Revogada pela Medida Provisória "
        "nº 955, de 2020', for 12.11.2019 to 20.4.2020). The 1990 caput and §§ 1º-2º stand to 12.11.2019, again from 20.4.2020 "
        "to 18.8.2020 (while MP 955 stood) and from 19.8.2020 (the unstruck copy below)")
B8.SPAN_FIX += [
    ((_LSD, "art-25", "Art. 25", "Art. 25. As infrações às disposições desta Lei pelo empregador", 0),
     {"start": "2020-08-18", "start_law": "mp-955-2020-fim", "end": "2020-08-19", "end_law": "mp-905-2019-fim",
      "end_how": "mp-pair", "gaps": []}, _W25),
    ((_LSD, "art-25", "Art. 25", "Art. 25. As infrações às disposições desta Lei pelo empregador", 1),
     {"start": "2019-11-12", "start_law": "mp-905-2019", "end": "2020-04-20", "end_law": "mp-955-2020",
      "end_how": "mp-pair", "gaps": []}, _W25),
    *[((_LSD, "art-25", lab, pre, 0), {"end": "2020-08-18", "end_law": "mp-955-2020-fim", "end_how": "mp-pair",
                                       "gaps": [_MP905_GAP], "skip": False}, _W25)
      for lab, pre in [("Art. 25", "Art. 25. O empregador que infringir"), ("§ 1º", "§ 1º Serão competentes para impor"),
                       ("§ 2º", "§ 2º Além das penalidades administrativas")]],
    *[((_LSD, "art-25", lab, pre, 1), {"start": "2020-08-19", "start_law": "mp-905-2019-fim", "restored": True}, _W25)
      for lab, pre in [("Art. 25", "Art. 25. O empregador que infringir"), ("§ 1º", "§ 1º Serão competentes para impor"),
                       ("§ 2º", "§ 2º Além das penalidades administrativas")]],
]
_MROSC = "marco-regulatorio-das-oscs"
_WPRE = ("Lei 13.019 (in force 23.1.2016): Medidas Provisórias 658/2014 and 684/2015 gave arts. 83 §§ 1º-2º and 88 wordings "
         "that their conversion laws (Leis 13.102/2015 and 13.204/2015) replaced before the act took effect; they never "
         "stood and are left out (the first day's two versions show the act as enacted and the text in force)")
_WSAME = ("Lei 13.019 art. 35 i) and art. 42 XX: the wordings of 2014 (struck, no note) were replaced by Lei 13.204/2015 "
          "before the act took effect; they belong to the act as enacted and end with the first day's second version, like "
          "the act's other lines Lei 13.204 rewrote")
B8.SPAN_FIX += [
    *[((_MROSC, unit, lab, pre, 0), {"skip": True, "end_how": "never-in-force"}, _WPRE) for unit, lab, pre in [
        ("art-88", "Art. 88", "Art. 88. Esta Lei entra em vigor após decorridos 360 (trezentos e sessenta) dias de sua "
                              "publicação oficial."),
        ("art-88", "Art. 88", "Art. 88. Esta Lei entra em vigor após decorridos 540 (quinhentos e quarenta)"),
        ("art-83", "§ 1º", "§ 1º A exceção de que trata o caput não se aplica às prorrogações"),
        ("art-83", "§ 2º", "§ 2º Para qualquer parceria referida no caput eventualmente firmada")]],
    ((_MROSC, "art-35", "i)", "i) da aprovação do regulamento de compras", 0),
     {"end": "2016-01-23", "end_law": "lei-13204-2015", "end_how": "same-day", "skip": False}, _WSAME),
    ((_MROSC, "art-42", "XX -", "XX - a responsabilidade exclusiva da organização da sociedade civil pelo pagamento", 0),
     {"end": "2016-01-23", "end_law": "lei-13204-2015", "end_how": "same-day", "skip": False}, _WSAME),
]
B13.OPEN_ITEMS[_MROSC] = (
    "Lei 13.019 (open items): the history starts on 23.1.2016, the act's in-force day for the Union, States and Federal "
    "District; for Municipalities its art. 88 § 1º sets 1.1.2017 (or earlier by local act, § 2º), which a single national "
    "history does not separate; the text amended before 23.1.2016 (Medidas Provisórias 658/2014 and 684/2015, Leis "
    "13.102/2015 and 13.204/2015) is the first day's second version")
B.EXPLAINED[_LSD] = {
    "art-11": "the consolidated page leaves out inciso V ('V - outros recursos que lhe sejam destinados.'), which the "
              "annotated page prints, unstruck and without a note, as part of the 1990 text",
}
B13.OPEN_ITEMS[_LSD] = (
    "Lei 7.998 (open items): its changes by Medida Provisória 2.164-41/2001 (arts. 2, 2-A, 2-B, 3-A, 7-A, 8-A to 8-C) are "
    "dated by that edition's publication (27.8.2001), as Planalto's notes name it; the earlier editions of the chain are not "
    "modelled; Lei 13.134/2015 art. 4 defers only the financial effects of its art. 9 changes (from the 2016 financial "
    "year), so they keep the in-force day; art. 19 prints two incisos 'XIV' (the second, '(Vetado);', after XV, as on "
    "both Planalto pages): kept as printed; Planalto's 'Vide' pointers strike no words and are not modelled")
P.VIGENCIA_PROVISION[("mp-905-2019", _LSD, "art-04-b")] = (
    "2020-03-01", "Medida Provisória 905/2019 art. 53 II: 'no primeiro dia do quarto mês subsequente ao da publicação desta "
                  "Medida Provisória, quanto à inclusão do art. 4º-B na Lei nº 7.998, de 1990, promovida pelo art. 43' (DOU "
                  "12.11.2019): 1.3.2020")
P.NOTE_FIX.update({} if _LSD not in ENABLED else {"(Redação dada pela Lei nº 10.261, de 2021)": (
    "(Redação dada pela Lei nº 14.261, de 2021)",
    "Lei 7.998: two notes read '(Redação dada pela Lei nº 10.261, de 2021)'; their link is Lei nº 14.261, de 16.12.2021 "
    "(L14261.htm#art12), whose art. 12 amends Lei 7.998")})

# ---------------------------------------------------------------------------------------------------------------
# Lei 4.320/1964, part c: page fixes (paragraphs wrapper)
#  - many articles (69 to 82, 99 to 113, ...) are printed 'Artigo 109.' at the start of their paragraph: read as 'Art. 109.'
#  - '(Veto rejeitado no DOU, de 5.5.1964)' / '(Veto rejeitado no D.O. 05/05/1964)' after a line: the parts President
#    Goulart vetoed and Congress kept, promulgated in the DOU of 5.5.1964, before the act's in-force day (7.5.1964): a note,
#    taken out of the text; it dates nothing
ARTIGO_FIXED: dict[str, int] = {}
VETO_NOTES: dict[str, int] = {}
_VETO = re.compile(r"\s*\(\s*Veto\s+rejeitado\s+no\s+(?:DOU|D\.\s*O\.)\s*,?\s*(?:de\s+)?(?:5\.5\.1964|05/05/1964)\s*\)\s*\.?", re.I)
_paragraphs16 = P.paragraphs


def paragraphs(html, digits):
    page = B8.CURRENT_PAGE[0]
    if page in ("l4320", "l4320-compilado"):
        html, n = re.subn(r"(<p\b[^>]*>(?:\s|&nbsp;|<(?!/p)[^>]+>)*)Artigo\s+(\d+)", r"\1Art. \2", html, flags=re.I)
        ARTIGO_FIXED[page] = n
    out, rest = _paragraphs16(html, digits)
    if page in ("l4320", "l4320-compilado"):
        for p in out:
            hits = 0
            for f in ("text", "struck_text", "plain_text"):
                if isinstance(p.get(f), str) and _VETO.search(p[f]):
                    p[f], k = _VETO.subn("", p[f])
                    p[f] = P.norm(p[f])
                    hits = max(hits, k)
            if hits:
                p["notes"] = list(p["notes"]) + ["(Veto rejeitado no DOU de 5.5.1964)"]
                VETO_NOTES[page] = VETO_NOTES.get(page, 0) + 1
    if page == "l6001":
        # Estatuto do Índio art. 20: the page prints its parágrafos '1º A intervenção [...]' without the § sign
        for p in out:
            m = re.match(r"^(\d)º\s", p["text"]) if p["unit"] == "art-20" and not p["label"] and not p["heading"] else None
            if m:
                p["text"] = "§ " + p["text"]
                p["label"] = f"§ {m.group(1)}º"
                SECTION_SIGN.append(f"art. 20 § {m.group(1)}º")
    if page == "l5764":
        # Lei 5.764 art. 110 ends '[...] Decreto-Lei n. 60, de 21 de novembro de 1966, com a redação dada pelo Decreto-Lei
        # n. 668, de 3 de julho de 1969.': words of the article (which law's wording of DL 60 art. 13 it names), not an
        # amendment note; the reader took them for a note left without parentheses
        for p in out:
            hit = [n for n in p["notes"] if re.fullmatch(r"\(?\s*reda[çc][ãa]o dada pelo Decreto-Lei n\. 668, de 3 de julho "
                                                         r"de 1969\.?\s*\)?", n.strip(), re.I)]
            if p["unit"] == "art-110" and hit and p["text"].rstrip().endswith("com a"):
                p["text"] = p["text"].rstrip() + " redação dada pelo Decreto-Lei n. 668, de 3 de julho de 1969."
                p["notes"] = [n for n in p["notes"] if n not in hit]
                BARE_KEPT.append("Lei 5.764 art. 110")
    if page in ("l4320", "l4320-compilado"):
        # the classification schemes of arts. 11 to 13 (and later ones) are centred lines inside the article: they are
        # lines of that article, not headings (a heading is a Título/Capítulo/Seção line or the name line after it)
        cur = None
        for p in out:
            if p["heading"]:
                if P.HEADING.match(p["text"]):
                    cur = None
                elif cur is not None:
                    p.update({"heading": False, "unit": cur, "label": "", "center": False})
                    TABLE_LINES[page] = TABLE_LINES.get(page, 0) + 1
            elif p["unit"].startswith("art-"):
                cur = p["unit"]
    return out, rest


B15.TEXT_FIX.append(("l4320", "para feito do disposto no artigo anterior", "para efeito do disposto no artigo anterior",
                     "Lei 4.320 art. 49: the annotated page misprints 'para feito do disposto no artigo anterior'; the "
                     "consolidated page reads 'para efeito'"))
B15.TEXT_FIX.append(("l9455", "(sessenta) anos; '$", "(sessenta) anos;",
                     "Lei 9.455 art. 1 § 4º II (Lei 10.741/2003): the page leaves a stray quotation mark after the line ('[...] "
                     "maior de 60 (sessenta) anos; ''), the closing quote of the amending law's text"))
B.EXPLAINED[_L4320] = {
    "art-009": "the consolidated page drops the period before the veto note ('[...] por essas entidades (Veto rejeitado no "
               "DOU, de 5.5.1964)'); the annotated page prints it",
    "art-033": "the consolidated page drops a comma ('nesse ponto a inexatidão'); the annotated page prints 'nesse ponto, a "
               "inexatidão'",
    "art-057": "the consolidated page prints 'artigo 3. desta lei'; the annotated page 'artigo 3º'",
    "art-064": "the consolidated page drops the period before the veto note ('serviços de contabilidade (Veto rejeitado "
               "[...])')",
    "art-069": "the consolidated page misprints 'responsável por dois adiantamento.'; the annotated page reads "
               "'adiantamentos'",
    "art-082": "capitalisation: the annotated page prints 'Leis orgânicas dos Municípios' in art. 82, the consolidated page "
               "'Leis Orgânicas'",
    "art-101": "the annotated page lists the annexes as 'números 1, 6 - 7 - 8 - 9 - 10 - 11 - 16 e 17', the consolidated page "
               "with commas",
    "art-106": "the annotated page numbers the incisos 'I)', 'II)', 'III)' as enacted, the consolidated page 'I -'",
    "art-108": "as art. 106: 'II)' on the annotated page, 'II -' on the consolidated page",
    "art-111": "the consolidated page drops the ordinal sign ('§ 2 O quadro'); the annotated page prints '§ 2º'",
    "titulos": "the consolidated page misprints a heading ('Da Proposta Orcamentária'); the annotated page reads 'Orçamentária'",
}
B13.OPEN_ITEMS[_L4320] = (
    "Lei 4.320 (open items): its annexes (the model statements, Anexos 1 to 17) are not part of the history; art. 114's "
    "counting of the act's effects (budgets from 1.1.1964, the other activities from 1.1.1965, Lei 4.489/1964) is "
    "retroactive for budgets and is not modelled as a later effect day: the act is dated by its in-force day; the "
    "sub-division names 'I) Das Subvenções Sociais' and 'II) Das Subvenções Econômicas' are kept as marginal headings of "
    "arts. 16 and 18")
TABLE_LINES: dict[str, int] = {}
TABLE_DATED: list[str] = []
SECTION_SIGN: list[str] = []
BARE_KEPT: list[str] = []


def scheme_lines(paras):
    """Lei 4.320: a struck line of a classification scheme (no label, no note) stands as long as the labelled struck line
    above it in the same article (art. 11 § 4º's 1964 scheme, replaced by Decreto-Lei 1.939/1982)"""
    for i, p in enumerate(paras):
        if p["heading"] or p["label"] or p["state"] == "plain" or p["notes"] or not p["unit"].startswith("art-"):
            continue
        q = next((q for q in reversed(paras[:i]) if q["unit"] == p["unit"] and q["label"] and not q["heading"]), None)
        if q is None or q["state"] == "plain" or not q.get("end"):
            continue
        if (p["start"], p.get("end"), p.get("skip")) != (q["start"], q["end"], False):
            p.update({"start": q["start"], "start_law": q["start_law"], "end": q["end"], "end_law": q["end_law"],
                      "end_how": "parent", "skip": False, "gaps": list(q.get("gaps") or [])})
            TABLE_DATED.append(f"{p['unit']} '{p['text'][:30]}'")


P.paragraphs = B.paragraphs = paragraphs

# ---------------------------------------------------------------------------------------------------------------
_inner16 = B6.PB5B._write_part5


def _inner(*a):
    dec = list(EXTRA)
    if CONV_CHILD_USED:
        dec.append("Código Brasileiro de Aeronáutica: where Medida Provisória 1.089/2021 revoked whole articles or sections (its "
                   "art. 4 IV: 'os art. 73 a art. 76', 'a Seção II do Capítulo V do Título III', 'os art. 116 e art. 117', "
                   "...), Planalto notes the MP's revocation on the caput only and on the lines under it only the revocation "
                   "by Lei 14.368/2022, its conversion; those lines fall with the caput on the MP's day (30.12.2021): "
                   + ", ".join(dict.fromkeys(CONV_CHILD_USED)) + ".")
    if ARTIGO_FIXED.get("l4320"):
        dec.append("Lei 4.320: Planalto's pages print many articles with the label 'Artigo 69.', 'Artigo 109.' ... at the start "
                   "of their paragraph; they are read as 'Art. 69.' etc. (" + ", ".join(
                       f"{k} {v}" for k, v in sorted(ARTIGO_FIXED.items())) + " paragraphs).")
    if VETO_NOTES.get("l4320"):
        dec.append("Lei 4.320: lines followed by '(Veto rejeitado no DOU, de 5.5.1964)' or '(Veto rejeitado no D.O. 05/05/1964)' "
                   f"({VETO_NOTES['l4320']} on the annotated page) are the parts President Goulart vetoed and Congress kept "
                   "promulgated in the DOU of 5.5.1964, before the act's in-force day (7.5.1964): the "
                   "words are a note, taken out of the text, and those parts are in force with the act, as promulgated parts "
                   "of other acts in this corpus are dated by their promulgation.")
    if TABLE_LINES.get("l4320"):
        dec.append("Lei 4.320: the classification schemes inside arts. 11 to 13 (and other articles) are centred lines on "
                   "Planalto's pages; they are lines of the article they are printed in, not headings (only Título, "
                   "Capítulo, Seção and Subseção lines and the name line after them are headings): "
                   + ", ".join(f"{k} {v}" for k, v in sorted(TABLE_LINES.items())) + " lines. The 1964 scheme of art. 11 "
                   "§ 4º (struck, no note) stands as long as § 4º itself, to Decreto-Lei 1.939/1982" +
                   (f" ({len(TABLE_DATED)} lines)" if TABLE_DATED else "") + ".")
    if SECTION_SIGN:
        dec.append("Estatuto do Índio art. 20: Planalto's page prints the article's parágrafos without the § sign ('1º A "
                   "intervenção poderá ser decretada: [...]'); they are read as §§ 1º to 5º: "
                   + ", ".join(dict.fromkeys(SECTION_SIGN)) + ".")
    if BARE_KEPT:
        dec.append("Lei 5.764 art. 110 ends 'Decreto-Lei n. 60, de 21 de novembro de 1966, com a redação dada pelo Decreto-Lei "
                   "n. 668, de 3 de julho de 1969.': these words name the wording of the provision the article refers to; "
                   "they are part of the article's text, not an amendment note.")
    B5.EXTRA_DECISIONS.extend(dec)
    return _inner16(*a)


B6.PB5B._write_part5 = _inner

SRC = HERE / "sources_batch16.json"
if not SRC.exists():
    SRC.write_text('{\n "fetch": []\n}\n', encoding="utf-8", newline="\n")
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
