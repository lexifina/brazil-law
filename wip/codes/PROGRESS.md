# gitlaw-BR-codes progress (Código Civil + LGPD)

Helper on Brazil. Owns only `scripts/brazil-law/codes/` and `scripts/brazil-law/corpus.d/50-codes.json`.
The main Brazil agent owns CF/88 in corpus.json, fetch.py, parse.py, sources.json. Autopush builds and pushes.

## Status (2026-10-28 ~18:20 UTC): done, written, test-built clean

- `corpus.d/50-codes.json` (1.17 MB since 18:30 UTC: versions after the first give only `changes`, SCHEMA.md "Large acts"; was 46 MB with full `units`; atomic write): acts `codigo-civil` (63 versions, 2003-01-11 .. 2025-12-11) and
  `lgpd` (11 versions, 2018-08-15 .. 2026-02-25); 75 laws (incl. 2 MP-lapse records `mp-700-2015-fim`,
  `mp-958-2020-fim` with `restores`). 0 replay problems. Also carries `country` (used only if corpus.json is absent).
- Test build (with the main agent's corpus.json, 3 acts): 219 commits, 410 tags, 0 unexplained; check.py:
  0 mismatches, 0 trailer errors; `--compare` rebuild: history identical (tip 17fc436). Note: `--compare` writes
  `rebuild` into `scripts/brazil-law/verification.json` (builder behaviour).
- Replay vs Planalto's consolidated page: LGPD 0 differences; CC 10 articles differ, all source differences
  (typing slips in the annotated page, a missing º and capitalised headings in the consolidated page, and the
  consolidated page still printing the revoked EIRELI heading). Listed in `decisions`.

- `changes` rewrite verified: build into codes/.tmp/build-changes with `--compare` against a full-`units` build of the
  same corpus: history identical (218 commits, 410 tags, tip c83d540; only the docs commit differs, as it
  records the corpus sha256); check.py 0 mismatches. 50-codes.PUBLISH kept.

## Checklist

- [x] Read BRIEF.md, SCHEMA.md (corpus.d), brazil-law/PROGRESS.md, memory/git_for_law.md
- [x] codes/fetch_codes.py (reuses ../fetch.py: curl, ../.cache, requests.jsonl; extra shared-politeness wait)
- [x] Pinned + fetched (codes/sources_codes.json): cc-original (l10406.htm annotated), cc (l10406compilada.htm),
      lgpd (l13709.htm annotated), lgpd-compilado, every law/MP linked from a note (`law:<key>`), Atos
      Declaratórios for MP 700 (`ato:mp-700-2015`) and MP 958
- [x] parse_codes.py -> corpus.d/50-codes.json (`--dry --stats` to inspect without writing)
- [x] test build into codes/.tmp/build-changes + check.py + --compare
- [x] corpus.d/50-codes.PUBLISH written (CC 2009/2019 units match l10406compilada, 10 are source differences; LGPD 80/80)

## How to rerun

    python -X utf8 scripts/brazil-law/codes/fetch_codes.py plan      # all pinned captures (cached: no requests)
    python -X utf8 scripts/brazil-law/codes/parse_codes.py --stats
    python -X utf8 scripts/gitlaw_common/build.py scripts/brazil-law --repo scripts/brazil-law/codes/.tmp/build-changes --docs-date 2026-10-28
    python -X utf8 scripts/gitlaw_common/check.py scripts/brazil-law/codes/.tmp/build-changes --corpus scripts/brazil-law/corpus.json

## Method / decisions (full list is in the part's `decisions`)

- Struck-text replay as for the CF, plus: CSS `text-decoration:line-through` counts as struck; notes standing in
  their own block; a bare unparenthesised note; heading blocks split into successive wordings; restorations
  (wording repeated after an unconverted/lapsed MP wording starts when that ended); MP wording without successor
  ends on the conversion law's day; lapsed MPs (700/2015 last day 17.5.2016, 958/2020 last day 24.8.2020, from
  the Ato Declaratório / Congress record) end the next day and the restored text is credited to `<mp>-fim`.
- Dates: own vigência clause; staged clauses hand-checked (VIGENCIA_FIXED); "N dias" = pub + N; "N meses/anos" =
  pub + period + 1 day (STJ on the CPC: 18.3.2016); CC itself 11.1.2003 (the day courts use); LINDB +45 otherwise.
  Laws that defer only "efeitos" are dated by vigência (listed in decisions), consistent with the CF.
- LGPD: per-article entry into force from art. 65 (art. 65 from publication; ANPD arts 28.12.2018; arts 52-54
  1.8.2021; the rest 18.9.2020). Vetoed items of Lei 13.853 replaced on promulgation (DOU 20.12.2019).
- Alias: a note printing "Lei nº 15.452, de 2026" links to L15352.htm -> credited to lei-15352-2026.

## Gotchas / for the coordinator

- Test-build dir: brief said `.tmp-build-codes`, but autopush's wip snapshot only skips `.tmp-build`, `.tmp`, `tmp`,
  `.cache`; used `codes/.tmp/build-codes` instead.
- The builder now ships subfolder scripts: tools/codes/fetch_codes.py, parse_codes.py and sources_codes.json are
  in the repo.
- CDX length is the compressed size: small Planalto pages are < 3000 bytes; fetch_codes uses min_len 1500.
- 4 un-logged CDX probe requests were made by hand with curl for l10.677 (same UA, 2 s apart).
- WebSearch used: 3 of 8.
