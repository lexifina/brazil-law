"""Prints the law as it stood on a day, read from this repository's history.

    python tools/on.py 2015-06-01                      # every act's commit in force that day
    python tools/on.py 2015-06-01 constitucion         # the whole act on that day
    python tools/on.py 2015-06-01 constitucion art-019 # one provision (a file name without .md)
    python tools/on.py 2015-06-01 constitucion 19      # the same, by article number
    python tools/on.py --law 2015-06-01 constitucion art-019  # also name the law behind the version shown

Each commit carries the day its change took effect in an `In-force:` trailer. That trailer, not the commit date, is
the source of truth: git cannot store dates before 1970, and reading the trailer avoids time-zone edge cases. The text
in force on a day is the last commit on or before it that touches the act. Laws published but not yet in force live on
the future branch, which is read for days after the newest commit on main. Merge commits are ignored. Standard library
only.
"""
import datetime as dt
import re
import subprocess
import sys


def git(*args: str) -> str:
    return subprocess.run(['git', *args], capture_output=True, text=True, encoding='utf-8', check=True).stdout


def branches() -> tuple[str, str | None]:
    """main, and the future branch named in data/repo.json (local or origin/), if it exists."""
    import json
    try:
        name = json.loads(git('show', 'main:data/repo.json')).get('future_branch')
    except (subprocess.CalledProcessError, ValueError):
        name = None
    if not name:
        return 'main', None
    for ref in (name, f'origin/{name}'):
        if subprocess.run(['git', 'rev-parse', '-q', '--verify', ref], capture_output=True).returncode == 0:
            return 'main', ref
    return 'main', None


def history(branch: str, path: str) -> list[tuple[str, str, str]]:
    """(commit, in-force day, author) for every commit touching path, newest first."""
    out = git('log', '--no-merges', '--format=%H%x09%(trailers:key=In-force,valueonly,separator=)%x09%an', branch, '--', path)
    rows = []
    for line in out.splitlines():
        h, d, a = (line.split('\t') + ['', ''])[:3]
        if d.strip():
            rows.append((h, d.strip(), a))
    return rows


def commit_on(day: str, path: str) -> tuple[str, str, str] | None:
    main, future = branches()
    rows = history(main, path)
    if future and (not rows or day > rows[0][1]):
        rows = history(future, path) or rows
    for h, d, a in rows:
        if d <= day:
            return h, d, a
    return None


def resolve(commit: str, act: str, unit: str) -> str | None:
    files = git('ls-tree', '-r', '--name-only', commit, f'{act}/').split('\n')
    exact = f'{act}/{unit}.md'
    if exact in files:
        return exact
    m = re.fullmatch(r'(\d+)(.*)', unit)
    if m:
        want = re.compile(rf'{re.escape(act)}/[a-z-]*0*{int(m.group(1))}{re.escape(m.group(2))}\.md$')
        hits = [f for f in files if want.match(f)]
        # A bare number means the article: "19" is art-019, not a transitional provision numbered 19.
        arts = [f for f in hits if f.split('/', 1)[1].startswith(('art-', 'art'))]
        if len(arts) == 1:
            return arts[0]
        if len(hits) == 1:
            return hits[0]
        if hits:
            sys.exit(f'{unit} is ambiguous in {act}: {", ".join(h.split("/", 1)[1][:-3] for h in hits)}. Give the file name.')
    return None


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = sys.argv[1:]
    show_law = '--law' in args
    args = [a for a in args if a != '--law']
    if not args:
        sys.exit(__doc__)
    day = args[0]
    try:
        dt.date.fromisoformat(day)
    except ValueError:
        sys.exit(f'{day!r} is not a date (YYYY-MM-DD).')
    if len(args) == 1:
        acts = sorted({p.split('/')[0] for p in git('ls-tree', '-r', '--name-only', 'main').split('\n')
                       if '/' in p and p.split('/')[0] not in ('data', 'tools')})
        for act in acts:
            hit = commit_on(day, act)
            print(f'{act}\t' + (f'{hit[1]}\t{hit[0][:10]}\t{hit[2]}' if hit else 'not in force yet'))
        return
    act = args[1]
    hit = commit_on(day, act)
    if not hit:
        sys.exit(f'{act} is not in the record on {day}: it took effect later, or the name is wrong (see `python tools/on.py {day}`).')
    commit = hit[0]
    if len(args) > 2:
        path = resolve(commit, act, args[2])
        if not path:
            sys.exit(f'{act}/{args[2]} was not in the text on {day} (it may have been inserted later or removed earlier).')
        if show_law:
            last = commit_on(day, path)
            print(f'# in force from {last[1]}, last changed by {last[2]} ({last[0][:10]})\n')
        sys.stdout.write(git('show', f'{commit}:{path}'))
        return
    files = [f for f in git('ls-tree', '-r', '--name-only', commit, f'{act}/').split('\n')
             if f.endswith('.md') and not f.endswith('/README.md')]
    for f in sorted(files):
        sys.stdout.write(git('show', f'{commit}:{f}') + '\n')


if __name__ == '__main__':
    main()
