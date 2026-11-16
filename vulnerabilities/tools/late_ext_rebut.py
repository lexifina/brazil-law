"""The rebuttal step for empty periods, as triage.py does it for the other categories: for each flag the late-extension
review called a real gap, a second call gives the strongest argument that it is not, and says whether the gap survives.

    (source llm_env.sh)  python -X utf8 late_ext_rebut.py
Reads and rewrites gl/vulnerabilities/scripts/findings/run/late_extension_triage.jsonl (adds "rebut" to each candidate_gap).
"""
import json, os, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join(HERE, "gl", "vulnerabilities", "scripts")
sys.path.insert(0, os.path.join(SCR, "ingest"))
sys.path.insert(0, os.path.join(SCR, "triage"))
from llm import call  # noqa: E402
import triage as T  # noqa: E402

PATH = os.path.join(SCR, "findings", "run", "late_extension_triage.jsonl")
recs = [json.loads(l) for l in open(PATH, encoding="utf-8")]


def work(rec):
    if rec["j"]["verdict"] != "candidate_gap" or rec.get("rebut"):
        return rec
    r = rec["row"]
    ev = (f"Corpus: {r['corpus']}. File: {r['path']}.\nA time-limited rule ran 'until {r['old_until']}'. The record shows it "
          f"extended to '{r['new_until']}' by {r['law']}, which took effect on {r['extended_in_force']}, {r['gap_days']} days "
          f"after the old end date.\n\nTEXT BEFORE (around the old date):\n{r['old_context']}\n\nTEXT AFTER (around the new date):\n"
          f"{r['new_context']}")
    rb = call(f"Another analyst claims the rule lapsed and a real gap opened before the extension. Give the strongest argument "
              f"that it did NOT (for example: the date bounds which cases or events are covered, not when the rule applies; the "
              f"extension is a new, deliberate measure; the amending act applies retroactively; the two dates are in unrelated "
              f"sentences), and rate how likely that argument wins.\n\nEVIDENCE\n{ev}\n\nCLAIM\n{json.dumps(rec['j'], ensure_ascii=False)}",
              system=T.SYSTEM, schema=T.REBUT, provider="azure")
    rec["rebut"] = rb["json"]
    return rec


with ThreadPoolExecutor(12) as ex:
    recs = list(ex.map(work, recs))
with open(PATH, "w", encoding="utf-8", newline="\n") as f:
    for rec in recs:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
cand = [r for r in recs if r["j"]["verdict"] == "candidate_gap"]
print(len(recs), "reviewed;", len(cand), "candidate gaps;", sum(1 for r in cand if r["rebut"]["survives"]), "survive the rebuttal")
