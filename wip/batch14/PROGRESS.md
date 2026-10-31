# Brazil batch 14 progress (gitlaw-BR agent, 2026-10-31)

Owns `scripts/brazil-law/batch14/` and `corpus.d/99-batch14<x>.json` (+ `.PUBLISH`), one small part per 2-4 acts. Never
commits or pushes. Scratch outside the repo: `~/Documents/.gitlaw-scratch/brazil-b14` (trial parts, page
texts), merged build `brazil-b14-src` / `-build` / `-c`.

## How to run (per part x) - same pipeline as batch 13
- parse_batch14.py imports batch13 (BATCH13_ACTS='-') and replaces the configuration: ALL_ACTS / PARTS[x], PAGES,
  ACT_DAY_ALL, ACT_LAWS_ALL, hand tables. Clears batch 13's act tables and P.COURTS (batch 13's RSF 16/2006 decision was
  printed into every later part: 99-batch13h carries it although it holds no TCU act - harmless, left as published).
- Fetch (one process, BelowNormal): `python batch14/.tmp/run.py <log> scripts/brazil-law/batch14/fetch_batch14.py
  pages|laws <page ids>|missing|gap <id> <url>` (run from the lexifina root). `gap` skips an id already pinned: delete
  the bad pin from batch14/sources_batch14.json first.
- LexML day of one law: batch14/.tmp/lexml1.py <key> <enacted> (cached; the parser then corrects the page's DOU day).
- Parse twice: `BATCH14_PART=x BATCH14_OUT=<scratch>/x-run1.json python batch14/.tmp/run.py <log> .../parse_batch14.py --stats`.
- Checks: batch10/.tmp/dupline.py, batch7/.tmp/dupcheck.py, batch7/.tmp/leakcheck.py, batch10/.tmp/firstline.py,
  batch14/.tmp/headyear.py (pins), batch14/.tmp/pubgap.py <part> (publication day < enactment or > 20 days after),
  batch14/.tmp/undated.py <out> <acts> (UNITS=... env: dump lines; prints every 'undated' struck line).
- Merged build: batch14/.tmp/run.py <log> scripts/brazil-law/batch14/.tmp/runbuild.py <scratch>/99-batch14x.json.
- Docs: batch14/.tmp/docs.py batch14/.tmp/rows-x.json <candidate part>.
- Future repeals: B9.REPEALS with a day after today; the consolidated() wrapper keeps the Planalto comparison for them.

## 99-batch14a - PUBLISHed 2026-10-31
Lei Kandir LC 87/1996 (18 versions, 1996-2026 + repeal 1.1.2033), Lei do ISS LC 116/2003 (7, 2003-2025 + repeal 2033).
Hand: VIGENCIA_FIXED lc-102-2000 (1.8.2000), lc-190-2022, lc-122-2006 (pin repinned to Lcp122.htm: Planalto linked
Lcp138); LexML day for LC 92/1997 (footer misprints 1999); LABEL_FIX art. 13 '2º Não integra' -> § 2º; SPAN_FIX art. 12 §
5º + I/II from 13.6.2024 (LC 204 veto promulgation), art. 31 § 4º-A ends LC 115/2002 (unclosed note); REPEALS both acts
2033-01-01 (LC 214 art. 543). LC 214/190 'Produção de efeitos' wordings dated by in-force day (house rule). Open items:
LC 116's list of services and LC 87's struck Anexo not included. Part sha 3c0d6b6c; merged 103 acts, 1974 versions, 1677
commits, check 0/0, compare identical, audit clean (futuro has the 2033 repeal commit).

## 99-batch14b - PUBLISHed 2026-10-31
Lei 9.433/1997 (11), DL 201/1967 (6), LGT 9.472/1997 (14), Lei 1.521/1951 (4) = 35 versions. Hand: VIGENCIA_FIXED
lei-14173-2021 (art. 13 III); law:lei-14108-2020 pinned (gap); NOTE_FIX 'Lei º 14.108'; SPAN_FIX LGT art. 172 caput (Lei
13.879, unnoted new wording); WORD_FIX LGT art. 90 opening quote; MP_PENDING mp-2172-2001. Part sha 259185d5; merged 107
acts, 2009 versions, 1699 commits, check 0/0, compare identical, audit clean.
Bad pins seen by headyear (not used by a/b; fix before building the acts that cite them): law:lei-10877-2004 -> L10.887,
law:lei-11974-2009 -> L11934. False positives: lc-188-2021, lc-190-2022 (heading without 'DE'); lc-115-2000 unused.

## 99-batch14c - PUBLISHed 2026-10-31
SNUC 9.985/2000 (8), Lei da Liberdade Econômica 13.874/2019 (5), Estatuto da Igualdade Racial 12.288/2010 (2) = 15
versions. Hand: law:lei-11516-2007 pinned; NOTE_FIX 'Lei nº 11.516, 2007'; EXPLAINED dotted quoted lines (LLE 14, EIR
62/64); new paragraphs wrapper SQUOTE_KEPT: a quote-closing line in single quotes marked 'rubrica' goes back to the
article printed above it (LLE art. 7 'Art. 1.368-F'). Part sha f758bf63; merged 110 acts, 2024 versions, 1712 commits,
check 0/0, compare identical, audit clean.

## 99-batch14d - PUBLISHed 2026-10-31
Estatuto da Terra 4.504/1964 (12 versions). Hand: VIGENCIA_FIXED dl-2431-1988 (14.5.1988); rejection law record
adc-1989-dl2431 (via P.COURTS, kind law, 14.6.1989) + SPAN_FIX arts. 27/28 (FUNMIRAD wordings end, restored 1964 copies
start then); MP_PENDING mp-2183-2001; LexML day lei-6746-1979; 8 consolidated-page diffs EXPLAINED. Part sha 2c75cb00;
merged 111 acts, 2036 versions, 1725 commits, check 0/0, compare identical, audit clean.

## 99-batch14e - PUBLISHed 2026-10-31
LC 123/2006 (13 versions, from 6.3.2012 'oldest version available' + 2033 partial repeal on futuro). Hand: build_act
wrapper trims to ME_START and the part writer sets first_law null / earlier_laws (batch 12 pattern); VIGENCIA_FIXED
lc-188-2021, lc-155-2016, lc-216-2025; LAW_TITLE_FIX lc-155-2016 (letter-spaced ementa); SPAN_FIX base lines of arts.
18-C/38-A/85-A, bare d)/e) skipped; LABEL_FIX '§ 1º A.'; H1_PAGES (h1-h6 headings read as centred <p>); me_2033() ends
LC 214 art. 543 V targets (23 dispositivos incl. children) on 2033-01-01. Part sha b81541e9; merged 112 acts, 2049
versions, 1732 commits, check 0/0, compare identical, audit clean. New tools: .tmp/nonote.py (no-note lines dated after
the act day), .tmp/spaced.py (letter-spaced lines), .tmp/clause.py, .tmp/whichart.py.
NOTE: heredoc-written regexes lose backslashes ('' became a backspace once): write patches with the Write tool.

## Next
Configured in ALL_ACTS (pages pinned): Lei 8.212/1991 (l8212cons.htm vs compilado), Lei 8.213/1991 (l8213cons.htm vs
compilado), LC 123/2006 (watch LC 214 art. 543 V: partial 2033 repeals), Estatuto da Terra, LGT 9.472, Lei 9.433, SNUC,
Lei 13.874, CBA, Lei 12.288, Lei 1.521, DL 201/1967.

## Findings for the heavy acts (not built yet)
- (DONE in 14e) LC 123/2006: Planalto's page is the 2012 republication (LC 139/2011 art. 5; DOU 31.1.2012 and again 6.3.2012); its notes
  start with LC 147/2014, so 2006-2011 cannot be rebuilt -> plan: 'oldest version available' from the republication
  (batch 12's Lei 9.656 pattern). Also: lc-188-2021 day 31.12.2021 (heading lacks 'DE'); art. 18 ('§ 1º A.' label) and
  art. 18-A § 1º (letter-spaced struck text) problems; LC 214 art. 543 V partial 2033 repeals (about 20 dispositivos) to
  set as SPAN_FIX ends on futuro; annexes I-V (tax tables) not included.
- Lei 8.212/1991: 91 versions, 670 struck lines, 47 problems. Staged amenders read (batch14/.tmp/clause.py, whichart.py):
  Lei 13.756 art. 36 -> 13.12.2018; Lei 11.457 arts. 2/17/32 -> clause II (first business day of the 2nd month after
  19.3.2007: 2.5.2007); MP 258/2005 arts. 3/27/39 -> 15.8.2005, MP lapsed (date to source); Lei 14.784 arts. 2/4 ->
  28.12.2023; Lei 13.670 arts. 3/5 -> 30.5.2018; Lei 11.098/2005 art. 4 (art. 39 caput) depends on the act of its art. 8
  I (open); MP 905/2019 arts. 9/49 -> 12.11.2019, then MP 955 revocation / lapse. MP fates open: 927/2020, 841/2018,
  793/2017, 252/2005, 2216/2001, 2170/2001, 1202/2023 (lei-14873-2024 page to pin), 1110/2022. 12 consolidated diffs.
- Lei 8.213/1991: 78 versions, 106 problems: Lei 13.135/2015 and MP 664/2014 staged clauses, MP 905, Lei 13.876 art. 3
  (1.1.2020), MP 1.355/2026, 'MPv nº 404' and 'Lei nº 11,718' note typos, law:lei-10877-2004 pin points at L10.887
  (repin), 77 undated struck lines.
- CBA 7.565/1986: 264 problems (not analysed).

## Groundwork for Leis 8.212/8.213 (done after 14e, not in any part)
- Pins fixed in batch14/sources_batch14.json: law:lei-10877-2004 -> L10.877.htm, law:lei-11974-2009 -> L11974.htm (both
  had pointed at other acts' pages), law:lei-14873-2024 pinned (MP 1.202/2023's conversion). headyear now clean except the
  known false positives (lc-188, lc-190 headings without 'DE'; unused lc-115-2000).
- Atos Declaratórios pinned (ids ato:...) with the lapse days read from them (MP_LAPSE = day after 'encerrado no dia'):
  adc-65-2022-mpv1110: MP 1.110/2022 ended 7.8.2022 (DOU 19.8.2022) -> 2022-08-08
  cn-2005-mpv252: MP 252/2005 ended 13.10.2005 -> 2005-10-14
  cn-2005-mpv258: MP 258/2005 ended 18.11.2005 -> 2005-11-19
  adc-66-2017-mpv793: MP 793/2017 ended 28.11.2017 (DOU 7.12.2017) -> 2017-11-29
  adc-64-2018-mpv841: MP 841/2018 ended 23.10.2018 (DOU 25.10.2018) -> 2018-10-24
  adc-92-2020-mpv927: MP 927/2020 ended 19.7.2020 (DOU 31.7.2020) -> 2020-07-20
  MP 905/2019 and MP 955/2020: clt/parse_clt.py already has MP_LAPSE (905: 2020-08-19, 955: 2020-08-18, Atos 127 and
  113/2020, pinned in clt/sources_clt.json) and the MP_PAIRS / mp_pairs() model (905 revoked by 955, back after 955's
  lapse); the proc pipeline has no such model - port mp_pairs() into batch14 before building 8.212/8.213.
  MP 1.202/2023: converted into Lei 14.873/2024 but also 'Vigência encerrada' (MP 1.208/2024 revoked parts) - read it.
  Pending under EC 32 art. 2: MP 2.170-36/2001, MP 2.216-37/2001.
- Lei 8.212 also: footnote numbers leak into text ('e) as importâncias: 14' in art. 28; l8212cons.htm prints numbered
  footnotes '1 Alínea alterada pela...'), 'Pescado}' and 'TÍTULO VII l' typos, 2 'restored wording' (art. 26), 2 'ends
  before it starts' (art. 28 a), art. 50).
- CPU: the gitlaw-cpu.log five-minute load was above 90 from about 11:52 to 12:04; work waited (one short trial parse and
  the Ato fetches at 12:18, cpu5=91, were started just over the line).
