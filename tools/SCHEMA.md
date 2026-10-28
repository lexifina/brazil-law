# gitlaw_common: the corpus.json contract

The goal is one builder for every country. A country folder (`scripts/<slug>-law/`) writes only:

- `fetch.py`: downloads into `.cache/`. The cache is named by the sha256 of the URL, goes through curl, is polite and resumable, and records every request in `.cache/requests.jsonl`.
- `parse.py`: reads only the cache and writes `corpus.json`. It is deterministic: the same cache gives the same bytes.
- `repo/`: the country's static docs (`README.md` with the standard sections, `LICENSE`, and optionally `tools/<local-name>.py` as a thin wrapper around `tools/on.py`).

The shared builder turns `corpus.json` into the git repository. It produces:

- the commits, streamed through `git fast-import`
- the tags and the future branch
- `REPRODUCE.md` and `data/versions.json`
- `tools/on.py`, `tools/check_repo.py` and `tools/build.py`
- the site data
- the checks

The commands are:

    python -X utf8 scripts/gitlaw_common/build.py scripts/<slug>-law --repo ~/Documents/<slug>-law --docs-date YYYY-MM-DD
    python -X utf8 scripts/gitlaw_common/check.py ~/Documents/<slug>-law --corpus scripts/<slug>-law/corpus.json
    python -X utf8 scripts/gitlaw_common/build.py scripts/<slug>-law --repo <tmp> --docs-date D --compare ~/Documents/<slug>-law

`--docs-date` is required: use the day the data was retrieved, never the run day. The builder empties the target and keeps `origin`. It refuses to run if the target holds anything other than an earlier build.

## corpus.json

All dates are ISO `YYYY-MM-DD`. All text is UTF-8 with `\n` line endings. Keys and values are plain JSON.

```json
{
  "country": {
    "code": "CL", "name": "Chile", "slug": "chile", "lang": "es",
    "tz": "America/Santiago",
    "future_branch": "futuro",
    "publisher": {"name": "Biblioteca del Congreso Nacional (LeyChile)", "email": "bcn@leychile.invalid"},
    "default_in_force_rule": {"text": "Código Civil art. 7: a law is binding from its publication in the Diario Oficial",
                              "source": "https://www.bcn.cl/leychile/navegar?idNorma=172986"},
    "licence_note": "exact attribution line the source requires"
  },
  "sources": [
    {"name": "LeyChile (BCN)", "url": "https://www.bcn.cl/leychile", "retrieved": "2026-10-28", "requests": 412,
     "licence": "…", "notes": "…"}
  ],
  "laws": {
    "ley-21200": {
      "label": "Ley 21.200",
      "title": "Modifica el capítulo XV de la Constitución Política de la República",
      "kind": "law",
      "enacted": "2019-12-23",
      "published": "2019-12-24",
      "url": "https://www.bcn.cl/leychile/navegar?idNorma=1140340",
      "temporary_until": null,
      "restores": null,
      "note": null
    }
  },
  "acts": [
    {
      "slug": "constitucion",
      "short": "CPR",
      "title": "Constitución Política de la República de Chile",
      "url": "https://www.bcn.cl/leychile/navegar?idNorma=242302",
      "first_law": "dl-1980-1150",
      "earlier_laws": [],
      "versions": [
        {
          "from": "1981-03-11",
          "source_url": "https://…version…",
          "sha256": "sha256 of the cached source bytes this version was parsed from",
          "units": {
            "art-019": {"label": "Art. 19", "kind": "art", "text": "one paragraph per line\nnext paragraph\n"},
            "disp-transitoria-01": {"label": "Disposición transitoria primera", "kind": "transitional", "text": "…"}
          },
          "credits": {"art-019": ["ley-21200"], "art-020": ["ley-21200", "ley-20050"]},
          "note": "optional: anything a reader of this version should know"
        }
      ]
    }
  ],
  "applies": [
    {"law": "ley-21200", "provision": "art-019",
     "groups": [{"conditions": [{"kind": "commenced_on_or_after", "date": "2020-01-01"}], "set_by": "Ley 21.200, art. 2 transitorio"}]}
  ],
  "decisions": ["Every decision made by hand, one sentence each, so it is printed in REPRODUCE.md."],
  "ai_use": ["What a model did at data-build time, with counts. Write 'none' if none."]
}
```

### The rules the builder enforces (do not work around them)

**Unit keys and text**
- A unit key becomes the file path `<act slug>/<key>.md`.
- Keys must be lowercase ASCII `[a-z0-9-]` and sort naturally. Zero-pad numbers: `art-005`, `art-005-bis`.
- A unit's text is one paragraph or item per line, so blame works line by line, and it ends with `\n`.
- The first line may be a heading (`# Art. 19`). Keep volatile metadata (version numbers, source URLs) out of the text.
- Normalise publisher typesetting once in parse.py: NBSP becomes a space, collapse runs of spaces, use one form of quotes and dashes, and drop footnote markers.

**Versions and dates**
- `versions` is ordered by `from`.
- `from` is the day the version took effect: the in-force date, not the publication date. When the source gives only the publication date, apply the country's `default_in_force_rule`, or the law's own vigencia clause, in parse.py. Write that down in `decisions`.
- Versions with `from` after the build's `--docs-date` go on `future_branch`.

**Credits**
- `credits` maps every unit that differs from the previous version (added, changed or removed) to the law(s) that changed it.
- The builder writes one commit per law per in-force day, holding exactly the units credited to that law.
- A changed unit with no credit is committed separately, by the `publisher`, labelled "unexplained".
- Never guess a credit. If two laws are credited to one unit on the same day, the unit goes in the later law's commit and both are named in its message.
- The first version is credited to `first_law` if it is the act as enacted. Otherwise (`first_law: null`) it is credited to the publisher as "oldest version available", naming `earlier_laws`.

**Laws**
- `kind` is one of `law`, `decree`, `court`, `referendum`, `publisher` or `treaty`.
- A court ruling that strikes or conditions text is `kind: "court"`, for example Colombia C-xxx/yy (inexequible) and Brazil STF ADI. It is credited like a law, with the decision date as `enacted` and the date it took effect on the text as the version `from`.
- Temporary measures that lapse, such as Brazil's Medidas Provisórias and Argentina's DNU, set `temporary_until`. The lapse is a version credited to the law with `restores` set.
- The email is derived as `<law key>@<publisher-domain>.invalid`, so law keys must also be ASCII `[a-z0-9-]`.

**Applicability and data quality**
- A law may carry a `note`: one or two plain sentences that the commit message prints instead of the standard line for its kind. Use it for events that change no words, such as a referendum that was rejected or a ruling that only interprets. Credit such an event to the provisions it concerns in that version's `credits`, so it gets a commit with `Words-changed: no`; it needs a version (a `from` day) of its own only if the source has one.
- A version may omit `units`: it then reads as the version before it. Use this for an event that changed no words, with `credits` naming the provisions it concerns. Its commit names them in `Affecting:` and in the subject ("…, wording unchanged").
- **Large acts:** instead of `units`, a version may give `changes`: `{unit key: unit, or null to remove it}`, applied to the version before it. Use this for any act with many versions. It keeps part files small: GitHub rejects files over 100 MB, and wip snapshots skip files over 50 MB.
- **Two versions on one day:** a version may share its `from` day with the one before it if it is marked `"same_day": true`. Example: a law that repeals provisions on the very day the act first applies. Its commits come after the earlier version's on that day. check.py compares the day's state with the last version of the day, and the day before with the last version before it.
- `applies` is only for typed applicability from transitional provisions, in the group schema in memory/git_for_law.md.
- Leave `applies` empty rather than invent.
- Everything must be reproducible from the cache: no network in parse.py, and no model output treated as legal text.

## Splitting one country across several agents: corpus.d/

A country may also have `corpus.d/*.json` parts beside (or instead of) `corpus.json`. Each part holds `acts`, and optionally `laws`, `sources`, `applies`, `decisions` and `ai_use`. One part takes `country` if corpus.json is absent.

How parts are read:
- In file-name order (`20-codigo-civil.json`).
- Laws are merged by key. The same key in two files must have the same label, or the build stops.
- The build, check.py and autopush all read the merged corpus.

How to work with them:
- Each agent owns only its own part file and writes it atomically: write `.tmp`, then rename.
- Act slugs must not collide across parts.

Verification of parts: `main` holds corpus.json once the country's `PUBLISH` exists, and each part only once its owner writes `corpus.d/<part>.PUBLISH` (for example `50-codes.PUBLISH`). That file gives one line saying what was verified against the official text. Unverified parts still stream to the `preview` branch, together with everything else. Builds reading only verified parts set `GITLAW_VERIFIED_PARTS_ONLY=1`.

## Per-act publisher (optional, 2026-10-29)
An act may carry `"publisher": {"name": ..., "email": "...@<domain>.invalid"}` when its text comes from a different source than the country's publisher (for example a ministry's revised edition, SILEP, Veritas). That act's "oldest version available" commit and its unexplained changes are then authored by it. A commit spanning acts with different publishers uses the country's. Corpora without the field build byte-identically to before.
