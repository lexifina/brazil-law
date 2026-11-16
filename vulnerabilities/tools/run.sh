#!/usr/bin/env bash
# One-country run of global-law's vulnerability detectors (no sync: pins.json names one repository and its commit).
#   bash run.sh [shards]     shards = processes for the text and reference scans (default 6)
cd "$(dirname "$0")"
export LE_WORKERS=${LE_WORKERS:-6} LE_GREP_THREADS=${LE_GREP_THREADS:-6} PYTHONIOENCODING=utf-8 LE_PRIORITY=${LE_PRIORITY:-idle}   # redo.py passes its own
P="C:/Python314/python.exe -X utf8"
N=${1:-6}
R=$($P -c "import json;print(json.load(open('pins.json'))['corpora'][0]['repo'])")
set -x
$P ingest/extract.py && $P ingest/trailers.py
$P map_moved.py   # repositories that moved their act folders (data/paths.json): one folder per act through its history
$P add_root.py
$P ingest/textscan.py --shards $R:$N
$P ingest/refscan.py --shards $R:$N
# ref_detectors reads refs/*.parquet and refs_fileact/*.parquet; the one-file-per-act scan does not apply here, so an empty table
mkdir -p index/refs_fileact
$P -c "import duckdb,glob; f=sorted(glob.glob('index/refs/*.parquet'))[0].replace(chr(92),'/'); duckdb.sql(f\"copy (select * from '{f}' limit 0) to 'index/refs_fileact/_none.parquet' (format parquet)\")"
$P ingest/headings.py
$P detectors/trailer_only.py run; $P detectors/rank.py run; $P detectors/text_detectors.py run
$P detectors/ref_detectors.py run; $P detectors/placeholder_ref.py run; $P detectors/late_extension.py run
$P detectors/dead_fine.py run; $P detectors/notes_scan.py run
$P detectors/currency_scan.py run; $P detectors/dup_labels.py run
echo DONE
