"""Independent letters-and-digits check of every version against its source page (regex only, no HTML parser).

    python -X utf8 check_letters.py [part.json ...]

For each version: the page text from the first <h1> on, with struck-through text, the portal's alteration notes
(for a "texto com alterações" page) and its update line (a heading in parentheses such as "(Última atualização: ...)"
or "(Atualizada até ...)") removed, reduced to letters and digits, must equal the version's unit files reduced the same
way, each unit found at its place in document order.
"""
import hashlib, html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def ld(s):
    return ''.join(ch for ch in s if ch.isalnum())


def update_line(m):
    t = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
    return '' if t.startswith('(') and 'tualiza' in t.lower() else m.group(0)


def page_text(raw, current):
    s = raw.decode('utf-8', 'replace')
    s = s[s.index('<h1'):] if '<h1' in s else s[s.index('<body'):]
    s = re.sub(r'(?is)<script.*?</script>|<!--.*?-->', '', s)
    s = re.sub(r'(?is)<(s|strike|del)\b[^>]*>.*?</\1>', '', s)
    s = re.sub(r'(?is)<h1\b[^>]*>(.*?)</h1>', update_line, s)
    if current:
        def note(m):
            inner = m.group(1)
            if re.match(r'(?is)(?:\s|&nbsp;|<[^>]+>)*-', inner) and '<em' in inner.lower() and not re.sub(
                    r'(?is)<em>.*?</em>|<[^>]+>|&nbsp;|[\s.;,]', '', inner):
                return ''
            return m.group(0)
        s = re.sub(r'(?is)<p\b[^>]*>(.*?)</p>', note, s)
    return html.unescape(re.sub(r'<[^>]+>', ' ', s))


def main(paths):
    bad = total = 0
    for p in paths:
        c = json.load(open(p, encoding='utf-8'))
        for a in c['acts']:
            for v in a['versions']:
                raw = (HERE / '.cache' / 'raw' / hashlib.sha256(v['source_url'].encode()).hexdigest()).read_bytes()
                assert hashlib.sha256(raw).hexdigest() == v['sha256'], (a['slug'], 'sha256')
                src = ld(page_text(raw, '/original-' not in v['source_url']))
                rest = {k: ld(re.sub(r'(?m)^#+ ', '', u['text'])) for k, u in v['units'].items()}
                pos = 0
                while rest:
                    hit = None
                    for k, t in rest.items():
                        if t and src.startswith(t, pos) and (hit is None or len(t) > len(rest[hit])):
                            hit = k
                    if hit is None:
                        break
                    pos += len(rest.pop(hit))
                total += 1
                if rest or pos != len(src):
                    bad += 1
                    print(f'MISMATCH {a["slug"]} {v["from"]}: matched {pos}/{len(src)}; next source: '
                          f'{src[pos:pos + 80]!r}; unplaced: {list(rest)[:5]}')
    print(f'{total} versions checked, {bad} mismatches')
    return bad


if __name__ == '__main__':
    sys.exit(1 if main(sys.argv[1:] or sorted(str(p) for p in (HERE / 'corpus.d').glob('*.json'))) else 0)
