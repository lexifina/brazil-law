"""Reads the cache and writes scripts/brazil-law/corpus.d/80-proc.json: the Código de Processo Penal (Decreto-Lei
3.689/1941) and the Código de Defesa do Consumidor (Lei 8.078/1990), in the corpus format of
scripts/gitlaw_common/SCHEMA.md.

    python -X utf8 scripts/brazil-law/proc/parse_proc.py [--stats] [--dry]

Adapted from ../parse_phase2.py (Código Penal, CPC) and ../codes/parse_codes.py (Código Civil, LGPD): the same
struck-text replay of Planalto's annotated page, with the act configuration (ACTS, ACT_DAY), the hand tables and the
decisions changed for these acts. No network: every input is an Internet Archive raw capture of a www.planalto.gov.br
page, pinned in proc/sources_proc.json and fetched by proc/fetch_proc.py into ../.cache/. The same cache gives the
same bytes.

How each act's history is rebuilt
  Planalto's annotated page of an act (del3689.htm, l8078.htm) keeps every superseded wording in place, struck
  through, directly before the wording that replaced it, and ends each wording with the source's own note ("(Redação
  dada pela Lei nº 11.719, de 2008)", "(Incluído pela ...)", "(Revogado pela ...)"). Text with no note is the act as
  enacted. Each paragraph gets a life span: start = in-force day of the law in its note (else the act's own day);
  end = its "Revogado" note, else the start of the next wording of the same dispositivo; a Medida Provisória's
  wording with no later wording ends when the MP was converted or lapsed. The text of an article on day D is its
  paragraphs alive on D, in document order. Every change is credited to the law named in the note that started or
  ended the paragraph; anything else stays uncredited. The last version is checked against Planalto's consolidated
  page (del3689compilado.htm, l8078compilado.htm).
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
OUT = FOLDER / "corpus.d" / "80-proc.json"
RETRIEVED = "2026-10-28"

MONTHS = {"janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7,
          "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}

# ---------------------------------------------------------------------------------------------------------------
# cache access


def sources() -> dict[str, dict]:
    return {i["id"]: i for i in json.loads((HERE / "sources_proc.json").read_text(encoding="utf-8"))["fetch"]}


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
    if b[:2] in (bytes([0xFF, 0xFE]), bytes([0xFE, 0xFF])):
        return b.decode("utf-16", errors="replace")
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
    r"(Lei\s+Complementar|Lei|Medida\s+Provis[óo]ria|Decreto[-\s]?[Ll]ei)\s*(?:n\s*[.\]]?\s*[º°o]?\s*\.?)?\s*"
    r"(\d{1,2}(?:\.\s?\d{3})+|\d+)(?:-\d{1,2}(?!\d))?(?:[-\s]*(?P<suf>[A-Z])(?![a-z]))?(?:\s*\.)?(?:\s*,)?(?:\s*(?:de\s+)?(\d{1,2}º?\s*[./]\s*\d{1,2}\s*[./]\s*(\d{4}|\d{2})(?!\d))|"
    r"\s*de\s+(?:\d{1,2}º?\s+de\s+\w+\s+de\s+(\d{4})|(\d{4})))?", re.I)


def law_key(text: str, year_of: dict | None = None) -> str | None:
    """lei-14905-2024, lc-128-2008, mp-1085-2021, dl-4037-1942 for the first act named in text."""
    text = NOTE_FIX.get(text, (text,))[0]
    m = LAW_REF.search(text)
    if not m:
        return None
    kind = m.group(1).lower()
    pre = "lc" if "complementar" in kind else "mp" if kind.startswith("medida") else "dl" if kind.startswith("decreto") else "lei"
    n = str(int(re.sub(r"\D", "", m.group(2)))) + (m.group("suf") or "").lower()
    y = m.group(5) or m.group(6) or m.group(7)
    if y and len(y) == 2:
        y = ("19" if int(y) >= 40 else "20") + y
    if not y and year_of:
        y = year_of.get(f"{pre}-{n}")
    if not y:
        return None
    k = f"{pre}-{n}-{y}"
    return LAW_ALIAS.get(k, (k,))[0]


# Notes whose printed number is wrong, corrected only where the note's own link names the right act: key -> (key, why).
LAW_ALIAS = {}


def law_label(key: str) -> str:
    pre, n, y = key.split("-")
    suf = n.lstrip("0123456789")
    num = f"{int(n[:len(n) - len(suf)]):,}".replace(",", ".") + (f"-{suf.upper()}" if suf else "")
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
                # an <a href> left unclosed (the Código Penal page has one near the top) must not make every later
                # paragraph a link
                self.links = []
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
    r"\(\s*(?:Reda[çc][ãa]o|Inclu[ií]d|In[cl]u[ií]d|Inlcu[ií]d|Acrescentad|Acrescid|Revogad[oa]s?\s+(?:pel|por|Medida|Lei|Decreto|dada)|"
    r"Suprimid|Extint|Revigorad|Restaurad|Restabelecid|Inciso\s+inclu|Par[áa]grafo\s+inclu|Al[íi]nea\s+inclu|"
    r"Fica\s+sem\s+efeito|Corrigid|Renumerad|(?:Par[áa]grafo|Inciso|Al[íi]nea)\s+\S+\s+renumerad|Vide|Vig[êe]ncia|"
    r"Produ[çc][ãa]o\s+de\s+efeito|Regulament|Declarad|Suspens|Execu[çc][ãa]o|Express[ãa]o|Promulga|Convers|Convertid|"
    r"Texto\s+compilado|Atualizad|Mensagem|Revoga[çc][ãa]o|Par[áa]grafo\s+[úu]nico\s+(?:renumerad|transformad))[^()]*(?:\([^()]*\)[^()]*)*(?:\)|$)", re.I)
# a note Planalto left without parentheses at the end of a line: "...; Redação dada pela Medida Provisória nº 869, de 2018"
BARE_NOTE = re.compile(r"\s(?:Reda[çc][ãa]o\s+dada|Inclu[ií]d[oa]|Revogad[oa])\s+pel[oa]\s+(?:Lei|Medida|Decreto)[^()]*\)?\s*$", re.I)
LINKWORDS = re.compile(r"^\s*\(?\s*(?:Produ[çc][ãa]o\s+de\s+efeitos?|Vig[êe]ncia|Regulamento|Regulamenta[çc][ãa]o)"
                       r"\s*\)?\s*\.?\s*$", re.I)
LAPSED_WORDS = re.compile(r"\(?\s*Vig[êe]ncia\s+encerrada\s*\)?", re.I)
START_KIND = re.compile(r"Reda[çc][ãa]o\s+(?:dada|restabelecida)|Inclu[ií]d|In[cl]u[ií]d|Inlcu[ií]d|Acrescentad|Acrescid|"
                        r"Renumerad|Revigorad|Restaurad|Restabelecid|Corrigid", re.I)
END_KIND = re.compile(r"Revogad|Suprimid|Extint|Fica\s+sem\s+efeito|Vig[êe]ncia\s+suspensa", re.I)
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
    # "Art 180." (no full stop after Art, common in the 1940 text) -> "Art. 180."
    s = re.sub(r"^Art\s+(?=\d)", "Art. ", s)
    s = re.sub(r"^A rt\.", "Art.", s)
    s = re.sub(r"(º|\d)\((VETADO|Revogad)", r"\1 (\2", s)
    return s.strip()


def analyse(block: dict) -> dict:
    """Split a block into text, struck state and notes."""
    chars: list[tuple[str, bool]] = []
    links: list[bool] = []
    for text, struck, link in block["segs"]:
        if link and LINKWORDS.match(text):
            continue
        for ch in text:
            chars.append((ch, struck))
            links.append(link)
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
    # "...(art. 282, § 4º). (Incluído pela ...). (Redação dada pela ...)": the full stops between the notes stay
    # behind as "..": one full stop
    t = re.sub(r"\.(?:\s*\.)+$", ".", t)
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
    if state == "mixed":
        # typesetting slips in unstruck text: a struck ordinal sign or full stop ("§ 1<strike>º</strike>"), or a
        # struck cross-reference link ("(<strike><a>art. 110 do Código Penal</a></strike>)", CPP art. 336)
        if not re.sub(r"[º°.\s]", "", struck_text) or all(
                ln for (c, s), k, ln in zip(chars, keep, links) if k and s and not c.isspace()):
            keep_ch = [k and (not s or c in "º°" or ln) for (c, s), k, ln in zip(chars, keep, links)]
            t = norm("".join(c for (c, _), k in zip(chars, keep_ch) if k))
            t = re.sub(r"(?:\s*\(?\s*(?:Produ[çc][ãa]o de efeitos?|Vig[êe]ncia)\s*\)?\.?)+$", "", t).strip()
            t = re.sub(r"\.(?:\s*\.)+$", ".", t)
            state, plain_text, struck_text = "plain", "", ""
        # a strike that ends inside the last words of a struck wording ("... como tam</strike>bem ao juiz", CPP
        # art. 725 III): the wording is struck
        elif t.startswith(struck_text[:40]) and n_st > n_pl:
            state = "struck"
    all_link = all(link or not text.strip() for text, _, link in block["segs"])
    return {"text": t, "state": state, "notes": notes, "center": block["center"], "lapsed": lapsed,
            "plain_text": plain_text, "struck_text": struck_text, "all_link": all_link}


ROMAN = r"[IVXLC]+"
SUFFIX = r"(?:-[A-Z]{1,2}(?![A-Za-zÀ-ú]))?"
LABEL = re.compile(
    r"^(?:(Art\.\s*\d+(?:\.\d+)?º?" + SUFFIX + r")|(§\s*\d+º?" + SUFFIX + r")|(Par[áa]grafo\s+[úuÚ]nico)|"
    r"(" + ROMAN + SUFFIX + r")\s*[-–]+\s*|(?P<bare>" + ROMAN + r")(?P<bs>-?[A-Z])?\s+(?=[a-zà-ú])|([a-z]" + SUFFIX + r")\)|(\d+)\)\s)")


def label_of(text: str) -> str:
    if re.match(r"^Il\s*-\s", text):
        return "II -"  # "Il - no concurso ..." (CPP art. 78, a lower-case L typed for I)
    m = LABEL.match(text)
    if not m:
        return ""
    if m.group("bare"):
        bs = (m.group("bs") or "").lstrip("-")
        return m.group("bare") + ("-" + bs if bs else "") + " -"
    g = next(x for x in m.groups() if x)
    g = re.sub(r"\s+", "", g).replace("Parágrafoúnico", "Parágrafo único").replace("ParágrafoÚnico", "Parágrafo único").replace("Paragrafoúnico", "Parágrafo único")
    if m.group(4):
        g += " -"
    elif m.group(7) or m.group(8):
        g += ")"
    return g.replace("Art.", "Art. ").replace("§", "§ ")


def renum_label(note: str) -> str | None:
    m = re.search(r"Par[áa]grafo\s+(\d+)\s*º?\s+renumerad", note, re.I)
    if m:
        return f"§ {int(m.group(1))}º"
    m = re.search(r"Par[áa]grafo\s+[úu]nico\s+renumerad", note, re.I)
    if m:
        return "Parágrafo único"
    m = re.search(r"(?:Inciso|Al[íi]nea)\s+(\S+)\s+renumerad", note, re.I)
    if m:
        x = m.group(1).strip(".,")
        return x + (" -" if re.match(r"^[IVXLC]+$", x) else ")")
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


HEADING = re.compile(r"^(?:P\s?A\s?R\s?T\s?E|LIVRO|T[ÍI]TULO|CAP[ÍI]TULO|Se[çc][ãa]o|SE[ÇC][ÃA]O|SEC[ÇC][ÃA]O|Sec[çc][ãa]o|Subse[çc][ãa]o|SUBSE[ÇC][ÃA]O)\b")
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
    if re.search(r"Please enable JavaScript|Acesso Negado", head[:400]):
        return {"bad_page": "bot page"}
    num = key.split("-")[1]
    m = None
    for mm in re.finditer(r"(?:LEI|MEDIDA PROVIS[ÓO]RIA|DECRETO-LEI|DECRETO LEI)[^,]{0,40}?N\s*[º°O]?\s*\.?\s*([\d.]+)(?:-?([A-Z]))?(?:-\d+)?\s*,?\s*"
                          r"DE\s+(\d{1,2})\s*[º°o]?\s+(?:DE\s+)?(\w+)\s+DE\s+(\d{4})", head, re.I):
        if str(int(mm.group(1).replace(".", "") or 0)) + (mm.group(2) or "").lower() == num.lstrip("0") or                 str(int(mm.group(1).replace(".", "") or 0)) == num.rstrip("abcdefghijklmnopqrstuvwxyz"):
            m = mm
            break
    if not m:
        return {"bad_page": "the page is not this act: " + head[:120]}
    if m and m.group(4).lower() in MONTHS:
        info["enacted"] = f"{int(m.group(5)):04d}-{MONTHS[m.group(4).lower()]:02d}-{int(m.group(3)):02d}"
    pubs = list(re.finditer(r"publicad[oa]\s+n[oa]\s+D\.?\s*O\.?\s*U\.?\s*(?:de\s*)?(\d{1,2})\s*º?\s*\.\s*(\d{1,2})\s*\.\s*(\d{4})", head, re.I))
    # the page's own "Este texto não substitui o publicado no DOU de ..." line comes last
    pub = pubs[-1] if pubs else None
    # ... unless the page goes on after the law (Lei 13.964/2019 prints the vetoed parts promulgated in 2021, with
    # their own DOU line): the first "Este texto não substitui o publicado no DOU" line is the law's own
    own = [mm for mm in pubs if re.search(r"substitui\s+o\s*$", head[max(0, mm.start() - 40):mm.start()], re.I)]
    if own:
        pub = own[0]
    if pub:
        info["published"] = f"{int(pub.group(3)):04d}-{int(pub.group(2)):02d}-{int(pub.group(1)):02d}"
    elif key in PUBLISHED_FIXED:
        info["published"] = PUBLISHED_FIXED[key][0]
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
    clause_re = (r"(?:[EÊ]st[ae]\s+(?:Lei|Medida\s+Provis[óo]ria|C[óo]digo|Decreto[-\s]?[LlI]ei)(?:\s+Complementar)?|"
                 r"A\s+presente\s+Lei)\s+entra(?:r[áa])?\s+em\s+vigor")
    cl = [mm.start() for mm in re.finditer(clause_re, x, re.I)]
    if not cl:
        # a law Planalto shows struck as a whole (revoked): its own clause is inside the struck text
        x = head
        cl = [mm.start() for mm in re.finditer(clause_re, x, re.I)]
    if cl:
        tail = x[cl[-1]:]
        end = re.search(r"\.\s+(?:Art\. \d|Bras[íi]lia|Este texto)", tail)
        info["clause"] = tail[:end.start() + 1] if end else tail[:600]
    else:
        info["clause"] = ""
    return info


# STF rulings whose effect Planalto shows on the annotated page (a dispositivo struck, with a "Vide ADI" note naming
# the case). Dates from the STF case pages (portal.stf.jus.br, abaAndamentos, cached): a ruling binds everyone from the
# publication of its judgment record in the Diário da Justiça (Lei 9.868/1999 art. 28), which is the version day.
COURTS = {
    "stf-adi-2797": {
        "label": "STF, ADI 2.797",
        "title": "Ação direta de inconstitucionalidade 2.797: procedente; declara inconstitucional a Lei nº 10.628, de "
                 "24 de dezembro de 2002, que acresceu os §§ 1º e 2º ao art. 84 do Código de Processo Penal",
        "kind": "court", "enacted": "2005-09-15", "published": "2005-09-26",
        "url": "https://portal.stf.jus.br/processos/detalhe.asp?incidente=2082833",
        "from": "2005-09-26", "case": r"2\.?797",
        "where": [("codigo-de-processo-penal", "art-084", "§ 1º"), ("codigo-de-processo-penal", "art-084", "§ 2º")],
        "why": "STF, ADI 2.797 (Plenário, 15.9.2005): declared Lei 10.628/2002, which added §§ 1º and 2º to CPP art. 84, "
               "unconstitutional; decision published in the DJ and DOU on 26.9.2005 (ata nº 25, STF case record), the "
               "day the version takes effect. Embargos de declaração (17.5.2012) fixed the effects from 15.9.2005; the "
               "history keeps the publication day. Planalto strikes both paragraphs, noting the case"},
}

# Editorial lines in the annotated page standing for a dispositivo: (act, unit, label) -> (law, line start, reason).
EDITORIAL: dict[tuple[str, str, str], tuple[str, str, str]] = {
    ("codigo-de-defesa-do-consumidor", "art-039", "XI -"): (
        "lei-9870-1999", "XI - Dispositivo incluído pela MPV nº 1.890-67",
        "CDC art. 39 XI: Planalto prints, in place of the inciso, the editorial line 'Dispositivo incluído pela MPV nº "
        "1.890-67, de 22.10.1999, transformado em inciso XIII, quando da conversão na Lei nº 9.870, de 23.11.1999' (the "
        "consolidated page too). It is kept as the source's text, starting on Lei 9.870/1999's in-force day and credited "
        "to it (the anachronism rule: not before the laws it names); the MP's own wording of XI is not on the page, so "
        "the history has no XI before then"),
}

# Publication days a law page does not print (it cites only the CLBR): key -> (date, source).
PUBLISHED_FIXED: dict[str, tuple[str, str]] = {
    "lei-263-1948": ("1948-02-26", "LexML (urn:lex:br:federal:lei:1948-02-23;263): 'Publicação Original: Diário Oficial "
                                   "da União, Seção 1, 26/02/1948, p. 2713'"),
}
# Notes that omit the act's kind, corrected only where the note's own link names the act: note -> (corrected, why).
NOTE_FIX: dict[str, tuple[str, str]] = {
    "(Redação dada pela nº 11.785, de 2008)": (
        "(Redação dada pela Lei nº 11.785, de 2008)",
        "CDC art. 54 § 3º: the note reads 'Redação dada pela nº 11.785, de 2008' and links to "
        "_Ato2007-2010/2008/Lei/L11785.htm, so it is Lei nº 11.785, de 2008"),
}
# Medidas Provisórias still within their term on the retrieval day (CF art. 62 §§ 3 and 7: 60 days, extendable once by
# 60): their wording stands, with no end date yet. key -> reason.
MP_PENDING: dict[str, str] = {
    "mp-1393-2026": "published 25.9.2026 (DOU, edição extra), in force on publication; on 28.10.2026 it was neither "
                    "converted nor lapsed (CF art. 62 § 3: 60 days, extendable once by 60), so its wording of CDC art. 57 "
                    "stands open",
}

# Hand-checked in-force days where a law's own clause is staged or not machine-readable: key -> (date, reason).
VIGENCIA_FIXED: dict[str, tuple[str, str]] = {
    "lei-263-1948": ("1948-02-29", "art. 11: 'Esta Lei entrará em vigor: no Distrito Federal, três dias depois da sua "
                                   "publicação; dez dias nos Estados do Rio de Janeiro, São Paulo e Minas; e, vinte dias, nos "
                                   "demais Estados e Territórios' (published in the DOU of 26.2.1948, per LexML: the page "
                                   "cites only the CLBR). Dated by the first day it was in force, in the Distrito Federal "
                                   "(26.2 + 3 days = 29.2.1948); in the other states it applied from 7.3 and 17.3.1948"),
}
# Provisions whose in-force day differs from the rest of their law: (law, act, unit) -> (date, reason).
VIGENCIA_PROVISION: dict[tuple[str, str, str], tuple[str, str]] = {}
# The day a lapsed Medida Provisória stopped having effect, from the Ato Declaratório of the President of Congress
# (CF art. 62 §§ 3, 4, 7 and 11): key -> (date, reason). Filled in after reading each MP page.
# Vetoed parts later promulgated after Congress overrode the veto (CF art. 66 §§ 5 and 7): law -> (day, reason).
VETO_PROMULGATION: dict[str, tuple[str, str]] = {
    "lei-13964-2019": ("2021-04-30", "the parts of Lei 13.964/2019 vetoed on 24.12.2019 were promulgated after Congress "
                                     "overrode the veto (CF art. 66 § 5; DOU 30.4.2021, printed at the end of the Lei "
                                     "13.964 page): for the CPP, art. 3º-B § 1º and art. 14-A §§ 3º to 5º"),
}
# The dispositivos each promulgation covers, read from the promulgation text on the law's page: law -> {(act, unit, label)}
VETO_PROMULGATED_UNITS: dict[str, set[tuple[str, str, str]]] = {
    "lei-13964-2019": {("codigo-de-processo-penal", "art-003-b", "§ 1º"), ("codigo-de-processo-penal", "art-014-a", "§ 3º"),
                       ("codigo-de-processo-penal", "art-014-a", "§ 4º"), ("codigo-de-processo-penal", "art-014-a", "§ 5º")},
}
MP_LAPSE: dict[str, tuple[str, str]] = {}


def months_rule(pub: str, n: int, unit: str) -> tuple[str, str]:
    months = n * 12 if unit.startswith("ano") else n
    if pub < LC107_DAY:
        return (plus_months(pub, months),
                f"own clause: {n} {unit} after publication ({pub}); before LC 107/2001 the period is counted by Lei "
                f"810/1949 arts. 2-3 (from the day of publication to the corresponding day), and the law is in force "
                f"on that day")
    return (plus_days(plus_months(pub, months), 1),
            f"own clause: {n} {unit} after publication ({pub}); the period ends on the same calendar day and the "
            f"law is in force the day after (LC 95/1998 art. 8 § 1, as the STJ applied it to the CPC, in force 18.3.2016)")


# LC 107/2001 (DOU 26.4.2001) added the counting rule of LC 95/1998 art. 8 § 1
LC107_DAY = "2001-04-26"


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
        return months_rule(pub, n, unit)
    # the same clauses written with stray spaces ("p ublicaçã o"), numbers in words ("noventa dias", "seis meses"),
    # "depois de", or the typo "entrará em vigor a data de sua publicação": match on the text without spaces
    c = re.sub(r"\s+", "", cl.lower())
    if re.search(r"entra(?:r[áa])?emvigor(?:na|a)datad[ae]suapublica", c):
        return pub, f"own clause 'entra em vigor na data de sua publicação' (published {pub})"
    words = "|".join(sorted((w.replace(" ", "") for w in NUMWORDS), key=len, reverse=True))
    m = re.search(r"entra(?:r[áa])?emvigor(?:ap[óo]sdecorrid[oa]s|decorrid[oa]s|ap[óo]s)?(\d+|" + words + r")(?:\([^)]*\))?"
                  r"(dias|meses|m[êe]s|anos?)(?:ap[óo]s|depoisd[ae]|d[ae]|contadosda|apartirda)?(?:a)?(?:datad[ae])?(?:sua|dasua)publica", c)
    if m:
        w = m.group(1)
        n = int(w) if w.isdigit() else {k.replace(" ", ""): v for k, v in NUMWORDS.items()}[w]
        unit = m.group(2)
        if unit == "dias":
            return plus_days(pub, n), f"own clause: {n} days after publication ({pub}; LC 95/1998 art. 8 § 1)"
        return months_rule(pub, n, unit)
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
            if re.match(r"^(?:LEI|DECRETO-LEI)\s+N", t):
                zone = "pre"
            continue
        if zone == "end":
            break
        if t.startswith(("Brasília,", "Rio de Janeiro,", "Este texto não substitui")):
            zone = "end"
            continue
        if not t or re.fullmatch(r"[.;,:\s]+", t):
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
        if CENTER_HEADINGS:
            heading = (not lab and (b["center"] or bool(HEADING.match(t)))) or (b["center"] and not lab.startswith("Art."))
        else:
            # pages whose alignment is unreliable (the Código Penal keeps its 1940 Parte Geral inside centred blocks):
            # a heading is a Parte/Título/Capítulo/Seção line, the name line right after one, or a line in capitals
            prev_head = bool(out) and out[-1]["heading"] and bool(HEADING.match(out[-1]["text"]))
            heading = not lab and (bool(HEADING.match(t)) or bool(re.match(r"^Parte\s+(?:Geral|Especial)", t, re.I))
                                   or prev_head or (t.upper() == t and "," not in t and any(c.isalpha() for c in t)))
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
    move_rubricas(out)
    heading_groups(out)
    for i, p in enumerate(out):
        p["i"] = i
    return out, notes_only


def move_rubricas(out: list[dict]) -> None:
    """The Código Penal and others put a marginal heading (rubrica, "Anterioridade da Lei") on its own line before an
    article. Such a line has no label and no closing punctuation, and the next labelled line starts a new article: it
    belongs to that article's file, as its first line, labelled "rubrica" so its wordings replace each other."""
    for i, p in enumerate(out):
        if p["heading"] or p["label"] or not p["unit"].startswith(("art-", "preambulo")) or re.search(r"[.;:,]$", p["text"]) or p["text"].startswith("Pena "):
            continue
        for q in out[i + 1:]:
            if q["heading"]:
                break
            if not q["label"] and not re.search(r"[.;:,]$", q["text"]):
                continue  # another rubrica (an older wording, struck)
            if q["label"].startswith("Art.") and q["unit"] != p["unit"]:
                p["unit"], p["label"] = q["unit"], "rubrica"
            break


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
    # editorial lines Planalto prints in place of a dispositivo, naming the acts that made it so (EDITORIAL): they start
    # with the act they describe (the anachronism rule: never before the law they name)
    for p in paras:
        hit = EDITORIAL.get((cx.act, p["unit"], p["label"]))
        if hit and p["state"] == "plain" and p["text"].startswith(hit[1]) and hit[0] in cx.eff:
            p["start"], p["start_law"], p["start_how"] = cx.eff[hit[0]], hit[0], "editorial"
    # a whole dispositivo struck by a court (COURTS): it ends on the ruling's day
    for p in paras:
        for k, c in COURTS.items():
            if (p["state"] != "plain" and not p["end"] and (cx.act, p["unit"], p["label"]) in c["where"]
                    and any(re.search(c["case"], n) for n in p["notes"])):
                p["end"], p["end_law"], p["end_how"] = c["from"], k, "court"
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
        if q["heading"]:
            # a heading reworded between the old and the new wording of one article (CPP Capítulo V before art. 201)
            continue
        if q["unit"] != p["unit"]:
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
    # laws in force on the act's own first day (SAME_DAY_LAWS): the act as enacted comes first, then their changes
    # as a second version of the same day ("same_day": true)
    same = {law for p in paras for d, law in events(p) if d == act_day and law in SAME_DAY_LAWS}
    order = [(act_day, True)] if same else []
    order += [(d, False) for d in sorted(days)]
    for day, pre in order:
        cur: dict[str, str] = {}
        for u in units:
            if gate.get(u, act_day) > day:
                continue
            if pre:
                live = [p for p in by_unit[u] if not p.get("skip") and p["start"] <= day
                        and not (p["start"] == day and p["start_law"] in same)
                        and (p["end"] is None or day < p["end"] or (p["end"] == day and p["end_law"] in same))]
            else:
                live = [p for p in by_unit[u] if alive(p, day)]
            lines = [p["text"] for p in live]
            # a marginal heading left above an article whose text is gone (revoked) is not an article
            if all(p["label"] == "rubrica" for p in live):
                lines = []
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
        v = {"from": day, "units": {u: {"label": unit_label(u, by_unit[u]), "kind": unit_kind(u), "text": t}
                                    for u, t in cur.items()}, "credits": credits}
        if versions and versions[-1]["from"] == day:
            v["same_day"] = True
        versions.append(v)
        prev = cur
    return versions


def to_deltas(versions: list[dict]) -> list[dict]:
    """SCHEMA "Large acts": the first version in full, every later one as `changes` (None removes a unit)."""
    out, prev = [], None
    for v in versions:
        units = v.pop("units")
        if prev is None:
            v["units"] = units
        else:
            v["changes"] = {u: units.get(u) for u in sorted(set(units) | set(prev)) if units.get(u) != prev.get(u)}
        out.append(v)
        prev = units
    return out


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


BARE_LABEL = re.compile(r"^(?:Arts?\. [\d.]+º?(?:-[A-Z]{1,2})?\.?(?: a [\d.]+º?(?:-[A-Z]{1,2})?\.?)?(?: -)?|§ \d+º?(?:-[A-Z])?\.?(?: -)?|Parágrafo único\.?(?: -)?|[IVXLC]+(?:-[A-Z])? -|[a-z]\))$")


# the CPP consolidated page's other forms of a revoked dispositivo: "Art. 556. a Art. 560", "Art. 561. e Art. 562.",
# "Art. 632.:", "IV - (revogado).", "§ 2º (Revogado):."
PLACEHOLDER = re.compile(r"^(?:Arts?\. [\d.]+º?(?:-[A-Z]{1,2})?\.?(?:\s*[ae]\s+Art\. [\d.]+º?(?:-[A-Z]{1,2})?\.?)?[:.;]*|"
                         r"(?:Arts?\. [\d.]+º?(?:-[A-Z]{1,2})?\.?|§ \d+º?(?:-[A-Z])?\.?|Parágrafo único\.?|[IVXLC]+(?:-[A-Z])? -|[a-z]\))"
                         r"\s*\((?:[Rr]evogad[oa]s?|REVOGAD[OA]S?)\)[.;:]*)$")


def consolidated(ident: str, digits: int) -> dict[str, str]:
    b, _ = raw(ident)
    paras, _ = paragraphs(decode(b), digits)
    out: dict[str, list[str]] = {}
    for p in paras:
        # the consolidated page keeps a revoked dispositivo as its bare label ("Art. 757.", "III -"): not text
        t = p["text"] if p["state"] == "plain" else p["plain_text"] if p["state"] == "mixed" else ""
        if t and not BARE_LABEL.match(t) and not PLACEHOLDER.match(t):
            out.setdefault(p["unit"], []).append(t)
    # a revoked article the consolidated page still marks by its marginal heading only (no text of its own)
    out = {u: ls for u, ls in out.items()
           if u == "titulos" or any(label_of(l) or re.search(r"[.;:,]$", l) for l in ls)}
    return {u: "".join(l + "\n" for l in ls) for u, ls in out.items()}


def compare(last: dict[str, str], ref: dict[str, str]) -> list[str]:
    # an unstruck "(Revogado)" placeholder of the annotated page is not text either (the consolidated page's are
    # dropped in consolidated())
    def text_only(t: str) -> str | None:
        x = "".join(l + "\n" for l in t.splitlines() if not PLACEHOLDER.match(l))
        return x or None
    last = {u: x for u, t in last.items() if (x := text_only(t))}
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
    {"slug": "codigo-de-processo-penal", "short": "CPP", "page": "cpp", "consolidated": "cpp-compilado",
     "law": "dl-3689-1941", "title": "Código de Processo Penal (Decreto-Lei nº 3.689, de 3 de outubro de 1941)",
     "digits": 3, "center_headings": False, "url": PL + "decreto-lei/del3689compilado.htm"},
    {"slug": "codigo-de-defesa-do-consumidor", "short": "CDC", "page": "cdc", "consolidated": "cdc-compilado",
     "law": "lei-8078-1990", "title": "Código de Defesa do Consumidor (Lei nº 8.078, de 11 de setembro de 1990)",
     "digits": 3, "url": PL + "leis/l8078compilado.htm"},
]

# The day each act came into force (its own vigência clause), and its own law record.
ACT_DAY = {
    "dl-3689-1941": ("1942-01-01", "Decreto-Lei 3.689/1941 art. 810: 'Este Código entrará em vigor no dia 1º de janeiro "
                                   "de 1942' (published in the DOU of 13.10.1941, rectified 24.10.1941)"),
    "lei-8078-1990": ("1991-03-11", "Lei 8.078/1990 art. 118: 'Este código entrará em vigor dentro de cento e oitenta "
                                    "dias a contar de sua publicação' (published in the DOU of 12.9.1990, edição extra): "
                                    "12.9.1990 + 180 days = 11.3.1991"),
}
ACT_LAWS = {
    "dl-3689-1941": {"label": "Decreto-Lei nº 3.689, de 1941", "title": "Código de Processo Penal.", "kind": "decree",
                     "enacted": "1941-10-03", "published": "1941-10-13", "url": PL + "decreto-lei/del3689.htm",
                     "temporary_until": None, "restores": None, "note": None},
    "lei-8078-1990": {"label": "Lei nº 8.078, de 1990", "title": "Dispõe sobre a proteção do consumidor e dá outras "
                      "providências.", "kind": "law", "enacted": "1990-09-11", "published": "1990-09-12",
                      "url": PL + "leis/l8078.htm", "temporary_until": None, "restores": None, "note": None},
}

# Act-specific decisions, printed in REPRODUCE.md (filled in as each act is checked).
ACT_DECISIONS: list[str] = [
]

# A law that re-enacted a whole part of an act: Planalto keeps the old part as one struck block, then prints the new
# part, whose lines often carry no note. act slug -> (law, the heading that ends the new part, reason).
REWRITES: dict = {
}
# A law that re-enacted one chapter: Planalto prints the old chapter as one struck block, then the new chapter.
# (act slug, law, name line of the old chapter's struck heading, first heading line after the new chapter, reason)
REWRITE_BLOCKS = [
    ("codigo-de-processo-penal", "lei-11689-2008", "DO PROCESSO DOS CRIMES DA COMPETÊNCIA DO JÚRI", "CAPÍTULO III",
     "Lei 11.689/2008 art. 1 re-enacted Livro II, Título I, Capítulo II (the Júri procedure, arts. 406 to 497: 'O "
     "Capítulo II do Título I do Livro II do Decreto-Lei nº 3.689 ... passa a vigorar com a seguinte redação'). "
     "Planalto prints the old chapter (with its amendments up to 2008) as one struck block, then the new chapter. "
     "Every struck line of the old block that no note or later wording ends is ended on Lei 11.689's in-force day, and "
     "every line of the new chapter without a note of its own starts that day, credited to Lei 11.689"),
]


def rewrite_blocks(paras: list[dict], act: dict, eff: dict, fixed: set) -> None:
    for slug, law, name, end_heading, _ in REWRITE_BLOCKS:
        if slug != act["slug"] or law not in eff:
            continue
        day = eff[law]
        k = next(i for i, p in enumerate(paras) if p["heading"] and p["state"] != "plain" and p["text"] == name)
        first = k - 1 if k and paras[k - 1]["heading"] and paras[k - 1]["state"] != "plain" else k
        new_from = next(i for i in range(first, len(paras)) if paras[i]["state"] == "plain")
        new_to = next(i for i in range(new_from + 1, len(paras)) if paras[i]["heading"] and paras[i]["text"] == end_heading)
        for p in paras[first:new_from]:
            if not p["end"]:
                p["end"], p["end_law"], p["end_how"] = day, law, "rewrite"
                fixed.add(p["i"])
        for p in paras[new_from:new_to]:
            if p["start_law"] is None and p["start"] < day:
                p["start"], p["start_law"] = day, law

def apply_rewrites(paras: list[dict], act: dict, eff: dict, problems: list[str]) -> list[str]:
    fixed = set()
    hit = REWRITES.get(act["slug"])
    if hit:
        rewrite(paras, hit, eff, fixed)
    rewrite_blocks(paras, act, eff, fixed)
    # a struck "(VETADO)" line with no note directly above a wording of the same dispositivo that a law's note
    # introduces, the law's vetoed parts having been promulgated later (VETO_PROMULGATION, CPP art. 3º-B § 1º): the
    # "(VETADO)" line stands from that law's day to the promulgation, and the promulgated wording starts then
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["notes"] or not re.search(r"\(VETADO\)\.?$", p["text"], re.I) or not p["label"]:
            continue
        q = next((q for q in paras[i + 1:i + 8] if q["unit"] == p["unit"] and q["label"] == p["label"]), None)
        if q is None:
            continue
        pv = VETO_PROMULGATION.get(q["start_law"] or "")
        if not pv or (act["slug"], p["unit"], p["label"]) not in VETO_PROMULGATED_UNITS.get(q["start_law"], set()):
            continue
        p["start"], p["start_law"] = q["start"], q["start_law"]
        p["end"], p["end_law"], p["end_how"] = pv[0], q["start_law"], "promulgation"
        q["start"], q["promulgated"] = pv[0], True
        fixed.add(i)
    # a law in force on the act's first day (SAME_DAY_LAWS) replaces or revokes wording that starts that same day:
    # the ordinary rules want a strictly later start, so its wordings are matched here
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end"] or p["heading"]:
            continue
        lv = level(p["label"])
        for q in paras[i + 1:]:
            if q["unit"] != p["unit"] or q["heading"] or (lv < 5 and level(q["label"]) < lv):
                break
            if same_slot(p, q) and q["start_law"] in SAME_DAY_LAWS and q["start"] >= p["start"]:
                p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "same-day"
                fixed.add(i)
                break
        if p["end"]:
            continue
        for q in reversed(paras[:i]):
            if q["unit"] != p["unit"]:
                break
            if level(q["label"]) < lv and not q["heading"]:
                if q["state"] != "plain" and q["end"] and q["end_law"] in SAME_DAY_LAWS and q["end"] >= p["start"]:
                    p["end"], p["end_law"], p["end_how"] = q["end"], q["end_law"], "same-day"
                    fixed.add(i)
                break
        if p["end"]:
            continue
        for q in paras[i + 1:]:
            if q["unit"] != p["unit"] or q["state"] == "plain":
                break
            if q["end_law"] in SAME_DAY_LAWS and q["end"] and q["end"] >= p["start"]:
                p["end"], p["end_law"], p["end_how"] = q["end"], q["end_law"], "same-day"
                fixed.add(i)
                break
    # no line is older than its article: in an article every caput of which carries a later note (inserted after the
    # act), a line dated earlier (no note, or a note Planalto copied from an older article: CP art. 334-A § 2º cites
    # Lei 4.729/1965) starts with the article's first caput
    by_unit: dict[str, list[dict]] = {}
    for p in paras:
        by_unit.setdefault(p["unit"], []).append(p)
    for unit, ps in by_unit.items():
        caps = [p for p in ps if p["label"].startswith("Art.")]
        if not caps or not all(p["start_law"] for p in caps) or unit in ("titulos", "preambulo"):
            continue
        first = min(caps, key=lambda p: p["start"])
        for p in ps:
            if p["start"] < first["start"] and (p["end"] is None or p["end"] > first["start"]):
                p["start"], p["start_law"], p["start_how"] = first["start"], first["start_law"], "article"
    # a struck paragraph whose words reappear later in the same article under another label (CP art. 334: the 1940
    # § 2º is the § 3º that Lei 4.729/1965 "included") was renumbered when that label starts
    def body(t: str) -> str:
        return re.sub(r"^(?:§ \d+º?|Parágrafo único)\.?\s*-?\s*", "", t)
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end_how"] not in (None, "parent") or not p["label"].startswith(("§", "Parágrafo")):
            continue
        for q in paras[i + 1:]:
            if q["unit"] != p["unit"]:
                break
            if (q["label"] != p["label"] and q["label"].startswith("§") and body(q["text"]) == body(p["text"])
                    and q["start"] > p["start"] and (p["end"] is None or q["start"] < p["end"])):
                p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "renumbered-same-text"
                fixed.add(i)
                break
    # successive struck wordings of one dispositivo that Planalto printed out of date order (art. 121 § 7º II: the
    # 2022 wording above the 2018 one): chain them by their own dates; the last ends with the run's revocation note
    i = 0
    while i < len(paras):
        j = i
        while (j + 1 < len(paras) and paras[j + 1]["unit"] == paras[i]["unit"] and paras[j + 1]["label"] == paras[i]["label"]
               and paras[i]["label"] and paras[j + 1]["state"] != "plain" and paras[i]["state"] != "plain"):
            j += 1
        run = paras[i:j + 1]
        if len(run) > 1 and [p["start"] for p in run] != sorted(p["start"] for p in run):
            revs = [(d, law) for p in run for n in p["notes"] if END_KIND.search(n)
                    for law in [law_key(n)] if law and (d := eff.get(law))]
            chain = sorted(run, key=lambda p: (p["start"], p["i"]))
            for a, b in zip(chain, chain[1:]):
                a["end"], a["end_law"], a["end_how"] = b["start"], b["start_law"], "date-order"
                fixed.add(a["i"])
            if revs:
                last = chain[-1]
                last["end"], last["end_law"], last["end_how"] = (*max(revs), "date-order")
                fixed.add(last["i"])
            for p in run:
                p.pop("restored", None)
            problems = [x for x in problems if not ("restored wording" in x and any(p["text"][:80] in x for p in run))]
        i = j + 1
    # a vetoed item ("§ 2º - (VETADO).") that Planalto leaves unstruck above the wording Congress later promulgated
    # over the veto: the "(VETADO)" line stands from the law's day to the promulgation, the promulgated wording after
    for i, p in enumerate(paras):
        if p["state"] != "plain" or p["end"] or not re.search(r"\(VETADO\)\.?$", p["text"]) or not p["label"]:
            continue
        for q in paras[i + 1:]:
            if q["unit"] != p["unit"]:
                break
            hit = VETO_PROMULGATION.get(q["start_law"] or "")
            if q["label"] == p["label"] and hit:
                if p["start_law"] is None:
                    p["start"], p["start_law"] = q["start"], q["start_law"]
                p["end"], p["end_law"], p["end_how"] = hit[0], q["start_law"], "promulgation"
                q["start"] = hit[0]
                break
    # a "Parágrafo único" Planalto left unstruck although a later law (named in the note of a "§ 1º" below it) made
    # it § 1º: an article cannot have both, so it ends when the § 1º starts
    for i, p in enumerate(paras):
        if p["state"] != "plain" or p["end"] or p["label"] != "Parágrafo único":
            continue
        for q in paras[i + 1:]:
            if q["unit"] != p["unit"]:
                break
            if q["label"] == "§ 1º" and q["start"] > p["start"] and q["start_law"]:
                p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "renumbered"
                break
    # Planalto often closes a struck run of lines (a revoked article) with one "Revogado pela" note on its last line:
    # an earlier line of the same struck run with nothing else to end it is revoked with it
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end"] or p["heading"]:
            continue
        for q in paras[i + 1:]:
            if q["unit"] != p["unit"] or q["state"] == "plain":
                break
            if q["end_how"] == "note" and any(END_KIND.search(n) for n in q["notes"]) and q["end"] > p["start"]:
                p["end"], p["end_law"], p["end_how"] = q["end"], q["end_law"], "run-revoked"
                fixed.add(i)
                break
    # a struck marginal heading (or an unlabelled heading line inside an article) with nothing to end it falls with
    # the dispositivo it heads: the next labelled line of the same article
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end"] or p["heading"] or p["label"] not in ("rubrica", ""):
            continue
        q = next((q for q in paras[i + 1:] if q["label"] not in ("rubrica", "") or q["unit"] != p["unit"]), None)
        if q is not None and q["unit"] == p["unit"] and q["state"] != "plain" and q["end"] and q["end"] > p["start"]:
            p["end"], p["end_law"], p["end_how"] = q["end"], q["end_law"], "heads"
            fixed.add(i)
    # a struck heading block (CAPÍTULO V / DAS PERGUNTAS AO OFENDIDO) with struck articles under it, then the same
    # heading reworded (CAPÍTULO V / DO OFENDIDO, the note on its name line): the old block ends when the new one,
    # dated by its note, starts; the new block's unannotated lines start with it
    for i, p in enumerate(paras):
        if not p["heading"] or p["state"] == "plain" or p["end"] or (i and paras[i - 1]["heading"] and paras[i - 1]["state"] != "plain"):
            continue
        run = [i]
        while run[-1] + 1 < len(paras) and paras[run[-1] + 1]["heading"] and paras[run[-1] + 1]["state"] != "plain":
            run.append(run[-1] + 1)
        j = run[-1] + 1
        while j < len(paras) and not paras[j]["heading"] and paras[j]["state"] != "plain":
            j += 1
        if j >= len(paras) or not paras[j]["heading"] or paras[j]["state"] != "plain" or paras[j]["text"] != p["text"]:
            continue
        new = [j]
        while new[-1] + 1 < len(paras) and paras[new[-1] + 1]["heading"] and paras[new[-1] + 1]["state"] == "plain":
            new.append(new[-1] + 1)
        dated = [(paras[k]["start"], paras[k]["start_law"]) for k in new[:len(run)] if paras[k]["start_law"]]
        if not dated:
            continue
        d, law = max(dated)
        for k in run:
            if not paras[k]["end"]:
                paras[k]["end"], paras[k]["end_law"], paras[k]["end_how"] = d, law, "heading-reworded"
                fixed.add(k)
        for k in new[:len(run)]:
            if not paras[k]["start_law"] and paras[k]["start"] < d:
                paras[k]["start"], paras[k]["start_law"] = d, law
    # a struck heading left inside a revoked run of articles (CPP Capítulo II 'DO JULGAMENTO' among arts. 556-562)
    # falls with the next struck dispositivo after it
    for i, p in enumerate(paras):
        if not p["heading"] or p["state"] == "plain" or p["end"]:
            continue
        q = next((q for q in paras[i + 1:] if not q["heading"]), None)
        if q is not None and q["state"] != "plain" and q["end"] and q["end"] > p["start"]:
            p["end"], p["end_law"], p["end_how"] = q["end"], q["end_law"], "heads"
            fixed.add(i)
    return [x for x in problems if not any(f"{paras[i]['text'][:90]!r}" in x for i in fixed)]


def rewrite(paras: list[dict], hit: tuple, eff: dict, fixed: set) -> None:
    law, end_heading, _ = hit
    day = eff[law]
    body = [i for i, p in enumerate(paras) if p["unit"] != "preambulo"]
    first = body[0]
    new_from = next(i for i in body if paras[i]["state"] == "plain")
    new_to = next(i for i in range(new_from, len(paras)) if paras[i]["heading"] and paras[i]["text"].upper() == end_heading)
    for p in paras[first:new_from]:
        if p["state"] != "plain" and not p["end"]:
            p["end"], p["end_law"], p["end_how"] = day, law, "rewrite"
            fixed.add(p["i"])
    for p in paras[new_from:new_to]:
        if p["start_law"] is None and p["start"] < day:
            p["start"], p["start_law"] = day, law

# Laws in force on the very day their act first applies (Lei 13.256/2016 amended the CPC before it came into force,
# "no início da vigência"): their changes are a second version of that day, after the act as enacted.
SAME_DAY_LAWS: set[str] = set()

# set per act before parsing its pages: trust <p align="center"> to mark headings
CENTER_HEADINGS = True

# not used for these acts; kept so the shared replay code runs unchanged
LGPD_GATES: dict = {}


def lgpd_gates(units: list[str]) -> tuple[dict[str, str], dict[str, str]]:
    gate, law = {}, {}
    for u in units:
        if u in ("art-065", "preambulo"):
            continue
        g = "early" if u in LGPD_EARLY else "sanctions" if u in LGPD_SANCTIONS else "rest"
        gate[u], law[u] = LGPD_GATES[g][0], LGPD_GATES[g][1]
    return gate, law


def anachronisms(paras: list[dict], cx: Ctx) -> list[str]:
    """The coordinator's rule on text that appears before its law: every line alive on a day must have every law its
    start notes name already in force. The replay dates lines by those notes, so this lists what the later rules
    (article, restoration, promulgation) moved earlier."""
    out = []
    for p in paras:
        if p.get("skip"):
            continue
        for n in p["notes"]:
            if not START_KIND.search(n):
                continue
            law = law_key(n, cx.mp.get("_years"))
            d = law and (VIGENCIA_PROVISION.get((law, cx.act, p["unit"]), (None,))[0] or cx.eff.get(law))
            if d and p["start"] < d:
                out.append(f"{p['unit']} [{p['label']}] starts {p['start']} before {law} ({d}): {p['text'][:70]!r}")
    return out


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
    global CENTER_HEADINGS
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--dry", action="store_true", help="do not write corpus.d/80-proc.json")
    a = ap.parse_args(argv)
    problems: list[str] = []
    decisions: list[str] = []

    # paragraphs of each act
    parsed = {}
    for act in ACTS:
        b, src = raw(act["page"])
        CENTER_HEADINGS = act.get("center_headings", True)
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
        elif k in MP_PENDING:
            fate = {}
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
    for k, rec in ACT_LAWS.items():
        laws[k] = dict(rec)
    for (_, _, _), (_, _, why) in EDITORIAL.items():
        decisions.append(why + ".")
    for k, (d, why) in PUBLISHED_FIXED.items():
        decisions.append(f"{law_label(k)}: published {d} ({why}).")
    for k, (fixed_note, why) in NOTE_FIX.items():
        decisions.append(f"Note corrected: {why}.")
    for k, c in COURTS.items():
        laws[k] = {kk: c[kk] for kk in ("label", "title", "kind", "enacted", "published", "url")}
        laws[k].update({"temporary_until": None, "restores": None, "note": None})
        decisions.append(c["why"] + ".")

    # acts
    acts_out = []
    checks = {}
    for act in ACTS:
        paras, src, sha = parsed[act["slug"]]
        act_day = ACT_DAY[act["law"]][0]
        cx = Ctx(act_day, eff, mp, lapse_key, act["slug"])
        pr = lifespans(paras, cx)
        pr = apply_rewrites(paras, act, eff, pr)
        problems += [f"{act['short']}: {x}" for x in pr]
        ana = anachronisms(paras, cx)
        problems += [f"{act['short']}: text before its law: {x}" for x in ana]
        units = list(dict.fromkeys(p["unit"] for p in paras))
        if act["slug"] == "lgpd":
            gate, gate_law = lgpd_gates(units)
        else:
            gate, gate_law = {}, {}
        versions = build_act(paras, act_day, gate, gate_law, unit_label)
        for v in versions:
            v["source_url"] = src
            v["sha256"] = sha
        today_units = [v for v in versions if v["from"] <= RETRIEVED][-1]["units"]
        versions = to_deltas(versions)
        acts_out.append({"slug": act["slug"], "short": act["short"], "title": act["title"], "url": act["url"],
                         "first_law": act["law"], "earlier_laws": [], "versions": versions})
        CENTER_HEADINGS = act.get("center_headings", True)
        ref = consolidated(act["consolidated"], act["digits"])
        diffs = compare({u: x["text"] for u, x in today_units.items()}, ref)
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
        elif k in MP_PENDING:
            out.append(f"{law_label(k)} (in force {eff.get(k)}) still pending: {MP_PENDING[k]}")
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
        "sources": [{
            "name": "Planalto (Presidência da República), Legislação: annotated and consolidated pages of the CPP and "
                    "the CDC and of every law their notes cite, read as Internet Archive raw captures",
            "url": PL, "retrieved": RETRIEVED, "requests": reqs,
            "licence": "Official acts are not protected by copyright (Lei 9.610/1998 art. 8, IV)",
            "notes": "www.planalto.gov.br blocks non-browser clients ('Acesso Negado'), so every page is the Internet "
                     "Archive raw capture (web.archive.org/web/<ts>id_/<planalto url>), byte-identical to what Planalto "
                     "served; the capture timestamps are pinned in proc/sources_proc.json."}],
        "laws": laws,
        "acts": acts_out,
        "applies": [],
        "decisions": [
            "Acts of this part (" + ", ".join(x["title"] for x in ACTS) + "): each paragraph's life span is read from "
            "Planalto's annotated page of the act (" + ", ".join(sources()[x["page"]]["url"].rsplit("/", 1)[1] for x in ACTS) +
            "): struck wordings stay in place before the wording that replaced them, each closed by the source's own note "
            "('Redação dada pela…', 'Incluído pela…', 'Revogado pela…'); text with no note is the act as enacted.",
            "Credits come only from those notes; a changed article with no note naming a law stays uncredited.",
            "A struck wording with no 'Revogado' note ends when the next wording of the same dispositivo (same label in the "
            "same article) starts; a Medida Provisória's wording with no later wording ends on the in-force day of the "
            "law that converted the MP (read from the MP page's 'Convertida na Lei' line).",
            "Medidas Provisórias are dated by publication (CF art. 62: force of law from publication); laws by their own "
            "vigência clause, else LINDB art. 1 (publication + 45 days).",
            *[f"{x['title']}: in force {ACT_DAY[x['law']][0]} ({ACT_DAY[x['law']][1]})." for x in ACTS],
            "Headings (Parte, Título, Capítulo, Seção) and the marginal headings (rubricas) are kept in one file per act, "
            "titulos.md, one line each; a note standing alone after a heading is given to the heading lines just before it.",
            "Text normalised once: NBSP to space, runs of spaces collapsed, curly quotes and dashes made plain, 'Art. 1o' "
            "written 'Art. 1º'; Planalto's link words ('Vigência', 'Produção de efeitos') and 'Vide' notes are dropped.",
            "The consolidated pages print a revoked dispositivo as its bare label ('Art. 757.'); the check ignores those "
            "label-only lines, and the history leaves revoked text out.",
            *ACT_DECISIONS,
            *[f"{a['title']}: {REWRITES[a['slug']][2]}" for a in ACTS if a["slug"] in REWRITES],
            *[f"{x[4]}." for x in REWRITE_BLOCKS],
            *[f"{law_label(k)}: {why}." for k, (d, why) in VETO_PROMULGATION.items()],
        ] + decisions + mpn + vig_notes + ([
            "Laws with no vigência clause of their own are dated by LINDB art. 1 (publication + 45 days): " + "; ".join(lindb) + "."
        ] if lindb else []) + [
            f"Replay check, {act}: the last version differs from Planalto's consolidated page in {len(d)} articles" +
            (": " + "; ".join(d) if d else ".") for act, d in checks.items()
        ] + ([f"Open problems in the replay ({len(problems)}): " + "; ".join(problems[:40])] if problems else []),
        "ai_use": ["Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote proc/fetch_proc.py and proc/parse_proc.py (adapted "
                   "from fetch_phase2.py/parse_phase2.py, clt/fetch_clt.py and codes/parse_codes.py) and the hand "
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
