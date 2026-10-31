CHECKPOINTED 2026-10-28 (after README update for CLT/CPP/CDC)

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
Details: batch13/PROGRESS.md.
