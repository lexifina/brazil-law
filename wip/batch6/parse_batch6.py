"""Reads the cache and writes scripts/brazil-law/corpus.d/99-batch6.json (SCHEMA.md corpus part): the acts in ACTS
below (administrative improbity, environmental crimes, access to information, federal administrative procedure, and
further federal laws as they are verified).

    python -X utf8 scripts/brazil-law/batch6/parse_batch6.py [--stats] [--dry]

Imports ../batch5b/parse_batch5b.py (which configures ../batch5, ../batch4, ../batch3 and ../proc, the struck-text
replay of Planalto's annotated pages) and replaces only its configuration: the acts, the in-force days, the pins and
the output. Batch 5b's hand tables (MP fates, Senate resolutions, note fixes) stay in place; entries an act here does
not use are not printed. The parts of batch 5b and earlier are not touched (their parsers, run on their own, write the
same bytes as before). No network.

BATCH6_ACTS=<slug,...> selects acts for trial runs; by default the VERIFIED list is written.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
sys.path.insert(0, str(FOLDER / "batch5b"))
import parse_batch5b as PB5B  # noqa: E402  (configures batch 5 / 4 / 3 / parse_proc for batch 5b; reconfigured below)

B5, B4, B, P = PB5B.B5, PB5B.B4, PB5B.B, PB5B.P
PL = P.PL
B5.OUT = FOLDER / "corpus.d" / "99-batch6.json"
B5.STAGE = HERE / ".tmp" / "stage.json"
P.RETRIEVED = "2026-10-29"

PAGES = {k: v for k, v in PB5B.PAGES.items() if k in ("lia", "lia-compilada", "lca", "lai", "lpa")}
PAGES.update(EXTRA_PAGES := {})
B.PAGES.clear()
B.PAGES.update(PAGES)
B5.PAGES = PAGES

ALL_ACTS: list[dict] = [a for a in PB5B.ALL_ACTS if a["page"] in PAGES]
VERIFIED: list[str] = []
ENABLED = [s for s in os.environ.get("BATCH6_ACTS", "").split(",") if s] or VERIFIED
ACTS = [a for a in ALL_ACTS if a["slug"] in ENABLED]
B.ACTS[:] = ACTS
B5.ACTS = ACTS

# In-force days of the acts (their own closing clause and the DOU day; LC 95/1998 art. 8 § 1 counting).
ACT_DAY_ALL = dict(PB5B.ACT_DAY_ALL)
ACT_DAY_ALL.update({
    "lei-9605-1998": ("1998-03-30", "Lei 9.605/1998: its vigência article (art. 81) was vetoed, so LINDB art. 1 applies: in "
                                    "force 45 days after publication (DOU 13.2.1998), on 30.3.1998. The DOU of 17.2.1998 "
                                    "printed a retificação, but it corrects only the heading ('onde se lê: Nº 9.605, DE "
                                    "FEVEREIRO DE 1998 leia-se: LEI Nº 9.605, DE 12 DE FEVEREIRO DE 1998', as the Chamber of "
                                    "Deputies' record of the law gives it), not the law's text, so it is not a new "
                                    "publication of the text that would restart the period (LINDB art. 1 § 3)"),
    "lei-9784-1999": ("1999-02-01", "Lei 9.784/1999 art. 70: 'Esta Lei entra em vigor na data de sua publicação' (DOU "
                                    "1.2.1999). The retificação in the DOU of 11.3.1999 corrects only the signatures ('Na "
                                    "página 5, 1ª coluna, nas assinaturas, leia-se: Fernando Henrique Cardoso, Renan "
                                    "Calheiros e Paulo Paiva', as the Chamber of Deputies' record of the law gives it), not "
                                    "the law's text"),
})
ACT_LAWS_ALL = dict(PB5B.ACT_LAWS_ALL)
ACT_LAWS_ALL.update({
    "lei-9605-1998": B._act_law("Lei nº 9.605, de 1998", "Dispõe sobre as sanções penais e administrativas derivadas de "
                                "condutas e atividades lesivas ao meio ambiente, e dá outras providências.", "1998-02-12",
                                "1998-02-13", PAGES["lca"]),
    "lei-9784-1999": B._act_law("Lei nº 9.784, de 1999", "Regula o processo administrativo no âmbito da Administração "
                                "Pública Federal.", "1999-01-29", "1999-02-01", PAGES["lpa"]),
})
B.ACT_DAY.clear()
B.ACT_DAY.update({k: v for k, v in ACT_DAY_ALL.items() if any(a["law"] == k for a in ACTS)})
B.ACT_LAWS.clear()
B.ACT_LAWS.update({k: v for k, v in ACT_LAWS_ALL.items() if any(a["law"] == k for a in ACTS)})

# Amending laws whose own vigência is staged by level of government: dated by the first day the new wording was law
# (for the União, the States and the Distrito Federal); the later day for the other levels is given in the reason.
P.VIGENCIA_FIXED["lei-13019-2014"] = (
    "2016-01-23", "art. 88 as amended by Lei 13.204/2015: 'Esta Lei entra em vigor após decorridos quinhentos e quarenta "
                  "dias de sua publicação oficial' (DOU 1.8.2014: the 540th day counted from publication is 22.1.2016, "
                  "LC 95/1998 art. 8 § 1), and § 1: 'Para os Municípios, esta Lei entra em vigor a partir de 1º de janeiro "
                  "de 2017'. Its changes are dated 23.1.2016, the day they became law for the União, the States and the "
                  "Distrito Federal; for the Municípios they applied from 1.1.2017")
P.VIGENCIA_FIXED["lei-14129-2021"] = (
    "2021-06-28", "art. 55: 'Esta Lei entra em vigor após decorridos: I - 90 (noventa) dias de sua publicação oficial, "
                  "para a União; II - 120 (cento e vinte) dias [...] para os Estados e o Distrito Federal; III - 180 (cento "
                  "e oitenta) dias [...] para os Municípios' (DOU 30.3.2021: the 90th day counted from publication is "
                  "27.6.2021, LC 95/1998 art. 8 § 1). Its changes are dated 28.6.2021, the day they became law for the "
                  "União; for the States and the Distrito Federal they applied from 28.7.2021, for the Municípios from "
                  "26.9.2021")

# ---------------------------------------------------------------------------------------------------------------
# Medidas Provisórias reissued with a changed wording, where the act's page prints both wordings and credits each to
# its own reissue ('Incluído pela Medida Provisória nº 1.710, de 1998', then 'Redação dada pela Medida Provisória nº
# 1.710-1, de 1998'). parse_proc keys an MP by its base number, which would date both wordings by the first issue; a
# reissue listed here gets its own key (mp-<n>r<reissue>-<year>), page and day. Other reissues keep the base key.
REISSUES: set[tuple[str, str, str]] = {("1710", "1", "1998")}
REISSUE_KEY = re.compile(r"^mp-(\d+)r(\d+)-(\d{4})$")
REISSUE_REF = re.compile(r"Medida\s+Provis[óo]ria\s*(?:n\s*[º°o]?\s*\.?)?\s*(\d{1,2}(?:\.\d{3})+|\d+)-(\d{1,2})(?!\d)\s*,?\s*de\s+(\d{4})", re.I)
_law_key6, _law_label6, _lexml_url6, _page_info6 = P.law_key, P.law_label, P.lexml_url, P.page_info


def law_key(text: str, year_of: dict | None = None) -> str | None:
    m = REISSUE_REF.search(text)
    if m:
        n = m.group(1).replace(".", "")
        if (n, m.group(2), m.group(3)) in REISSUES and not P.LAW_REF.search(text[:m.start()]):
            return f"mp-{n}r{m.group(2)}-{m.group(3)}"
    return _law_key6(text, year_of)


def law_label(key: str) -> str:
    m = REISSUE_KEY.match(key)
    if m:
        return f"Medida Provisória nº {int(m.group(1)):,}-{m.group(2)}, de {m.group(3)}".replace(",", ".")
    return _law_label6(key)


def lexml_url(key: str, enacted: str | None) -> str | None:
    m = REISSUE_KEY.match(key)
    if m:
        return f"{P.LEXML}medida.provisoria:{enacted};{m.group(1)}-{m.group(2)}" if enacted else None
    return _lexml_url6(key, enacted)


# MP pages whose heading leaves out the 'DE' before the year ('MEDIDA PROVISÓRIA Nº 62, DE 22 DE AGOSTO 2002'): the
# heading is read with it put back (only for page_info's dates; the act pages are not touched)
HEAD_NO_DE = re.compile(r"(\bDE\s+\d{1,2}\s*[º°o]?\s+DE\s+(?:JANEIRO|FEVEREIRO|MAR[ÇC]O|ABRIL|MAIO|JUNHO|JULHO|AGOSTO|SETEMBRO|"
                        r"OUTUBRO|NOVEMBRO|DEZEMBRO))\s+(\d{4})")
HEAD_FIXED: list[str] = []


def page_info(key: str) -> dict:
    """parse_proc/batch 3 page_info; a reissue key reads its own pinned page under the base key's number check, and a
    heading with no 'DE' before the year is read with it."""
    m = REISSUE_KEY.match(key)
    base = f"mp-{m.group(1)}-{m.group(3)}" if m else key
    raw0, dec0 = P.raw, P.decode

    def raw(ident: str):
        return raw0("law:" + key) if (m and ident == "law:" + base) else raw0(ident)

    def decode(b: bytes) -> str:
        t = dec0(b)
        t2 = HEAD_NO_DE.sub(r"\1 DE \2", t, count=1)
        if t2 != t:
            HEAD_FIXED.append(key)
        return t2
    P.raw, P.decode = raw, decode
    try:
        info = _page_info6(base)
    finally:
        P.raw, P.decode = raw0, dec0
    if m and info:
        P.LEXML_USED.discard(_lexml_url6(base, info.get("enacted")))
        P.LEXML_USED.add(lexml_url(key, info.get("enacted")))
    return info


P.law_key, P.law_label, P.lexml_url, P.page_info = law_key, law_label, lexml_url, page_info
B.law_key, B.law_label, B.lexml_url, B.page_info = law_key, law_label, lexml_url, page_info

# An MP the Senate declared 'prejudicada' after rejecting its conversion bill: Planalto prints 'Prejudicada' after the
# struck wording (Lei 9.605 art. 25 § 5º), read like '(Vigência encerrada)'
P.LAPSED_WORDS = re.compile(P.LAPSED_WORDS.pattern + r"|(?<=[.;:])\s*(?-i:Prejudicad[ao])\s*$", re.I)
P.MP_LAPSE["mp-62-2002"] = (
    "2002-11-20", "declared 'prejudicada': Ato Declaratório do Presidente do Senado Federal de 20.11.2002 (DOU 21.11.2002): "
                  "'em sessão realizada no dia 20 de novembro de 2002, o Plenário da Casa declarou prejudicada a Medida "
                  "Provisória nº 62, de 22 de agosto de 2002 [...] em virtude da rejeição do Projeto de Lei de Conversão nº "
                  "27, de 2002'; the Lei 9.605 wording of art. 25 it had replaced is back from that day")
B5.MP_REJECTED["mp-62-2002"] = (
    "Medida Provisória nº 62, de 2002: prejudicada",
    "Medida Provisória nº 62, de 2002, declared prejudicada by the Senate after its conversion bill was rejected (Ato "
    "Declaratório de 20 de novembro de 2002)")
P.MP_PENDING.update({
    "mp-1710-1998": "Medida Provisória nº 1.710, de 7.8.1998, 'Reeditada pela MPv nº 1.710-1, de 1998', whose changed "
                    "wording of Lei 9.605 art. 79-A Planalto prints and credits separately: the reissue's wording ends it",
    "mp-1710r1-1998": "Medida Provisória nº 1.710-1, de 8.9.1998, 'Reeditada pela MPv nº 1.710-2, de 1998', a chain of "
                      "reissues down to MP 2.163-41, de 23.8.2001; Planalto prints no wording of the reissues in between, "
                      "so its wording of Lei 9.605 art. 79-A stands until MP 2.163-41's",
    "mp-2163-2001": "Medida Provisória nº 2.163-41, de 23.8.2001 (DOU 24.8.2001) was in force on 11.9.2001, so it stays in "
                    "force until a later MP revokes it or Congress votes on it (Emenda Constitucional 32/2001, art. 2)",
})

SRC = HERE / "sources_batch6.json"
B5.SRC = SRC
B5.PIN_FILES = B5.PIN_FILES + [SRC]

if __name__ == "__main__":
    sys.exit(P.main(sys.argv[1:]))
