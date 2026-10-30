"""Builds corpus.d parts for Minas Gerais from the retrieved ALMG open-data records (no network).

    python -X utf8 parse.py --today YYYY-MM-DD [--part-size 50]

Each norma's record (dadosabertos.almg.gov.br/api/v2/legislacao/mineira/<tipo>/<num>/<ano>) carries the text as
enacted ("texto") and the consolidated text ("textoConsolidado"). An act ALMG shows no alteration for is given as
enacted, credited to the act itself; an altered act only as its text in force, credited to ALMG as the oldest version
available, dated by the latest alteration the record cites.
"""
import argparse, gzip, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from br_lib import lines_of, units_of, dates_in, write_part, sha  # noqa: E402

CACHE = HERE / '.cache'
API = 'https://dadosabertos.almg.gov.br/api/v2/legislacao/mineira'
ALTER = re.compile(r'ALTERA|ACR[ÉE]SCIMO|REVOGA|SUPRESS|RENUMERA|NOVA REDA|INCONSTITUCIONAL|SUSPENS', re.I)
NOTE_WORDS = re.compile(r'reda[çc][ãa]o|acrescentad|revogad|renumerad|declarad|suspens|inconstitucional|alterad|'
                        r'retificad|vigência|vigor|efeitos|suprimid|promulgad|derrubad|substitu', re.I)


def raw(url):
    p = CACHE / 'raw' / sha(url.encode())
    return p.read_bytes() if p.exists() else None


def is_note(l):
    """An ALMG editorial note: a whole paragraph in parentheses, e.g. "(Inciso com redação dada pelo art. 1º da
    Emenda à Constituição nº 87, de 4/11/2011.)" or "(Vide Lei nº 12.999, de 31/7/1998.)". "(Vetado)" is text."""
    return l.startswith('(') and l.endswith(')') and not re.fullmatch(r'\((Vetad[oa]|VETAD[OA])\.?\)\.?', l)


def text_lines(h):
    h = re.sub(r'(?is)<del\b[^>]*>.*?</del>|<s\b[^>]*>.*?</s>|<strike\b[^>]*>.*?</strike>', '', h)
    out = []
    for kind, l in lines_of(h):
        if is_note(l) or re.fullmatch(r'=+', l) or re.match(r'Data da última atualização', l):
            continue
        out.append((kind, l))
    return out


def notes_of(h):
    return [l for _, l in lines_of(h) if is_note(l)]


def iso8(d):
    return f'{d[:4]}-{d[4:6]}-{d[6:8]}' if d and len(d) == 8 else None


COUNTRY = {
    'code': 'BR-MG', 'name': 'Minas Gerais', 'slug': 'brazil-minas-gerais', 'lang': 'pt', 'tz': 'America/Sao_Paulo',
    'future_branch': 'futuro',
    'publisher': {'name': 'Assembleia Legislativa do Estado de Minas Gerais (ALMG)', 'email': 'almg@almg.gov.br.invalid'},
    'default_in_force_rule': {
        'text': 'Decreto-Lei 4.657/1942 (LINDB) art. 1: unless it says otherwise, a law takes effect 45 days after its '
                'official publication. Minas Gerais laws almost always say "Esta lei entra em vigor na data de sua '
                'publicação"; this record dates each act as enacted by its publication in the Minas Gerais Diário do '
                'Executivo (the Constituição by its promulgation).',
        'source': 'https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm'},
    'licence_note': 'Texts: Assembleia Legislativa do Estado de Minas Gerais (ALMG), Legislação Mineira, '
                    'dadosabertos.almg.gov.br. Lei 9.610/1998 art. 8 IV: the texts of laws and other official acts '
                    'are not protected by copyright. Non-official text: only the Diário Oficial is authoritative.',
}
DECISIONS = [
    'An act ALMG shows no alteration for is given as enacted (the record\'s "texto"), credited to the act itself and '
    'dated by its publication in the Diário do Executivo (the Constituição by its promulgation, 21 September 1989). '
    'An altered act is given only as its text in force (the record\'s "textoConsolidado"), credited to ALMG as the '
    'oldest version available and dated by the latest date among the alterations the record cites (its notes in '
    'parentheses and its linked altering acts). The wordings in between are not reconstructed, so no earlier version '
    'is given rather than a wrong one.',
    'ALMG\'s editorial notes (whole paragraphs in parentheses, such as "(Inciso com redação dada pelo ...)" or "(Vide '
    'Lei nº ...)"), the text it strikes through and its "Data da última atualização" line are left out; "(Vetado)" is '
    'kept as text.',
    'One file per Art. (articles of an Ato das Disposições Transitórias as adt-*); headings of the Títulos, Capítulos '
    'and Seções stand above the first article under them; "000-titulo" holds the title, the ementa and the preamble. '
    'Text after the last article (place, date, signatures) stays with the last article.',
    'Acts whose record lists a total revocation ("REVOGAÇÃO TOTAL") are left out.',
]
AI = ["Claude Code (claude-opus-5-5) wrote Lexifina's code and chose the sources. No model output is used as legal "
      "text or dates: every word comes from the ALMG records."]


def act_of(t, num, ano):
    url = f'{API}/{t}/{num}/{ano}?formato=json'
    b = raw(url)
    if b is None:
        return None, {}, 'not fetched'
    items = json.loads(b).get('resultado', {}).get('listaItem') or []
    if not items:
        return None, {}, 'no record'
    r = items[0]
    vide = r.get('listaVide') or []
    if any('REVOGAÇÃO TOTAL' in (v.get('descricao') or '').upper() for v in vide):
        return None, {}, 'revoked'
    enacted = iso8(r.get('data'))
    pub = [d for d in dates_in(r.get('fonte') or '')]
    published = pub[0] if pub else None
    first = enacted if t in ('CON', 'ADT') else (published or enacted)
    slug = {'CON': 'constituicao', 'ADT': 'adt-1989'}.get(t) or f'{t.lower()}-{ano}-{int(num):04d}'
    law_key = 'constituicao-1989' if t in ('CON', 'ADT') else slug
    label = {'CON': 'Constituição do Estado de Minas Gerais',
             'ADT': 'Ato das Disposições Constitucionais Transitórias da Constituição do Estado de Minas Gerais',
             'LCP': f'Lei Complementar nº {num}, de {ano}'}.get(t, r.get('norma'))
    ementa = re.sub(r'\s+', ' ', (r.get('ementa') or '')).strip()
    laws = {law_key: {'label': 'Constituição do Estado de Minas Gerais' if t == 'ADT' else label, 'title': ementa.capitalize() if ementa else label, 'kind': 'law', 'enacted': enacted,
                      'published': published, 'url': f'https://www.almg.gov.br/legislacao-mineira/{t}/{num}/{ano}/',
                      'temporary_until': None, 'restores': None, 'note': None}}
    cons = r.get('textoConsolidado') or ''
    orig = r.get('texto') or ''
    alter = []
    for n in notes_of(cons):
        if NOTE_WORDS.search(n):
            alter += dates_in(n)
    for v in vide:
        d = (v.get('descricao') or '').split('\n')
        if d and ALTER.search(d[-1]):
            alter += dates_in(' '.join(d[1:2]))
    for a in r.get('listaAdin') or []:
        alter += dates_in(json.dumps(a, ensure_ascii=False))
    alter = sorted(d for d in alter if first and d > first)
    if not alter and orig.strip():
        units, field, from_, first_law, note = units_of(text_lines(orig)), 'texto', first, law_key, None
    else:
        src = cons or orig
        units, field, from_, first_law = units_of(text_lines(src)), 'textoConsolidado' if cons else 'texto', \
            (alter[-1] if alter else first), None
        note = (f'Text in force as consolidated by ALMG; {label} was altered on {len(set(alter))} date(s) the record '
                f'cites, the latest {alter[-1]}.' if alter else 'Text in force as consolidated by ALMG.')
    if not units:
        return None, {}, 'no text'
    v = {'from': from_, 'source_url': url, 'sha256': sha(b), 'units': units}
    v['note'] = (note + ' ' if note else '') + f'From the "{field}" field of the ALMG record.'
    act = {'slug': slug, 'short': {'CON': 'CE-MG', 'ADT': 'ADCT-MG'}.get(t) or f'LC {num}/{ano}', 'title': label + (f' ({ementa.capitalize()})' if ementa and len(ementa) < 160 else ''),
           'url': f'https://www.almg.gov.br/legislacao-mineira/{t}/{num}/{ano}/', 'first_law': first_law,
           'earlier_laws': [] if first_law else [law_key], 'versions': [v]}
    if t in ('CON', 'ADT'):
        act['title'] = label
    return act, laws, 'ok'


def part(name, acts, laws, today):
    c = {'country': COUNTRY,
         'sources': [{'name': 'Assembleia Legislativa do Estado de Minas Gerais (ALMG), Dados Abertos: the record of '
                      'each norma (texto and textoConsolidado)', 'url': 'https://dadosabertos.almg.gov.br',
                      'retrieved': today, 'licence': COUNTRY['licence_note'], 'notes': f'{len(acts)} acts in this part.'}],
         'laws': laws, 'acts': acts, 'applies': [], 'decisions': DECISIONS, 'ai_use': AI}
    return write_part(HERE / 'corpus.d', name, c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--today', required=True)
    ap.add_argument('--part-size', type=int, default=50)
    a = ap.parse_args()
    acts, laws = [], {}
    for t in ('CON', 'ADT'):
        act, l, why = act_of(t, '1989', '1989')
        print(t, why)
        if act:
            acts.append(act); laws.update(l)
    if len(acts) == 2:
        print(part('10-constituicao', acts, laws, a.today))
    locs = []
    for i in (1, 2, 3):
        locs += re.findall(r'<loc>([^<]+)</loc>', gzip.decompress((CACHE / 'sitemap' / f'legislacao-mineira_{i}.xml.gz').read_bytes()).decode('utf-8'))
    lcp = sorted({(int(m.group(1)), m.group(2)) for u in locs
                  for m in [re.match(r'https://www.almg.gov.br/legislacao-mineira/LCP/(\d+)/(\d{4})/$', u)] if m},
                 key=lambda x: (x[1], x[0]))
    for i in range(0, len(lcp), a.part_size):
        chunk = lcp[i:i + a.part_size]
        if any(raw(f'{API}/LCP/{n}/{y}?formato=json') is None for n, y in chunk):
            continue  # written only once every act in it is fetched, so a published part never changes
        acts, laws, why = [], {}, {}
        for n, y in chunk:
            act, l, w = act_of('LCP', str(n), y)
            why[w] = why.get(w, 0) + 1
            if act:
                acts.append(act); laws.update(l)
        print(part(f'20-lc-{i // a.part_size + 1:02d}', acts, laws, a.today), why)


if __name__ == '__main__':
    main()
