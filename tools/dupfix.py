"""dupfix.py: lines a replay printed twice (or kept beside their successor), removed by a reviewed table.

dupsame.py lists every line printed twice in one unit on some day. Most are the law's own repetitions (dupsame_allow.json).
The rest are reading faults: Planalto prints a block twice (a Medida Provisória's insertion with its note and again with
the revoking note; a 1943 CLT article before and after the 1946 block that Decreto-Lei 8.987-A suspended), or a struck
wording without a note of its own stays beside its successor. dup_fixes.json lists each of those, reviewed against the
pages one by one: {"fixes": [{"part", "act", "unit", "from", "until", "op", ..., "why"}]}, applied to every version whose
day is in [from, until) (until null: to the last version):

    dedupe      "lines": each listed line printed more than once keeps only its first copy
    drop        "lines": every copy of each listed line is removed
    drop_block  "block": the last run of these consecutive lines is removed ("first": true: the first run)
    set         "lines": the unit's text is exactly these lines

Only the text of the named units changes; a version's changes are recomputed for those units only, and the run stops if
a fix would leave a unit changing in a version that does not credit it, or if a fix finds nothing to do on first
application. A part is fixed once: the decision added names the fixes (MARK), so a second run leaves it unchanged.

    python -X utf8 scripts/brazil-law/dupfix.py <part.json> [...]     fix those parts in place

effects_fix.py runs it on every part it is given (after lawrecords), so a reparse of a part keeps the fixes. No network.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TABLE = HERE / "dup_fixes.json"
MARK = "Doubled lines:"


def table() -> list[dict]:
    return json.loads(TABLE.read_text(encoding="utf-8"))["fixes"] if TABLE.exists() else []


def _apply_op(lines: list[str], f: dict) -> list[str]:
    op = f["op"]
    if op == "dedupe":
        out, seen = [], set()
        for x in lines:
            if x in f["lines"] and x in seen:
                continue
            seen.add(x)
            out.append(x)
        return out
    if op == "drop":
        return [x for x in lines if x not in f["lines"]]
    if op == "drop_block":
        b = f["block"]
        order = range(len(lines) - len(b) + 1) if f.get("first") else range(len(lines) - len(b), -1, -1)
        for i in order:
            if lines[i:i + len(b)] == b:
                return lines[:i] + lines[i + len(b):]
        return lines
    if op == "set":
        return list(f["lines"])
    raise ValueError(op)


def apply(part: dict, name: str, fixes: list[dict] | None = None) -> list[str]:
    """Apply the table's fixes for this part; returns one line per fix (or [] when there is none or it is done)."""
    fixes = [f for f in (table() if fixes is None else fixes) if f["part"] == name]
    if not fixes or any(x.startswith(MARK) for x in part.get("decisions", [])):
        return []
    done = []
    for act in part["acts"]:
        mine = [f for f in fixes if f["act"] == act["slug"]]
        if not mine:
            continue
        vs = act["versions"]
        units = sorted({f["unit"] for f in mine})
        # full text of each named unit in each version, before and after
        before, st = [], {}
        for v in vs:
            if v.get("units") is not None:
                st = {u: copy.deepcopy(v["units"].get(u)) for u in units}
            else:
                for u in units:
                    if u in (v.get("changes") or {}):
                        st[u] = copy.deepcopy(v["changes"][u])
            before.append({u: st.get(u) for u in units})
        # one copy per version: versions in which a unit does not change share its text object in `before`, and an op
        # applied to a shared object would be applied once per version (a drop_block then removes every run, not one)
        after = [copy.deepcopy(b) for b in before]
        for f in mine:
            n = 0
            for i, v in enumerate(vs):
                if v["from"] < f["from"] or (f["until"] and v["from"] >= f["until"]):
                    continue
                c = after[i][f["unit"]]
                if not isinstance(c, dict):
                    continue
                old = c["text"].split("\n")
                body, tail = (old[:-1], [""]) if old and old[-1] == "" else (old, [])
                new = _apply_op(body, f) + tail
                if new != old:
                    c["text"] = "\n".join(new)
                    n += 1
            if not n:
                raise SystemExit(f"dupfix: {name} {act['slug']} {f['unit']} {f['from']}..{f['until']} {f['op']}: nothing to fix")
            span = f"{f['from']}..{f['until'] or 'end'}"
            head = f"{act['slug']} {f['unit']} "
            if done and done[-1].startswith(head) and done[-1].endswith(": " + f["why"]):
                spans = done[-1][len(head):-len(": " + f["why"])]
                if spans.endswith(".." + f["from"]):                                  # the next period: one span
                    spans = spans[:-len(f["from"])] + (f["until"] or "end")
                else:
                    spans += ", " + span
                done[-1] = f"{head}{spans}: {f['why']}"
            else:
                done.append(f"{head}{span}: {f['why']}")
        # write back: first version's units, later versions' changes, for the named units only
        for i, v in enumerate(vs):
            for u in units:
                cur = after[i][u]
                if v.get("units") is not None:
                    if cur is None:
                        v["units"].pop(u, None)
                    else:
                        v["units"][u] = cur
                    continue
                prev = after[i - 1][u]
                was = u in (v.get("changes") or {})
                if cur != prev:
                    if not was and u not in (v.get("credits") or {}):
                        raise SystemExit(f"dupfix: {name} {act['slug']} {u} would change on {v['from']} with no credit")
                    v.setdefault("changes", {})[u] = cur
                elif was:
                    del v["changes"][u]
    if done:
        part["decisions"].append(
            MARK + " where the source prints a block twice, or a struck wording with no note of its own beside its "
            "successor, the doubled lines were removed after the replay (reviewed one by one against the pages; "
            "dupfix.py): " + " | ".join(done) + ".")
    return done


def apply_file(path: str | Path) -> list[str]:
    path = Path(path)
    part = json.loads(path.read_text(encoding="utf-8"))
    done = apply(part, path.stem)
    if done:
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(part, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8",
                       newline="\n")
        tmp.replace(path)
    return done


if __name__ == "__main__":
    for p in sys.argv[1:]:
        d = apply_file(p)
        print(Path(p).name, len(d), "doubled-line fixes" + (": " + " | ".join(d) if d else ""))
