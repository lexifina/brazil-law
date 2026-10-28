"""Reads the cache and writes scripts/brazil-law/corpus.d/90-batch3.json (SCHEMA.md corpus part).

    python -X utf8 scripts/brazil-law/batch3/parse_batch3.py [--stats] [--dry]

Imports ../proc/parse_proc.py (the CPP/CDC helper's struck-text replay of Planalto's annotated pages) and only
replaces its configuration: the acts, the hand tables, the pin file and the output. No network.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
sys.path.insert(0, str(FOLDER))
sys.path.insert(0, str(FOLDER / "proc"))
import parse_proc as P  # noqa: E402

PL = P.PL
PAGES = {
    "ctn": "leis/l5172.htm",
    "ctn-compilado": "leis/l5172compilado.htm",
    "eca": "leis/l8069.htm",
    "eca-compilado": "leis/l8069compilado.htm",
    "ce": "leis/l4737.htm",
    "ce-compilado": "leis/l4737compilado.htm",
}

ACTS: list[dict] = []
P.ACTS = ACTS


def main(argv: list[str]) -> int:
    return P.main(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
