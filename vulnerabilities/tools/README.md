# Tools

The scripts behind this Brazil-only run of global-law's vulnerability detectors. They run inside a copy of
[global-law/vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts) (Python 3.11+,
`pip install duckdb pyarrow`), with a bare clone of this repository at `sources/corpus/brazil-law.git`, a blobless bare
clone of global-law at `sources/global-law.git`, and a `pins.json` that names only brazil-law and its commit.
`build_vulns.py`, `flags_chart.py`, `late_ext_select.py`, `late_ext_rebut.py`, `late_ext_check.py` and `patch_pt.py` sit
two folders above the scripts, next to `config.json`.

| Script | What it does |
| --- | --- |
| `run.sh` | Indexes the history and texts, maps paths to today's folders, adds this repository's history rows, and runs the detectors (`bash run.sh <shards>`) |
| `map_moved.py` | Rewrites old file paths to each act's folder today through `data/paths.json`, for repositories that moved their act folders; this repository has no `data/paths.json`, so it changes nothing here |
| `add_root.py` | Builds the history rows from this repository's own commits, so the history detectors read every change |
| `patch_pt.py` | The Portuguese fixes below, in the copy of global-law's scripts (`python -X utf8 patch_pt.py <scripts dir>`; a fix already in place is skipped) |
| `run_triage.sh` | The model review: the 40 strongest flags per category, the 40 strongest lapsed time limits in law texts, and the empty periods |
| `late_ext_select.py` | Chooses the empty periods for global-law's review of that category (here all 37, 13 of them with the old and new date in one sentence) |
| `late_ext_rebut.py` | Adds the second, arguing-against pass to the empty-period review, as `triage.py` does for the other categories |
| `build_vulns.py` | Builds `data/flags.csv`, `data/reviewed.csv` and `data/by_category.csv` from the findings and the model review |
| `flags_chart.py` | Draws the chart at the top of the READMEs, in Portuguese and English, light and dark |
| `config.json` | The repository, the Portuguese category names, the paths that are not law, and the chart's labels |
| `patch_detectors.py` | Fixes blind spots found in runs on several country repositories in the copy of global-law's scripts (`python -X utf8 patch_detectors.py <scripts dir>`; a fix already in place is skipped) |
| `patch_detectors_vi.py` | The Vietnamese fixes made for an earlier run, in the same form; they change nothing in Portuguese text |
| `patch_es.py` | The Spanish date and currency fixes made for the Spain run, in the same form; `redo.py` runs it on every repository |
| `redo.py` | Runs `patch_detectors.py`, `patch_detectors_vi.py` and `patch_es.py`, then again only the scans and detectors the fixes change, the model review of lapsed time limits, references to deleted provisions and empty periods, and the build (`python -X utf8 redo.py <run folder> [--keep-reviews] [--full]`; `EMBED_FONTS` names the script that embeds the chart's fonts). It does not run `patch_pt.py`; run that first. Not needed here, as the fixes were in place before the first run |
| `late_ext_check.py` | Hand-check helper: for each empty period that survived the review, the lines of the extending commit's diff that change a date, its `In-force` and `Published` trailers, and, where this repository holds the extending act, its provisions on when it takes effect |

The model review needs `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` and `LLM_AUTH` set for an OpenAI-compatible Responses API.
It was run as `bash run_triage.sh '^(data/|tools/|README|REPRODUCE|LICENSE|jurisdiction)'`; every act is in a folder of its
own at the top level, so the review of lapsed time limits in law texts drew the same 40 flags as the review of all of them.

The detectors in this copy already carried every fix of `patch_detectors.py`. Changes made for this repository:

- `pins.json` names the corpus language as `pt` (global-law's list of corpora gave none), so the detectors use the
  Portuguese month names, and `patch_pt.py`'s Portuguese rules apply.
- `add_root.py`, unchanged, counts the kinds `law`, `decree` (changes made by decrees in the 1908 to 2002 history of a few
  codes and laws, and the decree-laws that enacted the CLT, the Criminal Code and the Code of Criminal Procedure) and
  `publisher` (the single version of the 5,000 acts held with their current text only) as law: 7,978 commits. The 24
  corrections (`Kind: correction`) and the 13 decisions of the Supreme Federal Court (`Kind: court`) are left out.
- `patch_pt.py`, dates: the time-limit search now also reads the first day of a month written as an ordinal ("até 1º de
  janeiro de 2021", "1o de março"), "31 de dezembro do ano de 2020" and "até a data de 30 de abril de 2020". Lapsed time
  limits went from 1,631 to 1,692; empty periods stayed at 37.
- `patch_pt.py`, references: "art. 3º-A" was read as Article 3 (the ordinal sign stopped the letter suffix) and "arts. 4º
  a 7º" as Article 4 alone; "§ 2º", a paragraph of an article in Brazilian law, was read as Article 2; a quoted article
  label that opens amended text ('"Art. 5º ...') was read as a reference to the amending act's own article; and "art. 90
  da Medida Provisória nº 2.158-35", "art. 2º, inciso II, da Lei nº 9.317", "art. 37 da Constituição Federal" or
  "artigos 4º a 6º do Decreto-lei nº 1.439" were read as references to the act's own articles. `ingest/refscan.py` now
  takes the language from `pins.json`, as `textscan.py` does, so that `placeholder_ref.py` and `dead_fine.py`, which call
  its `refs()` directly, apply the same rules. References to deleted provisions went from 269 to 195 (the last fix, for
  ranges and lists before "do Decreto-lei", came after the model review: the 5 flags it brought into the 40 strongest
  were reviewed then, and 5 earlier reviews no longer match a flag).
- `patch_pt.py`, repeal placeholders: an article whose text is a repeal clause ("Fica revogado o § 1º ...", "São
  revogados os artigos ...", "Revogam-se ...") was read as a "(Revogado)" placeholder, and so was an article that merely
  uses the word ("A remuneração poderá ser reduzida ou suprimida ..."); "revogado" and "suprimido" now count only right
  after the article's label, as in "Art. 212. (Revogado).". References to repealed placeholders went from 107 to 10.
- `patch_pt.py`, currencies: amounts in the old Brazilian currencies written with their symbols ("Cr$ 200,00",
  "Cz$ 10.000,00", "NCz$ 50,00", "CR$ 5.000,00") were not read, only the words "cruzeiros" and "cruzados"; and "marco"
  (a survey marker, "partindo do marco 26") was read as the German mark. Dead currencies went from 11 to 677.
- `patch_pt.py`, duplicate numbering: "§ 1º A não observância ..." was read as paragraph 1-A (the article "A" after a
  space taken for a letter suffix; Brazilian suffixes are written "§ 1º-A", sometimes "§ 2º -A." or "§ 1º A."), which
  split one paragraph number into several labels ("§ 1º a", "§ 1º o"); and "Art. 1.635" and "Art. 1.636" were both read
  as "art 1". Duplicate numbering went from 1,409 to 1,955, because the paragraphs that had been split by their first
  word now count together.
