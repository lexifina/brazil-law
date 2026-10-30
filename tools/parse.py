"""Builds corpus.d parts for São Paulo from the retrieved ALESP pages (no network).

    python -X utf8 parse.py [--only constituicao|lc] [--part-size 50] [--today YYYY-MM-DD]

Each act gets up to two versions:
1. the text as enacted (ALESP "texto original"), credited to the act itself;
2. the text in force (ALESP "texto com alterações" with the struck-through earlier wordings and the portal's
   alteration notes left out), credited to the ALESP consolidation, when it differs from the first.
The pages and their sha256s are named in each version.
"""
import argparse, hashlib, html, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / '.cache'
OUT = HERE / 'corpus.d'

SPACES = re.compile('[  -   　]')


def norm(s):
    s = SPACES.sub(' ', s).replace('​', '').replace('﻿', '').replace('­', '')
    s = s.replace('‘', "'").replace('’', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace('‒', '-').replace('‑', '-')
    return re.sub(r'\s+', ' ', s).strip()


def raw(url):
    p = CACHE / 'raw' / hashlib.sha256(url.encode()).hexdigest()
    return p.read_bytes() if p.exists() else None


def is_note(inner):
    """An ALESP alteration note: a paragraph whose words are all in <em> and start with '-'."""
    outside = re.sub(r'(?s)<em>.*?</em>', '', inner)
    if re.sub(r'<[^>]+>|&nbsp;|[\s.;,]', '', outside):
        return False
    t = norm(html.unescape(re.sub(r'<[^>]+>', ' ', inner)))
    return t.startswith('-')


def body(s, current):
    s = s[s.index('<h1'):] if '<h1' in s else s[s.index('<body'):]
    s = s[:s.rindex('</body>')] if '</body>' in s else s
    s = re.sub(r'(?s)<script.*?</script>|<style.*?</style>|<!--.*?-->', '', s)
    s = re.sub(r'(?is)</?observacao>', '', s)
    s = re.sub(r'(?is)<(s|strike|del)\b[^>]*>.*?</\1>', '', s)  # earlier wordings, struck through by the portal
    if current:
        s = re.sub(r'(?is)<p\b[^>]*>(.*?)</p>', lambda m: '' if is_note(m.group(1)) else m.group(0), s)
    return s


def lines_of(s):
    """HTML body -> [(kind, text)], kind 'h' for heading lines (h1-h4), 'p' otherwise."""
    out = []
    for m in re.finditer(r'(?is)<(h[1-6])\b[^>]*>(.*?)</\1>|((?:(?!<h[1-6]\b).)+)', s):
        if m.group(1):
            kind, chunk = 'h' + m.group(1)[1], m.group(2)
        else:
            kind, chunk = 'p', m.group(3)
        chunk = re.sub(r'(?is)</t[dh]>', ' | ', chunk)
        chunk = re.sub(r'(?is)<br\s*/?>|</?(p|div|tr|li|table|tbody|ul|ol)\b[^>]*>', '\n', chunk)
        chunk = html.unescape(re.sub(r'<[^>]+>', '', chunk))
        for l in chunk.split('\n'):
            l = norm(l).strip(' |').strip()
            if l and re.search(r'\w', l):
                out.append((kind, l))
    return out


ART = re.compile(r'^(Artigo|Art\.?)\s*(\d+)\s*(?:[º°o]|\.)?(?:\s*-\s*([A-Z])(?=\s*[-.]|\s*$)|-?([A-Z])(?=\s*[-.]))?')
HEAD = re.compile(r'^(?:(?:T[ÍI]TULO|CAP[ÍI]TULO|SE[ÇC][ÃA]O|SUBSE[ÇC][ÃA]O|LIVRO|PARTE)\s+(?:[IVXLCDM]+|\d+|[ÚU]NIC[OA])\b'
                  r'|(?:T[íi]tulo|Cap[íi]tulo|Se[çc][ãa]o|Subse[çc][ãa]o|Livro)\s+(?:[IVXLCDM]+|\d+|[ÚU]nic[oa])\b'
                  r'|ATO DAS DISPOSI|(?:DAS )?DISPOSI[ÇC][ÕO]ES (?:GERAIS|FINAIS|TRANSIT|PRELIMINARES|CONSTITUCIONAIS))')
ADT = re.compile(r'DISPOSI[ÇC][ÕO]ES\s+(CONSTITUCIONAIS\s+)?TRANSIT[ÓO]RIAS', re.I)


def units_of(lines):
    units = {}
    titel, cur, pending, prefix, last = [], None, [], 'art', None
    order = []

    def start(key, label, first):
        nonlocal cur
        k, n = key, 2
        while k in units:
            k = f'{key}-dup{n}'
            n += 1
        units[k] = {'label': label, 'kind': 'article', 'lines': [f'## {p}' for p in pending] + [first]}
        order.append(k)
        cur = k

    for kind, l in lines:
        if kind == 'h1' and l.startswith('(') and 'atualiza' in l.lower():
            continue  # the portal's "last updated" line: metadata, not text
        m = ART.match(l)
        heading = (kind in ('h2', 'h3', 'h4') and (cur is not None or pending)) or (HEAD.match(l) and not m)
        if m:
            num = int(m.group(2))
            suf = (m.group(3) or m.group(4) or '').lower()
            pos = (prefix, num, suf)
            if last is None or pos[0] != last[0] or (num, suf) > (last[1], last[2]):
                key = f'{prefix}-{num:04d}' + (f'-{suf}' if suf else '')
                label = ('ADT ' if prefix == 'adt' else '') + l[:m.end()].rstrip(' -.')
                start(key, label, l)
                pending, last = [], pos
                continue
        if heading:
            if ADT.search(l):
                prefix, last = 'adt', None
            pending.append(l)
            continue
        if pending:
            pending.append(l)
        elif cur is None:
            titel.append(('# ' if kind == 'h1' and not titel else '') + l)
        else:
            units[cur]['lines'].append(l)
    if pending:
        (units[cur]['lines'] if cur else titel).extend(pending)
    out = {}
    if titel:
        out['000-titulo'] = {'label': 'Título', 'kind': 'title', 'text': '\n'.join(titel) + '\n'}
    for k in order:
        u = units[k]
        out[k] = {'label': u['label'], 'kind': 'article', 'text': '\n'.join(u['lines']) + '\n'}
    return out


DATE = re.compile(r'\b(\d{2})/(\d{2})/(\d{4})\b')


def iso(d):
    m = DATE.search(d or '')
    return f'{m.group(3)}-{m.group(2)}-{m.group(1)}' if m else None


def note_dates(s):
    """Dates of the acts the portal cites in its alteration notes (struck or not) and its 'last updated' line."""
    ds = []
    for m in re.finditer(r'(?is)<p\b[^>]*>(.*?)</p>|<h1\b[^>]*>(.*?)</h1>', s):
        inner = m.group(1) or m.group(2) or ''
        plain = re.sub(r'(?is)</?(s|strike|del)\b[^>]*>', '', inner)
        if (m.group(1) and is_note(plain)) or (m.group(2) and 'atualiza' in inner.lower()):
            ds += [f'{y}-{mo}-{d}' for d, mo, y in DATE.findall(html.unescape(re.sub(r'<[^>]+>', ' ', plain)))]
    return sorted(ds)


def slug_of(rec):
    t = rec['tipo']
    n = re.sub(r'\D', '', rec['nuNorma'] or '0')
    y = iso(rec['data'])[:4]
    return {'Constituição': 'constituicao', 'Lei Complementar': f'lc-{y}-{int(n):04d}', 'Lei': f'lei-{y}-{int(n):05d}',
            'Emenda Constitucional': f'ec-{y}-{int(n):03d}'}[t]


def short_of(rec):
    t = rec['tipo']
    if t == 'Constituição':
        return 'CE-SP'
    return {'Lei Complementar': 'LC', 'Lei': 'Lei'}[t] + f" {rec['nuNorma']}/{iso(rec['data'])[:4]}"


COUNTRY = {
    'code': 'BR-SP', 'name': 'São Paulo', 'slug': 'brazil-sao-paulo', 'lang': 'pt', 'tz': 'America/Sao_Paulo',
    'future_branch': 'futuro',
    'publisher': {'name': 'Assembleia Legislativa do Estado de São Paulo (ALESP)', 'email': 'alesp@al.sp.gov.br.invalid'},
    'default_in_force_rule': {
        'text': 'Decreto-Lei 4.657/1942 (LINDB) art. 1: unless it says otherwise, a law takes effect 45 days after its '
                'official publication. São Paulo laws almost always say "Esta lei entra em vigor na data de sua '
                'publicação"; this record dates each act as enacted by its publication in the Diário Oficial (the '
                'Constituição by its promulgation).',
        'source': 'https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm'},
    'licence_note': 'Texts: Assembleia Legislativa do Estado de São Paulo (ALESP), Legislação Estadual, '
                    'www.al.sp.gov.br. Lei 9.610/1998 art. 8 IV: the texts of laws and other official acts are not '
                    'protected by copyright. Non-official text: only the Diário Oficial do Estado is authoritative.',
}
DECISIONS = [
    'An act the portal shows no alteration for is given as enacted (ALESP "texto original"), credited to the act itself '
    'and dated by its publication in the Diário Oficial. An altered act is given only as the text in force (ALESP '
    '"texto com alterações"), credited to ALESP as the oldest version available and dated by the latest date among '
    'the alterations the portal cites (its alteration notes, its "última atualização" line and the constitutional '
    'actions it lists). The wordings in between are not reconstructed, so no earlier version is given rather than a '
    'wrong one.',
    'The text in force leaves out what the portal strikes through (earlier wordings) and its alteration notes '
    '(paragraphs in italics starting with "-", such as "- Caput com redação dada pela ..."); markers such as "(NR)" '
    'that are part of the text are kept. Anything struck through in a "texto original" page is left out too.',
    'One file per Artigo (articles of the Ato das Disposições Transitórias as adt-*); headings of the Títulos, '
    'Capítulos and Seções stand above the first article under them; "000-titulo" holds the title, the ementa and the '
    'preamble. Text after the last article (place, date, signatures) stays with the last article.',
    'Tables are one line per row, cells separated by " | "; images are left out.',
]
AI = ["Claude Code (claude-opus-5-5) wrote Lexifina's code and chose the sources. No model output is used as legal "
      "text or dates: every word comes from the ALESP pages."]


def act_of(rec, today):
    orig_u, cur_u = rec.get('urlIntegraOriginal'), rec.get('urlIntegraAtualizada')
    ob, cb = (raw(orig_u) if orig_u else None), (raw(cur_u) if cur_u else None)
    if ob is None and cb is None:
        return None, {}
    slug = slug_of(rec)
    enacted, published = iso(rec['data']), iso(rec.get('dataPublicacao'))
    first = enacted if rec['tipo'] == 'Constituição' else (published or enacted)
    law_key = slug if slug != 'constituicao' else 'constituicao-1989'
    laws = {law_key: {'label': rec['nomeNorma'], 'title': rec.get('dsEmenta') or rec['nomeNorma'], 'kind': 'law',
                      'enacted': enacted, 'published': published, 'url': f"https://www.al.sp.gov.br/norma/{rec['idNorma']}",
                      'temporary_until': None, 'restores': None, 'note': None}}
    api = raw(f"https://baleg-api-prd.al.sp.gov.br/norma/{rec['idNorma']}")
    court = []  # dates the portal gives for constitutional actions against the act (filing, rulings, publication)
    if api:
        for c in json.loads(api).get('constitucionalidades') or []:
            for an in c.get('andamentos') or []:
                court += [f'{y}-{mo}-{d}' for d, mo, y in DATE.findall(html.unescape(re.sub(r'<[^>]+>', ' ', an.get('titulo') or '')))]
                if an.get('dtAndamento'):
                    court.append(an['dtAndamento'][:10])
    s = cb.decode('utf-8', 'replace') if cb is not None else ''
    alter = sorted(d for d in note_dates(s) + court if d > first)
    if ob is not None and not alter:
        # Never altered: the text as enacted, credited to the act itself.
        u = units_of(lines_of(body(ob.decode('utf-8', 'replace'), current=False)))
        if not u:
            return None, {}
        versions = [{'from': first, 'source_url': orig_u, 'sha256': hashlib.sha256(ob).hexdigest(), 'units': u}]
        first_law = law_key
    else:
        if cb is None:
            return None, {}
        u = units_of(lines_of(body(s, current=True)))
        if not u:
            return None, {}
        # Altered: only the text in force, as the oldest version available, dated by the latest alteration the portal
        # cites. The wordings in between are not reconstructed, so no earlier version is given rather than a wrong one.
        versions = [{'from': alter[-1] if alter else first, 'source_url': cur_u, 'sha256': hashlib.sha256(cb).hexdigest(),
                     'units': u, 'note': f'Text in force as consolidated by ALESP; the act ({rec["nomeNorma"]}) was '
                                         f'altered {len(set(alter))} time(s) by the dates the portal cites, '
                                         f'the latest on {alter[-1] if alter else first}.'}]
        first_law = None
    act = {'slug': slug, 'short': short_of(rec), 'title': rec['nomeNorma'] + (f" ({rec['dsEmenta']})" if rec.get('dsEmenta') and len(rec['dsEmenta']) < 160 else ''),
           'url': f"https://www.al.sp.gov.br/norma/{rec['idNorma']}",
           'first_law': first_law, 'earlier_laws': [] if first_law else [law_key], 'versions': versions}
    if rec['tipo'] == 'Constituição':
        act['title'] = 'Constituição do Estado de São Paulo'
    return act, laws


def part(name, acts, laws, today, n_src):
    c = {'country': COUNTRY,
         'sources': [{'name': 'Assembleia Legislativa do Estado de São Paulo (ALESP), Legislação Estadual: texto '
                      'original and texto com alterações of each norma', 'url': 'https://www.al.sp.gov.br/legislacao',
                      'retrieved': today, 'licence': COUNTRY['licence_note'],
                      'notes': f'{len(acts)} acts in this part, {n_src} source pages.'}],
         'laws': laws, 'acts': acts, 'applies': [], 'decisions': DECISIONS, 'ai_use': AI}
    OUT.mkdir(exist_ok=True)
    p = OUT / f'{name}.json'
    s = json.dumps(c, ensure_ascii=False, indent=1) + '\n'
    if p.exists() and p.read_text(encoding='utf-8') == s:
        return p
    tmp = p.with_suffix('.tmp')
    tmp.write_text(s, encoding='utf-8', newline='\n')
    os.replace(tmp, p)
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='')
    ap.add_argument('--part-size', type=int, default=50)
    ap.add_argument('--today', required=True)
    a = ap.parse_args()
    idx = json.loads((CACHE / 'index.json').read_text(encoding='utf-8'))
    listing, page = [], 0
    while True:  # the full list of Leis Complementares, as retrieved: fixes the parts before every act is fetched
        b = raw(f'https://baleg-api-prd.al.sp.gov.br/normas?idsTipo=2&idsSituacao=1&page={page}&size=100')
        if b is None:
            break
        d = json.loads(b)
        listing += d['content']
        if d.get('last', True) or not d['content']:
            break
        page += 1
    key = lambda r: (iso(r['data']), int(re.sub(r'\D', '', r['nuNorma'] or '0') or 0), r['idNorma'])
    if a.only in ('', 'constituicao'):
        r = idx['155101']
        act, laws = act_of(r, a.today)
        print(part('10-constituicao', [act], laws, a.today, len(act['versions'])), len(act['versions']), 'versions',
              sum(len(v['units']) for v in act['versions']), 'units')
    if a.only in ('', 'lc'):
        lcs = sorted(listing, key=key)
        # A part is written only once every act in it is fetched, so a published part never changes.
        for i in range(0, len(lcs), a.part_size):
            chunk = lcs[i:i + a.part_size]
            if any(r['idNorma'] not in idx for r in chunk):
                continue
            chunk = [idx[r['idNorma']] for r in chunk]
            acts, laws, n = [], {}, 0
            for r in chunk:
                act, l = act_of(r, a.today)
                if act:
                    acts.append(act); laws.update(l); n += len(act['versions'])
            print(part(f'20-lc-{i // a.part_size + 1:02d}', acts, laws, a.today, n), len(acts), 'acts', n, 'versions')


if __name__ == '__main__':
    main()
