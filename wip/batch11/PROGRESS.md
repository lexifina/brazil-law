# Brazil batch 11 progress (gitlaw-BR agent on alan-dell, 2026-10-31)

Owns `scripts/brazil-law/batch11/` and `corpus.d/99-batch11.json` (+ `.PUBLISH`). Never commits or pushes. Scratch OUTSIDE
the repo: `~/Documents/.gitlaw-scratch/brazil-b11` (trial parts, page texts), merged build via
batch10/.tmp/runbuild_rub.py (brazil-rub-src / brazil-rub / brazil-rub-c).

## Choice
The coordinator's examples (LGPD, Lei 11.101, Lei das S.A., Improbidade, CTN, Anticorrupção, Marco Civil, Lei de Drogas)
are all in the corpus already; of them only the Lei de Execução Fiscal was missing. Batch 11 = 10 major federal acts not
yet in it, chosen for weight in practice and a clean source: LEF 6.830/1980, Lei 12.529/2011 (CADE), EOAB 8.906/1994,
Lei 9.868/1999 (ADI/ADC), Lei 9.882/1999 (ADPF), Lei 8.137/1990, Lei 9.296/1996, Lei 8.009/1990, Lei 4.717/1965, Lei
7.492/1986.

## 99-batch11 - PUBLISHed 2026-10-31
10 acts, 55 versions, sha 885d9e06 (parse twice identical); merged 72 acts, 1692 versions, 1510 commits, check 0/0,
--compare identical, audit clean. README rows + jurisdiction.json (72 acts).
- Pages: 18 pinned (Common Crawl), 136 cited laws (84 new pins, the rest reused); gaps law:lei-14470-2022 (bad link on
  the page) and law:dl-2064-1983 pinned by hand.
- Hand tables (parse_batch11.py): VIGENCIA_FIXED lei-8176-1991 (5 days), mp-871-2019 (art. 34 III), mp-687-2015 and
  lei-13196-2015 (publication, with VIGENCIA_PROVISION Lei 13.196 -> LDC art. 23 from 1.1.2016; MP 687's p.u. from
  18.8.2015 until the conversion dropped it), mp-871 LOAS art. 20 (90 days, for LOAS if built); VETO_PROMULGATION Lei
  13.964 (DOU 30.4.2021) with VETO_PROMULGATED_UNITS LIT art. 8º-A §§ 2º/4º (checked in the promulgation text).
- Act days: LEF 23.12.1980 (90 days), LDC 29.5.2012 (180 days from DOU 1.12.2011; page misprints 1º.11.2011), LAP
  19.8.1965 (no clause: LINDB 45 days; republished 8.4.1974), the rest on publication.
- EOAB: 'Vide ADI' notes only (1.105, 1.127, 1.194, 3.026, 6.021, 6.053, 7.227, 7.231): no struck text, not modelled.
- Tools: .tmp/run.py (BelowNormal runner), .tmp/pagetxt.py, .tmp/dump.py (replayed lines of units).

## Configured, deferred (in ALL_ACTS, not VERIFIED)
- Lei 9.656/1998 (planos de saúde): MP 1.908/2.177-44 chain (MP 2.177-44 'pending' fate to set, EC 32 art. 2), 4 diffs vs
  compilado (art. 10 § 2º, 32 § 10 only in compilado: probably later laws Planalto's annotated page lacks).
- Lei 6.385/1976 (CVM): Decreto 3.995/2001 changes (a decree amending the law: needs a law record of kind decree) and 7
  'restored wording after an open one' problems.
- Lei 6.766/1979 (parcelamento do solo): compilado differs only in 'Art. 1º.' typesetting (7 units) - close to ready.
- Lei 8.742/1993 (LOAS): MP 1.164/2023 and MP 446/2008 fates; 1 diff (art. 20 stray quote).
