"""Hand-check helper: for each empty-period flag that survived the rebuttal, the extending commit's word diff (lines that
change a date), its In-force/Published trailers, and, where this repository holds the extending act (as lei-N-de-Y/,
lei-complementar-N-de-Y/ or decreto-lei-N-de-Y/), that act's provisions on when it takes effect.

    python -X utf8 late_ext_check.py        (run in the workspace folder, next to gl/)
"""
import json, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(HERE, "gl", "vulnerabilities", "scripts")
G = os.path.join(S, "sources", "corpus", "brazil-law.git")
PIN = json.load(open(os.path.join(S, "pins.json"), encoding="utf-8"))["corpora"][0]["sha"]
DATE = re.compile(r"\d{1,2}[ºo°]? de (?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro) de|\b(?:19|20)\d\d\b")
VIG = re.compile(r"(?i)entra(?:m|rá|rão)? em vigor|produz\w* efeitos|retroag|com efeitos? a partir")


def git(*a):
    return subprocess.run(["git", "--git-dir", G, *a], capture_output=True).stdout.decode("utf-8", "replace")


def folder(law):
    m = re.match(r"(Lei Complementar|Lei|Decreto-Lei) nº ([\d.]+), de (\d{4})", law)
    if not m:
        return None
    pre = {"Lei Complementar": "lei-complementar", "Lei": "lei", "Decreto-Lei": "decreto-lei"}[m.group(1)]
    return f"{pre}-{m.group(2).replace('.', '')}-de-{m.group(3)}"


seen = set()
for x in map(json.loads, open(os.path.join(S, "findings", "run", "late_extension_triage.jsonl"), encoding="utf-8")):
    if not (x.get("rebut") or {}).get("survives"):
        continue
    r = x["row"]; k = (r["path"], r["old_until"], r["new_until"], r["law"])
    if k in seen:
        continue
    seen.add(k)
    print(f"## {r['path']}\n   {r['old_until']} -> {r['new_until']} by {r['law']} in force {r['extended_in_force']} ({r['gap_days']} d)")
    for line in git("log", "--format=%h%x09%an", PIN, "--", r["path"]).splitlines():
        cc, an = line.split("\t", 1)
        if an != r["law"]:
            continue
        print("   ", cc, " ".join(l for l in git("log", "-1", "--format=%B", cc).splitlines() if l.startswith(("In-force", "Published", "Enacted"))))
        for l in git("diff", "--word-diff", "-U0", f"{cc}^", cc, "--", r["path"]).splitlines():
            if ("{+" in l or "[-" in l) and DATE.search(l):
                print("      ", l.strip()[:600])
    f = folder(r["law"])
    if f:
        hits = [l for l in git("grep", "-h", "-i", "-E", VIG.pattern.replace("(?i)", ""), PIN, "--", f + "/").splitlines()]
        print("    act:", f, "|", " / ".join(h[:400] for h in hits[:4]) or "(not in this repository or no clause found)")
