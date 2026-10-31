"""Stale wordings: two wordings of one dispositivo alive at once in a replay of Planalto's annotated page. Applied to the
final life spans of an act's lines, just before its versions are built (a wrapper of the parser's build_act).

Rules (each use is listed in the part's decisions):

A. A wording ends no later than the next wording of the same dispositivo. parse_proc and its copies end a struck line
   by its own 'Revogado' note first and look for the next wording only when there is none, so the original Parágrafo
   único of CP art. 216 (revoked in 2009) stood beside the wording Lei 11.106/2005 gave it. Also a law in force on the
   act's own first day (SAME_DAY_LAWS: Lei 13.256/2016 for the CPC) replaces the wording it rewrote that same day, even
   where a later wording was taken as its successor. The unlabelled lines printed right under the ended line ('Pena -
   ...') that started and ended with it end with it.

B. An unnoted wording printed below a struck wording of the same dispositivo with the same start (Planalto struck the
   old text and printed the new one without a note: CP art. 273 § 2º, rewritten by Lei 9.677/1998) starts when the
   struck one ended, credited to the law that ended it.

C. Two copies of one line, alive at once, word for word the same apart from typesetting (Planalto printing the same
   dispositivo twice, struck and unstruck, or twice unstruck): the later-printed copy starts when the earlier one ends;
   if neither ends, the struck copy is left out.
"""
from __future__ import annotations

import re

USED: dict[str, list[str]] = {"A": [], "B": [], "C": []}


def _norm_label(s: str) -> str:
    return re.sub(r"[\s.\-:]", "", s or "").replace("°", "º").replace("o", "º")


def _norm_text(s: str) -> str:
    s = s.replace("°", "º")
    s = re.sub(r"^((?:Art\.|§)\s*[\d.]+\s*(?:º|o)?(?:-[A-Z])?|Parágrafo único)\s*[.\-:–]?\s*", lambda m: _norm_label(m.group(1)) + " ", s)
    return re.sub(r"[^0-9a-zà-ÿ]", "", s.lower())


def fix(M, paras: list[dict], act: str, same_day_laws: set[str]) -> None:
    level = M.level
    # A
    for i, p in enumerate(paras):
        if p["heading"] or not p["label"] or p.get("skip") or not p["end"]:
            continue
        lv = level(p["label"])
        for q in paras[i + 1:]:
            if q["heading"]:
                continue
            if q["unit"] != p["unit"] or level(q["label"]) < min(lv, 2) or (lv < 5 and level(q["label"]) < lv):
                break
            if q.get("skip") or _norm_label(q["label"]) != _norm_label(p["label"]):
                continue
            later = q["start"] > p["start"]
            same = (q["start"] == p["start"] and q["start_law"] in same_day_laws and p["start_law"] not in same_day_laws)
            if (later or same) and q["start"] < p["end"]:
                old_end, old_law = p["end"], p["end_law"]
                p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "next-wording-first"
                USED["A"].append(f"{act} {p['unit']} [{p['label']}] {old_end} -> {q['start']}")
                for r in paras[i + 1:]:
                    if r["unit"] != p["unit"] or r["label"] or r["heading"]:
                        break
                    if r["start"] == p["start"] and r["end"] == old_end and r["end_law"] == old_law:
                        r["end"], r["end_law"], r["end_how"] = p["end"], p["end_law"], "next-wording-first"
                break
            if later:
                break
    # B
    for i, p in enumerate(paras):
        if p["state"] != "plain" or p["start_law"] or p.get("skip") or p["heading"]:
            continue
        for q in reversed(paras[:i]):
            if q["unit"] != p["unit"]:
                break
            if q["heading"] or q.get("skip") or q["state"] == "plain" or q["start"] != p["start"] or not q["end"]:
                continue
            if p["label"] and _norm_label(q["label"]) == _norm_label(p["label"]) or (
                    not p["label"] and not q["label"] and _norm_text(q["text"]) == _norm_text(p["text"])):
                if q["end"] > p["start"] and (p["end"] is None or q["end"] < p["end"]):
                    p["start"], p["start_law"] = q["end"], q["end_law"]
                    USED["B"].append(f"{act} {p['unit']} [{p['label'] or p['text'][:30]}] from {q['end']}")
                break
    # C
    def alive_span(p):
        return (p["start"], p["end"] or "9999-12-31")
    by_unit: dict[str, list[dict]] = {}
    for p in paras:
        if not p["heading"] and not p.get("skip"):
            by_unit.setdefault(p["unit"], []).append(p)
    for unit, ps in by_unit.items():
        for a_i, a in enumerate(ps):
            for b in ps[a_i + 1:]:
                if a.get("skip") or b.get("skip") or _norm_text(a["text"]) != _norm_text(b["text"]) or not a["text"]:
                    continue
                (s1, e1), (s2, e2) = alive_span(a), alive_span(b)
                if not (s1 < e2 and s2 < e1):
                    continue
                if a["end"] and a["end"] > b["start"] and (b["end"] is None or a["end"] < b["end"]):
                    b["start"], b["start_law"] = a["end"], a["end_law"]
                    USED["C"].append(f"{act} {unit} [{b['label'] or b['text'][:30]}] second copy from {a['end']}")
                elif b["end"] and b["end"] > a["start"] and (a["end"] is None or b["end"] < a["end"]) and b["start"] <= a["start"]:
                    a["start"], a["start_law"] = b["end"], b["end_law"]
                    USED["C"].append(f"{act} {unit} [{a['label'] or a['text'][:30]}] second copy from {b['end']}")
                else:
                    drop = a if a["state"] != "plain" else b
                    drop["skip"], drop["end_how"] = True, "copy"
                    USED["C"].append(f"{act} {unit} [{drop['label'] or drop['text'][:30]}] {drop['state']} copy left out")


def decisions() -> list[str]:
    out = []
    if USED["A"]:
        out.append("A wording ends no later than the next wording of the same dispositivo (also a wording a law in force on "
                   "the act's first day rewrote that day), even where the source also notes a later revocation; the "
                   "unlabelled lines right under it end with it: " + "; ".join(dict.fromkeys(USED["A"])) + ".")
    if USED["B"]:
        out.append("An unnoted wording printed below a struck wording of the same dispositivo with the same start is the "
                   "new wording: it starts when the struck one ended, credited to that law: "
                   + "; ".join(dict.fromkeys(USED["B"])) + ".")
    if USED["C"]:
        out.append("A line Planalto prints twice, word for word the same: the later copy starts when the earlier ends, or, "
                   "when neither ends, the struck copy is left out: " + "; ".join(dict.fromkeys(USED["C"])) + ".")
    return out
