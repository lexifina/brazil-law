"""Seventh round (found by the Vietnam update), in the shape of patch_detectors.py: Vietnamese dates, references, đồng.

    python -X utf8 patch_vi.py <scripts dir>        (idempotent)

Dates (ingest/textscan.py, detectors/text_detectors.py):
  - "ngày 31 tháng 12 năm 2020" (day, "tháng" month, "năm" year), and the end of a year ("hết năm 2020", "cuối năm 2020");
  - "until" words "đến", "cho đến" (not "tính đến", which is "as at"), with "hết", "là", "vào", "ngày" between word and date:
    "đến hết ngày 31 tháng 12 năm 2016", "cho đến ngày 01 tháng 7 năm 2017";
  - deadline words "chậm nhất" ("chậm nhất là ngày 01 tháng 01 năm 2019") and "trước" ("trước ngày 01/7/2021"): read as
    limits, ranked as deadlines, left out of empty periods.
References (ingest/refscan.py): "Điều 12", "khoản 2 Điều 5", "điểm a khoản 1 Điều 3" (the article is the key); "và"/"hoặc"
  lists and "đến" ranges; "Điều 5 của Luật Đất đai" / "Điều 5 Bộ luật Hình sự" is another act (but "Luật này" is this one).
Amounts (ingest/textscan.py): "5.000.000 đồng", "50 triệu đồng", "VND".
"""
import sys
from pathlib import Path

S = Path(sys.argv[1])
done, skipped = [], []


def patch(rel, pairs):
    p = S / rel
    s = p.read_text(encoding="utf-8")
    for name, a, b in pairs:
        if b in s:
            skipped.append(f"{rel}: {name}")
            continue
        if s.count(a) != 1:
            raise SystemExit(f"{rel}: {name}: anchor found {s.count(a)} times")
        s = s.replace(a, b)
        done.append(f"{rel}: {name}")
    p.write_bytes(s.encode("utf-8"))


patch("ingest/textscan.py", [
    ("Vietnamese end of a year",
     r'fund(?:in)?\s+t[ëe]\s+vitit\s+)(?P<y6>',
     r'fund(?:in)?\s+t[ëe]\s+vitit\s+|(?:hết|cuối)\s+năm\s+)(?P<y6>'),
    ("Vietnamese 'ngày D tháng M năm Y'",
     r'        r"|(?P<d3>\d{1,2})(?:η|ή)?\s?[./]',
     r'        r"|(?P<d9>\d{1,2})\s+tháng\s+(?P<m9>\d{1,2}),?\s+năm\s+(?P<y9>\d{4})"' + "\n" +
     r'        r"|(?P<d3>\d{1,2})(?:η|ή)?\s?[./]'),
    ("Vietnamese deadline words",
     r'legkésőbb|jo më vonë se")',
     r'legkésőbb|jo më vonë se|chậm nhất|trước")'),
    ("Vietnamese 'until' words",
     r'cel mai t[âî]rziu la|jo më vonë se")',
     r'cel mai t[âî]rziu la|jo më vonë se|cho đến|(?<!tính )đến|chậm nhất|trước")'),
    ("Vietnamese fillers",
     r'dnia|dnem|la)\s+"',
     r'dnia|dnem|la|ngày|hết|là|vào)\s+"'),
    ("parse 'ngày D tháng M năm Y'",
     '            elif g.get("y5"):',
     '            elif g.get("y9"):\n                y, mo, d = int(g["y9"]), int(g["m9"]), int(g["d9"])\n            elif g.get("y5"):'),
    ("Vietnamese VND",
     r'dinars?|dirhams?|riyals?")',
     r'dinars?|dirhams?|riyals?|vnd")'),
    ("Vietnamese đồng, after the number only ('hợp đồng 12 tháng' is a contract, not 12 đồng)",
     r'|(?P<n2>{NUM})\s?(?P<c2>{CUR}|{PCT}))(?!\w)")',
     r'|(?P<n2>{NUM})\s?(?P<c2>{CUR}|{PCT}|(?:triệu\s|tỷ\s|tỉ\s)?đồng))(?!\w)")'),
])
patch("detectors/text_detectors.py", [
    ("Vietnamese deadline in the ranking", "|jo më vonë)') as deadline,", "|jo më vonë|chậm nhất|trước ngày)') as deadline,"),
    ("Vietnamese deadline in the score", "|jo më vonë|report|submit", "|jo më vonë|chậm nhất|trước ngày|report|submit"),
])
patch("ingest/refscan.py", [
    ("Vietnamese 'Điều'",
     r'seksyen|regulation|rule|"',
     r'seksyen|regulation|rule|điều|"'),
    ("Vietnamese lists",
     r'\bта\b|\bи\b|\bа\b|"',
     r'\bта\b|\bи\b|\bа\b|\bvà\b|\bhoặc\b|"'),
    ("Vietnamese 'Điều' in lists",
     r'(?:(?:art\.|arts\.|§§?|section|sections|artikel|artículo|artigo|articolo)\s*)?{NUM}")',
     r'(?:(?:art\.|arts\.|§§?|section|sections|artikel|artículo|artigo|articolo|điều)\s*)?{NUM}")'),
    ("Vietnamese ranges",
     r'till|–|-|—|до|do)\s*(?:(?:art\.|§§?|section)\s*)?{NUM}", re.I)' + "\n# Czech",
     r'till|–|-|—|до|do|đến)\s*(?:(?:art\.|§§?|section|điều)\s*)?{NUM}", re.I)' + "\n# Czech"),
    ("Vietnamese reference to another act",
     "    return bool(EXT_BEFORE.search(before[-60:]) or EXT_AFTER.match(tail))",
     "    return bool(EXT_BEFORE.search(before[-60:]) or EXT_AFTER.match(tail) or EXT_AFTER_VI.match(tail))\n\n\n"
     "# Vietnamese: \"Điều 5 của Luật Đất đai\", \"khoản 2 Điều 5 Bộ luật Hình sự\" name another act; \"Luật này\" is this one\n"
     "EXT_AFTER_VI = re.compile(r\"^\\s*,?\\s*(?:của\\s+|tại\\s+)?(?:Luật|Bộ\\s+luật|Hiến\\s+pháp|Pháp\\s+lệnh|Nghị\\s+định|Nghị\\s+quyết|\"\n"
     "                          r\"Thông\\s+tư|Quyết\\s+định|Công\\s+ước|Hiệp\\s+định|Điều\\s+ước)(?!\\s+này)\\b\")"),
])
print("applied:", *done, sep="\n  ")
print("already in place:", *skipped, sep="\n  ")
