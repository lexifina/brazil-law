# Brazil batch 10 progress (gitlaw-BR agent on alan-dell, 2026-10-31)

Owns `scripts/brazil-law/batch10/` and `corpus.d/99-batch10.json` (+ `.PUBLISH`). Never commits or pushes. Scratch OUTSIDE
the repo: `~/Documents/.gitlaw-scratch/brazil-b10parts` (regenerated parts, batch10/.tmp/runparts.py),
`brazil-b10src` (country folder copy + trial parts), `brazil-b10` (build), `brazil-b10c` (--compare);
batch10/.tmp/runbuild.py runs build, check, compare.

## 1. Pin scan of every older part - DONE 2026-10-31 ~03:35Z

batch10/.tmp/pinscan.py resolves each pin of all 14 pin files to its cached bytes (as the parsers do) and flags bot /
JavaScript placeholder pages, cut pages, and heading numbers that differ from the pin's id. 1,573 pins. Real faults:
- codes/sources_codes.json law:mp-75-2002: F5 'Please enable JavaScript' page (IA 2021). -> IA 20031125232840 (batch 9's).
- codes/sources_codes.json law:lei-15452-2026: Lei 15.352's page (L15352.htm). -> L15452.htm, IA 20261016023405.
  Batch 9 inherited it: Código de Trânsito art. 326-C (Incluído pela Lei 15.452/2026) was dated 25.2.2026 from Lei
  15.352's page. Lei 15.452 is de 30.6.2026, DOU 1º.7.2026, in force on publication -> art. 326-C from 1.7.2026; the two
  wrong hand entries (VIGENCIA_FIXED, PUBLISHED_FIXED) removed from parse_batch9.py.
- clt/sources_clt.json law:lei-3807-1960: bot page. -> leis/1950-1969/L3807.htm, IA 20261023235338 ('Vide' notes only).
- batch3/sources_batch3.json law:mp-765-2016: Lei 8.270's page. -> mpv765.htm (rju's pin, IA 20261015082912).
- batch5/sources_batch5.json law:mp-922-2020: MP 992's page. -> mpv922.htm (batch 9's CC pin).
Old-format (ts, no 'via') pins are read from .cache/<sha>.bin: the two IA captures fetched through wayback.py were copied
there and their log lines added to .cache/requests.jsonl. Pin files before the change: batch10/.tmp/pins-before/.
Flags checked and fine: Atos Complementares / Resoluções do Senado (heading pattern), Atos Declaratórios ~3 KB (real),
lei-10973 (no </html>, whole, known). sources.json (CF, corpus.json) has no cache here, so it could not be scanned.
Regenerated every part 50..99-batch9 to scratch: identical except 50-codes (request count 79->80 only), 99-batch9 (art.
326-C day, Lei 15.452 record), and 97-batch4 / 99-batch6 (source request counts and the hand-cleaned published wording
differ from a fresh run; no act, version or law differs, pins they use unchanged -> left as published). Installed
50-codes (5563f253) and 99-batch9 (17f87c10), PUBLISH rewritten; merged scratch build 1352 commits, 51 acts, 1496
versions, check.py 0/0, --compare identical, audit_push clean.

## 2. 99-batch10 v1 - PUBLISHed 2026-10-31 ~03:45Z
6 acts, 44 versions: Lei de Concessões 12, Lei das PPPs 14, Lei de Abuso de Autoridade 2, LC 64/1990 (Inelegibilidades,
incl. Ficha Limpa) 5, Lei 8.142/1990 1, Lei Geral do Esporte 10. Part sha256 53ba8701, parse twice identical; merged
scratch build 1384 commits, 57 acts, 1540 versions, check 0/0, --compare identical, audit clean. README rows and
jurisdiction.json (57 acts) updated.
New in parse_batch10.py (imports batch9 with BATCH9_ACTS=-; batch 9's hand tools cleared):
- OWN_PROMULGATION: an act's own vetoed parts promulgated after a veto override. A printed line is promulgated when its
  words are in the promulgation text after the act's signature, in a contiguous block starting at a line with the note
  '(Promulgação partes vetadas)' (headings only with the note); it starts on the DOU day credited to the act's law, and
  the '(VETADO)' line stands until then; version note added. LGE: DOU 22.5.2024 (20 units); LAA: 27.9.2019, before the
  act's in-force day, so no change.
- CONVERTED_FIX MP 577/2012, 575/2012 ('Convertida pela Lei'); VIGENCIA_FIXED Lei 13.137/2015 (art. 26 VII); NOTE_FIX MP
  513 'de 2.010'; SPAN_FIX LConc art. 27 I/II (renumbering 11.196/2005), LGE art. 99 IV bare label skipped (Lei 15.522's
  future wording not printed); EXPLAINED LConc art. 15, LPPP art. 10/26, LAA art. 15-A.
- P.PUBLISHED_FIXED: batch 9's mp-75-2002 popped (every entry there is printed in decisions).
Checks: batch10/.tmp/dupline.py (new: word-for-word repeated labelled line, or a label twice under one parent, any
version; catches doubled incisos, which batch7's dupcheck does not), batch7/.tmp/dupcheck.py, leakcheck.py.

## 2b. 99-batch10 v2 - re-PUBLISHed 2026-10-31 ~03:55Z
+ Estatuto dos Militares (15 versions) and Estatuto do Torcedor (9, repealed 15.6.2023): 8 acts, 68 versions, part sha
f857823e; the 6 v1 acts byte-identical; merged 1408 commits, 59 acts, 1564 versions, check 0/0, --compare identical,
audit clean; README + jurisdiction.json (59 acts). autopush pushed main bde1fb7be at 03:52Z (before v2).
- EMil: VIGENCIA_FIXED Lei 11.447/2007; MP_PENDING MP 2.215-10/2001; LABEL_FIX 'lll -' and 'u§ 2º'; SPAN_FIX art. 98 IV
  from 11.12.1981 and art. 3 § 1º b) II {"keep": True} (new: B7.stale_fix.fix wrapped so 'keep' lines survive rule B,
  which took b) II for a twin of a) II because its parent model ignores alíneas); EXPLAINED art. 98 (XIV placeholder),
  art. 101 (consolidated omits item 4).
- ETor: page 'etorc-2023' = Arquivo.pt capture 20230321080515 (before the repeal; the live page strikes everything);
  B9.REPEALS entry (Lei 14.597 art. 217 III, 15.6.2023); art. 44 staged: gates art-18/22/25/33 + SPAN_FIX art. 13 p.u.
  from 17.11.2003.
- Pins fixed in batch10/sources_batch10.json (Planalto links to the wrong page): law:lei-15103-2025 was L9991.htm#art19 ->
  L15103.htm; law:mp-671-2015 was l10.671.htm -> mpv671.htm. pinscan.py now also flags FIRSTHEAD (first heading's number
  differs from the id's); over all files only these two plus a false positive (clt lei-11295: <title> says 11.294).
- Also pinned: law:mp-513-2010, law:lei-9990-2000, ato:apn-31-2013-mpv592, ato:adc-70-2018-mpv844, ato:adc-36-2019-mpv868.

## 3. Next (configured in ALL_ACTS, not VERIFIED)
- Lei do Saneamento Básico (11.445): ACT_DAY 22.2.2007 (no vigência clause: LINDB 45 days). MP 844/2018 and 868/2018
  lapses (Atos 70/2018, 36/2019), their staged clauses and Lei 13.312/2016 (5 years) are set; left: Planalto prints whole
  articles (art. 2 and others) three or four times for MP 844 -> lapse -> MP 868 -> lapse -> Lei 14.026/2020, and the
  replay overlaps them (art. 2 doubled incisos; 'ends before it starts' art. 35 I-III; restored wording art. 23, 52).
  Needs a hand model of 9.7.2018-15.7.2020.
- Lei do Petróleo (9.478): days for Leis 15.103/2025 (repinned), 15.082/2024, LC 225/2026, NOTE_FIX 9.990, MP 592/2012
  lapse (Ato 31/2013), MP 532/2011 conversion set. Left: MP 1.063/2021 -> Lei 14.292/2022 (vetoed arts. 68-B/68-C) with
  MP 1.069/2021 (revoked by MP 1.100/2022 / Lei 14.367/2022) over the same articles; MP 1.255/2024 (revoked by Lei
  15.075/2024); 6 diffs (art. 8, 10, 48, 49, 68-B, 68-C).
- PNMA (6.938): compilada is a retyped edition (24 units differ in punctuation/case and some words): needs care.
- Unresolved MP fates seen: 1069/2021, 1255/2024, 2215/2001, 532/2011, 592/2012, 671/2015, 844/2018, 868/2018.

## 4. dupline.py over every published part (2026-10-31 ~04:05Z)
Most hits are legitimate (repeated '(revogado)' lines, quoted amendments, alíneas holding incisos, 'I-B' read as 'I').
One real fault fixed: 99-batch9 LDB art. 36-B incisos I-III doubled 2008-2023 (renumbering by Lei 14.645/2023; SPAN_FIX
in parse_batch9.py, as LConc art. 27 here); 99-batch9 re-PUBLISHed (sha 8ddfebdc). Not reviewed one by one: CLT (115
hits, many known), LBI 16, LRF 8, ECA 6, LRP 6 (sampled: repeated lists, legit), CPC 5; worth a pass by label.
