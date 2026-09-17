# Figure production for CCF-A-class papers

Figures are arguments, not decoration. Each figure needs a source artifact, an intended inference, and a falsifiable connection to the paper's claims.

## Choose the production route

| Figure | Preferred source | Delivery |
|---|---|---|
| Quantitative comparison | CSV/JSON + plotting code | PDF/SVG + preview PNG |
| Curves/training dynamics | raw logs + aggregation code | vector line plot + uncertainty |
| Heatmap/matrix | data array + plotting code | PDF/SVG; raster only for dense images |
| Method/architecture/workflow | structured diagram JSON | editable SVG + PDF; optional native-shape PPTX |
| Qualitative result grid | source images + deterministic layout code | PDF/PNG + manifest |
| Dataset/sample overview | documented source items + layout code | vector/raster combination |
| Conceptual teaser | structured vector first; generated art only when needed | source spec or prompt/model provenance |
| Existing raster reconstruction | specialized vectorization + manual verification | SVG/draw.io/PPTX plus original comparison |

Never use a text-to-image model for numerical axes, precise equations, exact labels, or topology that carries the scientific claim.

## Figure plan

For every figure record:

- `figure_id`, title, paper location, size target;
- one reader question and one intended inference;
- linked claim IDs and evidence/result IDs;
- figure type and why it is the right encoding;
- source data/images and transformation/generation script;
- uncertainty, sample size, units, exclusions, and missing-value policy;
- color/accessibility strategy and grayscale redundancy;
- output formats and whether each is editable;
- caption status and review status.

## Quantitative plots

Before plotting:

1. Identify the unit of replication; do not confuse samples with seeds/runs.
2. Name the estimator and uncertainty: SD, SE, CI, percentile, or posterior interval.
3. Decide how missing, censored, failed, and excluded observations appear.
4. Choose scales and baselines that do not exaggerate the effect.
5. Declare aggregation, normalization, smoothing, bins, and random seeds.

Select the main result from the predeclared paper claim and evaluation protocol, not from whichever metric has the largest observed gain. If several metrics are co-primary, show all of them or state the predeclared prioritization rule.

Implementation rules:

- Prefer position on a common scale; avoid decorative 3D and area encodings.
- Bar length normally starts at zero. Nonzero line/point limits may be valid when context is clear.
- Show raw observations when feasible; otherwise report `n` and aggregation.
- Use color plus marker, line style, hatching, direct labels, or panel separation.
- Keep method order, colors, metric names, and legend terms consistent across the paper.
- Highlight “ours” without muting baselines so aggressively that comparison becomes impossible.
- Export at the exact intended physical width. Inspect the rendered PDF, not only a notebook window.
- Preserve code, data fingerprint, environment/lock information, and output manifest.

## Architecture and workflow diagrams

Start from a semantic graph:

- nodes: exact components with stable IDs;
- edges: direction, meaning, and type (data, control, loss/gradient, feedback);
- groups: semantic regions, not decorative containers;
- edge semantics: data, control, loss, gradient, feedback, or generic;
- edge phase: training, inference, or both;
- inputs/outputs and train/inference boundaries;
- optional tensor/data shapes only when they help comprehension;
- hierarchy and reading direction.

Then choose a layout pattern:

- sequential transformation → left-to-right pipeline;
- layered system → stacked bands with short inter-layer edges;
- controller/tool system → hub-and-spoke;
- iterative algorithm → main path plus a clearly styled feedback edge;
- decision/audit process → decision diamond and explicit pass/fail branches.

Use `scripts/render_diagram_svg.py` for a small deterministic path. The versioned JSON schema supports canvas, nodes, edges, groups, title, subtitle, palette, edge semantics, and train/inference phase. Validate before rendering. Reuse stable semantic IDs for PowerPoint via `scripts/render_diagram_pptx.mjs`; create a slide-specific layout spec when the paper layout is too dense or has a different aspect ratio.

The bundled renderer outputs SVG only. Export a derived PDF/PNG with a locally available tool such as Inkscape or `rsvg-convert`, then inspect the derived file; do not claim a derived format was produced if the converter is unavailable.

The bundled renderer is intentionally simple. For sophisticated routing, nested containers, icons, equations, or existing-image reconstruction, use draw.io/Figma/Inkscape, TikZ, AutoFigure-Edit, or another dedicated tool—while keeping a source artifact and review trace.

## AI-generated illustration route

Use only when the figure's value is conceptual/visual and exact editability is not the primary requirement.

1. Prepare a content contract: required entities, relationships, prohibited additions, exact labels, reading order, visual style.
2. Retrieve a few legitimately reusable style references; do not copy distinctive copyrighted layouts.
3. Generate multiple candidates.
4. Critique semantics before aesthetics.
5. Rebuild critical labels, arrows, axes, and numbers as vector overlays or a structured diagram.
6. Record prompt, model, provider, date, input assets, and manual edits.
7. Proofread every character and compare the visual relationships with the method text.

External services may receive unpublished method details and images. Respect the project's confidentiality boundary.

## Figure 1 and teaser design

Figure 1 should answer at least two of these without reading the body:

- What problem is being solved?
- What is the key mechanism or insight?
- What changes compared with prior approaches?
- What is the most decisive result or behavior?

Avoid a collage of unrelated panels. Use a deliberate reading path, a small number of semantic groups, and a caption that states the takeaway without overstating evidence.

## Multi-panel figures

- Give each panel a distinct question and refer to it in order.
- Align axes and scales when comparison is intended.
- Use shared legends only when mappings are identical.
- Keep panel letters, typography, line weights, and padding consistent.
- Do not shrink panels until labels become unreadable; split the figure instead.
- Explain all colors, symbols, abbreviations, uncertainty, and sample sizes in the caption.

## Caption contract

A standalone caption states:

1. the takeaway or purpose;
2. what each panel shows;
3. datasets/settings/populations and method identities;
4. metrics, direction, units, and uncertainty;
5. sample size/unit of replication and statistical test where relevant;
6. abbreviations and special encodings;
7. a calibrated interpretation, not a new unsupported claim.

## Final visual audit

Inspect at manuscript column size and in grayscale:

- all text readable; no clipped labels or arrows;
- topology and edge directions correct;
- axes, units, legends, panel labels, scale bars, and uncertainty complete;
- colors distinguishable with redundant encoding;
- no inconsistent method color/order across figures;
- no rasterized text where vector output is expected;
- no unreported image manipulation or selective omission;
- caption and body interpretation match the data;
- editable source and rebuild command are present.
