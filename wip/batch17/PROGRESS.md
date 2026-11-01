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
