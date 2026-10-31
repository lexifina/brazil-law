"""strip_links(text): drop the link lines Planalto prints between a law's heading and its ementa.

The law pages print, after the heading 'LEI Nº ..., DE ...' and before the ementa, links such as 'Mensagem de veto',
'Vigência', 'Regulamento', 'Conversão da MPv nº 1.890-67, de 1999', 'Vide Decreto nº 3.048, de 1999', '(Promulgação
partes vetadas)', 'Revogada pela Lei nº 8.630, de 25.2.1993', 'Texto para impressão'. The page_info readers took the
ementa as the text from the heading to 'O PRESIDENTE DA REPÚBLICA', skipping some of these links; the rest started
the law's title. strip_links removes every such link at the start of the text, one after another, so the title is
the ementa itself. It removes only text at the start; the ementa is never changed.
"""
from __future__ import annotations

import re

_NUM = r"n?\s*[º°o]?\s*s?\s*\.?\s*:?\s*\d[\d.]*(?:\s\d[\d.]*)?(?:\s*-\s*[A-Z0-9]+)?"          # nº 1.890-67, nºs: 8.029, nº 2.110-40
_DATE = r"(?:\d{1,2}\s*[º°]?\s*\.\s*\d{1,2}\s*\.\s*\d{2,4}|\d{4})"           # 1999, 25.2.93, 6.9.2021
_OF = rf"(?:\s*,?\s*(?:de\s*)?{_DATE})"                                        # ', de 1999', ', 1971', ' de 25.3.2008'
_KIND = (r"(?:Lei(?:s)?(?:\s+Complementar|\s+Delegada)?|Medida\s+Provis[óo]ria|Medida|MPV|Mpv|MPv|Decreto(?:s)?(?:[-\s]?Lei)?|"
         r"Del|RSF|Ato\s+Declarat[óo]rio|Resolu[çc][ãa]o(?:\s+do\s+Senado\s+Federal)?|ADIN?|ADPF|ADC|Mensagem\s+de\s+Veto(?:\s+Total)?|Ato\s+Complementar|"
         r"Emenda\s+Constitucional)")
_REF = rf"{_KIND}\s*{_NUM}{_OF}?(?:\s*(?:,|e)\s*[\d.]+{_OF})*"                # one cited act (or a list of numbers)

LINKS = [
    # any parenthesised link: (Vide ...), (Promulgação partes vetadas), (Vigência), (Mensagem de veto), (Regulamento) ...
    r"\(\s*(?:V\s?ide|Promulga|Mensagem|Vig[êe]ncia|Regulamento|Produ[çc][ãa]o|Convers|Convertid|Revogad|Exposi|"
    r"Altera[çc][õo]es\s+contempladas|Texto|Rejeitad|Prorrogad|Partes\s+vetadas|Execu[çc][ãa]o)[^()]*(?:\([^()]*\)[^()]*)*\)",
    r"V\s?ide\s*:?\s*-?\s*(?:ADIN?\s*n?[º°]?\s*s?\s*[\d./-]+(?:\s+[\d./-]+)*(?:-?\s*STF\b)?(?:" + _OF + r")?\.?|" + _REF + r"\)?)",
    r"Convers[ãa]o\s+(?:d[aeo]\s+)?(?:Medida\s+Provis[óo]ria|MPV|MPv|Mpv|PMV)\s*" + _NUM + _OF + r"?",
    r"Convertid[ao]\s+(?:d[ao]|n[ao])\s+" + _REF,
    r"Promulga[çc][ãa]o\s+(?:d[aeo]s?\s+)?(?:partes?|parte)\s+vetadas?",
    r"Mensagem\s+de\s+veto(?:\s+total)?(?:\s*" + _NUM + _OF + r"?)?",
    r"Vig\s?[êe]\s?ncia(?:\s+encerrada|\s+e\s+produ[çc][ãa]o\s+de\s+efeitos?)?",
    r"Regulamento\b(?:\s*:\s*" + _REF + r"(?:[\s.]+" + _REF + r")*)?",   # 'Regulamento: Decreto nº 6.829, de 2009.'
    r"Regulamenta(?=\s+(?:Disp[õo]e|Altera|Institui|Estabelece)\b)",   # a 'Regulamento' link printed 'Regulamenta'
    r"P\s?rodu[çc][ãa]o\s+de\s+e\s?feitos?",       # also 'P rodução de efeitos' (LC 190/2022)
    r"Exposi[çc][ãa]o\s+d[aeo]s?\s+[Mm]otivos?",
    r"Te(?:x)?to\s+(?:(?:para|de)\s+impress\s?[ãa]o|compilado)",
    r"Prejudicad[ao]\b",
    r"Reeditad[ao]\s+pel[ao]\s+" + _REF,
    r"Artigo\s+\d+\s+da\s+Constitui[çc][ãa]o\s+Federal(?=\s+(?:Altera|Disp[õo]e|Institui|Regulamenta|Estabelece)\b)",
    r"Partes\s+promulgadas(?:\s+pelo\s+Congresso\s+Nacional)?",
    r"Revogad[ao]s?(?:\s+e\s+Reeditad[ao])?\s+pel[ao]\s+" + _REF,
    r"Prorrogad[ao]\s+(?:pel[ao]|por)\s+" + _REF,
    r"Rejeitad[ao]\b",
    r"-\s*\d+\s*,\s*de\s+\d{4}",                 # the tail of a conversion link an older reader cut at the MP number
]
_LEAD = re.compile(r"^[\s.]*(?:" + "|".join(f"(?:{x})" for x in LINKS) + r")[\s.;:)]*", re.I)


def strip_links(text: str) -> str:
    """The text with every link at its start removed (the ementa follows them)."""
    while True:
        m = _LEAD.match(text)
        if not m or not m.group(0).strip():
            return text.lstrip()
        text = text[m.end():]


# The ementa: the text after the heading (and its links) up to the enacting formula. The readers took it only when it
# ended with a full stop right before 'O PRESIDENTE ...' within 1500 characters of the heading; ementa_old is that
# reading, kept first so every title it gave is unchanged. ementa_more reads the layouts it missed.
_FORMULA = r"(?:O\s+PRESIDENTE|O\s+VICE|A\s+PRESIDENTA|O\s+CONGRESSO|Fa[çc]o saber)"
_OLD = re.compile(r"(.*?\.)\s*" + _FORMULA, re.S)

# the enacting formula as the pages print it: in capitals or not ('O Presidente da República, usando da atribuição'),
# split ('O PRESIDENT E DA REPÚBLICA'), without the article ('PRESIDENTE DA REPÚBLICA'), the 1969 military ministers
# ('OS MINISTROS DA MARINHA DE GUERRA, ...'), Congress ('O Congresso Nacional decreta'). Case-sensitive on purpose: an
# ementa names 'do Presidente da República' in lower case.
_FORMULA_MORE = re.compile(
    r"O\s+PRESIDENT\s?E\b|O\s+VICE\b|VICE-?\s*PRESIDENTE\s+DA\s+REP|A\s+PRESIDENTA\b|O\s+CONGRESSO\b|Fa[çc]o\s+saber|"
    r"PRESIDENTE\s+DA\s+REP[ÚU]BLICA|O\s+Presidente\s+da\s+Rep[úu]blica|OS\s+MINISTROS\s+DA\s+MARINHA|"
    r"O\s+Congresso\s+Nacional\s+decreta|O\s+PRESIDENTE\s+DO\s+SENADO|"
    r"A\s+Mesa\s+do\s+Congresso\s+Nacional|As\s+Mesas\s+da\s+C[âa]mara\s+dos\s+Deputados")   # constitutional amendments
# page links and navigation the old reader's links list lacked, or their remnants, before the ementa
_LEAD_MORE = re.compile(
    r"^[\s.]*(?:Fica\s+sem\s+efeito\s+pel[ao]\s+" + _REF + r"|[Ss]uspens[ao]\s+pel[ao]\s+" + _REF + r"|"
    r"V\s?ide\s+texto\s+compilado|e\s+vig[êe]ncia\b|E\s+feitos?\s+financeiros?|Estrutura\s+Regimental(?:\s*\([^()]*\))?|"
    r"N[ãa]o\s+remover|Down\b|Up\b|-->|Texto\s+atualizado)[\s.;:)]*")
# the same at the end, between the ementa and the formula: navigation ('Não remover Down Up Texto para impressão Texto
# atualizado Texto compilado'), every link strip_links knows, and the notes of a rewritten ementa ('(Redação dada pela
# Lei nº 14.423, de 2022)', '(Vigência encerrada)')
_TAIL = re.compile(
    r"(?:\s|^)(?:N[ãa]o\s+remover|Down|Up|-->|Texto\s+atualizado|"
    r"\(\s*(?:Reda[çc][ãa]o\s+dada|Inclu[íi]d[ao])\s+pel[ao]\s+[^()]*\)|" + "|".join(f"(?:{x})" for x in LINKS) + r")[\s.;:]*$")   # links are capitalised: not re.I
_NAV = re.compile(r"\bN[ãa]o\s+remover\b|\bTexto\s+(?:compilado|atualizado|para\s+impress)|-->|\bUp\s+Down\b|\bDown\s+Up\b", re.I)
_REWRITTEN = re.compile(r"\(\s*Reda[çc][ãa]o\s+dada\s+pel[ao]\s", re.I)


def _lead_more(text: str) -> str:
    while True:
        text = strip_links(text)
        m = _LEAD_MORE.match(text)
        if not m or not m.group(0).strip():
            return text
        text = text[m.end():]


def ementa_more(after: str) -> str:
    """Layouts the old reading missed, '' when none fits: no full stop before the formula ('Modifica o art. 226 da
    Consolidação das Leis do Trabalho O Presidente da República, usando ...'), navigation and links between the ementa
    and the formula, the formula in other forms (_FORMULA_MORE), an ementa longer than the old window. An ementa a later
    act rewrote is printed twice, the enacted wording first, then the new one with its '(Redação dada pela ...)' note:
    the law's title is the enacted wording (its first sentence), as other parts already give it."""
    text = _lead_more(after.lstrip(" ."))       # the heading's own full stop ('DE 1966. Altera ...')
    f = _FORMULA_MORE.search(text)
    if not f:
        return ""
    e = text[:f.start()]
    nav = _NAV.search(e)              # page navigation never belongs to an ementa: it ends there
    if nav:
        e = e[:nav.start()]
    rewritten = bool(_REWRITTEN.search(e))
    while True:
        m = _TAIL.search(e)
        if not m or m.start() == len(e):
            break
        e = e[:m.start()]
    e = " ".join(e.split())
    e = re.sub(r"(\.)\s*\([A-ZÁÉÍÓÚÂÊÔÃÕÇ ]+\)$", r"\1", e)      # a nickname after the ementa: '... providências. (LEI DOS PORTOS)'
    e = e.rstrip(" ,;:")
    if rewritten:
        s = re.search(r"\.(?=\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ(])", e)
        if not s:
            return ""
        e = e[:s.end()]
    if not re.match(r"[A-ZÁÉÍÓÚÂÊÔÃÕÇ]", e) or len(e) < 10 or re.search(r"\bArt\.\s*\d", e):
        return ""
    return e


def ementa(after: str, rest: str = "") -> str:
    """The law's title from the text after its heading (links stripped); `rest` is the page text that follows `after`."""
    t = ementa_old(after)
    if not t:
        t = ementa_more(after + rest)
        import os
        if os.environ.get("TITLES_DUMP"):
            import json
            with open(os.environ["TITLES_DUMP"], "a", encoding="utf-8") as f:
                f.write(json.dumps({"after": after, "rest": rest, "title": t}, ensure_ascii=False) + "\n")
    return t


def ementa_old(after: str) -> str:
    em = _OLD.match(after)
    return em.group(1).strip() if em else ""
