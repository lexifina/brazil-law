# How this repository was made (Paraná)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Sistema Estadual de Legislação (Casa Civil do Estado do Paraná): the Compilado and Original views of each act | <https://www.legislacao.pr.gov.br/legislacao> | 2026-10-30 | Texts: Sistema Estadual de Legislação, Casa Civil do Governo do Estado do Paraná, www.legislacao.pr.gov.br. Lei 9.610/1998 art. 8 IV: the texts of laws and other official acts are not protected by copyright. Non-official text: "Este texto não substitui o publicado no Diário Oficial do Estado". |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constituicao` | Constituição do Estado do Paraná | 1 | 2026-06-30 to 2026-06-30 |

The build made 1 commits:

| Commits | Kind |
| ---: | --- |
| 1 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `futuro`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 1 laws in the record.
- 1 tags.

## Dates

Each commit is dated at noon (America/Sao_Paulo) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Decreto-Lei 4.657/1942 (LINDB) art. 1: unless it says otherwise, a law takes effect 45 days after its official publication. This record dates each act as enacted by its publication in the Diário Oficial do Estado (the Constituição by its promulgation and publication, 5 October 1989). https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `65099df12ff2ba796de19bb5c245f9dbf7a981721b3b4774dd3af670da15b66d` (304321 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a97ff7ea62c3c7595c5668a297d533da0b74373c`, `check.py` `3e59cb6f05eccb94a9ec14431a7f6781221e83ef`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- An act with no alteration note is given as enacted ("Original"), credited to the act itself and dated by its publication in the Diário Oficial do Estado (the Constituição by its promulgation, 5 October 1989). An altered act is given only as its compiled text ("Compilado": the text with the last alteration of each provision), credited to the publisher as the oldest version available and dated by the latest date its alteration notes cite. The wordings in between are not reconstructed yet, so no earlier version is given rather than a wrong one.
- The publisher's notes (links in parentheses, such as "(Redação dada pela Emenda Constitucional 7 de 24/04/2000)" or "(vide Lei ...)") are left out of the text; "(vide ...)" notes are cross-references and do not date a version.
- One file per Art. (articles of the Ato das Disposições Constitucionais Transitórias as adt-*); headings of the Títulos, Capítulos and Seções stand above the first article under them; "000-titulo" holds the title, the publication line and the preamble. Text after the last article (place, date, signatures) stays with the last article.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (claude-opus-5-5) wrote Lexifina's code and chose the sources. No model output is used as legal text or dates: every word comes from the Sistema Estadual de Legislação pages.
