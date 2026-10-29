# gitlaw-BR-batch3 progress (CTN, ECA, Código Eleitoral, Lei 8.112)

Helper on Brazil. Owns only `scripts/brazil-law/batch3/` and `scripts/brazil-law/corpus.d/90-batch3.json`
(+ `90-batch3.PUBLISH`). Autopush builds and pushes. Method: proc/'s replay, imported (not copied):
`fetch_batch3.py` configures `../proc/fetch_proc.py`; `parse_batch3.py` configures `../proc/parse_proc.py`.

## Terms (checked 2026-10-28, before any fetch)

- www.planalto.gov.br/robots.txt: none. Every Wayback capture of it (www, www1, 2025-26) is Planalto's error page
  "O conteúdo não foi encontrado"; www4 captures are F5 bot-challenge pages.
- gov.br Termo de Uso (Wayback 20261015002456 of https://www.gov.br/pt-br/termos-de-uso): no clause on automated
  access, scraping or bulk download; portal content CC BY-ND 3.0. Legal texts: official acts, no copyright (Lei
  9.610/1998 art. 8 IV). Nothing forbids the work, so it went ahead.
- Coordinator (2026-10-28): archive.org `id_` captures only, never Planalto directly; at most 1 archive.org request
  per 3 s (fetch_batch3 waits 3 s after the last request any Brazil script logged).

## Pages (pinned in sources_batch3.json)

ctn l5172.htm 20261023041622 / l5172compilado.htm 20261026202202; eca l8069.htm 20261023184051 / compilado
20261022101843; ce l4737.htm 20261021192341 / compilado 20261020015444; rju l8112cons.htm 20261016041731 /
l8112compilado.htm 20261004195859.

## Status (2026-10-29 ~00:00 local): CTN, ECA, CE DONE, written, PUBLISH written; Lei 8.112 in progress

- `corpus.d/90-batch3.json` (1.2 MB, `changes` deltas, atomic write; sha 7b69bebb…): codigo-tributario-nacional (21
  versions, 1967-01-01 ..), estatuto-da-crianca-e-do-adolescente (57, 1990-10-14 ..), codigo-eleitoral (46, 1965-08-18 ..);
  128 laws incl. court stf-adi-869, stf-adi-2404 and Senate resolution rsf-337-1983. 0 replay problems, 0 lines before
  their law. Parse twice: same sha.
- Remaining differences vs consolidated pages (CTN 11, ECA 1, CE 8 units) each explained in EXPLAINED (decisions).
- 6 undated struck lines left out and listed (CTN art. 52 § 3º II 'Vide' wording, CE art. 175 § 2º IV, CE art. 262 I-IV
  '(revogado)' placeholders).
- Merged test build (batch3/.tmp/testbuild.sh: all Brazil parts -> .tmp/build): 755 commits, 11 acts, 0 unexplained;
  check.py 0 mismatches; `testbuild.sh compare` identical.
- `corpus.d/90-batch3.PUBLISH` written.

## Handoff (wind-down 00:3xZ)

- Autopush: main 8358e40 pushed 00:20Z (BUILD_STATUS.json). No background jobs of mine are running.
- Cache: every page parse needs is in ../.cache (fetch.py, Wayback id_) and ../.cache/cc (wayback.py: RSF 337/1983).
- Exact next step: Lei 8.112. Run `BATCH3_RJU=1 python -X utf8 batch3/parse_batch3.py --stats --dry`, then fill
  P.MP_LAPSE (Ato Declaratório days; the CLT helper has MP 873/2019: back from 29.6.2019), P.MP_PENDING or
  permanent-MP handling for MP 2.225-45/2001 (EC 32 art. 2), VIGENCIA_FIXED or VIGENCIA_PROVISION for Lei 13.135/2015,
  MP 664/2014 and MP 871/2019 (staged clauses), re-pin MP 765/2016 with `fetch_batch3.py gap law:mp-765-2016
  <planalto mpv765 url>`, review the 82 undated lines, then compare with l8112compilado and flip the WITH_RJU default.
  Known bug: with RJU on, proc's mp_notes raises KeyError for mp-871-2019 (no in-force day yet).

## Checklist

- [x] Terms + robots recorded
- [x] fetch_batch3.py / parse_batch3.py; pages and cited laws fetched (laws, missing, lexml); gaps via wayback.py
- [x] rules (wrappers around parse_proc, all in decisions): Lcp / Ato Complementar notes; fixed-day clauses; staged
      Lei 14.690; mixed paragraphs split (Lei 12.010 swap; ADI 869, ADI 2.404); RSF 337/1983 (COURTS entry, kind law);
      Lei 13.509 promulgated vetoed parts (23.2.2018); laws in force before the act -> same_day versions (CTN: AC 27,
      AC 31, DL 27, DL 28 of 1966); printed-after; vetoed renumbering (CTN art. 205); Parágrafo único -> § 1º when § 2º
      added (ECA 152); unlabeled rows/'Pena' lines; BLOCKS (CTN art. 91 tables); TYPOS; RESTORE_AFTER (CE art. 242);
      undated struck text left out (as CLT)
- [x] write part, test build, check.py, --compare
- [x] 90-batch3.PUBLISH
- [ ] Lei 8.112/1990 (BATCH3_RJU=1; default off so a plain rerun gives the written part). Open: MP fates (664
      converted into 13.135 with staged clause; 689/2015, 792/2017, 805/2017, 873/2019 lapsed -> MP_LAPSE days; 2.225-45
      kept by EC 32 art. 2; 1.132/2022; 765/2016 pinned to a wrong page), staged clauses (Lei 13.135/2015, MP 664/2014, MP
      871/2019), 82 undated struck lines to review.

## How to rerun

    python -X utf8 scripts/brazil-law/batch3/fetch_batch3.py plan        # everything pinned (cached: no requests)
    python -X utf8 scripts/brazil-law/batch3/parse_batch3.py --stats --dry
    python -X utf8 scripts/brazil-law/batch3/parse_batch3.py             # writes corpus.d/90-batch3.json
    sh scripts/brazil-law/batch3/.tmp/testbuild.sh [compare]

## Requests outside fetch.py's log

- terms/robots probes (about 12 curl requests to archive.org and 1 to planalto.gov.br/robots.txt that got no
  answer, made before the coordinator's "never Planalto directly"); 3 CDX probes for the Lei 8.112 page names.
  WebSearch used: 0. RSF 337/1983 via gitlaw_common/wayback.py (Common Crawl had no capture; archive.org; logged in
  ../.cache/cc/requests.jsonl). STF case pages (4) and LexML (120) through fetch.get (logged).

## Lei 8.112 moved out (2026-10-29)

The open RJU item above is done by gitlaw-BR-8112 as its own part corpus.d/95-rju.json (rju/parse_rju.py turns BATCH3_RJU on and keeps only the RJU). Leave BATCH3_RJU unset here: 90-batch3.json stays CTN, ECA, CE. See rju/PROGRESS.md.
