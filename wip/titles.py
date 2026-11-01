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
    r"Produ[çc][ãa]o\s+de\s+e\s?feitos?",
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
