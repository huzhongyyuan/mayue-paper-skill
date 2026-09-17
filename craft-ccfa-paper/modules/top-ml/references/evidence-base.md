# Evidence base and coverage

## Scope

Treat every number below as a snapshot dated 2026-08-04, not a timeless fact.
The bundled corpus contains 25,421 records collected from official proceedings
or official conference schedules. "All" means all records exposed by those
sources, not every submitted paper and not an exhaustive local PDF archive.

| Venue-year | Records | Poster | Spotlight | Highlight | Oral | Source state |
|---|---:|---:|---:|---:|---:|---|
| CVPR 2025 | 2,871 | 2,777 | 0 | 0 | 94 | CVF proceedings + official virtual program |
| CVPR 2026 | 4,068 | 3,358 | 0 | 569 | 141 | CVF proceedings + official virtual program |
| ICCV 2025 | 2,701 | 2,637 | 0 | 0 | 64 | CVF proceedings + official virtual program |
| NeurIPS 2025 | 5,823 | 5,015 | 721 | 0 | 87 | official proceedings + virtual program |
| ICML 2025 | 3,330 | 2,988 | 223 | 0 | 119 | PMLR v267 + official virtual program |
| ICML 2026 | 6,628 | 6,054 | 421 | 0 | 153 | official schedule + virtual program |

Totals include 658 oral, 569 highlight, 1,365 spotlight, and 22,829 other
poster records. Some official event pages contain title variants or special
tracks that do not match the main paper list; the manifest records both listed
and matched counts.

## Years that must not be hallucinated

- CVPR 2027, ICCV 2027, NeurIPS 2026/2027, and ICML 2027 were future events at
  the snapshot date.
- ICCV has no 2026 edition; ECCV has no 2025 or 2027 edition.
- ECCV 2026 had no public official proceedings/accepted-paper list at the
  snapshot date. Re-run the collector after publication.

## Official sources

- CVPR/ICCV paper lists: `https://openaccess.thecvf.com/`
- CVPR/ICCV presentation labels: the official `*.thecvf.com/virtual/` programs
- NeurIPS papers: `https://papers.nips.cc/paper_files/paper/2025`
- NeurIPS labels: `https://neurips.cc/virtual/2025/`
- ICML 2025: `https://proceedings.mlr.press/v267/`
- ICML labels and ICML 2026: `https://icml.cc/virtual/` and the official schedule

Read `corpus/manifest.json` for exact URLs and parser match counts. Query
`corpus/papers.jsonl.gz` through `scripts/query_corpus.py`; never load the whole
file into model context.

## Quantitative signals

Across all 25,421 titles:

- Median title length is 9 words; the interquartile range is 8-11.
- 59.9% use a colon. This is a convention, not evidence that colons improve
  acceptance.
- 2.0% are questions. Priority papers use questions more often than other
  posters (3.0% vs. 1.9%), but questions remain rare.
- 40.1% begin with an acronym followed by a colon. Priority papers do this less
  often than other posters (37.5% vs. 40.4%); do not invent an acronym for
  prestige.
- Oral titles have median 9 words; highlight titles have median 10. Selection
  does not correlate with longer titles in this snapshot.

The full-text feature pass used a stable stratified sample of 55 accessible
PDFs: 25 oral, 5 highlight, 10 spotlight, and 15 other posters. ICML 2026 PDFs
were blocked by OpenReview anti-bot checks, so ICML 2026 contributes metadata
and presentation labels but not PDF-derived section statistics.

A separate resumable exhaustive pass can be run with
`scripts/analyze_full_corpus.py`. It streams each accessible PDF through SQLite,
stores per-section writing features plus every detected figure/table caption,
layout, and visual-region features, then deletes the PDF. Its report must remain
labelled `in_progress` while pending or processing records exist. Until a
completed `full-corpus-report.md` is available, the 55-paper stratified sample
below—not partial exhaustive-pass counts—is the stable evidence snapshot.

Observed section word-count medians and interquartile ranges are diagnostics,
not venue limits:

| Section | PDFs detected | Median words | IQR |
|---|---:|---:|---:|
| Abstract | 54 | 188 | 156-220 |
| Introduction | 55 | 893 | 700-1,471 |
| Related work | 31 | 666 | 447-1,421 |
| Method | 33 | 2,199 | 682-3,531 |
| Experiments | 29 | 1,408 | 1,053-1,785 |
| Limitations | 14 | 235 | 175-343 |
| Conclusion | 43 | 224 | 162-400 |

PDF extraction from two-column layouts is noisy. Prefer medians and broad
ranges; never cite these values as causal acceptance factors.

## Reproduction

Refresh metadata:

```bash
python3 scripts/collect_corpus.py --output-dir /tmp/top-ml-corpus --refresh
```

For newly published venue-years, provide official URLs through
`corpus/source-config.example.json` and `--source-config`; update the manifest
status override instead of editing a future year into a fake zero count.

Analyze a stratified sample (requires `pypdf` and `curl`):

```bash
python3 scripts/analyze_corpus.py \
  --corpus /tmp/top-ml-corpus/papers.jsonl \
  --output-dir /tmp/top-ml-analysis \
  --priority-per-stratum 12 --poster-per-venue 8 --jobs 4
```

Use a very large per-stratum limit only when the user explicitly requests an
exhaustive PDF pass and accepts the bandwidth, runtime, publisher load, and
anti-bot constraints. Never describe a stratified sample as exhaustive.

For an exhaustive streaming pass (requires PyMuPDF, NumPy, and `curl`):

```bash
python3 scripts/analyze_full_corpus.py \
  --corpus references/corpus/papers.jsonl.gz \
  --database /tmp/top-ml-full/full.sqlite \
  --temp-dir /tmp/top-ml-full/tmp \
  --progress-json /tmp/top-ml-full/progress.json \
  --jobs 3
python3 scripts/report_full_corpus.py \
  --database /tmp/top-ml-full/full.sqlite \
  --output-dir /tmp/top-ml-full/report
```

Report `done`, `blocked`, `error`, `not_found`, `no_pdf`, `pending`, and future
venue-years separately. An unavailable year is not a zero-paper observation.
