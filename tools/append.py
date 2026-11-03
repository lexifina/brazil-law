"""Grow a published git-for-law history append-only: new acts and newer versions go on top; nothing is rewritten.

    python -X utf8 append.py <scripts/<slug>-law> --repo <clone of the published repo> --docs-date YYYY-MM-DD

The clone's main must equal origin/main. What main already holds is read from git itself: for each act, the newest
In-force day it carries, and that the text in force on that day equals the corpus version. Then:

- an act main does not hold yet is appended as one block: its first version, then one commit per law per in-force day,
  in in-force order;
- a version of an act main already holds, in force after the newest one there, is appended as a change, as the full
  build would make it;
- a version in force on or before the newest one there that main lacks (a back-filled form), or a version whose text
  differs from main (a correction), stops the run, unless --corrections is given (below);
- versions in force after --docs-date are left for a later run (they are appended when their day comes).

Author date: noon local time on the in-force day, as in the full build. Committer date: the published head's committer
time plus one second per appended commit, so committer dates never go backwards and the same head and corpus always
give the same hashes. Tags that already exist are never moved; new ones are added. A documentation commit is appended
last (README, REPRODUCE.md, data/), never replacing the earlier one. The result is pushed with a plain `git push`.

Readers choose versions by the In-force trailer (tools/on.py, tools/check_repo.py), so an appended block reads the same
as a full build does.

With --corrections, held text that differs from the corpus does not stop the run. Before anything new, the run appends
correction commits for versions whose text main holds wrongly (or lacks: a back-filled version), and explicit
metadata-only corrections, in in-force order, then by act and correction range. Open ranges are split at stale
ordinary rows while retaining the source In-force date. Files hold that version's corrected text; the act's newest held
version's commit also sets back any file the earlier corrections changed, so the tip then equals the corpus and the
new versions appended after it build on the corrected text. Each is made by Lexifina, dated noon on the version's day,
and carries:

    Kind: correction
    In-force: <the version's first day>
    Corrects: <act> <from>..<to>      <to>: the day before the act's next version; open (<from>..) for the newest
    Supersedes: <sha>                 the published commit that carried the wrong text on that day, or none
    Reason: <one line>                supplied correction metadata, else --reason or a back-fill/tip-restore reason
    Act-path: <path>                  the act's folder (or file), relative to the repository root
    Files: <path>                     one line per file it corrects, repeated (a path may hold a comma); its tree
                                      holds their text, and a path it lacks is removed. Needed as a commit can't
                                      show a file it sets to the text the tip already has (a version found late)

The history is not re-sorted: the commits before keep their text as first published. Readers apply corrections by
date (Reader): the text of an act on a day is the commit the In-force trailer picks among the commits that touch its
Act-path and are not corrections, then, file by file and in commit order, each correction whose Corrects range holds
the day; an open range ends the day before the next such non-correction commit (one touching Act-path: a sibling
file's commit in a shared folder does not end it). A commit with no Act-path falls back to the folder of its Files,
and then to its Corrects act name. tools/on.py and tools/check_repo.py as published do not
apply them yet; check_corrected() checks such a main (0 mismatches, read this way, and the tip equal to the corpus on
--docs-date). A second run reads main with its corrections applied, finds nothing to correct and adds nothing.
"""
import argparse
import csv
import io
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build as B  # noqa: E402
import check_repo as K  # noqa: E402
import published_parts  # noqa: E402


def git(repo: Path, *args: str) -> str:
    return B.git(repo, *args)


def published_state(repo: Path, c: dict, verify: bool = True) -> dict[str, str]:
    """{act slug: newest In-force day on main} for every act main holds; checks that day's text equals the corpus
    (verify=False: no check, for --corrections)."""
    slugs = [a['slug'] for a in c['acts']]
    rows = K.all_commits_by_act(repo, 'main', slugs)
    # A law credited for a version that changed no words gets a commit that touches no file, which the per-path walk
    # above cannot see. data/commits.csv names the acts of every commit, so those days count too; otherwise each such
    # commit would be appended again on every run.
    listed: dict[str, str] = {}
    try:
        for e in published_log(repo):
            if e['branch'] == 'main':
                for s in e['acts']:
                    listed[s] = max(listed.get(s, ''), e['day'])
    except B.CorpusError:  # no data/commits.csv on main
        pass
    # Read with any correction commits applied (Reader): on a main without them this is the In-force trailer's pick.
    rd = Reader(repo, slugs, rows=rows) if verify else None
    state = {}
    problems = []
    try:
        for act in c['acts']:
            r = rows[act['slug']]
            if not r:
                continue
            last = max([d for _, d in r] + [listed.get(act['slug'], '')])
            state[act['slug']] = last
            if not verify:
                continue
            # Every corpus version on or before `last` must read back from main exactly (else: correction or back-fill).
            for i, v in enumerate(act['versions']):
                if v['from'] > last:
                    break
                if i + 1 < len(act['versions']) and act['versions'][i + 1]['from'] == v['from']:
                    continue
                files = rd.files(act['slug'], v['from']) or {}
                want = {f'{act["slug"]}/{k}.md': K.blob_oid(u['text']) for k, u in v['units'].items()}
                if files != want:
                    bad = sorted(f for f in set(files) | set(want) if files.get(f) != want.get(f))
                    problems.append(f'{act["slug"]} {v["from"]}: main differs from the corpus in {len(bad)} file(s), '
                                    f'e.g. {bad[:3]} (a correction or a back-filled form: decide by hand)')
    finally:
        if rd:
            rd.close()
    if problems:
        raise B.CorpusError('main does not match the corpus for versions it already holds:\n  ' + '\n  '.join(problems[:40]))
    return state


DEFAULT_REASON = 'text corrected from the official source'
BACKFILL_REASON = 'version found late: the published history had no version for this day'
RESTORE_REASON = 'the text in force now, restored at the tip after the corrections to earlier versions'


def correction_metadata(act: dict, version: dict) -> dict:
    """Explicit correction assertions, with per-version values overriding act defaults."""
    meta = {}
    withdrawal = act.get('corpus_withdrawal', {})
    if withdrawal.get('reason'):
        meta['reason'] = 'corpus withdrawal, not legislative repeal: ' + withdrawal['reason']
    for owner, key in ((act, 'editorial_date_correction'), (act, 'correction'), (version, 'correction')):
        value = owner.get(key, {})
        if not isinstance(value, dict):
            raise B.CorpusError(f'{act["slug"]}: {key} must be an object')
        meta.update(value)
    for key in ('in_force_basis', 'text_as_of'):
        if key in version:
            meta[key] = version[key]
    # Compatibility with the delivered date corrections: this assertion explicitly
    # identifies `from` as the retained retrieval day. metadata_only alone does not.
    legacy = act.get('editorial_date_correction', {})
    if ('text_as_of' not in meta and
            'Retrieval day retained because exact commencement is unknown.' in legacy.get('in_force_basis', '')):
        meta['text_as_of'] = version['from']
    for key in ('reason', 'in_force_basis', 'text_as_of', 'supersedes'):
        if key in meta and (not isinstance(meta[key], str) or not meta[key].strip() or
                            '\n' in meta[key] or '\r' in meta[key]):
            raise B.CorpusError(f'{act["slug"]}: correction {key} must be one nonempty line')
        if key in meta:
            # Git trims trailer values; use the same form for repeat-plan comparisons.
            meta[key] = meta[key].strip()
    if 'metadata_only' in meta and not isinstance(meta['metadata_only'], bool):
        raise B.CorpusError(f'{act["slug"]}: correction metadata_only must be a boolean')
    if 'text_as_of' in meta:
        if not B._is_date(meta['text_as_of']):
            raise B.CorpusError(f'{act["slug"]}: correction text_as_of must be YYYY-MM-DD')
        if not meta.get('in_force_basis'):
            raise B.CorpusError(f'{act["slug"]}: correction text_as_of requires in_force_basis')
    return meta


def correction_assertions(repo: Path) -> dict[str, dict[str, str]]:
    """Read assertions from existing commits, independently of their changed paths."""
    keys = ('Reason', 'In-force-basis', 'Text-as-of', 'Supersedes', 'Source', 'Text-source', 'In-force')
    fmt = '%H%x1e' + '%x1e'.join(f'%(trailers:key={k},valueonly,separator=%x1f)' for k in keys) + '%x1d'
    return {fields[0]: dict(zip(keys, fields[1:])) for rec in git(repo, 'log', '--format=' + fmt, 'main').split('\x1d')
            if len(fields := rec.strip('\n').split('\x1e')) == len(keys) + 1}


def metadata_trailers(act: dict, version: dict, meta: dict) -> dict[str, str]:
    out = {trailer: meta[key] for key, trailer in (('in_force_basis', 'In-force-basis'), ('text_as_of', 'Text-as-of'))
           if meta.get(key)}
    # Legacy corrections with no source metadata retain their original trailer block.
    if act.get('url'):
        out['Source'] = act['url']
    if version.get('source_url'):
        out['Text-source'] = version['source_url']
        out.setdefault('Source', version['source_url'])
    return out


def corpus_on(vs: list[dict], day: str) -> dict | None:
    """The corpus version in force at the end of `day` (the last one of its day), or None before the first."""
    out = None
    for v in vs:
        if v['from'] > day:
            break
        out = v
    return out


def last_of_day(vs: list[dict]) -> list[dict]:
    """The versions that are in force at the end of their day (a same-day version is replaced by the next one)."""
    return [v for i, v in enumerate(vs) if i + 1 == len(vs) or vs[i + 1]['from'] != v['from']]


def unit_oids(slug: str, v: dict | None) -> dict[str, str]:
    return {f'{slug}/{k}.md': K.blob_oid(u['text']) for k, u in v['units'].items()} if v else {}


def day_before(day: str) -> str:
    return (B.dt.date.fromisoformat(day) - B.dt.timedelta(days=1)).isoformat()


def _ls(repo: Path, commit: str, path: str) -> dict[str, str]:
    """{path: blob id} of every file at or under `path` in `commit` (none if it is not there)."""
    out = {}
    for rec in git(repo, '-c', 'core.quotePath=false', 'ls-tree', '-r', '-z', commit, '--', path).split('\0'):
        meta, _, p = rec.partition('\t')
        if p and meta.split()[1] == 'blob':
            out[p] = meta.split()[2]
    return out


def corrections_on(repo: Path, ref: str = 'main') -> list[dict]:
    """The correction commits on ref, oldest first: {'commit', 'ranges': {act: (from, to or None)}, 'paths': {act:
    Act-path}, 'files': {act: {path: blob id, or None if removed}}}. An act's files are those its Files trailers name
    (one path per line), read from its tree, a path the tree lacks being removed; with no Files trailer, the files the
    commit changes under the act's path. A commit with no Act-path gives each act the folder its Files share (an older
    form), else the act's name."""
    out = git(repo, 'log', '--no-merges', '--reverse', '--format=%H%x1e%(trailers:key=Kind,valueonly,separator=%x1f)'
              '%x1e%(trailers:key=Corrects,valueonly,separator=%x1f)%x1e'
              '%(trailers:key=Act-path,valueonly,separator=%x1f)%x1e'
              '%(trailers:key=Files,valueonly,separator=%x1f)%x1d', ref)
    fixes = []
    for rec in out.split('\x1d'):
        h, kind, cor, apath, named = (rec.strip('\n').split('\x1e') + ['', '', '', ''])[:5]
        if not h or 'correction' not in [k.strip() for k in kind.split('\x1f')]:
            continue
        ranges = {}
        for line in cor.split('\x1f'):
            parts = line.split()
            if len(parts) == 2 and '..' in parts[1]:
                a, _, b = parts[1].partition('..')
                ranges[parts[0]] = (a, b or None)
        acts = list(ranges)
        listed = [p.strip() for p in named.split('\x1f') if p.strip()]
        given = [p.strip().rstrip('/') for p in apath.split('\x1f') if p.strip()]
        paths = {}
        for i, a in enumerate(acts):
            if i < len(given):
                paths[a] = given[i]
            else:
                dirs = {p.rsplit('/', 1)[0] for p in listed if '/' in p}
                paths[a] = dirs.pop() if len(dirs) == 1 and len(acts) == 1 else a

        def under(p: str, base: str) -> bool:
            return p == base or p.startswith(base + '/')

        files: dict[str, dict] = {}
        if listed:
            for a in acts:
                mine = [p for p in listed if under(p, paths[a])]
                if mine:
                    have = _ls(repo, h, paths[a])
                    files[a] = {p: have.get(p) for p in mine}
        else:
            raw = git(repo, '-c', 'core.quotePath=false', 'diff-tree', '-r', '-z', '--no-renames', '--no-commit-id',
                      f'{h}^', h)
            f = raw.split('\0')
            for meta, path in zip(f[0::2], f[1::2]):
                for a in acts:
                    if under(path, paths[a]) and path.endswith('.md') and path != f'{paths[a]}/README.md':
                        m = meta.split()
                        files.setdefault(a, {})[path] = None if m[4] == 'D' else m[3]
        fixes.append({'commit': h, 'ranges': ranges, 'paths': paths, 'files': files})
    return fixes


class Reader:
    """An act's files on a day, with correction commits applied: the commit the In-force trailer picks among the
    commits that touch the act's path and are not corrections (tools/on.py's rule), then, file by file and in commit
    order, every correction commit whose Corrects range for the act holds the day. An open range (`<from>..`) ends the
    day before the next such commit (not a correction, touching the act's path) with a later In-force day.

    `acts`: the acts to read, by the name Corrects gives them; `paths` maps a name to its path (default: the path the
    act's correction commits give as Act-path, else the name itself, the act's folder as the builder writes it). An
    act's files are the .md files under a folder path (README.md excepted), or the file a path names."""

    def __init__(self, repo: Path, acts: list[str], ref: str = 'main', rows: dict | None = None,
                 paths: dict[str, str] | None = None):
        self.repo = repo
        self.fixes = corrections_on(repo, ref)
        skip = {f['commit'] for f in self.fixes}
        self.path = {a: a for a in acts}
        for f in self.fixes:
            for a, p in f['paths'].items():
                if a in self.path:
                    self.path[a] = p
        self.path.update(paths or {})
        # `rows` (by act name) is used only for acts read at their own name.
        need = sorted({p for a, p in self.path.items() if rows is None or a not in rows or p != a})
        by_path = K.all_commits_by_act(repo, ref, need) if need else {}
        self.rows = {a: [(h, d) for h, d in (by_path[p] if p in by_path else rows[a]) if h not in skip]
                     for a, p in self.path.items()}
        self.cat, self.trees, self.blobs = K.Cat(repo), {}, {}

    def _at(self, commit: str, act: str) -> dict[str, str]:
        p = self.path[act]
        if p.endswith('.md'):  # an act that is one file
            if (commit, p) not in self.blobs:
                self.blobs[(commit, p)] = _ls(self.repo, commit, p)
            return dict(self.blobs[(commit, p)])
        return dict(K.tree_oids(self.cat, commit, p, self.trees))

    def files(self, act: str, day: str) -> dict[str, str] | None:
        h = K.state_on(self.rows[act], day)
        out = self._at(h, act) if h else None
        for f in self.fixes:
            if act not in f['ranges']:
                continue
            a, b = f['ranges'][act]
            b = self.range_end(act, a, b)
            if a <= day <= b:
                out = out if out is not None else {}
                for p, o in f['files'].get(act, {}).items():
                    if o is None:
                        out.pop(p, None)
                    else:
                        out[p] = o
        return out

    def range_end(self, act: str, start: str, end: str | None) -> str:
        return end if end is not None else day_before(
            min((d for _, d in self.rows[act] if d > start), default='9999-12-31'))

    def boundaries(self, act: str) -> set[str]:
        """All days on which an ordinary row or an existing correction changes the read."""
        days = {d for _, d in self.rows[act]}
        for fix in self.fixes:
            if act in fix['ranges']:
                start, end = fix['ranges'][act]
                days.add(start)
                if end and end < '9999-12-31':
                    days.add((B.dt.date.fromisoformat(end) + B.dt.timedelta(days=1)).isoformat())
        return days

    def close(self):
        self.cat.close()


def text_credits(c: dict, act: dict, target: dict, key: str) -> list[str]:
    """Labels of the laws the corpus credits for the text `key` has in `target`: those of the version it began in."""
    vs = act['versions']
    j = next(i for i, v in enumerate(vs) if v is target)
    want = target['units'][key]['text']
    while j > 0 and vs[j - 1]['units'].get(key, {}).get('text') == want:
        j -= 1
    keys = ([act['first_law']] if act.get('first_law') else []) if j == 0 else \
        sorted(set(vs[j].get('credits', {}).get(key, [])), key=lambda l: B.law_order(c['laws'], l))
    return [c['laws'][k]['label'] for k in keys if k in c['laws']]


def plan_corrections(repo: Path, c: dict, head: str, state: dict[str, str], reason: str) -> list[dict]:
    """Correct differing text or explicit metadata over each canonical version's range. Split open ranges at stale
    ordinary rows, then restore the newest held text at the tip. Order by legal day, act, and range start."""
    held = [a for a in c['acts'] if a['slug'] in state]
    rd = Reader(repo, [a['slug'] for a in held])
    fixes = []
    assertions = None
    try:
        for act in held:
            s = act['slug']
            allv = last_of_day(act['versions'])
            pos = {id(v): i for i, v in enumerate(allv)}
            vs = [v for v in allv if v['from'] <= state[s]]

            def next_day(v):
                return allv[pos[id(v)] + 1]['from'] if pos[id(v)] + 1 < len(allv) else None
            own = []
            for i, v in enumerate(vs):
                nxt = next_day(v)
                meta = correction_metadata(act, v)
                supplied_sup = meta.get('supersedes')
                if supplied_sup and supplied_sup not in ({h for h, _ in rd.rows[s]} |
                        {f['commit'] for f in rd.fixes if s in f['ranges']}):
                    raise B.CorpusError(f'{s}: correction supersedes {supplied_sup!r} is not in this act\'s published history')
                needs_metadata = meta.get('metadata_only', False) or bool(act.get('correction') or v.get('correction'))
                if needs_metadata and assertions is None:
                    assertions = correction_assertions(repo)
                want = unit_oids(s, v)
                # A closed canonical range already crosses historical rows. An open
                # one must restart there, otherwise Reader ends it at the stale row.
                starts = [v['from']] + (sorted({d for _, d in rd.rows[s] if d > v['from']}) if nxt is None else [])
                for j, start in enumerate(starts):
                    stop = starts[j + 1] if j + 1 < len(starts) else nxt
                    end = day_before(stop) if stop else None
                    days = [start] + sorted(d for d in rd.boundaries(s) if start < d < (stop or '9999-12-31'))
                    bad = set()
                    for d in days:
                        have = rd.files(s, d) or {}
                        bad |= {f for f in set(have) | set(want) if have.get(f) != want.get(f)}
                    sup = supplied_sup or K.state_on(rd.rows[s], start) or 'none'
                    expected = {**metadata_trailers(act, v, meta), 'Reason': meta.get('reason', reason),
                                'Supersedes': sup, 'In-force': v['from']}
                    # Require the latest applicable correction to carry the assertion
                    # throughout this range; an older matching correction is not enough.
                    missing_metadata = False
                    if needs_metadata:
                        for day in days:
                            latest = next((f for f in reversed(rd.fixes) if s in f['ranges'] and
                                f['ranges'][s][0] <= day <= rd.range_end(s, *f['ranges'][s])), None)
                            if latest is None or any(assertions.get(latest['commit'], {}).get(k, '') != value
                                                     for k, value in expected.items()):
                                missing_metadata = True
                                break
                    if not bad and not missing_metadata:
                        continue
                    named = bad | (set(want) if missing_metadata else set())
                    own.append({'act': act, 'version': v, 'range_from': start, 'to': end, 'bad': sorted(bad),
                                'have': rd.files(s, start) or {}, 'want': want, 'metadata': meta,
                                'metadata_changed': missing_metadata,
                                'files': {f: (v['units'][f[len(s) + 1:-3]]['text'] if f in want else None) for f in named},
                                'supersedes': sup, 'backfill': not any(d == start for _, d in rd.rows[s]), 'restored': []})
            if not vs:
                continue
            # The tip after these commits must hold the newest held version (the next appended version builds on it).
            cur = dict(K.tree_oids(rd.cat, head, s, rd.trees))
            for x in own:
                for f, t in x['files'].items():
                    if t is None:
                        cur.pop(f, None)
                    else:
                        cur[f] = K.blob_oid(t)
            top = vs[-1]
            want = unit_oids(s, top)
            rest = sorted(f for f in set(cur) | set(want) if cur.get(f) != want.get(f))
            if rest:
                if not own or own[-1]['version'] is not top:
                    nxt = next_day(top)
                    start = max([top['from']] + [d for _, d in rd.rows[s] if d >= top['from']]) if nxt is None else top['from']
                    meta = correction_metadata(act, top)
                    own.append({'act': act, 'version': top, 'range_from': start, 'metadata': meta,
                                'to': day_before(nxt) if nxt else None, 'bad': [],
                                'have': want, 'want': want, 'files': {},
                                'supersedes': meta.get('supersedes') or K.state_on(rd.rows[s], start) or 'none', 'backfill': False,
                                'restored': []})
                for f in rest:
                    own[-1]['files'][f] = top['units'][f[len(s) + 1:-3]]['text'] if f in want else None
                own[-1]['restored'] = [f for f in rest if f not in own[-1]['bad']]
            for x in own:
                x['reason'] = x['metadata'].get('reason') or (reason if x.get('metadata_changed') else
                    ((BACKFILL_REASON if x['backfill'] else reason) if x['bad'] else RESTORE_REASON))
                x['sup_subject'] = (git(repo, 'log', '-1', '--format=%s', x['supersedes']).strip()
                                    if x['supersedes'] != 'none' else '')
            fixes += own
    finally:
        rd.close()
    fixes.sort(key=lambda x: (x['version']['from'], x['act']['slug'], x['range_from']))
    return fixes


def correction_message(c: dict, x: dict) -> tuple[list[str], list[str]]:
    """Subject and body, and trailers, of one correction commit (see the module doc)."""
    act, v, have, want = x['act'], x['version'], x['have'], x['want']
    s, a = act['slug'], v['from']
    start = x.get('range_from', a)
    span = f'from {start} to {x["to"]}' if x['to'] else f'from {start} on'

    def label(path: str) -> str:
        k = path[len(s) + 1:-3]
        u = v['units'].get(k) or next((w['units'][k] for w in reversed(act['versions']) if k in w['units']), None)
        return B.unit_label(u) if u and B.unit_label(u) else k

    msg = [B.short_subject(f'Correction: {act["short"]}, version in force from {a}'), '']
    if x['bad']:
        n = len(x['bad'])
        msg += B.wrap(f'{act["title"]}: the text main held for the version in force {span} differed from the corpus '
                      f'in {n} provision{"s" if n != 1 else ""}.' +
                      (' Main had no version for this day, so it read as the version before it; this version was '
                       'found later.' if x['backfill'] else '')) + ['']
        how = {'w': [], 'm': [], 'x': []}
        for f in x['bad']:
            how['w' if f in have and f in want else 'm' if f in want else 'x'].append(label(f))
        for key, name in (('w', 'Wording differed'), ('m', 'Missing from the published text'),
                          ('x', 'Published, but not in force in this version')):
            if how[key]:
                msg += B.wrap(f'{name}: {", ".join(how[key])}.')
        msg += ['']
        credits = sorted({l for f in x['bad'] if f in want for l in text_credits(c, act, v, f[len(s) + 1:-3])})
        if credits:
            msg += B.wrap(f'The corrected text was made by {", ".join(credits)}.') + ['']
    else:
        msg += B.wrap(f'{act["title"]}: the text main published for the version in force {span} was right.') + ['']
        if x.get('metadata_changed'):
            msg += B.wrap('This correction records the supplied date or provenance metadata; its Files may name '
                          'unchanged text.') + ['']
    if x['restored']:
        msg += B.wrap(f'{len(x["restored"])} more file{"s" if len(x["restored"]) != 1 else ""} '
                      f'({", ".join(label(f) for f in x["restored"][:8])}{", …" if len(x["restored"]) > 8 else ""}) '
                      'are set back to this version, the one in force now, because corrections to earlier versions '
                      'changed them at the tip.') + ['']
    msg += B.wrap('The files of this commit hold the corrected text of this version, from the corpus. The history is '
                  'not re-sorted: the commits before it keep their text as first published, and readers apply this '
                  'commit to the days in its Corrects range.' +
                  (f' It supersedes {x["supersedes"][:12]} ("{x["sup_subject"]}").' if x['sup_subject'] else '')) + ['']
    msg += B.pre_1970(a)
    trailers = ['Kind: correction', f'In-force: {a}', f'Corrects: {s} {start}..{x["to"] or ""}',
                f'Supersedes: {x["supersedes"]}', f'Reason: {x["reason"]}', f'Act-path: {s}']
    trailers += [f'Files: {f}' for f in sorted(x['files'])]
    trailers += [f'{key}: {value}' for key, value in metadata_trailers(act, v, x.get('metadata', {})).items()]
    return msg, trailers


def cut(c: dict, docs_date: str) -> dict:
    """The corpus as main holds it: versions in force on or before docs_date."""
    return {**c, 'acts': [{**a, 'versions': vs} for a in c['acts']
                          if (vs := [v for v in a['versions'] if v['from'] <= docs_date])]}


def check_corrected(repo: Path, c: dict, docs_date: str) -> dict:
    """check_repo's check of main against the corpus up to docs_date, reading with correction commits applied (Reader):
    every version on its first day, the day before, and each historical/correction boundary inside it, file by file;
    and `tip_mismatches`,
    the files at main's tip that differ from the corpus on docs_date. The other counts (trailers, merges, dates) are
    check_repo's own."""
    import json
    import tempfile
    c = cut(c, docs_date)
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / 'corpus.json'
        p.write_text(json.dumps({**c, 'country': {**c['country'], 'future_branch': '.no-future-branch'}},
                                ensure_ascii=False), encoding='utf-8', newline='\n')
        res = K.check(repo, p)  # main only, whatever branches the clone holds
    rd = Reader(repo, [a['slug'] for a in c['acts']])
    head = git(repo, 'rev-parse', 'main').strip()
    mismatches, tip, versions, details = 0, 0, 0, []
    try:
        for act in c['acts']:
            s, vs = act['slug'], act['versions']
            for i, v in enumerate(vs):
                versions += 1
                if i + 1 < len(vs) and vs[i + 1]['from'] == v['from']:
                    continue
                before = next((w for w in reversed(vs[:i]) if w['from'] < v['from']), None)
                nxt = vs[i + 1]['from'] if i + 1 < len(vs) else '9999-12-31'
                days = {v['from']} | {d for d in rd.boundaries(s) | {docs_date} if v['from'] <= d < nxt and d <= docs_date}
                checks = [(day_before(v['from']), before)] + [(d, v) for d in sorted(days)]
                for day, want in checks:
                    have = rd.files(s, day)
                    expect = unit_oids(s, want) if want else None
                    if have == expect:
                        continue
                    n = (sum(1 for f in set(have) | set(expect) if have.get(f) != expect.get(f))
                         if have is not None and expect is not None else 1)
                    mismatches += n
                    if len(details) < 50:
                        details.append(f'{s} on {day}: {n} file(s) differ from version '
                                       f'{want["from"] if want else "(none)"}')
            want = unit_oids(s, corpus_on(vs, docs_date))
            have = K.tree_oids(rd.cat, head, s, rd.trees)
            bad = sorted(f for f in set(have) | set(want) if have.get(f) != want.get(f))
            tip += len(bad)
            if bad and len(details) < 50:
                details.append(f'{s} at the tip: {len(bad)} file(s) differ from the corpus, e.g. {bad[:3]}')
    finally:
        rd.close()
    return {**{k: res[k] for k in ('acts', 'trailer_errors', 'missing_in_force', 'merges', 'backwards', 'future_dated')},
            'versions': versions, 'mismatches': mismatches, 'tip_mismatches': tip, 'details': details,
            'corrections': len(rd.fixes)}


def to_append(c: dict, state: dict[str, str], docs_date: str) -> tuple[dict, set[str]]:
    """A corpus of only what is new. A held act keeps its newest held version as the base, so the first new version
    is planned as a change from it; that base's own 'start' commit is dropped (main has it)."""
    out = dict(c)
    acts, based = [], set()
    for act in c['acts']:
        vs = [v for v in act['versions'] if v['from'] <= docs_date]
        last = state.get(act['slug'])
        if last is None:
            if vs:
                acts.append({**act, 'versions': vs})
            continue
        held = [v for v in vs if v['from'] <= last]
        new = [v for v in vs if v['from'] > last]
        if new:
            acts.append({**act, 'versions': [held[-1]] + new})
            based.add(act['slug'])
    out['acts'] = acts
    return out, based


def published_log(repo: Path) -> list[dict]:
    text = git(repo, 'show', 'main:data/commits.csv')
    log = []
    for r in csv.DictReader(io.StringIO(text)):
        log.append({'day': r['day'], 'kind': r['kind'], 'law': r['law'] or None, 'acts': r['acts'].split(),
                    'units': int(r['files'] or 0), 'branch': r['branch'], 'clamped': r['day'] < '1970-01-01'})
    return log


class Appender:
    """`git fast-import` onto an existing main; separate author and committer dates."""

    def __init__(self, repo: Path, head: str, head_ct: int, head_tz: str):
        self.p = subprocess.Popen(['git', 'fast-import', '--quiet', '--done', '--date-format=raw'], cwd=repo,
                                  stdin=subprocess.PIPE)
        self.mark, self.parent, self.ct, self.tz = 0, head, head_ct, head_tz

    def _w(self, b: bytes):
        self.p.stdin.write(b)

    def _data(self, s: str):
        b = s.encode('utf-8')
        self._w(f'data {len(b)}\n'.encode() + b + b'\n')

    def commit(self, author: tuple[str, str], when: str, committer: tuple[str, str], message: str,
               files: dict[str, str | None]) -> int:
        self.mark += 1
        self.ct += 1
        self._w(f'commit refs/heads/main\nmark :{self.mark}\n'.encode())
        self._w(f'author {author[0]} <{author[1]}> {when}\n'.encode('utf-8'))
        self._w(f'committer {committer[0]} <{committer[1]}> {self.ct} {self.tz}\n'.encode('utf-8'))
        self._data(message)
        self._w((f'from {self.parent}\n' if isinstance(self.parent, str) else f'from :{self.parent}\n').encode())
        for path in sorted(files):
            if files[path] is None:
                self._w(f'D {path}\n'.encode('utf-8'))
            else:
                self._w(f'M 100644 inline {path}\n'.encode('utf-8'))
                self._data(files[path])
        self.parent = self.mark
        return self.mark

    def tag(self, name: str, mark: int):
        self._w(f'reset refs/tags/{name}\nfrom :{mark}\n\n'.encode('utf-8'))

    def finish(self):
        self._w(b'done\n')
        self.p.stdin.close()
        if self.p.wait():
            raise B.CorpusError('git fast-import failed')


def append(folder: Path, repo: Path, docs_date: str, dry_run: bool = False, corrections: bool = False,
           reason: str = DEFAULT_REASON) -> dict:
    try:
        required = published_parts.required(repo, folder)
    except published_parts.PublishedPartError as exc:
        raise B.CorpusError(str(exc)) from exc
    part_records = {}
    c, raw = B.load(folder, part_records=part_records, required_parts=required)
    errs = B.validate(c)
    if errs:
        raise B.CorpusError('corpus has problems:\n  ' + '\n  '.join(errs[:60]))
    c['_docs_date'] = docs_date
    if git(repo, 'status', '--porcelain', '--untracked-files=no').strip():
        raise B.CorpusError(f'{repo} has uncommitted changes; refusing')
    head = git(repo, 'rev-parse', 'main').strip()
    origin = subprocess.run(['git', 'rev-parse', '--verify', '-q', 'origin/main'], cwd=repo, capture_output=True,
                            text=True).stdout.strip()
    if origin and origin != head:
        raise B.CorpusError(f'main {head[:12]} is not origin/main {origin[:12]}: fetch and reset to the published head first')
    head_ct, head_tz = git(repo, 'log', '-1', '--format=%ct %ci', 'main').split()[0::3]
    head_ct = int(head_ct)
    state = published_state(repo, c, verify=not corrections)
    sub, based = to_append(c, state, docs_date)
    commits = B.plan(sub) if sub['acts'] else []
    commits = [x for x in commits if not (x['kind'] == 'start' and x['act']['slug'] in based)]
    existing_tags = set(git(repo, 'tag', '--list').split())
    co = c['country']
    committer = ('Lexifina', f'{co["slug"]}-law@lexifina.com')
    clock = B.Clock(co['tz'])
    planned = []
    for x in commits:
        if x['kind'] == 'start':
            author, msg, trailers = B.start_message(c, x)
            files = B.act_files(x['act'], x['version']['units'], None)
            touched = [x['act']['slug']]
        else:
            author, msg, trailers = B.change_message(c, x)
            files = {}
            for p in x['parts']:
                files.update(B.act_files(p['act'], p['cur']['units'], p['prev']['units'], p['keys']))
            touched = [p['act']['slug'] for p in x['parts']]
        B.check_trailers(trailers)
        planned.append({'x': x, 'day': x['day'], 'author': author, 'files': files, 'touched': touched,
                        'text': '\n'.join(msg).rstrip('\n') + '\n\n' + '\n'.join(trailers) + '\n'})
    fixes = plan_corrections(repo, c, head, state, reason) if corrections else []
    texts = []
    for x in fixes:
        msg, trailers = correction_message(c, x)
        B.check_trailers(trailers)
        texts.append('\n'.join(msg).rstrip('\n') + '\n\n' + '\n'.join(trailers) + '\n')
    summary = {'head': head, 'new_acts': sorted(a['slug'] for a in sub['acts'] if a['slug'] not in based),
               'extended_acts': sorted(based), 'commits': len(planned) + len(fixes), 'corrections': len(fixes)}
    if fixes:
        summary['corrected'] = {s: {'versions': sum(1 for x in fixes if x['act']['slug'] == s),
                                    'from': min(x['version']['from'] for x in fixes if x['act']['slug'] == s)}
                                for s in sorted({x['act']['slug'] for x in fixes})}
    if dry_run or not (planned or fixes):
        summary['main'] = head
        return summary
    w = Appender(repo, head, head_ct, head_tz)
    tags: dict[str, int] = {}
    log = []
    # Corrections first: the tip then holds each act's newest held version, which the appended versions build on.
    for x, text in zip(fixes, texts):
        w.commit(committer, clock.stamp(x['version']['from']), committer, text, x['files'])
        log.append({'day': x['version']['from'], 'kind': 'correction', 'law': None, 'acts': [x['act']['slug']],
                    'units': len(x['files']), 'branch': 'main', 'clamped': x['version']['from'] < '1970-01-01'})
    for e in planned:
        x = e['x']
        mark = w.commit(e['author'], clock.stamp(x['day']), committer, e['text'], e['files'])
        for s in e['touched']:
            tags.setdefault(f'{s}/{x["day"]}', mark)
        if x['kind'] == 'law':
            tags.setdefault(f'law/{x["law"]}', mark)
        elif x['kind'] == 'start' and x['act'].get('first_law'):
            tags.setdefault(f'law/{x["act"]["first_law"]}', mark)
        log.append({'day': x['day'], 'kind': x['kind'],
                    'law': x.get('law') or (x['act'].get('first_law') if x['kind'] == 'start' else None),
                    'acts': e['touched'], 'units': len(e['files']), 'branch': 'main', 'clamped': x['day'] < '1970-01-01'})
    full_log = published_log(repo) + log
    all_tags = {t: 0 for t in existing_tags} | {t: m for t, m in tags.items()}
    docs = B.docs_files(c, folder, raw, full_log, all_tags, docs_date, part_records=part_records)
    # Ship this script beside build.py, so the repository says how its appended commits were made.
    docs['tools/append.py'] = Path(__file__).read_text(encoding='utf-8').replace('\r\n', '\n')
    # Never future-dated: a docs date of today is noon local, so before then it is capped at now (else every later
    # append fails the future-dated check until noon).
    ts, tz = clock.stamp(docs_date).split()
    w.commit(committer, f'{min(int(ts), int(time.time()))} {tz}', committer,
             f'Documentation, tables, tools and REPRODUCE.md\n\nAppended {len(log)} commits to {head[:12]}'
             + (f' ({len(fixes)} of them corrections)' if fixes else '') + f'; corpus '
             f'sha256 {B.hashlib.sha256(raw).hexdigest()}, data retrieved {docs_date}.\n', docs)
    for name, mark in sorted(tags.items()):
        if name not in existing_tags:
            w.tag(name, mark)
    w.finish()
    git(repo, '-c', 'checkout.workers=0', 'checkout', '-q', '-f', 'main')
    new_head = git(repo, 'rev-parse', 'main').strip()
    if subprocess.run(['git', 'merge-base', '--is-ancestor', head, new_head], cwd=repo).returncode:
        raise B.CorpusError('internal: the published head is not an ancestor of the new main')
    summary.update({'main': new_head, 'tags_added': sum(1 for t in tags if t not in existing_tags)})
    return summary


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('folder')
    ap.add_argument('--repo', required=True)
    ap.add_argument('--docs-date', required=True)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--corrections', action='store_true',
                    help='where main holds text that differs from the corpus, append correction commits instead of '
                         'refusing')
    ap.add_argument('--reason', default=DEFAULT_REASON, help='the Reason trailer of a correction commit (one line)')
    a = ap.parse_args()
    print(append(Path(a.folder), Path(a.repo), a.docs_date, a.dry_run, a.corrections, a.reason))


if __name__ == '__main__':
    main()
