# Brazil: law history in git

The law of Brazil as a git history: one file per article, one commit per amendment on the day it took effect, and the amendment that made each change as the commit's author. `git blame` names the amendment behind every paragraph; `git log` lists every change to an article; checking out a date gives the text in force that day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `br/`.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constituicao/` | Constituição da República Federativa do Brasil de 1988 | 122 | From its promulgation (5 October 1988) to today: every Emenda Constitucional (1 to 141) and Emenda Constitucional de Revisão (1 to 6) that changed its words, and one ruling of the Supremo Tribunal Federal |

Each article is a file: `constituicao/art-006.md` is art. 6, `constituicao/adct-art-002.md` is art. 2 of the Ato das Disposições Constitucionais Transitórias (ADCT). The preamble is `preambulo.md`, and the headings (títulos, capítulos, seções) are `titulos.md` and `adct-titulos.md`. The per-act `README.md` lists every provision, how often it changed and when. Further acts are added in their own folders as they are built.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did art. 6 say on 1 January 2015? | `python tools/vigente_em.py 2015-01-01 constituicao 6` |
| The same, with raw git (bash) | `git show $(git rev-list -1 --before="2015-01-01T23:59:59Z" main -- constituicao/art-006.md):constituicao/art-006.md` |
| The same, in PowerShell | `$r = git rev-list -1 --before="2015-01-01T23:59:59Z" main -- constituicao/art-006.md; git show "$($r):constituicao/art-006.md"` |
| Which amendment wrote each paragraph of art. 37? | `git blame constituicao/art-037.md` |
| Every change to art. 37, word by word | `git log -p --word-diff constituicao/art-037.md` |
| Every amendment in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one amendment changed | `git show law/ec-26-2000` (tags `law/<key>` mark each amendment's commit) |
| The whole Constitution on a date | `python tools/vigente_em.py 1995-01-01 constituicao` |
| The Constitution as of a version day | `git show constituicao/2000-02-15` (tags `<act>/<in-force day>`) |
| Changes enacted but not yet in force | `git log main..futuro` (empty today; see below) |

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## Dates

- Each commit is dated at **noon, America/Sao_Paulo, on the day the change took effect** (the in-force date). Enactment and publication dates are trailers (`Enacted:`, `Published:`), and the in-force day is in `In-force:`, which the tools read.
- **Each amendment's own clause decides.** Most say "Esta Emenda Constitucional entra em vigor na data de sua publicação": the day of the Diário Oficial da União, from Planalto's table of amendments (quadro_emc). Others are dated as their clause says: on promulgation (EC 19, 33, 58, 95), on a fixed day (EC 14: 1 January 1997; EC 25: 1 January 2001; EC 78: 1 January 2015; EC 105: 1 January 2020; Emenda de Revisão 5: 1 January 1995), or provision by provision (EC 109's change to art. 29-A from 1 January 2025; EC 114's change to art. 100 § 5 from 1 January 2022).
- **Default rule.** Amendments with no vigência clause of their own (EC 2 to 9, 12, 13, 15, 16, 42, 72, 77, 90) are dated by Decreto-Lei 4.657/1942 (LINDB) art. 1: in force 45 days after official publication, counted under LC 95/1998 art. 8 § 1. Some authors hold that an amendment with no clause is in force on publication; the rule is applied as written, and `REPRODUCE.md` lists every date it sets.
- **Effects are not the in-force day.** Where an amendment is in force on publication but "produzirá efeitos" later (EC 58, 69, 84, 86, 87, 93, 100, 102, 108, 112, 133), the text changes on the in-force day and the clause is quoted in `REPRODUCE.md`.
- **EC 126/2022 art. 9** revoked ADCT arts. 106 to 114 "após a sanção da lei complementar prevista no art. 6º", that is Lei Complementar 200/2023 (sanctioned 30 August, published 31 August 2023), so those articles end on 31 August 2023.
- `--before="YYYY-MM-DD"` alone uses your clock's time of day, so a change that took effect that day may be missed before noon. Use `T23:59:59Z` as above, or the tool.

## How it is checked

- Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`. Results are in `REPRODUCE.md`.
- Health checks: no merge commits on `main`, commit dates never go backwards, nothing dated in the future, and every commit's trailers parse with `git interpret-trailers --parse`.
- **Against the official text today.** The history is rebuilt from Planalto's annotated page and then compared with Planalto's separate consolidated page (`constituicaocompilado.htm`), unit by unit. On 28 October 2026, 392 of 414 units were identical. The other 22 differ only where the two official pages are typeset differently: a stray or missing full stop, comma, space, accent or "§" sign, a word split in one page ("capu t", "198 6"), "habeas corpus" against "habeas-corpus", a missing word in the consolidated page (ADCT art. 70 "até a mesma"), notes printed without brackets there (art. 216-A), and bare placeholders for revoked provisions. Each is listed in `REPRODUCE.md`.
- The repository is rebuilt from the same data a second time and must give identical hashes.

## What "author" means

The author of a commit is the amendment (or ruling) that made the change, with an e-mail address that cannot exist (`ec-26-2000@planalto.invalid`), so `git blame` and `git log --author` name amendments. The committer is always Lexifina.

- **Credits come only from the source.** Planalto's annotated page keeps every superseded wording struck through beside its replacement, each with a note: "(Redação dada pela Emenda Constitucional nº 26, de 2000)", "(Incluído pela …)", "(Revogado pela …)", "(Renumerado …)". A change is credited to the amendment its note names; text with no note is the 1988 original.
- **Where Planalto shows a change with no note**, it is dated only from the source itself: heading renames by the amendment whose own text renames them (seven headings, for example "DA CIÊNCIA E TECNOLOGIA" to "DA CIÊNCIA, TECNOLOGIA E INOVAÇÃO" by EC 85/2015); a struck "Parágrafo único" that became "§ 1º" by the amendment that added the article's "§ 2º"; and struck items with no note of their own by the enclosing article or paragraph they fell with. `REPRODUCE.md` gives the counts.
- **Court rulings.** The Supremo Tribunal Federal's ruling in ADI 7047 (with ADI 7064), judged on 30 November 2023, excluded the words "com auto aplicabilidade para a União" from art. 100 § 11; Planalto shows them struck. It is a commit of kind "court", dated 4 December 2023, the day the minutes were published in the DJE. Planalto's many "(Vide ADI …)" notes change no words and are not commits.
- Blame credits whole lines (one paragraph per line). In a paragraph rewritten several times, use `git log -p --word-diff` to see which words each amendment changed.

## What it does not show

- **Future text.** EC 132/2023 (tax reform) changes provisions from 2027 and 2033, and EC 141/2026 changes art. 7 XV two months after publication. Planalto shows these only as "Vide … Vigência" notes beside the text in force, not as text, so they are not on the `futuro` branch yet.
- **Effects that differ from the in-force day** (see Dates), and the STF's interpretations that leave the words alone ("Vide ADI").
- **The signatures** of the Constituent Assembly, and Planalto's notes, which are used only to date and credit changes.
- **Typesetting.** Spacing, quotes, dashes and label punctuation ("§ 1º -" and "§ 1º") were normalised; the source's own typos are kept.

## How it is built

The Planalto site refuses automated readers, so `tools/fetch.py` reads every Planalto page from an Internet Archive raw copy (`web.archive.org/web/<timestamp>id_/<Planalto URL>`, byte for byte what Planalto served), pinned by timestamp in `tools/sources.json`; it uses curl, one request per second, cached by the sha256 of the URL. `tools/parse.py` turns the cache into `corpus.json`, and the shared builder `tools/build.py` writes the history with `git fast-import`. The same corpus always gives the same hashes. `REPRODUCE.md` records every command, tool version, data hash and decision, and the result of a hash-for-hash rebuild.

No AI model wrote or changed legal text. Claude Opus 5.5 wrote the scripts and chose the sources; see `REPRODUCE.md`.

## Sources

| Source | Kind | Past versions by date | Names the amending act | API or bulk | Notes |
| --- | --- | --- | --- | --- | --- |
| [Planalto (legislação)](https://www.planalto.gov.br/ccivil_03/) | Official legislation | partly: superseded wording kept, struck through, no date selector | yes, a note on every changed paragraph | no | Used, through Internet Archive copies: `constituicao.htm` (annotated), `constituicaocompilado.htm` (check), `quadro_emc.htm` (dates), each amendment's page (its vigência clause), `lcp200.htm` |
| [Supremo Tribunal Federal, case pages](https://portal.stf.jus.br/) | Court | n/a | n/a | no | Used for ADI 7047: the decision and the DJE date of its minutes |
| [LexML Brasil](https://www.lexml.gov.br) | Standards | no | no | yes (OAI-PMH) | URN:LEX identifiers, Akoma Ntoso-inspired XML; not used yet |
| [Evaldoes/legislacao-br](https://github.com/Evaldoes/legislacao-br) | Volunteer git repo (CC0) | yes | partly | n/a | Prior art, for reconciliation only; no text copied |

Research guides that cover every country: [GlobaLex](https://www.nyulawglobal.org/globalex/) and the [Law Library of Congress Guide to Law Online](https://www.loc.gov/research-centers/law-library-of-congress/researcher-resources/guide-to-law-online/).

## Licence

The legal texts are official texts of the Federative Republic of Brazil, as published by the Presidency of the Republic (Casa Civil) on planalto.gov.br. Official acts are not protected by copyright in Brazil (Lei 9.610/1998, art. 8º, IV). Este texto não substitui o publicado no Diário Oficial da União. The arrangement, tables, commit messages and tools are by Lexifina, under the terms in `LICENSE`.

This repository is not legal advice and not an official publication.

## Em português

Histórico do direito brasileiro em git: um arquivo por artigo e um commit por emenda, datado no dia em que entrou em vigor e assinado pela emenda que fez a alteração (`git blame` mostra a emenda de cada parágrafo). Contém a Constituição Federal de 1988 desde a promulgação, com todas as Emendas Constitucionais (1 a 141) e de Revisão (1 a 6) que alteraram o texto, e a decisão do STF na ADI 7047.

- Texto vigente em uma data: `python tools/vigente_em.py 2015-01-01 constituicao 6`
- Datas: a cláusula de vigência de cada emenda; sem cláusula, o art. 1º da LINDB (45 dias após a publicação oficial).
- Autoria: cada alteração é atribuída à emenda citada na nota do Planalto ("Redação dada pela…", "Incluído pela…", "Revogado pela…").
- Conferência: o texto de hoje foi comparado com o texto compilado do Planalto; as diferenças são apenas tipográficas e estão listadas em `REPRODUCE.md`.
- Fonte: Presidência da República, Casa Civil (planalto.gov.br), lida por cópias do Internet Archive. Nenhum modelo de IA escreveu texto legal.
