# Brazil batch 9 progress (gitlaw-BR agent on alan-dell, 2026-10-31)

Owns `scripts/brazil-law/batch9/` and `corpus.d/99-batch9.json` (+ `.PUBLISH`). parse_batch9.py imports batch8 with
BATCH8_ACTS=- (batch 8's hand tools SPAN_FIX/COURT_SPLIT/LABEL_FIX/UNIT_FIX/NAV_LINES/EXTRA_LAWS are cleared and reused;
P.COURTS and P.NOTE_FIX replaced, so nothing of batch 8 leaks into the decisions). Scratch: same folders as batch 8
(.gitlaw-scratch/brazil-b8src, brazil-b8, brazil-b8c; batch8/.tmp/runbuild.py).

## 99-batch9 - DONE, PUBLISH written 2026-10-31 ~05:00Z
LDB 77 versions, Lei Orgânica da Saúde 32, Lei das Eleições 21 (130). Part sha256 76b112a7; parse twice identical;
merged scratch build 1191 commits, 46 acts, 1288 versions, check 0/0, --compare identical, audit_push clean. README rows
added. Hand entries: VIGENCIA_FIXED for Leis 10.793/2003 (school-year clause -> 1.1.2004, stated), 11.700/2008,
12.061/2009, 14.986/2024; MP 1.303/2025 lapse (Ato Declaratório 67/2025, pinned ato:adc-67-2025); UNIT_FIX 'Art. 61A.'
(Lei das Eleições) and 'Art. 6º A.' (Lei 8.080).

## 99-batch9 v2 - Lei 8.666 and LACP added, re-PUBLISHed 2026-10-31 ~06:10Z
5 acts, 177 versions (LACP 11, Lei 8.666 36); the 3 earlier acts byte-identical. Part sha256 d2734d52; merged scratch
build 1226 commits, 48 acts, 1335 versions, check 0/0, --compare identical, audit clean. jurisdiction.json now lists all
48 acts with counts (regenerate with the snippet in this file's history: titles + first/last year + versions).
- Lei 8.666: page id `l8666-2023` pinned to Arquivo.pt capture 20231120085131 (245 strikes; the current page strikes all
  1,041 lines). REPEALS table in parse_batch9: every line alive on 30.12.2023 ends then, credited lei-14133-2021; the
  check compares the last pre-repeal version with that capture (P.consolidated returns {} for the act). SPAN_FIX art. 21
  § 2º V (recast by Lei 8.883/1994). Lei 10.973/2004 pinned by hand to a CC capture lacking '</html>' (complete() rejects
  it; content whole). MP 896/2019 and 910/2019 lapses from Atos 6/2020 and 36/2020.
- LACP: SPAN_FIX model of art. 1 (MP 2.180-35 revoked Lei 10.257 art. 53 before 9.10.2001), LABEL_FIX l/ll -> I/II,
  Lei 12.529/2011 published 1.12.2011 (page says 1.11) via batch8's new LAW_FIELD_FIX + VIGENCIA_FIXED -> 29.5.2012.
- batch8 changes (99-batch8 regenerates byte-identical, sha d5b1da8c): LAW_FIELD_FIX hook; 'restored wording after an
  open one' problems on hand-pinned dispositivos are dropped.

## Configured but deferred (in ALL_ACTS, not VERIFIED)
- Código de Trânsito (9.503, in force 22.1.1998): 145 problems: Leis 13.160/2015 and 14.229/2021 have no in-force day
  (staged clauses to read), ~20 'restored wording after an open one'. Next part.
- Código Florestal (12.651): MP 867/2018 lapse day (Ato Declaratório to fetch), a struck-by-STF expression in art. 3
  VIII b) (ADC 42 / ADI 4.903, 2018; needs the STF dates), a cited MP 2.216-37/2001 page Common Crawl lacks.
- Registros Públicos (6.015): the page is 'Atualizada a partir da republicação' (Lei 6.216/1975 republished the act):
  needs a model of the republication. Not tried.
- CTB problem list (batch9/.tmp/ctb.log): vigência of Leis 13.160/2015 (150 days), 12.971/2014 (1st day of 6th month),
  12.865/2013 (staged), 14.229/2021 (staged by CTB article), 12.249/2010 (staged), 15.452/2026 (no DOU day read); MP
  fates 75/2002, 646/2014, 882/2019, 1.050/2021, 1.360/2026; 7 mistyped notes; 15 restored-wording; 20 diffs.
