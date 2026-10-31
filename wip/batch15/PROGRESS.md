# Brazil batch 15 progress (gitlaw-BR agent, 2026-10-31)

Owns `scripts/brazil-law/batch15/` and `corpus.d/99-batch15a.json` (Lei 8.212/1991) and `99-batch15b.json` (Lei 8.213/1991),
each with its `.PUBLISH`. Also added the two parts' MOVES to `../effects_fix.py`. Never commits or pushes. Scratch outside
the repo: `~/Documents/.gitlaw-scratch/brazil-b15` (trial parts, page texts, `eff/` = parts after
effects_fix), merged build `brazil-b15-src` / `-build` / `-c`. No background processes left running (all runs were
foreground, BelowNormal via .tmp/run.py; PIDs are printed at the top of each .tmp/*.log).

## State: both parts PUBLISHed 2026-10-31 ~13:52 local
- 99-batch15a: Lei 8.212 (custeio), 114 versions 1991-07-25 .. 2026-03-27; installed sha256 cf794f18 (pre-effects dbe4ce9c).
- 99-batch15b: Lei 8.213 (benefícios), 95 versions 1991-07-25 .. 2026-09-01; installed sha256 bd6484dc (pre-effects 10a690b9).
- Merged scratch build: 114 acts, 2265 versions (2056 + 209), 1861 commits, future 5, check.py 0 mismatches / 0 trailer
  errors, --compare identical (main identical), audit_push clean main and futuro.
- README rows + jurisdiction.json (114 acts, 2265 versions) updated with batch14/.tmp/docs.py .tmp/rows-ab.json.

## How to rerun (per part x = a | b)
    BATCH15_PART=x BATCH15_OUT=<scratch>/x-run1.json python batch15/.tmp/run.py <log> scripts/brazil-law/batch15/parse_batch15.py --stats
    (twice, sha256 equal), then copy to <scratch>/eff/99-batch15x.json and
    python -X utf8 scripts/brazil-law/effects_fix.py <scratch>/eff/99-batch15x.json      # MOVES "99-batch15a/b.json"
    python batch15/.tmp/run.py <log> scripts/brazil-law/batch15/.tmp/runbuild.py <eff>/99-batch15a.json <eff>/99-batch15b.json
- Without BATCH15_OUT the parser writes corpus.d/99-batch15x.json directly (pre-effects: always run effects_fix after).
- Fetch: `python batch15/.tmp/run.py <log> scripts/brazil-law/batch15/.tmp/gaps.py id=url ...` pins into
  batch15/sources_batch15.json (Common Crawl first). Pinned here: ato:adc-58-2016-mpv739, ato:adc-67-2019-mpv891,
  ato:adc-89-2026-mpv1355, ctx:dec-5256-2004, law:mp-222-2004, law:mp-404-2007, ctx:rsf-26-2005, ctx:rsf-10-2016,
  ctx:rsf-15-2017, ctx:l8212-original (L8212orig.htm).
- Tools (.tmp/): spans.py <part> <units|undated> (final life spans), udiff.py <part> <act> <unit> [from to] (line diffs of
  each change), lawtxt.py <key|page> [needle] [n], region.py <page> <from> <to>, effrep.py <act no.> <laws> (articles naming
  the act + vigência clause), ordercheck.py (lines out of order), missorig.py (original articles first seen late),
  headyear.py (batch15 pins), fixbs.py (repair heredoc backspaces).
- Checks per part: batch10/.tmp/dupline.py, batch7/.tmp/dupcheck.py, batch7/.tmp/leakcheck.py, batch10/.tmp/firstline.py,
  .tmp/ordercheck.py, .tmp/missorig.py, batch14/.tmp/pubgap.py, .tmp/headyear.py (+ batch14's).

## What parse_batch15.py adds (imports batch14 with BATCH14_PART='-')
- MP 905/955 sequence: CLT's mp_pairs ported. It runs inside batch3's `_lifespans` hook (after parse_proc.lifespans,
  before every batch wrapper), re-reads notes into _starts/_ends (fused notes split), then mp_pairs_restore() after the
  rewrites puts the unstruck third copy of a revoked wording back from 19.8.2020 (the shared duplicate rule had skipped it).
- Footnotes: <sup>NN</sup> markers (1998 edition) dropped from l8212 and its compilado (50 markers).
- Headings: bare <p> inside <center> blocks starting TÍTULO/CAPÍTULO/Seção (or all-caps lines in mixed blocks) centred.
- Tables: cells inside body <table>s de-centred and marked; cells the rubrica rule moved go back to their article.
- Arts. 22A/22B/25A (no hyphen) split into art-022-a/-b, art-025-a. Note-closing period after ';'/':' dropped.
- L8212orig.htm: 1991 text of arts. 20 (with its table and p.u.), 26, 36, 68, 94 and art. 6 § 10 inserted struck.
- Senate resolutions as COURTS (part a only): RSF 26/2005 (art. 12 I h), RSF 10/2016 (art. 22 IV), RSF 15/2017 (art. 25 I).
- Hand spans (B8.SPAN_FIX / ARTICLE_FIX) with reasons printed in the decisions; EXPLAINED for every consolidated diff.

## Judgement calls to review
- RSF 15/2017 applied to art. 25 I (Lei 9.528's wording, still the text in 2017): inciso absent 13.9.2017-10.1.2018.
  Contested in practice (STF RE 718.874); the history follows the resolution's words and Planalto's note.
- Lei 9.876/1999 'majoração de contribuição' read as art. 21, art. 22 III-IV, art. 30 I b) and §§ 4º-5º (1.3.2000).
- Lei 11.098/2005 art. 4 dated 14.1.2005 (Decreto 5.256/2004, the act its art. 14 I waits for, was published 28.10.2004);
  MP 222/2004 (same wording, not noted on the page) not modelled.
- Lei 13.135/2015's 2-year term: art. 77 § 2º IV from 19.6.2017 (absent 18.6.2015-19.6.2017); its art. 16 III left out.
- Art. 77 § 2º II: Lei 13.183 prevails over Lei 13.146 on 3.1.2016 (same day; the later law).
- MP 619/2013 + Lei 12.873/2013 effect days: the '; e' on the item before each new item moved with it.
- Art. 106 I (Lei 11.718) kept although Planalto strikes it by style (no note; consolidated page has it in force).

## Not settled / left out (in the decisions as open items)
- Lei 8.213 art. 74 § 3º: MP 871/2019's wording (120 days after 18.1.2019) is not printed; not modelled.
- 'Vide ADI' pointers on both pages (no struck words): not modelled.
- Lei 8.212 art. 93: caput revoked 1998 (Lei 9.639), parágrafo único alone until 2008 (firstline flag, true).

## Earlier groundwork (batch14/PROGRESS.md) used: pins, MP lapse days, staged clauses; all applied above.
