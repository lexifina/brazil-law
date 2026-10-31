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
   it, where an older wording under the same label is printed struck in the article (CLT art. 678's alíneas under the
   incisos Lei 5.442/1968 added; ECA art. 4 a)-d) under the § 1º of Lei 15.240/2025, printed struck under the old
   Parágrafo único too).

C. Two copies of one labelled line, alive at once, word for word the same apart from typesetting (Planalto printing the same
   dispositivo twice, struck and unstruck, or twice unstruck): the later-printed copy starts when the earlier one ends;
   if neither ends, the struck copy is left out.
"""
from __future__ import annotations

import re

USED: dict[str, list[str]] = {"A": [], "B": [], "C": [], "D": [], "E": [], "L": [], "G": []}


def _norm_label(s: str) -> str:
    return re.sub(r"[\s.\-:]", "", s or "").replace("°", "º").replace("o", "º")


def _norm_text(s: str) -> str:
    s = s.replace("°", "º")
    s = re.sub(r"^((?:Art\.|§)\s*[\d.]+\s*(?:º|o)?(?:-[A-Z])?|Parágrafo único)\s*[.\-:–]?\s*", lambda m: _norm_label(m.group(1)) + " ", s)
    return re.sub(r"[^0-9a-zà-ÿ]", "", s.lower())


def fix(M, paras: list[dict], act: str, same_day_laws: set[str], rule_c: bool = False) -> None:
    level = M.level
    parent: dict[int, str] = {}
    for i, p in enumerate(paras):
        lab = "" if p["heading"] or not p["label"] or p["label"] == "rubrica" else p["label"]
        par = ""
        if lab:
            lv0 = level(lab)
            for q in reversed(paras[:i]):
                if q["unit"] != p["unit"]:
                    break
                if q["heading"] or not q["label"] or q["label"] == "rubrica":
                    continue
                if level(q["label"]) < lv0:
                    par = _norm_label(q["label"])
                    break
        parent[id(p)] = par
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
            same = q["start"] == p["start"] and q["start_law"] and (
                (q["start_law"] in same_day_laws and p["start_law"] not in same_day_laws)
                or (p["start_law"] is None and p["state"] != "plain" and not same_day_laws))
            if (later or same) and q["start"] < p["end"]:
                old_end, old_law = p["end"], p["end_law"]
                p["end"], p["end_law"], p["end_how"] = q["start"], q["start_law"], "next-wording-first"
                USED["A"].append(f"{act} {p['unit']} [{p['label']}] {old_end} -> {q['start']}")
                for r in paras[i + 1:]:
                    if r["heading"]:
                        continue
                    if r["unit"] != p["unit"] or (r["label"] and r["label"] != "rubrica" and level(r["label"]) <= lv):
                        break
                    if r["start"] >= p["start"] and r["end"] == old_end and r["end_law"] == old_law:
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
                # ... and only where an older wording under p's label is printed struck in the same article (so p is
                # not simply an old line kept under a renumbered parent: ECA art. 91 a)-d) under the § 1º that was its
                # Parágrafo único)
                older = any(r["unit"] == p["unit"] and r["state"] != "plain" and r is not p and r["start"] < q["start"]
                            and _norm_label(r["label"]) == _norm_label(p["label"]) for r in paras)
                if inserted and older and q["start"] > p["start"]:
                    p["start"], p["start_law"] = q["start"], q["start_law"]
                    USED["D"].append(f"{act} {p['unit']} [{p['label'] or p['text'][:30]}] from {q['start']}")
                break
    # G: an unstruck wording printed above a struck MP wording of the same dispositivo that came in later and ended by
    # the MP's conversion or lapse (the wording is back): it has a gap for the MP's time (RJU art. 68, MP 568/2012)
    for i, p in enumerate(paras):
        if p["state"] != "plain" or p["end"] or p.get("gaps") or p.get("skip") or p["heading"] or not p["label"]:
            continue
        for q in paras[i + 1:]:
            if q["unit"] != p["unit"]:
                break
            if (q["state"] != "plain" and not q.get("skip") and _norm_label(q["label"]) == _norm_label(p["label"])
                    and parent[id(q)] == parent[id(p)]
                    and q["start"] > p["start"] and q["end"] and (q["end_how"] or "") in ("conversion", "lapse", "mp-dropped")
                    and (q["start_law"] or "").startswith("mp-")):
                p["gaps"] = [(q["start"], q["end"], q["start_law"], q["end_law"])]
                USED["G"].append(f"{act} {p['unit']} [{p['label']}] {q['start']}..{q['end']}")
                break
    # (Not done: dating an unnoted struck line by the struck caput printed above it. Planalto prints an article's
    # unchanged paragraphs once, below its latest superseded caput: CP art. 180 §§ 1º-3º of 1940 under the 1955 caput.)
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
            if (q["heading"] or q.get("skip") or q["state"] == "plain" or q["start"] != p["start"] or not q["end"]) and not (
                    q["state"] != "plain" and not q["end"] and not q.get("skip") and not q["heading"] and p["state"] != "plain"
                    and p["end"] and q["start"] == p["start"] and p["label"] and _norm_label(q["label"]) == _norm_label(p["label"])
                    and parent[id(q)] == parent[id(p)]
                    and _norm_text(q["text"]) == _norm_text(p["text"])):
                continue
            if not q["end"]:
                # two struck copies of one wording, the upper with no end of its own: the noted lower copy stands for it
                q["skip"], q["end_how"] = True, "twin"
                USED["B"].append(f"{act} {q['unit']} [{q['label']}] unended copy left out (the copy below has the note)")
                break
            same_label = p["label"] and _norm_label(q["label"]) == _norm_label(p["label"]) and parent[id(q)] == parent[id(p)]
            same_text = _norm_text(q["text"]) == _norm_text(p["text"])
            twin = (same_label and (same_text or not p["start_law"])) or (
                not p["label"] and not q["label"] and same_text and not p["text"].startswith("Pena"))
            if not twin:
                continue
            if same_text and p["state"] != "plain" and p["end"] == q["end"]:
                q["skip"], q["end_how"] = True, "twin"   # the same struck wording printed twice, same life span
                USED["B"].append(f"{act} {q['unit']} [{q['label']}] repeated copy left out")
                break
            if p["end"] is not None and p["end"] <= q["end"]:
                break
            # the first day from q's end on when no other wording of this dispositivo stands
            day, law = q["end"], q["end_law"]
            for _ in range(20):
                blk = [r for r in paras if r is not p and r is not q and r["unit"] == p["unit"] and not r["heading"]
                       and (r["label"] and _norm_label(r["label"]) == _norm_label(p["label"])) and alive_at(r, day)
                       and r["start"] >= day and parent[id(r)] == parent[id(p)]]   # a wording that came in at or after that day (not a sibling list's own item)
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
                   "lines under it (its incisos, alíneas, penalties) that ended with it end with it: " + "; ".join(dict.fromkeys(USED["A"])) + ".")
    if USED["L"]:
        out.append("A caput printed 'Artigo N - ...' is read as that article's caput: " + "; ".join(dict.fromkeys(USED["L"])) + ".")
    if USED["G"]:
        out.append("An unstruck wording printed above a struck Medida Provisória wording of the same dispositivo that came "
                   "in later and ended with the MP's conversion or lapse gives way to it for that time: "
                   + "; ".join(dict.fromkeys(USED["G"])) + ".")
    if USED["D"]:
        out.append("A line with no note of its own, printed unstruck under an unstruck line a later law inserted "
                   "('Incluído'), starts with it where an older wording under the same label is printed struck in the "
                   "article: "
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
