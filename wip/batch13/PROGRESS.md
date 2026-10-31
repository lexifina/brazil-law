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

## 99-batch13f - PUBLISHed 2026-10-31
Lei 4.595/1964 SFN (27 versions), Lei do Cheque 7.357/1985 (1). Hand: NOTE_FIX 'Del nº' notes (7); law:dl-581-1969 repinned
(missing had pinned DL 581/1938!) to decreto-lei/del0581.htm + VIGENCIA_FIXED 21.5.1969; WORD_FIX art. 56 'Vide Lei
6.419'; SPAN_FIX art. 10 IV renumbered copy skip, art. 42 quoted lines gap for MP 784; EXPLAINED arts. 4, 5, 10, 19.
New tool batch13/.tmp/headyear.py: checks each law pin's first heading number AND year (pinscan checks number only);
remaining flag law:lei-5143-1965 (page is Lei 5.143/1966; used only in a 'Vide' note, harmless).
Part sha 3964e97f; merged 93 acts, 1910 versions, 1637 commits, check 0/0, compare identical, audit clean.

## Deferred: Lei do FGTS 8.036/1990 (configured lei-do-fgts, page leis/l8036consol.htm - l8036.htm is the ORIGINAL text)
Trial: 140 problems (Lei 13.932/2019 note 'Incluído dada pela', MP 905/2019 -> MP 955/2020 revocation chain, many
'restored wording after an open one', 60 undated). Needs a hand model like the Saneamento one.

## 99-batch13g - PUBLISHed 2026-10-31
Lei das Duplicatas 5.474/1968 (6), Lei dos Cartórios 8.935/1994 (12), Lei Orgânica do TCU 8.443/1992 (5), Lei 10.259/2001
JEF (3). Hand: VIGENCIA_FIXED lei-14206-2021; SPAN_FIX LDup arts. 15-18 end at Lei 6.458/1977 (DL 436 kept art. 15 §§
1-11); law:lei-14301-2022 repinned; P.COURTS rsf-16-2006 + batch5b SPLIT_NOTES (TCU art. 55 § 1º expression);
paragraphs wrapper upper-cases the TCU heading ('Lei Nº' missed the start-of-act test: 0 paragraphs before);
EXPLAINED LDup preambulo/titulos. Part sha fcaf9391; merged 97 acts, 1936 versions, 1653 commits, check 0/0, compare
identical, audit clean.

## 99-batch13h - PUBLISHed 2026-10-31
Lei 12.153/2009 JEFP (1, from 24.6.2010), Lei 8.038/1990 (6), Lei de Alimentos 5.478/1968 (3), PNRS 12.305/2010 (3). Hand:
paragraphs wrapper moves LAlim 'art-921' (quoted CPC 1939 article, no quote marks) into art-19 + SPAN_FIX (end Lei
6.014/1973); SPAN_FIX PNRS art. 19 XIX 2010 wording ends 16.7.2020 (page leaves it unstruck) + EXPLAINED. Part sha
89e2c9ab; merged 101 acts, 1949 versions, 1659 commits, check 0/0, compare identical, audit clean.

## State at handoff (2026-10-31)
Parts 99-batch13a..h installed with .PUBLISH (24 acts, 168 versions; merged 101 acts, 1949 versions). README rows +
jurisdiction.json (101 acts) current. No background processes left running.
Deferred, configured in ALL_ACTS: Lei 4.320/1964 (lei-4320-de-1964) and Lei do FGTS 8.036/1990 (lei-do-fgts); reasons
above. Next candidates (not configured): LC 87/1996, LC 116/2003 (watch LC 214/2025's 2033 repeal -> futuro), Lei 8.213 and
8.212/1991 (heavy MP chains), Lei 9.472/1997 (LGT), Lei 9.433/1997, Lei 9.985/2000 (SNUC), Lei 13.874/2019, LC 123/2006,
Lei 4.504/1964 (Estatuto da Terra), Lei 7.565/1986 (CBA), Lei 12.288/2010, Lei 1.521/1951, DL 201/1967.
Check per part also: batch13/.tmp/headyear.py (pins' heading number + year) - it caught DL 581/1938 pinned for DL 581/1969
and a Lei 14.301 link pointing at another act's page.
