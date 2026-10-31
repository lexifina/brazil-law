"""Rebuild one of the older Brazil parts with batch 7's stale-wording rules (stale_fix.py) and the published source
texts (published_text.json: the source notes and ai_use as published, without fetch details).

    python -X utf8 scripts/brazil-law/batch7/oldparts.py <part> [--out FILE] [--nofix]
    parts: 60-phase2 (CP, CPC), 70-clt, 80-proc (CPP, CDC), 90-batch3 (CTN, ECA, Código Eleitoral), 95-rju

The part's own parser does the replay; this wraps its build_act to apply the rules to the final life spans, then
writes the part with its decisions extended. No network.
"""
from __future__ import annotations

import importlib.util
import io
import contextlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
F = HERE.parent
sys.path.insert(0, str(HERE))
import stale_fix  # noqa: E402

SCRIPTS = {"60-phase2": "parse_phase2.py", "70-clt": "clt/parse_clt.py", "80-proc": "proc/parse_proc.py",
           "90-batch3": "batch3/parse_batch3.py", "95-rju": "rju/parse_rju.py"}


def load(script: str):
    sys.path.insert(0, str(F)); sys.path.insert(0, str((F / script).parent))
    spec = importlib.util.spec_from_file_location("part_" + Path(script).stem, F / script)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main(argv: list[str]) -> int:
    part = argv[0]
    out = Path(argv[argv.index("--out") + 1]) if "--out" in argv else F / "corpus.d" / f"{part}.json"
    m = load(SCRIPTS[part])
    core = getattr(m, "P", m) if part in ("90-batch3", "95-rju") else m
    tmp_out = HERE / ".tmp" / f"oldparts-{part}.json"
    if part == "90-batch3":
        core.OUT = tmp_out
    else:
        m.OUT = tmp_out
    same_day = set(getattr(core, "SAME_DAY_LAWS", set()))
    if "--nofix" not in argv:
        _build = core.build_act
        cur = {"act": None}
        acts = core.ACTS

        def build_act(paras, act_day, *a, **k):
            slug = next((x["slug"] for x in acts if x.get("_day") == act_day), None) or cur["act"]
            stale_fix.fix(core, paras, slug or "?", same_day)
            return _build(paras, act_day, *a, **k)
        core.build_act = build_act
        if part == "95-rju" or part == "90-batch3":
            m.B = getattr(m, "B", None)
        _paragraphs = core.paragraphs

        def paragraphs(html, digits):
            res = _paragraphs(html, digits)
            return res
        # the act slug for the decisions: read from the order build_act is called in (ACTS order)
        order = iter([x["slug"] for x in acts])

        def build_act2(paras, act_day, *a, **k):
            stale_fix.fix(core, paras, next(order, "?"), same_day)
            return _build(paras, act_day, *a, **k)
        core.build_act = build_act2
    with contextlib.redirect_stdout(io.StringIO()) as buf:
        rc = core.main([]) if part not in ("90-batch3",) else m.main([])
    sys.stdout.write("\n".join(l for l in buf.getvalue().splitlines() if "problem" in l.lower() or "DIFF" in l) + "\n")
    produced = Path(getattr(m, "OUT", tmp_out)) if part != "90-batch3" else tmp_out
    d = json.loads(produced.read_text(encoding="utf-8"))
    pub = json.loads((HERE / "published_text.json").read_text(encoding="utf-8"))[part]
    for s, ps in zip(d["sources"], pub["sources"]):
        s.update(ps)
    d["ai_use"] = pub["ai_use"]
    if "--nofix" not in argv:
        d["decisions"] += stale_fix.decisions()
    t = out.with_suffix(".json.tmp")
    t.write_text(json.dumps(d, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    os.replace(t, out)
    print("wrote", out, "rules used:", {k: len(v) for k, v in stale_fix.USED.items()})
    return rc or 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
