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

## Next: batch 7 (corpus.d/99-batch7.json, scripts in batch7/, importing batch6)

Planned: Estatuto da Cidade (10.257/2001), Estatuto da Pessoa Idosa (10.741/2003), LEP (7.210/1984), Lei das S.A.
(6.404/1976), Marco Legal das Startups (LC 182/2021), Maria da Penha (11.340/2006), Estatuto do Desarmamento
(10.826/2003), LRF (LC 101/2000), Mandado de Segurança (12.016/2009), Lavagem de Dinheiro (9.613/1998).
