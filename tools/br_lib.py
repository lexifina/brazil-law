"""Shared helpers for the Brazilian state builds (no network): HTML to lines, lines to one unit per Artigo, part files.

Each state folder keeps its own copy (the builder ships a folder's scripts in the repository's tools/ so the repository
can rebuild itself).
"""
import hashlib, html, json, os, re
from pathlib import Path

SPACES = re.compile('[  -   　]')


def norm(s):
    s = SPACES.sub(' ', s).replace('​', '').replace('﻿', '').replace('­', '')
    s = s.replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace('‒', '-').replace('‑', '-')
    return re.sub(r'\s+', ' ', s).strip()


def ld(s):
    return ''.join(ch for ch in s if ch.isalnum())


def sha(b):
    return hashlib.sha256(b).hexdigest()


def lines_of(s):
    """HTML fragment -> [(kind, text)]; kind 'h1'..'h6' for heading elements, 'p' otherwise."""
    s = re.sub(r'(?is)<script.*?</script>|<style.*?</style>|<!--.*?-->|<head\b.*?</head>', '', s)
    out = []
    for m in re.finditer(r'(?is)<(h[1-6])\b[^>]*>(.*?)</\1>|((?:(?!<h[1-6]\b).)+)', s):
        if m.group(1):
            kind, chunk = 'h' + m.group(1)[1], m.group(2)
        else:
            kind, chunk = 'p', m.group(3)
        chunk = re.sub(r'\s+', ' ', chunk)  # line breaks in the HTML source are not paragraph breaks
        chunk = re.sub(r'(?is)</t[dh]>', ' | ', chunk)
        chunk = re.sub(r'(?is)<br\s*/?>|</?(p|div|tr|li|table|tbody|thead|ul|ol|center|blockquote)\b[^>]*>', '\n', chunk)
        chunk = html.unescape(re.sub(r'<[^>]+>', '', chunk))
        for l in chunk.split('\n'):
            l = norm(l).strip(' |').strip()
            if l and re.search(r'\w', l):
                out.append((kind, l))
    return out


ART = re.compile(r'^(Artigo|Art\.?)\s*(\d+)\s*(?:[º°ºo]|\.)?(?:\s*-\s*([A-Z])(?=\s*[-.–]|\s*$)|-?([A-Z])(?=\s*[-.–]))?')
HEAD = re.compile(r'^(?:(?:T[ÍI]TULO|CAP[ÍI]TULO|SE[ÇC][ÃA]O|SUBSE[ÇC][ÃA]O|LIVRO|PARTE)\s+(?:[IVXLCDM]+|\d+|[ÚU]NIC[OA])\b'
                  r'|(?:T[íi]tulo|Cap[íi]tulo|Se[çc][ãa]o|Subse[çc][ãa]o|Livro)\s+(?:[IVXLCDM]+|\d+|[ÚU]nic[oa])\b'
                  r'|ATO DAS DISPOSI|(?:DAS )?DISPOSI[ÇC][ÕO]ES (?:GERAIS|FINAIS|TRANSIT|PRELIMINARES|CONSTITUCIONAIS))')
ADT = re.compile(r'DISPOSI[ÇC][ÕO]ES\s+(CONSTITUCIONAIS\s+)?TRANSIT[ÓO]RIAS', re.I)


def units_of(lines, title_label='Título', adt=True):
    """One unit per Artigo (keys art-0001, art-0001-a; after an "Ato das Disposições ... Transitórias" heading,
    adt-0001). Headings stand above the first article under them ("## "). Lines before the first article form
    000-titulo. An article number lower than the one before (a quoted provision) does not start a new unit."""
    units, order = {}, []
    titel, cur, pending, prefix, last = [], None, [], 'art', None

    def start(key, label, first):
        nonlocal cur
        k, n = key, 2
        while k in units:
            k = f'{key}-dup{n}'
            n += 1
        units[k] = {'label': label, 'lines': [f'## {p}' for p in pending] + [first]}
        order.append(k)
        cur = k

    for kind, l in lines:
        m = ART.match(l)
        heading = (kind in ('h2', 'h3', 'h4', 'h5') and (cur is not None or pending)) or (HEAD.match(l) and not m)
        if m:
            num = int(m.group(2))
            suf = (m.group(3) or m.group(4) or '').lower()
            if last is None or prefix != last[0] or (num, suf) > (last[1], last[2]):
                key = f'{prefix}-{num:04d}' + (f'-{suf}' if suf else '')
                label = ('ADT ' if prefix == 'adt' else '') + l[:m.end()].rstrip(' -.–')
                start(key, label, l)
                pending, last = [], (prefix, num, suf)
                continue
        if heading:
            if adt and ADT.search(l):
                prefix, last = 'adt', None
            pending.append(l)
            continue
        if pending:
            pending.append(l)
        elif cur is None:
            titel.append(('# ' if not titel else '') + l)
        else:
            units[cur]['lines'].append(l)
    if pending:
        (units[cur]['lines'] if cur else titel).extend(pending)
    out = {}
    if titel:
        out['000-titulo'] = {'label': title_label, 'kind': 'title', 'text': '\n'.join(titel) + '\n'}
    for k in order:
        out[k] = {'label': units[k]['label'], 'kind': 'article', 'text': '\n'.join(units[k]['lines']) + '\n'}
    return out


DATE = re.compile(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b')
MONTHS = {m: i + 1 for i, m in enumerate(['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto',
                                           'setembro', 'outubro', 'novembro', 'dezembro'])}
LONG = re.compile(r'\b(\d{1,2})[º°]?\s+de\s+(' + '|'.join(MONTHS) + r')\s+de\s+(\d{4})', re.I)


def dates_in(s):
    out = [f'{int(y):04d}-{int(mo):02d}-{int(d):02d}' for d, mo, y in DATE.findall(s) if 1 <= int(mo) <= 12 and 1 <= int(d) <= 31]
    out += [f'{int(y):04d}-{MONTHS[mo.lower()]:02d}-{int(d):02d}' for d, mo, y in LONG.findall(s)]
    return out


def write_part(out_dir, name, c):
    out_dir = Path(out_dir)
    out_dir.mkdir(exist_ok=True)
    p = out_dir / f'{name}.json'
    s = json.dumps(c, ensure_ascii=False, indent=1) + '\n'
    if p.exists() and p.read_text(encoding='utf-8') == s:
        return p
    tmp = p.with_suffix('.tmp')
    tmp.write_text(s, encoding='utf-8', newline='\n')
    os.replace(tmp, p)
    return p


def letters_check(versions, page_text):
    """versions: [(name, units, source_text)]: each unit found in order in the source's letters and digits, and
    nothing left over. Returns a list of mismatch lines."""
    bad = []
    for name, units, src_text in versions:
        src = ld(src_text)
        rest = {k: ld(re.sub(r'(?m)^#+ ', '', u['text'])) for k, u in units.items()}
        pos = 0
        while rest:
            hit = None
            for k, t in rest.items():
                if t and src.startswith(t, pos) and (hit is None or len(t) > len(rest[hit])):
                    hit = k
            if hit is None:
                break
            pos += len(rest.pop(hit))
        if rest or pos != len(src):
            bad.append(f'MISMATCH {name}: matched {pos}/{len(src)}; next source: {src[pos:pos + 80]!r}; '
                       f'unplaced: {list(rest)[:5]}')
    return bad
