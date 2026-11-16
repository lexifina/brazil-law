"""Spanish blind spots, in a copy of global-law's vulnerabilities/scripts (idempotent):
- ingest/textscan.py: dates the time-limit search missed: "hasta el día 31 de diciembre de 2020" (the word "día" between
  "hasta el" and the date) and "31 de diciembre del 2020" / "31 de diciembre del año 2020" (the year after "del (año)");
- detectors/currency_scan.py: "marco" (framework) and "escudo" (coat of arms) read as currencies: now only in lower case
  ("Artículo 4. Marco ...", "1. Escudo, emblema ..." are headings and list items), not "Decisión marco 2002/629/JAI",
  and not "escudo 390 mm".

    python -X utf8 patch_es.py <scripts dir>
"""
import sys
from pathlib import Path


def patch(rel, pairs):
    p = Path(sys.argv[1]) / rel
    s = p.read_text(encoding="utf-8")
    for name, a, b, *marker in pairs:
        if b in s or (marker and marker[0] in s):  # a marker: in place even if another patch edited the same text since
            print("in place:", name)
        elif a in s:
            s = s.replace(a, b, 1)
            print("patched:", name)
        else:
            raise SystemExit(f"not found: {name}")
    p.write_text(s, encoding="utf-8", newline="\n")


patch("ingest/textscan.py", [
    ("FILL: día", r'FILL = r"(?:the|le|el|o|il|', r'FILL = r"(?:the|le|el|d[íi]a|o|il|'),
    ("DATE: del (año)", r"(?:de\s+)?(?P<mon>{MON})\s*(?:de\s+)?(?P<y1>",
     r"(?:de\s+)?(?P<mon>{MON})\s*(?:del?\s+(?:año\s+)?)?(?P<y1>",
     r"(?:del?\s+(?:año\s+)?)?(?P<y1>"),
])
patch("detectors/currency_scan.py", [
    ("escudo: lower case, not a size in mm", r"pesetas?|escudos?|francos?\b", r"pesetas?|(?-i:escudos?)\b(?!\s*[0-9.,]+\s*mm)|francos?\b",
     r"(?-i:escudos?)\b(?!\s*[0-9.,]+\s*mm)"),  # patch_ca.py adds pessetes after pesetas, so the marker says this is in place
    ("marco: lower case, not 'Decisión marco'", r"|marcos?\b|", r"|(?<![Dd]ecisión )(?-i:marcos?)\b|"),
])
