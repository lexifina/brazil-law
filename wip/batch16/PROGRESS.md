# Brazil batch 16 progress (gitlaw-BR agent, 2026-10-31)

Owns `scripts/brazil-law/batch16/` and `corpus.d/99-batch16<x>.json` (+ `.PUBLISH`), one small part per 1-4 acts. Never
commits or pushes. Scratch outside the repo: `~/Documents/.gitlaw-scratch/brazil-b16` (trial parts, `eff/` =
parts after effects_fix), merged build `brazil-b16-src` / `-build` / `-c`.

## How to rerun (per part x)
    BATCH16_PART=x BATCH16_OUT=<scratch>/x-run1.json python batch16/.tmp/run.py <log> scripts/brazil-law/batch16/parse_batch16.py --stats
    (twice, sha256 equal), copy to <scratch>/eff/99-batch16x.json, then
    python batch16/.tmp/run.py <log> scripts/brazil-law/effects_fix.py <scratch>/eff/99-batch16x.json
    python batch16/.tmp/run.py <log> scripts/brazil-law/batch16/.tmp/runbuild.py <eff>/99-batch16a.json ...
- run.py (from the lexifina root) waits until the last line of %LOCALAPPDATA%/gitlaw-cpu.log shows cpu5 <= 90, then runs
  the script at BelowNormal and prints its PID. (Before this wait was added, the two part-a parses at 15:46 started at
  cpu5=92: over the line; every later run waited.)
- parse_batch16.py imports batch15 (BATCH15_PART='-', which brings batch 14/13/... and the MP 905/955 model) and
  configures CBA (from batch14 ALL_ACTS), Lei 4.320 and FGTS (from batch13 ALL_ACTS, page ids re-added to PAGES).
- Fetch/pin: `python batch16/.tmp/run.py <log> scripts/brazil-law/batch16/.tmp/gaps.py id=url ...` (pins into
  batch16/sources_batch16.json, Common Crawl first). Pinned: ato:adc-112-2024-mpv1240, ato:adc-48-2026-mpv1336.
  Act pages and cited laws: `fetch_batch16.py pages` (every PAGES entry), `BATCH16_ACTS=<slugs> fetch_batch16.py laws`,
  then `... missing` (all through run.py).
- Tools (.tmp/): spans.py <part> <units|undated>, udiff.py, lawtxt.py, region.py, cons.py, effrep.py, ordercheck.py,
  missorig.py, overlap.py <part> (SAME = identical copies with overlapping spans: a restored copy dated too early),
  convs.py <part> (lines ended by an MP conversion + the next wording), headyear.py (batch16 pins).
- Checks per part: batch10/.tmp/dupline.py, batch7/.tmp/dupcheck.py, batch7/.tmp/leakcheck.py (only literal '(revogado)'
  wordings allowed), batch10/.tmp/firstline.py, batch14/.tmp/pubgap.py, .tmp/ordercheck.py, .tmp/missorig.py,
  .tmp/overlap.py (SAME lines), batch14/.tmp/headyear.py + .tmp/headyear.py.
- Docs: `python -X utf8 batch14/.tmp/docs.py batch16/.tmp/rows-x.json` (README row + jurisdiction.json counts).

## 99-batch16a - PUBLISHed 2026-10-31 ~15:55 local
Código Brasileiro de Aeronáutica (Lei 7.565/1986), 19 versions 1986-12-23 .. 2025-06-06. The batch-14 trial's 264
problems were 261 x 'no in-force day for mp-1089-2021' (its two-clause vigência), MP 1.240/2024's lapse and one ordering.
- VIGENCIA_FIXED mp-1089-2021 = 30.12.2021 (art. 6 II); MP_LAPSE mp-1240-2024 = 7.11.2024 (Ato Declaratório 112/2024).
- conv_children (CONV_CHILD_ACTS): lines under a caput/§ that MP 1.089 revoked whole carry only Lei 14.368's revocation
  note; they end with the caput on 30.12.2021 (19 lines: arts. 73, 74, 75, 81, 84, 116, ...; listed in the decisions).
- SPAN_FIX: arts. 181/182 (MP 714/2016 vetoed in Lei 13.319/2016: 1986 text back 26.7.2016 - 13.12.2018); art. 303 § 2º.
- EXPLAINED: art-184 (arts. 184-186 one line), art-197 (word dropped on compilado), art-270 (§ sign), titulos (revoked
  headings kept on compilado).
- No effect-day moves (every amender in force on publication for the CBA; Lei 14.034's 1.1.2021 effects are for
  other laws). effects_fix: 0 moves, decision wording only.
- Part sha a860d1cf (pre-effects d91df0f0); merged 115 acts, 2284 versions, 1876 commits, check 0/0, compare identical,
  audit clean. README row + jurisdiction.json (115 acts).

## 99-batch16b - PUBLISHed 2026-10-31 ~16:05 local
Lei do FGTS (Lei 8.036/1990), 51 versions 1990-05-14 .. 2026-08-07 (page l8036consol.htm vs l8036compilada.htm).
- VIGENCIA_FIXED lei-13932-2019 (12.12.2019) + SPAN_FIX by_provision: art. 5 §§ 8º-9º 1.1.2020, art. 20 XXI/XXII
  9.6.2020 (judgement call: MP 889's XXI ends 12.12.2019, so XXI is absent 12.12.2019-9.6.2020, as Lei 8.213 art. 77 §
  2º IV in batch 15).
- MP_LAPSE mp-1336-2026 6.6.2026 (ato:adc-48-2026-mpv1336 pinned); CONVERTED_FIX mp-996-2020 -> lei-14118-2021;
  MP_PENDING mp-2164/2196/2197/2216-2001 (mp-2216 text rewritten for the FGTS: Lei 9.649 art. 49 rewrite).
- SPAN_FIX: art. 3 (1998 caput + I-VI to 1.9.2001, present caput and § 5º from MP 2.216-37, read from Lei 9.649's page -
  judgement call: Planalto's FGTS page notes them 'Lei 9.649'), art. 13 § 5º I gap 24.7-12.12.2019, art. 23 § 2º
  (1990 a)/b) and Lei 13.932's c) around MP 905's § 2º; MP 889's c) to 12.11.2019; its second copy left out).
- TEXT_FIX: art. 5 § 9º doubled label. EXPLAINED art-05, art-09 (compilado out of date: MP 848's § 9º), art-23.
- OPEN_ITEMS: MP editions before 2001, MP 1.107/Lei 14.438 effects tied to an event (in-force day kept), Anexo, Vide.
- Part sha fc492539 (pre-effects ef51c20b); merged 116 acts, 2335 versions, 1909 commits, check 0/0, compare identical,
  audit clean. README row + jurisdiction.json (116 acts).
- (See the reproducibility note at handoff: later pins change only sources[0].requests.)

## 99-batch16a re-PUBLISHed ~16:10 local
Decision text fix only (MP 1.089's revocations are its art. 4 IV, not art. 5 IV); acts/laws byte-identical; sha 1c3e6818
(pre-effects b600c1c7). Line appended to 99-batch16a.PUBLISH.

## 99-batch16c - PUBLISHed 2026-10-31 ~16:10 local
Lei 4.320/1964, 6 versions 1964-05-07 .. 2024-07-03 (l4320.htm vs l4320compilado.htm; 11 diffs explained).
- paragraphs wrapper (l4320 pages): 'Artigo NN.' at paragraph start -> 'Art. NN.' (the trial folded arts. 69-82 and 99-113
  into arts. 68/98 and missed 109-113); '(Veto rejeitado no DOU, de 5.5.1964)' / '(... D.O. 05/05/1964)' moved to notes
  (promulgated before the in-force day: no dating effect); centred scheme lines inside an article (arts. 11-13) moved from
  titulos into the article (TABLE_LINES); scheme_lines() in apply_rewrites dates the struck 1964 art. 11 § 4º scheme with
  § 4º (the trial's 19 undated lines).
- TEXT_FIX art. 49 'para feito' -> 'para efeito'. EXPLAINED 11 units. OPEN_ITEMS: annexes, art. 114, the two 'I)/II) Das
  Subvenções' sub-division names kept as rubricas of arts. 16/18 (firstline flags these 2 only).
- effects_fix MOVES "99-batch16c.json": DL 1.939/1982 (in force 5.7.1982, LINDB) -> 1.1.1983 (art. 2: applied to budgets
  and balance sheets from the 1983 financial year). Judgement call: read as a fixed effect day, not an event.
- Part sha 34c3deae (pre-effects 95d1cb26); merged 117 acts, 2341 versions, 1914 commits, check 0/0, compare identical,
  audit clean. README row + jurisdiction.json (117 acts).

## 99-batch16d - PUBLISHed 2026-10-31 ~16:20 local
Lei de Tortura 9.455/1997 (3 versions), Lei do Genocídio 2.889/1956 (1; LINDB day 16.11.1956), Lei do Mandado de Injunção
13.300/2016 (1), Lei do Habeas Data 9.507/1997 (1). Pages pinned (fetch_batch16 pages), cited laws (laws/missing: 1 new).
TEXT_FIX: Lei 9.455 art. 1 § 4º II stray quote. 0 diffs, 0 problems, 0 effect moves. Part sha ec069db1; merged 121 acts,
2347 versions, 1918 commits, check 0/0, compare identical, audit clean. README rows + jurisdiction.json (121 acts).

## 99-batch16e - PUBLISHed 2026-10-31 ~16:35 local
Estatuto do Índio 6.001/1973 (2 versions), Lei das Cooperativas 5.764/1971 (10), Lei da Reforma Agrária 8.629/1993 (10; vs
l8629compilado.htm). Hand: EInd art. 20 § signs (paragraphs wrapper, SECTION_SIGN); EInd art. 2 IX from Lei 14.701 art. 32
promulgation 28.12.2023; LCoop art. 110 bare-note words kept as text (BARE_KEPT); MP_PENDING mp-2168-2001; LRA art. 20
§§ 1º-4º from Lei 13.465 (unnoted lines printed after its caput: found by .tmp/latecaput.py), art. 6 § 9º VETADO ->
promulgation 13.6.2024. EXPLAINED LRA art-05/art-17; OPEN_ITEMS LRA (MP 2.183 chain from 1997), EInd (ADC 87 etc.).
Part sha 4057d035 (pre-effects 7940e0dd); merged 124 acts, 2369 versions, 1930 commits, check 0/0, compare identical,
audit clean. README rows + jurisdiction.json (124 acts).
- New tool .tmp/latecaput.py <part>: unnoted lines dated from the act's first day printed after a later caput (noisy:
  mostly untouched children of a rewritten caput; read each). On a-c it found nothing new to fix.

## 99-batch16f - PUBLISHed 2026-10-31 ~16:50 local
Lei do Seguro-Desemprego 7.998/1990, 20 versions (l7998.htm vs l7998compilado.htm; 1 diff explained: compilado omits art. 11 V).
- VIGENCIA_FIXED mp-665-2014 30.12.2014 + VIGENCIA_PROVISION arts. 3/4 28.2.2015 (60 days), SPAN_FIX art. 3 II revoked on
  publication (MP 665 art. 4 II under art. 3 III); VIGENCIA_PROVISION mp-905-2019 art-04-b 1.3.2020 (MP 905 art. 53 II);
  SPAN_FIX art. 25 (MP 905's two copies printed in reverse order; the 1990 article back while MP 955 stood and from
  19.8.2020); NOTE_FIX 'Lei nº 10.261, de 2021' -> 14.261 (link L14261.htm#art12).
- effects_fix MOVES "99-batch16f.json": LC 155/2016 art. 3 § 4º -> 1.1.2018 (art. 11 III). Lei 13.134 art. 4 financial
  effects only: in-force day kept (open item).
- Part sha 76f47cb1 (pre-effects a7a4a7e4); merged 125 acts, 2389 versions, 1938 commits, check 0/0, compare identical,
  audit clean. README row + jurisdiction.json (125 acts).

## 99-batch16g - PUBLISHed 2026-10-31 ~17:00 local
MROSC Lei 13.019/2014, 5 versions (two on 23.1.2016: as enacted + 'same_day' text in force; then 2020, 2022 x2). In-force
day 23.1.2016 (art. 88 as worded by Lei 13.204/2015; 540th day 22.1.2016). SPAN_FIX: MP 658/684 wordings of arts. 83 §§
1º-2º and 88 replaced before the in-force day -> skip ('never-in-force'); arts. 35 i), 42 XX 2014 wordings end same-day.
OPEN_ITEMS: municipalities 1.1.2017 not separated. 0 diffs, 0 problems, 0 effect moves. Part sha 08fc731c (re-PUBLISHed: first install 3b2abdc5 carried a stray 'Note corrected: Lei 7.998' decision from a global NOTE_FIX, now scoped to part f); merged 126
acts, 2394 versions, 1941 commits, check 0/0, compare identical, audit clean. README row + jurisdiction.json (126 acts).

## State at handoff (batch 16)
Parts 99-batch16a..g installed with .PUBLISH (15 acts, 129 versions; merged 126 acts, 2394 versions, 1941 commits, check
0/0, --compare identical, audit clean). README rows + jurisdiction.json (126 acts) current. effects_fix.py MOVES added for
99-batch16c (DL 1.939/1982 -> 1.1.1983) and 99-batch16f (LC 155/2016 -> 1.1.2018). No background processes left running
(every run was foreground through .tmp/run.py; PIDs are printed in the command output only, all exited).

Reproducibility check at handoff: fresh parses of a-g give the installed parts' acts, laws and decisions; a-d differ only
in sources[0].requests (the count covers the whole growing pin file batch16/sources_batch16.json; batch 13 precedent,
left as published).

## Next candidates (not configured)
Major federal acts still missing (check corpus.d first): Lei 5.889/1973 (trabalho rural), Lei 4.090/1962 (13º salário),
Lei 605/1949 (repouso semanal), Lei 7.418/1985 (vale-transporte), Lei 9.029/1995, Lei 6.634/1979 (faixa de fronteira),
Lei 9.637/1998 (OS), Lei 9.790/1999 (OSCIP), Lei 8.987 done; tax laws Lei 7.713/1988 (IRPF), Lei 9.430/1996, Lei 9.249/1995
(heavy MP chains); Lei 6.024/1974; Lei 4.728/1965; Lei 10.931/2004; Lei 11.977/2009; Lei 13.465/2017; Lei 9.609/1998
(software); Lei 12.037/2009; Lei 6.404 done.
