# gitlaw-BR-4 progress (batch 4: Lei 11.101/2005, Lei 9.099/1995)

Helper on Brazil. Owns only `scripts/brazil-law/batch4/` and `corpus.d/97-batch4.json` (+ `97-batch4.PUBLISH`), plus
the README rows for these acts. Never pushes or commits (autopush publishes). Other parts are not touched
(90-batch3 sha 7b69bebb…, 95-rju sha a1950f76…, unchanged).

## Status (2026-10-29 ~09:00Z): DONE, PUBLISH written

- `corpus.d/97-batch4.json`: 399,380 bytes, sha a4058d3d…, 22 versions, 20 laws; parse twice identical.
  - lei-de-recuperacao-e-falencia (LRF, Lei 11.101/2005): 9 versions, 2005-06-09 .. 2021-03-26.
  - juizados-especiais (JEC, Lei 9.099/1995): 13 versions, 1995-11-26 .. 2021-11-23.
- Replay: 0 problems, 0 undated lines; 0 units differ from l11101compilado.htm (LRF) and from l9099.htm's unstruck
  text (JEC, one page only).
- Merged test build (all Brazil parts, empty repo scratchpad/br4/b-new, docs-date 2026-10-28): 821 commits, 14 acts,
  836 versions, 0 unexplained; check.py 0 mismatches, 0 trailer errors; `--compare` identical (main_identical true).
- Published acts byte-identical: for each of the 12 earlier acts, the sequence (author date, act tree) on main and
  futuro is the same as in a build without this part (scratchpad/br4/samebytes.py).
- Commit messages changed only on shared law-days (a law that also amends an earlier act on the same day now names
  LRF/JEC too): Lei 11.127/2005 (2005-06-29, CC), Lei 12.873/2013 (2013-10-25, CLT), LC 147/2014 (2014-08-08, CC),
  Lei 13.105/2015 (2016-03-18, CC + CE), MP 881/2019 (2019-04-30, CC), Lei 13.874/2019 (2019-09-20, CC + CLT),
  Lei 14.245/2021 (2021-11-23, CP + CPP); plus the docs commit. Lei 11.101's own CPP commit (2005-06-09) is unchanged;
  LRF's as-enacted commit is a new commit on that day.
- README: two table rows + check results bullet. jurisdiction.json not updated (main BR agent's file).

## Method

- `batch4/parse_batch4.py` imports `../batch3/parse_batch3.py` (which configures `../proc/parse_proc.py`) and replaces
  only its configuration, as `../rju/parse_rju.py` does. Pins: every Brazil pin file is read; batch4's win.
- `batch4/fetch_batch4.py` pins into `batch4/sources_batch4.json` via gitlaw_common/wayback.py (archive.org `id_`,
  newest good capture), cached in `../.cache/cc`. Planalto never contacted. Common Crawl: 0 Planalto captures.
- Pages: lrf l11101.htm 20261018232228, lrf-compilado l11101compilado.htm 20260607230534 (newest), jec l9099.htm
  20261027135943; 12 law pages pinned (7 more reused from other parts).

## Hand rules (all printed in decisions)

- VIGENCIA_FIXED: Lei 12.873/2013 -> 2013-10-25 (art. 72 III; its 11.101 change is art. 22), Lei 13.874/2019 ->
  2019-09-20 (art. 20 II); same days as the codes/CLT parts. Checked by hand: Lei 11.196/2005 art. 122 and LC 147/2014
  art. 5 are not among their staged items (publication day).
- TYPOS: art. 60 'Parágrafo-único.' (Lei 14.112 wording, both pages) read as 'Parágrafo único'.
- MP_DROPPED: art. 82-A as MP 881/2019 wrote it ends 2019-09-20: Lei 13.874/2019 (conversion) has no article on
  Lei 11.101 (checked on its page); new art. 82-A by Lei 14.112 from 2021-01-23.
- PROMULGATED_UNITS: Lei 14.112's vetoed parts promulgated after the override (DOU 26.3.2021 edição extra, printed
  at the end of the L14112 page, each marked '(Promulgação partes vetadas)'): art. 6 § 13, art. 6-B, art. 50-A,
  art. 60 Parágrafo único, art. 66 § 3º start 2021-03-26; art. 60's 2005 Parágrafo único stands until then.
- Lettered-article rule: art. 6-B (note only on its last line) and art. 167-D §§ 1º-2º take the article's
  'Incluído' law and day instead of the act's own day.

## Choice of acts (2026-10-29)

- Not taken: Lei 14.133/2021 (single page, no compilado), Lei 8.666/1993 (revoked 30.12.2023), Lei 6.015/1973 (very
  many MPs), Código Florestal (STF ADC/ADI conditioning). archive.org ran at 0.3-0.5 req/s machine-wide on 2026-10-29,
  so each extra act costs ~2 requests per cited law. Lei 14.133 is the natural next one (same method as Lei 9.099).

## Checklist

- [x] pages pinned + fetched
- [x] laws pinned + fetched
- [x] parse --stats --dry: 0 problems, 0 diffs
- [x] write part; scratch build (empty repo) + check.py + --compare
- [x] 97-batch4.PUBLISH; README rows

## How to rerun

    python -X utf8 scripts/brazil-law/batch4/fetch_batch4.py plan
    python -X utf8 scripts/brazil-law/batch4/parse_batch4.py --stats --dry
    python -X utf8 scripts/brazil-law/batch4/parse_batch4.py
