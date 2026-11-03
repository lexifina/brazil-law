"""Part sign-offs, optionally bound to the exact JSON bytes reviewed.

Unhashed markers remain valid for compatibility. Only a separate reviewer should
call write(); collectors should submit .PUBLISH.pending files instead.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import os
import re
import tempfile
from pathlib import Path


def status(part: Path, *, content: bytes | None = None) -> tuple[str, str]:
    """Return legacy/match/mismatch/absent and a reportable explanation.

    content lets a loader check the very bytes it will consume, avoiding a second
    read of a changing part. Keep Path subclasses (the append gate's snapshot).
    """
    marker = part.with_suffix('.PUBLISH')
    try:
        raw = marker.read_bytes()
    except FileNotFoundError:
        return 'absent', f'{marker.name}: no marker'
    except OSError as exc:
        return 'mismatch', f'{marker.name}: cannot read marker: {exc}'
    lines = [line.strip() for line in raw.decode('utf-8-sig', errors='replace').splitlines()]
    hashes = [line for line in lines if line.lower().startswith('sha256:')]
    if not hashes:
        return 'legacy', f'{marker.name}: legacy marker without sha256'
    if len(hashes) != 1 or not re.fullmatch(r'sha256:[0-9a-f]{64}', hashes[0]):
        return 'mismatch', f'{marker.name}: expected one sha256: line with 64 lowercase hex digits'
    expected = hashes[0][len('sha256:'):]
    try:
        actual = hashlib.sha256(part.read_bytes() if content is None else content).hexdigest()
    except OSError as exc:
        return 'mismatch', f'{part.name}: cannot read part: {exc}'
    if actual != expected:
        return 'mismatch', f'{part.name}: sha256 mismatch: reviewed {expected}, current {actual}'
    return 'match', f'{part.name}: sha256:{actual}'


def verified(part: Path) -> bool:
    return status(part)[0] in ('legacy', 'match')


def write(part: Path, reviewer: str) -> None:
    """Atomically replace the sign-off, hashing bytes without text normalization."""
    if len(reviewer.splitlines()) > 1 or '\r' in reviewer or '\n' in reviewer:
        raise ValueError('reviewer must be a single line')
    digest = hashlib.sha256(part.read_bytes()).hexdigest()
    at = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    data = f'sha256:{digest}\nreviewer: {reviewer}\nat: {at}\n'.encode('utf-8')
    marker = part.with_suffix('.PUBLISH')
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(dir=marker.parent, prefix=f'.{marker.name}.', suffix='.tmp',
                                         delete=False) as stream:
            tmp = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, marker)
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)
