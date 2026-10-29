"""Fetch Brazilian federal law sources into .cache/ (curl only, polite, resumable).

Usage:
    python -X utf8 scripts/brazil-law/fetch.py plan          # fetch everything in sources.json
    python -X utf8 scripts/brazil-law/fetch.py url URL...    # fetch single URLs into the cache

Every file is cached under .cache/<sha256(url)>.<ext>; each network request is
appended to .cache/requests.jsonl.  At most one request per second per host.

Planalto (www.planalto.gov.br) answers "Acesso Negado" to non-browser user
agents, so official pages are read from Internet Archive captures of the
Planalto URL (the raw `id_` form, byte-identical to what Planalto served).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = HERE / ".cache"
LOG = CACHE / "requests.jsonl"
UA = "lexifina-watch/1.0 (+https://lexifina.com/watch; corpus@lexifina.com)"
_last: dict[str, float] = {}


def key(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def cached(url: str) -> Path | None:
    p = CACHE / (key(url) + ".bin")
    return p if p.exists() and p.stat().st_size > 0 else None


def _polite(host: str) -> None:
    now = time.time()
    wait = 1.0 - (now - _last.get(host, 0))
    if wait > 0:
        time.sleep(wait)
    _last[host] = time.time()


def get(url: str, *, retries: int = 4, refresh: bool = False) -> Path:
    """Return the cache path for url, downloading it if needed."""
    CACHE.mkdir(exist_ok=True)
    gi = CACHE / ".gitignore"
    if not gi.exists():
        gi.write_text("*\n", encoding="utf-8")
    out = CACHE / (key(url) + ".bin")
    if out.exists() and out.stat().st_size > 0 and not refresh:
        return out
    host = urllib.parse.urlsplit(url).hostname or ""
    tmp = out.with_suffix(".part")
    err = ""
    for attempt in range(retries):
        _polite(host)
        t0 = time.time()
        r = subprocess.run(
            ["curl", "-s", "-L", "--compressed", "-A", UA, "--max-time", "180",
             "-o", str(tmp), "-w", "%{http_code} %{content_type}", url],
            capture_output=True, text=True)
        code, _, ctype = (r.stdout or "000 ").partition(" ")
        size = tmp.stat().st_size if tmp.exists() else 0
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "url": url, "status": code,
                                "type": ctype, "bytes": size, "secs": round(time.time() - t0, 2),
                                "sha256_url": key(url)}) + "\n")
        if code == "200" and size > 0:
            os.replace(tmp, out)
            return out
        err = f"HTTP {code} ({r.stderr.strip()[:200]})"
        if code in ("404", "403", "410"):
            break
        time.sleep(3 * (attempt + 1))
    if tmp.exists():
        tmp.unlink()
    raise RuntimeError(f"fetch failed: {url}: {err}")


def wayback(url: str, ts: str) -> str:
    """Raw Internet Archive capture of url at timestamp ts."""
    return f"https://web.archive.org/web/{ts}id_/{url}"


def cdx(url: str, **params) -> list[list[str]]:
    q = {"url": url, "output": "json", **params}
    p = get("https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(q))
    txt = p.read_text(encoding="utf-8", errors="replace").strip()
    if not txt:
        return []
    rows = json.loads(txt)
    return rows[1:] if rows else []


def pick(url: str, min_len: int = 3000, before: str | None = None) -> str | None:
    """Newest 200 capture of url longer than min_len bytes (Planalto's block page is ~800 bytes)."""
    params = {"filter": "statuscode:200", "fl": "timestamp,length", "limit": "-25"}
    if before:
        params["to"] = before
    rows = cdx(url, **params)
    good = [ts for ts, ln in rows if ln.isdigit() and int(ln) >= min_len]
    return max(good) if good else None


PL = "https://www.planalto.gov.br/ccivil_03/"
FIXED = {
    "cf": "constituicao/constituicao.htm",
    "cf-compilado": "constituicao/constituicaocompilado.htm",
    "quadro-emc": "constituicao/emendas/emc/quadro_emc.htm",
}


def discover() -> None:
    """Choose a Wayback capture for every Planalto page we read; writes sources.json (pinned timestamps)."""
    path = HERE / "sources.json"
    plan = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"fetch": []}
    have = {i["id"]: i for i in plan["fetch"]}
    want = dict(FIXED)
    for n in range(1, 160):
        want[f"emc-{n}"] = f"constituicao/emendas/emc/emc{n:02d}.htm" if n < 10 else f"constituicao/emendas/emc/emc{n}.htm"
    for n in range(1, 7):
        want[f"ecr-{n}"] = f"constituicao/emendas/ecr/ecr{n}.htm"
    for k, v in json.loads((HERE / "acts.json").read_text(encoding="utf-8")).items() if (HERE / "acts.json").exists() else []:
        want[k] = v
    for i, (ident, rel) in enumerate(want.items()):
        if ident in have and (have[ident].get("ts") or ident.startswith("emc-")):
            continue
        url = PL + rel
        try:
            ts = pick(url.split("://", 1)[1])
        except RuntimeError as e:
            print("cdx error", ident, e)
            continue
        have[ident] = {"id": ident, "url": url, "ts": ts}
        path.write_text(json.dumps({"fetch": list(have.values())}, indent=1, ensure_ascii=False), encoding="utf-8")
        print(ident, ts, flush=True)
        if ident.startswith("emc-") and ts is None and int(ident[4:]) > 141:
            break
    plan["fetch"] = sorted(have.values(), key=lambda i: list(want).index(i["id"]) if i["id"] in want else 9999)
    path.write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "url":
        for u in argv[1:]:
            print(get(u))
        return 0
    if argv[0] == "pick":
        # pick: choose the newest good Wayback capture for each Planalto path given
        for u in argv[1:]:
            print(u, pick(u))
        return 0
    if argv[0] == "discover":
        discover()
        return 0
    if argv[0] == "plan":
        plan = json.loads((HERE / "sources.json").read_text(encoding="utf-8"))
        for item in plan["fetch"]:
            if not item.get("ts"):
                print("NO CAPTURE", item["id"])
                continue
            u = wayback(item["url"], item["ts"])
            try:
                print(get(u).name, u)
            except RuntimeError as e:
                print("FAIL", e)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
