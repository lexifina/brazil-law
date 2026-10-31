# Brazil batch 10 progress (gitlaw-BR agent on alan-dell, 2026-10-31)

Owns `scripts/brazil-law/batch10/` and `corpus.d/99-batch10.json` (+ `.PUBLISH`). Never commits or pushes. Scratch OUTSIDE
the repo: `~/Documents/.gitlaw-scratch/brazil-b10parts` (regenerated parts, batch10/.tmp/runparts.py),
`brazil-b10src` (country folder copy + trial parts), `brazil-b10` (build), `brazil-b10c` (--compare);
batch10/.tmp/runbuild.py runs build, check, compare.

## 1. Pin scan of every older part - DONE 2026-10-31 ~03:50Z

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

## 2. 99-batch10 (next ~10 federal laws)
In progress: Concessões 8.987, PPPs 11.079, Saneamento 11.445, Petróleo 9.478, Abuso de Autoridade 13.869, Estatuto dos
Militares 6.880, LC 64/1990 (Inelegibilidades, incl. Ficha Limpa), Lei 8.142/1990, Lei Geral do Esporte 14.597, Estatuto
do Torcedor 10.671, PNMA 6.938. Pages pinned (20, all Common Crawl) in batch10/sources_batch10.json.
