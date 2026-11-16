"""A repository that moved its act folders (Vietnam on 11 November 2026, Türkiye on 10 November) names each file by its old
folder in every commit before the move, and by its new folder after it. The detectors group files by folder, so an act's
history would be split in two at the move: the reference scan found no current provision with a history (keys_now=0), and
lapsed limits found no last change for any current file. data/paths.json at the pin maps each old folder to the new one;
this rewrites path and old_path in index/changes/<repo>.parquet to the new folders (run after ingest/extract.py)."""
import json, os, subprocess
import duckdb, pyarrow as pa

HERE = os.path.dirname(os.path.abspath(__file__))
pin = json.load(open(os.path.join(HERE, "pins.json"), encoding="utf-8"))["corpora"][0]
git = os.path.join(HERE, "sources", "corpus", pin["repo"] + ".git")
out = subprocess.run(["git", "show", f'{pin["sha"]}:data/paths.json'], cwd=git, capture_output=True)
moved = json.loads(out.stdout.decode("utf-8")).get("paths", {}) if out.returncode == 0 else {}
moved = {k: v for k, v in moved.items() if k != v}
f = os.path.join(HERE, "index", "changes", pin["repo"] + ".parquet")
if not moved:
    print("map_moved: no data/paths.json, nothing to map")
    raise SystemExit
t = duckdb.sql(f"select * from '{f.replace(chr(92), '/')}'").arrow()
if hasattr(t, "read_all"):
    t = t.read_all()


def m(p):
    if not p:
        return p
    head, _, name = p.rpartition("/")
    return f"{moved[head]}/{name}" if head in moved else p


n = 0
cols = {}
for c in ("path", "old_path"):
    vals = t.column(c).to_pylist()
    new = [m(v) for v in vals]
    n += sum(a != b for a, b in zip(vals, new))
    cols[c] = pa.array(new, pa.string())
for c, a in cols.items():
    t = t.set_column(t.schema.get_field_index(c), c, a)
tmp = f + ".new"
duckdb.from_arrow(t).write_parquet(tmp, compression="zstd")
os.replace(tmp, f)
print(f"map_moved: {len(moved)} folders, {n} paths rewritten to their folder since the move")
