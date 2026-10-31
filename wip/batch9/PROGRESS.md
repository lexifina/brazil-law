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

## Configured but deferred (in ALL_ACTS, not VERIFIED)
- Código de Trânsito (9.503, in force 22.1.1998): 145 problems: Leis 13.160/2015 and 14.229/2021 have no in-force day
  (staged clauses to read), ~20 'restored wording after an open one'. Next part.
- Código Florestal (12.651): MP 867/2018 lapse day (Ato Declaratório to fetch), a struck-by-STF expression in art. 3
  VIII b) (ADC 42 / ADI 4.903, 2018; needs the STF dates), a cited MP 2.216-37/2001 page Common Crawl lacks.
- Registros Públicos (6.015): the page is 'Atualizada a partir da republicação' (Lei 6.216/1975 republished the act):
  needs a model of the republication. Not tried.
- Lei 8.666/1993: the whole page is struck (revoked by Lei 14.133 from 30.12.2023): needs the repeal-version pattern and
  a check against the last version before repeal. Not tried. Lei 10.973/2004 and MP 2.216/2001 pages not in Common Crawl.
- Lei da Ação Civil Pública: see batch8/PROGRESS.md.
