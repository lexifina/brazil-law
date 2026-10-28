"""Reads the cache and writes scripts/brazil-law/corpus.d/50-codes.json: the Código Civil (Lei 10.406/2002) and the
LGPD (Lei 13.709/2018), in the corpus format of scripts/gitlaw_common/SCHEMA.md.

    python -X utf8 scripts/brazil-law/codes/parse_codes.py [--stats] [--check]

No network: every input is an Internet Archive raw capture of a www.planalto.gov.br page, pinned in
codes/sources_codes.json and fetched by codes/fetch_codes.py into ../.cache. The same cache gives the same bytes.

How each act's history is rebuilt
  Planalto's annotated page of a law (l10406.htm, l13709.htm) keeps every superseded wording in place, struck
  through, directly before the wording that replaced it, and ends each wording with the source's own note:
  "(Redação dada pela Lei nº 13.146, de 2015)", "(Incluído pela Medida Provisória nº 881, de 2019)",
  "(Revogado pela Lei nº 15.040, de 2024)", "(Renumerado do parágrafo único pela Lei nº 11.481, de 2007)".
  Text with no note is the act as enacted. Each paragraph (one <p>, one line of output) gets a life span:
    start = in-force day of the law in its "Redação dada / Incluído / Renumerado" note (else the act's own day);
    end   = for struck text, the in-force day of its "Revogado" note, else the start of the next wording of the
            same dispositivo (same label, later start) in the same article; a Medida Provisória's wording with no
            later wording ends when the MP was converted (the conversion law's day) or lapsed;
    a wording Planalto repeats after a lapsed or unconverted MP wording is the old wording restored: it starts
    again when the MP wording ended.
  The text of an article on day D is its paragraphs alive on D, in document order. Every change is credited to
  the law named in the note that started or ended the paragraph; anything else stays uncredited.
  The last version is checked against Planalto's consolidated page (l10406compilada.htm, L13709compilado.htm).
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import hashlib
import html as htmlmod
import json
import os
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
sys.path.insert(0, str(FOLDER))
import fetch  # noqa: E402  (the main Brazil fetcher: cache naming and Wayback URLs)

PL = "https://www.planalto.gov.br/ccivil_03/"
OUT = FOLDER / "corpus.d" / "50-codes.json"
RETRIEVED = "2026-10-28"

MONTHS = {"janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7,
          "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}

# ---------------------------------------------------------------------------------------------------------------
# cache access


def sources() -> dict[str, dict]:
    return {i["id"]: i for i in json.loads((HERE / "sources_codes.json").read_text(encoding="utf-8"))["fetch"]}


def raw(ident: str) -> tuple[bytes, str] | None:
    s = sources().get(ident)
    if not s or not s.get("ts"):
        return None
    u = fetch.wayback(s["url"], s["ts"])
    p = fetch.cached(u)
    if not p:
        return None
    return p.read_bytes(), u


def decode(b: bytes) -> str:
    m = re.search(rb'charset=["\']?([\w-]+)', b[:4000], re.I)
    enc = (m.group(1).decode() if m else "windows-1252").lower()
    if enc in ("iso-8859-1", "latin1", "latin-1"):
        enc = "windows-1252"
    try:
        return b.decode(enc)
    except (UnicodeDecodeError, LookupError):
        return b.decode("windows-1252", errors="replace")


# ---------------------------------------------------------------------------------------------------------------
# law references in notes

LAW_REF = re.compile(
    r"(Lei\s+Complementar|Lei|Medida\s+Provis[óo]ria|Decreto[-\s]?[Ll]ei)\s*(?:n\s*[º°o]?\s*\.?|n\.)?\s*"
    r"(\d{1,2}(?:\.\s?\d{3})+|\d+)(?:[-\s]*[A-Z](?![a-z]))?(?:\s*\.)?(?:\s*,)?(?:\s*de\s+(\d{1,2}º?\s*[./]\s*\d{1,2}\s*[./]\s*(\d{4})|"
    r"\d{1,2}º?\s+de\s+\w+\s+de\s+(\d{4})|(\d{4})))?", re.I)


def law_key(text: str, year_of: dict | None = None) -> str | None:
    """lei-14905-2024, lc-128-2008, mp-1085-2021, dl-4037-1942 for the first act named in text."""
    m = LAW_REF.search(text)
    if not m:
        return None
    kind = m.group(1).lower()
    pre = "lc" if "complementar" in kind else "mp" if kind.startswith("medida") else "dl" if kind.startswith("decreto") else "lei"
    n = int(re.sub(r"\D", "", m.group(2)))
    y = m.group(4) or m.group(5) or m.group(6)
    if not y and year_of:
        y = year_of.get(f"{pre}-{n}")
    if not y:
        return None
    k = f"{pre}-{n}-{y}"
    return LAW_ALIAS.get(k, (k,))[0]


# Notes whose printed number is wrong, corrected only where the note's own link names the right act: key -> (key, why).
LAW_ALIAS = {
    "lei-15452-2026": ("lei-15352-2026", "one LGPD note reads 'Lei nº 15.452, de 2026' but links to L15352.htm, the "
                                         "conversion of MP 1.317/2025 that the other notes in the same article cite"),
}


def law_label(key: str) -> str:
    pre, n, y = key.split("-")
    num = f"{int(n):,}".replace(",", ".")
    return {"lei": f"Lei nº {num}, de {y}", "lc": f"Lei Complementar nº {num}, de {y}",
            "mp": f"Medida Provisória nº {num}, de {y}", "dl": f"Decreto-Lei nº {num}, de {y}"}[pre]


# ---------------------------------------------------------------------------------------------------------------
# HTML -> blocks of (text, struck, link) segments (after scripts/brazil-law/parse.py)

BREAK = {"p", "br", "div", "tr", "td", "th", "table", "li", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "center",
         "blockquote", "ul", "ol", "dd", "dt"}
STRIKE = {"strike", "s", "del"}


class Blocks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[dict] = []
        self.cur: list[tuple[str, bool, bool]] = []
        self.strike = 0
        self.links: list[bool] = []
        self.skip = 0
        self.center = False
        self.spans: list[bool] = []

    def flush(self) -> None:
        if any(s.strip() for s, _, _ in self.cur):
            self.blocks.append({"segs": self.cur, "center": self.center})
        self.cur = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if tag in BREAK:
            self.flush()
            if tag == "p":
                st = (a.get("style") or "").replace(" ", "").lower()
                self.center = (a.get("align") or "").lower() == "center" or "text-align:center" in st
        if tag in STRIKE:
            self.strike += 1
        if tag in ("span", "font"):
            # Planalto also strikes text with CSS: <span style="text-decoration:line-through">
            lt = "line-through" in (a.get("style") or "").lower()
            self.spans.append(lt)
            self.strike += lt
        if tag == "a":
            self.links.append(bool(a.get("href")))

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
        if tag in BREAK:
            self.flush()
        if tag in STRIKE:
            self.strike = max(0, self.strike - 1)
        if tag in ("span", "font") and self.spans:
            self.strike = max(0, self.strike - self.spans.pop())
        if tag == "a" and self.links:
            self.links.pop()

    def handle_data(self, data):
        if not self.skip:
            self.cur.append((data, self.strike > 0, any(self.links)))


def blocks_of(html: str) -> list[dict]:
    html = re.sub(r"</p<a>", "</p>", html, flags=re.I)
    html = re.sub(r"\s*<sup>\s*(?:<[^>]+>\s*)*([oaº°ª])\s*(?:<[^>]+>\s*)*</sup>",
                  lambda m: "ª" if m.group(1) in "aª" else "º", html, flags=re.I)
    p = Blocks()
    p.feed(html)
    p.close()
    p.flush()
    return p.blocks


NOTE = re.compile(
    r"\(\s*(?:Reda[çc][ãa]o|Inclu[ií]d|Acrescentad|Acrescid|Revogad[oa]s?\s+(?:pel|por)|Renumerad|Vide|Vig[êe]ncia|"
    r"Produ[çc][ãa]o\s+de\s+efeito|Regulament|Declarad|Suspens|Execu[çc][ãa]o|Express[ãa]o|Promulga|Convers|Convertid|"
    r"Texto\s+compilado|Atualizad|Mensagem|Revoga[çc][ãa]o)[^()]*(?:\([^()]*\)[^()]*)*(?:\)|$)", re.I)
# a note Planalto left without parentheses at the end of a line: "...; Redação dada pela Medida Provisória nº 869, de 2018"
BARE_NOTE = re.compile(r"\s(?:Reda[çc][ãa]o\s+dada|Inclu[ií]d[oa]|Revogad[oa])\s+pel[oa]\s+(?:Lei|Medida|Decreto)[^()]*\)?\s*$", re.I)
LINKWORDS = re.compile(r"^\s*\(?\s*(?:Produ[çc][ãa]o\s+de\s+efeitos?|Vig[êe]ncia|Regulamento|Regulamenta[çc][ãa]o)"
                       r"\s*\)?\s*\.?\s*$", re.I)
LAPSED_WORDS = re.compile(r"\(?\s*Vig[êe]ncia\s+encerrada\s*\)?", re.I)
START_KIND = re.compile(r"Reda[çc][ãa]o\s+dada|Inclu[ií]d|Acrescentad|Acrescid|Renumerad", re.I)
END_KIND = re.compile(r"Revogad", re.I)
RENUM_FROM = re.compile(r"Renumerad[oa]\s+d[eo]s?\s+(par[áa]grafo\s+[úu]nico|inciso\s+[IVXLC]+|§\s*\d+\s*[º°o]?)", re.I)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = s.replace(" ", " ").replace("​", "").replace("­", "")
    s = s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    s = s.replace("–", "-").replace("—", "-")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"(\bArt\.|§)\s*(\d+(?:\.\d{3})*)\s*\.?\s*[o°º](?![a-zà-ú])", r"\1 \2º", s)
    s = re.sub(r"\bArt\.(?=\d)", "Art. ", s)
    s = re.sub(r"(\d) º", r"\1º", s)
    s = re.sub(r"\bn º", "nº", s)
    s = re.sub(r"(\d)º(?=[A-Za-zÀ-ú])", r"\1º ", s)
    s = re.sub(r"\s+([.,;:])", r"\1", s)
    s = re.sub(r"\(\s+", "(", s)
    s = re.sub(r"\s+\)", ")", s)
    return s.strip()


def analyse(block: dict) -> dict:
    """Split a block into text, struck state and notes."""
    chars: list[tuple[str, bool]] = []
    for text, struck, link in block["segs"]:
        if link and LINKWORDS.match(text):
            continue
        for ch in text:
            chars.append((ch, struck))
    full = "".join(c for c, _ in chars)
    notes = []
    keep = [True] * len(chars)
    lapsed = False
    for rx in (NOTE, LAPSED_WORDS):
        for m in rx.finditer(full):
            if not any(keep[m.start():m.end()]):
                continue
            if rx is LAPSED_WORDS:
                lapsed = True
            else:
                notes.append(norm(m.group(0)))
            for i in range(m.start(), m.end()):
                keep[i] = False
    rest = "".join(c if k else "\0" for (c, _), k in zip(chars, keep))
    m = BARE_NOTE.search(rest.replace("\0", " "))
    if m and "\0" not in rest[m.start():]:
        notes.append("(" + norm(m.group(0)) + ")")
        for i in range(m.start(), len(chars)):
            keep[i] = False
    text = "".join(c for (c, _), k in zip(chars, keep) if k)
    n_st = sum(1 for (c, s), k in zip(chars, keep) if k and s and not c.isspace())
    n_pl = sum(1 for (c, s), k in zip(chars, keep) if k and not s and not c.isspace())
    t = norm(text)
    t = re.sub(r"(?:\s*\(?\s*(?:Produ[çc][ãa]o de efeitos?|Vig[êe]ncia)\s*\)?\.?)+$", "", t).strip()
    state = "plain" if n_st == 0 else ("struck" if n_pl == 0 else "mixed")
    if state == "mixed":
        pl = norm("".join(c for (c, s), k in zip(chars, keep) if k and not s))
        if len(re.sub(r"[^\w]|\b(?:[IVXLC]+|[a-z]|\d+[º]?|Art|A)\b", "", pl)) == 0 and n_st > n_pl:
            state = "struck"
        elif lapsed or n_st > 4 * n_pl:
            state = "struck"
    if lapsed:
        notes.append("(Vigência encerrada)")
    plain_text = norm("".join(c for (c, s), k in zip(chars, keep) if k and not s)) if state == "mixed" else ""
    struck_text = norm("".join(c for (c, s), k in zip(chars, keep) if k and s)) if state == "mixed" else ""
    all_link = all(link or not text.strip() for text, _, link in block["segs"])
    return {"text": t, "state": state, "notes": notes, "center": block["center"], "lapsed": lapsed,
            "plain_text": plain_text, "struck_text": struck_text, "all_link": all_link}


ROMAN = r"[IVXLC]+"
SUFFIX = r"(?:-[A-Z]{1,2}(?![A-Za-zÀ-ú]))?"
LABEL = re.compile(
    r"^(?:(Art\.\s*\d+(?:\.\d+)?º?" + SUFFIX + r")|(§\s*\d+º?" + SUFFIX + r")|(Par[áa]grafo\s+[úu]nico)|"
    r"(" + ROMAN + SUFFIX + r")\s*[-–]+\s*|(?P<bare>" + ROMAN + r")(?P<bs>-?[A-Z])?\s+(?=[a-zà-ú])|([a-z]" + SUFFIX + r")\)|(\d+)\)\s)")


def label_of(text: str) -> str:
    m = LABEL.match(text)
    if not m:
        return ""
    if m.group("bare"):
        bs = (m.group("bs") or "").lstrip("-")
        return m.group("bare") + ("-" + bs if bs else "") + " -"
    g = next(x for x in m.groups() if x)
    g = re.sub(r"\s+", "", g).replace("Parágrafoúnico", "Parágrafo único").replace("Paragrafoúnico", "Parágrafo único")
    if m.group(4):
        g += " -"
    elif m.group(7) or m.group(8):
        g += ")"
    return g.replace("Art.", "Art. ").replace("§", "§ ")


def renum_label(note: str) -> str | None:
    m = RENUM_FROM.search(note)
    if not m:
        return None
    s = m.group(1)
    if re.match(r"par", s, re.I):
        return "Parágrafo único"
    if s.lower().startswith("inciso"):
        return s.split()[1] + " -"
    return "§ " + re.sub(r"\D", "", s) + "º"


def level(label: str) -> int:
    if label.startswith("Art."):
        return 0
    if label.startswith("§") or label.startswith("Parágrafo"):
        return 1
    if label.endswith(" -"):
        return 2
    if re.match(r"^[a-z]", label):
        return 3
    if re.match(r"^\d", label):
        return 4
    return 5


HEADING = re.compile(r"^(?:P\s?A\s?R\s?T\s?E|LIVRO|T[ÍI]TULO|CAP[ÍI]TULO|Se[çc][ãa]o|SE[ÇC][ÃA]O|Subse[çc][ãa]o|SUBSE[ÇC][ÃA]O)\b")
NAV = re.compile(r"^(?:Texto compilado|Mensagem de veto|Vig[êe]ncia|[ÍI]NDICE|Vide\b|Regulamento|Convers[ãa]o d|"
                 r"Convertid|Produ[çc][ãa]o de efeito|Lei de Introdu[çc][ãa]o)", re.I)

# ---------------------------------------------------------------------------------------------------------------
# dates


def dmy(s: str) -> str:
    d, m, y = (int(x) for x in re.findall(r"\d+", s)[:3])
    return f"{y:04d}-{m:02d}-{d:02d}"


def plus_days(d: str, n: int) -> str:
    return (dt.date.fromisoformat(d) + dt.timedelta(days=n)).isoformat()


def plus_months(d: str, n: int) -> str:
    x = dt.date.fromisoformat(d)
    y, m = divmod(x.month - 1 + n, 12)
    y, m = x.year + y, m + 1
    return dt.date(y, m, min(x.day, calendar.monthrange(y, m)[1])).isoformat()


NUMWORDS = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "seis": 6, "doze": 12, "dezoito": 18,
            "trinta": 30, "quarenta e cinco": 45, "sessenta": 60, "noventa": 90, "cento e vinte": 120,
            "cento e oitenta": 180, "trezentos e sessenta e cinco": 365, "vinte e quatro": 24}

# ---------------------------------------------------------------------------------------------------------------
# the laws the notes cite: their pages give enactment, publication, vigência, and an MP's fate


def page_info(key: str) -> dict:
    """Enacted and published dates, ementa, the vigência clause and (MPs) the conversion law or lapse."""
    r = raw("law:" + key)
    if not r:
        return {}
    b, u = r
    t = decode(b)
    head = norm(htmlmod.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", t))))
    body = re.sub(r"(?is)<script.*?</script>|<style.*?</style>|<strike>.*?</strike>", " ", t)
    x = norm(htmlmod.unescape(re.sub(r"<[^>]+>", " ", body)))
    info: dict = {"source_url": u, "sha256": hashlib.sha256(b).hexdigest()}
    m = re.search(r"(?:LEI|MEDIDA PROVIS[ÓO]RIA|DECRETO-LEI)[^,]{0,40}?N[º°O]?\s*\.?\s*[\d.]+\s*,?\s*DE\s+(\d{1,2})º?\s+DE\s+(\w+)\s+DE\s+(\d{4})",
                  head, re.I)
    if m and m.group(2).lower() in MONTHS:
        info["enacted"] = f"{int(m.group(3)):04d}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    pub = re.search(r"publicad[oa]\s+n[oa]\s+D\.?\s*O\.?\s*U\.?\s*(?:de\s*)?(\d{1,2})\s*º?\s*\.\s*(\d{1,2})\s*\.\s*(\d{4})", head, re.I)
    if pub:
        info["published"] = f"{int(pub.group(3)):04d}-{int(pub.group(2)):02d}-{int(pub.group(1)):02d}"
    if m:
        after = head[m.end():m.end() + 1500]
        after = re.sub(r"^(?:\s*(?:Mensagem de veto|Texto compilado|Vig[êe]ncia(?: encerrada)?|Convers[ãa]o da Medida Provis[óo]ria\s+n[º°]?\s*[\d.]+(?:,\s*de\s+\d{4})?|"
                       r"Convertida na Lei\s+n[º°]?\s*[\d.]+(?:,\s*de\s+\d{4})?|Regulamento|Produ[çc][ãa]o de efeitos?|Vide [^.]*?\d{4}\)?|"
                       r"\(Vide [^)]*\)|Exposi[çc][ãa]o de motivos|Promulga[çc][ãa]o (?:partes )?vetadas?|Rejeitada|Ato declarat[óo]rio[^.]*?\d{4}|"
                       r"Revogad[ao][^.]*?\d{4}|\.|Prorrogada[^.]*?\d{4}))+", "", after, flags=re.I)
        em = re.match(r"(.*?\.)\s*(?:O\s+PRESIDENTE|O\s+VICE|A\s+PRESIDENTA|O\s+CONGRESSO|Fa[çc]o saber)", after, re.S)
        info["title"] = em.group(1).strip() if em else ""
    conv = re.search(r"Convertid[ao]\s+n[ao]\s+Lei\s+n[º°]?\s*([\d.]+)\s*,?\s*de\s+(?:\d{1,2}[./]\d{1,2}[./])?(\d{4})", head, re.I)
    if conv:
        info["converted"] = f"lei-{int(conv.group(1).replace('.', ''))}-{conv.group(2)}"
    if re.search(r"Vig[êe]ncia\s+encerrada", head[:3000], re.I):
        info["lapsed"] = True
    if re.search(r"\bRejeitada\b", head[:3000], re.I):
        info["rejected"] = True
    cl = [mm.start() for mm in re.finditer(r"(?:Est[ae]\s+(?:Lei|Medida\s+Provis[óo]ria|C[óo]digo)(?:\s+Complementar)?|"
                                            r"A\s+presente\s+Lei)\s+entra(?:r[áa])?\s+em\s+vigor", x, re.I)]
    if cl:
        tail = x[cl[-1]:]
        end = re.search(r"\.\s+(?:Art\. \d|Bras[íi]lia|Este texto)", tail)
        info["clause"] = tail[:end.start() + 1] if end else tail[:600]
    else:
        info["clause"] = ""
    return info


# Hand-checked in-force days where a law's own clause is staged or not machine-readable: key -> (date, reason).
VIGENCIA_FIXED: dict[str, tuple[str, str]] = {
    "lei-12873-2013": ("2013-10-25", "art. 72, III: 'na data de sua publicação quanto aos demais dispositivos' (published "
                                     "25.10.2013); the change to the Código Civil (art. 1.439) is not among the provisions "
                                     "items I and II defer"),
    "lei-13874-2019": ("2019-09-20", "art. 20, II: 'na data de sua publicação, para os demais artigos' (published 20.9.2019; "
                                     "item I was vetoed)"),
    "lei-14382-2022": ("2022-06-28", "art. 21, II: 'na data de sua publicação, quanto aos demais dispositivos' (published "
                                     "28.6.2022); item I defers only the change to Lei 6.015 art. 130"),
    "mp-1085-2021": ("2021-12-28", "its clause II: 'na data de sua publicação, quanto aos demais dispositivos' (published "
                                   "28.12.2021); item I defers only the change to Lei 6.015 art. 130"),
    "lei-14690-2023": ("2024-03-31", "its clause I: 'após decorridos 180 (cento e oitenta) dias de sua publicação oficial, "
                                     "quanto ao art. 30 desta Lei' - art. 30 is the change to the Código Civil (published "
                                     "3.10.2023 + 180 days)"),
    "lei-14711-2023": ("2023-10-31", "its clause II: 'na data de sua publicação, quanto aos demais dispositivos' (published "
                                     "31.10.2023; item I was vetoed)"),
}
# Provisions whose in-force day differs from the rest of their law: (law, act, unit) -> (date, reason).
VIGENCIA_PROVISION: dict[tuple[str, str, str], tuple[str, str]] = {}
# The day a lapsed Medida Provisória stopped having effect, from the Ato Declaratório of the President of Congress
# (CF art. 62 §§ 3, 4, 7 and 11): key -> (date, reason). Filled in after reading each MP page.
# Vetoed parts later promulgated after Congress overrode the veto (CF art. 66 §§ 5 and 7): law -> (day, reason).
VETO_PROMULGATION = {
    "lei-13853-2019": ("2019-12-20", "the parts of Lei 13.853/2019 vetoed on 8.7.2019 were promulgated after Congress "
                                     "overrode the veto (DOU 20.12.2019, printed on the Lei 13.853 page)"),
}
MP_LAPSE: dict[str, tuple[str, str]] = {
    "mp-700-2015": ("2016-05-18", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 23, de 2016 (DOU "
                                  "19.5.2016): 'teve seu prazo de vigência encerrado no dia 17 de maio'; the replaced "
                                  "wording is back from 18.5.2016"),
    "mp-958-2020": ("2020-08-25", "Congresso Nacional, MPV 958/2020: 'Término do prazo de vigência, em 24 de agosto de 2020' "
                                  "(DCN 27.8.2020; Ato Declaratório nº 153, de 2020); the revoked article is back from "
                                  "25.8.2020"),
}


def vigencia_of(key: str, info: dict) -> tuple[str | None, str]:
    """In-force day of a law's text changes, and a one-line reason."""
    if key in VIGENCIA_FIXED:
        return VIGENCIA_FIXED[key]
    pub = info.get("published") or info.get("enacted")
    cl = info.get("clause", "")
    if not pub:
        return None, "no publication date found"
    if not cl:
        if key.startswith("mp-"):
            return pub, f"published {pub}; a Medida Provisória has force of law from publication (CF art. 62)"
        return plus_days(pub, 45), f"no vigência clause: LINDB art. 1, published {pub} + 45 days"
    if re.search(r"entra(?:r[áa])?\s+em\s+vigor\s+na\s+data\s+d[ae]\s+sua\s+publica", cl, re.I):
        return pub, f"own clause 'entra em vigor na data de sua publicação' (published {pub})"
    m = re.search(r"entra(?:r[áa])?\s+em\s+vigor\s+(?:ap[óo]s\s+decorrid[oa]s?\s+|ap[óo]s\s+)?(\d+)\s*\(([^)]+)\)\s*(dias|meses|m[êe]s|anos?)\s+"
                  r"(?:ap[óo]s\s+|de\s+|da\s+|contados\s+da\s+|a\s+partir\s+da\s+)?(?:a\s+)?(?:data\s+de\s+|data\s+da\s+)?(?:sua|da\s+sua)\s+publica",
                  cl, re.I)
    if m:
        n, unit = int(m.group(1)), m.group(3).lower()
        if unit == "dias":
            return plus_days(pub, n), f"own clause: {n} days after publication ({pub}; LC 95/1998 art. 8 § 1)"
        months = n * 12 if unit.startswith("ano") else n
        return (plus_days(plus_months(pub, months), 1),
                f"own clause: {n} {unit} after publication ({pub}); the period ends on the same calendar day and the "
                f"law is in force the day after (LC 95/1998 art. 8 § 1, as the STJ applied it to the CPC, in force 18.3.2016)")
    return None, f"unhandled clause: {cl[:300]}"


# ---------------------------------------------------------------------------------------------------------------
# an act's paragraphs


def paragraphs(html: str, digits: int) -> tuple[list[dict], list[str]]:
    """Paragraphs of a law in document order, with unit keys and labels, from its title to the signature."""
    bl = [analyse(b) for b in blocks_of(html)]
    out: list[dict] = []
    zone = None
    unit = None
    notes_only: list[dict] = []
    for b in bl:
        t = b["text"]
        if zone is None:
            if re.match(r"^LEI\s+N", t):
                zone = "pre"
            continue
        if zone == "end":
            break
        if t.startswith("Brasília,") or t.startswith("Este texto não substitui"):
            zone = "end"
            continue
        if not t:
            if b["notes"] and out:
                # a note in a block of its own belongs to the line(s) before it
                if out[-1]["heading"]:
                    out[-1].setdefault("notes_after", []).extend(b["notes"])
                else:
                    attach_notes(out, b["notes"])
            continue
        if zone == "pre" and (b["all_link"] or NAV.match(t)):
            continue
        lab = label_of(t)
        heading = (not lab and (b["center"] or bool(HEADING.match(t)))) or (b["center"] and not lab.startswith("Art."))
        if zone == "pre" and (lab.startswith("Art.") or heading):
            zone = "body"
        if zone == "pre":
            out.append({**b, "unit": "preambulo", "label": "", "heading": False})
            continue
        if heading:
            out.append({**b, "unit": "titulos", "label": t if HEADING.match(t) else "", "heading": True})
            continue
        if lab.startswith("Art."):
            unit = unit_key(lab, digits)
        if unit is None:
            unit = "preambulo"
        out.append({**b, "unit": unit, "label": lab, "heading": False})
    heading_groups(out)
    for i, p in enumerate(out):
        p["i"] = i
    return out, notes_only


def heading_groups(out: list[dict]) -> None:
    """Planalto keeps each wording of a block of headings in place, one block after the other ("CAPÍTULO IX / DA
    AUTORIDADE ...", then "CAPÍTULO IX / DA AGÊNCIA ..."), with the note standing alone somewhere in the block. A run
    of heading lines is split into wordings wherever its first line repeats; every line of a wording gets the
    wording's notes and an internal slot label (run, position) so the wordings replace each other line by line. In
    the last wording only as many lines as the wording before it had are the replacement; the lines after it are
    headings of their own. A run with one wording gives a standing note to the lines just before it, and its struck
    lines share their notes."""
    i, run = 0, 0
    while i < len(out):
        if not out[i]["heading"]:
            i += 1
            continue
        j = i
        while j < len(out) and out[j]["heading"]:
            j += 1
        lines = out[i:j]
        run += 1
        first = lines[0]["text"]
        starts = [k for k, p in enumerate(lines) if p["text"] == first]
        if len(starts) > 1 and HEADING.match(first):
            groups = [lines[a:b] for a, b in zip(starts, starts[1:] + [len(lines)])]
            for g, grp in enumerate(groups):
                notes = [n for p in grp for n in p.get("notes_after", [])]
                n_repl = len(grp) if g < len(groups) - 1 else len(groups[g - 1])
                for pos, p in enumerate(grp):
                    p["label"] = f"h{run}-{pos}"
                    if pos < n_repl:
                        p["notes"] = p["notes"] + [n for n in notes if n not in p["notes"]]
        else:
            for k, p in enumerate(lines):
                p["label"] = f"h{run}-{k}"
                if p.get("notes_after"):
                    attach_notes(out[:i + k + 1], p["notes_after"])
            struck = [p for p in lines if p["state"] != "plain"]
            shared = [n for p in struck for n in p["notes"]]
            for p in struck:
                p["notes"] = p["notes"] + [n for n in shared if n not in p["notes"]]
        i = j


def attach_notes(out: list[dict], notes: list[str]) -> None:
    """Notes in a block of their own: give them to the lines just before, back to the last line that has notes, a
    change between struck and unstruck, or a repeated line."""
    last = out[-1]
    seen = set()
    for p in reversed(out):
        if p["notes"] or p["state"] != last["state"] or p["text"] in seen or p["heading"] != last["heading"]:
            break
        seen.add(p["text"])
        p["notes"] = p["notes"] + notes
        if not p["heading"]:
            break


def unit_key(label: str, digits: int) -> str:
    m = re.match(r"Art\. (\d+(?:\.\d+)?)º?(?:-([A-Z]{1,2}))?", label)
    n = int(m.group(1).replace(".", ""))
    return f"art-{n:0{digits}d}" + (f"-{m.group(2).lower()}" if m.group(2) else "")


# ---------------------------------------------------------------------------------------------------------------
# life spans


class Ctx:
    def __init__(self, act_day: str, eff: dict, mp: dict, lapse_key: dict, act: str):
        self.act_day, self.eff, self.mp, self.lapse_key, self.act = act_day, eff, mp, lapse_key, act


def lifespans(paras: list[dict], cx: Ctx) -> list[str]:
    problems = []
    for p in paras:
        starts, ends = [], []
        p["renum_from"] = None
        for n in p["notes"]:
            if re.match(r"\(\s*(?:Vide|Vig[êe]ncia|Produ|Regulament|Declarad|Suspens|Execu|Express|Promulga|Convers|Convertid|Mensagem|Texto)", n, re.I):
                continue
            law = law_key(n, cx.mp.get("_years"))
            if not law:
                if START_KIND.search(n) or END_KIND.search(n):
                    problems.append(f"note names no law: {n!r}")
                continue
            d = VIGENCIA_PROVISION.get((law, cx.act, p["unit"]), (None,))[0] or cx.eff.get(law)
            if not d:
                problems.append(f"no in-force day for {law} (note {n!r})")
                continue
            if START_KIND.search(n):
                starts.append((d, law))
                if re.search(r"Renumerad", n, re.I):
                    p["renum_from"] = (renum_label(n), d, law)
            elif END_KIND.search(n):
                ends.append((d, law))
        p["start"], p["start_law"] = max(starts) if starts else (cx.act_day, None)
        p["end"], p["end_law"], p["end_how"] = None, None, None
        p["gaps"] = []
        # a revocation by an MP that lapsed is only a gap; one by an MP that was converted stands
        real_ends = []
        for d, law in ends:
            fate = cx.mp.get(law)
            if fate and fate.get("lapsed_on"):
                p["gaps"].append((d, fate["lapsed_on"], law, cx.lapse_key[law]))
            else:
                real_ends.append((d, law))
        if real_ends and (p["state"] != "plain" or p["text"] == ""):
            p["end"], p["end_law"] = min(real_ends)
            p["end_how"] = "note"
        elif p["state"] == "plain" and real_ends and not starts:
            # an unstruck "(Revogado)" placeholder: it starts when the repeal took effect
            p["start"], p["start_law"] = max(real_ends)
        # wording made by an MP that lapsed ends when the MP lapsed
        fate = cx.mp.get(p["start_law"]) if p["start_law"] else None
        if fate and fate.get("lapsed_on") and p["state"] != "plain":
            lap = (fate["lapsed_on"], cx.lapse_key[p["start_law"]])
            if not p["end"] or lap < (p["end"], p["end_law"]):
                p["end"], p["end_law"], p["end_how"] = lap[0], lap[1], "lapse"
        # a vetoed item ("(VETADO)") replaced when Congress overrode the veto and the parts were promulgated
        if p["state"] != "plain" and not p["end"] and any(re.search(r"Promulga[çc][ãa]o\s+(?:das\s+)?partes\s+vetadas", n, re.I) for n in p["notes"]):
            hit = VETO_PROMULGATION.get(p["start_law"] or "")
            if hit:
                p["end"], p["end_law"], p["end_how"] = hit[0], p["start_law"], "promulgation"
    # struck wordings: the next wording of the same dispositivo ends them
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end"]:
            continue
        succ = successor(paras, i)
        if succ is not None:
            q = paras[succ]
            p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "successor"
            continue
        fate = cx.mp.get(p["start_law"]) if p["start_law"] else None
        if fate and fate.get("converted_on"):
            p["end"], p["end_law"], p["end_how"] = fate["converted_on"], fate["converted"], "conversion"
    # restored wordings: a wording repeated after a later one starts again when that one ended
    for i, q in enumerate(paras):
        r = predecessor(paras, i)
        if r is None:
            continue
        pr = paras[r]
        if q["text"] == pr["text"] and pr["gaps"] and not pr["end"] and q["start"] <= pr["start"]:
            # the same wording struck twice: once by a lapsed MP's revocation (a gap), then by a lasting revocation
            pr["end"], pr["end_law"], pr["end_how"] = q["end"], q["end_law"], "repeat"
            q["skip"] = True
            continue
        if q["start"] < pr["start"] or (q["start"] == pr["start"] and q["start_law"] == pr["start_law"] and pr["state"] != "plain"
                                         and pr.get("end")):
            if pr["end"]:
                q["start"], q["start_law"], q["restored"] = pr["end"], pr["end_law"], True
            else:
                problems.append(f"restored wording after an open one: {q['unit']} [{q['label']}] {q['text'][:80]!r}")
    # second pass for struck text whose successor was a restoration
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end"]:
            continue
        succ = successor(paras, i)
        if succ is not None:
            q = paras[succ]
            p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "successor"
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end"] or p["gaps"]:
            continue
        lv = level(p["label"])
        if p["heading"]:
            # a struck heading line falls with the struck heading lines around it
            for q in list(paras[i + 1:i + 6]) + list(reversed(paras[max(0, i - 5):i])):
                if q["heading"] and q["state"] != "plain" and q["end"] and q["start"] == p["start"]:
                    p["end"], p["end_law"], p["end_how"] = q["end"], q["end_law"], "group"
                    break
        else:
            for q in reversed(paras[:i]):
                if q["unit"] != p["unit"]:
                    break
                if level(q["label"]) < lv and not q["heading"]:
                    if q["state"] != "plain" and q["end"] and q["end"] > p["start"]:
                        p["end"], p["end_law"], p["end_how"] = q["end"], q["end_law"], "parent"
                    break
        if not p["end"]:
            problems.append(f"no end for struck {p['unit']} [{p['label']}] {p['text'][:90]!r} notes={p['notes']}")
    for p in paras:
        if p["end"] and p["end"] < p["start"]:
            problems.append(f"ends before it starts: {p['unit']} [{p['label']}] {p['start']}..{p['end']} {p['text'][:70]!r} {p['notes']}")
    return problems


def same_slot(p: dict, q: dict) -> bool:
    if p["heading"] or q["heading"]:
        return p["heading"] and q["heading"] and bool(p["label"]) and p["label"] == q["label"]
    return (q["label"] == p["label"] or (q["renum_from"] and q["renum_from"][0] == p["label"])
            or (p["label"] == "Parágrafo único" and q["label"] == "§ 1º"))


def successor(paras: list[dict], i: int) -> int | None:
    p = paras[i]
    lv = level(p["label"])
    for j in range(i + 1, len(paras)):
        q = paras[j]
        if p["heading"]:
            if not q["heading"]:
                return None
            if q["start"] > p["start"] and same_slot(p, q):
                return j
            continue
        if q["unit"] != p["unit"] or q["heading"]:
            return None
        if level(q["label"]) < min(lv, 2) or (lv < 5 and level(q["label"]) < lv):
            return None
        if same_slot(p, q) and q["start"] > p["start"]:
            return j
    return None


def predecessor(paras: list[dict], i: int) -> int | None:
    """The nearest earlier wording of the same dispositivo, among its siblings."""
    q = paras[i]
    if q["heading"] or not q["label"]:
        if q["heading"] and q["label"]:
            for j in range(i - 1, max(-1, i - 40), -1):
                r = paras[j]
                if not r["heading"]:
                    return None
                if r["label"] == q["label"]:
                    return j
        return None
    lv = level(q["label"])
    for j in range(i - 1, -1, -1):
        r = paras[j]
        if r["unit"] != q["unit"] or r["heading"]:
            return None
        if level(r["label"]) < lv:
            return None
        if level(r["label"]) == lv and r["label"] == q["label"]:
            return j
    return None


def alive(p: dict, day: str) -> bool:
    if p.get("skip"):
        return False
    if p["start"] > day or (p["end"] is not None and day >= p["end"]):
        return False
    return not any(a <= day < b for a, b, _, _ in p["gaps"])


def events(p: dict) -> list[tuple[str, str | None]]:
    ev = [(p["start"], p["start_law"])]
    if p["end"]:
        ev.append((p["end"], p["end_law"]))
    for a, b, la, lb in p["gaps"]:
        ev += [(a, la), (b, lb)]
    return ev


# ---------------------------------------------------------------------------------------------------------------
# building an act


def build_act(paras: list[dict], act_day: str, gate: dict[str, str], gate_law: dict[str, str], unit_label) -> list[dict]:
    """Versions: one per day on which any unit's text changes."""
    units = []
    for p in paras:
        if p["unit"] not in units:
            units.append(p["unit"])
    by_unit: dict[str, list[dict]] = {u: [p for p in paras if p["unit"] == u] for u in units}
    days = {act_day} | set(gate.values())
    for p in paras:
        for d, _ in events(p):
            if d >= act_day:
                days.add(d)
    versions = []
    prev: dict[str, str] = {}
    for day in sorted(days):
        cur: dict[str, str] = {}
        for u in units:
            if gate.get(u, act_day) > day:
                continue
            lines = [p["text"] for p in by_unit[u] if alive(p, day)]
            if lines:
                cur[u] = "".join(l + "\n" for l in lines)
        if versions and cur == prev:
            continue
        credits: dict[str, list[str]] = {}
        if versions:
            for u in sorted(set(cur) | set(prev)):
                if cur.get(u) == prev.get(u):
                    continue
                ls = set()
                for p in by_unit[u]:
                    for d, law in events(p):
                        if d == day and law:
                            ls.add(law)
                if gate.get(u) == day and u not in prev:
                    ls.add(gate_law[u])
                if ls:
                    credits[u] = sorted(ls)
        versions.append({"from": day, "units": {u: {"label": unit_label(u, by_unit[u]), "kind": unit_kind(u), "text": t}
                                                for u, t in cur.items()}, "credits": credits})
        prev = cur
    return versions


def unit_kind(u: str) -> str:
    return "art" if u.startswith("art-") else "heading" if u == "titulos" else "preamble"


def unit_label(u: str, ps: list[dict]) -> str:
    if u == "titulos":
        return "Títulos, capítulos e seções"
    if u == "preambulo":
        return "Preâmbulo"
    for p in ps:
        if p["label"].startswith("Art."):
            return p["label"].rstrip(".")
    return u


# ---------------------------------------------------------------------------------------------------------------
# check against Planalto's consolidated page


BARE_LABEL = re.compile(r"^(?:Arts?\. [\d.]+º?(?:-[A-Z]{1,2})?\.?(?: a [\d.]+º?(?:-[A-Z]{1,2})?\.?)?|§ \d+º?(?:-[A-Z])?\.?|Parágrafo único\.?|[IVXLC]+(?:-[A-Z])? -|[a-z]\))$")


def consolidated(ident: str, digits: int) -> dict[str, str]:
    b, _ = raw(ident)
    paras, _ = paragraphs(decode(b), digits)
    out: dict[str, list[str]] = {}
    for p in paras:
        # the consolidated page keeps a revoked dispositivo as its bare label ("Art. 757.", "III -"): not text
        t = p["text"] if p["state"] == "plain" else p["plain_text"] if p["state"] == "mixed" else ""
        if t and not BARE_LABEL.match(t):
            out.setdefault(p["unit"], []).append(t)
    return {u: "".join(l + "\n" for l in ls) for u, ls in out.items()}


def compare(last: dict[str, str], ref: dict[str, str]) -> list[str]:
    diffs = []
    for u in sorted(set(last) | set(ref)):
        a, b = last.get(u), ref.get(u)
        if a == b:
            continue
        if a is None or b is None:
            diffs.append(f"{u}: only in {'consolidated' if a is None else 'replay'}")
            continue
        al, bl = a.splitlines(), b.splitlines()
        import difflib
        out = []
        sm = difflib.SequenceMatcher(None, bl, al, autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            if tag == "replace" and i2 - i1 == j2 - j1:
                for x, y in zip(bl[i1:i2], al[j1:j2]):
                    cs = difflib.SequenceMatcher(None, x, y, autojunk=False)
                    for t, a1, a2, b1, b2 in cs.get_opcodes():
                        if t != "equal":
                            out.append(f"Planalto consolidated {x[max(0, a1 - 25):a2 + 10]!r} / replay {y[max(0, b1 - 25):b2 + 10]!r}")
                continue
            for x in bl[i1:i2]:
                out.append(f"only in consolidated: {x[:120]!r}")
            for y in al[j1:j2]:
                out.append(f"only in replay: {y[:120]!r}")
        diffs.append(f"{u}: " + " | ".join(out[:6]))
    return diffs


# ---------------------------------------------------------------------------------------------------------------
# the two acts

ACTS = [
    {"slug": "codigo-civil", "short": "CC", "page": "cc-original", "consolidated": "cc", "law": "lei-10406-2002",
     "title": "Código Civil (Lei nº 10.406, de 10 de janeiro de 2002)", "digits": 4,
     "url": PL + "leis/2002/l10406compilada.htm"},
    {"slug": "lgpd", "short": "LGPD", "page": "lgpd", "consolidated": "lgpd-compilado", "law": "lei-13709-2018",
     "title": "Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709, de 14 de agosto de 2018)", "digits": 3,
     "url": PL + "_ato2015-2018/2018/lei/L13709compilado.htm"},
]

# The day each act came into force (its own vigência clause).
ACT_DAY = {
    "lei-10406-2002": ("2003-01-11", "Lei 10.406/2002 art. 2.044: 'Este Código entrará em vigor 1 (um) ano após a sua "
                                     "publicação' (published 11.1.2002): in force 11.1.2003"),
    "lei-13709-2018": ("2018-08-15", "Lei 13.709/2018 was published 15.8.2018; only its vigência clause (art. 65) is "
                                     "taken as in force from publication, every other article by art. 65 as amended "
                                     "(see the per-article days)"),
}

# LGPD art. 65 (as amended by MP 869/2018, Lei 13.853/2019 and Lei 14.010/2020): the day each article came into force.
LGPD_EARLY = ["art-055-a", "art-055-b", "art-055-c", "art-055-d", "art-055-e", "art-055-f", "art-055-g", "art-055-h",
              "art-055-i", "art-055-j", "art-055-k", "art-055-l", "art-058-a", "art-058-b"]
LGPD_SANCTIONS = ["art-052", "art-053", "art-054"]
LGPD_GATES = {
    "early": ("2018-12-28", "mp-869-2018", "art. 65, I (MP 869/2018, then Lei 13.853/2019): in force 28.12.2018 for arts. "
              "55-A to 55-L, 58-A and 58-B (55-L only from its inclusion by Lei 13.853/2019)"),
    "sanctions": ("2021-08-01", "lei-14010-2020", "art. 65, I-A (Lei 14.010/2020): in force 1.8.2021 for arts. 52, 53 and 54"),
    "rest": ("2020-09-18", "lei-13709-2018", "art. 65, II: 24 months after publication (Lei 13.853/2019), postponed to "
             "3.5.2021 by MP 959/2020 art. 4, which Congress left out when converting it (Lei 14.058/2020, published "
             "18.9.2020): every other article came into force on 18.9.2020"),
}


def lgpd_gates(units: list[str]) -> tuple[dict[str, str], dict[str, str]]:
    gate, law = {}, {}
    for u in units:
        if u in ("art-065", "preambulo"):
            continue
        g = "early" if u in LGPD_EARLY else "sanctions" if u in LGPD_SANCTIONS else "rest"
        gate[u], law[u] = LGPD_GATES[g][0], LGPD_GATES[g][1]
    return gate, law


def note_laws(paras: list[dict]) -> set[str]:
    out = set()
    for p in paras:
        for n in p["notes"]:
            if START_KIND.search(n) or END_KIND.search(n):
                k = law_key(n)
                if k:
                    out.add(k)
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--dry", action="store_true", help="do not write corpus.d/50-codes.json")
    a = ap.parse_args(argv)
    problems: list[str] = []
    decisions: list[str] = []

    # paragraphs of each act
    parsed = {}
    for act in ACTS:
        b, src = raw(act["page"])
        paras, _ = paragraphs(decode(b), act["digits"])
        parsed[act["slug"]] = (paras, src, hashlib.sha256(b).hexdigest())

    # every law a start/end note names, and the conversion laws of the MPs among them
    keys = set()
    for paras, _, _ in parsed.values():
        keys |= note_laws(paras)
    years = {k.rsplit("-", 1)[0]: k.rsplit("-", 1)[1] for k in keys}
    infos = {k: page_info(k) for k in sorted(keys)}
    for k in sorted(keys):
        if k.startswith("mp-") and infos[k].get("converted"):
            c = infos[k]["converted"]
            if c not in infos:
                infos[c] = page_info(c)
    eff: dict[str, str] = {}
    vig_notes = []
    lindb = []
    for k, info in sorted(infos.items()):
        if not info:
            problems.append(f"law {k}: page not cached")
            continue
        d, why = vigencia_of(k, info)
        if not d:
            problems.append(f"law {k}: {why}")
            continue
        eff[k] = d
        if "LINDB" in why:
            lindb.append(f"{law_label(k)} ({info.get('published')} -> {d})")
        elif k in VIGENCIA_FIXED or "after publication" in why:
            vig_notes.append(f"{law_label(k)}: in force {d}, {why}.")
    for k, (d, why) in ACT_DAY.items():
        eff[k] = d
    effects = []
    for k, info in sorted(infos.items()):
        cl = (info or {}).get("clause", "")
        if re.search(r"produz\w*\s+efeitos", cl, re.I) and k in eff:
            effects.append(f"{law_label(k)} (in force {eff[k]}): \"{cl[:260]}{'…' if len(cl) > 260 else ''}\"")
    if effects:
        decisions.append("Some laws are in force on one day but defer the effects of some provisions ('produzirá "
                         "efeitos'); their versions are dated by the in-force day (the day the wording became the "
                         "law's text), as for the Constitution. Their clauses: " + " | ".join(effects))
    for k, (k2, why) in LAW_ALIAS.items():
        decisions.append(f"Note corrected: {why}; credited to {law_label(k2)}.")
    # Medidas Provisórias: converted (the conversion law's day ends the MP wording) or lapsed
    mp: dict = {"_years": years}
    lapse_key: dict[str, str] = {}
    for k, info in sorted(infos.items()):
        if not k.startswith("mp-") or not info:
            continue
        fate = {}
        if info.get("converted") and info["converted"] in eff:
            fate = {"converted": info["converted"], "converted_on": eff[info["converted"]]}
        elif k in MP_LAPSE:
            fate = {"lapsed_on": MP_LAPSE[k][0]}
            lapse_key[k] = k + "-fim"
        else:
            problems.append(f"{k}: neither converted nor a known lapse ({ {x: info.get(x) for x in ('converted', 'lapsed', 'rejected')} })")
        mp[k] = fate

    # laws
    laws: dict[str, dict] = {}

    def add_law(k: str, **over) -> None:
        info = infos.get(k) or {}
        laws[k] = {"label": law_label(k), "title": info.get("title") or "", "kind": "law",
                   "enacted": info.get("enacted"), "published": info.get("published"),
                   "url": (sources().get("law:" + k) or {}).get("url"), "temporary_until": None, "restores": None,
                   "note": None, **over}

    for k in sorted(eff):
        if k in ACT_DAY:
            continue
        add_law(k)
        if k in lapse_key:
            laws[k]["temporary_until"] = MP_LAPSE[k][0]
    for k, lk in sorted(lapse_key.items()):
        d, why = MP_LAPSE[k]
        laws[lk] = {"label": f"{law_label(k)}: vigência encerrada", "title": f"{law_label(k)} lost effect without "
                    f"conversion into law", "kind": "law", "enacted": d, "published": d, "url": laws[k]["url"],
                    "temporary_until": None, "restores": k,
                    "note": f"{law_label(k)} lost effect on {d} without being converted into law ({why}); the wording "
                            f"it had replaced is in force again."}
    laws["lei-10406-2002"] = {"label": "Lei nº 10.406, de 2002", "title": "Institui o Código Civil.", "kind": "law",
                              "enacted": "2002-01-10", "published": "2002-01-11", "url": PL + "leis/2002/l10406.htm",
                              "temporary_until": None, "restores": None, "note": None}
    laws["lei-13709-2018"] = {"label": "Lei nº 13.709, de 2018", "title": "Lei Geral de Proteção de Dados Pessoais (LGPD).",
                              "kind": "law", "enacted": "2018-08-14", "published": "2018-08-15",
                              "url": PL + "_ato2015-2018/2018/lei/l13709.htm", "temporary_until": None, "restores": None,
                              "note": None}

    # acts
    acts_out = []
    checks = {}
    for act in ACTS:
        paras, src, sha = parsed[act["slug"]]
        act_day = ACT_DAY[act["law"]][0]
        cx = Ctx(act_day, eff, mp, lapse_key, act["slug"])
        pr = lifespans(paras, cx)
        problems += [f"{act['short']}: {x}" for x in pr]
        units = list(dict.fromkeys(p["unit"] for p in paras))
        if act["slug"] == "lgpd":
            gate, gate_law = lgpd_gates(units)
        else:
            gate, gate_law = {}, {}
        versions = build_act(paras, act_day, gate, gate_law, unit_label)
        for v in versions:
            v["source_url"] = src
            v["sha256"] = sha
        acts_out.append({"slug": act["slug"], "short": act["short"], "title": act["title"], "url": act["url"],
                         "first_law": act["law"], "earlier_laws": [], "versions": versions})
        ref = consolidated(act["consolidated"], act["digits"])
        diffs = compare(versions[-1]["units"] and {u: x["text"] for u, x in versions[-1]["units"].items()}, ref)
        checks[act["slug"]] = diffs
        if a.stats:
            from collections import Counter
            print(act["short"], "paragraphs", len(paras), Counter(p["state"] for p in paras), "units", len(units),
                  "versions", len(versions))
            print("  end_how", Counter(p["end_how"] for p in paras if p["state"] != "plain"))
            for p in paras:
                if p["state"] == "mixed":
                    print("  MIXED", p["unit"], p["label"], "| struck:", p["struck_text"][:70], "| plain:", p["plain_text"][:70])
            for d in diffs:
                print("  DIFF", d)
            print(" ", len(diffs), "units differ from the consolidated page")
    for x in problems:
        print("PROBLEM", x)
    print(len(problems), "problems")
    if a.dry:
        return 0
    # ... corpus part written below
    return write_part(acts_out, laws, decisions, vig_notes, lindb, checks, problems, mp_notes(infos, eff))


def mp_notes(infos: dict, eff: dict) -> list[str]:
    out = []
    for k, info in sorted(infos.items()):
        if not k.startswith("mp-") or not info:
            continue
        if info.get("converted") and info["converted"] in eff:
            out.append(f"{law_label(k)} (in force {eff[k]}) was converted into {law_label(info['converted'])} "
                       f"(in force {eff[info['converted']]})")
        elif k in MP_LAPSE:
            out.append(f"{law_label(k)} (in force {eff.get(k)}) lapsed: {MP_LAPSE[k][1]}")
    return ["Medidas Provisórias and their fate, from each MP page's 'Convertida na Lei' line or the Congress records: "
            + "; ".join(out) + "."] if out else []


COUNTRY = {
    "code": "BR", "name": "Brazil", "slug": "brazil", "lang": "pt", "tz": "America/Sao_Paulo", "future_branch": "futuro",
    "publisher": {"name": "Presidência da República, Planalto (Legislação)", "email": "planalto@planalto.gov.br.invalid"},
    "default_in_force_rule": {
        "text": "Decreto-Lei 4.657/1942 (LINDB) art. 1: unless it says otherwise, a law is in force throughout the "
                "country 45 days after its official publication (counted under LC 95/1998 art. 8 § 1)",
        "source": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm"},
    "licence_note": "Texto de legislação federal: Presidência da República, Casa Civil, Subchefia para Assuntos "
                    "Jurídicos (www.planalto.gov.br/ccivil_03). Official acts are not protected by copyright (Lei "
                    "9.610/1998 art. 8, IV). 'Este texto não substitui o publicado no DOU.'",
}


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
    src = sources()
    reqs = 0
    mine = {fetch.wayback(i["url"], i["ts"]) for i in src.values() if i.get("ts")}
    mine_cdx = {i["url"].split("://", 1)[1] for i in src.values()}
    try:
        for line in (fetch.LOG).read_text(encoding="utf-8").splitlines():
            u = json.loads(line)["url"]
            if u in mine or any(urlq in u for urlq in []) or ("cdx/search" in u and any(
                    re.sub(r"%2F", "/", u).find(c.split("www.", 1)[-1]) >= 0 for c in mine_cdx)):
                reqs += 1
    except OSError:
        pass
    part = {
        "country": COUNTRY,
        "sources": [{
            "name": "Planalto (Presidência da República), Legislação: annotated and consolidated pages of Lei 10.406/2002 "
                    "and Lei 13.709/2018 and of every law their notes cite, read as Internet Archive raw captures",
            "url": PL, "retrieved": RETRIEVED, "requests": reqs,
            "licence": "Official acts are not protected by copyright (Lei 9.610/1998 art. 8, IV)",
            "notes": "www.planalto.gov.br blocks non-browser clients ('Acesso Negado'), so every page is the Internet "
                     "Archive raw capture (web.archive.org/web/<ts>id_/<planalto url>), byte-identical to what Planalto "
                     "served; the capture timestamps are pinned in codes/sources_codes.json."}],
        "laws": laws,
        "acts": acts_out,
        "applies": [],
        "decisions": [
            "Código Civil and LGPD: each paragraph's life span is read from Planalto's annotated page (l10406.htm, "
            "l13709.htm): struck wordings stay in place before the wording that replaced them, each closed by the source's "
            "own note ('Redação dada pela…', 'Incluído pela…', 'Revogado pela…'); text with no note is the act as enacted.",
            "Credits come only from those notes; a changed article with no note naming a law stays uncredited.",
            "A struck wording with no 'Revogado' note ends when the next wording of the same dispositivo (same label in the "
            "same article) starts; a Medida Provisória's wording with no later wording ends on the in-force day of the "
            "law that converted the MP (read from the MP page's 'Convertida na Lei' line).",
            "Where Planalto repeats an older wording after an MP wording (an MP provision that lapsed or that the "
            "conversion law dropped), the repeated wording is dated from the day the MP wording ended.",
            "Revocations by a Medida Provisória that lapsed are gaps: the text is out of force from the MP's day to the "
            "lapse and back afterwards, credited to a separate '<MP>: vigência encerrada' record that restores it.",
            "Medidas Provisórias are dated by publication (CF art. 62: force of law from publication); laws by their own "
            "vigência clause, else LINDB art. 1 (publication + 45 days).",
            "Código Civil: in force 2003-01-11 (" + ACT_DAY["lei-10406-2002"][1] + ").",
            "LGPD: " + ACT_DAY["lei-13709-2018"][1] + ". " + " ".join(f"{why}." for _, _, why in LGPD_GATES.values()) +
            " Articles not yet in force are absent from the version; when one comes into force it carries the wording "
            "of that day (including changes made before it was in force) and is credited to the law that set the day "
            "(Lei 13.709/2018 itself for art. 65 II).",
            "Headings (Livro, Título, Capítulo, Seção) are kept in one file per act, titulos.md, one line each; a note "
            "standing alone after a heading is given to the heading lines just before it.",
            "Text normalised once: NBSP to space, runs of spaces collapsed, curly quotes and dashes made plain, 'Art. 1o' "
            "written 'Art. 1º'; Planalto's link words ('Vigência', 'Produção de efeitos') and 'Vide' notes are dropped.",
            "Código Civil replay check: every remaining difference from l10406compilada.htm is a difference between "
            "Planalto's two pages, not a replay error: typing slips in the annotated page that the history is read from "
            "('i ncisos' in arts. 1.559 and 1.645, 'co nvocada' in art. 1.341, 'nstalada' in art. 1.078, '§ 3º o A' in "
            "art. 204, a stray '(' in art. 1.734 and ')' in art. 2.031, ':' for '.' in art. 1.583 § 2º); a missing 'º' "
            "in the consolidated page (art. 66 § 1º); two headings set in capitals there ('DAS ASSOCIAÇÕES', 'DAS "
            "FUNDAÇÕES'); and Título I-A (EIRELI), which the consolidated page still prints although the annotated "
            "page marks it revoked by MP 1.085/2021 and Lei 14.382/2022. The annotated text is kept as Planalto prints it.",
            "The consolidated pages print a revoked dispositivo as its bare label ('Art. 757.', 'Art. 1.620. a "
            "1.629.'); the check ignores those label-only lines, and the history leaves revoked text out.",
        ] + decisions + mpn + vig_notes + ([
            "Laws with no vigência clause of their own are dated by LINDB art. 1 (publication + 45 days): " + "; ".join(lindb) + "."
        ] if lindb else []) + [
            f"Replay check, {act}: the last version differs from Planalto's consolidated page in {len(d)} articles" +
            (": " + "; ".join(d) if d else ".") for act, d in checks.items()
        ] + ([f"Open problems in the replay ({len(problems)}): " + "; ".join(problems[:40])] if problems else []),
        "ai_use": ["Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote fetch_codes.py and parse_codes.py and the hand "
                   "tables in them (vigência days, MP lapse days) from the official pages. No model wrote, summarised or "
                   "changed legal text; no model runs at data-build or git-build time."],
    }
    OUT.parent.mkdir(exist_ok=True)
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(part, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8",
                   newline="\n")
    os.replace(tmp, OUT)
    print("wrote", OUT, OUT.stat().st_size, "bytes;", sum(len(x["versions"]) for x in acts_out), "versions")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
