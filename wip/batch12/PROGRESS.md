# Brazil batch 12 progress (gitlaw-BR agent on alan-dell, 2026-10-31)

Owns `scripts/brazil-law/batch12/` and `corpus.d/99-batch12.json` (+ `.PUBLISH`). Never commits or pushes. Scratch outside
the repo: `~/Documents/.gitlaw-scratch/brazil-b12` (trials, page texts, dumps), `brazil-vfix` (re-dated older
parts), merged build via batch10/.tmp/runbuild_rub.py. Tools: .tmp/run.py (BelowNormal), pagetxt.py, dump.py, cons.py.

## 99-batch12 - PUBLISHed 2026-10-31: Lei 6.766/1979, Lei 8.742/1993 (LOAS), Lei 6.385/1976 (72 versions, sha 007b576e)
- Lei 6.766: LABEL_FIX art. 4 'III-A. -'; WORD_FIX art. 22 § 1º leftover 'Parágrafo único.' (Lei 14.620 art. 24 keeps the
  p.u. as § 1º); 8 typesetting diffs EXPLAINED.
- LOAS: MP 1.164/2023 CONVERTED_FIX (page says 'Convertida na Lei 14.601' without 'nº'); MP 446/2008 rejected 10.2.2009
  (Ato do Presidente da Câmara, Planalto adc--mpv446.htm, pinned ato:adc-2009-mpv446) via MP_LAPSE + MP_REJECTED; Lei
  14.176 staged (23.6.2021 / 26-A..H 1.10.2021 / 20-B and art. 20 § 11-A 1.1.2022); Lei 14.601 20.6.2023; NOTE_FIX 'Lei
  9.720, de 26.4.1991'; art. 9 § 3º (MP 2.187-13 printed twice around MP 446) and art. 20 § 7º spans by hand; stray "'"
  after art. 20 § 14 dropped. 0 diffs vs compilado.
- Lei 6.385: decree support in parse_batch12 (law_key/law_label/page_info/lexml for key dec-3995-2001, kind decree):
  Decreto 3.995/2001 (DOU 1.11.2001), autonomous decree rewriting the matters vetoed in Lei 10.303/2001; NOTE_FIX
  'Redação pelo Decreto'; Lei 10.303's '(VETADO)' art. 9 §§ 3º-6º and art. 18 h) left out (SPAN_FIX skip, settled problems
  filtered); art. 9 § 4º decree span to MP 784; art. 9 caput 1976 wording read from l6385original.htm (ctx:lcvm-original),
  placed struck above the decree's (otherwise the article rule dated all of art. 9 from 2001); art. 17-A note word. 1 diff
  (consolidated stray quote) EXPLAINED.

## Lei 9.656/1998 (planos de saúde) - NOT built, reasons
- MP chain: from 5.6.1998 (MP 1.665, before the act's own entry into force on 2.9.1998) to 27.8.2001 the act was rewritten
  by ~44 monthly reissues (1.665, 1.685-x, 1.730-x, 1.801-x, 1.908-x, 1.976-x, 2.097-x, 2.177-x). Planalto's annotated page
  prints only the 1998 text (struck) and MP 2.177-44's wording, with 'Vide MP ...' notes: the replay would show the 1998
  text standing until 27.8.2001, which is false for every unit the chain touched. Options: (a) start the history at
  27.8.2001 as 'oldest version available' (first_law null, earlier_laws the chain) - clean and true, loses 1998-2001;
  (b) model each reissue from its own MP page (~44 pages, quoted-amendment parsing) - large.
- ADI 1.931: the STF's cautelar (2003) suspended art. 35-E and the merits ruling (2018) struck art. 35-E and the words
  'atuais e' in art. 10 § 2º (Planalto strikes them, 'Vide ADI nº 1.931'); the dates need the STF record (case pages under
  portal.stf.jus.br/processos are off-limits); the replay currently drops art. 35-E altogether and ends art. 10 § 2º in 2021.
- Smaller: MP 1.301/2025 art. 32 § 10 must end at its conversion (Lei 15.233/2025); art. 35-B editorial '(composição: vide
  Dec. 4.044)' in the text.
Needs: the coordinator's choice of (a) or (b), and an allowed source for ADI 1.931's dates.

## Found on the way: staged vigência clauses misdated in published parts (fixed)
batch3's fixed-day fallback (FIXED_DAY) dates a law by the first day its clause names, even when the clause gives that
day to other provisions only. Audit (env VIG_AUDIT=<file>: batch3.vigencia_of logs each fallback use; no output change)
over all parts found: Lei 14.382/2022 (LRP, 2024 -> 28.6.2022, art. 130 stays 1.1.2024), Lei 13.097/2015 (1.1.2015 ->
20.1.2015: LConc, LPPP, LOC, CTB, LOS), Lei 14.183/2021 (Lavagem, 1.1.2025 -> 15.7.2021). Correct as they are: LC 200/2023
(its art. 11 is the LRF change, 1.1.2024), MP 1.023/2020, DL 406/1968, Lei 14.176/2021 and 14.601/2023 (now hand-set in
batch12). Hand entries in batch8 (13.097, 14.183) and batch9 (14.382 + VIGENCIA_PROVISION art-130). 99-batch8 (1ea64501),
99-batch9 (954884bb), 99-batch10 (30d49612) re-PUBLISHed; 99-batch11 unchanged.
Merged: 75 acts, 1765 versions, 1553 commits, check 0/0, --compare identical, audit clean. README (+3 rows, LRP 73) and
jurisdiction.json (75 acts) updated.

## Lei 9.656/1998 - added to 99-batch12 (coordinator: option 1), re-PUBLISHed
- History starts 27.8.2001, oldest version available (MP 2.177-44 wording; first_law null, earlier_laws Lei 9.656/1998 and
  Lei 10.223/2001, re-added to the part's laws after writing); 16 versions to 15.11.2025. Decision, version note and README
  row say the 1998 text and the ~44 monthly reissues (MP 1.665 -> 2.177-44) are not modelled and why. MP_PENDING mp-2177-2001.
- ADI 1.931: Planalto's notes are undated 'Vide ADI nº 1.931' -> not modelled (open item in decisions); art. 35-E and the
  struck 'atuais e' in art. 10 § 2º left out of every version (undated struck text rule); art. 10 § 2º kept to today by
  SPAN_FIX (next-wording had ended it in 2021). MP 1.301/2025 art. 32 § 10 ends at Lei 15.233 (8.10.2025); art. 35-B
  editorial '(composição: vide Dec.4.044)' dropped. 3 diffs vs compilado explained (art. 32 § 10 compilado truncated; ours
  = Lei 15.233's text).
- Part 88 versions (other 3 acts byte-identical), parse twice identical; merged 76 acts, 1781 versions, 1567 commits, check
  0/0, --compare identical, audit clean. README row + jurisdiction.json (76 acts).
