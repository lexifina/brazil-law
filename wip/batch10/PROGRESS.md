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

## 5. Coordinator follow-up (2026-10-31 ~04:05-04:35Z)

99-batch10 v3/v3b re-PUBLISHed (10 acts, 99 versions, sha f2567df2; merged 61 acts, 1595 versions, check 0/0, compare
identical, audit clean):
- Lei do Saneamento Básico: san_model (parse_batch10.py; runs inside the stale_fix wrapper, after every other rule):
  each 2007-era wording of an article MP 844/868 touched is kept once (last copy, today's place), from its first day to
  the last copy's end, gapped while an MP that replaced it was in force (whole article if the MP rewrote the caput, else
  same label; MP-own lines = notes 'Redação dada/Incluído pela MP'). Hand: art. 35 MP 844 incisos end at lapse; art. 11
  § 5º-A is MP 868's; art. 52 § 1º I (2007 wording returns with Lei 14.026, SAN_FINAL). Check: batch10/.tmp/lsbinv.py
  (every unit on 1.12.2018 and 1.7.2019 equals 8.7.2018) clean; settled replay problems filtered (SAN_SETTLED).
- PNMA: verified against the Chamber's archived 'publicação original' (pinned ctx:camara-lei-6938-1981-original) and the
  amending laws (batch10/.tmp/pnma_adj.py): every line matches its source; Ibama/IBAMA per Leis 9.960/10.165; art. 8 V
  'fiananciamento' as published; art. 19 VETADO ends with Lei 7.804; consolidated page = retyped edition (EXPLAINED).
- move_rubricas wrapper: '(NR)'/quoted/dotted closing lines stay in their article (LPPP art. 26, LSB 55-58 changed).
- Lei do Petróleo: NOT built. 68-B/68-C done (MP 1.069 wordings end with Lei 14.292, 4.1.2022), MP fates set, ADI 4.917
  cautelar (18.3.2013, from the archived andamentos, pinned ctx:stf-adi-4917-andamentos) as a no-words court version.
  Blocking: Lei 12.734/2012's vetoed parts were promulgated 14.3.2013 (DOU 15.3.2013) - arts. 48 II, 49 II, 49-A..C,
  50 § 2º, 50-A..E start then, not 30.11.2012 (the annotated page does not say so) - and MP 592/2012 (3.12.2012-13.5.2013)
  overlaps 49-A/50-A/50-B (mixed states seen). Needs: the promulgated dispositivos from the promulgation text on Lei
  12.734's page, old wordings to 15.3.2013, MP 592 vs promulgation order, then ADI credits only where 12.734 wording stood.
- CLT duplicate-line review (all 115 flags): fixed via batch7/oldparts.py OLD_FIX/OLD_RANGES (arts. 379, 515, 525, 558,
  592, 606); 70-clt re-PUBLISHed (bfe1a543). Left: the documented open units (530, 534, 538, 553, 628-A, 634, 636, 654,
  693, 896, 902); 401 'Art. 401A/401B (VETADO)' filed in art. 401 as on the consolidated page; 758 printed 'e)' for c);
  589 and the 1943/1976 art. 592 label repeats are legitimate (items 'I.'-'IV.' are unlabelled lines).
- LBI (16 flags): all in quoted amendments (arts. 101-114) - legitimate. LRF (Recuperação e Falência, 8): art. 35 lists,
  '(revogada)' lines, I-B..I-E read as 'I' - legitimate. Lei de Responsabilidade Fiscal (1): art. 20 lists - legitimate.
- NEW FINDING, not fixed (affects published parts): batch10/.tmp/firstline.py - lines that close a quoted amendment
  ('....." (NR)', a quoted 'Art. N') are moved into the NEXT article by parse_proc.move_rubricas in older parts: CPC
  arts. 1061-1069, Lei 14.133 art. 178, LAI 44/45, Estatuto da Cidade 55/56, Pessoa Idosa 54/111-115, LBI 97-108, Maria
  da Penha 44, Hediondos 7, LOC 26/288, LPI 241, Lei das Eleições 104, Código Florestal 81/82, Inquilinato 84/87,
  Mediação 46, Startups 18, ECA 265 and others. The batch10 wrapper is the fix; applying it to parse_proc would change
  ~15 parts (needs the coordinator's go-ahead and per-part re-verification). Also RLP arts. 294-297, CC 227/1240-A,
  Código Eleitoral 247 ('At. 248') start with a non-caput line - to review.

## 6. Quoted-amendment closing lines, fixed in the shared parsers (coordinator task, 2026-10-31)
- Fix: `closes_quote()` in proc/parse_proc.py, parse_phase2.py and clt/parse_clt.py (move_rubricas): a line ending '(NR)',
  starting with a quotation mark or dots, or ending with punctuation + closing quote ('... poder. "') is never a rubrica and
  stays in the article that quotes it (a rubrica may end with a quoted word: CP art. 178 '... ou "warrant"' still moves).
  Counted in RUBRICA_KEPT; `rubrica_decision()` adds the decision in each parser's main. The batch10 wrapper was removed.
- Baseline (before) and fixed parts regenerated to scratch (brazil-rub-base / brazil-rub-fix, runparts.py); .tmp/rubdiff.py
  shows per act which lines moved and checks every version holds the same multiset of lines (0 faults; one expected:
  Estatuto da Cidade art. 53's struck closing line now leaves with art. 53, revoked on the act's first day).
- Changed: 60-phase2 (CPC 1.060-1.069), 90-batch3 (ECA 264), 98-batch5 (LLC 177/179), 99-batch5b (Inquilinato 83/86,
  Mediação 45), 99-batch6 (LAI 43/44; published sources kept), 99-batch7 (ECid 53-55, Idoso 53/111-114, Startups 17, Maria da
  Penha 43), 99-batch8 (Hediondos, LOC 24/25, LPI 240, LBI 96-118), 99-batch9 (Eleições 103, Código Florestal 80/81),
  99-batch10 (decision wording only). Unchanged: 50, 70, 80, 95, 97. Consolidated-page compare lists, dupline/dupcheck/
  leakcheck output identical before/after. Merged build 61 acts, 1595 versions, check 0/0, --compare identical, audit clean.
  All touched parts installed and PUBLISH appended (~09:3xZ).
- (FIXED in section 8) quoted articles printed without an opening quote are read as articles of the act itself, giving
  units that are another law's articles: Crimes Hediondos art-159/213/214/223/267/270 (CP articles quoted in its art. 6),
  Organizações Criminosas art-288, LBI art-1783-a (CC), Lei 14.133 art-337-e..p (CP arts. inserted by its art. 178).
  Fixing needs a quote-state tracker in paragraphs() (same-label successor logic would misread §§ of several quoted
  articles in one unit), then re-verification of 98-batch5/99-batch8.

## 7. Lei do Petróleo - PUBLISHed in 99-batch10 (2026-10-31)
- lpet_model (parse_batch10.py, after stale_fix like san_model): Lei 12.734/2012 art. 3 (arts. 48, 49, 50, 49-A..C, 50-A..F)
  and art. 4 were vetoed WHOLE and promulgated 14.3.2013 (DOU 15.3.2013; text on L12734.htm, republished in part 25.3.2013)
  -> every 12.734-noted line starts 15.3.2013, replaced wordings end then. MP 592/2012 (3.12.2012) art. 3 revoked art. 49
  § 3º and art. 50 § 4º (page only says 'Vide') -> end 3.12.2012; its 49-A, 50 § 5º, 50-A, 50-B end 15.3.2013; 48-A and
  81-A at the lapse 13.5.2013. Version note on 15.3.2013. ADI 4.917 (18.3.2013) unchanged.
- .tmp/lpetpromo.py: all 116 Lei 12.734 lines found word for word in the promulgation text. EXPLAINED for arts. 8, 10, 48,
  49, 68-B, 68-C. 42 versions; part 11 acts, 141 versions, sha 3baa103f (parse twice identical); merged 62 acts, 1637
  versions, 1472 commits, check 0/0, --compare identical, audit clean. README row + jurisdiction.json (62 acts) updated.
- Tools: .tmp/lpetdump.py (replayed lines of units), lpetcons.py (diff vs consolidated), lawtext.py (cached page text).

## 8. Quotation state in the shared parsers (coordinator task, 2026-10-31)
- paragraphs() in proc/parse_proc.py, parse_phase2.py, clt/parse_clt.py and codes/parse_codes.py tracks an open quotation
  (track_quote: opened by a line or heading starting with a double quote, closed by '(NR)' or a closing quote at the end of
  a line). While open, an 'Art. N' line stays in the current unit (keeping its label) unless N is the current article or
  the next one, which also closes a quotation left open (quoted_article; QUOTED_ARTICLES -> quoted_decision()).
  parse.py (CF) not changed: it builds units differently, holds no quoted amendments, and its cache is not on this machine.
- All 14 parts regenerated before/after: only 98-batch5 and 99-batch8 change. Units gone (lines moved, same lines/credits
  /days in every version, rubdiff 0 faults): LLC art-337-e..p -> art-178; Hediondos art-159/213/214/223/267/270 -> art-06;
  LOC art-288 -> art-24; LBI art-1783-a -> art-116. Decisions: new quoted-article decision; rubrica count 34 -> 32 in
  99-batch8 (two closing lines now already in the quoting unit); Hediondos EXPLAINED re-keyed art-159/223 -> art-06 in
  batch8/parse_batch8.py. dupline/dupcheck now list the quoted §§ in LLC art-178 and Hediondos art-06 (legitimate).
- Parse twice identical (98-batch5 01374560, 99-batch8 42fbba63); merged 62 acts, 1637 versions, 1472 commits, check 0/0,
  --compare identical, audit clean; both installed and PUBLISH appended.
