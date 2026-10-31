# Brazil batch 6+ progress (gitlaw-BR-batch6 agent on alan-dell, 2026-10-31)

Owns only `scripts/brazil-law/batch6/` (and later `batch7/`, ...), `corpus.d/99-batch6.json` (+ `.PUBLISH`) and later
parts `corpus.d/99-batch7.json`, ... Never commits or pushes (autopush publishes PUBLISHed parts under the standing yes).
Claim: scripts/world-law/claims/brazil-law.txt. Scratch builds go OUTSIDE the main repo:
`~/Documents/.gitlaw-scratch/brazil-b6` (build) and `brazil-b6c` (--compare).

## 99-batch6: the four acts batch 5b deferred - DONE, PUBLISH written 2026-10-31 ~00:25Z

- LIA (Lei 8.429/1992) 14 versions, LCA (Lei 9.605/1998) 19, LAI (Lei 12.527/2011) 4, LPA (Lei 9.784/1999) 4.
- Dates settled from official records (Chamber of Deputies' Legislação Informatizada, read from archive copies, pinned
  as `ctx:*` in sources_batch6.json):
  - Lei 9.605 retificação (DOU 17.2.1998) corrects only the heading -> LINDB 45 days from 13.2.1998 = 1998-03-30.
  - Lei 9.784 retificação (DOU 11.3.1999) corrects only signatures -> in force 1999-02-01, no text version.
  - Lei 13.019/2014 (LIA art. 10/11/23): 2016-01-23 (540 days; União/States), Municípios 2017-01-01 in decisions.
  - Lei 14.129/2021 (LAI art. 12): 2021-06-28 (90 days, União); States 2021-07-28, Municípios 2021-09-26 in decisions.
  - MP 62/2002 (LCA art. 25) 'Prejudicada': Ato Declaratório of the Senate President, 20.11.2002 -> back 2002-11-20.
- New generic rules in parse_batch6.py (wrappers over parse_proc/batch3/batch5b):
  - REISSUES: an MP reissue with its own wording gets its own key `mp-<n>r<k>-<year>` (MP 1.710-1/1998).
  - HEAD_NO_DE: MP headings 'DE 22 DE AGOSTO 2002' read with 'DE' for dates (MP 62/2002, MP 2.163-41/2001).
  - 'Prejudicada' after a struck wording read like '(Vigência encerrada)'.
  - WITH_WORDING: '(Incluído pela Lei X, com a redação dada pela Lei Y)' -> credited to Y from max(day X, day Y).
  - NEVER_IN_FORCE (hand table): LIA art. 10 XIX-XXI as 13.019 first wrote them (13.204 rewrote before in force).
  - MP_CHAINS: wording credited to first+last MP of a reissue chain starts with the first once the text is found on
    both MP pages (LIA art. 17 § 3º from MP 1.337/1996, § 5º from MP 1.984-16/2000).
  - EXPLAINED: LIA art-17 (§ 6º-A typesetting) and titulos ('Seção II-A' revoked placeholder on the compilada).
- Checks: parse twice identical (part sha256 f96caabd...); merged scratch build 894 commits, 1787 tags, 25 acts,
  check.py 918 versions 0 mismatches 0 trailer errors; --compare history identical (main differs by verification.json
  only, ISSUES #3).
- README rows for the 4 acts + a Câmara dos Deputados source row added to repo/README.md.

## How to rerun

    python -X utf8 scripts/brazil-law/batch6/fetch_batch6.py refetch <ids>        # pins in batch6/sources_batch6.json
    python -X utf8 scripts/brazil-law/batch6/parse_batch6.py --stats --dry
    python -X utf8 scripts/brazil-law/batch6/parse_batch6.py                       # writes corpus.d/99-batch6.json
    (BATCH6_ACTS=<slug,..> for trials, BATCH6_OUT=<file> to write elsewhere)

## Fix after first publish (2026-10-31 ~01:00Z)

99-batch6 reached main at 00:23Z with a wrong Lei 9.605 art. 25 (notes '(Renumerando do §2º para §3º ...)' were read as
text; §§ 3-4 missing before 2014). PUBLISH was pulled, fixed in parse_batch6 (NOTE_VERB_TYPOS decode fix; renum_pre adds
the old-label wording of a renumbered line when none is printed; renum_post restores a wording a lapsed MP replaced until
the renumbering; 'Prejudicada' after a note), re-verified (sha 70bee5ad, check 0/0, compare identical) and PUBLISH
rewritten. The standing yes covers the rewrite.

## 99-batch7 - DONE, PUBLISH written 2026-10-31 ~01:05Z (scripts in batch7/, imports batch6)

Estatuto da Cidade 19 versions, Estatuto da Pessoa Idosa 11, LEP 30, Lei das S.A. 31, Marco Legal das Startups 1, Maria da
Penha 23, LRF 15, Mandado de Segurança 2 (132). Part sha a230a200; merged scratch build 999 commits, 33 acts, check 0/0,
--compare identical. New rules in parse_batch7.py: LC title line read as 'LEI N', centred labelled lines kept in their
article, notes fixed in place (NOTE_FIX), stray link text, CONVERTED_FIX (MP 459), MP_LAPSE from Atos Declaratórios (MP
1.065/2021, 1.158/2023, 784/2017, 892/2019; pinned as ato:*), VIGENCIA_FIXED/PROVISION (11.638, 14.711, LC 178 arts. 51/42,
13.818 art. 289 -> 2022-01-01), next-wording rule for undated struck lines of recast lists, PLAIN_ENDS (LRF art. 51 § 1º),
successor-before-lapse. fetch_batch7.complete() also accepts UTF-16 pages (Lei 11.340).

Checks used for every part now: batch7/.tmp/dupcheck.py (same § / Parágrafo único / Art. twice in a unit, any version) and
batch7/.tmp/leakcheck.py (note words left in text). Run them before PUBLISH: self-checked acts (no compilada) can't catch
these otherwise.

Deferred (configured in batch7 ALL_ACTS, not in VERIFIED):
- Estatuto do Desarmamento (10.826/2003): 2007-08 chain MP 379 -> revoked by MP 390 -> MP 394 (no fate on its page) -> MP
  417 -> Lei 11.706; needs MP 390/394 fates from Congress records; also art. 35 referendum (2005) as a note.
- Lei de Lavagem (9.613/1998): art. 14/16 COAF chain (MP 870 -> Lei 13.844 dropped it; MP 886 -> Lei 13.901; MP 893
  revoked art. 16 on 20.8.2019 -> Lei 13.974); Lei 13.506 § 2º printed unstruck though revoked; label typo '2º' (MP 784).
- LexML (www.lexml.gov.br/urn/...) answered 503 to every request on 2026-10-31 ~00:50Z; batch7/fetch_lexml.py (5 s
  Crawl-delay) stopped. The parts use the DOU day Planalto prints; LexML would only cross-check it.

Other parts (not mine), dupcheck finds possible unended wordings: CLT 55 units, CP art-121/216/273/359-m, CPC art-0988/
1042, CPP art-035, CDC art-057, CTN art-071, ECA art-046/263, RJU art-068, Lei de Mediação art-44 (some are quoted
amendments). Worth a look by their owners.

## Next candidates

Lei 8.666/1993 (revoked 30.12.2023: needs an act-end), LINDB (del4657), Lei da Ação Civil Pública (7.347), Crimes Hediondos
(8.072), Código de Trânsito (9.503), LDB (9.394), Lei 8.080, Estatuto da Pessoa com Deficiência (13.146), Lei das Eleições
(9.504), Código Florestal (12.651), Lei de Registros Públicos (6.015), Lei 12.850, Lei 9.279, Lei 9.610, plus EDes/LLav above.

## Stale-wording fix across the older parts (coordinator task, 2026-10-31 01:10-03:00Z)

Problem: a duplicate-label check (batch7/.tmp/dupcheck.py, dupdetail.py, dupspan.py) found units where two wordings of
one dispositivo stood at once in some versions (CLT ~54 units, CP art. 216/272/273, CPC art. 988/1042 (2016-2026!),
CPP art. 35, CDC art. 57, CTN art. 71, RJU art. 68; later also LLC art. 193, LAC art. 16/30, CC art. 1.769, LRF art. 21).

Fix: batch7/stale_fix.py, rules applied to each act's final life spans just before build_act (each use in decisions):
- A: a wording ends no later than the next wording of the same dispositivo (also a same-day law, SAME_DAY_LAWS, or the
  act's own text replaced by a law in force on its first day); lines under it that ended with it end with it. Lines
  with gaps or pinned by the CLT's MP 905/955 model are left alone.
- B: twin wordings (same label, same parent label, same start, below a struck copy): word-for-word copies or unnoted new
  wordings start on the first day no other wording of that dispositivo (same parent) stands, or with the restored caput
  of the article; a struck lower copy that never stands alone, and an unended upper copy of a noted struck wording,
  are left out.
- D: unnoted unstruck line under an 'Incluído' parent starts with it, only where an older wording under the same label
  is printed struck (CLT art. 678, ECA art. 4; not ECA art. 91).
- G: an unstruck wording printed above a later struck MP wording that ended by conversion/lapse gets a gap (RJU 68).
- L: 'Artigo 896 - ...' read as the caput (CLT).
- Tried and dropped: a struck-block rule (dated unnoted struck lines by the struck caput above: wrong for CP art. 180 §§
  1-3, which Planalto prints once under the 1955 caput) and an identical-line rule (CPC art. 932 IV/V a), b) are legit).
How the older parts are rebuilt now: `python -X utf8 scripts/brazil-law/batch7/oldparts.py <50-codes|60-phase2|70-clt|
80-proc|90-batch3|95-rju>` (wraps the part's own parser; published source notes/ai_use from batch7/published_text.json,
which keeps the privacy-cleaned texts the parts were published with). batch5/5b/7 parsers apply the rules in their own
__main__ / module (BATCH5_OUT / BATCH5B_OUT env for trial output).
Cache: the older parts' archive.org pins were refetched (batch7/refetch_old.py, 734 pages, 0 failed); LexML records for
the parts that use them refetched one at a time 5 s apart (batch7/fetch_lexml.py; LexML answers 503 for some URNs).
Never run an older parser without an OUT override while investigating: a regenerated part in corpus.d is picked up by
autopush (one check failed at 01:37Z for that reason; nothing was pushed).
Open in CLT (listed in its decisions): arts. 530, 534, 538, 654, 693, 896, 902 (1940s-50s unnoted superseded blocks) and
553, 628-A, 634, 636 (days around MP 905/955). Today's text unaffected.

Deferred acts, facts found:
- Estatuto do Desarmamento: MP 379/2007 revoked by MP 390/2007 (converted, Lei 11.579/2007); MP 394/2007 (DOU
  21.9.2007, republished 24.9.2007): efficacy suspended by an STF liminar in ADI 3.964 (date still needed), declared
  prejudicada 7.2.2013 (Chamber record, archive copy); MP 417/2008 -> Lei 11.706/2008.
- Lei de Lavagem: COAF arts. 14/16 chain, see earlier notes.
Result (02:30Z): parts rewritten and PUBLISH re-verified: 50-codes, 60-phase2, 70-clt, 80-proc, 90-batch3, 95-rju,
98-batch5, 99-batch5b, 99-batch7 (99-batch6 unchanged). Merged scratch build 998 commits, 33 acts, 1049 versions,
check.py 0/0, --compare identical; replay checks of every part unchanged; duplicate check clean except the 10 open CLT
units. LexML: DL 6.109/1943 still 503 -> its published day 1943-12-18 kept as a hand entry in oldparts.py (80-proc).
Estatuto do Desarmamento and Lei de Lavagem still deferred (facts above).
