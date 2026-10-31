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

## Next
Configured in ALL_ACTS (pages pinned): Lei 8.212/1991 (l8212cons.htm vs compilado), Lei 8.213/1991 (l8213cons.htm vs
compilado), LC 123/2006 (watch LC 214 art. 543 V: partial 2033 repeals), Estatuto da Terra, LGT 9.472, Lei 9.433, SNUC,
Lei 13.874, CBA, Lei 12.288, Lei 1.521, DL 201/1967.
