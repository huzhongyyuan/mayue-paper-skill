# End-to-end CCF-A paper workflow

This is an iterative research loop, not a one-way writing pipeline. Results may invalidate the narrative; review may require new analysis; a new baseline may change the claim contract.

## Workspace state

Keep these artifacts versioned with the project:

```text
paper-project/
  project_manifest.json
  claims.csv
  literature/
    search_protocol.md
    source_manifest.json
    references.bib
  experiments/
    experiment_registry.csv
    configs/
    logs/
  results/
    raw/
    processed/
  figures/
    figure_manifest.json
    specs/
    scripts/
    data/
    rendered/
  paper/
    main.tex
    layout_plan.csv
    sections/
  reviews/
  slides/
```

Initialize a minimal version with `python3 scripts/init_project.py <dir>`.

## Phase 0 — Brief and boundary

Record:

- target venue, track, article type, stage, deadline, page/appendix policy;
- current official rule URLs and access dates;
- authorship/anonymity state and permitted external services;
- one-sentence problem, one-sentence contribution, intended reader takeaway;
- budget: compute, API, time, and human evaluation;
- explicit non-goals and unresolved decisions.

Do not freeze a venue-sensitive layout from memory. Use the current official template.

## Phase 1 — Problem and literature

Create a search protocol before collecting papers:

- seed papers and terminology;
- inclusion/exclusion criteria and date range;
- multiple queries for method, task, domain, baseline, negative result, and concurrent work;
- sources used and pagination/coverage limitations;
- backward/forward citation chaining;
- deduplication key and stop condition.

Stop only when a new round mostly returns known papers or the declared budget is exhausted. State what was not searched. Verify each final citation's metadata and the exact proposition it supports.

Outputs: `search_protocol.md`, source manifest, verified BibTeX, related-work taxonomy, missing-baseline list.

## Phase 2 — Claim contract

For each major claim record:

- stable ID and exact statement;
- type: comparative, causal, generalization, descriptive, theoretical, efficiency, usability;
- scope and exclusions;
- falsifier or failure threshold;
- required experiments, analyses, figures, and citations;
- current status: proposed, supported, qualified, contradicted, unresolved.

Type-specific evidence:

- comparative → strong/recent and compute-matched baselines;
- causal → isolation or intervention/ablation, not correlation alone;
- generalization → heterogeneous datasets/settings and named boundary conditions;
- efficiency → wall-clock, memory, hardware, batch/precision, and quality trade-off;
- theoretical → explicit assumptions and proof-to-empirical boundary;
- robustness → specified perturbations, severity, and failure cases.

If evidence cannot support the scope, narrow the claim before improving prose.

## Phase 3 — Experiment design

Pre-register internally:

- research question and linked claim IDs;
- datasets/splits, leakage checks, preprocessing, licenses;
- baselines and why each is fair;
- components and ablations;
- metrics, estimator, uncertainty, units of replication, seeds;
- tuning budget and whether test data influences selection;
- compute/hardware/software versions;
- expected outcomes and what each alternative outcome means;
- stop/retry criteria and incremental save path.

Pilot cheaply, validate the pipeline, then run the final sweep. Preserve failures and negative results. Separate generation, evaluation, aggregation, and plotting code.

## Phase 4 — Results and figures

Bind every result to raw records and a transformation script. For each intended figure ask:

1. What reader question does this answer?
2. Which claim does it support or qualify?
3. What comparison and uncertainty must be visible?
4. Can the intended inference be made at final column size?
5. What failure case or boundary would change the interpretation?

Draft Figure 1 early. It should communicate the contribution or decisive evidence without depending on marketing language. Read `figure-production.md`.

## Phase 5 — Drafting

Draft in dependency order, not necessarily manuscript order:

1. claims, figure/table list, notation;
2. method and experimental protocol from implementation records;
3. results from verified outputs;
4. limitations and failure cases;
5. introduction and related work after the story is stable;
6. abstract and title last;
7. conclusion after scope is audited.

Keep claim/evidence tags in working drafts. Run a reverse outline after each section. Remove tags only after the final audit leaves a separate traceable map.

## Phase 6 — Manuscript layout

Read `manuscript-layout.md`. Build `paper/layout_plan.csv` from reader questions,
claim IDs, evidence objects, and the verified page budget. Plan float width and
order before using manual placement controls. Compile from a clean state, render
every page, and inspect thumbnail-level story rhythm plus 100%-scale typography.

Do not alter official fonts, margins, or line spacing to fit the page limit.
Record manual page breaks, float barriers, spacing changes, and template-sensitive
packages. Reconcile the page map with the final compiled PDF.

## Phase 7 — Adversarial review

Use independent passes for:

- contribution/novelty and concurrent work;
- claim scope and evidence relevance;
- experimental rigor and statistical interpretation;
- reproducibility and missing implementation detail;
- figures/tables/captions and visual truth;
- clarity, notation, paragraph flow, and page-budget trade-offs;
- anonymity, ethics, licenses, disclosures, and venue checklist.

Review the paper from rendered PDF at least once. Source-only inspection misses overflow, float order, illegible figures, and broken references.

## Phase 8 — Rebuttal and revision

Create one row per reviewer issue:

```text
reviewer | issue_id | issue | category | affected_claims | evidence_needed |
action | manuscript_location | response | status
```

Lead with the answer, then evidence, then exact change/location. Acknowledge valid limitations. Do not use new claims unsupported by the submitted or newly documented evidence.

## Phase 9 — Submission and post-acceptance

Before submission, archive:

- exact template/version and compiled PDF;
- source manifest and citation verification state;
- claim/experiment/figure manifests;
- code/data availability and anonymity decisions;
- final checksums or release tag;
- unresolved risks accepted by accountable authors.

For oral/highlight/spotlight work, build the talk around the contribution and strongest evidence. Do not merely shrink the paper section by section. Read `ppt-diagrams.md`.
