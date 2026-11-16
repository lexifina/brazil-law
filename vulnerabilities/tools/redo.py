"""Re-runs a finished country after patch_detectors.py: only the steps the fixes change, then rebuilds out/.

    python -X utf8 redo.py <workspace dir D> [--fileact] [--workers N] [--keep-reviews] [--full]

--full: every step again through run.sh (extract, map_moved, all scans and detectors), all categories reviewed,
every review already made kept (triage skips ids it has); for repositories that moved their act folders.

D is the run's folder, holding gl/vulnerabilities/scripts, build_vulns.py and config.json (--fileact: one file per act). Steps:
 1. patch_detectors.py, patch_detectors_vi.py and patch_es.py on D/gl/vulnerabilities/scripts (S); map_moved.py into S
 2. delete the outputs those steps write (dates, amounts, refs; lapsed, references, empty periods, currencies)
 3. textscan, refscan, text_detectors, ref_detectors, late_extension, currency_scan
 4. model review again for lapsed_limit, dangling_ref and late_extension (old reviews kept in findings/run/pre-fix/;
    the other categories' reviews are unchanged, as their flags are)
 5. D/build_vulns.py (or D/build_czechia_vulns.py) -> D/out, chart, fonts
Log: S/redo.log.
"""
import glob, json, os, shutil, subprocess, sys, time

D = os.path.abspath(sys.argv[1])
FILEACT = "--fileact" in sys.argv
W = sys.argv[sys.argv.index("--workers") + 1] if "--workers" in sys.argv else "3"
KEEP = "--keep-reviews" in sys.argv  # a second pass: keep every review already made, review only new strong flags
S = os.path.join(D, "gl", "vulnerabilities", "scripts")
KIT = os.path.dirname(os.path.abspath(__file__))
PY = "C:/Python314/python.exe"
LOG = open(os.path.join(S, "redo.log"), "a", encoding="utf-8")
ENV = dict(os.environ, LE_WORKERS=W, LE_GREP_THREADS=W, PYTHONIOENCODING="utf-8", LE_PRIORITY="idle")
pins = json.load(open(os.path.join(S, "pins.json"), encoding="utf-8"))["corpora"][0]
REPO = pins["repo"]


def run(*cmd, cwd=S, env=ENV):
    LOG.write(f"\n+ {' '.join(cmd)}  [{time.strftime('%H:%M:%S')}]\n"); LOG.flush()
    r = subprocess.run(list(cmd), cwd=cwd, env=env, stdout=LOG, stderr=subprocess.STDOUT, creationflags=0x08000000)
    if r.returncode:
        LOG.write(f"FAILED ({r.returncode})\n"); LOG.flush()
        raise SystemExit(f"{os.path.basename(D)}: failed: {' '.join(cmd)} (see {S}/redo.log)")


def rm(*patterns):
    for p in patterns:
        for f in glob.glob(os.path.join(S, p)):
            shutil.rmtree(f) if os.path.isdir(f) else os.remove(f)


# 1. patch (and round 7, Vietnamese; map_moved.py for repositories that moved their act folders)
run(PY, "-X", "utf8", os.path.join(KIT, "patch_detectors.py"), S)
run(PY, "-X", "utf8", os.path.join(KIT, "patch_detectors_vi.py"), S)
run(PY, "-X", "utf8", os.path.join(KIT, "patch_es.py"), S)
shutil.copy2(os.path.join(KIT, "map_moved.py"), os.path.join(S, "map_moved.py"))
FULL = "--full" in sys.argv  # every step again from extract (index/changes changes, e.g. after map_moved), reviews kept
if FULL:
    KEEP = True
    shutil.copy2(os.path.join(KIT, "run.sh"), os.path.join(S, "run.sh"))
    rm("index/dates", "index/amounts", "index/amount_changes", "index/refs", "index/refs_fileact", "index/headings/" + REPO + ".parquet")
    F0 = os.path.join(S, "findings", "run")
    pre0 = os.path.join(F0, "pre-full"); os.makedirs(pre0, exist_ok=True)
    for f in glob.glob(os.path.join(F0, "*.*")):
        shutil.copy2(f, pre0)
    rm("findings/run/ranked_*.parquet", "findings/run/late_extension.jsonl", "findings/run/dead_currency.jsonl",
       "findings/run/*_scan.jsonl", "findings/runlaw/ranked_*.parquet")
    run("C:/Program Files/Git/bin/bash.exe", "run.sh", W)
F = os.path.join(S, "findings", "run")
P = [PY, "-X", "utf8"]
if not FULL:  # 2-3: only the steps the fixes change (FULL ran them all through run.sh above)
    # 2. clear what the changed steps write
    rm("index/dates", "index/amounts", "index/amount_changes", "index/refs_fileact/" + REPO + "*.parquet")
    if not FILEACT:
        rm("index/refs/" + REPO + "*.parquet")
    pre = os.path.join(F, "pre-fix"); os.makedirs(pre, exist_ok=True)
    for name in ("triage.jsonl", "late_extension_triage.jsonl", "late_extension_filtered.json", "ranked_lapsed_limit.parquet",
                 "ranked_dangling_ref.parquet", "late_extension.jsonl", "dead_currency.jsonl"):
        if os.path.exists(os.path.join(F, name)) and not os.path.exists(os.path.join(pre, name)):
            shutil.copy2(os.path.join(F, name), os.path.join(pre, name))
    rm("findings/run/ranked_lapsed_limit.parquet", "findings/run/ranked_stale_amount.parquet", "findings/run/ranked_dangling_ref.parquet",
       "findings/run/late_extension.jsonl", "findings/run/dead_currency.jsonl")
    if not KEEP:
        rm("findings/run/late_extension_triage.jsonl", "findings/run/late_extension_filtered.json", "findings/runlaw")
    # 3. detectors
    if FILEACT:
        run(*P, "ingest/textscan.py")
        run(*P, "ingest/refscan.py", "--fileact", REPO)
    else:
        run(*P, "ingest/textscan.py", "--shards", f"{REPO}:{W}")
        run(*P, "ingest/refscan.py", "--shards", f"{REPO}:{W}")
    for d, sub in (("refs", "refs_fileact"), ("refs_fileact", "refs")):  # ref_detectors reads both globs; an empty table where one is unused
        os.makedirs(os.path.join(S, "index", d), exist_ok=True)
        if not glob.glob(os.path.join(S, "index", d, "*.parquet")):
            src = glob.glob(os.path.join(S, "index", sub, "*.parquet"))[0].replace("\\", "/")
            run(*P, "-c", f"import duckdb; duckdb.sql(\"copy (select * from '{src}' limit 0) to 'index/{d}/_none.parquet' (format parquet)\")")
    run(*P, "detectors/text_detectors.py", "run")
    run(*P, "detectors/ref_detectors.py", "run")
    run(*P, "detectors/late_extension.py", "run")
    run(*P, "detectors/currency_scan.py", "run")
# 4. model review of the categories whose flags changed
T = os.path.join(F, "triage.jsonl")
if os.path.exists(T) and not KEEP:
    keep = [l for l in open(T, encoding="utf-8") if json.loads(l)["detector"] not in ("lapsed_limit", "dangling_ref")]
    open(T, "w", encoding="utf-8", newline="\n").writelines(keep)
# llm_env.sh may compute the key with a shell command, so source it in bash and read the environment back
out = subprocess.run(["C:/Program Files/Git/bin/bash.exe", "-c", "source ./llm_env.sh >/dev/null 2>&1; C:/Python314/python.exe -c 'import os,json; print(json.dumps({k: v for k, v in os.environ.items() if k.startswith(chr(76) + chr(76) + chr(77) + chr(95))}))'"],
                     cwd=S, capture_output=True, text=True).stdout
llm = json.loads(out or "{}")
if not llm.get("LLM_API_KEY"):
    raise SystemExit("llm_env.sh gave no LLM_API_KEY")
E2 = dict(ENV, **llm)
run(*P, "triage/triage.py", "run", "--per", "40", "--workers", "12", *([] if FULL else ["--dets", "lapsed_limit,dangling_ref"]), env=E2)
cfg = os.path.join(D, "config.json")
notlaw = json.load(open(cfg, encoding="utf-8"))["not_law"] if os.path.exists(cfg) else \
    ["navrhy/", "caselaw/", "usneseni-vlady/", "vestnik/", "metodika/", "data/", "tools/"]
rx = "^(" + "|".join(n.rstrip("/").replace(".", "\\.") for n in notlaw) + ")/"
os.makedirs(os.path.join(F, "..", "runlaw"), exist_ok=True)
run(*P, "-c", f"import duckdb; duckdb.sql(\"copy (select * from 'findings/run/ranked_lapsed_limit.parquet' where not regexp_matches(path, '{rx}')) to 'findings/runlaw/ranked_lapsed_limit.parquet' (format parquet)\")")
run(*P, "triage/triage.py", "runlaw", "--per", "40", "--workers", "12", "--dets", "lapsed_limit", env=E2)
run(*P, os.path.join(D, "late_ext_select.py"), env=E2)
LT, LF = os.path.join(F, "late_extension_triage.jsonl"), os.path.join(F, "late_extension_filtered.json")
rk = lambda r: (r["path"], r["old_until"], r["new_until"], r["law"], r["old_context"][:80], r["new_context"][:80])
if KEEP and os.path.exists(LT):  # review only the selected rows that have no review yet, then merge
    old = [json.loads(l) for l in open(LT, encoding="utf-8")]
    have = {rk(o["row"]) for o in old}
    sel = json.load(open(LF, encoding="utf-8"))
    new = [r for r in sel if rk(r) not in have]
    if new:
        json.dump(new, open(LF, "w", encoding="utf-8"), ensure_ascii=False)
        run(*P, "triage/late_ext_triage.py", "run", env=E2)
        fresh = [json.loads(l) for l in open(LT, encoding="utf-8")]
        json.dump(sel, open(LF, "w", encoding="utf-8"), ensure_ascii=False)
        open(LT, "w", encoding="utf-8", newline=chr(10)).writelines(json.dumps(x, ensure_ascii=False) + chr(10) for x in old + fresh)
    LOG.write(f"late extension: {len(new)} new of {len(sel)} selected reviewed" + chr(10))
else:
    run(*P, "triage/late_ext_triage.py", "run", env=E2)
run(*P, os.path.join(D, "late_ext_rebut.py"), env=E2)
# 5. rebuild
b = os.path.join(D, "build_czechia_vulns.py" if FILEACT else "build_vulns.py")
run(*P, b, os.path.join(D, "out"), cwd=D)
run(*P, os.path.join(D, "flags_chart.py"), os.path.join(D, "out", "data"), os.path.join(D, "out", "img"), cwd=D)
run(*P, os.environ.get("EMBED_FONTS", "embed_fonts.py"), *glob.glob(os.path.join(D, "out", "img", "*.svg")), cwd=D)
print(f"{os.path.basename(D)}: redo done")
