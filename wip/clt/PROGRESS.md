# gitlaw-BR-clt progress (CLT, Decreto-Lei 5.452/1943)

Helper on Brazil. Owns only `scripts/brazil-law/clt/` and `scripts/brazil-law/corpus.d/70-clt.json` +
`corpus.d/70-clt.PUBLISH`. Autopush builds and pushes. Method copied from codes/ (struck-text replay of Planalto's
annotated page through Wayback `id_` captures, credits from the page's own notes).

## Status (2026-10-28 ~20:10 UTC): written, test-built clean, PUBLISH written

- `corpus.d/70-clt.json` (2.2 MB, `changes` deltas, atomic write): act `clt`, 220 versions (1943-11-10 .. 2026),
  229 laws (incl. `mp-808-2017-fim`, `mp-873-2019-fim`, `mp-905-2019-fim`, `mp-955-2020-fim`, STF ADI 1770/5938/5766).
  parse deterministic (sha256 914419d0… twice).
- Test build (all Brazil parts) in clt/.tmp/build: 575 commits (230 touch clt/), 1109 tags, 0 unexplained;
  check.py 0 mismatches / 0 trailer errors; `--compare` history identical (tip e3e441c; only the docs commit differs).
- Today vs del5452compilado.htm: 837/847 units equal; 10 are differences between Planalto's two pages (listed in
  decisions). 60 struck lines with no datable end are left out of all versions (listed in decisions).
- 72 replay problems remain, all in the decisions' "Open problems" line: mostly 1946 DL 8.740 / 8.987-A
  suspension tangles (art. 515, 532, 555, 558, 670, 738, 895, 902) and old struck blocks with no note.

## Files

- `fetch_clt.py` (copy of ../fetch_phase2.py): pins in `sources_clt.json` (reuses ../sources_phase2.json and
  ../codes/sources_codes.json pins); `pages`, `laws <page ids>`, `missing` (guesses Planalto paths for note laws
  without links), `plan`. Only ONE fetch_clt process at a time (each rewrites sources_clt.json from memory).
- `parse_clt.py` (copy of ../parse_phase2.py) -> `../corpus.d/70-clt.json`. `--stats --dry`, `--dump file.json`.
- Test builds only in `clt/.tmp/`.

## How to rerun

    python -X utf8 scripts/brazil-law/clt/fetch_clt.py plan          # everything pinned (cached: no requests)
    python -X utf8 scripts/brazil-law/clt/parse_clt.py --stats --dry  # inspect
    python -X utf8 scripts/brazil-law/clt/parse_clt.py                # write the part
    python -X utf8 scripts/gitlaw_common/build.py scripts/brazil-law --repo scripts/brazil-law/clt/.tmp/build --docs-date 2026-10-28
    python -X utf8 scripts/gitlaw_common/check.py scripts/brazil-law/clt/.tmp/build --corpus scripts/brazil-law/corpus.json

## Method additions over codes/ (all in the part's decisions)

- Decree preamble (DL 5.452 arts. 1-2) = preambulo.md; the closing ANEXO (art. 577 table) = anexo.md.
- Note forms: Suprimido, Extinto, Fica sem efeito (ends); Restabelecido/Restaurado/Revigorado/Corrigido (starts);
  typos Incuído/Inlcuído, "n]", "Revogado Medida Provisória", two notes fused in one parenthesis (split).
- "com vigência suspensa pelo DL 8.987-A": wording by DL 8.740 ends at 8.987-A; revocation by 8.740 is a gap;
  "Redação restabelecida" text printed once is also the 1943 text.
- MP 905/2019 + MP 955/2020: 905 in force 12.11.2019 (arts. 161/634/634-A 10.2.2020), revoked by 955 on 20.4.2020;
  955 lapsed 17.8.2020 (ADC 113) so 905 had effect again on 18.8.2020; 905's term ended 18.8.2020 (ADC 127).
  Planalto prints both copies; MP_PAIRS models it (one-day version on 2020-08-18).
- MP 808/2017 lapsed 23.4.2018 (ADC 22), MP 873/2019 lapsed 28.6.2019 (ADC 43); MPs 2.164-41, 2.180-35, 2.226/2001
  stand under EC 32 art. 2.
- STF: ADI 1770 (art. 453 § 1º, DJ 20.10.2006), ADI 5938 (art. 394-A II/III expression, DJE 4.6.2019), ADI 5766
  (art. 790-B caput expression and § 4º, art. 791-A § 4º expression, DJE 5.11.2021).
- End fallbacks for struck text: successor, note, parent, caput (the caput in force at its start was replaced),
  sibling (same start, nearest struck sibling), duplicate copies; else "undated" (left out, listed).
- Staged/odd vigência hand table: Lei 11.457/2007, 12.873/2013 (art. 392-B 23.1.2014), 13.874/2019, 13.876/2019,
  14.690/2023, MP 905/2019, Lei 4.825/1965, Lei 7.108/1983 (page misprints 1986); alias Lei 9.528 "de 1998" -> 1997.

## Requests outside fetch.py's log

- 3 curl requests to portal.stf.jus.br/processos/listarProcessos.asp (ADI 5766, 5938, 1770) for the incidente ids.
- WebSearch used: 0 of 6.

## Possible next steps

- Resolve the 1946 suspension tangles by reading DL 8.740 / 8.987-A pages (cached) article by article.
- Date the 60 undated struck lines from the amending laws' texts (many are DL 229/1967, DL 8.737/1946 blocks).
