"""Reads the cache and writes scripts/brazil-law/corpus.d/95-rju.json: Lei 8.112/1990, the Regime Jurídico dos
Servidores Públicos Civis da União, as its own corpus part (SCHEMA.md "corpus.d").

    python -X utf8 scripts/brazil-law/rju/parse_rju.py [--stats] [--dry]

Batch 3 (../batch3/parse_batch3.py, which configures ../proc/parse_proc.py) already holds the RJU behind
BATCH3_RJU=1. This module turns that switch on, keeps only the RJU among batch 3's acts, and adds what the RJU needs:
the fates of its Medidas Provisórias (lapse days from the Atos Declaratórios, conversions, MP 2.225-45/2001 kept by
EC 32), the staged vigência clauses of MP 664/2014, Lei 13.135/2015 and MP 871/2019, and the remaining-difference
notes. Batch 3's own part (90-batch3.json) is not touched: run batch 3's parser without BATCH3_RJU and it writes the
same bytes as before. No network.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

os.environ["BATCH3_RJU"] = "1"
HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
sys.path.insert(0, str(FOLDER / "batch3"))
import parse_batch3 as B  # noqa: E402

P = B.P
RJU = "lei-8112-1990"
SLUG = "regime-juridico-dos-servidores-publicos"
OUT = FOLDER / "corpus.d" / "95-rju.json"
STAGE = HERE / ".tmp" / "stage.json"   # batch 3's write_part writes here; the part is finished from it

# only the RJU among batch 3's acts
B.ACTS[:] = [a for a in B.ACTS if a["law"] == RJU]
for table in (B.ACT_DAY, B.ACT_LAWS):
    for k in [k for k in table if k != RJU]:
        del table[k]
# batch 3's rulings concern the CTN and the ECA. The RJU has one: a Senate resolution suspending, after a final STF
# ruling, the execution of provisions (CF art. 52 X), a legislative act, so kind "law" (as batch 3's RSF 337/1983); it
# takes effect on its DOU publication. Planalto strikes the provisions with 'Execução suspensa pela RSF nº 46, de 1997'.
RJU_WHERE = [(SLUG, "art-008", "IV -"), (SLUG, "art-023", "Art. 23"), (SLUG, "art-023", "§ 1º"), (SLUG, "art-023", "§ 2º")]
P.COURTS = {
    "rsf-46-1997": {
        "label": "Resolução do Senado Federal nº 46, de 1997", "kind": "law", "enacted": "1997-05-23",
        "published": "1997-05-26",
        "title": "Suspende a execução do art. 8º, IV, e do art. 23 e seus parágrafos, da Lei nº 8.112, de 11 de dezembro "
                 "de 1990.",
        "url": P.PL + "Congresso/RSF/ResSF46-1997.htm",
        "from": "1997-05-26", "case": r"RSF\s*n[º°]?\s*46\b", "where": RJU_WHERE,
        "why": "Resolução do Senado Federal nº 46, de 23.5.1997 (DOU 26.5.1997; Planalto page ResSF46-1997.htm, capture "
               "20080414200129): 'É suspensa a execução do art. 8º, IV, e do art. 23 e seus parágrafos, da Lei nº 8.112 "
               "[...] declarados inconstitucionais por decisão definitiva do Supremo Tribunal Federal no Mandado de "
               "Segurança nº 22148-8' (CF art. 52 X), in force on publication. Planalto strikes RJU art. 8 IV and art. 23 "
               "(caput, §§ 1º and 2º) with the note 'Execução suspensa pela RSF nº 46, de 1997'; the history ends them on "
               "26.5.1997, credited to the resolution (kind law: a Senate act), before Lei 9.527/1997 (in force "
               "11.12.1997) revoked them"},
}
B.PROMULGATED.clear()    # ECA only

# ---------------------------------------------------------------------------------------------------------------
# pins: batch 3's, plus rju/sources_rju.json (rju/fetch_rju.py), which wins for the same id

SRC = HERE / "sources_rju.json"
_b_sources = B.sources


def sources() -> dict[str, dict]:
    s = dict(_b_sources())
    if SRC.exists():
        s.update({i["id"]: i for i in json.loads(SRC.read_text(encoding="utf-8"))["fetch"]})
    return s


B.sources = P.sources = sources

# ---------------------------------------------------------------------------------------------------------------
# Medidas Provisórias

# Lapse days, each read from the Ato Declaratório of the President of the Mesa of Congress that the RJU page links from
# the MP's '(Vigência encerrada)' note (pinned as ato:<mp> in sources_rju.json): the MP's wording stops having effect
# the day after its term ended, and the wording it replaced is back from that day (CF art. 62 §§ 3, 7 and 11).
P.MP_LAPSE = {
    "mp-689-2015": ("2016-02-08", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 1, de 2016 (DOU "
                                  "12.2.2016): 'teve seu prazo de vigência encerrado no dia 7 de fevereiro do corrente "
                                  "ano'; the replaced wording is back from 8.2.2016"),
    "mp-792-2017": ("2017-11-29", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 65, de 2017 (DOU "
                                  "7.12.2017): 'teve seu prazo de vigência encerrado no dia 28 de novembro do corrente "
                                  "ano'; the replaced wording is back from 29.11.2017"),
    "mp-805-2017": ("2018-04-09", "Ato do Presidente da Mesa do Congresso Nacional nº 19, de 2018 (DOU 10.4.2018): 'teve "
                                  "seu prazo de vigência encerrado no dia 8 de abril do corrente ano'; the replaced wording "
                                  "is back from 9.4.2018"),
    "mp-873-2019": ("2019-06-29", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 43, de 2019: 'teve seu "
                                  "prazo de vigência encerrado no dia 28 de junho'; the replaced wording is back from "
                                  "29.6.2019"),
}
# Medidas Provisórias of before Emenda Constitucional 32/2001 stay in force until a later MP revokes them or Congress
# votes on them (EC 32/2001 art. 2): their wording stands like a law's. parse_proc's MP_PENDING gives exactly that (no
# end date); the decision line says why.
MP_STANDING = {
    "mp-2225-2001": "Medida Provisória nº 2.225-45, de 4.9.2001 (DOU 5.9.2001, edição extra) was in force on 11.9.2001, "
                    "so it stays in force until a later MP revokes it or Congress votes on it (Emenda Constitucional "
                    "32/2001, art. 2); neither had happened by the retrieval day, so its wording stands. Planalto credits "
                    "its changes to this last reissue; the earlier reissues (from MP 1.815/1999) are not separated"}
P.MP_PENDING = dict(MP_STANDING)
# Conversion laws a page prints in a form parse_proc's pattern does not read: key -> (law, why)
CONVERTED_FIX = {
    "mp-1132-2022": ("lei-14509-2022", "the MP 1.132/2022 page prints 'Convertida na Lei nº 14 509, de 2022' (a space "
                                       "for the thousands point); it is Lei nº 14.509, de 2022, whose page the RJU note "
                                       "'(Revogado pela Lei nº 14.509, de 2022)' links"),
}
_page_info = P.page_info


def page_info(key: str) -> dict:
    info = _page_info(key)
    if key in CONVERTED_FIX and info and not info.get("converted"):
        info["converted"] = CONVERTED_FIX[key][0]
    return info


P.page_info = page_info

# ---------------------------------------------------------------------------------------------------------------
# staged vigência clauses, read from each act's own page

P.VIGENCIA_FIXED.update({
    "mp-664-2014": ("2015-03-01", "art. 5: 'Esta Medida Provisória entra em vigor: I - na data de sua publicação para "
                                  "[arts. 60 §§ 5º-6º and 74 § 1º of Lei 8.213 and its own arts. 2, 4 and 6 II a, d]; II - "
                                  "quinze dias a partir da sua publicação para o § 2º do art. 74 da Lei nº 8.213; e III - no "
                                  "primeiro dia do terceiro mês subseqüente à data de publicação desta Medida Provisória "
                                  "quanto aos demais dispositivos' (DOU 30.12.2014, edição extra). Its changes to Lei 8.112 "
                                  "(art. 3, and the revocations of art. 6 I) fall under III: 1.3.2015; Planalto links each "
                                  "of them to art. 5 III ('Vigência')"),
    "lei-13135-2015": ("2015-06-18", "art. 6: 'Esta Lei entra em vigor em: I - 180 (cento e oitenta) dias a partir de sua "
                                     "publicação, quanto à inclusão de pessoas com deficiência grave entre os dependentes "
                                     "[...] do Regime Próprio de Previdência Social (RPPS) previstos na Lei nº 8.112 [...]; "
                                     "II - 2 (dois) anos para a nova redação: [...] b) do art. 217, inciso IV, alínea \"c\", "
                                     "da Lei nº 8.112 [...]; III - na data de sua publicação, para os demais dispositivos' "
                                     "(DOU 18.6.2015). Its changes to Lei 8.112 take effect on publication, 18.6.2015, except "
                                     "art. 217 IV c (below)"),
    "mp-871-2019": ("2019-01-18", "art. 39: in force 90 days after publication for Lei 8.742 art. 20 § 13, 120 days for "
                                  "Lei 8.213 art. 74 § 3º, 'III - na data de sua publicação, quanto aos demais "
                                  "dispositivos' (DOU 18.1.2019, edição extra): its changes to Lei 8.112 take effect on "
                                  "publication"),
})
# One line whose in-force day differs from the rest of its law (parse_proc's VIGENCIA_PROVISION works per article):
# (act, unit, label, start of the text, law, day, reason)
LINE_VIGENCIA = [
    (SLUG, "art-217", "c)", "c) tenha deficiência grave", "lei-13135-2015", P.months_rule("2015-06-18", 2, "anos")[0],
     "Lei 8.112 art. 217 IV c ('c) tenha deficiência grave; ou'), written by Lei 13.135/2015 art. 3: its art. 6 II b "
     "gives 'a nova redação [...] do art. 217, inciso IV, alínea \"c\"' 2 years (published 18.6.2015; the period ends on "
     "the same calendar day and the law is in force the day after, as for the other Brazil parts), and Planalto links the "
     "alínea to art. 6 II ('Vigência'). Art. 6 I (180 days, 'inclusão de pessoas com deficiência grave entre os "
     "dependentes [...] RPPS') names no other dispositivo of Lei 8.112, and II b names this alínea, so the history dates "
     "it by II b"),
]
LINE_USED: list[str] = []
_lifespans = B.lifespans


def lifespans(paras: list[dict], cx) -> list[str]:
    problems = _lifespans(paras, cx)
    # the resolution ends its provisions even where a later revocation note (Lei 9.527/1997) ended them first in the
    # replay (parse_proc's court rule only fills an open end)
    for k, c in P.COURTS.items():
        for p in paras:
            if ((cx.act, p["unit"], p["label"]) in c["where"] and p["state"] != "plain"
                    and any(re.search(c["case"], n) for n in p["notes"]) and p["end"] and p["end"] > c["from"]):
                p["end"], p["end_law"], p["end_how"] = c["from"], k, "court"
    for slug, unit, label, start, law, day, _ in LINE_VIGENCIA:
        if slug != cx.act:
            continue
        hit = [p for p in paras if p["unit"] == unit and p["label"] == label and p["text"].startswith(start)
               and p["start_law"] == law]
        if len(hit) != 1:
            problems.append(f"LINE_VIGENCIA {unit} [{label}] {start!r}: {len(hit)} lines")
            continue
        p = hit[0]
        old = p["start"]
        p["start"] = day
        for q in paras:
            if q is not p and q["unit"] == unit and q["label"] == label and q["end"] == old and q["end_law"] == law:
                q["end"] = day
        LINE_USED.append(f"{unit} [{label}] from {day}")
    return problems


B.lifespans = P.lifespans = lifespans

# A note Planalto printed without its opening parenthesis and followed by '(Vigência encerrada)', so parse_proc's
# BARE_NOTE (which wants it at the very end of the line) leaves it in the text: it is moved to the notes.
OPEN_NOTE = re.compile(r"\s+((?:Reda[çc][ãa]o\s+dada|Inclu[íi]d[oa]|Revogad[oa])\s+pel[oa]\s+(?:Lei|Medida\s+Provis[óo]ria)"
                       r"\s+n[º°]\s*[\d.]+(?:-\d+)?,\s+de\s+[\d.]+\))$")
NOTES_MOVED: list[str] = []
_paragraphs = B.paragraphs


def paragraphs(html: str, digits: int) -> tuple[list[dict], list[str]]:
    out, rest = _paragraphs(html, digits)
    for p in out:
        m = OPEN_NOTE.search(p["text"])
        if m:
            p["text"] = p["text"][:m.start()]
            p["notes"] = ["(" + m.group(1)] + p["notes"]
            NOTES_MOVED.append(f"{p['unit']} [{p['label']}] '{m.group(1)}'")
    for unit, after, _ in TABLE_ROWS:
        k = next((k for k, p in enumerate(out) if p["unit"] == unit and p["text"].startswith(after)), None)
        if k is None:
            continue
        j = k + 1
        while j < len(out) and out[j]["heading"] and not out[j]["notes"] and not P.HEADING.match(out[j]["text"]):
            out[j].update(unit=unit, label="", heading=False)
            j += 1
        ROWS_MOVED.append(f"{unit}: {j - k - 1} rows")
    return out, rest


B.paragraphs = P.paragraphs = paragraphs

# Lines no note dates, dated by hand from the amending act's own text (each read on its pinned page):
# (unit, label, start of the text, law, how, reason). how: "end" ends a struck line on the law's day; "start" starts an
# unstruck line on the law's day (credited to it); "gap" takes an unstruck line out while the law (a lapsed MP) was in
# force (credited to the MP, then to its lapse).
HAND = [
    ("art-091", "§ 1º", "§ 1º A licença poderá ser interrompida, a qualquer tempo, a pedido do servidor ou no interesse",
     "mp-2225-2001", "end",
     "art. 91 § 1º as enacted ('A licença poderá ser interrompida, a qualquer tempo, a pedido do servidor ou no interesse "
     "do serviço.'), struck with no note: MP 2.225-45/2001 art. 1 rewrote art. 91 as a caput and a 'Parágrafo único' with "
     "these same words, ending the § 1º on its day"),
    ("art-091", "§ 2º", "§ 2º Não se concederá nova licença antes de decorridos dois anos", "mp-2225-2001", "end",
     "art. 91 § 2º as Lei 9.527/1997 wrote it, struck with no note of its end: MP 2.225-45/2001 art. 1 rewrote art. 91 "
     "whole (caput and 'Parágrafo único', closed '(NR)' with no line of dots), so the § 2º ends on its day"),
    ("art-091", "Parágrafo único", "Parágrafo único. A licença poderá ser interrompida", "mp-792-2017", "gap",
     "art. 91 Parágrafo único (MP 2.225-45/2001), not struck: MP 792/2017 art. 26 gave art. 91 a § 1º ('A licença poderá "
     "ser interrompida, a qualquer tempo, a pedido do servidor ou a interesse do serviço público') and a § 2º, which "
     "replace a 'Parágrafo único'; it is out while MP 792 was in force and back when MP 792 lapsed"),
    ("art-098", "Parágrafo único", "Parágrafo único. Para efeito do disposto neste artigo", "lei-9527-1997", "end",
     "art. 98 Parágrafo único as enacted, struck with no note: Lei 9.527/1997 art. 1 wrote art. 98 § 1º ('Para efeito do "
     "disposto neste artigo, será exigida a compensação de horário no órgão ou entidade que tiver exercício [...]') with "
     "§§ 2º and 3º, so the Parágrafo único ends on its day"),
    ("art-098", "§ 1º", "§ 1º Para efeito do disposto neste artigo", "lei-9527-1997", "start",
     "art. 98 § 1º, printed with no note: its words are those of Lei 9.527/1997 art. 1 (above), so it starts on that "
     "law's day, credited to it"),
    # placeholders Planalto prints for an MP's insertion whose wording it does not give, with only a 'Vide' note: no
    # text, no day of their own, so they are left out (the MP period is listed in the decisions)
    ("art-051", "IV -", "IV -", "mp-301-2006", "skip",
     "art. 51 IV: a struck bare 'IV -' with only '(Vide Medida Provisória nº 301 de 2006)', a placeholder for MP "
     "301/2006's inciso, whose wording the page does not give; left out ('IV - auxílio-moradia.' starts with Lei "
     "11.355/2006)"),
    ("titulos", "h24-0", "Subseção IV", "mp-301-2006", "skip",
     "the heading 'Subseção IV / Do Auxílio-Moradia' printed first with only '(Vide Medida Provisória nº 301 de 2006)' "
     "(number line unstruck, name line struck), then again with '(Incluído pela Lei nº 11.355, de 2006)': the first "
     "copy is MP 301/2006's subsection, whose articles the page does not print, so both of its lines are left out and the "
     "subsection starts with Lei 11.355/2006"),
    ("titulos", "h24-1", "Do Auxílio-Moradia", "mp-301-2006", "skip", "as the line above"),
    ("art-060-b", "IX -", "IX -.", "mp-341-2006", "skip",
     "art. 60-B IX: a struck bare 'IX -.' with only '(Vide Medida Provisória nº 341, de 2006)', a placeholder for MP "
     "341/2006's inciso, whose wording the page does not give; left out (IX starts with Lei 11.490/2007)"),
]
# Rows of a table Planalto centres (so parse_proc reads them as headings) that belong to the article above them:
# (unit, start of the line the table follows, reason). The rows move into that article as unlabeled lines, so they
# live with that line (batch 3's rule for unlabeled rows).
TABLE_ROWS = [
    ("art-217", "I - o tempo de duração da pensão por morte será calculado de acordo com a expectativa de sobrevida",
     "art. 217 § 3º I as MP 664/2014 wrote it ('conforme tabela abaixo'): its table of life expectancy and pension "
     "duration ('Expectativa de sobrevida à idade x ...' to 'vitalícia', 14 struck centred cells) is part of that inciso, "
     "not a heading; it lives with it, from MP 664's day (1.3.2015) to Lei 13.135/2015"),
]
ROWS_MOVED: list[str] = []
MP_VIDE_NOTE = ("Medidas Provisórias whose wording Planalto's annotated page does not print (only a 'Vide' note on the "
                "lines they touched): MP 301/2006 (in force 30.6.2006: arts. 51 IV, 52, 93 § 2º and Subseção IV, arts. "
                "60-A to 60-E), MP 341/2006 (art. 60-B IX) and MP 359/2007 (arts. 76-A and 98 § 4º). The history goes "
                "from the wording before each MP straight to the wording of the law that converted it (Lei 11.355/2006, "
                "Lei 11.490/2007, Lei 11.501/2007), on that law's day; the MP periods are not shown.")
HAND_USED: list[str] = []
_apply_rewrites = B.apply_rewrites


def apply_rewrites(paras: list[dict], act: dict, eff: dict, problems: list[str]) -> list[str]:
    out = _apply_rewrites(paras, act, eff, problems)
    lapse = {k: (d, k + "-fim") for k, (d, _) in P.MP_LAPSE.items()}
    for unit, label, start, law, how, _ in HAND:
        if how == "skip":   # only a line whose every note is a 'Vide' naming the law
            n = re.compile(r"Medida Provisória nº " + law.split("-")[1] + r",? de " + law.split("-")[2])
            hit = [p for p in paras if p["unit"] == unit and p["label"] == label and p["text"].startswith(start)
                   and p["notes"] and all(x.startswith("(Vide") and n.search(x) for x in p["notes"])]
        else:
            hit = [p for p in paras if p["unit"] == unit and p["label"] == label and p["text"].startswith(start)
                   and (p["state"] == "plain") == (how != "end")]
        if len(hit) != 1 or (how != "skip" and law not in eff) or (how == "gap" and law not in lapse):
            out.append(f"HAND {unit} [{label}] {start[:40]!r}: {len(hit)} lines")
            continue
        p, day = hit[0], eff.get(law)
        if how == "skip":
            p["skip"], p["end_how"] = True, "hand-skip"
            B.UNDATED[:] = [u for u in B.UNDATED if u != f"{act['short']} {p['unit']} [{p['label'] or 'line'}] {p['text'][:60]!r}"]
        elif how == "end":
            tag = f"{act['short']} {p['unit']} [{p['label'] or 'line'}] {p['text'][:60]!r}"
            B.UNDATED[:] = [u for u in B.UNDATED if u != tag]
            p["end"], p["end_law"], p["end_how"], p["skip"] = day, law, "hand", False
        elif how == "start":
            p["start"], p["start_law"] = day, law
        else:
            p["gaps"].append((day, lapse[law][0], law, lapse[law][1]))
        HAND_USED.append(f"{unit} [{label}] {how} {day}")
    return out


B.apply_rewrites = P.apply_rewrites = apply_rewrites


def mp_notes(infos: dict, eff: dict) -> list[str]:
    out = []
    for k, info in sorted(infos.items()):
        if not k.startswith("mp-") or not info:
            continue
        if info.get("converted") and info["converted"] in eff:
            out.append(f"{P.law_label(k)} (in force {eff[k]}) was converted into {P.law_label(info['converted'])} "
                       f"(in force {eff[info['converted']]})" + (f" ({CONVERTED_FIX[k][1]})" if k in CONVERTED_FIX else ""))
        elif k in P.MP_LAPSE:
            out.append(f"{P.law_label(k)} (in force {eff.get(k)}) lapsed: {P.MP_LAPSE[k][1]}")
        elif k in MP_STANDING:
            out.append(f"{P.law_label(k)} (in force {eff.get(k)}) stands: {MP_STANDING[k]}")
        elif k in P.MP_PENDING:
            out.append(f"{P.law_label(k)} (in force {eff.get(k)}) still pending: {P.MP_PENDING[k]}")
    return ["Medidas Provisórias and their fate, from each MP page's 'Convertida na Lei' line or the Congress records: "
            + "; ".join(out) + "."] if out else []


P.mp_notes = mp_notes

# ---------------------------------------------------------------------------------------------------------------
# remaining differences from Planalto's consolidated page, each checked by hand against both pages

B.EXPLAINED[SLUG] = {
    "art-060-b": "typesetting: the annotated page ends inciso V with 'ou equivalentes;', the consolidated page drops the "
                 "semicolon",
    "art-078": "the consolidated page prints the placeholder '§ 1º e § 2º' for the paragraphs Lei 9.527/1997 revoked; "
               "the history leaves revoked text out",
    "art-133": "typesetting: the consolidated page ends inciso I with 'objeto da apuração;', the annotated page drops "
               "the semicolon",
    "art-217": "the consolidated page prints art. 217 IV c only as 'c) (Vide Lei nº 13.135, de 2015) (Vigência)', "
               "without its words; the annotated page gives them ('c) tenha deficiência grave; ou', Redação dada pela Lei "
               "13.135/2015) and so does Lei 13.135/2015 art. 3, so the history keeps them (from 19.6.2017, see the "
               "staged clause)",
}

# ---------------------------------------------------------------------------------------------------------------
# the part file: batch 3's write_part, then the RJU's own sources, notes and requests

_write_part = B.write_part


def _cc_requests(pins: dict[str, dict]) -> int:
    """Requests gitlaw_common/wayback.py logged for these pins (Common Crawl ranges and archive.org captures + CDX)."""
    log = FOLDER / ".cache" / "cc" / "requests.jsonl"
    want = set()
    for i in pins.values():
        if i.get("cc"):
            c = i["cc"]
            want.add(f'cc:{c["filename"]}:{c["offset"]}:{c["length"]}')
        elif i.get("via") == "wayback.py":
            want.add(B.fetch.wayback(i["url"], i["ts"]))
            want.add("cdx:" + i["url"].split("://", 1)[1].lower())
    n, seen = 0, set()
    for line in (log.read_text(encoding="utf-8").splitlines() if log.exists() else []):
        u = json.loads(line)["url"]
        key = u
        if "cdx/search" in u:
            m = re.search(r"[?&]url=([^&]+)", u)
            key = "cdx:" + (m.group(1).lower() if m else "")
        if key in want and key not in seen:
            seen.add(key)
            n += 1
    return n


def write_part(acts_out, laws, decisions, vig_notes, lindb, checks, problems, mpn) -> int:
    used = {a["first_law"] for a in acts_out}
    for act in acts_out:
        for v in act["versions"]:
            for ls in v["credits"].values():
                used |= set(ls)
    used |= {laws[k]["restores"] for k in used if laws.get(k, {}).get("restores")}
    allp = sources()
    pins = {k: v for k, v in allp.items()
            if k in ("rju", "rju-compilado") or (k.startswith(("law:", "ato:")) and k.split(":", 1)[1] in used)}
    B.sources = lambda: pins          # batch 3's request count and page names: only the pins this part uses
    try:
        decisions = decisions + ([f"A line whose in-force day differs from the rest of its law: {why}."
                                  for (_, _, _, _, _, _, why) in LINE_VIGENCIA] if LINE_USED else []) + (
            [f"Lines no note dates, dated from the amending act's own text or left out ({len(HAND_USED)}): "
             + "; ".join(why for (*_, why) in HAND) + "."] if HAND_USED else []) + (
            [f"Notes Planalto printed without their opening parenthesis, read as notes ({len(NOTES_MOVED)}): "
             + "; ".join(NOTES_MOVED) + "."] if NOTES_MOVED else []) + (
            [f"Table rows read as part of an article, not as headings: {why} ({'; '.join(ROWS_MOVED)})."
             for (*_, why) in TABLE_ROWS] if ROWS_MOVED else []) + [MP_VIDE_NOTE]
        P.OUT = STAGE
        STAGE.parent.mkdir(exist_ok=True)
        _write_part(acts_out, laws, decisions, vig_notes, lindb, checks, problems, mpn)
    finally:
        B.sources = sources
    part = json.loads(STAGE.read_text(encoding="utf-8"))
    pl = part["sources"][0]
    pl["name"] = ("Planalto (Presidência da República), Legislação: annotated and consolidated pages of Lei 8.112/1990 "
                  "(RJU), of every law its notes cite and of the Atos Declaratórios of the President of Congress for its "
                  "lapsed Medidas Provisórias, read as Internet Archive raw captures"
                  + (" and Common Crawl captures" if any(i.get("cc") for i in pins.values()) else ""))
    pl["requests"] += _cc_requests(pins)
    pl["notes"] = pl["notes"].replace(
        "batch3/sources_batch3.json.",
        "batch3/sources_batch3.json and rju/sources_rju.json (the latter fetched through scripts/gitlaw_common/wayback.py"
        + ("; Common Crawl captures are pinned by crawl, WARC file, offset and length and used under the Common Crawl "
           "terms of use" if any(i.get("cc") for i in pins.values()) else "") + ").")
    part["ai_use"] = ["Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote rju/fetch_rju.py and rju/parse_rju.py "
                      "(configuration of ../batch3 and ../proc, imported) and the hand tables in them (MP lapse days, "
                      "staged vigência days, explained differences) from the official pages; batch 3's tables come from "
                      "batch3/parse_batch3.py. No model wrote, summarised or changed legal text; no model runs at "
                      "data-build or git-build time."]
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(part, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8",
                   newline="\n")
    os.replace(tmp, OUT)
    print("wrote", OUT, OUT.stat().st_size, "bytes;", sum(len(x["versions"]) for x in acts_out), "versions")
    return 0


B.write_part = P.write_part = write_part

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
