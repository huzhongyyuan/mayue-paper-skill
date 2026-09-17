# Full-manuscript layout and pagination

Treat layout as part of the scientific argument. The goal is not to make every
page equally dense; it is to make the claim-evidence path easy to follow while
preserving the current official template.

## Layout contract

Before changing LaTeX, record:

- venue, track, article type, template/version, rules URL, and access date;
- main-text, appendix, references, and supplementary page policies;
- one- or two-column format and whether anonymous supplementary files are allowed;
- compiled PDF, source tree, bibliography, figure/table inventory, and build command;
- target page budget and current over/under budget;
- mandatory sections, declarations, checklists, and anonymity constraints.

Do not change margins, base font, line spacing, heading sizes, caption style, or
template internals unless the official instructions explicitly permit it. Never
use accepted-paper PDFs as authority for current venue rules.

## Required layout artifacts

Produce and maintain:

1. `paper/layout_plan.csv`: page/section budget, reader question, linked claims,
   planned visuals, entry state, exit state, and status;
2. a float plan: figure/table ID, width, first textual reference, preferred
   placement, dependencies, and fallback placement;
3. a rendered-PDF audit with page-numbered findings;
4. a short intervention log for manual float barriers, page breaks, spacing
   changes, and template-sensitive packages.

The page map is a plan, not a promise. Update it whenever experiments, claims,
or venue rules change.

## Build a paper-wide page map

For each section or page range, specify:

- reader question on entry;
- one-sentence answer on exit;
- claim IDs and decisive evidence;
- target space and maximum acceptable space;
- required figure, table, equation, or algorithm;
- transition to the next section;
- material that can move to the appendix or supplementary under current rules.

Use page fractions as diagnostic starting points rather than fixed rules. A
typical empirical paper gives the largest share to method plus experiments, but
the evidence burden controls the allocation. Theory-heavy, dataset, benchmark,
systems, and application papers require different maps.

## First-page layout

The first page should establish a complete minimal argument:

- the title names the scientific object and supported delta;
- the abstract is visually compact and contains the strongest evidence;
- the introduction reaches the precise bottleneck and key insight quickly;
- Figure 1 appears early only when it materially accelerates understanding;
- author, affiliation, anonymity, teaser, and footnote treatment follow the
  official template exactly.

Audit the first page at print size and as a thumbnail. A reviewer should recover
the problem, insight, and evidence plan without reading later pages.

## Section and page rhythm

- Start a section where the reader's question changes, not merely where a page
  has space.
- Avoid a heading stranded at the bottom of a column and avoid one-line carryover
  paragraphs when a nearby edit can resolve them.
- Keep definitions before use and keep result interpretation near the referenced
  table or figure.
- Let dense technical pages alternate with visually explanatory pages when the
  argument supports it; do not force uniform density.
- Do not create whitespace by moving essential evidence away from its claim.
- Balance the final main-text page only after content and references are stable.

## Figures and tables in the page plan

Choose width by the reading task:

- single-column: one local comparison, compact plot, small ablation, or simple
  diagram readable at `\columnwidth`;
- double-column: architecture, wide qualitative grid, large result table, or a
  comparison needing a shared horizontal scale;
- appendix/supplement: protocol-complete detail that is not required to judge the
  central main-paper claim.

For every float:

- place the first interpretive reference before or near its appearance;
- reserve caption height in the page plan, not only artwork height;
- crop genuine external whitespace in the source asset;
- inspect labels after final LaTeX scaling;
- keep panel order, caption order, and body references identical;
- prevent a float from visually opening the wrong section;
- avoid `[H]`, repeated `\vspace`, or global float-parameter changes as first-line
  fixes. Use them only when allowed, necessary, and documented.

Prefer changing the source figure's aspect ratio or splitting an overloaded
visual over shrinking labels below readable size.

## Equations, algorithms, and code

- Break long equations at semantic operators and align on the relation or main
  additive structure.
- Keep equation numbers, punctuation, and definitions consistent with the prose.
- Do not scale equations as images to make them fit.
- Place proof sketches and algorithms where their outputs become necessary.
- Move routine algebra, exhaustive pseudocode, or complete proofs only when the
  main-paper argument remains independently checkable.
- Check algorithm and code-listing packages against the official template.

## Two-column integrity

Inspect both the logical reading order and the physical eye path:

- column 1 should not end with a setup whose result is hidden far down column 2;
- a full-width float should not separate a heading from its opening paragraph;
- captions should not be mistaken for body text from the adjacent column;
- table rules, equation tags, and long URLs must stay inside column bounds;
- footnotes, author blocks, and acknowledgments must not collide with floats;
- references should not contain isolated URLs, broken identifiers, or excessive
  whitespace caused by unbreakable strings.

## Page-economy decision order

When over budget, apply fixes in this order:

1. remove duplicated claims, setup, and interpretation;
2. merge paragraphs with the same job;
3. move non-decisive detail to appendix/supplement if allowed;
4. redesign or crop figures and tables;
5. shorten captions without deleting protocol or caveats;
6. improve float order and section boundaries;
7. make local, documented spacing changes permitted by the template.

Never solve page pressure by reducing the template font, margins, or line spacing.
Never hide a fairness condition, uncertainty definition, limitation, or decisive
negative result merely to save space.

## LaTeX iteration loop

1. Compile from a clean state with the documented build command.
2. Treat missing references/citations and overfull boxes as unresolved findings.
3. Render every page to images or contact sheets.
4. Review first at thumbnail scale for story rhythm and whitespace, then at 100%
   for typography, clipping, and legibility.
5. Change the smallest source-level cause: prose, float dimensions, caption,
   section order, or asset crop.
6. Recompile at least twice when references or floats may move.
7. Record any manual page break, float barrier, negative spacing, or package-level
   override and verify that it survives a clean build.

## Rendered-PDF page audit

Review every page and record exact page/column locations for:

- template page size, margins, headers, footers, and anonymity;
- title/author block, abstract, section hierarchy, and contribution visibility;
- orphan/widow lines, stranded headings, bad column breaks, and large dead zones;
- float order, first reference, caption completeness, and cross-reference targets;
- clipped or rasterized text, tiny labels, inconsistent fonts, and weak contrast;
- equations outside columns, broken tables, missing units, and unreadable footnotes;
- references, URLs, appendix labels, supplementary links, and final-page balance;
- embedded fonts, file size, broken hyperlinks, and PDF warnings required by the
  venue's current checker.

Classify truth, anonymity, template, corrupt-PDF, and unreadable-core-evidence
failures as blockers. Treat major float-order or page-flow failures as major.

## Appendix and supplementary layout

- Keep numbering and cross-references unambiguous across main and supplementary
  material.
- Put reproduction-critical details in a predictable order: setup, implementation,
  extended results, proofs, additional qualitative evidence, and failure cases.
- Give every supplementary table/figure a standalone caption and a main-paper
  pointer when permitted.
- Do not use supplementary material to repair a main-paper claim that lacks enough
  evidence to be judged under the venue's review rules.

## Completion gate

Do not call the layout ready until:

- the official template and page policy are verified with access dates;
- the layout plan matches the compiled PDF;
- every main claim is near its decisive evidence;
- all pages have been visually inspected at final size;
- fonts are embedded and core text/equations/plots remain vector where expected;
- no undocumented template or spacing override remains;
- the source rebuilds to the delivered PDF from a clean state.
