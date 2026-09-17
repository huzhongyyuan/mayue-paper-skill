# Review and release gates

Use these as independent passes. A single reviewer should not be trusted to catch every category, and a numerical score is not a substitute for findings with evidence spans.

## Gate 1 — Source and citation integrity

- every bibliography entry exists and metadata matches the primary source;
- every citation supports the nearby proposition, not merely the topic;
- quotes and page/section locators are exact;
- concurrent work and contrary evidence were searched;
- placeholders and citations copied only from another bibliography are unresolved failures.

## Gate 2 — Claim calibration

For each major claim:

- evidence is relevant to the claim type;
- scope matches datasets, models, tasks, regimes, and sample size;
- causal language has isolating evidence;
- generalization/robustness language has heterogeneous conditions;
- comparative language uses fair and current baselines;
- falsification criteria are actionable;
- limitations do not contradict the abstract/introduction.

## Gate 3 — Experimental rigor

- no train/validation/test leakage or post hoc test-set selection;
- tuning budget and stopping rules are stated;
- baselines receive fair implementation/tuning/compute;
- ablations isolate claimed components;
- metrics measure the asserted property;
- units of replication, seeds, uncertainty, and statistical tests are correct;
- compute/hardware/software versions enable meaningful reproduction;
- negative/failed/inconclusive outcomes are not selectively hidden.

## Gate 4 — Method/result consistency

Cross-check repeated facts and names:

- dataset sizes/splits and preprocessing;
- model/module names, equations, loss terms, hyperparameters;
- metrics, units, directions, denominators, decimal precision;
- numbers in abstract, text, tables, captions, appendix, and slides;
- train versus inference behavior;
- claimed released artifacts versus actual repository state.

## Gate 5 — Figure and table integrity

- source data/code/spec and rebuild commands exist;
- axes, baselines, scales, uncertainty, legends, and sample sizes are honest;
- method order/color/terminology are consistent;
- diagrams encode the actual topology and distinguish data/control/feedback;
- every label is readable at final size;
- raster/generated assets have provenance and manual semantic review;
- captions explain panels and do not add unsupported claims.

## Gate 6 — Writing and reviewer comprehension

- one-sentence contribution is stable across title/abstract/introduction/conclusion;
- reverse outline has no orphan paragraphs or duplicated jobs;
- each experiment explicitly answers a question;
- notation and terminology are stable;
- novelty is distinguished from implementation detail;
- important caveats appear where claims are made, not only in limitations;
- the first page and Figure 1 communicate the story without hype.

## Gate 7 — Full-manuscript layout

- the page map matches the compiled PDF and verified page budget;
- first-page hierarchy communicates problem, insight, and evidence plan;
- section openings, column breaks, float order, and cross-references preserve the reading path;
- no stranded headings, one-line spillovers, large unexplained gaps, clipped content, or unreadable scaled visuals;
- equations, tables, captions, URLs, footnotes, and algorithms remain inside template bounds;
- every page was inspected at thumbnail scale and at final reading size;
- manual breaks, float barriers, spacing changes, and template-sensitive packages are documented;
- official fonts, margins, and line spacing were not altered to solve page pressure.

## Gate 8 — Venue and submission

Verify against current official instructions:

- template/version, page/appendix/supplement rules;
- anonymity, acknowledgments, links, and supplementary metadata;
- ethics, broader impacts, limitations, checklists, disclosures;
- citation/reference treatment and reproducibility requirements;
- PDF fonts, file size, accessibility, margins, and broken references;
- artifact/code/data licenses and double-blind repository state.

Render the final PDF and inspect every page.

## Gate 9 — Rebuttal

- every reviewer issue has an answer and exact change/location;
- responses distinguish clarification, correction, new evidence, and disagreement;
- new experiments have documented protocol/results and do not contradict the paper;
- promises are feasible and time-bounded;
- tone is factual and respectful; no reviewer speculation;
- word limit and confidentiality policy are respected.

## Gate 10 — Talk/PPT

- action titles alone tell the argument;
- slide numbers match paper source artifacts;
- figures are projection-readable and not misleadingly cropped;
- borrowed material is cited in-slide;
- PPTX passes content, structural, and rendered visual QA;
- backup slides cover likely questions, baselines, ablations, limitations, and setup.

## Severity and disposition

Use:

- **blocker:** truth, leakage, fabrication, corrupt output, anonymity, or venue-rule failure;
- **major:** central claim unsupported, unfair baseline, missing decisive experiment, unreadable core figure;
- **minor:** local ambiguity, consistency, polish, or incomplete secondary detail;
- **suggestion:** optional improvement not required for defensibility.

Every finding should name the affected claim/artifact, quote or locate the evidence, explain why it matters, and propose a concrete remedy. Do not mark the project ready while blockers or unresolved major findings remain.
