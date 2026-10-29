# gitlaw-BR-proc progress (CPP + CDC)

Helper on Brazil. Owns only `scripts/brazil-law/proc/` and `scripts/brazil-law/corpus.d/80-proc.json`
(+ `80-proc.PUBLISH`). Autopush builds and pushes. Method copied from ../parse_phase2.py / ../fetch_phase2.py
(struck-text replay of Planalto's annotated page through Wayback `id_` captures), with generic pieces of
../clt/parse_clt.py (law-ref regex, note forms, page_info checks).

## Status (2026-10-28 ~20:20 UTC): DONE, written, PUBLISH written

- `corpus.d/80-proc.json` (820 KB, `changes` deltas, atomic write; sha 424103606c66…): acts
  `codigo-de-processo-penal` (70 versions, 1942-01-01 .. 2026-08-07) and `codigo-de-defesa-do-consumidor`
  (16 versions, 1991-03-11 .. 2026-09-25); 85 laws incl. court `stf-adi-2797`. 0 replay problems, 0 anachronisms.
- Replay vs consolidated: CDC 0 differences; CPP 1 (heading 'CAPÍTULO II / DO JULGAMENTO' struck on the annotated
  page with arts. 556-562, kept by the consolidated page; explained in decisions).
- Merged test build (all 8 Brazil acts, proc/.tmp/country -> proc/.tmp/build): 644 commits, 1263 tags, 0
  unexplained; check.py 0 mismatches; --compare identical (history tip d04186b). parse twice: same sha.
- `corpus.d/80-proc.PUBLISH` written 20:20Z. Autopush 20:25Z: main 59e40f4 (642 commits, 8 acts, 634 versions), check 0 mismatches.
- For the main Brazil agent: repo/README.md and jurisdiction.json do not list CPP and CDC yet (not my files).

## Files

- `fetch_proc.py` (copy of ../clt/fetch_clt.py): `pages`, `laws cpp cdc`, `missing`, `lexml`, `plan`. Pins in
  `sources_proc.json`; reuses pins of ../sources_phase2.json, ../codes/sources_codes.json, ../clt/sources_clt.json;
  shared ../.cache and requests.jsonl; waits 1.5 s after anyone's last logged request. One process at a time.
- `parse_proc.py` -> `../corpus.d/80-proc.json`. `--stats --dry` to inspect.
- Test builds in `proc/.tmp/` only. `.tmp/dump.py <cpp|cdc> <unit>...` prints parsed paragraphs; `.tmp/dry_write.py`
  writes the part to .tmp; `.tmp/verify.py` sanity-checks a part.

## How to rerun

    python -X utf8 scripts/brazil-law/proc/fetch_proc.py plan     # all pinned captures (cached: no requests)
    python -X utf8 scripts/brazil-law/proc/parse_proc.py --stats --dry
    python -X utf8 scripts/brazil-law/proc/parse_proc.py

## Rules added (beyond parse_phase2; all in decisions)

- struck "(VETADO)" + promulgated wording (Lei 13.964: CPP 3º-B § 1º, 14-A §§ 3º-5º, DOU 30.4.2021)
- COURTS stf-adi-2797 (CPP art. 84 §§ 1º-2º struck; ata DJ 26.9.2005 from STF abaAndamentos)
- REWRITE_BLOCKS: Lei 11.689/2008 re-enacted the Júri chapter (arts. 406-497) as one struck block + new chapter
- heading-reworded (CPP Capítulo V, Lei 11.690/2008), heads for struck headings, successor past headings
- typesetting-mixed paragraphs (struck º/./link = unstruck; strike ending mid-word = struck); ".." -> "."
- EDITORIAL: CDC art. 39 XI editorial line dated by Lei 9.870/1999 (anachronism rule)
- NOTE_FIX: CDC art. 54 § 3º note missing "Lei" (link L11785.htm)
- VIGENCIA_FIXED Lei 263/1948 (staged by region: Distrito Federal day 29.2.1948); PUBLISHED_FIXED from LexML
- LexML cross-check of DOU days: 6 Planalto pages print a wrong day (5.941/1973 prints 1975, 12.681/2012 prints a
  day before enactment, ...): LexML day used
- MP_PENDING: MP 1.393/2026 (CDC art. 57) still within its term on 28.10.2026: wording stands open

## Requests outside fetch.py's log

- none. STF (3) and LexML (82) pages went through fetch.get (logged). WebSearch used: 0.
