# Drafting and review rubric

## Claim-evidence ledger

Before drafting, create one row per major claim:

| Claim | Novel relative to | Evidence | Boundary | Paper location |
|---|---|---|---|---|
| Specific, falsifiable sentence | Closest work/assumption | Table, figure, theorem, ablation | Where it may not hold | Abstract/intro/method/results |

Delete, soften, or test any claim with an empty evidence or boundary cell.

## Section brief

For each section, record:

- reader question entering the section;
- one-sentence answer leaving the section;
- required evidence or artifact;
- facts that belong elsewhere;
- maximum space allowed by the page budget.

## Paragraph test

Score every paragraph 0 or 1 on each item:

- The first sentence states the paragraph's job.
- Every sentence advances that job.
- Terms are defined before use.
- Claims have evidence or citations.
- The final sentence provides implication or transition.

Rewrite paragraphs scoring below 4/5.

## Submission-level audit

Rate each dimension from 1 to 5 and explain scores below 4:

1. Thesis: Can a reviewer repeat the contribution in one accurate sentence?
2. Gap: Is the failure mode specific and fairly compared to prior work?
3. Mechanism: Does the paper explain why the method should work?
4. Evidence: Does each major claim have an aligned experiment or theorem?
5. Fairness: Are data, compute, tuning, and protocol comparisons visible?
6. Robustness: Are sensitivity, uncertainty, generalization, and failure cases tested?
7. Reproducibility: Could an informed reader reconstruct training and inference?
8. Calibration: Do wording and scope match the evidence?
9. Compression: Is every paragraph necessary to the claim-evidence chain?
10. Layout: Does the rendered PDF preserve the claim-evidence reading path, float order, final-size legibility, and official template?
11. Venue fit: Does the draft obey current track rules and reviewer expectations?

Do not report only a total score. Return the three highest-risk issues in this
format:

`risk -> why a reviewer may object -> exact revision -> evidence still needed`

## Rewrite protocol

When revising user text:

1. Preserve technical meaning, notation, numbers, and citations.
2. Flag unsupported additions instead of inventing evidence.
   Treat inferred prior-work weaknesses and causal explanations as unsupported
   additions unless the user supplies analysis, citations, or an experiment.
3. Produce the revised passage.
4. List material changes by rhetorical function, not copy-edit trivia.
5. List missing facts as explicit placeholders such as `[DATASET]`, `[METRIC]`,
   `[DELTA]`, or `[LIMITATION]`.
6. Run the claim-evidence and paragraph tests.

Never fabricate experiments, citations, baselines, novelty, acceptance status,
or presentation labels.
