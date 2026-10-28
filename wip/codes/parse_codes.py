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
    r"(Lei\s+Complementar|Lei|Medida\s+Provis[óo]ria|Decreto[-\s]?[Ll]ei)\s*(?:n[º°o]?\s*\.?|n\.)?\s*"
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
    return f"{pre}-{n}-{y}"


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
        if tag == "a":
            self.links.append(bool(a.get("href")))

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
        if tag in BREAK:
            self.flush()
        if tag in STRIKE:
            self.strike = max(0, self.strike - 1)
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
    r"Texto\s+compilado|Atualizad|Mensagem|Revoga[çc][ãa]o)[^()]*(?:\([^()]*\)[^()]*)*\)", re.I)
# a note Planalto left without parentheses at the end of a line: "...; Redação dada pela Medida Provisória nº 869, de 2018"
BARE_NOTE = re.compile(r"\s(?:Reda[çc][ãa]o\s+dada|Inclu[ií]d[oa]|Revogad[oa])\s+pel[oa]\s+(?:Lei|Medida|Decreto)[^()]*$", re.I)
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
    m = re.search(r"(?:LEI|MEDIDA PROVIS[ÓO]RIA|DECRETO-LEI)[^,]{0,40}?N[º°O]?\s*\.?\s*[\d.]+\s*,\s*DE\s+(\d{1,2})º?\s+DE\s+(\w+)\s+DE\s+(\d{4})",
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
VIGENCIA_FIXED: dict[str, tuple[str, str]] = {}
# Provisions whose in-force day differs from the rest of their law: (law, act, unit) -> (date, reason).
VIGENCIA_PROVISION: dict[tuple[str, str, str], tuple[str, str]] = {}
# The day a lapsed Medida Provisória stopped having effect, from the Ato Declaratório of the President of Congress
# (CF art. 62 §§ 3, 4, 7 and 11): key -> (date, reason). Filled in after reading each MP page.
MP_LAPSE: dict[str, tuple[str, str]] = {}


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
    m = re.search(r"entra(?:r[áa])?\s+em\s+vigor\s+(?:ap[óo]s\s+decorrid[oa]s\s+|ap[óo]s\s+)?(\d+)\s*\(([^)]+)\)\s*(dias|meses|m[êe]s|anos?)\s+"
                  r"(?:ap[óo]s\s+|de\s+|da\s+data\s+de\s+|contados\s+da\s+data\s+de\s+|a\s+partir\s+da\s+data\s+de\s+)?(?:a\s+data\s+de\s+)?(?:sua|da\s+sua)\s+publica",
                  cl, re.I)
    if m:
        n, unit = int(m.group(1)), m.group(3).lower()
        if unit == "dias":
            return plus_days(pub, n), f"own clause: {n} days after publication ({pub}; LC 95/1998 art. 8 § 1)"
        months = n * 12 if unit.startswith("ano") else n
        return plus_months(pub, months), f"own clause: {n} {unit} after publication ({pub})"
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
                # a note in a block of its own belongs to the line(s) before it (headings, mostly)
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
    for i, p in enumerate(out):
        p["i"] = i
    return out, notes_only


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
        if p["gaps"] and p["state"] != "plain" and not p["end"]:
            # struck only because of a lapsed MP's revocation: Planalto keeps the strike, the text is back
            pass
    # struck wordings: the next wording of the same dispositivo ends them
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end"]:
            continue
        if p["gaps"] and not any(re.search(r"Reda|Inclu|Revog", n, re.I) and not cx.mp.get(law_key(n, cx.mp.get("_years")) or "", {}).get("lapsed_on")
                                 for n in p["notes"] if END_KIND.search(n)):
            pass
        succ = successor(paras, i)
        if succ is not None:
            q = paras[succ]
            p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "successor"
            continue
        fate = cx.mp.get(p["start_law"]) if p["start_law"] else None
        if fate and fate.get("converted_on"):
            p["end"], p["end_law"], p["end_how"] = fate["converted_on"], fate["converted"], "conversion"
            continue
        if p["gaps"]:
            continue
    # restored wordings: a wording repeated after a later one starts again when that one ended
    for i, q in enumerate(paras):
        r = predecessor(paras, i)
        if r is None:
            continue
        pr = paras[r]
        if q["start"] < pr["start"] or (q["start"] == pr["start"] and q["start_law"] == pr["start_law"] and pr["state"] != "plain"
                                         and q["text"] == pr["text"] and pr.get("end")):
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
        return p["heading"] and q["heading"] and bool(p["label"]) and p["label"].split()[0] == q["label"].split()[0] \
            and p["label"] == q["label"]
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
            if q["start"] > p["start"] and (not p["label"] or same_slot(p, q) or not q["label"]):
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
            for j in range(i - 1, max(-1, i - 8), -1):
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


def consolidated(ident: str, digits: int) -> dict[str, str]:
    b, _ = raw(ident)
    paras, _ = paragraphs(decode(b), digits)
    out: dict[str, list[str]] = {}
    for p in paras:
        if p["state"] == "plain" and p["text"]:
            out.setdefault(p["unit"], []).append(p["text"])
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
        d = [x for x in difflib.unified_diff(bl, al, lineterm="", n=0) if not x.startswith(("---", "+++", "@@"))]
        diffs.append(f"{u}: " + " | ".join(x[:160] for x in d[:6]))
    return diffs
