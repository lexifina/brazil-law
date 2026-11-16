"""Portuguese (Brazilian) blind spots, in a copy of global-law's vulnerabilities/scripts (idempotent):
- ingest/textscan.py: dates the time-limit search missed: the ordinal first day ("até 1º de janeiro de 2021", "1o de
  março"), "31 de dezembro do ano de 2020" and "até a data de 30 de abril de 2020";
- ingest/refscan.py: "art. 3º-A" was read as article 3 (the ordinal sign stopped the letter suffix) and "arts. 4º a 7º" as
  article 4 alone; "§ 2º" (a paragraph of an article in Brazilian law) was read as article 2; a quoted article label that
  opens the amended text in an amending act ('"Art. 5º ...') was read as a reference to the amending act's own article;
  and "art. 90 da Medida Provisória nº 2.158-35", "art. 37 da Constituição Federal", "art. 2º, inciso II, da Lei nº
  9.317" or "artigos 4º a 6º do Decreto-lei nº 1.439" were read as references to the act's own articles. The language
  comes from pins.json, as in textscan.py;
- detectors/placeholder_ref.py: a live article whose text is a repeal clause ("Fica revogado o § 1º ...", "São
  revogados os artigos ...", "Revogam-se ...") was read as a repeal placeholder, and so was an article that merely uses
  the word ("A remuneração poderá ser reduzida ou suprimida ..."): "revogado" and "suprimido" now count only right after
  the article's label, as in "Art. 212. (Revogado).";
- detectors/currency_scan.py: amounts in the old Brazilian currencies are written with their symbols ("Cr$ 200,00",
  "Cz$ 10.000,00", "NCz$ 50,00", "CR$ 5.000,00"), which were not read; "cruzeiros" and "cruzados" were; and "marco"
  (a survey marker, "partindo do marco 26", or a framework, "marco legal") was read as the German mark;
- detectors/dup_labels.py: "§ 1º A não observância ..." was read as paragraph 1-A (the article "A" after a space taken for
  a letter suffix; Brazilian suffixes are written "§ 1º-A", sometimes "§ 2º -A." or "§ 1º A."), and "Art. 1.635" and
  "Art. 1.636" both as "art 1".

    python -X utf8 patch_pt.py <scripts dir>      (after the kit's patches: patch_detectors.py, patch_es.py, ...)
"""
import sys
from pathlib import Path


def patch(rel, pairs):
    p = Path(sys.argv[1]) / rel
    s = p.read_text(encoding="utf-8")
    for name, a, b, *marker in pairs:
        if b in s or (marker and marker[0] in s):
            print("in place:", name)
        elif a in s:
            s = s.replace(a, b, 1)
            print("patched:", name)
        else:
            raise SystemExit(f"not found: {name}")
    p.write_text(s, encoding="utf-8", newline="\n")


patch("ingest/textscan.py", [
    ("DATE: 1º de", r"(?P<d1>\d{{1,2}})(?:η|ή|ης|ής|-?го|-?ти)?",
     r"(?P<d1>\d{{1,2}})(?:η|ή|ης|ής|-?го|-?ти|º|°|o(?=\s+de\s))?"),
    ("DATE: do ano de", r"(?:del?\s+(?:año\s+)?)?(?P<y1>", r"(?:del?\s+(?:año\s+)?|do\s+ano\s+de\s+)?(?P<y1>"),
    ("FILL: a data de", r'FILL = r"(?:the|', r'FILL = r"(?:a\s+data\s+de|the|', r'a\s+data\s+de|'),
])
patch("ingest/refscan.py", [
    ("NUM: 3º-A", r"|[\-‑]?([A-Za-z]{{1,2}})(?![A-Za-zÀ-ÿ\d]))?", r"|[º°]?[\-‑]?([A-Za-z]{{1,2}})(?![A-Za-zÀ-ÿ\d]))?"),
    ("LISTNUM: 4º, 5º", r'LISTNUM = re.compile(rf"\s*(?:,|;|', r'LISTNUM = re.compile(rf"[º°]?\s*(?:,|;|'),
    ("RANGENUM: 4º a 7º", r'RANGENUM = re.compile(rf"\s*(?:to|through|thru|bis|à|a|al|',
     r'RANGENUM = re.compile(rf"[º°]?\s*(?:to|through|thru|bis|à|a|al|'),
    ("language from pins.json", '_LANG = {"v": ""}\n',
     '_LANG = {"v": ""}\ntry:  # a one-country run (pins.json names one corpus): placeholder_ref and dead_fine call refs() without one()\n'
     '    _LANG["v"] = (lambda cs: (cs[0].get("language") or "").lower() if len(cs) == 1 else "")(pins()["corpora"])\n'
     'except Exception:\n    pass\n'),
    ("pt: § and quoted labels",
     '                continue  # Nordic "6 § 2 mom.": the § belongs to the number before it\n',
     '                continue  # Nordic "6 § 2 mom.": the § belongs to the number before it\n'
     '            if rx is REF and _LANG["v"] == "pt" and (m.group(0).lstrip().startswith("§") or re.search(r"[\\"“]\\s*$", before)):\n'
     '                continue  # Portuguese: "§ 2º" is a paragraph, not an article; \'"Art. 5º ...\' opens quoted amended text\n'),
    ("pt: external tails", "    return bool(EXT_BEFORE.search(before[-60:])",
     "    return bool((_LANG[\"v\"] == \"pt\" and EXT_AFTER_PT.match(tail)) or EXT_BEFORE.search(before[-60:])"),
    ("EXT_AFTER_PT", "\n\nTHAI = re.compile(",
     "\n\n# Portuguese: \"art. 90 da Medida Provisória nº ...\", \"art. 2º, inciso II, da Lei nº ...\", \"art. 37 da Constituição\"\n"
     "EXT_AFTER_PT = re.compile(r\"(?i)^[º°]?\\.?(?:\\s*(?:,|e|a|até)\\s*\\d+[º°]?(?:-[A-Z])?)*\\s*(?:(?:,\\s*|\\s+)(?:caput|§§?\\s*\\d+[º°]?(?:-[A-Z])?|incisos?\\s+[IVXLCDM]+(?:-[A-Z])?|\"\n"
     "                          r\"al[íi]neas?\\s+[\\\"“]?[a-z][\\\"”]?|par[áa]grafo\\s+[úu]nico|itens?\\s+\\d+)\"\n"
     "                          r\"(?:\\s*(?:,|e)\\s*(?:[IVXLCDM]+|\\d+[º°]?|[\\\"“]?[a-z][\\\"”]?))*)*\\s*,?\\s*(?:d[oa]s?|n[oa]s?)\\s+\"\n"
     "                          r\"(?:Lei|Decreto|Medida|Constitui|C[óo]digo|Consolida|Emenda|Estatuto|Resolu|Portaria|Instru|Conven|\"\n"
     "                          r\"Tratado|Regulamento|Regimento|Ato\\b|CLT\\b|CTN\\b|ADCT\\b|CF\\b|LC\\b)\")\n\n\nTHAI = re.compile(",
     "EXT_AFTER_PT = re.compile("),
])
patch("detectors/placeholder_ref.py", [
    ("repeal clauses", "|quedan derogad|ficam revogad|",
     "|quedan derogad|ficam? revogad|(?:são|é|serão|será|foram|foi) revogad|revogam-se|revoga-se|"),
    ("revogado only after the label",
     "    return len(substantive) <= 400 and bool(GONE.search(substantive[:70]))",
     "    g = GONE.search(substantive[:70])\n"
     "    if g and re.match(r\"(?i)revogad|suprimid\", g.group(0)) and not PT_AT_LABEL.match(substantive):\n"
     "        return False  # Portuguese: \"(Revogado)\" stands right after the label; \"... reduzida ou suprimida\" is text\n"
     "    return len(substantive) <= 400 and bool(g)\n"
     "PT_AT_LABEL = re.compile(r\"(?i)^\\W{0,3}(?:(?:art\\.?|artigo|artículo|§)\\s*)?(?:\\d[\\d.]*\\s*[º°o]?\\s*(?:-\\s*[A-Z]{1,2}\\b)?\\s*)?\"\n"
     "                         r\"[.\\-–—:]?\\s*[(\\[]?\\s*(?:revogad|suprimid)\")"),
])
patch("detectors/currency_scan.py", [
    ("Cr$, Cz$, NCz$, CR$", r"|cruzeiros?|cruzados?|", r"|cruzeiros?|cruzados?|(?-i:(?<![A-Za-z])(?:N?Cz|Cr|CR)\$)|"),
    ("marco: not in Portuguese", r'NOT_CURRENCY = {"', r'NOT_CURRENCY = {"pt": (r"|(?<![Dd]ecisión )(?-i:marcos?)\b",), "',
     r'"pt": (r"|(?<![Dd]ecisión )(?-i:marcos?)\b",)'),
])
patch("detectors/dup_labels.py", [
    ("§ 1º A: no space before a letter suffix", r"(§+\s*\d+[º°o]?(?:[-‑ ]?[A-Z]{1,2}\b)?", r"(§+\s*\d+[º°o]?(?:\s?[-‑][A-Z]{1,2}\b|[A-Z]{1,2}\b|\s[A-Z]{1,2}(?=\.\s))?"),
    ("Art. 1.635: thousands; no space before a letter suffix",
     r"\s+\d+[º°o]?(?:[-‑ ]?(?:[A-Z]{1,2}|bis|",
     r"\s+(?:\d{1,3}(?:\.\d{3})+|\d+)[º°o]?(?:\s?[-‑][A-Z]{1,2}\b|[A-Z]{1,2}\b|\s[A-Z]{1,2}(?=\.\s)|[-‑ ]?(?:bis|"),
])
