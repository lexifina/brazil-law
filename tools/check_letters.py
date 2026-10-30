"""Independent letters-and-digits check of every version against its ALMG record (regex only, no HTML parser).

    python -X utf8 check_letters.py [part.json ...]

For each version: the record's field the version was taken from ("texto" or "textoConsolidado"), with struck-through
text, the editorial paragraphs in parentheses (except "(Vetado)") and the "Data da última atualização" line removed,
reduced to letters and digits, must equal the version's unit files reduced the same way, each unit found at its place
in document order.
"""
import hashlib, html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from br_lib import letters_check  # noqa: E402


def field_text(h):
    h = re.sub(r'(?is)<head[ >].*?</head>|<style[ >].*?</style>|<script[ >].*?</script>|<!--.*?-->', ' ', h)
    h = re.sub(r'(?is)<(del|s|strike)\b[^>]*>.*?</\1>', '', h)

    def para(m):
        t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', m.group(1)))).replace('\xa0', ' ').strip()
        if (t.startswith('(') and t.endswith(')') and not re.fullmatch(r'\((?i:vetad[oa])\.?\)\.?', t)) \
                or re.fullmatch(r'=+', t) or t.startswith('Data da última atualização'):
            return ' '
        return ' ' + m.group(1) + ' '
    h = re.sub(r'(?is)<p\b[^>]*>(.*?)</p>', para, h)
    return html.unescape(re.sub(r'<[^>]+>', ' ', h))


def main(paths):
    vs = []
    for p in paths:
        c = json.load(open(p, encoding='utf-8'))
        for a in c['acts']:
            for v in a['versions']:
                raw = (HERE / '.cache' / 'raw' / hashlib.sha256(v['source_url'].encode()).hexdigest()).read_bytes()
                assert hashlib.sha256(raw).hexdigest() == v['sha256'], (a['slug'], 'sha256')
                field = re.search(r'From the "(\w+)" field', v['note']).group(1)
                rec = json.loads(raw)['resultado']['listaItem'][0]
                vs.append((f"{a['slug']} {v['from']}", v['units'], field_text(rec[field])))
    bad = letters_check(vs, None)
    for b in bad:
        print(b)
    print(f'{len(vs)} versions checked, {len(bad)} mismatches')
    return len(bad)


if __name__ == '__main__':
    sys.exit(1 if main(sys.argv[1:] or sorted(str(p) for p in (HERE / 'corpus.d').glob('*.json'))) else 0)
