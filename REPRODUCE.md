# How this repository was made

1. The World Law Sources register (https://claude.ai/artifact/DdS9F6yqpPZtV2i7FGQhYZ, private to Lexifina) was compiled on 28 October 2026 by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`), with research sub-agents on the same model. They read each source’s own pages, official descriptions, and Internet Archive copies for sites that block automated readers. Links were checked with curl.
2. The register rows were exported to `scripts/world-law/register.json` in the Lexifina repository (sha256 `d9227a6c3bb0ede0311f050e70af718ec0dfbec2248ea97e85efa8bb995caab1`).
3. `python scripts/world-law/build_countries.py <out> --push` (script blob `05900382ae230db5d92569e1581ac13a5e7d8ce6`) wrote README.md, SOURCES.md, jurisdiction.json and this file for every country, committed them as one commit dated 2026-10-28T12:00:00+00:00 by Lexifina <world-law@lexifina.com>, and pushed each to a private repository under the lexifina organisation.

No AI model runs in step 3, and no AI wrote legal text. Rebuilding from the same register gives the same commit hashes.

When the first law history is built for this country, that build replaces this placeholder history entirely (a fresh history, force-pushed) and records its own steps here. It never appends to the placeholder commit.
