# Brazil batch 5 / 5b progress (agent on alan-dell, 2026-10-29 evening)

Owns only `scripts/brazil-law/batch5/`, `scripts/brazil-law/batch5b/`, `corpus.d/98-batch5.json` (+ `.PUBLISH`) and
`corpus.d/99-batch5b.json` (+ `.PUBLISH`). Never commits or pushes. Earlier parts untouched.

## State found on alan-dell (restore from world-law-ops wip/brazil-law 90b1abe, 19:41Z)

- `corpus.d/98-batch5.json`, `99-batch5b.json`, both `.PUBLISH` files, `batch5/PROGRESS.md`, all of `.cache/` and
  every `.tmp*` were NOT in the restore (also not on wip/archive branches or on lexifina/brazil-law main, which holds
  the 14 acts up to batch 4, bb7cf9e). Only `batch5/fetch_batch5.py`, `parse_batch5.py`, `sources_batch5.json`
  (114 Common Crawl pins, LLC only) survived. The laptop's later batch-5 work (and what was in 99-batch5b) is lost;
  rebuilt below.

## 98-batch5: Lei 14.133/2021 (LLC) - rebuilt

- Refetched every pin into the cache (`fetch_batch5.py refetch --all-batch5`, then `refetch --need` from
  `batch5/.tmp/need.py`, an instrumented dry parse that lists cache misses); 8 LexML URN records refetched direct
  (robots allows /urn/). Common Crawl index of planalto.gov.br/ccivil_03/ rebuilt (`ccindex 16`, 659,511 records).
- New hand rules (all printed in decisions):
  - MP_LAPSE: MP 1.166/2023 back from 2023-07-21 (ADC nº 50/2023, 'encerrado no dia 20 de julho'), MP 1.167/2023 back
    from 2023-07-29 (ADC nº 51/2023, 'encerrado no dia 28 de julho'); ADC pages pinned as ato:adc-50-2023,
    ato:adc-51-2023 (Common Crawl).
  - PROMULGATED_PARTS: vetoed parts promulgated after override, DOU 11.6.2021 (LexML record of Lei 14.133:
    'Publicação de Veto Parcialmente Rejeitado 2021-06-11'): art. 37 § 2º (+ I, II), art. 54 § 1º, art. 115 § 4º,
    art. 175 § 2º; the struck '(VETADO)' lines end then.
  - LAPSE_RESTORED: art. 191 Parágrafo único printed struck (revoked by MP 1.167) and again unstruck: struck copy ends
    2023-03-31, unstruck copy back 2023-07-29 credited to mp-1167-2023-fim.
- Published-text cleanup (PUSH RULES 3): sources name/notes no longer mention Common Crawl, Wayback or bot challenges;
  the extra "Common Crawl" source entry is gone; a version's `source_url` is the Planalto URL (capture pinned in the
  pin file); ai_use generic.
- Result: 11 versions 2021-04-01 .. 2026-07-21, 0 problems, 0 undated lines, 0 units differ from the page's unstruck
  text (Planalto has no compilado for 14.133). Parse twice identical, sha 1770bbd8….
- Merged scratch build (.tmp-build, docs-date 2026-10-29): 0 unexplained, check.py exit 0 (details []).

## Checklist

- [x] 98-batch5 rebuilt + determinism
- [x] earlier 14 acts unchanged vs published main bb7cf9e: `batch5/.tmp/samebytes.py .tmp/ops refs/remotes/pubmain~1
      .tmp-build main~1` (sequence of (author date, act tree) per act, docs commit excluded since its date is the
      docs-date): all 14 "same"; futuro's 3 commits have identical CF trees and dates. `--compare` rebuild: history
      identical (main tip differs only by verification.json, ISSUES #3).
- [x] 98-batch5.PUBLISH (22:27Z; check.py 15 acts, 847 versions, 0 mismatches, 0 trailer errors)
- [x] 99-batch5b: Marco Civil, Anticorrupção, Drogas (+ Arbitragem, Inquilinato, Mediação) + PUBLISH
- [ ] deferred: Improbidade (Lei 13.019 art. 88 municipal split), Crimes Ambientais (retificação vs LINDB § 3),
      LAI (Lei 14.129 staged by entity), Lei 9.784 (retificação of 11.3.1999 not shown)
- Repos: `.tmp/ops` holds published main/futuro (for samebytes); `.tmp-build` is the last verified scratch build.

## 99-batch5b (scripts in batch5b/, acts enabled by env BATCH5B_ACTS=<slug,...>)

- Pages pinned (Common Crawl) for all five: mci, lac, lia, lia-compilada, lca, lad (lad needed `complete()` fixed:
  its F5 tail after </html> is ~90 KB). 43 cited laws linked, 34 newly pinned. ADC 58/2021 (MP 1.068), ADC 27/2016
  (MP 703), RSF 5/2012 pinned as ato:*.
- MCI (Marco Civil): ready. 4 versions (2014-06-23 art. 32 60 days; 2020-09-18 LGPD art. 60; 2021-09-06 MP 1.068;
  2021-09-14 MP 1.068 rejected, ADC 58/2021 'rejeita sumariamente', relabelled law "...: rejeitada"). '(Rejeitada)'
  read like '(Vigência encerrada)'. 0 problems, 0 diffs (page = its own consolidated text). STF Tema 987 (art. 19,
  2025) is not marked on Planalto's page: not modelled.
- LAC (Anticorrupção): ready. 3 versions (2014-01-29 art. 31 180 days; 2015-12-21 MP 703; 2016-05-30 lapse, ADC
  27/2016). 0 problems, 0 diffs.
- LAD (Drogas): ready. 12 versions 2006-10-08 .. 2026-03-25 (art. 74, 45 days); RSF 5/2012 split rule (expression
  struck in art. 33 § 4º, DOU 16.2.2012, kind law like batch 3's RSF 337/1983); note typo 'Lei 15.581/2025' ->
  Lei 15.281/2025 (NOTE_FIX; pin id renamed law:lei-15281-2025, same capture); struck chapter-name lines under struck
  'CAPÍTULO' lines read as headings (HEADING_NAME_FIX). Vide RE 635659 / ADI 4274 / ADIN 3807 are 'Vide' only (words
  unchanged on Planalto): not modelled. 0 problems, 0 diffs.
- 99-batch5b.json written with MCI+LAC+LAD (BATCH5B_ACTS=marco-civil-da-internet,lei-anticorrupcao,lei-de-drogas):
  19 versions, parse twice identical (sha 5ae5a503…). Scratch build 849 commits, check.py 18 acts / 866 versions /
  0 mismatches / 0 trailer errors; 14 published acts "same".
- 99-batch5b.json now MCI+LAC+LAD+LArb+LInq+LMed (BATCH5B_ACTS=marco-civil-da-internet,lei-anticorrupcao,lei-de-drogas,
  lei-de-arbitragem,lei-do-inquilinato,lei-de-mediacao): 30 versions, parse twice identical (sha e646743a…), 0 problems,
  0 diffs (LInq against l8245compilado.htm). LInq: MP 2.223/2001 standing (EC 32 art. 2) until Lei 10.931/2004; label
  typo 'd}' fixed (TYPOS). Scratch build (.tmp-build): 858 commits, check.py 21 acts / 877 versions / 0 mismatches /
  0 trailer errors; samebytes: 14 published acts "same" vs pubmain, and all 18 acts of the 3-act build "same" (LLC,
  MCI, LAC, LAD unchanged by adding LArb/LInq/LMed); --compare history identical. 99-batch5b.PUBLISH written 23:2xZ.
  parse_batch5b.py now defaults to these six (VERIFIED); BATCH5B_ACTS only for trials.
- LIA deferred: Lei 13.019/2014 art. 88 (as amended by Lei 13.204/2015) puts the law in force 540 days after
  publication (23.1.2016) but 1.1.2017 'para os Municípios'; its art. 77 changes to LIA art. 10 (XIX-XXI) therefore
  have no single settled in-force day, and 13.019's original XX/XXI wording (struck) never came into force (13.204
  rewrote it during the vacatio). The parser's default picks 2017-01-01. MP chains are handled (MP_PENDING), so LIA
  is otherwise ready (2 typesetting diffs vs l8429compilada.htm: art. 17 comma, 'Seção II-A' heading kept as revoked
  placeholder on the compilada).
- LAI deferred: Lei 14.129/2021's changes take effect 90/120/180 days after publication for União/Estados/Municípios
  (its vigência clause), so no single in-force day.
- README rows added for LLC, MCI, LAC, LAD (+ check-results sentence). jurisdiction.json not touched.
- NOTE for coordinator: adding acts inserts commits into the published history (and shared law-days such as Lei
  13.964/2019 on 2020-01-23 now also name the new acts' units), so main is not a fast-forward: needs the user's yes
  under PUSH RULES 3 (trees of the 14 published acts are unchanged).
- LIA (Improbidade): open: MP reissue chain notes (MP 1.337/1996, 1.472-31, 1.984, 2.088-35 'Vide', 2.180-35,
  2.225-45 standing under EC 32 art. 2), 46 '(Vide ADI 7042/7043/7156/7236)' notes; 29 problems on first dry run.
- LCA (Crimes Ambientais): open date: art. 81 (vigência) vetoed, so LINDB 45 days, but the DOU 17.2.1998
  retificação may restart the term (LINDB art. 1 § 3) -> 30.3.1998 vs 3.4.1998 not settled by the page. Deferred.

## Further acts (added to batch5b's ALL_ACTS; enable with BATCH5B_ACTS)

- Pages pinned: Arbitragem l9307.htm, LAI l12527.htm, LPA l9784.htm, Inquilinato l8245.htm + l8245compilado.htm,
  Mediação l13140.htm; 15 cited laws linked, 11 newly pinned.
- In-force days set: Arbitragem 1996-11-23 (60 days), LAI 2012-05-16 (180 days), Inquilinato 1991-12-20 (60 days),
  Mediação 2015-12-26 (180 days).
- LPA (Lei 9.784/1999) deferred: 'publicado no DOU de 1.2.1999 e retificado em 11.3.1999' (in force on publication):
  Planalto prints the rectified text and does not say what the rectification changed, so the 1.2-11.3.1999 wording
  is not settled. Same kind of issue as LCA.
- Lei do Inquilinato cites MP 2.223/2001 ('Revogada pela Lei nº 10.931, de 2004').

## How to rerun

    python -X utf8 scripts/brazil-law/batch5/fetch_batch5.py refetch --all-batch5
    python -X utf8 scripts/brazil-law/batch5/parse_batch5.py --stats --dry
    python -X utf8 scripts/brazil-law/batch5/parse_batch5.py
