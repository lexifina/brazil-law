"""Reads the cache and writes scripts/brazil-law/corpus.d/70-clt.json: the Consolidação das Leis do Trabalho (CLT,
Decreto-Lei 5.452/1943), in the corpus format of scripts/gitlaw_common/SCHEMA.md.

    python -X utf8 scripts/brazil-law/clt/parse_clt.py [--stats] [--dry]

Adapted from ../parse_phase2.py and ../codes/parse_codes.py (the Código Civil/LGPD part): the same struck-text replay
of Planalto's annotated page, with the CLT's configuration, hand tables and decisions. No network: every input is an
Internet Archive raw capture of a www.planalto.gov.br page (or a cached STF case page), pinned in clt/sources_clt.json
and fetched by clt/fetch_clt.py into ../.cache/. The same cache gives the same bytes.

How the history is rebuilt
  Planalto's annotated page (del5452.htm) keeps every superseded wording in place, struck through, directly before
  the wording that replaced it, and ends each wording with the source's own note ("(Redação dada pela Lei nº 13.467,
  de 2017)", "(Incluído pelo Decreto-lei nº 229, de 1967)", "(Revogado pela ...)", "(Suprimido pelo ...)"). Text with
  no note is the CLT as it came into force on 10.11.1943. Each paragraph gets a life span: start = in-force day of the
  law in its note (else 10.11.1943); end = its "Revogado" note, else the start of the next wording of the same
  dispositivo; a Medida Provisória's wording ends when the MP was converted, lapsed or was revoked. The text of an
  article on day D is its paragraphs alive on D, in document order. Every change is credited to the law named in the
  note that started or ended the paragraph; anything else stays uncredited. The last version is checked against
  Planalto's consolidated page (del5452compilado.htm).
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
OUT = FOLDER / "corpus.d" / "70-clt.json"
RETRIEVED = "2026-10-28"

MONTHS = {"janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7,
          "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}

# ---------------------------------------------------------------------------------------------------------------
# cache access


def sources() -> dict[str, dict]:
    return {i["id"]: i for i in json.loads((HERE / "sources_clt.json").read_text(encoding="utf-8"))["fetch"]}


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
    r"(Lei\s+Complementar|Lei|Medida\s+Provis[óo]ria|Decreto[-\s]?[Ll]ei)\s*(?:n\s*[.\]]?\s*[º°o]?\s*\.?)?\s*"
    r"(\d{1,2}(?:\.\s?\d{3})+|\d+)(?:-\d{1,2}(?!\d))?(?:[-\s]*(?P<suf>[A-Z])(?![a-z]))?(?:\s*\.)?(?:\s*,)?(?:\s*(?:de\s+)?(\d{1,2}º?\s*[./]\s*\d{1,2}\s*[./]\s*(\d{4}|\d{2})(?!\d))|"
    r"\s*de\s+(?:\d{1,2}º?\s+de\s+\w+\s+de\s+(\d{4})|(\d{4})))?", re.I)


def law_key(text: str, year_of: dict | None = None) -> str | None:
    """lei-14905-2024, lc-128-2008, mp-1085-2021, dl-4037-1942 for the first act named in text."""
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
LAW_ALIAS = {
    "lei-9528-1998": ("lei-9528-1997", "the note on art. 144 reads 'Lei nº 9.528, de 1998'; Lei 9.528 is of 10.12.1997 "
                                       "(its page, and the CLT's other notes citing it)"),
}


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
    r"Texto\s+compilado|Atualizad|Mensagem|Revoga[çc][ãa]o)[^()]*(?:\([^()]*\)[^()]*)*(?:\)|$)", re.I)
# a note Planalto left without parentheses at the end of a line: "...; Redação dada pela Medida Provisória nº 869, de 2018"
BARE_NOTE = re.compile(r"\s(?:Reda[çc][ãa]o\s+dada|Inclu[ií]d[oa]|Revogad[oa])\s+pel[oa]\s+(?:Lei|Medida|Decreto)[^()]*\)?\s*$", re.I)
LINKWORDS = re.compile(r"^\s*\(?\s*(?:Produ[çc][ãa]o\s+de\s+efeitos?|Vig[êe]ncia|Regulamento|Regulamenta[çc][ãa]o)"
                       r"\s*\)?\s*\.?\s*$", re.I)
# "(Redação dada pelo Decreto-lei nº 8.740, de 19.1.1946, com vigência suspensa pelo Decreto-lei nº 8.987-A, de 1946)"
SUSPENDED = re.compile(r",?\s*com\s+vig[êe]ncia\s+suspensa\s+(pel[oa]\s+[^()]*?)\)", re.I)
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
    s = re.sub(r"\bArt\.\.\s*(?=\d)", "Art. ", s)
    s = re.sub(r"^Art\s+(?=\d)", "Art. ", s)
    s = re.sub(r"\bArt\.(?=\d)", "Art. ", s)
    s = re.sub(r"(\d) º", r"\1º", s)
    s = re.sub(r"\bn º", "nº", s)
    s = re.sub(r"(\d)º(?=[A-Za-zÀ-ú])", r"\1º ", s)
    s = re.sub(r"\s+([.,;:])", r"\1", s)
    s = re.sub(r"\(\s+", "(", s)
    s = re.sub(r"\s+\)", ")", s)
    s = re.sub(r"\bArt\.\.\s*(?=\d)", "Art. ", s)
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
    for rx in (SUSPENDED, NOTE, LAPSED_WORDS):
        for m in rx.finditer(full):
            if not any(keep[m.start():m.end()]):
                continue
            if rx is SUSPENDED:
                notes.append(norm("(Vigência suspensa " + m.group(1) + ")"))
            elif rx is LAPSED_WORDS:
                lapsed = True
            else:
                # "(Incluído pelo Decreto-lei nº 1.535, de 13.4.1977 (Revogado pela Lei nº 13.874, de 2019)": two notes
                for part in re.split(r"\s*(?=\((?:Revogad|Reda|Inclu|Vig|Suprim|Renumer)\w*\s)", norm(m.group(0))):
                    if part.strip():
                        notes.append(part if part.endswith(")") else part + ")")
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
    # a struck cross-reference link inside unstruck text ("... no art. 3º desta Consolidação") is a typesetting slip
    link_strike = state == "mixed" and all(ln for (c, s), k, ln in zip(chars, keep, links) if k and s and not c.isspace())
    plain_text = norm("".join(c for (c, s), k in zip(chars, keep) if k and not s)) if state == "mixed" else ""
    struck_text = norm("".join(c for (c, s), k in zip(chars, keep) if k and s)) if state == "mixed" else ""
    all_link = all(link or not text.strip() for text, _, link in block["segs"])
    t = re.sub(r"\s*\((?:Al[íi]nea|Inciso|Par[áa]grafo)\s*$", "", t)
    return {"text": t, "state": state, "notes": notes, "center": block["center"], "lapsed": lapsed, "link_strike": link_strike,
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


HEADING = re.compile(r"^(?:P\s?A\s?R\s?T\s?E|LIVRO|T[ÍI]TULO|CAP[ÍI]TULO|Se[çc][ãa]o|SE[ÇC][ÃA]O|Sec[çc][ãa]o|SEC[ÇC][ÃA]O|Subse[çc][ãa]o|SUBSE[ÇC][ÃA]O)\b")
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
                          r"DE\s+(\d{1,2})º?\s+(?:DE\s+)?(\w+)\s+DE\s+(\d{4})", head, re.I):
        if str(int(mm.group(1).replace(".", "") or 0)) + (mm.group(2) or "").lower() == num.lstrip("0") or                 str(int(mm.group(1).replace(".", "") or 0)) == num.rstrip("abcdefghijklmnopqrstuvwxyz"):
            m = mm
            break
    if not m:
        return {"bad_page": "the page is not this act: " + head[:120]}
    if m.group(5) != key.split("-")[2]:
        if key not in VIGENCIA_FIXED:
            return {"bad_page": f"the page's act is of {m.group(5)}: " + head[:120]}
        info["year_mismatch"] = m.group(5)
    if m and m.group(4).lower() in MONTHS:
        info["enacted"] = f"{int(m.group(5)):04d}-{MONTHS[m.group(4).lower()]:02d}-{int(m.group(3)):02d}"
    pubs = list(re.finditer(r"publicad[oa]\s+n[oa]\s+D\.?\s*O\.?\s*U\.?\s*(?:de\s*)?(\d{1,2})\s*º?\s*\.\s*(\d{1,2})\s*\.\s*(\d{4})", head, re.I))
    # the page's own "Este texto não substitui o publicado no DOU de ..." line comes last
    pub = pubs[-1] if pubs else None
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
    clause_rx = (r"(?:(?:Est[ae]|[ÊE]st[ae]|O\s+presente|A\s+presente)\s+(?:Lei|Decreto[-\s]?[Ll]ei|Medida\s+Provis[óo]ria|C[óo]digo)"
                 r"(?:\s+Complementar)?)\s*,?\s+entra(?:r[áa])?\s+em\s+vigor|entrando\s+(?:[êe]st[ae]|o\s+presente)\s+(?:Lei|Decreto[-\s]?[Ll]ei)\s+em\s+vigor")
    cl = [mm.start() for mm in re.finditer(clause_rx, x, re.I)]
    if not cl:
        # an act revoked as a whole is struck through on its page: read its clause from the struck text
        x = head
        cl = [mm.start() for mm in re.finditer(clause_rx, x, re.I)]
    if cl:
        tail = x[cl[-1]:]
        end = re.search(r"\.\s+(?:Art\. \d|Bras[íi]lia|Este texto)", tail)
        info["clause"] = tail[:end.start() + 1] if end else tail[:600]
    else:
        info["clause"] = ""
    return info


# Hand-checked in-force days where a law's own clause is staged or not machine-readable: key -> (date, reason).
VIGENCIA_FIXED: dict[str, tuple[str, str]] = {
    "lei-4825-1965": (None, "own clause 'entra em vigor na [data] de sua publicação' (a word is missing on the page): "
                            "the publication day"),
    "lei-7108-1983": ("1983-07-05", "its page is inconsistent: the heading and the DOU line print 1986, but the act "
                                    "is signed by President João Figueiredo 'em 05 de julho de 1983' and the CLT note "
                                    "gives 5.7.1983; in force 'na data de sua publicação', whose date the page misprints, "
                                    "so the signing day is used"),
    "lei-11457-2007": ("2007-05-02", "art. 51, II: 'no primeiro dia útil do segundo mês subseqüente à data de sua "
                                     "publicação' for all but arts. 40, 41 and 47-50 (published 19.3.2007; its art. 42 "
                                     "changes the CLT; 1.5.2007 was a holiday)"),
    "lei-12873-2013": ("2013-10-25", "art. 72, III: 'na data de sua publicação quanto aos demais dispositivos' "
                                     "(published 25.10.2013); item II, b defers art. 392-B of the CLT (below)"),
    "lei-13874-2019": ("2019-09-20", "art. 20, II: 'na data de sua publicação, para os demais artigos' (published "
                                     "20.9.2019; item I was vetoed)"),
    "lei-13876-2019": ("2019-09-23", "art. 4º, II: 'quanto aos demais dispositivos, na data de sua publicação' (published "
                                     "23.9.2019); item I defers only its art. 3º, which is not the change to the CLT"),
    "lei-14690-2023": ("2023-10-03", "its clause II: 'na data de sua publicação, quanto aos demais dispositivos' "
                                     "(published 3.10.2023); item I defers only its art. 30, not the change to the CLT "
                                     "(art. 29)"),
    "mp-905-2019": ("2019-11-12", "art. 53, III: 'na data de sua publicação, quanto aos demais dispositivos' (published "
                                  "12.11.2019); item I defers its changes to CLT arts. 161, 634 and 634-A (below). Its "
                                  "§ 1º defers only the effects of some provisions (art. 457, 457-A)"),
}
# Provisions whose in-force day differs from the rest of their law: (law, act, unit) -> (date, reason).
VIGENCIA_PROVISION: dict[tuple[str, str, str], tuple[str, str]] = {
    ("lei-12873-2013", "clt", "art-392-b"): ("2014-01-23", "Lei 12.873/2013 art. 72, II, b: '90 (noventa) dias após a "
                                                           "data de sua publicação' for CLT art. 392-B (25.10.2013 + 90)"),
    **{("mp-905-2019", "clt", u): ("2020-02-10", "MP 905/2019 art. 53, I: 'noventa dias após a data de sua publicação, "
                                                 "quanto às alterações promovidas pelo art. 28 nos art. 161, art. 634 e "
                                                 "art. 634-A' (12.11.2019 + 90)")
       for u in ("art-161", "art-634", "art-634-a")},
}
# The day a lapsed Medida Provisória stopped having effect, from the Ato Declaratório of the President of Congress
# (CF art. 62 §§ 3, 4, 7 and 11): key -> (date, reason). Filled in after reading each MP page.
# Vetoed parts later promulgated after Congress overrode the veto (CF art. 66 §§ 5 and 7): law -> (day, reason).
VETO_PROMULGATION = {}
MP_LAPSE: dict[str, tuple[str, str]] = {
    "mp-808-2017": ("2018-04-24", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 22, de 2018 (DOU "
                                  "25.4.2018): 'teve seu prazo de vigência encerrado no dia 23 de abril'; the replaced "
                                  "wording is back from 24.4.2018"),
    "mp-873-2019": ("2019-06-29", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 43, de 2019: 'teve seu "
                                  "prazo de vigência encerrado no dia 28 de junho'; the replaced wording is back from "
                                  "29.6.2019"),
    "mp-955-2020": ("2020-08-18", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 113, de 2020 (DOU "
                                  "20.8.2020): 'teve seu prazo de vigência encerrado no dia 17 de agosto de 2020'; MP "
                                  "905/2019, which it had revoked, had effect again from 18.8.2020"),
    "mp-905-2019": ("2020-08-19", "Ato Declaratório do Presidente da Mesa do Congresso Nacional nº 127, de 2020 (DOU "
                                  "29.9.2020): 'teve seu prazo de vigência encerrado no dia 18 de agosto de 2020'; the "
                                  "wording it had replaced is back from 19.8.2020"),
}
# Medidas Provisórias of before Emenda Constitucional 32/2001 stay in force until revoked or voted on (EC 32 art. 2):
# key -> reason. Their wordings stand like a law's.
MP_STANDING: dict[str, str] = {
    k: "an MP in force on 11.9.2001 stays in force until a later MP revokes it or Congress votes on it (Emenda "
       "Constitucional 32/2001, art. 2)" for k in ("mp-2164-2001", "mp-2180-2001", "mp-2226-2001")}
# An MP ended by another act rather than by lapse: the end is credited to that act (no "-fim" record).
MP_LAPSE_BY: dict[str, str] = {}
# MPs that lapsed without anything coming back (their only CLT effect was to revoke another MP): key -> commit note.
MP_LAPSE_NO_EFFECT: dict[str, str] = {}


def vigencia_of(key: str, info: dict) -> tuple[str | None, str]:
    """In-force day of a law's text changes, and a one-line reason."""
    pub = info.get("published") or info.get("enacted")
    if key in VIGENCIA_FIXED:
        d, why = VIGENCIA_FIXED[key]
        return (d or pub), why
    cl = info.get("clause", "")
    if not pub:
        return None, "no publication date found"
    if not cl:
        if key.startswith("mp-"):
            return pub, f"published {pub}; a Medida Provisória has force of law from publication (CF art. 62)"
        return plus_days(pub, 45), f"no vigência clause: LINDB art. 1, published {pub} + 45 days"
    if re.search(r"em\s+vigor\s+(?:na|[àa])\s+data\.?\s+d[ae]\s+(?:sua\s+)?publica", cl, re.I):
        return pub, f"own clause 'entra em vigor na data de sua publicação' (published {pub})"
    fx = re.search(r"entra(?:r[áa])?\s+em\s+vigor\s+(?:no\s+dia|em|a\s+partir\s+de)\s+(\d{1,2})[º°]?\s+de\s+(\w+)\s+d[eo]\s+(\d{4})", cl, re.I)
    if fx and fx.group(2).lower() in MONTHS:
        d = f"{int(fx.group(3)):04d}-{MONTHS[fx.group(2).lower()]:02d}-{int(fx.group(1)):02d}"
        return d, f"own clause: in force on a fixed day ({cl[:120]})"
    words = "|".join(sorted(NUMWORDS, key=len, reverse=True))
    m = re.search(r"entra(?:r[áa])?\s+em\s+vigor\s+(?:no\s+prazo\s+de\s+)?(?:ap[óo]s\s+decorrid[oa]s?\s+|ap[óo]s\s+)?(\d+|" + words + r")\s*(?:\(([^)]+)\))?\s*(dias|meses|m[êe]s|anos?)\s+"
                  r"(?:ap[óo]s\s+|de\s+|da\s+|contados\s+da\s+|a\s+partir\s+da\s+)?(?:a\s+)?(?:data\s+de\s+|data\s+da\s+)?(?:sua|da\s+sua)\s+publica",
                  cl, re.I)
    if m:
        n = int(m.group(1)) if m.group(1).isdigit() else NUMWORDS[m.group(1).lower()]
        unit = m.group(3).lower()
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
            if re.match(r"^(?:LEI|DECRETO-LEI)\s+N", t):
                zone = "pre"
            continue
        if zone == "end":
            break
        if zone == "between":
            # the CLT: the approving decree-law is signed first; the Consolidação follows as its annex
            if re.match(r"^CONSOLIDA[ÇC][ÃA]O DAS LEIS DO TRABALHO$", t):
                zone, unit = "body", None
            else:
                continue
        if zone == "anexo":
            if t != "*":
                out.append({**b, "unit": "anexo", "label": "", "heading": False})
            continue
        if t.startswith(("Brasília,", "Rio de Janeiro,", "Este texto não substitui")):
            zone = "between" if (ANNEXED_CODE and zone == "pre") else "end"
            continue
        if ANNEXED_CODE and zone == "body" and t == "ANEXO":
            zone = "anexo"
            out.append({**b, "unit": "anexo", "label": "", "heading": False})
            continue
        if not t:
            if b["notes"] and out:
                # a note in a block of its own belongs to the line(s) before it
                if out[-1]["heading"]:
                    out[-1].setdefault("notes_after", []).extend(b["notes"])
                else:
                    attach_notes(out, b["notes"])
            continue
        if out and re.match(r"^,\s*de\s+\d{4}\)?$", t) and out[-1]["notes"] and out[-1]["notes"][-1] in NOTE_FIX:
            # a note Planalto broke over two paragraphs ("(Incluído pela Medida Provisória nº" / ", de 2019)"); the
            # number is missing from the words, so NOTE_FIX gives it from the note's link target
            out[-1]["notes"] = out[-1]["notes"][:-1] + [NOTE_FIX[out[-1]["notes"][-1]]] + b["notes"]
            continue
        if zone == "pre" and (b["all_link"] or NAV.match(t)):
            continue
        lab = label_of(t)
        if CENTER_HEADINGS:
            heading = (not lab and (b["center"] or bool(HEADING.match(t)))) or (b["center"] and not lab.startswith("Art."))
            if heading and TABLE_WORDS.match(t):
                heading = False
            # the name line under a struck "SECÇÃO II" is often not centred: a short unlabelled line with no closing
            # punctuation right after a heading line is part of the heading
            if (not heading and not lab and out and out[-1]["heading"] and HEADING.match(out[-1]["text"])
                    and not re.search(r"[.;:,]$", t) and len(t) < 160):
                heading = True
        else:
            # pages whose alignment is unreliable (the Código Penal keeps its 1940 Parte Geral inside centred blocks):
            # a heading is a Parte/Título/Capítulo/Seção line, the name line right after one, or a line in capitals
            prev_head = bool(out) and out[-1]["heading"] and bool(HEADING.match(out[-1]["text"]))
            heading = not lab and (bool(HEADING.match(t)) or bool(re.match(r"^Parte\s+(?:Geral|Especial)", t, re.I))
                                   or prev_head or (t.upper() == t and any(c.isalpha() for c in t)))
        if zone == "pre" and not ANNEXED_CODE and (lab.startswith("Art.") or heading):
            zone = "body"
        if zone == "pre":
            out.append({**b, "unit": "preambulo", "label": lab if ANNEXED_CODE else "", "heading": False})
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
        if p["heading"] or p["label"] or not p["unit"].startswith(("art-", "preambulo")) or re.search(r"[.;:,]$", p["text"]):
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
        starts = [k for k, p in enumerate(lines) if heading_id(p["text"]) == heading_id(first)]
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


def heading_id(t: str) -> str:
    """'SECÇÃO II' and 'SEÇÃO II', 'Seção II' are the same heading slot (old spelling, case)."""
    x = unicodedata.normalize("NFD", t.upper())
    x = "".join(c for c in x if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", x.replace("SECCAO", "SECAO")).strip()


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
            if re.match(r"\(\s*(?:Vide|Vig[êe]ncia(?!\s+suspensa)|Produ|Regulament|Declarad|Suspens|Execu|Express|Promulga|Convers|Convertid|Mensagem|Texto)", n, re.I):
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
            elif re.search(r"Vig[êe]ncia\s+suspensa", n, re.I):
                p["suspended"] = (d, law)
            elif END_KIND.search(n):
                ends.append((d, law))
        p["_starts"], p["_ends"] = list(starts), list(ends)
        p["start"], p["start_law"] = max(starts) if starts else (cx.act_day, None)
        p["end"], p["end_law"], p["end_how"] = None, None, None
        p["gaps"] = []
        # "com vigência suspensa pelo Decreto-lei nº 8.987-A": the suspending act undid the change. A wording made by
        # the suspended act ends when the suspension took effect; a revocation by it is only a gap.
        if p.get("suspended"):
            sd, slaw = p["suspended"]
            if ends and not starts:
                for d, law in ends:
                    if sd > d:
                        p["gaps"].append((d, sd, law, slaw))
                ends = []
                if not p["gaps"]:
                    p["suspended_noop"] = True  # suspended before the revocation took effect
            elif p["state"] != "plain":
                ends.append(p["suspended"])
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
    problems += mp_pairs(paras, cx)
    for p in paras:
        if p.get("force_start"):
            p["start"], p["start_law"] = p["force_start"]
        if p.get("force_end") and not p["end"]:
            p["end"], p["end_law"], p["end_how"] = (*p["force_end"], "court")
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
    # "Redação restabelecida pelo ...", "Restaurado pelo ...": the act brought back the wording an earlier change had
    # replaced. When Planalto prints that wording only once (after the replaced one), it is also the wording from
    # before the change: alive from its earlier start, with a gap while the change stood.
    for i, q in enumerate(paras):
        rn = [n for n in q["notes"] if re.search(r"restabelecid|Restaurad|Revigorad", n, re.I)
              and not re.search(r"com\s+nova\s+reda", n, re.I)]
        if not rn or q["start_law"] is None:
            continue
        r = predecessor(paras, i)
        if r is None:
            continue
        pr = paras[r]
        if pr["start"] >= q["start"]:
            # the change never took effect before it was undone: it is not part of the history
            pr["skip"], pr["never"] = True, True
            pp = predecessor(paras, r)
            if pp is None:
                q["start"], q["start_law"] = cx.act_day, None
            continue
        pp = predecessor(paras, r)
        if pp is None and pr["start"] > cx.act_day:
            q["gaps"].append((pr["start"], q["start"], pr["start_law"], q["start_law"]))
            q["start"], q["start_law"] = cx.act_day, None
            q["restored_from_original"] = True
    # restored wordings: a wording repeated after a later one starts again when that one ended
    for i, q in enumerate(paras):
        r = predecessor(paras, i)
        if r is None or q.get("restored_from_original") or q.get("pinned") or paras[r].get("never"):
            continue
        pr = paras[r]
        if q["text"] == pr["text"] and (pr["gaps"] or pr.get("suspended_noop")) and not pr["end"] and q["start"] <= pr["start"]:
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
    # Planalto prints a wording twice around a change that was undone (a lapsed MP's revocation, a suspended
    # decree-law): a struck copy carrying the interruption, then the wording again further down the article (after
    # a restored caput). The later copy carries on; it takes the interruption and the struck copy is not shown.
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end"] or not p["gaps"] or p.get("pinned") or p["heading"]:
            continue
        for q in paras[i + 1:]:
            if q["unit"] != p["unit"]:
                break
            if q["label"] == p["label"] and q["text"] == p["text"] and q["start"] <= p["start"] and not q.get("skip"):
                q["gaps"] = sorted(q["gaps"] + p["gaps"])
                p["skip"], p["end_how"] = True, "duplicate"
                break
        if not p.get("skip"):
            # a struck wording revoked and suspended, printed again in a new wording: it ended with the revocation
            if p.get("suspended"):
                for q in paras[i + 1:]:
                    if q["unit"] != p["unit"]:
                        break
                    if same_slot(p, q) and q["start"] >= p["gaps"][0][1]:
                        a0, _, la, _ = p["gaps"][0]
                        p["end"], p["end_law"], p["end_how"], p["gaps"] = a0, la, "note", []
                        break
    # an unstruck wording printed before struck copies of the same words further down the article is a stray copy
    for i, p in enumerate(paras):
        if p["state"] != "plain" or p["heading"] or not p["label"] or p.get("skip"):
            continue
        for q in paras[i + 1:]:
            if q["unit"] != p["unit"]:
                break
            if q["label"] == p["label"] and q["text"] == p["text"] and q["state"] == "struck" and q.get("pinned"):
                p["skip"], p["end_how"] = True, "stray-copy"
                STRAY.append(f"{p['unit']} [{p['label']}]")
                break
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end"] or p["gaps"] or p.get("skip"):
            continue
        lv = level(p["label"])
        if p["heading"]:
            # a struck heading line falls with the struck heading lines around it
            for q in list(paras[i + 1:i + 6]) + list(reversed(paras[max(0, i - 5):i])):
                if q["heading"] and q["state"] != "plain" and q["end"] and q["start"] == p["start"]:
                    p["end"], p["end_law"], p["end_how"] = q["end"], q["end_law"], "group"
                    break
            # else the heading line printed right after it, if that one has a later start, replaced it
            if not p["end"] and i + 1 < len(paras):
                q = paras[i + 1]
                if q["heading"] and q["start"] > p["start"] and not HEADING.match(q["text"]) and not HEADING.match(p["text"]):
                    p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "next-heading"
        else:
            for q in reversed(paras[:i]):
                if q["unit"] != p["unit"]:
                    break
                if level(q["label"]) < lv and not q["heading"]:
                    if q["state"] != "plain" and q["end"] and q["end"] > p["start"]:
                        p["end"], p["end_law"], p["end_how"] = q["end"], q["end_law"], "parent"
                    break
        if not p["end"] and not p["heading"]:
            # a struck copy of a wording printed again, unstruck, further down the same article (Planalto repeats a
            # wording around a change that was undone): the copy is never shown
            for q in paras[i + 1:]:
                if q["unit"] != p["unit"]:
                    break
                if q["text"] == p["text"] and q["label"] == p["label"] and q["start"] <= p["start"] and not q.get("skip"):
                    p["skip"], p["end_how"] = True, "duplicate"
                    break
        if not p["end"] and not p["heading"] and not p.get("skip"):
            # struck with no note, no successor and no struck parent: it went with the nearest struck wording of the
            # same article that started on the same day (a block a later law left out when it rewrote the article)
            for q in reversed(paras[:i]):
                if q["unit"] != p["unit"]:
                    break
                if q["state"] != "plain" and q["end"] and (q["start"], q["start_law"]) == (p["start"], p["start_law"])                         and q["end_how"] in ("successor", "note", "parent", "sibling"):
                    p["end"], p["end_law"], p["end_how"] = q["end"], q["end_law"], "sibling"
                    break
        if not p["end"] and not p.get("skip") and p["heading"]:
            # a struck heading with nothing to date its end: the consolidated page still prints these headings, so
            # they are kept
            UNDATED_HEADINGS.append(p["text"])
            continue
        if not p["end"] and not p.get("skip"):
            # Planalto strikes it, so it is not in force today, but the page gives no clue when it went: it is left out
            # of the history and listed in the decisions
            p["skip"], p["end_how"] = True, "undated"
            UNDATED.append(f"{p['unit']} [{p['label'] or 'line'}] {p['text'][:60]!r}")
            problems.append(f"no end for struck {p['unit']} [{p['label']}] {p['text'][:90]!r} notes={p['notes']}")
    for p in paras:
        if p["end"] and p["end"] <= p["start"] and p.get("suspended") and p["end"] == p["suspended"][0]:
            p["skip"], p["never"] = True, True  # suspended before it took effect
            continue
        if p["end"] and p["end"] < p["start"]:
            problems.append(f"ends before it starts: {p['unit']} [{p['label']}] {p['start']}..{p['end']} {p['text'][:70]!r} {p['notes']}")
    return problems


# STF rulings (ação direta de inconstitucionalidade) whose effect Planalto shows on the annotated page: words struck
# inside a wording, or a whole dispositivo struck, with a note naming the case. Dates from the STF case pages
# (portal.stf.jus.br, abaAndamentos): a ruling binds everyone from the publication of its judgment record (ata) in
# the Diário da Justiça (Lei 9.868/1999 art. 28; STF, Rcl 3.632 AgR), which is the version day.
COURTS = {
    "stf-adi-1770": {
        "label": "STF, ADI 1.770",
        "title": "Ação direta de inconstitucionalidade 1.770: procedente; declara inconstitucional o § 1º do art. 453 "
                 "da CLT, na redação dada pelo art. 3º da Lei nº 9.528/1997",
        "kind": "court", "enacted": "2006-10-11", "published": "2006-10-20",
        "url": "https://portal.stf.jus.br/processos/detalhe.asp?incidente=1694480",
        "from": "2006-10-20", "case": r"1\.?770", "where": [("art-453", "§ 1º")],
        "why": "STF, ADI 1.770 (Plenário, 11.10.2006): declared art. 453 § 1º unconstitutional; decision published in the "
               "DJ and DOU on 20.10.2006 (ata nº 30, STF case record); Planalto strikes the paragraph, noting the case"},
    "stf-adi-5938": {
        "label": "STF, ADI 5.938",
        "title": "Ação direta de inconstitucionalidade 5.938: procedente; declara inconstitucional a expressão \"quando "
                 "apresentar atestado de saúde, emitido por médico de confiança da mulher, que recomende o afastamento\" "
                 "dos incisos II e III do art. 394-A da CLT (redação da Lei nº 13.467/2017)",
        "kind": "court", "enacted": "2019-05-29", "published": "2019-06-04",
        "url": "https://portal.stf.jus.br/processos/detalhe.asp?incidente=5447065",
        "from": "2019-06-04", "case": r"5\.?938", "where": [("art-394-a", "II -"), ("art-394-a", "III -")],
        "why": "STF, ADI 5.938 (Plenário, 29.5.2019): struck the expression requiring a medical certificate from art. 394-A "
               "II and III; judgment record published in the DJE on 4.6.2019 (an interim order of 30.4.2019 had suspended "
               "it; the version is dated by the final judgment)"},
    "stf-adi-5766": {
        "label": "STF, ADI 5.766",
        "title": "Ação direta de inconstitucionalidade 5.766: parcialmente procedente; declara inconstitucionais o art. "
                 "790-B, caput (expressão \"ainda que beneficiária da justiça gratuita\") e § 4º, e o art. 791-A, § 4º "
                 "(expressão \"desde que não tenha obtido em juízo, ainda que em outro processo, créditos capazes de "
                 "suportar a despesa\"), da CLT, na redação da Lei nº 13.467/2017",
        "kind": "court", "enacted": "2021-10-20", "published": "2021-11-05",
        "url": "https://portal.stf.jus.br/processos/detalhe.asp?incidente=5250582",
        "from": "2021-11-05", "case": r"5\.?766",
        "where": [("art-790-b", "Art. 790-B"), ("art-790-b", "§ 4º"), ("art-791-a", "§ 4º")],
        "why": "STF, ADI 5.766 (Plenário, 20.10.2021): struck words of art. 790-B caput and art. 791-A § 4º and the whole "
               "of art. 790-B § 4º; judgment record published in the DJE on 5.11.2021. Planalto leaves art. 844 § 2º "
               "(also upheld in part) unstruck with a 'Vide ADIN 5766' note, so the history leaves it unchanged"},
}


def split_court_strikes(paras: list[dict]) -> list[str]:
    """A wording with words struck by a court becomes two: the full wording until the ruling, the rest after. A whole
    dispositivo struck by a court ends on the ruling's day. A struck cross-reference link inside unstruck text is a
    typesetting slip (the consolidated page shows it unstruck): the wording is read as unstruck."""
    out, problems, slips = [], [], []
    for p in paras:
        court = None
        for k, c in COURTS.items():
            if (p["unit"], p["label"]) in c["where"] and any(re.search(c["case"], n) for n in p["notes"]):
                court = k
        if court and p["state"] == "mixed":
            c = COURTS[court]
            out += [dict(p, state="struck", force_end=(c["from"], court)),
                    dict(p, state="plain", text=p["plain_text"], force_start=(c["from"], court))]
            continue
        if court and p["state"] == "struck":
            out.append(dict(p, force_end=(COURTS[court]["from"], court)))
            continue
        if p["state"] == "mixed":
            if p.get("link_strike"):
                slips.append(f"{p['unit']} [{p['label']}] {p['struck_text']!r}")
            else:
                problems.append(f"partly struck wording with no explanation: {p['unit']} [{p['label']}] struck "
                                f"{p['struck_text']!r}; read as unstruck")
            p = dict(p, state="plain")
        out.append(p)
    paras[:] = out
    for i, p in enumerate(paras):
        p["i"] = i
    LINK_SLIPS[:] = slips
    return problems


# Notes broken over two paragraphs whose act number is missing from the words: the note's own link names the act.
NOTE_FIX = {
    "(Incluído pela Medida Provisória nº)": "(Incluído pela Medida Provisória nº 905, de 2019)",
}
LINK_SLIPS: list[str] = []
UNDATED: list[str] = []
UNDATED_HEADINGS: list[str] = []
STRAY: list[str] = []
# column heads and cells of the tables inside art. 580, centred on the page but not headings
TABLE_WORDS = re.compile(r"^(?:Discrimina[çc][ãa]o|Percentagem|CLASSES DE CAPITAL|AL[ÍI]QUOTA|[\d.,]+\s*%?)$")


# A Medida Provisória revoked by another MP that then lapsed, after which the revoked MP ran out its own term:
# MP 905/2019 (in force 12.11.2019) was revoked by MP 955/2020 (20.4.2020); MP 955 lapsed on 17.8.2020 (Ato
# Declaratório 113/2020), so MP 905 had effect again until its own term ended on 18.8.2020 (Ato Declaratório
# 127/2020). Planalto prints each MP 905 wording twice: struck "(Revogado pela Medida Provisória n. 955, de 2020)
# (Vigência encerrada)" for the first period, struck "(Vigência encerrada)" for 18.8.2020; and each wording MP 905
# revoked twice likewise. revoked MP -> revoking MP.
MP_PAIRS = {"mp-905-2019": "mp-955-2020"}


def mp_pairs(paras: list[dict], cx: Ctx) -> list[str]:
    problems = []
    for m_key, r_key in MP_PAIRS.items():
        if m_key not in cx.eff or r_key not in cx.eff or m_key not in cx.lapse_key or r_key not in cx.lapse_key:
            problems.append(f"MP pair {m_key}/{r_key}: dates missing")
            continue
        r_eff = cx.eff[r_key]
        r_lapse, r_fim = MP_LAPSE[r_key][0], cx.lapse_key[r_key]
        m_lapse, m_fim = MP_LAPSE[m_key][0], cx.lapse_key[m_key]
        first_copies: dict[tuple, str] = {}
        for i, p in enumerate(paras):
            s_m = [d for d, law in p["_starts"] if law == m_key]
            e_m = [d for d, law in p["_ends"] if law == m_key]
            e_r = any(law == r_key for _, law in p["_ends"])
            if not (s_m or e_m) or p["state"] == "plain":
                continue
            slot = (p["unit"], p["label"], p["text"])
            p["pinned"] = True
            p["gaps"] = []
            if s_m and e_r:          # MP 905 wording, first period
                p["start"], p["start_law"] = max(s_m), m_key
                p["end"], p["end_law"], p["end_how"] = r_eff, r_key, "mp-pair"
                first_copies[slot] = "made"
            elif s_m:                # MP 905 wording again on 18.8.2020 (or a single copy: both periods)
                if first_copies.get(slot) == "made":
                    p["start"], p["start_law"] = r_lapse, r_fim
                else:
                    p["start"], p["start_law"] = max(s_m), m_key
                    p["gaps"] = [(r_eff, r_lapse, r_key, r_fim)]
                p["end"], p["end_law"], p["end_how"] = m_lapse, m_fim, "mp-pair"
            elif e_m and e_r:        # wording MP 905 revoked, back while MP 955 stood
                p["end"], p["end_law"], p["end_how"] = r_lapse, r_fim, "mp-pair"
                p["gaps"] = [(min(e_m), r_eff, m_key, r_key)]
                first_copies[slot] = "revoked"
            else:                    # the same wording revoked again on 18.8.2020: never shown, restores after
                if first_copies.get(slot) == "revoked":
                    p["start"], p["start_law"] = r_lapse, r_fim
                    p["end"], p["end_law"], p["end_how"] = m_lapse, m_fim, "mp-pair"
                    p["skip"] = True
                else:
                    p["end"], p["end_law"], p["end_how"] = m_lapse, m_fim, "mp-pair"
                    p["gaps"] = [(min(e_m), r_eff, m_key, r_key)]
        # a wording MP 905 replaced came back while MP 955 stood
        for i, p in enumerate(paras):
            if p.get("pinned") or p["state"] == "plain" or p["end"]:
                continue
            j = successor(paras, i)
            if j is None:
                continue
            q = paras[j]
            if q.get("pinned") and q["start_law"] == m_key and q["end_law"] == r_key:
                p["end"], p["end_law"], p["end_how"] = r_lapse, r_fim, "mp-pair"
                p["gaps"] = [(q["start"], r_eff, m_key, r_key)]
                p["pinned"] = True
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
    return "art" if u.startswith("art-") else "heading" if u == "titulos" else "annex" if u == "anexo" else "preamble"


def unit_label(u: str, ps: list[dict]) -> str:
    if u == "titulos":
        return "Títulos, capítulos e seções"
    if u == "preambulo":
        return "Preâmbulo (Decreto-Lei nº 5.452, de 1943)"
    if u == "anexo":
        return "Anexo (quadro a que se refere o art. 577)"
    for p in ps:
        if p["label"].startswith("Art."):
            return p["label"].rstrip(".")
    return u


# ---------------------------------------------------------------------------------------------------------------
# check against Planalto's consolidated page


BARE_LABEL = re.compile(r"^(?:Arts?\. [\d.]+º?(?:-[A-Z]{1,2})?\.?(?: a [\d.]+º?(?:-[A-Z]{1,2})?\.?)?(?: -)?|§ \d+º?(?:-[A-Z])?\.?(?: -)?|"
                        r"Parágrafo único\.?(?: -)?|[IVXLC]+(?:-[A-Z])? -|[a-z]\)|\d+\))[.;]?$")


def consolidated(ident: str, digits: int) -> dict[str, str]:
    b, _ = raw(ident)
    paras, _ = paragraphs(decode(b), digits)
    out: dict[str, list[str]] = {}
    for p in paras:
        # the consolidated page keeps a revoked dispositivo as its bare label ("Art. 757.", "III -"): not text
        slip = p["state"] == "mixed" and p.get("link_strike") and not any(re.search(r"ADI", n) for n in p["notes"])
        t = p["text"] if p["state"] == "plain" or slip else p["plain_text"] if p["state"] == "mixed" else ""
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
    {"slug": "clt", "short": "CLT", "page": "clt", "consolidated": "clt-compilado", "law": "dl-5452-1943",
     "title": "Consolidação das Leis do Trabalho (Decreto-Lei nº 5.452, de 1º de maio de 1943)", "digits": 3,
     "center_headings": True, "url": PL + "decreto-lei/del5452compilado.htm"},
]

# The day each act came into force (its own vigência clause), and its own law record.
ACT_DAY = {
    "dl-5452-1943": ("1943-11-10", "Decreto-Lei 5.452/1943 art. 2: 'O presente decreto-lei entrará em vigor em 10 de "
                                   "novembro de 1943' (published in the DOU of 9.8.1943)"),
}
ACT_LAWS = {
    "dl-5452-1943": {"label": "Decreto-Lei nº 5.452, de 1943", "title": "Aprova a Consolidação das Leis do Trabalho.",
                     "kind": "decree", "enacted": "1943-05-01", "published": "1943-08-09",
                     "url": PL + "decreto-lei/del5452.htm", "temporary_until": None, "restores": None, "note": None},
}

# Act-specific decisions, printed in REPRODUCE.md (filled in as each act is checked).
ACT_DECISIONS: list[str] = [
    "The CLT is the annex of Decreto-Lei 5.452/1943: the decree's own text (ementa, arts. 1 and 2) is the file "
    "preambulo.md, the Consolidação starts at its heading 'CONSOLIDAÇÃO DAS LEIS DO TRABALHO', and the closing 'ANEXO' "
    "(the table of economic and professional categories art. 577 refers to) is one file, anexo.md, one table cell per "
    "line in page order.",
    "Planalto's note forms read as starts: 'Redação dada', 'Incluído' (and the misspellings 'Incuído', 'Inlcuído'), "
    "'Acrescido', 'Renumerado', 'Redação restabelecida', 'Restabelecido', 'Restaurado', 'Revigorado', 'Corrigido'; as "
    "ends: 'Revogado', 'Suprimido', 'Extinto', 'Fica sem efeito'. 'Vide' notes change nothing.",
    "'com vigência suspensa pelo Decreto-lei nº 8.987-A, de 1946': the wording Decreto-Lei 8.740/1946 gave ends when "
    "8.987-A took effect; a revocation by 8.740 is a gap that 8.987-A closed; a wording 'restabelecida' by 8.987-A that "
    "Planalto prints only once is also the 1943 wording, in force before 8.740 took effect. A change suspended before "
    "it took effect is left out of the history.",
    "One note on art. 457-A, III is broken over two paragraphs and lacks the act's number ('(Incluído pela Medida "
    "Provisória nº' / ', de 2019)'); both halves link to mpv905.htm, so it is read as MP 905/2019.",
    "A struck cross-reference link inside an unstruck wording (art. 329 'art. 325', art. 442-B 'art. 3º desta "
    "Consolidação') is a typesetting slip: the consolidated page prints it unstruck, and so does the history.",
]

# set per act before parsing its pages: trust <p align="center"> to mark headings
CENTER_HEADINGS = True
# the act is the annex of an approving decree-law (the CLT): the decree's own text is the preamble, the code
# starts at its "CONSOLIDAÇÃO DAS LEIS DO TRABALHO" heading, and its closing "ANEXO" (the art. 577 table) is one unit
ANNEXED_CODE = True

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
    ap.add_argument("--dry", action="store_true", help="do not write corpus.d/70-clt.json")
    ap.add_argument("--dump", help="write every paragraph's life span to this JSON file (debugging)")
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
    no_pub = []
    for k, info in sorted(infos.items()):
        if not info:
            problems.append(f"law {k}: page not cached")
            continue
        if info.get("bad_page"):
            problems.append(f"law {k}: {info['bad_page']}")
            continue
        d, why = vigencia_of(k, info)
        if d and not info.get("published") and k not in VIGENCIA_FIXED:
            no_pub.append(f"{law_label(k)} (enacted {info.get('enacted')})")
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
    if no_pub:
        decisions.append("Pages that print no Diário Oficial date (some 1940s decree-laws give only the Coleção das Leis do "
                         "Brasil, an annual compilation): the enactment day stands in for the publication day: "
                         + "; ".join(no_pub) + ".")
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
            lapse_key[k] = MP_LAPSE_BY.get(k, k + "-fim")
        elif k in MP_LAPSE_NO_EFFECT or k in MP_STANDING:
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
    for k, note in MP_LAPSE_NO_EFFECT.items():
        if k in laws:
            laws[k]["note"] = note
    for k, lk in sorted(lapse_key.items()):
        if not lk.endswith("-fim"):
            continue
        d, why = MP_LAPSE[k]
        laws[lk] = {"label": f"{law_label(k)}: vigência encerrada", "title": f"{law_label(k)} lost effect without "
                    f"conversion into law", "kind": "law", "enacted": d, "published": d, "url": laws[k]["url"],
                    "temporary_until": None, "restores": k,
                    "note": f"{law_label(k)} lost effect on {d} without being converted into law ({why}); the wording "
                            f"it had replaced is in force again."}
    for k, rec in ACT_LAWS.items():
        laws[k] = dict(rec)
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
        pr = split_court_strikes(paras) + lifespans(paras, cx)
        if a.dump:
            Path(a.dump).write_text(json.dumps([{k: p.get(k) for k in ("i", "unit", "label", "state", "start", "start_law", "end",
                                                                       "end_law", "end_how", "gaps", "skip", "notes")}
                                                | {"text": p["text"][:90]} for p in paras], ensure_ascii=False, indent=0),
                                    encoding="utf-8")
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
    if UNDATED_HEADINGS:
        decisions.append("Headings struck on the annotated page with nothing to date their end, but still printed on the "
                         "consolidated page: kept (" + "; ".join(UNDATED_HEADINGS) + ").")
    if STRAY:
        decisions.append("An unstruck wording printed before struck copies of the same words further down the article "
                         "(the copies carrying MP 905/955) is a stray copy and is not shown: " + "; ".join(STRAY) + ".")
    if UNDATED:
        decisions.append(f"Struck text whose end the page does not date (no note, no later wording of the same "
                         f"dispositivo, no struck parent or sibling): left out of every version, since Planalto shows it "
                         f"is not in force but not since when ({len(UNDATED)} lines): " + "; ".join(UNDATED) + ".")
    if LINK_SLIPS:
        decisions.append("Struck cross-reference links read as unstruck: " + "; ".join(LINK_SLIPS) + ".")
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
        "sources": [{
            "name": "Planalto (Presidência da República), Legislação: annotated and consolidated pages of the CLT and "
                    "of every law its notes cite, read as Internet Archive raw captures",
            "url": PL, "retrieved": RETRIEVED, "requests": reqs,
            "licence": "Official acts are not protected by copyright (Lei 9.610/1998 art. 8, IV)",
            "notes": "www.planalto.gov.br blocks non-browser clients ('Acesso Negado'), so every page is the Internet "
                     "Archive raw capture (web.archive.org/web/<ts>id_/<planalto url>), byte-identical to what Planalto "
                     "served; the capture timestamps are pinned in clt/sources_clt.json."}, {
            "name": "Supremo Tribunal Federal, case pages (andamentos) of ADI 1.770, 5.938 and 5.766",
            "url": "https://portal.stf.jus.br/processos/", "retrieved": RETRIEVED, "requests": 6,
            "licence": "Official acts are not protected by copyright (Lei 9.610/1998 art. 8, IV)",
            "notes": "Read for the judgment dates and the publication of the judgment records; 3 requests to "
                     "listarProcessos.asp for the case ids, 3 to abaAndamentos.asp (cached)."}],
        "laws": laws,
        "acts": acts_out,
        "applies": [],
        "decisions": [
            "CLT (" + ", ".join(x["title"] for x in ACTS) + "): each paragraph's life span is read from "
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
        ] + decisions + mpn + vig_notes + ([
            "Laws with no vigência clause of their own are dated by LINDB art. 1 (publication + 45 days): " + "; ".join(lindb) + "."
        ] if lindb else []) + [
            f"Replay check, {act}: the last version differs from Planalto's consolidated page in {len(d)} articles" +
            (": " + "; ".join(d) if d else ".") for act, d in checks.items()
        ] + ([f"Open problems in the replay ({len(problems)}): " + "; ".join(problems[:40])] if problems else []),
        "ai_use": ["Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote clt/fetch_clt.py and clt/parse_clt.py (adapted from "
                   "../parse_phase2.py and the helper's codes/parse_codes.py) and the hand tables in them (staged "
                   "vigência days, MP fates, STF rulings) from the official pages. No model wrote, summarised or "
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
