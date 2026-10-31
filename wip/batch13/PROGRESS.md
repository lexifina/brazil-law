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

## 99-batch13c - PUBLISHed 2026-10-31
Lei 4.591/1964 (16 versions), Lei 9.514/1997 (17), DL 911/1969 (6; page decreto-lei/1965-1988/del0911.htm). Hand:
MP_PENDING mp-2221-2001 (revoked by Lei 10.931); VIGENCIA_FIXED mp-656-2014 = 8.10.2014 (FIXED_DAY fallback had taken
1.1.2015 from art. 55 I); SPAN_FIX DL 911 art. 5 p.u. ends 4.7.1974; EXPLAINED LCI art-33, DL911 preambulo/titulos.
VIG_AUDIT run on parts a, b, c: no fallback uses. Part sha bec3bdce; merged 85 acts, 1856 versions, 1600 commits, check
0/0, compare identical, audit clean.
Note: a fresh parse of 13a/13b now differs from the installed parts only in sources[0].requests (the count covers the
whole growing pin file sources_batch13.json); left as published, as batch 10 did for 97/99-batch6.

## 99-batch13d - PUBLISHed 2026-10-31
Lei das Estatais 13.303/2016 (2 versions), Lei dos Partidos Políticos 9.096/1995 (18). LPP art. 44 §§ 5º-A/7º struck for ADI
5.617 undated -> left out, EXPLAINED + open item. Part sha 92160155; merged 87 acts, 1876 versions, 1609 commits, check
0/0, compare identical, audit clean.

## Deferred: Lei 4.320/1964 (configured as lei-4320-de-1964, pinned, not in any part)
Trial (d1.json): 16 diffs vs l4320compilado. Needs: '(Veto rejeitado no DOU, de 5.5.1964)' / '(Veto rejeitado no D.O.
05/05/1964)' read as notes (they leak into the text now); arts. 109-113 missing from the replay ('Artigo 113.' style
labels?); 19 'undated' struck lines; typesetting diffs (art. 33, 49, 57, 68, 98). In-force day set: 7.5.1964 (LINDB; the
vetoed parts kept by Congress were promulgated DOU 5.5.1964, before it); art. 114 (effects) noted.

## 99-batch13e - PUBLISHed 2026-10-31
Lei de Migração 13.445/2017 (1 version, from 21.11.2017; annex fee table NOT included - open item), Lei 9.474/1997 (1),
Lei 13.260/2016 (1), Lei 7.960/1989 (3). Part sha fdd59324; merged 91 acts, 1882 versions, 1613 commits, check 0/0,
compare identical, audit clean.
