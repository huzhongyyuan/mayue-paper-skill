# Conference corpus tools

All commands here assume the working directory is the unified `craft-ccfa-paper` root. When working inside a paper repository, resolve these paths against the installed skill rather than changing or overwriting the paper's files. Read [coverage](merged-evidence.md) before reporting counts. Existing scripts inside `modules/top-ml/` retain their original sibling-import layout.

## Query the stored metadata

```bash
python3 modules/top-ml/scripts/query_corpus.py \
  --corpus modules/top-ml/references/corpus/papers.jsonl.gz \
  --conference CVPR --presentation oral --query 'diffusion|generation' --limit 12
```

Use records for discovery. Read the primary paper before citing its technical claim. Do not load the complete compressed metadata into model context.

## Refresh only the evidence needed

For a requested updated metadata snapshot:

```bash
python3 modules/top-ml/scripts/collect_corpus.py --output-dir /tmp/top-ml-corpus --refresh
```

Inspect the generated manifest before reporting current coverage. For newly public venue-years use `modules/top-ml/references/corpus/source-config.example.json`, replace placeholders with verified official URLs, and pass `--source-config /path/to/sources.json`. Do not invent endpoints or interpret an empty response as zero accepted papers.

For a requested or necessary proportional full-text sample, with `pypdf` and `curl` available:

```bash
python3 modules/top-ml/scripts/analyze_corpus.py \
  --corpus /tmp/top-ml-corpus/papers.jsonl \
  --output-dir /tmp/top-ml-analysis \
  --priority-per-stratum 12 --poster-per-venue 8 --jobs 4
```

## Resumable exhaustive pass

Use when the user's scope requests an exhaustive pass, not merely an ordinary writing task or skill merge. Install the dependencies from `modules/top-ml/scripts/requirements-full-corpus.txt` into an appropriate isolated environment. The analyzer streams PDFs through temporary files and stores extracted features in SQLite; omit `--keep-pdfs` unless retaining the large PDF archive is explicitly requested.

```bash
python3 modules/top-ml/scripts/analyze_full_corpus.py \
  --corpus modules/top-ml/references/corpus/papers.jsonl.gz \
  --database /tmp/top-ml-full/full.sqlite \
  --temp-dir /tmp/top-ml-full/tmp \
  --progress-json /tmp/top-ml-full/progress.json \
  --jobs 3
python3 modules/top-ml/scripts/report_full_corpus.py \
  --database /tmp/top-ml-full/full.sqlite \
  --output-dir /tmp/top-ml-full/report
```

The same analyzer command resumes the database. Blocked publishers use per-host circuit breakers. Retry blocked sources only when the cause has changed; use `--retry-errors` for transient failures. Report `done`, `blocked`, `error`, `not_found`, `no_pdf`, `pending`, and unavailable venue-years separately. Keep reports `in_progress` while analyzable records remain.

Exported `full-corpus-report.md`, `summary.json`, `sections.jsonl.gz` and `figures.jsonl.gz` preserve aggregate and record-level features. A partially completed report does not turn the original 55-paper sample into an exhaustive observation. For independent databases from an earlier task, inspect their reports and status rather than inferring completion from these installed scripts.
