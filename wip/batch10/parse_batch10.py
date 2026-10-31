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
    _act("estatuto-do-torcedor", "ETor", "etorc", "etorc-compilado", "lei-10671-2003",
         "Estatuto de Defesa do Torcedor (Lei nº 10.671, de 15 de maio de 2003)", 2),
    _act("politica-nacional-do-meio-ambiente", "PNMA", "pnma", "pnma-compilada", "lei-6938-1981",
         "Política Nacional do Meio Ambiente (Lei nº 6.938, de 31 de agosto de 1981)", 2),
]
VERIFIED: list[str] = ["lei-de-concessoes", "lei-das-parcerias-publico-privadas", "lei-de-abuso-de-autoridade",
                        "lei-das-inelegibilidades", "lei-8142-de-1990", "lei-geral-do-esporte"]
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
P.NOTE_FIX.update({
    "(Redação dada pela Medida provisória nº 513, de 2.010)": (
        "(Redação dada pela Medida Provisória nº 513, de 2010)",
        "Lei das PPPs: notes read 'Medida provisória nº 513, de 2.010'; Medida Provisória nº 513, de 26.11.2010"),
    "(Incluído pela Medida provisória nº 513, de 2.010)": (
        "(Incluído pela Medida Provisória nº 513, de 2010)", "as the 'Redação dada' notes of MP 513/2010"),
})
B.EXPLAINED.update({
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


def lifespans(paras, cx):
    problems = _lifespans10(paras, cx)
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
_build_act10 = P.build_act


def build_act(paras, act_day, gate, gate_law, unit_label):
    slug = ACTS[len(B7._act_order)]["slug"] if len(B7._act_order) < len(ACTS) else "?"
    versions = _build_act10(paras, act_day, gate, gate_law, unit_label)
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
    B5.EXTRA_DECISIONS.extend(x + "." for x in dict.fromkeys(OWN_PROMULGATION_USED))
    return _inner10(*a)


B6.PB5B._write_part5 = _inner

SRC = HERE / "sources_batch10.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
