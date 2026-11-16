"""Builds a country repository's vulnerabilities/ folder from the one-country run of global-law's detectors and model review.

    python -X utf8 build_vulns.py <out dir>

config.json (next to this script): repo, lang (the native language code), cats ({detector: native category name}),
not_law (top-level folders that are not law).

Inputs (from gl/vulnerabilities/scripts/): findings/run/*.parquet and *.jsonl, findings/run/triage.jsonl (and
findings/runlaw/triage.jsonl, the review of law texts only), pins.json.
Writes <out>/data/flags.csv, <out>/data/reviewed.csv, <out>/data/by_category.csv. The READMEs are written by hand.
"""
import csv, json, os, subprocess, sys
from collections import Counter
import duckdb

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, "gl", "vulnerabilities", "scripts")
RUN = os.path.join(SCR, "findings", "run")
OUT = sys.argv[1]
PIN = json.load(open(os.path.join(SCR, "pins.json"), encoding="utf-8"))["corpora"][0]["sha"]
CFG = json.load(open(os.path.join(HERE, "config.json"), encoding="utf-8"))
REPO, LANG = CFG["repo"], CFG["lang"]
NATIVE = [] if LANG == "en" else ["category_" + LANG]   # an English-only repository has no second category column
BLOB = f"https://github.com/lexifina/{REPO}/blob/{PIN}/"
COMMIT = f"https://github.com/lexifina/{REPO}/commit/"

CATS = {  # detector -> (English, native: replaced from config.json) category, as in global-law's list
    "lapsed_limit": ("Lapsed time limits", "Uplynulé lhůty"),
    "repeal_gap": ("Repeal gaps", "Mezery po zrušení"),
    "same_day_conflict": ("Same-day conflicts", "Změny téhož dne"),
    "retroactive_date": ("Retroactive or pre-publication dates", "Účinnost před vyhlášením"),
    "late_extension": ("Empty periods", "Prázdná období"),
    "stale_amount": ("Stale amounts", "Zastaralé částky"),
    "dangling_ref": ("References to deleted provisions", "Odkazy na zrušená ustanovení"),
    "placeholder_ref": ("References to repealed placeholders", "Odkazy na ustanovení „zrušeno“"),
    "dead_fine": ("Dead fines", "Pokuty bez skutkové podstaty"),
    "dup_label": ("Duplicate numbering", "Dvojí číslování"),
    "dead_currency": ("Dead currencies", "Zaniklé měny"),
    "publisher_flag": ("Publisher notes", "Poznámky vydavatele"),
    "dead_act_ref": ("Citations of acts no longer in force", "Citations of acts no longer in force"),  # Spain only (es_crossref.py)
}
# parts of this repository that are not law: bills and drafts, case law, government resolutions, ministry bulletins, guidance
NOT_LAW = tuple(CFG["not_law"])
CATS = {d: (en, CFG["cats"].get(d, en)) for d, (en, _) in CATS.items()}


NOT_LAW_FILES = tuple(CFG.get("not_law_files", []))  # file names that are not law wherever they are (an act's index of blocks)


def kind_of(path: str) -> str:
    return "other" if path and (path.startswith(NOT_LAW) or (NOT_LAW_FILES and path.rsplit("/", 1)[-1] in NOT_LAW_FILES)) else "law"


con = duckdb.connect()


def pq(name):
    p = os.path.join(RUN, name)
    if not os.path.exists(p):
        return []
    q = con.sql(f"select * from '{p.replace(chr(92), '/')}'")
    cols = q.columns
    return [dict(zip(cols, r)) for r in q.fetchall()]


def ident(det, d):
    """the same key for a findings row and the row stored with its review"""
    if det == "dead_act_ref":
        return (det, d.get("path") or "", str(d.get("cited_id") or ""), str(d.get("line") or ""))
    return (det, d.get("path") or d.get("law") or "", str(d.get("in_force") or d.get("removed_on") or d.get("until") or ""),
            str(d.get("ref") or ""), (d.get("context") or "").replace("\n", " ")[:400] if det == "lapsed_limit" else "",
            f'{d.get("old")}>{d.get("new")}' if det == "stale_amount" else
            f'{d.get("old_until")}>{d.get("new_until")}>{d.get("law")}>{d.get("old_context") or ""}>{d.get("new_context") or ""}'
            if det == "late_extension" else "")


# retroactive-date links: the commit that made this act's version on this day, from the detectors' history table
ROOT_COMMIT = {}
for _law, _inf, _c in duckdb.sql(f"""select law, in_force, corpus_commit from '{os.path.join(SCR, "index", "root.parquet").replace(chr(92), "/")}'
                                   where corpus = '{json.load(open(os.path.join(SCR, "pins.json"), encoding="utf-8"))["corpora"][0]["path"]}'
                                   and kind = 'law' order by in_force""").fetchall():
    ROOT_COMMIT.setdefault((_law, str(_inf)), _c)
AUTHOR_COMMIT = {}
for line in subprocess.run(["git", "-C", os.path.join(SCR, "sources", "corpus", REPO + ".git"), "log", "--format=%H%x09%an", PIN],
                           capture_output=True, text=True, encoding="utf-8").stdout.splitlines():
    sha, an = line.split("\t", 1)
    AUTHOR_COMMIT.setdefault(an, sha)

GIT = os.path.join(SCR, "sources", "corpus", REPO + ".git")
TREE = set(subprocess.run(["git", "-C", GIT, "ls-tree", "-r", "--name-only", PIN], capture_output=True, text=True,
                          encoding="utf-8").stdout.splitlines())
_last = None


def blob_url(path):
    """the file at the pinned commit, or, for one deleted since, at the parent of the commit that deleted it (one git log pass)"""
    global _last
    if path in TREE:
        return BLOB + path
    if _last is None:
        _last = {}
        out = subprocess.run(["git", "-C", GIT, "log", "--diff-filter=D", "--name-only", "--format=%x1e%P", PIN],
                             capture_output=True).stdout.decode("utf-8", "replace")
        for rec in out.split(chr(0x1e))[1:]:
            head, _, names = rec.partition(chr(10))
            parent = head.split()[0] if head.split() else ""
            for n in names.splitlines():
                if n.strip():
                    _last.setdefault(n.strip(), parent)
    if not _last.get(path):  # deleted before the repository moved its act folders: look it up under its old folder (data/paths.json)
        head, _, name = path.rpartition("/")
        old = f"{OLD_FOLDER[head]}/{name}" if head in OLD_FOLDER else ""
        return f"https://github.com/lexifina/{REPO}/blob/{_last[old]}/{old}" if old and _last.get(old) else ""
    return f"https://github.com/lexifina/{REPO}/blob/{_last[path]}/{path}"


def _old_folders():
    """paths.json maps each act's old folder (its id) to its folder since the move; the detectors read today's folders"""
    out = subprocess.run(["git", "-C", GIT, "show", f"{PIN}:data/paths.json"], capture_output=True)
    if out.returncode:
        return {}
    p = json.loads(out.stdout.decode("utf-8")).get("paths", {})
    return {v: k for k, v in p.items()} if isinstance(p, dict) else {}


OLD_FOLDER = _old_folders()


rows = []


def add(det, d, **r):
    r.setdefault("url", blob_url(r["path"]) if r.get("path") else "")
    r["_id"] = ident(det, d)
    rows.append(dict(detector=det, **r))


for d in pq("ranked_lapsed_limit.parquet"):
    add("lapsed_limit", d, path=d["path"], date=str(d["until"] or ""), reference=d.get("last_law") or "",
        summary=(d.get("context") or "").replace("\n", " ")[:400], score=round(d["score"] or 0, 3))
for d in pq("ranked_repeal_gap.parquet"):
    add("repeal_gap", d, path=d["path"], date=str(d["removed_on"]), reference=f'{d["removed_by"]} -> {d["back_by"]}',
        summary=f'removed {d["removed_on"]}, back {d["back_on"]} ({d["gap_days"]} days without text)', score=round(d["score"] or 0, 3))
for d in pq("ranked_same_day_conflict.parquet"):
    add("same_day_conflict", d, path=d["path"], date=str(d["in_force"]), reference="; ".join(d["laws"] or []),
        summary=f'{d["n_laws"]} acts change it on {d["in_force"]}, made {d["spread_days"]} days apart', score=round(d["score"] or 0, 3))
# retroactive dates are per act, not per file: the path is the first file the act's commit on that day wrote,
# so kind_of can tell notices, circulars and decisions from law
FIRST_PATH = dict(con.sql(f"""select commit, min(path)
    from '{os.path.join(SCR, "index", "changes", REPO + ".parquet").replace(chr(92), "/")}' group by 1""").fetchall())
for d in pq("ranked_retroactive_date.parquet"):
    first = ROOT_COMMIT.get((d["law"], str(d["in_force"])), "") or AUTHOR_COMMIT.get(d["law"], "")
    add("retroactive_date", d, path=FIRST_PATH.get(first, ""), date=str(d["in_force"]), reference=d["law"],
        summary=f'in force {d["in_force"]}, {d["made_field"].lower()} {d["made"]} ({d["back_days"]} days earlier): {d.get("subject") or ""}'[:400],
        score=round(d["score"] or 0, 3), url=(COMMIT + first) if first else "")
for d in pq("ranked_stale_amount.parquet"):
    add("stale_amount", d, path=d["path"], date=str(d["in_force"]), reference=d.get("law") or "",
        summary=f'{d["law"]} changed {d["old"]} to {d["new"]}; {d["old"]} still appears {d.get("n_other") or ""} time(s): {d.get("still_in") or ""}'[:400],
        score=round(d["score"] or 0, 3))
for d in pq("ranked_dangling_ref.parquet"):
    # removed_on is empty when no law change removed the target file (the detector then names the act of its last version)
    add("dangling_ref", d, path=d["path"], date=str(d.get("removed_on") or d.get("target_last_seen") or ""),
        reference=f'{d["ref"]} (removed by {d.get("removed_by") or "?"})' if d.get("removed_on") else
        f'{d["ref"]} ({d.get("target_path") or "?"}, last in the record {d.get("target_last_seen")})',
        summary=(d.get("context") or "").replace("\n", " ")[:400], score=round(d["score"] or 0, 3))
for d in pq("ranked_dead_act_ref.parquet"):
    add("dead_act_ref", d, path=d["path"], date=str(d.get("citing_last_change") or ""),
        reference=f'{d["cite"]} ({d["cited_id"]}, {d["cited_rango"]}: {d["cited_title"]})'[:300],
        summary=f'line {d["line"]}: ' + (d.get("context") or "").replace("\n", " ")[:380], score=round(d["score"] or 0, 3))
p = os.path.join(RUN, "late_extension.jsonl")
for d in (json.loads(l) for l in open(p, encoding="utf-8")) if os.path.exists(p) else ():
    add("late_extension", d, path=d["path"], date=d["old_until"], reference=d["law"],
        summary=f'"until {d["old_until"]}" became "until {d["new_until"]}" by {d["law"]}, in force {d["extended_in_force"]} ({d["gap_days"]} days after the old end)',
        score="")
for det in ("placeholder_ref", "dead_fine", "dup_label", "dead_currency", "publisher_flag"):
    p = os.path.join(RUN, f"{det}.jsonl")
    if not os.path.exists(p):
        continue
    for line in open(p, encoding="utf-8"):
        d = json.loads(line)
        if det == "dup_label":
            summ = f'"{d.get("label")}" appears {d.get("n")} times'
        else:
            summ = (d.get("text") or d.get("context") or d.get("why") or json.dumps({k: v for k, v in d.items() if k not in ("corpus", "repo", "path")},
                                                                                   ensure_ascii=False)).replace("\n", " ")[:300]
        add(det, d, path=d.get("path") or "", date=str(d.get("in_force") or d.get("date") or ""),
            reference=str(d.get("line") or d.get("ref") or d.get("law") or ""), summary=summ, score="")

# the model review (where a flag was reviewed twice, the later review is kept)
rev = {}
TRIAGE = [os.path.join(RUN, "triage.jsonl"), os.path.join(os.path.dirname(RUN), "runlaw", "triage.jsonl")]
for line in (l for f in TRIAGE if os.path.exists(f) for l in open(f, encoding="utf-8")):
    d = json.loads(line)
    rev[ident(d["detector"], d["row"])] = d
# empty periods: global-law's late_ext_triage.py, then late_ext_rebut.py (the same rebuttal step as above)
LE = {"candidate_gap": "candidate_defect", "no_gap": "lawful", "artefact": "artefact"}
p = os.path.join(RUN, "late_extension_triage.jsonl")
for d in (json.loads(l) for l in open(p, encoding="utf-8")) if os.path.exists(p) else ():
    rev[ident("late_extension", d["row"])] = {"verify": {"verdict": LE[d["j"]["verdict"]], "reason": d["j"]["one_line"]}, "rebut": d.get("rebut")}
# citations of acts no longer in force (Spain): global-law's dead_ref_triage.py, then dead_ref_rebut.py
DR = {"candidate_defect": "candidate_defect", "cured_or_harmless": "lawful", "artefact": "artefact"}
p = os.path.join(RUN, "dead_act_ref_triage.jsonl")
for d in (json.loads(l) for l in open(p, encoding="utf-8")) if os.path.exists(p) else ():
    rev[ident("dead_act_ref", d["row"])] = {"verify": {"verdict": DR[d["j"]["verdict"]], "reason": d["j"]["one_line"]}, "rebut": d.get("rebut")}
for r in rows:
    d = rev.get(r.pop("_id"))
    v = (d or {}).get("verify") or {}
    b = (d or {}).get("rebut") or {}
    r["review"] = v.get("verdict", "")
    r["review_note"] = v.get("reason", "")
    r["survives_rebuttal"] = "" if not b else ("yes" if b.get("survives") else "no")
    r["category"] = CATS[r["detector"]][0]
    if NATIVE:
        r[NATIVE[0]] = CATS[r["detector"]][1]
    r["kind"] = kind_of(r["path"])
print(sum(1 for r in rows if r["review"]), "of", len(rev), "reviews matched to a flag")

os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
fields = ["category", *NATIVE, "detector", "kind", "path", "date", "reference", "summary", "score", "review", "survives_rebuttal", "review_note", "url"]
rows.sort(key=lambda r: (list(CATS).index(r["detector"]), r["kind"] != "law", -(r["score"] or 0) if r["score"] != "" else 0))
for name, sel in (("flags.csv", rows), ("reviewed.csv", [r for r in rows if r["review"]])):
    with open(os.path.join(OUT, "data", name), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(sel)
tot = Counter(r["detector"] for r in rows)
law = Counter(r["detector"] for r in rows if r["kind"] == "law")
revd = Counter(r["detector"] for r in rows if r["review"])
cand = Counter(r["detector"] for r in rows if r["review"] == "candidate_defect")
surv = Counter(r["detector"] for r in rows if r["survives_rebuttal"] == "yes")
with open(os.path.join(OUT, "data", "by_category.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["category", *NATIVE, "flags", "in_law_texts", "model_reviewed", "candidate_defects", "survive_rebuttal"])
    for det, (en, cs) in CATS.items():
        if tot[det]:
            w.writerow([en, *([cs] if NATIVE else []), tot[det], law[det], revd[det], cand[det], surv[det]])
print(len(rows), "flags;", sum(revd.values()), "reviewed;", sum(cand.values()), "candidates;", sum(surv.values()), "survive")
for det, (en, cs) in CATS.items():
    if tot[det]:
        print(f"{en:40s} {tot[det]:6d} law {law[det]:6d} rev {revd[det]:4d} cand {cand[det]:3d} surv {surv[det]:3d}")
