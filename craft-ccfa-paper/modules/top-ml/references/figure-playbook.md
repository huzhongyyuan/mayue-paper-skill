# Scientific figure construction playbook

## Contents

1. Decide the figure's claim
2. Figure 1 and teasers
3. Architecture and pipeline diagrams
4. Qualitative comparison grids
5. Quantitative plots
6. Ablation and sensitivity figures
7. Dataset and benchmark figures
8. Representation visualizations
9. Failure-case figures
10. Tables
11. Captions and cross-references
12. Visual system
13. Figure audit

## 1. Decide the figure's claim

Write one sentence before drawing: `This figure demonstrates [claim] under
[setting] by showing [evidence].` If the sentence needs "and" more than once,
split the figure. Map every main-paper figure to a claim in the claim-evidence
ledger. Remove decorative figures with no reviewer decision value.

Choose the evidence form before the software:

- process or dependency -> pipeline/architecture diagram;
- perceptual difference -> controlled qualitative grid;
- relationship or trend -> plot with uncertainty;
- component causality -> ablation/sensitivity figure;
- data scope -> stratified dataset examples;
- boundary -> failure-case figure.

## 2. Figure 1 and teasers

Make Figure 1 answer three questions within seconds: what enters, what changes,
and what improves. Use either:

- problem contrast: prior behavior versus desired behavior;
- end-to-end promise: input, compact mechanism, output;
- surprising finding: one controlled comparison or trend.

Place the central insight visually, not in a paragraph inside the figure. Use a
short takeaway label and consistent arrows. Avoid a dense architecture when the
reader has not yet learned the task. Ensure the caption states the claim and the
comparison conditions.

## 3. Architecture and pipeline diagrams

Lay out the execution order left-to-right or top-to-bottom. Use lanes for data,
model components, losses, and outputs. Distinguish training-only paths from
inference paths with line style or labeled background regions, not color alone.

Draw in this order:

1. input/output objects and their shapes or modalities;
2. major stages and data flow;
3. the novel component, visually emphasized once;
4. supervision, losses, or feedback paths;
5. train/test differences;
6. a legend for colors, dashed lines, frozen modules, and repeated blocks.

Keep repeated components visually identical. Label transformations with purpose
(`frequency alignment`) instead of implementation-only names (`Block C`). Put
tensor shapes only at ambiguity points. Avoid crossing arrows; if feedback is
necessary, route it along the edge of the figure.

## 4. Qualitative comparison grids

Fix rows and columns before selecting examples. A common structure is columns
for cases and rows for input, ground truth, baselines, ours, and error map. Use
the same crop, scale, color mapping, post-processing, and display range for all
methods.

Include examples that test the stated mechanism, not only visually attractive
ones. Add zoom boxes only when the crop exposes a named failure mode. Mark the
same region across methods. Include at least one representative weakness when
the claim concerns robustness or generalization.

State selection policy, dataset/split, and display normalization in the
caption. Never use an unannounced cherry-picked subset as general evidence.

## 5. Quantitative plots

Use one scientific question per panel. Name axes with units; state whether
higher or lower is better. Show uncertainty or repeated-run variation when the
measurement is stochastic. Expose data, compute, model size, or latency on an
axis when efficiency or scaling is part of the claim.

Prefer direct labels or a short legend near the data. Use color plus marker or
line style so the plot survives grayscale and color-vision differences. Keep
axis ranges honest; label broken or truncated axes. Annotate only the points
needed for the takeaway.

## 6. Ablation and sensitivity figures

Map each panel to one method claim. Change one factor at a time unless the panel
explicitly studies interaction. Put the reference configuration in every panel
and keep metrics and scales aligned.

Use curves for continuous hyperparameters, grouped marks for discrete
components, and small multiples for interactions. Show the operating point used
in the main result. Explain non-monotonic behavior rather than selecting only
the favorable range.

## 7. Dataset and benchmark figures

Show scope and stratification: domains, classes, conditions, annotation types,
or long-tail structure. State the sampling rule. Use counts or proportions with
denominators and reveal missing or underrepresented groups relevant to the
claims.

For example grids, avoid duplicated near-neighbors. Preserve privacy and usage
rights. Separate illustrative samples from quantitative distribution evidence.

## 8. Representation visualizations

Use a shared color scale, normalization, projection method, and reference frame.
For attention maps or heatmaps, show the original input and identify the queried
token, region, or layer. For embedding projections, report the projection
algorithm, seed, sample size, and whether labels influenced the projection.

Do not use a visually separated cluster as proof of downstream performance.
Pair representation plots with a quantitative test of the claimed property.

## 9. Failure-case figures

Use the same layout and display settings as successful examples. Group failures
by mechanism or condition, not by anecdote. For each group, state the trigger,
observed error, likely cause, and practical consequence. Distinguish model
failure from annotation ambiguity and metric failure.

## 10. Tables

Give each table one reviewer decision: main performance, fairness/efficiency,
component causality, robustness, or data scope. Put protocol-defining columns
before metrics: training data, supervision, backbone, input size, compute,
evaluation split, and any test-time adaptation that affects comparability.

Group rows by genuinely comparable regimes. State units and `higher/lower is
better` in the header. Report mean and variation when runs are stochastic;
define the number of seeds and aggregation rule. Use bold only for the best
value inside a valid comparison group, and distinguish reproduced from cited
numbers. Do not hide a different data or tuning budget in a footnote while
claiming a fair win.

For ablation tables, begin with the matched base system, change one factor per
row, and include the full configuration. If components interact, add the
minimal factorial rows needed to expose the interaction rather than pretending
that sequential additions identify independent effects. Include cost columns
when a component changes parameters, FLOPs, memory, data, steps, or latency.

## 11. Captions and cross-references

Write captions as miniature evidence arguments:

1. claim or takeaway;
2. setting and protocol;
3. panel definitions;
4. legend, metric, units, and direction;
5. boundary or caveat when necessary.

Avoid captions that only say "Overview" or "Results." Define every panel label,
color, arrow, symbol, and abbreviation needed for standalone reading. In the
body, reference the figure for an interpretive claim, not merely "Figure 3
shows our method."

## 12. Visual system

Use a restrained, consistent palette across all figures. Reserve one accent
color for the proposed method and reuse baseline colors. Use a venue-legible
font size after final-page scaling. Prefer vector text, lines, and plots; use
raster only for images or dense fields. Export at final aspect ratio and inspect
the compiled PDF at 100% zoom.

Do not encode meaning by color alone. Keep line weights, arrowheads, corner
radii, capitalization, and stage colors consistent. Align objects to a grid and
use whitespace to express grouping before adding boxes.

## 13. Figure audit

For every figure, answer yes/no:

- Does it test or explain a named claim?
- Can the takeaway be understood without searching the body text?
- Are protocol and comparison conditions fair and visible?
- Are panels, axes, units, legends, and uncertainty defined?
- Is the proposed method visually emphasized without distorting evidence?
- Does the figure remain readable at final print size and in grayscale?
- Are failure cases and scope shown where the claim requires them?
- Is the caption an interpretation rather than a filename?

When a full-corpus SQLite database is available, run
`scripts/report_full_corpus.py` and use its medians only as diagnostics. Never
force a figure into the median aspect ratio or colorfulness of accepted papers.
