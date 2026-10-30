# Paraná: law history in git

The law of the State of Paraná (Estado do Paraná) (Brazil) as a git history: one file per Artigo, one paragraph per line, so `git blame`, `git log` and `git diff` work line by line. The text is Portuguese, the only official language.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

## What this repository holds

| Folder | Act | Versions |
| --- | --- | ---: |
| `constituicao/` | Constituição do Estado do Paraná (5 October 1989) with its Ato das Disposições Constitucionais Transitórias (`adt-*`), compiled text in force | 1 |

An altered act is given **only as its compiled text in force**, credited to the publisher as the oldest version available: the wordings in between are not reconstructed yet, so no earlier version is shown rather than a wrong one. Leis Complementares, Leis and decrees are not included yet.

## Source

[Sistema Estadual de Legislação](https://www.legislacao.pr.gov.br/legislacao/), published by the Casa Civil do Governo do Estado do Paraná. Each version names the page it was taken from and that page's sha256, in `data/versions.json`.

## Dates

An altered act's compiled text is dated by the latest date its alteration notes cite ("(Redação dada pela Emenda Constitucional 7 de 24/04/2000)"); "(vide ...)" cross-references do not date a version. An unaltered act would be dated by its publication in the Diário Oficial do Estado. Commits are at noon in Curitiba.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

The "Compilado" view of each act becomes one file per Art.; headings of the Títulos, Capítulos and Seções stand above the first article under them; `000-titulo.md` holds the title, the publication line and the preamble. The publisher's linked notes in parentheses are left out.

## How it is checked

Every version is read back from git on the day it took effect (`tools/check_repo.py`) and must match the corpus; an independent letters-and-digits comparison of every version against the source page must show no difference. Results are in `REPRODUCE.md`.

## What "author" means

The author of each commit is the law that made the text, or, for a consolidated text, the publisher, with an e-mail address that cannot exist; the committer is always Lexifina.

## Limits

Not a complete history: an altered act starts at its compiled text in force. The text is not the official version: "Este texto não substitui o publicado no Diário Oficial do Estado". Text after the last article (place, date, signatures) stays in the last article's file.

## Licence

See [LICENSE](LICENSE): Brazilian law texts are not protected by copyright (Lei 9.610/1998, art. 8, IV). Fonte: Sistema Estadual de Legislação, Casa Civil do Governo do Estado do Paraná.
