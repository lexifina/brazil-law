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

# Units where two wordings of one dispositivo still stand at once for a time, because Planalto's page prints a rewritten
# block with no note (or with a note naming no day) and nothing on the page dates it; checked by hand 2026-10-31.
OPEN = {
    "70-clt": "Open (not dated by the source): in arts. 654, 693, 896 and 902 Planalto prints a superseded "
              "wording of the 1940s-1950s without a note (or a note that names no day), so for some years of that time "
              "two wordings of one paragraph stand at once in this history; in art. 538, from 21.1.1946 to 23.2.1946, "
              "the 1943 § 3º (on the conselho dos representantes), which the page prints with no note, stands beside "
              "the § 2º Decreto-Lei 8.740 wrote on the same subject; in arts. 634 and 636 the same happens for a few "
              "days around MP 905/2019 and MP 955/2020 (arts. 530, 553 and 628-A: see the doubled-lines decision). "
              "The text in force today is not affected.",
}
# Life spans set by hand after the stale-wording rules, where Planalto's page prints a wording that the rules cannot place
# (reviewed one by one from the duplicate-line check, batch10/.tmp/dupline.py, 2026-10-31): part -> [(act, unit, label,
# line start, n-th such line, fields, why)]
_W8740 = ("Decreto-Lei 8.740/1946 (19.1.1946) rewrote these articles and Decreto-Lei 8.987-A/1946 suspended it, restoring the "
          "1943 wording; Planalto prints the 1943 wording, the 1946 block and the 1943 wording again")
_W592 = ("CLT art. 592: Planalto prints the 1943 article (caput, I to IV with their alíneas, parágrafo único), the lines "
         "later decree-laws changed, a second copy of item I with its alíneas, and the items II to IV as Decreto-Lei "
         "925/1969 rewrote them")
_WT7 = ("CLT Título VII headings: Medida Provisória 905/2019 renamed the Título ('DAS PENALIDADES E DO PROCESSO "
        "ADMINISTRATIVO') and gave its Capítulo I name again; Medida Provisória 955/2020 revoked it from 20.4.2020 and "
        "lapsed on 18.8.2020, so Medida Provisória 905's names stand again on 18.8.2020, the last day before it lapsed, "
        "as arts. 553 and 628-A read that day; the 1943 names stand before 12.11.2019, from 20.4.2020 and from 19.8.2020")
_T7 = (("h109-0", "TÍTULO VII"), ("h109-1", "DO PROCESSO DE MULTAS ADMINISTRATIVAS"), ("h109-2", "CAPÍTULO I"),
       ("h109-3", "DA FISCALIZAÇÃO, DA AUTUAÇÃO"))
_W13964 = ("Código Penal art. 121 § 2º VIII: vetoed on 24.12.2019 and promulgated after Congress overrode the veto (DOU "
           "30.4.2021; the Lei 13.964 page prints the inciso struck as '(VETADO)' and again as promulgated, 'Promulgação "
           "partes vetadas'); the part's rule for such wording applies: '(VETADO)' from Lei 13.964's day, 23.1.2020, the "
           "promulgated wording from 30.4.2021 (the '(VETADO)' line had been read as text of 1942 and the wording as in "
           "force from 23.1.2020)")
OLD_FIX: dict[str, list[tuple[str, str, str, str, int, dict, str]]] = {
    "70-clt": [
        ("clt", "art-379", lab, start, 0, {"start": "1984-06-05", "start_law": "lei-7189-1984"},
         "CLT art. 379 §§ 1º and 8º: their incisos ('I - à mulher que ocupe posto de direção ...', 'II - à mulher empregada "
         "em serviços de higiene ...', 'I - por decreto do Poder Executivo ...', 'II - por portaria do Ministro do Trabalho "
         "...') are printed without a note under the paragraphs Lei 7.189/1984 wrote; they are that law's wording, in force "
         "from 5.6.1984 (they had been read as text of 1943)")
        for lab, start in (("I -", "I - à mulher que ocupe posto de direção"),
                           ("II -", "II - à mulher empregada em serviços de higiene"),
                           ("I -", "I - por decreto do Poder Executivo"), ("II -", "II - por portaria do Ministro do Trabalho"))
    ] + [
        ("clt", "art-558", "§ 1º", "§ 1º O registo a que se refere o presente artigo", 0,
         {"end": "1946-01-21", "end_law": "dl-8740-1946", "end_how": "successor"},
         "CLT art. 558 § 1º: the 1943 wording ends on 21.1.1946, when the article's caput and the copy Planalto prints after "
         "the 1946 block take over (" + _W8740 + "); both copies had stood until 1969"),
        ("clt", "art-525", "a)", "a) os delegados do Ministério do Trabalho", 0,
         {"end": "1946-01-21", "end_law": "dl-8740-1946", "end_how": "successor"},
         "CLT art. 525 a): the 1943 wording ends with Decreto-Lei 8.740/1946's (21.1.1946); the restored copy follows from "
         "23.2.1946 (" + _W8740 + "); both copies had stood until 27.7.1946"),
        ("clt", "art-606", "§ 1º", "§ 1º - A Comissão Nacional de Sindicalização", 0, {"skip": True, "end_how": "twin"},
         "CLT art. 606 § 1º: Decreto-Lei 8.740/1946's wording is printed twice (once with a dash after the label); the second "
         "copy is left out"),
        *[("clt", "art-592", lab, start, 1, {"skip": True, "end_how": "twin"},
           _W592 + "; the second copy of item I and its alíneas, the same words as the first, is left out")
          for lab, start in (("", "I. De empregadores e de agentes autônomos:"),
                             ("a)", "a) em serviços de assistência técnica e judiciária;"),
                             ("b)", "b) na realização de estudos econômicos e financeiros;"), ("c)", "c) em bibliotecas;"),
                             ("d)", "d) em medidas de divulgação comercial"),
                             ("e)", "e) nas despesas decorrentes dos encargos criados pelo presente capítulo"))],
        ("clt", "art-592", "a)", "a) em serviços de assistência técnica e judiciária;", 0,
         {"end": "1976-12-10", "end_law": "lei-6386-1976", "end_how": "parent"},
         _W592 + "; item I's alínea a) stands until Lei 6.386/1976 rewrote the article, like the rest of item I (it had "
                 "been ended in 1946 by Decreto-Lei 8.740's new alínea a) of item II)"),
        *[("clt", "art-592", lab, start, 0,
           {"skip": False, "end": "1969-10-13", "end_law": "dl-925-1969", "end_how": "successor"},
           _W592 + "; alíneas of the 1943 items II to IV whose words Decreto-Lei 925/1969 repeated (II d), II j), III a), "
                   "IV a)) stand from 1943 until then (the twin-wording rule had left them out of the 1943 text)")
          for lab, start in (("d)", "d) em assistência judiciária;"),
                             ("j)", "j) nas despesas decorrentes dos encargos criados pelo presente capítulo"),
                             ("a)", "a) em bibliotecas especializadas;"), ("a)", "a) na assistência à maternidade;"))],
        ("clt", "art-592", "a)", "a) em agências de colocação, na forma das instruções que forem expedidas pelo ministro", 0,
         {"skip": False, "start": "1943-11-10", "start_law": None, "end": "1946-01-21", "end_law": "dl-8740-1946",
          "end_how": "successor"},
         _W592 + "; item II alínea a) as enacted stands until Decreto-Lei 8.740/1946's wording (" + _W8740 + ")"),
        ("clt", "art-515", "Parágrafo único", "Parágrafo único - O Ministro do Trabalho poderá", 0,
         {"skip": True, "end_how": "twin"},
         "CLT art. 515 parágrafo único: inside the Decreto-Lei 8.740/1946 block Planalto prints the 1943 paragraph again, "
         "struck as revoked by that decree-law; it is the same wording as the 1943 copy above it, which stands until then, "
         "and is left out"),
        # arts. 534 and 538 (2026-11-01): Decreto-Lei 8.740/1946's paragraphs carry 'Redação dada', so they replaced the
        # 1943 paragraphs of the same number from 21.1.1946; the 1943 wording Planalto prints again after them (struck,
        # no note) is the one Decreto-Lei 8.987-A restored on 23.2.1946: the first copy stands with a gap for those days
        # and keeps its place in the article; the second copy, the same words, is left out
        *[("clt", unit, lab, start, nth, fields,
           f"CLT art. {unit[4:]} {lab}: the 1943 wording gives way on 21.1.1946 to the wording Decreto-Lei 8.740/1946 "
           f"gave the paragraph ('Redação dada') and stands again from 23.2.1946 (" + _W8740 + "); the second copy "
           f"Planalto prints after Decreto-Lei 8.740's wording is left out (both wordings had stood at once from 21.1 "
           f"to 23.2.1946)")
          for unit, lab, start in (("art-534", "§ 1º", "§ 1º As federações serão constituídas por Estados, podendo o Ministro"),
                                   ("art-538", "§ 1º", "§ 1º A diretoria será constituida, no máximo"),
                                   ("art-538", "§ 2º", "§ 2º O presidente da federação ou confederação"))
          for nth, fields in ((0, {"gaps": [("1946-01-21", "1946-02-23", "dl-8740-1946", "dl-8987a-1946")]}),
                              (1, {"skip": True, "end_how": "twin"}))],
        # Título VII headings (2026-11-01), as arts. 553 and 628-A read: Medida Provisória 905/2019's names from 12.11.2019,
        # gone while Medida Provisória 955/2020 stood (20.4 to 18.8.2020), back for 18.8.2020, ended 19.8.2020; the 1943
        # names (printed twice, struck and plain) up to 12.11.2019 and again from 20.4.2020, except on 18.8.2020
        *[("clt", "titulos", lab, start, 0, {"end": "2019-11-12", "end_law": "mp-905-2019", "end_how": "successor", "gaps": []},
           _WT7) for lab, start in _T7],
        *[("clt", "titulos", lab, start, nth,
           {"gaps": [("2020-04-20", "2020-08-18", "mp-955-2020", "mp-955-2020-fim")], "end": "2020-08-19",
            "end_law": "mp-905-2019-fim", "end_how": "mp-pair"}, _WT7)
          for lab, start, nth in (("h109-0", "TÍTULO VII", 1), ("h109-1", "DAS PENALIDADES E DO PROCESSO ADMINISTRATIVO", 0),
                                  ("h109-2", "CAPÍTULO I", 1), ("h109-3", "DA FISCALIZAÇÃO, DA AUTUAÇÃO", 1))],
        *[("clt", "titulos", lab, start, 0, {"skip": True, "end_how": "twin"},
           _WT7 + "; the second copy of Medida Provisória 905's Capítulo I heading is left out")
          for lab, start in (("h109-4", "CAPÍTULO I"), ("h109-5", "DA FISCALIZAÇÃO, DA AUTUAÇÃO"))],
        *[("clt", "titulos", lab, start, nth,
           {"gaps": [("2020-08-18", "2020-08-19", "mp-955-2020-fim", "mp-905-2019-fim")]}, _WT7)
          for lab, start, nth in (("h109-0", "TÍTULO VII", 2), ("h109-1", "DO PROCESSO DE MULTAS ADMINISTRATIVAS", 1),
                                  ("h109-2", "CAPÍTULO I", 2), ("h109-3", "DA FISCALIZAÇÃO, DA AUTUAÇÃO", 2))],
    ],
    "60-phase2": [
        ("codigo-penal", "art-121", "§ 6º", "§ 6º A pena é aumentada de 1/3 (um terço) até a metade se o crime for praticado "
         "por milícia privada", 0, {"start": "2012-09-28", "start_law": "lei-12720-2012"},
         "Código Penal art. 121 § 6º: the annotated page prints it without a note; Lei 12.720/2012 art. 2 added it "
         "('passa a vigorar acrescido do seguinte § 6º', and the compiled page's note 'Incluído pela Lei nº 12.720, de "
         "2012'), so it starts on that law's day, 28.9.2012 (it had been read as text of 1942)"),
        ("codigo-penal", "art-121", "VIII -", "VIII - (VETADO):", 0,
         {"start": "2020-01-23", "start_law": "lei-13964-2019", "end": "2021-04-30", "end_law": "lei-13964-2019",
          "end_how": "promulgation"}, _W13964),
        ("codigo-penal", "art-121", "VIII -", "VIII - com emprego de arma de fogo", 0, {"start": "2021-04-30"}, _W13964),
        ("codigo-penal", "art-121", "", "Pena - reclusão, de doze a trinta anos.", 1,
         {"start": "2020-01-23", "start_law": "lei-13964-2019"},
         "Código Penal art. 121 § 2º: the penalty line Planalto prints again after the last inciso starts with Lei "
         "13.964/2019, which added inciso VIII (it had been read as text of 1942)"),
    ],
}
# the same for a run of printed lines: part -> [(act, unit, first line start, start of the line after the run, fields, why)]
OLD_RANGES: dict[str, list[tuple[str, str, str, str, dict, str]]] = {
    "70-clt": [
        ("clt", "art-592", "II. De empregados:", "Parágrafo único. A aplicação do imposto sindical",
         {"end": "1969-10-13", "end_law": "dl-925-1969", "end_how": "successor"},
         _W592 + "; the 1943 items II to IV and their alíneas end when Decreto-Lei 925/1969 gave those items their new "
                 "wording (13.10.1969; they had stood until 1976 beside it)"),
    ],
}
OLD_FIX_USED: list[str] = []
CARRY = ["Acts of this part", "Text before its law"]
SCRIPTS = {"50-codes": "codes/parse_codes.py", "60-phase2": "parse_phase2.py", "70-clt": "clt/parse_clt.py", "80-proc": "proc/parse_proc.py",
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
    if part == "80-proc":
        # LexML's record of Decreto-Lei 6.109/1943 (Publicação Original 18.12.1943, read on 2026-10-29 for the published
        # part) answered 503 on 2026-10-31; the day it gave is kept here (the Planalto page prints none)
        core.PUBLISHED_FIXED["dl-6109-1943"] = ("1943-12-18", "LexML record 'Publicação Original' 18.12.1943 (the Planalto "
                                                              "page prints no DOU day)")
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
            slug = next(order, "?")
            stale_fix.fix(core, paras, slug, same_day)
            for act, unit, label, start, nth, fields, why in OLD_FIX.get(part, []):
                if act != slug:
                    continue
                hits = [p for p in paras if p["unit"] == unit and p["label"] == label and core.norm(p["text"]).startswith(start)]
                if len(hits) > nth:
                    hits[nth].update(fields)
                    OLD_FIX_USED.append(why)
                else:
                    print("OLD_FIX problem: missed", part, unit, label, start)
            for act, unit, first, after, fields, why in OLD_RANGES.get(part, []):
                if act != slug:
                    continue
                rows = [p for p in paras if p["unit"] == unit]
                i = next((n for n, p in enumerate(rows) if core.norm(p["text"]).startswith(first)), None)
                j = next((n for n, p in enumerate(rows) if i is not None and n > i and core.norm(p["text"]).startswith(after)), None)
                if i is None or j is None:
                    print("OLD_FIX problem: missed range", part, unit, first)
                    continue
                for p in rows[i:j]:
                    if not p.get("skip") and (p["end"] is None or p["end"] > fields["end"]) and p["start"] < fields["end"]:
                        p.update(fields)
                OLD_FIX_USED.append(why)
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
    # static method decisions as published (the published parts reworded them; their content does not depend on data)
    for i, x in enumerate(d["decisions"]):
        for pre in CARRY:
            if x.startswith(pre):
                same = [y for y in pub.get("decisions_static", []) if y.startswith(pre)]
                if len(same) == 1:
                    d["decisions"][i] = same[0]
    if "--nofix" not in argv:
        d["decisions"] += stale_fix.decisions()
        if OLD_FIX_USED:
            d["decisions"].append("Life spans set by hand after the stale-wording rules: " + "; ".join(dict.fromkeys(OLD_FIX_USED)) + ".")
        open_ = OPEN.get(part)
        if open_:
            d["decisions"].append(open_)
    t = out.with_suffix(".json.tmp")
    t.write_text(json.dumps(d, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")
    os.replace(t, out)
    print("wrote", out, "rules used:", {k: len(v) for k, v in stale_fix.USED.items()})
    return rc or 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
