"""Prints the law of Brazil as it stood on a given day, read from this repository's history.

    python tools/vigente_em.py 2015-01-01 constituicao 6         # art. 6 of the Constitution on 1 January 2015
    python tools/vigente_em.py 2016-01-01 constituicao art-006   # the same, by file name
    python tools/vigente_em.py 2000-01-01 constituicao adct-2    # art. 2 of the ADCT
    python tools/vigente_em.py 1995-01-01 constituicao           # the whole Constitution on 1 January 1995
    python tools/vigente_em.py --law 2016-01-01 constituicao 6   # also name the amendment behind that wording

A thin wrapper around tools/on.py: the version is chosen by each commit's `In-force:` trailer, never by its commit
date, and branches named wip* are ignored. A bare article number (`6`, `29-A` written `29-a`) means the article of the
main text (`art-006`, `art-029-a`); `adct-2` means art. 2 of the Ato das Disposições Constitucionais Transitórias.
Standard library only.
"""
import re
import runpy
import sys
from pathlib import Path


def unit(arg: str) -> str:
    m = re.fullmatch(r'(adct-)?(\d+)(-[a-z]+)?', arg.lower())
    if not m:
        return arg
    return f'{"adct-" if m.group(1) else ""}art-{int(m.group(2)):03d}{m.group(3) or ""}'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    args = [a for a in sys.argv[1:] if a != '--law']
    if len(args) == 3:
        i = len(sys.argv) - 1 - sys.argv[::-1].index(args[2])
        sys.argv[i] = unit(args[2])
    sys.argv[0] = str(Path(__file__).with_name('on.py'))
    runpy.run_path(sys.argv[0], run_name='__main__')
