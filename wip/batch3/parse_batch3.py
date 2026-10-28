"""Reads the cache and writes scripts/brazil-law/corpus.d/90-batch3.json (SCHEMA.md corpus part).

    python -X utf8 scripts/brazil-law/batch3/parse_batch3.py [--stats] [--dry]

Imports ../proc/parse_proc.py (the CPP/CDC helper's struck-text replay of Planalto's annotated pages) and only
replaces its configuration: the acts, the hand tables, the pin file and the output. No network.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
sys.path.insert(0, str(FOLDER))
sys.path.insert(0, str(FOLDER / "proc"))
import fetch  # noqa: E402
import parse_proc as P  # noqa: E402

PL = P.PL
PAGES = {
    "ctn": "leis/l5172.htm",
    "ctn-compilado": "leis/l5172compilado.htm",
    "eca": "leis/l8069.htm",
    "eca-compilado": "leis/l8069compilado.htm",
    "ce": "leis/l4737.htm",
    "ce-compilado": "leis/l4737compilado.htm",
    "rju": "leis/l8112cons.htm",
    "rju-compilado": "leis/l8112compilado.htm",
}

ACTS: list[dict] = [
    {"slug": "codigo-tributario-nacional", "short": "CTN", "page": "ctn", "consolidated": "ctn-compilado",
     "law": "lei-5172-1966", "title": "Código Tributário Nacional (Lei nº 5.172, de 25 de outubro de 1966)",
     "digits": 3, "center_headings": False, "url": PL + "leis/l5172compilado.htm"},
    {"slug": "estatuto-da-crianca-e-do-adolescente", "short": "ECA", "page": "eca", "consolidated": "eca-compilado",
     "law": "lei-8069-1990", "title": "Estatuto da Criança e do Adolescente (Lei nº 8.069, de 13 de julho de 1990)",
     "digits": 3, "url": PL + "leis/l8069compilado.htm"},
    {"slug": "codigo-eleitoral", "short": "CE", "page": "ce", "consolidated": "ce-compilado",
     "law": "lei-4737-1965", "title": "Código Eleitoral (Lei nº 4.737, de 15 de julho de 1965)",
     "digits": 3, "url": PL + "leis/l4737compilado.htm"},
]
P.ACTS = ACTS

ACT_DAY = {
    "lei-5172-1966": ("1967-01-01", "Lei 5.172/1966 art. 218: 'Esta Lei entrará em vigor, em todo o território nacional, "
                                    "no dia 1º de janeiro de 1967' (published in the DOU of 27.10.1966, rectified "
                                    "31.10.1966)"),
    "lei-8069-1990": ("1990-10-14", "Lei 8.069/1990 art. 266: 'Esta Lei entra em vigor noventa dias após sua publicação' "
                                    "(published in the DOU of 16.7.1990, rectified 27.9.1990): 16.7.1990 + 90 days = "
                                    "14.10.1990"),
    "lei-4737-1965": ("1965-08-18", "Lei 4.737/1965 art. 382: 'Êste Código entrará em vigor 30 dias após a sua "
                                    "publicação' (published in the DOU of 19.7.1965, rectified 30.7.1965): 19.7.1965 + "
                                    "30 days = 18.8.1965"),
}
P.ACT_DAY = ACT_DAY


def _act_law(label, title, enacted, published, rel):
    return {"label": label, "title": title, "kind": "law", "enacted": enacted, "published": published,
            "url": PL + rel, "temporary_until": None, "restores": None, "note": None}


ACT_LAWS = {
    "lei-5172-1966": _act_law("Lei nº 5.172, de 1966", "Dispõe sôbre o Sistema Tributário Nacional e institui normas "
                              "gerais de direito tributário aplicáveis à União, Estados e Municípios.",
                              "1966-10-25", "1966-10-27", "leis/l5172.htm"),
    "lei-8069-1990": _act_law("Lei nº 8.069, de 1990", "Dispõe sobre o Estatuto da Criança e do Adolescente e dá outras "
                              "providências.", "1990-07-13", "1990-07-16", "leis/l8069.htm"),
    "lei-4737-1965": _act_law("Lei nº 4.737, de 1965", "Institui o Código Eleitoral.", "1965-07-15", "1965-07-19",
                              "leis/l4737.htm"),
}
P.ACT_LAWS = ACT_LAWS

# Lei 8.112/1990 (Regime Jurídico dos Servidores Públicos Civis da União), added once its checks pass
WITH_RJU = os.environ.get("BATCH3_RJU", "1") == "1"
if WITH_RJU:
    ACTS.append({"slug": "regime-juridico-dos-servidores-publicos", "short": "RJU", "page": "rju",
                 "consolidated": "rju-compilado", "law": "lei-8112-1990",
                 "title": "Regime Jurídico dos Servidores Públicos Civis da União (Lei nº 8.112, de 11 de dezembro de 1990)",
                 "digits": 3, "url": PL + "leis/l8112compilado.htm"})
    ACT_DAY["lei-8112-1990"] = ("1990-12-12", "Lei 8.112/1990 art. 252: 'Esta Lei entra em vigor na data de sua "
                                              "publicação, com efeitos financeiros a partir do primeiro dia do mês "
                                              "subseqüente' (published in the DOU of 12.12.1990, republished 18.3.1998)")
    ACT_LAWS["lei-8112-1990"] = _act_law("Lei nº 8.112, de 1990", "Dispõe sobre o regime jurídico dos servidores "
                                         "públicos civis da União, das autarquias e das fundações públicas federais.",
                                         "1990-12-11", "1990-12-12", "leis/l8112cons.htm")

# Vetoed parts Congress kept (CF art. 66 §§ 4-7): Planalto prints the struck '(Vetado)' line, then the kept wording
# marked '(Mantido pelo Congresso Nacional)', and at the end of the page the promulgation by the President of the
# Senate ('Senado Federal, 18 de abril de 1991 ... Este texto não substitui o publicado no DOU de 19.4.1991').
# act law -> (day the kept parts took effect, reason). The kept wording starts that day and the '(Vetado)' line ends.
KEPT_BY_CONGRESS: dict[str, tuple[str, str]] = {
    "lei-8112-1990": ("1991-04-19", "Lei 8.112/1990: the parts vetoed on 11.12.1990 that Congress kept were "
                                    "promulgated by the President of the Senate on 18.4.1991 (CF art. 66 § 7) and "
                                    "published in the DOU of 19.4.1991 (printed at the end of Planalto's l8112cons.htm); "
                                    "Planalto marks each such wording '(Mantido pelo Congresso Nacional)', a marker the "
                                    "history drops from the text. Until 19.4.1991 the dispositivo reads '(Vetado).'"),
}
# Vetoed parts of an amending law promulgated later (CF art. 66 § 5), read from the promulgation printed at the end of
# the law's own page: law -> (day, reason, {(act, unit, label)}). The law's wording of each listed dispositivo starts
# that day (not on the law's own day); a struck '(VETADO)' line the law's note puts there stands until then, and so
# does the wording it was to replace.
PROMULGATED: dict[str, tuple[str, str, set]] = {
    "lei-13509-2017": ("2018-02-23", "Lei 13.509/2017 (in force on publication, DOU 23.11.2017): the parts vetoed on "
                                     "22.11.2017 were promulgated after Congress overrode the veto ('eu promulgo, nos "
                                     "termos do parágrafo 5º do art. 66 da Constituição Federal, as seguintes partes "
                                     "vetadas', 22.2.2018, DOU 23.2.2018 edição extra, printed at the end of the Lei "
                                     "13.509 page): for the ECA art. 19 § 1º, art. 19-A §§ 6º and 10 and art. 19-B § 2º. "
                                     "Those wordings start on 23.2.2018; until then art. 19 § 1º keeps its 2009 wording "
                                     "and the others read '(VETADO).'",
                       {("estatuto-da-crianca-e-do-adolescente", "art-019", "§ 1º"),
                        ("estatuto-da-crianca-e-do-adolescente", "art-019-a", "§ 6º"),
                        ("estatuto-da-crianca-e-do-adolescente", "art-019-a", "§ 10"),
                        ("estatuto-da-crianca-e-do-adolescente", "art-019-b", "§ 2º")}),
}
VETADO_LINE = re.compile(r".*\(\s*VETAD[OA]\s*\)\.?", re.I)
KEPT = re.compile(r"\s*\(\s*Mantid[oa]s?\s+pelo\s+Congresso\s+Nacional\s*\)+")


SRC = HERE / "sources_batch3.json"
P.OUT = FOLDER / "corpus.d" / "90-batch3.json"


def sources() -> dict[str, dict]:
    return {i["id"]: i for i in json.loads(SRC.read_text(encoding="utf-8"))["fetch"]} if SRC.exists() else {}


P.sources = sources

# ---------------------------------------------------------------------------------------------------------------
# hand tables (same meaning as in parse_proc.py), emptied of the CPP/CDC entries and filled for these acts

# STF rulings (portal.stf.jus.br case pages, abaDecisoes + abaAndamentos, cached through fetch.get). As in
# parse_proc: a ruling binds from the publication of its judgment record (ata) in the Diário da Justiça, which is the
# version day. "where": whole dispositivos the ruling strikes (parse_proc's rule); [] for an expression struck inside a
# paragraph (the split rule above).
P.COURTS = {
    "stf-adi-869": {
        "label": "STF, ADI 869", "kind": "court", "enacted": "1999-08-04", "published": "1999-08-16",
        "title": "Ação direta de inconstitucionalidade 869: procedente; declara inconstitucional, no § 2º do art. 247 da "
                 "Lei nº 8.069, de 1990, a expressão \"ou a suspensão da programação da emissora até por dois dias, bem "
                 "como da publicação do periódico até por dois números\"",
        "url": "https://portal.stf.jus.br/processos/detalhe.asp?incidente=1563583",
        "from": "1999-08-16", "case": r"\b869\b", "where": [],
        "why": "STF, ADI 869 (Plenário, 4.8.1999): declared unconstitutional the expression 'ou a suspensão da "
               "programação da emissora até por dois dias, bem como da publicação do periódico até por dois números' in "
               "ECA art. 247 § 2º; judgment record (ata nº 22, of 4.8.1999) in a DJ extra edition dated 13.8.1999 that "
               "'circulou no dia 16/08/1999' (STF case record), the day the version takes effect. Planalto strikes the "
               "expression inside the paragraph, noting the case"},
    "stf-adi-2404": {
        "label": "STF, ADI 2.404", "kind": "court", "enacted": "2016-08-31", "published": "2016-09-12",
        "title": "Ação direta de inconstitucionalidade 2.404: procedente; declara inconstitucional a expressão \"em "
                 "horário diverso do autorizado\", contida no art. 254 da Lei nº 8.069, de 1990",
        "url": "https://portal.stf.jus.br/processos/detalhe.asp?incidente=1902202",
        "from": "2016-09-12", "case": r"2\.?404", "where": [],
        "why": "STF, ADI 2.404 (Plenário, 31.8.2016): declared unconstitutional the expression 'em horário diverso do "
               "autorizado' in ECA art. 254; judgment record published in the DJE on 12.9.2016 (STF case record), the "
               "day the version takes effect. Planalto strikes the expression inside the article, noting the case"},
}
P.EDITORIAL = {}
P.LAW_ALIAS = {}
P.NOTE_FIX = {}
P.MP_PENDING = {}
P.MP_LAPSE = {}
P.PUBLISHED_FIXED = {}
# Hand-checked in-force days where a law's own clause is staged (key -> (date, reason)), read from the law's page.
P.VIGENCIA_FIXED = {
    "lei-14690-2023": ("2023-10-03", "art. 37: 'Esta Lei entra em vigor: I - após decorridos 180 (cento e oitenta) dias "
                                     "de sua publicação oficial, quanto ao art. 30 desta Lei; e II - na data de sua "
                                     "publicação, quanto aos demais dispositivos' (DOU 3.10.2023, edição extra); its only "
                                     "change to these acts, the revocation of Código Eleitoral art. 7 § 1º IV, is in art. 36 "
                                     "I, so it took effect on publication"),
}
P.VIGENCIA_PROVISION = {}
P.VETO_PROMULGATION = {}
P.VETO_PROMULGATED_UNITS = {}
P.REWRITES = {}
P.REWRITE_BLOCKS = []
P.SAME_DAY_LAWS = set()
P.ACT_DECISIONS = []

# ---------------------------------------------------------------------------------------------------------------
# note forms these acts add to parse_proc's rules (wrappers: the original functions stay in charge of everything else)

_law_key, _law_label, _lexml_url, _page_info, _vigencia_of = P.law_key, P.law_label, P.lexml_url, P.page_info, P.vigencia_of
AC_REF = re.compile(r"Ato\s+Complementar\s*(?:n\s*[.\]]?\s*[º°o]?\s*\.?)?\s*(\d+)\s*,?\s*de\s*(\d{4})", re.I)


def law_key(text: str, year_of: dict | None = None) -> str | None:
    """parse_proc.law_key, plus 'Lcp nº 104' (CTN notes: Lei Complementar) and 'Ato Complementar nº 34, de 1967'
    (the CTN's 1966-67 amendments by Ato Complementar, key ac-34-1967)."""
    t = re.sub(r"\bLcp\b\.?", "Lei Complementar", text, flags=re.I)
    m = AC_REF.search(t)
    if m and not P.LAW_REF.search(t[:m.start()]):
        return f"ac-{int(m.group(1))}-{m.group(2)}"
    return _law_key(t, year_of)


def law_label(key: str) -> str:
    if key.startswith("ac-"):
        _, n, y = key.split("-")
        return f"Ato Complementar nº {int(n)}, de {y}"
    return _law_label(key)


def lexml_url(key: str, enacted: str | None) -> str | None:
    if key.startswith("ac-"):
        if not enacted:
            return None
        return f"{P.LEXML}ato.complementar:{enacted};{int(key.split('-')[1])}"
    return _lexml_url(key, enacted)


def page_info(key: str) -> dict:
    """parse_proc.page_info; for an Ato Complementar (whose header parse_proc does not read) the same fields read from
    its page: 'ATO COMPLEMENTAR Nº 34, DE 30 DE JANEIRO DE 1967', the DOU line, its vigência sentence."""
    if not key.startswith("ac-"):
        return _page_info(key)
    r = P.raw("law:" + key)
    if not r:
        return {}
    b, u = r
    t = P.decode(b)
    x = P.norm(P.htmlmod.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", t))))
    info: dict = {"source_url": u, "sha256": P.hashlib.sha256(b).hexdigest()}
    n = key.split("-")[1]
    m = re.search(r"ATO\s+COMPLEMENTAR\s+N\s*[º°O]?\s*\.?\s*0*" + n + r"\s*,?\s*DE\s+(\d{1,2})\s*[º°o]?\s+DE\s+(\w+)\s+DE\s+(\d{4})", x, re.I)
    if not m or m.group(2).lower() not in P.MONTHS:
        return {"bad_page": "the page is not this act: " + x[:120]}
    info["enacted"] = f"{int(m.group(3)):04d}-{P.MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    pubs = list(re.finditer(r"publicad[oa]\s+n[oa]\s+D\.?\s*O\.?\s*U\.?\s*(?:de\s*)?(\d{1,2})\s*º?\s*\.\s*(\d{1,2})\s*\.\s*(\d{4})", x, re.I))
    if pubs:
        p = pubs[-1]
        info["published"] = f"{int(p.group(3)):04d}-{int(p.group(2)):02d}-{int(p.group(1)):02d}"
    P.LEXML_USED.add(lexml_url(key, info.get("enacted")))
    lx = P.lexml_published(key, info.get("enacted"))
    if lx and lx != info.get("published"):
        P.PUB_CORRECTED[key] = (info.get("published"), lx)
        info["published"] = lx
    em = re.search(r"DE\s+\d{4}\s*\.?\s*(.*?\.)\s*O\s+PRESIDENTE", x[m.start():m.start() + 1500], re.S)
    info["title"] = em.group(1).strip() if em else ""
    cl = list(re.finditer(r"(?:Êste|Este|O\s+presente)\s+Ato(?:\s+Complementar)?\s+entra(?:r[áa])?\s+em\s+vigor[^.]*\.", x, re.I))
    info["clause"] = cl[-1].group(0) if cl else ""
    return info


FIXED_DAY = re.compile(r"entra(?:r[áa])?\s+em\s+vigor[^.]{0,80}?\b(?:em|no\s+dia|a\s+partir\s+de)\s+(\d{1,2})\s*[º°o]?\s+de\s+(\w+)\s+de\s+(\d{4})", re.I)


def vigencia_of(key: str, info: dict) -> tuple[str | None, str]:
    """parse_proc.vigencia_of, plus a clause naming a fixed day ('entrará em vigor em 1º de janeiro de 1969')."""
    d, why = _vigencia_of(key, info)
    if d is None and info.get("clause"):
        m = FIXED_DAY.search(info["clause"])
        if m and m.group(2).lower() in P.MONTHS:
            d = f"{int(m.group(3)):04d}-{P.MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
            return d, f"own clause names the day: '{m.group(0)}'"
    return d, why


P.law_key, P.law_label, P.lexml_url, P.page_info, P.vigencia_of = law_key, law_label, lexml_url, page_info, vigencia_of

# ---------------------------------------------------------------------------------------------------------------
# expressions struck inside a paragraph (a "mixed" paragraph: part struck, part not). parse_proc keeps such a paragraph
# as one text holding both wordings; here it becomes two wordings of the same dispositivo, the old one (struck words
# kept, replacement words left out) and the new one (unstruck words only), the change dated by the law or ruling the
# note names:
#   '(Expressão substituída pela Lei nº 12.010, de 2009)': the struck words are followed by their replacement
#   (EXPRESSION_SWAPS, read from the amending law's own text);
#   '(Expressão declarada inconstitucional pela ADI 2.404)': the struck words are dropped (COURTS).

_paragraphs, _lifespans = P.paragraphs, P.lifespans
SWAP_NOTE = re.compile(r"\(\s*Express(?:[ãa]o|[õo]es)\s+substitu[íi]das?\s+pel[ao]\s+[^)]*\)", re.I)
COURT_NOTE = re.compile(r"\(\s*Express(?:[ãa]o|[õo]es)\s+declarad[ao]s?\s+inconstitucion\w*\s+pel[ao]\s+ADIN?\s*(?:n\s*[º°]\s*)?([\d.]+)[^)]*\)", re.I)
# law -> [(struck words, replacement words)], each pair checked against the law's own text (see decisions)
EXPRESSION_SWAPS: dict[str, list[tuple[str, str]]] = {
    # Lei 12.010/2009 art. 3: 'A expressão "pátrio poder" contida nos arts. 21, 23, 24, no parágrafo único do art. 36,
    # no § 1º do art. 45, no art. 49, no inciso X do caput do art. 129, nas alíneas "b" e "d" do parágrafo único do
    # art. 148, nos arts. 155, 157, 163, 166, 169, no inciso III do caput do art. 201 e no art. 249 [...] bem como na
    # Seção II do Capítulo III do Título VI da Parte Especial [...] fica substituída pela expressão "poder familiar"'
    "lei-12010-2009": [("pátrio poder", "poder familiar"), ("Pátrio Poder", "Poder Familiar")],
}
SPLIT_PROBLEMS: list[str] = []
SPLITS: list[str] = []
PRINTED_AFTER: list[str] = []
# Typing slips in the annotated page, where the consolidated page has the plain form: (line start, corrected start,
# label, where). Only the label words are corrected; the rest of the line is the source's.
TYPOS: list[tuple[str, str, str, str]] = [
    ("arágrafo único. A votação continuará", "Parágrafo único. A votação continuará", "Parágrafo único",
     "Código Eleitoral art. 153: the annotated page prints 'arágrafo único.' (the consolidated page 'Parágrafo único.')"),
]
TYPOS_USED: set[str] = set()


def court_key(case: str) -> str:
    return "stf-adi-" + case.replace(".", "")


def paragraphs(html: str, digits: int) -> tuple[list[dict], list[str]]:
    out, rest = _paragraphs(html, digits)
    res: list[dict] = []
    for p in out:
        if p["state"] != "mixed":
            res.append(p)
            continue
        swap = next((n for n in p["notes"] if SWAP_NOTE.match(n)), None)
        court = next((n for n in p["notes"] if COURT_NOTE.match(n)), None)
        if swap:
            key = law_key(swap)
            pairs = EXPRESSION_SWAPS.get(key or "", [])
            old = p["text"]
            for s, r in pairs:
                old = old.replace(f"{s} {r}", s)
            new = old
            for s, r in pairs:
                new = new.replace(s, r)
            if not pairs or new != p["plain_text"] or old == p["text"]:
                SPLIT_PROBLEMS.append(f"{p['unit']} [{p['label']}] swap by {key} not matched: {p['text'][:90]!r}")
                res.append(p)
                continue
            note = swap
        elif court:
            key = court_key(COURT_NOTE.match(court).group(1))
            old, new = p["text"], p["plain_text"]
            if key not in P.COURTS:
                SPLIT_PROBLEMS.append(f"{p['unit']} [{p['label']}] ruling {key} not in COURTS: {p['text'][:90]!r}")
                res.append(p)
                continue
            note = court
        else:
            res.append(p)
            continue
        notes = [n for n in p["notes"] if n != note]
        base = {k: v for k, v in p.items() if k not in ("text", "state", "notes", "plain_text", "struck_text")}
        res.append({**base, "text": old, "state": "struck", "notes": notes, "plain_text": "", "struck_text": "",
                    "split": ("old", key)})
        res.append({**base, "text": new, "state": "plain", "notes": notes, "plain_text": "", "struck_text": "",
                    "split": ("new", key)})
        SPLITS.append(f"{p['unit']} [{p['label'] or 'heading'}] by {law_label(key) if not key.startswith('stf') else P.COURTS[key]['label']}")
    for p in res:
        for (start, fixed, label, _) in TYPOS:
            if p["text"].startswith(start):
                p["text"] = fixed + p["text"][len(start):]
                p["label"] = label
                TYPOS_USED.add(start)
        if KEPT.search(p["text"]):
            p["text"] = P.norm(KEPT.sub("", p["text"]))
            p["kept"] = True
        if any(KEPT.fullmatch(" " + n) for n in p["notes"]):
            p["notes"] = [n for n in p["notes"] if not KEPT.fullmatch(" " + n)]
            p["kept"] = True
    for i, p in enumerate(res):
        p["i"] = i
    return res, rest


def lifespans(paras: list[dict], cx) -> list[str]:
    problems = _lifespans(paras, cx)
    for p in paras:
        if not p.get("split"):
            continue
        side, key = p["split"]
        d = P.COURTS[key]["from"] if key in P.COURTS else cx.eff.get(key)
        if not d:
            problems.append(f"no in-force day for {key} (split {p['unit']} [{p['label']}])")
            continue
        if side == "new":
            p["start"], p["start_law"], p["restored"] = max(p["start"], d), key, False
        else:
            p["end"], p["end_law"], p["end_how"] = d, key, "expression"
    # a struck wording with no note printed right after the unstruck wording that replaced it (ECA art. 92 II: the
    # 2009 wording above the 1990 one): it ends when that wording starts
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end"] or p["notes"] or not p["label"] or i == 0:
            continue
        q = paras[i - 1]
        if (q["state"] == "plain" and q["unit"] == p["unit"] and q["label"] == p["label"] and q["start_law"]
                and q["start"] > p["start"]):
            p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "printed-after"
            PRINTED_AFTER.append(f"{cx.act} {p['unit']} [{p['label']}]")
            tags = (f"restored wording after an open one: {p['unit']} [{p['label']}] {p['text'][:80]!r}",
                    f"no end for struck {p['unit']} [{p['label']}] {p['text'][:90]!r}")
            problems[:] = [x for x in problems if not x.startswith(tags)]
    for law, (day, _, where) in PROMULGATED.items():
        old = cx.eff.get(law)
        if not old:
            continue
        for p in paras:
            if (cx.act, p["unit"], p["label"]) not in where or p["start_law"] != law or p["start"] != old:
                continue
            if VETADO_LINE.fullmatch(p["text"]) and p["state"] != "plain":
                p["end"], p["end_law"], p["end_how"] = day, law, "promulgation"
                continue
            p["start"], p["promulgated"] = day, True
            for q in paras:
                if (q is not p and q["unit"] == p["unit"] and q["label"] == p["label"] and q["state"] != "plain"
                        and q["end"] == old and q["end_law"] == law):
                    q["end"], q["end_how"] = day, "promulgation"
    hit = KEPT_BY_CONGRESS.get(next((a["law"] for a in ACTS if a["slug"] == cx.act), ""))
    if hit:
        law = next(a["law"] for a in ACTS if a["slug"] == cx.act)
        for i, p in enumerate(paras):
            if not p.get("kept") or p["start"] > hit[0]:
                continue
            p["start"], p["start_law"] = hit[0], law
            v = next((q for q in reversed(paras[max(0, i - 6):i]) if q["unit"] == p["unit"] and q["label"] == p["label"]
                      and q["state"] != "plain" and re.fullmatch(r".*\(\s*Vetad[oa]\s*\)\.?", q["text"], re.I)), None)
            if v is not None:  # else the dispositivo had no line at all until the kept wording (RJU art. 240 d)
                v["end"], v["end_law"], v["end_how"] = hit[0], law, "kept-by-congress"
    return problems


_apply_rewrites = P.apply_rewrites
VETOED_RENUMBER: list[str] = []


def apply_rewrites(paras: list[dict], act: dict, eff: dict, problems: list[str]) -> list[str]:
    """parse_proc.apply_rewrites, except that an unstruck 'Parágrafo único' is not ended by a '§ 1º' whose only
    wording is '(VETADO).' (CTN art. 205: LC 236/2026 made it § 1º, but that wording was vetoed; Planalto's consolidated
    page keeps the Parágrafo único above '§ 1º (VETADO).')."""
    out = _apply_rewrites(paras, act, eff, problems)
    for i, p in enumerate(paras):
        if p["state"] != "plain" or p["end_how"] != "renumbered":
            continue
        q = next((q for q in paras[i + 1:] if q["unit"] == p["unit"] and q["label"] == "§ 1º"), None)
        if q is not None and VETADO_LINE.fullmatch(q["text"]) and q["start"] == p["end"]:
            p["end"], p["end_law"], p["end_how"] = None, None, None
            VETOED_RENUMBER.append(f"{act['short']} {p['unit']}")
    return out


P.paragraphs, P.lifespans, P.apply_rewrites = paragraphs, lifespans, apply_rewrites

# ---------------------------------------------------------------------------------------------------------------
# the part file


def _requests() -> tuple[int, int, int]:
    src = sources()
    mine = {fetch.wayback(i["url"], i["ts"]) for i in src.values() if i.get("ts")}
    paths = {i["url"].split("://", 1)[1].lower() for i in src.values()}
    lexml = {u for u in P.LEXML_USED if u}
    courts = [c["url"] for c in P.COURTS.values()]
    n_pl = n_lx = n_stf = 0
    try:
        lines = fetch.LOG.read_text(encoding="utf-8").splitlines()
    except OSError:
        lines = []
    seen = set()
    for line in lines:
        u = json.loads(line)["url"]
        if u in seen:
            continue
        if u in mine:
            n_pl += 1
        elif "cdx/search" in u:
            q = urllib.parse.parse_qs(urllib.parse.urlsplit(u).query).get("url", [""])[0].lower()
            if q in paths:
                n_pl += 1
        elif u in lexml:
            n_lx += 1
        elif "portal.stf.jus.br" in u and any(c.rsplit("=", 1)[-1] in u for c in courts):
            n_stf += 1
        else:
            continue
        seen.add(u)
    return n_pl, n_lx, n_stf


def write_part(acts_out, laws, decisions, vig_notes, lindb, checks, problems, mpn) -> int:
    used = set()
    for act in acts_out:
        used.add(act["first_law"])
        for v in act["versions"]:
            for ls in v["credits"].values():
                used |= set(ls)
    for k in list(used):
        if laws.get(k, {}).get("restores"):
            used.add(laws[k]["restores"])
    laws = {k: laws[k] for k in sorted(used) if k in laws}
    n_pl, n_lx, n_stf = _requests()
    names = ", ".join(a["short"] for a in ACTS)
    srcs = [{
        "name": f"Planalto (Presidência da República), Legislação: annotated and consolidated pages of the {names} and "
                "of every law their notes cite, read as Internet Archive raw captures",
        "url": PL, "retrieved": P.RETRIEVED, "requests": n_pl,
        "licence": "Official acts are not protected by copyright (Lei 9.610/1998 art. 8, IV)",
        "notes": TERMS_NOTE + " Every page is the Internet Archive raw capture (web.archive.org/web/<ts>id_/<planalto "
                 "url>), byte-identical to what Planalto served; the capture timestamps are pinned in "
                 "batch3/sources_batch3.json."},
        {"name": "LexML Brasil (Senado Federal): record of each cited law, for its 'Publicação Original' DOU day",
         "url": "https://www.lexml.gov.br/", "retrieved": P.RETRIEVED, "requests": n_lx,
         "licence": "Public federal portal; bibliographic data of official acts",
         "notes": "One URN page per law (urn:lex:br:federal:<kind>:<date>;<number>); used only to check the DOU day "
                  "printed on the Planalto page."}]
    stf = [c for c in P.COURTS.values() if c["kind"] == "court"]
    if stf:
        srcs.append({"name": "Supremo Tribunal Federal: case pages of " + ", ".join(c["label"].replace("STF, ", "")
                                                                                       for c in stf),
                     "url": "https://portal.stf.jus.br/", "retrieved": P.RETRIEVED, "requests": n_stf,
                     "licence": "Public court records",
                     "notes": "Judgment day and the day the judgment record was published in the DJ (abaAndamentos)."})
    part = {
        "sources": srcs,
        "laws": laws,
        "acts": acts_out,
        "applies": [],
        "decisions": [
            "Acts of this part (" + "; ".join(x["title"] for x in ACTS) + "): each paragraph's life span is read from "
            "Planalto's annotated page of the act (" + ", ".join(sources()[x["page"]]["url"].rsplit("/", 1)[1] for x in ACTS) +
            "), with the replay of ../proc/parse_proc.py (imported, not copied): struck wordings stay in place before the "
            "wording that replaced them, each closed by the source's own note ('Redação dada pela…', 'Incluído pela…', "
            "'Revogado pela…'); text with no note is the act as enacted.",
            "Credits come only from those notes; a changed article with no note naming a law stays uncredited.",
            "A struck wording with no 'Revogado' note ends when the next wording of the same dispositivo (same label in the "
            "same article) starts; a Medida Provisória's wording with no later wording ends on the in-force day of the "
            "law that converted the MP (read from the MP page's 'Convertida na Lei' line).",
            "Medidas Provisórias are dated by publication (CF art. 62: force of law from publication); laws by their own "
            "vigência clause, else LINDB art. 1 (publication + 45 days).",
            *[f"{x['title']}: in force {ACT_DAY[x['law']][0]} ({ACT_DAY[x['law']][1]})." for x in ACTS],
            "Headings (Parte, Livro, Título, Capítulo, Seção) and the marginal headings (rubricas) are kept in one file per "
            "act, titulos.md, one line each; a note standing alone after a heading is given to the heading lines just "
            "before it.",
            "Text normalised once: NBSP to space, runs of spaces collapsed, curly quotes and dashes made plain, 'Art. 1o' "
            "written 'Art. 1º'; Planalto's link words ('Vigência', 'Produção de efeitos') and 'Vide' notes are dropped.",
            "The consolidated pages print a revoked dispositivo as its bare label ('Art. 757.'); the check ignores those "
            "label-only lines, and the history leaves revoked text out.",
            "No OCR: every text comes from the HTML text layer of the Planalto pages.",
            *P.ACT_DECISIONS,
            *([f"Expressions struck inside a paragraph (Planalto strikes the old words in place, followed by the new "
               f"ones or by nothing): each such paragraph is read as two wordings of the dispositivo, the old one up to "
               f"the day of the law or ruling its note names ('Expressão substituída pela…', 'Expressão declarada "
               f"inconstitucional pela ADI…'), the new one from then. Replacement words are taken from the amending law: "
               + "; ".join(f"{law_label(k)} replaces " + ", ".join(f"'{a}' with '{b}'" for a, b in v)
                           for k, v in EXPRESSION_SWAPS.items()) + f". Paragraphs read this way ({len(SPLITS)}): "
               + "; ".join(SPLITS) + "."] if SPLITS else []),
            *[f"{law_label(k)}: {why}." for k, (_, why, _) in PROMULGATED.items()],
            *[f"Typing slip corrected: {w}." for (a, _, _, w) in TYPOS if a in TYPOS_USED],
            *([f"An unstruck 'Parágrafo único' stays when the '§ 1º' a later law put below it reads only '(VETADO).' "
               f"(the law's renumbering was vetoed; the consolidated page keeps both): " + "; ".join(VETOED_RENUMBER) + "."]
              if VETOED_RENUMBER else []),
            *([f"Struck wordings with no note printed directly after the unstruck wording that replaced them end when "
               f"that wording starts ({len(PRINTED_AFTER)}): " + "; ".join(PRINTED_AFTER) + "."] if PRINTED_AFTER else []),
            *[f"{why}." for k, (_, why) in KEPT_BY_CONGRESS.items() if any(a["law"] == k for a in ACTS)],
            *[f"{a['title']}: {P.REWRITES[a['slug']][2]}" for a in ACTS if a["slug"] in P.REWRITES],
            *[f"{x[4]}." for x in P.REWRITE_BLOCKS],
            *[f"{P.law_label(k)}: {why}." for k, (d, why) in P.VETO_PROMULGATION.items()],
        ] + decisions + mpn + vig_notes + ([
            "Laws with no vigência clause of their own are dated by LINDB art. 1 (publication + 45 days): " + "; ".join(lindb) + "."
        ] if lindb else []) + [
            f"Replay check, {act}: the last version differs from Planalto's consolidated page in {len(d)} articles" +
            (": " + "; ".join(d) if d else ".") for act, d in checks.items()
        ] + ([f"Open problems in the replay ({len(problems)}): " + "; ".join(problems[:60])] if problems else []),
        "ai_use": ["Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote batch3/fetch_batch3.py and batch3/parse_batch3.py "
                   "(configuration of ../proc/fetch_proc.py and ../proc/parse_proc.py, imported) and the hand tables in "
                   "them (vigência days, MP fates, court rulings) from the official pages. No model wrote, summarised or "
                   "changed legal text; no model runs at data-build or git-build time."],
    }
    out = P.OUT
    out.parent.mkdir(exist_ok=True)
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(part, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8",
                   newline="\n")
    os.replace(tmp, out)
    print("wrote", out, out.stat().st_size, "bytes;", sum(len(x["versions"]) for x in acts_out), "versions")
    return 0


P.write_part = write_part

TERMS_NOTE = ("Terms checked 2026-10-28: www.planalto.gov.br has no robots.txt (Wayback captures of /robots.txt return "
              "Planalto's 'O conteúdo não foi encontrado' page); the gov.br Termo de Uso (capture 20261015002456 of "
              "https://www.gov.br/pt-br/termos-de-uso) sets no rule against automated access and states the portal's own "
              "content is CC BY-ND 3.0; the legal texts are official acts, outside copyright (Lei 9.610/1998 art. 8, IV). "
              "Planalto answers non-browser clients with a bot challenge, so it was never contacted directly.")


def main(argv: list[str]) -> int:
    return P.main(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
