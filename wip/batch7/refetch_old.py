"""Refetch into ../.cache every Internet Archive capture pinned (id, url, ts) by the older Brazil parts' pin files, where
the cache lost it (the restore to alan-dell did not carry .cache). Same capture, same cache path as ../fetch.py; read
through gitlaw_common/wayback.py's one machine-wide archive.org rate.

    python -X utf8 scripts/brazil-law/batch7/refetch_old.py <pin file> [...]
"""
from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent.parent / "gitlaw_common"))
import fetch as FT  # noqa: E402
import wayback  # noqa: E402


def one(item: dict) -> bool:
    u = FT.wayback(item["url"], item["ts"])
    if FT.cached(u):
        return True
    body = wayback.fetch(u, None)
    if not body:
        return False
    p = FT.CACHE / (FT.key(u) + ".bin")
    tmp = p.with_suffix(".part")
    tmp.write_bytes(body)
    tmp.replace(p)
    with FT.LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"url": u, "status": 200, "bytes": len(body), "via": "wayback.fetch (refetch)"}) + "\n")
    return True


def main(files: list[str]) -> int:
    items = []
    for f in files:
        items += [i for i in json.loads(Path(f).read_text(encoding="utf-8"))["fetch"] if i.get("ts") and not i.get("via")]
    todo = [i for i in items if not FT.cached(FT.wayback(i["url"], i["ts"]))]
    print(len(items), "pins,", len(todo), "to fetch", flush=True)
    with ThreadPoolExecutor(4) as ex:
        ok = list(ex.map(one, todo))
    bad = [i["id"] for i, o in zip(todo, ok) if not o]
    print("failed", len(bad), bad[:20], flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
