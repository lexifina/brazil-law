"""Reads the Planalto cache (fetch.py) and writes scripts/brazil-law/corpus.json (scripts/gitlaw_common/SCHEMA.md).

    python -X utf8 scripts/brazil-law/parse.py [--stats] [--retrieved YYYY-MM-DD]

No network: everything comes from .cache/ (Internet Archive raw captures of www.planalto.gov.br, pinned in
sources.json). The same cache gives the same bytes.

How the Constitution's history is rebuilt
  Planalto's annotated page (constituicao.htm) keeps every superseded wording in place, struck through
  (<strike>), directly before the wording that replaced it, and ends each wording with the source's own note:
  "(Redação dada pela Emenda Constitucional nº 26, de 2000)", "(Incluído pela ...)", "(Revogado pela ...)",
  "(Renumerado do parágrafo único, pela ...)". Text with no note is the 1988 original.
  Each paragraph (one <p>, one line of the output) gets a life span:
    start = in-force day of the amendment in its "Redação dada / Incluído / Renumerado" note (else 1988-10-05);
    end   = for struck text, the in-force day of its "Revogado pela" note, else the start of the next wording of
            the same dispositivo (same label, later start) in the same article; unstruck text is still in force.
  The text of an article on day D is its paragraphs alive on D, in document order. Every change is credited to
  the amendment named in the note that started or ended the paragraph; anything else stays uncredited.
  The last version is checked line by line against Planalto's consolidated page (constituicaocompilado.htm).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fetch  # noqa: E402

PL = "https://www.planalto.gov.br/ccivil_03/"
CF_URL = PL + "constituicao/constituicao.htm"
CF_DATE = "1988-10-05"

# ---------------------------------------------------------------------------------------------------------------
# cache access


def sources() -> dict[str, dict]:
    return {i["id"]: i for i in json.loads((HERE / "sources.json").read_text(encoding="utf-8"))["fetch"]}


def raw(ident: str) -> tuple[bytes, str] | None:
    """Bytes of the pinned capture of a source id, and its Wayback URL; None if not cached."""
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
# HTML -> blocks of (text, struck) segments

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
        self.anchors: list[str] = []

    def flush(self) -> None:
        if any(s.strip() for s, _, _ in self.cur):
            self.blocks.append({"segs": self.cur, "center": self.center, "anchors": self.anchors})
        self.cur, self.anchors = [], []

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
            if a.get("name"):
                self.anchors.append(a["name"])
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
    # "Art. 6<sup>o</sup>" -> "Art. 6º"
    html = re.sub(r"\s*<sup>\s*(?:<[^>]+>\s*)*([oaº°ª])\s*(?:<[^>]+>\s*)*</sup>",
                  lambda m: "ª" if m.group(1) in "aª" else "º", html, flags=re.I)
    p = Blocks()
    p.feed(html)
    p.close()
    p.flush()
    return p.blocks


# ---------------------------------------------------------------------------------------------------------------
# notes and text

NOTE = re.compile(
    r"\(\s*(?:Reda[çc][ãa]o|Inclu[ií]d|Acrescentad|Acrescid|Revogad[oa]s?\s+(?:pel|por)|Renumerad|Vide|Vig[êe]ncia|"
    r"Produ[çc][ãa]o\s+de\s+efeito|Regulament|Declarad|Suspens|Execu[çc][ãa]o|Express[ãa]o|Promulga|Convers|"
    r"Texto\s+compilado|Atualizad|Mensagem)[^()]*(?:\([^()]*\)[^()]*)*\)", re.I)
LINKWORDS = re.compile(r"^\s*\(?\s*(?:Produ[çc][ãa]o\s+de\s+efeitos?|Vig[êe]ncia|Regulamento|Regulamenta[çc][ãa]o)"
                       r"\s*\)?\s*\.?\s*$", re.I)
EC_REF = re.compile(r"Emenda\s+(?:Constitu\w*\s+){1,2}(de\s+Revis[ãa]o\s+)?(?:n\s*[º°o]\.?|n\.)?\s*(\d+)", re.I)
START_KIND = re.compile(r"Reda[çc][ãa]o\s+dada|Inclu[ií]d|Acrescentad|Acrescid|Renumerad", re.I)
END_KIND = re.compile(r"Revogad", re.I)
RENUM_FROM = re.compile(r"Renumerad[oa]\s+d[eo]s?\s+(par[áa]grafo\s+[úu]nico|inciso\s+[IVXLC]+|§\s*\d+\s*[º°o]?)", re.I)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s)
    s = s.replace(" ", " ").replace("​", "")
    s = s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    s = s.replace("–", "-").replace("—", "-")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"(\bArt\.|§)\s*(\d+)\s*\.?\s*[o°º](?![a-zà-ú])", r"\1 \2º", s)
    s = re.sub(r"\bArt\.(?=\d)", "Art. ", s)
    s = re.sub(r"\s+([.,;:])", r"\1", s)
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
    for m in NOTE.finditer(full):
        notes.append(norm(m.group(0)))
        for i in range(m.start(), m.end()):
            keep[i] = False
    text = "".join(c for (c, _), k in zip(chars, keep) if k)
    n_st = sum(1 for (c, s), k in zip(chars, keep) if k and s and not c.isspace())
    n_pl = sum(1 for (c, s), k in zip(chars, keep) if k and not s and not c.isspace())
    t = norm(text)
    # trailing link words left outside <a> ("... Vigência")
    t = re.sub(r"(?:\s*\(?\s*(?:Produ[çc][ãa]o de efeitos?|Vig[êe]ncia)\s*\)?\.?)+$", "", t).strip()
    state = "plain" if n_st == 0 else ("struck" if n_pl == 0 else "mixed")
    if state == "mixed":
        # labels or punctuation left outside <strike> ("a) <strike>texto</strike>"; "<strike>rt. 76</strike>")
        pl = norm("".join(c for (c, s), k in zip(chars, keep) if k and not s))
        if len(re.sub(r"[^\w]|(?:[IVXLC]+|[a-z]|\d+[º]?|Art|A)", "", pl)) == 0 and n_st > n_pl:
            state = "struck"
    # in a mixed block, keep the struck text apart so it can be reported
    struck_text = norm("".join(c for (c, s), k in zip(chars, keep) if k and s)) if state == "mixed" else ""
    plain_text = norm("".join(c for (c, s), k in zip(chars, keep) if k and not s)) if state == "mixed" else ""
    return {"text": t, "state": state, "notes": notes, "center": block["center"], "anchors": block["anchors"],
            "struck_text": struck_text, "plain_text": plain_text}


ROMAN = r"[IVXLC]+"
SUFFIX = r"(?:\s*-\s*[A-Z]{1,2}(?![A-Za-zÀ-ú]))?"
LABEL = re.compile(
    r"^(?:(Art\.\s*\d+(?:\.\d+)?º?" + SUFFIX + r")|(§\s*\d+º?" + SUFFIX + r")|(Par[áa]grafo\s+[úu]nico)|"
    r"(" + ROMAN + SUFFIX + r")\s*[-–]+\s*|([a-z]" + SUFFIX + r")\)|(\d+)\)\s)")


def label_of(text: str) -> str:
    m = LABEL.match(text)
    if not m:
        return ""
    g = next(x for x in m.groups() if x)
    g = re.sub(r"\s+", "", g).replace("Parágrafoúnico", "Parágrafo único").replace("Paragrafoúnico", "Parágrafo único")
    if m.group(4):
        g += " -"
    elif m.group(5) or m.group(6):
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


# ---------------------------------------------------------------------------------------------------------------
# amendments: quadro_emc (enactment and DOU date) and each amendment's own vigência clause

def dmy(s: str) -> str:
    d, m, y = (int(x) for x in re.findall(r"\d+", s)[:3])
    return f"{y:04d}-{m:02d}-{d:02d}"


def amendments() -> dict[str, dict]:
    """Law records for the ECs (from quadro_emc) and ECRs (from their own pages)."""
    laws: dict[str, dict] = {}
    b, u = raw("quadro-emc")
    t = re.sub(r"<script\b.*?</script>", " ", decode(b), flags=re.I | re.S)
    t = re.sub(r"\(function\(\)\{var f5_cspm.*", "", t, flags=re.S)
    for row in re.split(r"<tr\b", t, flags=re.I)[1:]:
        txt = norm(__import__("html").unescape(re.sub(r"<[^>]+>", " ", "<tr" + row)))
        txt = re.sub(r"(\d)º\.", r"\1.", txt)  # "1º.7.2004"
        m = re.match(r"(\d+),\s*de\s*(\d{1,2}\.\d{1,2}\.\d{4})\s*Publicad[ao]\s+no\s+DOU\s*(?:de\s*)?(\d{1,2}\.\d{1,2}\.\d{4})"
                     r"(.*)$", txt)
        if not m:
            continue
        n = int(m.group(1))
        rest = m.group(4).strip()
        rest = re.sub(r"^[-\s]*(?:Edi[çc][ãa]o\s+extra|Retificad[ao][^A-Z]*|Republicad[ao][^A-Z]*)\s*", "", rest).strip()
        laws[f"ec-{n:03d}"] = {
            "label": f"Emenda Constitucional nº {n}, de {int(m.group(2)[-4:])}",
            "title": rest,
            "kind": "law",
            "enacted": dmy(m.group(2)),
            "published": dmy(m.group(3)),
            "url": PL + (f"constituicao/emendas/emc/emc{n:02d}.htm" if n < 10 else f"constituicao/emendas/emc/emc{n}.htm"),
            "temporary_until": None, "restores": None, "note": None,
        }
    for n in range(1, 7):
        r = raw(f"ecr-{n}")
        if not r:
            continue
        x = norm(__import__("html").unescape(re.sub(r"<[^>]+>", " ", decode(r[0]))))
        m = re.search(r"REVIS[ÃA]O\s+N[º°O]?\s*\.?\s*%d,?\s+DE\s+(\d+)\s+DE\s+(\w+)\s+DE\s+(\d{4})" % n, x, re.I)
        pub = re.search(r"publicad[oa]\s+no\s+D\.?\s*O\.?\s*U\.?\s+(?:de\s+)?(\d{1,2}\.\d{1,2}\.\d{4})", x, re.I)
        laws[f"ecr-{n}"] = {
            "label": f"Emenda Constitucional de Revisão nº {n}, de 1994",
            "title": "", "kind": "law",
            "enacted": f"{int(m.group(3)):04d}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}" if m else None,
            "published": dmy(pub.group(1)) if pub else None,
            "url": PL + f"constituicao/emendas/ecr/ecr{n}.htm",
            "temporary_until": None, "restores": None, "note": None,
        }
    return laws


MONTHS = {"janeiro": 1, "fevereiro": 2, "março": 3, "marco": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7,
          "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}


def vigencia_clause(ident: str) -> str:
    """The amendment's own 'entra em vigor' sentence (for the stats report and decisions)."""
    r = raw(ident)
    if not r:
        return ""
    x = norm(__import__("html").unescape(re.sub(r"<[^>]+>", " ", decode(r[0]))))
    m = re.search(r"[^.]*(?:entra(?:rá)? em vigor|produz(?:indo|irá)? efeitos?)[^.]*\.", x, re.I)
    return m.group(0).strip() if m else ""


# ---------------------------------------------------------------------------------------------------------------
# the Constitution


def unit_key(label: str, adct: bool) -> str:
    m = re.match(r"Art\. (\d+)(?:\.\d+)?º?(?:-([A-Z]{1,2}))?", label)
    k = f"art-{int(m.group(1)):03d}" + (f"-{m.group(2).lower()}" if m.group(2) else "")
    return ("adct-" + k) if adct else k


def cf_paragraphs(html: str) -> list[dict]:
    """Paragraphs of the Constitution in document order with unit keys and labels."""
    bl = [analyse(b) for b in blocks_of(html)]
    out = []
    zone = None   # None (before preamble), 'pre', 'body', 'sig', 'adct', 'end'
    unit = None
    for b in bl:
        t = b["text"]
        if not t:
            continue
        if zone is None:
            if t == "PREÂMBULO":
                zone, unit = "pre", "preambulo"
            continue
        if t.startswith("Este texto não substitui"):
            zone = "end" if zone == "adct" else "sig"
            continue
        if t.startswith("ATO DAS DISPOSIÇÕES CONSTITUCIONAIS TRANSITÓRIAS"):
            zone, unit = "adct", None
            continue
        if zone in ("sig", "end"):
            continue
        if zone in ("pre", "body", "adct") and t.startswith("Brasília, 5 de outubro de 1988"):
            zone = "sig" if zone != "adct" else "end"
            continue
        lab = label_of(t)
        if zone == "pre" and t.startswith("TÍTULO I"):
            zone = "body"
        if b["center"] or (not lab and re.match(r"^(TÍTULO|CAPÍTULO|Seção|SEÇÃO|Subseção|SUBSEÇÃO)\b", t)):
            out.append({**b, "unit": "adct-titulos" if zone == "adct" else "titulos", "label": "", "heading": True})
            continue
        if lab.startswith("Art."):
            unit = unit_key(lab, zone == "adct")
        if unit is None:
            unit = "adct-preambulo" if zone == "adct" else "preambulo"
        out.append({**b, "unit": unit, "label": lab, "heading": False})
    return out


def law_of_note(note: str) -> str | None:
    m = EC_REF.search(note)
    if not m:
        return None
    n = int(m.group(2))
    return f"ecr-{n}" if m.group(1) else f"ec-{n:03d}"


def lifespans(paras: list[dict], eff: dict[str, str], effect_override) -> list[str]:
    """Set start/end (and their laws) on every paragraph; return problems found."""
    problems = []
    for p in paras:
        starts, ends = [], []
        p["renum_from"] = None
        for n in p["notes"]:
            law = law_of_note(n)
            if not law:
                continue
            if law not in eff:
                problems.append(f"unknown law in note {n!r}")
                continue
            d = effect_override(law, p) or eff[law]
            if START_KIND.search(n):
                starts.append((d, law))
                if re.search(r"Renumerad", n, re.I):
                    p["renum_from"] = (renum_label(n), d, law)
            elif END_KIND.search(n):
                ends.append((d, law))
        p["start"], p["start_law"] = max(starts) if starts else (CF_DATE, None)
        p["end"], p["end_law"] = (None, None)
        if p["state"] != "plain" and ends:
            p["end"], p["end_law"] = min(ends)
        elif p["state"] == "plain" and ends and not starts:
            # an unstruck "(Revogado)" placeholder: it starts when the repeal took effect
            p["start"], p["start_law"] = max(ends)
    for i, p in enumerate(paras):
        p["end_how"] = "note" if p["end"] else None
        if p["state"] == "plain" or p["end"]:
            continue
        lv = level(p["label"])
        if p.get("heading"):
            # a struck heading is replaced by the heading lines right after it
            for q in paras[i + 1:]:
                if not q.get("heading"):
                    break
                if q["start"] > p["start"]:
                    p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "successor"
                    break
            if not p["end"]:
                problems.append(f"no end for struck heading {p['text'][:90]!r} notes={p['notes']}")
            continue
        for q in paras[i + 1:]:
            if q["unit"] != p["unit"]:
                break
            if level(q["label"]) < min(lv, 2) or (lv < 5 and level(q["label"]) < lv):
                break
            same = q["label"] == p["label"] or (q["renum_from"] and q["renum_from"][0] == p["label"])
            if same and q["start"] > p["start"]:
                p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "successor"
                break
        if not p["end"]:
            # struck with no note and no later wording: it fell with the nearest struck enclosing dispositivo
            for q in reversed(paras[:i]):
                if q["unit"] != p["unit"]:
                    break
                if level(q["label"]) < lv and not q.get("heading"):
                    if q["state"] != "plain" and q["end"] and q["end"] > p["start"]:
                        p["end"], p["end_law"], p["end_how"] = q["end"], q["end_law"], "parent"
                    break
        if not p["end"]:
            problems.append(f"no end for struck {p['unit']} [{p['label']}] {p['text'][:90]!r} notes={p['notes']}")
    return problems


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


def text_on(paras: list[dict], unit: str, day: str) -> str:
    lines = [p["text"] for p in paras if p["unit"] == unit and p["start"] <= day and (p["end"] is None or day < p["end"])]
    return "".join(l + "\n" for l in lines)


# ---------------------------------------------------------------------------------------------------------------


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--retrieved", default="2026-10-28")
    a = ap.parse_args(argv)
    laws = amendments()
    eff = {k: v["published"] for k, v in laws.items()}
    b, cf_src = raw("cf")
    paras = cf_paragraphs(decode(b))
    problems = lifespans(paras, eff, lambda law, p: None)
    if a.stats:
        from collections import Counter
        print("paragraphs", len(paras), Counter(p["state"] for p in paras))
        print("units", len({p["unit"] for p in paras}))
        for p in paras:
            if p["state"] == "mixed":
                print("MIXED", p["unit"], p["label"], "| struck:", p["struck_text"][:80], "| plain:", p["plain_text"][:80])
        for x in problems:
            print("PROBLEM", x)
        print(len(problems), "problems")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
