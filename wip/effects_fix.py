"""effects_fix.py: date each change by the day it takes effect where the amending act fixes a later 'produção de efeitos'
day for it (coordinator rule, 2026-10-31: 'we record the day text actually applies; dates after today go on futuro').

    python -X utf8 scripts/brazil-law/effects_fix.py <part.json> [--out FILE] [--report]

A post-step over a written part (the parsers date every change by its law's in-force day): for each entry of MOVES for
the part, the changes the named law made on the named day are split into hunks (difflib over the unit's lines, before
and after that version); each hunk gets the day its selector gives (the effect day; None = never took effect, because a
later act replaced it before that day), and the unit's text is rebuilt for every day from the version day to the unit's
next change: the old text with the hunks of each day applied. New versions are added on effect days that have none,
credited to the same law; a version left with no change is dropped. The part's decisions record every unit moved. The
step refuses an effect day on or after the unit's next change (a conflict to settle by hand). Idempotent: a part whose
decisions already hold the effect-days decision is left as it is. No network.
"""
from __future__ import annotations

import copy
import difflib
import json
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
MARK = "Effect days (produção de efeitos):"
WARN: list[str] = []
TODAY = "2026-10-31"


def _norm(s: str) -> str:
    s = s.lower().replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    s = re.sub(r"[\"'.…]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def ALL(hunk) -> bool:
    return True


def lines_match(rx: str):
    r = re.compile(rx)

    def f(h):
        return any(r.search(x) for x in h["new"] + h["old"])
    f.__name__ = f"lines_match({rx!r})"
    return f


def new_in(ref: str, minlen: int = 25):
    """a hunk whose new lines (long enough to be telling) are found word for word in a reference text"""
    R = _norm(ref)

    def f(h):
        ls = [_norm(x) for x in h["new"] if len(_norm(x)) >= minlen]
        return bool(ls) and all(x[:120] in R for x in ls)
    return f


# ---------------------------------------------------------------------------------------------------------------------
# Reference texts read from the cached pages (LC 214/2025 art. 517, the articles whose effects start on 1.1.2027)
_REF: dict[str, str] = {}


def ref(key: str) -> str:
    if key not in _REF:
        import html as _h
        import os
        os.environ.setdefault("BATCH14_ACTS", "-")
        sys.path.insert(0, str(HERE / "batch14"))
        import parse_batch14 as M  # noqa: E402
        lawkey, a, b = key.split("|")
        t = _h.unescape(re.sub(r"<[^>]+>", " ", M.P.decode(M.P.raw("law:" + lawkey)[0])))
        t = re.sub(r"\s+", " ", t)
        t = re.sub(r"\[\[S:.*?:S\]\]", " ", t)
        i = t.find(a)
        j = t.find(b, i + len(a))
        assert i >= 0 and j > i, key
        _REF[key] = t[i:j]
    return _REF[key]


def lc214_517(h) -> bool:
    return new_in(ref("lc-214-2025|Art. 517. A Lei Complementar nº 123|Art. 518. A Lei Complementar nº 123"))(h)


# ---------------------------------------------------------------------------------------------------------------------
# MOVES: part -> [(act, law, version day, [(selector, effect day or None)], why)]. The first selector a hunk matches
# gives its day; hunks no selector matches stay on the version day.
_LC214 = ("Lei Complementar 214/2025 art. 544: 'Esta Lei Complementar entra em vigor na data de sua publicação, produzindo "
          "efeitos: [...] III - a partir de 1º de janeiro de 2027, em relação aos arts. [...] 509 a 515, 517 [...]; [...] VI - a "
          "partir de 1º de janeiro de 2026, em relação aos demais dispositivos'")
MOVES: dict[str, list] = {
    "corpus.json": [
        ("constituicao", "ec-58-2009", "2009-09-23", [("units:art-029-a", "2010-01-01")],
         "Emenda Constitucional 58/2009 art. 3: 'produzindo efeitos: I - o disposto no art. 1º, a partir do processo "
         "eleitoral de 2008 [before the amendment: kept on its in-force day]; e II - o disposto no art. 2º, a partir de 1º "
         "de janeiro do ano subsequente ao da promulgação desta Emenda' (promulgated 23.9.2009): art. 2's change to art. "
         "29-A from 1.1.2010"),
        ("constituicao", "ec-69-2012", "2012-03-30", [(ALL, "2012-07-28")],
         "Emenda Constitucional 69/2012 art. 4: 'produzindo efeitos quanto ao disposto no art. 1º após decorridos 120 "
         "(cento e vinte) dias de sua publicação oficial' (DOU 30.3.2012): art. 1's changes from 28.7.2012"),
        ("constituicao", "ec-87-2015", "2015-04-17", [(ALL, "2016-01-01")],
         "Emenda Constitucional 87/2015 art. 3: 'produzindo efeitos no ano subsequente e após 90 (noventa) dias desta' "
         "(DOU 17.4.2015): from 1.1.2016"),
        ("constituicao", "ec-100-2019", "2019-06-27", [(ALL, "2020-01-01")],
         "Emenda Constitucional 100/2019 art. 4: 'produzirá efeitos a partir da execução orçamentária do exercício "
         "financeiro subsequente' (DOU 27.6.2019): from 1.1.2020"),
        ("constituicao", "ec-102-2019", "2019-09-27", [("not-adct", "2020-01-01")],
         "Emenda Constitucional 102/2019 art. 4: 'produzirá efeitos a partir da execução orçamentária do exercício "
         "financeiro subsequente, excetuada a alteração ao Ato das Disposições Constitucionais Transitórias, que terá "
         "eficácia no mesmo exercício de sua publicação' (DOU 27.9.2019): its changes to the permanent text from 1.1.2020, "
         "its ADCT change on its in-force day"),
    ],
    "50-codes.json": [
        ("codigo-civil", "lei-14905-2024", "2024-07-01",
         [(lines_match(r"^§ 2º A metodologia de cálculo da taxa legal"), "2024-07-01"), (ALL, "2024-08-30")],
         "Lei 14.905/2024 art. 5: 'produzirá efeitos: I - na data de sua publicação, quanto à parte do art. 2º que inclui o "
         "§ 2º no art. 406 [...]; e II - 60 (sessenta) dias após a data de sua publicação, quanto aos demais dispositivos' "
         "(DOU 1.7.2024): from 30.8.2024, art. 406 § 2º on publication"),
    ],
    "90-batch3.json": [
        ("codigo-tributario-nacional", "lc-91-1997", "1997-12-23", [(ALL, "1998-01-01")],
         "Lei Complementar 91/1997 art. 6: 'produzindo efeitos a partir de 1º de janeiro de 1998'"),
        ("codigo-tributario-nacional", "lc-214-2025", "2025-01-16", [(ALL, "2026-01-01")],
         _LC214 + "; its change to the CTN (art. 496) falls under VI: from 1.1.2026"),
        ("estatuto-da-crianca-e-do-adolescente", "lei-9532-1997", "1997-12-11", [(ALL, "1998-01-01")],
         "Lei 9.532/1997 art. 81: 'produzindo efeitos: I - nessa data, em relação aos arts. 9º, 37 a 42, 44 a 54, 64 a 68, "
         "74 e 75; II - a partir de 1º de janeiro de 1998, em relação aos demais dispositivos': its change to the ECA (art. "
         "6) from 1.1.1998"),
    ],
    "95-rju.json": [
        ("regime-juridico-dos-servidores-publicos", "mp-689-2015", "2015-08-31", [(ALL, "2015-12-01")],
         "Medida Provisória 689/2015 art. 3: 'produzindo efeitos a partir do primeiro dia do quarto mês subsequente ao de "
         "sua publicação' (DOU 31.8.2015): from 1.12.2015, until the MP lapsed"),
    ],
    "99-batch5b.json": [
        ("lei-do-inquilinato", "lei-11196-2005", "2005-11-22", [(ALL, "2006-01-01")],
         "Lei 11.196/2005 art. 132: 'produzindo efeitos: [...] IV - a partir de 1º de janeiro de 2006, em relação ao "
         "disposto: [...] b) nos arts. 17 a 27, 31 e 32, 34, 70 a 75 e 76 a 90 desta Lei': its change to the Lei do "
         "Inquilinato (art. 89) from 1.1.2006"),
        ("lei-de-mediacao", "lei-13327-2016", "2016-07-29", [(ALL, "2016-08-01")],
         "Lei 13.327/2016 art. 42: 'produzindo efeitos a partir de 1º de agosto de 2016' (DOU 29.7.2016)"),
    ],
    "99-batch6.json": [
        ("lei-de-improbidade-administrativa", "lc-157-2016", "2016-12-30", [(ALL, "2017-12-31")],
         "Lei Complementar 157/2016 art. 7 § 1: 'O disposto [...] no art. 10-A, no inciso IV do art. 12 e no § 13 do art. 17, "
         "todos da Lei nº 8.429 [...] somente produzirão efeitos após o decurso do prazo referido no art. 6º' (one year from "
         "publication, DOU 30.12.2016; the year ends on 30.12.2017, Lei 810/1949): from 31.12.2017"),
    ],
    "99-batch7.json": [
        ("lei-de-responsabilidade-fiscal", "lc-164-2018", "2018-12-18", [(ALL, "2019-01-01")],
         "Lei Complementar 164/2018 art. 2: 'produzirá efeitos a partir do exercício financeiro subsequente'"),
        ("lei-de-responsabilidade-fiscal", "lc-214-2025", "2025-01-16", [(ALL, "2026-01-01")],
         _LC214 + "; its change to the LRF (art. 535) falls under VI: from 1.1.2026"),
        ("lei-de-responsabilidade-fiscal", "lc-224-2025", "2025-12-26", [(ALL, "2026-01-01")],
         "Lei Complementar 224/2025 art. 15: 'produzirá efeitos: I - a partir do primeiro dia do quarto mês subsequente "
         "[...] em relação: a) ao disposto no art. 4º [...]; e b) aos arts. 7º e 9º; II - (VETADO); e III - a partir de 1º "
         "de janeiro de 2026, em relação aos demais dispositivos': its changes to the LRF (arts. 1 and 2) from 1.1.2026"),
        ("lei-das-sociedades-por-acoes", "lei-9249-1995", "1995-12-27", [(ALL, "1996-01-01")],
         "Lei 9.249/1995 art. 35: 'produzindo efeitos a partir de 1º de janeiro de 1996'"),
        ("lei-das-sociedades-por-acoes", "mp-517-2010", "2010-12-31",
         [("units:art-060", "2010-12-31"), (ALL, "2011-01-01")],
         "Medida Provisória 517/2010 art. 24: 'produzindo efeitos a partir de 1º de janeiro de 2011 em relação aos arts. 1º "
         "a 17': its art. 6 (arts. 55, 59 and 66) from 1.1.2011; its art. 21 (revocation of art. 60) on publication"),
        ("lei-das-sociedades-por-acoes", "mp-1040-2021", "2021-03-30",
         [(lines_match(r"^§ 3º É vedada, nas companhias abertas, a acumulação"), None)],
         "Medida Provisória 1.040/2021 art. 58: 'produz efeitos: I - trezentos e sessenta dias, contado da data de sua "
         "publicação, quanto à parte do art. 5º que altera o § 3º do art. 138 da Lei nº 6.404' (25.3.2022); the MP was "
         "converted into Lei 14.195/2021 on 27.8.2021, before that day, so its art. 138 § 3º never took effect"),
        ("lei-das-sociedades-por-acoes", "lei-14195-2021", "2021-08-27",
         [(lines_match(r"^§ 3º É vedada, nas companhias abertas, a acumulação"), "2022-08-22")],
         "Lei 14.195/2021 art. 58: 'produzirá efeitos: [...] II - em 360 (trezentos e sessenta) dias, contados da data de sua "
         "publicação, quanto à parte do art. 5º que altera o § 3º do art. 138 da Lei nº 6.404' (DOU 27.8.2021): art. 138 § "
         "3º from 22.8.2022"),
    ],
    "99-batch10.json": [
        ("lei-das-parcerias-publico-privadas", "lc-214-2025", "2025-01-16", [(ALL, "2027-01-01")],
         _LC214 + "; its change to the Lei das PPPs (art. 513) falls under III: from 1.1.2027 (future branch)"),
        ("lei-do-saneamento-basico", "lei-13329-2016", "2016-08-02", [(ALL, "2018-01-01")],
         "Lei 13.329/2016 art. 4: 'produzirá efeitos a partir do segundo exercício subsequente à sua vigência' (in force "
         "2.8.2016): from 1.1.2018"),
        ("lei-do-petroleo", "mp-1063-2021", "2021-08-12", [("units:art-68-b,art-68-c", None)],
         "Medida Provisória 1.063/2021 art. 6: 'produz efeitos: I - na data da sua publicação, quanto ao: a) art. 1º, na "
         "parte que acresce o art. 68-D [...]; e b) art. 3º; e II - no primeiro dia do quarto mês subsequente ao de sua "
         "publicação, quanto aos demais dispositivos' (1.12.2021): its arts. 68-B and 68-C were rewritten by Medida "
         "Provisória 1.069/2021 (13.9.2021, in force on publication) before that day, so its own wording of them never took "
         "effect; art. 68-D on publication"),
    ],
    "99-batch11.json": [
        ("lei-dos-crimes-contra-a-ordem-tributaria", "lei-8383-1991", "1991-12-31", [(ALL, "1992-01-01")],
         "Lei 8.383/1991 art. 98: 'produzirá efeitos a partir de 1º de janeiro de 1992'"),
        ("lei-dos-crimes-contra-a-ordem-tributaria", "lc-224-2025", "2025-12-26", [(ALL, "2026-01-01")],
         "Lei Complementar 224/2025 art. 15 III: 'a partir de 1º de janeiro de 2026, em relação aos demais dispositivos': its "
         "change to Lei 8.137 (art. 11) from 1.1.2026"),
    ],
    "99-batch14a.json": [
        ("lei-kandir", "lc-115-2002", "2002-12-27", [(ALL, "2003-01-01")],
         "Lei Complementar 115/2002 art. 4: 'produzindo efeitos a partir de 1º de janeiro de 2003'"),
        ("lei-kandir", "lc-120-2005", "2005-12-30", [(ALL, "2006-01-01")],
         "Lei Complementar 120/2005 art. 3: 'produzindo efeitos a partir do dia 1º de janeiro subseqüente' (DOU 30.12.2005)"),
        ("lei-kandir", "lc-190-2022", "2022-01-05", [(ALL, "2022-04-05")],
         "Lei Complementar 190/2022 art. 3: 'observado, quanto à produção de efeitos, o disposto na alínea \"c\" do inciso "
         "III do caput do art. 150 da Constituição Federal' (ninety days after publication, DOU 5.1.2022): from 5.4.2022"),
        ("lei-kandir", "lc-214-2025", "2025-01-16", [(ALL, "2026-01-01")],
         _LC214 + "; its change to the Lei Kandir (art. 501, art. 31-A) falls under VI: from 1.1.2026"),
        ("lei-do-iss", "lc-157-2016", "2016-12-30",
         [(lines_match(r"^(Art\. 8º-A|§ 1º O imposto não será objeto|§ 2º É nula a lei)"), "2017-12-31")],
         "Lei Complementar 157/2016 art. 7 § 1: 'O disposto no caput e nos §§ 1º e 2º do art. 8º-A da Lei Complementar nº "
         "116 [...] somente produzirão efeitos após o decurso do prazo referido no art. 6º' (one year from publication, DOU "
         "30.12.2016): art. 8º-A caput and §§ 1º-2º from 31.12.2017; § 3º and the other changes on publication"),
        ("lei-do-iss", "lc-214-2025", "2025-01-16", [(ALL, "2026-01-01")],
         _LC214 + "; its change to the Lei do ISS (art. 508, art. 8º-B) falls under VI: from 1.1.2026"),
    ],
    "99-batch14e.json": [
        ("estatuto-da-microempresa", "lc-147-2014", "2014-08-08", "LC147", None),
        ("estatuto-da-microempresa", "lc-155-2016", "2016-10-28",
         [("units:art-61-a,art-61-b,art-61-c,art-61-d", "2017-01-01"), (ALL, "2018-01-01")],
         "Lei Complementar 155/2016 art. 11: 'produzindo efeitos: I - na data de sua publicação, com relação ao art. 9º [not "
         "a change to this act]; II - a partir de 1º de janeiro de 2017, com relação aos arts. 61-A, 61-B, 61-C e 61-D da "
         "Lei Complementar nº 123 [...]; III - a partir de 1º de janeiro de 2018, quanto aos demais dispositivos'"),
        ("estatuto-da-microempresa", "lc-214-2025", "2025-01-16",
         [(lines_match(r"^VII - "), "2025-01-16"), (lc214_517, "2027-01-01"), (ALL, "2026-01-01")],
         _LC214 + "; its art. 516 (arts. 1º, 2º, 3º, 12, 17, 25-A, 25-B, 26, 38-A, 41) falls under VI, from 1.1.2026, and "
         "its art. 517 (wordings found word for word in it) under III, from 1.1.2027 (future branch); art. 541's revocation "
         "of art. 13 § 1º VII 'a partir de 1º de janeiro de 2025' (II, before the law's publication) stays on the in-force "
         "day"),
    ],
    "99-batch15a.json": [
        ("lei-de-custeio-da-seguridade-social", "lei-9876-1999", "1999-11-29",
         [("units:art-021", "2000-03-01"),
          (lines_match(r"^(III - vinte por cento sobre o total das remunerações|IV - quinze por cento sobre o valor bruto|"
                       r"§ 4º Na hipótese de o contribuinte individual prestar|§ 5º Aplica-se o disposto no § 4º ao cooperado|"
                       r"b\) recolher o produto arrecadado na forma da alínea anterior, a contribuição a que se refere o "
                       r"inciso IV)"), "2000-03-01")],
         "Lei 9.876/1999 art. 8: 'produzindo efeitos, quanto à majoração de contribuição e ao disposto no § 4º do art. 30 da "
         "Lei nº 8.212, de 1991, com a redação dada por esta Lei, a partir do dia primeiro do mês seguinte ao nonagésimo dia "
         "daquela publicação' (DOU 29.11.1999; 90th day 27.2.2000): from 1.3.2000 the contributions it raised or created "
         "(art. 21, the single 20% rate; art. 22 III, 20% on contribuintes individuais; art. 22 IV, 15% on cooperatives' "
         "invoices, with its collection in art. 30 I b) and art. 30 § 4º with § 5º, which extends it; its other changes "
         "(definitions, deadlines) on publication"),
        ("lei-de-custeio-da-seguridade-social", "lei-10256-2001", "2001-07-10", [("units:art-022-a", "2001-11-01")],
         "Lei 10.256/2001 art. 5: 'produzindo efeitos, quanto ao disposto no art. 22-A da Lei nº 8.212 [...] a partir do dia "
         "1º (primeiro) do mês seguinte ao 90º (nonagésimo) dia daquela publicação' (DOU 10.7.2001; 90th day 8.10.2001): art. "
         "22-A from 1.11.2001"),
        ("lei-de-custeio-da-seguridade-social", "lei-10684-2003", "2003-05-31", [("units:art-022-a", "2003-09-01")],
         "Lei 10.684/2003 art. 29: 'produzindo efeitos: [...] III - em relação aos arts. 18, 19, 20 e 22, a partir do mês "
         "subseqüente ao do termo final do prazo nonagesimal, a que refere o § 6º do art. 195 da Constituição Federal' (DOU "
         "31.5.2003; the 90 days end on 29.8.2003): its art. 19 (art. 22-A §§ 6º-7º) from 1.9.2003"),
        ("lei-de-custeio-da-seguridade-social", "mp-252-2005", "2005-06-16", [(ALL, "2005-10-01")],
         "Medida Provisória 252/2005 art. 73: 'produzindo efeitos: [...] III - a partir de 1º de outubro de 2005, em relação "
         "ao disposto nos arts. 33, 69 e 70' (DOU 16.6.2005): its art. 70 (art. 89 § 8º) from 1.10.2005, until the MP lapsed "
         "(14.10.2005)"),
        ("lei-de-custeio-da-seguridade-social", "mp-529-2011", "2011-04-08", [(ALL, "2011-05-01")],
         "Medida Provisória 529/2011 art. 2: 'produzindo efeitos a partir do dia 1º de maio de 2011' (DOU 8.4.2011)"),
        ("lei-de-custeio-da-seguridade-social", "mp-619-2013", "2013-06-07",
         [(lines_match(r"^(VI - a associação em cooperativa agropecuária; e|VII - a incidência do Imposto|"
                       r"c\) se tornar segurado obrigatório de outro regime previdenciário; e|d\) participar de sociedade|"
                       r"§ 14\. A participação)"), None)],
         "Medida Provisória 619/2013 art. 16: 'produzindo efeitos no primeiro dia do sétimo mês após sua publicação, em "
         "relação: I - ao inciso VII do § 9º do art. 12, à alínea \"d\" do inciso I do § 11 do art. 12, e ao § 14 do art. 12 da "
         "Lei nº 8.212' (DOU 7.6.2013: 1.1.2014); the MP was converted into Lei 12.873/2013 (25.10.2013) before that day, so "
         "its wording of those dispositivos (with the '; e' it added to the item before each new item) never took effect"),
        ("lei-de-custeio-da-seguridade-social", "lei-12873-2013", "2013-10-25",
         [(lines_match(r"^(VI - a associação em cooperativa agropecuária; e|VII - a incidência do Imposto|"
                       r"c\) tornar-se segurado obrigatório|d\) participar de sociedade|§ 14\. A participação|"
                       r"§ 15\. \(VETADO\))"), "2014-01-01")],
         "Lei 12.873/2013 art. 63 III: 'na data de sua publicação quanto aos demais dispositivos, produzindo efeitos a partir "
         "de 1º de janeiro de 2014, em relação: a) ao inciso VII do § 9º do art. 12, à alínea d do inciso I do § 11 do art. "
         "12, e aos §§ 14 e 15 do art. 12 da Lei nº 8.212' (DOU 25.10.2013): those dispositivos (with the item before each new "
         "item, which takes its '; e') from 1.1.2014"),
        ("lei-de-custeio-da-seguridade-social", "lei-13606-2018", "2018-01-10",
         [(lines_match(r"^§ 13\. O produtor rural pessoa física poderá optar"), "2019-01-01")],
         "Lei 13.606/2018 art. 40: 'produzirá efeitos: I - a partir de 1º de janeiro de 2018, quanto ao disposto nos arts. 14 "
         "e 15, exceto o § 13 do art. 25 da Lei nº 8.212 [...] que produzirão efeitos a partir de 1º de janeiro de 2019' (DOU "
         "10.1.2018; the 1.1.2018 effects are retroactive and keep the in-force day): art. 25 § 13 from 1.1.2019"),
    ],
    "99-batch15b.json": [
        ("lei-de-beneficios-da-previdencia-social", "lei-10684-2003", "2003-05-31", [("units:art-126", "2003-09-01")],
         "Lei 10.684/2003 art. 29: 'produzindo efeitos: [...] III - em relação aos arts. 18, 19, 20 e 22, a partir do mês "
         "subseqüente ao do termo final do prazo nonagesimal, a que refere o § 6º do art. 195 da Constituição Federal' (DOU "
         "31.5.2003; the 90 days end on 29.8.2003): its art. 20 (art. 126 § 1º) from 1.9.2003"),
        ("lei-de-beneficios-da-previdencia-social", "lei-10710-2003", "2003-08-06", [(ALL, "2003-09-01")],
         "Lei 10.710/2003 art. 2: 'produzindo efeitos em relação aos benefícios requeridos a partir do primeiro dia do mês "
         "seguinte ao de sua publicação' (DOU 6.8.2003): its changes (arts. 71, 71-A, 72, 73) from 1.9.2003"),
        ("lei-de-beneficios-da-previdencia-social", "mp-619-2013", "2013-06-07",
         [(lines_match(r"^(VI - a associação em cooperativa agropecuária; e|VII - a incidência do Imposto|"
                       r"c\) se tornar segurado obrigatório de outro regime previdenciário; e|d\) participar de sociedade|"
                       r"§ 12\. A participação)"), None)],
         "Medida Provisória 619/2013 art. 16: 'produzindo efeitos no primeiro dia do sétimo mês após sua publicação, em "
         "relação: [...] II - ao inciso VII do § 8º do art. 11, à alínea \"d\" do inciso I do § 10 art. 11, e ao parágrafo § 12 "
         "do art. 11 da Lei nº 8.213, de 1991; e III - ao art. 17 desta Medida Provisória' (DOU 7.6.2013: 1.1.2014); the MP "
         "was converted into Lei 12.873/2013 (25.10.2013) before that day, so its wording of those dispositivos (with the "
         "'; e' it added to the item before each new item) never took effect"),
        ("lei-de-beneficios-da-previdencia-social", "lei-12873-2013", "2013-10-25",
         [(lines_match(r"^(VI - a associação em cooperativa agropecuária; e|VII - a incidência do Imposto|"
                       r"c\) tornar-se segurado obrigatório|d\) participar de sociedade|§ 12\. A participação|"
                       r"§ 13\. \(VETADO\)|§ 6º Simultaneamente com a inscrição)"), "2014-01-01")],
         "Lei 12.873/2013 art. 63 III: 'produzindo efeitos a partir de 1º de janeiro de 2014, em relação: [...] b) ao inciso "
         "VII do § 8º do art. 11, à alínea d do inciso I do § 10 do art. 11, aos §§ 12 e 13 do art. 11 da Lei nº 8.213 [...]; e "
         "c) ao art. 64 desta Lei' (its art. 64 revokes art. 17 § 6º; DOU 25.10.2013): those dispositivos (with the item "
         "before each new item, which takes its '; e') and the revocation from 1.1.2014"),
    ],
    "99-batch16c.json": [
        ("lei-4320-de-1964", "dl-1939-1982", "1982-07-05", [(ALL, "1983-01-01")],
         "Decreto-Lei 1.939/1982 art. 2: 'As disposições deste Decreto-lei serão aplicadas aos Orçamentos e Balanços a partir "
         "do exercício, de 1983, inclusive' (DOU 21.5.1982; no vigência clause, in force 5.7.1982 under LINDB art. 1): its new "
         "classification of revenue in art. 11 applies from the 1983 financial year, 1.1.1983"),
    ],
    "99-batch16f.json": [
        ("lei-do-seguro-desemprego", "lc-155-2016", "2016-10-28", [(ALL, "2018-01-01")],
         "Lei Complementar 155/2016 art. 11: 'produzindo efeitos: I - na data de sua publicação, com relação ao art. 9º; II "
         "- a partir de 1º de janeiro de 2017, com relação aos arts. 61-A, 61-B, 61-C e 61-D da Lei Complementar nº 123 [...]; "
         "III - a partir de 1º de janeiro de 2018, quanto aos demais dispositivos': its art. 8 (Lei 7.998 art. 3 § 4º) falls "
         "under III, from 1.1.2018"),
    ],
    "99-batch17g.json": [
        ("lei-do-mercado-de-capitais", "lei-14754-2023", "2023-12-13", [(ALL, "2024-01-01")],
         "Lei 14.754/2023 art. 47: 'Esta Lei entra em vigor na data de sua publicação e produzirá efeitos: I - "
         "imediatamente, quanto aos arts. 28 e 29, aos §§ 4º, 5º e 6º do art. 30 e aos arts. 42 e 43; e II - a partir de 1º "
         "de janeiro de 2024, quanto aos demais dispositivos': its art. 46 I (revocation of Lei 4.728 arts. 49 and 50) falls "
         "under II, from 1.1.2024"),
    ],
    "99-batch17h.json": [
        ("lei-da-csll", "mp-413-2008", "2008-01-03", [(ALL, "2008-05-01")],
         "Medida Provisória 413/2008 art. 18: 'produzindo efeitos em relação: [...] II - aos arts. 3º, 13 e 17, a partir do "
         "primeiro dia do quarto mês subseqüente ao de publicação desta Medida Provisória' (DOU 3.1.2008): its art. 17 (Lei "
         "7.689 art. 3) from 1.5.2008"),
        ("lei-da-csll", "mp-1115-2022", "2022-04-28", [(ALL, "2022-08-01")],
         "Medida Provisória 1.115/2022: 'Esta Medida Provisória entra em vigor na data de sua publicação e produz efeitos a "
         "partir do primeiro dia do quarto mês subsequente ao de sua publicação' (DOU 28.4.2022): from 1.8.2022"),
        ("lei-da-csll", "mp-1303-2025", "2025-06-11", [(ALL, "2025-10-01")],
         "Medida Provisória 1.303/2025: 'produz efeitos: [...] II - no primeiro dia do quarto mês subsequente ao de sua "
         "publicação, quanto aos art. 61 e art. 62' (DOU 11.6.2025): its art. 62 (Lei 7.689 art. 3) from 1.10.2025, until the "
         "MP lapsed (8.10.2025)"),
        ("lei-da-csll", "lc-224-2025", "2025-12-26", [(ALL, "2026-04-01")],
         "Lei Complementar 224/2025: 'produzirá efeitos: I - a partir do primeiro dia do quarto mês subsequente ao de sua "
         "publicação, em relação: [...] b) aos arts. 7º e 9º' (DOU 26.12.2025): its art. 7 (Lei 7.689 art. 3) from 1.4.2026"),
        ("lei-da-csll", "lei-15525-2026", "2026-09-29", [(ALL, "2027-01-01")],
         "Lei 15.525/2026: 'produzindo efeitos: I - quanto aos arts. 2º e 5º, a partir de 1º de janeiro de 2027' : its art. 2 "
         "(Lei 7.689 art. 3) from 1.1.2027"),
        ("lei-9249-de-1995", "lei-10684-2003", "2003-05-31", [(ALL, "2003-09-01")],
         "Lei 10.684/2003: 'produzindo efeitos: [...] III - em relação aos arts. 18, 19, 20 e 22, a partir do mês subseqüente "
         "ao do termo final do prazo nonagesimal, a que refere o § 6º do art. 195 da Constituição Federal' (DOU 31.5.2003; the "
         "90 days end in August 2003): its art. 22 (Lei 9.249 art. 20) from 1.9.2003"),
        ("lei-9249-de-1995", "lei-11196-2005", "2005-11-22", [(ALL, "2006-01-01")],
         "Lei 11.196/2005 art. 132: 'produzindo efeitos: [...] IV - a partir de 1º de janeiro de 2006, em relação ao disposto: "
         "[...] b) nos arts. 17 a 27, 31 e 32, 34 [...] desta Lei': its art. 34 (Lei 9.249 arts. 15 and 20) from 1.1.2006"),
        ("lei-9249-de-1995", "lei-11727-2008", "2008-06-24", [(ALL, "2009-01-01")],
         "Lei 11.727/2008 art. 41: 'produzindo efeitos em relação: [...] VI - aos arts. 22, 23, 29 e 31, a partir do primeiro "
         "dia do ano seguinte ao da publicação desta Lei': its art. 29 (Lei 9.249 art. 15) from 1.1.2009"),
        ("lei-9249-de-1995", "lei-14789-2023", "2023-12-29", [(ALL, "2024-01-01")],
         "Lei 14.789/2023: 'Esta Lei entra em vigor na data de sua publicação e produzirá efeitos a partir de 1º de janeiro de "
         "2024': its art. 18 (Lei 9.249 art. 9) from 1.1.2024"),
        ("lei-9249-de-1995", "lei-15270-2025", "2025-11-27", [(ALL, "2026-01-01")],
         "Lei 15.270/2025: 'Esta Lei entra em vigor na data de sua publicação e produzirá efeitos a partir de 1º de janeiro de "
         "2026': its art. 3 (Lei 9.249 arts. 10 and 10-A) from 1.1.2026"),
        ("lei-9249-de-1995", "lc-224-2025", "2025-12-26", [(ALL, "2026-01-01")],
         "Lei Complementar 224/2025: 'produzirá efeitos: [...] III - a partir de 1º de janeiro de 2026, em relação aos demais "
         "dispositivos': its art. 8 (Lei 9.249 art. 9 § 2º) from 1.1.2026"),
        ("lei-9249-de-1995", "lei-15525-2026", "2026-09-29", [(ALL, "2030-01-01")],
         "Lei 15.525/2026: 'produzindo efeitos: [...] II - quanto aos arts. 3º e 4º, a partir de 1º de janeiro de 2030': its "
         "art. 3 (Lei 9.249 art. 3 § 5º) from 1.1.2030"),
    ],
    "99-batch17a.json": [
        ("lei-do-vale-transporte", "lei-9532-1997", "1997-12-11", [(ALL, "1998-01-01")],
         "Lei 9.532/1997 art. 82: 'Ficam revogados: [...] II - a partir de 1º de janeiro de 1998: [...] f) o art. 3º da Lei "
         "nº 7.418, de 16 de dezembro de 1985' (with its parágrafo único): from 1.1.1998"),
    ],
    "99-batch17i.json": [
        ("lei-9250-de-1995", "lei-9532-1997", "1997-12-11", [(ALL, "1998-01-01")],
         "Lei 9.532/1997 art. 81: 'produzindo efeitos: I - nessa data, em relação aos arts. 9º, 37 a 42, 44 a 54, 64 a 68, 74 "
         "e 75; II - a partir de 1º de janeiro de 1998, em relação aos demais dispositivos': its art. 25 (Lei 9.250 art. 7 § "
         "2º) from 1.1.1998"),
        ("lei-9250-de-1995", "mp-528-2011", "2011-03-28", [(ALL, "2011-04-01")],
         "Medida Provisória 528/2011 art. 4: 'produzindo efeitos em relação aos arts. 1º a 3º: I - a partir de 1º de janeiro "
         "de 2011, para fins do disposto no parágrafo único do art. 1º da Lei nº 11.482 [...]; II - a partir de 1º de abril de "
         "2011, para os demais casos' (DOU 28.3.2011): its art. 3 (Lei 9.250 arts. 4, 8 and 10) falls under II, from 1.4.2011"),
        ("lei-9250-de-1995", "lei-13043-2014", "2014-11-14", [(ALL, "2015-01-01")],
         "Lei 13.043/2014 art. 113: 'Esta Lei entra em vigor na data de sua publicação, exceto: [...] II - os arts. 1º a 15, "
         "30 a 32, 97, 106 e os artigos da Seção XXI do Capítulo I, que entram em vigor a partir de 1º de janeiro de 2015' (DOU "
         "14.11.2014): its art. 84 (Seção XXI; Lei 9.250 art. 4 VII and art. 8 II i) from 1.1.2015"),
        ("lei-9250-de-1995", "lei-14754-2023", "2023-12-13", [(ALL, "2024-01-01")],
         "Lei 14.754/2023 art. 47: 'produzirá efeitos: I - imediatamente, quanto aos arts. 28 e 29, aos §§ 4º, 5º e 6º do art. "
         "30 e aos arts. 42 e 43; e II - a partir de 1º de janeiro de 2024, quanto aos demais dispositivos': its art. 46 II "
         "(revocation of Lei 9.250 art. 25 § 4º) from 1.1.2024"),
        ("lei-9250-de-1995", "lei-15270-2025", "2025-11-27", [(ALL, "2026-01-01")],
         "Lei 15.270/2025: 'Esta Lei entra em vigor na data de sua publicação e produzirá efeitos a partir de 1º de janeiro de "
         "2026' (DOU 27.11.2025): its arts. 2 and 7 (Lei 9.250 arts. 3º-A, 6º-A, 10, 11, 11-A, 12, 13, 16-A, 16-B and the "
         "new chapter headings) from 1.1.2026"),
    ],
    "99-batch17j.json": [
        ("lei-7713-de-1988", "mp-68-1989", "1989-06-22", [(ALL, "1989-07-01")],
         "Medida Provisória 68/1989 art. 45: 'A partir de 1º de julho de 1989, os dispositivos a seguir enumerados da Lei nº "
         "7.713 [...] passam a vigorar com a seguinte redação' (DOU 22.6.1989): arts. 6, 14, 17, 24, 25, 28, 35, 45 and 53 from "
         "1.7.1989"),
        ("lei-7713-de-1988", "mp-114-1989", "1989-11-29",
         [(lambda h: path_sel([("art-06", "caput", "XV -", None)], None)(h), "1990-01-01"),
          ("units:art-25", "1990-01-01"), ("units:art-14,art-45", None)],
         "Medida Provisória 114/1989 art. 9: 'as alterações procedidas nos art. 6º, XV, 14, II, 25, 45 e § 1º, da Lei nº 7.713 "
         "[...] produzirão efeitos a partir de 1º de janeiro de 1990' (DOU 29.11.1989): art. 6 XV and art. 25 from 1.1.1990; "
         "its art. 14 II and art. 45 wordings never took effect, its conversion law (Lei 7.959/1989, in force 22.12.1989, "
         "same clause in its art. 8) having replaced them before that day"),
        ("lei-7713-de-1988", "lei-7959-1989", "1989-12-22", [("units:art-14,art-45", "1990-01-01")],
         "Lei 7.959/1989 art. 8: 'as alterações procedidas nos arts. 6º, XV, 14, II, 25, 45 e § 1º, da Lei nº 7.713, de 1988 "
         "[...] produzirão efeitos a partir de 1º de janeiro de 1990' (DOU 22.12.1989): art. 14 II and art. 45 from 1.1.1990"),
        ("lei-7713-de-1988", "lei-8383-1991", "1991-12-31", [(ALL, "1992-01-01")],
         "Lei 8.383/1991: 'Esta lei entra em vigor na data de sua publicação e produzirá efeitos a partir de 1º de janeiro de "
         "1992' (DOU 31.12.1991): from 1.1.1992"),
        ("lei-7713-de-1988", "lei-8541-1992", "1992-12-24", [(ALL, "1993-01-01")],
         "Lei 8.541/1992: 'Esta lei entra em vigor na data de sua publicação e produzirá efeitos a partir de 1º de janeiro de "
         "1993' (DOU 24.12.1992): from 1.1.1993"),
        ("lei-7713-de-1988", "mp-451-2008", "2008-12-16", [(ALL, "2009-01-01")],
         "Medida Provisória 451/2008: 'produzindo efeitos: I - a partir de 1º de janeiro de 2009, em relação ao disposto: a) "
         "nos arts. 3º a 5º [...]' (DOU 16.12.2008): its art. 5 (Lei 7.713 art. 6) from 1.1.2009"),
        ("lei-7713-de-1988", "mp-528-2011", "2011-03-28", [(ALL, "2011-04-01")],
         "Medida Provisória 528/2011 art. 4: 'produzindo efeitos em relação aos arts. 1º a 3º: I - a partir de 1º de janeiro "
         "de 2011, para fins do disposto no parágrafo único do art. 1º da Lei nº 11.482 [...]; II - a partir de 1º de abril de "
         "2011, para os demais casos' (DOU 28.3.2011): its art. 2 (Lei 7.713 art. 6) falls under II, from 1.4.2011"),
    ],
    "99-batch17k.json": [
        ("lei-9430-de-1996", "mp-2013-1999", "1999-12-30", [(ALL, "2000-01-01")],
         "Medida Provisória 2.013-4/1999: 'Esta Medida Provisória entra em vigor na data de sua publicação, produzindo efeitos "
         "a partir de 1º de janeiro de 2000' (DOU 30.12.1999): its change to Lei 9.430 art. 18 from 1.1.2000"),
        ("lei-9430-de-1996", "mp-66-2002", "2002-08-30", [("units:art-74", "2002-10-01")],
         "Medida Provisória 66/2002 art. 63: 'produzindo efeitos: I - a partir de 1º de outubro de 2002, em relação aos arts. "
         "31 e 49; [...] IV - a partir da data da publicação desta Medida Provisória, em relação aos demais artigos' (DOU "
         "30.8.2002): its art. 49 (Lei 9.430 art. 74) from 1.10.2002; arts. 58 and 60 (arts. 42 and 81) on publication"),
        ("lei-9430-de-1996", "mp-478-2009", "2009-12-29", [(ALL, "2010-01-01")],
         "Medida Provisória 478/2009: 'Esta Medida Provisória entra em vigor na data de sua publicação, produzindo efeitos a "
         "partir de 1º de janeiro de 2010 em relação ao disposto nos arts. 9º e 10' (DOU 29.12.2009): its arts. 9 and 10 (Lei "
         "9.430 arts. 18, 19-A and 19-B) from 1.1.2010, until it lapsed (1.6.2010)"),
        ("lei-9430-de-1996", "mp-517-2010", "2010-12-31", [(ALL, "2011-01-01")],
         "Medida Provisória 517/2010: 'produzindo efeitos a partir de 1º de janeiro de 2011 em relação aos arts. 1º a 17' (DOU "
         "31.12.2010, edição extra): its art. 8 (Lei 9.430 art. 12) from 1.1.2011"),
        ("lei-9430-de-1996", "lei-15265-2025", "2025-11-21", [("units:art-17", "2026-01-01")],
         "Lei 15.265/2025: 'produz efeitos a partir de: I - 1º de janeiro de 2026, quanto aos arts. 18 a 30 e aos arts. 33 e 34; "
         "II - na data de sua publicação, quanto aos demais dispositivos' (DOU 21.11.2025, edição extra): its art. 33 (Lei "
         "9.430 art. 17) from 1.1.2026; its art. 32 (art. 74) on publication"),
        ("lei-9430-de-1996", "lei-15525-2026", "2026-09-29", [(ALL, "2030-01-01")],
         "Lei 15.525/2026: 'produzindo efeitos: [...] II - quanto aos arts. 3º e 4º, a partir de 1º de janeiro de 2030' (DOU "
         "29.9.2026): its art. 4 (Lei 9.430 art. 2 § 5º) from 1.1.2030"),
    ],
}
# LC 147/2014 art. 17: 'exceto no que se refere: I - ao § 14 do art. 3º, ao inciso VI do art. 17, ao caput e aos §§ 2º,
# 5º-D, 5º-F, 5º-I, 7º, 13, 14, 16, 17, 18, 18-A e 24 do art. 18, ao inciso I do § 4º do art. 18-A, ao caput do art. 19,
# ao § 3º do art. 20, aos incisos I, II e V do § 4º do art. 21 [...] ao art. 3º e aos incisos III a V do art. 16 desta
# Lei Complementar, que produzirão efeitos a partir de 1º de janeiro do primeiro ano subsequente [...]; II - ao § 15 do
# art. 3º, aos §§ 12 a 14 do art. 26, ao art. 38-B, à alínea a do inciso XIII do § 1º e aos §§ 7º e 8º do art. 13 e ao
# art. 21-A [...] e ao inciso I do art. 16 desta Lei Complementar, que produzirão efeitos a partir de 1º de janeiro do
# segundo ano subsequente' (DOU 8.8.2014). Art. 16 III-V revoke art. 17 XI and XIII, art. 18 §§ 5º-A, 5º-G and § 14 I-II,
# art. 49 I; art. 16 I revokes art. 4 § 1º II. Selectors are by dispositivo path (unit, paragraph, inciso, alínea).
LC147_2015 = [("art-03", "§ 14", None, None), ("art-17", "caput", "VI -", None), ("art-17", "caput", "XI -", None),
              ("art-17", "caput", "XIII -", None), ("art-18", "caput", None, None),
              *[("art-18", p, None, None) for p in ("§ 2º", "§ 5º-D", "§ 5º-F", "§ 5º-I", "§ 7º", "§ 13", "§ 14", "§ 16",
                                                     "§ 17", "§ 18", "§ 18-A", "§ 24", "§ 5º-A", "§ 5º-G")],
              ("art-18-a", "§ 4º", "I -", None), ("art-19", "caput", None, None), ("art-20", "§ 3º", None, None),
              ("art-21", "§ 4º", "I -", None), ("art-21", "§ 4º", "II -", None), ("art-21", "§ 4º", "V -", None),
              ("art-49", "caput", "I -", None)]
LC147_2016 = [("art-03", "§ 15", None, None), ("art-26", "§ 12", None, None), ("art-26", "§ 13", None, None),
              ("art-26", "§ 14", None, None), ("art-38-b", "*", None, None), ("art-13", "§ 1º", "XIII -", "a)"),
              ("art-13", "§ 7º", None, None), ("art-13", "§ 8º", None, None), ("art-21-a", "*", None, None),
              ("art-04", "§ 1º", "II -", None)]
LC147_WHY = ("Lei Complementar 147/2014 art. 17: 'entra em vigor na data de sua publicação, exceto no que se refere: I - ao § 14 "
             "do art. 3º, ao inciso VI do art. 17, ao caput e aos §§ 2º, 5º-D, 5º-F, 5º-I, 7º, 13, 14, 16, 17, 18, 18-A e 24 do "
             "art. 18, ao inciso I do § 4º do art. 18-A, ao caput do art. 19, ao § 3º do art. 20, aos incisos I, II e V do § 4º "
             "do art. 21 [...] e aos incisos III a V do art. 16 desta Lei Complementar [the revocations of art. 17 XI and XIII, "
             "art. 18 §§ 5º-A, 5º-G and 14 I-II, art. 49 I], que produzirão efeitos a partir de 1º de janeiro do primeiro ano "
             "subsequente ao da publicação [...]; II - ao § 15 do art. 3º, aos §§ 12 a 14 do art. 26, ao art. 38-B, à alínea a do "
             "inciso XIII do § 1º e aos §§ 7º e 8º do art. 13 e ao art. 21-A [...] e ao inciso I do art. 16 [revocation of art. 4 "
             "§ 1º II], que produzirão efeitos a partir de 1º de janeiro do segundo ano subsequente' (DOU 8.8.2014): those "
             "dispositivos from 1.1.2015 and 1.1.2016, the rest on publication")
_LV = re.compile(r"^(?:(Art\.\s*\d+[º°]?(?:-[A-Z])?)|(§\s*\d+[º°]?(?:-[A-Z])?|Parágrafo único)|([IVXLC]+(?:-[A-Z])?\s*-)|([a-z]\)))")


def paths(lines: list[str]) -> list[tuple]:
    out, par, inc, ali = [], "caput", None, None
    for x in lines:
        m = _LV.match(x)
        if m and m.group(1):
            par, inc, ali = "caput", None, None
        elif m and m.group(2):
            par, inc, ali = re.sub(r"\s+", " ", m.group(2)).replace("°", "º"), None, None
        elif m and m.group(3):
            inc, ali = re.sub(r"\s+", " ", m.group(3)).strip(), None
            inc = re.sub(r"\s*-$", " -", inc)
        elif m and m.group(4):
            ali = m.group(4)
        out.append((par, inc, ali, bool(m and m.group(1))))
    return out


def path_sel(targets, unit_of_hunk):
    def f(h):
        for u, par, inc, ali in targets:
            if u != h["unit"]:
                continue
            if par == "*":
                return True
            for p in h["paths"]:
                if p[0] != par:
                    continue
                if par == "caput" and inc is None and not p[3]:
                    continue        # 'caput' alone: the caput sentence, not its incisos
                if inc is not None and p[1] != inc:
                    continue
                if ali is not None and p[2] != ali:
                    continue
                return True
        return False
    return f


def _lab(x: str) -> str | None:
    m = _LV.match(x)
    return re.sub(r"\s+", " ", m.group(0)).strip() if m else None


def hunks(old: str | None, new: str | None, unit: str) -> tuple[list[dict], list[dict]]:
    """the unit's line operations, in order: 'eq' lines and one-line hunks (a replaced line paired with the new line of
    the same label, else a deleted or an inserted line); each hunk carries the dispositivo paths of its lines"""
    a = (old or "").splitlines()
    b = (new or "").splitlines()
    pa, pb = paths(a), paths(b)
    ops, hs = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            ops.extend({"eq": x} for x in a[i1:i2])
            continue
        olds = list(range(i1, i2))
        pair = {}
        for j in range(j1, j2):
            lab = _lab(b[j])
            hit = next((i for i in olds if i not in pair.values() and lab and _lab(a[i]) == lab), None)
            if hit is not None:
                pair[j] = hit
        subs = []
        for i in olds:
            if i not in pair.values():
                subs.append({"old": [a[i]], "new": [], "unit": unit, "paths": [pa[i]], "oi": i, "nj": None})
        for j in range(j1, j2):
            i = pair.get(j)
            subs.append({"old": [a[i]] if i is not None else [], "new": [b[j]], "unit": unit,
                         "paths": ([pa[i]] if i is not None else []) + [pb[j]], "oi": i, "nj": j})
        hs.extend(subs)
        ops.append({"block": subs, "a": a[i1:i2], "b": b[j1:j2]})
    return ops, hs


def rebuild(ops: list[dict], applied) -> str | None:
    """the old text with the applied hunks: a block wholly applied gives its new lines, wholly unapplied its old lines;
    a mixed block follows the new order, with unapplied deleted lines put back before the first line that followed
    them in the old text"""
    res = []
    for h in ops:
        if "eq" in h:
            res.append(h["eq"])
            continue
        subs = h["block"]
        st = [bool(applied(s)) for s in subs]
        if all(st):
            res += h["b"]
        elif not any(st):
            res += h["a"]
        else:
            items = []      # (old index or None, line)
            for s, ok in zip(sorted(subs, key=lambda s: (s["nj"] is None, s["nj"] or 0)), [None] * len(subs)):
                if s["nj"] is None:
                    continue
                if applied(s):
                    items.append((s["oi"], s["new"][0]))
                elif s["oi"] is not None:
                    items.append((s["oi"], s["old"][0]))
            for s in subs:
                if s["nj"] is None and not applied(s):
                    pos = next((k for k, (oi, _) in enumerate(items) if oi is not None and oi > s["oi"]), len(items))
                    items.insert(pos, (s["oi"], s["old"][0]))
            res += [x for _, x in items]
    return ("\n".join(res) + "\n") if res else None


def full(versions):
    st, out = {}, []
    for v in versions:
        if "units" in v:
            st = copy.deepcopy(v["units"])
        for k, u in (v.get("changes") or {}).items():
            if u is None:
                st.pop(k, None)
            else:
                st[k] = copy.deepcopy(u)
        w = {k: x for k, x in v.items() if k not in ("units", "changes")}
        w["units"] = copy.deepcopy(st)
        out.append(w)
    return out


def deltas(versions):
    out, prev = [], None
    for v in versions:
        units = v.pop("units")
        if prev is None:
            v["units"] = units
        else:
            v["changes"] = {u: units.get(u) for u in sorted(set(units) | set(prev)) if units.get(u) != prev.get(u)}
        out.append(v)
        prev = units
    return out


def key_order(v):
    return [k for k in ("from", "same_day", "credits", "note", "source_url", "sha256") if k in v]


def apply_move(act: dict, law: str, day: str, rules, moved: list[str]) -> None:
    vs = full(act["versions"])
    idx = [i for i, v in enumerate(vs) if v["from"] == day and any(law in c for c in v.get("credits", {}).values())]
    assert len(idx) == 1, (act["slug"], law, day, idx)
    k = idx[0]
    v, prev = vs[k], vs[k - 1]["units"] if k else {}
    units = [u for u, c in v["credits"].items() if law in c]
    for u in units:
        old = prev.get(u, {}).get("text") if u in prev else None
        new = v["units"].get(u, {}).get("text") if u in v["units"] else None
        ops, hs = hunks(old, new, u)
        if not hs:
            continue
        for h in hs:
            h["day"] = day
            for sel, eff in rules:
                if isinstance(sel, str) and sel.startswith("units:"):
                    hit = u in sel[6:].split(",")
                elif sel == "not-adct":
                    hit = not u.startswith("adct-")
                else:
                    hit = sel(h)
                if hit:
                    h["day"] = eff
                    break
        effs = sorted({h["day"] for h in hs if h["day"] and h["day"] != day})
        drops = [h for h in hs if h["day"] is None]
        if not effs and not drops:
            continue
        # context for re-inserting a deleted line: the old-side line before it
        last = None
        for h in ops:
            if "eq" in h:
                last = h["eq"]
            else:
                for s in sorted(h["block"], key=lambda s: (s["oi"] is None, s["oi"] or 0)):
                    s["prev"] = last
                    if s["old"]:
                        last = s["old"][0]
        # the unit's next change after this version (a dropped hunk is undone only up to it)
        nxt = next((j for j in range(k + 1, len(vs)) if vs[j]["units"].get(u) != v["units"].get(u)), None)
        drop_until = vs[nxt]["from"] if nxt is not None else "9999"
        base_unit = copy.deepcopy(v["units"].get(u) or prev.get(u))
        # insert versions for effect days with none
        for e in effs:
            if not any(w["from"] == e for w in vs):
                pos = next((j for j, w in enumerate(vs) if w["from"] > e), len(vs))
                src = vs[pos - 1]
                nv = {"from": e, "credits": {}, "source_url": v.get("source_url"), "sha256": v.get("sha256"),
                      "units": copy.deepcopy(src["units"])}
                nv = {kk: nv[kk] for kk in ("from", "credits", "source_url", "sha256", "units") if nv.get(kk) is not None
                      or kk == "units"}
                vs.insert(pos, nv)
        k = next(i for i, w in enumerate(vs) if w is v)
        last_eff = max(effs) if effs else day
        for j in range(k, len(vs)):
            w = vs[j]
            pending = [h for h in hs if (h["day"] is not None and h["day"] != day and h["day"] > w["from"])
                       or (h["day"] is None and w["from"] < drop_until)]
            if not pending:
                if w["from"] >= last_eff and w["from"] >= min(drop_until, "9999"):
                    break
                continue
            cur = (w["units"].get(u) or {}).get("text")
            if cur == new:
                # the unit as the law left it: rebuilt exactly from the line operations
                pend = {id(h) for h in pending}
                t = rebuild(ops, lambda h: id(h) not in pend)
                lines = (t or "").splitlines()
                pending = []
            else:
                lines = (cur or "").splitlines()
            for h in pending:
                if h["new"] and h["old"]:
                    if h["new"][0] in lines:
                        lines[lines.index(h["new"][0])] = h["old"][0]
                    else:
                        WARN.append(f"{act['slug']} {u} {w['from']}: replaced line gone, kept: {h['new'][0][:50]}")
                elif h["new"]:
                    if h["new"][0] in lines:
                        lines.remove(h["new"][0])
                    else:
                        WARN.append(f"{act['slug']} {u} {w['from']}: inserted line gone: {h['new'][0][:50]}")
                else:
                    pos = (lines.index(h["prev"]) + 1) if h["prev"] in lines else (0 if h["prev"] is None else None)
                    if pos is None:
                        WARN.append(f"{act['slug']} {u} {w['from']}: no place to restore: {h['old'][0][:50]}")
                        pos = len(lines)
                    lines.insert(pos, h["old"][0])
            if lines:
                nu = copy.deepcopy(w["units"].get(u) or base_unit)
                nu["text"] = "\n".join(lines) + "\n"
                w["units"][u] = nu
            else:
                w["units"].pop(u, None)

        def text_on(t):
            return (next(w for w in vs if w["from"] == t)["units"].get(u) or {}).get("text")
        # credits: the version day keeps the law only if something of it applies then
        if text_on(day) == old:
            v["credits"][u] = [x for x in v["credits"][u] if x != law]
            if not v["credits"][u]:
                del v["credits"][u]
        for e in effs:
            w = next(w for w in vs if w["from"] == e and not w.get("same_day"))
            w["credits"].setdefault(u, [])
            if law not in w["credits"][u]:
                w["credits"][u].append(law)
        moved.append(f"{act['slug']} {u}: {law} " + ", ".join(
            f"{'never (superseded)' if h['day'] is None else h['day']} [{(h['new'] or h['old'] or [''])[0][:40]}]"
            for h in hs if h["day"] != day))
    # drop versions left without any change or credit (never the first)
    out = [vs[0]]
    for w in vs[1:]:
        if w["units"] == out[-1]["units"] and not w.get("credits") and not w.get("note"):
            continue
        out.append(w)
    act["versions"] = deltas([{kk: w[kk] for kk in key_order(w) + ["units"]} for w in out])


def run(path: str, out: str | None) -> list[str]:
    name = Path(path).name
    raw = Path(path).read_text(encoding="utf-8")
    d = json.loads(raw)
    done = any(x.startswith(MARK) for x in d["decisions"])
    moved: list[str] = []
    for act_slug, law, day, rules, why in ([] if done else MOVES.get(name, [])):
        act = next(a for a in d["acts"] if a["slug"] == act_slug)
        if rules == "LC147":
            rules = [(path_sel(LC147_2015, None), "2015-01-01"), (path_sel(LC147_2016, None), "2016-01-01")]
            why = LC147_WHY
        before = len(moved)
        apply_move(act, law, day, rules, moved)
        if len(moved) > before:
            moved[before] = why + ". Moved: " + moved[before]
    d["decisions"] = [re.sub(r"their versions are dated by the in-force day \(the day the wording became the law's "
                             r"text\), as for the Constitution",
                             "a change is dated by the day it takes effect where the clause fixes a later day for it (the "
                             "effect-days decision lists the units moved); effects that are retroactive, financial only or "
                             "left to a later act or condition keep the in-force day", x) for x in d["decisions"]]
    d["decisions"] = [x.replace("as for other deferred effects, the wording is dated by the in-force day",
                                "an effect day left to a later act is not a fixed day, so the wording is dated by the "
                                "in-force day") for x in d["decisions"]]
    d["decisions"] = [x.replace("as for other deferred effects, its wording is dated by the in-force day",
                                "its changes are dated by their effect day (see the effect-days decision)")
                      for x in d["decisions"]]
    new_dec = d["decisions"]
    if not moved and json.loads(raw)["decisions"] == new_dec:
        return []
    if moved:
        d["decisions"].append(
            MARK + " where an act fixes a later day from which a provision produces effects ('produzindo efeitos a "
            "partir de ...'), the change is dated by that day, not by the act's in-force day (dates after "
            f"{TODAY} are on the future branch); hunks a later act replaced before their effect day never took effect. "
            "Applied by effects_fix.py after the replay. " + " | ".join(moved) + ".")
    o = Path(out or path)
    tmp = o.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=None, separators=(",", ":")) + "\n", encoding="utf-8",
                   newline="\n")
    tmp.replace(o)
    return moved


if __name__ == "__main__":
    args = sys.argv[1:]
    out = args[args.index("--out") + 1] if "--out" in args else None
    res = run(args[0], out)
    print(len(res), "moves")
    for w in WARN:
        print("WARN", w)
    if "--report" in args:
        for x in res:
            print(" -", x[-700:])
