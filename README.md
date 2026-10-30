# Bahia: law history in git

The law of the State of Bahia (Estado da Bahia) (Brazil) as a git history: one file per Artigo, one paragraph per line, so `git blame`, `git log` and `git diff` work line by line. The text is Portuguese, the only official language.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

## What this repository holds

| Folder | Act | Versions |
| --- | --- | ---: |
| `constituicao/` | Constituição do Estado da Bahia (5 October 1989) with its Ato das Disposições Constitucionais Transitórias (`adt-*`), text in force | 1 |
| `lc-<year>-<number>/` | the Leis Complementares listed by Legisla Bahia, added part by part | 1 each |

Legisla Bahia gives most Leis Complementares as published, without later alterations (its note points to other publishers for updated texts): such an act is given **as enacted**, credited to the act itself. An altered act is given **only as its text in force**, credited to the publisher as the oldest version available: the wordings in between are not reconstructed yet, so no earlier version is shown rather than a wrong one. Ordinary Leis, decrees and the Emendas Constitucionais as acts are not included yet.

## Source

[Legisla Bahia](https://www.legislabahia.ba.gov.br), published by the Casa Civil do Estado da Bahia. Each version names the page it was taken from and that page's sha256, in `data/versions.json`.

## Dates

An unaltered act is dated by its publication in the Diário Oficial do Estado (Bahia laws almost always take effect on publication). An altered act's text in force is dated by the latest date its alteration notes cite ("Alterado pela Emenda ... de 18 de janeiro de 1999"). Commits are at noon in Salvador.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

Each page becomes one file per Art.; headings of the Títulos, Capítulos and Seções stand above the first article under them; `000-titulo.md` holds the title, the ementa and the preamble. The publisher's alteration notes (paragraphs that quote the "Redação original") are left out. Tables are one line per row, with cells separated by ` | `.

## How it is checked

Every version is read back from git on the day it took effect (`tools/check_repo.py`) and must match the corpus; an independent letters-and-digits comparison of every version against the source page must show no difference. Results are in `REPRODUCE.md`.

## What "author" means

The author of each commit is the law that made the text, or, for a consolidated text, the publisher, with an e-mail address that cannot exist; the committer is always Lexifina.

## Limits

Not a complete history: an altered act starts at its text in force. A listed Lei Complementar may have been revoked in whole or in part. The text is not the official version: only the Diário Oficial do Estado is authoritative. Text after the last article (place, date, signatures) stays in the last article's file.

## Licence

See [LICENSE](LICENSE): Brazilian law texts are not protected by copyright (Lei 9.610/1998, art. 8, IV). Fonte: Legisla Bahia, Casa Civil do Estado da Bahia.
