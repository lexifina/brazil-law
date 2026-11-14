# Brazil: law history in git


The law of Brazil as a git history: one file per article, one commit per version on the day it took effect, and the act that made each change as the commit's author. `git blame` names the act behind every paragraph; `git log` lists every change to an article; picking a date gives the text in force that day.

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is Brazil's federal law, which global-law reads at `brazil/national/acts/`.

**What is in it now:** the Constitution and 322 federal codes and laws with their history, 4,358 versions from 1851 on (24 of them, not yet in force, on the `futuro` branch); and 5,000 further federal acts (4,145 Leis, 137 Leis Complementares and 718 Decretos-Leis) with their current text only. Each act's folder has a `README.md` listing its provisions, how often each changed and when; [`data/laws.csv`](data/laws.csv) lists the 2,714 acts that made the changes, with their days.

Each act is a folder named after it, one file per article (`clt/art-134.md` is art. 134 of the Consolidação das Leis do Trabalho, the labour code, Decreto-Lei 5.452/1943; `lei-10334-de-2001/` is Lei 10.334/2001); the Constitution is [`constituicao/`](constituicao/), with the articles of the ADCT as `adct-art-<n>.md`.

The text is in Portuguese, as Planalto prints it. An English translation is not part of this record.

## Questions as git commands

| Question | Command |
| --- | --- |
| Every change to art. 134 of the CLT (annual leave) | `git log -p --word-diff -- clt/art-134.md` |
| Which act wrote each paragraph of art. 134? | `git blame clt/art-134.md` |
| Every version of the CLT, with the day each took effect | `git log --format="%h %(trailers:key=In-force,valueonly,separator=) %an" -- clt ':!clt/README.md'` |
| Art. 134 as in force on 1 January 2015 | `python tools/vigente_em.py 2015-01-01 clt 134` |

**Outside git**, we also host this record publicly, for free:

- **[Ask Claude about Brazilian law](https://global-law.lexifina.com/v1/try_claude?country=brazil)**: opens Claude with a first question ready.
- **[Ask ChatGPT](https://global-law.lexifina.com/v1/try_chatgpt?country=brazil)**: the same question in ChatGPT.
- **[Call the API in your browser](https://global-law.lexifina.com/v1/search_law?query=f%C3%A9rias&jurisdictions=brazil)**: a search of Brazilian law for "férias" (annual leave), returned as JSON. See the [documentation here](https://lexifina.com/api/global-law).

Both assistants read the record through the free Global law connector (MCP, `https://global-law.lexifina.com/mcp`); the first time, the chat gives you the link that adds it. Ask in Portuguese or in English.

**Host it yourself easily.** All it takes is git and Python, and the tools run on your machine:

```sh
git clone --depth 1 https://github.com/lexifina/global-law && cd global-law
python3 tools/countries.py add brazil/national/acts
python3 tools/law.py show 2026-01-01 brazil/national/acts/clt/art-134.md
```

Opened in Claude Code, Cursor, VS Code or Codex, the clone also starts a local MCP server with the same tools ([MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md)).

## Dates

Each commit is dated at noon, America/Sao_Paulo, on the day the version took effect, and carries it in its `In-force:` trailer, beside `Enacted:` and `Published:`:

- the day the amending act's own vigência clause gives (on publication, on promulgation, on a fixed day, or provision by provision), or the later day it fixes for a provision to produce effects; with no clause, LINDB art. 1: 45 days after official publication, counted under LC 95/1998 art. 8 § 1;
- a Medida Provisória from its publication; one that lapsed or was rejected is followed by a commit that restores the earlier wording, dated by the Congress record;
- for the 5,000 acts with their current text only, the in-force day of the latest change that text shows;
- git cannot store dates before 1970, so the 235 earlier commits are dated from 1970-01-01, one second apart, with the real day in `In-force:`. Ask for a date with `tools/vigente_em.py`, not `git log --before`.

Each change is credited to the act Planalto's note beside it names ("Redação dada pela Lei nº 13.467, de 2017"), at an address that cannot exist (`lei-13467-2017@planalto.invalid`); rulings of the Supremo Tribunal Federal that Planalto shows as struck words are commits of kind `court`. The one version of each current-text act is credited to Planalto as the oldest version available. The `futuro` branch also holds what is enacted but not yet in force, such as EC 141/2026's art. 7 XV (16 December 2026) and EC 132/2023's tax-reform stages of 2027 and 2033.

## How it is checked

- `tools/check_repo.py` reads every one of the 9,366 versions back from git on the day it took effect and on the day before, and compares it with the corpus: 0 mismatches. The results are in [`REPRODUCE.md`](REPRODUCE.md).
- The text in force today of the Constitution and the codes is compared with Planalto's consolidated page, unit by unit. For the Constitution, 392 of 414 units were identical on 28 October 2026, and the other 22 differ only where Planalto's two pages are typeset differently; every difference is listed in `REPRODUCE.md`.
- No merge commits on `main`, no commit dates that go backwards, nothing dated after the build, and every commit's trailers parse.
- History is append-only: new acts and versions are added on top (`tools/append.py`), and no published commit is rewritten.

## What it does not show

- **Earlier wordings of 5,000 acts.** They have their current text only; their history is to be added later as labelled corrections.
- **Other federal acts.** No decretos or other regulations, and no Medidas Provisórias in their own right (they appear only as the changes they made). No case law, apart from the rulings that struck words.
- **Wording the source does not date.** In the CLT, 60 struck lines with no note are left out of every version; in Lei 8.112/1990, the periods of Medidas Provisórias 301/2006, 341/2006 and 359/2007, whose wording Planalto does not print, are missing.
- **Effects that change no words**: the STF's interpretations ("Vide ADI"), and effects that are only financial, retroactive or left to a later act.
- **Signatures, Planalto's notes** (used only to date and credit changes) and a few annexes, such as the fee table of the Estatuto do Desarmamento.

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [Planalto (Legislação)](https://www.planalto.gov.br/ccivil_03/) (Presidência da República, Casa Civil) | Official legislation | partly: superseded wording kept, struck through, with a note naming the amending act | Each act's page (annotated, and consolidated where Planalto has one) and the page of every act its notes cite, read through dated Internet Archive copies; the authoritative text is the one published in the Diário Oficial da União |
| [Supremo Tribunal Federal](https://portal.stf.jus.br/) | Court | n/a | Case pages of the rulings that struck words, for the decision and the day it was published |
| [LexML Brasil](https://www.lexml.gov.br) (Senado Federal) | Legislative records | no | Each cited law's "Publicação Original" day in the Diário Oficial |
| [Câmara dos Deputados, Legislação Informatizada](https://www2.camara.leg.br/legin/fed/) | Parliament | no | Publication facts only (retificações, an Ato Declaratório) |

## Licence

See [`LICENSE`](LICENSE). The texts are official acts of Brazil as the Presidency of the Republic (Casa Civil) publishes them on planalto.gov.br, and official acts are not protected by copyright in Brazil (Lei 9.610/1998, art. 8º, IV); the arrangement of the history, the commit messages, the tables and the tools are CC0 1.0.

No AI model wrote, translated or changed legal text, and none runs when the history is built; the scripts, and the tables of in-force days in them, were written by an AI model from the official pages (see [`REPRODUCE.md`](REPRODUCE.md)).

## Em português

Histórico do direito federal brasileiro em git: um arquivo por artigo, um commit por versão no dia em que entrou em vigor e, como autor do commit, o ato que fez cada alteração (`git blame` mostra o ato de cada parágrafo). Contém a Constituição e 322 códigos e leis federais com seu histórico, 4.358 versões desde 1851, e mais 5.000 atos federais só com o texto vigente hoje. Texto vigente em uma data: `python tools/vigente_em.py 2015-01-01 clt 134`. Fonte: Presidência da República, Casa Civil (planalto.gov.br). Pergunte ao Claude ou ao ChatGPT pelos links acima, em português ou em inglês.

## More

From [lexifina/global-law](https://github.com/lexifina/global-law):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): every feature, and what every corpus must support (`git blame`, `law.py`, the MCP tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): questions and answers · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): proposing changes · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): the MCP server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): how it was built · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): how current each corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): whether updates are running · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): how each official source is watched for changes
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): how fast the tools are, measured
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): charts and bridges across the world's law
- [Vulnerabilities](https://github.com/lexifina/global-law/tree/main/vulnerabilities): mistakes in legislation as published
