"""Independent letters-and-digits check of every version against its source page (string splitting, no parser).

    python -X utf8 check_letters.py [part.json ...]

For each version: the page from the act's title (<h3>) to the closing rule (<hr/>), without the publisher's linked notes
in parentheses and the form fields, reduced to letters and digits, must equal the version's unit files reduced the same
way, each unit found at its place in document order.
"""
import hashlib, html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from br_lib import letters_check  # noqa: E402


def page_text(s):
    s = s.split('<h3>', 1)[1].split('<hr/>', 1)[0]
    out, rest = [], s
    while True:
        m = re.search(r"(?i)<a href=", rest)
        if not m:
            out.append(rest)
            break
        out.append(rest[:m.start()])
        end = rest.lower().find('</a>', m.start())
        inner = html.unescape(re.sub(r'<[^>]+>', '', rest[m.start():end]))
        if inner.strip().startswith('('):
            rest = rest[end + 4:]
        else:
            out.append(rest[m.start():end + 4])
            rest = rest[end + 4:]
    s = re.sub(r'(?i)<input[^>]*>', ' ', ''.join(out))
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
