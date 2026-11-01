"""lawrecords.py: one record per law key in every Brazil part.

A law key shared by several parts must have the same record (label, title, kind, enacted, published, url, ...) in each:
the builder keeps the first part's record, so a part that differs shows nothing of its own, and a reader of the parts
finds two records for one law. law_records.json holds the agreed record of every key the parts once wrote differently
(the form most parts used; on a tie the record of the first part in build order, which the published history showed).

    python -X utf8 scripts/brazil-law/lawrecords.py <part.json> [...]     set those keys' records in each part (in place)

effects_fix.py runs it on every part it is given, so a reparse of a batch part keeps the agreed records. The check that
no two parts differ is batch17/.tmp/uniqlaws.py (pipe.sh runs it). No network.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TABLE = HERE / "law_records.json"


def canon() -> dict[str, dict]:
    return json.loads(TABLE.read_text(encoding="utf-8")) if TABLE.exists() else {}


def apply(part: dict, table: dict[str, dict] | None = None) -> list[str]:
    """Set the agreed record of every key of the table the part holds; returns 'key: field, ...' for each change."""
    table = canon() if table is None else table
    changed = []
    for key, law in part.get("laws", {}).items():
        want = table.get(key)
        if want is None:
            continue
        fields = [f for f in sorted(set(law) | set(want)) if law.get(f) != want.get(f)]
        if fields:
            for f in fields:
                if f in want:
                    law[f] = want[f]
                else:
                    law.pop(f)
            changed.append(f"{key}: {', '.join(fields)}")
    return changed


def apply_file(path: str | Path) -> list[str]:
    path = Path(path)
    part = json.loads(path.read_text(encoding="utf-8"))
    changed = apply(part)
    if changed:
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(part, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8",
                       newline="\n")
        tmp.replace(path)
    return changed


if __name__ == "__main__":
    for p in sys.argv[1:]:
        ch = apply_file(p)
        print(Path(p).name, len(ch), "law records set" + (": " + "; ".join(ch) if ch else ""))
