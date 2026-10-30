"""Builds corpus.d parts for Bahia from the retrieved Legisla Bahia pages (no network).

    python -X utf8 parse.py --today YYYY-MM-DD [--part-size 50]

Legisla Bahia (Casa Civil) publishes each act's text in force, with its alteration notes as paragraphs of class
"Alteracao" ("Alterado pela Emenda ..., Redação original: ..."). An act with no such note is given as enacted, credited
to the act itself; an altered act only as its text in force, credited to the publisher as the oldest version available,
dated by the latest date its notes cite.
"""
import argparse, html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from br_lib import lines_of, units_of, dates_in, write_part, sha  # noqa: E402

CACHE = HERE / '.cache'
SITE = 'https://www.legislabahia.ba.gov.br'
NOTE = re.compile(r'(?is)<p\b[^>]*class="?(?:Alteracao|info-complementar)"?[^>]*>.*?</p>')


def raw(url):
    p = CACHE / 'raw' / sha(url.encode())
    return p.read_bytes() if p.exists() else None


def field(s, name):
    """A metadata field of the page: the date of a date field (its datetime attribute), else the item's text."""
    i = s.find('field--name-field-' + name)
    if i < 0:
        return ''
    m = re.search(r'(?is)<div class="field--item">(.*?)</div>', s[i:])
    if not m:
        return ''
    t = re.search(r'datetime="(\d{4}-\d{2}-\d{2})', m.group(1))
    if t:
        y, mo, d = t.group(1).split('-')
        return f'{d}/{mo}/{y}'
    return html.unescape(re.sub(r'<[^>]+>', ' ', m.group(1))).strip()


def body(s):
    """The act's text: the body field of the page, without its Word style sheet."""
    i = s.index('<div class="field field--name-body')
    j = s.index('field--name-field-criado-por-arquivo', i) if 'field--name-field-criado-por-arquivo' in s[i:] else len(s)
    b = s[s.index('>', i) + 1:j]
    b = b[:b.rindex('<div')] if '<div' in b else b
    return re.sub(r'(?is)<style\b.*?</style>', '', b)


COUNTRY = {
    'code': 'BR-BA', 'name': 'Bahia', 'slug': 'brazil-bahia', 'lang': 'pt', 'tz': 'America/Bahia',
    'future_branch': 'futuro',
    'publisher': {'name': 'Casa Civil do Estado da Bahia (Legisla Bahia)', 'email': 'legislabahia@legislabahia.ba.gov.br.invalid'},
    'default_in_force_rule': {
        'text': 'Decreto-Lei 4.657/1942 (LINDB) art. 1: unless it says otherwise, a law takes effect 45 days after its '
                'official publication. Bahia laws almost always say "Esta Lei entra em vigor na data de sua '
                'publicação"; this record dates each act as enacted by its publication in the Diário Oficial do Estado '
                '(the Constituição by its promulgation).',
        'source': 'https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm'},
    'licence_note': 'Texts: Legisla Bahia, Casa Civil do Estado da Bahia, www.legislabahia.ba.gov.br. Lei 9.610/1998 '
                    'art. 8 IV: the texts of laws and other official acts are not protected by copyright. Non-official '
                    'text: only the Diário Oficial do Estado is authoritative.',
}
DECISIONS = [
    'An act Legisla Bahia shows no alteration note for is given as enacted, credited to the act itself and dated by its '
    'publication in the Diário Oficial do Estado (the Constituição by its promulgation, 5 October 1989). An altered '
    'act is given only as its text in force, credited to the publisher as the oldest version available and dated by '
    'the latest date its alteration notes cite. The wordings in between (the notes quote each "Redação original") are '
    'not reconstructed yet, so no earlier version is given rather than a wrong one.',
    'The alteration notes (paragraphs of class "Alteracao") and the publisher\'s notes (class "info-complementar", '
    'such as "Nota: O texto atualizado desta Lei encontra-se disponível no endereço ...") are left out of the text. '
    'Legisla Bahia gives most Leis Complementares as published, without later alterations: they are given as enacted.',
    'One file per Art. (articles of the Ato das Disposições Constitucionais Transitórias as adt-*); headings of the '
    'Títulos, Capítulos and Seções stand above the first article under them; "000-titulo" holds the title, the ementa '
    'and the preamble. Text after the last article (place, date, signatures) stays with the last article.',
]
AI = ["Claude Code (claude-opus-5-5) wrote Lexifina's code and chose the sources. No model output is used as legal "
      "text or dates: every word comes from the Legisla Bahia pages."]


def act_of(path, kind):
    url = SITE + path
    b = raw(url)
    if b is None:
        return None, {}, 'not fetched'
    s = b.decode('utf-8', 'replace')
    try:
        h = body(s)
    except ValueError:
        return None, {}, 'no body'
    notes = [html.unescape(re.sub(r'<[^>]+>', ' ', n)) for n in NOTE.findall(h)]
    text = NOTE.sub('', h)
    num = field(s, 'numero-doc')
    enacted = (dates_in(field(s, 'data-doc')) or [None])[0]
    published = (dates_in(field(s, 'data-de-publicacao-no-doe')) or [None])[0]
    if kind == 'con':
        slug, law_key, short, title, enacted = 'constituicao', 'constituicao-1989', 'CE-BA', 'Constituição do Estado da Bahia', '1989-10-05'
        first = enacted
    else:
        m = re.search(r'lei-complementar-no-(\d+)-de-.*?(\d{4})$', path)
        n, y = int(m.group(1)), m.group(2)
        slug = law_key = f'lc-{y}-{n:03d}'
        short, title = f'LC {n}/{y}', f'Lei Complementar nº {n}, de {y}'
        first = published or enacted
    if not first:
        return None, {}, 'no date'
    ementa = re.sub(r'\s+', ' ', field(s, 'ementa'))
    laws = {law_key: {'label': title, 'title': ementa or title, 'kind': 'law', 'enacted': enacted, 'published': published,
                      'url': url, 'temporary_until': None, 'restores': None, 'note': None}}
    alter = sorted(d for n in notes for d in dates_in(n) if d > first)
    units = units_of(lines_of(text), adt=(kind == 'con'))
    if not units:
        return None, {}, 'no text'
    v = {'from': alter[-1] if alter else first, 'source_url': url, 'sha256': sha(b), 'units': units}
    if alter:
        v['note'] = (f'Text in force as published by Legisla Bahia; {title} was altered on {len(set(alter))} date(s) its '
                     f'notes cite, the latest {alter[-1]}.')
    act = {'slug': slug, 'short': short, 'title': title + (f' ({ementa})' if ementa and len(ementa) < 160 and kind != 'con' else ''),
           'url': url, 'first_law': None if alter else law_key, 'earlier_laws': [law_key] if alter else [], 'versions': [v]}
    return act, laws, 'ok'


def part(name, acts, laws, today):
    c = {'country': COUNTRY,
         'sources': [{'name': 'Legisla Bahia (Casa Civil do Estado da Bahia): the page of each act', 'url': SITE,
                      'retrieved': today, 'licence': COUNTRY['licence_note'], 'notes': f'{len(acts)} acts in this part.'}],
         'laws': laws, 'acts': acts, 'applies': [], 'decisions': DECISIONS, 'ai_use': AI}
    return write_part(HERE / 'corpus.d', name, c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--today', required=True)
    ap.add_argument('--part-size', type=int, default=50)
    a = ap.parse_args()
    idx = json.loads((CACHE / 'index.json').read_text(encoding='utf-8'))
    act, laws, why = act_of(idx['11'][0], 'con')
    print('constituicao', why)
    if act:
        print(part('10-constituicao', [act], laws, a.today))
    if not (CACHE / 'fetch-done').exists():
        return
    def yr(p):
        m = re.search(r'lei-complementar-no-(\d+)-de-.*?(\d{4})$', p)
        return (m.group(2), int(m.group(1))) if m else ('9999', 0)
    lcs = sorted((p for p in idx['5'] if re.search(r'lei-complementar-no-\d+-de-', p)), key=yr)
    for i in range(0, len(lcs), a.part_size):
        acts, laws, why = [], {}, {}
        for p in lcs[i:i + a.part_size]:
            act, l, w = act_of(p, 'lc')
            why[w] = why.get(w, 0) + 1
            if act:
                acts.append(act); laws.update(l)
        print(part(f'20-lc-{i // a.part_size + 1:02d}', acts, laws, a.today), why)


if __name__ == '__main__':
    main()
