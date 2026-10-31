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
  batch16/sources_batch16.json, Common Crawl first). Pinned: ato:adc-112-2024-mpv1240.
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
- Note: a fresh parse of part a now differs from the installed 99-batch16a only in sources[0].requests (the pin file
  grew by one Ato); left as published (batch 13 precedent).

## Next
Lei 4.320/1964 (lei-4320-de-1964: veto-override notes, arts. 109-113, struck lines); then batch13/14 candidates.
