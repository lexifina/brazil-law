# How this repository was made ({{NAME}})

This file is written by the build on {{DOCS_DATE}}, the day the source data was retrieved. Everything below is enough to rebuild this repository hash for hash.

## Sources

| Source | Address | Retrieved | Requests | Licence |
| --- | --- | --- | ---: | --- |
{{SOURCES}}

Every response is cached by the sha256 of its URL, and the table above lists every source with its retrieval date. Lexifina keeps its fetch scripts privately; `tools/parse.py` reads only the cache and writes `corpus.json`, so the same cache always gives the same corpus.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
{{ACTS}}

The build made {{COMMITS}} commits:

| Commits | Kind |
| ---: | --- |
| {{START_COMMITS}} | first version of an act |
| {{LAW_COMMITS}} | one law on its in-force day |
| {{UNEXPLAINED}} | changes no amendment note explains, credited to the publisher |

Other counts:
- {{FUTURE}} commits on the branch `{{FUTURE_BRANCH}}`: laws not yet in force on {{DOCS_DATE}}.
- {{CLAMPED}} commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- {{LAWS}} laws in the record.
- {{TAGS}} tags.

## Dates

Each commit is dated at noon ({{TZ}}) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: {{RULE}} {{RULE_SOURCE}}

## Commands, in order

```sh
# fill the cache from the sources listed above (network; Lexifina's fetch scripts are kept privately)
python -X utf8 tools/parse.py                  # cache -> corpus.json (no network)
python -X utf8 tools/build.py <folder> --repo <empty folder> --docs-date {{DOCS_DATE}}
python -X utf8 tools/check_repo.py <repo> --corpus <folder>/corpus.json --write
python -X utf8 tools/build.py <folder> --repo <another empty folder> --docs-date {{DOCS_DATE}} --compare <repo>
```

In the main Lexifina repository these files live as follows:
- `fetch.py`, `parse.py` and `repo/`: in `scripts/{{SLUG}}-law/`.
- `build.py`, `check_repo.py` (`check.py` there) and `on.py`: in `scripts/gitlaw_common/`, with the corpus format in `SCHEMA.md`.

## Exact inputs

- `corpus.json` sha256 `{{CORPUS_SHA}}` ({{CORPUS_BYTES}} bytes)
- Script blob hashes (`git hash-object`):

| Script | Blob |
| --- | --- |
| build.py | `{{BUILD_BLOB}}` |
| check.py | `{{CHECK_BLOB}}` |
| on.py | `{{ON_BLOB}}` |
| fetch.py | `{{FETCH_BLOB}}` |
| parse.py | `{{PARSE_BLOB}}` |

- Tools:
  - {{PYTHON}}
  - {{GIT}}
  - {{CURL}}

## Checks

{{CHECK}}

{{REBUILD}}

These results are from the check run on the build before this one, from the same corpus.

## Decisions made by hand

{{DECISIONS}}

## What AI did and did not do

The fetch, parse and check scripts were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above, through code that anyone can rerun.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
{{AI_USE}}
