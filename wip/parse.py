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
import os
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
CACHE_LOG = HERE / ".cache" / "requests.jsonl"

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
        self.spans: list[bool] = []

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
        if tag == "span":
            lt = "line-through" in (a.get("style") or "").lower()
            self.spans.append(lt)
            self.strike += lt
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
        if tag == "span" and self.spans:
            self.strike = max(0, self.strike - self.spans.pop())
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
        if len(re.sub(r"[^\w]|\b(?:[IVXLC]+|[a-z]|\d+[º]?|Art|A)\b", "", pl)) == 0 and n_st > n_pl:
            state = "struck"
    # in a mixed block, keep the struck text apart so it can be reported
    struck_text = norm("".join(c for (c, s), k in zip(chars, keep) if k and s)) if state == "mixed" else ""
    plain_text = norm("".join(c for (c, s), k in zip(chars, keep) if k and not s)) if state == "mixed" else ""
    plain_text = re.sub(r",\s*,", ",", plain_text)
    return {"text": t, "state": state, "notes": notes, "center": block["center"], "anchors": block["anchors"],
            "struck_text": struck_text, "plain_text": plain_text}


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


def page_text(ident: str) -> str:
    r = raw(ident)
    t = re.sub(r"(?is)<script.*?</script>|<strike>.*?</strike>", " ", decode(r[0]))
    x = norm(__import__("html").unescape(re.sub(r"<[^>]+>", " ", t)))
    return x[:x.rfind("Brasília")] if "Brasília" in x else x


def final_clause(ident: str) -> str:
    """The amendment's own closing 'Esta Emenda ... entra em vigor ...' article, or ''."""
    x = page_text(ident)
    m = [mm.start() for mm in re.finditer(r"Art\. \d+º?\.?\s*(?:-\s*)?[Ee]sta\s+Emenda[^.]*?entra", x)]
    if not m:
        return ""
    tail = x[m[-1]:]
    end = re.search(r"\.\s+(?:Art\. \d|Mesa d|Este texto)", tail)
    return tail[:end.start() + 1] if end else tail


def plus_days(d: str, n: int) -> str:
    return (dt.date.fromisoformat(d) + dt.timedelta(days=n)).isoformat()


# In-force days the amendment's own clause sets, other than its publication day. Each: (date, reason).
VIGENCIA_FIXED = {
    "ec-014": ("1997-01-01", "art. 6: 'entra em vigor a primeiro de janeiro do ano subseqüente ao de sua promulgação' (promulgated 12.9.1996)"),
    "ec-025": ("2001-01-01", "art. 3: 'entra em vigor em 1º de janeiro de 2001'"),
    "ec-078": (None, "art. 3: 'entra em vigor no exercício financeiro seguinte ao de sua publicação': 1 January of the next year"),
    "ec-105": (None, "art. 3: 'entra em vigor em 1º de janeiro do ano subsequente ao de sua publicação'"),
    "ecr-5": ("1995-01-01", "art. 2: 'entra em vigor no dia 1º de janeiro de 1995'"),
}
# Provisions whose in-force day differs from the rest of their amendment: (law, unit, label) -> (date, reason).
VIGENCIA_PROVISION = {
    ("ec-109", "art-029-a", "Art. 29-A"): ("2025-01-01", "EC 109/2021 art. 7: the change to art. 29-A 'entra em vigor a partir do "
                                           "início da primeira legislatura municipal após a data de publicação' (published "
                                           "16.3.2021; the next municipal legislature began on 1.1.2025)"),
    ("ec-114", "art-100", "§ 5º"): ("2022-01-01", "EC 114/2021 art. 8, I: the change to art. 100 § 5º enters into force 'a partir "
                                    "de 2022'"),
}


def vigencia(laws: dict[str, dict]) -> tuple[dict[str, str], list[str]]:
    """In-force day of every amendment (its own clause, else LINDB art. 1), and the decisions that explain it."""
    eff, dec, lindb = {}, [], []
    for k, law in sorted(laws.items()):
        ident = ("emc-" + str(int(k[3:]))) if k.startswith("ec-") else k
        clause = final_clause(ident)
        if k in VIGENCIA_FIXED:
            d, why = VIGENCIA_FIXED[k]
            if d is None:
                d = f"{int(law['published'][:4]) + 1}-01-01"
            eff[k] = d
            dec.append(f"{law['label']}: in force {d} by its own {why}.")
        elif re.search(r"entra em vigor na data d[ae] sua publica", clause, re.I):
            eff[k] = law["published"]
            if re.search(r"efeito|aplicando|exceto|excetuad", clause, re.I):
                dec.append(f"{law['label']}: dated by its publication day {law['published']} ('entra em vigor na data de "
                           f"sua publicação'); its clause also defers or limits effects, which does not change the text's "
                           f"in-force day: \"{clause}\"")
        elif re.search(r"entra em vigor na data d[ae] sua promulga", clause, re.I):
            eff[k] = law["enacted"]
            dec.append(f"{law['label']}: in force on its promulgation day {law['enacted']} by its own clause \"{clause}\"")
        elif re.search(r"entra em vigor:", clause, re.I):
            eff[k] = law["published"]
            dec.append(f"{law['label']}: staged clause \"{clause}\"; the text Planalto shows is dated by publication "
                       f"({law['published']}) except the provisions listed separately.")
        elif not clause:
            eff[k] = plus_days(law["published"], 45)
            lindb.append(f"{law['label'].replace('Emenda Constitucional', 'EC')} ({law['published']} -> {eff[k]})")
        else:
            raise SystemExit(f"unhandled vigência clause for {k}: {clause!r}")
    if lindb:
        dec.append("Amendments with no vigência clause of their own are dated by the default rule (LINDB art. 1: in "
                   "force 45 days after official publication, counted with LC 95/1998 art. 8 § 1, i.e. publication day "
                   "+ 45): " + "; ".join(lindb) + ". Some authors hold that an amendment with no clause is in force "
                   "on publication; the rule is applied as written.")
    for (law, unit, label), (d, why) in sorted(VIGENCIA_PROVISION.items()):
        dec.append(f"{unit} {label}: the {laws[law]['label']} wording is dated {d}: {why}.")
    return eff, dec


# ---------------------------------------------------------------------------------------------------------------
# the Constitution

# Headings an amendment renamed, which Planalto shows struck with the new name below and no note. Each new name is
# checked against the amendment's own text at parse time.
HEADING_RENAMES = {
    "DOS SERVIDORES PÚBLICOS CIVIS": ("ec-018", "DOS SERVIDORES PÚBLICOS"),
    "DOS TRIBUNAIS E JUÍZES DO TRABALHO": ("ec-092", "Do Tribunal Superior do Trabalho, dos Tribunais Regionais do Trabalho e dos Juízes do Trabalho"),
    "DA CIÊNCIA E TECNOLOGIA": ("ec-085", "DA CIÊNCIA, TECNOLOGIA E INOVAÇÃO"),
    "DA FAMÍLIA, DA CRIANÇA, DO ADOLESCENTE E DO IDOSO": ("ec-065", "Da Família, da Criança, do Adolescente, do Jovem e do Idoso"),
    "DOS SERVIDORES PÚBLICOS MILITARES": ("ec-018", "DOS MILITARES DOS ESTADOS, DO DISTRITO FEDERAL E DOS TERRITÓRIOS"),
    "DA ADVOCACIA-GERAL DA UNIÃO": ("ec-019", "DA ADVOCACIA PÚBLICA"),
    "DA ADVOCACIA E DA DEFENSORIA PÚBLICA": ("ec-080", "Da Advocacia"),
}

# Court rulings that removed words, shown by Planalto as a struck expression linked to the case.
COURTS = {
    "stf-adi-7047": {
        "label": "STF, ADI 7047 (with ADI 7064)",
        "title": "Ação direta de inconstitucionalidade 7047: parcialmente procedente; interpretação conforme ao art. 100, "
                 "§ 11, para excluir a expressão \"com auto aplicabilidade para a União\" (redação da EC 113/2021)",
        "kind": "court",
        "enacted": "2023-11-30",
        "published": "2023-12-04",
        "url": "https://portal.stf.jus.br/processos/detalhe.asp?incidente=6318731",
        "from": "2023-12-04",
        "where": [("art-100", "§ 11")],
        "why": "STF judged ADI 7047 (with ADI 7064) in the virtual session of 30.11.2023 and excluded the expression "
               "'com auto aplicabilidade para a União' from art. 100 § 11 (EC 113/2021 wording); the minutes (ata de "
               "julgamento) were published in the DJE on 04.12.2023, the day the ruling binds all (STF portal, case "
               "tabs Decisões and Andamentos, cached). Planalto shows the expression struck, linked to the case.",
    },
}

# EC 126/2022 art. 9 revoked ADCT arts. 106, 107, 109, 110, 111, 111-A, 112 and 114 "após a sanção da lei
# complementar prevista no art. 6º": LC 200/2023, sanctioned 30.8.2023 and published in the DOU on 31.8.2023.
EC126_REVOKED = {"adct-art-106", "adct-art-107", "adct-art-109", "adct-art-110", "adct-art-111", "adct-art-111-a",
                 "adct-art-112", "adct-art-114"}
EC126_REVOKED_FROM = "2023-08-31"


def effect_override(law: str, p: dict, kind: str) -> str | None:
    if kind == "end" and law == "ec-126" and p["unit"] in EC126_REVOKED:
        return EC126_REVOKED_FROM
    hit = VIGENCIA_PROVISION.get((law, p["unit"], p["label"]))
    return hit[0] if hit and kind == "start" else None


def check_heading_renames() -> None:
    for old, (law, new) in HEADING_RENAMES.items():
        page = page_text("emc-" + str(int(law[3:]))).lower()
        if new.lower() not in page:
            raise SystemExit(f"heading rename {old!r} -> {new!r}: not in the text of {law}")


def split_court_strikes(paras: list[dict]) -> list[str]:
    """A paragraph with words struck by a court becomes two: the full wording until the ruling, the rest after."""
    out, problems = [], []
    where = {w: k for k, c in COURTS.items() for w in c["where"]}
    for p in paras:
        if p["state"] != "mixed":
            out.append(p)
            continue
        court = where.get((p["unit"], p["label"]))
        if not court:
            problems.append(f"partly struck paragraph with no explanation: {p['unit']} [{p['label']}] "
                            f"struck {p['struck_text']!r}")
            p["state"] = "plain"
            p["text"] = p["plain_text"]
            out.append(p)
            continue
        c = COURTS[court]
        full = dict(p, state="struck", force_end=(c["from"], court))
        cur = dict(p, state="plain", text=p["plain_text"], force_start=(c["from"], court))
        out += [full, cur]
    paras[:] = out
    return problems




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
    """Set start/end (and their laws) on every paragraph; return problems found.

    Each rule that dates a paragraph records how in p["end_how"] / p["start_how"], so counts can be reported.
    """
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
            if START_KIND.search(n):
                d = effect_override(law, p, "start") or eff[law]
                starts.append((d, law))
                if re.search(r"Renumerad", n, re.I):
                    p["renum_from"] = (renum_label(n), d, law)
            elif END_KIND.search(n):
                d = effect_override(law, p, "end") or eff[law]
                ends.append((d, law))
        p["start"], p["start_law"] = max(starts) if starts else (CF_DATE, None)
        p["start_how"] = "note" if starts else "original"
        p["end"], p["end_law"], p["end_how"] = (None, None, None)
        if p["state"] != "plain" and ends:
            p["end"], p["end_law"], p["end_how"] = (*min(ends), "note")
        elif p["state"] == "plain" and ends and not starts:
            # an unstruck "(Revogado)" placeholder: it starts when the repeal took effect
            p["start"], p["start_law"] = max(ends)
            p["start_how"] = "note"
        if p.get("force_start"):
            p["start"], p["start_law"] = p["force_start"]
            p["start_how"] = "court"
        if p.get("force_end"):
            p["end"], p["end_law"], p["end_how"] = (*p["force_end"], "court")

    # headings renamed by an amendment that Planalto shows without a note (HEADING_RENAMES, checked against the
    # amendment's own text)
    for i, p in enumerate(paras):
        if not (p.get("heading") and p["state"] == "struck" and p["text"] in HEADING_RENAMES):
            continue
        law, new = HEADING_RENAMES[p["text"]]
        q = next((q for q in paras[i + 1:i + 4] if q.get("heading") and q["state"] == "plain" and q["text"] == new), None)
        if q is None:
            problems.append(f"heading rename target not found after {p['text']!r}")
            continue
        p["end"], p["end_law"], p["end_how"] = eff[law], law, "heading-rename"
        q["start"], q["start_law"], q["start_how"] = eff[law], law, "heading-rename"

    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["end"]:
            continue
        # a struck copy of text that is still shown unstruck later in the same unit, dated no later: Planalto keeps
        # the old copy beside a renumbered or re-marked block; it adds nothing, so it is never shown
        for q in paras[i + 1:]:
            if q["unit"] != p["unit"]:
                break
            if q["text"].casefold() == p["text"].casefold() and q["start"] <= p["start"] and q["state"] == "plain":
                p["end"], p["end_law"], p["end_how"] = p["start"], None, "duplicate"
                break
        if p["end"]:
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
            same = (q["label"] == p["label"] or (q["renum_from"] and q["renum_from"][0] == p["label"])
                    or (p["label"] == "Parágrafo único" and q["label"] == "§ 1º"))
            if same and q["start"] > p["start"]:
                p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "successor"
                break
        if not p["end"] and p["label"] == "Parágrafo único":
            # "Parágrafo único" shown struck before an unannotated "§ 1º": it became § 1º when an amendment added
            # § 2º to the article (the § 2º carries the source's own "Incluído pela" note)
            unit = [q for q in paras if q["unit"] == p["unit"]]
            s1 = next((q for q in unit[unit.index(p) + 1:] if q["label"] == "§ 1º" and q["state"] == "plain"
                       and q["start_how"] == "original"), None)
            s2 = sorted((q["start"], q["start_law"]) for q in unit
                        if q["label"] == "§ 2º" and q["start"] > p["start"] and q["start_law"])
            if s1 is not None and s2:
                d, law = s2[0]
                p["end"], p["end_law"], p["end_how"] = d, law, "renumbered"
                s1["start"], s1["start_law"], s1["start_how"] = d, law, "renumbered"
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
    for p in paras:
        if p["end"] and p["end"] < p["start"]:
            problems.append(f"ends before it starts: {p['unit']} [{p['label']}] {p['start']} > {p['end']} {p['text'][:60]!r}")
            p["end"] = p["start"]
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


def public_key(k: str, laws: dict[str, dict]) -> str:
    """Law keys shared with the other Brazil parts (corpus.d/): ec-<n>-<year>, ecr-<n>-<year>."""
    m = re.match(r"(ec|ecr)-0*(\d+)$", k)
    if not m:
        return k
    return f"{m.group(1)}-{int(m.group(2))}-{laws[k]['enacted'][:4]}"


def unit_label(unit: str, lines: list[str]) -> tuple[str, str]:
    if unit == "preambulo":
        return "Preâmbulo", "preamble"
    if unit == "titulos":
        return "Títulos, capítulos e seções", "heading"
    if unit == "adct-titulos":
        return "ADCT: títulos", "heading"
    lab = next((label_of(l) for l in lines if label_of(l).startswith("Art.")), unit)
    return (("ADCT " + lab) if unit.startswith("adct-") else lab), ("transitional" if unit.startswith("adct-") else "art")


def snapshot(paras: list[dict], day: str) -> dict[str, list[str]]:
    units: dict[str, list[str]] = {}
    for p in paras:
        if p["start"] <= day and (p["end"] is None or day < p["end"]):
            units.setdefault(p["unit"], []).append(p["text"])
    return units


def compilado_units() -> dict[str, list[str]]:
    b, _ = raw("cf-compilado")
    out: dict[str, list[str]] = {}
    for p in cf_paragraphs(decode(b)):
        if p["state"] == "struck":
            continue
        out.setdefault(p["unit"], []).append(p["plain_text"] if p["state"] == "mixed" else p["text"])
    return out


def build_cf(paras, laws, eff, src_url, src_bytes, docs_date):
    days = sorted({p["start"] for p in paras} | {p["end"] for p in paras if p["end"]})
    days = [d for d in days if d >= CF_DATE]
    versions, prev = [], None
    sha = hashlib.sha256(src_bytes).hexdigest()
    for day in days:
        snap = snapshot(paras, day)
        texts = {u: "".join(l + "\n" for l in ls) for u, ls in snap.items()}
        if prev is not None and texts == prev:
            continue
        units = {}
        for u in sorted(texts):
            lab, kind = unit_label(u, snap[u])
            units[u] = {"label": lab, "kind": kind, "text": texts[u]}
        credits = {}
        if prev is not None:
            for u in sorted(set(texts) | set(prev)):
                if texts.get(u) == prev.get(u):
                    continue
                who = {p["start_law"] for p in paras if p["unit"] == u and p["start"] == day and p["start_law"]}
                who |= {p["end_law"] for p in paras if p["unit"] == u and p["end"] == day and p["end_law"]}
                if who:
                    credits[u] = sorted(public_key(w, laws) for w in who)
        versions.append({"from": day, "source_url": src_url, "sha256": sha, "units": units, "credits": credits})
        prev = texts
    return versions


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--retrieved", default="2026-10-28")
    a = ap.parse_args(argv)
    laws = amendments()
    eff, vdec = vigencia(laws)
    b, cf_src = raw("cf")
    paras = cf_paragraphs(decode(b))
    check_heading_renames()
    problems = split_court_strikes(paras)
    problems += lifespans(paras, eff, effect_override)
    if a.stats:
        from collections import Counter
        print("paragraphs", len(paras), Counter(p["state"] for p in paras))
        print("units", len({p["unit"] for p in paras}))
        print("start", Counter(p["start_how"] for p in paras), "end", Counter(p["end_how"] for p in paras))
        for x in problems:
            print("PROBLEM", x)
        print(len(problems), "problems")

    # check: today's replayed text against Planalto's consolidated page
    today = snapshot(paras, a.retrieved)
    comp = compilado_units()
    mism = []
    for u in sorted(set(today) | set(comp)):
        x, y = today.get(u, []), comp.get(u, [])
        if x != y:
            mism.append((u, x, y))
    print(f"check vs constituicaocompilado.htm: {len(mism)} units differ of {len(set(today) | set(comp))}")
    if a.stats:
        import difflib
        for u, x, y in mism[:40]:
            print("DIFF", u)
            for l in difflib.unified_diff(y, x, "compilado", "replay", n=0, lineterm=""):
                if not l.startswith(("---", "+++", "@@")):
                    print("   ", l[:200])

    versions = build_cf(paras, laws, eff, cf_src, b, a.retrieved)
    used = {c for v in versions for cs in v["credits"].values() for c in cs}
    out_laws = {"cf-1988": {
        "label": "Constituição Federal de 1988",
        "title": "Constituição da República Federativa do Brasil de 1988",
        "kind": "law", "enacted": CF_DATE, "published": CF_DATE, "url": CF_URL,
        "temporary_until": None, "restores": None, "note": None}}
    for k in sorted(laws):
        pk = public_key(k, laws)
        if pk in used:
            out_laws[pk] = {kk: vv for kk, vv in laws[k].items()}
    for k, c in COURTS.items():
        if k in used:
            out_laws[k] = {kk: c[kk] for kk in ("label", "title", "kind", "enacted", "published", "url")}
            out_laws[k].update({"temporary_until": None, "restores": None, "note": None})
    from collections import Counter
    hows = Counter(p["end_how"] for p in paras if p["end_how"])
    n_req = sum(1 for _ in (CACHE_LOG.open(encoding="utf-8") if CACHE_LOG.exists() else []))
    decisions = [
        "Planalto (www.planalto.gov.br) refuses non-browser clients, so every Planalto page is read from an Internet "
        "Archive raw capture (web.archive.org/web/<timestamp>id_/<Planalto URL>), byte-for-byte what Planalto served; "
        "the capture timestamps are pinned in tools/sources.json.",
        "The Constitution's history is rebuilt from Planalto's annotated page (constituicao.htm), which keeps every "
        "superseded wording struck through beside its replacement, each with the source's own note ('Redação dada "
        "pela', 'Incluído pela', 'Revogado pela', 'Renumerado'). Text with no note is the 1988 original.",
        "A paragraph starts on the in-force day of the amendment in its note; a struck paragraph ends on the in-force "
        "day of its 'Revogado pela' note, else when the next wording of the same dispositivo in the same article "
        f"starts. Counts of how struck paragraphs were ended: {dict(sorted(hows.items()))}.",
        "'parent': a struck paragraph with no note and no later wording is taken to have fallen with the nearest "
        "struck enclosing dispositivo (for example the items of an article revoked as a whole).",
        "'duplicate': Planalto sometimes keeps a struck copy of a block next to the same text unstruck (renumbered "
        "or re-marked); such a struck copy is never shown.",
        "'renumbered': a struck 'Parágrafo único' followed by an unannotated '§ 1º' became § 1º when an amendment "
        "added § 2º to the article; the date and credit are those of the § 2º's own 'Incluído pela' note.",
        "Heading renames that Planalto shows without a note are dated and credited by the amendment whose text "
        "renames them (checked at parse time): " + "; ".join(f"'{o}' -> '{n}' ({laws[l]['label']})"
                                                           for o, (l, n) in HEADING_RENAMES.items()) + ".",
        "EC 126/2022 art. 9 revoked ADCT arts. 106, 107, 109, 110, 111, 111-A, 112 and 114 'após a sanção da lei "
        "complementar prevista no art. 6º'; that is LC 200/2023, sanctioned 30.8.2023 and published 31.8.2023 "
        f"(Planalto lcp200.htm), so those revocations are dated {EC126_REVOKED_FROM}.",
        *[c["why"] for c in COURTS.values()],
        "'Vide ADI' notes are informational and change no text; only a ruling that Planalto shows as struck words "
        "is a court law here.",
        "Future text is not modelled: Planalto shows EC 132/2023's changes that take effect in 2027 and 2033 "
        "(art. 23) and EC 141/2026's change to art. 7 XV (in force two months after publication) only as 'Vide' "
        "notes beside the text now in force, so the future branch has no versions yet.",
        "Units: one file per article (art-NNN, ADCT adct-art-NNN), plus the preamble and one file each for the "
        "headings of the main text and of the ADCT (titulos, adct-titulos). Each paragraph or item is one line; "
        "notes are removed; the signatures are left out.",
        "Typesetting normalised once: NBSP to space, runs of spaces collapsed, curly quotes and en/em dashes to ASCII, "
        "'Art. 6o' / '§ 2.º' to 'Art. 6º' / '§ 2º', space before punctuation removed. Source typos are kept "
        "(for example 'III o acesso' without the dash).",
        *vdec,
    ]
    corpus = {
        "country": {
            "code": "BR", "name": "Brazil", "slug": "brazil", "lang": "pt", "tz": "America/Sao_Paulo",
            "future_branch": "futuro",
            "publisher": {"name": "Presidência da República, Planalto (Legislação)", "email": "legislacao@planalto.invalid"},
            "default_in_force_rule": {
                "text": "Decreto-Lei 4.657/1942 (LINDB) art. 1: 'Salvo disposição contrária, a lei começa a vigorar em "
                        "todo o país quarenta e cinco dias depois de oficialmente publicada'; the period is counted "
                        "under LC 95/1998 art. 8 § 1 (publication day and last day included, in force the day after).",
                "source": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm"},
            "licence_note": "Texto oficial: Presidência da República, Casa Civil (planalto.gov.br/legislacao). Atos "
                            "oficiais não são protegidos por direito autoral (Lei 9.610/1998, art. 8º, IV). Este texto "
                            "não substitui o publicado no Diário Oficial da União.",
        },
        "sources": [
            {"name": "Planalto, Legislação (via Internet Archive raw captures)",
             "url": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm",
             "retrieved": a.retrieved, "requests": n_req,
             "licence": "Official acts are not protected by copyright (Lei 9.610/1998 art. 8 IV).",
             "notes": "Live Planalto blocks non-browser clients; pages read from web.archive.org id_ captures pinned in "
                      "sources.json. Pages: constituicao.htm (annotated, struck history), constituicaocompilado.htm "
                      "(check), quadro_emc.htm (amendment dates), emcNN.htm and ecrN.htm (each amendment's vigência "
                      "clause and renames), lcp200.htm."},
            {"name": "Supremo Tribunal Federal, case pages", "url": "https://portal.stf.jus.br/",
             "retrieved": a.retrieved, "requests": 2, "licence": "Official acts (Lei 9.610/1998 art. 8 IV).",
             "notes": "ADI 7047: decisions and docket tabs, for the ruling and DJE ata dates."},
        ],
        "laws": out_laws,
        "acts": [{
            "slug": "constituicao",
            "short": "CF/88",
            "title": "Constituição da República Federativa do Brasil de 1988",
            "url": CF_URL,
            "first_law": "cf-1988",
            "earlier_laws": [],
            "versions": versions,
        }],
        "applies": [],
        "decisions": decisions,
        "ai_use": ["none: no model wrote, translated or summarised legal text; the parser and the hand tables "
                   "(vigência overrides, heading renames, court ruling) were written by an AI coding agent from the "
                   "cached official pages, and each hand entry is checked against those pages at parse time."],
    }
    if mism:
        corpus["decisions"].append(f"Check against constituicaocompilado.htm: {len(mism)} units differ; see PROGRESS.md.")
    tmp = HERE / "corpus.json.tmp"
    tmp.write_text(json.dumps(corpus, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, HERE / "corpus.json")
    print(f"corpus.json: {len(versions)} CF versions, {len(out_laws)} laws, {len(problems)} problems")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
