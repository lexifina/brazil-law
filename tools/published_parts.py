"""Keep previously published inputs verified before planning an append."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess

import publish_marker

MANIFEST = 'data/parts.json'


class PublishedPartError(ValueError):
    pass


def _document(repo: Path, head: str, path: str):
    def git(*args):
        return subprocess.run(['git', *args], cwd=repo, capture_output=True, check=True,
                              encoding='utf-8', timeout=120).stdout
    if not git('ls-tree', '--name-only', head, '--', path).strip():
        return None
    return json.loads(git('show', f'{head}:{path}'))


def all_parts(folder: Path) -> list[Path]:
    # Frozen exposes even rejected inputs, with their captured bytes and markers.
    snapshot = getattr(folder, 'publication_parts', None)
    return list(snapshot()) if snapshot else sorted((folder / 'corpus.d').glob('*.json'))


def _slugs(path: Path) -> set[str]:
    data = json.loads(path.read_bytes())
    return {a['slug'] for a in data.get('acts', [])}


def required(repo: Path, folder: Path, head: str = 'main') -> set[str]:
    """Read ownership from the committed main, never from a newly filtered build.

    Older builds have no part manifest. Infer their ownership from committed act
    metadata and the unfiltered inputs; missing ownership must stop, not withdraw
    published acts. The next successful docs commit records exact part names.
    """
    paths = {p.name: p for p in all_parts(folder)}
    previous = _document(repo, head, MANIFEST)
    if previous is not None:
        if (not isinstance(previous, dict) or previous.get('schema') != 1
                or not isinstance(previous.get('parts'), dict)):
            raise PublishedPartError(f'{head}:{MANIFEST}: invalid published part manifest')
        names = set(previous['parts'])
        if any(Path(name).name != name or '/' in name or '\\' in name or not name.endswith('.json') for name in names):
            raise PublishedPartError(f'{head}:{MANIFEST}: invalid published part name')
    else:
        versions = _document(repo, head, 'data/versions.json')
        if versions is None:
            raise PublishedPartError(f'{head}: no published input/act metadata; cannot verify previous parts')
        published = {a['slug'] for a in versions['acts']}
        names, covered = set(), set()
        base = folder / 'corpus.json'
        try:
            covered.update(_slugs(base))
        except FileNotFoundError:
            pass
        for name, path in paths.items():
            try:
                slugs = _slugs(path)
            except (OSError, ValueError, KeyError, TypeError):
                slugs = set()  # an unverified new part may still be being written
            if slugs & published:
                names.add(name)
            covered.update(slugs)
        missing = published - covered
        if missing:
            candidates = [f'{name}: {publish_marker.status(path)[1]}' for name, path in paths.items()
                          if not publish_marker.verified(path)]
            detail = '; '.join(candidates) or 'the previous part name is unavailable in this legacy build'
            raise PublishedPartError('published acts have lost input ownership: '
                                     + ', '.join(sorted(missing)) + '; ' + detail)
    failures = []
    for name in sorted(names):
        if name not in paths:
            failures.append(f'{name}: absent part file (previously published)')
            continue
        state, detail = publish_marker.status(paths[name])
        if state not in ('legacy', 'match'):
            failures.append(f'{name}: {state}: {detail}')
    if failures:
        raise PublishedPartError('previously published part is no longer verified; append stopped: '
                                 + '; '.join(failures))
    return names
