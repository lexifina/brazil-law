# Brazil: law history in git

The law of Brazil as a git history: one file per article, one commit per amendment on the day it took effect, and the amendment that made each change as the commit's author. `git blame` names the amendment behind every paragraph; `git log` lists every change to an article; checking out a date gives the text in force that day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `br/`.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constituicao/` | Constituição da República Federativa do Brasil de 1988 | 122 | From its promulgation (5 October 1988) to today: every Emenda Constitucional (1 to 141) and Emenda Constitucional de Revisão (1 to 6) that changed its words, and one ruling of the Supremo Tribunal Federal |
| `codigo-civil/` | Código Civil (Lei 10.406/2002) | 63 | From its entry into force (11 January 2003) to today |
| `lgpd/` | Lei Geral de Proteção de Dados Pessoais (Lei 13.709/2018) | 11 | From 2018, article by article as its art. 65 brought them into force |
| `codigo-penal/` | Código Penal (Decreto-Lei 2.848/1940) | 111 | From its entry into force (1 January 1942) to today, through the new Parte Geral of Lei 7.209/1984 (in force 13 January 1985) |
| `codigo-de-processo-civil/` | Código de Processo Civil (Lei 13.105/2015) | 18 | From its entry into force (18 March 2016), with Lei 13.256/2016's changes of that same day as a second version, to today |
| `clt/` | Consolidação das Leis do Trabalho (Decreto-Lei 5.452/1943) | 220 | From its entry into force (10 November 1943) to 6 April 2026, with three STF rulings (ADI 1.770, 5.938, 5.766) and the Medidas Provisórias that lapsed (MP 808/2017, 873/2019, 905/2019, 955/2020); 60 struck lines the source does not date are left out (see below) |
| `codigo-de-processo-penal/` | Código de Processo Penal (Decreto-Lei 3.689/1941) | 70 | From its entry into force (1 January 1942) to 7 August 2026, through the new Júri chapter of Lei 11.689/2008 and the STF ruling in ADI 2.797 |
| `codigo-de-defesa-do-consumidor/` | Código de Defesa do Consumidor (Lei 8.078/1990) | 16 | From its entry into force (11 March 1991) to 25 September 2026 |
| `codigo-tributario-nacional/` | Código Tributário Nacional (Lei 5.172/1966) | 21 | From its entry into force (1 January 1967) to 4 September 2026, with Senate Resolution 337/1983 |
| `estatuto-da-crianca-e-do-adolescente/` | Estatuto da Criança e do Adolescente (Lei 8.069/1990) | 57 | From its entry into force (14 October 1990) to 23 September 2026, with the STF rulings in ADI 869 and ADI 2.404 |
| `codigo-eleitoral/` | Código Eleitoral (Lei 4.737/1965) | 46 | From its entry into force (18 August 1965) to 25 March 2026 |
| `regime-juridico-dos-servidores-publicos/` | Regime Jurídico dos Servidores Públicos Civis da União (Lei 8.112/1990) | 56 | From its entry into force (12 December 1990) to 4 August 2022, including the Medidas Provisórias that lapsed; the wording of MP 301/2006, 341/2006 and 359/2007 is not printed by the source, so those periods are missing (see `REPRODUCE.md`) |

Each article is a file: `constituicao/art-006.md` is art. 6, `constituicao/adct-art-002.md` is art. 2 of the Ato das Disposições Constitucionais Transitórias (ADCT), `codigo-penal/art-121.md` is art. 121 of the Código Penal. Each act's preamble is `preambulo.md` (for the CLT, the text of Decreto-Lei 5.452 itself), and its headings (partes, títulos, capítulos, seções) are in `titulos.md` (and `adct-titulos.md`). In the Código Penal the marginal heading of an article (rubrica, "Homicídio simples") is the article file's first line; in the CLT, CPP and CDC the rubricas are kept in `titulos.md`. The CLT's annex (the table of categories that art. 577 refers to) is `clt/anexo.md`. The per-act `README.md` lists every provision, how often it changed and when. Further acts are added in their own folders as they are built.

Every act is rebuilt the same way, from Planalto's annotated page of the act (superseded wording kept, struck through, with the source's note naming the amending law), and checked against Planalto's consolidated page; the rules each act needed are listed in `REPRODUCE.md`. Git cannot store dates before 1970: the commits of the Código Penal, the CLT and the CPP before 1970 are dated 1 January 1970, one second apart, and the real in-force day is in each commit's `In-force:` trailer, which the tools read.

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
| Changes enacted but not yet in force | `git log main..futuro` (EC 141/2026 art. 7 XV from 16 December 2026; EC 132/2023's tax reform stages of 2027 and 2033) |

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
- **Against the official text today, the codes.** Each is compared with Planalto's consolidated page of the act. Código Civil: 2009 of 2019 units identical; LGPD: all 80; Código Penal: all but 25 articles; CPC: all but 1; CLT: 837 of 847 units; CPP: all but one heading (Capítulo II "DO JULGAMENTO", struck on the annotated page with arts. 556 to 562); CDC: every article. Every difference is between Planalto's two pages (typing slips, numbers written in words on one page and in figures on the other, placeholders for revoked text) and is listed in `REPRODUCE.md`.
- **Against the official text today, the Constitution.** The history is rebuilt from Planalto's annotated page and then compared with Planalto's separate consolidated page (`constituicaocompilado.htm`), unit by unit. On 28 October 2026, 392 of 414 units were identical. The other 22 differ only where the two official pages are typeset differently: a stray or missing full stop, comma, space, accent or "§" sign, a word split in one page ("capu t", "198 6"), "habeas corpus" against "habeas-corpus", a missing word in the consolidated page (ADCT art. 70 "até a mesma"), notes printed without brackets there (art. 216-A), and bare placeholders for revoked provisions. Each is listed in `REPRODUCE.md`.
- The repository is rebuilt from the same data a second time and must give identical hashes.

## What "author" means

The author of a commit is the amendment (or ruling) that made the change, with an e-mail address that cannot exist (`ec-26-2000@planalto.invalid`), so `git blame` and `git log --author` name amendments. The committer is always Lexifina.

- **Credits come only from the source.** Planalto's annotated page keeps every superseded wording struck through beside its replacement, each with a note: "(Redação dada pela Emenda Constitucional nº 26, de 2000)", "(Incluído pela …)", "(Revogado pela …)", "(Renumerado …)". A change is credited to the amendment its note names; text with no note is the 1988 original.
- **Where Planalto shows a change with no note**, it is dated only from the source itself: heading renames by the amendment whose own text renames them (seven headings, for example "DA CIÊNCIA E TECNOLOGIA" to "DA CIÊNCIA, TECNOLOGIA E INOVAÇÃO" by EC 85/2015); a struck "Parágrafo único" that became "§ 1º" by the amendment that added the article's "§ 2º"; and struck items with no note of their own by the enclosing article or paragraph they fell with. `REPRODUCE.md` gives the counts.
- **Court rulings.** The Supremo Tribunal Federal's ruling in ADI 7047 (with ADI 7064), judged on 30 November 2023, excluded the words "com auto aplicabilidade para a União" from art. 100 § 11; Planalto shows them struck. It is a commit of kind "court", dated 4 December 2023, the day the minutes were published in the DJE. The same ruling declared art. 100 § 9 and ADCT art. 101 § 5 (as worded by EC 113/2021) unconstitutional, but Planalto leaves those words in place with a "Vide ADI" note, so they stay in the text here too. Planalto's many "(Vide ADI …)" notes change no words and are not commits. In the codes, the rulings Planalto shows as struck words are court commits too, each dated by the publication of the decision: CLT ADI 1.770 (art. 453 § 1º, 20 October 2006), ADI 5.938 (art. 394-A II and III, 4 June 2019) and ADI 5.766 (arts. 790-B and 791-A § 4º, 5 November 2021); CPP ADI 2.797 (art. 84 §§ 1º and 2º, 26 September 2005).
- **Medidas Provisórias** are commits on their publication day. Wording of an MP that was converted ends when the conversion law takes effect; an MP that lapsed (CLT: MP 808/2017, 873/2019, 905/2019, 955/2020) is followed by a commit that restores the earlier wording, dated by the Congress record of the lapse. CDC art. 57 carries the wording of MP 1.393/2026, still pending on 28 October 2026.
- Blame credits whole lines (one paragraph per line). In a paragraph rewritten several times, use `git log -p --word-diff` to see which words each amendment changed.

## What it does not show

- **Future text, from the amendments' own words.** The branch `futuro` holds EC 141/2026's new art. 7 XV (in force on 16 December 2026, two months after publication) and EC 132/2023's tax-reform stages: its arts. 3 and 11 'em 2027' and arts. 4 and 5 'em 2033' (dated 1 January of those years), with the revocations of its art. 22 (art. 195 I "b", IV and § 12 in 2027; arts. 155 II and §§ 2º to 5º, 156 III and § 3º, 158 IV "a" and § 1º, 161 I and ADCT arts. 80 II, 82 § 2º and 83 in 2033). Planalto's Constitution page shows these only as "Vide … Vigência" notes, so their wording is read from each amendment's own page and placed by its labels (article, paragraph, inciso, alínea). Planalto has not consolidated them yet, so this text has not been checked against a consolidated page.
- **Effects that differ from the in-force day** (see Dates), and the STF's interpretations that leave the words alone ("Vide ADI").
- **The signatures** of the Constituent Assembly, and Planalto's notes, which are used only to date and credit changes.
- **CLT: 60 struck lines with no date.** Planalto's annotated page strikes them but gives no note, no later wording and no struck parent or sibling to date their end, so they are left out of every version (listed in `REPRODUCE.md`; among them old wordings of arts. 28, 60, 88, 287, 375, 387, 555 and 670). The CLT's replay also records 72 open problems rather than guess (struck lines with no datable end, wordings Planalto prints again after a later wording, one note that names no law); those lines follow the annotated page as printed.
- **CLT, 1946 suspension.** Decreto-Lei 8.740/1946's changes, suspended by Decreto-Lei 8.987-A/1946, stand only between the two; a change suspended before it took effect is left out.
- **Some publication days.** A few 1940s decree-laws print no Diário Oficial date on Planalto (only the Coleção das Leis): for them the enactment day stands in (CLT). For the CPP and CDC, where Planalto's DOU day differs from LexML's "Publicação Original", LexML's day is used.
- **Typesetting.** Spacing, quotes, dashes and label punctuation ("§ 1º -" and "§ 1º") were normalised; the source's own typos are kept.

## How it is built

The Planalto site refuses automated readers, so `tools/fetch.py` reads every Planalto page from an Internet Archive raw copy (`web.archive.org/web/<timestamp>id_/<Planalto URL>`, byte for byte what Planalto served), pinned by timestamp in `tools/sources.json`; it uses curl, one request per second, cached by the sha256 of the URL. `tools/parse.py` turns the cache into `corpus.json`, and the shared builder `tools/build.py` writes the history with `git fast-import`. The same corpus always gives the same hashes. `REPRODUCE.md` records every command, tool version, data hash and decision, and the result of a hash-for-hash rebuild.

No AI model wrote or changed legal text. Claude Opus 5.5 wrote the scripts and chose the sources; see `REPRODUCE.md`.

## Sources

| Source | Kind | Past versions by date | Names the amending act | API or bulk | Notes |
| --- | --- | --- | --- | --- | --- |
| [Planalto (legislação)](https://www.planalto.gov.br/ccivil_03/) | Official legislation | partly: superseded wording kept, struck through, no date selector | yes, a note on every changed paragraph | no | Used, through Internet Archive copies: `constituicao.htm` (annotated), `constituicaocompilado.htm` (check), `quadro_emc.htm` (dates), each amendment's page (its vigência clause), `lcp200.htm`; for the codes their annotated and consolidated pages (`l10406.htm`, `l13709.htm`, `del2848.htm`, `l13105.htm`, `del5452.htm`, `del3689.htm`, `l8078.htm` and their compiled versions) and the page of every law their notes cite |
| [Supremo Tribunal Federal, case pages](https://portal.stf.jus.br/) | Court | n/a | n/a | no | Used for ADI 7047 (Constitution), ADI 1.770, 5.938 and 5.766 (CLT) and ADI 2.797 (CPP): each decision and the date it was published |
| [LexML Brasil](https://www.lexml.gov.br) | Standards | no | no | yes (OAI-PMH) | Used for the CPP and CDC: each cited law's "Publicação Original" DOU day |
| [Evaldoes/legislacao-br](https://github.com/Evaldoes/legislacao-br) | Volunteer git repo (CC0) | yes | partly | n/a | Prior art, for reconciliation only; no text copied |

Research guides that cover every country: [GlobaLex](https://www.nyulawglobal.org/globalex/) and the [Law Library of Congress Guide to Law Online](https://www.loc.gov/research-centers/law-library-of-congress/researcher-resources/guide-to-law-online/).

## Licence

The legal texts are official texts of the Federative Republic of Brazil, as published by the Presidency of the Republic (Casa Civil) on planalto.gov.br. Official acts are not protected by copyright in Brazil (Lei 9.610/1998, art. 8º, IV). Este texto não substitui o publicado no Diário Oficial da União. The arrangement, tables, commit messages and tools are by Lexifina, under the terms in `LICENSE`.

This repository is not legal advice and not an official publication.

## Em português

Histórico do direito brasileiro em git: um arquivo por artigo e um commit por emenda, datado no dia em que entrou em vigor e assinado pela emenda que fez a alteração (`git blame` mostra a emenda de cada parágrafo). Contém (lista completa na tabela acima) a Constituição Federal de 1988 desde a promulgação, com todas as Emendas Constitucionais (1 a 141) e de Revisão (1 a 6) que alteraram o texto, e a decisão do STF na ADI 7047; o Código Civil, a LGPD, o Código Penal (desde 1942, com a nova Parte Geral da Lei 7.209/1984), o Código de Processo Civil (desde 2016), a CLT (desde 10 de novembro de 1943, 220 versões, com as ADI 1.770, 5.938 e 5.766), o Código de Processo Penal (desde 1942, 70 versões, com a ADI 2.797) e o Código de Defesa do Consumidor (desde 11 de março de 1991, 16 versões). A nova redação do art. 7º, XV (EC 141/2026), em vigor a partir de 16 de dezembro de 2026, está no ramo `futuro`.

- Texto vigente em uma data: `python tools/vigente_em.py 2015-01-01 constituicao 6`
- Datas: a cláusula de vigência de cada emenda; sem cláusula, o art. 1º da LINDB (45 dias após a publicação oficial).
- Autoria: cada alteração é atribuída à emenda citada na nota do Planalto ("Redação dada pela…", "Incluído pela…", "Revogado pela…").
- Conferência: o texto de hoje foi comparado com o texto compilado do Planalto; as diferenças são apenas tipográficas e estão listadas em `REPRODUCE.md`.
- CLT: 60 linhas riscadas que a página do Planalto não data ficam fora de todas as versões, e o processamento registra 72 problemas em aberto, sem adivinhar datas (lista em `REPRODUCE.md`).
- Fonte: Presidência da República, Casa Civil (planalto.gov.br), lida por cópias do Internet Archive. Nenhum modelo de IA escreveu texto legal.
