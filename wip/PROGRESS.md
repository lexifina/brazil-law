CHECKPOINTED 2026-10-31 (batch 17: 99-batch17a-y PUBLISHed, 49 acts; merged 175 acts, 2978 versions; MP edition reader in batch 6; DATED RE-CHECK of MP 1.382/2026 after 28.11.2026; details in batch17/PROGRESS.md)

# gitlaw-BR progress (Brazil)

Repo: lexifina/brazil-law (PRIVATE, never change visibility). Clone ~/Documents/brazil-law is OWNED BY autopush.py (do not build into it or push; push_wip.sh deleted). Slug `brazil`, tz America/Sao_Paulo, lang pt, future branch `futuro`. Brief: scripts/south-america-law/BRIEF.md (read "Changed after the restart").

Split (coordinator): helper agent gitlaw-BR-codes owns Código Civil and LGPD in `corpus.d/50-codes.json` (do not edit corpus.d/). I own CF/88 in corpus.json only. Shared law keys: `ec-<n>-<year>` (enactment year, e.g. `ec-26-2000`), `ecr-<n>-1994`, `cf-1988`, `lei-<n>-<year>`; EC label format "Emenda Constitucional nº 26, de 2000". fetch.py (get/wayback/cdx/pick) and parse.py (raw/decode/blocks_of/analyse/norm/label_of/amendments/vigencia) are importable helpers.

## Checklist

- [x] Read brief, memory/git_for_law.md, SCHEMA.md, PLAN.md
- [x] Probe (Planalto live blocked; Wayback id_ works)
- [x] fetch.py; sources.json pins every capture (cf, cf-compilado, quadro-emc, emc-1..141, ecr-1..6, lcp-200); all cached
- [x] parse.py for CF/88 -> corpus.json (122 versions, 139 laws incl. cf-1988 and stf-adi-7047), 0 parse problems
- [x] Test build in .tmp-build: 142 commits, 261 tags, 0 unexplained, check.py 0 mismatches; autopush pushed `preview` f77a78c
- [x] 22 remaining unit differences vs constituicaocompilado.htm are typesetting differences between the two Planalto pages; listed automatically in the corpus decisions (diff_summary)
- [x] PUBLISH created 18:03Z; autopush pushed main 51ebcfa (143 commits incl. docs), check 0 mismatches
- [x] Determinism: parse.py twice gives identical corpus.json (sha256 01bc01c7… before the ADI 101 credit); build --compare identical (scratch dir deleted afterwards: autopush wip chokes on nested .git, ISSUES.md #1)
- [x] repo/README.md (English then pt), repo/LICENSE, repo/jurisdiction.json, repo/tools/vigente_em.py
- [x] Extra rules: `article` (no-note line in an article inserted after 1988 takes the article's date), `same-day-twin` (art. 246 by EC 6 and EC 7); ADI 7047 also credited to ADCT art. 101 (words unchanged)
- [x] Sanity check over all versions: every article unit has exactly one caput line, no doubled labels
- [x] futuro: EC 141 art. 7 XV from 2026-12-16 (FUTURE table; wording read from emc141 page). corpus: 123 versions (122 main + 1 futuro); parse deterministic (sha a7db09a9…); --compare identical
- [x] EC 132 future text (see Phase 2 section)
- [ ] Optional: LexML probe, legislacao-br reconciliation (prior art, read-only)

## Phase 2 (coordinator 18:2xZ): CP, then CPC, then CLT -> corpus.d/60-phase2.json (+ corpus.d/60-phase2.PUBLISH when verified)

- Do not touch corpus.json (CF) or corpus.d/50-codes.json (helper). Pre-1970 dates: builder clamps commit dates, real date in In-force trailer.
- Scripts: fetch_phase2.py / parse_phase2.py = copies of the helper's codes/fetch_codes.py / codes/parse_codes.py (generic Planalto act replay incl. MPs, LINDB, staged clauses), with ACTS/ACT_DAY/ACT_LAWS for my acts, hand tables emptied, sources in sources_phase2.json (law pages already pinned by the helper are reused at the same capture). Fix made: unclosed <a href> no longer leaks across <p> (CP page has one).
- [x] Pages pinned+fetched: cp del2848.htm (annotated, 980 strikes) 20261020142644, cp-compilado 20261026202755, cpc l13105.htm 20261023070835, clt del5452.htm 20261022194436, clt-compilado 20261019225805
- [x] Size fix (coordinator): corpus.json now writes `changes` deltas after the first version (58 MB -> 1.9 MB, check 0 mismatches); parse_phase2 does the same (to_deltas). Helper's 50-codes (46 MB) still full snapshots: tell coordinator/helper.
- [x] parse_phase2: CENTER_HEADINGS=False for CP (alignment unreliable; headings = Parte/Título/... lines, name line after, all-caps); rubricas (marginal headings, no label, no closing punctuation) moved into the next article as first line, label 'rubrica'.
- [x] CP DONE: corpus.d/60-phase2.json (751 KB, 111 versions 1942-2026, 112 laws), 0 problems, 25 typesetting-only diffs vs del2848compilado.htm (listed in decisions), check 0 mismatches, --compare identical, part sha 2b9b2288…; corpus.d/60-phase2.PUBLISH written 19:15Z. Rules added: REWRITES (Lei 7.209/1984 Parte Geral), run-revoked, heads, date-order, VETO_PROMULGATION (13.964: 2021-04-30), unstruck Parágrafo único, article start clamp, renumbered-same-text, months rule (pre-LC107 Lei 810), clause matching without spaces/number words, UTF-16 pages, whole-struck law pages.
- [ ] OLD NOTE (superseded): CP: 3509 paragraphs, 111 laws cited; `fetch_phase2.py laws cp cp-compilado` running (log .cache/phase2-laws-cp.log); next `parse_phase2.py --stats --dry`, fix problems, VIGENCIA_FIXED for staged/odd clauses (Lei 7.209/1984: 6 months), decisions text (write_part still has CC wording: rewrite), then write part, test build, PUBLISH file
- CLT moved to helper gitlaw-BR-clt (corpus.d/70-clt.json): do not start it.
- [x] CPC DONE: l13105.htm (annotated) vs l13105compilada.htm (consolidated, pinned as cpc-compilada); 18 versions from 2016-03-18; Lei 13.256/2016 in force the same day -> SAME_DAY_LAWS + 'same_day' version + same-day matching rule; 1 diff (compilada misplaces art. 1.041 § 2º). Part now 1.5 MB, 129 versions (sha fd5f5d78…); full test build 347 commits, 5 acts, check 0 mismatches, history identical on --compare (main tip differs only because --compare writes verification.json, as the helper noted). PUBLISH text updated for CP+CPC.
- [x] repo/README.md + jurisdiction.json list CF, CC, LGPD, CP, CPC (CLT row to add when the CLT helper's part is published); tools/vigente_em.py picks 3- or 4-digit article files
- [x] EC 132 futuro DONE in parse.py (EC132_STAGES: 2027-01-01 art. 3 + art. 22 I revocations; 2033-01-01 arts. 4, 5 + art. 22 II revocations; wording read from emc132 page, placed by label path; line_paths/ec132_changes/apply_ec132). corpus.json: 125 CF versions (122 main + 3 futuro: EC 141 2026-12-16, EC 132 2027, 2033); deterministic (sha 0260fdd6…); test build 349 commits, check 0 mismatches.

## Endpoints

- Planalto pages only via `https://web.archive.org/web/<ts>id_/https://www.planalto.gov.br/ccivil_03/<path>`; capture discovery fetch.pick() (CDX).
- constituicao/constituicao.htm (annotated, struck history) ts 20261026203643; constituicaocompilado.htm (check) ts 20261022115717; emendas/emc/quadro_emc.htm (EC enactment + DOU dates); emendas/emc/emcNN.htm (2-digit below 10); emendas/ecr/ecrN.htm; leis/lcp/lcp200.htm.
- STF case pages work live: portal.stf.jus.br/processos/abaDecisoes.asp?incidente=N and abaAndamentos.asp (ADI 7047 = incidente 6318731).

## How parse.py rebuilds CF/88 (details in docstring and corpus decisions)

- Struck = superseded. Paragraph start = in-force day of its note's amendment; struck end = "Revogado pela" note, else next wording with same label in the same article (search stops at a higher-level label), else rules: `duplicate` (struck copy of later identical unstruck text, never shown), `renumbered` (Parágrafo único -> unannotated § 1º, dated by the § 2º's Incluído note), `parent` (falls with nearest struck enclosing dispositivo), HEADING_RENAMES (verified against EC text), COURTS (ADI 7047: art. 100 § 11 expression, DJE ata 2023-12-04).
- End counts: successor 463, parent 232, note 54, duplicate 9, heading-rename 7, renumbered 4, court 1.
- In-force: vigencia() reads each EC's closing clause: publication (most), promulgation (EC 19, 33, 58, 95), fixed (EC 14, 25, 78, 105, ECR 5), no clause -> LINDB pub+45 (EC 2-9, 12, 13, 15, 16, 42, 72, 77, 90). Provision overrides: EC 109 art. 29-A 2025-01-01; EC 114 art. 100 § 5º 2022-01-01; EC 126 revocation of ADCT 106-114 = 2023-08-31.
- Future text is not in Planalto's CF page; EC 141 art. 7 XV added from the EC page (FUTURE table); EC 132's 2027/2033 changes not modelled (noted in decisions).

## Coordinator rules

- Never kill a process you did not start; stop only your own background tasks by id.

## Gotchas

- Python urllib TLS fails: curl only.
- Heredoc Python edits mangle regex escapes (a literal backspace got into parse.py once): use the Edit tool for regex lines.
- Wayback captures can be bot pages: "Acesso Negado" (814 B) and F5 "Please enable JavaScript" (~5 KB). emc-4/emc-13 pinned to 2017 captures, ecr-5/ecr-6 to 2016.
- CDX `length` is the compressed size.
- corpus.json ~58 MB (122 full snapshots); autopush skips files > 50 MB from wip.

## Cache

.cache/: ~10 MB, ~400 requests in .cache/requests.jsonl.

- [x] Coordinator job: repo/README.md and repo/jurisdiction.json now list the CLT (70-clt.json) and the CPP and CDC (80-proc.json): table rows, check results, STF rulings, MPs, CLT's 60 undated struck lines and 72 open replay problems in 'What it does not show', sources (STF ADIs, LexML), Portuguese summary. Parts not touched. Stopped here as instructed.

## Pushed (autopush)

19:30Z: main 9e7b1fc (347 commits, 5 acts, 328 versions), futuro a37ebf6 (EC 141 + EC 132 2027/2033; same hash as my local test build), check 0 mismatches. Later README/jurisdiction edits trigger one more rebuild.

18:14Z: main bb1169a (220 commits, 3 acts: CF/88 + the helper's codes from corpus.d), futuro c44c5bd, 411 tags; check 0 mismatches.

## Open issues

ISSUES.md: (1) autopush wip fails on a nested .git in a non-skipped scratch dir; (2) build.py does not name an unchanged-but-credited unit when the same law also changes words.

Coordination: PUBLISH covers the merged corpus, so once the helper writes corpus.d/50-codes.json its acts go to main too; the helper must verify its acts before writing the part file (or the coordinator should gate it).

## Lei 8.112/1990 (helper gitlaw-BR-8112, 2026-10-29)

Done as its own part: corpus.d/95-rju.json + 95-rju.PUBLISH, scripts in rju/ (imports batch3 with BATCH3_RJU=1; 90-batch3.json untouched, still sha 7b69bebb…). 56 versions, check 0 mismatches, --compare identical. Details: rju/PROGRESS.md.

## Coordinator (2026-10-29)
repo/README.md table now lists the CTN, ECA, Código Eleitoral and Lei 8.112. jurisdiction.json not yet updated.

## Batch 4: Lei 11.101/2005 and Lei 9.099/1995 (helper gitlaw-BR-4, 2026-10-29)

Own part corpus.d/97-batch4.json + 97-batch4.PUBLISH, scripts in batch4/ (imports batch3 -> proc, like rju/). LRF 9
versions, JEC 13; merged test build 821 commits, 14 acts, check 0 mismatches, 0 trailer errors, --compare identical;
the 12 earlier acts byte-identical. README table rows added; jurisdiction.json not updated. Details: batch4/PROGRESS.md.

## Batch 5 / 5b (alan-dell agent, 2026-10-29 late)

98-batch5 (Lei 14.133/2021) and 99-batch5b were missing after the restore and were rebuilt; 99-batch5b now holds
Marco Civil, Lei Anticorrupção, Lei de Drogas, Lei de Arbitragem, Lei do Inquilinato and Lei de Mediação. Improbidade,
Crimes Ambientais, LAI and Lei 9.784 are deferred (open in-force days). Details, checks and how to rerun:
batch5/PROGRESS.md. Scripts in batch5/ and batch5b/ (acts chosen by env BATCH5B_ACTS).

## Batch 6+ (gitlaw-BR-batch6 agent on alan-dell, 2026-10-31)

99-batch6 = the four acts batch 5b deferred (Improbidade, Crimes Ambientais, LAI, Lei 9.784), dates settled from the
Chamber's records of the retificações and the Senate's Ato Declaratório on MP 62/2002; 41 versions, check 0/0,
--compare identical, 99-batch6.PUBLISH written. Next parts 99-batch7, ... Details: batch6/PROGRESS.md.
99-batch7 (8 acts: Estatuto da Cidade, Pessoa Idosa, LEP, Lei das S.A., LC 182, Maria da Penha, LRF, Mandado de
Segurança; 132 versions) PUBLISHed 2026-10-31; batch6 republished after a Lei 9.605 art. 25 fix. Desarmamento and Lavagem
deferred. Details: batch6/PROGRESS.md.
2026-10-31 ~02:30Z: stale-wording fix (batch7/stale_fix.py) applied to 50/60/70/80/90/95/98/99-batch5b/99-batch7, all
re-verified and PUBLISHed; 10 CLT units stay open (in its decisions). Older parts now rebuild via batch7/oldparts.py.

## Batch 8 (gitlaw-BR agent, 2026-10-31)

99-batch8 PUBLISHed ~04:10Z: Lei de Lavagem and Estatuto do Desarmamento (batch 7's deferred acts, MP/STF chains set by
hand) plus Crimes Hediondos, LINDB, Organizações Criminosas, Propriedade Industrial, Direitos Autorais, Estatuto da
Juventude, Lei Geral do Turismo, Estatuto da Pessoa com Deficiência: 10 acts, 109 versions; merged scratch build 43 acts,
1158 versions, check 0/0, --compare identical. Lei da Ação Civil Pública deferred. Details: batch8/PROGRESS.md.
99-batch9 PUBLISHed ~05:00Z: LDB, Lei Orgânica da Saúde, Lei das Eleições (130 versions); merged scratch build 46 acts,
1288 versions, check 0/0, --compare identical. CTB, Código Florestal, Registros Públicos, Lei 8.666 configured in batch9
but deferred (reasons in batch9/PROGRESS.md).
99-batch9 re-PUBLISHed ~06:10Z with Lei 8.666/1993 (repeal version 30.12.2023) and Lei da Ação Civil Pública: 5 acts,
177 versions; merged 48 acts, 1335 versions, check 0/0. repo/jurisdiction.json updated to the 48 acts.
99-batch9 re-PUBLISHed ~07:30Z with Código de Trânsito, Código Florestal and Registros Públicos: 8 acts, 338 versions;
merged 51 acts, 1496 versions, check 0/0, --compare identical. jurisdiction.json updated (51 acts).

## Batch 10 (gitlaw-BR agent, 2026-10-31)
Pin scan of all older parts (batch10/.tmp/pinscan.py): 5 bad pins fixed in codes/, clt/, batch3/, batch5/ pin files
(MP 75/2002 and Lei 3.807 bot pages; Lei 15.452, MP 765/2016, MP 922/2020 pinned to other acts' pages). Only 99-batch9
changed in content (CTB art. 326-C now from 1.7.2026, Lei 15.452's real day) and 50-codes in its request count; both
re-PUBLISHed ~03:35Z (merged 51 acts, 1496 versions, check 0/0, --compare identical). Details: batch10/PROGRESS.md.
99-batch10 PUBLISHed ~03:45Z: Lei de Concessões, Lei das PPPs, Lei de Abuso de Autoridade, LC 64/1990 (Inelegibilidades),
Lei 8.142/1990, Lei Geral do Esporte (44 versions); merged 57 acts, 1540 versions, check 0/0, --compare identical.
jurisdiction.json and README updated (57 acts). Saneamento, Petróleo, Estatuto dos Militares, PNMA, Estatuto do Torcedor
configured, next. Details: batch10/PROGRESS.md.
99-batch10 v2 re-PUBLISHed ~03:55Z: + Estatuto dos Militares and Estatuto do Torcedor (repealed 2023): 8 acts, 68
versions; merged 59 acts, 1564 versions, check 0/0, --compare identical; jurisdiction.json and README (59 acts).
99-batch9 re-PUBLISHed ~04:05Z: LDB art. 36-B doubled incisos 2008-2023 fixed (found by batch10/.tmp/dupline.py).
~04:35Z: 99-batch10 v3b (+ Lei do Saneamento Básico, PNMA; 10 acts, 99 versions; merged 61 acts, 1595 versions, check 0/0)
and 70-clt (duplicate-line review fixes) re-PUBLISHed. Lei do Petróleo deferred (Lei 12.734 promulgation of vetoed parts,
MP 592). Quoted-amendment closing lines misfiled into the next article across older parts: reported, not fixed.
~09:40Z: quoted-amendment closing-line fix moved into the shared parsers (proc/parse_proc.py, parse_phase2.py, clt/parse_clt.py); 9 parts regenerated, re-verified and re-PUBLISHed. Lei do Petróleo added to 99-batch10 (Lei 12.734's vetoed art. 3/4 promulgated DOU 15.3.2013, MP 592 overlap modelled): merged 62 acts, 1637 versions, check 0/0, --compare identical. New finding (not fixed): quoted articles without an opening quote read as the act's own units (Hediondos, LOC art. 288, LBI art. 1.783-A, Lei 14.133 arts. 337-E..P). Details: batch10/PROGRESS.md sections 6-7.
Later 10-31: quotation-state fix in the shared parsers (proc, phase2, clt, codes): quoted articles without an opening quote no longer become units (LLC art-337-e..p, Hediondos art-159..270, LOC art-288, LBI art-1783-a gone, lines kept in the amending article); 98-batch5 and 99-batch8 re-PUBLISHed, merged check 0/0, compare identical. batch10/PROGRESS.md s. 8.
Batch 11 (2026-10-31): 99-batch11 PUBLISHed: LEF, Lei 12.529 (CADE), EOAB, Lei 9.868, Lei 9.882, Lei 8.137, Lei 9.296, Lei 8.009, Lei 4.717, Lei 7.492 (55 versions); merged 72 acts, 1692 versions, check 0/0, --compare identical. Lei 9.656, 6.385, 6.766, 8.742 configured, deferred. Details: batch11/PROGRESS.md.
Batch 12 (2026-10-31): 99-batch12 PUBLISHed: Lei 6.766, LOAS 8.742, Lei 6.385 (with Decreto 3.995/2001 as a decree law), 72 versions. Lei 9.656 NOT built (MP 1.665->2.177-44 chain wordings not on Planalto; ADI 1.931 dates). Staged-clause misdating fixed in 99-batch8/9/10 (Leis 13.097, 14.183, 14.382). Merged 75 acts, 1765 versions, check 0/0, --compare identical. Details: batch12/PROGRESS.md.
Batch 12 update: Lei 9.656 added to 99-batch12 from 27.8.2001 (oldest version available; MP 1.665 chain not modelled; ADI 1.931 open item). Merged 76 acts, 1781 versions, check 0/0, --compare identical.
Batch 13 (2026-10-31): small parts 99-batch13a, b, ... (2-4 acts each). 99-batch13a PUBLISHed: Lei das Contravenções
Penais, Lei 1.079/1950, Lei 7.716/1989 (24 versions); merged 79 acts, 1805 versions, check 0/0, --compare identical.
99-batch13b PUBLISHed: Lei de Greve, LC 150/2015, Lei 6.019/1974 (12 versions); merged 82 acts, 1817 versions, check 0/0.
99-batch13c PUBLISHed: Lei 4.591/1964, Lei 9.514/1997, DL 911/1969 (39 versions); merged 85 acts, 1856 versions, check 0/0.
99-batch13d PUBLISHed: Lei das Estatais, Lei dos Partidos Políticos (20 versions); merged 87 acts, 1876 versions, check 0/0. Lei 4.320/1964 deferred.
99-batch13e PUBLISHed: Lei de Migração, Lei 9.474/1997, Lei Antiterrorismo, Lei 7.960/1989 (6 versions); merged 91 acts, 1882 versions, check 0/0.
99-batch13f PUBLISHed: Lei 4.595/1964 (SFN), Lei do Cheque (28 versions); merged 93 acts, 1910 versions, check 0/0. FGTS deferred.
99-batch13g PUBLISHed: Lei das Duplicatas, Lei 8.935/1994, Lei Orgânica do TCU, Lei 10.259/2001 (26 versions); merged 97 acts, 1936 versions, check 0/0.
99-batch13h PUBLISHed: Lei 12.153/2009, Lei 8.038/1990, Lei de Alimentos, PNRS (13 versions); merged 101 acts, 1949 versions, check 0/0.
Details: batch13/PROGRESS.md.
Batch 14 (2026-10-31): small parts 99-batch14a, b, ... 99-batch14a PUBLISHed: Lei Kandir (LC 87/1996) and LC 116/2003 (ISS), both repealed 1.1.2033 by LC 214/2025 on futuro (25 versions); merged 103 acts, 1974 versions, check 0/0, compare identical. Details: batch14/PROGRESS.md.
99-batch14b PUBLISHed: Lei 9.433/1997, DL 201/1967, LGT 9.472/1997, Lei 1.521/1951 (35 versions); merged 107 acts, 2009 versions, check 0/0.
99-batch14c PUBLISHed: SNUC, Lei da Liberdade Econômica, Estatuto da Igualdade Racial (15 versions); merged 110 acts, 2024 versions, check 0/0.
99-batch14d PUBLISHed: Estatuto da Terra (12 versions, DL 2.431/1988 and its 1989 rejection modelled); merged 111 acts, 2036 versions, check 0/0.
99-batch14e PUBLISHed: LC 123/2006 (13 versions from the 2012 republication, oldest available; LC 214 art. 543 V partial repeal 2033 on futuro); merged 112 acts, 2049 versions, check 0/0.
State at handoff (batch 14): parts 99-batch14a..e installed with .PUBLISH (12 acts, 100 versions; merged 112 acts, 2049 versions, 1732 commits, check 0/0). README rows + jurisdiction.json (112 acts) current. No background processes left running. Next: Leis 8.212/8.213 (groundwork, pins and MP lapse days in batch14/PROGRESS.md), CBA 7.565 (264 problems), FGTS and Lei 4.320 (batch 13 deferred).
Effect-day rule applied 2026-10-31 (coordinator): changes whose act fixes a later 'produção de efeitos' day are dated by that day (scripts/brazil-law/effects_fix.py, a post-step to rerun after regenerating any part); 116 unit-moves in corpus.json (CF), 50, 90, 95, 99-batch5b/6/7/10/11/14a/14e; decision wording in 12 more parts; merged 112 acts, 2056 versions, 1744 commits, check 0/0, compare identical, audit clean; PUBLISH files appended. Details and judgement calls: batch14/PROGRESS.md. Leis 8.212/8.213 go to a fresh agent.
Batch 15 (2026-10-31): 99-batch15a (Lei 8.212/1991, 114 versions) and 99-batch15b (Lei 8.213/1991, 95 versions) PUBLISHed: MP 905/955 sequence ported from the CLT parser (mp_pairs in parse_batch15.py), 1998 footnote markers dropped, headings/tables/22A-25A layout fixed, 1991 text of five 8.212 articles read from L8212orig.htm, Senate resolutions 26/2005, 10/2016, 15/2017, effect days via effects_fix.py (new MOVES for both parts; 18 unit-moves). Merged 114 acts, 2265 versions, 1861 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (114 acts). Open: MP 871/2019 art. 74 § 3º wording (not printed), Vide ADI pointers. Details and judgement calls: batch15/PROGRESS.md. Next: CBA 7.565 (264 problems), FGTS, Lei 4.320.
Batch 16 (2026-10-31): 99-batch16a PUBLISHed: Código Brasileiro de Aeronáutica (Lei 7.565/1986, 19 versions; MP 1.089/2021 -> Lei 14.368/2022 conversion-child rule, MP 714/2016 vetoed changes, MP 1.240/2024 lapse); merged 115 acts, 2284 versions, 1876 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (115 acts). Details: batch16/PROGRESS.md.
99-batch16b PUBLISHed: Lei do FGTS (Lei 8.036/1990, 51 versions; MP 905/955 model, Lei 13.932/2019 staged clauses by provision, MP 2.216-37 art. 3 wording, MP 1.336/2026 lapse); merged 116 acts, 2335 versions, 1909 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (116 acts).
99-batch16c PUBLISHed: Lei 4.320/1964 (6 versions; 'Artigo NN.' labels, veto-override notes, scheme lines, DL 1.939/1982 effect day 1.1.1983 via a new effects_fix MOVES entry); 99-batch16a re-PUBLISHed (decision text fix). Merged 117 acts, 2341 versions, 1914 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (117 acts).
99-batch16d PUBLISHed: Lei de Tortura, Lei do Genocídio, Lei do Mandado de Injunção, Lei do Habeas Data (6 versions); merged 121 acts, 2347 versions, 1918 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (121 acts).
99-batch16e PUBLISHed: Estatuto do Índio, Lei das Cooperativas, Lei da Reforma Agrária (22 versions); merged 124 acts, 2369 versions, 1930 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (124 acts).
99-batch16f PUBLISHed: Lei do Seguro-Desemprego 7.998/1990 (20 versions; MP 905/955, MP 665/2014 staged, LC 155 effect day via effects_fix); merged 125 acts, 2389 versions, 1938 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (125 acts).
99-batch16g PUBLISHed: MROSC Lei 13.019/2014 (5 versions; in force 23.1.2016, pre-in-force amendments as the first day's 'same_day' version). State at handoff (batch 16): 99-batch16a..g, 15 acts, 129 versions; merged 126 acts, 2394 versions, 1941 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (126 acts). No background processes left running. Details and next candidates: batch16/PROGRESS.md.
Batch 17 (2026-10-31): small parts 99-batch17a, b, ... 99-batch17a PUBLISHed: Lei do Trabalho Rural 5.889/1973, Lei 4.090/1962 (13º salário), Lei 605/1949 (repouso semanal), Lei do Vale-Transporte 7.418/1985 (29 versions; Lei 7.619/1987 article renumbering rebuilt, MP 905's headings on the Lei 605 page left out, Lei 9.532 effect day via effects_fix); merged 130 acts, 2423 versions, 1957 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (130 acts). Details: batch17/PROGRESS.md.
99-batch17b PUBLISHed: Lei 9.029/1995, Lei do Software 9.609/1998, Lei das Organizações Sociais 9.637/1998 (MP 850/2018 rejected 12.2.2019), Lei das OSCIPs 9.790/1999 (14 versions); merged 134 acts, 2437 versions, 1966 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (134 acts).
99-batch17c PUBLISHed: Lei 1.060/1950, Lei 9.492/1997, Lei 6.024/1974, Lei 12.037/2009 (30 versions); merged 138 acts, 2467 versions, 1982 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (138 acts).
99-batch17d PUBLISHed: Lei de Biossegurança 11.105/2005, Lei do Planejamento Familiar 9.263/1996 (vetoed parts promulgated 20.8.1997), Lei 11.419/2006 processo eletrônico (9 versions); merged 141 acts, 2476 versions, 1989 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (141 acts).
99-batch17e PUBLISHed: Lei da Mobilidade Urbana 12.587/2012 (13 versions; MP 748 lapse, MP 818/906 chain on art. 24); merged 142 acts, 2489 versions, 1999 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (142 acts).
99-batch17f PUBLISHed: Lei da Faixa de Fronteira 6.634/1979 (Lei 14.004 vetoed part promulgated 8.9.2020), Lei 9.469/1997, Lei de Segurança do Tráfego Aquaviário 9.537/1997 (16 versions); merged 145 acts, 2505 versions, 2008 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (145 acts).
99-batch17g PUBLISHed: Lei do Susp 13.675/2018 (Lei 14.531 vetoed parts promulgated 19.7.2023), Lei do Mercado de Capitais 4.728/1965 (Lei 14.754 effect day 1.1.2024 via effects_fix) (24 versions); merged 147 acts, 2529 versions, 2025 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (147 acts).
99-batch17h PUBLISHed: Lei 7.689/1988 (CSLL) and Lei 9.249/1995 (35 versions; MP effect days by hand, 14 effect-day moves, Lei 15.525/2026 changes on futuro 2027/2030, Lei 7.689 art. 8 left out: Senate resolution 11/1995 not available); merged 149 acts, 2564 versions, 2048 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (149 acts).
99-batch17i PUBLISHed: Lei 9.250/1995 (IRPF, 35 versions; MP 644/2014 and MP 1.171/2023 lapses, 17 effect-day moves); merged 150 acts, 2599 versions, 2071 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (150 acts). NOTE: data.commoncrawl.org and arquivo.pt robots.txt Disallow the paths used; fetch via batch17/.tmp/iaonly.py (archive.org only).
99-batch17j PUBLISHed: Lei 7.713/1988 (IR, 43 versions; MP 1.251/2024 lapse, 1989 MP 68/114 effect days, 20 effect-day moves); 99-batch17i re-PUBLISHed (decision wording); merged 151 acts, 2642 versions, 2101 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (151 acts).
99-batch17k PUBLISHed: Lei 9.430/1996 (69 versions; Lei 12.715/12.766 and 11.727 provision days, MP 252/478/303/75 chains, Lei 14.596 in force 1.1.2024, 8 effect-day moves, Lei 15.525 2030 on futuro); merged 152 acts, 2711 versions, 2136 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (152 acts).
99-batch17l PUBLISHed: Lei 13.465/2017 (REURB, 8 versions; vetoed parts promulgated 8.9.2017 modelled); merged 153 acts, 2719 versions, 2138 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (153 acts).
99-batch17m PUBLISHed: Lei 11.977/2009 (Minha Casa, Minha Vida, 39 versions; MP 478/2009 lapse, Capítulo III revoked by MP 759/2016 with earlier wordings ended by their successors, revocations from 31.12.2011, MP 1.382/2026 pending); merged 154 acts, 2758 versions, 2158 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (154 acts).
99-batch17n PUBLISHed: Lei do Estágio 11.788/2008, Lei da Alienação Parental 12.318/2010, Lei 10.048/2000 (atendimento prioritário), Lei dos Alimentos Gravídicos 11.804/2008 (10 versions); merged 158 acts, 2768 versions, 2165 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (158 acts).
99-batch17o PUBLISHed: Lei dos Consórcios Públicos 11.107/2005, Lei da Acessibilidade 10.098/2000 (11 versions); merged 160 acts, 2779 versions, check 0/0, --compare identical, audit clean.
99-batch17p PUBLISHed: Lei do ProUni 11.096/2005 (Lei 14.350/2022 effects from 1.7.2022), Lei de Cotas 12.711/2012, Lei 13.431/2017 (15 versions); merged 163 acts, 2794 versions, 2183 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (163 acts). Re-check MP 1.382/2026 (Lei 11.977, part m) after its term ends about 28.11.2026.
99-batch17q PUBLISHed: Lei 10.522/2002 (Cadin, 32 versions; MP 1.160/2023 lapse, art. 20-D promulgated 18.4.2018, art. 11 §§ 1º-3º restored by Lei 11.941; art. 32 quoted § 2º left out, ADI 1.976 undated); merged 164 acts, 2826 versions, 2192 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (164 acts). Lei 10.931/2004: no archive.org capture, not built.
99-batch17r PUBLISHed: Lei 9.873/1999 and Lei do Pregão 10.520/2002 (repealed 30.12.2023 by Lei 14.133, read from a pre-repeal capture) (9 versions); 99-batch17q re-PUBLISHed (decision wording); merged 166 acts, 2835 versions, check 0/0, --compare identical, audit clean; README + jurisdiction.json (166 acts).
99-batch17s PUBLISHed: Lei 12.783/2013 (16 versions; MP 612/2013 and MP 1.232/2024 lapses); 99-batch17t PUBLISHed: Lei dos Portos 12.815/2013 (7 versions); merged 168 acts, 2858 versions, 2206 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (168 acts).
99-batch17u PUBLISHed: Lei 9.074/1995 (25 versions; MP 612/2013 and MP 1.065/2021 lapses, MP 1.300/2025's changes ended by its conversion Lei 15.235 on 9.10.2025); merged 169 acts, 2883 versions, 2220 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (169 acts).
99-batch17v PUBLISHed: Lei 12.462/2011 (RDC, 25 versions; arts. 1-47-A revoked 30.12.2023 by Lei 14.133; art. 63 § 17 (MP 1.349/2026, lapse day unread) left out); merged 170 acts, 2908 versions, 2231 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (170 acts).
99-batch17w PUBLISHed: Lei 10.233/2001 (ANTT/ANTAQ/DNIT, 38 versions; MP 800/2017 lapse, MP 2.217-3/2001 edition, MP 155/2003 -> Lei 10.871, MP 1.065/2021 vs Lei 14.273/2021 settled by provision, art. 88-A from its promulgation 11.12.2019); 99-batch17v re-PUBLISHed: Lei 12.462 art. 63-B's five-year term (Lei 14.901 art. 5) ends on 26.6.2029 on futuro; 99-batch17x PUBLISHed: Lei 13.848/2019 (agências reguladoras) and Lei 9.986/2000 (13 versions; MP 1.181/2023 lapse). Merged 173 acts, 2960 versions, 2259 commits, check 0/0, --compare identical, audit clean; README + jurisdiction.json (173 acts).
Leis 9.961/2000 (ANS) and 9.717/1998 (RPPS) configured as part y, NOT published: their pages credit individual reissues of pre-EC-32 MPs (2.177-43/-44, 2.097-36/-40, 2.187-12/-13 ...), which the reader keys by number and year; needs edition-level MP keys (details in batch17/PROGRESS.md).
MP edition reader (2026-10-31, eighth batch-17 session): batch6/parse_batch6.py keys every pre-EC 32 MP edition a note names (other than the pinned one) as mp-<n>r<e>-<y>, dated by its own page/DOU day; stacked edition notes start with the earliest edition whose page carries the words; an edition's struck wording the next edition dropped ends on that edition's day. All 53 batch 6-17 parts reparse byte-identical (0 units moved; the 21 crediting pre-EC32 editions got a PUBLISH line). 99-batch17y PUBLISHed: Lei 9.961/2000 (ANS) and Lei 9.717/1998 (RPPS), 18 versions; merged 175 acts, 2978 versions, check 0/0, --compare identical, audit clean. Lei 9.656 not extended (only 'Vide' pointers to earlier editions). Details: batch17/PROGRESS.md.
