# Brazil batch 17 progress (gitlaw-BR agent, 2026-10-31)

Owns `scripts/brazil-law/batch17/` and `corpus.d/99-batch17<x>.json` (+ `.PUBLISH`), one small part per 2-4 acts. Never
commits or pushes. Scratch outside the repo: `~/Documents/.gitlaw-scratch/brazil-b17` (trial parts, page
texts, `eff/` = parts after effects_fix), merged build `brazil-b17-src` / `-build` / `-c`.

## How to rerun (per part x) - same pipeline as batch 16
    BATCH17_PART=x BATCH17_OUT=<scratch>/x-run1.json python batch17/.tmp/run.py <log> scripts/brazil-law/batch17/parse_batch17.py --stats
    (twice, sha256 equal), copy to <scratch>/eff/99-batch17x.json, then
    python batch17/.tmp/run.py <log> scripts/brazil-law/effects_fix.py <scratch>/eff/99-batch17x.json
    python batch17/.tmp/run.py <log> scripts/brazil-law/batch17/.tmp/runbuild.py <eff>/99-batch17a.json ...
- Run from the lexifina root. run.py waits until cpu5 <= 90 in %LOCALAPPDATA%/gitlaw-cpu.log, runs at BelowNormal, prints
  the PID (all runs so far foreground, one at a time; every PID exited).
- parse_batch17.py imports batch16 (BATCH16_PART='-', which brings 15/14/13/... and the MP 905/955 model) and adds its
  acts, pages (into the shared PAGES dict), ACT_DAY/ACT_LAWS, hand tables. Pins: batch17/sources_batch17.json.
- Fetch: `fetch_batch17.py pages`, then `laws`, then `missing` (BATCH17_ACTS limits; all through run.py).
- Checks per part: batch10/.tmp/dupline.py, batch7/.tmp/dupcheck.py, batch7/.tmp/leakcheck.py, batch10/.tmp/firstline.py,
  batch14/.tmp/pubgap.py, .tmp/ordercheck.py, .tmp/missorig.py, .tmp/overlap.py <x> (SAME lines), .tmp/headyear.py,
  .tmp/quotecheck.py (new: lines with quotation marks or '(NR)', and article-number gaps > 20).
- Tools (.tmp/, copied from batch16 with names changed): spans.py, udiff.py, lawtxt.py, region.py, cons.py, convs.py,
  effrep.py, latecaput.py.
- Docs: `python -X utf8 batch14/.tmp/docs.py batch17/.tmp/rows-x.json` (README row + jurisdiction.json counts).

## 99-batch17a - PUBLISHed 2026-10-31 ~17:20 local
Lei do Trabalho Rural 5.889/1973 (10 versions), Lei 4.090/1962 13º salário (2), Lei 605/1949 repouso semanal (12), Lei do
Vale-Transporte 7.418/1985 (5) = 29 versions.
- CONVERTED_FIX mp-410-2007 -> lei-11718-2008 (page 'Lei n 1 1.718'); MP_PENDING mp-2164-2001 (text rewritten without the
  FGTS wording batch 16 gave it), mp-2165-2001.
- Lei 7.418: renum_articles() (apply_rewrites wrapper): Lei 7.619/1987 renumbered arts. 3-13 -> 2-12 and changed no other
  words (read on its page); copies of every line in force on 1.10.1987 under the old unit art-(N+1) from 17.12.1985.
- Lei 605: paragraphs wrapper drops MP 905's own headings 'Descanso semanal' / 'Harmonização de multas trabalhistas
  constantes de legislações esparsas' (printed on the page, no note; read on MP 905's page).
- effects_fix MOVES "99-batch17a.json": Lei 9.532/1997 art. 82 II f) -> Lei 7.418 art. 3 repealed from 1.1.1998.
- Part sha 98ec82cb (pre-effects 6856b19d); merged 130 acts, 2423 versions, 1957 commits, check 0/0, compare identical,
  audit clean. README rows + jurisdiction.json (130 acts).
- Open (not modelled): 'Vide' pointers (Lei 5.889: MPs 927/2020, 1.046/2021, 1.109/2022, Lei 14.437/2022).

## 99-batch17b - PUBLISHed 2026-10-31 ~17:45 local
Lei 9.029/1995 (3 versions), Lei do Software 9.609/1998 (1), Lei das Organizações Sociais 9.637/1998 (4), Lei das OSCIPs
9.790/1999 (6) = 14 versions.
- MP_LAPSE mp-850-2018 = 12.2.2019 (Chamber rejected it in preliminary review, Ato of 13.2.2019 pinned
  ato:acd-2019-mpv850; also pinned ato:adc-66-2018-mpv850, the 60-day extension) + B5.MP_REJECTED label (batch 12 MP 446
  model). MP_PENDING mp-2216-2001 text made generic for Lei 9.790 (batch 16's FGTS text is not used by 17a/17b).
- OPEN_ITEMS LOS (Anexos I-II, MP 479 credit), LOSCIP (MP 2.123-29 chain, Vide Lei 13.800).
- effects_fix: 0 moves. Part sha 1be8ad89 (pre-effects c99b8025); merged 134 acts, 2437 versions, 1966 commits, check
  0/0, compare identical, audit clean. README rows + jurisdiction.json (134 acts).
- Reproducibility: a fresh parse of 17a now differs from the installed part only in sources[0].requests (60 -> 64: the
  count covers the whole growing pin file; batch 13/16 precedent, left as published).

## 99-batch17c - PUBLISHed 2026-10-31 ~18:10 local
Lei 1.060/1950 assistência judiciária (12 versions, vs l1060compilada.htm), Lei 9.492/1997 protesto (6), Lei 6.024/1974
intervenção/liquidação (4), Lei 12.037/2009 identificação criminal (8) = 30 versions.
- MP_PENDING mp-1894-1999 (reissue chain; ended by Lei 9.841, LINDB 20.11.1999).
- SPAN_FIX Lei 6.024 art. 19 a)-d) second copies start 20.10.2017 (MP 784 lapse; overlap.py found them dated from 1974).
- note_laws wrapper adds mp-955-2020 where a page cites MP 905 only (Lei 12.037); mp955_two_copies() (apply_rewrites):
  struck copy to MP 955's lapse 18.8.2020, unstruck copy from 19.8.2020 (MP955_ACTS = {Lei 12.037}).
- Lei 1.060 art. 15 order flag: 1950 text (items as §§ 1º-5º before a Parágrafo único), as on the compilada page.
- effects_fix: 0 moves. Part sha bd72860b (pre-effects a6ad2d21); merged 138 acts, 2467 versions, 1982 commits, check
  0/0, compare identical, audit clean. README rows + jurisdiction.json (138 acts).

## 99-batch17d - PUBLISHed 2026-10-31 ~18:35 local
Lei de Biossegurança 11.105/2005 (2), Lei do Planejamento Familiar 9.263/1996 (4), Lei 11.419/2006 processo eletrônico (3)
= 9 versions.
- VETO_KEPT (veto_kept() in apply_rewrites): Lei 9.263 arts. 10, 11, 15 + art. 14 p.u. from 20.8.1997 (Mensagem 928/1997
  pinned as ato:mv-928-1997, DOU 20.8.1997).
- paragraphs wrapper: l11105 quoted '"ANEXO VIII' heading -> line of art. 37; empty heading dropped.
- Part sha 979f692c (effects_fix 0 moves); merged 141 acts, 2476 versions, 1989 commits, check 0/0, compare identical,
  audit clean. README rows + jurisdiction.json (141 acts).

## 99-batch17e - PUBLISHed 2026-10-31 ~18:55 local
Lei da Mobilidade Urbana 12.587/2012, 13 versions 2012-04-13 .. 2025-11-27 (in force 13.4.2012, 100 days).
- MP_LAPSE mp-748-2016 = 23.3.2017 (ato:adc-20-2017-mpv748 pinned). SPAN_FIX art. 24: § 5º (MP 748) ends at the lapse;
  § 3º MP 818 wording ends 20.6.2018 (Lei 13.683 conversion dropped it); Lei 13.406's § 3º second copy 20.6.2018-20.11.2019
  (MP 906); '§ 3º (Revogado).' from Lei 14.000 (20.5.2020) - judgement call: absent 20.11.2019-20.5.2020.
- OPEN_ITEMS: Vide MP 1.179/2023, Lei 15.432/2026. effects_fix 0 moves. Part sha 5d79c481; merged 142 acts, 2489
  versions, 1999 commits, check 0/0, compare identical, audit clean. README row + jurisdiction.json (142 acts).

## 99-batch17f - PUBLISHed 2026-10-31 (second session)
Lei da Faixa de Fronteira 6.634/1979 (5 versions), Lei 9.469/1997 (8, vs l9469compilado.htm), Lei de Segurança do Tráfego
Aquaviário 9.537/1997 (3; in force 10.6.1998, 180 days) = 16 versions.
- VIGENCIA_PROVISION lei-14004-2020 x Lei 6.634 art-04/art-08-a = 8.9.2020 (vetoed art. 1 promulgated after the override,
  DOU 8.9.2020 extra, read on Lei 14.004's page) + EXTRA decision (only when part f's acts run).
- MP_PENDING mp-2226-2001 (new); mp-2216-2001 text for Lei 6.634 art. 9 § 1º set ONLY when PART == "f" (part b keeps its
  Lei 9.790 text). The base parser already handles Lei 9.469 art. 6 Parágrafo único -> § 1º (MP 2.226 renumbering).
- OPEN_ITEMS L9469 (Vide ADIN 2.527-9: the STF suspension of MP 2.226 art. 3 is NOT modelled; portal.stf.jus.br robots.txt
  now Disallows /processos, so no STF pages may be read; MP 1.561 chain), LESTA (regulations).
- effects_fix 0 moves. Part sha fabe98f0 (pre-effects b6af9804); merged 145 acts, 2505 versions, 2008 commits, check 0/0,
  compare identical, audit clean. README rows + jurisdiction.json (145 acts).
- New: .tmp/pipe.sh <part> runs the whole per-part pipeline (2 parses, sha, effects_fix, every check, merged build).

## 99-batch17g - PUBLISHed 2026-10-31 (second session)
Lei do Susp 13.675/2018 (8 versions; in force 12.7.2018), Lei do Mercado de Capitais 4.728/1965 (16, vs l4728compilado.htm)
= 24 versions.
- PROMULGATED (promulgated() in apply_rewrites, per line: unit, label, text prefix, day, law): Lei 14.531 art. 2's vetoed
  art. 9 § 2º XVII and art. 42-A § 7º from 19.7.2023 (DOU of the promulgation). Lei 14.751's promulgated parts do not touch
  Lei 13.675 (read). EXPLAINED LSUSP art-47; OPEN_ITEMS LSUSP (ADPF 995).
- Lei 4.728 (all set only when its act runs, because NOTE_FIX/VIGENCIA_FIXED text lands in every part's decisions):
  NOTE_FIX 'Del 1.338' x2, 'Decreto nº 911', 'Decreto nº 2.287' (links checked: Decretos-Leis); VIGENCIA_FIXED dl-614-1969
  6.6.1969 and dl-911-1969 3.10.1969 (reader missed both clauses and fell back to LINDB). law:dl-911-1969 pinned (gaps.py,
  path decreto-lei/1965-1988/del0911.htm). MP_PENDING mp-2160-2001. EXPLAINED art-29, art-80. OPEN_ITEMS (Vide pointers).
- LexML: DL 1.338/1974 (footer 23.8.1974 -> 23.7.1974) and Lei 5.589/1970 (footer prints 1966 -> 6.7.1970) fetched by
  .tmp/lexml1.py (one request per 6 s; parse_proc's PUB_CORRECTED then applies them).
- effects_fix MOVES "99-batch17g.json": Lei 14.754/2023 (art. 47 II, effects 1.1.2024) -> Lei 4.728 arts. 49-50: 2 moves.
- Part sha 7cf8eca0 (pre-effects 31f78f16); merged 147 acts, 2529 versions, 2025 commits, check 0/0, compare identical,
  audit clean. README rows + jurisdiction.json (147 acts).

## 99-batch17h - PUBLISHed 2026-10-31 (second session)
Lei 7.689/1988 CSLL (18 versions, 1988-12-16 .. 2027-01-01 on futuro), Lei 9.249/1995 (17, 1996-01-01 .. 2030-01-01 on
futuro) = 35 versions. Coordinator confirmed: Lei 9.249 dated by its effects clause (ACT_DAY 1.1.1996).
- Scoped to part h's acts: VIGENCIA_FIXED mp-675-2015 1.9.2015, mp-1034-2021 1.7.2021 (art. 5 II), mp-694-2015 1.1.2016
  (art. 4 I). MP_LAPSE mp-694-2015 9.3.2016 (ato:adc-5-2016-mpv694 pinned from CC). LexML: Lei 8.034/1990 -> 13.4.1990.
- BARE_TEXT (paragraphs wrapper): 'com a redação dada pelo Decreto-Lei nº ...' kept as text in l7689 art-11, l9249 art-14
  (the reader had cut the sentence at 'com a' and credited DL 2.449 / DL 1.730 on the first day).
- l9249 art-09: opening quote before MP 694's caput dropped and label set (wrapper; B15.TEXT_FIX is a plain substring and
  does not relabel); SPAN_FIX nth=2 restores the 1995 caput from 9.3.2016.
- effects_fix MOVES "99-batch17h.json": 14 moves (see PUBLISH). Kept in-force day: Lei 9.430 (financial effects), Lei
  11.727 art. 17 / 13.169 / 14.446 (retroactive to the MP's day).
- OPEN_ITEMS: Lei 7.689 art. 8 LEFT OUT: struck '(Execução suspensa pela RSF nº 11, de 1995)'; every crawl of Planalto's
  RSF page is a 404, Arquivo.pt has no Chamber legin copy, so the suspension cannot be dated (the parser skips it). L9249:
  Lei 9.430 financial effects, Vide pointers.
- Benign check flags: dupline 'label II-B/II-C' (Lei 7.689 art. 3 on 1.4.2026; text read, correct), leakcheck '(revogado)'.
- Part sha 61170d5e (pre-effects 621d32ca); merged 149 acts, 2564 versions, 2048 commits, check 0/0, compare identical,
  audit clean. README rows + jurisdiction.json (149 acts).
- New tools: .tmp/lexml1.py (one LexML record per 6 s), .tmp/ptlist.py (Arquivo.pt prefix list).

## Third session (2026-10-31 evening): ROBOTS FINDING - read before fetching
robots.txt read 18:1x: data.commoncrawl.org 'User-Agent: * / Disallow: /' and arquivo.pt 'Disallow: /wayback' (the
path wayback.pt_get/pt_captures use; also Crawl-delay 5). So from this session on NO Common Crawl data requests and NO
Arquivo.pt requests. web.archive.org serves no robots.txt (404): allowed. LexML: /urn and /sru allowed, Crawl-delay 5,
/busca/ /doc/ /linker/ Disallowed. Use `.tmp/iaonly.py <fetch_batch17 command>` (pages|laws|missing|gap id url): the same
commands with Common Crawl and Arquivo.pt pins switched off (archive.org only); the local Common Crawl path index file
(.cache/cc/planalto-ccivil03-cc-index.jsonl) is still read from disk to find candidate paths (no request).

## 99-batch17i - PUBLISHed 2026-10-31 (third session)
Lei 9.250/1995 (IRPF), 35 versions 1995-12-27 .. 2026-01-01 (in force on publication, art. 41).
- VIGENCIA_FIXED lei-12213-2010 1.1.2011 (art. 5), lei-13498-2017 1.1.2018 (art. 2); MP_LAPSE mp-644-2014 30.8.2014
  (ato:adc-35-2014-mpv644, lowercase http URL variant), mp-1171-2023 28.8.2023 (ato:adc-62-2023-mpv1171); MP_PENDING
  mp-2189-2001.
- SPAN_FIX art-04 (p.u. I/II of Lei 13.202 end 1.5.2023, no return: Lei 14.663 numbered the p.u. as § 1º on 28.8.2023, the
  lapse day; MP 1.171's struck unnoted § 2º 1.5-28.8.2023), art-08 item 9 (MP 670 unstruck copy, label ''), art-22 (1995
  caput back 14.10-22.11.2005 via gaps; gaps are 4-tuples (start, end, start_law, end_law)).
- paragraphs wrapper l9250: 'Sem eficácia' marker stripped, empty struck 'a)'-'d)' (Vide MP 340) dropped, Lei 15.270 table
  titles moved from titulos into arts. 3-A/11-A, chapter-name lines take the CAPÍTULO line's note. EXPLAINED art-04, art-03-a,
  art-11-a, titulos.
- effects_fix MOVES "99-batch17i.json": 5 entries, 17 unit-moves (9.532 -> 1.1.1998, MP 528 -> 1.4.2011, Lei 13.043 art. 84
  -> 1.1.2015 (in-force clause, Seção XXI), 14.754 -> 1.1.2024, 15.270 -> 1.1.2026).
- Part sha f7bbf441 (pre-effects a99dbc22); merged 150 acts, 2599 versions, 2071 commits, check 0/0, compare identical,
  audit clean. README row + jurisdiction.json (150 acts).

- Re-PUBLISHed (same session) with decision wording only: empty struck 'Vide MP 340' items now one shared decision
  (EMPTY_ITEM_PAGES; art. 4 and art. 10); sha eea6e50f.

## 99-batch17j - PUBLISHed 2026-10-31 (third session)
Lei 7.713/1988 (IR), 43 versions 1989-01-01 .. 2024-12-06 (in force 1.1.1989, art. 57; DOU 23.12.1988 from LexML).
- VIGENCIA_FIXED lei-11052-2004 1.1.2005, lei-7975-1989 1.3.1990 (DOU 27.12.1989 from LexML), mp-582-2012 1.1.2013 (art. 20
  II), lei-12794-2013 3.4.2013 (retroactive start kept on publication); MP_LAPSE mp-1251-2024 6.12.2024
  (ato:adc-125-2024-mpv1251); mp-644-2014 lapse now set for 9.250 or 7.713; NOTE_FIX 'Lei nº 7.759' -> 7.959; TEXT_FIX art. 7
  ')'; EXPLAINED art-30. law:lei-7959-1989 pin = L7959.htm (was pinned under the misprinted key).
- effects_fix MOVES "99-batch17j.json": 7 entries, 20 moves; MP 114 art-14/art-45 hunks None + Lei 7.959 same units ->
  1.1.1990 (moves chain: apply_move recomputes from the already-moved versions); path_sel must be wrapped in a lambda in
  MOVES (defined later in the file) and takes 4-tuples (unit, par, inc, ali).
- Part sha 8b41fb85 (pre-effects 6a70a200); merged 151 acts, 2642 versions, 2101 commits, check 0/0, compare identical,
  audit clean. README row + jurisdiction.json (151 acts).

## 99-batch17k - PUBLISHed 2026-10-31 (fourth session)
Lei 9.430/1996, 69 versions 1996-12-30 .. 2026-01-14 (+ 2030-01-01 on futuro). In force 30.12.1996 (art. 87 financial effects).
- l9430 RE-PINNED (archive.org, ts 20261020175558; the old CC pin 20260910 predates Lei 15.525/2026's art. 2 § 5º, which the
  compilada has). Old pin file kept at <scratch>/k/sources_batch17.before-k.json.
- Hand (part k block, scoped to the act): MP_PENDING mp-2158-2001; VIGENCIA_FIXED lei-14596-2023 = 1.1.2024 (art. 47);
  VIGENCIA_PROVISION: Lei 12.715 (art. 78 § 1º) arts 12/18/18-A/19/19-A/22 and Lei 12.766 (art. 13 II) art 22 -> 1.1.2013;
  Lei 11.727 (art. 41 VI) arts 24/24-A/24-B and MP 449 art 24-A -> 1.1.2009; MP 1.602 (art. 72 II) and Lei 9.532 (art. 81
  II) arts 44/47 -> 1.1.1998 (MP lines skipped: never in effect). SPAN_FIX (module level, keyed to the act): art-70 § 2º (MP
  252 never in effect; 11.196 from 1.1.2006), art-19-a/19-b (MP 478 lines noted only 'Vide'), art-22 (12.715 caput/§ 5º
  never), art-63 § 3º (MP 75), art-44/45/46 and art-18 II alíneas (Planalto's second copies = restored text or duplicates),
  art-09 § 7º II a), art-24-a 11.727 p.u. (never). heads_14596() in apply_rewrites: headings of arts 18-22 end with Lei
  14.596. paragraphs wrapper l9430: '(Sem eficácia)' and 'Rejeitada' markers stripped; BARE_TEXT art-88 (regex widened to
  'pel[oa] (Decreto-Lei|Lei)'; parts h/j re-parsed: equal except sources[0].requests, known).
- EXPLAINED art-74, art-88, titulos; OPEN_ITEMS L9430.
- effects_fix MOVES "99-batch17k.json": 6 entries, 8 moves (MP 2.013-4, MP 66 art-74, MP 478, MP 517, Lei 15.265 art-17,
  Lei 15.525 -> 2030). Amenders read with effrep (scratch k/effrep.txt): the rest are in force on publication for 9.430 or
  retroactive (9.959, 10.637 art. 49, 12.249) - kept.
- Part sha b55b1083 (pre-effects 2b1a7d53); merged 152 acts, 2711 versions, 2136 commits, check 0/0, compare identical,
  audit clean. README row + jurisdiction.json (152 acts). Checks: dupline 3 / overlap 2 SAME = art. 9 § 1º vs § 7º (same
  incisos, correct); leakcheck only literal '(revogado)'.
- New tool .tmp/cdxlist.py <planalto path>...: archive.org CDX listing (timestamps, lengths).

## State at handoff (batch 17, fourth session, 2026-10-31)
Parts 99-batch17a..k installed with .PUBLISH (26 acts, 317 versions; merged 152 acts, 2711 versions, 2136 commits, check
0/0, --compare identical, audit clean). README rows + jurisdiction.json (152 acts) current. All runs foreground through
.tmp/run.py at BelowNormal; every PID exited; nothing left running. Fetching: archive.org only (iaonly.py); Arquivo.pt is
user-approved (BRIEF) but not needed so far; no Common Crawl requests.
Next: Leis 13.465/2017 and 11.977/2009 (pages not yet pinned: `iaonly.py gap <id> <url>`; .tmp/cdxlist.py lists captures).

## State at handoff (batch 17, third session, 2026-10-31)
Parts 99-batch17a..j installed with .PUBLISH (25 acts, 248 versions; merged 151 acts, 2642 versions, 2101 commits, check
0/0, --compare identical, audit clean). README rows + jurisdiction.json (151 acts) current. Fresh parses + effects_fix of i
and j equal the installed parts in every key (after the part k config was added). effects_fix.py MOVES added for
99-batch17i and j. All runs foreground through .tmp/run.py at BelowNormal; every PID exited; nothing left running.
Fetching: archive.org only (iaonly.py) and one LexML /urn record per run (lexml1.py, 6 s apart); see the ROBOTS FINDING.
Next: finish part k (above), then Leis 13.465/2017 and 11.977/2009 (pages not yet pinned: pin via iaonly.py gap; the local
CC path index lists candidate paths).

## State at handoff (batch 17, second session, 2026-10-31)
Parts 99-batch17a..h installed with .PUBLISH (23 acts, 170 versions; merged 149 acts, 2564 versions, 2048 commits, check
0/0, --compare identical, audit clean). README rows + jurisdiction.json (149 acts) current. effects_fix.py MOVES for
99-batch17a, g, h. Fresh parses of b, e, f after this session's edits equal the installed parts except
sources[0].requests (known). No background processes left running (all runs foreground via .tmp/run.py; PIDs exited).
Robots: read a host's robots.txt before the first request to it (coordinator). portal.stf.jus.br Disallows /processos.

## Next (tax laws, configured pages only)
Pages pinned for Lei 9.250 (+compilado), 7.713 (+compilada), 9.430 (+compilada): PAGES entries exist, acts not configured.
Sizes: 9.250 293 notes / 192 struck runs; 7.713 328/314; 9.430 547/608. Expect the same work as part h: each MP's and
law's own vigência/efeitos clause (effrep.py <act number> <law keys>), MP lapses (Atos Declaratórios: search the CC index
for 'congresso/adc-NNN-mpvNNN'), Senate resolutions, bare 'com a redação dada' tails (BARE_TEXT), then MOVES. Lei 9.250
first (smallest; Lei 15.270/2025 changes from 1.1.2026). Then Leis 13.465/2017 and 11.977/2009 (+compilado; CC index).

## Next candidates (pages in the Common Crawl index)
Lei 13.675/2018, Lei 9.537/1997, Lei 6.634/1979, Lei 9.469/1997 (+compilado), Lei 4.728/1965 (+compilado);
heavy tax laws Lei 7.713/1988 (+compilada), 9.430/1996 (+compilada), 9.249/1995, 9.250/1995, 7.689/1988; Lei 13.465/2017,
Lei 11.977/2009. Lei 10.931/2004: no page in the index.
