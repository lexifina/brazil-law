"""global-law replays a country repository only up to its pinned commit (or not at all), so the history detectors would miss
later changes. This replaces the corpus's rows in index/root.parquet with rows built from the repository's own history at
the pin: law = the Law: trailer if there is one, else (for a commit that restates another's text, Re-asserts:) the author of
that commit, else the commit's author (the act that made the change); in_force = the
In-force: trailer; kind = the Kind: trailer, where none (or "as-promulgated") counts as law, so drafts, case law, records,
corrections and documentation keep their own kind and the history detectors (which read kind = 'law') leave them out."""
import json, os, subprocess
import duckdb, pyarrow as pa

HERE = os.path.dirname(os.path.abspath(__file__))
pin = json.load(open(os.path.join(HERE, "pins.json"), encoding="utf-8"))["corpora"][0]
out = subprocess.run(["git", "log", "--format=%H%x1f%an", pin["sha"]], cwd=os.path.join(HERE, "sources", "corpus", pin["repo"] + ".git"),
                     capture_output=True, check=True).stdout.decode("utf-8")
pairs = [l.split("\x1f") for l in out.splitlines()]
authors = pa.table({"commit": [p[0] for p in pairs], "author": [p[1] for p in pairs]})
con = duckdb.connect()
con.register("authors", authors)
con.sql(rf"""
create table s as
select c.commit as root, '{pin["path"]}' as corpus, c.commit as corpus_commit,
       coalesce(json_extract_string(c.trailers, '$.Law[0]'), ra.author, a.author) as law,
       regexp_extract(json_extract_string(c.trailers, '$."In-force"[0]'), '\d{{4}}-\d{{2}}-\d{{2}}') as in_force,
       case when json_extract_string(c.trailers, '$.Kind[0]') is null
              or lower(json_extract_string(c.trailers, '$.Kind[0]')) in ('as-promulgated', 'as-enacted', 'enacted', 'law', 'amendment', 'original', 'decree', 'publisher') then 'law'
            else lower(json_extract_string(c.trailers, '$.Kind[0]')) end as kind,
       '{pin["name"]}: ' || c.subject as subject
from 'index/commits/{pin["repo"]}.parquet' c join authors a using (commit)
     -- a commit that restates an earlier one's text (Re-asserts: <sha>, spain-law's re-statements after same-day versions)
     -- is credited to the law of that commit, not to the repository that wrote it
     left join authors ra on ra.commit = json_extract_string(c.trailers, '$."Re-asserts"[0]')
where json_extract_string(c.trailers, '$."In-force"[0]') is not null""")
print(con.sql("select kind, count(*) from s group by 1 order by 2 desc").fetchall())
con.sql(f"""copy (select * from 'index/root.parquet' where corpus <> '{pin["path"]}' union all select * from s)
           to 'index/root.new.parquet' (format parquet, compression zstd)""")
con.close()
os.replace(os.path.join(HERE, "index", "root.new.parquet"), os.path.join(HERE, "index", "root.parquet"))
print("root.parquet: rows for", pin["path"], "replaced")
