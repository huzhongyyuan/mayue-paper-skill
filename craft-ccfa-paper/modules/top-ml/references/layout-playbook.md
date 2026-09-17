# Top-conference manuscript layout playbook

Use layout to expose the claim-evidence graph. Do not copy the page shape of an
accepted paper and do not modify the official template to imitate a visual style.

## 1. Freeze the layout contract

Verify the current official template, track, paper type, page policy, appendix
policy, reference treatment, anonymity rules, mandatory declarations, and access
date. Keep venue-sensitive choices provisional until these facts are verified.

Inventory the current section text, figures, tables, equations, algorithms,
bibliography, supplementary material, and compiled PDF. Record the build command.

## 2. Create a page-level argument map

For each planned page or page range, write:

- reader question entering the page;
- claim or answer leaving the page;
- evidence object and claim ID;
- target page fraction;
- visual width and intended placement;
- transition to the next page;
- material eligible for appendix/supplement under current rules.

Read only the page-map questions and answers. They should form the paper's argument
without requiring section prose. Revise the map before compressing typography.

## 3. Design the first page

The title, abstract, first introduction paragraphs, and optional Figure 1 should
jointly communicate:

`problem -> precise gap -> key insight -> evidence plan`

Do not spend the first page on broad field history. Use Figure 1 only when it
reduces explanation cost or reveals the decisive contrast. At thumbnail scale,
the first page should have a clear entry point and one dominant visual hierarchy.

## 4. Allocate sections by evidence burden

Allocate space after mapping claims, not by copying median section lengths.

- Related work earns space only for distinctions used by the method or evaluation.
- Method earns space for the novel mechanism, formal contract, and reproducible
  train/inference behavior.
- Experiments receive enough space to establish protocol fairness, main evidence,
  mechanism/ablation evidence, and boundaries.
- Limitations stay near affected claims as well as in any required section.
- The conclusion compresses the supported thesis; it does not rescue omitted evidence.

Use corpus word/page ranges only as diagnostics. Venue, paper type, contribution,
and claim-evidence needs control the final allocation.

## 5. Plan visual placement

For every figure/table, record the first interpretive reference, claim ID, width,
caption footprint, preferred page/column, and fallback placement.

- Use one column for local evidence readable at final column size.
- Use two columns for wide architectures, qualitative grids, or result tables whose
  comparison logic depends on a shared horizontal scale.
- Keep decisive evidence in the main paper.
- Keep a visual from opening a section whose prose has not introduced it.
- Place captions and body interpretation close enough that the reader does not need
  to search across pages.

Do not solve float pressure by shrinking labels below readable size. Redesign the
visual, split it, crop source whitespace, or change its role.

## 6. Control two-column reading order

Check the physical eye path:

- headings are followed by opening prose;
- definitions precede equations and symbols;
- full-width floats do not detach setup from consequence;
- figure/table order matches body references;
- a column does not end on a setup whose answer is distant;
- captions cannot be mistaken for adjacent-column body text;
- long equations, tables, URLs, and footnotes stay inside bounds.

Uneven page density is acceptable when it improves comprehension. Large unexplained
dead zones, stranded headings, and repeated one-line spillovers are layout defects.

## 7. Compress without weakening the paper

Apply page-economy changes in this order:

1. remove duplicated claims and setup;
2. merge paragraphs with identical rhetorical jobs;
3. move non-decisive detail under the verified appendix policy;
4. crop or redesign figures/tables;
5. shorten captions while preserving protocol, units, and caveats;
6. improve section/float order;
7. make only permitted, documented local spacing changes.

Never reduce official font sizes or margins. Never cut fairness conditions,
uncertainty, limitations, or negative evidence solely to fit the page limit.

## 8. Lay out equations and algorithms

- Break equations at semantic operators and keep notation identical across text,
  captions, figures, and appendix.
- Define symbols before or immediately after first use.
- Keep complete objectives and train/inference distinctions in the main paper when
  they are necessary to understand the method.
- Move routine proof algebra or exhaustive pseudocode only when the main argument
  remains independently judgeable.
- Never convert equations to bitmap images to make them fit.

## 9. Iterate from the rendered PDF

Compile cleanly, inspect warnings, render every page, and run two passes:

1. thumbnail pass: story rhythm, visual hierarchy, density, whitespace, and float order;
2. 100% pass: fonts, equations, labels, clipping, references, captions, and links.

Recompile after any change that can move floats or references. Review the entire PDF,
not only changed pages. Record manual page breaks, float barriers, negative spacing,
and template-sensitive package changes.

## 10. Layout review output

For a layout task, return:

1. verified venue/template constraints and access dates;
2. page-budget table and page-by-page argument map;
3. float-placement plan with first-reference locations;
4. page-numbered findings ordered by severity;
5. exact source-level remedies rather than generic aesthetic advice;
6. unresolved rule, source, or evidence dependencies;
7. a final PDF audit stating fonts, vector/raster status, page size, overflow,
   cross-references, and whether every page was visually inspected.

Do not claim venue compliance or submission readiness while blocker or major layout
findings remain.
