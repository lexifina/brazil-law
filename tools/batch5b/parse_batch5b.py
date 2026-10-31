"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch5b.json (SCHEMA.md corpus part): the acts in ACTS
below (internet civil framework, anti-corruption, administrative improbity, environmental crimes, drugs).

    python -X utf8 scripts/brazil-law/batch5b/parse_batch5b.py [--stats] [--dry] [--only <slug,...>]

Imports ../batch5/parse_batch5.py (which configures ../batch4, ../batch3 and ../proc, the struck-text replay of
Planalto's annotated pages) and replaces only its configuration: the acts, the hand tables, the pins and the output.
The parts of batch 5 and earlier are not touched (their parsers, run on their own, write the same bytes as before).
No network.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
sys.path.insert(0, str(FOLDER / "batch5"))
import parse_batch5 as B5  # noqa: E402  (configures batch 4 / batch 3 / parse_proc for batch 5; reconfigured below)

B4, B, P = B5.B4, B5.B, B5.P
PL = P.PL
B5.OUT = Path(os.environ.get("BATCH5B_OUT") or FOLDER / "corpus.d" / "99-batch5b.json")
B5.STAGE = HERE / ".tmp" / "stage.json"
P.RETRIEVED = "2026-10-29"

PAGES = {
    "mci": "_ato2011-2014/2014/lei/l12965.htm",
    "lac": "_ato2011-2014/2013/lei/l12846.htm",
    "lia": "leis/l8429.htm",
    "lia-compilada": "leis/l8429compilada.htm",
    "lca": "leis/l9605.htm",
    "lad": "_ato2004-2006/2006/lei/l11343.htm",
    "larb": "leis/l9307.htm",
    "lai": "_ato2011-2014/2011/lei/l12527.htm",
    "lpa": "leis/l9784.htm",
    "lloc": "leis/l8245.htm",
    "lloc-compilado": "leis/l8245compilado.htm",
    "lmed": "_ato2015-2018/2015/lei/l13140.htm",
}
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = PAGES

# Acts are added one at a time: ENABLED lists the ones whose open dates the official sources settle (see
# ../batch5/PROGRESS.md); Lei 8.429/1992, Lei 9.605/1998, Lei 12.527/2011 and Lei 9.784/1999 are configured but deferred.
ALL_ACTS: list[dict] = [
    {"slug": "marco-civil-da-internet", "short": "MCI", "page": "mci", "consolidated": "mci", "law": "lei-12965-2014",
     "title": "Marco Civil da Internet (Lei nº 12.965, de 23 de abril de 2014)", "digits": 2,
     "url": PL + PAGES["mci"]},
    {"slug": "lei-anticorrupcao", "short": "LAC", "page": "lac", "consolidated": "lac", "law": "lei-12846-2013",
     "title": "Lei Anticorrupção (Lei nº 12.846, de 1º de agosto de 2013)", "digits": 2, "url": PL + PAGES["lac"]},
    {"slug": "lei-de-improbidade-administrativa", "short": "LIA", "page": "lia", "consolidated": "lia-compilada",
     "law": "lei-8429-1992", "title": "Lei de Improbidade Administrativa (Lei nº 8.429, de 2 de junho de 1992)",
     "digits": 2, "url": PL + PAGES["lia"]},
    {"slug": "lei-de-crimes-ambientais", "short": "LCA", "page": "lca", "consolidated": "lca", "law": "lei-9605-1998",
     "title": "Lei de Crimes Ambientais (Lei nº 9.605, de 12 de fevereiro de 1998)", "digits": 2,
     "url": PL + PAGES["lca"]},
    {"slug": "lei-de-drogas", "short": "LAD", "page": "lad", "consolidated": "lad", "law": "lei-11343-2006",
     "title": "Lei de Drogas (Lei nº 11.343, de 23 de agosto de 2006)", "digits": 2, "url": PL + PAGES["lad"]},
    {"slug": "lei-de-arbitragem", "short": "LArb", "page": "larb", "consolidated": "larb", "law": "lei-9307-1996",
     "title": "Lei de Arbitragem (Lei nº 9.307, de 23 de setembro de 1996)", "digits": 2, "url": PL + PAGES["larb"]},
    {"slug": "lei-de-acesso-a-informacao", "short": "LAI", "page": "lai", "consolidated": "lai", "law": "lei-12527-2011",
     "title": "Lei de Acesso à Informação (Lei nº 12.527, de 18 de novembro de 2011)", "digits": 2,
     "url": PL + PAGES["lai"]},
    {"slug": "lei-do-processo-administrativo", "short": "LPA", "page": "lpa", "consolidated": "lpa",
     "law": "lei-9784-1999", "title": "Lei do Processo Administrativo Federal (Lei nº 9.784, de 29 de janeiro de 1999)",
     "digits": 2, "url": PL + PAGES["lpa"]},
    {"slug": "lei-do-inquilinato", "short": "LInq", "page": "lloc", "consolidated": "lloc-compilado",
     "law": "lei-8245-1991", "title": "Lei do Inquilinato (Lei nº 8.245, de 18 de outubro de 1991)", "digits": 2,
     "url": PL + PAGES["lloc"]},
    {"slug": "lei-de-mediacao", "short": "LMed", "page": "lmed", "consolidated": "lmed", "law": "lei-13140-2015",
     "title": "Lei de Mediação (Lei nº 13.140, de 26 de junho de 2015)", "digits": 2, "url": PL + PAGES["lmed"]},
]
# the acts verified and published in 99-batch5b.json (99-batch5b.PUBLISH); BATCH5B_ACTS overrides for trial runs
VERIFIED = ["marco-civil-da-internet", "lei-anticorrupcao", "lei-de-drogas", "lei-de-arbitragem", "lei-do-inquilinato",
            "lei-de-mediacao"]
ENABLED = [s for s in os.environ.get("BATCH5B_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = ACTS

# In-force days, read from each act's own closing clause and the DOU day Planalto prints under it ('Este texto não
# substitui o publicado no DOU de ...'). Day counts follow LC 95/1998 art. 8 § 1 (publication day and last day included;
# in force the day after).
ACT_DAY_ALL = {
    "lei-12965-2014": ("2014-06-23", "Lei 12.965/2014 art. 32: 'Esta Lei entra em vigor após decorridos 60 (sessenta) dias "
                                     "de sua publicação oficial' (DOU 24.4.2014): the 60th day counted from publication is "
                                     "22.6.2014 (LC 95/1998 art. 8 § 1)"),
    "lei-12846-2013": ("2014-01-29", "Lei 12.846/2013 art. 31: 'Esta Lei entra em vigor 180 (cento e oitenta) dias após a "
                                     "data de sua publicação' (DOU 2.8.2013): the 180th day counted from publication is "
                                     "28.1.2014 (LC 95/1998 art. 8 § 1)"),
    "lei-11343-2006": ("2006-10-08", "Lei 11.343/2006 art. 74: 'Esta Lei entra em vigor 45 (quarenta e cinco) dias após a "
                                     "sua publicação' (DOU 24.8.2006): the 45th day counted from publication is 7.10.2006 "
                                     "(LC 95/1998 art. 8 § 1)"),
    "lei-9307-1996": ("1996-11-23", "Lei 9.307/1996 art. 43: 'Esta Lei entrará em vigor sessenta dias após a data de sua "
                                    "publicação' (DOU 24.9.1996): 60 days after 24.9.1996 is 23.11.1996 (the same day "
                                    "whether or not the publication day is counted, LC 95/1998 art. 8 § 1)"),
    "lei-12527-2011": ("2012-05-16", "Lei 12.527/2011 art. 47: 'Esta Lei entra em vigor 180 (cento e oitenta) dias após a "
                                     "data de sua publicação' (DOU 18.11.2011, edição extra): the 180th day counted from "
                                     "publication is 15.5.2012 (LC 95/1998 art. 8 § 1)"),
    "lei-8245-1991": ("1991-12-20", "Lei 8.245/1991 art. 89: 'Esta lei entrará em vigor sessenta dias após a sua "
                                    "publicação' (DOU 21.10.1991): 60 days after 21.10.1991 is 20.12.1991 (the same day "
                                    "whether or not the publication day is counted, LC 95/1998 art. 8 § 1)"),
    "lei-13140-2015": ("2015-12-26", "Lei 13.140/2015 art. 47: 'Esta Lei entra em vigor após decorridos cento e oitenta "
                                     "dias de sua publicação oficial' (DOU 29.6.2015): the 180th day counted from "
                                     "publication is 25.12.2015 (LC 95/1998 art. 8 § 1)"),
    "lei-8429-1992": ("1992-06-03", "Lei 8.429/1992 art. 24: 'Esta lei entra em vigor na data de sua publicação' (DOU "
                                    "3.6.1992)"),
}
ACT_LAWS_ALL = {
    "lei-12965-2014": B._act_law("Lei nº 12.965, de 2014", "Estabelece princípios, garantias, direitos e deveres para o uso "
                                 "da Internet no Brasil.", "2014-04-23", "2014-04-24", PAGES["mci"]),
    "lei-12846-2013": B._act_law("Lei nº 12.846, de 2013", "Dispõe sobre a responsabilização administrativa e civil de "
                                 "pessoas jurídicas pela prática de atos contra a administração pública, nacional ou "
                                 "estrangeira, e dá outras providências.", "2013-08-01", "2013-08-02", PAGES["lac"]),
    "lei-11343-2006": B._act_law("Lei nº 11.343, de 2006", "Institui o Sistema Nacional de Políticas Públicas sobre "
                                 "Drogas - Sisnad; prescreve medidas para prevenção do uso indevido, atenção e reinserção "
                                 "social de usuários e dependentes de drogas; estabelece normas para repressão à produção "
                                 "não autorizada e ao tráfico ilícito de drogas; define crimes e dá outras providências.",
                                 "2006-08-23", "2006-08-24", PAGES["lad"]),
    "lei-9307-1996": B._act_law("Lei nº 9.307, de 1996", "Dispõe sobre a arbitragem.", "1996-09-23", "1996-09-24",
                                PAGES["larb"]),
    "lei-12527-2011": B._act_law("Lei nº 12.527, de 2011", "Regula o acesso a informações previsto no inciso XXXIII do art. "
                                 "5º, no inciso II do § 3º do art. 37 e no § 2º do art. 216 da Constituição Federal; altera "
                                 "a Lei nº 8.112, de 11 de dezembro de 1990; revoga a Lei nº 11.111, de 5 de maio de 2005, e "
                                 "dispositivos da Lei nº 8.159, de 8 de janeiro de 1991; e dá outras providências.",
                                 "2011-11-18", "2011-11-18", PAGES["lai"]),
    "lei-8245-1991": B._act_law("Lei nº 8.245, de 1991", "Dispõe sobre as locações dos imóveis urbanos e os procedimentos "
                                "a elas pertinentes.", "1991-10-18", "1991-10-21", PAGES["lloc"]),
    "lei-13140-2015": B._act_law("Lei nº 13.140, de 2015", "Dispõe sobre a mediação entre particulares como meio de solução "
                                 "de controvérsias e sobre a autocomposição de conflitos no âmbito da administração "
                                 "pública; altera a Lei nº 9.469, de 10 de julho de 1997, e o Decreto nº 70.235, de 6 de "
                                 "março de 1972; e revoga o § 2º do art. 6º da Lei nº 9.469, de 10 de julho de 1997.",
                                 "2015-06-26", "2015-06-29", PAGES["lmed"]),
    "lei-8429-1992": B._act_law("Lei nº 8.429, de 1992", "Dispõe sobre as sanções aplicáveis aos agentes públicos nos casos "
                                "de enriquecimento ilícito no exercício de mandato, cargo, emprego ou função na "
                                "administração pública direta, indireta ou fundacional e dá outras providências.", "1992-06-02", "1992-06-03", PAGES["lia"]),
}
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})
# Rulings and Senate resolutions that strike words (batch 3's COURTS format). A Senate resolution suspending, after a
# final STF ruling, the execution of a provision (CF art. 52 X) is a legislative act: kind "law", in force on its DOU
# publication.
P.COURTS = {
    "rsf-5-2012": {
        "label": "Resolução do Senado Federal nº 5, de 2012", "kind": "law", "enacted": "2012-02-15",
        "published": "2012-02-16",
        "title": "Suspende, nos termos do art. 52, inciso X, da Constituição Federal, a execução de parte do § 4º do art. 33 "
                 "da Lei nº 11.343, de 23 de agosto de 2006.",
        "url": PL + "_Ato2011-2014/2012/Congresso/RSF-05-2012.htm",
        "from": "2012-02-16", "case": r"Resolu[çc][ãa]o\s+n[º°]?\s*5\s*,\s*de\s*2012", "where": [],
        "why": "Resolução do Senado Federal nº 5, de 15.2.2012 (DOU 16.2.2012; Planalto page RSF-05-2012.htm), art. 1: 'É "
               "suspensa a execução da expressão \"vedada a conversão em penas restritivas de direitos\" do § 4º do art. "
               "33 da Lei nº 11.343 [...] declarada inconstitucional por decisão definitiva do Supremo Tribunal Federal "
               "nos autos do Habeas Corpus nº 97.256/RS'; art. 2: in force on publication. Planalto strikes the "
               "expression inside the paragraph, linking the resolution; the history drops it on 16.2.2012, credited to "
               "the resolution (kind law: a Senate act, not a court ruling)"},
}
# mixed paragraphs (an expression struck inside unstruck text) whose note names an entry of P.COURTS that batch 3's
# split rule does not read (it reads only 'Expressão declarada inconstitucional pela ADI ...'): note pattern -> key
SPLIT_NOTES = {"rsf-5-2012": re.compile(r"\(\s*Vide\s+Resolu[çc][ãa]o\s+n[º°]?\s*5\s*,\s*de\s*2012\s*\)", re.I)}
SPLIT_USED: list[str] = []
HEADING_NAME_FIX: list[str] = []
_paragraphs5b = P.paragraphs


def paragraphs(html: str, digits: int):
    out, rest = _paragraphs5b(html, digits)
    res = []
    for p in out:
        key = next((k for k, rx in SPLIT_NOTES.items() if p["state"] == "mixed" and any(rx.fullmatch(n) for n in p["notes"])), None)
        if key is None:
            res.append(p)
            continue
        notes = [n for n in p["notes"] if not SPLIT_NOTES[key].fullmatch(n)]
        base = {k: v for k, v in p.items() if k not in ("text", "state", "notes", "plain_text", "struck_text")}
        res.append({**base, "text": p["text"], "state": "struck", "notes": notes, "plain_text": "", "struck_text": "",
                    "split": ("old", key)})
        res.append({**base, "text": p["plain_text"], "state": "plain", "notes": notes, "plain_text": "",
                    "struck_text": "", "split": ("new", key)})
        SPLIT_USED.append(f"{p['unit']} [{p['label']}] by {P.COURTS[key]['label']}")
    # a struck chapter name printed as plain paragraph text (not detected as a heading) right under its struck
    # 'CAPÍTULO' line (Lei de Drogas, chapters II and IV renamed by Lei 13.840/2019): it is that heading's name line
    for j in range(1, len(res)):
        p, h = res[j], res[j - 1]
        if (p["state"] == "struck" and not p["heading"] and not p["label"] and not p["notes"] and p["text"].isupper()
                and h["heading"] and h["state"] == "struck" and h["unit"] == "titulos" and h["label"].endswith("-0")):
            p.update(unit="titulos", heading=True, label=h["label"][:-2] + "-1")
            HEADING_NAME_FIX.append(f"{h['text']} / {p['text']}")
    for i, p in enumerate(res):
        p["i"] = i
    return res, rest


P.paragraphs = B.paragraphs = paragraphs
# Medidas Provisórias that stopped having effect without conversion: key -> (day the wording they replaced is back,
# reason), read from the Ato Declaratório the act's page links.
P.MP_LAPSE = {
    "mp-1068-2021": ("2021-09-14", "rejected: Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 58, de 2021 "
                                   "(DOU 16.9.2021) makes known the Mensagem nº 92 (CN), of 14.9.2021, 'que rejeita "
                                   "sumariamente e devolve a Medida Provisória nº 1.068, de 2021' and ends its passage in "
                                   "Congress; the MP (DOU 6.9.2021, in force on publication) has no effect from 14.9.2021. "
                                   "CF art. 62 § 3 makes a rejected MP lose effect from its edition; the history keeps "
                                   "its wording for the days Planalto shows it standing (6.9 to 13.9.2021), marked "
                                   "'(Rejeitada)' on the Marco Civil page"),
    "mp-703-2015": ("2016-05-30", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 27, de 2016 (DOU "
                                  "31.5.2016): the MP, 'publicada no Diário Oficial da União no dia 21' of December 2015, "
                                  "'teve seu prazo de vigência encerrado no dia 29 de maio'; the Lei 12.846 wording it had "
                                  "replaced or revoked is back from 30.5.2016"),
}
# Medidas Provisórias whose wording stands with no end of its own (parse_proc's MP_PENDING: a later wording, when there
# is one, still ends it): reissue chains Planalto credits to their first and last reissue, and MPs in force on
# 11.9.2001, which stay in force until revoked or voted on (Emenda Constitucional 32/2001, art. 2).
P.MP_PENDING = {
    "mp-1337-1996": "Medida Provisória nº 1.337, de 12.3.1996 (DOU 13.3.1996), 'Reeditada pela MPV nº 1.379, de 1996', "
                    "a chain of reissues with the same ementa down to MP 1.472-31, de 22.11.1996, 'Convertida na Lei nº "
                    "9.366, de 1996'; Planalto credits the wording of Lei 8.429 art. 17 § 3º to both MP 1.337 and MP "
                    "1.472-31 and the next wording to Lei 9.366, which ends it",
    "mp-1984-2000": "Medida Provisória nº 1.984-16, de 6.4.2000 (DOU 7.4.2000), 'Reeditada pela MPv nº 1.984-17', a chain "
                    "of reissues with the same ementa down to MP 2.180-35, de 24.8.2001; Planalto credits Lei 8.429 art. "
                    "17 § 5º to both",
    "mp-2180-2001": "Medida Provisória nº 2.180-35, de 24.8.2001 (DOU 27.8.2001) was in force on 11.9.2001, so it stays in "
                    "force until a later MP revokes it or Congress votes on it (Emenda Constitucional 32/2001, art. 2)",
    "mp-2223-2001": "Medida Provisória nº 2.223, de 4.9.2001 (DOU 5.9.2001, edição extra) was in force on 11.9.2001, so it "
                    "stayed in force (Emenda Constitucional 32/2001, art. 2) until Lei 10.931/2004 revoked it ('Revogada "
                    "pela Lei nº 10.931, de 2004' on its page); in the Lei do Inquilinato that law's wording of art. 32 "
                    "Parágrafo único ends it",
    "mp-2225-2001": "Medida Provisória nº 2.225-45, de 4.9.2001 (DOU 5.9.2001, edição extra) was in force on 11.9.2001, so "
                    "it stays in force until a later MP revokes it or Congress votes on it (Emenda Constitucional 32/2001, "
                    "art. 2)",
}
# Planalto marks the wording of a rejected MP '(Rejeitada)' where a lapsed one has '(Vigência encerrada)': read both
# as the end of the MP's effect (its day from MP_LAPSE).
P.LAPSED_WORDS = re.compile(r"\(?\s*Vig[êe]ncia\s+encerrada\s*\)?|\(\s*Rejeitad[ao]\s*\)", re.I)
# Lei 13.709/2018 (LGPD) art. 60, which rewrote Marco Civil art. 7 X and art. 16 II, is among the articles in force
# from 18.9.2020 (the Código Civil/LGPD part's reading of art. 65 as amended; same day here)
P.VIGENCIA_FIXED["lei-13709-2018"] = ("2020-09-18", "art. 65, II as amended (24 months after publication, Lei 13.853/2019; "
                                                    "MP 959/2020's postponement left out on conversion by Lei 14.058/2020, "
                                                    "published 18.9.2020): its art. 60 (Marco Civil) came into force on "
                                                    "18.9.2020, as in the LGPD part")
# Notes whose law number is a typo (the link gives the right law): note -> (fixed note, why)
P.NOTE_FIX = {
    "(Incluído pela Lei nº 15.581, de 2025)": (
        "(Incluído pela Lei nº 15.281, de 2025)",
        "Lei de Drogas art. 23 Parágrafo único: the note reads 'Incluído pela Lei nº 15.581, de 2025' but links to "
        "_Ato2023-2026/2025/Lei/L15281.htm, Lei nº 15.281, de 5.12.2025, whose art. 1 adds exactly that parágrafo único "
        "to art. 23"),
}
# Typing slip in a label (batch 3's TYPOS rule: only the label is corrected): Lei do Inquilinato art. 67 'd}' (the
# consolidated l8245compilado.htm prints 'd)')
B.TYPOS.append(("d} não ter sido o depósito integral", "d) não ter sido o depósito integral", "d)",
                "Lei do Inquilinato art. 67: the annotated page prints the alínea label 'd}', the consolidated page "
                "(l8245compilado.htm) 'd)'"))
B5.MP_REJECTED.clear()
B5.MP_REJECTED.update({
    "mp-1068-2021": ("Medida Provisória nº 1.068, de 2021: rejeitada",
                     "Medida Provisória nº 1.068, de 2021, rejected and returned by the President of Congress (Mensagem "
                     "nº 92 (CN), de 14 de setembro de 2021; Ato Declaratório nº 58, de 2021)"),
})
B5.PROMULGATED_PARTS = {}
B5.PROMULGATED_PARTS_USED.clear()
B5.LAPSE_RESTORED.clear()

SRC = HERE / "sources_batch5b.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

_write_part5 = B5.write_part


def write_part(*a) -> int:
    B5.EXTRA_DECISIONS[:] = []
    if SPLIT_USED:
        B5.EXTRA_DECISIONS.append(
            "An expression struck inside an unstruck paragraph by a Senate resolution (CF art. 52 X) is split into the "
            "wording before and after it, dated by the resolution: " + "; ".join(dict.fromkeys(SPLIT_USED)) + ".")
    if HEADING_NAME_FIX:
        B5.EXTRA_DECISIONS.append(
            "A struck chapter name Planalto prints as plain paragraph text right under its struck 'CAPÍTULO' line is "
            "read as that heading's name line, so it ends with the heading: " + "; ".join(dict.fromkeys(HEADING_NAME_FIX))
            + ".")
    if any(a_["slug"] == "marco-civil-da-internet" for a_ in B5.ACTS):
        B5.EXTRA_DECISIONS.append(
            "Marco Civil: Planalto marks the wording of the rejected Medida Provisória nº 1.068, de 2021 '(Rejeitada)' "
            "where a lapsed MP has '(Vigência encerrada)'; it is read the same way, with the day from the Ato "
            "Declaratório (see the MP fates). The STF's rulings on art. 19 are not marked on Planalto's page and are not "
            "part of this history.")
    rc = _write_part5(*a)
    # parse_proc words an MP with no end of its own as 'still pending'; here those are reissue chains and MPs kept in
    # force by EC 32/2001 art. 2, so the decision says 'stands'
    import json as _json
    part = _json.loads(B5.OUT.read_text(encoding="utf-8"))
    part["decisions"] = [d.replace(") still pending: ", ") stands: ") for d in part["decisions"]]
    tmp = B5.OUT.with_suffix(".json.tmp")
    tmp.write_text(_json.dumps(part, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8",
                   newline="\n")
    os.replace(tmp, B5.OUT)
    return rc


B5.write_part = B.write_part = P.write_part = write_part

if __name__ == "__main__":
    # stale-wording rules (../batch7/stale_fix.py), applied only when this part is written (not when imported)
    sys.path.insert(0, str(FOLDER / "batch7"))
    import stale_fix
    _build_plain = P.build_act
    _n: list[int] = []

    def _build_act_stale(paras, *a, **k):
        stale_fix.fix(P, paras, ACTS[len(_n)]["slug"] if len(_n) < len(ACTS) else "?", set())
        _n.append(1)
        return _build_plain(paras, *a, **k)
    P.build_act = B.build_act = _build_act_stale
    _inner_plain = _write_part5

    def _inner_stale(*a) -> int:
        B5.EXTRA_DECISIONS.extend(stale_fix.decisions())
        return _inner_plain(*a)
    _write_part5 = _inner_stale
    sys.exit(P.main(sys.argv[1:]))
