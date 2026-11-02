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

## 99-batch17l - PUBLISHed 2026-10-31 (fourth session)
Lei 13.465/2017 (REURB), 8 versions 2017-07-12 .. 2023-12-20. Page l13465.htm pinned (archive.org ts 20261022110427); no
compilado page exists (the act's own page is its consolidated page; 4 check artefacts EXPLAINED: dotted quoted '§ 1º.').
- paragraphs wrapper l13465: '(Partes vetadas)' link stripped; quoted Lei 11.952 art. 16 (no opening quote, inside art. 4)
  moved from unit art-16 back into art-04 (only before art-05 is seen).
- SPAN_FIX: promulgated vetoed parts (President, 6.9.2017, DOU 8.9.2017; text at the foot of the page) start 8.9.2017
  credited to lei-13465-2017: art-03 quoted Lei 13.001 art. 3 caput + its dotted closing line (nth 0), art-03-a (all 2017
  lines), art-04 quoted § 2º 'Caso a análise'; art-33 § 1º II/III third (unnoted) copy starts with Lei 14.118 (13.1.2021).
- Amenders all in force on publication (effrep read): 0 effect moves. OPEN_ITEMS: MP 759/2016 text, rectification 6.9.2017.
- Benign checks: dupline 108 / dupcheck 9 / leakcheck / overlap 3 SAME = quoted text of the amending articles (arts. 2, 4,
  55, 67, 81, 91-93 ...). Part sha 0eb43315; merged 153 acts, 2719 versions, 2138 commits, check 0/0, compare identical,
  audit clean. README row + jurisdiction.json (153 acts).

## 99-batch17m - PUBLISHed 2026-10-31 (fifth session)
Lei 11.977/2009 (Minha Casa, Minha Vida), 39 versions 2009-07-08 .. 2026-08-01 (l11977.htm vs l11977compilado.htm; 2 diffs
EXPLAINED: titulos 'CAPÍTULO III', art-12 p.u.). Fetch: `iaonly.py laws l11977 l11977-compilado` (15 new pins) + `missing`.
- Hand (part m block, scoped to the act): VIGENCIA_FIXED mp-472-2009 16.12.2009 (art. 60 I d), lei-13161-2015 31.8.2015 (art.
  7 II); MP_LAPSE mp-478-2009 2.6.2010; MP_PENDING mp-1382-2026 (1.8.2026, pending on 31.10.2026) and mp-1350-2026 (revoked
  by MP 1.382 art. 9 II; its only change, art. 20 IV, revoked the same day); NOTE_FIX 'Mediada Provisória nº 561' x2;
  VIGENCIA_PROVISION art-41: MP 656 7.11.2014, Lei 13.097 19.2.2015 (30 days, arts. 9-17 / 54-62).
- SPAN_FIX: art-79 2009 copy after MP 478 (nth 1/2) and art-11 p.u. 2nd copy restored 2.6.2010; art-13 I Lei 12.249 copy
  14.6-2.12.2010; art-04 II '(VETADO)' struck copy skipped; art-59 III '(revogado)' from 17.6.2011; art-63 '(VETADO)' ends
  23.12.2016; arts. 5, 12 (incl. the unstruck p.u.), 18 caput (nth 1) + § 2º, 19 caput end 31.12.2011 (MP 514 art. 9 IV / Lei
  12.424 art. 13 III); art-41 p.u. MP 656 to 19.2.2015. TEXT_FIX art. 47 §§ 1º/2º doubled labels.
- ch3_successors() (apply_rewrites): Capítulo III (arts. 46-71-A) revoked by MP 759 (23.12.2016); Planalto puts the
  revocation notes on every struck line, so 'note' ends that P.successor() finds earlier are moved back; MP 514 lines
  restated by Lei 12.424 (arts. 47 IX, 56, 59, 60-A, 71-A) and art. 59's 2009 lines end 17.6.2011; art. 60 § 1º I / § 2º keep
  MP 514's wording to 2016 (Lei 12.424 left them dotted; judgement call, as Planalto prints); lines noted only 'Revogado
  pela Lei 13.465' end 23.12.2016; children follow the parent's corrected end.
- Amenders read with effrep (scratch log .tmp/m-effrep.log): none has a later effect day for this act: effects_fix 0 moves.
- Part sha 8507788a (pre-effects 6c70a060); merged 154 acts, 2758 versions, 2158 commits, check 0/0, compare identical,
  audit clean. README row + jurisdiction.json (154 acts). Part l re-parsed after the edits: identical.
- New tools: .tmp/noteover.py <spans log> (struck lines outliving a later same-label line), .tmp/lawgrep.py <law> <regex>,
  .tmp/cdxpre.py <archive.org prefix> (CDX prefix listing). OPEN_ITEMS LMCMV (MP 459 text, MP 1.382 pending, Vide).

## 99-batch17n - PUBLISHed 2026-10-31 (fifth session)
Lei do Estágio 11.788/2008 (2 versions), Lei da Alienação Parental 12.318/2010 (2), Lei 10.048/2000 atendimento prioritário
(5), Lei dos Alimentos Gravídicos 11.804/2008 (1) = 10 versions. Pages pinned (`iaonly.py pages`, 4) + `laws`/`missing` (3).
No hand tables; 0 diffs, 0 problems, effects_fix 0 moves (amenders read: all on publication except Leis 10.741 (90 days)
and 13.146 (180 days), which the reader dates). Part sha 9b942bf0; merged 158 acts, 2768 versions, 2165 commits, check 0/0,
compare identical, audit clean. README rows + jurisdiction.json (158 acts).

## 99-batch17o - PUBLISHed 2026-10-31 (fifth session)
Lei dos Consórcios Públicos 11.107/2005 (4 versions), Lei da Acessibilidade 10.098/2000 (7) = 11 versions. No hand tables;
0 diffs, 0 problems, 0 moves (Leis 13.835 +180 days, 13.443 +90 days, 13.146 +180 days dated by the reader). Part sha
96021f87; merged 160 acts, 2779 versions, 2174 commits, check 0/0, compare identical, audit clean.

## 99-batch17p - PUBLISHed 2026-10-31 (fifth session)
Lei do ProUni 11.096/2005 (9 versions, vs l11096compilado), Lei de Cotas 12.711/2012 (4), Lei 13.431/2017 escuta protegida
(2; in force 5.4.2018, one year) = 15 versions.
- Lei 14.350/2022 art. 6 I: effects from 1.7.2022 for ProUni art. 2 I (+ alíneas a-e) and § 1º (+ I-VI), art. 7 II (+ a-c),
  §§ 1º, 1º-A, 2º (+ I-II): done as SPAN_FIX start/end 2022-07-01 in parse_batch17 (_WPU). An effects_fix MOVES entry was
  tried first: its hunk pairing left MP 1.075's § 3º incisos orphaned on 26.5.2022, so it was removed (effects_fix.py is back
  to its earlier content). MP 1.075's same clause: no printed wordings, nothing to move. Bare struck '§ 1º' (Vide) line in
  art. 2 skipped.
- Part sha 14c0577a (pre-effects c4f81fec); merged 163 acts, 2794 versions, 2183 commits, check 0/0, compare identical,
  audit clean. README rows + jurisdiction.json (163 acts).

## 99-batch17q - PUBLISHed 2026-10-31 (sixth session)
Lei 10.522/2002 (Cadin), 32 versions 2002-07-22 .. 2026-01-09 (l10522.htm vs l10522compilado.htm, 1 diff EXPLAINED art-20-b).
- Pages for all next candidates added to PAGES and pinned (`iaonly.py pages`; l9074 = leis/l9074cons.htm, no capture of
  leis/l9074.htm); `BATCH17_ACTS=lei-do-cadin iaonly.py laws` (7 new) + `missing` (0); ato:adc-41-2023-mpv1160 pinned (gap).
- Hand (part q block, scoped to the act): VIGENCIA_FIXED lei-12844-2013 19.7.2013 (art. 49 V), lei-13988-2020 14.4.2020 (II);
  MP_LAPSE mp-1160-2023 2.6.2023. SPAN_FIX: art-20-d '(VETADO' line text fixed, 10.1-18.4.2018, promulgated caput + I-III
  from 18.4.2018 (Lei 13.606 promulgation, as batch 15); art-11 §§ 1º-3º second (unstruck) copies restored 28.5.2009 (Lei
  11.941 kept only MP 449's caput); pointer lines art-10 'Vide Mpv 75' (nth 1) and art-13-a 'Vide MP 249' skipped.
  paragraphs wrapper: art. 37-B § 10 mixed line (struck dash only) read as plain (MIXED_PLAIN). B15.TEXT_FIX: 'Lei no'/'Decreto
  no' -> 'nº' (4), art. 20-D caput colon. New batch17 lifespans wrapper drops 'no end for struck' for SPAN_FIX-ended lines.
- LEFT OUT: art. 32 quoted § 2º (struck 'Vide Adin 1.976-7', undated; STF pages robots-closed) - in OPEN_ITEMS + README row.
- Amenders read with effrep: all on publication for this act; Lei 14.112 30 days (reader). effects_fix 0 moves.
- Benign: dupline 2 / overlap 2 SAME = art. 10-A V and VI a)/b) (identical in Lei 14.112). Part sha 63cfb9c7 (pre-effects
  d065fc1f); merged 164 acts, 2826 versions, 2192 commits, check 0/0, compare identical, audit clean. README row +
  jurisdiction.json (164 acts).
- Lei 10.931/2004: NO archive.org capture of _ato2004-2006/2004/lei/l10931.htm (cdxlist and cdxpre on the 2004 lei/ prefix:
  absent; the local CC index lists it, but Common Crawl is robots-closed). Not built; PAGES entry removed.

- 99-batch17q re-PUBLISHed (same session): + decision for the MIXED_PLAIN reading (added with part r's decision code); acts and
  laws identical; sha 1dd97069.

## 99-batch17r - PUBLISHed 2026-10-31 (sixth session)
Lei 9.873/1999 (5 versions 1999-11-24 .. 2017-11-14), Lei do Pregão 10.520/2002 (4 versions 2002-07-18 .. 2023-12-30) = 9.
- Lei 10.520: page id l10520-2023 = archive.org capture 20231210053808 (before the repeal), pinned with the new tool
  `.tmp/pinat.py <id> <url> <ts>` (pin at a chosen timestamp + refetch). B9.REPEALS entry (Lei 14.133 art. 193 II b,
  30.12.2023): last version removes every unit; REPEAL CHECK 0 differences.
- Lei 9.873: BARE_TEXT now takes a tuple of units (l9873 art-03, art-08; _BARE_RX9873 for art. 8's long tail); paragraphs
  wrapper drops the 'Congresso Nacional, em ...' closing line and splits art. 2º-A (printed '. Art. 2º-A.') with its
  incisos out of art. 2 (L9873_FIXED decision).
- MP 784/2017 and MP 896/2019 lapses from the shared tables. effects_fix 0 moves. All checks 0. Part sha 7f724c5f; merged
  166 acts, 2835 versions, 2194 commits, check 0/0, compare identical, audit clean. README rows + jurisdiction.json (166).

## 99-batch17s - PUBLISHed 2026-10-31 (sixth session)
Lei 12.783/2013 (concessões do setor elétrico), 16 versions 2013-01-14 .. 2025-11-25.
- Hand (part s block, `_LCSE`, scoped): VIGENCIA_FIXED lei-12844-2013 (V, now also set for this act) and mp-612-2013
  4.4.2013 (III; art. 22 retroactive, day kept); MP_LAPSE mp-612-2013 2.8.2013 (ato:adc-49-2013-mpv612) and mp-1232-2024
  11.10.2024 (ato:adc-101-2024-mpv1232); SPAN_FIX art-27 quoted lines get the MP 1.232 gap. EXPLAINED art-30 (_DOTTED).
- Benign: dupline/dupcheck art-30 quoted '§ 2º' x2; leakcheck art-23 quoted '(revogada)'. effects_fix 0 moves. Part sha
  b3ac0974 (pre-effects 36d2941a); merged 167 acts, 2851 versions, 2205 commits, check 0/0, compare identical, audit clean.

## 99-batch17t - PUBLISHed 2026-10-31 (sixth session)
Lei dos Portos 12.815/2013, 7 versions 2013-06-05 .. 2022-02-06. No hand dates; EXPLAINED art-71 (_DOTTED); flags all in
art. 71's quoted Lei 10.233 text. Part sha 37d58a62; merged 168 acts, 2858 versions, 2206 commits, check 0/0, compare
identical, audit clean. README rows + jurisdiction.json (168 acts).

## 99-batch17u - PUBLISHed 2026-10-31 (sixth session)
Lei 9.074/1995, 25 versions 1995-07-08 .. 2025-11-25 (l9074cons.htm vs l9074compilada.htm, 0 diffs).
- Pinned (gap): law:lei-11668-2008, law:lei-15235-2025. Hand (`_L9074`): VIGENCIA_FIXED mp-1300-2025 21.5.2025 (III) and
  lei-15235-2025 9.10.2025 (conversion that drops MP 1.300 art. 1: its 9.074 wordings end on publication); mp-612-2013
  settings now set for _LCSE or _L9074 (text differs per act so part s's decisions are unchanged: s reparse = installed except
  sources[0].requests). OPEN_ITEMS L9074. effects_fix 0 moves; all checks 0. Part sha 52d31eb8 (pre-effects 87993a50);
  merged 169 acts, 2883 versions, 2220 commits, check 0/0, compare identical, audit clean. README row + jurisdiction (169).

## 99-batch17v - PUBLISHed 2026-10-31 (sixth session)
Lei 12.462/2011 (RDC), 25 versions 2011-08-05 .. 2024-09-19 (l12462 vs l12462compilado; 4 diffs EXPLAINED).
- Hand (`_LRDC`, scoped): VIGENCIA_FIXED lei-14133-2021 = 30.12.2023 (all its notes on the page are the art. 193 II c
  revocation of arts. 1-47-A), mp-551-2011 = 10.1.2012 (effects I), lei-12688-2012 = 19.7.2012 (IV); NOTE_FIX 'Lei nº
  1.4002' -> 14.002; SPAN_FIX Lei 14.034 art. 13 effects 1.1.2021 (art. 63 § 5º caput/I/II start, 2012 § 5º end, Lei
  12.648's § 1º II copy nth 1 ends). paragraphs wrapper drops art. 63 § 17 on l12462 only (MP 1.349/2026 lapsed, Ato
  adc-77-mpv1.349 not on archive.org: cdxpre of 2026/congresso lists 16 Atos, not this one) -> LEFT OUT + decision +
  EXPLAINED art-63. OPEN: art. 63-B 5-year term (Lei 14.901 art. 5) not modelled; ADIs 4.645/4.655.
- Benign flags: art. 48/53 quoted Lei 10.683/11.182 text. Part sha 7e378797 (pre-effects dab71ee5); merged 170 acts, 2908
  versions, 2231 commits, check 0/0, compare identical, audit clean. README row + jurisdiction.json (170 acts).

## 99-batch17w - PUBLISHed 2026-10-31 (seventh session)
Lei 10.233/2001 (ANTT, ANTAQ, DNIT), 38 versions 2001-06-06 .. 2024-01-16 (l10233 is its own consolidated page; 0 diffs).
- Pinned ato:adc-6-2018-mpv800 (iaonly.py gap). Hand (`_LANTT`, scoped): MP_LAPSE mp-800-2017 27.2.2018; MP_PENDING
  mp-2217-2001 (art. 7 on publication, DOU 5.9.2001; art. 6 confirms MP 2.201-2); CONVERTED_FIX mp-155-2003 -> lei-10871-2004
  (its page: 'Conversão da MPv nº 155, de 2003').
- MP 1.065/Lei 14.273 clash (SPAN_FIX _W1065): Lei 14.273 in force 6.2.2022 (LINDB from DOU 23.12.2021 extra), MP lapse day
  7.2.2022. MP lines Lei 14.273 replaced/revoked end 6.2.2022 (art-13 p.u., art-38, art-82 § 1º) and their restored copies
  are skipped ('never-restored'); batch7's 'with its article' rule had wrongly ended art-24 IV and art-25 III on 6.2.2022
  (Lei 14.273 did not touch them; read its art. 72): both now end with the lapse 7.2.2022 and art-25 III's 2001 text is back.
- Undated lines: art. 7º-A Lei 10.683 wording (printed 'Art. 7 o A', read under art-07) moved to art-07-a 29.5.2003-8.5.2007
  (SPAN_FIX can set unit/label; new 'moved_from' key lets the lifespans wrapper drop its 'no end' problem), MP 2.217 wording
  ends 29.5.2003; art-88 p.u. (unclosed note) ends MP 870 1.1.2019.
- Found by checks/reading: art-115 2001 caput and § 1º end 5.9.2001 (MP 2.217-3 caput + art. 8 revocation); art. 118 § 1º
  split in the paragraphs wrapper (2001 'art. 114' / MP 2.217-3 'art. 114-A', read on the MP page); art. 102-A printed after a
  stray '"' -> own unit; art. 88-A from its promulgation 11.12.2019 (Lei 13.901 art. 5 vetoed, override; DOU 11.12.2019).
- effrep (w-effrep.log): all on publication except Lei 13.848 (90 days, reader), Lei 14.273 (LINDB); Lei 10.470/MP 375
  financial effects only (kept). effects_fix 0 moves. Benign flags: leakcheck 10 literal, firstline art-94 (§§ 3º-4º stay after
  Lei 10.871 revoked caput/§§ 1º-2º), ordercheck art-47-b (Lei 14.298 prints p.u. (Revogado) before §§ 1º-3º), quotecheck 3.
- Part sha 12d37dc7 (pre-effects 9272ba39); merged 171 acts, 2946 versions, 2253 commits, check 0/0, compare identical, audit
  clean. README row + jurisdiction.json (171 acts).

## 99-batch17v re-PUBLISHed 2026-10-31 (seventh session): art. 63-B term
Lei 14.901/2024 art. 5: art. 63-B 'terá vigência por 5 (cinco) anos' from 26.6.2024 (DOU, in force on publication): term
26.6.2024..25.6.2029, so SPAN_FIX ends caput + p.u. on 2029-06-26 (end_how 'term', credited lei-14901-2024) -> one futuro
version (scratch build futuro: '2029-06-26 LRDC: Art. 63-B (Lei nº 14.901, de 2024)'). No extending law on the page (capture
23.10.2026). Counting: first day counted (LC 95 style), version the day after the last day. OPEN_ITEMS text updated.
Part sha f184eb6f (pre-effects 4071b233); merged 171 acts, 2947 versions, 2254 commits, check 0/0, compare identical, audit
clean; same benign flags as before. README row (26) + futuro lines + jurisdiction.json.

## 99-batch17x - PUBLISHed 2026-10-31 (seventh session)
Lei Geral das Agências Reguladoras 13.848/2019 (2 versions; in force 24.9.2019, 90 days) and Lei 9.986/2000 (11 versions).
Pages l13848 (ts 20261019033049), l9986 (ts 20261004205325; both their own consolidated pages); `iaonly.py laws` (7 new) +
`missing` (0); pinned ato:adc-79-2023-mpv1181.
- Hand (`_L9986`, scoped): CONVERTED_FIX mp-155-2003 (also set for _LANTT); MP_LAPSE mp-1181-2023 15.11.2023; MP_PENDING
  mp-2229-2001 and mp-2216-2001 (Lei 9.986 text; part b/f texts untouched). SPAN_FIX art-32 p.u. falls with the article
  (Lei 14.724 art. 36 III, 14.11.2023; MP gap from 18.7.2023); EXPLAINED art-32.
- Benign: Lei 13.848 dupline 18 / dupcheck 3 / leakcheck 4 / quotecheck = quoted amendments in arts. 41-45. effects 0 moves.
- Part sha 7cae6c66 (pre-effects a289b28f). Final merged build (all installed parts, after README edits): 173 acts, 2960
  versions, 2259 commits, check 0/0, compare identical, audit clean.

## Eighth session (2026-10-31 late): MP edition reader (batch 6) + 99-batch17y PUBLISHed
Reader change, in batch6/parse_batch6.py (the reader every batch 6-17 parser imports; batch 3/4/5/5b, proc, phase2, clt,
codes, rju do not import it and credit only pinned editions):
- law_key: a note 'Medida Provisória nº <n>-<e>, de <y>' gets its own key mp-<n>r<e>-<y> whenever the page pinned as
  law:mp-<n>-<y> is a different edition (pinned_edition() reads the edition from the pinned URL '.../<n>-<e>.htm'); the
  base key stays the pinned edition (labels unchanged: 'Medida Provisória nº 2.177, de 2001' = 2.177-44). REISSUES (1710-1)
  kept. page_info for r-keys was already in batch 6 (own pinned page, base-number check, LexML ';n-e').
- mp_chain() replaces the hand MP_CHAINS (still honoured): 2+ start notes naming pre-EC32 MPs whose editions rise with
  their DOU days -> the wording starts with the earliest, if its text (alnum, label stripped) is on every edition's page;
  else latest day kept, listed (MP_CHAIN_UNREAD decision). Renumbering notes left alone.
- Edition end: page_info marks an MP page before 11.9.2001, not converted / MP_LAPSE / MP_PENDING, with 'Reeditada pela
  MPv nº X-E' (next page pinned) as REISSUED (MP_PENDING marker so parse_proc raises no fate problem; mp_notes wrapper
  says 'was reissued as ... (DOU d)'); reissue_ends(): a struck line of that edition with no end ends on the next
  edition's DOU day unless the next page carries the same label+words (then a problem); also (pre-EC32 editions only) §§
  an edition made end when a later edition's 'Parágrafo único' after them starts, and a wording printed again later in the
  article with a later edition's note ends the first copy (successor search stops at a higher-level line). The next
  edition is added to ACT_LAWS (pruned if unused).
- LexML for a base key whose pinned page is an edition: record ';<n>-<e>' read if cached (MP 1.891-8: page DOU 27.8.1999 is
  the previous edition's; LexML 25.9.1999 edição extra).
- Decision added only when r-keys are in a part: base label = pinned edition list.
Verification: batch18/.tmp/reparse_all.py <dir> reparses all 53 batch 6-17 parts (+effects_fix), one process at a time.
Baseline (before the change) in .gitlaw-scratch/brazil-b18/base; after the final reader (after3) every one of the 53 is
byte-identical to its baseline (17q's 3 problems pre-exist). NOTE: the baseline already differs from several INSTALLED
parts in sources notes/requests and later global NOTE_FIX decision lines (13a-g, 14a-c, 16a-d, 17a-x): pre-existing drift,
not from this change.
Installed parts crediting pre-EC32 MP editions (batch18/.tmp/edparts.py): 6, 7, 9, 10, 12, 14b, 14d, 15a, 15b, 16b, 16e,
16f, 17a, 17b, 17c, 17f, 17g, 17i, 17k, 17w, 17x (+70-clt, 95-rju, other parsers): every credited edition is the pinned
one -> 0 units moved; the open items (MPs 2.164, 2.165, 2.183, 2.196, 2.197, 2.216, 1.894, 2.168) stay open because
Planalto's pages name no earlier edition. Each of the 21 PUBLISH files got a re-verification line.
Lei 9.656 (99-batch12): NOT extended to 1998: its pre-2.177-44 editions (1.685-5, 1.730-7, 1.801-11/-14, 1.908-17/-18/-20)
appear only in struck 'Vide' pointers and credit no wording. Next step if wanted: walk chains BACKWARD through each
edition's convalidation article ('Ficam convalidados os atos praticados com base na Medida Provisória nº X-(E-1)') and date
a final-edition wording by the earliest edition whose page carries it (~40-56 pages per chain, ~300 pages for all chains
above); Lei 9.656 back to 1998 would also need the intermediate wordings parsed from the edition pages.

### 99-batch17y - PUBLISHed (eighth session)
Lei 9.961/2000 ANS (9 versions 2000-01-29 .. 2019-09-24), Lei 9.717/1998 RPPS (9, 1998-11-28 .. 2019-06-18); 0 diffs, 0 problems.
Pinned (iaonly.py gap, archive.org): mp-1891r9-1999, mp-1891r10-1999, mp-2097r37/r40/r41-2001, mp-2177r43-2001,
mp-2187r12-2001, mp-2043r21-2000, mp-1976r34-2000; LexML medida.provisoria:1999-09-24;1891-8 cached (robots read: /urn ok).
Chain starts: ANS art. 4 XVII, XXXV, XL, XLI + a)-g), etc. from 2.177-43 (28.7.2001) / 2.097-36 (27.1.2001) / 1.976-33; 9
wordings kept at 2.177-44 (text not on the earlier page: 2.177-43's page misprints 'depanos'; 2.097-36's § 7º and art. 33
differ). Ends: art. 4 XLIII, § 4º (2.177-43) on 27.8.2001; L9717 art. 1 §§ 1º-2º (2.043-20) on 28.7.2001; art. 9 III.
OPEN_ITEMS both acts. effrep: all on publication (13.848 90 days by the reader); effects_fix 0 moves. Benign: leakcheck 5
literal '(revogado)', quotecheck 2 ('alínea "f"'). Part sha a81ebfe4; merged 175 acts, 2978 versions, 2271 commits, check
0/0, compare identical, audit clean (also after the README rows). README rows + jurisdiction.json (175 acts).

## Ninth session (2026-10-31 night): parts z, za
robots.txt read at start (web.archive.org 404; archive.org Disallows /control/ /report/ only). Fetching: archive.org only
(iaonly.py pages/laws/missing/gap). pipe.sh now runs its file checks through run.py too (cpu gate). New tool .tmp/notecount.py
<page id>... (amending acts named per page). Part names after z: za, zb, ... (corpus.d sorts 99-batch17z before 99-batch17za).
Pages pinned: l9427 (l9427cons.htm, ts 20261022010720), l9427-compilada, l9782, l9782-compilado, l8745 (l8745cons.htm),
l8745-compilada; `iaonly.py laws` for the three acts: 33 new pins; NO CAPTURE law:lei-15524-2026 (Lei 9.782, 4 notes).
edscan: l9427 and l8745 name no pre-EC32 edition except MP 2.229-43 (l8745, its pinned edition) and a 'Vide 2.216-37'; l9782
names 1.814-4, 1.912-6/-7/-9, 2.000-16/-17, 2.039-24, 2.134-28/-31, 2.190-34 (stack 2.039-24 + 2.190-34 once).

## 99-batch17z - PUBLISHed 2026-10-31 (ninth session)
Lei 9.427/1996 (ANEEL), 31 versions 1996-12-27 .. 2025-11-25 (l9427cons vs l9427compilada, 0 diffs).
- Hand (`_LANEEL`, scoped): VIGENCIA_FIXED mp-1300-2025 21.5.2025 (art. 2 + art. 9 I a under III), lei-15235-2025 9.10.2025
  (conversion keeps only art. 20 § 1º I-II revocation); MP_LAPSE mp-1212-2024 8.8.2024 (ato:adc-62-2024-mpv1212 pinned, read).
- SPAN_FIX: art-03 XVII and art-20 § 1º MP 1.300 wordings end 9.10.2025, Planalto's struck second copies of the earlier
  wordings = restored 9.10-25.11.2025 (Lei 15.269); art-26 § 12 '(VETADO)' 2.3-11.6.2021, promulgated § 12 from 11.6.2021
  (Lei 14.120 promulgation, DOU 11.6.2021, read on its page).
- effrep: all on publication (z-effrep2.log). effects_fix 0 moves. All checks 0 (quotecheck 4 = 'alínea "f"' law text).
- Part sha 931d49fa (pre-effects 77b1fb78); merged 176 acts, 3009 versions, 2281 commits, check 0/0, compare identical, audit
  clean. README row + jurisdiction.json (176 acts).

## 99-batch17za - PUBLISHed 2026-10-31 (ninth session)
Lei 8.745/1993 (contratação temporária), 32 versions 1993-12-10 .. 2026-03-31 (l8745cons vs l8745compilada, 1 diff EXPLAINED
art-05). MP 922/2020 (110 notes) handled by the reader (shared lapse 30.6.2020, Ato 72/2020).
- Hand (`_LCTEMP`, scoped): MP_LAPSE mp-1181-2023 (text for 8.745), mp-1186-2023 20.2.2024 (ato:adc-7-2024-mpv1186 pinned,
  read); MP_PENDING mp-2229-2001 (8.745 text); NOTE_FIX '(Incluído pela MPV nº 2.229-43, de 6.9.2001)'.
- SPAN_FIX: art-04 parágrafo único (Lei 10.667) no end (reader's 'renumbered' by MP 922 removed; gap 2.3-30.6.2020 kept);
  art-05 p.u. unstruck revoked copy (nth 1) skipped; art-04 '§ 8º' Vide MP 86 pointer skipped.
- paragraphs wrapper l8745 + l8745-compilada: 'Prorrogação de prazo' pointers (MP 431 / Lei 11.784 art. 173, one unclosed)
  and stray full stops removed from art-02 d) and the 2003 art-04 caput (L8745_FIXED decision).
- effrep (za-effrep.log): all on publication. effects_fix 0 moves. Benign: leakcheck 1 (art. 9 'Parágrafo único. (Revogado).'
  as Lei 11.784 worded it), quotecheck 30 (quoted alínea letters). Part sha d4d41427 (pre-effects b889675d); merged 177 acts,
  3041 versions, 2296 commits, check 0/0, compare identical, audit clean. README row + jurisdiction.json (177 acts).

## 99-batch17zb - PUBLISHed 2026-10-31 (ninth session)
Lei 9.782/1999 (Anvisa), 12 versions 1999-01-27 .. 2019-09-24 (l9782 vs l9782compilado, 1 diff EXPLAINED titulos).
- Editions: only 2.039-24 (art. 3 caput, stacked with 2.190-34: mp_chain starts it 22.12.2000) and 2.190-34 credit wordings;
  the other editions are 'Vide' only, so no extra edition pins were needed. law:mp-2134r25-2001 (2.039-24's 'Reeditada pela'
  next edition): NO archive.org capture (cdxpre lists 2134-26..31 only) -> P.MP_PENDING['mp-2039-2000'] fate text (scoped).
- Hand (`_LANVISA`, scoped): MP_PENDING mp-2190-2001; MP_LAPSE mp-557-2011 1.6.2012 (ato:apn-26-2012-mpv557 pinned, read);
  NOTE_FIX 'Lei nº 13.411, de 2017' (x2 forms) -> 2016 (law:lei-13411-2016 pinned to L13411.htm).
- LEFT OUT: art. 8º-A (Lei 15.524/2026, 4 lines): no archive.org capture of l15524 (cdxlist 4 case variants, cdxpre of
  2026/lei/l155: 15501-15526 except 15520/15524) -> paragraphs wrapper drops lines noted 'Lei nº 15.524' on l9782 and
  l9782-compilado; decision + OPEN_ITEMS + README row. Re-check later: if L15524.htm gets archived, pin it, read its
  vigência and add art. 8º-A.
- effrep (zb-effrep.log): on publication except 12.090 (60 d), 13.411, 13.848 (90 d) by the reader. effects_fix 0 moves; all
  checks 0. Part sha f8f86152; merged 178 acts, 3053 versions, 2303 commits, check 0/0, compare identical, audit clean.
  README row + jurisdiction.json (178 acts). New tool .tmp/pinfo.py <law key>... (reader page_info).

## 99-batch17zc - PUBLISHed 2026-11-01 (ninth session)
Lei 10.101/2000 PLR (9 versions), Lei 9.608/1998 serviço voluntário (5), Lei 12.506/2011 aviso prévio (1) = 15 versions; 0 diffs.
- Pages pinned for zc/zd/ze (l10101 + compilado, l9608 + compilado, l12506, l9984 + compilado, l12334, lcp105); `iaonly.py
  laws` for all six acts (13 new) + `missing` (1).
- VIGENCIA_PROVISION (mp-411-2007, Lei 9.608, art-03-a) = 1.1.2008 (MP 411 art. 24 I 'a partir de 1º de janeiro de 2008').
- FOREIGN_RUBRICS l10101 + l10101-compilado: 'Participação nos lucros e prêmios' = MP 905's heading above its art. 48 (read
  on the MP page); FOREIGN_DROPPED decision now split per page (17a reparse: acts/laws equal, only the effects decision
  differs because effects_fix MOVES key on the file name - known).
- lplr_905() (apply_rewrites, Lei 10.101 only): arts. 6/6-A/6-B struck MP 905 copy to 18.8.2020 + unstruck copy (with Lei
  11.603's note, malformed note tolerated) from 19.8.2020; MP 388 copies of 6-A/6-B printed twice -> second skipped
  ('duplicate'); art. 2 §§ 3º-A, 5º-10 (+ incisos) MP 905 lines end 20.4.2020 (no 18.8 return: Lei 14.020 of 7.7.2020 gave
  them their wording); the 18.8 copy of § 3-A skipped. Helper names _lplr_lab/_lplr_alnum (a module-level `_lab` loop
  variable exists further down: do not reuse that name).
- effrep (zc-effrep*.log): MP 597 in force 1.1.2013 (reader), Lei 12.832 retroactive effects keep publication. effects_fix 0
  moves; all checks 0. Part sha 428dae61 (pre-effects 1cfca63f); merged 181 acts, 3068 versions, 2312 commits, check 0/0,
  compare identical, audit clean. README rows + jurisdiction.json (181 acts).

## 99-batch17zd - PUBLISHed 2026-11-01 (ninth session)
Lei 12.334/2010 barragens (3 versions), Lei Complementar 105/2001 sigilo bancário (3) = 6 versions; 0 diffs, 0 problems.
- Hand (`_LC105`, scoped): VIGENCIA_FIXED lc-166-2019 = 9.7.2019 (art. 6 II, 91 days from DOU 9.4.2019, LC 95 counting);
  VIGENCIA_PROVISION (lc-224-2025, LC 105, art-01) = 1.1.2026 (effects clause III). OPEN_ITEMS LC 105 (STF ADIs).
- effrep (zd-effrep*.log). effects_fix 0 moves; all checks 0. Part sha 6dde61b9 (pre-effects b1f9424c); merged 183 acts, 3074
  versions, 2315 commits, check 0/0, compare identical, audit clean (final build after README edits: final9-build.log).

## 99-batch17zf - PUBLISHed 2026-11-01 (tenth session)
Lei 9.984/2000 (ANA), 18 versions 2000-07-18 .. 2023-06-20 (l9984 vs l9984compilado, 0 diffs, 0 problems).
- Pinned law:lei-11805-2008 (iaonly.py gap). MP 437/2008 fate: revoked by MP 439/2008 art. 4 (DOU 29.8.2008 extra; Lei 11.805
  art. 4 repeats it); MP 439's page is pinned under the misprinted key law:mp-439-1998 (note 'Vide MP 439, de 1998'), so the
  credit uses B8.EXTRA_LAWS['mp-439-2008'] (set only when the act runs). ana_437() (apply_rewrites): every struck MP 437 line ends
  29.8.2008 (end_how revoked-mp) and is removed from B.UNDATED / B7.NEXT_WORDING_USED (else the generic decisions call them
  undated). MP_PENDING mp-437-2008 and mp-2216-2001 (Lei 9.984 text), scoped.
- paragraphs wrapper l9984: 'XXIIIA'/'XXIVA -'/'§ 9º A'/'§ 10A.' -> MP 868 labels XXIII-A, XXIV-A, § 9º-A, § 10-A; MP 844's
  'Art. 4ºA.' block -> unit art-04-a (L9984_FIXED). BARE_TEXT l9984 + l9984-compilado art-29 (_BARE_RX9984). SPAN_FIX art-04-b MP
  844 caput pinned (printed after Lei 14.026's 4-B); art-04 § 2º one wording with both MP gaps, copies nth 1/2 skipped.
- effrep (zf-effrep.log): all on publication (13.848 90 days by the reader). effects_fix 0 moves. Benign: leakcheck 2 literal
  '(Revogado).', quotecheck 30 (quoted Lei 8.001 / 9.433 text in arts. 28-32). Part sha b125c12e; zd reparse identical;
  merged 184 acts, 3092 versions, 2318 commits, check 0/0, compare identical, audit clean. README row + jurisdiction.json.

## 99-batch17zg - PUBLISHed 2026-11-01 (tenth session)
Lei 11.182/2005 ANAC (9 versions 2005-09-28 .. 2022-06-15), Lei 13.575/2017 ANM (5, 2017-12-27 .. 2026-09-16); both own consolidated
pages (no compilado capture on archive.org: cdxlist). Pages for zg/zh pinned (`iaonly.py pages`, 6) + `laws` (9 new) + `missing` (0).
- ANM: CONVERTED_FIX mp-1133-2022 -> lei-14514-2022 (page 'Lei nº 14 514'); VIGENCIA_FIXED lei-14514-2022 30.12.2022 (art. 25 III);
  VIGENCIA_PROVISION (lei-14514-2022, LANM, art-21) = 22.5.2024 (vetoed art. 21 changes promulgated 21.5.2024, DOU 22.5.2024).
- ANAC: art-34 struck copy of quoted Lei 6.009 lines skipped (duplicate); lifespans wrapper now also settles 'no end for struck'
  for pinned skipped duplicates (matched by unit, label and text). EXPLAINED art-34 (label-only quoted line). OPEN_ITEMS: Lei
  11.292 art. 29 TFAC anterioridade kept at in-force day (the wording replaced the 2005 one on publication).
- effrep (zg-effrep.log): on publication. effects_fix 0 moves. Benign: leakcheck 6 literal, quotecheck 5. Part sha 6fb78e7a
  (pre-effects 3e49022a); merged 186 acts, 3106 versions, 2326 commits, check 0/0, compare identical, audit clean.

## 99-batch17zh - PUBLISHed 2026-11-01 (tenth session)
Lei 11.428/2006 Mata Atlântica (3 versions), Lei 4.886/1965 representantes comerciais (4), Lei 8.397/1992 cautelar fiscal (2), Lei
9.795/1999 educação ambiental (3) = 12 versions; all own consolidated pages.
- Lei 4.886: paragraphs wrapper l4886: struck '(Suprimido)' marks -> '(Revogado pela Lei nº 8.420, de 1992)' (8.420 art. 3, read);
  Lei 12.246's plain '§ 1º (Suprimido)' kept as text (L4886_FIXED). lrc_renum() (apply_rewrites): art. 10 alíneas a)-g) copies
  1965-28.5.2010 (Lei 12.246 art. 1 renumbering, read); 1965 arts. 42/43 copies of arts. 48/49 to 11.5.1992 (Lei 8.420 art. 2
  'passarão a ter os números 41 ... 47'; original numbering read on the Chamber's publicacaooriginal page via archive.org,
  pinned ctx:camara-lei-4886-1965-original + -retificacao with pinat.py, listed as a source through B6.CONTEXT).
- Lei 11.428: Lei 15.190/2025 (180 days -> 4.2.2026); its art. 66 III (revocation of art. 14 §§ 1º-2º) vetoed then promulgated
  5.12.2025 (DOU 8.12.2025), before the in-force day: 4.2.2026 kept. EXPLAINED art-48. Retificações (11.428: 9.1.2007; 8.397:
  16.1.1992; 4.886: 20.12.1965 '§' sign only) in OPEN_ITEMS.
- effrep (zh-effrep*.log): Lei 9.532 art. 65 under art. 81 I (on publication), Lei 14.195 art. 53 under art. 58 V. effects_fix 0
  moves. All checks 0 except quotecheck 8 (quoted law text). Part sha 6de8461d (pre-effects 19ce6a43); zg reparse identical;
  merged 190 acts, 3118 versions, 2335 commits, check 0/0, compare identical, audit clean (final10-build.log, after README rows).

## 99-batch17zi - PUBLISHed 2026-11-01 (tenth session, after the coordinator's go-ahead)
Lei 11.417/2006 súmula vinculante (1 version, in force 20.3.2007: 3 months), Lei 13.460/2017 usuários (4; federal stage 360 days
-> 22.6.2018; Lei 14.129 federal stage 90 days -> 28.6.2021, reader), Lei 12.187/2009 PNMC (3), Lei 13.123/2015 biodiversidade
(1; DOU 21.5.2015 read in LexML via lexml1.py (robots read: /urn allowed, Crawl-delay 5), Planalto footer misprints 14.5.2015;
180 days -> 17.11.2015) = 9 versions. ACT_DAY entries carry the reasons; OPEN_ITEMS for the staged stages (13.460) and 13.123.
- Lei 11.418/2006 NOT built: it only adds arts. 543-A/543-B to the CPC of 1973 (no text of its own to version).
- effrep (zi-effrep*.log): on publication except Lei 14.129 (staged, reader). effects_fix 0 moves; all checks 0 (quotecheck 4 =
  quoted Lei 9.784 text). Part sha ff74dbd3; zh reparse equal except sources requests; merged 194 acts, 3127 versions, 2340
  commits, check 0/0, compare identical, audit clean (final10b-build.log, after README rows).

## 99-batch17zj - PUBLISHed 2026-11-01 (eleventh session)
Lei 9.718/1998 (PIS/Pasep and Cofins), 38 versions 1998-11-28 .. 2025-05-01 (+ 2027-01-01 on futuro); l9718 vs l9718compilada,
1 diff EXPLAINED (art-05 'Vide MP 497' note printed in the compilada line). robots.txt read at start (web.archive.org 404;
archive.org Disallows /control/ /report/ only); archive.org only.
- Pages pinned for zj/zk/zl (`iaonly.py pages`, 6: l9718 + compilada, l10637 + compilado, l10833 (leis/2003/l10.833.htm) +
  compilado); `BATCH17_ACTS=lei-9718-de-1998 iaonly.py laws` (10 new) + `missing` (0). Gap pins: law:mp-1991r18-2000,
  mp-1807r1-1999, mp-1858r7-1999, mp-1991r16-2000, mp-2037-2000 (2.037-19: keyed WITHOUT r because mp-2037-2000 had no pin;
  next_edition() looks up law_key(), which gives the base key when the base is unpinned - renamed in the pin file),
  ato:apn-36-2013-mpv601.
- Staged start (art. 17): build_act wrapper in parse_batch17 (_G9718 gates: arts. 2-8 1.2.1999, arts. 9/12-15 1.1.1999;
  lines of gated units starting before the gate are moved to the gate, so MP 1.807 is credited with the gate day). Same
  wrapper: lc214_2027() (LC 214 art. 542 X repeals arts. 2-8-B, art. 504 new art. 9 wording, both 1.1.2027: not on Planalto's
  9.718 page) and the art. 5 § 4º-A incisos reorder (MP 1.063 incisos under MP 1.069's caput).
- 'DO de' footers: MP editions of 2000 end 'publicado no DO de' (no U); _R_PUB + _with_pub() (wraps B6.page_info AND
  P.page_info, patching P.decode for those keys only) - PUBLISHED_FIXED is NOT usable for edition keys (batch 6 reads an edition
  under its base key, so the base entry dates every edition, and the REISSUED check inside B6.page_info needs the day).
- Hand (`_L9718`, scoped): VIGENCIA_FIXED lei-12844-2013 (V), mp-472-2009 (I d), mp-601-2012 (publication), lei-13043-2014
  1.1.2015 (art. 113 II); MP_LAPSE mp-601-2012 4.6.2013; MP_PENDING mp-2158-2001 (9.718 text); SPAN_FIX art-03 § 6 I/II end
  27.8.2001 (reader had ended them at § 8's I/II), MP 1.063 art-05 lines start/end 1.12.2021 (effects_fix REFUSES: MP 1.069
  changed art. 5 on 13.9.2021, before the effect day), MP 1.063 § 4º-A skipped; TEXT_FIX (both pages) art. 4 p.u. stray '"',
  § 8 II '.)'; paragraphs wrapper drops 'Sem eficácia'. OPEN_ITEMS + EXPLAINED.
- effects_fix MOVES "99-batch17zj.json": 11 entries, 18 moves (MP 1.991-15 arts 4-6 None, 1.991-18 -> 1.7.2000, 2.158-35 § 9 ->
  1.12.2001, 10.637 -> 1.1.2003, 10.865 -> 1.5.2004, MP 413 None (judgement: event-tied, Lei 11.727 fixed 1.10.2008), 11.727 ->
  1.10.2008, MP 451 -> 1.1.2009, MP 601 -> 1.1.2013, 12.814 -> 1.1.2014, LC 214 -> 1.5.2025). Amenders read: scratch zj/effrep.txt.
- Checks: dupline/dupcheck/order/firstline/pubgap 0, leakcheck 7 literal '(revogado)', quotecheck 6 benign, missorig 12 = gates,
  overlap 0, headyear only rNN false positives. Part sha 9e3dce70 (pre-effects 8cf1b49e); k and zi reparsed: equal except
  sources[0]. Merged 195 acts, 3165 versions, 2360 commits, check 0/0, compare identical, audit clean (final11-build.log, after
  README row + jurisdiction.json).

## 99-batch17zk - PUBLISHed 2026-11-01 (twelfth session)
Lei 10.637/2002 (PIS/Pasep não cumulativo), 44 versions 2002-12-31 .. 2026-01-09 (+ 2027-01-01 on futuro); l10637 vs l10637compilado,
6 diffs EXPLAINED (placeholder lines for revoked dispositivos; 'n o'/'nº'). robots.txt read at start (web.archive.org 404; archive.org
Disallows /control/ /report/ only); archive.org only (iaonly.py laws/missing/gap).
- Generalised date-by-article wrapper: _GATES {slug: (table, act law, used list)} in build_act (9.718 unchanged: zj reparse equal);
  _G10637 (art. 68 III: arts. 34, 37-44, 46, 48 -> 1.1.2003; I/II reach back before publication) and _G10833 (art. 93, ready for zl).
- futuro: _FUT2027 {slug: (units ended, {unit: (caput prefix, new caput)}, decision)} + fut_2027() (LC 214 art. 542 XVIII, art. 507
  art. 35 caput). Only capita can be rewritten so far: extend to (unit, label) for zl.
- Pins: law:lei-11529-2007 RE-PINNED to l11529.htm (Planalto's notes link to l10637.htm#art3, so `laws` had pinned the act's own
  page); mp-382-2007, mp-392-2007, lei-11604-2007, ato:adc-40-2023-mpv1159 (iaonly.py gap). New tools .tmp/hrefs.py (anchors whose
  text matches), ctx.py / mq.py (page text around matches; mq = several page::regex::before::after queries in one process).
- Hand (zk/zl block, scoped to the two acts): MP_LAPSE mp-1159-2023 2.6.2023; MP_PENDING mp-382-2007; VIGENCIA_FIXED lei-14596-2023
  1.1.2024, lei-13043-2014 1.1.2015; NOTE_FIX MP 382 ', 2007', MP 392 (no year), 'MP nº 11.488, de 2007' (x2) -> MP 447/2008;
  VIGENCIA_PROVISION (lei-12973-2014, 10.637, art-55) 14.5.2014; BARE_TEXT l10637(+compilado) art-47, art-54 (_BARE_RX10637; own
  decision; the generic 7.689/9.249 decision now excludes l10637); lifespans wrapper: MP 1.159 restored copies (start_law
  mp-1159-2023-fim, end < start: Lei 14.592 replaced them 30.5.2023) skipped (MP1159_SKIPPED decision; applies to zl too).
- SPAN_FIX (effects_fix would refuse: Lei 11.787 26.9.2008, MP 451 16.12.2008, Lei 11.898 9.1.2009 changed the units in between):
  MP 413 lines skipped (never in effect, as 9.718); Lei 11.727 art. 14 + art. 42 III c) revocations -> 1.10.2008, art. 35 (art. 2
  VIII/IX) -> 1.1.2009; MP 451 art. 3 § 15 -> 1.4.2009. Watch prefixes: 'VIII - no art. 49 da Lei nº 10.833' first matched Lei
  10.865's earlier VIII (fixed with a longer prefix; ordercheck caught it).
- effects_fix MOVES "99-batch17zk.json": 9 entries, 18 moves (see PUBLISH). Kept on publication: retroactive effects (10.684, MP
  447, 11.933, 11.945, 11.727 art. 42 II a)). Judgement: Lei 10.833 art. 94 VI 'data de início dos efeito' = 1.2.2004; MP 451's
  art. 22 I items are printed struck on its page, read as published (as zj did).
- Checks: dupline 3 / overlap SAME 3 = art. 32 p.u. repeats incisos I-III (law text); leakcheck 1 literal; quotecheck = quoted
  amendments; missorig 11 = gates. Part sha edb71afb (pre-effects 8393b4fa); zj and zf reparsed equal (except sources[0] requests);
  merged 196 acts, 3209 versions, 2384 commits, check 0/0, compare identical, audit clean (final12-build.log, after README row +
  jurisdiction.json).

## Part zl (Lei 10.833/2003) - thirteenth-session notes (all items DONE and PUBLISHed in the fourteenth session: see 99-batch17zl below)
Configured: _act lei-10833-de-2003 (L10833), PARTS zl, ACT_DAY (art. 93: 30.12.2003; gates in _G10833: arts. 1-15, 25-27, 29, 30,
34, 52 -> 1.2.2004; 49-51, 53-58 -> 1.4.2004), ACT_LAWS. Latest trial zl-t5 (scratch zl-t5.json): 46 versions, 0 problems, 6 diff
units, all EXPLAINED (art-02 'n o'/'nº' + stray 'IX - n' on the consolidated page, art-03 'desta Lei.' + 'nos'/'nºs', art-18/62/70
'n o', art-77 dotted quoted lines). Done this session (all in parse_batch17.py, scoped to the act):
- 1. MP 472/2009 (art. 27 -> art. 18, I d) and Lei 12.844/2013 (art. 23 -> art. 62, V): own zl VIGENCIA_FIXED block (end of file),
  read with effrep; crash gone.
- 2. MP 2.158-35 / Lei 9.990 / Lei 10.548 'com a redação dada' tails: BARE_TEXT l10833 art-23, art-25 (2003 caput), art-40
  (+ compilado art-23/40), _BARE_RX10833 + own decision; 'l10833' added to _BX.
- 3. 'efeito'/'efeitos': third text = the Chamber's copy of the original publication, archive.org capture pinned with pinat.py as
  ctx:camara-lei-10833-2003-original (ts 20251216123940; robots.txt read: web.archive.org 404, archive.org /control/ /report/
  only). It prints 'efeitos' wherever the consolidated page does (incl. 'gases liquefeitos', arts. 93, 94 VI): the annotated
  page dropped the 's' throughout (227 'efeito' vs 57 'efeitos' on the consolidated page). efeitos_fix() in the paragraphs
  wrapper (page l10833 only): a line whose letters+digits are found in none of EFX_REFS (consolidated page, Chamber original,
  Lei 11.727's page) or its note's act page, but are found with one set of its 'efeito' made 'efeitos', takes those words: 29
  lines fixed, 0 open; decisions EFX_FIXED/EFX_OPEN; B6.CONTEXT lists the Chamber page as a source. ACT_DAY and zk OPEN_ITEMS
  quotes corrected to 'efeitos'. Decision text avoids the phrase "Planalto's consolidated page" (batch5 rewrites it).
- 4. NOTE_FIX 'Lei nº 11.933, de 2007' (x2) -> 2009 and 'Lei nº 12.767, de 20212' -> 2012 (links read with hrefs.py). 'Vide Lei
  nº 10.685, de 2004' is a pointer on the struck Anexo Único (credits nothing; its link goes to L10.865#art26): no fix needed.
  MP 436's lower-case notes key correctly (mp-436-2008).
- 5. futuro: fut_2027 generalised (ends: unit or (unit, label) + the incisos under it; rewrites: (prefix, new caput) or [(label,
  prefix, new)]; optional inserts {unit: (after label, [(label, text)])}; capita matched by label 'Art. N' - the old matcher
  wanted label 'caput', so part zk's art. 35 was never rewritten: zk re-PUBLISHed, see below). _FUT2027[_L10833]: art. 542 XXI
  (arts. 1-16, 25, 31 § 1º, 49, 50, 52, 55, 57, 58, 91) + art. 509 (capita 23, 30, 31, 33, 34, 67; art. 32 p.u. caput; art. 67
  § 3º + I, II new), all 1.1.2027 (art. 544 III as LC 227 worded it). Checked on the 2027 state (tool .tmp/state.py).
- SPAN_FIX pointers skipped: art-03 '§ 22.' (Vide MP 413), art-30 '§ 4º' (Vide MP 232).
REMAINING (item 5 of the old list: effect days; amenders all read with effrep, log .tmp/zl-effrep.log, clauses in zl-q13/14/15):
  a) Beverage regime arts. 58-A..58-V: Lei 11.727 art. 41 VII (MP 436 / Lei 11.827 wording) -> effects 1.1.2009 for its arts.
     32-39. Plan: add art-58-a..art-58-u to _G10833 at ('2009-01-01', 'Lei 11.727 art. 41 VII') with gate law lei-11727-2008
     (base build_act hides the unit before the gate; the batch17 wrapper moves earlier starts to the gate, so MP 436 lines ended by
     Lei 11.827 never show, Lei 11.827 / MP 451 lines start 1.1.2009) and print the art-58 entries of G10833_USED in their own
     decision. CHECK FIRST: art-58-m 'I -'/'II -' Lei 11.827 lines are skip=1 'undated' (wrongly taken as duplicates of MP 436's
     identical lines: un-skip, end 13.097); art-58-m caput (struck, only a revocation note) starts 2003-12-30: start with Lei 11.727.
  b) Lei 11.727 art. 42 IV a) (as Lei 11.827 worded it): arts. 49, 50, 52, 55, 57 and 58 REVOKED from 1.1.2009 ('não havendo, após
     essa data, outra forma de tributação além dos 2 regimes previstos nos arts. 58-A a 58-U'). Planalto prints them unstruck
     with only 'Vide Lei 11.727'; LC 214 art. 542 XXI revokes them again in 2027. Judgement (recommended): end them 1.1.2009
     credited lei-11727-2008 (SPAN_FIX end, end_how 'repealed'), EXPLAINED for the consolidated diff, drop them from the zl
     _FUT2027 ends (nothing left to end). Check whether any later law re-enacted them first.
  c) Effect-day moves (effects_fix MOVES "99-batch17zl.json", or SPAN_FIX where it refuses): Lei 10.865 -> 1.5.2004 (art. 53);
     Lei 10.925 art. 5 re art. 2 § 1º and art. 51 -> 1.11.2004 (art. 17 I c); Lei 11.051 art. 23 re § 20 (as to § 19 II) and art.
     35 IV (art. 84 revoked) -> 1.4.2005 (arts. 24, 35); Lei 11.196 art. 43 re art. 3 and art. 10 XXVII -> 1.12.2005 (art. 132 III
     c); art. 10 XXVI / art. 15 retroactive 14.10.2005, keep); Lei 11.727 art. 15 (arts. 2, 3) and art. 42 III d) (art. 1 § 3º
     IV, art. 10 VII a) -> 1.10.2008 (art. 41 IV); MP 451 art. 9 re art. 1 § 3º VI -> 1.1.2009 (art. 22 I c), re art. 3 § 23 ->
     1.4.2009 (II b; items printed struck on MP 451's page, read as published as in zj/zk); Lei 12.766 art. 3 (art. 10 caput) ->
     1.1.2013 (II); Lei 12.995 art. 27 I e) (art. 58-T § 2º) -> 1.1.2015; Lei 13.097 art. 37 (art. 3) and art. 169 III b) (art. 2
     § 1º VII-IX, arts. 51, 53, 54, 58-A..58-V) -> 1.5.2015; MP 1.159 art. 2 re art. 3 § 2º III -> 1.5.2023; MP 1.185 -> 1.1.2024
     (its art. 15 revocation; check the Lei 14.789 note 'Revogado Lei nº 14.789' without 'pela'); LC 214 art. 539 (art. 2 § 1º-A)
     -> 1.5.2025. Still to read: Lei 13.043 arts. 56, 79, 114 (items IV-V of art. 113), Lei 13.137 art. 24 (arts. 31, 35).
     Keep (retroactive or on publication): 10.548 (bare text), 10.996, 11.307, 11.434, 11.452, 11.488, 11.787, 11.827, 11.898,
     11.933 (1.10.2008 retroactive), 11.945 (I and IV retroactive), 12.024, 12.249 (d retroactive), 12.375, 12.507, 12.767,
     12.844, 12.973 (1.1.2015 by the reader), 13.670, 14.368, 14.440, 14.592, 14.596 (1.1.2024), 14.651, 14.967, MP 447, MP 466,
     MP 472, MP 497, LC 216.
  d) Anexo Único (TIPI list, revoked by Lei 10.925 art. 16 / 17 from 26.7.2004) is not modelled: add to OPEN_ITEMS (or model it).
  e) Then OPEN_ITEMS[_L10833] text, pipe.sh zl, PUBLISH, README row + jurisdiction.json (docs.py).

## 99-batch17zl - PUBLISHed 2026-11-01 (fourteenth session)
Lei 10.833/2003, 53 versions 2003-12-30 .. 2025-07-29 (+ 2027-01-01 futuro); 15 diff units all EXPLAINED; 0 problems. Details in
corpus.d/99-batch17zl.PUBLISH. All in parse_batch17.py (scoped to the act) + effects_fix MOVES "99-batch17zl.json":
- Gates: _G10833 entries may carry a 3rd item = gate law; _BEV art-58-a..v at ('2009-01-01', 41 VII, lei-11727 / 58-V mp-451).
  build_act wrapper no longer moves the start of a line that ends on/before its gate (such lines never show; avoids false
  credits). zj/zk reparsed: equal except sources[0].
- _REV2009 (arts. 49, 50, 52, 55, 57, 58) end 1.1.2009 lei-11727 'repealed' in the build_act wrapper (REV2009_USED decision);
  dropped from _FUT2027 ends (decision text notes it). EXPLAINED for those 6 + art-10 (VII a) ended 1.10.2008 by SPAN_FIX).
- SPAN_FIX block (_W11727Z etc.): Lei 11.727 art. 15 / 42 III d) -> 1.10.2008, art. 36 -> 1.1.2009 lines of arts. 2, 3; MP 451
  art. 3 § 23 -> 1.4.2009; art-58-m caput start lei-11727, 11.727 I/II end MP 436, 11.827 I/II un-skipped (nth 2); art-58 caput
  I/II (struck, no note) stand to 1.1.2009; art-69 '§ 3º' pointer skipped. VIGENCIA_PROVISION: lei-11727 art-01 1.10.2008,
  art-51/53 1.1.2009; lei-13043 art-67/69/76 14.11.2014 (art. 113 general rule; VIGENCIA_FIXED 1.1.2015 stays for art-10).
- art. 43 quoted item '1. ... ; e' was read as a 'rubrica' of art-44: moved back (L10833_FIXED decision; EXPLAINED art-43/44
  because the consolidated page is read with the same rule).
- effects_fix: 12 entries, 57 unit-moves (list in the PUBLISH). Lei 11.196 art. 74 (art. 35 -> 1.1.2006) was missing from the
  old handoff list; Lei 11.051 § 20 kept on publication (partial effect: OPEN_ITEMS); Lei 12.995 1.1.2015 judgement.
- OPEN_ITEMS[_L10833] written (Anexo Único not modelled, MP 135/2003, retroactive effects, § 20, MP 451 struck items, 12.995,
  MP 1.185/Lei 14.789, Vide pointers).
- Checks: dupline 14 / dupcheck 2 = quoted amendments (arts. 77, 79) + art. 58-R §§ 1º/9º repeated incisos (law text); overlap 2
  SAME = those; leakcheck 3 literal; firstline 0; order 0; quote 30 benign; missorig 30 = gates; headyear = zk's list.
  Parse sha fc743e64 (x2), after effects_fix 8b9fb86e; merged 197 acts, 3262 versions, 2395 commits, check 0/0, compare
  identical, audit clean (final13-build.log, after README row + jurisdiction.json via docs.py rows-zl.json).
- New tools: .tmp/spansj.py <part> <out.json> (every line's span to JSON, one parse), .tmp/sjq.py <json> <law-rx> [unit-rx],
  .tmp/cmppart.py <installed> <new> (key compare, sources[0].requests ignored), .tmp/reparse.sh <parts> (parse + effects_fix
  + compare, one at a time). pipe logs .tmp/zl-pipe1..4.out.

## Fifteenth session (2026-11-01): parts zm, ...
robots.txt read at start (web.archive.org 404; archive.org Disallows /control/ /report/ only). Fetching: archive.org only (iaonly.py
pages/laws/missing/gap, cdxlist). Candidates chosen for thin areas (installed slugs checked first: LDB, Lei 8.142, LC 101, Lei 8.080,
CDC, CADE, Lei 8.137, Eleições, Partidos, LC 64 are already in). Pages pinned for all of them (`iaonly.py pages`, 12): lcp141, l14113,
l12414, l11442, lcp200, l11284, l6091, l9611, l10209, l14119, l9434, l10216 (no compilado captures for l14113/l12414). notecount:
lcp141 7 notes (LC 209/2024, 227/2026, 234/2026); l14113 47 (14.276 32, 14.325 11, MP 1.074, 14.711, LC 227); l12414 67 (all LC
166/2019); l11442 109 (14.206/2021 34, 14.599/2023 18, MP 1.051/2021 15, MP 1.153/2022 11, 13.103 11, 15.485/2026 9 ...); lcp200 13
(LC 207, 211, 223); l11284 149 (14.590/2023 108, MP 1.151/2022 40); l6091 28 (Lei 7.493/1986 25); l9611 0; l10209 19 (10.561/2002,
14.206, MP 1.051); l14119 1; l9434 36 (10.211/2001, MP 2.083-32); l10216 0.
Plan: zm LC 141 + Fundeb (done), zn Lei 12.414 + LC 200, zo transport (11.442, 10.209, 9.611), zp forests (11.284, 14.119), zq
6.091 / 9.434 / 10.216.

## 99-batch17zm - PUBLISHed 2026-11-01 (fifteenth session)
Lei Complementar 141/2012 (lei-do-financiamento-da-saude, 4 versions 2012-01-16 .. 2026-08-07) and Lei 14.113/2020 (lei-do-fundeb, 7
versions 2020-12-25 .. 2026-01-14); 0 diffs, 0 problems. Laws: `iaonly.py laws` (5 new) + `missing` (0); gap pin
ato:adc-35-2022-mpv1074.
- Hand (`_LFUNDEB`, scoped): MP_LAPSE mp-1074-2021 22.4.2022 (wording already replaced by Lei 14.276 on 28.12.2021);
  VIGENCIA_PROVISION (lei-14276-2021, Fundeb, art-21) = 25.3.2022 (vetoed § 9º promulgated, DOU 25.3.2022, on Lei 14.276's page) +
  EXTRA decision (VIGENCIA_PROVISION reasons are not printed as decisions by the shared code; published zg has the same gap - wording
  only, not changed).
- Fundeb act dict has "center_headings": False (headings are <h4>, not centred: name lines were going into articles; firstline.py
  caught it). paragraphs wrapper (page l14113 only): '(Transformado em § 1º pela Lei nº 14.276, de 2021)' -> '(Renumerado do
  parágrafo único para § 1º pela ...)' and the missing space after the struck 'Parágrafo único.' (LFUNDEB_FIXED decision).
- LC 227/2026 (DOU 14.1.2026, republished 15.1, rectified 23.1.2026): arts. 170-171 under art. 182 III (publication); dated by the
  first publication (OPEN_ITEMS). No fixed-term clauses in either act (Fundeb art. 43 rules name financial years; kept).
- Checks all 0 except quotecheck 5 (quoted alínea letters) and latecaput (art. 43 2020 lines, correct). Parse sha f2c001d7 (x2), after
  effects_fix aca140cb (0 moves); zi reparsed: equal except sources. Merged 199 acts, 3273 versions, 2403 commits, check 0/0, compare
  identical, audit clean (final15-build.log, after README rows + jurisdiction.json via rows-zm.json).
- GOTCHA again: a shell heredoc turned r"\1" in Python into a control character; write such edits from a script FILE (scratch
  zm/fixlines.py) or the Edit tool.

## 99-batch17zn - PUBLISHed 2026-11-01 (fifteenth session)
Lei 12.414/2011 (lei-do-cadastro-positivo, 3 versions 2011-06-10 .. 2019-07-09) and Lei Complementar 200/2023
(lei-do-regime-fiscal-sustentavel, 5 versions 2023-08-31 .. 2025-12-19). `iaonly.py laws` (2 new) + `missing` (0).
- Hand (`_LCADPOS`, scoped): VIGENCIA_FIXED lc-166-2019 9.7.2019 (art. 7 II) also for 12.414; SPAN_FIX art. 12 new caput and § 6º from
  9.4.2019 (art. 7 I a), old caput ends then; flagged "by_provision" so the anachronism check (batch15 wrapper) skips them.
  NOTE: LC 166's vigência clause is art. 7; published part zd's VIGENCIA_FIXED text says 'art. 6' (wording slip, not changed).
- LC 200: gate _GLC200 art-11 -> 1.1.2024 (art. 15 I) in _GATES + decision; the art. 11 quoted '§ 7º (VETADO)' line is skipped by the
  reader and the promulgated § 7º (DOU 22.12.2023) first shows with art. 11 on 1.1.2024 (EXTRA decision). EXPLAINED art-11 (_DOTTED).
  Published 99-batch7's law entry lc-200-2023 has '(Promulgação partes vetadas)' at the start of its title (cosmetic, not changed).
- Checks: leakcheck 7 = LC 166's own '(Revogado).' wordings; missorig 1 = gate; quotecheck 4 quoted text; latecaput = struck capita.
  Parse sha 76baa61c (x2, 0 moves). Merged 201 acts, 3281 versions, 2408 commits, check 0/0, compare identical, audit clean
  (final15b-build.log, after rows-zn.json docs).

## 99-batch17zo - PUBLISHed 2026-11-01 (fifteenth session)
Lei 11.442/2007 (lei-do-transporte-rodoviario-de-cargas, 11 versions 2007-01-08 .. 2026-08-06), Lei 10.209/2001 (lei-do-vale-pedagio, 5
versions 2001-03-24 .. 2021-10-22), Lei 9.611/1998 (lei-do-transporte-multimodal, 1 version). `iaonly.py laws` (3 new) + `missing` (0).
- Hand (zo block, scoped): VIGENCIA_PROVISION (lei-14229-2021, LVP, art-08) = 22.10.2021 (art. 7 I; batch9's VIGENCIA_FIXED for
  14.229 is the 180-day default 20.4.2022) + EXTRA decision. SPAN_FIX: LTRC art-05 renumbered § 1º skipped (Lei 14.206 art. 18
  renumbered and gave '§ 1º (Revogado).' at once); LVP art-04 p.u. ends 14.11.2002 'repealed' (Lei 10.561 art. 4 revoked the whole
  article; EXPLAINED); LVP art-07 struck copy = 2001 original (notes cleared, start 24.3.2001, ends 14.11.2002).
- paragraphs wrapper (page l11442): art. 13 'Parágrafo único. (Revogado).' placeholder moved after § 9º and lines renumbered
  (L11442_FIXED decision); ordercheck flags it in any position (benign).
- Lei 13.103/2015 has no in-force clause (LINDB 45 days, 17.4.2015, reader). Lei 12.249 art. 128 retroactive (kept at publication).
  Lei 15.485/2026 converted MP 1.343/2026 (no MP note on the page). OPEN_ITEMS for all three.
- Parse sha 3474f7a0 (x2, 0 moves); zm, zn reparsed identical. Merged 204 acts, 3298 versions, 2414 commits, check 0/0, compare
  identical, audit clean (final15c-build.log, after rows-zo.json docs).

## 99-batch17zp - PUBLISHed 2026-11-01 (fifteenth session)
Lei 11.284/2006 (lei-de-gestao-de-florestas-publicas, 4 versions 2006-03-03 .. 2023-05-25) and Lei 14.119/2021
(lei-do-pagamento-por-servicos-ambientais, 4 versions 2021-01-14 .. 2023-08-24). `iaonly.py laws` (2 new) + `missing` (0); pinned with
pinat.py ctx:camara-lei-14119-2021-promulgacao-162551 (DOU 26.3.2021 extra-D) and -162973 (DOU 11.6.2021): Chamber records of the
two promulgations (cdxpre of www2.camara.leg.br/legin/fed/lei/2021/lei-14119 lists 9 pages).
- prom_14119() in apply_rewrites (PROM14119 table): '(VETADO)' lines un-skipped, stand to the promulgation; promulgated lines start on
  their DOU day credited lei-14119-2021; quote marks of the promulgation text dropped (art. 6 § 8º label fixed). EXPLAINED arts. 6,
  15, 16 (quotes), 23 (_DOTTED). NOTE_FIX 'Lei nº 11.516, 2007' (scoped).
- Benign: dupline/dupcheck/overlap = art. 39 caput II vs § 1º II (same words) and quoted Leis 9.605/6.938 text; leakcheck 18 literal.
- Parse sha 80e7a4a5 (x2, 0 moves); zo reparsed identical. Merged 206 acts, 3306 versions, 2420 commits, check 0/0, compare identical,
  audit clean (final15d-build.log, after rows-zp.json docs).
- GOTCHA: in heredoc-written Python, "\'" inside r'' collapsed too; zp/fixline.py rewrote the line. Prefer script files.

## 99-batch17zq - PUBLISHed 2026-11-01 (fifteenth session)
Lei 6.091/1974 (lei-do-transporte-de-eleitores, 3 versions 1974-08-15 .. 1986-06-18), Lei 10.216/2001 (lei-da-saude-mental, 1), Lei
9.434/1997 (lei-dos-transplantes, 6 versions 1997-03-22 .. 2024-05-22). `iaonly.py laws` (7 new) + `missing` (0); page
l9434-compilado pinned (leis/l9434compilado.htm) and used as Lei 9.434's comparison page.
- Lei 9.434: no in-force clause -> ACT_DAY 22.3.1997 (LINDB 45 days from DOU 5.2.1997). paragraphs wrapper (l9434 + compilado):
  art. 10 '1º Nos casos ...' -> '§ 1º' (L9434_FIXED). EXPLAINED art-10 (compilado keeps the struck 1997 p.u.). MP 2.083-32 (pinned
  edition, DOU 23.2.2001) -> Lei 10.211 conversion; earlier editions not named (OPEN_ITEMS).
- Lei 6.091: Lei 7.493/1986 art. 26 revokes arts. 17-25 outright (read). OPEN_ITEMS for all three.
- Parse sha 3eed2b62 (x2, 0 moves); zp reparsed: equal except sources (pin growth). Merged 209 acts, 3316 versions, 2430 commits, check
  0/0, compare identical, audit clean (final15e-build.log, after rows-zq.json docs).

## State at handoff (batch 17, fifteenth session, 2026-11-01)
Parts zm, zn, zo, zp, zq installed with .PUBLISH (12 acts, 52 versions): LC 141/2012, Lei 14.113/2020 (Fundeb), Lei 12.414/2011, LC
200/2023, Leis 11.442/2007, 10.209/2001, 9.611/1998, 11.284/2006, 14.119/2021, 6.091/1974, 10.216/2001, 9.434/1997. Merged 209 acts,
3316 versions, 2430 commits, check 0/0, --compare identical, audit clean. README rows + jurisdiction.json (209 acts) current. All runs
through .tmp/run.py / pipe.sh / reparse.sh at BelowNormal (cpu gate), one at a time; every PID exited; nothing running. Fetching:
archive.org only (robots.txt read at start); no Common Crawl, no Arquivo.pt, no LexML, no GitHub.
DATED RE-CHECK (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026 - not before.
Left out / unsettled (unchanged): Lei 9.782 art. 8º-A; Lei 10.931; Lei 10.522 art. 32 quoted § 2º; Lei 12.462 art. 63 § 17. No act
of this session was left out.
Noticed, not changed (published parts, wording only): zd's LC 166 VIGENCIA_FIXED text says 'art. 6' (it is art. 7); 99-batch7's law
title for lc-200-2023 starts '(Promulgação partes vetadas)'; VIGENCIA_PROVISION reasons are not printed as decisions (zg has none for
Lei 14.514 art. 21; zm/zn/zo add EXTRA lines instead).
Next candidates (not in the corpus): Lei 13.005/2014 (PNE), Lei 11.494/2007 (old Fundeb, repealed 2021), Lei 9.424/1996 (Fundef),
Lei 11.738/2008 (piso do magistério), Lei 10.861/2004 (SINAES), Lei 12.009/2009 (mototaxistas), Lei 13.103/2015 (motorista
profissional; mostly amends CLT/CTB), Lei 12.379/2011 (Sistema Nacional de Viação), LC 159/2017 (recuperação fiscal), LC 178/2021,
Lei 6.437/1977 (infrações sanitárias), Lei 6.360/1976 (vigilância sanitária), Lei 6.996/1982 (processamento eletrônico eleitoral),
Lei 9.870/1999 (mensalidades escolares). Paths: check the local index, then cdxlist.

## 99-batch17zf - re-PUBLISHed 2026-11-01 (fourteenth session)
_BX now includes "l9984": the generic Lei 7.689/9.249 BARE_TEXT line is no longer given to part zf. Installed file = previous
minus that line (sha cf20e3a2); reparse equal except sources[0]. PUBLISH line appended.

## 99-batch17zk - re-PUBLISHed 2026-11-01 (thirteenth session)
fut_2027's caput matcher wanted label 'caput' (capita carry 'Art. N'), so LC 214 art. 507's new caput of art. 35 (2027) was
described in the decisions but missing from the part; now applied (2027 version gains art-35, credited lc-214-2025). OPEN_ITEMS
quote 'dos efeitos'. Pipeline (pipe.sh zk, log .tmp/zk-pipe4.out): parse twice identical (pre-effects 5e06b68e, after effects_fix
fea61a5c, 18 moves), checks as before; zj, zf, h reparsed: equal except sources[0].requests. Merged 196 acts, 3209 versions, 2384
commits, check 0/0, --compare identical, audit clean. PUBLISH line appended.

## State at handoff (batch 17, fourteenth session, 2026-11-01)
Part zl (Lei 10.833/2003) installed with .PUBLISH; part zf re-PUBLISHed (wording). Merged 197 acts, 3262 versions, 2395
commits, check 0/0, --compare identical, audit clean. All runs through .tmp/run.py / pipe.sh / reparse.sh at BelowNormal (cpu
gate), one at a time; every PID exited; nothing running. No fetching this session (all pages already cached/pinned).
DATED RE-CHECK (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026 - not before.
Left out / unsettled (unchanged): Lei 9.782 art. 8º-A; Lei 10.931; Lei 10.522 art. 32 quoted § 2º; Lei 12.462 art. 63 § 17.
NEXT: pick the next act (see 'Next (tax laws, configured pages only)' below); no part is half-done.

## State at handoff (batch 17, thirteenth session, 2026-11-01)
zk re-PUBLISHed (above). zl NOT published: items 1-4 done, effect days (REMAINING a-e in the zl section) still to model; the code
is in place and scoped (a zl parse gives 0 problems, 6 EXPLAINED diffs). Merged state unchanged in acts/versions: 196 acts, 3209
versions, 2384 commits, check 0/0, --compare identical, audit clean. All runs through .tmp/run.py / pipe.sh at BelowNormal (cpu
gate), one at a time; every PID exited; nothing running. Fetching: archive.org only (one CDX listing + one pinned capture).
New tools: .tmp/efx.py (efeito counts on the three texts), .tmp/state.py <part> <day> <unit>... (units in force on a day),
.tmp/fixbs2.py (replace literal backspaces a shell heredoc writes for ''), .tmp/futedit.py (one-off edit, kept for the record).
DATED RE-CHECK (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026 - not before.
Left out / unsettled (unchanged): Lei 9.782 art. 8º-A; Lei 10.931; Lei 10.522 art. 32 quoted § 2º; Lei 12.462 art. 63 § 17.
Noticed, not fixed: in the BARE_TEXT decisions, _BX lacks "l9984", so part zf also gets the generic Lei 7.689/9.249 decision line
(published zf; wording only).

## State at handoff (batch 17, twelfth session, 2026-11-01)
Part zk (Lei 10.637/2002) installed with .PUBLISH; merged 196 acts, 3209 versions, 2384 commits, check 0/0, --compare identical,
audit clean. Part zl configured, not published (to-do list above). All runs through .tmp/run.py / pipe.sh at BelowNormal (cpu
gate), at most 2 at once (a fetch beside a parse/build; parses never in parallel: they share .tmp/stage.json); every PID exited;
nothing running. DATED RE-CHECK (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026 - not before.
Left out / unsettled (unchanged): Lei 9.782 art. 8º-A; Lei 10.931; Lei 10.522 art. 32 quoted § 2º; Lei 12.462 art. 63 § 17.

## State at handoff (batch 17, eleventh session, 2026-11-01)
Part zj (Lei 9.718/1998) installed with .PUBLISH; merged 195 acts, 3165 versions, 2360 commits, check 0/0, --compare identical,
audit clean. All runs through .tmp/run.py / pipe.sh at BelowNormal (cpu gate), one at a time; every PID exited; nothing running.
DATED RE-CHECK (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026 - not before.
Left out / unsettled (unchanged): Lei 9.782 art. 8º-A; Lei 10.931; Lei 10.522 art. 32 quoted § 2º; Lei 12.462 art. 63 § 17.
NEXT: Lei 10.637/2002 as part zk, then Lei 10.833/2003 as part zl (one act per part). Pages ALREADY PINNED (ids l10637,
l10637-compilado, l10833, l10833-compilado); acts NOT configured (add _act + PARTS + ACT_DAY + ACT_LAWS as for zj).
- notecount: l10637 233 notes (heavy: 10.865/2004 29, 12.973/2014 28, 11.196 22, LC 225/2026 20, 10.684 14); l10833 518 notes
  (11.727/2008 106, 10.865 79, 13.043 37, 11.827 32, 10.925 31, 13.097 30, 11.051 27, MP 436/2008 23 - MP 436's notes are
  lower-case 'me 436' on the page, check law_key).
- Both are MP conversions (10.637 of MP 66/2002, 10.833 of MP 135/2003): their own effect clauses are staged (10.637 art. 68: I
  arts 29/49 1.10.2002, II arts 1-6 and 8-11 1.12.2002, III arts 34, 37-44, 46, 48 1.1.2003, IV rest on publication; 10.833 art.
  93 similar: read it) -> gates as zj's _G9718 (generalise the wrapper with a per-act table). LC 214 art. 542 (from 1.1.2027)
  revokes parts of both (read items XII+ on LC 214's page) -> futuro like lc214_2027(). LC 225/2026: read its effect clause.
- Expect effects_fix refusals where an MP changed the unit between in-force and effect day: settle with SPAN_FIX as MP 1.063.

## State at handoff (batch 17, tenth session, 2026-11-01)
Parts 99-batch17a..zi installed with .PUBLISH (this session: zf Lei 9.984, zg Leis 11.182 + 13.575, zh Leis 11.428 + 4.886 + 8.397
+ 9.795, zi Leis 11.417 + 13.460 + 12.187 + 13.123 = 11 acts, 53 versions); merged 194 acts, 3127 versions, 2340 commits, check
0/0, --compare identical, audit clean. README rows + jurisdiction.json (194 acts) current. All runs through .tmp/run.py / pipe.sh at BelowNormal (cpu gate), one at a
time; every PID exited; nothing left running. Fetching: archive.org only (robots.txt read at start: web.archive.org 404,
archive.org Disallows /control/ /report/ only); no Common Crawl, no Arquivo.pt, no LexML this session.
Shared-code edits this session (all scoped to their acts; zd, zf, zg reparsed after: identical except sources[0].requests): BARE_TEXT
l9984(+compilado) art-29; paragraphs blocks l9984, l4886; apply_rewrites ana_437, lrc_renum; lifespans wrapper settles 'no end'
for pinned skipped duplicates (unit+label+text match).
DATED RE-CHECK (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026 - not before.
Left out / unsettled (unchanged): Lei 9.782 art. 8º-A (Lei 15.524/2026 not archived); Lei 10.931 (no capture); Lei 10.522 art. 32
quoted § 2º; Lei 12.462 art. 63 § 17. New open item: Lei 11.182 art. 29 TFAC anterioridade (kept at in-force day).
Next candidates: heavy tax Leis 9.718/1998, 10.637/2002, 10.833/2003 (PIS/COFINS, MP chains: one act per part); otherwise pick
further federal acts not in the corpus (check corpus.d first). Lei 11.418/2006 is not a candidate (amending law only). Add PAGES, `iaonly.py pages`, `BATCH17_ACTS=... iaonly.py laws` + `missing`, notecount.py, then the
trial and pipe.sh.

## State at handoff (batch 17, ninth session, 2026-11-01)
Parts 99-batch17a..zd installed with .PUBLISH (this session: z, za, zb, zc, zd = 9 acts, 95 versions); merged 183 acts, 3074
versions, 2315 commits, check 0/0, --compare identical, audit clean. README rows + jurisdiction.json (183 acts) current.
All runs through .tmp/run.py at BelowNormal (cpu gate; pipe.sh's file checks now gated too), at most 2 at once (one waiting
on the gate while another ran); every PID exited; nothing left running. Fetching: archive.org only (robots read at start).
DATED RE-CHECK (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026.
Left out / unsettled this session: Lei 9.782 art. 8º-A (Lei 15.524/2026 not archived); MP 2.134-25 not archived (fate of
2.039-24 recorded by hand).
Part zf (Lei 9.984/2000, ANA) CONFIGURED, NOT PUBLISHED: pages pinned (l9984 + compilado), laws pinned; trial zd-t1 (when it
shared part zd): 17 versions, 0 diffs, 4 problems: mp-437-2008 fate unknown (read its page: conversion line or Ato), and
'restored wording after an open one' on art-04-b, art-04 § 9º, § 10 (MP 844/2018 lapse 19.11.2018 and MP 868/2018 lapse
3.6.2019 restored copies vs Lei 14.026/2020; 13 'undated' ends). edscan: 2049-21/-23 'Vide' (check), 2.216-37 x20 (its
pinned edition: MP_PENDING text for Lei 9.984 needed). Run `BATCH17_PART=zf` trial, spans of art-04/art-04-a/04-b, then pipe.
Next candidates (none in the corpus; paths in the local index): Lei 11.182/2005 (ANAC, _ato2004-2006/2005/lei/l11182.htm),
Lei 13.575/2017 (ANM), Lei 11.428/2006 (Mata Atlântica), Lei 4.886/1965 (representação comercial), Lei 11.417/2006 and
11.418 (súmula vinculante / repercussão geral), Lei 8.397/1992 (cautelar fiscal), Lei 9.795/1999 (educação ambiental), Lei
13.460/2017 (usuário de serviços públicos), Lei 12.187/2009 (clima), Lei 13.123/2015 (biodiversidade); heavy tax: Leis
9.718/1998, 10.637/2002, 10.833/2003 (PIS/COFINS, MP chains).

## State at handoff (batch 17, eighth session, 2026-10-31)
Parts 99-batch17a..y installed with .PUBLISH (49 acts); merged 175 acts, 2978 versions, 2271 commits, check 0/0, --compare
identical, audit clean. All runs foreground through .tmp/run.py at BelowNormal, one at a time (PIDs in the logs; all exited;
nothing running). Fetching archive.org + one LexML /urn record only; robots.txt read this session (web.archive.org 404,
archive.org /control/ /report/ only, LexML /urn allowed, Crawl-delay 5). No Common Crawl, no Arquivo.pt.
DATED RE-CHECK (unchanged): MP 1.382/2026 (part m) after 28.11.2026.
Next: Lei 9.427/1996 (l9427cons.htm vs l9427compilada.htm), Lei 9.782/1999 (MP 2.190-34 chain), Lei 8.745/1993
(l8745cons.htm) as small parts: pin pages (iaonly.py pages), run batch18/.tmp/edscan.py / stackscan.py on them first, pin
every edition a crediting note names that differs from the pinned base edition and each such edition's 'Reeditada pela'
next edition (edlinks.py lists hrefs), then the usual pipeline (pipe.sh <part>).

## State at handoff (batch 17, seventh session, 2026-10-31)
Parts 99-batch17a..x installed with .PUBLISH (47 acts; merged 173 acts, 2960 versions, 2259 commits, check 0/0, --compare
identical, audit clean). README rows + futuro lines + jurisdiction.json (173 acts) current. All runs foreground through
.tmp/run.py / pipe.sh at BelowNormal, one at a time; every PID exited; nothing left running. Fetching: archive.org only
(robots.txt read this session: web.archive.org 404, archive.org Disallows only /control/ and /report/); no Common Crawl or
Arquivo.pt requests. This session: w (Lei 10.233), v re-PUBLISHed (art. 63-B term -> futuro 2029-06-26), x (Leis 13.848,
9.986); y (Leis 9.961, 9.717) configured, not published (below).
DATED RE-CHECK (unchanged): on or after 29.11.2026 read MP 1.382/2026's fate (part m).
Left out / unsettled: unchanged from the sixth session (Lei 10.931 no capture; Lei 10.522 art. 32 quoted § 2º; Lei 12.462 art.
63 § 17), plus: Lei 10.233 art. 118 § 1º 'MP 246' wording (none printed); Lei 9.986 ADI 2.310 not modelled.
Part y (coordinator asked for the next candidates): Lei 9.961/2000 (ANS) and Lei 9.717/1998 (RPPS) CONFIGURED AS PART y, NOT
PUBLISHED. Pages pinned (l9961 ts 20261024003623; l9717 20261023143525; l9717-compilado 20261018005809) + 5 cited laws.
Trial y-t1: LANS 5 versions, L9717 7, 0 diffs, 4 problems (mp-1891-1999, mp-1976-2000, mp-2043-2000, mp-2097-2001: no
conversion/lapse known). BLOCKER, why they stay out for now: both pages credit wordings to individual reissues of pre-EC-32
MPs (ANS: 1.976-33/2000, 2.097-36 and -40/2001, 2.177-43 and -44/2001; RPPS: 1.891-8 and -9/1999, 2.043-20/2000, 2.187-12
and -13/2001), but the shared reader keys MPs by number and year (mp-2177-2001 = the pinned 2.177-44, DOU 27.8.2001), so
2.177-43's wordings get 2.177-44's day, 2.097-36 and -40 share one key, and editions that were reissued without conversion
need a dated end per edition (the next reissue's day). Settling them needs edition-level keys (e.g. mp-2177-43-2001, each
pinned to MPV/Antigas/<n>-<ed>.htm, its DOU day, end at the next edition) in the batch17 note reader - a parser change, not a
hand table; batch 12 left Lei 9.656 (same MP 2.177 chain) starting from 27.8.2001 for the same reason. Not done this session.
Next candidates still open: Lei 8.745/1993 (leis/l8745cons.htm; MP chains too), Lei 9.427/1996 (l9427cons.htm vs
l9427compilada.htm), Lei 9.782/1999 (l9782.htm vs l9782compilado.htm; MP 2.190-34 chain). Check each page's note counts for
pre-2001 MP editions first (lawtxt.py + the grep in this session's log) and prefer acts without them.

## State at handoff (batch 17, sixth session, 2026-10-31)
Parts 99-batch17a..v installed with .PUBLISH (44 acts, 514 versions; merged 170 acts, 2908 versions, 2231 commits, check
0/0, --compare identical, audit clean). README rows + jurisdiction.json (170 acts) current. All runs foreground through
.tmp/run.py at BelowNormal, one at a time (PIDs printed in the logs, every one exited; nothing left running). Fetching:
archive.org only (iaonly.py, cdxlist/cdxpre, new pinat.py); robots.txt read at session start (web.archive.org 404 = no
rules; archive.org allows all but /control/ and /report/). No Common Crawl or Arquivo.pt requests.
DATED RE-CHECK (unchanged): on or after 29.11.2026 read MP 1.382/2026's fate (part m; see the fifth-session state below).
This session: q (Lei 10.522), r (Leis 9.873, 10.520), s (Lei 12.783), t (Lei 12.815), u (Lei 9.074), v (Lei 12.462) =
7 acts, 114 versions; q re-PUBLISHed once (decision wording).
Left out / unsettled:
- Lei 10.931/2004: no archive.org capture of its Planalto page (only in the robots-closed Common Crawl index). Not built.
- Lei 10.522 art. 32 quoted § 2º (ADI 1.976, undated) and Lei 12.462 art. 63 § 17 (MP 1.349/2026: Ato Declaratório 77/2026
  not archived, lapse day unknown): LEFT OUT, in decisions/OPEN_ITEMS/README rows. Lei 12.462 art. 63-B 5-year term (Lei
  14.901 art. 5) not modelled.
- Lei 10.233/2001 (ANTT/ANTAQ): CONFIGURED AS PART w, NOT PUBLISHED. Pages + 21 cited laws pinned. Trial w-t1: 35 versions,
  0 diffs vs l10233 (own consolidated page), 6 problems: MP 800/2017 lapse (Ato '../../2018/Congresso/adc-6-mpv800.htm',
  pin it as ato:adc-6-2018-mpv800); MP 2.217-3/2001 (pre-EC 32 chain: MP_PENDING text, as mp-2216-2001); MP 155/2003 (its
  page names no conversion: likely Lei 10.871/2004, read that page before setting CONVERTED_FIX); three 'ends before it
  starts' lines at 2022-02-07..06 (art-13 p.u., art-38 caput, art-82 § 1º: MP 1.065/2021 lapse 7.2.2022 vs Lei 14.273/2021
  in force 6.2.2022 - restored copies need ending on the 14.273 day or skipping); 6 undated lines; then effrep of all
  amenders (510 notes). Next after that: none of the listed candidates remain.

## State at handoff (batch 17, fifth session, 2026-10-31)
Parts 99-batch17a..p installed with .PUBLISH (37 acts, 400 versions; merged 163 acts, 2794 versions, 2183 commits, check
0/0, --compare identical, audit clean). README rows + jurisdiction.json (163 acts) current. All runs foreground through
.tmp/run.py at BelowNormal (one at a time); every PID exited; nothing left running. Fetching: archive.org only (iaonly.py,
cdxlist/cdxpre); no Common Crawl or Arquivo.pt requests.
DATED RE-CHECK: on or after 29.11.2026 read MP 1.382/2026's fate (published 1.8.2026; 60 + 60 days, no recess in the span: term ends about 28.11.2026). If converted: CONVERTED via the MP page, re-parse part m. If lapsed: MP_LAPSE mp-1382-2026 (Ato Declaratório), and MP 1.350/2026 regains effect for its remaining term (revoked-MP rule): re-parse m, effects_fix, checks, re-PUBLISH.
Unsettled / open: Lei 11.977 art. 12 parágrafo único (ended 31.12.2011 with the article, against both Planalto pages:
EXPLAINED); art. 60 § 1º I / § 2º kept in MP 514's wording to 2016 (judgement call).
Next candidates (not in the corpus; pages in the local path index): Lei 10.522/2002 (CADIN; heavy MP chain, own part),
Lei 12.462/2011 (RDC), Lei 10.520/2002 (pregão), Lei 9.873/1999, Lei 10.233/2001, Lei 9.074/1995, Lei 12.815/2013 (portos),
Lei 12.783/2013. Lei 10.931/2004: no page in the index (try archive.org CDX).

## State at handoff (batch 17, fourth session, 2026-10-31)
Parts 99-batch17a..l installed with .PUBLISH (27 acts, 325 versions; merged 153 acts, 2719 versions, 2138 commits, check
0/0, --compare identical, audit clean). README rows + jurisdiction.json (153 acts) current. All runs foreground through
.tmp/run.py at BelowNormal; every PID exited; nothing left running. Fetching: archive.org only (iaonly.py); Arquivo.pt is
user-approved (BRIEF) but not needed so far; no Common Crawl requests.
Next: Lei 11.977/2009 as part m (pages pinned, not configured: see 'Part m').

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

## Sixteenth session (2026-11-01): wording fixes in published parts + parts zr, ...
robots.txt read at start (web.archive.org 404; archive.org Disallows /control/ /report/ only). Fetching: archive.org only.
Task 1 (all three fixed in the parsers, parts regenerated and re-PUBLISHed; merged 209 acts, 3316 versions, 2430 commits, check
0/0, --compare identical, audit clean; build log batch17/.tmp/t1-build.log):
- (a) zd: LC 166 VIGENCIA_FIXED text now 'art. 7' (parse_batch17).
- (b) batch7: lc-200-2023 title without '(Promulgação partes vetadas)' (parse_batch7 __main__ block, TITLE_MARK / TITLE_FIXED =
  {lc-200-2023}; batch 8+ import batch7 and are not touched). No commit changes (merged build takes lc-200's title from 17zn,
  first by file name). NOT done (needs a decision: it changes law commit messages): the same link text starts 124 law entries in
  47 parts (incl. 50-codes, owned by gitlaw-BR-codes), 54 of them the merged build's title (and 183 merged titles start with
  other page links: 'Vide ...', 'Conversão da MPv ...', 'Mensagem de veto', 'Vigência'); e.g. lc-177-2021, lc-212-2025, lei-14843-2024 (from
  99-batch7), lc-214-2025 (90-batch3), lei-14273-2021 (17t), lei-14430-2022 (17zj), lei-14711-2023 (50-codes). Root cause:
  parse_proc.page_info's marker regex lacks the parenthesised form '(Promulgação partes vetadas)' (and 'das partes').
- (c) batch5/parse_batch5.py provision_decisions() (called in write_part): one decision line per (act, law, day, reason) for
  every P.VIGENCIA_PROVISION entry whose law the part's versions credit on that unit (laws sharing articles/day/reason merged
  into one line). Skips B5.PROVISION_AUTO (batch6's 'com a redação dada' keys, added there) and B5.PROVISION_REPORTED (law, act)
  pairs whose EXTRA line already explains the day (17f lei-14004, 17zm lei-14276, 17zo lei-14229: those parts unchanged).
- Regenerated (reparse_all for 7, 9, 11, 12, 15a, 15b, 16f; reparse.sh for 17 f k m zc zd zg zk zl zm zo; out in
  .gitlaw-scratch/brazil-b17/t1/re and brazil-b17/re). Installed = previous file with the regenerated decisions (and laws for
  batch7) via t1/splice.py (refuses if any other key differs; sources ignored = pin growth). Changed parts (each PUBLISH appended):
  7, 9, 11, 12, 15a, 15b, 16f, 17k, 17m, 17zc, 17zd, 17zg, 17zk, 17zl. Previous files in brazil-b17/t1/before.

## 99-batch17zr - PUBLISHed 2026-11-01 (sixteenth session)
Lei 6.996/1982 (lei-do-processamento-eletronico-eleitoral, 4 versions 1982-06-08 .. 1995-09-20) and Lei 9.870/1999
(lei-das-mensalidades-escolares, 3 versions 1999-11-24 .. 2013-11-27); both own consolidated pages. Pages pinned for zr and later
candidates (`iaonly.py pages`, 10: l11738, l12009, l6996, l9870, l12379, l6437 + compilado, l13005, lcp159, lcp178); `laws` (5 new)
+ `missing` (0).
- Lei 6.996: SPAN_FIX art. 16 §§ 1º-2º end 20.9.1995 'repealed' (Lei 9.096 art. 63 revokes the whole article; Planalto strikes
  only the caput) + EXPLAINED art-16. B8.LAW_FIELD_FIX (scoped): lei-7663-1988 enacted 27.5.1988 (heading misprints JUNHO),
  lei-7444-1985 title (ementa without full stop).
- Lei 9.870: MP_PENDING mp-2173-2001 (2.173-24); mesc_renum() in apply_rewrites: MP 2.173-24 renumbered art. 1 §§ 3º-4º -> 5º-6º
  and art. 6 §§ 1º-3º -> 2º-4º (read on the MP page, no words changed): copies under the old numbers 24.11.1999-24.8.2001
  (MESC_RENUM decision). OPEN_ITEMS both acts.
- Amenders all in force on publication; effects_fix 0 moves. Benign: dupline/dupcheck 1 (art. 9 quoted arts. 7º-A/7º-B), quote 4.
  Parse sha 67be88f2 (x2, 0 moves). Merged 211 acts, 3323 versions, 2435 commits, check 0/0, compare identical, audit clean
  (final16-build.log, after rows-zr.json docs).
- NOT built (configured in ALL_ACTS, in no part): Lei 11.738/2008 (lei-do-piso-do-magisterio): Lei 15.437/2026 (31 notes, also
  rewrote the ementa) has no archive.org capture (cdxpre of 2026/lei/l1543: 15430-15439 except 15435/15437); Lei 12.009/2009
  (lei-dos-mototaxistas): MP 1.360/2026 (art. 2) lapsed, Ato adc-96-mpv1.360 not archived (cdxlist 3 variants; cdxpre of
  2026/congresso lists 16 Atos, not this one), so its lapse day cannot be read. Re-check both later.
- Noticed, not changed (published, first by file name in the merged build): 90-batch3's lei-7663-1988 has enacted 1988-06-27
  (same heading slip); 80-proc's lei-9870-1999 title starts '-67, de 1999 Dispõe ...' (MP 1.890-67 conversion link text).

## Seventeenth session (2026-11-01): law titles fixed at the source (coordinator-approved Task 1)
- New shared module brazil-law/titles.py: strip_links(text) removes, one after another, the link lines Planalto prints between
  a law's heading and its ementa ('(Promulgação partes vetadas)' and variants, 'Vide ...' (acts, ADIN lists, RSF, Ato
  Declaratório), 'Conversão da MPv/Medida Provisória nº N-NN, de Y', 'Convertida na/da Lei ...', 'Mensagem de veto [nº N]',
  'Vigência [encerrada | e produção de efeitos]', 'Regulamento[: Decreto nº ...]', 'Produção de efeito(s)', 'Exposição de
  motivos', 'Texto para impressão' (and 'Teto'/'de' typos), 'Revogada/Reeditada/Prorrogada pela ...', 'Prejudicada',
  'Rejeitada', 'Partes promulgadas pelo Congresso Nacional', any parenthesised link, a stray '-67, de 1999' tail). Called in
  the four title readers (parse_proc, parse_codes, parse_phase2, parse_clt page_info) on the raw text after the heading and
  again after the older regex (which left remnants such as 'nº 730 Vigência', ') Texto para impressão', '1.977, de 2009').
- parse_phase2 heading regex now allows 'LEI N o 2.505' (space before the o): 12 laws had the first cited law's date as
  enacted (Lei 10.028/2000 '1950-04-10', Lei 2.505/1955 '1940-12-07', ...) or none; 10 had empty titles. Fixed (enacted + title).
- batch3 write_part: Lei 7.663/1988 enacted 27.5.1988 + the same decision line part zr has (only when the Código Eleitoral is
  among the acts, i.e. batch 3's own part). 80-proc's Lei 9.870 title fixed by the filter.
- Method (scratch .gitlaw-scratch/brazil-b17/t2): regen.py (all 66 parts, one at a time via run.py; old parsers through
  runp.py, which redirects OUT; children inherit BelowNormal), runp.py --off (strip_links = identity) for the 50 parts whose
  fresh parse already differs from the installed file (pre-existing drift: acts/decisions/sources of 50-codes, 60-phase2,
  70-clt, 80-proc, 90-batch3, 95-rju, 97-batch4, 13a/c/d/f/g, 14a/b/c, 16b, 17q, and pin counts in sources notes of most 17x
  parts), splice2.py (installs into the installed file only the off->on difference, refusing anything but titles + the
  allowed enacted/decision; asserts the installed value equals the 'off' value), cmp2.py, chk.py (8 file checks before/after:
  identical except pubgap, which no longer flags the corrected dates in 60-phase2 / 90-batch3). Previous files: t2/before/.
- 99-batch17q: the current parser no longer reproduces its law list (lei-13988-2020, lei-14689-2023, mp-1160-2023-fim
  missing from a fresh parse; mp-1160-2023.temporary_until lost). Its Lei 14.689 title was fixed by applying strip_links to the
  installed title (equals 99-batch11's). NOT investigated further: re-check part q's hand block before any re-parse of q.
- Result: 511 law-title entries changed in 66 parts (each PUBLISH appended), 298 merged titles (54 '(Promulgação partes
  vetadas)', 98 'Conversão ...', 35 'Texto ...', 29 'Vide ...', 10 empty, rest other links), 13 merged enacted days. Final
  re-parse of all 66 with the final code: only the spliced titles differ. Merged scratch build 211 acts, 3323 versions, 2435
  commits, check 0/0, --compare identical, audit_push clean (t2/build2.log); built history has no link text in any message.
- Not settled (not link text, left): 138 merged laws still have EMPTY titles (the reader needs a full stop before 'O
  PRESIDENTE'; e.g. lei-10741-2003 empty in 60-phase2 (first by name) though 99-batch7 has it); 3 laws whose parts differ only
  by capture typography or a hand-abbreviated '[...]' title (lei-13848-2019 in 17x, lei-14119-2021 in 17zp, lei-11977-2009 in
  17m; merged titles correct); page-garbled ementas kept as printed ('I nstitui', lc-155 in 16f).
- batch7's __main__ TITLE_FIXED wrapper for lc-200-2023 is now redundant (harmless).
- Task 2 (Lei 12.379/2011, Lei 6.437/1977, Lei 13.005/2014, LC 159/2017, LC 178/2021) NOT started (context). Pages pinned in
  the sixteenth session; LC 159/178 law keys exist in 99-batch7 (keep ACT_LAWS titles identical).
- PIDs (all mine, all exited; printed by run.py / regen.py in t2/regen-*.log, chk*.log, build*.log). Nothing running.

## State at handoff (batch 17, seventeenth session, 2026-11-01)
Task 1 done (above). Merged 211 acts, 3323 versions, 2435 commits, check 0/0, --compare identical, audit clean. Nothing running.
DATED RE-CHECK (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026 - not before. Next: Task 2 candidates (sixteenth-session
list below); 17q reproducibility; empty titles (decision: they change commit messages).

## State at handoff (batch 17, sixteenth session, 2026-11-01)
Task 1 done (zd art. 7; batch7 LC 200 title; shared provision-day decisions) with 14 parts re-PUBLISHed (decision/title wording
only). Part zr installed with .PUBLISH. Merged 211 acts, 3323 versions, 2435 commits, check 0/0, --compare identical, audit clean.
README rows + jurisdiction.json (211 acts) current. All runs through .tmp/run.py / pipe.sh / reparse.sh / reparse_all.py at
BelowNormal (cpu gate), at most 2 at once (a fetch beside a parse), never two parses; every PID this session was printed by run.py
in its log (t1/reall*.log, t1/re2.out, .tmp/*-zr*.log, *-re.log, t1-build.log, final16-build.log); all mine, all exited. Nothing running.
DATED RE-CHECK (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026 - not before.
Left out / unsettled: Lei 9.782 art. 8º-A; Lei 10.931; Lei 10.522 art. 32 quoted § 2º; Lei 12.462 art. 63 § 17; + Lei 11.738 and
Lei 12.009 (above).
Decision wanted: page link text at the start of law titles across parts (see Task 1 (b) above).
Next candidates (pages pinned): Lei 12.379/2011 (Sistema Nacional de Viação; Lei 14.273/2021 58 notes + MP 1.065/2021 36: reuse
part w's MP 1.065 / Lei 14.273 handling), Lei 6.437/1977 (+ compilado; MP 2.190-34 34 notes, Lei 9.695/1998 20, MP 116/1989),
Lei 13.005/2014 (PNE; 1 note, Lei 14.627/2023; ten-year term of art. 1 and its extension: read before modelling), LC 159/2017 and
LC 178/2021 (both law keys already in 99-batch7 with marker-free titles: keep ACT_LAWS titles identical to batch7's so the merged
build's commit messages do not change). Not pinned yet: Lei 6.360/1976, Lei 11.494/2007, Lei 9.424/1996, Lei 10.861/2004.

## Eighteenth session (2026-11-01): empty law titles filled (coordinator-approved Task 1) + part q reproducible (Task 2)
Scratch: ~/Documents/.gitlaw-scratch/brazil-b18/t3 (tools, before-install/ = every part + corpus.json before this
session's install, re-off/ re/ re-all/ re-q/ regenerated parts, logs). robots.txt read before the only fetch (archive.org:
Disallows /control/ /report/ only; web.archive.org/robots.txt 404). Only fetch: the six pinned ECR pages (fetch_ecr.py).
- titles.py: new ementa(after, rest): ementa_old (the old '(.*?\.) O PRESIDENTE' reading, first, so no title it gave changes),
  else ementa_more on after+rest: _FORMULA_MORE (any case 'O Presidente da República', bare 'PRESIDENTE DA REPÚBLICA', 'O
  PRESIDENT E', 'OS MINISTROS DA MARINHA', 'O Congresso Nacional decreta', 'A Mesa do Congresso Nacional' ...), _LEAD_MORE
  (remnant links: 'Fica sem efeito pelo ...', 'suspensa pelo ...', 'Vide texto compilado', 'e vigência', 'E feitos financeiros',
  'Estrutura Regimental (ANA)'), _NAV (cut at 'Não remover / Texto compilado / Up Down'), _TAIL (links and '(Redação dada ...)'
  at the end), a rewritten ementa -> its first sentence (the enacted wording, as 99-batch7 and 16g already gave it), trailing
  nickname '(LEI DOS PORTOS)' dropped. strip_links: 'P rodução de efeitos' too. TITLES_DUMP env = debug log of fallback cases.
  Readers (parse_proc, parse_codes, parse_phase2, parse_clt) call titles.ementa(after, head[+1500:+12000]); batch3's Ato
  Complementar reader falls back to ementa_more; parse.py ecr_title for the ECRs.
- Heading fixes (change enacted/published, allowed): parse_codes heading accepts 'LEI N o 10.677' (lei-10677 enacted 22.5.2003,
  lei-10825 22.12.2003, was 10.1.2002); parse_proc heading accepts no 'DE' before the day (LC 188/2021, LC 190/2022 now read).
- Cross-part: 99-batch5b's LGPD title = 50-codes' hand title (__main__ wrapper in parse_batch5b); parse_batch17 ACT_LAWS
  titles of lei-13465-2017 (17l) and lei-9984-2000 (17zf) made the full ementa. Result: 0 merged empty titles (was 128 +
  lei-13988 in 17q); 249 law-title entries in 66 parts + 5 ECR titles in corpus.json. 16 laws still differ across parts only by
  capture typography ('n o' vs 'nº', dashes) or batch 17 hand '[...]' abridgements (lei-12334 17zd, lei-13848 17x) - pre-existing,
  not empty, left.
- Method: regen.py --off (runp --off = ementa_more returns '') vs on, all 81 parts with the final code (re-all): law differences
  vs installed = filled empties + the listed fields only, plus known drift (70-clt dl-6053-1943 extra in a fresh parse, 80-proc
  dl-6109-1943 published None in a fresh parse: NOT installed); decisions/acts unchanged vs last session's regen (13b/13e have
  the same 7 pre-existing 'Del' decision drift as 13a/c/d). splice3.py installed laws only; splice_ecr.py the 5 ECR titles.
  chk3.py (8 file checks before/after, 66 parts): identical except pubgap no longer flagging lei-10825's wrong date.
- Task 2: part q's hand entries VIGENCIA_FIXED lei-13988-2020 and MP_LAPSE mp-1160-2023 sat inside part s's (_LCSE) block;
  moved back into the _LCADIN block. Fresh parse of q = installed (acts, laws, decisions; only sources request counts / pin
  notes drift); 17s and 17u fresh parses unchanged by the move.
- Merged scratch build (t3/build.log): 211 acts, 3323 versions, 2435 commits, check 0/0, --compare identical, audit_push clean
  main + futuro. PUBLISH appended for the 66 parts and the folder PUBLISH (corpus.json ECRs).
- PIDs (all mine, all exited): run.py children 44860 (failed: CRLF list), 25536, 36184, 28716, 27788, 27544, 44164 (fetch), 50640,
  49228 (checks), build (t3/build.log); regen children in t3/regen-*.log. Nothing running.
- Gotcha: backslashes in heredoc Python string literals were collapsed (wrote \x08 into titles.py once; fixed): use Edit.
- Task 3 NOT started (context). Notes for it: Lei 13.005 page has 'Vide Lei 14.934/2024' (term extension, no words changed:
  a note law, not a wording), 'Incluído pela Lei 14.627/2023' (1 note), 'Vide ADI 5668'; the Anexo is large.

## State at handoff (batch 17, eighteenth session, 2026-11-01)
Tasks 1 and 2 done (above). Merged 211 acts, 3323 versions, 2435 commits, check 0/0, --compare identical, audit clean. Nothing
running. DATED RE-CHECK (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026 - not before. Next: Task 3 candidates (Lei
12.379/2011, Lei 6.437/1977, Lei 13.005/2014, LC 159/2017, LC 178/2021; pages pinned; see sixteenth-session handoff).

## Nineteenth session (2026-11-01): Task 3 candidates, parts zs, zt, zu
robots.txt read at start (archive.org: Disallows /control/ /report/ only; web.archive.org/robots.txt 404). Fetching: archive.org only
(`iaonly.py laws` for the five acts: 10 new pins; `missing` 0; Lei 14.934/2024 was already pinned). Configured in parse_batch17: ALL_ACTS
+ PARTS zs (PNE, LSNV), zt (Lei 6.437), zu (LC 159, LC 178), ACT_DAY, ACT_LAWS (LC 159/178 entries = 99-batch7's title AND url
'leis/lcp/Lcp159.htm' / 'Lcp178.htm', so merged messages do not change).

## 99-batch17zs - PUBLISHed 2026-11-01 (nineteenth session)
Lei 13.005/2014 (PNE, 3 versions 2014-06-26 .. 2026-01-01) and Lei 12.379/2011 (SNV, 4 versions 2011-01-07 .. 2022-02-07).
- PNE Anexo: the reader stops at the signature; paragraphs wrapper (page l13005) appends pne_annex(): units 'anexo' (ANEXO / METAS E
  ESTRATÉGIAS) and anexo-meta-01..20 (labels 'Meta N', 'N.M)'); P.unit_kind -> 'annex', P.unit_label -> 'Anexo' / 'Meta N do Anexo'
  (a comma in the label made commit label lists ambiguous); B15.TABLES count popped for l13005 (tables are in Meta 7; own decision).
- PNE term (user instruction: extension = note, not a version; lapse = version on the day after the term): B9.REPEALS[PNE] =
  2026-01-01 credited lei-14934-2024, added by B8.EXTRA_LAWS with a `note` (printed in the commit instead of the standard line). The
  month 26.6-25.7.2024 between the ten-year term and the extension is NOT a gap (decision + OPEN_ITEMS). build_act wrapper rewords
  the REPEAL CHECK line for the PNE (term, not repeal; 'anexo: only in replay' is the consolidated() filter of unpunctuated units).
- LSNV: SPAN_FIX _W1065S (MP 1.065 vs Lei 14.273, part w model): art. 10 I MP line ends 6.2.2022 'repealed'; restored copies skipped
  (art-10 I nth1, art-22 caput nth1, c) nth1, d) nth1, § 2º nth1, art-24 caput nth2); art-24 MP caput ends 6.2.2022; art-22 a)/b) MP
  lines end with the lapse 7.2.2022 (2011 wording back). Lei 14.273 2023 promulgated parts do not touch 12.379 (read).
- Part sha cc0c38dc (0 moves); merged 213 acts, 3330 versions, 2439 commits, check 0/0, compare identical, audit clean
  (final19-zs-build2.log, after rows-zs.json docs + a jurisdiction.json note on the PNE's term).

## 99-batch17zt - PUBLISHed 2026-11-01 (nineteenth session)
Lei 6.437/1977 (lei-das-infracoes-sanitarias), 7 versions 1977-08-24 .. 2023-09-12, vs l6437compilado (0 diffs, 0 problems).
- Hand (scoped `_LIS`): MP_PENDING mp-2190-2001 (6.437 text), P.PUBLISHED_FIXED lei-9695-1998 = 21.8.1998 ('publicado pelo D.O.U.'
  not read by page_info's regex) + EXTRA decision; OPEN_ITEMS (MP 116 -> Lei 7.967 same words; Lei 9.005 converted MP 834).
- Part sha 5f486783 (0 moves); merged 214 acts, 3337 versions, 2445 commits, check 0/0, compare identical, audit clean
  (final19-zt-build.log, after rows-zt.json docs).
- FOUND (not changed yet): 99-batch8 dates Lei 9.695's change of the Crimes Hediondos (art. 1) 1998-08-20 with published None (same
  page slip); the merged law entry now reads published 1998-08-21 (17zt sorts first). Fix = PUBLISHED_FIXED in batch8's run + re-verify.

## 99-batch17zu - PUBLISHed 2026-11-01 (nineteenth session)
LC 159/2017 (lei-do-regime-de-recuperacao-fiscal, 5 versions 2017-05-22 .. 2024-05-17) and LC 178/2021 (lei-do-plano-de-equilibrio-fiscal,
3 versions 2021-01-14 .. 2025-01-14); own consolidated pages; law entries lc-159/lc-178 = 99-batch7's (checked equal, also lc-206/lc-212).
- NOTE_FIX (scoped) 'Lei Complementar nº 189, de 2021' -> 2022 (hrefs.py: Lcp189.htm#art2). EXPLAINED LC178 art-12/13/16 = _DOTTED.
- Part sha 280fbbd2 (0 moves); merged 216 acts, 3345 versions, 2449 commits, check 0/0, compare identical, audit clean
  (final19-zu-build.log, after rows-zu.json docs). Benign flags listed in the PUBLISH.

## 99-batch8 re-PUBLISHed + 99-batch17zt re-PUBLISHed (nineteenth session)
- batch8/parse_batch8.py: P.PUBLISHED_FIXED lei-9695-1998 = 21.8.1998 when the Hediondos act runs ('publicado pelo D.O.U.' slip).
  reparse_all baseline = installed (1ca68ec0); fix e857b16d (x2): only the Hediondos version 1998-08-20 -> 21, the law's published
  day and one decision. 8 file checks identical except that day (scratch .gitlaw-scratch/brazil-b19: base/, fix/, fix2/, b8-chk-*.txt).
- zt: the EXTRA decision duplicated proc's automatic PUBLISHED_FIXED decision: removed; part sha dc3c8fab.
- Merged after both: 216 acts, 3345 versions, 2448 commits (Lei 9.695's two acts now one commit), check 0/0, compare identical, audit
  clean (final19-b8-build.log).

## 99-batch17zv - PUBLISHed 2026-11-01 (nineteenth session)
Lei 7.853/1989 (lei-da-pessoa-com-deficiencia-de-1989, 9 versions, vs l7853compilado), Lei 9.807/1999 (lei-de-protecao-a-testemunhas,
2), Lei 10.861/2004 (lei-do-sinaes, 3). Pages pinned (`iaonly.py pages`: l7853(+compilado), l9807, l10861, l9456; l10973 pinned with
pinat.py ts 20260901034100 because pick() gave NO CAPTURE); `laws` (10 new) + `missing` (0).
- Lei 7.853 art. 10: MP 437 (30.7.2008) wording ends 29.8.2008 (MP 439 art. 4), Lei 8.028's restored copy (nth 1) starts 29.8.2008
  credited mp-439-2008 (EXTRA_LAWS, MP_PENDING mp-437 text scoped); Lei 11.958 (29.6.2009) = MP 437's words.
- Lei 9.807 art. 17 BARE_TEXT (_BARE_RX9807; 'l9807' in _BX + own decision).
- MP 1.370/2026 (SINAES art. 5 § 12) MP_PENDING: last capture of mpv1370.htm 22.10.2026, term ends ~30.10.2026 (recess 18-31.7
  suspends it). RE-CHECK when archive.org has a capture after 30.10.2026 (cdxlist _ato2023-2026/2026/mpv/mpv1370.htm): converted ->
  CONVERTED via the MP page; lapsed -> MP_LAPSE (Ato Declaratório) and a version on the day after the term.
- Part sha 149e561a (0 moves); merged 219 acts, 3359 versions, 2456 commits, check 0/0, compare identical, audit clean
  (final19-zv-build.log, after rows-zv.json docs).

## LIVE-HOST LIMIT (coordinator, 2026-11-01 ~09:30, BRIEF.md) - read in the nineteenth session
Any host without a Crawl-delay: <= 1 request / 3 s and ~5,000 / day machine-wide; archive.org through the shared client only (now
<= 1 request/s machine-wide, ArchiveDailyCap 20,000/day); stop for good on any challenge page. This session's fetches all used the
shared client (iaonly.py -> fetch_batch5 -> wayback.get / wayback.captures; cdxlist/cdxpre -> wayback.captures; pinat.py -> refetch
via the same client); one LexML /urn record via lexml1.py (6 s spacing, LexML Crawl-delay 5); robots.txt curls (1 each). No
challenge page seen. Keep using only these paths; never add a direct curl loop without a 3 s sleep and a daily count.

## 99-batch17zw - PUBLISHed 2026-11-01 (nineteenth session)
Lei 10.973/2004 (lei-de-inovacao, 7 versions 2004-12-03 .. 2024-10-17) and Lei 9.456/1997 (lei-de-protecao-de-cultivares, 2 versions
1997-04-28 .. 2018-04-18). l10973 pinned with pinat.py (ts 20260901034100).
- LInov: NOTE_FIX '(Redação pela Lei nº 13.243, de 2016)' x40 (scoped); act flag center_headings False; paragraphs wrapper (page
  l10973) moves '(NR)' closing lines the capitals rule took for headings back into arts. 24/25 (LINOV_FIXED decision); EXPLAINED art-24.
- LPC: ACT_DAY 28.4.1997 from LexML (lexml1.py; robots read: /urn allowed, Crawl-delay 5); SPAN_FIX _P9456 art-10 V and art-14-a start
  18.4.2018 (Lei 13.606 art. 27 vetoed + promulgated).
- Part sha cd3846f4 (pre-effects 3b9ddb4c, 0 moves); merged 221 acts, 3368 versions, 2460 commits, check 0/0, compare identical,
  audit clean (final19-zw-build.log, after rows-zw.json docs).

## State at handoff (batch 17, nineteenth session, 2026-11-01)
Parts zs, zt, zu, zv, zw installed with .PUBLISH (12 acts, 37 versions): PNE 13.005 (+ Anexo; term to 31.12.2025, lapse version
1.1.2026, Lei 14.934 as a note), SNV 12.379, Lei 6.437, LC 159, LC 178, Leis 7.853, 9.807, 10.861, 10.973, 9.456. 99-batch8
re-PUBLISHed (Lei 9.695 dated 21.8.1998). Merged 221 acts, 3368 versions, 2460 commits, check 0/0, --compare identical, audit_push
clean; README rows + jurisdiction.json (221 acts) current. All runs through .tmp/run.py / pipe.sh / reparse_all.py at BelowNormal (cpu
gate), one at a time, never two parses; every PID was printed by run.py in its log (.tmp/*-zs..zw*.log, final19-*.log,
.gitlaw-scratch/brazil-b19/*.log); all mine, all exited. Nothing running.
DATED RE-CHECKS: MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, SINAES art. 5 § 12) as soon as archive.org
has a capture of _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026 (its term end).
Left out / unsettled (unchanged): Lei 9.782 art. 8º-A; Lei 10.931; Lei 10.522 art. 32 quoted § 2º; Lei 12.462 art. 63 § 17; Leis
11.738 and 12.009 (not built).
Next candidates (paths found in the local index, captures exist on archive.org): Lei 7.802/1989 (agrotóxicos, repealed by Lei
14.785/2023: needs a pre-repeal capture via pinat.py + B9.REPEALS), Lei 14.785/2023, Lei 11.947/2009 (PNAE), Lei 10.820/2003
(consignado), Lei 9.612/1998 (rádio comunitária), Lei 12.871/2013 (Mais Médicos; heavy MPs, incl. MP 1.370), Lei 13.979/2020 (COVID,
temporary). Not pinned yet: Lei 6.360/1976, Lei 11.494/2007, Lei 9.424/1996.

## Twentieth session (2026-11-01): Task 1 PNE gap, then Task 2 candidates
robots.txt read at start (archive.org: Disallow /control/ /report/ only; web.archive.org 404). Fetching: archive.org only, through
the shared client (iaonly.py, pinat.py, cdxlist.py). Scratch for reads: .gitlaw-scratch/brazil-b20.

### 99-batch17zs re-PUBLISHed (coordinator decision: model the PNE's term gap)
- parse_batch17: pne_term_gap() (called from the PNE branch of the build_act wrapper): lapse version 2024-06-26 (all units
  removed, credited lei-13005-2014, version note), back 2024-07-26 (2023-07-20 units, credited lei-14934-2024); 2026-01-01 end
  unchanged (B9.REPEALS). _N14934 note reworded for both of 14.934's commits; REPEALS decision and OPEN_ITEMS updated. Lei 14.934
  read (lawtxt): art. 2 on publication, nothing retroactive.
- pipe.sh zs (t20-zs-pipe.out): parse x2 sha 0acc6bbf, 0 moves, checks as before; merged 221 acts, 3370 versions, 2462 commits,
  check 0/0, compare identical, audit clean; headyear clean (t20-hy.log). Installed; docs.py rows-zs.json (5 versions) +
  jurisdiction.json build text (gap named, '(3)' -> '(5)'). PUBLISH appended.

### 99-batch17zx - PUBLISHed 2026-11-01 (twentieth session)
Lei 7.802/1989 (lei-dos-agrotoxicos-de-1989, short LAgro), 3 versions 1989-07-12 .. 2023-12-28. Page id l7802-2023 = archive.org
capture 20231218091920 (pinat.py). Lei 14.785/2023 pinned as page l14785 (capture 20261004152908; also the next candidate act).
- B9.REPEALS 2023-12-28 credited lei-14785-2023 (B8.EXTRA_LAWS entry, ementa as title); OPEN_ITEMS (regulations).
- SPAN_FIX keep: art-07 § 2º II d) (stale_fix twin rule skipped it; found with .tmp/dbg8.py, which prints a stack trace where a
  line gets skip=True). Lei 9.974 art. 7 vetoed -> LINDB 22.7.2000.
- Part sha 2597bf51 (0 moves); merged 222 acts, 3373 versions, 2465 commits, check 0/0, compare identical, audit clean
  (zx-build.log); installed; docs.py rows-zx.json + jurisdiction build text (2023 repeals list).
- Pinned for the next parts: l11947 (20261024010406), l10820 (20261004162912), l9612 (20261021095939); PAGES entries added.
  NOTE: lawtxt.py with an empty needle prints the page at every position (a 3.4 GB log was written and deleted): omit the needle.

### 99-batch17zy - PUBLISHed 2026-11-01 (twentieth session): Lei 9.612/1998 (lei-da-radiodifusao-comunitaria, LRC), Lei 11.947/2009 (lei-da-alimentacao-escolar, PNAE)
- iaonly laws: 13 pinned, missing 0. Hand (block `_LRC, _LPNAE`): MP_PENDING mp-2143-2001 (2.143-32 -> 2.216-37 chain);
  VIGENCIA_FIXED lei-15255-2025 = 1.1.2026 (first financial year after DOU 11.11.2025); SPAN_FIX _W14734: Lei 14.734/2023 (LINDB
  7.1.2024) vetoed art. 17 XI + a)-i) and art. 20 IV, promulgated DOU 22.5.2024: '(VETADO)' lines 7.1.2024-22.5.2024, words from
  22.5.2024. OPEN_ITEMS (ADI 2566 'Vide' only; Lei 14.734 art. 2; MP 455 text before conversion).
- zy: pipe.sh (t20-zy-pipe.out): parse x2 sha 05f53150, 0 moves; flags benign (art. 30 quoted §§ 1º, LRC art. 6-B caput revoked by
  Lei 15.182 whose revocation of §§ 1º-2º was vetoed, quoted amendments in arts. 30-32); LRC 7 versions, PNAE 11; merged 224 acts, 3391
  versions, 2481 commits, check 0/0, compare identical, audit clean; installed, docs.py rows-zy.json, PUBLISH written.

## State at handoff (batch 17, twentieth session, 2026-11-01)
99-batch17zs re-PUBLISHed (PNE term gap: out 26.6.2024, back 26.7.2024 credited Lei 14.934, out again 1.1.2026; 5 versions);
99-batch17zx (Lei 7.802/1989, 3 versions) and 99-batch17zy (Leis 9.612/1998, 11.947/2009; 18 versions) PUBLISHed. Final merged build
of the installed folder after all docs (final20-build.log): 224 acts, 3391 versions, 2481 commits, check 0/0, --compare identical,
audit_push clean on main and futuro; README rows + jurisdiction.json (224 acts) current. All runs through .tmp/run.py / pipe.sh at
BelowNormal behind the cpu gate, one parse at a time; PIDs printed in each log (t20-*.log, zx-*.log, zy-*.log, final20-build.log);
all mine, all exited (one shell of mine stopped by its own task id after lawtxt.py was given an empty needle; no process left).
Nothing running.
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv) once archive.org has a capture
of _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026.
Next candidates: Lei 14.785/2023 (agrotóxicos; page pinned as l14785, capture 20261004152908; 14 'Promulgação partes vetadas' notes:
vetoed parts promulgated DOU 22.5.2024 and 2.7.2025 (arts. 59-62 taxa), 13 Lei 15.070/2024 rewrites + 2 revocations; law entry
lei-14785-2023 already exists via part zx's EXTRA_LAWS: keep label/title/url equal), Lei 10.820/2003 (consignado; pinned l10820,
heavy: MPs 656, 681, 719, 922, 1.106, 1.164, 1.292 - several 'Vigência encerrada'), Lei 12.871/2013 (Mais Médicos; MP 1.370),
Lei 13.979/2020 (COVID, temporary). Not pinned yet: Lei 6.360/1976, Lei 11.494/2007, Lei 9.424/1996.

## 99-batch17zz - PUBLISHed 2026-11-01 (twentieth session, after the coordinator's 'continue' message)
Lei 14.785/2023 (lei-dos-agrotoxicos, short LAgro23), 4 versions 2023-12-28 .. 2025-07-02, page l14785 (capture 20261004152908).
- _T14785 (ementa) moved above ACT_DAY_ALL so ACT_LAWS (part zz) and part zx's EXTRA_LAWS share it: law entries checked equal.
  zx reparsed after the move: acts, laws, decisions identical; only sources' 'requests' counter differs (grows with every fetch),
  so the installed zx file was left as it is.
- SPAN_FIX _W14785: promulgations DOU 22.5.2024 (art. 4 § 5º V, 27 I-III, 28 + par. único, 29 § 2º, 30 § 2º) and DOU 2.7.2025
  (arts. 59 + §§ 1º-2º, 60, 61, 62 I): '(VETADO)' lines (skip False) to the promulgation, words from it. Lei 15.070 on publication
  24.12.2024. OPEN_ITEMS (regulations; art. 65's Anexo repeals of other laws).
- pipe.sh zz: sha 030ccdb7, 0 moves; flags = law text (art. 25 a) under four incisos: dupline 1 / overlap 6 SAME; '(revogado);'
  x3 Lei 15.070's wording); merged 225 acts, 3395 versions, 2485 commits, check 0/0, compare identical, audit clean; installed,
  docs.py rows-zz.json, PUBLISH; final merged build after docs (final20b-build.log): same counts, check 0/0, compare identical,
  audit clean.

## State at handoff (batch 17, twentieth session, end, 2026-11-01)
Parts this session: zs re-PUBLISHed (PNE gap), zx (Lei 7.802), zy (Leis 9.612, 11.947), zz (Lei 14.785). Merged 225 acts, 3395
versions, 2485 commits, check 0/0, --compare identical, audit_push clean (final20b-build.log); README rows + jurisdiction.json (225
acts) current. Nothing running; every PID mine and exited (logs t20-*, zx-*, zy-*, zz-*, final20*).
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv) once archived after 30.10.2026.
Next (coordinator order): Lei 10.820/2003 (consignado; page pinned l10820, PAGES entry present, not configured: MPs 656/2014,
681/2015, 719/2016, 922/2020, 1.106/2022, 1.164/2023, 1.292/2025 - several 'Vigência encerrada', so MP_LAPSE days from the Atos
declaratórios; Lei 15.179/2025 59 notes), then Lei 12.871/2013 (Mais Médicos; MP 1.370), Lei 13.979/2020 (COVID, temporary), and
the unpinned Leis 6.360/1976, 11.494/2007, 9.424/1996.

## Twenty-first session (2026-11-01): Lei 10.820, then the coordinator's list
robots.txt read at start (archive.org: Disallow /control/ /report/ only; web.archive.org 404). Fetching: archive.org only,
through the shared client (iaonly.py). Scratch: .gitlaw-scratch/brazil-b17 (zza-*.json, eff/), page dump .gitlaw-scratch/l10820.txt.

### 99-batch17zza - PUBLISHed 2026-11-01 (twenty-first session): Lei 10.820/2003 (lei-do-credito-consignado, LCons)
- iaonly laws (19 cited, 6 new pins), missing 0. Hand block `_LCONS`: CONVERTED_FIX mp-719-2016 (page 'Convertida na Lei
  13.313' without nº) and mp-1292-2025 (page captured 11.6.2026 has no link; Lei 15.179 heading 'Conversão da MP 1.292');
  VIGENCIA_PROVISION mp-656-2014 arts. 1-5 = 7.11.2014 (art. 55 II, 30 days; MP art. 9); SPAN_FIX art. 4 § 1º (Lei 13.097
  vetoed MP 656's change: MP line ends 20.1.2015, 2003 'Vide' copy 20.1.2015-13.7.2015), art. 2 IV MP 681 plain copy ends
  22.10.2015, art. 6 § 7º Lei 14.431 plain copy ends 20.6.2023; EXPLAINED art-02/art-06; OPEN_ITEMS (MP 130 pre-text, Vides).
- MP 922/2020 lapse = batch9's global MP_LAPSE (30.6.2020); the only lapsed MP on the page ('Vigência encerrada' x10).
- pipe.sh zza (t21-zza-pipe2.out): sha 045a1b07 x2, 0 moves; flags benign (PUBLISH lists them); headyear unchanged vs t20
  (t21-hy.log). Merged 226 acts, 3413 versions, 2492 commits, check 0/0, compare identical, audit clean. Installed; docs.py
  rows-zza.json; PUBLISH written. PIDs (all mine, exited): printed in t21-*.log / zza-*.log.

### Lei 12.871/2013 (Mais Médicos) - LEFT OUT this session
Medida Provisória 1.370/2026 (19.6.2026; 30 notes on l12871, capture 20.10.2026) changes much of the Lei; its term ended about
30.10.2026 and archive.org has no capture of mpv1370.htm after 30.10.2026 (CDX from=20261030: 0 rows, 1.11.2026), so whether it
was converted (and with which words) or lapsed cannot be read. Build it with the MP 1.370 re-check (part zv).

### Lei 13.979/2020 (COVID) - LEFT OUT
Pinned (l13979, capture 20261023004148), not configured. Its end cannot be settled from the official page: art. 8 ties it to
Decreto Legislativo 6/2020 (to 31.12.2020), but STF ADI 6625 kept arts. 3 to 3-J in force after that (page prints the Lei
unstruck); ADIs 6341/6343/6347/6351/6353 and ADPFs 714/715/718/754 condition or suspend parts (MP 928's art. 6-B), and MPs
926/927/928/951 lapsed ('Vigência encerrada'). Not a fixed-term lapse with one day.

### 99-batch17zzb - PUBLISHed 2026-11-01 (twenty-first session): Lei 6.360/1976 (lei-da-vigilancia-sanitaria-de-medicamentos, LVSM)
- Pages pinned (`iaonly.py pages`): l13979, l6360 (20261019130600), l11494 (20261018234644), l9424 (20261015110252).
  iaonly laws (14 cited, 10 new), missing 0. ACT_DAY 28.12.1976 (95 days after DOU 24.9.1976, pre-LC 95 count as Lei 9.537).
- Hand (block `_LVSM`): MP_PENDING mp-2190-2001 (6.360 text: art. 9, art. 15 revokes art. 82); NOTE_FIX 'Decreto nº 6.480'
  -> Lei 6.480; B8.LABEL_FIX l6360 art. 17-A 'I - benefícios' -> 'II -'; LAW_FIELD_FIX lei-9782-1999 url = part zb's
  (lowercase page) - lawcmp.py (.gitlaw-scratch/lawcmp.py <part> <name>) compares a candidate's law entries with every part.
- pipe.sh zzb (t21-zzb-pipe2.out): sha 9624198d x2, 0 moves, 0 diffs; merged 227 acts, 3427 versions, 2504 commits, check 0/0,
  compare identical, audit clean; headyear unchanged (t21-hy2.log). Installed; docs.py rows-zzb.json; PUBLISH written.

### 99-batch17zzc - PUBLISHed 2026-11-01 (twenty-first session): Lei 11.494/2007 (lei-do-fundeb-de-2007, Fundeb07)
- Page l11494-2020 = archive.org capture 20201215182439 (pinat.py; CDX until 20201231: the ~3 KB rows are bot pages), check
  page l11494 = today's page (unstruck: preamble, Seção II heading, art. 12 caput + I-III). iaonly laws: 7 cited, 3 new.
- Partial repeal (no whole-act REPEALS): lifespans wrapper (cx.act == _LF07) ends every line but preamble, art. 12 and art. 12's
  heading group (found by the 'Da Comissão Intergovernamental ...' name line) on 1.1.2021 (lei-14113-2020, 'act-repealed');
  art. 12 §§ on 28.12.2021 (lei-14276-2021: art. 53 reworded 'ressalvado o caput do art. 12', retroactive wording -> publication
  day). B8.EXTRA_LAWS lei-14113-2020 (= ACT_LAWS_ALL) and lei-14276-2021 (= part zm's record). Decision _W53 goes through
  EXTRA (B5.EXTRA_DECISIONS is cleared by batch5b's writer). OPEN_ITEMS: MP 339 pre-text, Anexo formulas (images).
- Checks: .gitlaw-scratch/prerepeal.py (version before 1.1.2021 vs l11494-2020 unstruck: 0 differ); parse consolidated vs
  today's page 0 differ. pipe.sh zzc (t21-zzc-pipe2.out): sha 81ef8146 x2, all checks 0; merged 228 acts, 3437 versions, 2509
  commits, check 0/0, compare identical, audit clean; headyear unchanged (t21-hy3.log). Installed; docs.py rows-zzc.json;
  jurisdiction.json build text names the partial repeal; PUBLISH written.

### 99-batch17zzd - PUBLISHed 2026-11-01 (twenty-first session): Lei 9.424/1996 (lei-do-fundef, Fundef)
- iaonly laws: 5 cited, 5 new; MP 173/2004 pinned with `iaonly.py gap law:mp-173-2004 <url>` (ts 20261006130027).
- Hand (block `_LFUNDEF`): lifespans wrapper moves the 'Revogado pela Lei 11.494' ends (21.6.2007) to 1.1.2007 credited
  mp-339-2006 (MP 339 art. 48 'a partir de 1º de janeiro de 2007', DOU 29.12.2006); SPAN_FIX art. 4 § 5º start 17.3.2004 credited
  mp-173-2004 with by_provision (keeps the anachronism check quiet; batch15 precedent); VIGENCIA_FIXED lei-10832-2003 = 1.1.2004
  (first day of the next financial year); B8.EXTRA_LAWS mp-339-2006, mp-173-2004 (from the MPs' pages); decisions via EXTRA.
- pipe.sh zzd (t21-zzd-pipe4.out): sha 222503bb x2, all checks 0; merged 229 acts, 3442 versions, 2514 commits, check 0/0,
  compare identical, audit clean. headyear (t21-hy4.log): only the two new MP pins, false positives (headings 'DE 16 DE MARÇO
  2004' / 'DE 28 DE DEZEMBRO 2006' lack 'DE' before the year; pages read). Installed; docs.py rows-zzd.json; PUBLISH written.
- Re-check: part zz reparsed with the session's parser + effects_fix: laws, acts, applies, decisions identical to the installed
  file (only sources' request counter differs, as before).

## State at handoff (batch 17, twenty-first session, 2026-11-01)
Parts zza (Lei 10.820/2003, 18 versions), zzb (Lei 6.360/1976, 14), zzc (Lei 11.494/2007, 10; repealed 1.1.2021 except art. 12,
§§ gone 28.12.2021), zzd (Lei 9.424/1996, 5) PUBLISHed. Final merged build of the installed folder after all docs
(final21-build.log): 229 acts, 3442 versions, 2514 commits, check 0/0, --compare identical, audit_push clean on main and futuro;
README rows + jurisdiction.json (229 acts; Lei 11.494's partial repeal named in the build text) current. All runs through
.tmp/run.py / pipe.sh at BelowNormal behind the cpu gate, one parse at a time; every PID printed in its log (zza-*, zzb-*, zzc-*,
zzd-*, t21-*, final21-build.log); all mine, all exited. Nothing running.
LEFT OUT: Lei 12.871/2013 (MP 1.370/2026 outcome unreadable: no capture after its term) - build it together with the MP 1.370
re-check; Lei 13.979/2020 (end of the act set by STF ADI 6625 and other rulings, not one fixed day).
DATED RE-CHECKS: MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once archive.org has a
capture of _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026 (none on 1.11.2026).
Coordinator's list is done (built or left out with reasons). Next: whatever the coordinator names.

## Twenty-second session (2026-11-01): fresh ranked list, parts zze, zzf, zzg, ...
robots.txt read at start (archive.org: Disallow /control/ /report/ only; web.archive.org 404). Fetching: archive.org only, through
the shared client (iaonly.py pages/laws/missing). Scratch: .gitlaw-scratch/brazil-b22 (trial parses, cfg1.py, lawfind.py <law key>...
= every installed part's record of a law). Per-part pipeline: pipe.sh (scratch brazil-b17 as before).
Fresh ranked list (installed slugs and titles checked; path = local CC index file, read from disk, no request):
 1 LC 109/2001 previdência complementar [zze]          2 LC 108/2001 previdência complementar pública [zze]
 3 LC 140/2011 cooperação ambiental [zzf]               4 Lei 9.709/1998 plebiscito/referendo [zzf]
 5 LC 179/2021 autonomia do BC [zzg]                    6 Lei 14.286/2021 mercado de câmbio [zzg]
 7 Decreto-Lei 200/1967 organização da Administração Federal (Decreto-Lei/Del0200.htm)
 8 LC 80/1994 Defensoria Pública (leis/lcp/lcp80.htm)   9 LC 75/1993 Estatuto do MPU (leis/lcp/lcp75.htm)
10 Lei 12.351/2010 pré-sal/partilha (_ato2007-2010/2010/lei/l12351.htm)   11 Lei 14.134/2021 Lei do Gás (_ato2019-2022/2021/lei/l14134.htm)
12 Lei 8.625/1993 LONMP (leis/l8625.htm)   13 Lei 14.129/2021 Governo Digital   14 Lei 12.813/2013 conflito de interesses
15 Lei 12.865/2013 arranjos de pagamento   16 Lei 8.437/1992 + Lei 9.494/1997 (tutela contra o Poder Público)
17 Lei 12.618/2012 Funpresp   18 Lei 14.601/2023 Bolsa Família   19 Lei 10.848/2004 comercialização de energia (no path in the
local index: cdxlist leis/2004/l10.848.htm first)   20 environment: Lei 9.966/2000 (óleo), Lei 7.661/1988 (costeiro), Lei 11.959/2009
(pesca), Lei 5.197/1967 (fauna), Lei 7.735/1989 (Ibama), Lei 11.516/2007 (ICMBio)   21 energy: Lei 14.300/2022, Lei 10.438/2002,
Lei 9.991/2000, Lei 9.847/1999   22 banking: LC 130/2009, Lei 10.214/2001, Lei 13.506/2017, Lei 8.929/1994 (CPR), Lei 13.775/2018
23 public administration: Lei 8.159/1991, Lei 9.491/1997, Lei 13.334/2016; LC 35/1979 (LOMAN), Lei 5.010/1966.
Law records that already exist in other parts must be copied exactly (lc-140-2011 = 99-batch10, lc-179-2021 = 13f,
lei-14286-2021 = 13f/17g): done for zzf/zzg (url 'leis/LCP/Lcp140.htm' etc.).

### 99-batch17zze - PUBLISHed: LC 109/2001 (lei-da-previdencia-complementar, LC109, 2 versions) + LC 108/2001
(lei-da-previdencia-complementar-do-setor-publico, LC108, 1). VIGENCIA_FIXED lc-213-2025 = 16.1.2025 (art. 13 III; its art. 6 =
LC 109 art. 38 III), scoped. Parse sha 85734907 x2, 0 moves, all checks 0; merged 231 acts, 3445 versions, 2517 commits, check 0/0,
compare identical, audit clean. headyear unchanged (t22-hy.log). rows-zze.json docs.
### 99-batch17zzf - PUBLISHed: LC 140/2011 (lei-da-cooperacao-ambiental, 1 version) + Lei 9.709/1998
(lei-do-plebiscito-e-do-referendo, 1). No notes on either page. sha d611ee6d, 0 moves; leakcheck 3/quotecheck 5 = LC 140 art. 20's
quoted Lei 6.938 text. Merged 233 acts, 3447 versions, 2519 commits, check 0/0, compare identical, audit clean.
### 99-batch17zzg - PUBLISHed: LC 179/2021 (lei-da-autonomia-do-banco-central, 1) + Lei 14.286/2021 (lei-do-mercado-de-cambio,
3 versions 2022-12-30 .. 2024-01-01; in force one year after DOU 30.12.2021 = 30.12.2022, as Lei 13.431's same clause).
Hand (_LCAMBIO, scoped): VIGENCIA_FIXED lei-14596-2023 1.1.2024 (art. 46 XI revokes art. 24 'na parte em que altera o art. 50 da
Lei 8.383'); SPAN_FIX art-24 'Parágrafo único. (Revogado).' (struck on the page with the caput; the reader had skipped it as
undated) -> skip False, ends 1.1.2024; EXPLAINED art-25 (_DOTTED). sha 778e93d9, 0 moves; leak 6/quote 15 = quoted amendments.
Merged 235 acts, 3451 versions, 2521 commits, check 0/0, compare identical, audit clean. PIDs: printed in t22-*.log, zz[efg]-*.log,
all mine, all exited.
### 99-batch17zzh - PUBLISHed: Lei 14.134/2021 (lei-do-gas, LGas, 1 version) + LC 75/1993 (estatuto-do-ministerio-publico-da-uniao,
LOMPU, 1; page capture 11.10.2026 carries no amendment note: OPEN_ITEMS says so). Pages pinned (`iaonly.py pages`, 5: l12351, l14134,
del0200, lcp80, lcp75); laws for zzh/zzi 4 new, missing 0. New paragraphs wrapper (after the zzg block): l14134 art. 46's quoted Lei
9.478 'Art. 2º ......' has no opening quote -> lines after art. 46's caput and before art. 47 filed under art-02 moved to art-46
(EXTRA decision); EXPLAINED art-46 (_DOTTED). sha 937dfa60, 0 moves; dupline/dupcheck 1 (quoted § 1º in two quoted articles), leak 6,
quote 15 = quoted amendments. Merged 237 acts, 3453 versions, 2523 commits, check 0/0, compare identical, audit clean.
### 99-batch17zzi - PUBLISHed: LC 80/1994 (lei-organica-da-defensoria-publica, LODP, 3 versions: 1994-01-13, LC 98 1999-12-06, LC 132
2009-10-08). Same wrapper: on lcp80 '<s>º</s>' / '<s>ª</s>' (56 ordinal signs coded with a strike tag, as on LC 132's own page) read as
plain (the 5 'ª' lines were MIXED and missing from the history before; 'º' lines were already restored by the reader). GOTCHA again:
a heredoc wrote r"\1" as \x01 - fixed with a byte replace; use the Edit tool for backreferences. sha 82976f26, 0 moves, all checks 0;
latecaput = 1994 §§ under LC 132 capita (page read: no notes, LC 132 left them). Merged 238 acts, 3456 versions, 2525 commits, check
0/0, compare identical, audit clean. headyear unchanged after the new pins (t22-hy2.log).
Next on the list: DL 200/1967 (page del0200 pinned; 326 notes, DLs 900/1969 (79), 2.300/1986 (76), 900/1968? (35; check the year
key), Lei 6.036/1974 (31), DL 991/1969 (27)), Lei 12.351/2010 (pinned l12351; 189 notes: Lei 15.164/2025 67, MP 1.291/2025 42, MP
1.226/2024 16, Lei 14.981/2024 16, MP 1.304/2025 6 - settle each MP's fate (conversion or Ato) before building).
### 99-batch17zzj - PUBLISHed: Lei 12.813/2013 (lei-de-conflito-de-interesses, LCI, 3 versions 2013-07-01 .. 2017-11-29; arts. 14-15
vetoed -> LINDB 45 days from DOU 17.5.2013) + Lei 8.437/1992 (lei-das-cautelares-contra-o-poder-publico, LCPP, 2 versions 1992-07-01,
2001-08-27). Pages pinned (`iaonly.py pages`, 4: l8437, l9494, l12813, l14129); laws 0 new; Ato pinned `iaonly.py gap
ato:adc-65-2017-mpv792 <95-rju's url>`. Hand (scoped): MP_LAPSE mp-792-2017 29.11.2017 with 95-rju's text word for word (the
mp-792-2017-fim record is built from it and must be equal: lawcmp caught a difference first); NOTE_FIX '2,180-35' (comma) x2;
MP_PENDING mp-2180-2001 (8.437 text). sha 61d9ce92, 0 moves, all checks 0; latecaput = art. 9 2013 items under the restored caput.
Merged 240 acts, 3461 versions, 2527 commits, check 0/0, compare identical, audit clean.

## State at handoff (batch 17, twenty-second session, 2026-11-01)
Parts zze, zzf, zzg, zzh, zzi, zzj PUBLISHed (11 acts, 19 versions): LC 109/2001, LC 108/2001, LC 140/2011, Lei 9.709/1998, LC
179/2021, Lei 14.286/2021, Lei 14.134/2021, LC 75/1993, LC 80/1994, Lei 12.813/2013, Lei 8.437/1992. Final merged build of the
installed folder after all docs (final22-build.log): 240 acts, 3461 versions, 2527 commits, check 0/0, --compare identical, audit_push
clean on main and futuro; README rows + jurisdiction.json (240 acts) current. lawcmp: every new part's law records equal the other
parts'. reparse.sh zzd zza zze zzg: equal except sources (pin counter growth, known). headyear unchanged (t22-hy3.log). All runs
through .tmp/run.py / pipe.sh / reparse.sh at BelowNormal behind the cpu gate, one at a time (never two parses); every PID was printed
in its log (t22-*.log, zz[e-j]-*.log, final22-build.log); all mine, all exited. Nothing running. No challenge page seen; archive.org
only (robots.txt read at start).
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once archive.org
has a capture of _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026.
Left out this session (configured or pinned, not built, reasons): Lei 9.494/1997 (page pinned l9494): its footer reads 'publicado no
D.O.U. de 24.12.1997' for a law of 10.9.1997 (conversion of MP 1.570-5) - settle the publication day (LexML /urn, Crawl-delay 5)
before building; MP 2.180-35 notes (9) + Lei 11.960 (1). Lei 14.129/2021 (pinned l14129; record exists in 99-batch6/17zi): staged
vigência (90/120/180 days by federative level, art. 55) and promulgated vetoed parts (DOU 11.6.2021) need a decision on the act's
first day before building. Not started: DL 200/1967 (pinned del0200, 326 notes), Lei 12.351/2010 (pinned l12351; MPs 1.226/2024,
1.291/2025, 1.304/2025: read each fate first).
Next on the ranked list after those: Lei 8.625/1993, Lei 12.865/2013, Lei 12.618/2012, Lei 14.601/2023, Lei 10.848/2004 (path via
cdxlist), environment (Leis 9.966, 7.661, 11.959, 5.197, 7.735, 11.516), energy (14.300, 10.438, 9.991, 9.847), banking (LC 130,
Leis 10.214, 13.506, 8.929, 13.775), public administration (Leis 8.159, 9.491, 13.334; LC 35/1979; Lei 5.010/1966).

## Twenty-second session, continued: coordinator decisions (1) Lei 14.129 by its federal stage, (2) Lei 9.494 from LexML
- LexML robots.txt read (Allow /urn /sru, Crawl-delay 5); one record via lexml1.py: lei-9494-1997 -> published 1997-09-11.
### 99-batch17zzk - PUBLISHed: Lei 9.494/1997 (lei-da-tutela-antecipada-contra-a-fazenda-publica, LTAFP, 3 versions 1997-09-11,
2001-08-27 (MP 2.180-35), 2009-06-30 (Lei 11.960)). sha 9f2b9835, 0 moves, checks 0 (quote 1 = quoted Lei 7.347 art. 16).
### 99-batch9 re-PUBLISHed: with the LexML day cached, a fresh parse dates Lei 7.347 art. 16 (Lei 9.494 art. 2) 1997-09-11 (was
1997-12-24), law record published 1997-09-11, + PUB_CORRECTED decision; nothing else differs (sources = pin growth). reparse_all twice
(scratch brazil-b22/b9, b9b): sha f7afc7c2 both; previous file kept at brazil-b22/b9/99-batch9.before.json.
### 99-batch17zzl - PUBLISHed: Lei 14.129/2021 (lei-do-governo-digital, LGD, 1 version 2021-06-28 = federal stage, art. 55 I);
promulgated arts. 32/35 (DOU 11.6.2021) precede that day -> stand from the first version, struck '(VETADO)' lines never in force
(EXTRA decision); later stages in OPEN_ITEMS. sha ed2c13c1, 0 moves, checks 0 (quote 12 = quoted amendments).
Final merged build (final22b-build.log, after docs rows-zzkl.json): 242 acts, 3465 versions, 2529 commits, check 0/0, --compare
identical, audit_push clean main + futuro. PIDs printed in t22-*.log / zzk-* / zzl-*; all mine, all exited. Nothing running.

## State at handoff (batch 17, twenty-second session, end, 2026-11-01)
Installed this session: zze, zzf, zzg, zzh, zzi, zzj, zzk, zzl (13 acts) + 99-batch9 re-PUBLISH (Lei 9.494 day). Merged 242 acts,
3465 versions, 2529 commits, check 0/0, compare identical, audit clean; README + jurisdiction.json (242 acts) current.
NEXT (coordinator order): Decreto-Lei 200/1967 (page del0200 pinned; configure act + ACT_DAY (its vigência clause: read) + ACT_LAWS;
`iaonly.py laws` for it; notecount: DL 900/1969 79, DL 2.300/1986 76, 'De 900/1968' 35 (check the key/year of those notes), Lei
6.036/1974 31, DL 991/1969 27, Lei 7.232/1984 12, Lei 6.650/1979 12, Lei 6.118/1974 11, Lei 6.946/1981 10, Lei 7.596/1987 8 ...; pre-1988
DLs credit by publication; check the compilado capture with cdxlist decreto-lei/del0200compilado.htm), then Lei 12.351/2010 (page
l12351 pinned): read first the fates of MP 1.226/2024 (16 notes), MP 1.291/2025 (42) and MP 1.304/2025 (6) - conversion (Lei 15.075/2024?
Lei 15.164/2025? Lei 15.269/2025 (= MP 1.304, see part z)) or lapse (Ato Declaratório pinned via iaonly gap) - and Lei 14.981/2024,
15.164/2025 vigência clauses, before building.
DATED RE-CHECKS (unchanged): MP 1.382/2026 on or after 29.11.2026; MP 1.370/2026 (and Lei 12.871) once archived after 30.10.2026.

## Twenty-third session (2026-11-01): DL 200/1967, then Lei 12.351/2010
robots.txt read at start (web.archive.org 404; archive.org Disallows /control/ /report/ only). Fetching: archive.org only, through
the shared client (iaonly.py laws/missing, cdxlist). Scratch: .gitlaw-scratch/brazil-b23 (cfg*.py edits, trial parses, page dumps,
tools/dbgvi.py = traces which build_act wrapper drops a line).

### 99-batch17zzm - PUBLISHed: Decreto-Lei 200/1967 (decreto-lei-200-de-1967, DL200, 22 versions 1967-03-15 .. 1998-05-18)
- No real compilado capture (del0200compilado: all ~3 KB bot pages) -> own page is the consolidated page. `iaonly.py laws` 31 new pins;
  law:dl-900-1968 (misprinted key) REMOVED from sources_batch17.json after the NOTE_FIX (headyear flagged it).
- Act dict center_headings False (h4/h5 headings); paragraphs wrapper (page del0200, after the zzh one): 'SEçãO' -> 'SEÇÃO' in the
  html; heading blocks starting 'SETOR '/'MINISTÉRIO ' go back into the article above (arts. 35, 39); bare 'Vide ...' tails dropped
  (_VIDE_TAIL); arts. 97/161 'Expressão substituída pelo DL 900' -> struck 1967 line read back from DL 900 art. 7 + new line with a
  'Redação dada' note (_DL200_SWAP). SPAN_FIX keep x4 art-039 VI lines (stale_fix twin rule dropped them); TEXT_FIX art. 39 ':,'.
- Hand: NOTE_FIX 'Decreto-Lei nº 900, de 1968' x35; VIGENCIA_FIXED dl-991-1969 30.10.1969. OPEN_ITEMS (art. 113, rectifications,
  Vide). Amenders all on publication except DL 991 / Lei 7.232 (60 days).
- pipe.sh zzm (brazil-b23/zzm-pipe2.out): sha 257059c9 x2, 0 moves; benign flags listed in the PUBLISH. Final merged build
  (final23-build.log): 243 acts, 3487 versions, 2551 commits, check 0/0, compare identical, audit clean. README row + jurisdiction.json
  (rows-zzm.json). reparse zzl/zzh equal (zzh sources counter only).

### 99-batch17zzn - PUBLISHed: Lei 12.351/2010 (lei-da-partilha-de-producao, LPartilha, 17 versions 2010-12-23 .. 2026-01-01 + 2031 futuro)
- MP fates (read first): MP 592/2012 lapse 13.5.2013 (batch10's shared MP_LAPSE); MP 1.226/2024 REVOKED by Lei 14.981/2024 art. 29 III
  (DOU 23.9.2024) -> P.MP_PENDING fate text (no generic 'revoked MP' fate exists); MP 1.291 -> Lei 15.164; MP 1.304 -> Lei 15.269.
- Block `_LPART` (end of parse_batch17, before SRC): PROMULGATED[_LPART] (Lei 12.734 vetoed parts, 15.3.2013), SPAN_FIX art-49 (IV, §
  1º + quoted 9.478 lines end 15.3.2013), art-58 § 5º (Lei 15.164), art-60-a (start 1.1.2026, end 1.1.2031 'term'), art-42-b II f)
  (start 30.11.2012 + MP 592 gap); B8.EXTRA_LAWS stf-adi-4917 = 99-batch10's record word for word; build_act_lp() (new outer
  build_act wrapper) inserts the ADI 4.917 no-words version 18.3.2013 for art-42-b/42-c; paragraphs wrapper appends the Anexo
  (polygon table, one line per row); B.EXPLAINED anexo.
- pipe.sh zzn (brazil-b23/zzn-pipe1.out): sha bd5d025e x2 (eff 04c547fb), 0 moves; benign flags in the PUBLISH. Final merged build
  (final23c-build.log, after rows-zzn.json docs + README futuro lines): 244 acts, 3504 versions, 2560 commits, check 0/0, compare
  identical, audit clean.

### 99-batch17zzo - PUBLISHed: Lei 8.625/1993 (lei-organica-nacional-do-ministerio-publico, LONMP, 1 version) + Lei 14.601/2023
(lei-do-programa-bolsa-familia, LPBF, 4 versions 2023-06-20 .. 2026-02-13)
- Pages pinned this session (`iaonly.py pages`, 4): l8625, l12618, l12865, l14601. notecount: l8625 0 notes; l14601 6 (15.077, 15.348);
  l12618 66 (MP 1.119/2022 29 -> Lei 14.463/2022 29, 13.183, MP 1.286/2024, 15.141); l12865 88 (12.973 24, 14.031 18, MP 930/2020 15,
  MP 627/2013 9, 14.943 7, MP 1.227/2024 5, MP 897/2019 2, MP 784/2017 1, LC 225/2026 1 ...).
- Lei 14.601 art. 34: _G14601 (arts. 30, 31 -> 1.1.2024) added to _GATES; SPAN_FIX by_provision art-04 § 3º, art-33 I -> 1.1.2024; EXTRA
  decision. Law record = 99-batch12's. sha 7dbd3dc3, 0 moves; benign flags in the PUBLISH. Final merged build (final23d-build.log):
  246 acts, 3509 versions, 2563 commits, check 0/0, compare identical, audit clean. README rows + jurisdiction.json (rows-zzo.json).

## State at handoff (batch 17, twenty-third session, 2026-11-01)
Installed this session: zzm (Decreto-Lei 200/1967, 22 versions), zzn (Lei 12.351/2010, 17 + Anexo), zzo (Leis 8.625/1993, 14.601/2023;
5) = 4 acts, 44 versions. Final merged build of the installed folder after all docs (final23d-build.log): 246 acts, 3509 versions, 2563
commits, check 0/0, --compare identical, audit_push clean on main and futuro; README rows (+ futuro lines for Lei 12.351 art. 60-A) and
jurisdiction.json (246 acts) current. lawcmp clean for every new part; reparse zzm/zzh/zzl/zzn equal (sources counter only). headyear
unchanged (t23-hy3.log; misprinted pin law:dl-900-1968 removed from sources_batch17.json, copy before the edit in brazil-b23).
All runs through .tmp/run.py / pipe.sh / reparse.sh at BelowNormal behind the cpu gate, one at a time (never two parses); every PID
printed in its log (brazil-b23/*.log, .tmp/zz[mno]-*.log, t23-*.log, final23*-build.log); all mine, all exited. Nothing running.
Fetching: archive.org only through the shared client (robots.txt read at start); no challenge page seen.
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once archive.org
has a capture of _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026.
Left out (unchanged): Lei 9.782 art. 8º-A; Lei 10.931; Lei 10.522 art. 32 quoted § 2º; Lei 12.462 art. 63 § 17; Leis 11.738, 12.009,
12.871, 13.979. No act of this session was left out.
NEXT on the ranked list: Lei 12.618/2012 (Funpresp; page l12618 pinned, not configured). Read first: art. 33 I puts Capítulo I in force
'na data em que forem criadas quaisquer das entidades de que trata o art. 4º' (event-tied: Decreto 7.808/2012 created Funpresp-Exe;
pin and read it, decide the day with the coordinator if unclear), MP 1.119/2022 -> Lei 14.463/2022 (29 notes each), MP 1.286/2024 (1
note: fate?), Lei 15.141/2025, Lei 13.183/2015 (records exist in 15a/15b/17zza/17i/6: copy exactly). Then Lei 12.865/2013 (page l12865
pinned; MPs 627/2013, 784/2017 (lapsed, shared table), 897/2019, 930/2020, 1.227/2024: fates first), Lei 10.848/2004 (cdxlist
leis/2004/l10.848.htm), environment (Leis 9.966, 7.661, 11.959, 5.197, 7.735, 11.516), energy (14.300, 10.438, 9.991, 9.847), banking (LC
130, Leis 10.214, 13.506, 8.929, 13.775), public administration (Leis 8.159, 9.491, 13.334; LC 35/1979; Lei 5.010/1966).
New in parse_batch17 this session (all scoped to their acts): DL 200 paragraphs wrapper (SEçãO, SETOR/MINISTÉRIO heading blocks, bare
Vide tails, 'Expressão substituída' read back from DL 900 art. 7 via _DL200_SWAP); _LPART block (PROMULGATED, SPAN_FIX, EXTRA_LAWS
stf-adi-4917, Anexo reader, build_act_lp = new outermost build_act wrapper); _G14601 in _GATES.

## Twenty-fourth session (2026-11-01): Lei 12.618/2012 (coordinator decision on art. 33 I), then the ranked list
robots.txt read at start (archive.org: Disallow /control/ /report/ only; web.archive.org 404). Fetching: archive.org only, through the
shared client (iaonly.py gap/laws/missing, cdxlist, cdxpre). Scratch: .gitlaw-scratch/brazil-b24 (page dumps, trial parses, logs;
copies of parse_batch17.py, sources_batch17.json, README.md, jurisdiction.json before the session's edits).

### 99-batch17zzp - PUBLISHed: Lei 12.618/2012 (lei-da-previdencia-complementar-dos-servidores-federais, LFunpresp, 7 versions 2012-05-02 .. 2025-06-03)
- Coordinator decision: Capítulo I takes effect 'na data em que forem criadas quaisquer das entidades de que trata o art. 4º'; date it
  by an official text if one fixes the first entity's creation day, else leave it out. Read: Decreto 7.808/2012 (pinned
  law:dec-7808-2012, capture 20261004172246): art. 1 'Fica criada ... Funpresp-Exe', art. 12 in force on publication, DOU 21.9.2012;
  Planalto prints '(Vide Decreto nº 7.808, de 2012)' on art. 33 I; 21.9.2012 is within art. 31's 180 days. -> Capítulo I DATED
  21.9.2012: _G12618 in _GATES (arts. 1-3) + build_act_fp (new outermost build_act wrapper) starts the 'CAPÍTULO I' heading lines
  that day; EXTRA decision. The Funpresp-Jud/-Leg creation acts were not read (said in the decision).
- MP 1.119/2022 -> Lei 14.463/2022 (CONVERTED_FIX: 'Convertida na Lei nº Lei nº 14.463'); MP 1.286/2024 MP_LAPSE 3.6.2025 (Ato
  Declaratório CN 46/2025 pinned ato:adc-46-2025-mpv1286: 'encerrado no dia 2 de junho de 2025'); Lei 15.141/2025 (DOU 3.6.2025)
  gives § 3º-A the same words that day and revokes the MP (art. 217 XXXIX). New pins: 3 laws + the Decreto + the Ato.
- pipe.sh zzp (brazil-b24/zzp-pipe1.out): sha d8be2331 x2, 0 moves, checks benign (see PUBLISH); lawcmp clean; headyear unchanged
  (t24-hy.log). Installed; docs.py rows-zzp.json; final merged build (final24-build.log): 247 acts, 3516 versions, 2568 commits, check
  0/0, compare identical, audit clean; PUBLISH written. PIDs printed in brazil-b24/*.log and .tmp/zzp-*.log, all mine, all exited.

### 99-batch17zzq - PUBLISHed: Lei 12.865/2013 (lei-12865-de-2013, L12865, 18 versions 2013-10-10 .. 2026-01-09 + 2027-01-01 futuro)
- Hand (block in `if any(... _L12865 ...)`, after the zzp block): _G12865 art-34 1.2.2014 (art. 43 I); scoped VIGENCIA_FIXED mp-627-2013
  12.11.2013 (art. 98: arts. 92-100 on publication) and lei-12973-2014 14.5.2014 (art. 119: arts. 93-119 on publication) - without
  them both fell on 1.1.2015 and art. 40 § 7º broke ('restored wording after an open one'); MP_LAPSE mp-1227-2024 4.6.2024 (Ato CN 36/2024:
  art. 6 rejected, 'não escritos' since its edition) + SPAN_FIX x5 (art. 31 § 6º I II, art. 32 caput + p.u. from 2013: the reader had
  started them on the MP's day from the struck 'Revogado pela MP 1.227' note); EXPLAINED art-20/art-33 _DOTTED; _FUT2027 arts. 29-32
  end 1.1.2027 (LC 214 art. 542 LIX) + B8.EXTRA_LAWS lc-214-2025 (= 14a/zj/zk record); OPEN_ITEMS.
- Pins: 5 laws (iaonly laws), 0 missing. pipe.sh zzq (brazil-b24/zzq-pipe2.out): sha 3d749b53 x2, 0 moves, benign flags (PUBLISH);
  lawcmp clean; reparse zzp/zzo equal, zzk sources counter only; headyear unchanged (t24-hy2.log). Installed; docs rows-zzq.json; README
  futuro summary line names the 2027 repeal; final merged build (final24b-build.log): 248 acts, 3534 versions, 2576 commits, check 0/0,
  compare identical, audit clean; PUBLISH written.
- OPEN (not changed, for the coordinator): Lei 14.286/2021's in-force day differs between parts: its own act (zzg) starts 30.12.2022
  (one year from DOU 30.12.2021, counted with the publication day), while the reader's default credits its changes to other acts on
  31.12.2022 (13f Lei 4.595, 17g Lei 4.728, and now zzq Lei 12.865 art. 25). zzq follows 13f/17g (reader default).

### Lei 10.848/2004 (part zzr) - CONFIGURED, NOT PUBLISHED (stopped here: clean point, context)
- Configured in parse_batch17: PAGES l10848 = _ato2004-2006/2004/lei/l10.848.htm (pinned, capture via `iaonly.py gap l10848 <url>`;
  no compilado capture on archive.org), act lei-da-comercializacao-de-energia-eletrica (LCEE), PARTS zzr, ACT_DAY 16.3.2004 (art. 33,
  publication), law record = 99-batch10/17u/17z's (url _Ato2004-2006/2004/Lei/L10.848.htm). `iaonly.py laws` 6 new pins, `missing` 0.
  notecount: Lei 15.269/2025 46, Leis 14.120/14.182 21 each, MP 998/2020 19, MP 1.300/2025 14, Lei 13.360 13, Lei 13.203 10 ...
- Trial parse (brazil-b24/zzr-t1.log) CRASHES in mp_notes (KeyError mp-1300-2025) and lists 19 problems. To do, in a scoped block like
  part z's (_LANEEL) and part u's (_L9074):
  a) VIGENCIA_FIXED mp-1300-2025 21.5.2025 (art. 4 = Lei 10.848 changes fall under its clause III) and lei-15235-2025 9.10.2025
     (the conversion keeps none of the MP's art. 4: read, Lei 15.235 names Lei 10.848 only in citations);
  b) MP 1.300's wordings end 9.10.2025 (conversion, lei-15235-2025) and Planalto prints each earlier wording again, struck, after the
     MP line (restored 9.10.2025 -> 25.11.2025, Lei 15.269) - as _E1300/_R1300 in part z; about 12 dispositivos (art. 1 § 5º, § 5º
     II/III/IV, art. 2 III (odd: Lei 13.360's wording printed unstruck before the MP line AND struck after it), art. 2 § 8º-A, art. 3
     caput, art. 3-A § 4º, art. 4 §§ 10-14 (MP insertions; Lei 15.269 adds §§ 15 ff.), art. 4-C (MP) vs 4-D (Lei 15.269)). Consider a
     generic wrapper instead of 12+ SPAN_FIX entries;
  c) MP_LAPSE for mp-641-2014 and mp-814-2017 (pages say 'Vigência encerrada'): find and pin each Ato Declaratório (cdxpre on
     _ato2011-2014/2014/congresso/ and _ato2015-2018/2018/congresso/), check whether batch tables already hold them;
  d) then pipe.sh zzr, lawcmp, docs rows, final build, PUBLISH.

## State at handoff (batch 17, twenty-fourth session, 2026-11-01)
Installed this session: 99-batch17zzp (Lei 12.618/2012, 7 versions; coordinator decision applied: Capítulo I dated 21.9.2012 by
Decreto 7.808/2012) and 99-batch17zzq (Lei 12.865/2013, 18 versions incl. 1 futuro). Final merged build of the installed folder after
all docs (final24b-build.log): 248 acts, 3534 versions, 2576 commits, check 0/0, --compare identical, audit_push clean on main and
futuro; README rows (+ futuro summary line) and jurisdiction.json (248 acts) current. lawcmp clean for both parts; reparse zzp/zzo equal,
zzk sources counter only; headyear unchanged (t24-hy2.log). All runs through .tmp/run.py / pipe.sh / reparse.sh at BelowNormal behind
the cpu gate, one at a time, never two parses; every PID printed in its log (brazil-b24/*.log, .tmp/zz[pq]-*.log, t24-*.log,
final24*-build.log); all mine, all exited (one stray grep of mine was stopped with TaskStop). Nothing running. Fetching: archive.org
only through the shared client (robots.txt read at start); no challenge page seen.
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once archive.org
has a capture of _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026.
OPEN for the coordinator: Lei 14.286/2021 day 30.12.2022 (zzg act) vs 31.12.2022 (credits in 13f, 17g, zzq).
NEXT: finish Lei 10.848 (zzr, to-do above), then environment (Leis 9.966, 7.661, 11.959, 5.197, 7.735, 11.516), energy (14.300,
10.438, 9.991, 9.847), banking (LC 130, Leis 10.214, 13.506, 8.929, 13.775), public administration (Leis 8.159, 9.491, 13.334; LC
35/1979; Lei 5.010/1966).

## Twenty-fifth session (2026-11-01): Task 1 Lei 14.286 day, Task 2 Lei 10.848 (zzr), then the ranked list
Scratch: .gitlaw-scratch/brazil-b25 (reparse_all.py = batch18's with every batch-17 part letter; runbuild.py = batch17's
accepting any 99-batch1* candidate; chk.sh <dir> <part> = pipe.sh's file checks; jd.py = version/decision diff; logs).
### Task 1 DONE: Lei 14.286/2021 day = 30.12.2022 in every part (coordinator decision)
- Day table: P.VIGENCIA_FIXED["lei-14286-2021"] = 2022-12-30 added in batch13/parse_batch13.py (after lei-14206-2021, unscoped
  law fact, inherited by batch14-17). Fresh parses before/after (brazil-b25/base, new): 13f, 17g, zzq differ ONLY in the one
  version day 2022-12-31 -> 2022-12-30 (credited lei-14286-2021 only) and the law's in-force decision line; zzg identical (sha
  6569e4af both). Pre-existing drift (not touched): 13f fresh parse adds the Res. SF 16/2006 decision (13g's), sources counter.
- Installed = previous file + exactly that delta (patch14286.py); per-part checks identical before/after (chk.sh); merged build
  (build1.log): 248 acts, 3534 versions, 2576 commits, check 0/0, compare identical, audit clean main+futuro. PUBLISH appended to
  13f (c9a35655), 17g (d13c66db), zzq (8da0eb69). Previous files in brazil-b25/before/. README already said 30 December 2022.
- PIDs (all mine, all exited): 31276 (base), 13140 (ctx), 45640 (new), chk PIDs in brazil-b25/pids-chk.txt, 40964 (build1).
### Task 2 (zzr, Lei 10.848) - in progress notes
- robots.txt read this session (archive.org: Disallow /control/ /report/; web.archive.org 404). New pins (archive.org, shared client):
  ato:adc-30-2014-mpv641 (MP 641 'encerrado no dia 21 de julho' 2014 -> MP_LAPSE 22.7.2014), ato:adc-30-2018-mpv814 (MP 814 ended
  1.6.2018 -> MP_LAPSE 2.6.2018), ctx:camara-lei-10848-2004-original (Chamber's original publication, ts 20260513233651).
- GENERAL RULE (CONV_RESTORE + lifespans wrapper at the end of parse_batch17; BATCH17_CONV_REPORT=1 prints every place it finds):
  MP wording, then a struck repeat of the wording it replaced, then a later law: MP wording ends at its conversion law's day, the
  repeat stands from then to the later law. Checked: on part z it finds exactly the 2 hand SPAN_FIX places (same days); on zzr 5
  places (art. 1 § 5º, § 5º II/III, art. 2 III, art. 3 caput); on part u it finds Lei 9.074 art. 15 § 7º, which the PUBLISHED
  part u gets WRONG (MP 1.300 wording kept 9.10-25.11.2025 instead of the restored Lei 10.848 wording) -> part u added to
  CONV_RESTORE, to be re-PUBLISHed. MP insertions (art. 1 § 5º IV, art. 2 § 8º-A, art. 3-A § 4º, art. 4 §§ 10-14, art. 4-C) already
  end 9.10.2025 by the reader's conversion end.
- art. 3º-D (Lei 15.269 art. 9): Planalto prints the label only; text read from Lei 15.269's page (paragraphs wrapper, page
  l10848); effects 23.2.2026 (Lei 15.269 art. 24 II, 90 days) via new effects_fix MOVES "99-batch17zzr.json".
- art. 2 § 6º: Planalto prints only Lei 11.943's caput; 2004 wording read from the Chamber copy, inserted struck above it.
- EXPLAINED art-10/11/13 _DOTTED; OPEN_ITEMS[_LCEE]. Backups: brazil-b25/parse_batch17.zzr1.py, effects_fix.before.py,
  sources_batch17.before.json.
### 99-batch17zzr - PUBLISHed: Lei 10.848/2004 (LCEE, 29 versions 2004-03-16 .. 2026-02-23)
- pipe.sh zzr final (brazil-b25/zzr-pipe4.out): sha bd9e3f10 x2, eff d5a5b0ed (1 move: art. 3º-D to 23.2.2026), all checks benign
  (PUBLISH lists them). Earlier pipe runs 1-3 superseded (pipe3 tried copying 17s's lei-12783-2013 record: reverted, because
  99-batch17s and 99-batch17z ALREADY DIFFER for lei-12783-2013 (URL case, 'nºs' vs 'nº s'); zzr equals 17z. OPEN for coordinator).
- rows-zzr.json docs; final25a-build.log: 249 acts, 3563 versions, 2586 commits, check 0/0, compare identical, audit clean.
### 99-batch17u re-PUBLISHed: Lei 9.074 art. 15 § 7º (MP 1.300 wording ended 9.10.2025, Lei 10.848 wording back to 25.11.2025)
- Found by the CONV_RESTORE report; part u added to CONV_RESTORE. Fresh reparse (reparse.sh u): only that 9.10.2025 version text +
  the rule's decision differ; installed = previous file with acts+decisions from the reparse, sources kept (e60d3f34); checks
  identical before/after (brazil-b25/ubefore, unew); merged build u-build.log clean. Previous file: brazil-b25/ubefore/.
### 99-batch17zzs - PUBLISHed: Lei 9.966/2000 (lei-da-poluicao-por-oleo, 1 version 28.7.2000) + Lei 11.959/2009 (lei-da-pesca, 1
version 29.8.2009); no amendment notes. sha 7b938858; final25b-build.log: 251 acts, 3565 versions, 2588 commits, check 0/0, compare
identical, audit clean. rows-zzs.json docs.

## State at handoff (batch 17, twenty-fifth session, 2026-11-01)
Done: Task 1 (Lei 14.286 30.12.2022 in 13f/17g/zzq), zzr (Lei 10.848), 17u re-PUBLISH, zzs (Leis 9.966, 11.959). Final merged build
of the installed folder after all docs (brazil-b25/final25b-build.log): 251 acts, 3565 versions, 2588 commits, check 0/0, --compare
identical, audit_push clean main + futuro; README rows + jurisdiction.json (251 acts) current. All runs through run.py / pipe.sh /
reparse.sh at BelowNormal behind the cpu gate, never two parses at once; PIDs printed in brazil-b25/*.log, pids-chk.txt and the pipe
outputs; all mine, all exited. Nothing running. Fetching: archive.org only (robots.txt read), no challenge page.
New in code: batch13 VIGENCIA_FIXED lei-14286-2021; parse_batch17 end: zzr block (MP 1.300 days, MP 641/814 lapses, EXPLAINED,
OPEN_ITEMS, l10848 paragraphs wrapper: art. 3º-D from Lei 15.269, art. 2 § 6º 2004 wording from the Chamber copy, CONTEXT source),
CONV_RESTORE rule + lifespans wrapper (BATCH17_CONV_REPORT=1 to survey any part), part zzs config; effects_fix MOVES zzr.
NEXT (pages pinned this session, not configured): Lei 7.661/1988 (l7661; its footer misprints 'DOU de 18.5.1998': settle the day via
LexML lexml1.py first; 2 notes: Leis 14.714/2023, 15.190/2025), Lei 5.197/1967 (l5197 + l5197compilado in the local index; 21 notes:
Leis 7.584, 7.653, 7.679, 9.111, 9.985), Lei 7.735/1989 (l7735; 11 notes incl. MP 2.216-37 (edition key), MP 366/2007 -> Lei 11.516),
Lei 11.516/2007 (l11516; MP 809/2017 -> Lei 13.668, MP 1.151/2022 -> Lei 14.590; record exists in 14c/zp: copy). Then energy
(14.300, 10.438 (+compilada), 9.991, 9.847 (+compilado)), banking, public administration as before.
Optional survey: run parses with BATCH17_CONV_REPORT=1 over other parts with MP conversions to find more places like Lei 9.074 § 7º
(only z and u were checked).
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once archived
after 30.10.2026.
OPEN for the coordinator: lei-12783-2013 record differs between 99-batch17s and 99-batch17z (URL case and 'nºs'/'nº s').

## Twenty-sixth session (2026-11-01): Task 1 converted-MP survey of every part, Task 2 Lei 12.783 record, Task 3 next candidates
Scratch: .gitlaw-scratch/brazil-b26 (conv_report.py = report-only outermost lifespans wrapper for ANY Brazil parser, run with
--dry; survey.py = it over every part with mp-* law records, one process at a time, cpu gate; sv/<part>.log; base/ new/ = fresh
reparses (b25 reparse_all.py); before/ = previous part, PUBLISH, README, jurisdiction.json; install.py = previous file with
every top-level key from the reparse except sources; topdiff.py; chk.sh = b25's pointed at b26). robots.txt read at start
(archive.org Disallow /control/ /report/; web.archive.org 404; LexML /urn /sru allowed, Crawl-delay 5).
### Task 1 DONE: survey (sv/, survey.log): 79 parts (50-codes, 70-clt, 80-proc, 95-rju, 97-batch4, 98-batch5, 5b, 6-12,
13-17 with MPs), all rc 0, corpus.d and sources*.json byte-identical after. 22 places found: 20 already dated as the rule dates them (8
Lei 9.613 x3 (MP 870), 16a CBA x3 (MP 714), 17e Lei 12.587 (MP 818), 17j Lei 7.713 x2 (MPs 68, 114), u, z x2, zza (MP 656), zzr x5); 2 WRONG:
- 99-batch16b Lei 8.036 art. 15 caput: MP 680/2015 wording kept 7.7.2015..17.3.2022; conversion Lei 13.189/2015 (DOU 20.11.2015,
  art. 12 on publication) only cites art. 15 in its art. 9 -> MP ends 20.11.2015, 1990 wording again to MP 1.107 (18.3.2022).
  New rule copy CONV_RESTORE16 in parse_batch16's __main__ block only (batch 17 imports batch16; its own copy stays).
- 99-batch17zw Lei 10.973 art. 2 V: MP 495/2010 wording kept to 11.1.2016; Lei 12.349/2010 art. 5 changes only art. 2 VII and
  art. 27 IV -> MP ends 16.12.2010, 2004 wording again to Lei 13.243 (12.1.2016). CONV_RESTORE[_LINOV]; decision text now
  _WCONV_RULE + CONV_WHY[act] (MP 1.300 text byte-identical: reparse z, u equal installed except the old sources drift, zzr SAME).
- Fresh reparses: 16b +1 version (20.11.2015, art-15, lei-13189-2015; law record added = 15a's) + decision; zw only the
  16.12.2010 version text + decision. Installed (install.py, sources kept): 16b ce1eb89a, zw 3609b77d. Checks before/after
  identical (chk.sh, zw overlap/latecaput identical). README FGTS row 52, jurisdiction.json 3566 versions / (52).
### Task 2 DONE: lei-12783-2013 = the 17z/zzr form (URL _Ato2011-2014/2013/Lei/L12783.htm, 'Leis nº s') in part s's ACT_LAWS;
  reparse s: only that record's title+url differ; installed 2084fbf4; checks identical. All 3 parts agree now.
- Merged build after docs (build2.log): 251 acts, 3566 versions, 2588 commits, check 0/0, compare identical, audit clean main +
  futuro. PUBLISH appended to 16b, zw, s. PIDs: survey 49188 (trial 41276), base 47452, new 11976, chk in
  pids-chk.txt, zw-ov 18544, zw-lc 23488, build1 6616, build2 9280; all mine, all exited.
### Task 3: 99-batch17zzt and 99-batch17zzu PUBLISHed
- Fetching: one LexML /urn record (lexml1.py lei-7661-1988=1988-05-16 -> DOU 18.5.1988; Planalto footer misprints 1998);
  archive.org through the shared client: `iaonly.py gap l5197-compilado` (ts 20261012014540), `iaonly.py laws` 5 + 2 new pins,
  `missing` 0. No challenge page.
- zzt: Lei 7.661/1988 (lei-do-gerenciamento-costeiro, LGCost, 3 versions) + Lei 5.197/1967 (lei-de-protecao-a-fauna, LFauna,
  6; check page l5197-compilado). Hand: B8.SPAN_FIX x3 (_W5197) for art. 27 § 4º, a), b): dated 17.2.1988 (Lei 7.653) ..
  24.11.1988 (Lei 7.679) like alínea c) (one note for the block; latecaput found them dated 1967). pipe.sh zzt
  (b26/zzt-pipe2.out): sha 7b345380 x2, 0 moves, flags benign (PUBLISH).
- zzu: Lei 7.735/1989 (lei-do-ibama, LIbama, 8) + Lei 11.516/2007 (lei-do-instituto-chico-mendes, LICMBio, 5; law record =
  14c/zp's). Hand (block '# part zzu' before SRC): NOTE_FIX 'pela Lei nº 11.516, 2007' x2; SPAN_FIX x3 (_W7735): Lei 7.735
  art. 2 I, II start 27.4.2007 (MP 366 art. 5 rewrote the whole article; Planalto prints the MP's lines unstruck) and MP
  2.216-37's parágrafo único ends 27.4.2007; EXPLAINED art-06 _DOTTED; OPEN_ITEMS both. pipe.sh zzu (b26/zzu-pipe2.out): sha
  88e8505d x2, 0 moves, latecaput 0, quotecheck 30 = Lei 11.516's quoted amendments.
- lawcmp: zzu clean; zzt only lei-9985-2000 URL case vs 99-batch14c ('l9985'; parts 6 and 10 and zzt use 'L9985'): OPEN, a
  pre-existing difference like the Lei 12.783 one (not changed). headyear unchanged (b26/hy.log = b25/hy.log). Converted-MP
  report on zzt/zzu: 0 places.
- Docs rows-zzt.json, rows-zzu.json; final26-build.log: 255 acts, 3588 versions, 2599 commits, check 0/0, compare identical,
  audit clean main + futuro. PIDs (all mine, all exited): lexml 31704, gap 40964, laws 2412/40040, missing 1436, trials
  13652/37696/52552/34504, pipe PIDs in b26/zz[tu]-pipe*.out, conv 21608/50332, region/lawtxt runs in b26/*.log, final 53104.

### Coordinator follow-up (same session): one law record per key across all parts
- New check batch17/.tmp/uniqlaws.py (--all [part.json ...] or <part.json>): every field of a shared law key's record (label,
  title, kind, enacted, published, url, temporary_until, restores, note) must agree over corpus.json + corpus.d (a given part
  replaces the installed one of the same name); exit 1 on any difference. Added to pipe.sh (after the file checks, on $E).
- Before: 94 differing fields on 72 keys (url 66 keys, title 15, published 3, note 2) of 570 shared keys.
- Fix: scripts/brazil-law/law_records.json (made by brazil-b26/mktable.py from the installed parts: per field the value most
  parts use; on a tie the first part's in build order, which build.py already showed; 44 field ties) and
  scripts/brazil-law/lawrecords.py (apply/apply_file; CLI `lawrecords.py <part.json> ...`). effects_fix.py's __main__ now runs
  it on every part it is given (idempotent; prints 'N law records set'), so batch reparses keep the agreed records (reparse of
  17x, 14c, 9: laws equal to installed). Parts written by other parsers (codes, clt, proc, phase2, rju, batch3/4/5,
  corpus.json) do not run effects_fix: run lawrecords.py on them after writing.
- Lei 1.431/1951 (published 13.9 in 60-phase2 vs 14.9 in 80-proc): LexML says 14.9.1951 (cached record). parse_phase2 got
  PUB_LEXML {"lei-1431-1951": "1951-09-14"} + PUB_CORRECTED + the 'Publication days' decision (as parse_proc); fresh parses
  without/with it (b26/base, new) differ only in that field, the CP version 28.10 -> 29.10.1951 (LINDB +45) and the two decision
  lines; installed 60-phase2 = previous + exactly that delta (patch1431.py; a fresh parse_phase2 run already differs from the
  installed part in older post-steps: driver b26/p2out.py writes elsewhere).
- Applied to all parts: 42 parts changed (list: b26/lawrec-apply.log); onlylaws.py: only law-record fields differ, 0 other
  differences; uniqlaws --all 0. pubgap before/after on all 42: identical except 70-clt, where the flags for Leis 13.509/2017
  and 13.877/2019 are gone (the CLT records had the vetoed-parts promulgation day as publication; versions unchanged). Lei
  9.985's URL (14c) is now the majority 'leis/L9985.htm'.
- Merged build (b26/build-laws.log): 255 acts, 3588 versions, 2598 commits (CP and CPP Lei 1.431 changes now share 29.10.1951),
  check 0/0, compare identical, audit clean main + futuro. PUBLISH appended to all 42 (publaws.py; 60-phase2 also the Lei
  1.431 line). Backups: b26/before-all (every part + PUBLISH before), before/ (effects_fix.py, pipe.sh, parse_phase2.py).
- Known pre-existing drift seen (not touched): fresh 14c parse adds a DL 2.431/1988 (Estatuto da Terra) decision line.
- PIDs (all mine, all exited): p2base 41020, p2new 51716, lexml1431 (cached, no request), pubgap_all 42156 (failed on a path) and
  54044, re3 46336, build-laws 22516.

## State at handoff (batch 17, twenty-sixth session, 2026-11-01)
Done: Task 1 (converted-MP survey of all 79 parts with MPs: 2 wrong places fixed, 16b Lei 8.036 art. 15 and zw Lei 10.973
art. 2 V; 16b/zw re-PUBLISHed), Task 2 (Lei 12.783 record = 17z/zzr form in part s; s re-PUBLISHed), Task 3 (zzt Leis 7.661,
5.197; zzu Leis 7.735, 11.516 PUBLISHed). Final merged build after all docs (brazil-b26/final26-build.log): 255 acts, 3588
versions, 2599 commits, check 0/0, --compare identical, audit_push clean main + futuro; README rows (+ FGTS 52) and
jurisdiction.json (255 acts, 3588 versions) current. Nothing running. Fetching: archive.org (shared client) + 1 LexML record;
robots.txt read; no challenge page.
New in code: parse_batch16 __main__-only CONV_RESTORE16 (FGTS); parse_batch17 CONV_RESTORE[_LINOV] + CONV_WHY/_WCONV_RULE,
part s ACT_LAWS lei-12783-2013, zzt/zzu config (PAGES l5197-compilado, acts, PARTS, ACT_DAY, ACT_LAWS, SPAN_FIX/NOTE_FIX
blocks). Backups: brazil-b26/parse_batch16.before.py, parse_batch17.before.py, before/.
Tool for later: brazil-b26/conv_report.py <any Brazil parse script> --dry (env for part/out) prints every converted-MP place
after all rules; survey.py runs it over every part with MPs. Run it on each new part with MPs.
Coordinator follow-up DONE too: uniqlaws check (in pipe.sh) + law_records.json/lawrecords.py; 42 parts
re-PUBLISHed, Lei 1.431 day fixed in 60-phase2; merged 255 acts, 3588 versions, 2598 commits, check 0/0, compare identical,
audit clean (brazil-b26/build-laws.log). Lei 9.985 OPEN item closed.
NEXT (coordinator's item 2, not started): energy as small parts - act pages NOT pinned yet (only law: records for 10.438 and
14.300): pin l14300 (_ato2019-2022/2022/lei/l14300.htm), l10438 (leis/2002/l10438.htm) + compilada, l9991, l9847 +
compilado via `iaonly.py gap`, then laws/missing; Lei 10.438 carries MP 1.300/2025 and MP 998/2020 (run conv_report.py and
uniqlaws). Then banking (LC 130, Leis 10.214, 13.506, 8.929,
13.775), public administration (Leis 8.159, 9.491, 13.334; LC 35/1979; Lei 5.010/1966).
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once
archive.org has a capture of _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026.
OPEN for the coordinator: none new (Lei 9.985's URL case fixed by the law-record step).

## Twenty-seventh session (2026-11-01): energy laws as small parts (zzv, zzw, ...)
robots.txt read at start (archive.org: Disallow /control/ /report/ only; web.archive.org 404). Fetching: archive.org only through
the shared client (iaonly.py pages/laws/missing). Scratch: .gitlaw-scratch/brazil-b27 (page dumps l*.txt, trial parses, logs,
before/ = README, jurisdiction.json, effects_fix.py before the session's edits, sources_batch17.before.json).
Pages pinned (`iaonly.py pages`, 6): l14300 (20261021135456), l10438 (20261004205046), l10438-compilada (20261004222624), l9991
(20261004222620), l9847 (20261007124148), l9847-compilado (20260510101524). notecount (zzv-era): l10438 266 notes (Lei 10.762 39, Lei
13.360 33, Lei 12.783 20, MP 579 17, MP 735 16, Lei 15.269 16, MP 1.304 12, Lei 10.848 11, Lei 13.299 11, Lei 14.120 8, MP 879 7, MP
998 7, MP 1.300 7, MP 1.078 6 ...); l9847 71 (Lei 11.097 26, Lei 14.993 13, MP 1.349/2026 8, MP 532/2011 7, Lei 12.490 6, MP
1.340/2026 4, '1/2490' misprint 1).
### 99-batch17zzv - PUBLISHed: Lei 14.300/2022 (LMMGD, 4 versions) + Lei 9.991/2000 (LPDSE, 19 incl. 2027 futuro)
- Block '# part zzv' before SRC: SPAN_FIX _W14300 (art. 11 § 3º, art. 28 p.u. promulgated DOU 5.8.2022), SPAN_FIX _W14514 (9.991
  art. 1 I: Lei 14.514's vetoed + promulgated wording from 22.5.2024; 13.203's to then), scoped VIGENCIA_FIXED lei-14514-2022 =
  30.12.2022 (zg's day; without it the reader took art. 25 I's 1.2.2023) and MP_LAPSE mp-1212-2024 (part z's text word for word);
  paragraphs wrapper on l9991: art. 1 § 1º note '(Alterado pela Lei 13.280)' -> renumbering note (EXTRA decision _W13280).
- effects_fix MOVES "99-batch17zzv.json": 14.300 <- Lei 15.269 all to 1.1.2026; 9.991 <- Lei 12.111 all to 1.1.2010; 9.991 art. 1º-A
  (Lei 15.269, '(VETADO)') to 1.1.2027 (futuro). 6 moves.
- Bad pin: law:mp-144-2003 (Vide link; capture = Lei 9.427's page; headyear BAD) removed from sources_batch17.json.
- pipe.sh zzv (b27/zzv-pipe3.out): sha 07dde0b0 x2, 6 moves, flags benign (PUBLISH). Installed ab0b8f03; docs rows-zzv.json + README
  futuro line; final27a-build.log: 257 acts, 3611 versions, 2607 commits, check 0/0, compare identical, audit clean; headyear same.
- PIDs (all mine, all exited): pages 52592, nc 9152, laws 21112, missing 38564, trials 21240/22840/54492, spans 35308/31560, conv
  27524, effrep (eff-zzv.log), pipe PIDs in zzv-pipe*.out, hy 46460/12672, final 40136.
### 99-batch17zzw - PUBLISHed: Lei 10.438/2002 (lei-do-proinfa-e-da-cde, LProinfa, 42 versions 2002-04-29 .. 2025-11-25)
- `iaonly.py laws l10438 l10438-compilada` 9 new pins, missing 0. Atos pinned (`iaonly.py gap`): ato:apn-39-2013-mpv605,
  ato:adc-46-2022-mpv1078, ato:adc-22-2019-mpv855, ato:ato-2019-mpv879 (Chamber rejection 20.8.2019), ato:adc-105-2020-mpv950.
- Block '# part zzw' (end of parse_batch17, before SRC): scoped VIGENCIA_FIXED mp-1300-2025, lei-15235-2025, lei-14514-2022 (30.12.2022;
  the reader took art. 25 I's 1.2.2023); MP_LAPSE 605, 814 (zzr text verbatim), 855, 879 (+ B5.MP_REJECTED), 950, 1.078;
  CONV_RESTORE[_LPROINFA] + CONV_WHY (art. 13 §§ 3º-D..F); EXPLAINED (compilada misprints / out of date; typesetting; _DOTTED);
  OPEN_ITEMS. effects_fix MOVES "99-batch17zzw.json": MP 1.304 art. 13-A -> None (never took effect).
- Bad pins law:mp-144-2003 and law:mp-181-2004 (re-pinned by `laws` from Vide links; captures are Lei 9.427's / Lei 10.438's
  pages) removed again; `laws` re-pins them on every run, so check headyear after each `laws` and remove them.
- pipe.sh zzw (b27/zzw-pipe3.out): sha 1946ace3 x2, 1 move, flags benign (PUBLISH). Installed aaa39925; docs rows-zzw.json;
  final27b-build.log: 258 acts, 3653 versions, 2620 commits, check 0/0, compare identical, audit clean. PIDs in b27 logs, all exited.
### 99-batch17zzx - PUBLISHed: Lei 9.847/1999 (lei-da-fiscalizacao-do-abastecimento-de-combustiveis, LFAC, 7 versions 1999-10-27 .. 2024-10-09)
- `iaonly.py laws l9847 l9847-compilado` 3 new pins (incl. law:mp-1340-2026), missing 0. MPs 1.340/2026 and 1.349/2026 lapsed, Atos
  adc-62-mpv1.340 / adc-77-mpv1.349 NOT on archive.org (cdxlist exact paths 0; cdxpre of the 2026 congresso prefix: 16 Atos, neither) ->
  block '# part zzx' (paragraphs wrapper on l9847) drops every line whose notes cite them (12 lines, art. 3 XXI/XXII/p.u., art. 5 III);
  EXTRA decision; EXPLAINED arts. 3, 5 (compilado captured 10.5.2026 while the MPs were in force; it also lacks Lei 14.993's art. 3
  XVIII); OPEN_ITEMS.
- pipe.sh zzx (b27/zzx-pipe1.out): sha de41b754 x2, 0 moves, flags benign (PUBLISH). Installed de41b754; docs rows-zzx.json;
  final27c-build.log: 259 acts, 3660 versions, 2621 commits, check 0/0, compare identical, audit clean; headyear same.
- NEW DATED RE-CHECK: Atos adc-62-mpv1.340 and adc-77-mpv1.349 (2026 congresso): once archived, add MPs 1.340/1.349 to zzx with
  their lapse days, and Lei 12.462 art. 63 § 17 to part v.
### 99-batch17zzy - PUBLISHed: banking - Leis 10.214/2001 (LSPB, 4), 13.506/2017 (LPAS, 2), 13.775/2018 (LDupE, 1)
- Pages pinned (`iaonly.py pages`, 5): lcp130 (20261021165157), l10214 (20261005192732), l13506 (20261004164912), l8929
  (20261015144412), l13775 (20261012064658). notecount: lcp130 107 (LC 196/2022 102, LC 161/2018 5); l8929 136 (Lei 13.986/2020 56,
  MP 897/2019 41, Lei 14.421/2022 23, Lei 10.200/2001 7, Lei 11.076/2004 5, MP 1.104/2022 3, Lei 14.112/2020 1).
- zzy: ACT_LAWS records copied from 99-batch8 (lei-13506-2017) and 99-batch17c (lei-13775-2018) by a script (exact strings);
  Lei 13.775 ACT_DAY 20.4.2019 (= part c's day). SPAN_FIX _W9_784 (Lei 10.214 art. 9 restored I/II/p.u. from 20.10.2017, _R784).
- pipe.sh zzy (b27/zzy-pipe2.out): sha 4ea4b197 x2, 0 moves, flags benign (PUBLISH). Installed; docs rows-zzy.json;
  final27d-build.log: 262 acts, 3667 versions, 2624 commits, check 0/0, compare identical, audit clean; headyear same.
- NEXT: LC 130/2009 (lcp130 pinned; LC 196/2022 rewrote most of it: 102 notes; record = 13f's) and Lei 8.929/1994 (CPR; l8929
  pinned; MP 897/2019 -> Lei 13.986/2020, MP 1.104/2022 -> Lei 14.421/2022: read each conversion and vigência first), then public
  administration (Leis 8.159, 9.491, 13.334; LC 35/1979; Lei 5.010/1966).

## State at handoff (batch 17, twenty-seventh session, 2026-11-01)
Installed with .PUBLISH this session: zzv (Leis 14.300/2022, 9.991/2000; 23 versions incl. 1 futuro), zzw (Lei 10.438/2002; 42), zzx
(Lei 9.847/1999; 7; MPs 1.340/1.349 of 2026 left out), zzy (Leis 10.214/2001, 13.506/2017, 13.775/2018; 7) = 7 acts, 79 versions.
Final merged build of the installed folder after all docs (brazil-b27/final27d-build.log): 262 acts, 3667 versions, 2624 commits,
check 0/0, --compare identical, audit_push clean on main and futuro; README rows (+ futuro line for Lei 9.991 art. 1º-A) and
jurisdiction.json (262 acts, 3667 versions) current. headyear unchanged (b27/hy6.log = b26/hy.log). All runs through .tmp/run.py /
pipe.sh at BelowNormal behind the cpu gate, one at a time, never two parses; PIDs printed in each b27 log / pipe output; all mine,
all exited. Nothing running. Fetching: archive.org only through the shared client (robots.txt read at start); no challenge page.
New in code: parse_batch17 PAGES (energy + banking pages), acts/PARTS/ACT_DAY/ACT_LAWS for zzv-zzy, blocks '# part zzv' (SPAN_FIX
_W14300, _W14514, scoped VIGENCIA_FIXED/MP_LAPSE, l9991 renumbering wrapper), '# part zzw' (MP fates, CONV_RESTORE/CONV_WHY
_LPROINFA, EXPLAINED), '# part zzx' (l9847 drop wrapper for MPs 1.340/1.349), '# part zzy' (_W9_784); effects_fix MOVES zzv (6
moves), zzw (MP 1.304 art. 13-A never in effect). sources_batch17.json: law:mp-144-2003, law:mp-181-2004 removed (bad pins; `laws`
re-adds them from Vide links: run headyear after every `laws` and remove them again). Backups: brazil-b27/before/.
DATED RE-CHECKS: MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once archive.org has
_ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026; NEW: Atos adc-62-mpv1.340 and adc-77-mpv1.349 (2026 congresso) once archived ->
add MPs 1.340/1.349 to part zzx and Lei 12.462 art. 63 § 17 to part v.
NEXT: LC 130/2009 and Lei 8.929/1994 (pages pinned, not configured; see zzy notes), then public administration (Leis 8.159, 9.491,
13.334; LC 35/1979; Lei 5.010/1966).

## Twenty-eighth session (2026-11-01): Task 1 bad-pin blocklist, Task 2 LC 130, Lei 8.929, then public administration
robots.txt read at start (archive.org: Disallow /control/ /report/ only; web.archive.org 404). Fetching: archive.org only through
the shared client (iaonly.py). Scratch: .gitlaw-scratch/brazil-b28 (before/ = fetch_batch5.py, sources_batch17.json,
parse_batch17.py, effects_fix.py, README, jurisdiction.json before the session; page dumps, logs, conv_report.py copy).
### Task 1 DONE: scripts/brazil-law/bad_pins.json + fetch_batch5.drop_bad()
- bad_pins.json {"keys": {key: reason}}: law:mp-144-2003, law:mp-181-2004 (Vide links whose pages are Leis 9.427 / 10.438) and
  law:dl-900-1968 (misprinted key, removed in zzm): every key headyear caught and a session removed. The headyear BAD lines that
  stay (hy6 baseline: rNN edition keys, lc-189-*, mp-173/339/37/86, lei-7619-1987 ...) are pinned and some are read by installed
  parts, so they are not blocked (blocking only stops new pins anyway; already-pinned keys are skipped by pin_many).
- fetch_batch5.py `laws` and `missing` pass their todo through drop_bad() (prints 'skipped (bad_pins.json): key - reason'); every
  batch fetcher built on fetch_batch5 (5b, 6-17, iaonly.py) gets it. `gap <id> <url>` still pins on purpose.
- Test (b28/laws-t1.log, PID 37684): `iaonly.py laws l14300 l9991 l10438 l10438-compilada l9847 l9847-compilado` -> both keys
  skipped, 0 pinned; every sources*.json byte-identical before/after (srcsha-before/after.txt); headyear = b27/hy6.log (PID
  52536). No part rewritten, corpus.d untouched.
### 99-batch17zzz - PUBLISHed: Lei Complementar 130/2009 (LCoopCred, 3 versions 2009-04-17, LC 161 2018-01-05, LC 196 2022-08-25)
- `iaonly.py laws lcp130 l8929` (PID 52816): 4 new pins law:lc-161-2018, lc-196-2022, lei-10200-2001, mp-1104-2022; missing 0;
  headyear same. No hand items. pipe.sh zzz (b28/zzz-pipe1.out): sha 2d6306ba x2, 0 moves, flags benign (PUBLISH). conv 0.
  Installed; rows-zzz.json; final28a-build.log: 263 acts, 3670 versions, 2627 commits, check 0/0, compare identical, audit clean.
### 99-batch17zzza - PUBLISHed: Lei 8.929/1994 (LCPR, 8 versions 1994-08-23 .. 2022-07-21)
- Block '# part zzza' (end of parse_batch17, before SRC): NOTE_FIX '(Redação da pela Lei nº 13.986, de 2020' (x25) and '(Revogado pela
  Lei nº 13.986, de 2020' (x19, both unclosed); SPAN_FIX _W897_4 (art. 4º-A § 4º of MP 897 ends 7.4.2020: Lei 13.986 art. 42 closes
  art. 4º-A after § 3º with (NR)); OPEN_ITEMS. Trial t1 had 2 'restored wording' problems + 2 undated lines, all from the bad notes.
- pipe.sh zzza (b28/zzza-pipe1.out): sha 6e0c81f1 x2, 0 moves, flags benign (PUBLISH). conv 0. Installed a9b3d6ea; rows-zzza.json;
  final28b-build.log: 264 acts, 3678 versions, 2630 commits, check 0/0, compare identical, audit clean. PIDs in b28 logs, all exited.
### 99-batch17zzzb - PUBLISHed: Lei 8.159/1991 (LArq, 2) + Lei Complementar 35/1979 (LOMAN, 6)
- Pages pinned (`iaonly.py pages`, 5): l8159, l9491, l13334, lcp35, l5010 (ts in sources_batch17.json). `laws l8159 lcp35 l5010 l9491`
  25 new pins; missing 0. gap pins: law:mp-246-2005, ato:atocd-2005-mpv246 (Câmara rejection, session 21.6.2005, DOU 22.6.2005),
  ctx:rsf-12-1990, ctx:rsf-31-1993. Bad pin law:mp-246-1997 (Lei 9.491 note misprint; page = MP 246/2005) removed and added to
  bad_pins.json. headyear (b28/hy4.log) = hy1 + NOHEAD law:lei-6044-1974 (UTF-8 BOM page, Vide only; benign).
- Block '# part zzzb': NOTE_FIX 'Lei nº 54, de 22.12.1986' x2; P.COURTS rsf-12-1990 / rsf-31-1993 (batch15 model); SPAN_FIX _W108 +
  EXPLAINED art-108. pipe.sh zzzb (b28/zzzb-pipe3.out): sha 87ef6f8a x2, 0 moves, flags benign. Installed; rows-zzzb.json;
  final28c-build.log: 266 acts, 3686 versions, 2637 commits, check 0/0, compare identical, audit clean.
### 99-batch17zzzc - PUBLISHed: Lei 5.010/1966 (LJF, 9) + Lei 9.491/1997 (LPND, 9)
- Block '# part zzzc': VIGENCIA_FIXED lei-13876-2019 (scoped), LAW_FIELD_FIX lei-6741-1979 enacted 5.12.1979 (2 LexML /urn requests,
  robots read: the 17.12 URN 'não encontrada', the 5.12 one gives DOU 6.12.1979), NOTE_FIX MP 246 '1997', MP_LAPSE/MP_REJECTED
  mp-246-2005, MP_PENDING mp-2161-2001, SPAN_FIX _W246 (gap) + EXTRA_LAWS lei-11483-2007, SPAN_FIX _W5_8 (art. 5 § 8º 'Vide').
- pipe.sh zzzc (b28/zzzc-pipe2.out): sha 956397aa x2, 0 moves, flags benign. Installed; rows-zzzc.json; final28d-build.log: 268 acts,
  3704 versions, 2651 commits, check 0/0, compare identical, audit clean; headyear hy5 = hy4.

## State at handoff (batch 17, twenty-eighth session, 2026-11-01)
Task 1 DONE: scripts/brazil-law/bad_pins.json (keys law:mp-144-2003, law:mp-181-2004, law:dl-900-1968, law:mp-246-1997) read by
fetch_batch5.drop_bad() in `laws` and `missing` (every batch fetcher and iaonly.py); a `laws` run skips them with a printed line, no
sources*.json changed, no part changed. Add a key there (with its reason) whenever headyear catches a pin from a misprinted note
or a wrong link, then remove the pin from the sources file. `gap` still pins on purpose.
Task 2: installed with .PUBLISH this session: zzz (LC 130/2009; 3 versions), zzza (Lei 8.929/1994; 8), zzzb (Lei 8.159/1991, 2;
LC 35/1979, 6), zzzc (Lei 5.010/1966, 9; Lei 9.491/1997, 9) = 6 acts, 37 versions. Final merged build of the installed folder after
all docs (brazil-b28/final28d-build.log): 268 acts, 3704 versions, 2651 commits, check 0/0, --compare identical, audit_push clean on
main and futuro; README rows and jurisdiction.json (268 acts, 3704 versions) current. Every earlier part byte-identical
(b28/corpusd-before.txt vs corpusd-after.txt). headyear (b28/hy5.log) = b27/hy6 + NOHEAD law:lei-6044-1974 (UTF-8 BOM page, a
Vide pin; benign). All runs through .tmp/run.py / pipe.sh at BelowNormal behind the cpu gate, one at a time, never two parses;
PIDs printed in each b28 log / pipe output; all mine, all exited. Nothing running. Fetching: archive.org through the shared client
(robots.txt read at start), 2 LexML /urn records (robots.txt read: /urn allowed, Crawl-delay 5; 6 s apart); no challenge page.
New in code: fetch_batch5 drop_bad + BAD_PINS; parse_batch17 PAGES l8159/l9491/l13334/lcp35/l5010, acts/PARTS/ACT_DAY/ACT_LAWS for
zzz-zzzc, blocks '# part zzz', '# part zzza' (NOTE_FIX x2, _W897_4, OPEN_ITEMS), '# part zzzb' (NOTE_FIX LC 54, COURTS rsf-12-1990
/ rsf-31-1993, _W108 + EXPLAINED), '# part zzzc' (VIGENCIA_FIXED lei-13876-2019, LAW_FIELD_FIX lei-6741-1979, MP 246 note/lapse/
rejection, MP_PENDING mp-2161-2001, _W246 + EXTRA_LAWS lei-11483-2007, _W5_8). Backups: brazil-b28/before/.
NEXT: Lei 13.334/2016 (PPI): page l13334 pinned (20261019061454), not configured, `laws`/`missing` not run for it. Heavy: 293 notes
(MP 882/2019 86, Lei 13.901/2019 63, Lei 13.502/2017 25, Lei 14.600/2023 25, MP 922/2020 21, MP 886/2019 19, MP 768/2017 18, MP
782/2017 15, MP 1.161/2023 11, MP 870/2019 6, Lei 15.506/2026 2); it is itself the conversion of MP 727/2016. Read every MP's fate
(conversion or lapse Ato) first and run conv_report.py (copy in brazil-b28) on it. Then the rest of the ranked list.
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once
archive.org has _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026; Atos adc-62-mpv1.340 and adc-77-mpv1.349 (2026 congresso) once
archived -> MPs 1.340/1.349 in part zzx and Lei 12.462 art. 63 § 17 in part v.

## Twenty-ninth session (2026-11-01): Lei 13.334/2016 (PPI), part zzzd
robots.txt read at start (archive.org: Disallow /control/ /report/ only; web.archive.org 404; copies in brazil-b29/robots). Fetching:
archive.org only through the shared client (iaonly.py). Scratch: .gitlaw-scratch/brazil-b29 (before/ = parse_batch17.py,
sources_batch17.json, effects_fix.py, README, jurisdiction.json, bad_pins.json before the session; l13334-reg.txt page dump; trial
parses, span dumps spj1/spj2, conv_report.py copy and logs; pipe outputs zzzd-pipe1/2.out; final29a-build.log).
Pins: `iaonly.py laws l13334` 4 new (law:lei-13502-2017, mp-768-2017, mp-782-2017, mp-1161-2023); `missing` 0; `gap` l13334-compilado
(L13334compilado.htm, ts 20261014174232) and ato:adc-42-2023-mpv1161 (Ato Declaratório 42/2023: MP 1.161 term ended 9.6.2023). headyear
(b29/hy1.log) = b28/hy5. No bad pin.
### 99-batch17zzzd - PUBLISHed: Lei 13.334/2016 (lei-do-programa-de-parcerias-de-investimentos, LPPI, 18 versions 2016-09-13 .. 2026-09-16)
- Config: act (check page l13334-compilado), PARTS zzzd, ACT_DAY 13.9.2016 (art. 22, DOU edição extra), ACT_LAWS lei-13334-2016 (new
  record). Block '# part zzzd' (end of parse_batch17, before SRC): scoped MP_LAPSE mp-1161-2023 (10.6.2023), NOTE_FIX '(Redação da pela
  Medida Provisória nº 768, de 2017)', MP_PENDING mp-768-2017 (revoked by MP 782); EXPLAINED art-07 (compilado drops a full stop);
  OPEN_ITEMS (MP 727 text; MP 768/782 and Lei 13.502 'produção de efeitos' tied to structure decrees with no day: dated by
  publication; Vide pointers); SPAN_FIX _W870 (art. 7 § 1º III/IV: MP 870 wordings end 18.6.2019, Lei 13.844 kept none; Lei 13.502's
  copies 18.6-19.6.2019; CONV_RESTORE not used because its general form also matches the MP 886 copy lines and would assert),
  _W882R (art. 8 I, IV, VI, art. 12 V: gaps 3.5-31.8.2019, MP 882's revocations were not among those MP 886 art. 10 revoked), _W9A
  (art. 9º-A from the promulgation of Lei 13.901's vetoed part, DOU 11.12.2019), _W7A (art. 7º-A p.u. back 30.6.2020), _W8B (MP 882's
  art. 8º-B IV/V end 19.6.2019, replaced by MP 886's; 8º-B without caput 31.8-12.11.2019, EXTRA decision, act-scoped).
- Existing tables used: batch 9's MP_LAPSE mp-882-2019 (31.8.2019) and mp-922-2020 (30.6.2020). 'Alteração revogada pela MP 886' notes
  were already read as MP 886 ends (art. 7 § 1º I, §§ 4º-5º, art. 7º-A, art. 8 caput, art. 8º-B II), as MP 886 art. 10 II-III says.
- pipe.sh zzzd (b29/zzzd-pipe2.out): sha 692134c5 x2, 0 moves, 0 law records set, dupline/dupcheck/order 0, firstline 1 (8º-B, above),
  leakcheck = '(revogado)' text, quotecheck = art. 18, latecaput = art. 7/art. 14 lines under restored caputs (benign), overlap 0,
  uniqlaws 0, missorig 0. conv_report (b29/zzzd-conv2.log): 11 OK, 0 BAD. Installed 3d3843db; README row + jurisdiction.json (269
  acts, 3722 versions). final29a-build.log: 269 acts, 3722 versions, 2657 commits, check 0/0, --compare identical, audit clean main +
  futuro. Every earlier part byte-identical (b29/corpusd-before.txt vs corpusd-after.txt).
- PIDs (all mine, all exited): laws 2188, missing 32508 (failed, wrong args) / 54312, hy 30760, gap 5524 / 28336, trials 23404 / spans
  30304 (conv1) / sp1 / spj1 / 39676 (spj2) / t2, pipe1 30028 14328 43120 42132 3572 11948, pipe2 41956 33228 2796 17240 44952 39340,
  conv2 40408, final 53608.

## State at handoff (batch 17, twenty-ninth session, 2026-11-01)
Installed with .PUBLISH this session: zzzd (Lei 13.334/2016, 18 versions). Final merged build of the installed folder after all docs
(brazil-b29/final29a-build.log): 269 acts, 3722 versions, 2657 commits, check 0/0, --compare identical, audit_push clean on main and
futuro; README row and jurisdiction.json (269 acts, 3722 versions) current. All runs through .tmp/run.py / pipe.sh at BelowNormal
behind the cpu gate, one at a time, never two parses; nothing running. Fetching: archive.org only (robots.txt read); no challenge page.
The twenty-second session's ranked list is now finished. NEXT candidates (public administration, not built; check slugs first):
Lei 14.600/2023 (organização da Presidência e dos Ministérios; current), Lei 13.448/2017 (prorrogação e relicitação de concessões),
Lei 10.180/2001 (sistemas de planejamento, orçamento, contabilidade e controle interno), Lei 9.636/1998 (bens imóveis da União), Lei
8.730/1993 (declaração de bens), Lei 11.473/2007 (Força Nacional).
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once archive.org
has _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026; Atos adc-62-mpv1.340 and adc-77-mpv1.349 (2026 congresso) once archived ->
MPs 1.340/1.349 in part zzx and Lei 12.462 art. 63 § 17 in part v.
OPEN for the coordinator: MP 768/782 and Lei 13.502 'produção de efeitos' (effects on organs from the structure decrees' entry into
force, no day in the acts): dated by publication in zzzd; say if the decree days should be read instead.

## Thirtieth session (2026-11-01): coordinator decision on zzzd, then Leis 13.448, 10.180, 8.730, 11.473, 14.600, 9.636
robots.txt read at start (archive.org: Disallow /control/ /report/ only; web.archive.org 404; copies in brazil-b30/robots). Fetching:
archive.org only through the shared client (iaonly.py). Scratch: .gitlaw-scratch/brazil-b30 (before/ = parse_batch17.py,
sources_batch17.json, effects_fix.py, bad_pins.json, law_records.json, README, jurisdiction.json before the session; tools/dump.py
(page text dumps <id>.txt), tools/conv_report.py copy; logs and pipe outputs).
### 99-batch17zzzd re-PUBLISHed: coordinator decision recorded in OPEN_ITEMS[_LPPI]
- Effects MPs 768/782 and Lei 13.502 leave to undated structure decrees keep the in-force day (an effect left to a later act is not a
  fixed day). Only that decision text changed. pipe.sh zzzd (b30/zzzd-pipe1.out): sha ced79f03 x2, 0 moves, checks as before, merged
  269 acts, 3722 versions, 2657 commits, check 0/0, compare identical, audit clean. Installed 5394d410; PUBLISH line appended.
### Pins
- `iaonly.py pages` (7): l14600 (20261012093944), l13448 (20261018013834), l10180 (20261004225430), l9636 (20261004150309),
  l9636-compilado, l8730 (20261012142849), l11473 (20261010022557). `laws` (all 7 pages) 21 new; `missing` (zzze-zzzg acts) 0.
  gap: law:dec-4427-2002 (decreto/2002/D4427.htm), l11473-compilado (L11473compilado.htm, 2026-05-19 capture).
- Bad pins from l9636's links (headyear BAD): law:lei-12963-2012 (note misprint; page = Lei 12.693/2012), law:mp-152-2003 (page =
  Lei 9.636) removed from sources_batch17.json and added to bad_pins.json. headyear (b30/hy2.log) = b29/hy1.
- notecount: l14600 52 notes (Lei 14.816/2024 30, MP 1.187/2023 18, MP 1.203, Lei 14.875, MP 1.317/2025, Lei 15.352/2026 1 each);
  l13448 5; l10180 9; l8730 0; l11473 81 (Lei 13.500/2017 26, MP 781 14, MP 755 12, Lei 13.756 5, ...); l9636 534 (Lei 14.011 101,
  Lei 13.465 100, MP 915/2019 84, Lei 11.481 59, MP 759 35, MP 1.065/2021 29, MP 852 21, Lei 13.813 20, Lei 14.474 20, ...).
### 99-batch17zzze - PUBLISHed: Lei 13.448/2017 (LRelic, 3), Lei 10.180/2001 (L10180, 5), Lei 8.730/1993 (LDBens, 1)
- Block '# part zzze': scoped VIGENCIA_FIXED lei-13328-2016 = 29.7.2016 (art. 152 I covers its art. 41) and dec-4427-2002 =
  18.10.2002; B12.DECREES dec-4427-2002 (autonomous decree for art. 32 caput/§ 1º, batch 12's Decreto 3.995 model); NOTE_FIX for the
  unclosed Decreto 4.427 note; OPEN_ITEMS LRelic (MP 752 text, Vide) and L10180 (MP 2.112 chain, decree credit). Record
  lei-13448-2017 = 99-batch17w's.
- pipe.sh zzze (b30/zzze-pipe1.out): sha 8fc49496 x2, 0 moves, flags benign (PUBLISH). conv 0. Installed ad1bb5b1; rows-zzze.json;
  merged 272 acts, 3731 versions, 2662 commits, check 0/0, compare identical, audit clean.
### 99-batch17zzzf - PUBLISHed: Lei 11.473/2007 (LFNSP, 13 versions 2007-05-11 .. 2019-06-18)
- Block '# part zzzf': scoped VIGENCIA_FIXED mp-755-2016 = 20.12.2016 (art. 5 II; the reader took I's 1.1.2017), MP_PENDING mp-755-2016
  (revoked by MP 781 art. 3 II), SPAN_FIX _W781 (MP 781's art. 3 §§ 1º-2º end 27.10.2017, Lei 13.500 kept neither), OPEN_ITEMS.
  Check page l11473-compilado (pinned by gap).
- pipe.sh zzzf (b30/zzzf-pipe1.out): sha cca5b66d x2, 0 moves, flags benign (PUBLISH). conv 0. Installed; rows-zzzf.json; merged
  273 acts, 3744 versions, 2669 commits, check 0/0, compare identical, audit clean.
### 99-batch17zzzg - PUBLISHed: Lei 14.600/2023 (LOPM, 7 versions 2023-06-20 .. 2026-02-25)
- Block '# part zzzg': scoped VIGENCIA_FIXED lei-14875-2024 = 31.5.2024 (art. 75 II; the reader took I's 1.8.2024), MP_PENDING
  mp-1203-2023 (revoked by Lei 14.875 art. 74 XVII), EXPLAINED art-63 (_DOTTED), OPEN_ITEMS (MP 1.154 text, art. 74 structures, Vide).
  No compilado archived: check page = annotated page.
- pipe.sh zzzg (b30/zzzg-pipe1.out): sha 7ba31b07 x2, 0 moves, flags benign (PUBLISH). conv 0. Installed; rows-zzzg.json; merged
  274 acts, 3751 versions, 2674 commits, check 0/0, compare identical, audit clean.
### 99-batch17zzm re-PUBLISHed: law record lei-9636-1998 (title without the page's link words) via law_records.json + lawrecords.py
- merged 274 acts, 3751 versions, 2674 commits, check 0/0, compare identical, audit clean (b30/zzm-build.log). Installed cc99f574.
### 99-batch17zzzh - PUBLISHed: Lei 9.636/1998 (LBIU, 22 versions 1998-05-18 .. 2022-12-07)
- Record lei-9636-1998 = law_records.json (new entry). Pinned ctx:camara-lei-9636-1998-original (pinat.py, ts 20250814060134; cdxpre of
  the Chamber's lei-9636 prefix: 7 URLs) to read the 1998 headings; listed through B6.CONTEXT.
- Block '# part zzzh': B15.HEAD_FIX + SPAN_FIX _W6_11481 (art. 6 and Seção II 1998 wordings end 31.5.2007), paragraphs wrapper on
  l9636 (drops the struck 'Seção II-A' heading; moves MP 1.065's art. 1 §§ 1º-2º below Lei 14.011's caput), SPAN_FIX art. 19 'VI -'
  pointer skip, _W2_1065 (art. 2 p.u. restored 7.2.2022), _W42_852 (art. 42 § 1º 'Numerado' notes), EXPLAINED art-16/art-32, OPEN_ITEMS
  (MPs 292/335 of 2006 Vide-only, MP 1.647 chain, MPs 152/2003 and 283/2006 Vide).
- pipe.sh zzzh (b30/zzzh-pipe3.out): sha 76005ca7 x2, 0 moves, flags benign (PUBLISH). conv 0. Installed; rows-zzzh.json; merged
  275 acts, 3773 versions, 2684 commits, check 0/0, compare identical, audit clean.
### Next ranked list (thirtieth session; checked against every installed part's acts and law keys, no request)
 1 Decreto-Lei 3.365/1941 desapropriação [zzzi]   2 Lei 4.132/1962 desapropriação por interesse social [zzzi]
 3 Decreto-Lei 25/1937 tombamento [zzzi]          4 Lei 12.608/2012 Proteção e Defesa Civil   5 Lei 13.089/2015 Estatuto da Metrópole
 6 Lei 9.393/1996 ITR   7 Lei 11.952/2009 regularização fundiária na Amazônia Legal   8 Lei 13.966/2019 franquia
 9 Lei 14.063/2020 assinaturas eletrônicas   10 Lei 13.988/2020 transação tributária   11 Lei 12.990/2014 cotas em concursos
12 Lei 10.887/2004   13 Lei 11.795/2008 consórcio   14 Lei 12.682/2012 digitalização   15 Lei 6.383/1976 ações discriminatórias
16 Lei 10.711/2003 sementes   17 Lei 9.069/1995 Plano Real   18 heavy tax laws: Decreto-Lei 1.598/1977, Lei 11.196/2005
19 historic codes (large): Código Comercial (Lei 556/1850), CPC 1973 (Lei 5.869/1973), Código Civil 1916 (Lei 3.071/1916).
### 99-batch17zzzi - PUBLISHed: Decreto-Lei 3.365/1941 (LDesap, 22), Lei 4.132/1962 (LDIS, 3), Decreto-Lei 25/1937 (LTomb, 2)
- Pages pinned (`iaonly.py pages`): del3365, del3365-compilado, l4132, del0025; `laws` 10 new, `missing` 0. Bad pin law:lei-6306-1978
  (note misprint; page = Lei 6.306/1975) removed + bad_pins.json; gap law:lei-6306-1975. LexML (robots.txt read: /urn allowed,
  Crawl-delay 5; lexml1.py, 6 s apart, 4 records): lei-6602-1978 published 12.12.1978 (footer misprints 1975; the LexML correction
  applies it), lei-4132-1962 7.11.1962, dl-3365-1941 18.7.1941, dl-25-1937 6.12.1937.
- In-force days: DL 3.365 28.7.1941 (DF, 10 days; as Lei 263/1948), Lei 4.132 22.12.1962 (LINDB 45 days), DL 25 9.12.1937 (1916
  Introdução, 3 days in the DF; republication 11.12.1937 in OPEN_ITEMS).
- Block '# part zzzi': paragraphs wrapper on del3365 (MP 2.183-56 'Art. 15A' lines -> art-15-a, MP 700 '§ 2ºA' -> § 2º-A label),
  SPAN_FIX _W15A (MP 2.183 art. 15-A copies: to 9.12.2015 / 18.5.2016-14.7.2023), _W15A4 (§ 4º absent during MP 700), art. 7 second
  sentence second copy from 18.5.2016, NOTE_FIX Lei 6.306 '1978', _W14701_31 (Lei 4.132 art. 2 IX from the promulgation 28.12.2023,
  as part 16e's Lei 14.701 art. 32), EXPLAINED art-05, OPEN_ITEMS (ADIs 2.260/2.332; ADC 87 etc.; DL 25 republication).
- pipe.sh zzzi (b30/zzzi-pipe3.out): sha df7ac180 x2, 0 moves, flags benign (PUBLISH). conv 0. Installed a4fd0439; rows-zzzi.json.
### 99-batch17zzzg re-PUBLISHed: Seção XIII-A heading (Lei 14.816's name line dated by its label's note; it had read from 2023-06-20)
- Found by the new check brazil-b30/tools/dupsame.py <part.json>... (a line > 30 chars printed twice in one unit on some day). pipe.sh
  zzzg (b30/zzzg-pipe2.out): sha 12a1cdd1 x2. Installed 12a1cdd1.
- dupsame over EVERY installed part (b30/dupsame-all.txt): 104 hits in older parts (70-clt 25, 99-batch9 10, 99-batch10 9, 60-phase2 7,
  17zt 6, 17zzn 5, 99-batch7 4, 17zzx 4, 17zzi 4, ...); not reviewed: some will be legitimate repeats (quoted amendments, identical
  incisos), some may be real doubled lines like the two found here. OPEN for the coordinator.

## State at handoff (batch 17, thirtieth session, 2026-11-01)
Installed with .PUBLISH this session: zzze (Leis 13.448/2017, 10.180/2001, 8.730/1993; 9 versions), zzzf (Lei 11.473/2007; 13), zzzg
(Lei 14.600/2023; 7), zzzh (Lei 9.636/1998; 22), zzzi (Decreto-Lei 3.365/1941, Lei 4.132/1962, Decreto-Lei 25/1937; 27) = 9 acts, 78
versions; re-PUBLISHed: zzzd (coordinator decision text), zzm (record lei-9636-1998). Final merged build of the installed folder after
all docs (brazil-b30/final30-build.log): 278 acts, 3800 versions, 2695 commits, check 0/0, --compare identical, audit_push clean on main
and futuro; README rows and jurisdiction.json (278 acts, 3800 versions) current. Only the intended parts changed (b30/corpusd-before.txt
vs corpusd-after.txt). headyear (b30/hy4.log) = b29/hy1. All runs through .tmp/run.py / pipe.sh at BelowNormal behind the cpu gate, at
most 2 at once, never two parses; PIDs printed in each b30 log / pipe output; all mine, all exited; nothing running. Fetching:
archive.org through the shared client (robots.txt read at start), 5 LexML /urn records (robots.txt read; >= 6 s apart); no challenge
page.
New in code: parse_batch17 PAGES (l14600 ... del0025), acts/PARTS/ACT_DAY/ACT_LAWS zzze-zzzi, blocks '# part zzze' (lei-13328-2016,
dec-4427-2002 via B12.DECREES), '# part zzzf', '# part zzzg' (+ l14600 heading wrapper), '# part zzzh' (HEAD_FIX, l9636 wrapper,
SPAN_FIX), '# part zzzi' (del3365 wrapper, SPAN_FIX); law_records.json lei-9636-1998; bad_pins.json + lei-12963-2012, mp-152-2003,
lei-6306-1978. Backups: brazil-b30/before/.
NEXT: the ranked list above from item 4 (Lei 12.608/2012). Run dupsame.py on each new part (add it to pipe.sh if the coordinator agrees).
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once archive.org
has _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026; Atos adc-62-mpv1.340 and adc-77-mpv1.349 (2026 congresso) once archived ->
MPs 1.340/1.349 in part zzx and Lei 12.462 art. 63 § 17 in part v.
OPEN for the coordinator: dupsame's 104 hits in older parts (above). zzzd's open item is settled (decision recorded).

## Thirty-first session (2026-11-01): Task 1 dupsame review (all hits), Task 2 ranked list from Lei 12.608/2012
Scratch: .gitlaw-scratch/brazil-b31 (before/ = the six parts + PUBLISH, pipe.sh, effects_fix.py, oldparts.py before the session;
tools/: dupctx/dupnb/unitat/uhist (unit history), pg/dump/dump13 (page dumps), partdiff (before/after part diff), genfix.py
(writes dup_fixes.json), genallow.py (writes dupsame_allow.json), chk.sh (the file checks + dupsame on a folder); pages/; logs).
### Task 1 DONE: dupsame in the repo, every hit reviewed, real ones fixed, allowlist read by the check
- scripts/brazil-law/dupsame.py (moved from b30/tools, rewritten): it replayed only `changes`, so lines doubled in a version written
  as full `units` (every first version) were never seen: 168 hits, not 104. Prints 'HIT ...' for unlisted hits (exit 1), counts
  allowlisted ones, prints STALE allowlist entries. In pipe.sh after uniqlaws ($x-dup.log).
- Reviewed all 168 against the pages: 132 are the law's own repetitions -> scripts/brazil-law/dupsame_allow.json (act, unit, line,
  why: quoted-amendment elision lines 32, penalty lines 24, repeated heading names 19, tables and parallel lists by article).
  36 were reading faults, all fixed by scripts/brazil-law/dupfix.py + dup_fixes.json (32 entries; ops dedupe / drop / drop_block
  [first] / set; only the named units' text changes, changes recomputed for them only; stops if a fix would leave an uncredited
  change or finds nothing; a decision 'Doubled lines: ...' marks the part done). effects_fix.py runs it after lawrecords, so a
  reparse keeps the fixes (checked: zf reparse + effects_fix = installed except the known sources drift).
- Fixed (and re-PUBLISHed): 60-phase2 (CP art. 121 '(VETADO)' VIII + penalty from 1942 -> from Lei 13.964; art. 129 § 9º 2006
  penalty beside Lei 14.994's 2024-2026; Título VI/Cap. I 1940 names beside Lei 12.015's from 2009; Cap. I-A name from 1942 ->
  2018), 70-clt (art. 530 set per period 1943-1967: it had lost alíneas b-d from 1946 to 1967; arts. 534/538 1943 copies; art. 580
  table doubled 1943-1946 and present under DL 8.740; art. 628-A, art. 553, Título VII headings around MPs 905/955; the 'Open (not
  dated by the source)' decision and batch7/oldparts.py OPEN updated: 534/538 still two wordings 21.1-23.2.1946), 99-batch13f (Lei
  4.595 art. 4º XIV items of each wording stacked 1965-1982), 99-batch17i (Lei 9.250 art. 8º MP 528 + Lei 12.469 copies), 99-batch17zf
  (Lei 9.984 ementa printed three times), 99-batch9 (Código Florestal Cap. III-A name). partdiff: only those units + decisions.
  Two credited units now unchanged on their day (wording-unchanged commits): CLT titulos 18.8.2020 (MP 955 end), Florestal titulos
  18.10.2012 (Lei 12.727). File checks before/after: same or fewer findings (CLT dupcheck 11->8, dupline 95->61, ordercheck 30->25).
- dupsame over every installed part + corpus.json: 0 hits, 132 allowlisted. Merged build (b31/build1.log): 278 acts, 3800 versions,
  2695 commits, check 0/0, --compare identical, audit_push clean main + futuro. PUBLISH appended for the six parts.
- Found, NOT fixed (not doubled lines): CP art. 121 § 6º (Lei 12.720/2012) has no note on either page, so it reads from 1942; CP art.
  121 VIII 'arma de fogo' reads from 23.1.2020 although the part's own rule dates promulgated-over-veto wording 30.4.2021; CLT
  titulos on 18.8.2020 shows the 1943 Título VII name while art. 628-A/553 show MP 905's for that day.
- PIDs (all mine, all exited): dupsame 21320 / dup-all2-4, fixes 28528 30068 6416 48136 (fix3b) + 13f refix, chk runs (one at a
  time), build 52584, zf reparse 48844 + eff 44252.
### Task 2: 99-batch17zzzj - PUBLISHed: Lei 12.608/2012 (lei-da-protecao-e-defesa-civil, LPDC, 3 versions 2012-04-11, 2023-12-13
  Lei 14.750, 2026-03-31 Lei 15.367 art. 36 -> art. 18-A)
- robots.txt read at start (archive.org Disallow /control/ /report/ only; web.archive.org 404; copies in b31/robots). PAGES l12608,
  l13089 pinned (`iaonly.py pages`: l12608 20261019165925, l13089 20261012033005); `laws l12608 l13089` 2 new; `missing` 0.
- Config: act, PARTS zzzj, ACT_DAY (art. 31, on publication; the Lei 6.766 art. 12 § 2º exception is not this act's text), ACT_LAWS
  record = 99-batch7/9/12's. No hand items. Trial 0 problems. pipe.sh zzzj (b31/zzzj-pipe1.out): sha 252c6635 x2, 0 moves, flags
  benign (PUBLISH), dupsame 0. Installed; README row + jurisdiction.json (279 acts, 3803 versions).
- No consolidated page archived for Lei 12.608 (check page = annotated page). Not done: conv_report (no MPs in the act's notes).

## State at handoff (batch 17, thirty-first session, 2026-11-01)
Task 1 DONE (above): dupsame.py + dupsame_allow.json (132 reviewed repetitions) + dupfix.py + dup_fixes.json (36 doubled lines in
6 parts), dupsame in pipe.sh; 60-phase2, 70-clt, 99-batch13f, 99-batch17i, 99-batch17zf, 99-batch9 re-PUBLISHed. Task 2: zzzj
(Lei 12.608/2012) PUBLISHed. Final merged build of the installed folder after all docs (b31/final31-build.log): 279 acts, 3803
versions, 2697 commits, check 0/0, --compare identical, audit_push clean on main and futuro. Only the intended parts changed
(b31/corpusd-before.txt vs corpusd-after.txt). All runs through .tmp/run.py / pipe.sh at BelowNormal behind the cpu gate, one at a
time, never two parses; PIDs in b31 logs and pipe output; all mine, all exited; nothing running. Fetching: archive.org only (4
requests through the shared client), no challenge page.
New in code: dupsame.py, dupsame_allow.json, dupfix.py, dup_fixes.json (generator b31/tools/genfix.py, genallow.py); effects_fix.py
calls dupfix after lawrecords; batch7/oldparts.py OPEN text for 70-clt; pipe.sh dupsame step; parse_batch17 PAGES l12608/l13089,
act/PARTS/ACT_DAY/ACT_LAWS for zzzj. Backups: b31/before/ (parse_batch17.py.orig there already has the PAGES lines).
When a new doubled line is a reading fault: add a dup_fixes.json entry (regenerate with genfix.py or edit by hand), run effects_fix
on the part; when it is the law's own repetition: add it to dupsame_allow.json with its reason.
NEXT: ranked list item 5, Lei 13.089/2015 (Estatuto da Metrópole): page l13089 pinned and its laws pinned; act not configured. Then
Lei 9.393/1996 (ITR), 11.952/2009, 13.966/2019, 14.063/2020, 13.988/2020, 12.990/2014, 10.887/2004, 11.795/2008, 12.682/2012,
6.383/1976, 10.711/2003, 9.069/1995, heavy tax laws, historic codes.
OPEN (found in Task 1, not doubled lines, not fixed): CP art. 121 § 6º (Lei 12.720/2012) has no note on either page and reads from
1942; CP art. 121 VIII 'arma de fogo' reads from 23.1.2020 though the part's rule dates wording promulgated over a veto 30.4.2021;
CLT titulos on 18.8.2020 keeps the 1943 Título VII name while arts. 553/628-A show MP 905's for that day; CLT arts. 534/538 two
wordings 21.1-23.2.1946 (in the CLT open-items decision).
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once archive.org
has _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026; Atos adc-62-mpv1.340 and adc-77-mpv1.349 (2026 congresso) once archived ->
MPs 1.340/1.349 in part zzx and Lei 12.462 art. 63 § 17 in part v.

## Thirty-second session (2026-11-01): Task 1 the four open items from the dupsame review, Task 2 Lei 13.089/2015
Scratch: .gitlaw-scratch/brazil-b32 (before/ = 60-phase2, 70-clt, 99-batch13f + PUBLISH, dup_fixes.json, dupsame_allow.json,
effects_fix.py, parse_batch17.py before the session; tools/: dumpparas.py (older parts: oldparts run + paragraph dump),
dump17.py (the same for a batch-17 part), daydiff.py (before/after diff BY DAY, not by version index), mergedec.py (new part
with decisions in the installed order), ut.py/uh.py (unit text on a day / unit history of any part file), runbuild2.py
(runbuild.py accepting any part name), chk2.sh (file checks + dupsame); re/ = baseline reparses, re2/ = reparses with the
fixes, fin/ = installed files; logs/).
### Task 1 DONE: 60-phase2 and 70-clt re-PUBLISHed (reparse via batch7/oldparts.py + effects_fix, decisions kept in order)
- Baseline first: oldparts + effects_fix reproduce the installed 70-clt exactly and 60-phase2 except the order of one decision.
- (a) CP art. 121 § 6º: Lei 12.720's page, art. 2: 'passa a vigorar acrescido do seguinte § 6º' (the compiled CP page also
  has the note 'Incluído pela Lei nº 12.720, de 2012'; the annotated page has none). Its art. 5 reads 'Esta Lei entra vigor na
  data de sua publicação' (no 'em'), which parse_phase2's clause regex missed, so the law had been dated by LINDB +45 days
  (12.11.2012): parse_phase2 VIGENCIA_FIXED lei-12720-2012 = 28.9.2012. So § 6º starts 28.9.2012 (OLD_FIX) and Lei
  12.720's changes to arts. 129 § 7º and 288-A move from 12.11.2012 to 28.9.2012 (same law, its own clause).
- (b) art. 121 § 2º VIII: OLD_FIX '(VETADO)' 23.1.2020..30.4.2021 (Lei 13.964), 'arma de fogo' from 30.4.2021; the penalty
  line printed after the last inciso starts 23.1.2020 (OLD_FIX; replaces the dup_fixes entry, removed).
- (c) CLT Título VII headings (OLD_FIX on the h109-* heading lines): 1943 block to 12.11.2019; MP 905's block (Título 'DAS
  PENALIDADES E DO PROCESSO ADMINISTRATIVO' + Capítulo I) 12.11.2019..20.4.2020 and 18.8.2020 (gap for MP 955), ends 19.8.2020
  (mp-905-2019-fim); its twin Capítulo I lines skipped; the plain 1943 block from 20.4.2020 with a gap on 18.8.2020. Two
  dup_fixes titulos entries removed.
- (d) CLT arts. 534 § 1º, 538 §§ 1º-2º: DL 8.740's paragraphs carry 'Redação dada' -> the first 1943 copy has a gap
  21.1..23.2.1946 (keeps its place in the article), the second copy skipped (twin); two dup_fixes dedupe entries removed.
  Open now only: art. 538 § 3º (1943, no note) beside DL 8.740's § 2º on the same subject in that window (OPEN text updated).
- Found and fixed: dupfix.py applied each op once per version to a text object several versions shared, so a drop_block
  removed every run, not one. It had removed MP 905's Capítulo I name entirely (CLT, now via (c)) and Lei 4.595 art. 4º XIV
  a)'s three items 19.2.1970..16.5.1974 (99-batch13f). Fix: one deep copy per version. 99-batch13f refixed from its pre-b31
  file (b31/before) with effects_fix: day diff = only those items; re-PUBLISHed. The other dupfix parts are identical with
  the fix (checked on all six).
- Day diffs (daydiff.py): only the intended units/days + decisions (60-phase2: art-121, art-129/288-A 28.9..12.11.2012,
  versions 28.9.2012 new / 12.11.2012 gone / 30.4.2021 credit; 70-clt: art-534, art-538 21.1..23.2.1946, titulos
  12.11.2019..20.4.2020 (Capítulo I name back) and 18.8.2020, 19.8.2020 titulos credit; 13f: art-04 1970..1974).
- Checks before/after (logs/chk-b-*, chk-a-*): all rc 0, same or fewer (CLT dupcheck 8->6, dupline 61->58); dupsame 0 hits;
  uniqlaws 0. Merged build with the three: 279 acts, 3803 versions, 2697 commits, check 0/0, compare identical, audit clean.
### Task 2: 99-batch17zzzk - PUBLISHed: Lei 13.089/2015 (estatuto-da-metropole, EMetr, 6 versions 2015-01-13 .. 2020-07-16)
- robots.txt read at start (archive.org: Disallow /control/ /report/; web.archive.org 404; b32/robots). One archive.org
  request via `iaonly.py gap ato:adc-29-2019-mpv862` (Ato CN 29/2019: MP 862 'encerrado no dia 14 de maio') -> MP_LAPSE.
- Config: act, PARTS zzzk, ACT_DAY (art. 25, publication 13.1.2015), ACT_LAWS (= 99-batch7's record); '# part zzzk' block:
  MP_LAPSE mp-862-2018, TEXT_FIX 'i ncisos', SPAN_FIX art. 4 parágrafo único second copy from 15.5.2019.
- pipe.sh zzzk (b32/logs/zzzk-pipe1.out): sha 9b60a619 x2, 0 problems, flags benign (quotecheck = art. 24's quoted art.
  34-A), dupsame 0, converted-MP report: no case. Installed; README row + jurisdiction.json (280 acts, 3809 versions).
- PIDs (all mine, all exited): reparse/dump 10524 36232 28932 21768 52708 32820 3148 45784 13588 4904 43528, 13f eff 28636,
  checks (chk2.sh, one at a time), builds 21784 25524, gap 43732, trials 21444 572 44616 26212 31964, pipe 52372 28336
  52636 26460 31580 33496 43748, dupsame-all 39376.

## State at handoff (batch 17, thirty-second session, 2026-11-01)
Task 1 DONE: the four open items fixed in 60-phase2 and 70-clt (batch7/oldparts.py OLD_FIX entries for both parts;
parse_phase2 VIGENCIA_FIXED lei-12720-2012; 5 dup_fixes.json entries removed as superseded; OPEN text updated); dupfix.py
shared-object bug fixed and 99-batch13f refixed; all three re-PUBLISHed. Task 2: zzzk (Lei 13.089/2015) PUBLISHed. Final
merged build of the installed folder (b32/logs/final32-build.log): 280 acts, 3809 versions, 2700 commits, check 0/0,
--compare identical, audit_push clean on main and futuro; dupsame over every installed part 0 hits / 132 allowlisted;
uniqlaws 0. corpus.d changed: 60-phase2, 70-clt, 99-batch13f (+ PUBLISH lines), new 99-batch17zzzk (+ PUBLISH). Everything
through run.py / pipe.sh at BelowNormal behind the cpu gate, one process at a time, never two parses; nothing running.
Backups: b32/before/. To rebuild an older part: `oldparts.py <part> --out X`, `effects_fix.py X`, then b32/tools/mergedec.py
for the installed decision order; compare with b32/tools/daydiff.py.
NEXT: ranked list from Lei 9.393/1996 (ITR), then 11.952/2009, 13.966/2019, 14.063/2020, 13.988/2020, 12.990/2014,
10.887/2004, 11.795/2008, 12.682/2012, 6.383/1976, 10.711/2003, 9.069/1995, heavy tax laws, historic codes (pages not pinned
yet: `iaonly.py pages` / `laws` / `missing` first).
OPEN: CLT art. 538 § 3º (1943, no note) beside Decreto-Lei 8.740's § 2º 21.1-23.2.1946 (in the CLT open-items decision).
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once
archive.org has _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026; Atos adc-62-mpv1.340 and adc-77-mpv1.349 (2026
congresso) once archived -> MPs 1.340/1.349 in part zzx and Lei 12.462 art. 63 § 17 in part v.

## Thirty-third session (2026-11-01): Task 1 corpus-wide vigência audit (45-day defaults), Task 2 Lei 9.393/1996
Scratch: .gitlaw-scratch/brazil-b33 (before/ = every part, corpus.json, parsers, effects_fix etc. before the session;
tools/: vigscan.py (every law the parts' decisions list as dated by the LINDB default), enddump.py / ecdump.py (page
endings), ecfetch.py (pinned CF captures), vigcmp.py (reader-level before/after over every pinned law page), vgoff.py
(run a parser with vigforms off = baseline), reparse.sh (base|new reparse + effects_fix, one at a time via run.py),
mkcand.py (new reparse applied to the installed part, keeping installed sources/ai_use), daydiff/mergedec/chk2/runbuild2
(from b32; runbuild2 places corpus.json at the root); re0/ = baselines, re1/re2/ = new (sha equal), fin/ = installed).
robots.txt read at start (archive.org: Disallow /control/ /report/; web.archive.org 404; b33/robots).
### Task 1 DONE
- Audit: 43 laws listed in the parts' 'Laws with no vigência clause' decisions + 9 hand-set no-clause acts + the 16 ECs of
  the CF list; every page's closing text read (enddump1/2.txt, ecdump.txt). The CF pages were not cached on this machine:
  129 pinned archive.org captures fetched through the shared client (ecfetch.py all; 0 bot pages) so parse.py runs again.
- Found (9): Leis 9.165/1995, 9.602/1998, 10.223/2001, 10.408/2002 'entra vigor' (no 'em'); 14.310/2022 'entra vigor após
  decorridos 90 dias'; 8.900/1994 'entre em vigor'; DL 57/1966 'O presente Decreto-Lei entra em vigor, na data';
  6.181/1974 'Esta Lei, que será regulamentada ..., entrará em vigor'; EC 16/1997 'Esta emenda constitucional' (lower
  case). All other listed laws truly have no clause (vetoed closing article or only a revocation article).
- Reader fix: new scripts/brazil-law/vigforms.py (clause_rx widens a reader's clause pattern by alternation; standard()
  rewrites the forms before the day is read; printed() names the clause for a decision). Used in proc/parse_proc.py,
  parse_phase2.py, clt/parse_clt.py, codes/parse_codes.py (clause pattern, vigencia_of, and a vig_notes line 'its clause
  is so printed: ...' for non-hand laws); parse.py final_clause accepts '[Ee]menda'; parse.py BRAZIL_CF_OUT env (scratch
  output). vigcmp over 2,903 pinned pages (proc 2409, phase2 146, clt 273, codes 75): days move only for the found laws
  plus laws used by no reader-dated part (O presente Decreto-lei pages pinned for the CLT, which its own reader already
  read; dl-614/911 are hand-set where used; lei-8845-1994 in no part).
- 99-batch9: Lei 9.602 now in force on the CTB's own first day: P.SAME_DAY_LAWS + decision SAME_DAY_9602 (added in the
  write hook), and SPAN_FIX art-147 parágrafo único ends 22.1.1998 (renumbered by Lei 9.602 art. 2; the renumber rules
  need a later start).
- Table (law, old -> new in-force day, clause): see the session report; parts 70-clt, 99-batch7, 9, 12, 13g, 14d, 16f and
  corpus.json reparsed (baseline with vigforms off = installed except sources/ai_use), day diffs only the intended units
  and decisions (b33/daydiff-final.txt), checks before/after same (chk-b/chk-a logs), dupsame 0, uniqlaws 0, parse x2
  identical; merged build 280 acts, 3809 versions, 2700 commits, check 0/0, compare identical, audit clean; installed and
  PUBLISH lines appended (PUBLISH for the CF).
- Not changed: DL 5.922/1943 (70-clt) dated 'None -> 1943-12-09' (no DOU day on its page, enacted + 45) - noted only.
### Task 2: 99-batch17zzzl - PUBLISHed: Lei 9.393/1996 (lei-do-imposto-territorial-rural, LITR, 8 versions 1997-01-01 .. 2015-01-01)
- Pins: `iaonly.py pages l9393` (20261023190718), `laws l9393` 1 new (law:mp-2166-2001). An all-acts `missing` run pinned
  law:lei-7803-1989 for this act's false note; the pin was removed (the words are law text, see below); act-scoped
  `missing` (BATCH17_PART=zzzl BATCH17_ACTS=lei-do-imposto-territorial-rural) 0. No compilado archived: check page = page.
- Config: PAGES l9393, act, PARTS zzzl, ACT_DAY 1.1.1997 (art. 23 'produzindo efeitos, quanto aos arts. 1º a 22, a partir
  de janeiro de 1997', as Lei 9.249), ACT_LAWS (new record). Block '# part zzzl': paragraphs wrapper on l9393 (art. 10 § 1º
  II a)'s words 'com a redação dada pela Lei nº 7.803, de 18 de julho de 1989;' put back from the bare-note reader; the
  Anexo table after the signature read as unit anexo, one line per cell), VIGENCIA_FIXED lei-12844-2013 (art. 49 V, its
  art. 24) and lei-13043-2014 (1.1.2015: arts. 82-83 in Seção XXI, art. 113 II), MP_PENDING mp-2166-2001, EXTRA decisions,
  EXPLAINED anexo, OPEN_ITEMS (MP 1.528/1996 text; arts. 23-24 dated with the rest).
- pipe.sh zzzl (b33/logs/zzzl-pipe3.out): sha 9276fb83 x2, 0 problems, 0 moves, checks 0 (quotecheck: quoted alínea
  letters only), dupsame 0, uniqlaws 0, conv_report no case. Installed 7cc36131; README row + jurisdiction.json (281 acts,
  3817 versions). Final merged build (b33/logs/final33-build.log): 281 acts, 3817 versions, 2702 commits, check 0/0,
  --compare identical, audit clean main + futuro.
- PIDs (all mine, all exited): vigscan 51184, enddump 34532/28028, ecfetch 34188/45856 (cf all), vigcmp 18080/18336,
  reparses via reparse.sh (PIDs in b33 re0/re1/re2 *.log and logs/re*.out), checks chk2 (one at a time), build1 31280,
  pages 40896, laws 18720, missing (all-acts) + missing2, pipe runs (PIDs in zzzl-pipe*.out), conv, final 45520.

## State at handoff (batch 17, thirty-third session, 2026-11-01)
Task 1 DONE: vigência audit of every 45-day-default law: 9 laws had an in-force clause the readers missed (table in
the session section above and the report). vigforms.py + reader edits (proc, phase2, clt, codes; parse.py for ECs);
corpus.json (CF), 70-clt, 99-batch7, 99-batch9, 99-batch12, 99-batch13g, 99-batch14d, 99-batch16f reparsed, checked and
re-PUBLISHed (PUBLISH lines appended). Task 2: zzzl (Lei 9.393/1996) PUBLISHed. Final merged build of the installed
folder: 281 acts, 3817 versions, 2702 commits, check 0/0, --compare identical, audit_push clean on main and futuro.
Everything through run.py / pipe.sh / reparse.sh at BelowNormal behind the cpu gate, one parse at a time (two dupsame runs
and quick reads were run directly). Nothing running. Fetching: archive.org only (robots read): 16+129 CF captures, 2 pins.
The CF pages are now cached on this machine again (parse.py runs; BRAZIL_CF_OUT=<file> writes elsewhere).
Rebuilding an older part for a reader change: b33/tools/reparse.sh base|new <dir> <part>... then mkcand.py
(installed sources/ai_use kept) and daydiff.py.
NEXT: ranked list from Lei 11.952/2009, then 13.966/2019, 14.063/2020, 13.988/2020, 12.990/2014, 10.887/2004,
11.795/2008, 12.682/2012, 6.383/1976, 10.711/2003, 9.069/1995, heavy tax laws, historic codes (pages not pinned yet;
run `missing` act-scoped: BATCH17_PART/BATCH17_ACTS set, or it pins for every act).
OPEN: CLT art. 538 § 3º (unchanged); DL 5.922/1943 in 70-clt dated enactment + 45 (page has only a CLBR date).
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once
archive.org has _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026; Atos adc-62-mpv1.340 and adc-77-mpv1.349 (2026
congresso) once archived -> MPs 1.340/1.349 in part zzx and Lei 12.462 art. 63 § 17 in part v.

## Thirty-fourth session (2026-11-01): ranked list from Lei 11.952/2009, one act per part (zzzm, zzzn, ...)
Claim: scripts/world-law/claims/brazil-law.txt taken at the start (release at the end). Scratch: .gitlaw-scratch/brazil-b34
(before/ = parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json, dupsame_allow.json, README,
jurisdiction.json, corpus.d/99-batch9.* before the session; logs/; tools/sp.py (compact spansj dump), tools/dupl.py (per
version: repeated paragraph/inciso/alínea labels under one parent, repeated lines)). robots.txt read at start (archive.org:
Disallow /control/ /report/; web.archive.org 404; b34/robots).
### 99-batch17zzzm - PUBLISHed: Lei 11.952/2009 (lei-da-regularizacao-fundiaria-na-amazonia-legal, LRFAL, 9 versions 2009-06-26 .. 2023-12-20)
- Pins (`iaonly.py pages l11952 l11952-compilado`, archive.org: 20261015114123 / 20260310100823; Planalto's consolidated page
  is spelt 'l11952complilado.htm'); `laws` 0 new; act-scoped `missing` (BATCH17_PART=zzzm BATCH17_ACTS=...) 0.
- Config: PAGES l11952 (+ -compilado), act, PARTS zzzm, ACT_DAY 26.6.2009 (art. 41 on publication), ACT_LAWS lei-11952-2009 =
  new law_records.json entry (99-batch9's record had MP 910's struck ementa joined to the title; 99-batch9 re-recorded by
  lawrecords.py, one field, re-PUBLISHed). Block '# part zzzm': SPAN_FIX _W5_910 (art. 5 IV/V and § 1º + I-IV printed again
  after MP 910's struck lines: first copies end 11.12.2019, second from 20.5.2020), _W5_759 (2009 § 1º ends 23.12.2016; MP
  759's parágrafo único 23.12.2016-12.7.2017), _W30_759 (art. 30: MP 759 caput only, '(NR)' with no dotted line -> 2009
  incisos/alíneas/§§ end 23.12.2016; inciso I had been skipped), _W19_910 (art. 19 second struck copy skipped; MP 910 had
  caput + § 1º with no dotted line between -> I-II absent during the MP; I, II, § 1º back 20.5.2020), art. 1 p.u. second
  copy from 20.5.2020 (MP 910 art. 1 caput only) + EXTRA decision; EXPLAINED art-01 (compilado leaves out art. 1 p.u.),
  art-39 (_DOTTED); OPEN_ITEMS (MP 458 text not modelled; the no-dotted-line reading is a judgement call, LC 95 art. 12
  III; Vide ADIN 4.269).
- pipe.sh zzzm (b34/logs/zzzm-pipe3.out): sha 85a98b9e x2, 0 problems, 0 moves, dupline/dupcheck/firstline/pubgap/missorig 0,
  overlap 0, leakcheck 14 = Lei 13.465's '(Revogado)' wordings, ordercheck 1 = art. 18 p.u. '(Revogado)' before §§ as
  printed, quotecheck = arts. 39/40 quoted amendments, latecaput reviewed (all as intended), dupsame 0, uniqlaws 0 (after
  99-batch9 re-record); conv_report no case. Installed 85a98b9e; README row + jurisdiction.json (282 acts, 3826 versions).
  Final merged build (b34/logs/zzzm-final-build.log): 282 acts, 3826 versions, 2703 commits, check 0/0, --compare
  identical, audit clean main + futuro; dupsame (zzzm + 9) 0 / 14 allowlisted.
- PIDs (all mine, all exited): pages 40876, laws 45640, missing 28300, trials 53912/47832/39608/51804, spans 3596, lawtxt
  runs (txt/txtc/mp910/mp759 logs), pipe runs (PIDs in zzzm-pipe*.out), ov3 34988, conv 31428, final 47844, dupsame 52104.
### 99-batch17zzzn - PUBLISHed: Lei 13.966/2019 (lei-de-franquia, LFranq, 1 version 2020-03-26)
- Pin `iaonly.py pages l13966` (archive.org); `laws` 0 links; act-scoped `missing` 0. ACT_DAY 26.3.2020 (art. 10, 90 days
  after DOU 27.12.2019, counted as Lei 13.848's entry); ACT_LAWS new record. No notes, no hand items, no compilado.
- pipe.sh zzzn (b34/logs/zzzn-pipe1.out): sha 33c8a08b x2, every check 0 (leak/order/quote too), overlap 0, latecaput 0,
  dupsame 0, uniqlaws 0. Installed 33c8a08b; README row + jurisdiction.json (283 acts, 3827 versions). Final merged build
  (b34/logs/zzzn-final-build.log): 283 acts, 3827 versions, 2704 commits, check 0/0, compare identical, audit clean.
  PIDs: pages 48340, laws 47852, missing 28156, pipe PIDs in zzzn-pipe1.out, final 49336 (all exited).
### 99-batch17zzzo - PUBLISHed: Lei 14.063/2020 (lei-das-assinaturas-eletronicas, LAssE, 3 versions 2020-09-24, 2023-02-15, 2023-07-14)
- Pin `iaonly.py pages l14063`; `laws` 2 links, 0 new; act-scoped `missing` 0. ACT_DAY 24.9.2020 (art. 20); ACT_LAWS = 13d's
  record. Block '# part zzzo': B8.NAV_LINES l14063 (Não remover/Down/Up/Texto para impressão), paragraphs wrapper (names of
  Capítulos/Seções not centred: rubric or unlabelled line right after a heading -> heading name hN-(M+1); Capítulo II's
  name had been the last line of art. 1) + EXTRA decision, OPEN_ITEMS (MP 983 not modelled).
- pipe.sh zzzo (b34/logs/zzzo-pipe2.out): sha 6ee79c97 x2, all 0 except leakcheck 3 (Lei 5.991 art. 35 '(revogada)' alíneas
  quoted in art. 15) and quotecheck (quoted amendments); conv 0. Installed; README row + jurisdiction.json (284 acts, 3830
  versions). Final merged build (b34/logs/zzzo-final-build.log): 284 acts, 3830 versions, 2705 commits, check 0/0,
  compare identical, audit clean. PIDs: pages 42592, laws 33928, missing 48228, trials 47272/30520/50336/11896/46448,
  paras 53216/44624, pipe PIDs in zzzo-pipe*.out, conv 54512, final 33056 (all exited).
### 99-batch17zzzp - PUBLISHed: Lei 13.988/2020 (lei-da-transacao-tributaria, LTransT, 8 versions 2020-04-14 .. 2025-01-23)
- Pin `iaonly.py pages l13988`; `laws` 6 links, 0 new; act-scoped `missing` 0. ACT_DAY 14.4.2020 (art. 30 II); ACT_LAWS = 17q's
  record. Block '# part zzzp': NAV_LINES l13988; heading-name wrapper of zzzo extended to l13988 (zzzo reparse = installed
  but for the sources request count); SPAN_FIX _W23_120 (art. 23 I + p.u. from 12.8.2020, art. 30 I: 120 days, start_law
  lei-13988-2020 by_provision, as Lei 14.601's single lines); MP_LAPSE mp-1160-2023 2.6.2023 (ADC 41/2023, already pinned)
  + EXTRA (art. 27-B: only its label struck); OPEN_ITEMS. law_records.json mp-1160-2023-fim (neutral note) -> 99-batch17q
  re-recorded (one field, 253bec26) and re-PUBLISHed.
- pipe.sh zzzp (b34/logs/zzzp-pipe1.out): sha a88a59df x2; all 0 except leakcheck 2 ('(revogado)' incisos of the amending
  laws), quotecheck 2 (quoted amendments); latecaput reviewed (Lei 14.375 dotted); conv 0. Installed; README row +
  jurisdiction.json (285 acts, 3838 versions). Final merged build (b34/logs/zzzp-final-build.log): 285 acts, 3838 versions,
  2707 commits, check 0/0, compare identical, audit clean. PIDs: pages 45228, laws 47748, missing 46412, trials
  47420/21168, zzzo-re 28852, pipe PIDs in zzzp-pipe1.out, conv 31716, final 41216 (all exited).
### Lei 12.990/2014 (cotas para negros em concursos) - HELD, not built (coordinator decision needed)
- Pinned (`iaonly.py pages l12990`, PAGES l12990 kept, act removed from ALL_ACTS/PARTS). The page heads 'Revogada pela Lei nº
  15.142, de 2025' and strikes only some lines (preamble, arts. 1, 2 and the signature); art. 6 'terá vigência pelo prazo de
  10 (dez) anos' (Vide ADI 7654: the STF's medida cautelar kept it in force past 10.6.2024 until the new law). Decide: (a) end
  at 10.6.2024 (term, as the PNE's term gap) or at Lei 15.142's repeal (4.6.2025?) under ADI 7.654 (court law note), and (b)
  read the repeal from Lei 15.142's own page (not pinned yet; its in-force clause to read).
### Lei 10.887/2004 (part zzzq) - CONFIGURED, NOT PUBLISHED (stopped here: clean point, context)
- Pins: `iaonly.py pages l10887` (PAGES l10887 = '_ato2004-2006/2004/lei/l10.887.htm'), `laws` 2 new, act-scoped `missing` 0.
  Config in parse_batch17: act lei-10887-de-2004 (L10887), PARTS zzzq, ACT_DAY 21.6.2004 (art. 17), ACT_LAWS = 15a's record.
  No hand block yet. Planalto prints 'Texto compilado' (a compilado page may exist: try `iaonly.py pages` with an id for
  '_ato2004-2006/2004/lei/l10.887compilado.htm' or similar; the check page is the annotated page for now).
- Trial t1 (b34/logs/zzzq-t1.log, 18 versions): 24 problems = (1) Lei 12.618 'no in-force day' x10 + unhandled clause:
  art. 33 staged (part zzp's coordinator decision: read which item covers its changes to Lei 10.887; VIGENCIA_FIXED scoped to
  the act); (2) Lei 13.328/2016 x5 + unhandled clause (art. 119? I publication for arts. 1-16, 40-89, ...; II from 1.8.2016
  ...: read which article amends Lei 10.887); (3) MP_LAPSE needed for mp-556-2011 ('Sem eficácia', staged 'Produção de
  efeito' notes on art. 4 X-XIV etc.: read MP 556's own effect clause) and mp-805-2017 (STF ADI 5.809 suspended it in
  12.2017, then it lapsed in 4.2018: Atos not pinned; a court law for the suspension); MP_PENDING/revocation for
  mp-1203-2023 (part zzzg has the MP_PENDING text: revoked by Lei 14.875/2024 art. 74 XVII, scope it to this act too);
  (4) 'restored wording after an open one' on art. 4 caput, VI, XIX and art. 5 caput (expected to clear once the MP fates
  are known; check with spansj + b34/tools/sp.py). dupl (b34/tools/dupl.py) on t1: art. 4 XIX doubled on 1.6.2012.
  Notes also cite MPs 431/2008 (-> 11.784), 449/2008 (-> 11.941), 497/2010 (-> 12.350, notes read 'pela de Medida
  Provisória'), 765/2016 (-> 13.464), 871/2019 (-> 13.846): converted-MP rule + conv_report after the fixes.

## State at handoff (batch 17, thirty-fourth session, 2026-11-01)
Installed with .PUBLISH this session: zzzm (Lei 11.952/2009; 9 versions), zzzn (Lei 13.966/2019; 1), zzzo (Lei 14.063/2020;
3), zzzp (Lei 13.988/2020; 8) = 4 acts, 21 versions; re-PUBLISHed for shared law records: 99-batch9 (lei-11952-2009 title)
and 99-batch17q (mp-1160-2023-fim note), both via new law_records.json entries + lawrecords.py, one field each. Final merged
build of the installed folder (b34/logs/zzzp-final-build.log): 285 acts, 3838 versions, 2707 commits, check 0/0,
--compare identical, audit_push clean on main and futuro; uniqlaws --all 0; dupsame over every installed part 0 hits / 132
allowlisted (b34/logs/dupsame-all2.log). README rows and jurisdiction.json (285 acts, 3838 versions) current. corpus.d
changed: new 99-batch17zzzm/zzzn/zzzo/zzzp (+ PUBLISH), 99-batch9.json and 99-batch17q.json (one law-record field each, +
PUBLISH lines). All runs through run.py / pipe.sh at BelowNormal behind the cpu gate, one at a time (never two parses);
PIDs in the part sections; all mine, all exited; nothing running. Fetching: archive.org only through the shared client
(robots.txt read at start): 7 page pins + 2 law pins; no LexML, no Common Crawl; no challenge page.
New in code: parse_batch17 PAGES l11952 (+ 'complilado'), l13966, l14063, l13988, l12990 (pinned, held), l10887; acts/PARTS/
ACT_DAY/ACT_LAWS zzzm-zzzq; blocks '# part zzzm' (SPAN_FIX art. 5/19/30/1, EXPLAINED, OPEN_ITEMS), '# part zzzo'
(NAV_LINES, heading-name wrapper for l14063 + l13988, OPEN_ITEMS), '# part zzzp' (NAV_LINES, art. 23 staged SPAN_FIX,
MP_LAPSE mp-1160-2023, OPEN_ITEMS); law_records.json + lei-11952-2009, mp-1160-2023-fim. Backups: brazil-b34/before/.
Judgement call to confirm: an MP's quoted article with no dotted line leaves out the units it does not quote during the
MP's term (zzzm: art. 30 under MP 759; art. 1 p.u. and art. 19 I-II under MP 910), as zzzi's MP 700 art. 15-A § 4º.
NEXT: finish zzzq (Lei 10.887, to-do above), then 11.795/2008, 12.682/2012, 6.383/1976, 10.711/2003, 9.069/1995, heavy tax
laws, historic codes; Lei 12.990 held (decision above). Run `missing` act-scoped (BATCH17_PART/BATCH17_ACTS).
OPEN (unchanged): CLT art. 538 § 3º; DL 5.922/1943 in 70-clt dated enactment + 45.
DATED RE-CHECKS (unchanged): MP 1.382/2026 (part m) on or after 29.11.2026; MP 1.370/2026 (part zv, and Lei 12.871) once
archive.org has _ato2023-2026/2026/mpv/mpv1370.htm after 30.10.2026; Atos adc-62-mpv1.340 and adc-77-mpv1.349 (2026
congresso) once archived -> MPs 1.340/1.349 in part zzx and Lei 12.462 art. 63 § 17 in part v.

## Thirty-fifth session (2026-11-01): coordinator decisions (MP '(NR)' no dotted line; Lei 12.990), then Lei 10.887 (zzzq)
Claim: scripts/world-law/claims/brazil-law.txt taken at the start (release at the end). Scratch: .gitlaw-scratch/brazil-b35
(before/ = parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json, dupsame_allow.json, README,
jurisdiction.json before the session; logs/; tools/ = b34's sp.py, dupl.py, paras.py). robots.txt read at start (archive.org:
Disallow /control/ /report/; web.archive.org 404; b35/robots).
### Decision 1 (MP '(NR)' with no dotted line): confirmed; 99-batch17zzzm re-PUBLISHed
- OPEN_ITEMS[_LRFAL] now cites LC 95/1998 art. 12 III (whole unit replaced) instead of 'judgement call', and names all three
  cases (art. 1 p.u. and art. 19 I-II under MP 910, art. 30 under MP 759). pipe.sh zzzm (b35/logs/zzzm-pipe1.out): 762d3bc8 x2,
  only that decision line and the sources request count changed; checks as before. Installed, PUBLISH line appended.
### 99-batch17zzzr - PUBLISHed: Lei 12.990/2014 (lei-12990-de-2014, L12990, 2 versions 2014-06-10, 2025-06-04)
- Decision 2: no lapse at art. 6's 10-year term (STF medida cautelar ADI 7.654); B9.REPEALS -> empty version on 4.6.2025
  credited to lei-15142-2025 (art. 13; art. 14 in force on publication, DOU 4.6.2025) + EXTRA decision (term + ruling) +
  OPEN_ITEMS (ADI not a version; art. 11 saving clause). Pins: PAGES l12990-2025 (`pinat.py`, ts 20250531000943, before the
  repeal: the later page strikes only some lines), l15142 (`iaonly.py pages`); `laws` 0, act-scoped `missing` 0.
- pipe.sh zzzr (b35/logs/zzzr-pipe2.out): 18b5ecdc x2, every check 0, REPEAL CHECK 0 articles differ, dupsame 0, uniqlaws 0;
  merged 286 acts, 3840 versions, 2709 commits, check 0/0, compare identical, audit clean. Installed; README row +
  jurisdiction.json (286 acts, 3840 versions).
### 99-batch17zzzq - PUBLISHed: Lei 10.887/2004 (lei-10887-de-2004, L10887, 22 versions 2004-06-21 .. 2026-03-31)
- Pins (archive.org, shared client): ato:ato-19-2018-mpv805 (MP 805 in force to 8.4.2018), ato:apn-25-2012-mpv556 (MP 556 to
  31.5.2012), ctx:camara-noticia-530114-adi-5809 (dating only) and ctx:stf-adi-5809-liminar (the STF decision PDF, capture
  20180107121948, text layer read with pypdf in b35/pdf; no OCR). One WebSearch (stf/camara domains) to find the decision.
- Block '# part zzzq' (scoped): VIGENCIA_FIXED lei-12618-2012 (art. 33 II, 2.5.2012), lei-13328-2016 (art. 152 I),
  mp-556-2011 (effects 1.4.2012, art. 7 I), lei-12688-2012 (art. 36 IV, 19.7.2012; the reader had taken III's 1.6.2012),
  lei-14875-2024 (art. 75 II); MP_LAPSE mp-556-2011 1.6.2012 and mp-805-2017 9.4.2018 (text = 95-rju's, so the -fim record
  is shared); MP_PENDING mp-1203-2023; COURTS stf-adi-5809. ADI 5.809 MC (18.12.2017) suspended MP arts. 1-34 and 40 I-II and
  Lei 10.887 art. 4 I-II, § 3º and art. 5 in the MP's wording. Model (_W805 decision): increase lines (art. 4 caput/I/II,
  § 3º + I/II, art. 5 + p.u.) never take effect (art. 38: effects from 1.2.2018, after the ruling) -> skipped, with the
  struck repeats of 12.618's art. 4 and 2004 art. 5; art. 4 II a)-b) gap 30.10-18.12.2017 and art. 6 + p.u. absent in that
  window, back from the ruling; § 1º VI / XXV (not named by the ruling) MP wording to the lapse, VI back 9.4.2018.
  paragraphs wrapper: 'Sem eficácia' markers stripped; art. 10's 'redação dada pela MP 2.187-13 ...' kept as text (it had
  made a same_day version credited to MP 2.187). law_records.json + lei-12618-2012 (99-batch17zzp's record; zzp unchanged).
  OPEN_ITEMS (MP 167 text, ADI's later fate, Vide EC 47 / ADI 4.582). conv_report: no case.
- pipe.sh zzzq (b35/logs/zzzq-pipe2.out): c80bfeda x2, 0 problems, leakcheck 5 + quotecheck 17 = quoted amendments in
  arts. 10-14 as printed, rest 0, uniqlaws 0, dupsame 0; installed 61c7800f; README row + jurisdiction.json.
- NOTE: an edit mid-session spliced a duplicate of the zzzg..zzzq blocks into parse_batch17 (index of the wrong
  MP_PENDING); repaired (broken copy b35/parse_batch17.broken.py) and the diff against b35/before/ shows only the intended
  changes. zzzm/zzzr were piped before that edit and zzzq after the repair.
- PIDs (all mine, all exited): run.py children in b35/logs (lawtxt/cdx/pins/trials/sp/pipe/docs: 54916, 27256, 11272,
  26416, 12964, 21320, 41548, pipe PIDs in zzzr-pipe1/2.out, zzzm-pipe1.out, zzzq-pipe1/2.out, 39416, 45760 (gaps.py
  failed at once: it tries Common Crawl first and the client refused, no request), 32248, 36948, 18416, 53508, 18944,
  20844, final 576, uniqlaws 1064). One stray background shell (a slow `find` over .cache) stopped by its own task id.

## State at handoff (batch 17, thirty-fifth session, 2026-11-01)
Installed with .PUBLISH this session: zzzr (Lei 12.990/2014; 2), zzzq (Lei 10.887/2004; 22); re-PUBLISHed zzzm (decision line
only). Final merged build of the installed folder (b35/logs/final-build.log): 287 acts, 3862 versions, 2714 commits, check 0/0,
--compare identical, audit_push clean on main and futuro; uniqlaws --all 0. README rows + jurisdiction.json (287 acts, 3862
versions) current. corpus.d changed: new 99-batch17zzzq/zzzr (+ PUBLISH), 99-batch17zzzm.json (+ PUBLISH line).
law_records.json + lei-12618-2012. Fetching: archive.org only (robots read): 2 page pins, 2 Ato pins, 2 ctx pins; no LexML, no
Common Crawl, no Arquivo.pt; no challenge page.
NEXT: ranked list from Lei 11.795/2008, then 12.682/2012, 6.383/1976, 10.711/2003, 9.069/1995, heavy tax laws, historic codes.
Rule learnt: read an STF ruling's own dispositive text (stf.jus.br/arquivo PDFs via archive.org) for its scope before
modelling a suspension; the Câmara news gives the date only.
OPEN / DATED RE-CHECKS: unchanged from the thirty-fourth handoff.

## Thirty-sixth session (2026-11-01): ranked list from Lei 11.795/2008, one act per part (zzzs, ...)
Claim: scripts/world-law/claims/brazil-law.txt taken at the start (release at the end). Scratch: .gitlaw-scratch/brazil-b36
(before/ = parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json, dupsame_allow.json, README,
jurisdiction.json before the session; logs/; tools/ = b35's). robots.txt read at start (archive.org: Disallow /control/
/report/; web.archive.org 404; b36/robots). Coordinator rule confirmed: a change an STF ruling suspends before its own
effect day never takes effect (no version, a decision line); MP 805 in Lei 10.887 kept as built.
### 99-batch17zzzs - PUBLISHed: Lei 11.795/2008 (lei-do-sistema-de-consorcios, LSCons, 4 versions 2009-02-06 .. 2017-11-14)
- Pin `iaonly.py pages` (l11795 = _ato2007-2010/2008/lei/l11795.htm, archive.org); `laws` 2 linked, 0 new; act-scoped
  `missing` 0. ACT_DAY 6.2.2009 (art. 49: 120 days after DOU 9.10.2008); ACT_LAWS new record lei-11795-2008.
- Block '# part zzzs': SPAN_FIX _W42_784 (MP 784 art. 52 caput only, '(NR)' no dotted line -> art. 42 I-VIII + p.u. absent
  8.6-19.10.2017; Planalto's second copies printed after the MP caput start 20.10.2017, were dated from 2009 = overlap),
  _W784_REV (MP 784 art. 57 I h) revoked art. 7 IV, 43, 44 on 8.6.2017: gap to 20.10.2017); Lei 13.506 art. 63 + 71 XIV
  (14.11.2017) read on its page. MP_LAPSE mp-784-2017 already shared (batch7, Ato CN 56/2017). OPEN_ITEMS (Lei 13.506
  art. 64 not shown).
- pipe.sh zzzs (b36/logs/zzzs-pipe1.out): ebfdfa2a x2, 0 problems, leakcheck 9 = Lei 13.506's '(revogado)' incisos as
  printed, every other check 0, uniqlaws 0, dupsame 0; merged 288 acts, 3866 versions, 2715 commits, check 0/0, compare
  identical, audit clean main + futuro. Installed; README row + jurisdiction.json (288 acts, 3866 versions).
- PIDs (mine, all exited): pages 39548, laws 51928, missing 15532, trial 38552/42724, spans 38676, pipe PIDs in
  zzzs-pipe1.out (43264, 46568, 35520, 54604, 41840, 45544, 15684). One stray background grep (regex backtracking) stopped by
  its own task id.
### 99-batch17zzzt - PUBLISHed: Lei 12.682/2012 (lei-da-digitalizacao-de-documentos, LDigDoc, 4 versions 2012-07-10 .. 2021-06-28)
- Pages l12682, l6383 (leis/l6383.htm), l10711 (leis/2003/l10.711.htm) pinned in one `iaonly.py pages` run (3, archive.org);
  `laws` for the three (6 linked, 2 new), act-scoped `missing` 0. ACT_DAY 10.7.2012 (art. 8); ACT_LAWS new record.
- No hand items: MP 881 art. 11 (30.4.2019, art. 19) -> Lei 13.874 art. 10 (20.9.2019, art. 20 II); Lei 14.129 art. 53
  (art. 3 caput only; 28.6.2021, art. 55 I, as the corpus dates Lei 14.129). conv_report no case.
- pipe.sh zzzt (b36/logs/zzzt-pipe1.out): a734fe88 x2, all 0, latecaput 1 = art. 3 p.u. under the 2021 caput (intended);
  merged 289/3870/2716, check 0/0, compare identical, audit clean. Installed; README row + jurisdiction.json.
### 99-batch17zzzu - PUBLISHed: Lei 6.383/1976 (lei-do-processo-discriminatorio-de-terras-devolutas, LDiscr, 3 versions 1976-12-09, 2009-02-11, 2009-06-26)
- ACT_DAY 9.12.1976 (art. 33); ACT_LAWS new record. MP 458 art. 40 (art. 29 § 1º; 11.2.2009, art. 43); Lei 11.952 (its
  conversion) does not amend Lei 6.383 -> 1976 wording back 26.6.2009 (reader already dates it so; block '# part zzzu' adds
  the decision line only). conv_report no case (dated already).
- pipe.sh zzzu (b36/logs/zzzu-pipe1.out): 64551042 x2, all 0; lawrecords set lei-11952-2009 title (agreed record);
  merged 290/3873/2717, check 0/0, compare identical, audit clean. Installed 9638745e; README row + jurisdiction.json.
### 99-batch17zzzv - PUBLISHed: Lei 10.711/2003 (lei-do-sistema-nacional-de-sementes-e-mudas, LSem, 2 versions 2003-11-04, 2022-12-30)
- ACT_DAY 4.11.2003 (art. 51, 90 days after DOU 6.8.2003, LC 95 count as Lei 13.966); ACT_LAWS new record. Lei 14.515 art. 50
  X (art. 42, art. 43 I-VI) effects on publication (art. 51 III, 30.12.2022). No hand items.
- pipe.sh zzzv (b36/logs/zzzv-pipe1.out): dffbb6a5 x2, all 0 but quotecheck 2 (arts. 22/45 quote 'Semente de'/'Muda de');
  merged 291/3875/2719, check 0/0, compare identical, audit clean. Installed c83a5e13; README row + jurisdiction.json.
- PIDs (mine, all exited): pages 44808, laws 8604, missing 49520, trials 41404/46320/39088, spans + lawtxt runs (logs/),
  conv 28732/35968/35096, pipe PIDs in zzzt/zzzu/zzzv-pipe1.out.
### 99-batch17zzzw - PUBLISHed: Lei 9.069/1995 (lei-do-plano-real, LPReal, 16 versions 1995-06-30 .. 2023-06-20)
- Pin `iaonly.py pages` (l9069 = leis/l9069.htm); `laws` 15 linked, 2 new; `missing` 0; gap pins (archive.org):
  law:mp-320-2006, ato:atocn-2006-mpv320 (the 60-day extension, CN 56/2006), ato:adt-1-2006-mpv320 (Senate rejection,
  13.12.2006). ACT_DAY 30.6.1995 (art. 85); ACT_LAWS new record lei-9069-1995.
- Block '# part zzzw' (scoped): VIGENCIA_FIXED lei-13820-2019 1.7.2019 (art. 11 'primeiro dia do semestre subsequente', DOU
  3.5.2019); NOTE_FIX x2 ('Medida Provisória nº 320, 2006'); MP_LAPSE mp-320-2006 13.12.2006 (rejected; as MP 446/850);
  paragraphs wrapper (strip 'Sem eficácia' on l9069; art. 72's quoted Lei 4.131 'Art. 58.' line label '' so it ends with
  art. 72); SPAN_FIX _W65_320 (1995 § 1º incisos I-III and § 3º gap 25.8-13.12.2006: MP 320's § 1º is one sentence),
  _W67_784 (art. 67 caput/§1º/§2º gap 8.6-20.10.2017, MP 784 art. 57 I d); § 2º ends 14.11.2017: note lacks '('),
  EXTRA (MP 1.303/2025 art. 74 XXXIII on arts. 53-54 with effects 1.1.2026, lapsed 8.10.2025 -> never took effect, no
  version), EXPLAINED art-76 (quoted dotted '§ 1º'), OPEN_ITEMS.
- pipe.sh zzzw (b36/logs/zzzw-pipe1.out): b860a4b0 x2, 0 problems; dupline 2/dupcheck 1 = art. 78 quoting two Lei 8.884
  '§ 3º'; leakcheck 1 = art. 9 IV '(revogado).' (Lei 13.844's own wording); quotecheck = quoted amendments; latecaput 3
  reviewed (caput-only changes with dotted lines); conv 0; merged 292/3891/2723, check 0/0, compare identical, audit clean.
  Installed fdf5167e; README row + jurisdiction.json.
- PIDs (mine, all exited): pages 4224, laws 45456, missing 8804, gaps 8472/42040/27552, trials 43232/34792/14944/30808,
  spans + lawtxt runs (logs/), pipe PIDs in zzzw-pipe1.out, conv 42388, final 40276, dupsame 39196.

## State at handoff (batch 17, thirty-sixth session, 2026-11-02)
Installed with .PUBLISH this session: zzzs (Lei 11.795/2008; 4), zzzt (Lei 12.682/2012; 4), zzzu (Lei 6.383/1976; 3), zzzv
(Lei 10.711/2003; 2), zzzw (Lei 9.069/1995; 16) = 5 acts, 29 versions. Final merged build of the installed folder
(b36/logs/final-build.log): 292 acts, 3891 versions, 2723 commits, check 0/0, --compare identical, audit_push clean on main
and futuro; uniqlaws --all 0; dupsame over the 5 new parts 0. README rows + jurisdiction.json (292 acts, 3891 versions)
current. corpus.d changed: new 99-batch17zzzs..zzzw (+ .PUBLISH); no other part touched; folder PUBLISH unchanged.
parse_batch17.py: diff against b36/before/ is additions only (PAGES l11795, l12682, l6383, l10711, l9069; 5 acts; PARTS
zzzs-zzzw; ACT_DAY/ACT_LAWS; blocks '# part zzzs', '# part zzzu', '# part zzzw'); copy in b36/parse_batch17.after.py.
law_records.json unchanged. Fetching: archive.org only, shared client (robots read at start): 5 page pins, 2 law pins
(`laws`), 3 gap pins (MP 320 + 2 Atos); no Common Crawl, no Arquivo.pt, no LexML, no challenge page. All runs through
run.py / pipe.sh at BelowNormal behind the cpu gate, one at a time; all PIDs mine and exited; nothing running.
NEXT: heavy tax laws, then historic codes (rank and check each against installed parts first).
OPEN / DATED RE-CHECKS: unchanged from the thirty-fourth handoff.

## Thirty-seventh session (2026-11-02): heavy tax laws, one act per part (zzzx, ...)
Claim: scripts/world-law/claims/brazil-law.txt taken at the start (released at the end). Scratch: .gitlaw-scratch/brazil-b37
(before/ = parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json, dupsame_allow.json, effects_fix.py, README,
jurisdiction.json before the session; logs/; tools/ = b36's + state.py (units on a day; reads 'units' and 'changes')).
robots.txt read at start: archive.org (Disallow /control/ /report/), web.archive.org 404, www.lexml.gov.br (/urn allowed,
Crawl-delay 5; /busca/ /doc/ /linker/ Disallowed); copies in b37/robots.
Ranked check (no request): of the heavy tax laws only Decreto-Lei 1.598/1977 and Lei 11.196/2005 are not installed (7.689,
9.249, 9.250, 7.713, 9.430, 9.718, 10.637, 10.833 are in parts h-zl).
### 99-batch17zzzx - PUBLISHed: Decreto-Lei 1.598/1977 (decreto-lei-1598-de-1977, DL1598, 22 versions 1978-01-01 .. 2024-01-01)
- Pins (`iaonly.py pages`, archive.org, one run for 4 pages): del1598, del1598-compilado, l11196, l11196-compilado (the last two
  for the next part, not configured). `laws` 24 linked, 9 new; `missing` (BATCH17_PART=zzzx BATCH17_ACTS=decreto-lei-1598-de-1977)
  0, then 1 (dl-1870-1981 after the NOTE_FIX). Bad pin law:dl-1648-1977 (art. 10 'Vide Decreto-lei nº 1.648, de 1977' links
  DL 1.648/1978) removed + bad_pins.json. LexML (`lexml1.py`, 6 s apart, 3 records): dl-1730-1979 (DOU 17.12.1979; footer
  1982), dl-1654-1978 (urn 1978-12-29: signed and DOU 29.12.1978; page heading 9.1.1978, footer 10.1.1979), dl-1733-1979.
- ACT_DAY 1.1.1978 (art. 67 effects clause, as Lei 9.249); ACT_LAWS new record dl-1598-1977.
- Block '# part zzzx' (scoped): NOTE_FIX DL 1.870 ('1981' without 'de') and art. 19 IV 'Incluído pelo DL 2.065' -> 2.064 (words
  are DL 2.064's art. 20 I); page_info wrapper for dl-1654-1978 (enacted/published 29.12.1978 from LexML); paragraphs wrapper
  (Subseção III's struck 1977 names -> titulos h26-1/h26-2) + apply_span_fix wrapper (heading lines end 1.1.2015, SPAN_FIX
  skips headings); TEXT_FIX 'líquid o', stray closing quote art. 60 § 3º c); SPAN_FIX art. 8 II (1978 to 1.1.2015, Lei 12.973
  art. 117 III a), printed unstruck), art. 19 IV (DL 2.064 20.10-28.10.1983), art. 60 IV (1977 inciso stands; the misplaced
  art. 19 IV line on both Planalto pages skipped: DLs 2.064/2.065 never touch art. 60 IV), art. 61 §§ 2º-3º end 20.10.1983
  (whole-article wording of DL 2.064/2.065), art. 38 § 2º + a)/b) end with Lei 14.789 (MP 1.185's revocation never took
  effect: converted before its 1.1.2024 effect day; decision line, as MP 114 in 17j); EXPLAINED 14 units; OPEN_ITEMS (art. 67
  application rules, DL 1.730 art. 8, Lei 8.981 / 9.430 kept days, Lei 12.973 art. 119 § 1º option, DL 2.287 art. 22 regime).
- effects_fix.py MOVES "99-batch17zzzx.json": Lei 8.541 -> 1.1.1993, Lei 14.789 -> 1.1.2024 (4 moves).
- law_records.json + lei-7713-1988 (99-batch17j's record; the `laws` pin is LEIS/L7713.htm); dupsame_allow.json + the rubric
  'Baixa de Bens do Ativo Imobilizado' (before arts. 44 and 49).
- pipe.sh zzzx (b37/logs/zzzx-pipe2.out): f8f224f7 x2, 0 problems; dupline 2/ordercheck 1 = art. 48 'Il' as printed; firstline
  1 = art. 54 p.u. after its caput's revocation (DL 2.287 art. 31: caput only); leakcheck 0; quotecheck = quoted words as
  printed; latecaput 29 reviewed (Lei 12.973 dotted lines read on its page); dupsame 0 / 1 allowlisted; uniqlaws 0; merged
  293 acts, 3913 versions, 2736 commits, check 0/0, --compare identical, audit_push clean main + futuro. Installed 46f60ea5;
  README row + jurisdiction.json (293 acts, 3913 versions).
- PIDs (all mine, all exited): pages 36736, laws 36392, missing 18692/44736, lexml 31856, trials 6844/35132/50088/24536 + t5,
  spans (sp1/sp2/sp3 logs), lawtxt runs (b37/logs/txt-*), pipe1 PIDs 27400 52716 33896 ... 25132 31788 (+build), pipe2 33448
  31272 49304 21532 31844 31188 15404.
### Lei 11.196/2005 (Lei do Bem) - NOT STARTED beyond pins (next part zzzy)
- Pages l11196 (ts 20261021231658) and l11196-compilado (20261004132825) pinned and in PAGES; no act, no `laws` yet. Survey of
  the annotated page (311 KB, ~70 amending acts): Lei 12.859/2013 (86 notes), Lei 15.504/2026 (74), MP 1.318/2025 (67; fate to
  read), LC 214/2025 (43; 2027+ on futuro), MP 1.034/2021 (42) and Lei 14.183/2021, MP 694/2015 (33, lapsed: MP_LAPSE exists,
  part h), MP 1.095/2021 (27) and Lei 14.374/2022, MP 613/2013, Leis 12.715/2012, 11.774/2008, 11.487/2007, MP 690/2015 ->
  Lei 13.241/2015 (one note misprints '1941'), MP 428/2008, Lei 11.727/2008, MP 457/2009, Lei 14.652/2023, Lei 13.161/2015,
  MP 1.227/2024 (Ato Declaratório 36/2024: rejected, never took effect - part 12.865 precedent), ADIN 4254, LC 228/2026, Lei
  15.394/2026, plus many single notes. Art. 132 is staged ('produzindo efeitos' I-IV; effects_fix already cites IV for other
  acts). Expect several sessions: configure, `laws` + `missing` act-scoped, then work MP by MP.

## State at handoff (batch 17, thirty-seventh session, 2026-11-02)
Installed with .PUBLISH this session: zzzx (Decreto-Lei 1.598/1977; 22 versions). Merged scratch build (b37/logs/zzzx-pipe2.out):
293 acts, 3913 versions, 2736 commits, check 0/0, --compare identical, audit_push clean on main and futuro; uniqlaws 0; dupsame
0. README row + jurisdiction.json current. corpus.d changed: new 99-batch17zzzx.json + .PUBLISH only; folder PUBLISH unchanged.
Other files changed: parse_batch17.py (diff against b37/before/ is additions only: PAGES del1598(+compilado), l11196(+compilado);
act; PARTS zzzx; ACT_DAY/ACT_LAWS; block '# part zzzx'; copy b37/parse_batch17.after.py), effects_fix.py (MOVES zzzx),
law_records.json (+ lei-7713-1988), bad_pins.json (+ law:dl-1648-1977), dupsame_allow.json (+1), sources_batch17.json (pins).
Fetching: archive.org only through the shared client (4 page pins, 10 law pins incl. the gap pin, 1 bad pin removed), LexML 3
URN records 6 s apart; no Common Crawl, no Arquivo.pt, no challenge page. All runs through run.py / pipe.sh at BelowNormal behind
the cpu gate, one at a time; all PIDs mine and exited; nothing running.
NEXT: Lei 11.196/2005 (part zzzy; survey above), then the historic codes (Código Comercial Lei 556/1850, CPC 1973 Lei
5.869/1973, Código Civil 1916 Lei 3.071/1916; check each against installed parts first).
OPEN / DATED RE-CHECKS: unchanged from the thirty-fourth handoff.

## Thirty-eighth session (2026-11-02): Lei 11.196/2005 (Lei do Bem), part 99-batch17zzzy - CONFIGURED, NOT PUBLISHED
Claim: scripts/world-law/claims/brazil-law.txt taken at the start (released at the end). Scratch: .gitlaw-scratch/brazil-b38
(before/ = parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json, dupsame_allow.json, effects_fix.py, README,
jurisdiction.json before the session; logs/; tools/ = b37's + multi.py (page passages for many 'key|regex|chars' lines in one
process, spec1.txt/spec2.txt are the ones read), hrefsm.py (fate links: Vigência/Convertida/Ato on pages), hrefrx.py (<page>
<rx>: hrefs of matching anchors), robots.py). robots.txt read at start: archive.org (Disallow /control/ /report/),
web.archive.org 404 (b38/robots). No LexML, no Common Crawl, no Arquivo.pt request; no challenge page.
### Done (configuration; diff of parse_batch17.py against b38/before/ is additions only; copy b38/parse_batch17.after.py)
- ALL_ACTS: `lei-do-bem` (LBem, pages l11196 / l11196-compilado, law lei-11196-2005); PARTS zzzy; ACT_DAY 22.11.2005 (art. 132
  quoted; VIII 'demais dispositivos' on publication); ACT_LAWS lei-11196-2005; law_records.json + lei-11196-2005 (the record the
  12 parts already share, title 'I nstitui ...' as they print it).
- Gates (art. 132): _GBEM in _GATES: III d) arts. 37, 45, 66, 106-108 -> 1.12.2005; IV b) arts. 17-27, 31, 32, 34, 70-90 ->
  1.1.2006; V c) arts. 47, 48, 51, 56-62, 64, 65 -> 1.3.2006 (1st day of the 4th month after Nov. 2005); decision line from
  _write_bem (wraps B6.PB5B._write_part5, lists GBEM_USED).
- Block '# part zzzy' (scoped to the act): VIGENCIA_FIXED lei-13161-2015 31.8.2015 (art. 8 I revokes arts. 52-54 'a partir de
  1º de maio de 2015': retroactive -> publication, said in the text), mp-1034-2021 1.7.2021 (art. 5 II), mp-1300-2025 21.5.2025
  (art. 9 I b revokes art. 121; MP converted into Lei 15.235/2025, whose art. 5 also revokes it), mp-472-2009 16.12.2009 (in
  force; effect 1.1.2010 under art. 60 I b: effects_fix MOVE still TO DO), mp-836-2018 1.9.2018 (art. 2); NOTE_FIX 'Lei nº
  13.241, de 1941' -> 2015 (link L13241.htm#art12); CONVERTED_FIX mp-690-2015 -> lei-13241-2015 ('13;241'); MP_LAPSE
  mp-836-2018 11.10.2018 (Ato CN 61/2018: ended 10.10.2018), mp-1318-2025 26.2.2026 (Ato CN 11/2026, DOU 27.2.2026: ended
  25.2.2026), mp-1227-2024 4.6.2024 (Ato CN 36/2024: art. 6 III, revocation of art. 57-A §§ 1º-2º, never took effect; 12.865
  precedent).
- Pins (archive.org, shared client): `BATCH17_ACTS=lei-do-bem iaonly.py laws` (67 linked, 21 new), `missing` (BATCH17_PART=zzzy
  BATCH17_ACTS=lei-do-bem) 0; gap: ato:adc-61-2018-mpv836, ato:adc-11-2026-mpv1318. Bad pin law:lei-13241-1941 (misprinted
  note year; same page as law:lei-13241-2015) removed from sources_batch17.json and added to bad_pins.json.
- Trial t3 (b38/zzzy-t3.json, logs/zzzy-t3.log): 0 problems, 59 versions 2005-11-22 .. 2026-09-15, 11 units differ from the
  consolidated page; spans b38/zzzy-spans2.json (view: python b37/tools/sp.py <json> <units>). NO part file in corpus.d.
### Facts read this session (for the hand model)
- MP 1.318/2025 (DOU 18.9.2025): REDATA (ementa, Capítulo I name, arts. 1, 2, 11-A..11-J); its art. 5: effects 1.1.2026 for
  its changes to art. 11-C, the rest on publication; lapsed 25.2.2026 (Ato 11/2026). Lei 15.504/2026 (DOU 15.9.2026 extra, in
  force on publication) re-enacts the Redata with its own wording (not a conversion).
- MP 836/2018 (DOU 30.5.2018 extra) art. 1 II revokes arts. 56 to 57-B; in force 1.9.2018; lapsed 10.10.2018 -> REIQ gap
  1.9-11.10.2018 (the trial does NOT show it yet).
- MP 1.034/2021 (DOU 1.3.2021 extra) art. 4 II revokes arts. 56 to 57-B from 1.7.2021; converted into Lei 14.183/2021 (DOU
  15.7.2021), which instead gives art. 56 new rates (IV-VIII) and art. 57 § 1º, and whose art. 9 (as Lei 14.374/2022 worded
  it) revokes arts. 56, 57, 57-A and 57-C 'a partir de 1º de janeiro de 2028' (art. 10 I: art. 9 in force 1.1.2025) -> futuro.
  Read Lei 14.183's original art. 9 and the Lei 14.374 article that rewrote it (an original revocation day before the rewrite
  never took effect: decision line only).
- MP 1.095/2021 (31.12.2021, 27 notes) -> Lei 14.374/2022 (22.6.2022; adds 57-C, 57-D); LC 228/2026 (20.3.2026; art. 56,
  57-C § 5º); Lei 13.161/2015 art. 8 I (arts. 52-54); MP 1.300/2025 -> Lei 15.235/2025 (art. 121).
### TO DO, per item (in this order; publish only when every item is closed)
1. REIQ arts. 56, 57, 57-A, 57-B (also 57-C, 57-D): the reader keeps 2-3 overlapping copies of every line 2013-2021 (Planalto
   reprints the text after each lapse: MP 694 2016, MP 836 2018, MP 1.034/Lei 14.183 2021) and credits MP 1.034 / MP 1.095 with
   the old wording. Model by hand (SPAN_FIX with nth): one copy per line; MP 694 (read its arts. 4-5 for the art. 56/57-B day;
   lapsed 9.3.2016, MP_LAPSE exists); MP 836 gap 1.9-11.10.2018 (articles absent, back credited mp-836-2018-fim); MP 1.034
   revocation 1.7.2021, back 15.7.2021 with Lei 14.183's wording (converted-MP rule: the conversion kept the articles); MP 1.095
   (read its art. 2 effects clause, link mpv1095.htm#art2, and what it revoked/rewrote) and Lei 14.374; Lei 14.183 art. 9
   revocation from 1.1.2028 -> futuro (arts. 56, 57, 57-A, 57-C end 2028-01-01 on futuro); MP 1.227 art. 6 III: art. 57-A §§
   1º-2º unbroken (check after the MP_LAPSE; SPAN_FIX as _W1227 in the 12.865 block if needed).
2. LC 214/2025 (43 notes; 'Vigência encerrada (Vide LC 214)' on the ementa and articles): no futuro version is built yet. Read
   LC 214 art. 542/544 (+ LC 227/2026's wording of art. 544) for the Lei 11.196 items and their days; add a _FUT2027 entry (or
   another day) for lei-do-bem; spans after.
3. MP 1.318 REDATA: check every line 18.9.2025-26.2.2026 ('Vigência encerrada' markers must not be text); art. 11-C effect day
   1.1.2026 (the MP lapsed 25.2.2026, after that day, so it took effect: effects_fix MOVE); the ementa / Capítulo I name lines;
   preambulo has a doubled 'Institui o Regime Especial...' line 2005-11-22..2025-05-21 (dupl.py); art. 11-B § 2º doubled on
   2026-09-15 (Lei 15.504).
4. art. 96 § 5º: '... § 4º do art. 5º da Lei nº 9.639, de 25 de maio de 1998, com a' + note '(redação dada pela Medida
   Provisória nº 2.187-13, de 24 de agosto de 2001.)' -> words of the text (BARE_TEXT needs an MP form of _BARE_RX; today it
   credits mp-2187-2001 on 2005-11-22, a same_day version). art. 96 § 3º: two struck copies (MP 457 revocation 11.2.2009; Lei
   11.960, its conversion, 30.6.2009) overlap 2005-2009 -> one line to 11.2.2009.
5. effects_fix.py MOVES "99-batch17zzzy.json": MP 472 art. 17 -> 1.1.2010; MP 1.318 art. 11-C -> 1.1.2026; then every staged
   clause the notes link ('Produção de efeito(s)': Lei 11.727 art. 41, MP 447 art. 8, MP 460 art. 7, Lei 12.024 art. 31, Lei
   12.249 art. 139, Lei 12.715 art. 78, MP 690 art. 10 I, Lei 13.137 art. 26 V, MP 694 arts. 4 II/5 II, Lei 14.183 art. 10,
   MP 1.107 art. 18, Lei 14.438 art. 19, MP 1.110 art. 7 (lapsed, batch15 MP_LAPSE), Lei 11.933 art. 11, Lei 12.995 art. 27 I,
   MP 1.303 art. 75 (lapsed 9.10.2025: a change whose day came later never took effect, decision line only)). Read each
   clause (vigforms.py first).
6. art. 132 items not gated: mixed articles 33, 42, 43, 44, 46 (parts under II/III/IV/V a-b: decide per quoted line, SPAN_FIX
   start); art. 110 (VII: from an act, minimum 1.3.2006 / 1.1.2006) and arts. 114-115 (VI: from a joint act) -> OPEN_ITEMS unless
   the act's date can be read.
7. dupl.py (b37/tools) on the trial: art-113/118/120/33/43/44/46 doubled labels and dotted lines are quoted amendments (check
   each against the page, then EXPLAINED or nothing); the 11 'units differ' (art-09, 41, 44, 48, 56, 63, 65, 70, 83, 113,
   118): EXPLAINED or fix.
8. MP fates to confirm on their pages (conv_report after the hand model): MPs 413, 428, 447, 451/2008; 457, 460/2009; 492, 497,
   517/2010; 534, 540, 545/2011; 563, 564/2012; 613/2013; 656/2014; 1.107, 1.110/2022; ADIN 4254 (6 notes: read the ruling's
   scope before modelling).
9. Then OPEN_ITEMS[_LBEM], pipe.sh zzzy (two identical parses; every check), dupsame/uniqlaws 0, merged check 0/0 main + futuro,
   --compare identical, audit clean, README row + jurisdiction.json (docs.py), PUBLISH lines.
- PIDs (all mine, all exited): robots 42444, laws 43308, missing 54024, t1 47628, multi1 47656, hrefs1 (logs/hrefs1.log),
  gap 26212 / 46204, multi2 (logs/multi2.log), t2 51068, sp1 38616, t3 32116, dupl (logs/zzzy-dupl3.log), sp2
  (logs/zzzy-sp2.log), href1941 (logs/href1941.log). One background `until` wait and one Monitor, both mine, ended (the
  Monitor stopped by its own task id).

## State at handoff (batch 17, thirty-eighth session, 2026-11-02)
Nothing installed this session; installed state unchanged from the thirty-seventh handoff (293 acts, 3913 versions, 2736 commits,
check 0/0, compare identical, audit clean; README + jurisdiction.json current). corpus.d unchanged (no 99-batch17zzzy.json).
Files changed: parse_batch17.py (additions only: act, PARTS zzzy, ACT_DAY/ACT_LAWS lei-11196-2005, block '# part zzzy'),
sources_batch17.json (+22 pins), law_records.json (+ lei-11196-2005), bad_pins.json (+ law:lei-13241-1941). batch17/.tmp/stage.json
rewritten by the trial runs (as every run). Nothing running.
NEXT: Lei 11.196 (part zzzy), TO DO items 1-9 above, then the historic codes.
OPEN / DATED RE-CHECKS: unchanged from the thirty-fourth handoff.

## Thirty-ninth session (2026-11-02): Lei 11.196/2005 (Lei do Bem), part 99-batch17zzzy - items 1-4 DONE, 5 PARTLY, NOT PUBLISHED
Claim: scripts/world-law/claims/brazil-law.txt taken at the start (released at the end). Scratch: .gitlaw-scratch/brazil-b39
(before/ = parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json, dupsame_allow.json, effects_fix.py, README,
jurisdiction.json at session start; parse_batch17.after.py / effects_fix.after.py = state at handoff; logs/; tools/ = b38's +
rows.py (span rows with notes), spansj.py (batch17/.tmp/spansj.py + 'gaps'), st2.py (line heads of units on days), bylaw.py (days
and units each law is credited with in a part), ctxhref.py (page anchors with the text before them), artof.py (the article of an
amending law that names Lei 11.196)). No fetch at all this session (every text read was already cached), so no robots.txt read.
Diff of parse_batch17.py against b39/before/ is additions only (block '# part zzzy' grown); effects_fix.py additions only (MOVES
"99-batch17zzzy.json"). No other file changed. NO part file in corpus.d. Last trial: b39/zzzy-t6.json (0 problems, 62 versions
2005-11-22 .. 2027-01-01, sha e6b47527...); effects_fix test on a copy: b39/eff/99-batch17zzzy.json (5 moves, logs/zzzy-eff1.log).
### Done
1. REIQ hand model (_RQ_TABLE + _reiq_model, run from a wrapper of B8.apply_span_fix after the other hand spans): one copy of each
   wording, gaps MP 694 (1.1-9.3.2016: art. 56 II replaced, III/IV and 57-B out), MP 836 (1.9-11.10.2018: 56-57-B out), MP 1.034
   (1.7-15.7.2021, back with Lei 14.183's wording: 56 IV new, V-VIII, 57 § 1º new), MP 1.095 (art. 2 effects 1.4.2022: 56-58 out
   to 22.6.2022, Lei 14.374, its conversion; 57-B ends 1.4.2022 for good; 56 VI new wording 22.6.2022); Lei 14.374's promulgated
   vetoed parts (DOU 22.12.2022): 56 IX and 57-D from 22.12.2022. Facts read on the acts' pages: Lei 14.183 art. 9 as enacted
   revoked 56, 57, 57-A, 57-B from 1.1.2025 (art. 10 I) and was rewritten by the promulgated parts of Lei 14.374 (22.12.2022) to
   56, 57, 57-A, 57-C from 1.1.2028; that is moot on futuro: LC 214 art. 542 XXXIV h) revokes arts. 55-59 (read as taking in
   57-A..57-D; LC 228/2026 sets REIQ rates only to 12.2026) from 1.1.2027. MP 613's art. 57 'Parágrafo único' replaced the 2007
   §§ 1º-2º (end 8.5.2013); the enacted art. 57 p.u. (renumbered § 1º by Lei 11.488 art. 36, same words) added as a line
   2005-11-22..2007-06-15; MP 1.227's revocation of 57-A §§ 1º-2º never effective (unbroken). Line order fixed (art. 57 caput
   first; MP 694's 56 II after the 2013 II). Art. 57-D § 2º: both pages cut it at 'créditos adicionais previstos' -> TEXT_FIX
   (l11196 only) with the rest of the sentence from Lei 14.374's promulgation text; the consolidated page keeps the cut
   (EXPLAINED still to write). Decision text _RQ_DECISION (written by _write_bem with the copies set aside).
2. LC 214 futuro: _FUT2027[lei-do-bem] (art. 542 XXXIV ends; art. 515 new capita of arts. 11 and 110, art. 11 § 1º, new I/II;
   all 1.1.2027 under art. 544 III as LC 227 worded it). Planalto's page of Lei 11.196 prints none of LC 214's wordings.
3. Redata: ementa and art. 1 p.u. restored copies start 26.2.2026 (SPAN_FIX, mp-1318-2025-fim); Capítulo I name and 'CAPÍTULO I'
   (headings, _redata_model): 2005 lines with a gap 18.9.2025-26.2.2026, end 15.9.2026; Lei 15.504's name from 15.9.2026 plus a
   TEXT_FIX of its stray closing quote (l11196 only); MP 1.318's art. 11-C from 1.1.2026 (MP art. 5 I; it lapsed after that
   day); art. 11-B § 5º (Lei 15.504) split by Planalto into '... inciso II do' + '§ 2º deste artigo ...' -> joined (paragraphs
   wrapper, l11196 only). 'Vigência encerrada' markers are notes, not text (checked in the spans).
4. art. 96: § 5º 'com a redação dada pela Medida Provisória nº 2.187-13 [...]' read as text (both pages; the same-day version is
   gone); § 3º second struck copy set aside (ends 11.2.2009, MP 457); § 2º 2005 wording back from 30.6.2009 (Lei 11.960 did not
   keep MP 457's wording). Same bare-text fix for art. 65 § 1º II and V ('com a redação dada pela Lei nº 10.865 [...];', which
   had credited lei-10865-2004 on 1.3.2006).
5 (part). effects_fix MOVES "99-batch17zzzy.json": MP 472 art-30 -> 1.1.2010; MP 694 (arts. 19, 19-A, 26) -> 1.1.2016; Lei 11.727
   art-64 -> 1.10.2008 (art. 41 IV, its art. 9).
### TO DO, in this order (publish only when every item is closed)
5. rest of the effect days (texts already read: b39/logs/multi8.log, artof1.log, prod1.log, prod2.log):
   a) art. 65: Lei 11.727 art. 39 (VI, VIII, § 4º + I-III) takes effect 1.1.2009 (art. 41 VII), but MP 451 (DOU 16.12.2008; its art.
      12 adds 65 §§ 7º-8º and 64 § 6º) is dated before that, so effects_fix would refuse it: model by hand (SPAN_FIX starts/ends)
      after reading MP 451's vigência in full (law:mp-451-2008; multi needle 'entra em vigor', 1500 chars) and Lei 11.945 art. 33
      (I f: art. 20's 64 § 6º and 65 § 8º from 1.1.2009; III: 65 § 7º 'a partir da data de início de produção ...' - read the rest).
   b) art. 64, MP 413/2008 (DOU 3.1.2008): read its vigência (not in the old list; its change may be staged like Lei 11.727 art. 41 II).
   c) art. 70: MP 447 (read 'Art. 8 o': needle 'Art\. 8 o|entra em vigor'); Lei 11.933 art. 5 (art. 11 I: from 1.10.2008, before its
      publication 29.4.2009 -> keeps the publication day, decision line); MP 1.107 art. 12 / Lei 14.438 art. 12 (art. 19 I b 2: for
      fatos geradores from the start of collection through FGTS Digital, an executive day: coordinator rule = hold until that day
      if the act can be found and dated (find the MTE act fixing the start of FGTS Digital collection and its DOU; pin it), else a
      no-day hold with a decision line); MP 1.110 art. 4 (art. 7 I same condition; lapsed before it -> never took effect, MOVE
      None); MP 1.303 (art. 70 change, art. 75 I: from 1.1.2026; lapsed 9.10.2025 -> never took effect; check whether a line is printed).
   d) art. 62: MP 460 (read 'Art. 7 o'); Lei 12.024 art. 5 (art. 31 I: 1.7.2009, before its publication 28.8.2009 -> keeps
      the publication day).
   e) art. 65, Lei 13.137 art. 22 (art. 26 V: in force on publication, effects 1.5.2015, before the publication -> keeps 22.6.2015).
   f) art. 60: Lei 12.995 art. 27 I b) revokes it 'a partir da entrada em vigor do art. 13': read Lei 12.995's vigência for art. 13.
   g) arts. 28-30 (Inclusão Digital): MP 690 (DOU 31.8.2015; revocation of arts. 28-30 with effects from 1.12.2015, art. 10 I) is
      not in the trial at all; Lei 13.241 (conversion, DOU 31.12.2015) art. 9 rewrote art. 28 and added 28-A, its art. 12 revokes:
      model the MP's days, then the conversion rule. Lei 12.715 art. 62 (art. 28 changes) takes effect 'a partir de sua
      regulamentação' (art. 78 II): hold rule as in c); Lei 12.715 art. 61 (arts. 2, 13) on publication.
   h) art. 30 II: confirm on the effects_fix output that MP 472's line moved and Lei 12.249's same-words line adds no version.
6. art. 132 items not gated: mixed articles 33, 42, 43, 44, 46 (parts under II/III/IV/V a-b, decide per quoted line, SPAN_FIX start);
   art. 110 (VII: from an act, minimum 1.3.2006 / 1.1.2006) and arts. 114-115 (VI: from a joint act): coordinator rule (hold until
   the act's in-force day if it can be found and dated; else a no-day hold with a decision line).
7. dupl.py (b37/tools) on the trial; the 14 'units differ' of t6 (art-09, 11-b [§ 5º joined], 41, 44, 48, 56 [consolidated keeps
   Lei 12.859's IV beside Lei 14.183's], 57-d [§ 2º cut on the consolidated page], 63, 65, 70, 83, 113, 118, titulos [stray quote
   on the consolidated page]): EXPLAINED or fix. art-09's 'only in consolidated' lines are LC 214's art. 11 § 1º I-II (future wording).
8. MP fates on their pages (conv_report after the hand model): MPs 413, 428, 447, 451/2008; 457, 460/2009; 492, 497, 517/2010; 534,
   540, 545/2011; 563, 564/2012; 613/2013; 656/2014; 1.107, 1.110/2022; ADIN 4254 (6 notes; on art. 65 § 1º III-IV: read its scope).
   Also art. 11-J p.u. (Lei 15.504: benefits of art. 11-C I-III 'produzirão efeitos até 31 de dezembro de 2026'): proposed as an
   OPEN_ITEMS line (a limit on effects, not on words).
9. OPEN_ITEMS[_LBEM], pipe.sh zzzy (two identical parses; every check), dupsame/uniqlaws 0, merged check 0/0 main + futuro,
   --compare identical, audit clean, README row + jurisdiction.json (docs.py), PUBLISH lines.
- PIDs (all mine, all foreground through batch17/.tmp/run.py, all exited): multi1 41720, multi2 7836, multi3 29340, multi4 30220,
  multi5 54604, multi6 31172, t1 11196, t2 25140, sp1 37780, t3 23012, multi7 44200, href1 12696, t4 12704, t5 47596, prod1 9260,
  t6 35408, eff1 34988; sp2, prod2, artof1, multi8: run.py's own stdout (with the PID) was discarded by mistake; foreground,
  exited (logs in b39/logs). One plain grep over corpus.d ran outside run.py by mistake, as a background task of this session,
  and was stopped by its own task id after 2 min (no output used). Nothing running.

## State at handoff (batch 17, thirty-ninth session, 2026-11-02)
Nothing installed this session; installed state unchanged (293 acts, 3913 versions, 2736 commits, check 0/0, compare identical,
audit clean; README + jurisdiction.json current). corpus.d unchanged (no 99-batch17zzzy.json). Files changed: parse_batch17.py
(additions only, block '# part zzzy'), effects_fix.py (additions only, MOVES zzzy). batch17/.tmp/stage.json rewritten by the
trials. Nothing running. Claim released.
NEXT: Lei 11.196 (part zzzy), TO DO items 5 (rest) to 9 above, then the historic codes.
OPEN / DATED RE-CHECKS: unchanged from the thirty-fourth handoff.

## Fortieth session (2026-11-02): Lei 11.196/2005 (Lei do Bem), part 99-batch17zzzy - items 5-9 DONE, PUBLISHed
Claim: scripts/world-law/claims/brazil-law.txt taken at the start (released at the end). Scratch: .gitlaw-scratch/brazil-b40
(before/ = parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json, dupsame_allow.json, effects_fix.py, README,
jurisdiction.json at session start; parse_batch17.after.py / effects_fix.after.py = state at handoff; logs/; tools/ = b39's +
a70.py (a unit's text in the innermost build's output and its paras' fields after it)). robots.txt read at start: archive.org
(Disallow /control/ /report/), web.archive.org 404 (b40/robots). archive.org only, through the shared client; no Common Crawl,
no Arquivo.pt, no LexML, no challenge page. Coordinator readings confirmed: LC 214's 'arts. 55 a 59' takes in 57-A..57-D; art.
11-J p.u. (benefit end 31.12.2026) is an OPEN_ITEMS line, not a text change.
### Pins (sources_batch17.json, additions only)
law:mp-425-2008 (MP 425 of 30.4.2008, DOU extra: put MP 413 art. 18's 1.5.2008 off to an SRFB act), ato:adc-4-2008-mpv425 (rejected
9.7.2008, after Lei 11.727), law:dec-5602-2005 (regulation of arts. 28-30; shows Decreto 7.981 added VII/VIII), law:dec-7981-2013
(8.4.2013, DOU 9.4.2013, in force on publication, 'tendo em vista o disposto no art. 62 da Lei nº 12.715'), ato:portaria-mte-240-2024
(in.gov.br capture; DOU 1.3.2024, in force 1.3.2024; art. 3 leaves the 'operação efetiva' day to an SIT Edital). CDX probes: in.gov.br
'edital-sit' and 'edital-n-1-de-29-de-fevereiro-de-2024' 0 captures (Edital not found); Receita 'in575' found IN SRF 575/2005, pinned,
read (it rests on Lei 11.051, not art. 110) and the pin removed again (net: not in sources).
### Done (parse_batch17.py block '# part zzzy' grown; removals = only _FUT2027's art. 110 entries; effects_fix.py additions only)
5. Effect days: _effects_model (run from the span-fix wrapper): art. 65 Lei 11.727 art. 39 lines from 1.1.2009 (old wordings end then);
   art. 64 MP 413 lines set aside (never in effect: MP 425 + Lei 11.727 art. 41 p.u.), 2005 lines end 24.6.2008 so effects_fix's Lei
   11.727 move gives 1.10.2008; arts. 28-30 MP 690 (the struck copy before the reprinted caput set aside; gap 1.12-31.12.2015, back
   with Lei 13.241; 30 II ends 1.12.2015); art. 70 I d) hold (below). effects_fix MOVES + MP 460 art-62 -> 1.7.2009, Lei 12.715 art-28
   -> 9.4.2013 (Decreto 7.981). Decision lines _W_KEPT (MP 447/Lei 11.933, Lei 12.024, MP 451/Lei 11.945 [art. 65's effects start
   read as art. 132 V c, 1.3.2006], Lei 13.137, Lei 12.249: publication kept) and _W_OTHER (Lei 12.995 art. 27 I: art. 13 in force on
   publication per art. 26, so art. 60 ends 20.6.2014; MP 1.303 never in effect, only a struck 'Vide' at the page top). Item 5h:
   no 2010-06-14 version.
6. art. 132 partial articles (_BEM_PART): art. 33 quoted art. 2 from 1.1.2006; art. 42 from 1.12.2005, its § 3º I and § 7º II from
   1.3.2006; art. 43 quoted art. 3 and art. 10 XXVII 1.12.2005; art. 44 quoted art. 15 1.12.2005; art. 46 quoted art. 10 1.3.2006
   (start_law lei-11196-2005). Arts. 110, 114, 115 held with no day (_BEM_HELD; no act found) and left out, with LC 214's art. 110
   changes on futuro (_FUT2027 entries removed).
   HOLDS = coordinator rule read literally ('no-day hold' = the change does not enter the history). TO CONFIRM with the coordinator:
   art. 70 I d) (Lei 14.438; LC 150's d) stands) and arts. 110/114/115 (whole original articles). To undo: empty _BEM_HELD / drop the
   art-70 d) branch of _effects_model and put art. 110 back into _FUT2027 (b40/before/parse_batch17.py has the entries).
   If the SIT Edital starting FGTS Digital is found (in.gov.br), hold to its day instead.
7. dupl.py: every repeated label is a quoted amendment of several articles (arts. 33, 43, 44, 46, 113, 118, 120). Found and fixed:
   stale_fix rule B paired art. 70 p.u. II a)/b) with caput II's struck a)/b) (both parents 'II -') and set them aside since the
   first trials: _sf_bem wrapper restores them (decision _W70_PU). B.EXPLAINED[_LBEM] for the 17 differing units.
8. MP fates on their pages (hrefsm): all converted as the parser has them (413->11.727, 428->11.774, 447->11.933, 451->11.945,
   457->11.960, 460->12.024, 497->12.350, 517->12.431, 534->12.507, 540->12.546, 545->12.599, 563->12.715, 564->12.712, 613->12.859,
   656->13.097, 1.107->14.438, 690->13.241, 472->12.249); MP 492 'Sem eficácia' (only a Vide on art. 96); MP 1.110 lapsed (adc-65).
   conv_report: nothing. ADIN 4254: six 'Vide' links to the petition, nothing struck: lines stand, scope in OPEN_ITEMS.
9. OPEN_ITEMS[_LBEM]; Lei 11.487's footer 'DOU de 15.5.2007' (signed 15.6.2007) read as 15.6.2007 (page_info wrapper _pi_l11487;
   PUBGAP gone); dupsame_allow.json + 4 elision lines ('....." (NR)' in arts. 43, 44, 113, 118). pipe.sh zzzy x3 (final
   b40/logs/zzzy-pipe3.out): 2f529a2f x2, 0 problems, 7 moves, checks as in the PUBLISH line; installed corpus.d/99-batch17zzzy.json
   (b99f0176) + .PUBLISH; docs.py rows-zzzy.json (README row, jurisdiction 294 acts 3974 versions); final merged build
   (b40/logs/final-build.log): 294 acts, 3974 versions, 2764 commits, 0/0, identical, audit clean main + futuro.
- PIDs (all mine, all foreground through run.py unless said; all exited): t7 47992, bylaw1 3572, sp1 36640, multi1 16980, multi2 24356,
  href1 8368, artof1 8724, multi3 45612, multi4 48228, multi5 30028, multi6 47536, multi7 1368, robots 6540, gap1 34560, gap2 55040,
  multi8 42732, href2 43748, href3 2624, gap3 26256, gap4 4864, multi9 25792, cdx1 44764, pin5 33292, multi10 46328, multi11 32200,
  multi12 38236, cdx2 4588, cdx3 47168, pin6 18676, multi13 50048, t8 49296, eff1 12056, dupl1 25248, sp2 33756, a70 45576, a70b
  45328, multi14 40228, multi15 35140, t9 50460, conv1 33616, fates 9092, multi16 51892, multi17 32268, href4 (rc only), multi18,
  multi19, multi20, bylaw2, docs 6332, final build 52500; pipe1 (background task, mine) 1436 53296 25752 25204 32200 48096 37684;
  pipe2 (background) 6340 36128 5984 50660 53836 22980 34956; pipe3 5320 13212 14328 52048 40316 54876 21732. Two background
  `until` waits, mine, ended by themselves. The unpinning of IN 575 was a one-off inline Python edit of sources_batch17.json.

## State at handoff (batch 17, fortieth session, 2026-11-02)
Installed with .PUBLISH this session: zzzy (Lei 11.196/2005; 61 versions). Merged scratch build: 294 acts, 3974 versions, 2764
commits, check 0/0, --compare identical, audit_push clean on main and futuro; uniqlaws 0; dupsame 0. README row + jurisdiction.json
current. corpus.d: new 99-batch17zzzy.json + .PUBLISH; folder PUBLISH unchanged. Other files changed: parse_batch17.py, effects_fix.py,
sources_batch17.json (+5 pins), dupsame_allow.json (+4). Nothing running. Claim released.
NEXT: coordinator to confirm the no-day holds (art. 70 I d; arts. 110, 114, 115); then the historic codes (Código Comercial Lei
556/1850, CPC 1973 Lei 5.869/1973, Código Civil 1916 Lei 3.071/1916; check each against installed parts first).
OPEN / DATED RE-CHECKS: unchanged from the thirty-fourth handoff, plus: the SIT Edital dating FGTS Digital's 'operação efetiva'.

## Forty-first session (2026-11-02): zzzy re-PUBLISHed on the coordinator's effects rule; Código Comercial surveyed and pinned
Claim: scripts/world-law/claims/brazil-law.txt taken at the start (released at the end). Scratch: .gitlaw-scratch/brazil-b41
(before/ = parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json, dupsame_allow.json, effects_fix.py, README,
jurisdiction.json at session start; parse_batch17.after.py / effects_fix.after.py = state at handoff; logs/; tools/ = b40's +
unitdays.py (unit-level day diff of two part files: text T / credit C per day; replays 'changes'), acts.py (installed acts by
regex), cached.py (pin keys cached?), survey.py (note kinds and laws named on a page), struck.py (struck runs and headings),
hrefs.py (hrefs on a page by regex); multi.py patched to read keys outside PAGES). robots.txt read at start: archive.org (Disallow
/control/ /report/), web.archive.org 404 (b41/robots). archive.org only (pinat.py / cdxlist.py, shared client); no Common Crawl,
no Arquivo.pt, no challenge page.
### Coordinator decision applied: zzzy (Lei 11.196) re-PUBLISHed
- Rule: effects tied to a later undated act -> the text keeps its in-force day (decision line naming the act); only a clause
  deferring the provision's own vigência gets a hold. Wording read: Lei 11.196 art. 132 'Esta Lei entra em vigor na data de sua
  publicação, produzindo efeitos: [...] VI [...] VII'; MP 1.107 art. 18, MP 1.110 art. 7 (its vigência article), Lei 14.438 art.
  19 'entra em vigor na data de sua publicação e produz/produzirá efeitos' -> all effects-only: no holds.
- parse_batch17.py (block '# part zzzy'): _BEM_HELD and the art-70 d)/held branches of _effects_model removed; _W_70 and _W_HELD
  rewritten as decision lines (always recorded); EXPLAINED art-70/110/114/115 removed; OPEN_ITEMS sentence rewritten; _FUT2027
  [_LBEM] art. 110 entries (LC 214 art. 515 caput, art. 542 XXXIV k § 4º) and text restored as in b40/before.
- unitdays.py installed (b99f0176) vs new: only art-70, 110, 114, 115 change; one new day 18.3.2022. Found: the published part
  had dropped art. 70 I d) entirely from 2.6.2015 (LC 150's wording, which the hold meant to keep); now LC 150's d) from 2.6.2015,
  MP 1.107's from 18.3.2022; MP 1.110 and Lei 14.438 print the same words (no version).
- pipe.sh zzzy (b41/logs/zzzy-pipe1.out): sha 4367bf12 x2, 0 problems, 13 units differ (all EXPLAINED), 7 moves, checks as in
  the PUBLISH line (latecaput 52 incl. 13 art. 110 lines under LC 214's new caput on futuro, law text: only the caput replaced;
  note pipe.sh shows only `tail -30` of latecaput). Installed corpus.d/99-batch17zzzy.json 00e3dbd0; PUBLISH line appended;
  README row (62) + jurisdiction.json (3975 versions; docs.py's 5th field must be the build entry's own text, e.g.
  'Lei 11.196/2005 2005-2027 (62)', else it appends a new entry: first run did that, jurisdiction.json restored from before/ and
  redone). Final merged build of the installed folder (b41/logs/final-build.log): 294 acts, 3975 versions, 2764 commits, check
  0/0, --compare identical, audit_push clean main + futuro.
### Historic codes: none installed (acts.py over corpus.json + corpus.d). Código Comercial (Lei 556/1850) surveyed, NOT started in code
- Pins (sources_batch17.json, additions only): lim556 (leis/lim/lim556.htm, ts 20261023235140), lim556-compilado
  (lim556compilado.htm, 20261005014152), law:lei-7542-1986 (leis/l7542.htm, 20261009152716), law:dec-2044-1908
  (decreto/1900-1909/D2044.htm, 20080914202730; captures after 2008 are stubs <3.2 KB).
- What the source supports: the 1850 text; no 'Redação dada' notes at all (150 'Vide' pointers only, mostly DL 7.661/1945 on
  the Parte Terceira, DL 305/1967 on arts. 11-19, DL 1.608/1939 and Lei 5.869 on the Título Único). Dated changes: (1) in force
  1.1.1851 (art. 912: 'só principiará a obrigar e ter execução seis meses depois da data da sua publicação na Corte'; published
  in the Secretaria d'Estado 1.7.1850); (2) Título XVI, arts. 354-427, revoked by Decreto (do Poder Legislativo) 2.044 of
  31.12.1908 art. 57 (no vigência clause: work out the 1908 default rule and its publication day; CLB 1908 vol. 1 p. 216);
  (3) arts. 731-739 revoked by Lei 7.542/1986 art. 38 (in force on publication, art. 37; DOU 29.9.1986); (4) Parte Primeira
  (arts. 1-456) revoked by Lei 10.406/2002 art. 2.045 from 11.1.2003. Notes for (2)-(4) are bare struck text ('Revogado pelo
  Decreto do Poder Legislativo nº 2.044, de 1908:', 'Revogado pela Lei nº 7.542, de 26.9.1986', heading 'Parte revogada pela Lei
  10.406, de 10.1.2002'), not parenthesised: check the parser reads them. Consolidated page: 'Arts. 1º ao 456, revogados pela Lei
  nº 10.406, de 2002', 'Arts. 731 a 739, revogados pela Lei nº 7.542', Parte Terceira (arts. 797-913) and the Título Único printed.
- Parser issues to expect: the Título Único (administração da justiça) restarts at Art. 1º-30 -> unit keys clash with Parte
  Primeira arts. 1-30 (needs its own unit prefix); incisos numbered '1 -', '2 -' (act digits param); the Parte Terceira's real
  replacement by later falência laws is not noted on the page (keep it as printed, decision + README line).
- CPC 1973 (Lei 5.869): leis/l5869.htm has 1,266 captures (latest ~243 KB, 2026-10); l5869compilada.htm captures are stubs.
  CC 1916 (Lei 3.071): law:lei-3071-1916 already cached (1.39 MB, ts 20261022053934).
- PIDs (all mine, foreground through run.py unless said; all exited): t1 35812, m1 24972, m2 19136, m3 49200, eff1 37536, ud1
  24060 + 21956, m4 40328 + 10436, acts1 50812, cached1 53700, robots 18608, cdx1 18688 (moved to background by the tool
  timeout, mine, finished), docs 14016, docs2 53184, final build 38068, pin1 13116, survey1 20836, struck1 47764, pin2 5768,
  m5 46016 + 5472, m6 42504, cached2 51700, cdx2 36764, href1 27908, cdx3 53040, cdx4 26028, pin3 26856, pin4 27268, m7 10884,
  m8 9388; pipe1 (background task, mine): 43268 12660 12180 17572 44768 54512 42692 (the 8 file checks' run.py PIDs went to
  /dev/null in pipe.sh). One stray `find /` (no run.py) became a background task of this session and was stopped by its own
  task id (no output used). Nothing running.

## State at handoff (batch 17, forty-first session, 2026-11-02)
Installed this session: zzzy re-PUBLISH (00e3dbd0, 62 versions). Merged build of the installed folder: 294 acts, 3975 versions,
2764 commits, check 0/0, --compare identical, audit_push clean main + futuro; uniqlaws 0; dupsame 0. README row + jurisdiction.json
current. Files changed: parse_batch17.py (zzzy block only; diff vs b41/before = the edits above), sources_batch17.json (+4 pins),
corpus.d/99-batch17zzzy.json + .PUBLISH (line appended), repo/README.md, repo/jurisdiction.json, PROGRESS.md checkpoint.
effects_fix.py unchanged. Nothing running. Claim released.
NEXT: Código Comercial as part zzzz (one act): PAGES lim556/lim556-compilado, _act (digits for '1 -' items), ACT_DAY_ALL
lei-556-1850 1851-01-01 (art. 912), law records lei-556-1850 / dec-2044-1908 / lei-7542-1986 (lei-10406-2002 exists), the
Título Único unit prefix, the 1908 day; then CPC 1973, then Código Civil 1916.
OPEN / DATED RE-CHECKS: unchanged from the thirty-fourth handoff, plus: the SIT Edital dating FGTS Digital's 'operação efetiva'
(now only an effects date; no text change hangs on it).

## Forty-second session (2026-11-02): Código Comercial PUBLISHED (part zzzz); CPC 1973 configured as part zzzza (trials only)
Claim: scripts/world-law/claims/brazil-law.txt taken at the start (released at the end). Scratch: .gitlaw-scratch/brazil-b42
(before/ = parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json, dupsame_allow.json, effects_fix.py, README,
jurisdiction.json at session start; parse_batch17.after.py / effects_fix.after.py = state at handoff; logs/; tools/ = b41's +
g.py (grep via run.py), cdxp.py (CDX prefix listing), cdxu.py (CDX between two timestamps), vers.py (versions of a part),
pdump.py + pq.py (dated paras the innermost build gets, and a query over them), rawgrep.py, head.py, survey2.py (note kinds and
laws named on a page), lawsdec.py / dec84.py (a part's laws and decisions), bdiff.py (diff vs before/), docdiff.py, jdiff.py,
install.py, findf.py, pids.py; rows-zzzz.json, publish-zzzz.txt). robots.txt read at start: archive.org (Disallow /control/
/report/), web.archive.org 404 (b42/robots). archive.org only (shared client: pinat.py, cdxlist.py, iaonly.py laws); no
Common Crawl, no Arquivo.pt, no live host, no challenge page met.
### Part zzzz: Código Comercial (Lei 556/1850), PUBLISHED, 4 versions
- Decreto 2.044/1908 day (task rule: the general vigência rule then in force, from an official text): Decreto 572 of 12.7.1890
  art. 1 ('As leis da União e decretos do Governo Federal com força de lei obrigam [...] desde o dia que determinarem; e na falta
  desta determinação: I. No Districto Federal no terceiro dia depois da inserção no Diario Official'), read on the Chamber of
  Deputies' copy of the original publication; its Dados da Norma: revoked only by Decreto 11 of 18.1.1991. Decreto 2.044's
  publication: 'Diário Official - 6/1/1909, Página 116' (Chamber copy, Dados da Norma and the original-publication page, whose
  text has no vigência clause: art. 57 only revokes). Day: 9.1.1909 (third day after 6.1.1909), as dl-25-1937 was dated by the
  LICC 1916's three-day Distrito Federal rule. Decision line _W_CCOM2044.
- Pins (sources_batch17.json, additions only): ato:dec-572-1890 (camara publicacaooriginal, 20190224011717),
  ato:dec-572-1890-norma (20190224003040), ato:dec-2044-1908 (publicacaooriginal, 20190224003045), ato:dec-2044-1908-norma
  (20190922014138); all www2.camara.leg.br legin captures through archive.org.
- parse_batch17.py (additions only): PAGES lim556 / lim556-compilado; _act codigo-comercial (CCom, digits 3); PARTS zzzz;
  ACT_DAY_ALL lei-556-1850 1851-01-01; ACT_LAWS_ALL lei-556-1850 (published 1.7.1850, the Carta de Lei on the page); block
  '# part zzzz' before SRC: B12.DECREES dec-2044-1908 (batch 12's decree keys: Diário Official 6.1.1909), VIGENCIA_FIXED
  dec-2044-1908 1909-01-09 and lei-10406-2002 2003-01-11 (both gated on the act), NOTE_FIX for the two forms of 'Revogado pelo
  Decreto do Poder Legislativo nº 2.044, [de] 1908:'; _paragraphs_ccom (art. 518 split from 517 on lim556; after the 'TÍTULO
  ÚNICO' heading units art-NNN -> art-tu-NNN on both pages; the heading word 'e' between two Vide pointers dropped);
  _unit_label_ccom ('Título Único, Art. Nº'); _ccom_model via the apply_span_fix wrapper (Parte Primeira struck lines end
  11.1.2003 lei-10406-2002, Título XVI 9.1.1909 dec-2044-1908, by page range; the 'Parte' marker heading skipped);
  EXPLAINED art-742 / art-772 / art-730 / preambulo; OPEN_ITEMS. law_records.json: + lei-10406-2002 (the 50-codes record; the
  reader took the page's index line 'ÍNDICE Vigência ...' as its title). batch10/.tmp/firstline.py: unit-key pattern takes
  'art-tu-' (it crashed on the new keys).
- pipe.sh zzzz x2 (b42/logs/zzzz-pipe1.out, zzzz-pipe2.out): 48d07b87 x2, 0 problems, 4 units differ (EXPLAINED), 0 moves, all
  file checks 0, uniqlaws 0 (after law_records), dupsame 0, overlap 0, latecaput 0; merged: 295 acts, 3979 versions, 2768
  commits, 0/0, identical, audit clean. Installed corpus.d/99-batch17zzzz.json (75ad716e) + 99-batch17zzzz.PUBLISH; docs.py
  rows-zzzz.json (README row; jurisdiction 295 acts 3979 versions, build entry 'Lei 556/1850 1851-2003 (4)', no stray entries).
  Final merged build of the installed folder (b42/logs/final-build1.log via the task output): same numbers, clean.
- Note: a reparse of zzzz after this session's later CPC pins differs from the installed file only in sources[0].requests
  (502 -> 508, the pin count; jdiff b42/logs/jd1.log). Not a content change; no re-publish needed.
### Part zzzza: CPC 1973 (Lei 5.869/1973), CONFIGURED, NOT PUBLISHED (trials t1, t2)
- Pins: l5869 (current page, 20261019220418: after the repeal Planalto strikes every line, 4554 of 4647 lines struck, so not
  usable as the act page), l5869-2015 (http://www.planalto.gov.br:80/ccivil_03/leis/L5869.htm, 20151027142729, the last
  capture before the repeal), l5869compilada-2015 (L5869compilada.htm, 20151029045434; captures from 12.4.2016 on are stubs);
  iaonly.py laws l5869: 76 acts named in notes, 60 pinned from archive.org (the rest were cached).
- parse_batch17.py (additions only): PAGES l5869, l5869-2015, l5869compilada-2015; _act codigo-de-processo-civil-de-1973 (CPC73,
  page l5869-2015, consolidated l5869compilada-2015, digits 4 like the CPC 2015 / CC 2002 parts); PARTS zzzza; ACT_DAY_ALL
  lei-5869-1973 1974-01-01 (art. 1.220); ACT_LAWS_ALL lei-5869-1973 (DOU 17.1.1973); block '# part zzzza' before SRC: B9.REPEALS
  (2016-03-18, lei-13105-2015: art. 1.046, in force per art. 1.045 one year after DOU 17.3.2015 = the CPC 2015's first day in
  60-phase2), VIGENCIA_FIXED lei-8950-1994 1995-02-12 and lei-10173-2001 2001-03-11 ('no prazo de sessenta dias após/a partir
  da data de sua publicação', clauses the reader does not parse; pub + 60 days as the reader counts such terms).
- Trial t2 (b42/logs/c2.log, zzzza-t2.json): 4648 paras (3520 plain, 1128 struck), 1268 units, 66 versions; 3 problems;
  end_how: successor 315, note 200, undated 197, parent 179, next-wording-first 147, next-wording 44, run-revoked 44, twin 2.
### TO DO for zzzza, in this order (publish only when every item is closed)
1. The 3 problems: art-0741 parágrafo único and art-0500 II 'restored wording after an open one'; art-1218 XV 'ends before it
   starts' (1986-09-29 < 1980-05-13: Lei 6.780/1980 renumbered the incisos of art. 1.218 and Lei 7.542/1986 revoked XV - read
   which line the note belongs to).
2. Lei 5.925/1973 (DOU 2.10.1973; ~353 notes) changed and renumbered articles before the Code took effect (1.1.1974): check
   how the trial dates its lines (expected: the 5.925 wording from 1.1.1974, the 1973 wording never in force; decision line),
   and read Lei 5.925's own vigência clause on its page.
3. The 197 'undated' struck lines (pdump.py zzzza + pq.py): each must end by a note, a successor, or be explained.
4. The repeal check (decision 'differs from the unstruck text of Planalto's page ... in 17 articles', zzzza-t2 decisions;
   b42/logs/d84.log): art-0018 ('>' stray), art-0039 ('no' for 'nº'), art-0154 (note '(I ncluído pela Lei nº 11.419, de
   2006)' read as text: NOTE/TEXT fix), art-0275 (';'), art-0315 / art-0511 (renumbering notes on the compiled page),
   art-0431, art-1088, art-1092, art-1094 (only in consolidated), art-1082 (only in replay), art-0470 ('Vide Lei nº 13.105, de
   2015)' read as text), art-0475-e, art-0523, art-0649, art-0655-a (punctuation), titulos (CAPÍTULO VI Da liquidação da
   sentença, Subseção III Da adjudicação de imóvel, TÍTULO V Da remição: only in consolidated). Also find out why the
   'Replay check' against l5869compilada says 0 articles (does it compare the empty post-repeal version?).
5. Every amending law's in-force day (77 laws; vigforms, staged clauses; MP 2.180-35/2001 under the MP rules; 'Revigorado'
   notes of Lei 8.950/1994 = restorations); last change before the repeal in t2 is 25.10.2013 (Lei 12.873/2013?): confirm no
   2014-2015 change is missing (Lei 13.105's own 'Vide' pointers are not changes).
6. dupl/dupsame/uniqlaws, OPEN_ITEMS (art. 1.046 § 1º survival rule), EXPLAINED, README row, PUBLISH.
### Then CC 1916 (Lei 3.071/1916; law:lei-3071-1916 cached, ts 20261022053934): check whether that capture strikes every line
  after the 2002 repeal (as CPC 1973's does); if so find a capture before 11.1.2003. Ends with the repeal by Lei 10.406 from
  11.1.2003 (B9.REPEALS; VIGENCIA_FIXED lei-10406-2002 2003-01-11 as in zzzz).
- PIDs (all mine, foreground through run.py unless said; all exited): probe 8468 (a recursive glob, moved to the background by
  the tool timeout and stopped by its own task id; no output used), probe2 26884, setup 22728, g2 25516, g3 7780, robots 45924,
  cdx1 46316, pin1-4 20776 2144 6616 12656 (rc 2, wrong path) then 35260 12272 39012 49676, m2 40220, m3 42120, t1 3448, t2
  4288, t3 38724, cdx2 29684, pin5 21396, install 13852, docs 8468, final build 28524, q2 7436, laws1 51892 (background task),
  c1 50452, cdx3 38228, pin6 15984, cdx4 53016, pin7 55048, c2 43148, recheck 21872, pids 23328, claim release 32792; pipe1 (background, mine)
  10876 27872 29828 38300 44540 39660 22464; pipe2 (background) 34808 40028 42124 46956 27156 54852 14400. g1, m1, m4-m7, pd1,
  pq1-2, rg1-5, v1-2, q1, q3, sv1-2, ld3-4, bd1-3, dd, pubs, ff, d84, jd1, hd: run.py PIDs not kept (their pipes filtered on
  'rc'); foreground or my own background waits, all exited. Outside the wrappers (mistakes, all reads of small files, no
  network): the first ls/head/grep/cat of PROGRESS.md, batch17/.tmp and the claims folder; one `tail` of the cpu log; one `wc`;
  grep/cut/sort/sed/tail/sha256sum/cp and one `python -c` filter over my own scratch logs and files. Background `until` waits
  (shell loops, mine) ended by themselves or were stopped by their own task ids. Nothing running.

## State at handoff (batch 17, forty-second session, 2026-11-02)
Installed with .PUBLISH this session: zzzz (Código Comercial, Lei 556/1850; 4 versions). Merged build of the installed folder: 295
acts, 3979 versions, 2768 commits, check 0/0, --compare identical, audit_push clean main + futuro; uniqlaws 0; dupsame 0. README
row + jurisdiction.json current. Files changed: parse_batch17.py (additions only: zzzz and zzzza config and blocks; diff vs
b42/before = +211 -0), sources_batch17.json (pins above), law_records.json (+ lei-10406-2002), batch10/.tmp/firstline.py (key
pattern), corpus.d/99-batch17zzzz.json + .PUBLISH, repo/README.md, repo/jurisdiction.json, PROGRESS.md checkpoint.
effects_fix.py unchanged. zzzza is configured in PARTS but not published (no corpus.d file). Nothing running. Claim released.
NEXT: CPC 1973 (part zzzza) TO DO items 1-6 above; then CC 1916.
OPEN / DATED RE-CHECKS: unchanged from the forty-first handoff.

## Forty-third session (2026-11-02): CPC 1973 PUBLISHED (part zzzza, 67 versions); CC 1916 surveyed and pinned (not started in code)
Claim: scripts/world-law/claims/brazil-law.txt taken at the start (released at the end). Scratch: .gitlaw-scratch/brazil-b43
(before/ = parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json, dupsame_allow.json, effects_fix.py, README,
jurisdiction.json, PUBLISH, firstline.py, pipe.sh at session start; parse_batch17.after.py / effects_fix.after.py = state at
handoff; logs/; tools/ = b42's (paths -> b43) + uq.py (dump filter: key=value, --units, --ctx), uclass.py (undated lines by the
law of the next line), seq.py (dump in page order between two units), ddiff.py (span-field diff of two dumps), pinfo.py,
utext.py (one unit's text per version, replaying changes), lawdays.py (per law: days used vs publication; flags), lawvig.py
(a law page's vigor/efeitos sentences), lawtail.py, lawphr.py (law page text around a regex), lx.py (LexML cache + records),
lawin.py (installed parts holding a law key), yearnotes.py, strfrac.py (parser's struck/plain count of a page), noteq.py,
addrec.py, fixwhy.py, fmt.py, after.py; rows-zzzza.json, publish-zzzza.txt). robots.txt read before the first request
(b43/robots: archive.org Disallow /control/ /report/; web.archive.org 404). archive.org only, 2 requests (1 CDX, 1 capture)
through the shared client; no Common Crawl, no Arquivo.pt, no live host, no challenge page.
### Part zzzza: CPC 1973 (Lei 5.869/1973), PUBLISHED, 67 versions 1974-01-01 .. 2016-03-18
- parse_batch17.py: block '# part zzzza' grown (additions only, +278 -0 vs b43/before; effects_fix.py unchanged). All gated on
  the act being in ACTS. Items, in the to-do order:
  1. The 3 problems: art-0500 II (Lei 5.925's wording printed struck below Lei 8.038's: SPAN_FIX 1974..1990); art-0741 par.
     único (note '(Redação pela Lei nº 11.232, de 2005)': NOTE_FIX; MP 2.180-35's wording now 27.8.2001..24.6.2006);
     art-1218 XV (SPAN_FIX: 1973 XIV and XV end 13.5.1980 renumbered by Lei 6.780; LABEL_FIX 'X -Xl -' -> 'X -').
  2. Lei 5.925/1973 (art. 5: in force 1.1.1974): coordinator fold rule. _build_act_cpc73 credits the first version's units
     with Lei 5.925 wording to ['lei-5869-1973', 'lei-5925-1973'] + version note; decision _W_CPC73_FOLD. _cpc73_model marks
     the 1973 wording it replaced (struck, no note, start 1.1.1974, no law; the next law-written line of the unit is Lei
     5.925's on 1.1.1974, struck or not) skip/pinned 'never-in-force': 364 lines. This also removed real doubled text in
     the trial (arts. 232, 412, 500, 520, 585, 602, 1.095 printed both wordings from 1974).
  3. Undated struck lines: 0 left (191 were the 5.925 case; others dated by hand: art. 746 + its 1973 Capítulo IV ->
     21.1.2007 Lei 11.382; art. 1.102.a/.b/.c -> UNIT_FIX art-1102-a/b/c (both pages); Capítulo XV headings from Lei 9.079,
     its note line '(Capítulo acrescentado ...)' skipped).
  4. Pre-repeal check 17 -> 9 differences, all consolidated-page artifacts, explained by _W_CPC73_REPEALX (written only when
     the differing units are exactly those 9; else it prints 'CPC73 REPEAL CHECK: differences not as explained'). Fixed:
     art-0154 note '(I&nbsp; ncluído' and art-0470 'Vide ...)' mended in the HTML (also art-0602 I 'Inlcluído'); line ends
     corrected from the amending laws' own texts (_CPC73_ENDS: arts. 275 II, 475-E, 523 § 3º, 649 IV, 655-A § 4º); art-1082
     caput ends 23.11.1996 (Lei 9.307 art. 44). Why the 'Replay check' says 0: B9.consolidated() returns {} for an act in
     B9.REPEALS, so that line compares nothing (same for Lei 8.666's part); the pre-repeal check takes its place.
  5. In-force days: lawdays.py over every law; all own clauses read (vigforms) except the two hand days already set (Leis
     8.950/1994, 10.173/2001); Lei 11.112/2005 (art. 4 vetoed) and Lei 11.382/2006 (no clause) by LINDB 45 days (checked
     on the pages). Publication years misprinted on two law pages, corrected by B8.LAW_FIELD_FIX + VIGENCIA_FIXED from the
     acts' own signing dates: Lei 6.745 ('DOU de 6.12.1976' for a law signed 5.12.1979 -> 1979-12-06), Lei 8.637 ('D.O.U.
     de 1º.4.1990' for 31.3.1993 -> 1993-04-01). MP 2.180-35 stands (EC 32 art. 2). No amending note after Lei 12.873/2013
     (yearnotes: only CPC 2015 'Vide' pointers).
  6. Labels: incisos printed with l for I ('Vl', 'Vll', 'lII', 'Xl', 'l') get the numeral as label (text as printed); art.
     1.218 'Vlll - aos protestos' excluded (as VIII it displaced the struck 1973 VIII, which a later rule then dropped).
     Other hand spans: art-0253 par. único (struck copy skipped), art-0496 I-V of Lei 8.038's list start 29.5.1990,
     art-0508 par. único (unnoted copy skipped), art-0541 1973 caput ends 29.5.1990 (Lei 8.038 art. 44: 'arts. 541 a 546'),
     art-0983 placeholder 'Parágrafo único. (Revogado).' skipped, heading ')' after Título V skipped, LABEL_FIX art. 275 II
     'j) de eleição de cabecel' -> 'f)' (Lei 5.925's text). Decision for art-0644 (the page has no 1973 wording).
     B13.OPEN_ITEMS: art. 1.046 §§ 1º-2º survival; arts. 1.218/1.219.
- law_records.json + 4 (the installed records of lei-8038-1990, lei-9307-1996, lei-9868-1999, lei-11419-2006: URL case and
  title differed); dupsame_allow.json + 1 (titulos 'Das Disposições Comuns às Seções Precedentes', printed twice by the Code).
- pipe.sh zzzza x3 (b43/logs/zzzza-pipe1..3.out): final c717b6be x2, 0 problems, 0 moves; dupline/dupcheck/leakcheck/
  firstline 0, overlap 0, dupsame 0, uniqlaws 0; benign: pubgap 2 (Lei 7.219/1984 DOU 20.11.1984 and Lei 9.040/1995 DOU
  10.12.1995 as printed; not provably wrong, see re-checks), ordercheck 1 (art. 557 § 1º-A before § 1º as printed),
  quotecheck 5 ('visto', 'sem recurso'), missorig 1 (art. 644), latecaput (caput-only rewrites). Merged: 296 acts, 4046
  versions, 2826 commits, check 0/0, 0 trailer errors, --compare identical, audit_push clean main + futuro. Installed
  corpus.d/99-batch17zzzza.json 3013d42b + .PUBLISH; docs.py rows-zzzza.json (README row; jurisdiction 296 acts 4046
  versions, build entry 'Lei 5.869/1973 1974-2016 (67)', one entry).
### CC 1916 (Lei 3.071/1916): surveyed, pinned, NOT started in code (part zzzzb next)
- law:lei-3071-1916 (ts 20261022053934) strikes everything: the parser reads 3901 of 3907 paragraphs struck. It still holds
  the earlier wordings with their notes (1646 strike tags; 'Revogado pela' 129, 'Redação dada' 106, 'Incluído' 38).
- Pinned l3071-2002 (sources_batch17.json, pinat.py): http://www.planalto.gov.br:80/ccivil_03/leis/L3071.htm ts
  20020602033457 (CDX before 20030111: 20010509155642, 20011211140515, 20020602033457). It has NO strike tags: a colour
  legend (black original, blue altered, green revoked, red included) and only the wording in force with 294 'Redação dada'
  notes (205 name laws the reader does not key, e.g. 'Decreto do Poder Legislativo nº 3.725, de 15.1.1919'). So: use it as
  the pre-repeal consolidated check (unstruck text = text in force mid-2002), and build the history from the 2026 page with
  the repeal's page-wide strike removed (find how it is marked: an outer <strike> around the body, or per paragraph; earlier
  wordings may be struck twice or carry their notes). Check the green (revoked) text is not read as in force on the 2002 page.
- Then: PAGES l3071 (2026) / l3071-2002; _act (digits 4); ACT_DAY_ALL lei-3071-1916 1917-01-01 (art. 1.806); B9.REPEALS
  2003-01-11 lei-10406-2002 (VIGENCIA_FIXED as in zzzz); decree keys for 'Decreto do Poder Legislativo' notes (B12.DECREES,
  as dec-2044-1908); pre-1970 dates clamp in commits (In-force trailer keeps the day); the Decreto 572/1890 / LICC 1916
  three-day rule for laws without a day.
- PIDs (all mine, foreground through run.py unless said; all exited): probe 50828 (rc 2), 53012, 43224, setup 14012, r1
  36432, pd1 40880, pq1 21160, uq1 54096, uq2 36632, uc1 48508, 40436, uq3 4388, g2 16564, uq4 29308, sq1-3 25700 47316
  30996, pi1 45760, g3 20844, g4 22232, g5 47380, r2 29664, g6 51244, r3 2804, r4 12368, ld1 45564, lv1 19048, lt1 36032,
  g7 29444, g8 2492, lx1 49628, li1 50600, d84-type reads 47696 1368 13848, lp1 18872 (moved to background by the tool
  timeout while waiting on the cpu gate, mine, finished), bd1 40208, pd2 51288 (rc 1, KeyError) then 29220 26408, t3 49428,
  18416, 14036, dd1 18224, sq4-6 33140 37096 51548, ut1 51792, bd3 43096, t4 46664, 30692, pq3 16540, pq4-5 11764 17880,
  bd4 32772, d2 31880, bd5 51564, t5 33328, pd3 42904, ld2 53164, nq1 2748, sq7 29848, lp4 8460, bd6 8140, pd4 38968, dd2
  54748, sq8-9 17080 33708, pq6 49056, sq10 29956, rg4 23820, bd7 55228, pd5 12596, dd3 8460, t6 16368, ut 24228 17292
  26472 11156, ud1 53340, ut 12852 35544 33452 42592, yn1 11196, bd8 49568, sv1 52828, sf1 43032, robots 34468, cdx1 23768,
  r5 52868, pin1 39244, sf2+sv2 (background task, mine, finished), pd6 53648, 45760 44796 43292 51864 42692, lt2 2712, lp5
  45012, uq6 29764, rg5 31648, uq7 47700, r6 15844, pq7 38288, fmt 53520, addrec 47892, fixwhy 34352, bd9 5016, uqx 52752
  49628 28620, bd10 41428, inst 28676, docs 2040, dd 5948, after 38412, bd11 24648, pids 41712; pipe1 (background, mine)
  41060 29636 39220 22768 27920 51440 30196; pipe2 12848 20636 9752 43064 44476 49096 31236; pipe3 6844 29224 37828 14496
  43096 42004 51488 (pipe.sh's file-check run.py PIDs go to /dev/null). One Monitor (until-loop on the pipe1 log, mine,
  ended by itself). Outside the wrappers (mistakes; small local reads/writes only, no network): the first PowerShell
  Get-ChildItem of brazil-law and batch17 and a New-Item of b43/logs; heads/cats/greps/cut/sed/awk/tr over my own b43 tools
  and logs and the task output files; one grep of parse_batch17.py; one ls of batch17/.tmp and mkdir/cat of b43/robots;
  greps of zzzza-build.log, README.md and jurisdiction.json; ls of corpus.d. Nothing running.

## State at handoff (batch 17, forty-third session, 2026-11-02)
Installed with .PUBLISH this session: zzzza (Código de Processo Civil de 1973, Lei 5.869/1973; 67 versions). Merged build: 296
acts, 4046 versions, 2826 commits, check 0/0, --compare identical, audit_push clean main + futuro; uniqlaws 0; dupsame 0.
README row + jurisdiction.json current. Files changed: parse_batch17.py (zzzza block, +278 -0 vs b43/before),
sources_batch17.json (+1 pin l3071-2002), law_records.json (+4), dupsame_allow.json (+1 line), corpus.d/99-batch17zzzza.json +
.PUBLISH, repo/README.md, repo/jurisdiction.json, PROGRESS.md checkpoint. effects_fix.py unchanged. Nothing running. Claim
released (release PID 39084).
NEXT: CC 1916 as part zzzzb (plan above).
OPEN / DATED RE-CHECKS: unchanged from the forty-first handoff, plus: the DOU days of Lei 7.219/1984 (page: 20.11.1984, signed
19.9.1984) and Lei 9.040/1995 (page: 10.12.1995, signed 9.5.1995), both in force on publication, against their LexML records
(not cached; LexML Crawl-delay 5).

## Forty-fourth session (2026-11-02): zzzza DOU days corrected from LexML (re-PUBLISH); CC 1916 (part zzzzb) configured, trials only
Claim: scripts/world-law/claims/brazil-law.txt taken at the start ('gitlaw-BR-44 alan-dell 2026-11-02T05:23Z'), released at the
end. Scratch: .gitlaw-scratch/brazil-b44 (before/ = parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json,
dupsame_allow.json, effects_fix.py, README.md, jurisdiction.json, PUBLISH, firstline.py, pipe.sh at session start, plus the
installed zzzza part/.PUBLISH as *.installed; pages/ = decoded pages (l3071-2026.html, l3071-2002.html, lindb.html); logs/;
tools/ = b43's (paths -> b44) + setup.py, rawtxt.py, ltexp.py, colors.py, cls3.py (2026 page: css / tag / none class per
paragraph), cmp2002.py (THE CC16 pre-repeal check, see below), logsum.py, lxraw.py, reinstall.py; pids.txt). robots.txt read
before the first request (b44/robots: archive.org Disallow /control/ /report/; web.archive.org 404; www.lexml.gov.br: /urn and
/sru allowed, /busca/ /doc/ /linker/ disallowed, Crawl-delay 5). Requests: archive.org only through the shared client
(iaonly.py laws l3071: 32 acts named, 28 pinned); LexML 2 record pages (/urn/, 6 s apart, no challenge). No Common Crawl, no
Arquivo.pt, no live Planalto.
### zzzza: Lei 7.219/1984 and Lei 9.040/1995 DOU days (re-PUBLISH)
- LexML records (cached .cache/686a65c4... and 2c7b026a...): Lei 7.219 'Publicação Original 1984-09-20 Diário Oficial da União.
  Seção 1. 20/09/1984. p. 13730'; Lei 9.040 'Publicação Original 1995-05-10 Diário Oficial da União. Seção 1. 10/05/1995. p.
  6641'. Planalto's pages end 'publicado no D.O.U. de 20.11.1984' / '10.12.1995' (misprints); both 'entra em vigor na data de
  sua publicação' (art. 2). Corrected in the zzzza block (additions only: B8.LAW_FIELD_FIX + VIGENCIA_FIXED, decision lines);
  only zzzza holds these keys (lawin.py). pipe.sh zzzza x2 (b44/logs/zzzza-pipe1.out, -pipe2.out): parse 0ced74ea x2 in each,
  0 problems, 0 moves, dupline/dupcheck/leakcheck/firstline 0, pubgap 0 (was 2), overlap 0, dupsame 0, uniqlaws 0; benign as
  before: ordercheck 1, quotecheck 5, missorig 1, latecaput; merged 296 acts, 4046 versions, 2826 commits, 0/0, identical,
  audit clean main + futuro; eff 94744386 (versions of 20.9.1984 and 10.5.1995 now; 67 versions as before). RE-PUBLISHED:
  reinstall.py replaced corpus.d/99-batch17zzzza.json (3013d42b -> 94744386; old file + .PUBLISH kept in b44/before/*.installed)
  and rewrote its .PUBLISH (b44/publish-zzzza.txt). README row and jurisdiction.json need no change (row text and counts the
  same). Final merged build of the installed folder (b44/logs/final-build.log): same numbers, clean.
### CC 1916 (Lei 3.071/1916), part zzzzb: CONFIGURED, NOT PUBLISHED (trials t1-t5)
- Config (parse_batch17.py, additions only): PAGES l3071 (2026 page) / l3071-2002; pin l3071 in sources_batch17.json (same url/ts
  as sources_phase2 law:lei-3071-1916, NO "via" key: that cache lives in the old fetch cache, not wayback.py's); _act
  codigo-civil-de-1916 (CC16, digits 4); PARTS zzzzb; ACT_DAY_ALL lei-3071-1916 1917-01-01 (art. 1.806); ACT_LAWS_ALL (DOU
  5.1.1916, the page's footer); block '# part zzzzb' before SRC: VIGENCIA_FIXED lei-10406-2002, B9.REPEALS 2003-01-11, the
  Introdução's own unit keys art-in-NNNN ('Introdução, Art. N'), the 2002 page's green (#008000, revoked) text removed with
  'Texto original:' / 'Inciso suprimido ...' marker lines (_cc16_drop_green, _CC16_2002_MARK), _cc16_model (below).
- FINDING (the handoff's plan does not hold as written): the 2026 page strikes the 1916 ORIGINAL wording with the CSS
  line-through and every LATER wording (with its 'Redação dada'/'Incluído' note) with <strike> tags. Removing the CSS leaves the
  1916 text in force and the later wordings struck (e.g. art. 6: 1916 'II. As mulheres casadas' plain, Lei 4.121/1962's wording
  struck) - trial t3 showed exactly that. cls3.py: 3583 css, 313 tag, 6 none, 5 mixed paragraphs. So the trial reads EVERY line
  as a wording (no CSS removal), dated by its notes and by the next wording of its label; _cc16_model opens the wordings nothing
  ends (end_how 'undated': no note, no later wording) until the repeal (end 2003-01-11 lei-10406-2002, 'act-repealed', pinned)
  and drops them from B3.UNDATED. The 'none' lines are Planalto's annotations, mostly the text of Decreto 3.725/1919 itself
  ('Faça-se ponto na palavra morte ...', 'Diga-se escrivão em vez de notario.', 'Elimine-se o parenthese ...'): to skip.
- The 2002 capture is a modernised re-typesetting ('Art. 1º', 'I - os menores de 16 (dezesseis) anos;' for 1916's 'I. Os
  menores de dezesseis anos.'), has no Introdução at all, and prints only the in-force text in black/blue/red (green =
  revoked, under 'Texto original:'). The built-in REPEAL CHECK (exact text) therefore differs in ~1200 articles and cannot be
  the check: cmp2002.py is (per unit: present on both sides, same line labels after normalising, word-similarity >= 0.85 with
  accents/punctuation removed). Its decision line must replace the built-in one (or explain it) before PUBLISH.
- Trial t5 (b44/zzzzb-t5.json; logs/t5.log, cmp5.log): 3908 paras, 1820 units, 27 versions, last change before the repeal
  2001-02-16; cmp2002: ok 1636, differ 89, only-2002 12, only-replay 2 (+21 Introdução units, absent in 2002 by design).
### TO DO for zzzzb, in this order (publish only when every item is closed)
1. Replace the parser's struck-line ends for this act by a model fit for an all-struck page (the cause of most of the 89):
   'next-wording' ends a line at the next law-dated line of the ARTICLE whatever its label, so an 'Incluído' line ends its
   neighbours (art. 16: Lei 9.096/1995's III and § 3º ended the caput, I, II, §§ 1º-2º; same in arts. 12, 134, 178, 180, 195,
   248, 258, 267, 589, 947, 1.611, ...). Rule to implement: a line ends (a) by its own Revogado/Suprimido/Eliminado note, (b) at
   the start of the next line of the same unit with the same label key (roman numeral / § n / parágrafo único / alínea /
   caput; empty labels: read 'I.' / 'II.' from the text), (c) for sub-lines of a caput a law rewrote WITH new sub-lines of its
   own (art. 6: Lei 4.121 caput + I-III + par. único), at that rewrite; a caput-only rewrite leaves the old sub-lines; (d)
   otherwise at the repeal. Check 'parent'/'heads'/'successor' ends the parser set against this. Re-run cmp2002 until 0.
2. Decreto 3.725/1919 (the user calls it Lei 3.725/1919: 'Decreto do Poder Legislativo', page law:dl-3725-1919 =
   decreto/Historicos/DPL/DPL3725-1919.htm, cached; key it dec-3725-1919 in B12.DECREES like dec-2044-1908; footer 'publicado
   na CLBR, de 31.12.1919', signed 15.1.1919, art. 4 only revokes): a normal amendment on its own day (user). Find its Diário
   Official day (Chamber legin publicacaooriginal copy through archive.org, or LexML /urn/ record, 6 s), day = 3rd day after
   (CC 1916 Introdução art. 2, Distrito Federal; the LICC 1916 three-day rule). NOTE_FIX every form: 'Decretoi nº 3.725, de
   1919', 'Decreto nº 3.725, de 1919', 'Decreto-Lei nº 3.725, de 1919' and 'Decreto-Lei nº 3.725, de 1970' (both link to the
   DPL3725-1919 page: misprints), 'Eliminado pelo', 'Suprimido pelo', 'Renumerado do § 1º / do paragrafo único pelo'.
   Then the ~150 <strike>-no-note 1916 lines followed by a corrected css wording (cls3 'tagnonote'): each is a 3.725
   correction only if the decree's text lists that article (its 'Art. N - Diga-se/Supprima-se/Elimine-se ...' items): end the
   old line / start the corrected one on 3.725's day, credited to it, decision line listing them; any not in the decree stays
   explained or undated. Skip the decree-text annotation lines ('none'). Mixed lines (arts. 179 'X.', 443, 458, 624 x2):
   partial strikes inside one line, read each by hand.
3. Decreto 20.330/1931 (notes 'Incluído/Renumerado pelo Decreto nº 20.330, de 1931', art. 9 §§ 1º-2º; hrefs D20330.htm and
   D3520.htm): key, record, page and day (a decree of the Provisional Government with force of law).
4. 'Lei nº 4.123, de 1962' notes (5) link to L4121.htm: read Lei 4.121's text for those words; NOTE_FIX to 4.121 if so (Lei
   4.121: art. 4 '45 (quarenta e cinco) dias após a sua publicação', DOU 3.9.1962).
5. Unit keys: 'Art. 1.1504.' (art-11504 -> art-1504, UNIT_FIX), 'Art.. 1.661' and the testamento marítimo/militar run
   (arts. 1.656-1.669 mis-keyed: only-2002 1.659, 1.661-1.663, 1.665-1.667, 1.669, 1.720; replay 'art' labels in 1.658, 1.660,
   1.664, 1.668, 1.719), art. 332/333 (only-replay 332, only-2002 333), art. 1.400 (only 2002), art-0001 doubled 'Art. 1'.
6. 'restored wording after an open one' art-0693 (Lei 2.437/1955?), the 1.723/1.787 low ratios, preambulo/titulos.
7. Introdução (arts. 1-21): no official note dates its end; the LICC (Decreto-Lei 4.657/1942, in force 24.10.1942) has no
   revoking clause (checked on the cached lindb page); the 2002 capture omits it. As with the Código Comercial's Parte
   Terceira: stands as printed, B13.OPEN_ITEMS + decision (its arts. 5 and 20 par. único are <strike> with no note: read them).
8. Pre-1917 folds: no amending law in the notes is before 1.1.1917 (so far): confirm, and say so in the PUBLISH line.
9. Every law's in-force day (lawdays.py; pre-1970 dates clamp in commits, In-force trailer keeps the day); last change before
   the repeal 2001-02-16 in t5: confirm no 2001-2002 change is missing.
10. pipe.sh x2, dupsame/uniqlaws, merged check, README row (docs.py rows-zzzzb.json), jurisdiction.json, PUBLISH.
- PIDs (all mine, foreground through run.py unless said; all exited): setup 3732, head 20292 (rc 1), rt1 8396, rt2 54264, lt1
  37568, col1 31236, t1 18224 (rc 1: pin with "via") then 23464, robots 42120, laws1 49960 (background task, iaonly laws), t2
  27816, lx1 3112 (LexML, 2 requests 6 s apart), lx2 19764, lv1 2668, li1 27208, lt2 47684 (moved to background by the tool
  timeout while waiting on the cpu gate; finished), rt3 17088, bd1 48736, t3 24548, t3s 44260, cls1 12212, t4 17896, t4s 40072,
  pd1 7428, t5 29112, cmp5 40452, uq1 21944 (background by timeout; finished), pids1 4864 (rc 1), wait1, lt3 28468, lp1 54888,
  bd2, lv2, lv3, vd1, inst1 15832, final build 28548, bd3 6896 (+146 -0), finish 45304 (after-copies, claim released); pipe1 (background, mine) 45032 39692 21588
  51016 50700 43676 25464; pipe2 (foreground) 29224 44580 25392 51688 9240 42832 46104 (pipe.sh's file-check run.py PIDs go to
  /dev/null). Two waits of my own on the pipe1 log (one background until-loop, one foreground loop), both ended by themselves.
  Outside the wrappers (mistakes; small local reads/writes, no network): cat of setup.log; cat-heredoc writes of
  tools/colors.py and tools/logsum.py; mkdir of b44/robots; greps/cut/head/tail/tr over my own b44 logs and the pipe output;
  one no-op echo. Nothing running.

## State at handoff (batch 17, forty-fourth session, 2026-11-02)
Re-PUBLISHED this session: zzzza (CPC 1973; Lei 7.219/1984 and Lei 9.040/1995 DOU days from their official publication
records; 67 versions). Merged build of the installed folder: 296 acts, 4046 versions, 2826 commits, check 0/0, --compare
identical, audit_push clean main + futuro; uniqlaws 0; dupsame 0. README row + jurisdiction.json unchanged (still current).
Files changed: parse_batch17.py (+146 -0 vs b44/before: zzzza DOU fix; zzzzb config and block), sources_batch17.json (+1 pin
l3071), corpus.d/99-batch17zzzza.json + .PUBLISH, PROGRESS.md (+ checkpoint). effects_fix.py, law_records.json, README,
jurisdiction.json unchanged. zzzzb is configured in PARTS but not published (no corpus.d file). Nothing running. Claim released.
NEXT: CC 1916 (part zzzzb) TO DO items 1-10 above (item 1, the end model for an all-struck page, first).
OPEN / DATED RE-CHECKS: unchanged from the forty-first handoff (the two DOU days are closed).

## Forty-fifth session (2026-11-02): CC 1916 (part zzzzb) items 1, 3, 4 DONE, item 2 PARTLY; NOT PUBLISHED
Claim taken at the start ('gitlaw-BR-45 alan-dell 2026-11-02T06:00Z'), released at the end. Scratch: .gitlaw-scratch/brazil-b44
(before45/ = session-start copies of parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json,
dupsame_allow.json, effects_fix.py, README.md, jurisdiction.json, PUBLISH, firstline.py, pipe.sh, both PROGRESS.md; logs45/;
pids45.txt; new tools: rr.py (run.py + log print + PID record), sh.py (a shell read under run.py), bdiff45.py (diff vs
before45), pu.py (one unit's paras from a dump), notes45.py, href45.py (2026 page note links), used45.py (CC16_USED
counters), lx45.py (LexML: robots first, 6.5 s apart), ia45.py (archive.org: robots first, shared client)). cmp2002.py
changed: 1916 'Paragrapho unico' / 'Parágrafo.único' and l-for-I numerals read as labels; LB (line split) and ORDER kinds
shown; units in M._CC16_EXPLAINED (to be written, item 10) count as 'explained'.
Requests: robots.txt of www.lexml.gov.br, archive.org, web.archive.org (b44/robots45/); LexML 1 record
(urn:lex:br:federal:decreto:1919-01-15;3725, no challenge); archive.org 1 CDX + 1 capture (D20330.htm) through the shared
client. No Common Crawl, no Arquivo.pt, no live Planalto, no challenge page.
Trial t9 (b44/zzzzb-t9.json, logs45/t9.log, cmp9.txt): 0 problems (was 21), 29 versions; cmp2002 ok 1668, differ 57 (was
89; 10 are LB line splits), only-2002 12, only-replay 2, + 21 Introdução units.
### Done (parse_batch17.py, zzzzb block only: +254 -12, the 12 removed lines are this block's own trial code; effects_fix.py
unchanged; sources_batch17.json +2 pins law:dec-3725-1919 (DPL3725-1919.htm, 20261018192140) and law:dec-20330-1931
(decreto/1930-1949/D20330.htm, 20260801070244))
1. End model (_cc16_key, _cc16_model): label path per line (caput / § or parágrafo único / inciso / alínea / item, read from
   the text when the parser gives no label; l-for-I numerals; unlabelled caput lines are (1,'cont')). Ends: own note kept
   ('note', 'twin', ...); (b) 'next-label' = the next wording of the same path (parágrafo único = § 1º; renum_from); (c)
   'list-rewritten' = the line above rewritten the same day by the same law with a list of this kind from its first label;
   'with-caput' for a 'cont' line whose caput is replaced and the new caput has none; (a) 'parent-revoked'; else repeal.
   Headings no note/slot ends stand to the repeal (not the shared 'heads' rule). Print order (record=False pass): each
   wording takes its first predecessor's place (arts. 186, 258, ...: 16 units reordered).
3. Decreto 20.330/1931: B12.DECREES dec-20330-1931 (27.8.1931, DOU 1.9.1931 from its page footer, title from the page),
   VIGENCIA_FIXED 4.9.1931 (Introdução art. 2, three days). art. 9 parágrafo único -> § 1º, § 2º added: cmp ok.
4. 'Lei nº 4.123, de 1962' (5 notes): link L4121.htm#art1; Lei 4.121 art. 1 gives art. 246 parágrafo único, 263 XII-XIII,
   269 III-IV these lines -> NOTE_FIX to Lei 4.121 with reason. Also art. 263 XI's second line 'Redação dada pelo Decreto nº
   3.725, de 1919' (inside 4.121's recast list, words = Lei 4.121 art. 1's XI) -> NOTE_FIX to Lei 4.121, reason given.
2 (part). Decreto 3.725/1919: LexML record 'Publicação Original 1919-01-19 Diário Oficial da União. Seção 1. 19/01/1919. p.
   1084' (cached .cache, fetch.get); no vigência clause (art. 4 only revokes; arts. 1-2 order the corrected edition) ->
   VIGENCIA_FIXED 22.1.1919 (LICC 1916 = Introdução art. 2, three days, Distrito Federal); B12.DECREES dec-3725-1919;
   NOTE_FIX of the 6 misprinted forms (all their links open DPL3725-1919.htm: href45.py). Annotation lines (decree
   instructions printed unstruck in arts. 10, 137, 642) dropped in _paragraphs_cc16 (CC16_USED['annot']). Strike class per
   line ('cc16_cls': css / tag / none / mixed, from a second read with the CSS removed). _cc16_decree_units(): the 189
   articles art. 3 corrects (Introdução items keyed art-in-). FINDING: the 2026 page almost never prints both wordings:
   only 2 'dec-pair' (1916 css line then a corrected <strike> line, no note: arts. 139 and one more) -> corrected line
   starts 22.1.1919 credited to the decree; 138 'tag-alone-listed' lines = ONE wording printed, struck by <strike>, no note,
   in an article the decree corrects (mostly the 1916 words; some already corrected, e.g. art. 10), and 7
   'tag-alone-unlisted' (arts. 6 par. único, 9 par. único (20.330), 332, 346, 413 VI, 883, 1.605 § 1º). These keep the
   printed wording 1917 -> repeal (coordinator's reading) and need a decision line.
### TO DO for zzzzb (exact; publish only when every item is closed)
2 (rest). a) Decision line for the tag-alone lines (CC16_USED 'tag-alone-listed'/'-unlisted'): Planalto prints one
   wording, struck by <strike> without a note, where Decreto 3.725/1919 corrected the article; the corrected text is not
   on the page, so the printed wording stands 1917 -> repeal. Read the 7 unlisted ones (332, 346, 413 VI, 883, 1.605 § 1º:
   another law? 1.605 § 1º is absent in 2002). b) Whole-dispositivo suppressions the decree orders and the page strikes
   by <strike> (art. 1.372 parágrafo único 'Supprima-se'): end on 22.1.1919 credited to the decree (dated change from
   official text) - decide case by case; art. 1.786 par. único / 1.787 (decree: 1.787 suppressed, 1.786 par. único becomes
   art. 1.787) and art. 243 par. único (moved to art. 245 in 2002) are NOT printed in corrected form: keep as printed +
   decision. c) art. 220: 'none' line 'A anulação ... nºs I, II e III, só poderá demandar o outro cônjuge e, no caso do
   nº IV, só o marido' (unstruck, no note) + tag line 'A annullação ... o conjuge enganado' both alive (doubled): find the
   law of the unstruck wording (2002 has the 'cônjuge enganado' wording!), likewise art. 340 (unstruck caput). d) Mixed
   lines by hand: art. 179 'X. (Eliminado pelo Decretoi ...)' (NOTE_FIX is in place, but the note is inside the struck
   text: rubrica line), 443 III, 458, 624 caput and par. único. e) art. 35 §§ 3º-4º 'Renumerado do § 1º/§ 2º' start
   22.1.1919 with no 1917 wording on the page: before 22.1.1919 the old §§ 1º-2º are missing - placeholder line '[A fonte
   não dá o texto vigente nesta data.]' 1917 -> 22.1.1919 (coordinator rule) or decision. f) Introdução art-in-0005 and
   art-in-0020 par. único are tag-alone-listed (3.725 corrects them): fold into item 7.
5-10: unchanged from the forty-fourth session's list above (5 unit keys: art-0001 doubled 'Art. 1. 400' (= art. 1.400,
   only-2002), 'Art. 1.1504.' (art-11504), 332/333, 1.656-1.669 testamento run, 1.719/1.720; 6 art-0693 restore (no
   longer a problem line in t9: re-check), 1.723/1.787 ratios, preambulo/titulos; 7 Introdução; 8 pre-1917 folds; 9 every
   law's in-force day (watch: art. 134 §§ 1º-5º 'Incluído pela Lei nº 6.952, de 1981' start 1973-11-10 in t7: a wrong day
   or key, check lawdays); 10 pipe.sh x2, dupsame/uniqlaws, merged check, README row, jurisdiction.json, PUBLISH, and the
   decision lines: the end model, the print-order rule, 3.725/20.330/4.121 days and NOTE_FIXes, _CC16_EXPLAINED (the
   cmp2002 differences left: LB line splits, ORDER (art. 248 par. único after IV in 2002), retyping, 3.725 not printed)
   replacing the built-in REPEAL CHECK line (still 1208 articles in t9's log).
Remaining cmp2002 DIFF units in t9 (57): 0001 0035 0040 0152LB 0159LB 0179 0194 0195LB 0220 0243 0245 0248 0267 0368 0500
0521 0615 0617 0762LB 0770LB 0772LB 0802 0814LB 0817 0825LB 0889 0904LB 0910 1067 1081LB 1119 1164 1183 1229 1298 1372 1380
1381 1399 1409 1515 1521 1522 1566 1605 1658 1660 1664 1668 1671 1719 1723 1728 1779LB 1786 1787 preambulo; only-2002:
0333 1400 1504 1659 1661-1663 1665-1667 1669 1720; only-replay 0332 11504.
- PIDs (all mine, foreground through run.py via rr.py; all exited): setup45 53344, ls1 38572 (rc 2) 51948, ls2 27292, ls3
  10108, g1 20816, g2 47424, pu1 33416 (rc 1) 16392, c1 29676, bd1 12096, t6 6816 30064, cmp6 9240, cmp6s 51552, pd6 43676,
  pu2 35112, c2 9280, t7 45608, cmp7 49156, pd7 42836, pu3 37780, t8 52968, cmp8 20160, cmp8s 27756, c3 40144, c4 27352,
  lt1 49672, c5 12792, lx1 33408 (LexML), lt2 17088, n1 43408, c6 29188, pd8 14708, pu4 26740, c7 53424, h1 25864, g3
  20832, u1 30132, u2 26224, c8 33396, c9 33368, ia1 19916 (archive.org), lt3 45404, lt4 21248, g4 49308, g5 49508, t9
  33788, cmp9 47296, cmp9s 45328, bd2 16916, sd1 7304, then the handoff's pids/release runs (see pids45.txt). Outside the
  wrappers (mistakes, small local reads/writes, no network): at the start one ls of b44 and b44/tools + a cat of the
  missing claim file; ls/cat/head of brazil-law, batch17/.tmp/pipe.sh, run.py, setup.py, release.py and the first
  PROGRESS lines; a 'which cpuwait low.py'; one mkdir of logs45; one sed writing tools/bdiff45.py; small python -c / head
  reads of my own logs45 files (cmp lists, lt2/lt4 logs, pids45.txt). Nothing running.

## State at handoff (batch 17, forty-fifth session, 2026-11-02)
Nothing installed or published this session; installed state unchanged: 296 acts, 4046 versions, 2826 commits (check 0/0,
compare identical, audit clean as at the forty-fourth handoff). zzzzb configured in PARTS, trial t9 only, no corpus.d file.
Files changed: parse_batch17.py (zzzzb block, +254 -12 vs b44/before45), sources_batch17.json (+2 pins), PROGRESS.md (+
checkpoint), this file. effects_fix.py, law_records.json, dupsame_allow.json, README, jurisdiction.json unchanged.
NEXT: zzzzb TO DO 2 (rest, a-f), then 5-10, in order.

## Forty-sixth session (2026-11-02): CC 1916 (part zzzzb) items 2 (a-f) and 5-10 DONE; PUBLISHED
Claim taken at the start ('gitlaw-BR-46 alan-dell 2026-11-02T06:24Z'), released at the end. Scratch: .gitlaw-scratch/brazil-b44
(before46/ = session-start copies; logs46/; pids46.txt; new tools: setup46.py, rr46.py, bdiff46.py, dec46.py (Decreto 3.725
art. 3 items from the cached page), decs46.py (decisions of a part), art2002.py (an article's text on a cached page),
firstline46.py (firstline.py with the Introdução keys art-in-), lx46.py (LexML, robots first, 6.5 s apart); cmp2002.py now
counts ONLY units listed in M._CC16_EXPLAINED as explained (old copy cmp2002.bak45.py)).
Requests: robots.txt of www.lexml.gov.br (read twice, once per lx46 run; b44/robots46/) and 5 LexML /urn/ records, 6.5 s apart
(decreto.lei:1943-09-20;5860 (no record: wrong day), decreto.lei:1945-11-22;8207, lei:1981-12-10;6969, lei:1981-11-06;6952,
decreto.lei:1943-09-30;5860). No archive.org, no Common Crawl, no Arquivo.pt, no live Planalto, no challenge page.
Coordinator decisions applied: art. 263 XI's 'Redação dada pelo Decreto nº 3.725' line credited to Lei 4.121 (its NOTE_FIX
reason rewritten as the decision line: the decree adds XI once, its list gives no second wording); the one-wording lines stand
1917 -> repeal with ONE decision line (_W_CC16_ONEWORD; counts now 140 listed + 2 unlisted, see below).
### Done (parse_batch17.py zzzzb block only, +325 -6 vs before46 (the 6 removed lines are this block's own: the decree-unit
regex, the plain-line skip, the 263 XI reason); effects_fix.py unchanged; sources_batch17.json +1 pin law:lei-3447-1958 (same
url/ts as law:lei-3447-1957); law_records.json +1 record lei-9610-1998 (batch8's url, for uniqlaws))
2a. _W_CC16_ONEWORD (counts from CC16_USED). The decree-unit reader now also takes items after a comma (', Art. 883:'), 'Ao
   art: 346' and 'Art. 248;' (192 articles, was 189): 346 and 883 moved from 'unlisted' to 'listed'.
   Unlisted ones read: art. 332 = the 8.560 note misplaced on art. 333 (2002 page: 'Art. 332. Revogado pela Lei n° 8.560');
   note moved, 332 ends 30.12.1992, 333 to the repeal (_W_CC16_332). Art. 1.605 § 1º: the 2002 page prints '§ 1º Revogado
   pela Lei n° 6.515, de 26.12.1977' -> note added, ends 27.12.1977 (_W_CC16_1605) [NOT in the coordinator's ruling, which
   had it standing to the repeal: new evidence from the official 2002 page; revert = drop the note1605 block]. Left unlisted
   (stand as printed): art. 9 parágrafo único (Decreto 20.330's renumbering, ends by next-label), art. 413 VI.
2b. _CC16_SUPPRESSED: art. 1.372 parágrafo único and art. 1.787 end 22.1.1919 'dec-suppressed' (_W_CC16_SUPPR, which also says
   1.786 par. único / new 1.787 and 243 par. único are not printed as moved, and art. 178 § 10 X). The marker line 'X.
   (Eliminado pelo Decretoi nº 3.725, de 1919)' (keyed art-0179) is dropped (CC16_USED 'elim'). Decree additions printed with
   no note start 22.1.1919: art. 178 § 6º XIII, § 9º VI, art. 242 IX, art. 391 IV (_CC16_DEC_ADDED, _W_CC16_ADDED).
2c. art. 220: the unstruck 1916 caput ends 22.1.1919 when the decree's wording starts (cc16_plainend; _W_CC16_PAIRS lists the
   two pairs, arts. 139 and 220). Art. 340: one wording (caput unstruck), in _W_CC16_ONEWORD.
2d. Mixed lines (443 III, 458, 624 caput and par. único): one line each, as printed (_W_CC16_MIXED).
2e. art. 35 §§ 3º-4º start 22.1.1919 (§ 4º set by the block; § 3º by its note) (_W_CC16_ART35).
2f. Introdução arts. 5 and 20 par. único: in the one-wording count and named in B13.OPEN_ITEMS[_LCC16].
5. Labels: 'Art.. 1.659.' (1.659, 1.661-1.663, 1.665-1.667, 1.669, 1.720), 'Art. 1. 400.', 'Art. 1.1504.' read as 'Art. N.' and
   filed with their following lines under their own article (_W_CC16_LABELS); art. 194's closing formula moved from art. 195's
   'rubrica' to art. 194 (_W_CC16_194). 332/333 as in 2a.
6. art-0693 fine (1916 -> 2.437 1956 -> 5.827 1972); 1.723/1.787 explained; preamble explained (2002 legend).
   Also found: the shared 'rows' rule had given 1916 lines later starts (art. 12 II-IV from 1977, art. 178 § 6º X-XIII from
   1956): set back to 1917 (XIII to the decree) and removed from B3.ROWS (_W_CC16_ROWS); the shared 'next-wording' decision
   entries for this act removed (the model replaces those ends).
7. Introdução: B13.OPEN_ITEMS[_LCC16] (stands as printed; LICC 1942 has no revoking clause; not on the 2002 page).
8. No start/end before 1.1.1917 in the dump: no pre-1917 fold (said in the PUBLISH line).
9. Law days (lawdays.py): Lei 6.952/1981 published 10.11.1981 (page '1973'; LexML p. 21093; LAW_FIELD_FIX + VIGENCIA_FIXED):
   art. 134 §§ 1º-5º now start 10.11.1981. Lei 6.969/1981 (page 'DOU 11.12.1980') and Decreto-Lei 8.207/1945 (page CLBR only)
   corrected by page_info from the cached LexML records (11.12.1981 -> in force 25.1.1982, 45 days, art. 11; 27.11.1945).
   Decreto-Lei 5.860/1943: of 30.9.1943 (page head '20 de setembro'), DOU 2.10.1943 (LAW_FIELD_FIX enacted+published,
   VIGENCIA_FIXED). NOTE_FIX 'Lei nº 6.515, de 1970' -> 1977 (link L6515.htm#art50), 'Lei nº 3.447, de 1957' -> 1958 (two
   forms; Lei 3.447 of 23.10.1958). VIGENCIA_FIXED lei-2437-1955 1.1.1956 (art. 3) so it has a decision line. Last change
   before the repeal 16.2.2001 (Lei 10.192/2001).
10. Decision lines _W_CC16_MODEL (end model), _W_CC16_ORDER (print order, 16 articles), _W_CC16_REPEALX (replaces the built-in
   CC16 REPEAL CHECK line, which listed ~1,200 exact-text differences; 370 KB less in the part) from _CC16_EXPL_GROUPS /
   _CC16_EXPLAINED (46 units). cmp2002 on the installed part: ok 1691, explained 46, 0 differ, 0 only (+21 Introdução units).
   pipe.sh zzzzb x2 (logs46/pipe1.out, pipe2.out): pipe2 parse 43303bae x2, 0 problems, 0 moves, dupcheck/leakcheck/pubgap/
   missorig 0, uniqlaws 0 (pipe1 had 1: lei-9610-1998 url case -> law_records.json), dupsame 0; firstline.py CRASHES on
   art-in- keys (shared checker, not changed): firstline46.py gives 0. Benign, law text as printed: dupline 3 / ordercheck 1
   (art. 178 alíneas a)-c) under § 9º I and V), quotecheck 2 (arts. 588, 1.611), latecaput 28 (1916 lines under caput-only
   rewrites, per the end model); merged 297 acts, 4075 versions, 2851 commits, 0/0, identical, audit clean main + futuro.
   PUBLISHED: install.py zzzzb -> corpus.d/99-batch17zzzzb.json 1ee67c17 + .PUBLISH (b44/publish-zzzzb.txt); docs.py
   b44/rows-zzzzb.json (README row; jurisdiction.json 297 acts 4075 versions, entry 'Lei 3.071/1916 1917-2003 (29)', once).
   Final merged build of the installed folder (logs46/fb1.log): 297 acts, 4075 versions, 2851 commits, check 0/0, 0 trailer
   errors, --compare identical, audit_push clean main + futuro.
- PIDs (all mine, foreground through run.py via rr46.py unless said; all exited): see b44/pids46.txt (setup46 39920 ... fb1
  32952); pipe.sh runs 1 and 2 were background tasks of mine (their run.py PIDs are in logs46/pipe1.out / pipe2.out), each
  waited on by one Monitor until-loop of mine that ended by itself. Outside the wrappers (small local reads/writes, no
  network): at the start ls/head/cat/grep of brazil-law, b44, the brief and the handoff; sed copies writing tools/setup46.py,
  rr46.py, bdiff46.py, lx46.py, firstline46.py; one sed edit of tools/dec46.py; a heredoc writing tools/decs46.py; one python
  heredoc patching tools/cmp2002.py and one rewording two lines of parse_batch17.py (LF kept); small cat/grep reads of my own
  logs46 files and pids46.txt; tool-written files (Write/Edit): parse_batch17.py, sources_batch17.json, law_records.json,
  tools/dec46.py, tools/art2002.py, rows-zzzzb.json, publish-zzzzb.txt, this text. Nothing running.

## State at handoff (batch 17, forty-sixth session, 2026-11-02)
PUBLISHED: zzzzb (Código Civil de 1916, 29 versions 1917-2003). Installed: 297 acts, 4075 versions, 2851 commits, check 0/0,
compare identical, audit clean main + futuro; uniqlaws 0, dupsame 0; README row + jurisdiction.json updated.
Files changed: parse_batch17.py (+325 -6 vs b44/before46), sources_batch17.json (+1 pin), law_records.json (+1 record),
corpus.d/99-batch17zzzzb.json + .PUBLISH, repo/README.md (+1 row), repo/jurisdiction.json, PROGRESS.md, this file.
effects_fix.py, dupsame_allow.json unchanged. Claim released.
FOR THE COORDINATOR: (1) art. 1.605 § 1º now ends with Lei 6.515/1977 from the 2002 page's note (the ruling had it standing
to the repeal); (2) art. 1.786 par. único -> art. 1.787 (decree text gives the new wording, page does not print it) is left
as printed + decision; could be replayed from the decree's text if wanted; (3) shared batch10/.tmp/firstline.py crashes on
'art-in-' unit keys (Introdução); pipe.sh shows the traceback. NEXT: none open for zzzzb; OPEN / DATED RE-CHECKS unchanged.

## Forty-seventh session (2026-11-02): zzzzb re-PUBLISHED (art. 1.787 from Decreto 3.725's text); firstline.py widened; LC 95/1998 PUBLISHED (part zzzzc)
Claim taken at the start ('gitlaw-BR-47 alan-dell 2026-11-02T07:05Z'), released at the end. Scratch: .gitlaw-scratch/brazil-b44
(before47/ = session-start copies (parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json, dupsame_allow.json,
effects_fix.py, README.md, jurisdiction.json, PUBLISH, firstline.py, pipe.sh, both PROGRESS.md, corpus.d/99-batch17zzzzb.json);
logs47/; pids47.txt; new tools: setup47.py, rr47.py, bdiff47.py, finish47.py, flcmp47.py (old vs new firstline.py on every
part), allacts47.py (installed acts by number), pg47.py (regex over a cached page's text)).
Requests: robots.txt of archive.org (200: Disallow /control/ /report/) and web.archive.org (404) (b44/robots47/); archive.org
through the shared client (iaonly.py): 1 page pin (lcp95) + 1 law pin (law:lc-107-2001). No LexML, no Common Crawl, no
Arquivo.pt, no live Planalto, no challenge page.
Coordinator decisions applied: art. 1.605 § 1º ends 27.12.1977 and art. 332 ends with Lei 8.560/1992 (both already so; no change).
### 1. zzzzb: art. 1.786 parágrafo único / new art. 1.787 (re-PUBLISHED)
- parse_batch17.py zzzzb block: _CC16_MOVED {('art-1786', (1,'1'))} -> the parágrafo único ends 22.1.1919 'dec-moved', credited
  to dec-3725-1919; _cc16_dec_1787() reads the decree's words from its cached page ('...com esta redacção: «No caso do artigo
  antecedente, se ao tempo do fallecimento do doador, os donatarios já não possuirem os bens doados, trarão á collação o seu
  valor»'); _cc16_model inserts 'Art. 1.787. <words>.' (full stop after the quotation, as the decree's sentence) after the
  1916 art. 1.787 line, from 22.1.1919, credited to the decree, to the repeal (idempotent over the two passes, 'cc16_v1787').
  Decision _W_CC16_1787 (new); _W_CC16_SUPPR's sentence 'the history has no art. 1.787 from 22.1.1919' replaced by a pointer;
  _CC16_EXPL_GROUPS 'decadd' no longer lists 1786/1787 (they now match the 2002 page).
- Unit-level day diff (unitdays.py, installed 1ee67c17 vs new): ONLY art-1786 (T and C on 1919-01-22, T after) and art-1787
  (T from 1919-01-22) change; same 29 version days. cmp2002 on the new part: ok 1693 (was 1691), explained 44 (was 46), 0 differ.
- pipe.sh zzzzb (logs47/pipe1.out): parse ae93e796 x2, 0 problems; output identical to session 46's pipe2 except the sha, the
  firstline traceback (gone, 0 flags) and the built-in repeal-check count (1199 for 1200; that line is replaced by the decision);
  dupline 3 / ordercheck 1 / quotecheck 2 / latecaput as before; uniqlaws 0, dupsame 0; merged 297 acts, 4075 versions, 2851
  commits, 0/0, identical, audit clean main + futuro. reinstall.py -> corpus.d/99-batch17zzzzb.json eff29b94; .PUBLISH = the
  forty-sixth line + a forty-seventh line (b44/publish-zzzzb47.txt). README row + one sentence on art. 1.787 (counts unchanged;
  jurisdiction.json unchanged: same versions). Final merged build of the installed folder (logs47/fb1.log): 297/4075/2851, 0/0,
  identical, audit clean.
### 2. batch10/.tmp/firstline.py (shared checker) widened
- Unit-key pattern now `(?:adct-)?art-(?:tu-|in-)?0*(\d+)(?:-([a-z]+))?$` (as b44/tools/firstline46.py), comment updated.
  flcmp47.py (logs47/fl1.log): old (before47 copy) vs new on corpus.json + every corpus.d part (144 files): 143 identical
  output, rc 0 both; the only difference is 99-batch17zzzzb.json (old: AttributeError on art-in- keys; new: rc 0, no flags).
### 3. Ranked list: the thirtieth session's list is finished (items 1-19 installed: zzzi .. zzzzb). Fresh ranked list (installed
acts checked by allacts47.py, no request):
 1 Lei Complementar 95/1998 elaboração das leis [zzzzc, DONE]   2 Lei 9.615/1998 Lei Pelé (heavy; much replaced by Lei 14.597/2023)
 3 Lei 10.931/2004 patrimônio de afetação / CCB   4 Lei 8.171/1991 política agrícola   5 Lei Complementar 97/1999 Forças Armadas
 6 Lei Complementar 73/1993 AGU   7 Lei 5.250/1967 Lei de Imprensa (ADPF 130)   8 Lei 7.170/1983 LSN (revoked by Lei 14.197/2021)
 9 Lei 6.194/1974 DPVAT   10 heavy tax: Lei 10.865/2004, Lei 9.532/1997, Lei 12.546/2011.
### 99-batch17zzzzc - PUBLISHED: Lei Complementar 95/1998 (lei-da-elaboracao-das-leis, LCElab, 2 versions 1998-05-28, 2001-04-27)
- PAGES lcp95 (leis/lcp/lcp95.htm, pinned by `iaonly.py pages lcp95`); `laws lcp95` 1 new (law:lc-107-2001); act-scoped
  `missing` 0. Page: 22 notes (Redação 12, Incluído 5, Incluída 1 = LC 107/2001; Vide 4 = Decretos 2.954/1999, 4.176/2002,
  9.191/2017, 12.002/2024, regulations, not amendments). No compilado pinned (the page links one; the check page = the annotated
  page, as zzzg).
- Config: act (2 digits), PARTS zzzzc, ACT_DAY_ALL lc-95-1998 28.5.1998 (art. 19: ninety days from DOU 27.2.1998, counted as Lei
  13.966's), ACT_LAWS_ALL lc-95-1998 (ementa from the page; enacted 26.2.1998, DOU 27.2.1998). LC 107/2001: DOU 27.4.2001, art. 3
  in force on publication (read on its page; the reader dates it so).
- Block '# part zzzzc': paragraphs wrapper on lcp95 ('Art. 18 - A (VETADO)' -> unit art-18-a, label 'Art. 18-A', text as
  printed; EXTRA decision); B15.TEXT_FIX art. 8 § 2º closing quote after 'oficial' from LC 107's own text (decision via
  TEXT_FIX_USED).
- pipe.sh zzzzc (logs47/pipe-c1.out): ec95f93a x2, 0 problems, 0 moves; dupline/dupcheck/leakcheck/firstline/pubgap/ordercheck/
  missorig 0; quotecheck 5 = quoted words printed in the law; latecaput 3 = 1998 art. 14 I-III (end with LC 107's rewrite of
  the whole article that day); uniqlaws 0, dupsame 0; merged 298 acts, 4077 versions, 2853 commits, check 0/0, --compare
  identical, audit_push clean main + futuro. install.py -> corpus.d/99-batch17zzzzc.json ec95f93a + .PUBLISH
  (b44/publish-zzzzc.txt); docs.py b44/rows-zzzzc.json (README row; jurisdiction.json 298 acts 4077 versions, entry
  'LC 95/1998 1998-2001 (2)'). Final merged build of the installed folder (logs47/fb2.log): 298 acts, 4077 versions, 2853 commits, check 0/0, 0 trailer errors, --compare identical, audit_push clean main + futuro (fb2 PID 33692).
- PIDs (all mine; foreground through run.py via rr47.py, listed in b44/pids47.txt: dec1 43452 ... bd6 36416, then fb2, the
  handoff write and fin1; all exited): setup47 27156, ls1 34168 (rc 1, a /c/ path in Python), ls2 35040 through run.py
  directly; pipe.sh runs zzzzb and zzzzc foreground (their run.py PIDs in logs47/pipe1.out, pipe-c1.out); three rr47 runs
  (hd2, pg3, in1+dk1) and fb2 passed the tool's 2-minute limit while run.py waited on the cpu gate and finished as background
  tasks of mine (each waited on by its own notification, no poller). Outside the wrappers (small local reads/writes, no
  network): at the start one bash head/ls/wc/grep of brazil-law and batch17/PROGRESS.md, before the rules were re-read; one
  `cat` of logs47/ls1.log and ls2.log, pipe.sh, pipe1.out, pipe-c1.out and robots47 files; one `head -3` of three b44 tools;
  one `mkdir -p` of b44/robots47; tool-written files (Write/Edit): parse_batch17.py, batch10/.tmp/firstline.py,
  repo/README.md (the zzzzb sentence), b44 tools/rows/publish files, this text, PROGRESS.md. Nothing running.

## State at handoff (batch 17, forty-seventh session, 2026-11-02)
PUBLISHED: zzzzb re-PUBLISH (eff29b94; new art. 1.787 from Decreto 3.725's text) and zzzzc (LC 95/1998, ec95f93a, 2 versions).
Installed: 298 acts, 4077 versions, 2853 commits, check 0/0, compare identical, audit clean main + futuro; uniqlaws 0, dupsame
0; README rows + jurisdiction.json current. Files changed: parse_batch17.py (+97 -7 vs b44/before47: PAGES lcp95, act, PARTS
(+ the stale zzzzb comment), ACT_DAY/ACT_LAWS lc-95-1998, zzzzb block (1.787), '# part zzzzc'), batch10/.tmp/firstline.py (art-in-
keys), sources_batch17.json (+2 pins: lcp95, law:lc-107-2001), corpus.d/99-batch17zzzzb.json + .PUBLISH, corpus.d/99-batch17zzzzc
.json + .PUBLISH (new), repo/README.md (+1 row, +1 sentence), repo/jurisdiction.json, PROGRESS.md, this file. effects_fix.py,
law_records.json, bad_pins.json, dupsame_allow.json unchanged. Claim released.
NEXT: the fresh ranked list above from item 2 (Lei 9.615/1998, Lei Pelé: survey first; heavy, MPs and Lei 14.597/2023's
revocations). OPEN / DATED RE-CHECKS unchanged.

## Forty-eighth session (2026-11-02): ranked list item 2, Lei 9.615/1998 (Lei Pelé), PUBLISHED as part zzzzd (31 versions)
Claim taken at the start ('gitlaw-BR-48 alan-dell 2026-11-02T07:53Z'), released at the end. Scratch: .gitlaw-scratch/brazil-b44
(before48/ = session-start copies (parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json, dupsame_allow.json,
effects_fix.py, README.md, jurisdiction.json, PUBLISH, firstline.py, pipe.sh, both PROGRESS.md, corpus.d/99-batch17zzzzc.json);
logs48/ (pipe1-3.out = the three pipe.sh runs); pids48.txt; new tools: setup48.py, rr48.py, bdiff48.py, finish48.py, idx48.py
(local Common Crawl path index + pins by URL substring, no request), chain48.py (follows a pre-2001 MP reissue chain through
iaonly's archive.org pinning), dec48.py (a part's decisions, version days, law days), multigrep48.py (a regex over several cached
law pages), st48.py (a unit's lines on a day)).
Requests: robots.txt of archive.org (200: Disallow /control/ /report/) and web.archive.org (404) read first (logs48/archive.org.txt,
web.archive.org.txt); then archive.org only, through the shared client (iaonly.py): `pages` (2 pins: l9615 = leis/l9615consol.htm
20261012184703, l9615-compilado = leis/l9615compilada.htm 20261019201546), `laws l9615` (15 new law pins), act-scoped `missing`
(0), `gap` ato:adc-133-2020-mpv984 and law:mp-2141-1-2001, chain48 2.141-2 (law:mp-2141-2-2001, -2141-3, -2193-4, -2193-5,
-2193-6). No LexML, no Common Crawl, no Arquivo.pt, no live Planalto, no challenge page.
### Survey (Lei 9.615 page, 931 notes over 29 laws)
- Lei 14.597/2023 does NOT revoke Lei 9.615: its art. 217 II, the clause that named it, is '(VETADO)' on its page (lgesp pin,
  batch10); the page has no Lei 14.597 note. The heavy amenders: Leis 9.981/2000, 10.672/2003, 12.395/2011, 13.155/2015,
  13.756/2018, 13.322/2016, 14.073/2020; MPs 2.141/2001, 502/2010, 671/2015, 718/2016, 841/2018, 846/2018, 984/2020, 229/2004,
  2.049-24/2000, 2.216-37/2001.
### 99-batch17zzzzd - PUBLISHED: Lei 9.615/1998 (lei-pele, LPele, 31 versions 1998-03-25 .. 2021-09-20)
- Config: PAGES l9615 / l9615-compilado; act lei-pele (2 digits); PARTS zzzzd; ACT_DAY_ALL lei-9615-1998 25.3.1998 (art. 95, in
  force on publication); ACT_LAWS_ALL lei-9615-1998 (ementa from the page; 24.3.1998, DOU 25.3.1998).
- Block '# part zzzzd' (only when the act runs):
  - MP fates: MP_PENDING mp-2141-2001 (chain read page by page: 2.141 DOU 24.3.2001 -> -1 23.4 -> -2 23.5 -> -3 22.6 'Revogada e
    Reeditada pela MPv nº 2.193-4' -> 2.193-4 29.6 -> -5 27.7 -> 2.193-6 24.8.2001, same words throughout (2.193-6 read in full),
    kept by EC 32 until Lei 10.672/2003 art. 5 revoked it); MP_PENDING mp-2049-2000 (edition 2.049-24, DOU 27.10.2000, art. 26 ->
    art. 59) and mp-2216-2001 (text for this act); CONVERTED_FIX mp-229-2004 -> lei-11118-2005 ('ded 2005'); MP_LAPSE
    mp-984-2020 restore 16.10.2020 (Ato Declaratório nº 133/2020, DOU 20.10.2020, read on its page). MP 841's lapse is batch 15's.
  - VIGENCIA_PROVISION: (lei-13756-2018, lei-pele, art-18-a) 11.6.2019 (Lei 13.756 art. 47 I, 180 days from DOU 13.12.2018,
    LC 95 art. 8 § 1º; batch 15's 13.12.2018 stays for its other changes); (lei-14117-2021, lei-pele, art-46-a) 30.4.2021 (art. 8
    vetoed, the veto overridden, promulgation DOU 30.4.2021 printed on Lei 14.117's page).
  - Lei 14.073/2020: LAW_FIELD_FIX published 15.10.2020 + VIGENCIA_FIXED (its footer reads 'DOU de 15.10 de 2020', which the reader
    could not take; it had fallen back to the enactment day 14.10).
  - TEXT_FIX: art. 46-A § 2º drops the link words 'Promulgação partes vetadas' at the line end.
  - _paragraphs_pele: lifts 'Revogado, a partir de 31/12/2001, pela Lei nº 9.981, de 2000' out of the bingo lines' text.
  - _pele_model (in an apply_span_fix wrapper, idempotent): (a) every struck line of arts. 59-81 with no end ends 31.12.2001 credited
    to Lei 9.981 (art. 2 read on its page: 'Ficam revogados, a partir de 31 de dezembro de 2001, os arts. 59 a 81'); 57 of its lines
    were left out before (undated); (b) art. 55-B caput in Lei 13.322/2016's own words ('... os arts. 49 a 55.') from 29.7.2016 (the annotated page
    prints only MP 718's caput); (c) art. 56 § 3º (Lei 12.395) moved before Lei 12.395's § 4º (ordercheck).
  - SPAN_FIX: art. 10 § 3º (VETADO) (notes with a missing ')': ends 13.12.2018 with the MP 841 gap); MP 841 art. 26 XI (read on its
    page: arts. 6 II-IV, VI, §§ 1-4; arts. 8-10 whole; art. 56 IV, VI, VIII, §§ 1-10): art. 8 parágrafo único gets the MP gap, the
    reprinted copies of art. 9 §§ 1-2 and art. 56 § 2º I-II / § 8º I-III are left out (duplicate) and their first copies end
    13.12.2018 with the gap; art. 6 (Planalto's 'Redação dada pela MP 841' on VI, §§ 2 and 3 read as MP 841's revocation, its own
    text): VI from 15.8.2015 (Lei 13.155), § 2º 1998 -> MP 502 (21.9.2010; its words printed with no note, found in MP 502's text)
    -> Lei 12.395 (17.3.2011), § 3º 1998 -> Lei 12.395, § 4º Lei 12.395's line, all to 13.12.2018 with the MP 841 gap, their
    reprints left out; notes of VI/§ 2º/§ 3º set to the real ones (the 'text before its law' check); art. 42 § 1º plain copy from
    16.10.2020 (MP 984's lapse; the twin rule did the same at build time, now explicit).
  - EXPLAINED (11 units): art-18/28/29 bare revoked labels on the compiled page; art-27/29/30 'no'/'nº' typesetting; art-31/46-a
    '§ 4º (VETADO)' and art-90-a/90-b '(VETADO)' the compiled page leaves out; art-84 the 1998 '2º O disposto' printed without '§'
    (kept as printed: no amending act's text or official record read; anchor 'art84§2'); art-92 'C.L.T.'/'C.L.T'.
  - OPEN_ITEMS: 'Vide' pointers; Lei 12.868's art. 18-A 'produz efeitos a partir do 6º mês' kept at its in-force day (deferred
    effect); earlier editions of the MP 2.049 chain not modelled.
- Undated struck lines still left out (established rule): art. 29 § 7º I-V '(revogado)' (Lei 12.395's placeholders, struck, no day).
- pipe.sh zzzzd (logs48/pipe3.out): ca2a7953 x2, 0 problems, 0 moves, 0 law records set; dupline 1 and overlap SAME 1 = art. 56
  'I - (revogado);' printed under both § 2º and § 8º (Lei 13.756's text); dupcheck, firstline, pubgap, ordercheck, missorig 0;
  leakcheck 32 = '(revogado)'/'(Revogado)' wordings the amending laws wrote (Leis 9.981, 10.672, 12.395, 13.756; listed in
  logs48/leak2.log); quotecheck 4 = quoted words in the law (art. 15 § 2º, art. 18-A); latecaput = 1998 lines under later capita
  (kept as law, or ended the same day: arts. 50, 52, 53, 55, 84, 88); uniqlaws 0, dupsame 0; merged 299 acts, 4108 versions, 2872
  commits, check 0/0, --compare identical, audit_push clean main + futuro. install.py -> corpus.d/99-batch17zzzzd.json d1a45399 +
  .PUBLISH (b44/publish-zzzzd.txt); docs.py b44/rows-zzzzd.json (README row; jurisdiction.json 299 acts 4108 versions, entry
  'Lei 9.615/1998 1998-2021 (31)').
- headyear (logs48/hy1.log vs b30/hy4.log): new BAD lines this session: law:lei-12876-2013 (the header's 'Vide Lei nº 12.876, de
  2013' links L12867.htm, Lei 12.867's page) and law:mp-39-2002 (its first heading is the Lei 9.615 it amends): both are 'Vide'
  pins only, credited nowhere; not added to bad_pins.json. Four other new BAD lines (dl-3725-1970, lei-3447-1957, lei-4123-1962,
  lei-6515-1970) are earlier sessions' CC 1916 pins, unchanged here.
- PIDs (all mine; foreground through run.py via rr48.py, listed in b44/pids48.txt: idx1 27708 ... bd11 47484, fb1 19448 (final
  merged build of the installed folder, logs48/fb1.log: 299 acts, 4108 versions, 2872 commits, check 0/0, 0 trailer errors,
  --compare identical, audit_push clean main + futuro), fbq 31272, fin1 28740 (handoff copies b44/*.after48.py, claim released);
  all exited): setup48 11920 through run.py directly; pipe.sh runs pipe1-3 in the background as tasks of mine (their run.py PIDs in
  logs48/pipe1-3.out), each waited on by its own notification; several rr48 runs waited on the cpu gate past the tool's 2-minute
  limit and finished as background tasks of mine. Outside the wrappers (no network): one bash sed/grep making the session-48 tool
  copies from the session-47 ones, one bash wc/grep of fetch_batch17.py, and one python reading stdin from a piped rr48 call
  (st56, by mistake); tool-written files (Write/Edit): parse_batch17.py, b44 tools/rows/publish files, this text, PROGRESS.md.

## State at handoff (batch 17, forty-eighth session, 2026-11-02)
PUBLISHED: zzzzd (Lei 9.615/1998 Lei Pelé, d1a45399, 31 versions 1998-2021). Installed: 299 acts, 4108 versions, 2872 commits, check
0/0, compare identical, audit clean main + futuro; uniqlaws 0, dupsame 0; README row + jurisdiction.json current. Files changed:
parse_batch17.py (+282 -0 vs b44/before48: PAGES l9615/l9615-compilado, act lei-pele, PARTS zzzzd, ACT_DAY/ACT_LAWS lei-9615-1998,
'# part zzzzd'), sources_batch17.json (+2 page pins, +15 law pins from `laws`, +7 gap/chain pins), corpus.d/99-batch17zzzzd.json +
.PUBLISH (new), repo/README.md (+1 row), repo/jurisdiction.json, PROGRESS.md, this file. effects_fix.py, law_records.json,
bad_pins.json, dupsame_allow.json, firstline.py, pipe.sh unchanged. Claim released.
TO DO (fresh ranked list, item 2 done): 3 Lei 10.931/2004 (patrimônio de afetação / CCB); 4 Lei 8.171/1991 (política agrícola);
5 Lei Complementar 97/1999 (Forças Armadas); 6 Lei Complementar 73/1993 (AGU); 7 Lei 5.250/1967 (Lei de Imprensa, ADPF 130); 8 Lei
7.170/1983 (LSN, revoked by Lei 14.197/2021); 9 Lei 6.194/1974 (DPVAT); 10 heavy tax: Leis 10.865/2004, 9.532/1997, 12.546/2011.
One act per part, survey first. OPEN / DATED RE-CHECKS unchanged.

## Forty-ninth session (2026-11-02): ranked list item 3, Lei 10.931/2004, PUBLISHED as part zzzze (23 versions incl. 1 futuro)
Claim taken at the start ('gitlaw-BR-49 alan-dell 2026-11-02T09:03Z'), released at the end. Scratch: .gitlaw-scratch/brazil-b44
(before49/ = session-start copies, as before48/; NOTE: bad_pins.json was edited a few seconds before setup49 ran, so before49/
bad_pins.json already holds the two new keys; the true session-start copy is before48/bad_pins.json, unchanged in session 48);
logs49/ (pipe1-4.out = the four pipe.sh runs, fb1.log = final build); pids49.txt; new tools: setup49.py, rr49.py, bdiff49.py,
finish49.py, txt49.py (a cached page as plain text, struck text [-...-], into txt49/), lawrec49.py (a law key's record in parts),
tl49.py (a unit's lines on every day it changes), vc49.py (per version: units changed and credits)).
Requests: robots.txt of archive.org (200: Disallow /control/ /report/) and web.archive.org (404) read first (robots49/); then
archive.org only, through the shared client (iaonly.py): `pages` (2 pins: l10931 = _ato2004-2006/2004/lei/l10.931.htm,
l10931-compilado = l10.931compilado.htm), `laws l10931` (22 linked, 5 new pins), act-scoped `missing` (0). No LexML, no Common
Crawl, no Arquivo.pt, no live Planalto, no challenge page.
### Session items
- bad_pins.json: + law:lei-12876-2013 (Lei 9.615's 'Vide Lei nº 12.876, de 2013' links Lei 12.867's page) and law:mp-39-2002
  (the page's first heading is Lei 9.615): 'Vide' pins only, credited nowhere; the pinning commands now skip both.
- Art. 84 § 2º of Lei Pelé ('2º O disposto'): left as printed (zzzzd unchanged).
### Survey (annotated page: 158 notes over 22 acts; compiled page 65)
Amenders: Leis 11.196/2005, 12.024/2009 (conv. MP 460), 12.350/2010 (conv. MP 497), 12.543/2011, 12.655/2012 (conv. MP 552),
12.767/2012, 12.844/2013, 13.097/2015 (conv. MP 656), 13.476/2017 (conv. MP 775), 13.970/2019, 13.986/2020 (conv. MP 897; Planalto
prints the MP 897 lines unstruck, the reader ends them at the conversion), 14.430/2022 (conv. MP 1.103), 14.620/2023, LC 214/2025
(art. 498: art. 3; art. 510 + art. 542 XXVI: arts. 4 and 8 from 2027). MP fates: all converted except MP 601/2012 (lapsed, Ato 36/2013).
### 99-batch17zzzze - PUBLISHED: Lei 10.931/2004 (lei-10931-de-2004, L10931, 23 versions 2004-08-03 .. 2026-01-01 + 2027-01-01 futuro)
- Config: PAGES l10931 / l10931-compilado; act (2 digits); PARTS zzzze; ACT_DAY_ALL lei-10931-2004 3.8.2004 (art. 66); ACT_LAWS_ALL
  lei-10931-2004 with the URL path the other parts' record has ('_Ato2004-2006/2004/Lei/L10.931.htm', uniqlaws).
- Block '# part zzzze' (only when the act runs): VIGENCIA_FIXED mp-601-2012 (28.12.2012) + VIGENCIA_PROVISION (mp-601, art-04/art-08)
  1.1.2013 (art. 7 II; set in the parser, not effects_fix: Lei 12.767's art. 4 § 7º the same day would keep MP 601 credited on
  art. 4); MP_LAPSE mp-601-2012 4.6.2013 (text word for word as part zj's: one shared law record); VIGENCIA_FIXED lei-12844-2013
  19.7.2013 (art. 49 I, 'efeitos retroativos a 4 de junho de 2013': publication day kept); VIGENCIA_FIXED mp-656-2014 8.10.2014
  (art. 55 III); NOTE_FIX 'Redação da pela MP 656'; TEXT_FIX art. 8 IV full stop (MP 601's own text); _l10931_2027 (apply_span_fix
  wrapper): LC 214 art. 510 rates (art. 4 caput 1,92%, §§ 6º/8º 0,47%, art. 8 caput 1,92%, parágrafo único 0,47%; each new line =
  today's line with the rate replaced, accepted only if found word for word, spaces aside, in art. 510's text: all 5 found) and
  art. 542 XXVI revocations (art. 4 II, IV; art. 8 I, II of caput and parágrafo único) from 1.1.2027 (futuro); EXPLAINED art-08
  (compiled page prints the 2027 parágrafo único), art-57 (quoted Lei 9.514 headings struck by Planalto with MP 1.103 / Lei 14.430
  notes); OPEN_ITEMS.
- effects_fix.py MOVES '99-batch17zzzze.json': lc-214-2025 2025-01-16 -> 2026-01-01 (art. 498 under art. 544 VI). (An MP 601 move
  was tried and dropped for the VIGENCIA_PROVISION above.)
- pipe.sh zzzze (logs49/pipe4.out): 11809d5e x2, 0 problems, 1 move; leakcheck, pubgap, ordercheck, missorig 0; dupline 23 /
  dupcheck 4 / quotecheck = quoted texts arts. 53-61 give other laws (law as printed); firstline = the rubricas printed before arts.
  53, 55, 58-61; overlap SAME 4 = Lei 12.024's art. 8 III/IV restored copies (one line per version, checked on 2010, 2013-01, 2013-06,
  2026); latecaput = lines under later capita; uniqlaws 0, dupsame 0; merged 300 acts, 4131 versions, 2877 commits, check 0/0,
  --compare identical, audit_push clean main + futuro. install.py -> corpus.d/99-batch17zzzze.json 168fbde6 + .PUBLISH
  (b44/publish-zzzze.txt); docs.py b44/rows-zzzze.json (README row; jurisdiction.json 300 acts 4131 versions, entry 'Lei
  10.931/2004 2004-2027 (23)'). Final merged build of the installed folder (logs49/fb1.log, PID 25244): 300/4131/2877, check 0/0,
  0 trailer errors, --compare identical, audit_push clean main + futuro.
- PIDs (all mine, all exited; listed in b44/pids49.txt): setup 47976 and a cat 32540 through run.py directly; rr49 runs idx1 11412,
  idx1b, rob1 9584, bd1-bd7, pg1 2736, nc1 2936, tx1 47108, lr1 26524, laws1 39144, miss1 37312, t1 50300, t2 48468, t3 14972, tl1,
  vc1-vc4, mg1 51516, pg1-pg12, st*, s4*, dec1-2, in1 41104, dk1 37144, fb1 25244; pipe.sh runs pipe1-4 as background tasks of mine
  (their run.py PIDs in logs49/pipe1-4.out), each waited on by its own notification. A first idx1 attempt failed before starting
  any child (logs49/ did not exist yet). Outside the wrappers (no network): a `mkdir -p` of robots49, `head`/`grep` filtering of
  two rr49 outputs and `> /dev/null` redirects, one `cat` of a task output, and two shell wait loops on task-output files (one
  stopped by me with TaskStop); tool-written files (Write/Edit): parse_batch17.py, effects_fix.py, bad_pins.json, b44 tools/rows/
  publish files, this text, PROGRESS.md.

## State at handoff (batch 17, forty-ninth session, 2026-11-02)
PUBLISHED: zzzze (Lei 10.931/2004, 168fbde6, 23 versions 2004-2027 incl. 1 futuro). Installed: 300 acts, 4131 versions, 2877
commits, check 0/0, compare identical, audit clean main + futuro; uniqlaws 0, dupsame 0; README row + jurisdiction.json current.
Files changed: parse_batch17.py (vs b44/before49: PAGES, act, PARTS, ACT_DAY/ACT_LAWS lei-10931-2004, '# part zzzze'),
effects_fix.py (+1 MOVES entry), bad_pins.json (+2 keys), sources_batch17.json (+2 page pins, +5 law pins), corpus.d/99-batch17zzzze
.json + .PUBLISH (new), repo/README.md (+1 row), repo/jurisdiction.json, PROGRESS.md, this file. law_records.json,
dupsame_allow.json, firstline.py, pipe.sh unchanged. Claim released.
TO DO (ranked list, items 2-3 done): 4 Lei 8.171/1991 (política agrícola); 5 Lei Complementar 97/1999 (Forças Armadas); 6 Lei
Complementar 73/1993 (AGU); 7 Lei 5.250/1967 (Lei de Imprensa, ADPF 130); 8 Lei 7.170/1983 (LSN, revoked by Lei 14.197/2021); 9 Lei
6.194/1974 (DPVAT); 10 heavy tax: Leis 10.865/2004, 9.532/1997, 12.546/2011. One act per part, survey first (none surveyed yet).
OPEN / DATED RE-CHECKS unchanged.

## Fiftieth session (2026-11-02): MP 601 lapse note re-PUBLISHED (zj, zzzze); ranked items 4, 5, 6, 8 PUBLISHED (zzzzf-zzzzi)
Claim taken at the start ('gitlaw-BR-50 alan-dell 2026-11-02T09:58Z'), released at the end. Scratch: .gitlaw-scratch/brazil-b44
(before50/ = session-start copies, taken before any edit: parse_batch17.py, sources_batch17.json, law_records.json, bad_pins.json,
dupsame_allow.json, effects_fix.py, README.md, jurisdiction.json, PUBLISH, firstline.py, pipe.sh, both PROGRESS.md, corpus.json and
every corpus.d file); logs50/ (pipe-zj1, pipe-zzzze1, pipe-f1, pipe-g1, pipe-h1, pipe-i1 .out = the pipe.sh runs; rb1 = merged build
with both new zj/zzzze; fb1 = merged build of the installed folder after their re-PUBLISH); pids50.txt; new tools: setup50.py,
rr50.py, bdiff50.py, finish50.py, lawscan50.py (a law key's record in every file that carries it), shared50.py (every shared law
record with a note, flagged when its own words name an act), sdiff50.py (the differing middle of two strings at JSON paths),
chain50.py (a pre-2001 MP reissue chain, Antigas/ or antigas_2001/, with a regex per edition), mkd50.py, mv50.py, app50.py.
bdiff50.py was run after every edit of parse_batch17.py (bd1-bd10); effects_fix.py is unchanged (+0 -0 every time).
Requests: robots.txt of archive.org (200: Disallow /control/ /report/) and web.archive.org (404) first (b44/robots50/); then
archive.org only, through the shared client (iaonly.py): `pages` l8171, lcp97, lcp97-compilado, lcp73, l5250, l7170, l6194 (7 page
pins); `laws l8171` (18 law pins) + act-scoped `missing` (1); `laws lcp97` (2), `missing` (0); `laws l7170` (0); chain50.py: MP
1.956-50 .. 1.956-57, 2.080-58 (2000), 2.080-59 .. 2.080-64, 2.166-65, 2.166-66 (2001) (17 pins; one miss: 2.080-59 asked under
Antigas/, then read under antigas_2001/). No LexML, no Common Crawl, no Arquivo.pt, no live Planalto, no challenge page.
### 1. Coordinator decision: MP 601 lapse note (re-PUBLISHED zj and zzzze)
- parse_batch17.py: both MP_LAPSE['mp-601-2012'] texts (zj block and zzzze block) now end "'; the wordings it gave end on
  4.6.2013" (was "the wordings it gave Lei 9.718 end on 4.6.2013"); a comment at each says why (one shared record, uniqlaws).
  Only zj and zzzze carry mp-601-2012-fim (lawscan50.py over corpus.json + every corpus.d part).
- Unit-level diff (jdiff.py / sdiff50.py, installed vs new): zj: every act, version and line identical; changes = the law record
  note mp-601-2012-fim, the MP-fate decision sentence that repeats it, and sources[0].notes's pin count ('163 pages' -> '292
  pages', the parser counts today's sources_batch17.json) with sources[0].requests 270 -> 563; zzzze: only the note and the
  decision sentence. pipe.sh: zj 4a367316 x2, 0 problems (each pipe's own uniqlaws showed 1 = the other part still old, as
  expected); zzzze 42fa4fe5 x2, 0 problems; with both new parts in place: uniqlaws 0 (uq1), dupsame 0, merged build 300 acts, 4131
  versions, 2877 commits, check 0/0, --compare identical, audit_push clean (rb1). reinstall.py: zj a9ae6753 -> 4d9f9f90, zzzze
  168fbde6 -> 9d842732; each .PUBLISH keeps its lines + a fiftieth-session line (b44/publish-zj50.txt, publish-zzzze50.txt).
  Merged build of the installed folder (fb1): 300/4131/2877, 0/0, identical, audit clean.
- Other shared law records with the same pattern (shared50.py, 31 shared records with notes; NOT edited, for the coordinator):
  * mp-703-2015-fim (99-batch5b Lei 12.846 Anticorrupção, 99-batch6 Lei 8.429 Improbidade): "the Lei 12.846 wording it had
    replaced or revoked is back from 30.5.2016" names Lei 12.846 in Lei 8.429's part too.
  * mp-75-2002-fim (99-batch17k Lei 9.430, 99-batch9 Código de Trânsito): "its wording of Código de Trânsito arts. 285 and 288
    stands until the rejection was published" names the CTB in Lei 9.430's part too.
  * borderline: mp-814-2017-fim (99-batch17zzr, zzw): "the provision it had revoked is back from 2.6.2018" (singular, names no
    act; true for each part only if each lost one provision).
### 99-batch17zzzzf - PUBLISHED: Lei 8.171/1991 (lei-da-politica-agricola, LPAgr, 25 versions 1991-01-18 .. 2026-09-30)
- Survey: annotated page l8171 (capture 20261024004938, no compiled page on Planalto: the page is its own check, as zzzg), 97
  notes over 23 acts: Leis 9.272/1996, 9.712/1998, 9.972/2000, 10.228/2001, 10.246/2001, 10.298/2001, 10.327/2001, 10.990/2004,
  11.718/2008, 11.775/2008 (conv. MP 432/2008), 12.058/2009, LC 137/2010, 12.805/2013, 13.158/2015, 13.901/2019 (conv. MP
  886/2019), 14.515/2022, 15.077/2024, 15.223/2025, 15.490/2026, 15.526/2026 (seguro rural; renames Cap. XV 'DO SEGURO RURAL',
  rewrites art. 56 and writes '§ 1º (Revogado).' itself), MP 1.956-49/2000.
- Config: PAGES l8171; act (3 digits); PARTS zzzzf; ACT_DAY_ALL lei-8171-1991 18.1.1991 (art. 107; 'rectified 12.3.1991');
  ACT_LAWS_ALL lei-8171-1991 (no other part has the record).
- Block '# part zzzzf': VIGENCIA_FIXED lei-9972-2000 24.8.2000 (art. 12, ninety days from DOU 26.5.2000, counted as Lei 9.966's);
  CONVERTED_FIX mp-432-2008 -> lei-11775-2008 ('Convertida na L ei'); MP_LAPSE mp-1956-2000 28.5.2000: MP 1.956-49 (DOU 28.4.2000)
  art. 7 revoked art. 99; its reissue 1.956-50 (26.5.2000, DOU 28.5.2000 edição extra, art. 5 in force on publication) and every
  later edition to 2.166-67 (read page by page, chain50: no '8.171' in any) drop the revocation; SPAN_FIX art. 99: the first
  (struck) copy left out as duplicate, the second (unstruck) copy = the 1991 lines with the gap 28.4.2000-28.5.2000 (mp-1956-2000 /
  mp-1956-2000-fim); paragraphs wrapper: art. 104 caput's 'com a nova redação dada pela Lei n° 7.803, de 1989.' kept as words of the
  article (the reader had taken it for a bare note, giving 1991 two versions credited to Lei 7.803); EXPLAINED art-099 (§ 1º
  (Vetado) unstruck twice on the page); OPEN_ITEMS (Vide pointers, rectification not printed).
- In-force days checked in every amender's own text (multigrep48): all on publication except Lei 9.972 (90 days), Lei 10.990 (no
  clause: 45 days, 28.1.2005), Lei 12.805 (180 days, 27.10.2013); Lei 12.058 arts. 47-48 and Lei 14.515 art. 51 stagger other
  articles only (Lei 14.515's art. 49 = Lei 8.171 art. 29-A, under III, on publication).
- pipe.sh zzzzf (logs50/pipe-f1.out): 26af8bee x2, 0 problems, 0 moves; dupline, dupcheck, firstline, pubgap, ordercheck,
  quotecheck, missorig 0; leakcheck 1 = art. 56 '§ 1º (Revogado).' as Lei 15.526 art. 2 writes it; latecaput = lines kept under a
  rewritten caput (arts. 5, 37, 59, 82); uniqlaws 0, dupsame 0, overlap 0; merged 301 acts, 4156 versions, 2896 commits, check 0/0,
  --compare identical, audit_push clean main + futuro. install.py -> corpus.d/99-batch17zzzzf.json e6dc2f15 + .PUBLISH
  (b44/publish-zzzzf.txt); docs.py b44/rows-zzzzf.json (README row; jurisdiction.json 301 acts 4156 versions). headyear: no new
  BAD line against session 48's list.
### 99-batch17zzzzg - PUBLISHED: Lei Complementar 97/1999 (lei-das-forcas-armadas, LCFA, 3 versions 1999-06-10, 2004-09-03, 2010-08-26)
- PAGES lcp97 / lcp97-compilado; amended only by LC 117/2004 (DOU 3.9.2004) and LC 136/2010 (DOU 26.8.2010), both in force on
  publication (read on their pages). Block '# part zzzzg': paragraphs wrapper lifts Planalto's '(ADI 6457)' markers (art. 1 caput,
  art. 15 caput, §§ 1º-3º) out of the lines (they had leaked into the text); EXPLAINED art-17-a (compiled page: 'Art. 17A.' and the
  revoked inciso IV kept as a line); OPEN_ITEMS: ADI 6457 changes no words; its judgment record was not read and is not modelled
  (FOR THE COORDINATOR: model it as a no-words court version, as stf-adi-4917, only with an official record of the judgment day).
- pipe.sh zzzzg (pipe-g1.out): 98bf4fc4 x2, 0 problems; all file checks 0 except quotecheck 2 ('Autoridade Marítima',
  'Autoridade Aeronáutica', quoted in the law) and latecaput (arts. 7, 12: kept under a rewritten caput); uniqlaws 0, dupsame 0;
  merged 302/4159/2899, 0/0, identical, audit clean. install.py 98bf4fc4; docs.py rows-zzzzg.json.
### 99-batch17zzzzh - PUBLISHED: Lei Complementar 73/1993 (lei-organica-da-agu, LOAGU, 1 version 1993-02-11)
- PAGES lcp73 (the older law:lc-73-1993 capture has no notes at all; the fresh page pin has only 'Vide' pointers): never amended
  on Planalto's page. OPEN_ITEMS lists the pointers (Leis 8.682/1993, 9.028/1995, 9.366/1996, 9.469/1997, Decreto 6.120/2007, ADI
  4.652 on art. 28 III). pipe.sh zzzzh (pipe-h1.out): ab61928a x2, 0 problems; all checks 0 except quotecheck 1 (art. 44's quoted
  title); merged 303/4160/2900, 0/0, identical, audit clean. install.py ab61928a; docs.py rows-zzzzh.json.
### 99-batch17zzzzi - Lei 7.170/1983 (lei-de-seguranca-nacional, LSN, 2 versions 1983-12-15, 2021-12-01)
- PAGES l7170: every line struck after the repeal, one note above the ementa ('Revogado pela Lei nº 14.197, de 2021'); never
  amended. Block '# part zzzzi': apply_span_fix wrapper ends every line with no end on 1.12.2021, credited to lei-14197-2021,
  'repealed' (Lei 14.197 art. 4 revokes it; art. 5: ninety days from DOU 2.9.2021; the Código Penal part has the same day);
  EXTRA decision; OPEN_ITEMS. The page prints 'Il -' / 'Ill -' for II / III in art. 1 (kept as printed).
- pipe.sh zzzzi (pipe-i1.out): 2b9bba61 x2, 0 problems; every file check, uniqlaws, dupsame, overlap, latecaput 0; merged 304 acts,
  4162 versions, 2901 commits, check 0/0, --compare identical, audit_push clean main + futuro. install.py -> corpus.d/99-batch17zzzzi
  .json 2b9bba61 + .PUBLISH (b44/publish-zzzzi.txt); docs.py rows-zzzzi.json (jurisdiction.json 304 acts 4162 versions). Final merged
  build of the installed folder: logs50/fb2.log.
### Surveyed, not started
- Item 7, Lei 5.250/1967 (Lei de Imprensa): page l5250 pinned (11 notes: Decretos-Leis 207/1967, 510/1969, Leis 6.071/1974,
  6.640/1979, 7.300/1985; header 'Vide ADPF nº 130'). The whole Lei was held not received by the 1988 Constitution in ADPF 130:
  model as a court law ending every line on the judgment day, which needs an official record of that judgment (not read; the
  page gives no date). Skipped this session for that reason.
- Item 9, Lei 6.194/1974 (DPVAT): page l6194 pinned (capture 20261014050243), 48 notes: Leis 8.441/1992, 11.482/2007, MP 451/2008
  (-> Lei 11.945/2009), and 'Revogado pela Lei Complementar nº 207, de 2024' above the ementa (every line struck). Model = the
  amendment history + a whole-act repeal as zzzzi; read LC 207's vigência and revocation clause first.
- Item 10 (Leis 10.865/2004, 9.532/1997, 12.546/2011): not surveyed.
- PIDs (all mine, all exited; listed in b44/pids50.txt): setup50 55116 through run.py directly; rr50 runs ls1 41860 ... tx10
  18620 (pids50.txt); pipe.sh runs zj, zzzze, zzzzf, zzzzg, zzzzh, zzzzi as background tasks of mine, each waited on by its own
  notification (their run.py PIDs: zj 41628 53424 13412 11492 54840 16624 48480; zzzze 42076 35656 39180 55036 11700 23904
  43760; zzzzf 17800 48644 27728 2148 44060 53852 6972; zzzzg 36868 25936 22748 14372 48844 26648 18916; zzzzh 39608 24512 36884
  43392 36536 49428; zzzzi in pipe-i1.out); rb1 18800 and fb1 46520 as background tasks of mine. Outside the wrappers (no network):
  the first bash reads (head/sed/grep/ls/wc/cat) of PROGRESS.md, batch17/PROGRESS.md, BRIEF.md and b44 tools before setup; one
  stray `python batch17/.tmp/run.py` from the lexifina root before setup (no such file, failed at once, ran nothing); a `cp` of
  the two installed .PUBLISH files into b44; `cat`/`tail`/`sed`/`grep`/`ls`/`date`/`wc` reads of my own logs, task outputs and
  page texts; one `sort`/`comm` of headyear BAD lines into /tmp; one `sleep 1`. A relative path in the first mkd50/robots.py runs
  made ~/Documents/robots50 and txt50 (run.py's cwd); mv50.py moved the two robots files into b44 and removed both
  directories. Tool-written files (Write/Edit): parse_batch17.py, b44 tools/rows/publish files, this text, PROGRESS.md.

## State at handoff (batch 17, fiftieth session, 2026-11-02)
PUBLISHED: zj and zzzze re-PUBLISH (MP 601 lapse note names no act; 4d9f9f90, 9d842732); zzzzf (Lei 8.171/1991, e6dc2f15, 25
versions), zzzzg (LC 97/1999, 98bf4fc4, 3), zzzzh (LC 73/1993, ab61928a, 1), zzzzi (Lei 7.170/1983, 2b9bba61, 2). Installed: 304 acts, 4162 versions, 2901
commits, check 0/0, compare identical, audit clean main + futuro (fb2); uniqlaws 0,
dupsame 0; README rows + jurisdiction.json current. Files changed: parse_batch17.py (vs b44/before50: PAGES l8171, lcp97,
lcp97-compilado, lcp73, l5250, l7170, l6194; acts, PARTS zzzzf-zzzzi, ACT_DAY/ACT_LAWS lei-8171-1991, lc-97-1999, lc-73-1993,
lei-7170-1983; the two MP 601 lapse texts; blocks '# part zzzzf' .. '# part zzzzi'), sources_batch17.json (+7 page pins, +21 law
pins, +17 chain pins), corpus.d/99-batch17zj.json, zzzze.json + .PUBLISH (re-PUBLISH), corpus.d/99-batch17zzzzf..zzzzi.json +
.PUBLISH (new), repo/README.md (+4 rows), repo/jurisdiction.json, PROGRESS.md, this file. effects_fix.py, law_records.json,
bad_pins.json, dupsame_allow.json, firstline.py, pipe.sh unchanged. Claim released.
TO DO (ranked list): 7 Lei 5.250/1967 (needs ADPF 130's official judgment record); 9 Lei 6.194/1974 (surveyed: amendments + whole-act
repeal by LC 207/2024); 10 heavy tax: Leis 10.865/2004, 9.532/1997, 12.546/2011. FOR THE COORDINATOR: mp-703-2015-fim and
mp-75-2002-fim name one act in a shared record (above); ADI 6457 (LC 97) not modelled. OPEN / DATED RE-CHECKS unchanged.

## Fifty-first session (2026-11-02): coordinator decisions 1-3; shared lapse records re-PUBLISHED (5b, 6, 9, 17k, zzr, zzw); Lei 5.250 PUBLISHED as zzzzj
Claim taken at the start ('gitlaw-BR-51 alan-dell 2026-11-02T11:08Z'), released at the end. Scratch: .gitlaw-scratch/brazil-b44
(before51/ = session-start copies (setup51.py, before any edit): parse_batch17.py, sources_batch17.json, law_records.json,
bad_pins.json, dupsame_allow.json, effects_fix.py, README.md, jurisdiction.json, PUBLISH, firstline.py, pipe.sh, both PROGRESS.md,
corpus.json and every corpus.d file. parse_batch5b.py and parse_batch9.py were NOT in that list and the folder is not tracked by
git (gitshow51.py wrote empty HEAD copies, since removed); before51/parse_batch5b.py and parse_batch9.py were rebuilt exactly by
reversing this session's two string edits (unedit51.py), and bdiff51.py diffs all four parsers); logs51/; pids51.txt; eff51/ (the
effects-fixed 5b/6/9 parts); stf51/ (ADPF 130 acórdão PDFs); txt51/ (amender page texts); new tools: setup51, rr51, bdiff51,
finish51, where51 (every JSON path holding a phrase), udiff51 (a unit in two versions), gitshow51, unedit51, ia51 (archive.org
cdx/get through the shared client, with a challenge-page detector), runbuild51 (runbuild.py accepting any 99-*.json candidate),
pipeb51.sh (pipe.sh's steps for an older batch part: two parses, effects_fix, file checks, uniqlaws, dupsame, cmppart),
pdfinfo51 (PDF whole? text layer? regex context; pypdf, no OCR), install51 (the six re-records), allow51.
bdiff51 after every parser edit (bd1-bd5): final parse_batch17.py +74 -2, effects_fix.py +0 -0, parse_batch5b.py +3 -2,
parse_batch9.py +2 -2.
Requests (archive.org only, through the shared client): robots.txt of archive.org (200: Disallow /control/ /report/) and
web.archive.org (404) first (robots51/); CDX of portal.stf.jus.br/robots.txt and redir.stf.jus.br/robots.txt, then the archived
robots.txt of portal.stf.jus.br (capture 20250630071240: 'User-agent: * / Disallow: /processos'; so no /processos page was read, not
even as an archive copy) and of redir (capture 20130824210100 turned out to be the Internet Archive's own robots file; redir's
captures are 404 in 2023, then redirects/403: no robots rule of its own; /paginadorpub is disallowed by neither); CDX of the ADPF 130
acórdão on redir (2: the first with an unencoded '&'), 2 PDF gets (20201028055344 is a capture cut at 1 MiB, unreadable;
20220119005617, 6.1 MB, whole, 334 pages with a text layer); `iaonly.py laws l5250` (5 linked, 4 pinned); CDX of leis/l6194.htm;
pinat.py l6194-2024 (capture 20240510043901). No LexML, no Common Crawl, no Arquivo.pt, no live STF or Planalto, no challenge page.
### 1. Coordinator decision 1: shared lapse records (re-PUBLISHED 99-batch5b, 99-batch6, 99-batch9, 99-batch17k, zzr, zzw)
- mp-703-2015-fim (parse_batch5b.py MP_LAPSE; parts 5b Lei 12.846 and 6 Lei 8.429): '... the wording it had replaced or revoked
  is back from 30.5.2016' (was 'the Lei 12.846 wording ...'). mp-75-2002-fim (parse_batch9.py MP_LAPSE; parts 9 Código de Trânsito
  and 17k Lei 9.430): '... its wordings stand until the rejection was published' (was 'its wording of Código de Trânsito arts. 285
  and 288 stands ...'). mp-814-2017-fim (parse_batch17 zzr and zzw blocks): it covers two provisions, a revoked one restored (Lei
  10.848 art. 31 § 1º, zzr) and a replaced wording restored (Lei 10.438 art. 13 § 1º-B '2018' -> '2017', zzw; so 'the provision it
  had revoked' was also wrong there): now '... the wording it had replaced or revoked is back from 2.6.2018'. A comment at each.
- Each part: two parses identical (5b a44492d4, 6 871e750a, 9 98d262c4, 17k f40509eb, zzr 1b7222b7, zzw 0b6b359a), 0 problems,
  effects_fix, file checks, dupsame 0; unit-level diff against the installed part (jdiff/sdiff50/cmppart): only the law note, the
  MP-fate decision sentence that repeats it, and sources[0] pin/request counts (5b 34->35, 6 41->45 and sources[1] 0->1, 9 338->339;
  17k/zzr/zzw also sources[0].notes' page count, as zj in session 50). Each pipe's own uniqlaws showed 1 (its partner still old);
  with all six new: uniqlaws 0 (uq-all), merged build 304/4162/2901, check 0/0, --compare identical, audit_push clean main + futuro
  (rb1). install51.py: 5b 46f3a30c->0144fb30, 6 4543d0a5->f681a845, 9 62b1d97b->7b04efa0, 17k 99a2442d->0e83439d, zzr
  d5a5b0ed->144a2571, zzw aaa39925->ebce006f; each .PUBLISH keeps its lines + one fifty-first-session line. uniqlaws over the
  installed folder 0 (uq-inst).
### 2. Coordinator decision 2: court rulings
- ADPF 130 (item 7): read on the STF's own record, the acórdão at redir.stf.jus.br/paginadorpub/paginador.jsp?docTP=AC&docID=605411
  (archive.org capture 20220119005617): 'Brasília, 30 de abril de 2009'; 'acordam os Ministros ... em julgar procedente a ação';
  ementa item 12: 'Total procedência da ADPF, para o efeito de declarar como não recepcionado pela Constituição de 1988 todo o
  conjunto de dispositivos da Lei federal nº 5.250'. Judgment day 30.4.2009 used (the corpus's STF rule and the 50th handoff's).
- LC 97 / ADI 6457: NOT modelled. Planalto's '(ADI 6457)' markers link only portal.stf.jus.br/processos/detalhe.asp?incidente=
  5934738, under the Disallowed /processos, and the acórdão's paginador docID is unknown (no blind CDX hunt). FOR THE COORDINATOR:
  an allowed record of ADI 6457's judgment (a redir paginador docID, or a portal page outside /processos) is needed to see whether
  it imposes a reading (interpretação conforme) or changes no words.
### 99-batch17zzzzj - PUBLISHED: Lei 5.250/1967 (lei-de-imprensa, LImp, 7 versions 1967-03-14 .. 2009-04-30)
- Config: act (page l5250, its own check; 2 digits); PARTS zzzzj; ACT_DAY_ALL lei-5250-1967 14.3.1967 (art. 77; DOU 10.2.1967,
  rectified 10.3.1967); ACT_LAWS_ALL lei-5250-1967 (no other part has the record).
- Block '# part zzzzj': P.COURTS stf-adpf-130 (kind court, 30.4.2009, url = the acórdão); B9.REPEALS lei-de-imprensa (30.4.2009,
  stf-adpf-130: every open line ends, the consolidated check is bypassed and REPEAL CHECK compares the last version with the page's
  unstruck text: 0 articles); a lifespans wrapper turns those ends' end_how 'act-repealed' into 'court'; SPAN_FIX art. 3 § 7º from
  13.4.1967, credited to Decreto-Lei 207/1967 (art. 1 moved art. 60 § 3º there 'com a mesma redação'; no in-force clause, 45 days
  from DOU 27.2.1967; Planalto prints § 7º with no note); a _write_part5 wrapper rewords LImp's REPEAL CHECK decision ('before the
  judgment', 'unstruck after the judgment'; batch 14 otherwise rewrites every such line to '(the repeal is in the future)');
  OPEN_ITEMS (the 2008-2009 medidas cautelares are not modelled).
- Amenders' in-force days read on their pages (txt51): DL 207/1967 none (45 days), DL 510/1969 art. 3 on publication (21.3.1969),
  Lei 6.071/1974 art. 13 (4.7.1974), Lei 6.640/1979 art. 2 (10.5.1979), Lei 7.300/1985 (28.3.1985).
- pipe.sh zzzzj (logs51/pipe-zzzzj1.out): a355fda9 x2, 0 problems, 0 moves; dupcheck, leakcheck, firstline, pubgap, ordercheck,
  quotecheck, missorig, latecaput 0; dupline 1 / overlap SAME 1 = art. 9 II a) and IV a), the same words in the law; dupsame 2 ->
  dupsame_allow.json + 2 entries (art. 9 a); art. 18 caput and § 2º share the penalty line), then 0 (ds1); uniqlaws 0; merged 305
  acts, 4169 versions, 2907 commits, check 0/0, --compare identical, audit_push clean main + futuro. install.py -> corpus.d/
  99-batch17zzzzj.json a355fda9 + .PUBLISH (b44/publish-zzzzj.txt); docs.py b44/rows-zzzzj.json (README row; jurisdiction.json 305
  acts 4169 versions). Final merged build of the installed folder (logs51/fb1.log): 305/4169/2907, 0/0, identical, audit clean.
- Noted, not changed (shared code): the STF source entry batch3 writes for any P.COURTS law reads 'case pages of ... (abaAndamentos)'
  with url portal.stf.jus.br/ (zzzq's ADI 5.809 has the same); for zzzzj the record actually read is the acórdão. Batch 14's
  '(the repeal is in the future)' rewrite also reaches other B9.REPEALS parts (e.g. the CPC 1973 part): check those lines.
### 3. Coordinator decision 3: item 9, Lei 6.194/1974 (DPVAT) - STARTED, not configured
- LC 207/2024 read on its cached page (law:lc-207-2024, batch 9's pin): art. 28 I 'Revogam-se: I - a Lei nº 6.194, de 19 de dezembro
  de 1974 (Lei do DPVAT)'; art. 29 'Esta Lei Complementar entra em vigor na data de sua publicação'; DOU 17.5.2024. So the whole-act
  repeal is on 17.5.2024, credited to lc-207-2024 (LC 207 was itself revoked by LC 211/2024: no repristination; say so in the
  decision). art. 15 keeps 6.194 for accidents before it (decision line, not modelled).
- The 2026 page strikes every line (old and current wordings alike), so read the act from the pre-repeal capture: pinned as page
  id l6194-2024 (pinat.py, leis/l6194.htm capture 20240510043901; NOT yet in PAGES). Model as CPC73 (B9.REPEALS with day 2024-05-17,
  law lc-207-2024, act page and consolidated = 'l6194-2024'). Next: PAGES 'l6194-2024', act (slug e.g. lei-do-dpvat), PARTS zzzzk,
  ACT_DAY (art. 13? read the closing clause: 'entrará em vigor na data de sua publicação', DOU 20.12.1974), ACT_LAWS, `iaonly.py
  laws l6194-2024` + missing, then a trial: the page has 10 '(Produção de efeitos)' notes (MP 451/2008 -> Lei 11.945/2009: read its
  effect clause) and 9 'Vide Medida nº 340, de 2006' (-> Lei 11.482/2007).
- PIDs (all mine, all exited): pids51.txt (setup51 46660 through run.py directly; every rr51 run with its PID; fb1 8472 + uq-f);
  pipes as background tasks of mine, each waited on by its own notification (their run.py PIDs in logs51/pipe-*.out). Outside the
  wrappers (no network): the first reads of PROGRESS.md (head), BRIEF.md, batch17/PROGRESS.md and the b44 tools/logs listing; reads
  of tool/script heads (cat/sed/grep/head/wc/ls) and of my own logs and page texts; `until ... sleep` waits on my own log files
  (one stopped by me with TaskStop); one stray `python -` with an empty heredoc (no input, exited at once). Tool-written files
  (Write/Edit): parse_batch17.py, parse_batch5b.py, parse_batch9.py, b44 tools/rows/publish files, this text, PROGRESS.md.

## State at handoff (batch 17, fifty-first session, 2026-11-02)
PUBLISHED: re-PUBLISH of 99-batch5b, 99-batch6, 99-batch9, 99-batch17k, zzr, zzw (shared lapse records name no single act or
provision); zzzzj (Lei 5.250/1967, a355fda9, 7 versions 1967-2009, ends on ADPF 130's judgment day). Installed: 305 acts, 4169
versions, 2907 commits, check 0/0, compare identical, audit clean main + futuro (fb1); uniqlaws 0, dupsame 0; README row +
jurisdiction.json current. Files changed: parse_batch17.py (act, PARTS zzzzj, ACT_DAY/ACT_LAWS lei-5250-1967, the two mp-814 texts,
block '# part zzzzj'), parse_batch5b.py (mp-703 text), parse_batch9.py (mp-75 text), sources_batch17.json (+4 law pins, +1 page pin
l6194-2024), dupsame_allow.json (+2), corpus.d (six re-recorded parts + .PUBLISH; 99-batch17zzzzj.json + .PUBLISH new),
repo/README.md (+1 row), repo/jurisdiction.json, PROGRESS.md, this file. effects_fix.py, law_records.json, bad_pins.json,
firstline.py, pipe.sh unchanged. Claim released.
TO DO: item 9 Lei 6.194/1974 (above: repeal 17.5.2024, page l6194-2024 pinned); 10 heavy tax: Leis 10.865/2004, 9.532/1997,
12.546/2011 (not surveyed). FOR THE COORDINATOR: ADI 6457 needs an allowed record (portal /processos is Disallowed); the shared STF
source template and batch 14's 'repeal is in the future' rewrite (above). OPEN / DATED RE-CHECKS unchanged.

## Fifty-second session (2026-11-02): coordinator decisions 1-3 (nine parts re-PUBLISHED); Lei 6.194 PUBLISHED as zzzzk
Claim taken at the start ('gitlaw-BR-52 alan-dell 2026-11-02T12:02Z', setup52.py through run.py), released at the end. Scratch:
.gitlaw-scratch/brazil-b44 (before52/ = session-start copies taken before any edit: sources_batch17.json, law_records.json,
bad_pins.json, dupsame_allow.json, effects_fix.py, parse.py, parse_phase2.py, lawrecords.py, dupfix.py, vigforms.py, titles.py,
README.md, jurisdiction.json, PUBLISH, firstline.py, pipe.sh, both PROGRESS.md, corpus.json, every corpus.d file, and EVERY batch
parser in before52/parsers/<batch>/parse_*.py (all 20: batch3-17, clt, codes, rju)); logs52/; pids52.txt; eff52/ (the installed
candidates); txt52/ (page texts); robots52/; new tools: setup52, rr52, bdiff52 (all 20 parsers + effects_fix/parse/parse_phase2),
g52 (grep), sl52 (line range), phr52 (JSON strings holding a phrase), stf52 (a part's STF source + court laws), req52 (every
requests.jsonl line matching a URL regex, hidden caches included), lawrec52, fdiff52, b3run52 (parse_batch3 with its output sent to
scratch: batch 3 writes corpus.d/90-batch3.json directly), same52.sh, pipeb52.sh, install52.py.
bdiff52 after every parser edit (bd1-bd5): final parse_batch3.py +41 -1, parse_batch14.py +5 -0, parse_batch17.py +93 -1; every
other parser and effects_fix.py unchanged.
Requests: robots.txt of archive.org (200: Disallow /control/ /report/) and web.archive.org (404) first (robots52/); then
archive.org only, through the shared client: `iaonly.py laws l6194-2024` (4 linked, 1 pinned: law:lei-8441-1992). No LexML, no
Common Crawl, no Arquivo.pt, no live STF or Planalto, no challenge page.
### 1. Decision 1: ADI 6457 (re-PUBLISHED zzzzg)
- '# part zzzzg' block: EXTRA + "Lei Complementar 97: the Supremo Tribunal Federal's judgment in ADI 6.457, to which Planalto's
  '(ADI 6457)' markers point, is not shown in the history, because its record could not be read." Unit diff vs installed: that one
  added decision (the list shifts by one) and sources[0]'s pin/request counts. pipe.sh zzzzg (logs52/pipe-g1.out): 5b6f4fb8 x2,
  file checks as in session 50, uniqlaws 0, dupsame 0, merged 305/4169/2907, 0/0, identical, audit clean.
- NOT changed, for the coordinator: the zzzzg open item still says the judgment 'changes no words', which nobody has read either.
### 2. Decision 2: the shared STF source entry (re-PUBLISHED zzzzj, zzzq, 99-batch8, 99-batch9)
- What each part citing 'case pages ... (abaAndamentos)' actually read (request logs, .cache/requests.jsonl, cc/ and stf/):
  * 99-batch17zzzzj (ADPF 130): the acórdão on redir.stf.jus.br/paginadorpub (archive.org capture). Allowed path.
  * 99-batch17zzzq (ADI 5.809 MC): the decision PDF www.stf.jus.br/arquivo/cms/.../ADI5809liminar.pdf (archive.org). Allowed
    (www.stf.jus.br/robots.txt answered 404 on 2026-10-31).
  * 99-batch9 (ADC 42): Informativo STF 892 on www.stf.jus.br (direct, 2026-10-31, after its robots.txt). Allowed.
  * 99-batch8 (ADI 3.964 MC, ADI 5.948 MC): the case summary www.stf.jus.br/portal/peticaoInicial/verPeticaoInicial.asp (capture
    20140718) and the ADI 5.948 MC decision PDF (direct). Allowed. BUT see the coordinator list below.
  * 90-batch3 (ADI 869, ADI 2.404) and 80-proc (ADI 2.797): STF case pages portal.stf.jus.br/processos/abaDecisoes/abaAndamentos,
    read live through fetch.get (parse_batch3.py comment; base PROGRESS.md line 44 'STF case pages work live'). Their description
    is accurate, but they were built from the Disallowed /processos path: NOT CHANGED, listed below.
- Fix at the template: parse_batch3.py STF_READ (court law key -> record description, url, url fragments for the request count)
  and _stf_read_requests (unique URLs in every .cache/**/requests.jsonl matching a fragment). A part's STF source entry names the
  records read only when EVERY ruling it carries is in STF_READ; otherwise the old template. Entries: stf-adi-3964, stf-adi-5948,
  stf-adc-42, stf-adi-5809, stf-adpf-130. Notes: 'Read for the day of each ruling and what it struck or suspended, in the record
  named.' 90-batch3 and 80-proc unchanged (b3run52 run twice: sources[2] identical to the installed part).
- Unit diffs (only sources[2] name/url/notes/requests, plus sources[0] pin counts for the batch17 parts): zzzzj 'acórdão of ADPF 130
  (Plenário, 30.4.2009)' (requests 0 -> 4); zzzq 'decision granting the medida cautelar in ADI 5.809 (18.12.2017)' (0 -> 2); 8 'case
  summary of ADI 3.964 (medida cautelar, Plenário, 12.12.2007); decision in ADI 5.948 (medida cautelar, 29.6.2018)', url
  www.stf.jus.br (requests 4, unchanged); 9 'Informativo STF 892, on ADC 42 with ADI 4.903 and 4.937 (judgment concluded
  28.2.2018)' (0 -> 1). pipeb52.sh 8 and 9: two parses identical (5d76e428, 33305bbd), file checks as before, uniqlaws 0, dupsame 0,
  cmppart: acts/laws/decisions/ai_use/applies equal, sources differ.
- FOR THE COORDINATOR (built from, or requested, robots-Disallowed STF paths; nothing changed):
  * 90-batch3 (stf-adi-869, stf-adi-2404) and 80-proc (stf-adi-2797): dates read live from portal.stf.jus.br/processos case pages.
  * 70-clt (stf-adi-1770, 5938, 5766; its own source entry, not the shared one): 3 live listarProcessos.asp + 3 abaAndamentos.asp
    (clt/PROGRESS.md line 56; parse_clt.py line 1735).
  * base corpus.json (stf-adi-7047, incidente 6318731; parse.py 'Supremo Tribunal Federal, case pages').
  * 99-batch10 and 99-batch17zzn (stf-adi-4917, incidente 4379376): an archive.org copy of portal.stf.jus.br/processos/
    abaAndamentos.asp?incidente=4379376 (capture 20260831225339) was fetched 2026-10-31 (.cache/cc/requests.jsonl); check whether
    the ruling's dates came from it.
  * 99-batch8: built from allowed records, but on 2026-10-31 one live request to portal.stf.jus.br/processos/listarProcessos.asp
    (ADI 3964) was made 2 s after reading its robots.txt (batch8/PROGRESS.md: 'deleted from the cache unused'), and an Arquivo.pt
    copy of /processos/detalhe.asp?incidente=2560579 (capture 20210302214935) was fetched; its law url stf-adi-3964 still points
    to /processos/detalhe.asp.
### 3. Decision 3: batch 14's repeal-check rewrite (re-PUBLISHED r, zx, zzzr, zzzza)
- parse_batch14.py _inner: the '(the repeal is in the future)' rewrite now applies only to REPEAL_CHECK lines of acts whose
  B9.REPEALS day is after 2026-10-31 (the same test as batch 14's consolidated()), matched by the line's 'short:' prefix; an act
  repealed in the past keeps batch 9's 'the unstruck text of the pre-repeal capture of Planalto's page'. zzzzj's wrapper comment
  updated (it rewrote its own line first; its output unchanged).
- Lines that change: LPreg (r), LAgro (zx), L12990 (zzzr), CPC73 (zzzza): each read from a pre-repeal capture (10.12.2023,
  18.12.2023, 31.5.2025, 27/29.10.2015). 99-batch14a (LC 87, LC 116, repealed 1.1.2033) keeps '(the repeal is in the future)'
  (same52.sh: both lines identical; the raw 14a run differs from the installed file elsewhere, from later installed-file
  post-processing, untouched). Unit diffs: only that decision line + sources[0] pin/request counts (r 130->535, zx 305->531,
  zzzr 473->530, zzzza 632->657). pipe.sh r 094bfbed, zx 218b00d7, zzzr fca332e8, zzzza 9b399b3b, zzzq b9043757: two parses each
  identical, 0 problems, uniqlaws 0, dupsame 0.
- NOT changed, for the coordinator: zzzza decisions[19] reads 'against the unstruck text of the unstruck text of Planalto's page of
  the act (Planalto publishes no separate consolidated page for it) as captured on 29.10.2015' (batch 5's blanket rewrite of
  "Planalto's consolidated page" hits _W_CPC73_REPEALX; the CPC73 check is against the compiled page l5869compilada-2015).
- All nine together (eff52/): uniqlaws 0 (uq-all); merged build (rb1) 305 acts, 4169 versions, 2907 commits, check 0/0, --compare
  identical, audit_push clean main + futuro. install52.py: zzzzg 98bf4fc4->5b6f4fb8, zzzzj a355fda9->d6656e0e, zzzq
  61c7800f->b9043757, 8 92ee2e09->a0ebeb24, 9 7b04efa0->98c047df, r 30a57851->094bfbed, zx 2597bf51->218b00d7, zzzr
  18b5ecdc->fca332e8, zzzza 94744386->9b399b3b; each .PUBLISH keeps its lines + one fifty-second-session line. uniqlaws installed 0.
- Mistake: pipe zzzzj and pipe r ran at the same time and their merged-build steps collided in brazil-b17-src/-build/-c
  (zzzzj's crashed, r's printed nothing). From then on one pipe at a time; the rb1 build covers both parts.
### 99-batch17zzzzk - PUBLISHED: Lei 6.194/1974 (lei-do-dpvat, LDPVAT, 6 versions 1974-12-20 .. 2024-05-17)
- Config: PAGES l6194-2024 (capture 20240510043901, before the repeal); act (l6194-2024 page and check, 2 digits); PARTS zzzzk;
  ACT_DAY_ALL lei-6194-1974 20.12.1974 (art. 13, DOU 20.12.1974, rectified 31.12.1974); ACT_LAWS_ALL lei-6194-1974 (url = PAGES
  l6194). Block '# part zzzzk': EXTRA_LAWS lc-207-2024 (copied from the installed record, uniqlaws 0); B9.REPEALS 17.5.2024,
  lc-207-2024 (LC 207 art. 28 I, art. 29 in force on publication, DOU 17.5.2024; art. 15 keeps the Lei for accidents before;
  LC 211/2024 art. 4, DOU 31.12.2024, revokes LC 207 with no repristination clause: all read on their cached pages); a paragraphs
  wrapper reads art. 4's 'Parágrafo único. (Revogado pela Lei nº 8.441, de 1992).' as text (Lei 11.482 art. 8 prints it so; the
  reader had taken the parenthesis for a note, leaving a bare label and a REPEAL CHECK difference of 1); EXTRA decision on dating
  (Lei 11.945 art. 33 IV a) gives arts. 30-32 effect from 16.12.2008: retroactive, so kept on publication 5.6.2009, the corpus
  rule; MP 451 art. 22 IV from publication, DOU 16.12.2008, rectified 22.12.2008; Lei 11.482 art. 24 III from publication
  31.5.2007; Lei 8.441 art. 2 on publication 14.7.1992); OPEN_ITEMS (Anexo not included; 'Vide Medida nº 340, de 2006' pointers
  not modelled; MP 451's art. 3 § 1º II reads 'na alínea “a”' on the Lei's page but 'no inciso anterior' on the MP's own page).
- pipe.sh zzzzk (logs52/pipe-k2.out): ee86dc56 x2, 0 problems, 0 moves; dupline, dupcheck, firstline, pubgap, missorig, overlap 0;
  leakcheck 6 + ordercheck 1 = Lei 11.482 art. 8's own '(revogada)'/'(Revogado)' lines in its order; quotecheck = DL 73 quotes in
  arts. 1-2 and the MP 451 line above; latecaput = art. 7 §§ 1º-2º under Lei 8.441's caput; REPEAL CHECK 0 articles; uniqlaws 0;
  dupsame 0; merged 306 acts, 4175 versions, 2909 commits, check 0/0, --compare identical, audit_push clean main + futuro.
  install.py -> corpus.d/99-batch17zzzzk.json 95a0257a + .PUBLISH (b44/publish-zzzzk.txt); docs.py b44/rows-zzzzk.json (README
  row; jurisdiction.json 306 acts 4175 versions). Final merged build of the installed folder (logs52/fb1.log): 306/4175/2909, 0/0,
  identical, audit clean; uniqlaws installed 0.
- PIDs (all mine, all exited): pids52.txt (setup52 4092 through run.py directly; every rr52 run with its PID; same52.sh,
  pipeb52.sh and pipe.sh runs with their run.py PIDs in logs52/*.out; background tasks of mine, each waited on by its own
  notification; one `until ... sleep` waiter of mine stopped with TaskStop). Outside the wrappers (no network): the first reads
  (head/sed/grep/ls/wc/cat) of PROGRESS.md, batch17/PROGRESS.md, BRIEF.md, ACTIVE.txt, the claims folder listing, b44 tools,
  run.py and pipe.sh before setup; cat/grep/tail/head of my own logs, task outputs and tool/script heads (batch3, batch14, fetch,
  iaonly, docs.py); one `tail` of the cpu log; find/ls listings; `cp` of candidate parts into eff52; tool files written by cat
  heredocs and two sed -e/-i on my own tools; ONE direct `python -` heredoc (not through run.py) that made three string edits to
  parse_batch17.py (PAGES l6194-2024, the act, PARTS zzzzk; asserted, LF kept). Tool-written files (Write/Edit): parse_batch3.py,
  parse_batch14.py, parse_batch17.py, this text, PROGRESS.md.

## State at handoff (batch 17, fifty-second session, 2026-11-02)
PUBLISHED: re-PUBLISH of zzzzg (ADI 6457 decision line), zzzzj, zzzq, 99-batch8, 99-batch9 (STF source names the record read), r,
zx, zzzr, zzzza (repeal-check line names the pre-repeal capture); zzzzk (Lei 6.194/1974, 95a0257a, 6 versions 1974-2024).
Installed: 306 acts, 4175 versions, 2909 commits, check 0/0, compare identical, audit clean main + futuro (fb1); uniqlaws 0,
dupsame 0; README row + jurisdiction.json current. Files changed: parse_batch3.py (STF_READ), parse_batch14.py (rewrite test),
parse_batch17.py (zzzzg decision, zzzzj comment, PAGES l6194-2024, act, PARTS zzzzk, ACT_DAY/ACT_LAWS lei-6194-1974, block
'# part zzzzk'), sources_batch17.json (+1 law pin via iaonly: lei-8441-1992), corpus.d (nine re-recorded parts + .PUBLISH;
99-batch17zzzzk.json + .PUBLISH new), repo/README.md (+1 row), repo/jurisdiction.json, PROGRESS.md, this file. effects_fix.py,
law_records.json, bad_pins.json, dupsame_allow.json, firstline.py, pipe.sh unchanged. Claim released.
TO DO: item 10 heavy tax: Leis 10.865/2004, 9.532/1997, 12.546/2011 (not surveyed; one act per part, survey first). FOR THE
COORDINATOR: the Disallowed-path list in decision 2 above; zzzzg's open item 'changes no words' (unread); zzzza's doubled
'the unstruck text of the unstruck text' (batch 5 rewrite). OPEN / DATED RE-CHECKS unchanged.

## Fifty-third session (2026-11-02): coordinator decisions 2-4 (zzzzg, zzzza, zzzzk re-PUBLISHED); item 10 surveyed, pages pinned
Claim taken at the start ('gitlaw-BR-53 alan-dell 2026-11-02T13:04Z', setup53.py through run.py, PID 11412), released at the end.
Scratch: .gitlaw-scratch/brazil-b44 (before53/ = session-start copies of the same set as before52/: every batch parser (20) in
before53/parsers, effects_fix/parse/parse_phase2/lawrecords/dupfix/vigforms/titles, sources_batch17.json, law_records.json,
bad_pins.json, dupsame_allow.json, README.md, jurisdiction.json, PUBLISH, firstline.py, pipe.sh, both PROGRESS.md, corpus.json and
every corpus.d file); logs53/ (pipe-g1, pipe-a1, pipe-k1 .out = the pipe.sh runs; rb1 = merged build of the three candidates;
fb1 = final build); pids53.txt; eff53/ (installed candidates); txt53/ (page texts of the six item-10 pages); robots53/; edits53/
(mk1.py + spec-*.json: every parser edit, applied by ed53.py through run.py); new tools: setup53, rr53, ed53 (exact-string edit,
each old string must occur once, LF kept, atomic), bdiff53, g53, sl53, phr53, pdiff53 (leaf-level diff of two part files),
idx53, txt53, survey53 (note counts per amending law), robots53, kchk53, install53, finish53.
NOTE for rr53 users: it turns any argument naming a file/dir in its cwd into an absolute path; b44 holds a `pages` folder, so
`iaonly.py pages` must be run from another cwd (the first try, pg1, printed the usage and fetched nothing, rc 2).
bdiff53 after every parser edit (bd1-bd3): final parse_batch5.py +6 -3, parse_batch17.py +36 -7; every other parser and
effects_fix.py unchanged.
Requests: robots.txt of archive.org (200: Disallow /control/ /report/) and web.archive.org (404) first (robots53/); then
archive.org only, through the shared client: `iaonly.py pages` (6 pins: l10865, l10865-compilado, l9532, l9532-compilado,
l12546, l12546-compilado; 0 Common Crawl, 0 Arquivo.pt). No LexML, no Common Crawl, no Arquivo.pt, no STF (no /processos, live or
archived), no live Planalto, no challenge page.
### 1. Decision 1 (/processos parts): nothing touched (90-batch3, 80-proc, 70-clt, base, 99-batch10/zzn, 99-batch8 unchanged).
### 2. Decision 2: LC 97 open item (re-PUBLISHED zzzzg)
- B13.OPEN_ITEMS[_LC97]: '... point to the Supremo Tribunal Federal's judgment in that case, whose effect on the text could not
  be read (its record was not read); the markers are left out of the text and the judgment is not modelled'. pipe.sh zzzzg
  (pipe-g1): f620fac6 x2, checks as in session 52 (quotecheck = arts. 17/18 parágrafo único quotes, law text), uniqlaws 0,
  dupsame 0, merged 306/4175/2909, 0/0, identical, audit clean. Unit diff: decisions[13] (that line) + sources[0] pin/request
  counts only.
### 3. Decision 3: CPC 1973's doubled phrase (re-PUBLISHED zzzza)
- Source: parse_batch5.py's blanket rewrite of "Planalto's consolidated page" now skips the phrase when it already reads 'the
  unstruck text of Planalto's consolidated page' (regex lookbehind; the result for every other line is byte-identical to
  str.replace). Before the fix only zzzza held 'the unstruck text of the unstruck text' (phr53 over every installed part).
  The check page really is the consolidated page (act config: check = l5869compilada-2015, capture 20151029045434), so the
  rewrite's '(Planalto publishes no separate consolidated page for it)' was also wrong for this line; the stale comment at
  the head of the zzzza block ('the check is the annotated page itself') corrected (comment only).
- zzzza decisions[19] now: '... (the last version before the repeal against the unstruck text of Planalto's consolidated page
  as captured on 29.10.2015): every remaining difference explained: ...'. pipe.sh zzzza (pipe-a1): 711f41d2 x2, 0 problems,
  checks as before (quotecheck = the Code's own quoted words), uniqlaws 0, dupsame 0 (1 allowlisted, as before), merged 0/0,
  identical, audit clean. Unit diff: decisions[19] + sources[0] pin/request counts only.
### 4. Decision 4: MP 451 lines in Lei 6.194 (re-PUBLISHED zzzzk; open item closed)
- Comparing the MP's own page (txt52/mp-451-2008.txt, art. 20) with the Lei's struck MP lines (l6194-2024) found TWO lines that
  differ, not one: § 1º caput ('de que trata o inciso II, deverão' on the Lei's page, 'de que trata o inciso II do caput,
  deverão' on the MP's) and inciso II ('na forma prevista na alínea “a”' / 'na forma prevista no inciso anterior'). Art. 3
  caput, inciso I, § 2º, art. 5 § 5º and art. 12 §§ 3º-4º are the same on both. Under the decision (the MP's own text governs)
  both lines follow the MP's page.
- Block '# part zzzzk': _MP451_LINES (two exact substitutions in non-plain art-03 lines of l6194-2024; asserted both used);
  decision _W6194_MP451 names both differences and the DOU rectification of 22.12.2008; the MP 451 sentence of the open item
  removed. pipe.sh zzzzk (pipe-k1): 79c343ef x2, 0 problems; quotecheck now only the DL 73 quotes of arts. 1-2 (the MP 451
  flag is gone); leakcheck 6 + ordercheck 1 = Lei 11.482 art. 8's own '(revogada)' lines, as before; REPEAL CHECK 0; uniqlaws
  0; dupsame 0; merged 0/0, identical, audit clean. Unit diff: versions[3] art-03 text (kchk53: the old text with exactly
  the two substitutions equals the new; 6 versions as before), one added decision, the open item shortened, sources[0] pin
  counts (270 -> 276 pages: the six item-10 pins).
### Install
- rb1 (the three candidates together): 306 acts, 4175 versions, 2909 commits, check 0/0, --compare identical, audit_push clean
  main + futuro; uniqlaws 0. install53.py: zzzzg 5b6f4fb8->f620fac6, zzzza 9b399b3b->821ad0bb, zzzzk 95a0257a->35932b70; each
  .PUBLISH keeps its lines + one fifty-third-session line. dupsame on the installed three 0. README rows and jurisdiction.json
  unchanged (counts and row texts unaffected). Final build of the installed folder (fb1): 306 acts, 4175 versions, 2909 commits, check 0/0, --compare identical, audit_push clean main + futuro; uniqlaws installed 0.
### 5. Item 10 survey (pages pinned and read; NOTHING configured beyond PAGES; no act, no part)
- Pins (sources_batch17.json): l10865 (_ato2004-2006/2004/lei/l10.865.htm 20261024003616), l10865-compilado, l9532
  (leis/l9532.htm 20261022022230), l9532-compilado, l12546 (_ato2011-2014/2011/lei/l12546.htm 20261016051155), l12546-compilado
  (20261012170119). PAGES entries added in parse_batch17.py (fifty-third session comment). Texts in b44/txt53.
- Lei 9.532/1997 (smallest; suggested first): 151 notes over 35 acts (Leis 9.779/1999 20, 9.959/2000 11, 12.973/2014 12,
  14.754/2023 8, 12.868/2013 7, 12.402/2011 6, 10.887/2004 6, 10.637/2002 4; MP reissue chains 2.158-35 (8, two spellings),
  2.189-49 (8), 2.199-14 (16); MPs 449/2008 7, 1.184/2023 8, 1.303/2025 1 ('vigência encerrada'), 71/2000; LC 214/2025 2, LC
  187/2021). Art. 81: in force on publication (DOU 11.12.1997), effects from then for arts. 9, 37-42, 44-54, 64-68, 74 and 75,
  from 1.1.1998 for the rest: a split first version. Art. 80 keeps acts under MP 1.602/1997 (its origin). Court markers:
  'ADIN Nº 1802' on arts. 12-14 (immunity of education/assistance bodies) and 'ADI 1.758-4, DE 1998' near art. 28: their STF
  records sit under /processos; read only an allowed record (redir.stf.jus.br acórdão, Informativo) or state them as not
  modelled (as LC 97/ADI 6457).
- Lei 10.865/2004 (PIS/COFINS-Importação, conv. MP 164/2004): 511 notes over 69 acts; heavy: Leis 11.727/2008 38,
  12.649/2012 35, 13.137/2015 30, 12.859/2013 23, 14.183/2021 19, 12.715/2012 15, 13.670/2018 15, 10.925/2004 13, LC 214/2025
  35 (2027+ effects, futuro), LC 228/2026 3; MPs 549/2011 24, 668/2015 23, 1.034/2021 19, 1.095/2021 11, 563, 564, 836, 413,
  1.157, 1.202 (partly lapsed/revoked: check each fate), 774 and 794/2017 (774 revoked by 794, which lapsed). 95 'Produção de
  efeito' and 146 'Vigência' markers: many deferred effect days. Art. 53: in force on publication (DOU 30.4.2004), effects from
  1.5.2004 save the articles before.
- Lei 12.546/2011 (Reintegra, desoneração da folha; conv. MP 540/2011): 3,229 notes over 35 acts, nearly all 'Incluído' notes
  in the NCM code lists of arts. 7-8 and the Anexo (Lei 12.715/2012 1,741, Lei 12.794/2013 732, Lei 12.844/2013 205, MP
  612/2013 84 (lapsed), MPs 774 63 / 794 58, Lei 13.670/2018 65, Lei 14.195/2021 49, MP 1.040/2021 47); 16,249 page lines. Art.
  52: in force on publication, arts. 1-3 after regulation, arts. 7-9 and 14-21 from the first day of the fourth month after MP
  540's publication (2.8.2011: 1.12.2011). '(Vide ADI 7633)' and 'Vide Medida Provisória 1.208/2024' on arts. 7-8 (the 2024
  dispute): ADI 7633's record is under /processos too. 65 VETADO lines. Heaviest of the three; decide whether the NCM lists are
  in scope before starting.
- PIDs (all mine, all exited): pids53.txt (setup53 11412 through run.py directly; every rr53 run with its PID); pipe.sh runs
  zzzzg, zzzza, zzzzk as background tasks of mine, one at a time, each waited on by its own notification (their run.py PIDs in
  logs53/pipe-*.out); my own Monitor waiters stopped with TaskStop by task id. Outside the wrappers (no network): the first
  reads (head/sed/grep/ls/wc/cat) of PROGRESS.md, batch17/PROGRESS.md, BRIEF.md, the claims folder listing, b44 tools, run.py,
  pipe.sh, fetch_batch5.py's main and iaonly.py before and just after setup; cat/tail/head/grep of my own logs and task
  outputs; tool files written by sed (52 -> 53 copies) and cat heredocs; mkdir of logs53/edits53/eff53/robots53. Files written
  with the Write tool: my own tools/specs in b44 (mk1.py, install53.py, this text). Every parser edit went through ed53.py under
  run.py.

## State at handoff (batch 17, fifty-third session, 2026-11-02)
PUBLISHED: re-PUBLISH of zzzzg (LC 97 open item: ADI 6457's effect 'could not be read'), zzzza (CPC 1973 pre-repeal check line:
'the unstruck text of Planalto's consolidated page as captured on 29.10.2015'), zzzzk (MP 451's art. 3 § 1º caput and II from
the MP's own page; decision line; open item closed). Installed: 306 acts, 4175 versions, 2909 commits, check 0/0, compare
identical, audit clean main + futuro (fb1); uniqlaws 0, dupsame 0; README rows + jurisdiction.json current. Files changed:
parse_batch5.py (rewrite lookbehind), parse_batch17.py (zzzzg open item, zzzza comment, zzzzk block, PAGES for item 10),
sources_batch17.json (+6 page pins), corpus.d (three re-recorded parts + .PUBLISH lines), PROGRESS.md, this file.
effects_fix.py, law_records.json, bad_pins.json, dupsame_allow.json, firstline.py, pipe.sh, README.md, jurisdiction.json
unchanged. Claim released.
TO DO: item 10, one act per part, surveyed above: Lei 9.532/1997 first (split art. 81 effects; ADI 1.802 / 1.758 from
allowed records only or a 'not modelled' decision), then Lei 10.865/2004, then Lei 12.546/2011 (scope of the NCM lists).
FOR THE COORDINATOR: decision 1's /processos list unchanged (with the user). OPEN / DATED RE-CHECKS unchanged.
