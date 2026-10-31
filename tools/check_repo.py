"""Checks a git-for-law repository against the corpus.json it was built from, and against git's own rules.

    python -X utf8 scripts/gitlaw_common/check.py ~/Documents/<slug>-law --corpus scripts/<slug>-law/corpus.json [--write]

1. Every version of every act, read back from git on the day it took effect (choosing the commit by its In-force
   trailer, as tools/on.py does), matches the corpus file by file; and on the day before, the act still reads as the
   version before it. That second check is what catches a change committed on the wrong day.
2. Every commit's trailers parse with git (`%(trailers)`), and every law commit has an In-force trailer.
3. Health: no merge commits on main, commit dates never go backwards along main, nothing dated after now.
With --write, the result goes to verification.json next to corpus.json; build.py prints it into REPRODUCE.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path


def git(repo: Path, *args: str) -> str:
    return subprocess.run(['git', *args], cwd=repo, capture_output=True, text=True, encoding='utf-8', check=True).stdout


class Cat:
    """One long-lived `git cat-file --batch` for every blob read."""

    def __init__(self, repo: Path):
        self.p = subprocess.Popen(['git', 'cat-file', '--batch'], cwd=repo, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def read(self, spec: str) -> bytes | None:
        self.p.stdin.write(spec.encode('utf-8') + b'\n')
        self.p.stdin.flush()
        head = self.p.stdout.readline().decode()
        if head.endswith('missing\n'):
            return None
        size = int(head.split()[2])
        data = self.p.stdout.read(size)
        self.p.stdout.read(1)
        return data

    def close(self):
        self.p.stdin.close()
        self.p.wait()


def commits_by_act(repo: Path, branch: str, act: str) -> list[tuple[str, str]]:
    out = git(repo, 'log', '--no-merges', '--format=%H%x09%(trailers:key=In-force,valueonly,separator=)', branch, '--', act)
    return [(h, d.strip()) for h, d in (l.split('\t', 1) for l in out.splitlines()) if d.strip()]


def all_commits_by_act(repo: Path, branch: str, acts: list[str]) -> dict[str, list[tuple[str, str]]]:
    """commits_by_act() for every act from one `git log --name-only` walk instead of one walk per act (a corpus of a
    few thousand acts spent most of its check time there). Same commits, same order: a commit belongs to an act when
    it touches a path at or under it; --no-renames lists both sides of a move, as the per-act path filter sees it."""
    want = set(acts)
    rows: dict[str, list[tuple[str, str]]] = {a: [] for a in acts}
    out = git(repo, 'log', '--no-merges', '--no-renames', '--name-only',
              '--format=%x00%H%x09%(trailers:key=In-force,valueonly,separator=)', branch)
    for rec in out.split('\x00')[1:]:
        head, _, names = rec.partition('\n')
        h, _, d = head.partition('\t')
        d = d.strip()
        if not d:
            continue
        hit = set()
        for name in names.splitlines():
            parts = name.split('/')
            for i in range(1, len(parts) + 1):
                p = '/'.join(parts[:i])
                if p in want:
                    hit.add(p)
        for a in hit:
            rows[a].append((h, d))
    return rows


def state_on(rows: list[tuple[str, str]], day: str) -> str | None:
    for h, d in rows:
        if d <= day:
            return h
    return None


def tree_files(repo: Path, commit: str, act: str) -> list[str]:
    return [f for f in git(repo, 'ls-tree', '-r', '--name-only', commit, f'{act}/').split('\n')
            if f.endswith('.md') and f != f'{act}/README.md']


def blob_oid(text: str) -> str:
    """The id git gives a file with this text, so a file is compared by id without reading it back."""
    b = text.encode('utf-8')
    return hashlib.sha1(b'blob %d\0' % len(b) + b).hexdigest()


def tree_oids(cat: 'Cat', commit: str, act: str, cache: dict) -> dict[str, str]:
    """{path: blob id} of every .md under act/ (README.md excepted) at commit, read through the cat-file process
    already open (no `git ls-tree` per version) and cached per (commit, act): the day before a version is usually the
    commit of the version before it."""
    key = (commit, act)
    if key not in cache:
        out: dict[str, str] = {}

        def walk(spec: str, prefix: str):
            data = cat.read(spec)
            if data is None:
                return
            i = 0
            while i < len(data):
                sp = data.index(b' ', i)
                nul = data.index(b'\0', sp)
                mode, name, oid = data[i:sp], data[sp + 1:nul].decode('utf-8'), data[nul + 1:nul + 21].hex()
                i = nul + 21
                path = f'{prefix}/{name}'
                if mode == b'40000':
                    walk(oid, path)
                elif mode != b'160000':
                    out[path] = oid
        walk(f'{commit}:{act}', act)
        cache[key] = {f: o for f, o in out.items() if f.endswith('.md') and f != f'{act}/README.md'}
    return cache[key]


def check(repo: Path, corpus: Path) -> dict:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from build import load  # the same corpus.json + corpus.d/ merge the build used
    c, raw = load(corpus.parent)
    future = c['country'].get('future_branch', 'futuro')
    has_future = bool(git(repo, 'branch', '--list', future).strip())
    cat = Cat(repo)
    trees: dict = {}
    mismatches, versions, details = 0, 0, []
    by_act = all_commits_by_act(repo, future if has_future else 'main', [a['slug'] for a in c['acts']])
    for act in c['acts']:
        slug = act['slug']
        rows = by_act[slug]
        prev = None
        vs = act['versions']
        for i, v in enumerate(vs):
            versions += 1
            # With same-day versions only the last one of the day is the text in force at the end of that day, and
            # the day before reads as the last version before the day.
            if i + 1 < len(vs) and vs[i + 1]['from'] == v['from']:
                continue
            before = next((w for w in reversed(vs[:i]) if w['from'] < v['from']), None)
            for day, want in ((v['from'], v), ((dt.date.fromisoformat(v['from']) - dt.timedelta(days=1)).isoformat(), before)):
                h = state_on(rows, day)
                if want is None:
                    if h is not None:
                        mismatches += 1
                        details.append(f'{slug}: something is in force on {day}, before the first version')
                    continue
                if h is None:
                    mismatches += 1
                    details.append(f'{slug}: nothing in force on {day}')
                    continue
                files = tree_oids(cat, h, slug, trees)
                expect = {f'{slug}/{k}.md': blob_oid(u['text']) for k, u in want['units'].items()}
                for f in sorted(set(files) | set(expect)):
                    if files.get(f) != expect.get(f):
                        mismatches += 1
                        if len(details) < 50:
                            details.append(f'{slug} on {day}: {f} differs from version {want["from"]}')
            prev = v
    cat.close()
    trailer_errors, missing_in_force = 0, 0
    refs = ['main'] + ([future] if has_future else [])
    out = git(repo, 'log', '--no-merges', '--format=%H%x1f%an%x1f%(trailers:only,unfold,separator=%x1e)%x1d', *refs)
    for rec in out.split('\x1d'):
        rec = rec.strip('\n')
        if not rec:
            continue
        h, an, tr = rec.split('\x1f')
        if an == 'Lexifina':
            continue
        keys = [t.split(':', 1)[0] for t in tr.split('\x1e') if t]
        if not keys:
            trailer_errors += 1
        elif 'In-force' not in keys:
            missing_in_force += 1
    merges = int(git(repo, 'rev-list', '--merges', '--count', 'main').strip())
    cts = [int(x) for x in git(repo, 'log', '--first-parent', '--reverse', '--format=%ct', 'main').split()]
    backwards = sum(1 for a, b in zip(cts, cts[1:]) if b < a)
    now = int(time.time())
    # The last commit is the docs commit, dated noon local time on --docs-date; built the same day before noon it is
    # a few hours ahead of now. Allow it up to two days; every law commit must be in the past.
    future_dated = sum(1 for x in cts[:-1] if x > now) + (1 if cts and cts[-1] > now + 2 * 86400 else 0)
    return {'acts': len(c['acts']), 'versions': versions, 'mismatches': mismatches, 'trailer_errors': trailer_errors,
            'missing_in_force': missing_in_force, 'merges': merges, 'backwards': backwards,
            'future_dated': future_dated, 'details': details,
            # Which corpus this check read (a main build reads only the verified parts), so REPRODUCE.md quotes a check
            # only in the build it describes.
            'corpus_sha256': hashlib.sha256(raw).hexdigest()}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('repo')
    ap.add_argument('--corpus', required=True)
    ap.add_argument('--write', action='store_true', help='record the result in verification.json beside corpus.json')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    res = check(Path(args.repo), Path(args.corpus))
    print(json.dumps(res, indent=1, ensure_ascii=False))
    ok = not (res['mismatches'] or res['trailer_errors'] or res['missing_in_force'] or res['merges'] or res['backwards']
              or res['future_dated'])
    if args.write:
        p = Path(args.corpus).parent / 'verification.json'
        ver = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        ver['check'] = {k: v for k, v in res.items() if k != 'details'}
        p.write_text(json.dumps(ver, indent=1, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
    raise SystemExit(0 if ok else 1)


if __name__ == '__main__':
    main()
