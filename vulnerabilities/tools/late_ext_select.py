"""Chooses the 40 empty-period flags for global-law's late_ext_triage.py: the flags whose old and new date sit in the same
sentence (the first 60 characters of their contexts match), then the shortest gaps.

    python -X utf8 late_ext_select.py      -> gl/vulnerabilities/scripts/findings/run/late_extension_filtered.json
"""
import json, os

RUN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gl", "vulnerabilities", "scripts", "findings", "run")
rows = [json.loads(l) for l in open(os.path.join(RUN, "late_extension.jsonl"), encoding="utf-8")]
same = [r for r in rows if r["old_context"][:60] == r["new_context"][:60]]
rest = sorted((r for r in rows if r not in same), key=lambda r: int(r["gap_days"]))
sel = same + rest[:max(0, 40 - len(same))]
json.dump(sel, open(os.path.join(RUN, "late_extension_filtered.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(len(sel), "chosen:", len(same), "with both dates in one sentence")
