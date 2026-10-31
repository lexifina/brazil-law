# Brazil batch 8 progress (gitlaw-BR agent on alan-dell, 2026-10-31)

Owns only `scripts/brazil-law/batch8/` and `corpus.d/99-batch8.json` (+ `.PUBLISH`); later parts 99-batch9, ... in their
own folders. Never commits or pushes (autopush publishes PUBLISHed parts under the standing yes). Scratch builds OUTSIDE
the repo: `~/Documents/.gitlaw-scratch/brazil-b8src` (copy of the country folder + the trial part),
`brazil-b8` (build), `brazil-b8c` (--compare). Script `batch8/.tmp/runbuild.py` runs build, check, compare.

## 99-batch8 - DONE, PUBLISH written 2026-10-31 ~04:10Z

10 acts, 109 versions: Lei de Lavagem 20, Estatuto do Desarmamento 22 (the two acts batch 7 deferred), Crimes
Hediondos 20, LINDB 7, Organizações Criminosas 6, Propriedade Industrial 6, Direitos Autorais 7, Estatuto da Juventude 2,
Lei Geral do Turismo 7, Estatuto da Pessoa com Deficiência 12. Part sha256 d5b1da8c (after dropping two batch-7 NOTE_FIX decisions that leaked in: batch 8 now replaces P.NOTE_FIX); parse twice identical; merged
scratch build 1074 commits, 43 acts, 1158 versions, check.py 0/0, --compare identical, private.audit_push clean.
README rows added (repo/README.md); jurisdiction.json not updated.

How it works: parse_batch8.py imports batch7 with BATCH7_ACTS=- (no act of its own) and sets its own acts, days, pins
(sources_batch8.json). New generic hand tools:
- SPAN_FIX: (act, unit, label, text start or "", n-th) -> span fields (start/end/laws/gaps/skip), lines 'pinned' so
  stale_fix leaves them; re-applied after apply_rewrites (date-order rule overwrote them otherwise).
- COURT_SPLIT (a court note printed inside the text of a mixed line), LABEL_FIX, UNIT_FIX ('Art. 10A.'), NAV_LINES
  (Lei 12.850's page prints its nav links as lines), EXTRA_LAWS (MP 390, credited but cited only by 'Vide' notes).
- Lei 9.279 staged start via build_act gates (LPI_EARLY units from 15.5.1996, the rest 15.5.1997).
- write_part strips 'Texto para impressão ...' from law titles (page_info quirk; the older parts still carry it).

Facts settled (pins ctx:* in sources_batch8.json):
- LLav COAF chain: MP 870 (1.1.2019) -> Lei 13.844 art. 72 VETADO, so MP 870's art. 14/16 wording ends 18.6.2019 and
  the earlier one stands for a day -> MP 886 (19.6.2019) -> art. 16 revoked by MP 893 (20.8.2019; Lei 13.974); art. 14 back
  to the original when Lei 13.901 (12.11.2019, no 9.613 change) converted MP 886. § 2º (Lei 13.506) ends with MP 893.
- EDes: MP 379 (29.6.2007) revoked by MP 390 (DOU 18.9.2007 extra); restored wordings; MP 394 (21.9.2007, art. 5 § 3º
  only) suspended by STF ADI 3.964 MC, Plenário 12.12.2007 (STF case summary; acórdão DJ 11.4.2008; the ata's DJ day is
  NOT in any record read, so dated the session day, stated in decisions); MP 417 (1.2.2008) -> Lei 11.706 (20.6.2008).
  Art. 6 III (expressions) and IV: ADI 5.948 MC, monocratic 29.6.2018 ('IMEDIATA SUSPENSÃO'), final ADI 5.538/5.948/ADC
  38 (virtual session ended 27.2.2021, Informativo 1007). Art. 11 § 2º: Planalto's 'Vide MP 390' copy is MP 417's
  wording, so it is left out and the 2003 wording is restored instead.
- Robots: portal.stf.jus.br/processos is Disallowed for `*` (STF case pages are no longer read live; earlier parts did).
  One such page was fetched by mistake at ~02:20Z before checking and deleted from the cache unused.

Deferred:
- Lei da Ação Civil Pública (7.347): configured, not VERIFIED. Art. 1's incisos 2001-2014 (Lei 10.257/2001 inserting
  'III - à ordem urbanística' vs MP 2.180-35/2001 adding 'VI - à ordem urbanística' and rewording V) need a hand model;
  'l -'/'ll -' label slips (art. 1 I/II, art. 5 I) too.
- EDes: 2005 referendum on art. 35 (rejected) could be a no-words note law; the annex fee table is not modelled.

## Next (99-batch9)
Lei 8.666/1993 (repealed 30.12.2023 by Lei 14.133 art. 193 II as amended: repeal-version pattern), Código de Trânsito
(9.503), LDB (9.394), Lei 8.080, Lei das Eleições (9.504), Código Florestal (12.651), Registros Públicos (6.015:
l6015consolidado.htm), LACP. All pages present in the Common Crawl index (batch5's planalto index).

## How to rerun
    python -X utf8 scripts/brazil-law/batch8/fetch_batch8.py pages|laws|missing|gap <id> <url>|refetch <ids>
    BATCH8_ACTS=<slug> BATCH8_OUT=batch8/.tmp/x.json python -X utf8 scripts/brazil-law/batch8/parse_batch8.py --stats --dry
    python -X utf8 scripts/brazil-law/batch8/parse_batch8.py      # writes corpus.d/99-batch8.json
Debug: batch8/.tmp/spans.py <act> <unit regex> batch8 (final spans), batch8/.tmp/law.py batch8 <pin id> [regex].
