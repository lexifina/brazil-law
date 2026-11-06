"""Builds corpus.d/30-leis-NNN parts for the Município de Caicó from the Câmara Municipal's SAPL records of its laws
and their PDFs (no network).

    python -X utf8 laws.py --today YYYY-MM-DD [--part-size 50]

The records ("Lei" and "Lei Complementar") are read newest first, as SAPL lists them, from the saved API answers;
each record's texto_integral PDF is read with PyMuPDF. A law goes in as enacted, credited to itself and dated by the
publication date SAPL records for it (else by its date), when:
- the PDF has a text layer of its own (scans, with or without an OCR layer, are left out);
- its heading ("LEI Nº ...", "LEI COMPLEMENTAR Nº ...") carries the record's number;
- it has articles, and a closing line ending in its date written out after the last article;
- its text carries no alteration notes ("Redação dada pela ...", "Revogado pela ...");
- its own vigência clause says it takes effect on its publication (or its signature, promulgation or sanction).
The text runs from the heading to the closing line that ends in the date; lines repeated at the top or bottom of two or more pages
(letterheads, footers) and page numbers are left out. Lines are joined into paragraphs: a new paragraph at a provision
label, a heading line, or after a line ending in ".", ";" or ":".
Parts already published (<part>.PUBLISH) never change; later records go into new parts.
"""
import argparse, json, re, sys
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from br_lib import units_of, write_part, sha, norm  # noqa: E402

CONFIG = {"host": "sapl.caico.rn.leg.br", "city": "Caicó", "code": "BR-RN-CAICO", "slug": "brazil-caico-city", "tz": "America/Fortaleza", "email_domain": "caico.rn.leg.br"}
BASE = 'https://' + CONFIG['host']
RAW = HERE / '.cache' / 'sapl' / 'raw'
INDEX = HERE / '.cache' / 'sapl' / 'laws-index.json'
REGISTRY = HERE / 'laws-parts.json'
MONTHS = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro',
          'novembro', 'dezembro']
LONG = re.compile(r'\b(\d{1,2})\s*[º°o]?\s+de\s+(' + '|'.join(MONTHS) + r')\s+de\s+(\d{4})', re.I)
CLOSING = re.compile(LONG.pattern + r'\s*\.?\s*$', re.I)
HEAD = re.compile(r'^L\s?E\s?I\s+(COMPLEMENTAR\s+)?(?:ORDIN[ÁA]RIA\s+)?(?:MUNICIPAL\s+)?(?:N[º°ºo.]*|N[ÚU]MERO)\s*[:.]?\s*([\d.]+)', re.I)
ART = re.compile(r'^Art(?:igo)?\.?\s*\d')
STARTS = re.compile(r'^(?:Art\.|Art\s+\d|Artigo\s+\d|§|Par[áa]grafo|[IVXLC]+\s*[-–.)]|[a-z]\)|T[ÍI]TULO|CAP[ÍI]TULO|'
                    r'Se[c]?[çc][ãa]o|SE[C]?[ÇC][ÃA]O|Subse[c]?[çc][ãa]o|SUBSE[C]?[ÇC][ÃA]O)')
HEADING = re.compile(r'^(?:T[ÍI]TULO|CAP[ÍI]TULO|SE[C]?[ÇC][ÃA]O|Se[c]?[çc][ãa]o|Subse[c]?[çc][ãa]o|SUBSE[C]?[ÇC][ÃA]O)'
                     r'\s+(?:[IVXLC]+|[ÚU]NIC[OA])\b')
PAGENO = re.compile(r'^(?:P[áa]g(?:ina)?\.?\s*)?\d{1,3}(?:\s*(?:/|de)\s*\d{1,3})?$', re.I)
ALTER = re.compile(r'\((?:\s*)(?:Reda[çc][ãa]o\s+dada|Acrescentad|Acrescid|Revogad|Inclu[íi]d|Suprimid|Renumerad|'
                   r'Alterad|Vide\s)', re.I)
OCR = re.compile(r'(?i)abbyy|finereader|paper capture|ocr|tesseract|omnipage|scansoft|readiris|scan')
VIG = re.compile(r'(?i)entr(?:a|ar[áa])\s+em\s+vigor[^.;]*')
VIG_OK = re.compile(r'(?i)(?:data|dia|ato)\s+d[ae]\s+(?:sua\s+)?(?:publica[çc][ãa]o|assinatura|promulga[çc][ãa]o|'
                    r'san[çc][ãa]o)|a\s+partir\s+d[ae]\s+(?:sua\s+|da\s+)?(?:data\s+d[ae]\s+(?:sua\s+)?)?'
                    r'(?:publica[çc][ãa]o|assinatura|promulga[çc][ãa]o|san[çc][ãa]o)')
VIG_OTHER = re.compile(r'(?i)dias|m[êe]s|meses|ano\b|exerc[íi]cio|' + '|'.join(MONTHS) + r'|\d{1,2}/\d{1,2}/\d{2,4}')

COUNTRY = {
    'code': CONFIG['code'], 'name': CONFIG['city'], 'slug': CONFIG['slug'], 'lang': 'pt', 'tz': CONFIG['tz'],
    'future_branch': 'futuro',
    'publisher': {'name': f"Câmara Municipal de {CONFIG['city']} (SAPL)", 'email': f"sapl@{CONFIG['email_domain']}.invalid"},
    'default_in_force_rule': {
        'text': 'Decreto-Lei 4.657/1942 (LINDB) art. 1: unless it says otherwise, a law takes effect 45 days after its '
                'official publication. This record takes in only municipal laws whose own vigência clause says they '
                'take effect on their publication (or signature), and dates each by the publication date the '
                "Câmara's SAPL records for it (else by its date).",
        'source': 'https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm'},
    'licence_note': f"Texts: Câmara Municipal de {CONFIG['city']}, SAPL (Sistema de Apoio ao Processo Legislativo), "
                    f"{CONFIG['host']}; SAPL: \"Conteúdo e dados sob licença Creative Commons 4.0 Atribuir Fonte - "
                    'Compartilhar Igual". Lei 9.610/1998 art. 8 IV: the texts of laws and other official acts are not '
                    'protected by copyright. Non-official text: only the official gazette is authoritative.',
}
DECISIONS = [
    'Each municipal law ("Lei" and "Lei Complementar") is given as enacted, from the PDF the Câmara\'s SAPL holds for '
    'it, credited to the law itself and dated by the publication date SAPL records for it (else by the law\'s own '
    'date). Later amendments by other laws are not worked into earlier laws: each law is its own file set as enacted. '
    'Laws are taken newest first, in parts.',
    'Left out: scans (with or without an OCR layer), PDFs whose heading does not carry the record\'s number, texts '
    'with no article or no closing date line, texts carrying alteration notes, and laws whose vigência clause sets '
    'another day than their publication (or that have none, so that the 45 days of the LINDB apply).',
    'The text runs from the law\'s heading to its closing date line (signatures after it are left out); lines '
    'repeated at the top or bottom of two or more pages (letterheads, footers) and page numbers are left out. Lines '
    'are joined into paragraphs: a new paragraph starts at a provision label, a heading line, or after a line ending '
    'in ".", ";" or ":". One file per Art.; "000-titulo" holds what comes before the first article.',
]
AI = ["Claude Code (claude-opus-5-5) wrote Lexifina's code and chose the sources. No model output is used as legal "
      "text or dates: every word comes from the Câmara's SAPL."]


def file_url(r):
    u = r.get('texto_integral') or ''
    if u and not u.startswith('http'):
        u = BASE + u
    return u.replace('http://', 'https://', 1)


def gone(url):
    """sapl-runner (11-05): the file is not served: a remembered 404/410, or 3 time-outs (<raw>.skip)."""
    p = RAW / sha(url.encode())
    return Path(str(p) + '.404').exists() or Path(str(p) + '.skip').exists()


def furniture(pages):
    """Normalised lines (digits as #) seen among the first or last 4 lines of two or more pages."""
    seen = {}
    for ls in pages:
        for l in set(ls[:4] + ls[-4:]):
            k = re.sub(r'\d', '#', l)
            seen[k] = seen.get(k, 0) + 1
    return {k for k, n in seen.items() if n >= 2} if len(pages) >= 2 else set()


def pdf_lines(path):
    d = pymupdf.open(str(path))
    meta = ' '.join(str(v or '') for v in (d.metadata or {}).values())
    if OCR.search(meta):
        return None, 'scan with an OCR layer (producer)'
    pages, chars = [], 0
    for pg in d:
        t = pg.get_text()
        chars += len(re.sub(r'\W', '', t))
        area = abs(pg.rect)
        for img in pg.get_image_info():
            b = pymupdf.Rect(img['bbox']) & pg.rect
            if area and abs(b) > 0.6 * area and t.strip():
                return None, 'scan with an OCR layer (page image)'
        pages.append([l for l in (norm(x) for x in t.split('\n')) if l])
    if chars < 150 * d.page_count:
        return None, 'scan (no text layer)'
    fur = furniture(pages)
    lines = [l for ls in pages for l in ls if re.sub(r'\d', '#', l) not in fur and not PAGENO.match(l)]
    return lines, 'ok'


def paragraphs(lines):
    paras = []
    for l in lines:
        head = bool(HEADING.match(l))
        prev = paras[-1] if paras else None
        if prev is not None and re.fullmatch(r'Art\.?', prev[1]):
            prev[1] += ' ' + l
            continue
        if prev is None or STARTS.match(l) or head or re.search(r'[.;:]["”]?$', prev[1]):
            paras.append([head, l])
        elif prev[1].endswith('-') and not prev[1].endswith(' -'):
            prev[1] += l
        else:
            prev[1] += ' ' + l
    return [('h2' if h else 'p', norm(t)) for h, t in paras]


def number(r):
    s = str(r.get('numero') or '').strip()
    return int(s.replace('.', '')) if re.fullmatch(r'\d[\d.]*', s) else None


def law_act(r, kind, today):
    url = file_url(r)
    if not url:
        return None, {}, 'no file in SAPL'
    p = RAW / sha(url.encode())
    if not p.exists():
        return None, {}, 'file not served (404 or repeated time-outs)' if gone(url) else 'not fetched'
    b = p.read_bytes()
    if b[:5] != b'%PDF-':
        return None, {}, 'not a PDF'
    n = number(r)
    if n is None or not r.get('data'):
        return None, {}, 'odd number or no date'
    try:
        lines, why = pdf_lines(p)
    except Exception as e:
        return None, {}, f'unreadable ({type(e).__name__})'
    if lines is None:
        return None, {}, why
    start = next((i for i, l in enumerate(lines) if (m := HEAD.match(l)) and int(m.group(2).replace('.', '') or -1) == n
                  and bool(m.group(1)) == (kind == 'lc')), None)
    if start is None:
        return None, {}, 'no heading with the record number'
    arts = [i for i, l in enumerate(lines) if i > start and ART.match(l)]
    if not arts:
        return None, {}, 'no article'
    end = next((i for i in range(arts[-1], len(lines)) if CLOSING.search(lines[i])), None)
    if end is None:
        return None, {}, 'no closing date line'
    body = lines[start:end + 1]
    text = ' '.join(body)
    if ALTER.search(text):
        return None, {}, 'alteration notes in the text'
    vig = VIG.findall(text)
    if not vig:
        return None, {}, 'no vigência clause'
    if not all(VIG_OK.search(v) and not VIG_OTHER.search(v) for v in vig):
        return None, {}, 'takes effect on another day'
    enacted, published = r['data'], r.get('data_publicacao')
    if published and (published < enacted or int(published[:4]) - int(enacted[:4]) > 1):
        return None, {}, 'publication date out of range'
    since = published or enacted
    if since > today:
        return None, {}, 'in force after today'
    units = units_of(paragraphs(body), adt=False)
    if not any(k.startswith('art-') for k in units):
        return None, {}, 'no article'
    y = enacted[:4]
    key = f'{"lc" if kind == "lc" else "lei"}-{y}-{n:05d}'
    word = 'Lei Complementar' if kind == 'lc' else 'Lei'
    label = f'{word} nº {n:,}'.replace(',', '.') + f', de {int(enacted[8:10])} de {MONTHS[int(enacted[5:7]) - 1]} de {y}'
    ementa = norm(r.get('ementa') or '')
    page = f'{BASE}/norma/{r["id"]}'
    laws = {key: {'label': label, 'title': ementa or label, 'kind': 'law', 'enacted': enacted, 'published': published,
                  'url': page, 'temporary_until': None, 'restores': None, 'note': None}}
    v = {'from': since, 'source_url': url, 'sha256': sha(b), 'units': units,
         'note': f'As enacted, from the PDF the Câmara\'s SAPL holds for {label}; dated by '
                 + ('its publication date in SAPL.' if published else 'its date (SAPL records no publication date).')}
    act = {'slug': key, 'short': f'{"LC" if kind == "lc" else "Lei"} {n}/{y}', 'title': label, 'url': page,
           'first_law': key, 'earlier_laws': [], 'versions': [v]}
    return act, laws, 'ok'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--today', required=True)
    ap.add_argument('--part-size', type=int, default=50)
    a = ap.parse_args()
    if not INDEX.exists():
        print('no law index yet')
        return
    idx = json.loads(INDEX.read_text(encoding='utf-8'))
    if not idx['types'] or not idx['records']:
        print('SAPL lists no laws of the Lei / Lei Complementar types')
        return
    kinds = {idx['types'][0]: 'lei'}
    if len(idx['types']) > 1:
        kinds[idx['types'][1]] = 'lc'
    reg = json.loads(REGISTRY.read_text(encoding='utf-8')) if REGISTRY.exists() else {}
    xp = HERE / 'letters-excluded.json'
    excluded = set(json.loads(xp.read_text(encoding='utf-8'))) if xp.exists() else set()
    done = {i for name, ids in reg.items() if (HERE / 'corpus.d' / f'{name}.PUBLISH').exists()
            or (HERE / 'corpus.d' / f'{name}.EMPTY').exists() for i in ids}
    published_keys = set()
    for name in reg:
        q = HERE / 'corpus.d' / f'{name}.json'
        if (HERE / 'corpus.d' / f'{name}.PUBLISH').exists() and q.exists():
            published_keys |= {x['slug'] for x in json.loads(q.read_text(encoding='utf-8'))['acts']}
    for name in [k for k in reg if not (HERE / 'corpus.d' / f'{k}.PUBLISH').exists()
                 and not (HERE / 'corpus.d' / f'{k}.EMPTY').exists()]:
        reg.pop(name)
        (HERE / 'corpus.d' / f'{name}.json').unlink(missing_ok=True)
    rest = [r for r in idx['records'] if r['id'] not in done]
    if any(file_url(r) and not (RAW / sha(file_url(r).encode())).exists() and not gone(file_url(r)) for r in rest):
        print('not every file fetched yet: no part written')
        return
    n0 = max([int(k.rsplit('-', 1)[1]) for k in reg] or [0])
    left = json.loads((HERE / 'left-out.json').read_text(encoding='utf-8')) if (HERE / 'left-out.json').exists() else {}
    why = {}
    for i in range(0, len(rest), a.part_size):
        chunk = rest[i:i + a.part_size]
        acts, laws = [], {}
        for r in chunk:
            act, l, w = law_act(r, kinds.get(r['tipo'], 'lei'), a.today)
            if w == 'ok' and act['slug'] in excluded:
                w = 'the second PDF reader reads it differently'
            if w == 'ok' and (act['slug'] in published_keys or act['slug'] in laws):
                w = 'duplicate'
            why[w] = why.get(w, 0) + 1
            if w != 'ok':
                left[str(r['id'])] = f'{r.get("__str__")}: {w}'
                continue
            left.pop(str(r['id']), None)
            acts.append(act)
            laws.update(l)
        name = f'30-leis-{n0 + i // a.part_size + 1:03d}'
        reg[name] = [r['id'] for r in chunk]
        if not acts:  # sapl-runner (11-05): an empty window is final (every file fetched or not served)
            (HERE / 'corpus.d' / f'{name}.EMPTY').write_text(json.dumps(reg[name]) + '\n', encoding='utf-8',
                                                               newline='\n')
            continue  # nothing usable in this window: the registry still records it, no part file
        c = {'country': COUNTRY,
             'sources': [{'name': f"Câmara Municipal de {CONFIG['city']}, SAPL: records of the municipal laws and "
                                  f'their PDFs (newest first)', 'url': BASE + '/norma/pesquisar', 'retrieved': a.today,
                          'licence': COUNTRY['licence_note'], 'notes': f'{len(acts)} acts in this part.'}],
             'laws': laws, 'acts': acts, 'applies': [], 'decisions': DECISIONS, 'ai_use': AI}
        print(write_part(HERE / 'corpus.d', name, c), len(acts), 'acts of', len(chunk), 'records')
    REGISTRY.write_text(json.dumps(reg, indent=0) + '\n', encoding='utf-8', newline='\n')
    (HERE / 'left-out.json').write_text(json.dumps(left, indent=0, ensure_ascii=False) + '\n', encoding='utf-8',
                                        newline='\n')
    print(why)


if __name__ == '__main__':
    main()
