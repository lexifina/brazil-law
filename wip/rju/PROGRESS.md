# gitlaw-BR-8112 progress (Lei 8.112/1990, Regime Jurídico dos Servidores Públicos Civis da União)

Helper on Brazil. Owns only `scripts/brazil-law/rju/` and `corpus.d/95-rju.json` (+ `95-rju.PUBLISH`). Never pushes or
commits (cadence change 2026-10-29: a 4-hourly autopush pass publishes). 90-batch3.json is NOT touched: batch 3's
parser with BATCH3_RJU unset still writes its three acts byte-identical.

## Method

- `rju/parse_rju.py` sets BATCH3_RJU=1, imports `../batch3/parse_batch3.py` (which configures `../proc/parse_proc.py`),
  keeps only the RJU act and adds the RJU tables. Output: `corpus.d/95-rju.json` (batch 3's write_part writes
  `rju/.tmp/stage.json`, the part is finished from it: own sources/requests/ai_use).
- `rju/fetch_rju.py` imports `../batch3/fetch_batch3.py`, pins into `rju/sources_rju.json` (batch 3's pins are read too;
  mine win for the same id). Pages via gitlaw_common/wayback.py (Common Crawl first, then archive.org id_), cached in
  `../.cache/cc`. Planalto never contacted.

## Pins added (rju/sources_rju.json)

ato:mp-689-2015 (adc-001-mpv689, 20260616184643), ato:mp-792-2017 (adc-065-mpv792, 20260616185958), ato:mp-805-2017
(ato-19-mpv805, 20260712210517), ato:mp-873-2019 (adc-43-mpv873, 20261004193158), law:mp-765-2016 (mpv765.htm,
20261015082912; batch 3 had L8270.htm), law:lei-13464-2017 (fetch running).

## Batch 3 handoff items: status

- [x] MP lapse days (MP_LAPSE, from the Atos Declaratórios linked on the RJU page): 689 -> 2016-02-08, 792 -> 2017-11-29,
      805 -> 2018-04-09, 873 -> 2019-06-29 (same as the CLT part).
- [x] MP 2.225-45/2001 standing (EC 32 art. 2) via MP_PENDING + own decision text (MP_STANDING); MP 1.132/2022 converted
      into Lei 14.509/2022 (page prints '14 509': CONVERTED_FIX).
- [x] Staged clauses: MP 664/2014 -> 2015-03-01 (art. 5 III); Lei 13.135/2015 -> 2015-06-18 (art. 6 III) except art. 217
      IV c -> 2017-06-19 (art. 6 II b; LINE_VIGENCIA); MP 871/2019 -> 2019-01-18 (art. 39 III). KeyError gone.
- [x] MP 765/2016 re-pinned; converted into Lei 13.464/2017 (its art. 93 wording was not kept: restored wording).
- [x] 82 undated lines reviewed: 77 dated by the MP fates above; hand rules (HAND, from the amending act's own text):
      art. 91 § 1º/§ 2º end with MP 2.225-45, art. 91 Parágrafo único out while MP 792 in force, art. 98 Parágrafo
      único -> § 1º by Lei 9.527/1997; MP 792 note without '(' (art. 117 XI) read as note; placeholders with only
      'Vide MP 301/341' left out (art. 51 IV, Subseção IV heading copy, art. 60-B IX). Left out (undated): art. 44 III.
- [x] MP 664 table (art. 217 § 3º I) moved from titulos into art. 217 (TABLE_ROWS): was dated 1990.
- [x] Remaining consolidated-page diffs explained (EXPLAINED): art. 60-B, 78, 133, 217.
- [x] lei-13464-2017 pinned (20261012081916): 0 replay problems, 55 versions. 90-batch3 rebuilt without BATCH3_RJU:
      sha 7b69bebb… identical to the written part.
- [x] corpus.d/95-rju.json written 01:25 local (394 KB). Test build (rju/.tmp/testbuild.sh, all Brazil parts into empty
      rju/.tmp/build, docs-date 2026-10-28): 808 commits, 12 acts, 813 versions, 0 unexplained; check.py 0 mismatches,
      0 trailer errors.
- [x] RSF 46/1997 pinned (law:rsf-46-1997, Wayback 20080414200129; newer captures are F5 bot pages): DOU 26.5.1997,
      in force on publication; ends art. 8 IV and art. 23 (caput, §§ 1º-2º) on 1997-05-26 (COURTS entry, kind law, as
      batch 3's RSF 337/1983), before Lei 9.527's revocation.
- [x] FINAL (2026-10-29 ~01:50 local): corpus.d/95-rju.json 395,754 bytes, sha a1950f76…, 56 versions (1990-12-12 ..
      2022-08-04), 53 laws, 0 replay problems; parse twice identical. 90-batch3 still identical (7b69bebb…).
      Merged test build: 809 commits, 1603 tags, 12 acts, 814 versions, 0 unexplained; check.py 0 mismatches, 0 trailer
      errors; --compare identical (main_identical true).
- [x] corpus.d/95-rju.PUBLISH written. Nothing pushed or committed (autopush's 4-hourly pass publishes).

## Open / not possible

- MP periods without wording on Planalto's page (MP 301/2006, MP 341/2006, MP 359/2007) are not shown (decisions).
- art. 44 III (struck, no note; Lei 9.527/1997 rewrote I-II without it but names no revocation): left out, listed.
- repo/README.md and jurisdiction.json do not list batch 3's acts or the RJU yet (main BR agent's files).
- LexML records for MP 765/2016 and Lei 13.464/2017 not fetched (optional DOU cross-check; Planalto day used).

## How to rerun

    python -X utf8 scripts/brazil-law/rju/fetch_rju.py plan     # everything pinned (cached: no requests)
    python -X utf8 scripts/brazil-law/rju/parse_rju.py --stats --dry
    python -X utf8 scripts/brazil-law/rju/parse_rju.py          # writes corpus.d/95-rju.json
