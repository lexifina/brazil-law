# Brazil batch 13 progress (gitlaw-BR agent, 2026-10-31)

Owns `scripts/brazil-law/batch13/` and `corpus.d/99-batch13<x>.json` (+ `.PUBLISH`), one small part per 2-4 acts. Never
commits or pushes. Scratch outside the repo: `~/Documents/.gitlaw-scratch/brazil-b13` (trial parts, page
texts), merged build `brazil-b13-src` / `-build` / `-c`.

## How to run (per part x)
- Acts in parse_batch13.ALL_ACTS / PARTS[x]; pages in PAGES; act days ACT_DAY_ALL; laws ACT_LAWS_ALL; hand tables below.
- Fetch (one process, BelowNormal): `python -X utf8 batch13/.tmp/run.py <log> scripts/brazil-law/batch13/fetch_batch13.py pages|laws|missing`
  (BATCH13_ACTS=<slugs> limits laws/missing; pins in batch13/sources_batch13.json; Common Crawl -> Arquivo.pt -> archive.org).
- Parse: `BATCH13_PART=x BATCH13_OUT=<scratch>/x-run1.json ... parse_batch13.py [--stats]` twice, sha256 equal.
- Checks: batch10/.tmp/dupline.py, batch7/.tmp/dupcheck.py, batch7/.tmp/leakcheck.py, batch10/.tmp/firstline.py; quoted-
  article / rubrica decisions in the part.
- Docs: batch13/.tmp/docs.py batch13/.tmp/rows-x.json <candidate part> (README rows + jurisdiction.json counts).
- Merged build: batch13/.tmp/run.py <log> scripts/brazil-law/batch13/.tmp/runbuild.py <scratch>/99-batch13x.json
  (build, check.py, --compare, audit_push main/futuro). Then copy the part into corpus.d and write its .PUBLISH.
- Tools: .tmp/pagetxt.py <page id> (cached page text, struck as [[S: :S]]), cons.py, dump.py.

## 99-batch13a - PUBLISHed 2026-10-31
Lei das Contravenções Penais (DL 3.688/1941) 14 versions 1942-2024; Lei 1.079/1950 (crimes de responsabilidade) 3
(1950-05-27: no vigência clause -> LINDB 45 days; LC 227/2026 arts. 79-A/B); Lei 7.716/1989 7 (to Lei 14.532/2023). 0
diffs (Lei 7.716 vs compilado; others vs unstruck text). Hand: VIGENCIA_FIXED DL 6.916/1944 (on publication, its own
words); P.NOTE_FIX cleared (batch 12's were printed in decisions). Open items (decisions): Vide ADPF 1259/1260 (Lei
1.079), Vide ADO 26 (Lei 7.716). Part sha dbe2c636; merged 79 acts, 1805 versions, 1578 commits, check 0/0, compare
identical, audit clean.

## 99-batch13b - PUBLISHed 2026-10-31
Lei de Greve 7.783/1989 (7 versions, 1989-2020), LC 150/2015 domésticos (2, to Lei 15.455/2026), Lei 6.019/1974 (3, 1974-
2017). Hand: MP_LAPSE mp-883-2019 (19.9.2019, Ato Declaratório 58/2019 pinned ato:adc-58-2019-mpv883); SPAN_FIX LG art. 10 X
(1989 / MP 866 / MP 883 gap / Lei 13.903). Dup flags only LC 150 art. 37 quoted §§. Part sha 773c98e0; merged 82 acts,
1817 versions, 1587 commits, check 0/0, compare identical, audit clean.
