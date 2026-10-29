# Issues for the coordinator (gitlaw-BR)

1. autopush.py wip snapshot fails when the country folder holds a second scratch git repo whose name is not in
   SKIP_DIRS (a `--compare` rebuild into `.tmp-build2`):
   `git update-index --add --cacheinfo: error: Invalid path 'wip/.tmp-build2/.git/config'`.
   Worked around by deleting `.tmp-build2` after the compare. Suggest skipping any `.tmp*` directory and any
   directory containing `.git`.

2. build.py change_message: when a law changes words in some units and is also credited to a unit whose words did not
   change (SCHEMA "credit such an event to the provisions it concerns"), the unchanged unit is not named anywhere in
   the commit (no `Affecting:` entry). Example: version 2023-12-04 credits `stf-adi-7047` to `art-100` (changed) and
   `adct-art-101` (ruled unconstitutional, words unchanged on Planalto); the commit names only Art. 100. Suggest
   listing such units as "Concerned (wording unchanged): ..." in the body and in `Affecting:`.

**Fixed by the coordinator (2026-10-28):** (1) autopush skips .tmp* folders and nested .git; (2) Also-concerns: trailer names credited provisions a law left unchanged; (3) corpus.d parts need their own <part>.PUBLISH to reach main.

3. `build.py --compare` writes a `rebuild` entry into the country folder's verification.json, which the docs commit
   then includes, so a compare run right after a build reports `"main_identical": false` while the history is
   identical (seen on Brazil with corpus.d parts, 19:2xZ). Suggest leaving verification.json out of the docs commit
   or writing the compare result elsewhere.
