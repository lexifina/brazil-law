"""Independent letters-and-digits check of every law version against its PDF, read with a second PDF reader
(poppler's pdftotext, not the builder's PyMuPDF) and none of the builder's code.

    python -X utf8 check_laws.py part.json ...

The pdftotext text in content-stream order (-raw), page by page: lines seen among the first or last four lines of two or more pages (with digits
counted as the same) and lines that are only a page number are removed; then the text from the first line that starts
"LEI" (or "LEI COMPLEMENTAR", "LEI ORDINÁRIA", "L E I") and carries the law's number to the first line, from the last
article line on, that ends in a date written out ("10 de outubro de 2026."), that line included. Reduced to letters and digits, it must equal the
version's unit files reduced the same way, each unit found at its place in document order.
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE / '.cache' / 'sapl' / 'raw'
MONTHS = 'janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro'


def ld(s):
    return ''.join(ch for ch in s if ch.isalnum())


def clean(s):
    return re.sub(r'\s+', ' ', s.replace(' ', ' ')).strip()


def source_text(path, number, complementar):
    out = subprocess.run(['pdftotext', '-raw', '-enc', 'UTF-8', str(path), '-'], capture_output=True, check=True).stdout
    pages = [[clean(l) for l in pg.split('\n') if clean(l)] for pg in out.decode('utf-8').split('\f')]
    pages = [p for p in pages if p]
    count = {}
    for p in pages:
        for l in set(p[:4] + p[-4:]):
            k = re.sub(r'[0-9]', '#', l)
            count[k] = count.get(k, 0) + 1
    rep = {k for k, c in count.items() if c >= 2} if len(pages) >= 2 else set()
    lines = [l for p in pages for l in p
             if re.sub(r'[0-9]', '#', l) not in rep
             and not re.fullmatch(r'(?i)(?:p[áa]g(?:ina)?\.?\s*)?[0-9]{1,3}(?:\s*(?:/|de)\s*[0-9]{1,3})?', l)]
    a = None
    for i, l in enumerate(lines):
        m = re.match(r'(?i)L\s?E\s?I\s+(COMPLEMENTAR\s+)?(?:ORDIN[ÁA]RIA\s+)?(?:MUNICIPAL\s+)?(?:N[º°ºo.]*|N[ÚU]MERO)\s*[:.]?\s*([0-9.]+)', l)
        if m and m.group(2).replace('.', '') == str(number) and bool(m.group(1)) == complementar:
            a = i
            break
    last_art = max(i for i, l in enumerate(lines) if i > a and re.match(r'Art(?:igo)?\.?\s*[0-9]', l))
    b = next(i for i in range(last_art, len(lines))
             if re.search(r'\b[0-9]{1,2}\s*[º°o]?\s+de\s+(?:' + MONTHS + r')\s+de\s+[0-9]{4}\s*\.?\s*$', lines[i], re.I))
    return '\n'.join(lines[a:b + 1])


def main(paths):
    bad = total = 0
    for p in paths:
        for a in json.load(open(p, encoding='utf-8'))['acts']:
            m = re.fullmatch(r'(lei|lc)-[0-9]{4}-([0-9]+)', a['slug'])
            for v in a['versions']:
                path = RAW / hashlib.sha256(v['source_url'].encode()).hexdigest()
                assert hashlib.sha256(path.read_bytes()).hexdigest() == v['sha256'], (a['slug'], 'sha256')
                total += 1
                try:
                    src = ld(source_text(path, int(m.group(2)), m.group(1) == 'lc'))
                except (StopIteration, ValueError, TypeError) as e:
                    bad += 1
                    print(f'MISMATCH {a["slug"]} {v["from"]}: second reader finds no heading/article/closing line ({e})')
                    continue
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
                if rest or pos != len(src):
                    bad += 1
                    print(f'MISMATCH {a["slug"]} {v["from"]}: matched {pos}/{len(src)}; next source: '
                          f'{src[pos:pos + 80]!r}; unplaced: {list(rest)[:5]}')
    print(f'{total} versions checked, {bad} mismatches')
    return bad


if __name__ == '__main__':
    sys.exit(1 if main(sys.argv[1:]) else 0)
