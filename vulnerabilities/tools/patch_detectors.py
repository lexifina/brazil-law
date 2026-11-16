"""Fixes the blind spots found in the ten one-country runs, in a copy of global-law's vulnerabilities/scripts.

    python -X utf8 patch_detectors.py <scripts dir>        (idempotent: a fix already in place is skipped)

1. Dates (ingest/textscan.py, used by lapsed_limit and late_extension):
   - month names: Bosnian/Serbian/Montenegrin Latin (januara ... decembra), Serbian/Montenegrin Cyrillic (јануара ...),
     Bulgarian (януари ...), Croatian "studenog";
   - numeric dates written with spaces ("31. 12. 2020."), Greek ordinals ("31η Δεκεμβρίου 2020");
   - "until" phrases: Greek "έως (και) την", Romanian "până/pînă la data de", Croatian/Serbian "zaključno s(a)",
     Bosnian "do dana", and the end of a year ("do kraja 2020. godine", "do konce roku 2020", "до края на 2020 г.",
     "până la sfârșitul anului 2020");
   - Turkish, where the date comes first: "31/12/2020 tarihine kadar", "31 Aralık 2020'ye kadar", "2020 yılı sonuna kadar";
   - deadline words in more languages ("najkasnije", "en geç", "το αργότερο", "cel târziu", "най-късно"), so a deadline is
     ranked as one (detectors/text_detectors.py) and left out of empty periods.
2. References (ingest/refscan.py, used by dangling_ref):
   - Czech/Slovak "a" means "and", not "to": "§ 1817 a 1826a" and "§ 7 a § 11" are two references, not a range;
   - Belgian "259bis-9" is article 259bis-9, not 259bis;
   - file names "clanak-N" (Croatia), "clan-N" (Montenegro, Serbia) and "ugovor-/naredba-" prefixed ones give the article;
   - an article heading after a chapter heading at the top of a file is the file's own heading.
3. Currencies (detectors/currency_scan.py): the Belgian franc (francs, frank, BEF); "DM" only in capitals and as a word
   or right after a decimal amount (not "dm" decimetres or letters inside identifiers); "franco"/"inti"/"lire"/"marco" only as
   whole words; Albanian "lireta".
4. Albanian dates: "deri më datën 31.12.2010" and "deri në fund të vitit 2010".
"""
import re, sys
from pathlib import Path

S = Path(sys.argv[1])
done, skipped = [], []


def patch(rel, pairs):
    p = S / rel
    s = p.read_text(encoding="utf-8")
    for name, a, b, *marker in pairs:
        if b in s or (marker and marker[0] in s):  # a marker: the fix is in place even if a later insertion split it
            skipped.append(f"{rel}: {name}")
            continue
        if s.count(a) == 0:  # superseded by a later round already applied (e.g. the end-of-year forms)
            skipped.append(f"{rel}: {name} (superseded)")
            continue
        if s.count(a) != 1:
            raise SystemExit(f"{rel}: {name}: anchor found {s.count(a)} times")
        s = s.replace(a, b)
        done.append(f"{rel}: {name}")
    p.write_bytes(s.encode("utf-8"))


# ---------------------------------------------------------------- 1. dates
patch("ingest/textscan.py", [
    ("month names",
     '          "января февраля марта апреля мая июня июля августа сентября октября ноября декабря").split()',
     '          "января февраля марта апреля мая июня июля августа сентября октября ноября декабря "\n'
     '          "januara februara marta aprila maja juna jula augusta septembra oktobra novembra decembra "\n'
     '          "јануара фебруара марта априла маја јуна јула августа септембра октобра новембра децембра "\n'
     '          "януари февруари март април май юни юли август септември октомври ноември декември "\n'
     '          "siječnja veljače ožujka travnja svibnja lipnja srpnja kolovoza rujna listopada studenog prosinca "\n'
     '          "ianuarie februarie martie aprilie mai iunie iulie august septembrie octombrie noiembrie decembrie").split()'),
    ("dates: Greek ordinals, spaced numeric dates, end of a year",
     'DATE = (rf"(?P<d1>\\d{{1,2}})\\.?\\s*(?:de\\s+)?(?P<mon>{MON})\\s*(?:de\\s+)?(?P<y1>\\d{{4}})"',
     'DATE = (r"(?:kraja\\s+|konce\\s+roku\\s+|края\\s+на\\s+|sf[âa]r[sș]itul\\s+anului\\s+)(?P<y6>\\d{4})(?!\\d)(?!\\s?[./]\\s?\\d)(?:\\.?\\s*(?:godine|г\\.?))?|"\n'
     '        rf"(?P<d1>\\d{{1,2}})(?:η|ης|-?го|-?ти)?\\.?\\s*(?:de\\s+)?(?P<mon>{MON})\\s*(?:de\\s+)?(?P<y1>\\d{{4}})"'),
    ("spaced numeric dates",
     'r"|(?P<d3>\\d{1,2})[./](?P<m3>\\d{1,2})[./](?P<y3>\\d{4})"',
     'r"|(?P<d3>\\d{1,2})\\s?[./]\\s?(?P<m3>\\d{1,2})\\s?[./]\\s?(?P<y3>\\d{4})"'),
    ("deadline words",
     'DEADLINE = r"not later than|no later than|spätestens|au plus tard|a más tardar|uiterlijk|senest|senast|najpóźniej|nejpozději"',
     'DEADLINE = (r"not later than|no later than|spätestens|au plus tard|a más tardar|uiterlijk|senest|senast|najpóźniej|nejpozději|"\n'
     '            r"najneskôr|najkasnije|en geç|το αργότερο|cel (?:mai )?t[âî]rziu|най-късно|не по-късно от|не позднее|viimeistään|legkésőbb")'),
    ("until phrases",
     'r"mpaka|sampai dengan|hingga")',
     'r"mpaka|sampai dengan|hingga|pînă la|pînă pe|zaključno sa|zaključno s|zakljucno sa|zakljucno s|ως")'),
    ("fillers between 'until' and the date",
     'LIMIT = re.compile(rf"(?i)\\b(?:{UNTIL})\\s*(?:the\\s+|le\\s+|el\\s+|o\\s+|il\\s+|den\\s+|dem\\s+)?(?:{DATE})")',
     'FILL = r"(?:the|le|el|o|il|den|dem|και|την|τη|τις|το|data\\s+de|ziua\\s+de|dana|dne|dnia|dnem|la)\\s+"\n'
     'LIMIT = re.compile(rf"(?i)\\b(?:{UNTIL})\\s*(?:{FILL}){{0,2}}(?:{DATE})")\n'
     '# Turkish puts the date first: "31/12/2020 tarihine kadar", "31 Aralık 2020\'ye kadar", "2020 yılı sonuna kadar"\n'
     'LIMIT_POST = re.compile(rf"(?i)(?:(?P<y7>\\d{{4}})\\s+yılı(?:nın)?\\s+sonuna|(?:{DATE}))(?:[\'’]?\\w{{0,4}})?\\s*"\n'
     '                        rf"(?:tarihine|tarihi|gününe|günü)?\\s*(?:kadar|dek|değin)\\b")'),
    ("parse every match form",
     '    for m in LIMIT.finditer(text):\n        g = m.groupdict()\n        if not deadlines and re.match(rf"(?i)(?:{DEADLINE})\\b", m.group(0)):\n            continue\n        try:\n            if g.get("y5"):',
     '    for m in sorted(list(LIMIT.finditer(text)) + list(LIMIT_POST.finditer(text)), key=lambda x: x.start()):\n        g = m.groupdict()\n'
     '        if not deadlines and (re.match(rf"(?i)(?:{DEADLINE})\\b", m.group(0)) or DEADLINE_RX.search(text[max(0, m.start() - 30):m.start()])):\n'
     '            continue\n        try:\n            if g.get("y6") or g.get("y7"):\n                y, mo, d = int(g.get("y6") or g.get("y7")), 12, 31\n            elif g.get("y5"):'),
])
patch("detectors/text_detectors.py", [
    ("deadline words in the ranking",
     "regexp_matches(lower(d.context), '(not later than|no later than|spätestens|a más tardar|au plus tard|senast|uiterlijk)') as deadline,",
     "regexp_matches(lower(d.context), '(not later than|no later than|spätestens|a más tardar|au plus tard|senast|uiterlijk|najkasnije|nejpozději|najneskôr|en geç|το αργότερο|cel mai t.rziu|cel t.rziu|най-късно|не по-късно)') as deadline,"),
    ("deadline words in the score",
     "'(not later than|no later than|spätestens|a más tardar|au plus tard|senast|uiterlijk|report|submit|bericht|informe)') then 0 else 0.3 end)",
     "'(not later than|no later than|spätestens|a más tardar|au plus tard|senast|uiterlijk|najkasnije|nejpozději|najneskôr|en geç|το αργότερο|cel mai t.rziu|cel t.rziu|най-късно|не по-късно|report|submit|bericht|informe)') then 0 else 0.3 end)"),
])

# second round (found by the Albania update): "deri më datën 31.12.2010", "deri në fund të vitit 2010"
patch("ingest/textscan.py", [
    ("Albanian 'datën' before the date",
     'FILL = r"(?:the|le|el|o|il|den|dem|και|',
     'FILL = r"(?:the|le|el|o|il|den|dem|datën|datës|datë|date|και|'),
    ("Albanian end of a year",
     r'sf[âa]r[sș]itul\s+anului\s+)(?P<y6>',
     r'sf[âa]r[sș]itul\s+anului\s+|fund(?:in)?\s+t[ëe]\s+vitit\s+)(?P<y6>'),
])

# third round (found by the Bulgaria update): "не по-късно от 31.12.2010", "изтича на ...", Roman-numeral months
# ("31.XII.2001"), Romanian "cel târziu la", Albanian "jo më vonë se"
patch("ingest/textscan.py", [
    ("more 'until' phrases",
     r'zakljucno sa|zakljucno s|ως")',
     r'zakljucno sa|zakljucno s|ως|не по-късно от|изтича на|cel t[âî]rziu la|cel mai t[âî]rziu la|jo më vonë se")'),
    ("Roman-numeral months",
     r'r"|(?P<d3>\d{1,2})\s?[./]\s?(?P<m3>\d{1,2})\s?[./]\s?(?P<y3>\d{4})"',
     r'r"|(?P<d8>\d{1,2})\.\s?(?P<m8>XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)\.\s?(?P<y8>\d{4})"' + "\n        " +
     r'r"|(?P<d3>\d{1,2})\s?[./]\s?(?P<m3>\d{1,2})\s?[./]\s?(?P<y3>\d{4})"'),
    ("Roman numerals table",
     'FILL = r"(?:the|',
     'ROMAN = {r: i for i, r in enumerate("I II III IV V VI VII VIII IX X XI XII".split(), 1)}\nFILL = r"(?:the|'),
    ("parse Roman-numeral months",
     '            elif g.get("y5"):',
     '            elif g.get("y8"):\n                y, mo, d = int(g["y8"]), ROMAN[g["m8"].upper()], int(g["d8"])\n            elif g.get("y5"):',
     'ROMAN[g["m8"].upper()]'),
    ("Albanian deadline word",
     r'не по-късно от|не позднее|viimeistään|legkésőbb")',
     r'не по-късно от|не позднее|viimeistään|legkésőbb|jo më vonë se")'),
])
patch("detectors/text_detectors.py", [
    ("Albanian deadline in the ranking", "|не по-късно)') as deadline,", "|не по-късно|jo më vonë)') as deadline,"),
    ("Albanian deadline in the score", "|не по-късно|report|submit", "|не по-късно|jo më vonë|report|submit"),
])

# fourth round (found by the Türkiye update): "31.12.2020 günü sonuna kadar", "31/12/2020 günü saat 17.00'ye kadar"
patch("ingest/textscan.py", [
    ("Turkish end of the day or a time before 'kadar'",
     r'''rf"(?:tarihine|tarihi|gününe|günü)?\s*(?:kadar|dek|değin)\b")''',
     r'''rf"(?:\s*(?:tarihi|günü)?\s*(?:sonuna|saat\s*\d{{1,2}}[:.]\d{{2}}(?:['’]?\w{{0,4}})?))?"''' + "\n                        " +
     r'''rf"\s*(?:tarihine|tarihi|gününe|günü)?\s*(?:kadar|dek|değin)\b")'''),
])

# fifth round (found by the Croatia update): shards must split the work the same way in every process, and
# Croatian "listopada" is October (it is November in Polish, which came first in the month list)
patch("ingest/textscan.py", [
    ("same row order in every shard",
     "where left(ch.status,1)='M' and r.kind='law'\"\"\").fetchall()",
     "where left(ch.status,1)='M' and r.kind='law' order by ch.commit, ch.path\"\"\").fetchall()"),
    ("language of the corpus (Croatian 'listopada' is October)",
     'ROMAN = {r: i for i, r in enumerate(',
     '# the corpus language decides the few month names that differ between languages; pins.json names it for a one-country\n'
     '# run, and one() sets it per corpus otherwise\n'
     'try:\n    _LANG = {"v": (lambda cs: cs[0].get("language") or "" if len(cs) == 1 else "")(pins()["corpora"])}\n'
     'except Exception:\n    _LANG = {"v": ""}\n'
     'MONTH_BY_LANG = {"listopada": {"hr": 10, "bs": 10, "sr": 10, "cnr": 10, "sh": 10}}\n'
     'ROMAN = {r: i for i, r in enumerate(',
     'MONTH_BY_LANG = {"listopada"'),
    ("set the language per corpus",
     "def one(c: dict, shard: int = 0, nshards: int = 1):\n    lower_priority()\n    t0 = time.time()\n    repo = CORPUS / f\"{c['repo']}.git\"\n    D = {k: [] for k in (\"path\", \"until\", \"context\")}",
     "def one(c: dict, shard: int = 0, nshards: int = 1):\n    lower_priority()\n    _LANG[\"v\"] = (c.get(\"language\") or \"\").lower()\n    t0 = time.time()\n    repo = CORPUS / f\"{c['repo']}.git\"\n    D = {k: [] for k in (\"path\", \"until\", \"context\")}"),
    ("month by language",
     '                y, mo, d = int(g["y1"]), MI[g["mon"].lower()], int(g["d1"])',
     '                y, mo, d = int(g["y1"]), MONTH_BY_LANG.get(g["mon"].lower(), {}).get(_LANG["v"], MI[g["mon"].lower()]), int(g["d1"])'),
])
patch("ingest/textscan.py", [  # found by the Greece update: «31η.12.2020», «30ή Ιουνίου»
    ("Greek accented ordinal", r'(?:η|ης|-?го|-?ти)?', r'(?:η|ή|ης|ής|-?го|-?ти)?'),
    ("Greek ordinal before a month in figures", r'r"|(?P<d3>\d{1,2})\s?[./]', r'r"|(?P<d3>\d{1,2})(?:η|ή)?\s?[./]'),
])
patch("ingest/refscan.py", [
    ("stable shard split",
     "acts_shard = {a for a in {act_of(h[0]) for h in hist} if hash(a) % nshards == shard} if nshards > 1 else None",
     "acts_shard = {a for a in {act_of(h[0]) for h in hist} if zlib.crc32(a.encode('utf-8')) % nshards == shard} if nshards > 1 else None  # hash() differs per process"),
    ("zlib", "import re, sys, time\n", "import re, sys, time, zlib\n"),
])

# ---------------------------------------------------------------- 2. references
patch("ingest/refscan.py", [
    ("Czech/Slovak 'a' is 'and'",
     'RANGENUM = re.compile(rf"\\s*(?:to|through|thru|bis|à|a|al|até|fino a|tot en met|tot|t/m|till|–|-|—|до|do)\\s*(?:(?:art\\.|§§?|section)\\s*)?{NUM}", re.I)',
     'RANGENUM = re.compile(rf"\\s*(?:to|through|thru|bis|à|a|al|até|fino a|tot en met|tot|t/m|till|–|-|—|до|do)\\s*(?:(?:art\\.|§§?|section)\\s*)?{NUM}", re.I)\n'
     '# Czech and Slovak "a" is "and" ("§ 1817 a 1826a"): set per corpus by one() and one_fileact() from pins.json\n'
     'RANGENUM_AND_A = re.compile(rf"\\s*(?:to|through|thru|bis|à|al|até|fino a|tot en met|tot|t/m|till|–|-|—|до|do)\\s*(?:(?:art\\.|§§?|section)\\s*)?{NUM}", re.I)\n'
     'LISTNUM_A = re.compile(rf"\\s*\\ba\\b\\s*(?:§§?\\s*)?{NUM}")\n'
     '_LANG = {"v": ""}'),
    ("use the corpus's range words",
     '        r = RANGENUM.match(body, pos)',
     '        r = (RANGENUM_AND_A if _LANG["v"] in ("cs", "sk") else RANGENUM).match(body, pos)'),
    ("Czech/Slovak 'a' continues a list",
     '        l = LISTNUM.match(body, pos)',
     '        l = LISTNUM.match(body, pos) or (LISTNUM_A.match(body, pos) if _LANG["v"] in ("cs", "sk") else None)'),
    ("Belgian 259bis-9",
     '            else:\n                first = _mkey(m)\n                ks, end = _expand(body, m, first)',
     '            else:\n                first = _mkey(m)\n'
     '                sub = re.match(r"[\\-‑](\\d{1,3})(?!\\d)(?![.,]\\d)", body[m.end():m.end() + 7]) if re.search(rf"(?i)(?:{LATIN})$", m.group(0)) else None\n'
     '                if sub:  # Belgian numbering: article 259bis-9 is its own article, not 259bis\n'
     '                    first, ks, end = f"{first}-{sub.group(1)}", [f"{first}-{sub.group(1)}"], m.end() + sub.end()\n'
     '                else:\n                    ks, end = _expand(body, m, first)'),
    ("file names clanak-N, clan-N",
     'm = re.match(r"(?i)^(?:art|madde|section|sec|s|para|paragraf|article|a|par|clanek|neni)?[-_]?0*(\\d{1,4})[-_]?([a-z]{0,6})$", base)',
     'm = re.match(r"(?i)^(?:(?:ugovor|naredba)[-_])?(?:art|madde|section|sec|s|para|paragraf|article|a|par|clanek|clanak|clan|neni)?[-_]?0*(\\d{1,4})[-_]?([a-z]{0,6})$", base)'),
    ("heading after a chapter heading",
     '    first = next((l for l in text.splitlines() if l.strip()), "")\n    m = HEAD.match(first) or HEAD_NORDIC.match(first)',
     '    lines = [l for l in text.splitlines() if l.strip()][:6]\n'
     '    first = lines[0] if lines else ""\n'
     '    m = HEAD.match(first) or HEAD_NORDIC.match(first)\n'
     '    for l in lines[1:]:  # a chapter or part heading may come first ("## GLAVA I", then "### Članak 5.")\n'
     '        if m or not l.lstrip().startswith("#"):\n            break\n'
     '        m = HEAD.match(l) or HEAD_NORDIC.match(l)'),
])
s = (S / "ingest/refscan.py").read_text(encoding="utf-8")
for fn in ("def one(c: dict, shard: int = 0, nshards: int = 1):\n", "def one_fileact(c: dict):\n"):
    start = s.index(fn)
    if '_LANG["v"] = ' in s[start:s.index("\n\n\n", start)]:
        skipped.append(f"ingest/refscan.py: language in {fn.split('(')[0][4:]}")
        continue
    i = s.index(fn) + len(fn)
    if s[i:].lstrip().startswith('"""'):  # keep the docstring first
        j = s.index('"""', s.index('"""', i) + 3) + 3
        j = s.index("\n", j) + 1
    else:
        j = i
    s = s[:j] + '    _LANG["v"] = (c.get("language") or "").lower()\n' + s[j:]
    done.append(f"ingest/refscan.py: language in {fn.split('(')[0][4:]}")
(S / "ingest/refscan.py").write_bytes(s.encode("utf-8"))

# ---------------------------------------------------------------- 3. currencies
patch("detectors/currency_scan.py", [
    ("Belgian franc, whole words, DM in capitals",
     'CUR = (r"(australes?|pesos? (moneda nacional|ley 18\\.188)|pesetas?|escudos?|francos?|francs? (français|fran.ais)|"\n'
     '       r"lire|liras?|marcos?|deutsche mark|reichsmark|DM\\b|sucres?|cruzeiros?|cruzados?|intis?|"',
     'CUR = (r"(australes?|pesos? (moneda nacional|ley 18\\.188)|pesetas?|escudos?|francos?\\b|francs? (français|fran.ais)|"\n'
     '       r"francs? belges?|frank(en)?\\b|BEF\\b|francs?\\b(?!\\s+(suisses?|CFA|congolais|guinéens|rwandais|burundais|comoriens|djiboutiens|pacifique))|"\n'
     '       r"lire\\b|liras?\\b|marcos?\\b|deutsche mark|reichsmark|(?-i:\\bDM\\b)|sucres?\\b|cruzeiros?|cruzados?|intis?\\b|"'),
])
# second round: "DM" right after a decimal amount ("160,000.00DM", not "N520DM" or "...G2DM" in identifiers); Albanian "lireta"
patch("detectors/currency_scan.py", [
    ("DM after a decimal amount, lireta",
     r'r"lire\b|liras?\b|marcos?\b|deutsche mark|reichsmark|(?-i:\bDM\b)|',
     r'r"lire\b|lireta\b|liras?\b|marcos?\b|deutsche mark|reichsmark|(?-i:\bDM\b)|(?-i:(?<=[.,][0-9][0-9])DM\b)|'),
])
# fourth round: Turkish lira with its endings ("liradan", "lirası", "liraya"), lost when "liras?" became a whole word
patch("detectors/currency_scan.py", [
    ("lira with Turkish endings", r'lireta\b|liras?\b|', r'lireta\b|lira\w{0,6}|'),
])
# fifth round (found by the Montenegro update): "lira" only at the start of a word, not inside "recikliranja"
patch("detectors/currency_scan.py", [
    ("lira at the start of a word", r'lireta\b|lira\w{0,6}|', r'lireta\b|\blira\w{0,6}|'),
])
# fifth round: the Turkish date-first pattern is tried only where a Turkish "until" word occurs (it is slow on long texts)
patch("ingest/textscan.py", [
    ("Turkish pattern only where it can match",
     "    for m in sorted(list(LIMIT.finditer(text)) + list(LIMIT_POST.finditer(text)), key=lambda x: x.start()):",
     "    post = list(LIMIT_POST.finditer(text)) if _POST_WORDS.search(text) else []\n"
     "    for m in sorted(list(LIMIT.finditer(text)) + post, key=lambda x: x.start()):"),
    ("Turkish 'until' words",
     "ROMAN = {r: i for i, r in enumerate(",
     "_POST_WORDS = re.compile(r\"(?i)kadar|\\bdek\\b|değin\")\nROMAN = {r: i for i, r in enumerate(",
     "_POST_WORDS = re.compile("),
])
# sixth round: earlier versions of this script inserted the two blocks above again on each run (the second insertion split
# the first one's text, so it no longer matched); keep one copy of each
_t = (S / "ingest/textscan.py").read_text(encoding="utf-8")
for _blk in ('# the corpus language decides the few month names that differ between languages; pins.json names it for a one-country\n'
             '# run, and one() sets it per corpus otherwise\n'
             'try:\n    _LANG = {"v": (lambda cs: cs[0].get("language") or "" if len(cs) == 1 else "")(pins()["corpora"])}\n'
             'except Exception:\n    _LANG = {"v": ""}\n'
             'MONTH_BY_LANG = {"listopada": {"hr": 10, "bs": 10, "sr": 10, "cnr": 10, "sh": 10}}\n',
             "_POST_WORDS = re.compile(r\"(?i)kadar|\\bdek\\b|değin\")\n"):
    while _t.count(_blk) > 1:
        _i = _t.rindex(_blk)
        _t = _t[:_i] + _t[_i + len(_blk):]
        done.append("ingest/textscan.py: removed a repeated block")
(S / "ingest/textscan.py").write_bytes(_t.encode("utf-8"))
# sixth round (found by the Czechia update): "BEF" only in capitals (not hex checksums or URLs ending in "bef"); "lira" not
# in "liraglutid"; no Swiss "frank"; Latvian "latu"/"lati" only as words (not inside "platu", "úplatu")
patch("detectors/currency_scan.py", [
    ("BEF in capitals", r'frank(en)?\b|BEF\b|',
     r'(?<!švýcarský )(?<!švýcarských )(?<!švýcarského )(?<!švýcarskému )(?<!švýcarským )(?<!Zwitserse )frank(en)?\b(?!\s+(suisses?|CHF|švýcar))|(?-i:\bBEF\b)|'),
    ("lira not in liraglutid", r'\blira\w{0,6}|', r'\blira(?!glutid)\w{0,6}|'),
    ("Latvian lats as a word", r'litų|latu|lati|', r'litų|\blat[uůi]\b|'),
])
# fifth round: the model reviews "the strongest N" per category; many flags tie on score, so ties are broken by a hash of
# the row, and the same flags are chosen whatever order the scan wrote them in
patch("triage/triage.py", [
    ("deterministic tie-break",
     "row_number() over (partition by corpus order by score desc) rn\n                         from '{p.as_posix()}')",
     "row_number() over (partition by corpus order by score desc, md5(cast(x as varchar))) rn\n                         from '{p.as_posix()}' x)"),
])
# eighth round (found by the France run): francs CFP are still the currency of New Caledonia, French Polynesia and Wallis
# and Futuna; in French "lire" is the verb "to read" ("lire 2 000" in amending formulas) and "sucre" is sugar
patch("detectors/currency_scan.py", [
    ("francs CFP are current", "francs?\\b(?!\\s+(suisses?|CFA|", "francs?\\b(?!\\s+(suisses?|CFA|CFP|"),
    ("words that are not currencies in the corpus language",
     'PAT = rf"{NUM}\\s*{CUR}|{CUR}\\s*{NUM}"\n',
     'PAT = rf"{NUM}\\s*{CUR}|{CUR}\\s*{NUM}"\n'
     '# a word that is a currency in one language is something else in another (French "lire" = to read, "sucre" = sugar)\n'
     'NOT_CURRENCY = {"fr": (r"lire\\b|", r"sucres?\\b|")}\n\n\n'
     'def pat_for(c):\n'
     '    cur = CUR\n'
     '    for w in NOT_CURRENCY.get((c.get("language") or "").lower(), ()):\n'
     '        cur = cur.replace(w, "")\n'
     '    return rf"{NUM}\\s*{cur}|{cur}\\s*{NUM}"\n',
     'def pat_for(c):'),  # round 10 edits NOT_CURRENCY, so the marker, not the text, says this is in place
    ("use the corpus's pattern",
     '"-I", "-n", "-i", "-P", PAT, c["sha"]', '"-I", "-n", "-i", "-P", pat_for(c), c["sha"]'),
])
# tenth round (found by the Algeria run): the dinar is a current currency in Algeria, Tunisia and Serbia (only the Yugoslav,
# Croatian and Bosnian dinars are gone); French "abrogations" (a noun) is not a repeal marker
patch("detectors/currency_scan.py", [
    ("current dinars",
     'NOT_CURRENCY = {"fr": (r"lire\\b|", r"sucres?\\b|")}',
     'NOT_CURRENCY = {"fr": (r"lire\\b|", r"sucres?\\b|", r"|dinara?"), "ar": (r"|dinara?",), "sr": (r"|dinara?",)}',
     '"ar": (r"|dinara?",)'),
])
patch("detectors/placeholder_ref.py", [
    ("abrogations is a noun", r"nevalid\w*|abrogat\w*|", r"nevalid\w*|abrogat(?!ions?\b)\w*|"),
])
# twelfth round (found by the Montenegro update): "brisan" had no word end, so "brisanje/brisanja/brisanjem" (deleting an
# entry from a register, personal data) and "brisan iz Registra" read as a repealed placeholder ("Brisan.", "(brisano)" still do)
patch("detectors/placeholder_ref.py", [
    ("brisan as a whole word", r'razveljavljen|brisan|', r'razveljavljen|\bbrisan[oa]?\b(?!\s+iz\b)|'),
])
# fifteenth round (found by the Croatia update): the repeal word was searched in the first 70 characters only, and the cut
# could fall inside a word ("brisano i|z", "brisan|ju"), defeating the whole-word rules: search the text, keep the start < 70
patch("detectors/placeholder_ref.py", [
    ("repeal word must start in the first 70 characters",
     "    return len(substantive) <= 400 and bool(GONE.search(substantive[:70]))",
     "    m = GONE.search(substantive)  # not substantive[:70]: the cut can fall inside a word\n"
     "    return len(substantive) <= 400 and bool(m) and m.start() < 70"),
])
print("applied:", len(done)); [print("  +", d) for d in done]
print("already there:", len(skipped))
