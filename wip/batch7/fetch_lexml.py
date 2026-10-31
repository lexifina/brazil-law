"""Fetch LexML URN records (one per cited law: its 'Publicação Original' DOU day) one at a time, 5 s apart (LexML's
robots.txt Crawl-delay; /urn/ is allowed), into ../.cache/<sha256 of the URL>.bin where parse_proc reads them.

    python -X utf8 scripts/brazil-law/batch7/fetch_lexml.py <file with one URL per line>
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import fetch as FT  # noqa: E402

DELAY = 5.0


def main(path: str) -> int:
    urls = [u.strip() for u in Path(path).read_text(encoding="utf-8").splitlines() if u.strip()]
    todo = [u for u in urls if "lexml.gov.br/urn/" in u and not FT.cached(u)]
    print(len(todo), "to fetch of", len(urls), flush=True)
    bad = 0
    for i, u in enumerate(todo):
        if i:
            time.sleep(DELAY)
        r = subprocess.run(["curl", "-s", "-L", "--compressed", "--max-time", "60", "-A", FT.UA, "-w", "%{http_code}",
                            "-o", "-", u], capture_output=True)
        body, code = r.stdout[:-3], r.stdout[-3:].decode("ascii", "replace")
        with FT.LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"url": u, "status": code, "bytes": len(body), "via": "curl (Crawl-delay 5)"}) + "\n")
        if code == "200" and body:
            p = FT.CACHE / (FT.key(u) + ".bin")
            tmp = p.with_suffix(".part")
            tmp.write_bytes(body)
            tmp.replace(p)
        else:
            bad += 1
            print("FAIL", code, u, flush=True)
            if code in ("429", "503"):
                time.sleep(60)
    print("done; failed", bad, flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
