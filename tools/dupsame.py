"""dupsame.py [--allow FILE] <part.json>...: lines (over 30 characters) printed twice in one unit on some day.

Every version is replayed (full `units` replace the state, `changes` are applied to it), and each unit's text is read on
every day. A line printed twice in one unit is either the law's own repetition (a penalty line after several items, a
quoted amendment that repeats an item, a table) or a reading fault (a wording kept beside its successor). The reviewed
repetitions are listed in dupsame_allow.json beside this script: {"lines": [{"act", "unit", "line", "why"}]}. A hit not
in that list is printed as 'HIT <part> <act> <first day> <unit> <line>', and the exit status is 1; allowlisted hits are
only counted. Allowlist entries no part matches any more are printed as 'STALE' (exit status unchanged).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

MIN = 30


def hits(path):
    """(act slug, unit, line, first day) for every line printed twice in one unit on some day."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    out = []
    for a in d.get("acts", []):
        st, seen = {}, set()
        for v in a["versions"]:
            if v.get("units") is not None:
                st = dict(v["units"])
                touched = list(st)
            else:
                touched = []
                for u, c in (v.get("changes") or {}).items():
                    st[u] = c
                    touched.append(u)
            for u in touched:
                c = st.get(u)
                if not isinstance(c, dict):
                    continue
                ls = [x for x in c.get("text", "").split("\n") if len(x) > MIN]
                for x in sorted({x for x in ls if ls.count(x) > 1}):
                    if (u, x) not in seen:
                        seen.add((u, x))
                        out.append((a["slug"], u, x, v["from"]))
    return out


def main(argv):
    allow_path = Path(__file__).with_name("dupsame_allow.json")
    if argv[:1] == ["--allow"]:
        allow_path, argv = Path(argv[1]), argv[2:]
    allow = json.loads(allow_path.read_text(encoding="utf-8"))["lines"] if allow_path.exists() else []
    ok = {(e["act"], e["unit"], e["line"]) for e in allow}
    used, bad, n_ok = set(), 0, 0
    acts = set()
    for f in argv:
        for slug, u, x, day in hits(f):
            acts.add(slug)
            if (slug, u, x) in ok:
                used.add((slug, u, x)); n_ok += 1
            else:
                bad += 1
                print("HIT", Path(f).name, slug, day, u, x)
        acts.update(a["slug"] for a in json.loads(Path(f).read_text(encoding="utf-8")).get("acts", []))
    for k in sorted(ok - used):
        if k[0] in acts:
            print("STALE", *k)
    print(f"dupsame: {bad} hits, {n_ok} allowlisted")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
