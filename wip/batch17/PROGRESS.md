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

## State at handoff (batch 17, second session, 2026-10-31)
Parts 99-batch17a..g installed with .PUBLISH (21 acts, 135 versions; merged 147 acts, 2529 versions, 2025 commits, check
0/0, --compare identical, audit clean). README rows + jurisdiction.json (147 acts) current. effects_fix.py MOVES for
99-batch17a and 99-batch17g. Fresh parses of b, e, f after this session's edits equal the installed parts except
sources[0].requests (b, e; known). No background processes left running (every run foreground through .tmp/run.py; all
PIDs exited). Robots note: portal.stf.jus.br/robots.txt now Disallows /processos (one redirect lookup for ADI 2.527 was
made before reading it); read no STF case pages.

## Part h - configured, NOT published (Lei 7.689/1988 CSLL, Lei 9.249/1995)
PAGES for all five tax laws pinned (l7689, l9249, l9250 + compilado, l7713 + compilada, l9430 + compilada; `pages` done).
Acts, ACT_DAY, ACT_LAWS and PARTS["h"] are in parse_batch17.py; `laws` + `missing` fetched for h. Judgement call taken
in config: Lei 9.249's first version dated 1.1.1996 (art. 35: in force on publication 27.12.1995, 'produzindo efeitos a
partir de 1º de janeiro de 1996'); revisit if the coordinator prefers the in-force day. Trial h-t1: 0 consolidated diffs,
but 8 problems and a crash (KeyError mp-1034-2021 in mp_notes):
- VIGENCIA_FIXED needed: mp-675-2015 ('a partir do primeiro dia do quarto mês subsequente ao de sua publicação': DOU
  22.5.2015 -> 1.9.2015; converted into Lei 13.169/2015); mp-1034-2021 (I art. 2 on publication; II others from the 1st day
  of the 4th month after the DOU of 1.3.2021 -> 1.7.2021; read which article touches Lei 7.689; conversion Lei 14.183/2021).
- MP_LAPSE mp-694-2015 (Lei 9.249): pin its Ato Declaratório of lapse (see how ato:adc-* pins were made in
  sources_batch17.json / batch16 gaps) and read the day.
- Then effect days: many amenders carry 'produção de efeitos' clauses (Lei 12.973/2014, 13.169/2015, 14.183/2021,
  14.446/2022, 11.727/2008, MP 413/2008, LC 224/2025, LC 225/2026, Lei 15.270/2025, 15.525/2026; MP 1.303/2025 lapsed):
  read each and add MOVES "99-batch17h.json" in effects_fix.py where a later fixed day applies.
- Lei 9.250, 7.713, 9.430 not configured yet (9.430: 547 notes, 608 struck runs; 7.713: 328/314; 9.250: 293/192).
Leis 13.465/2017 and 11.977/2009 (+compilado) not started (pages in the CC index).

## Next candidates (pages in the Common Crawl index)
Lei 13.675/2018, Lei 9.537/1997, Lei 6.634/1979, Lei 9.469/1997 (+compilado), Lei 4.728/1965 (+compilado);
heavy tax laws Lei 7.713/1988 (+compilada), 9.430/1996 (+compilada), 9.249/1995, 9.250/1995, 7.689/1988; Lei 13.465/2017,
Lei 11.977/2009. Lei 10.931/2004: no page in the index.
