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
    "rju": "leis/l8112cons.htm",
    "rju-compilado": "leis/l8112compilado.htm",
}

ACTS: list[dict] = [
    {"slug": "codigo-tributario-nacional", "short": "CTN", "page": "ctn", "consolidated": "ctn-compilado",
     "law": "lei-5172-1966", "title": "Código Tributário Nacional (Lei nº 5.172, de 25 de outubro de 1966)",
     "digits": 3, "url": PL + "leis/l5172compilado.htm"},
    {"slug": "estatuto-da-crianca-e-do-adolescente", "short": "ECA", "page": "eca", "consolidated": "eca-compilado",
     "law": "lei-8069-1990", "title": "Estatuto da Criança e do Adolescente (Lei nº 8.069, de 13 de julho de 1990)",
     "digits": 3, "url": PL + "leis/l8069compilado.htm"},
    {"slug": "codigo-eleitoral", "short": "CE", "page": "ce", "consolidated": "ce-compilado",
     "law": "lei-4737-1965", "title": "Código Eleitoral (Lei nº 4.737, de 15 de julho de 1965)",
     "digits": 3, "url": PL + "leis/l4737compilado.htm"},
]
P.ACTS = ACTS

ACT_DAY = {
    "lei-5172-1966": ("1967-01-01", "Lei 5.172/1966 art. 218: 'Esta Lei entrará em vigor, em todo o território nacional, "
                                    "no dia 1º de janeiro de 1967' (published in the DOU of 27.10.1966, rectified "
                                    "31.10.1966)"),
    "lei-8069-1990": ("1990-10-14", "Lei 8.069/1990 art. 266: 'Esta Lei entra em vigor noventa dias após sua publicação' "
                                    "(published in the DOU of 16.7.1990, rectified 27.9.1990): 16.7.1990 + 90 days = "
                                    "14.10.1990"),
    "lei-4737-1965": ("1965-08-18", "Lei 4.737/1965 art. 382: 'Êste Código entrará em vigor 30 dias após a sua "
                                    "publicação' (published in the DOU of 19.7.1965, rectified 30.7.1965): 19.7.1965 + "
                                    "30 days = 18.8.1965"),
}
P.ACT_DAY = ACT_DAY


def _act_law(label, title, enacted, published, rel):
    return {"label": label, "title": title, "kind": "law", "enacted": enacted, "published": published,
            "url": PL + rel, "temporary_until": None, "restores": None, "note": None}


ACT_LAWS = {
    "lei-5172-1966": _act_law("Lei nº 5.172, de 1966", "Dispõe sôbre o Sistema Tributário Nacional e institui normas "
                              "gerais de direito tributário aplicáveis à União, Estados e Municípios.",
                              "1966-10-25", "1966-10-27", "leis/l5172.htm"),
    "lei-8069-1990": _act_law("Lei nº 8.069, de 1990", "Dispõe sobre o Estatuto da Criança e do Adolescente e dá outras "
                              "providências.", "1990-07-13", "1990-07-16", "leis/l8069.htm"),
    "lei-4737-1965": _act_law("Lei nº 4.737, de 1965", "Institui o Código Eleitoral.", "1965-07-15", "1965-07-19",
                              "leis/l4737.htm"),
}
P.ACT_LAWS = ACT_LAWS


def main(argv: list[str]) -> int:
    return P.main(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
