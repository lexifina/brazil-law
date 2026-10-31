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
})
B.PAGES.clear()
B.PAGES.update(PAGES)
for M in (B5, B6, B7, B8, B9, B10, B11, B12, B13, B14, B15):
    M.PAGES = PAGES

_CBA, _L4320, _FGTS = "codigo-brasileiro-de-aeronautica", "lei-4320-de-1964", "lei-do-fgts"
ALL_ACTS: list[dict] = ([a for a in B14.ALL_ACTS if a["slug"] == _CBA]
                        + [a for a in B13.ALL_ACTS if a["slug"] in (_L4320, _FGTS)])
PARTS: dict[str, list[str]] = {
    "a": [_CBA],
    "b": [_FGTS],
    "c": [_L4320],
}
VERIFIED: list[str] = PARTS.get(PART, [])
ENABLED = [s for s in os.environ.get("BATCH16_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = B6.ACTS = ACTS
for M in (B7, B8, B9, B10, B11, B12, B13, B14, B15):
    M.ACTS[:] = ACTS
ACT_DAY_ALL = {**B13.ACT_DAY_ALL, **B14.ACT_DAY_ALL}
ACT_LAWS_ALL = {**B13.ACT_LAWS_ALL, **B14.ACT_LAWS_ALL}
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
# 14.368, de 2022'). They fall with the line above them on the MP's day (MP 1.089/2021 art. 5 IV m): 'os art. 73 a art. 76',
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
_inner16 = B6.PB5B._write_part5


def _inner(*a):
    dec = list(EXTRA)
    if CONV_CHILD_USED:
        dec.append("Código Brasileiro de Aeronáutica: where Medida Provisória 1.089/2021 revoked whole articles or sections (its "
                   "art. 5 IV: 'os art. 73 a art. 76', 'a Seção II do Capítulo V do Título III', 'os art. 116 e art. 117', "
                   "...), Planalto notes the MP's revocation on the caput only and on the lines under it only the revocation "
                   "by Lei 14.368/2022, its conversion; those lines fall with the caput on the MP's day (30.12.2021): "
                   + ", ".join(dict.fromkeys(CONV_CHILD_USED)) + ".")
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
