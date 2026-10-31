"""Stale wordings: two wordings of one dispositivo alive at once in a replay of Planalto's annotated page. Applied to the
final life spans of an act's lines, just before its versions are built (a wrapper of the parser's build_act).

Rules (each use is listed in the part's decisions):

A. A wording ends no later than the next wording of the same dispositivo. parse_proc and its copies end a struck line
   by its own 'Revogado' note first and look for the next wording only when there is none, so the original Parágrafo
   único of CP art. 216 (revoked in 2009) stood beside the wording Lei 11.106/2005 gave it. Also a law in force on the
   act's own first day (SAME_DAY_LAWS: Lei 13.256/2016 for the CPC) replaces the wording it rewrote that same day, even
   where a later wording was taken as its successor. The unlabelled lines printed right under the ended line ('Pena -
   ...') that started and ended with it end with it.

B. Twin wordings: a line printed below a struck line of the same dispositivo with the same start, word for word the
   same (Planalto printing a wording again where it came back: CLT art. 582 § 1º after MP 873/2019 lapsed) or, when
   the lower one has no note, a new wording (CP art. 273 § 2º, rewritten by Lei 9.677/1998). The lower line starts on
   the first day from the struck line's end on when no other wording of the dispositivo stands (or with the restored
   caput of its article); a struck lower copy that never stands alone is left out.

D. A line with no note of its own printed unstruck under an unstruck line a later law inserted ('Incluído') starts with
   it (CLT art. 678's alíneas under the incisos Lei 5.442/1968 added).

C. Two copies of one labelled line, alive at once, word for word the same apart from typesetting (Planalto printing the same
   dispositivo twice, struck and unstruck, or twice unstruck): the later-printed copy starts when the earlier one ends;
   if neither ends, the struck copy is left out.
"""
from __future__ import annotations

import re

USED: dict[str, list[str]] = {"A": [], "B": [], "C": [], "D": [], "E": [], "L": []}


def _norm_label(s: str) -> str:
    return re.sub(r"[\s.\-:]", "", s or "").replace("°", "º").replace("o", "º")


def _norm_text(s: str) -> str:
    s = s.replace("°", "º")
    s = re.sub(r"^((?:Art\.|§)\s*[\d.]+\s*(?:º|o)?(?:-[A-Z])?|Parágrafo único)\s*[.\-:–]?\s*", lambda m: _norm_label(m.group(1)) + " ", s)
    return re.sub(r"[^0-9a-zà-ÿ]", "", s.lower())


def fix(M, paras: list[dict], act: str, same_day_laws: set[str], rule_c: bool = False) -> None:
    level = M.level
    # a caput printed 'Artigo 896 - ...' (CLT, Lei 861/1949) has no label: it is that article's caput
    for p in paras:
        m = re.match(r"^Artigo\s+([\d.]+)", p["text"])
        if m and not p["label"] and not p["heading"] and p["unit"].startswith("art-"):
            p["label"] = f"Art. {m.group(1)}"
            USED["L"].append(f"{act} {p['unit']} '{p['text'][:12]}'")
    # A
    for i, p in enumerate(paras):
        if p["heading"] or not p["label"] or p.get("skip") or not p["end"] or p.get("gaps") or p.get("pinned"):
            continue   # lines with gaps or pinned by an MP-pair model (CLT, MP 905/955) keep their modelled spans
        lv = level(p["label"])
        for q in paras[i + 1:]:
            if q["heading"]:
                continue
            if q["unit"] != p["unit"] or level(q["label"]) < min(lv, 2) or (lv < 5 and level(q["label"]) < lv):
                break
            if q.get("skip") or q.get("pinned") or _norm_label(q["label"]) != _norm_label(p["label"]):
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
    # D: an unnoted unstruck line is no older than the inserted unstruck line it hangs from (its nearest parent above)
    for i, p in enumerate(paras):
        if p["state"] != "plain" or p["start_law"] or p.get("skip") or p["heading"] or not p["label"] or p["label"] == "rubrica":
            continue   # unlabelled lines (penalties, marginal headings) are not placed by their position
        lv = level(p["label"])
        for q in reversed(paras[:i]):
            if q["unit"] != p["unit"]:
                break
            if q["heading"] or q.get("skip") or q["state"] != "plain" or not q["label"]:
                continue
            if level(q["label"]) < lv:
                inserted = any(re.search(r"Inclu[íi]d|Acrescid|Acrescentad", n, re.I) for n in q["notes"])
                if inserted and q["start"] > p["start"]:
                    p["start"], p["start_law"] = q["start"], q["start_law"]
                    USED["D"].append(f"{act} {p['unit']} [{p['label'] or p['text'][:30]}] from {q['start']}")
                break
    # E: an unnoted struck line inside a struck block whose caput or paragraph above it came in later belongs to that
    # block (Planalto prints each superseded wording of an article whole, the notes on its first lines)
    for i, p in enumerate(paras):
        if p["state"] == "plain" or p["start_law"] or p.get("skip") or p["heading"] or not p["label"] or p["label"] == "rubrica":
            continue
        lv = level(p["label"])
        for q in reversed(paras[:i]):
            if q["unit"] != p["unit"]:
                break
            if q["heading"] or q.get("skip") or not q["label"] or q["label"] == "rubrica":
                continue
            if level(q["label"]) < lv:
                if q["state"] != "plain" and q["start_law"] and q["start"] > p["start"] and (not p["end"] or q["start"] <= p["end"]):
                    p["start"], p["start_law"] = q["start"], q["start_law"]
                    if p["end"] and p["end"] < p["start"]:
                        p["end"] = p["start"]
                    USED["E"].append(f"{act} {p['unit']} [{p['label']}] from {q['start']}")
                break
    # B: twin wordings (same dispositivo, same start) printed one below the other
    def alive_at(r, d):
        return not r.get("skip") and r["start"] <= d and (r["end"] is None or d < r["end"]) and not any(
            a <= d < b for a, b, *_ in (r.get("gaps") or []))
    for i, p in enumerate(paras):
        if p["heading"] or p.get("skip") or not (p["label"] or p["state"] == "plain"):
            continue
        for q in reversed(paras[:i]):
            if q["unit"] != p["unit"]:
                break
            if q["heading"] or q.get("skip") or q["state"] == "plain" or q["start"] != p["start"] or not q["end"]:
                continue
            same_label = p["label"] and _norm_label(q["label"]) == _norm_label(p["label"])
            same_text = _norm_text(q["text"]) == _norm_text(p["text"])
            twin = (same_label and (same_text or (p["state"] == "plain" and not p["start_law"]))) or (
                not p["label"] and not q["label"] and same_text and not p["text"].startswith("Pena"))
            if not twin:
                continue
            if p["end"] is not None and p["end"] <= q["end"]:
                break
            # the first day from q's end on when no other wording of this dispositivo stands
            day, law = q["end"], q["end_law"]
            for _ in range(20):
                blk = [r for r in paras if r is not p and r is not q and r["unit"] == p["unit"] and not r["heading"]
                       and (r["label"] and _norm_label(r["label"]) == _norm_label(p["label"])) and alive_at(r, day)
                       and r["start"] >= day]   # a wording that came in at or after that day (not a sibling list's own item)
                if not blk or not p["label"]:
                    break
                r = max(blk, key=lambda r: r["end"] or "9999")
                if r["end"] is None:
                    day = None
                    break
                day, law = r["end"], r["end_law"]
            if day and p["state"] == "plain":
                back = [r for r in paras if r["unit"] == p["unit"] and r["state"] == "plain" and r is not p
                        and (r["start_law"] or "").endswith("-fim") and r["start"] > day]
                if back and all(r["start"] == back[0]["start"] for r in back):
                    day, law = back[0]["start"], back[0]["start_law"]
            if day is None or (p["end"] is not None and day >= p["end"]):
                p["skip"], p["end_how"] = True, "twin"
                USED["B"].append(f"{act} {p['unit']} [{p['label'] or p['text'][:30]}] second copy left out")
            else:
                p["start"], p["start_law"] = day, law
                USED["B"].append(f"{act} {p['unit']} [{p['label'] or p['text'][:30]}] from {day}")
            break
    # C (off unless asked: identical lines under different parents are legitimate, CPC art. 932 IV/V a) and b))
    if not rule_c:
        return

    def alive_span(p):
        return (p["start"], p["end"] or "9999-12-31")
    by_unit: dict[str, list[dict]] = {}
    for p in paras:
        if not p["heading"] and not p.get("skip"):
            by_unit.setdefault(p["unit"], []).append(p)
    for unit, ps in by_unit.items():
        for a_i, a in enumerate(ps):
            for b in ps[a_i + 1:]:
                if (a.get("skip") or b.get("skip") or not a["label"] or _norm_label(a["label"]) != _norm_label(b["label"])
                        or _norm_text(a["text"]) != _norm_text(b["text"])):
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
    if USED["L"]:
        out.append("A caput printed 'Artigo N - ...' is read as that article's caput: " + "; ".join(dict.fromkeys(USED["L"])) + ".")
    if USED["E"]:
        out.append("An unnoted struck line inside a struck wording of an article whose caput or paragraph above it came in "
                   "later belongs to that wording (Planalto prints each superseded wording whole, with the notes on its "
                   "first lines) and starts with it: " + "; ".join(dict.fromkeys(USED["E"])) + ".")
    if USED["D"]:
        out.append("A line with no note of its own, printed unstruck under an unstruck line a later law inserted "
                   "('Incluído'), starts with it: "
                   + "; ".join(dict.fromkeys(USED["D"])) + ".")
    if USED["B"]:
        out.append("Twin wordings: a line printed below a struck line of the same dispositivo with the same start, word for "
                   "word the same or (with no note of its own) a new wording, starts on the first day from the struck "
                   "line's end on when no other wording of that dispositivo stands, or with the restored caput of its "
                   "article; a struck lower copy that never stands alone is left out: "
                   + "; ".join(dict.fromkeys(USED["B"])) + ".")
    if USED["C"]:
        out.append("A line Planalto prints twice, word for word the same: the later copy starts when the earlier ends, or, "
                   "when neither ends, the struck copy is left out: " + "; ".join(dict.fromkeys(USED["C"])) + ".")
    return out
