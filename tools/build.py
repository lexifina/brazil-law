"""Builds a git-for-law repository from a country's corpus.json (see SCHEMA.md).

    python -X utf8 scripts/gitlaw_common/build.py scripts/<slug>-law --repo ~/Documents/<slug>-law --docs-date YYYY-MM-DD
    python -X utf8 scripts/gitlaw_common/build.py scripts/<slug>-law --repo <empty tmp> --docs-date D --compare <repo>

One commit per law per in-force day (across all acts), authored by the law at an address that cannot exist, dated noon
local time on the day it took effect; changes no law explains are committed by the publisher and labelled. Commits are
streamed into one `git fast-import`, so the same corpus gives the same hashes. Laws not yet in force on --docs-date go
on the future branch. The last commit on main adds the documentation, the tools and REPRODUCE.md, dated --docs-date.
Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
try:
    import private  # noqa: E402  (Lexifina's list of what stays off shared repos)
except ImportError:  # a published copy of this builder runs without it
    private = None
KEY = re.compile(r'^[a-z0-9][a-z0-9-]*$')
KINDS = {'law', 'decree', 'court', 'referendum', 'publisher', 'treaty'}
SUBJECT_MAX = 72


class CorpusError(SystemExit):
    pass


# ---------------------------------------------------------------- loading and validation

def load(folder: Path) -> tuple[dict, bytes]:
    """corpus.json, plus any parts in corpus.d/*.json (so several agents can each own some acts of one country).

    A part holds `acts`, and optionally `laws`, `sources`, `applies`, `decisions` and `ai_use`. Its laws are merged
    by key; the same key in two files must describe the same law (same label). Parts are read in file-name order. The
    returned bytes are what the build hashes: corpus.json followed by each part, so any change to any part changes it.
    """
    main_path = folder / 'corpus.json'
    parts = sorted((folder / 'corpus.d').glob('*.json')) if (folder / 'corpus.d').exists() else []
    if os.environ.get('GITLAW_VERIFIED_PARTS_ONLY') == '1':
        # The main-branch build: only parts their owner has verified against the official text (<part>.PUBLISH).
        parts = [p for p in parts if p.with_suffix('.PUBLISH').exists()]
    if not main_path.exists() and not parts:
        raise CorpusError(f'{folder} has no corpus.json')
    raw = main_path.read_bytes() if main_path.exists() else b''
    c = json.loads(raw.decode('utf-8')) if raw else {}
    for p in parts:
        b = p.read_bytes()
        raw += b'\n' + p.name.encode() + b'\n' + b
        part = json.loads(b.decode('utf-8'))
        if not c.get('country') and part.get('country'):
            c['country'] = part['country']
        for key, law in part.get('laws', {}).items():
            have = c.setdefault('laws', {}).get(key)
            if have and have.get('label') != law.get('label'):
                raise CorpusError(f'{p.name}: law {key!r} is {law.get("label")!r} here but {have.get("label")!r} elsewhere')
            c['laws'].setdefault(key, law)
        for field in ('acts', 'sources', 'applies', 'decisions', 'ai_use'):
            c.setdefault(field, []).extend(part.get(field, []))
    # A version without `units` is an event that changed no words (a ruling, a rejected referendum): it reads as the
    # version before it, so the corpus need not repeat the whole text.
    # A version may instead give only `changes`: {unit key: unit, or null to remove it}, applied to the version before
    # it. Large acts then store each version's delta, not every provision again.
    for act in c.get('acts', []):
        for prev, v in zip(act.get('versions', []), act.get('versions', [])[1:]):
            if 'units' in v:
                continue
            units = dict(prev['units'])
            for k, u in (v.get('changes') or {}).items():
                if u is None:
                    units.pop(k, None)
                else:
                    units[k] = u
            v['units'] = units
    return c, raw


def validate(c: dict) -> list[str]:
    """Every rule in SCHEMA.md the builder relies on. Returns the problems; the build stops if there are any."""
    errs = []
    co = c.get('country', {})
    for k in ('code', 'name', 'slug', 'lang', 'tz', 'publisher'):
        if not co.get(k):
            errs.append(f'country.{k} is missing')
    try:
        ZoneInfo(co.get('tz', 'UTC'))
    except Exception:
        errs.append(f'country.tz {co.get("tz")!r} is not a time zone')
    laws = c.get('laws', {})
    for key, law in laws.items():
        if not KEY.match(key):
            errs.append(f'law key {key!r} must be lowercase ASCII [a-z0-9-]')
        if law.get('kind', 'law') not in KINDS:
            errs.append(f'law {key}: kind {law.get("kind")!r} not in {sorted(KINDS)}')
        if not law.get('label'):
            errs.append(f'law {key}: label is missing')
        for d in ('enacted', 'published', 'temporary_until'):
            if law.get(d) and not _is_date(law[d]):
                errs.append(f'law {key}: {d} {law[d]!r} is not YYYY-MM-DD')
        if law.get('restores') and law['restores'] not in laws:
            errs.append(f'law {key}: restores {law["restores"]!r} is not a law key')
    slugs = set()
    for act in c.get('acts', []):
        s = act.get('slug', '')
        if not KEY.match(s) or s in slugs or s in {'data', 'tools'}:
            errs.append(f'act slug {s!r} must be unique lowercase ASCII and not data/tools')
        slugs.add(s)
        for k in ('short', 'title'):
            if not act.get(k):
                errs.append(f'act {s}: {k} is missing')
        if act.get('first_law') and act['first_law'] not in laws:
            errs.append(f'act {s}: first_law {act["first_law"]!r} is not a law key')
        if 'publisher' in act and not (isinstance(act['publisher'], dict) and act['publisher'].get('name')
                                       and '@' in str(act['publisher'].get('email', ''))):
            errs.append(f'act {s}: publisher needs a name and an email')
        for l in act.get('earlier_laws', []):
            if l not in laws:
                errs.append(f'act {s}: earlier law {l!r} is not a law key')
        vs = act.get('versions', [])
        if not vs:
            errs.append(f'act {s}: no versions')
        days = [v.get('from', '') for v in vs]
        same = [i for i, v in enumerate(vs) if i and v.get('same_day')]
        if days != sorted(days) or any(a == b and not vs[i + 1].get('same_day') for i, (a, b) in enumerate(zip(days, days[1:]))):
            errs.append(f'act {s}: versions must be in order, with distinct "from" days unless marked "same_day": true')
        for i in same:
            if days[i] != days[i - 1]:
                errs.append(f'act {s}: version {i} is marked same_day but does not share its day with the version before')
        for v in vs:
            if not _is_date(v.get('from', '')):
                errs.append(f'act {s}: version from {v.get("from")!r} is not YYYY-MM-DD')
            for uk, u in v.get('units', {}).items():
                if not KEY.match(uk) or uk == 'readme':
                    errs.append(f'act {s} {v.get("from")}: unit key {uk!r} must be lowercase ASCII [a-z0-9-]')
                t = u.get('text', '')
                if not t.endswith('\n') or '\r' in t:
                    errs.append(f'act {s} {v.get("from")} {uk}: text must end with \\n and contain no \\r')
                if not u.get('label'):
                    errs.append(f'act {s} {v.get("from")} {uk}: label is missing')
            for uk, ls in v.get('credits', {}).items():
                for l in ls:
                    if l not in laws:
                        errs.append(f'act {s} {v.get("from")} {uk}: credited law {l!r} is not a law key')
    for a in c.get('applies', []):
        if a.get('law') not in laws:
            errs.append(f'applies: law {a.get("law")!r} is not a law key')
    return errs


def _is_date(s) -> bool:
    try:
        dt.date.fromisoformat(s)
        return len(s) == 10
    except (TypeError, ValueError):
        return False


# ---------------------------------------------------------------- planning the commits

def law_order(laws: dict, key: str) -> tuple:
    law = laws[key]
    return (law.get('published') or law.get('enacted') or '9999', law.get('enacted') or '9999', key)


def plan(c: dict) -> list[dict]:
    """Every commit in order: (day, rank, ...) where rank 0 = an act's first version, 1 = a law, 2 = unexplained."""
    laws = c['laws']
    by_day_law: dict[tuple[str, str], dict] = {}
    commits = []
    for act in c['acts']:
        vs = act['versions']
        first = vs[0]
        commits.append({'day': first['from'], 'rank': 0, 'sort': act['slug'], 'kind': 'start', 'act': act,
                        'version': first})
        for vi, (prev, cur) in enumerate(zip(vs, vs[1:]), start=1):
            sd = sum(1 for j in range(1, vi + 1) if vs[j]['from'] == cur['from'] and vs[j].get('same_day'))
            pu, cu = prev['units'], cur['units']
            changed = sorted(k for k in set(pu) | set(cu) if pu.get(k, {}).get('text') != cu.get(k, {}).get('text'))
            credits = cur.get('credits', {})
            groups: dict[str, list[str]] = {}
            also: dict[str, list[str]] = {}
            unexplained = []
            for k in changed:
                ls = sorted(set(credits.get(k, [])), key=lambda l: law_order(laws, l))
                if not ls:
                    unexplained.append(k)
                    continue
                groups.setdefault(ls[-1], []).append(k)
                if len(ls) > 1:
                    also[k] = ls[:-1]
            # Laws credited for this version that changed no words still get a commit, so the record says so; the
            # provisions they are credited to are named in its Affecting trailer.
            named: dict[str, list[str]] = {}
            for k, ls in sorted(credits.items()):
                for l in ls:
                    named.setdefault(l, []).append(k)
                    if l not in groups and not any(l in a for a in also.values()):
                        groups.setdefault(l, [])
            for law, keys in groups.items():
                slot = by_day_law.setdefault((cur['from'], sd, law), {
                    'day': cur['from'], 'k': sd, 'rank': 1, 'sort': law_order(laws, law), 'kind': 'law', 'law': law, 'parts': []})
                slot['parts'].append({'act': act, 'prev': prev, 'cur': cur, 'keys': keys,
                                      'also': {k: also[k] for k in keys if k in also},
                                      'named': [k for k in named.get(law, []) if k not in keys and (k in cur['units'] or k in prev['units'])]})
            if unexplained:
                commits.append({'day': cur['from'], 'k': sd, 'rank': 2, 'sort': act['slug'], 'kind': 'unexplained',
                                'parts': [{'act': act, 'prev': prev, 'cur': cur, 'keys': unexplained, 'also': {}}]})
    commits.extend(by_day_law.values())
    # Same-day versions (marked "same_day") come after the version before them on that day: k counts them.
    commits.sort(key=lambda x: (x['day'], x.get('k', 0), x['rank'], str(x['sort'])))
    return commits


# ---------------------------------------------------------------- messages

def law_email(c: dict, key: str) -> str:
    dom = c['country']['publisher']['email'].split('@', 1)[1]
    return f'{key}@{dom}'


def unit_label(u: dict) -> str:
    return u.get('label') or ''


def kind_of(prev: dict | None, cur: dict | None) -> str:
    return 'Inserted' if prev is None else 'Removed' if cur is None else 'Changed'


def subject(prefix: str, labels: list[str], suffix: str) -> str:
    s = f'{prefix}: {", ".join(labels)}{suffix}'
    if len(s) <= SUBJECT_MAX:
        return s
    s = f'{prefix}: {len(labels)} provisions{suffix}'
    if len(s) <= SUBJECT_MAX:
        return s
    return s[:SUBJECT_MAX - 1] + '…'


def short_subject(s: str) -> str:
    return s if len(s) <= SUBJECT_MAX else s[:SUBJECT_MAX - 1] + '…'


def wrap(text: str, width: int = 100) -> list[str]:
    out, line = [], ''
    for w in text.split():
        if line and len(line) + 1 + len(w) > width:
            out.append(line)
            line = w
        else:
            line = f'{line} {w}' if line else w
    return out + ([line] if line else [])


def law_trailers(c: dict, key: str, day: str) -> list[str]:
    law = c['laws'][key]
    t = [f'Law: {law["label"]}', f'Kind: {law.get("kind", "law")}']
    if law.get('enacted'):
        t.append(f'Enacted: {law["enacted"]}')
    if law.get('published'):
        t.append(f'Published: {law["published"]}')
    t.append(f'In-force: {day}')
    if law.get('temporary_until'):
        t.append(f'Temporary-until: {law["temporary_until"]}')
    if law.get('restores'):
        t.append(f'Restores: {c["laws"][law["restores"]]["label"]}')
    if law.get('url'):
        t.append(f'Source: {law["url"]}')
    return t


def applies_trailers(c: dict, key: str, parts: list[dict]) -> list[str]:
    out = []
    touched = {(p['act']['slug'], k) for p in parts for k in p['keys']}
    for a in c.get('applies', []):
        if a['law'] != key:
            continue
        prov = a.get('provision', '')
        if prov and not any(k == prov or f'{s}/{k}' == prov for s, k in touched):
            continue
        for g in a.get('groups', []):
            conds = '; '.join(f'{x["kind"].replace("_", "-")} {x.get("date", "")}'.strip() for x in g.get('conditions', []))
            out.append(f'Applies: {prov or "all"} | {conds or "any-commencement"} | set-by {g.get("set_by", "")}'.rstrip(' |'))
    return out


def pre_1970(day: str) -> list[str]:
    if day >= '1970-01-01':
        return []
    return ['Git cannot store a date before 1970, so this commit is dated 1 January 1970, a second after the one',
            'before it. The day the change took effect is in the In-force trailer, which tools/on.py reads.', '']


def start_message(c: dict, x: dict) -> tuple[tuple[str, str], list[str], list[str]]:
    act, v = x['act'], x['version']
    pub = act.get('publisher') or c['country']['publisher']
    labels = []
    if act.get('first_law'):
        key = act['first_law']
        law = c['laws'][key]
        author = (law['label'], law_email(c, key))
        msg = [short_subject(f'{act["short"]} as enacted ({law["label"]})'), '',
               *wrap(f'{act["title"]}: the text as enacted, in force from {v["from"]}.'), '']
        trailers = law_trailers(c, key, v['from'])
    else:
        author = (pub['name'], pub['email'])
        msg = [short_subject(f'{act["short"]}: oldest version available, {v["from"]}'), '',
               *wrap(f'{act["title"]} in the oldest version the source publishes as text, in force from {v["from"]}. '
                     'Earlier versions are not available as text, so this commit is not credited to a law.'), '']
        if act.get('earlier_laws'):
            msg += ['The source names these laws as having produced this text:', '']
            msg += [f'- {c["laws"][l]["label"]}: {c["laws"][l].get("title", "")}'.rstrip(': ') for l in act['earlier_laws']]
            msg.append('')
        trailers = ['Kind: publisher', f'In-force: {v["from"]}']
    if v.get('note'):
        msg += [*wrap(v['note']), '']
    msg += pre_1970(v['from'])
    trailers += [f'Act: {act["short"]}', f'Provisions: {len(v["units"])}']
    if v.get('source_url'):
        trailers.append(f'Consolidated: {v["source_url"]}')
    return author, msg, trailers


def change_message(c: dict, x: dict) -> tuple[tuple[str, str], list[str], list[str]]:
    day = x['day']
    parts = x['parts']
    # An act may name its own publisher (its text comes from a different source than the country's); a commit that
    # spans acts with different publishers uses the country's.
    pubs = {json.dumps(p['act'].get('publisher') or c['country']['publisher'], sort_keys=True) for p in parts}
    pub = json.loads(pubs.pop()) if len(pubs) == 1 else c['country']['publisher']
    shorts = sorted({p['act']['short'] for p in parts})
    labels_by_part = [[unit_label(p['cur']['units'].get(k) or p['prev']['units'][k]) for k in p['keys']] for p in parts]
    all_labels = [l for ls in labels_by_part for l in ls]
    affecting = '; '.join(f'{p["act"]["short"]} {", ".join(ls)}' for p, ls in zip(parts, labels_by_part) if ls)
    named = [[unit_label(p['cur']['units'].get(k) or p['prev']['units'][k]) for k in p.get('named', [])] for p in parts]
    concerns = '; '.join(f'{p["act"]["short"]} {", ".join(ls)}' for p, ls in zip(parts, named) if ls)
    if not affecting:
        # A law that changed no words: name the provisions it is credited to (a ruling, a rejected referendum).
        affecting, concerns = concerns, ''
    lines = []
    for p, ls in zip(parts, labels_by_part):
        by_kind: dict[str, list[str]] = {}
        for k, l in zip(p['keys'], ls):
            by_kind.setdefault(kind_of(p['prev']['units'].get(k), p['cur']['units'].get(k)), []).append(l)
        for name in ('Inserted', 'Changed', 'Removed'):
            if name in by_kind:
                lines += wrap(f'{p["act"]["short"]}, {name.lower()}: {", ".join(by_kind[name])}')
    trailers = []
    if x['kind'] == 'law':
        key = x['law']
        law = c['laws'][key]
        author = (law['label'], law_email(c, key))
        about = [l for ls in named for l in ls]
        if not all_labels and about:
            msg = [subject(' + '.join(shorts), about, f', wording unchanged ({law["label"]})'), '']
        elif len(shorts) == 1 or not all_labels:
            msg = [subject(' + '.join(shorts), all_labels or ['wording unchanged'], f' ({law["label"]})'), '']
        else:
            full = '; '.join(f'{p["act"]["short"]} {", ".join(ls)}' for p, ls in zip(parts, labels_by_part) if ls)
            s = f'{full} ({law["label"]})'
            msg = [s if len(s) <= SUBJECT_MAX else subject(' + '.join(shorts), all_labels, f' ({law["label"]})'), '']
        if law.get('title'):
            msg += [*wrap(law['title']), '']
        msg += lines + ([''] if lines else [])
        if not all_labels and not law.get('note'):
            msg += ['The source lists this law for the version from this day, but none of the words of the text changed.', '']
        kind = law.get('kind', 'law')
        if law.get('note'):
            # The corpus's own description wins: a ruling that only interprets, a referendum that was rejected.
            msg += [*wrap(law['note']), '']
        elif kind == 'court' and all_labels:
            msg += ['A court ruling, not a statute: it struck out or conditioned the text from this day.', '']
        elif kind == 'court':
            msg += ['A court ruling, not a statute. It did not change the words of the text.', '']
        elif kind == 'referendum' and all_labels:
            msg += ['Approved by a popular vote.', '']
        elif kind == 'referendum':
            msg += ['A popular vote. It did not change the words of the text.', '']
        if law.get('temporary_until'):
            msg += [f'A temporary measure, in force until {law["temporary_until"]}.', '']
        if law.get('restores'):
            msg += [f'This restores wording that {c["laws"][law["restores"]]["label"]} had changed.', '']
        if law.get('enacted') and day < law['enacted']:
            msg += [f'In force from {day}, before the law was enacted ({law["enacted"]}): it reaches back.', '']
        also = sorted({l for p in parts for ls in p['also'].values() for l in ls}, key=lambda l: law_order(c['laws'], l))
        if also:
            msg += [*wrap('The source credits these provisions to more than one law that took effect on this day and does '
                          'not separate the changes, so all of them are in this commit, which is credited to the later law: '
                          + ', '.join(c['laws'][l]['label'] for l in also) + '.'), '']
            trailers += [f'Also-amended-by: {c["laws"][l]["label"]}' for l in also]
        trailers = law_trailers(c, key, day) + trailers
        trailers.append(f'Words-changed: {"yes" if all_labels else "no"}')
        trailers += applies_trailers(c, key, parts)
    else:
        author = (pub['name'], pub['email'])
        msg = [subject(shorts[0], all_labels, ' (unexplained)'), '',
               *wrap(f'The consolidated text changed on this day, but no amendment note names a law for it, so the change '
                     f'is not credited to any law. {pub["name"]} published it.'), '', *lines, '']
        trailers = ['Kind: publisher', f'In-force: {day}', 'Words-changed: yes']
    notes = sorted({p['cur'].get('note', '') for p in parts if p['cur'].get('note')})
    for n in notes:
        msg += [*wrap(n), '']
    msg += pre_1970(day)
    if affecting:
        trailers.append(f'Affecting: {affecting}')
    if concerns:
        # Provisions the source credits to this law whose words it left unchanged (e.g. a ruling that also reads one).
        trailers.append(f'Also-concerns: {concerns}')
    trailers += sorted({f'Consolidated: {p["cur"]["source_url"]}' for p in parts if p['cur'].get('source_url')})
    return author, msg, trailers


def check_trailers(trailers: list[str]):
    for t in trailers:
        k, sep, v = t.partition(': ')
        if not sep or not re.fullmatch(r'[A-Za-z][A-Za-z0-9-]*', k) or '\n' in v:
            raise CorpusError(f'bad trailer {t!r}: keys must be ASCII and values one line')


# ---------------------------------------------------------------- dates

class Clock:
    def __init__(self, tz: str):
        self.tz = ZoneInfo(tz)
        self.seq = 0

    def stamp(self, day: str) -> str:
        """Noon local time on the day; before 1970, 1 January 1970 plus one second per commit, in order."""
        d = dt.date.fromisoformat(day)
        if d.year < 1970:
            self.seq += 1
            return f'{self.seq} +0000'
        when = dt.datetime(d.year, d.month, d.day, 12, tzinfo=self.tz)
        off = int(when.utcoffset().total_seconds() // 60)
        sign = '+' if off >= 0 else '-'
        return f'{int(when.timestamp())} {sign}{abs(off) // 60:02d}{abs(off) % 60:02d}'


# ---------------------------------------------------------------- fast-import

class Writer:
    """One `git fast-import` for the whole history; commits are written as they are made and then forgotten."""

    def __init__(self, repo: Path):
        self.p = subprocess.Popen(['git', 'fast-import', '--quiet', '--done', '--date-format=raw'], cwd=repo,
                                  stdin=subprocess.PIPE)
        self.mark = 0
        self.heads: dict[str, int] = {}

    def _w(self, b: bytes):
        self.p.stdin.write(b)

    def _data(self, s: str):
        b = s.encode('utf-8')
        self._w(f'data {len(b)}\n'.encode() + b + b'\n')

    def commit(self, branch: str, author: tuple[str, str], committer: tuple[str, str], when: str, message: str,
               files: dict[str, str | None], parent: int | None = None) -> int:
        self.mark += 1
        self._w(f'commit refs/heads/{branch}\nmark :{self.mark}\n'.encode())
        self._w(f'author {author[0]} <{author[1]}> {when}\n'.encode('utf-8'))
        self._w(f'committer {committer[0]} <{committer[1]}> {when}\n'.encode('utf-8'))
        self._data(message)
        base = parent if parent is not None else self.heads.get(branch)
        if base:
            self._w(f'from :{base}\n'.encode())
        for path in sorted(files):
            text = files[path]
            if text is None:
                self._w(f'D {path}\n'.encode('utf-8'))
            else:
                self._w(f'M 100644 inline {path}\n'.encode('utf-8'))
                self._data(text)
        self.heads[branch] = self.mark
        return self.mark

    def tag(self, name: str, mark: int):
        self._w(f'reset refs/tags/{name}\nfrom :{mark}\n\n'.encode('utf-8'))

    def finish(self):
        self._w(b'done\n')
        self.p.stdin.close()
        if self.p.wait():
            raise CorpusError('git fast-import failed')


# ---------------------------------------------------------------- the repository

def git(repo: Path, *args: str) -> str:
    out = subprocess.run(['git', *args], cwd=repo, capture_output=True, text=True, encoding='utf-8')
    if out.returncode:
        raise CorpusError(f'git {" ".join(args)} failed: {out.stderr}')
    return out.stdout


def prepare(repo: Path) -> str | None:
    """Empties the target, keeping the remote. Refuses a folder that holds anything but an earlier build."""
    remote = None
    if repo.exists() and any(repo.iterdir()):
        if not (repo / '.git').exists():
            raise CorpusError(f'{repo} is not empty and not a git repository; refusing to overwrite it')
        out = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=repo, capture_output=True, text=True)
        remote = out.stdout.strip() or None

        def force(fn, path, _exc):
            os.chmod(path, 0o700)
            fn(path)
        for p in repo.iterdir():
            shutil.rmtree(p, onexc=force) if p.is_dir() else p.unlink()
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, 'init', '-q', '-b', 'main')
    git(repo, 'config', 'core.autocrlf', 'false')
    if remote:
        git(repo, 'remote', 'add', 'origin', remote)
    return remote


def act_files(act: dict, units: dict, prev: dict | None, keys: list[str] | None = None) -> dict[str, str | None]:
    files = {}
    for k in (keys if keys is not None else sorted(set(units) | set(prev or {}))):
        u = units.get(k)
        if prev is not None and prev.get(k, {}).get('text') == (u or {}).get('text'):
            continue
        files[f'{act["slug"]}/{k}.md'] = u['text'] if u else None
    return files


def write_history(repo: Path, c: dict, docs_date: str, commits: list[dict]) -> tuple[Writer, dict, list[dict], Clock]:
    co = c['country']
    committer = ('Lexifina', f'{co["slug"]}-law@lexifina.com')
    clock = Clock(co['tz'])
    w = Writer(repo)
    future = co.get('future_branch', 'futuro')
    tags: dict[str, int] = {}
    log = []
    on_future = False
    for x in commits:
        if x['day'] > docs_date and not on_future:
            # Laws already published but not yet in force go on their own branch, so main is the law on docs_date.
            on_future = True
            if 'main' in w.heads:
                w.heads[future] = w.heads['main']
        branch = future if on_future else 'main'
        if x['kind'] == 'start':
            author, msg, trailers = start_message(c, x)
            files = act_files(x['act'], x['version']['units'], None)
            touched = [x['act']['slug']]
        else:
            author, msg, trailers = change_message(c, x)
            files = {}
            for p in x['parts']:
                files.update(act_files(p['act'], p['cur']['units'], p['prev']['units'], p['keys']))
            touched = [p['act']['slug'] for p in x['parts']]
        check_trailers(trailers)
        text = '\n'.join(msg).rstrip('\n') + '\n\n' + '\n'.join(trailers) + '\n'
        mark = w.commit(branch, author, committer, clock.stamp(x['day']), text, files)
        for s in touched:
            tags[f'{s}/{x["day"]}'] = mark
        if x['kind'] == 'law':
            tags.setdefault(f'law/{x["law"]}', mark)
        elif x['kind'] == 'start' and x['act'].get('first_law'):
            tags.setdefault(f'law/{x["act"]["first_law"]}', mark)
        log.append({'day': x['day'], 'kind': x['kind'], 'law': x.get('law') or (x['act'].get('first_law') if x['kind'] == 'start' else None),
                    'acts': touched, 'units': len(files), 'branch': branch, 'clamped': x['day'] < '1970-01-01'})
    return w, tags, log, clock


# ---------------------------------------------------------------- documentation commit

def tables(c: dict, log: list[dict]) -> dict[str, str]:
    out = {}
    buf = io.StringIO()
    wr = csv.writer(buf, lineterminator='\n')
    wr.writerow(['key', 'label', 'kind', 'title', 'enacted', 'published', 'in_force_days', 'commits', 'url'])
    days: dict[str, list[str]] = {}
    for e in log:
        if e['law']:
            days.setdefault(e['law'], []).append(e['day'])
    for key in sorted(c['laws'], key=lambda k: law_order(c['laws'], k)):
        law = c['laws'][key]
        ds = sorted(set(days.get(key, [])))
        wr.writerow([key, law['label'], law.get('kind', 'law'), law.get('title', ''), law.get('enacted') or '',
                     law.get('published') or '', ' '.join(ds), len(days.get(key, [])), law.get('url') or ''])
    out['data/laws.csv'] = buf.getvalue()
    co = c['country']
    out['data/repo.json'] = json.dumps({'country': co['code'], 'name': co['name'], 'tz': co['tz'],
                                        'future_branch': co.get('future_branch', 'futuro'),
                                        'publisher': co['publisher']['name']}, ensure_ascii=False, indent=1) + '\n'
    out['data/versions.json'] = json.dumps({'country': c['country']['code'], 'acts': [{
        'slug': a['slug'], 'short': a['short'], 'title': a['title'], 'url': a.get('url'),
        'versions': [{'from': v['from'], 'units': len(v['units']), 'source_url': v.get('source_url'),
                      'sha256': v.get('sha256')} for v in a['versions']]} for a in c['acts']]},
        ensure_ascii=False, indent=1) + '\n'
    buf = io.StringIO()
    wr = csv.writer(buf, lineterminator='\n')
    wr.writerow(['day', 'kind', 'law', 'acts', 'files', 'branch'])
    for e in log:
        wr.writerow([e['day'], e['kind'], e['law'] or '', ' '.join(e['acts']), e['units'], e['branch']])
    out['data/commits.csv'] = buf.getvalue()
    for a in c['acts']:
        counts: dict[str, int] = {}
        last: dict[str, str] = {}
        for prev, cur in zip(a['versions'], a['versions'][1:]):
            for k in set(prev['units']) | set(cur['units']):
                if prev['units'].get(k, {}).get('text') != cur['units'].get(k, {}).get('text'):
                    counts[k] = counts.get(k, 0) + 1
                    last[k] = cur['from']
        now = [v for v in a['versions'] if v['from'] <= c['_docs_date']] or a['versions'][:1]
        units = now[-1]['units']
        rows = [f'# {a["title"]}', '', f'{a["short"]} · {len(a["versions"])} versions, from {a["versions"][0]["from"]} '
                f'(latest in force: {now[-1]["from"]})' + (f' · <{a["url"]}>' if a.get('url') else ''), '',
                '| Provision | File | Changes | Last changed |', '| --- | --- | ---: | --- |']
        for k in sorted(units):
            rows.append(f'| {units[k]["label"]} | [{k}.md]({k}.md) | {counts.get(k, 0)} | {last.get(k, "")} |')
        out[f'{a["slug"]}/README.md'] = '\n'.join(rows) + '\n'
    return out


def blob(path: Path) -> str:
    if not path.exists():
        return '(missing)'
    return subprocess.run(['git', 'hash-object', str(path)], capture_output=True, text=True).stdout.strip()


def version(cmd: list[str]) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True).stdout.strip().splitlines()[0]
    except Exception:
        return '?'


# Names of Lexifina's own scripts and their internals (a script's file name, a module's constant or function): how the
# sources were read is not part of the published record, only what was read and decided.
_SCRIPT = r'(?:[\w.*-]+/)*[\w.*-]+\.(?:py|sh)\b'
_ATTR = (r'\b[a-z_][a-z0-9_]*\.(?:[A-Z][A-Z0-9_]{2,}\b|[a-z][a-z0-9]*_[a-z0-9_]+\b|[a-z_][a-z0-9_]*\(\))|'
         r'\b(?:fetch|wayback|lii|peachjam|parse)\w*\.[a-z_]\w*\b(?<!\.py)(?<!\.sh)(?<!\.json)(?<!\.md)')
# The builder's own input files and gates, and the names of the sessions that ran the work.
_WORKFILE = r'\bcorpus\.d/[\w.-]+|(?<!\w)[\w-]*\.PUBLISH\b|\bgitla[w]-[\w-]+'
CODE_REF = re.compile(f'{_SCRIPT}|{_ATTR}|{_WORKFILE}')
_DOMAIN_PY = re.compile(r'\.(?:gov|gob|com|org|edu|net|mil|coop)\.py$')  # Paraguay's own domains end in .py
_CUT = '\x00'


def _code_refs(s: str, keep: frozenset[str] = frozenset()) -> list[str]:
    """Code references in s, except Paraguayan domains and the files this repository ships (`keep`, paths as
    published, e.g. tools/on.py)."""
    return [m.group(0) for m in CODE_REF.finditer(s) if not _DOMAIN_PY.search(m.group(0))
            and m.group(0) not in keep and m.group(0).rsplit('/', 1)[-1] not in {k.rsplit('/', 1)[-1] for k in keep}]


# How a site was reached (its defences, rates, caches, archive lookups): sentences saying so stay out of the published
# README. Citing a source, an archive included, stays.
# (Written so this published file does not itself spell out the defence words it filters.)
_ACCESS = re.compile(r'(?i)cloud[f]lare|capt[c]ha|bot chal[l]enge|fire[w]all|robots\.txt|this machine|from here\b|'
                     r'requests? (?:a|per|every) (?:second|minute)|request every|rate limit|\bCDX\b|\bcurl\b|\bcach(?:e|ed|ing)\b|'
                     r'common ?crawl|cluster\.idx|\bid_\b|automated (?:clients|requests)|\brefuses?\b|\bHTTP \d{3}\b|'
                     r'\b(?:401|403|429) (?:from|error|Forbidden|Too)\b|\bblocked\b|not reachable|unreachable|timed? out|'
                     r'throttl|\bpolite|\bdownloads? (?:every|each|all|the sources)|\bdownloaded (?:once|through|with|by)|'
                     r'scrap|signed link|\bendpoints?\b|encoded with a key|responseCrypto|'
                     r'\bAPI key\b|\bsession cookie|\buser[- ]agent|adaptive[ ]rate')
_SENTENCE = re.compile(r'(?<=[.;!?])\s+(?=[A-Z`(\[*"¿¡])')
BUILT = ("Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each "
         "change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus "
         "always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote "
         "Lexifina's code; it wrote no legal text, and no model runs when the history is built.")


# The old README boilerplate that BUILT replaces, or that REPRODUCE.md no longer makes true (it lists no commands now).
_STALE = re.compile(r'`REPRODUCE\.md` (?:lists|records) every|^Every command, tool version|'
                    r'^The same corpus always gives the same hashes\.$|'
                    r'^(?:The shared builder )?`tools/build\.py` (?:turns|writes)|'
                    r'^A model \(Claude\) wrote the scripts; it wrote no legal text\.$|^No model runs when the history is built\.$')


def _drop_access(text: str) -> str:
    """Sentences about how a site was reached removed. Quoted words are the source's own (its terms, its notes) and
    never count; "cached pages" is just "pages"."""
    kept = []
    for x in _SENTENCE.split(text):
        x = re.sub(r'\bcached (?=(?:pages|copies|PDFs|files|texts|responses)\b)', '', x)
        bare = re.sub(r'"[^"]*"|“[^”]*”|«[^»]*»', '""', x)
        if not _ACCESS.search(bare) and not _STALE.search(x.strip()):
            kept.append(x)
    return ' '.join(kept)


def _access_in(s: str) -> bool:
    return bool(_ACCESS.search(re.sub(r'"[^"]*"|“[^”]*”|«[^»]*»', '""', s)))


def _trim_access(sentence: str) -> str:
    """One sentence of a note without its access detail: parentheses that mention access go, then ;/:-separated
    clauses that do (keeping the sentence's end), and the sentence only if access is still mentioned."""
    if not _access_in(sentence):
        return sentence
    s = re.sub(r'\s*\([^()]*\)', lambda m: '' if _access_in(m.group(0)) else m.group(0), sentence)
    if _access_in(s):
        parts = re.split(r'(?<=[;:])\s+', s)
        kept = [p for p in parts if not _access_in(p)]
        s = ' '.join(kept).rstrip(';:, ')
        if s and not s.endswith(('.', '!', '?')) and sentence.rstrip().endswith('.'):
            s += '.'
    return '' if not s or _access_in(s) or _STALE.search(s.strip()) or len(s) < 12 else s


def public_readme(text: str, keep: frozenset[str]) -> str:
    """A country's static Markdown as published: sentences about how a site was reached (fetching, caches, rates,
    defences) are dropped, table cells keeping a dash; scripts the repository does not ship are named as Lexifina's
    code; and the "How it is built" section opens with the standard paragraph (BUILT), the rest of its method kept.
    Code blocks are left as they are."""
    out, fenced = [], False
    # Hard-wrapped prose is joined into one line per paragraph or list item first, so a sentence is judged whole.
    lines: list[str] = []
    for line in text.split('\n'):
        if line.startswith('```'):
            fenced = not fenced
        prose = line.strip() and not line.startswith(('|', '#', '```', '<')) and not fenced
        starts_item = re.match(r'\s*(?:[-*+]|\d+\.)\s', line)
        if prose and lines and lines[-1].strip() and not starts_item and not lines[-1].startswith(('|', '#', '```', '<')) \
                and not line.startswith(' ' * 4) and not lines[-1].endswith('  '):
            lines[-1] = lines[-1].rstrip() + ' ' + line.strip()
        else:
            lines.append(line)
    fenced = False
    for line in lines:
        if line.startswith('```'):
            fenced = not fenced
        if fenced or line.startswith('```'):
            out.append(line)
            continue
        if line.startswith('## '):
            out.append(line)
            if line.strip() == '## How it is built':
                out += ['', BUILT]
            continue
        if line.startswith('|') and not re.match(r'^\|[\s:|-]+\|?$', line):
            cells = line.split('|')
            line = '|'.join(c if i in (0, len(cells) - 1) else
                            (' ' + (_public_refs(_drop_access(c.strip()), keep) or '–') + ' ' if c.strip() else c)
                            for i, c in enumerate(cells))
        elif line.strip():
            new = _public_refs(_drop_access(line), keep)
            if not new.strip():
                continue
            line = new
        out.append(line)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out))


def _public_refs(s: str, keep: frozenset[str]) -> str:
    return public_note(s, keep) if _code_refs(s, keep) else s


def public_note(s: str, keep: frozenset[str] = frozenset()) -> str:
    """A decision, AI-use note or source name as published. A parenthesis that names a script, its internals or the
    builder's own files is dropped; any other mention of a script becomes "Lexifina's code" ("the same code", or just
    "the same" before a noun). Only the places cut are tidied: quoted text keeps its spacing."""
    s = re.sub(r'\s*\([^()]*\)', lambda m: _CUT if _code_refs(m.group(0), keep) else m.group(0), s)
    # The builder's own files outside a parenthesis keep their meaning in plain words.
    s = re.sub(r'(?<!\w)[\w-]*\.PUBLISH(?: file)?\b', 'sign-off', s)
    s = re.sub(r'\bcorpus\.d/[\w.-]+', 'a separate part of the corpus', s)
    s = re.sub(r'\b(?:in|from) the cache\b', 'as retrieved', s)
    ref = f'`?(?:{CODE_REF.pattern})`?'
    run = re.compile(rf'(the same |by |in |with |of |over |through |from )?{ref}(?:(?:, | and | or |/){ref})*')

    def sub(m: re.Match) -> str:
        if not _code_refs(m.group(0), keep):
            return m.group(0)
        lead = m.group(1) or ''
        if lead == 'the same ':
            after = s[m.end():m.end() + 6]
            return 'the same' if re.match(r' (?!as\b|that\b)[a-z]', after) else 'the same code'
        return f"{lead}Lexifina's code"
    s = run.sub(sub, s)
    s = re.sub(r"Lexifina's code(?:,? and Lexifina's code)+", "Lexifina's code", s)
    s = re.sub(rf'\s*{_CUT}+(?=[,.;:)])', '', s)
    s = re.sub(rf'\s*{_CUT}+\s*', ' ', s).strip()
    # How a site was reached (rates, robots.txt, defences) is not part of the record. A note is legal reasoning, so cut
    # as little as possible: first the parenthesis or the ;/: clause that says it, and the whole sentence only if
    # that is not enough.
    return ' '.join(x for x in (_trim_access(x) for x in _SENTENCE.split(s)) if x).strip()


def reproduce(c: dict, folder: Path, raw: bytes, log: list[dict], tags: dict, docs_date: str) -> str:
    co = c['country']
    ver = json.loads((folder / 'verification.json').read_text(encoding='utf-8')) if (folder / 'verification.json').exists() else {}
    tpl = (HERE / 'REPRODUCE.template.md').read_text(encoding='utf-8')
    n_law = sum(1 for e in log if e['kind'] == 'law')
    n_unexp = sum(1 for e in log if e['kind'] == 'unexplained')
    n_start = sum(1 for e in log if e['kind'] == 'start')
    n_future = sum(1 for e in log if e['branch'] != 'main')
    n_clamped = sum(1 for e in log if e['clamped'])
    src_rows = '\n'.join(f'| {public_note(s.get("name", ""))} | <{s.get("url", "")}> | {s.get("retrieved", "")} | '
                         f'{public_note(s.get("licence", ""))} |' for s in c.get('sources', []))
    act_rows = '\n'.join(f'| `{a["slug"]}` | {a["title"]} | {len(a["versions"])} | {a["versions"][0]["from"]} to '
                         f'{a["versions"][-1]["from"]} |' for a in c['acts'])
    # A check or second build counts only for the corpus it ran on: a main build (verified parts only) must not quote
    # the check of the full build, or of an earlier corpus.
    sha = hashlib.sha256(raw).hexdigest()
    chk = ver.get('check') if (ver.get('check') or {}).get('corpus_sha256') == sha else None
    check_line = (f'{chk["versions"]} versions of {chk["acts"]} acts read back from git on the day each took effect and '
                  f'on the day before: {chk["mismatches"]} mismatches. Trailers: {chk["trailer_errors"]} commits whose '
                  f'trailers git cannot parse. Health: {chk["merges"]} merge commits on main, {chk["backwards"]} commit '
                  f'dates that go backwards, {chk["future_dated"]} commits dated after the build.'
                  if chk else 'Not yet run for this build.')
    reb = ver.get('rebuild') if (ver.get('rebuild') or {}).get('corpus_sha256') == sha else None
    rebuild_line = (f'A second build from the same corpus into an empty folder gave identical hashes for all '
                    f'{reb["commits"]} history commits and {reb["tags"]} tags (history tip `{reb["history_tip"]}`).'
                    if reb and reb.get('identical') else
                    'A second build gave different hashes; see verification.json.' if reb else
                    'No second build of this corpus has been compared yet.')
    fill = {
        'NAME': co['name'], 'SLUG': co['slug'], 'DOCS_DATE': docs_date, 'TZ': co['tz'],
        'SOURCES': src_rows or '| (none listed) | | | | |', 'ACTS': act_rows,
        'RULE': (co.get('default_in_force_rule') or {}).get('text', '(not stated)'),
        'RULE_SOURCE': (co.get('default_in_force_rule') or {}).get('source', ''),
        'CORPUS_SHA': hashlib.sha256(raw).hexdigest(), 'CORPUS_BYTES': str(len(raw)),
        'LAWS': str(len(c['laws'])), 'COMMITS': str(len(log)), 'LAW_COMMITS': str(n_law), 'START_COMMITS': str(n_start),
        'UNEXPLAINED': str(n_unexp), 'FUTURE': str(n_future), 'CLAMPED': str(n_clamped), 'TAGS': str(len(tags)),
        'FUTURE_BRANCH': co.get('future_branch', 'futuro'),
        'BUILD_BLOB': blob(HERE / 'build.py'), 'CHECK_BLOB': blob(HERE / 'check.py'), 'ON_BLOB': blob(HERE / 'on.py'),
        'PYTHON': version([sys.executable, '--version']), 'GIT': version(['git', '--version']),
        'DECISIONS': '\n'.join(f'- {n}' for n in map(public_note, c.get('decisions', [])) if n) or '- None.',
        'AI_USE': '\n'.join(f'- {n}' for n in map(public_note, c.get('ai_use', [])) if n) or '- None at data-build time.',
        'CHECK': check_line, 'REBUILD': rebuild_line,
    }
    return re.sub(r'\{\{([A-Z_]+)\}\}', lambda m: fill[m.group(1)], tpl)


def docs_files(c: dict, folder: Path, raw: bytes, log: list[dict], tags: dict, docs_date: str) -> dict[str, str]:
    files: dict[str, str] = {}
    static = folder / 'repo'
    if static.exists():
        for p in sorted(static.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                files[p.relative_to(static).as_posix()] = p.read_text(encoding='utf-8').replace('\r\n', '\n')
    for name in ('on.py', 'check.py', 'build.py', 'SCHEMA.md', 'REPRODUCE.template.md'):
        text = (HERE / name).read_text(encoding='utf-8').replace('\r\n', '\n')
        # Passages for Lexifina's agents only (how sources are fetched, internal paths) stay out of the published copy.
        text = re.sub(r'\n?', '', text, flags=re.S)
        files[f'tools/{"check_repo.py" if name == "check.py" else name}'] = text
    # Every script and data file the country's fetch and parse use, so the repository alone can rebuild itself.
    # Subfolders (a helper agent's codes/ scripts) keep their relative path under tools/.
    # Skipped folders are pruned while walking, not listed and then dropped: an agent's scratch builds (.tmp-build*,
    # each a whole repository) and .cache can hold tens of thousands of files.
    found = []
    for top, dirs, names in os.walk(folder):
        dirs[:] = [d for d in dirs if not (d.startswith('.') or d in ('repo', 'corpus.d', '__pycache__', 'logs'))]
        found += [Path(top, n) for n in names
                  if n.endswith(('.py', '.sh')) or (n.endswith('.json') and n.startswith(('sources', 'acts')))]
    for p in sorted(found):
        rel = p.relative_to(folder)
        if p.is_file() and (p.suffix in ('.py', '.sh') or (p.suffix == '.json' and p.name.startswith(('sources', 'acts')))):
            if private and private.is_private(p):  # Lexifina's fetch tooling and notes stay private
                continue
            text = p.read_text(encoding='utf-8').replace('\r\n', '\n')
            files.setdefault(f'tools/{rel.as_posix()}', private.scrub(text) if private else text)
    # The country's own static docs as published: no account of how sources were reached, and only shipped scripts
    # named (public_readme). A static script that is part of fetching stays out like any other.
    own = [r for r in files if (static / r).is_file()] if static.exists() else []
    for rel in own:
        if rel.endswith(('.py', '.sh')) and private and private.is_private(static / rel):
            del files[rel]
    keep = frozenset(k for k in files if k.startswith('tools/')) | {'REPRODUCE.md'}
    for rel in own:
        if rel.endswith('.md') and rel in files:
            files[rel] = public_readme(files[rel], keep)
    files['data/corpus.sha256'] = f'{hashlib.sha256(raw).hexdigest()}  corpus.json\n'
    files.update(tables(c, log))
    files['REPRODUCE.md'] = reproduce(c, folder, raw, log, tags, docs_date)
    return files


# ---------------------------------------------------------------- main

def build(folder: Path, repo: Path, docs_date: str) -> dict:
    c, raw = load(folder)
    errs = validate(c)
    if errs:
        raise CorpusError('corpus.json has problems:\n  ' + '\n  '.join(errs[:60]) + (f'\n  … {len(errs) - 60} more' if len(errs) > 60 else ''))
    c['_docs_date'] = docs_date
    commits = plan(c)
    prepare(repo)
    w, tags, log, clock = write_history(repo, c, docs_date, commits)
    co = c['country']
    committer = ('Lexifina', f'{co["slug"]}-law@lexifina.com')
    files = docs_files(c, folder, raw, log, tags, docs_date)
    # The documentation commit goes on main, dated the day the data was retrieved, so a rebuild on any later day from
    # the same corpus gives the same hashes. The future branch keeps only laws; tools read it for later dates.
    future = co.get('future_branch', 'futuro')
    if 'main' not in w.heads:
        raise CorpusError(f'nothing is in force on {docs_date}: every version is later than --docs-date')
    w.commit('main', committer, committer, clock.stamp(docs_date),
                        f'Documentation, tables, tools and REPRODUCE.md\n\nBuilt from corpus.json '
                        f'(sha256 {hashlib.sha256(raw).hexdigest()}), data retrieved {docs_date}.\n',
                        files, parent=w.heads.get('main'))
    for name, mark in sorted(tags.items()):
        w.tag(name, mark)
    w.finish()
    if os.environ.get('GITLAW_NO_CHECKOUT') == '1':
        # A build only to check and push (autopush): the commits are complete without writing thousands of files
        # out, and the next build has none to delete. `git checkout -f main` gives the working tree back.
        pass
    else:
        # Parallel checkout (git 2.32+): one worker per core, same files.
        git(repo, '-c', 'checkout.workers=0', 'checkout', '-q', '-f', 'main')
    return {'commits': len(log), 'tags': len(tags), 'laws': sum(1 for e in log if e['kind'] == 'law'),
            'unexplained': sum(1 for e in log if e['kind'] == 'unexplained'),
            'future': sum(1 for e in log if e['branch'] != 'main'), 'main': git(repo, 'rev-parse', 'HEAD').strip()}


def site_data(c: dict, docs_date: str) -> dict:
    """The reader's data for lexifina.com/watch: each provision's versions (when its words changed, or when a law is
    credited to it without changing them: `same`), with the laws credited for each, and each act's versions with the
    laws credited in them. Built from the corpus, so it agrees with the repository commit for commit. Provisions are in
    the order the text gives them, a provision added later sitting after the one it follows."""
    laws = {k: {f: v.get(f) for f in ('label', 'title', 'kind', 'enacted', 'published', 'url', 'temporary_until')}
            for k, v in c['laws'].items()}
    order_laws = lambda ls: sorted(set(ls), key=lambda l: law_order(c['laws'], l))  # noqa: E731
    acts = []
    for a in c['acts']:
        units: dict[str, dict] = {}
        order: list[str] = []
        seen: set[str] = set()
        changes = []
        prev: dict = {}
        for i, v in enumerate(a['versions']):
            cur = v['units']
            credits = v.get('credits', {})
            after = None
            for k in cur:  # merge this version's order into the order so far
                if k not in seen:
                    order.insert(order.index(after) + 1 if after is not None else 0, k)
                    seen.add(k)
                after = k
            for k in sorted(set(prev) | set(cur)):
                same = bool(i) and prev.get(k, {}).get('text') == cur.get(k, {}).get('text')
                if (same and not credits.get(k)) or (i == 0 and k not in cur):
                    continue
                u = units.setdefault(k, {'key': k, 'label': (cur.get(k) or prev.get(k))['label'], 'versions': []})
                if k in cur:
                    u['label'] = cur[k]['label']
                credited = order_laws(credits.get(k) or ([a['first_law']] if i == 0 and a.get('first_law') else []))
                entry = {'from': v['from'], 'laws': credited, 'future': v['from'] > docs_date}
                if same:
                    entry['same'] = True
                else:
                    entry['text'] = cur[k]['text'] if k in cur else None
                u['versions'].append(entry)
            changes.append({'from': v['from'], 'laws': order_laws(l for ls in credits.values() for l in ls)
                            or ([a['first_law']] if i == 0 and a.get('first_law') else []),
                            'future': v['from'] > docs_date})
            prev = cur
        acts.append({'slug': a['slug'], 'short': a['short'], 'title': a['title'], 'url': a.get('url'),
                     'first': a['versions'][0]['from'], 'first_law': a.get('first_law'),
                     'earlier_laws': a.get('earlier_laws', []), 'versions': [v['from'] for v in a['versions']],
                     'changes': changes, 'units': [units[k] for k in order if k in units]})
    co = c['country']
    return {'country': {k: co.get(k) for k in ('code', 'name', 'slug', 'lang', 'tz', 'default_in_force_rule')},
            'publisher': co['publisher']['name'], 'built': docs_date, 'repo': f'https://github.com/lexifina/{co["slug"]}-law',
            'sources': c.get('sources', []), 'laws': laws, 'acts': acts}


def hashes(repo: Path) -> tuple[list[str], dict[str, str], dict[str, str]]:
    log = git(repo, 'log', '--format=%H', 'main').split()
    tags = dict(l.split(' ', 1)[::-1] for l in git(repo, 'show-ref', '--tags').split('\n') if l)
    heads = dict(l.split(' ', 1)[::-1] for l in git(repo, 'show-ref', '--heads').split('\n') if l)
    return log, tags, heads


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('folder', help='scripts/<slug>-law (holds corpus.json and repo/)')
    ap.add_argument('--repo', required=True, help='the repository to (re)build; emptied first, origin kept')
    ap.add_argument('--docs-date', required=True, help='the day the data was retrieved (never the run day)')
    ap.add_argument('--compare', help='an earlier build of the same corpus: report whether every hash is identical')
    ap.add_argument('--site-data', help='also write the /watch reader data (JSON) to this path')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    if not _is_date(args.docs_date):
        raise CorpusError('--docs-date must be YYYY-MM-DD')
    folder, repo = Path(args.folder).resolve(), Path(args.repo).resolve()
    if args.site_data:
        c, _ = load(folder)
        Path(args.site_data).parent.mkdir(parents=True, exist_ok=True)
        Path(args.site_data).write_text(json.dumps(site_data(c, args.docs_date), ensure_ascii=False, separators=(',', ':')),
                                        encoding='utf-8', newline='\n')
    res = build(folder, repo, args.docs_date)
    print(json.dumps(res, indent=1))
    if args.compare:
        a, b = hashes(Path(args.compare)), hashes(repo)
        rec = {'identical': a[0][1:] == b[0][1:] and a[1] == b[1],
               'history_tip': b[0][1] if len(b[0]) > 1 else b[0][0], 'commits': len(b[0]) - 1, 'tags': len(b[1]),
               'main_identical': a[0][0] == b[0][0], 'corpus_sha256': hashlib.sha256(load(folder)[1]).hexdigest()}
        print(json.dumps(rec, indent=1))
        p = folder / 'verification.json'
        ver = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
        ver['rebuild'] = rec
        p.write_text(json.dumps(ver, indent=1, sort_keys=True) + '\n', encoding='utf-8', newline='\n')
        for f in repo.rglob('*'):
            try:
                os.chmod(f, 0o700)
            except OSError:
                pass
        raise SystemExit(0 if rec['identical'] else 1)


if __name__ == '__main__':
    main()
