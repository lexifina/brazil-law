"""Builds corpus.d parts for Paraná from the retrieved pages of the Sistema Estadual de Legislação (no network).

    python -X utf8 parse.py --today YYYY-MM-DD

The Casa Civil's system shows each act "Compilado" (the text with only the last alteration of each provision) and
"Original" (as first published). Its alteration notes are links in parentheses, such as "(Redação dada pela Emenda
Constitucional 7 de 24/04/2000)". An act with no such note is given as enacted (Original), credited to the act itself;
an altered act only as its compiled text in force, credited to the publisher as the oldest version available, dated by
the latest date its alteration notes cite.
"""
import argparse, html, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from br_lib import lines_of, units_of, dates_in, write_part, sha  # noqa: E402

CACHE = HERE / '.cache'
SITE = 'https://www.legislacao.pr.gov.br/legislacao'
NOTE = re.compile(r'(?is)<a\s+href=[^>]*>\s*(\(.*?\))\s*</a>')
ALTERS = re.compile(r'reda[çc][ãa]o|inclu[íi]d|acrescid|acrescentad|revogad|suprimid|renumerad|inconstitucional|'
                    r'suspens|alterad', re.I)


def raw(url):
    p = CACHE / 'raw' / sha(url.encode())
    return p.read_bytes() if p.exists() else None


def region(s):
    """The act: from its title (<h3>) to the rule above the "Este texto não substitui" line."""
    i = s.index('<h3>')
    j = s.index('<hr/>', i)
    return re.sub(r'(?is)<input\b[^>]*>', '', s[i:j])


COUNTRY = {
    'code': 'BR-PR', 'name': 'Paraná', 'slug': 'brazil-parana', 'lang': 'pt', 'tz': 'America/Sao_Paulo',
    'future_branch': 'futuro',
    'publisher': {'name': 'Casa Civil do Estado do Paraná (Sistema Estadual de Legislação)',
                  'email': 'legislacao@legislacao.pr.gov.br.invalid'},
    'default_in_force_rule': {
        'text': 'Decreto-Lei 4.657/1942 (LINDB) art. 1: unless it says otherwise, a law takes effect 45 days after its '
                'official publication. This record dates each act as enacted by its publication in the Diário Oficial '
                'do Estado (the Constituição by its promulgation and publication, 5 October 1989).',
        'source': 'https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm'},
    'licence_note': 'Texts: Sistema Estadual de Legislação, Casa Civil do Governo do Estado do Paraná, '
                    'www.legislacao.pr.gov.br. Lei 9.610/1998 art. 8 IV: the texts of laws and other official acts are '
                    'not protected by copyright. Non-official text: "Este texto não substitui o publicado no Diário '
                    'Oficial do Estado".',
}
DECISIONS = [
    'An act with no alteration note is given as enacted ("Original"), credited to the act itself and dated by its '
    'publication in the Diário Oficial do Estado (the Constituição by its promulgation, 5 October 1989). An altered '
    'act is given only as its compiled text ("Compilado": the text with the last alteration of each provision), '
    'credited to the publisher as the oldest version available and dated by the latest date its alteration notes '
    'cite. The wordings in between are not reconstructed yet, so no earlier version is given rather than a wrong one.',
    'The publisher\'s notes (links in parentheses, such as "(Redação dada pela Emenda Constitucional 7 de 24/04/2000)" '
    'or "(vide Lei ...)") are left out of the text; "(vide ...)" notes are cross-references and do not date a version.',
    'One file per Art. (articles of the Ato das Disposições Constitucionais Transitórias as adt-*); headings of the '
    'Títulos, Capítulos and Seções stand above the first article under them; "000-titulo" holds the title, the '
    'publication line and the preamble. Text after the last article (place, date, signatures) stays with the last '
    'article.',
]
AI = ["Claude Code (claude-opus-5-5) wrote Lexifina's code and chose the sources. No model output is used as legal "
      "text or dates: every word comes from the Sistema Estadual de Legislação pages."]


def act_of(cod, slug, short, title, law_key, first, adt):
    cu = f'{SITE}/pesquisarAto.do?action=exibir&codAto={cod}&codTipoAto=&tipoVisualizacao=compilado'
    ou = f'{SITE}/pesquisarAto.do?action=exibir&codAto={cod}&codTipoAto=&tipoVisualizacao=original'
    cb, ob = raw(cu), raw(ou)
    if cb is None:
        return None, {}
    c = region(cb.decode('utf-8', 'replace'))
    notes = [html.unescape(re.sub(r'<[^>]+>', '', n)) for n in NOTE.findall(c)]
    alter = sorted(d for n in notes if ALTERS.search(n) and not n.lower().startswith('(vide') for d in dates_in(n) if d > first)
    if alter or ob is None:
        url, b, h = cu, cb, NOTE.sub('', c)
    else:
        url, b = ou, ob
        h = NOTE.sub('', region(ob.decode('utf-8', 'replace')))
    units = units_of(lines_of(h), adt=adt)
    laws = {law_key: {'label': title, 'title': title, 'kind': 'law', 'enacted': first, 'published': first,
                      'url': f'{SITE}/pesquisarAto.do?action=exibir&codAto={cod}', 'temporary_until': None,
                      'restores': None, 'note': None}}
    v = {'from': alter[-1] if alter else first, 'source_url': url, 'sha256': sha(b), 'units': units}
    if alter:
        v['note'] = (f'Compiled text in force as published by the Casa Civil; {title} was altered on {len(set(alter))} '
                     f'date(s) its notes cite, the latest {alter[-1]}.')
    act = {'slug': slug, 'short': short, 'title': title, 'url': f'{SITE}/pesquisarAto.do?action=exibir&codAto={cod}',
           'first_law': None if alter else law_key, 'earlier_laws': [law_key] if alter else [], 'versions': [v]}
    return act, laws


def part(name, acts, laws, today):
    c = {'country': COUNTRY,
         'sources': [{'name': 'Sistema Estadual de Legislação (Casa Civil do Estado do Paraná): the Compilado and '
                      'Original views of each act', 'url': SITE, 'retrieved': today, 'licence': COUNTRY['licence_note'],
                      'notes': f'{len(acts)} acts in this part.'}],
         'laws': laws, 'acts': acts, 'applies': [], 'decisions': DECISIONS, 'ai_use': AI}
    return write_part(HERE / 'corpus.d', name, c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--today', required=True)
    a = ap.parse_args()
    act, laws = act_of('9779', 'constituicao', 'CE-PR', 'Constituição do Estado do Paraná', 'constituicao-1989',
                       '1989-10-05', True)
    if act:
        v = act['versions'][0]
        print(part('10-constituicao', [act], laws, a.today), v['from'], len(v['units']))


if __name__ == '__main__':
    main()
