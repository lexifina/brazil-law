"""Independent letters-and-digits check of every version against its Legisla Bahia page (string splitting, no parser).

    python -X utf8 check_letters.py [part.json ...]

For each version: the page's body field (from the body div to the "criado por arquivo" field), without its style
sheet and without the paragraphs of class "Alteracao" or "info-complementar", reduced to letters and digits, must equal the version's unit
files reduced the same way, each unit found at its place in document order.
"""
import hashlib, html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from br_lib import letters_check  # noqa: E402


def page_text(s):
    s = s.split('<div class="field field--name-body', 1)[1].split('field--name-field-criado-por-arquivo', 1)[0]
    s = s.split('>', 1)[1]
    s = re.sub(r'(?is)<style.*?</style>', ' ', s)
    out = []
    for i, chunk in enumerate(re.split(r'(?i)(?=<p[\s>])', s)):
        head = chunk[:chunk.find('>') + 1]
        if re.search(r'class="?(?:Alteracao|info-complementar)\b', head):
            end = chunk.lower().find('</p>')
            chunk = ' ' + chunk[end + 4:] if end >= 0 else ' '
        out.append(chunk)
    s = ''.join(out)
    s = s[:s.rfind('<div')] if '<div' in s else s
    return html.unescape(re.sub(r'<[^>]+>', ' ', s))


def main(paths):
    vs = []
    for p in paths:
        for a in json.load(open(p, encoding='utf-8'))['acts']:
            for v in a['versions']:
                raw = (HERE / '.cache' / 'raw' / hashlib.sha256(v['source_url'].encode()).hexdigest()).read_bytes()
                assert hashlib.sha256(raw).hexdigest() == v['sha256'], (a['slug'], 'sha256')
                vs.append((f"{a['slug']} {v['from']}", v['units'], page_text(raw.decode('utf-8', 'replace'))))
    bad = letters_check(vs, None)
    for b in bad:
        print(b)
    print(f'{len(vs)} versions checked, {len(bad)} mismatches')
    return len(bad)


if __name__ == '__main__':
    sys.exit(1 if main(sys.argv[1:] or sorted(str(p) for p in (HERE / 'corpus.d').glob('*.json'))) else 0)
