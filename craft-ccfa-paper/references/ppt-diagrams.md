# Editable PowerPoint diagrams and conference talks

PowerPoint is both a delivery format and a native vector editor. For technical talks, keep text, shapes, connectors, charts, and tables editable whenever practical.

## Diagram source contract

Use the same stable semantic IDs as the paper SVG. A single coordinate spec is acceptable only when paper and slide aspect ratio/density are compatible; otherwise maintain `method.paper.json` and `method.slides.json` as layout variants derived from the same node/edge contract. The bundled PPTX renderer maps:

- rectangles, rounded rectangles, ellipses, and diamonds to native shapes;
- labels to native text;
- edges to native connectors/lines with arrowheads;
- groups to background shapes;
- title/subtitle to editable text.

Run:

```bash
node scripts/render_diagram_pptx.mjs figures/specs/method.json \
  --output figures/method.pptx
```

If `pptxgenjs` is unavailable, install it in an isolated project or use the runtime bundled with the host application. In Codex desktop, call the workspace-dependency locator and run the returned Node executable with `NODE_PATH` set to the returned Node packages directory. Do not silently rasterize the diagram as a workaround.

## PPT diagram rules

- Use a 16:9 canvas unless the venue or user specifies otherwise.
- Use a stable grid and at least 0.5-inch outer margins.
- Use connectors and arrowheads consistently; avoid lines passing through labels.
- Keep one visual grammar: same node role → same fill/stroke/typography.
- Encode edge meaning redundantly with label and line style, not color alone.
- Keep body labels large enough for projection; paper-size typography is too small for a talk.
- Use SVG or native shapes for icons where possible; preserve attribution for external assets.
- Fix the JSON/source and rebuild. Do not make untracked edits only in the final PPTX unless the user explicitly chooses a hand-edited fork.

## Turn a paper into a talk

Do not map manuscript sections one-to-one onto slides. First choose the talk's single argument and time budget.

Suggested budgets:

| Format | Duration | Typical slides | Story |
|---|---:|---:|---|
| Poster/lightning | 3–5 min | 5–7 | problem → insight → one result → takeaway |
| Spotlight | 5–8 min | 7–11 | motivation → insight → method → two results → takeaway |
| Oral | 15–20 min | 14–20 | problem → failed status quo → insight → method walkthrough → evidence → limits → takeaway |
| Invited | 30–45 min | 24–36 | broader context and deeper analysis, still one main arc |

Use talk time and venue instructions as controlling evidence; these counts are only planning defaults.

## Action-title outline

Each content slide gets:

- an action title that states the slide's takeaway;
- one dominant evidence/visual object;
- at most one supporting text block;
- a linked paper claim/evidence ID;
- speaker notes with the verbal transition;
- a time allocation.

Read all action titles alone. They should form a coherent argument (the ghost-deck test). Revise the outline before building if they do not.

## Slide content rules

- One main message per slide.
- For result slides, let the figure dominate and annotate the exact observation.
- Redesign paper figures for projection: larger fonts/lines and less density.
- Do not show a table when one highlighted comparison answers the question better.
- Preserve exact numbers, equations, and citations from source artifacts.
- Cite borrowed figures/data on the slide; include a references appendix.
- Put technical detail, extra ablations, and anticipated questions in backup slides.
- End the main narrative on the conclusion/takeaway; keep contact/QR unobtrusive.

## Technical QA

Run three distinct passes:

1. **Content:** titles, claims, numbers, citations, order, notes, placeholders.
2. **File:** PPTX opens, relationships/charts valid, fonts/media present, no corruption.
3. **Visual:** render every slide and inspect overflow, clipping, overlap, contrast, alignment, margins, figure legibility, and monotony.

Do not trust `python-pptx` or LibreOffice opening a deck as proof that PowerPoint will preserve every chart or relationship. Use a PPTX-aware validator when available and open a final candidate in PowerPoint if the deck is high stakes.

## Oral/highlight/spotlight emphasis

Selections labelled oral/highlight/spotlight usually reward work with a crisp, broadly relevant takeaway and unusually convincing evidence. The talk should therefore make visible:

- the community-level problem in the first minutes;
- the surprising insight before implementation detail;
- the one architecture/behavior diagram needed to understand the method;
- the strongest result with a fair comparison and uncertainty;
- one limitation/failure boundary that increases trust;
- a final sentence the audience can repeat.

Do not overfit the visual style to an assumed “oral look.” Clarity, evidence, and narrative compression matter more than decoration.
