# Section-by-section writing playbook

## Contents

1. Core model
2. Title
3. Abstract
4. Introduction
5. Related work
6. Background and problem setup
7. Method
8. Theory
9. Experiments
10. Limitations and broader impact
11. Conclusion
12. Figures, tables, captions, and appendix
13. Oral/highlight/spotlight compression
14. Venue adaptation

## 1. Core model

Build the paper as a claim-evidence graph:

`problem -> precise gap -> key insight -> mechanism -> evidence -> boundary`

Make every major claim point to a figure, table, theorem, ablation, or explicit
scope statement. Remove claims with no planned evidence, or soften them to the
level the evidence supports. Keep one central thesis that a reviewer can repeat
after a quick read.

Use paragraph roles. Give each paragraph one job and put that job in its first
sentence. Prefer a progression of claim, reason, evidence, implication. Avoid
paragraphs that mix motivation, implementation detail, and evaluation.

## 2. Title

Name the object and the delta. Choose one of these shapes only when accurate:

- `<Method>: <specific capability or task>`
- `<Specific finding> for <setting>`
- `<Action/insight>: <measurable consequence>`

Aim first for 8-11 informative words, then obey the venue and field. Use a colon
only when both halves add information. Use an acronym only when it is short,
pronounceable, unambiguous, and reused throughout. Avoid unsupported adjectives
such as universal, optimal, robust, or general unless the paper defines and
tests the corresponding scope.

## 3. Abstract

Write one compact story, usually 160-220 words unless the venue says otherwise:

1. State the task and why the unresolved part matters.
2. Name the exact failure mode or missing capability in prior work.
3. State the key insight, not merely the method name.
4. Explain the mechanism in one or two sentences.
5. Give the strongest evidence with task, dataset/setting, metric, and delta.
6. Close with the supported scope or implication.

Keep the order causal: the gap must make the method feel necessary, and the
result must test the claimed mechanism. Prefer numbers over "significant
improvements." Avoid citations, equations, bullet lists, literature surveys,
and claims whose conditions appear only later.

Diagnostic: after deleting the method name, the abstract should still reveal
the paper's insight. After deleting the result numbers, the contribution should
still be identifiable—but restore the numbers before submission.

## 4. Introduction

Use a five-part funnel; merge parts when space is tight:

1. Establish the task and stakes with concrete context.
2. Define the bottleneck precisely enough to be falsifiable.
3. Group existing approaches by why they miss this bottleneck.
4. Preview the key insight, mechanism, and overview figure.
5. List contributions as claims paired with evidence.

A contribution bullet should contain three elements:

`what is introduced + what capability/insight it creates + how it is validated`

Do not list ordinary engineering steps as independent contributions. Do not
write "to the best of our knowledge" as a substitute for comparison. End the
introduction with the smallest complete set of contributions, usually two to
four.

Use the observed 700-1,471-word interquartile range only as a warning signal.
The real constraint is whether the reader reaches the insight quickly without
missing the failure mode or the evidence plan.

## 5. Related work

Organize by decision-relevant axes, not by publication year or author parade.
For each family:

1. State what the family enables.
2. Identify the assumption or tradeoff relevant to this paper.
3. Explain the remaining gap without caricaturing the cited work.
4. Position the present method on that same axis.

Use comparison dimensions that reappear in experiments: supervision, data,
compute, latency, generalization regime, controllability, guarantees, or failure
conditions. If the taxonomy never affects the method or evaluation, compress it.
Avoid claiming that "no prior work" exists when the actual distinction is a
particular setting, guarantee, or combination.

## 6. Background and problem setup

Define the contract before the machinery:

- inputs, outputs, data-generating or interaction process;
- notation and shapes only when later used;
- assumptions and their practical meaning;
- objective, constraints, and evaluation interface;
- train-time versus test-time information.

Give intuition immediately after formal definitions. In theoretical work,
separate assumptions needed for the theorem from conveniences used by the
implementation. In benchmark work, define annotation, split, leakage controls,
and metrics here or in a clearly linked data section.

## 7. Method

Start with an overview figure and a one-paragraph execution trace from input to
output. Then order components by data flow or dependency, not by the order in
which the authors discovered them.

For each component, write:

1. why the component is necessary;
2. what transformation or decision it performs;
3. the equation or algorithm;
4. the meaning of each non-obvious term;
5. how it changes training, inference, complexity, or behavior.

Distinguish the key novelty from supporting implementation. State training and
inference separately when they differ. Report computational complexity,
parameter count, latency, memory, or sample cost when efficiency is part of the
claim. End with the complete objective or algorithm so the reader can reproduce
the method without assembling it from scattered equations.

Equation prose should explain purpose and consequence, not read symbols aloud.
Use "Equation 3 enforces X, which prevents Y" rather than "Equation 3 computes
the sum of..." when the notation already shows the computation.

## 8. Theory

State the result before the proof:

- formal claim;
- assumptions;
- comparison baseline or lower bound;
- interpretation in ordinary language;
- tightness, regime, and failure conditions.

Use proof sketches in the main paper to reveal the mechanism; move routine
lemmas and algebra to the appendix. Connect every theorem to either a design
choice or an empirical test. Do not imply that a theorem proves behavior outside
its stated assumptions.

## 9. Experiments

Make each subsection answer a question:

- Does the method solve the main task under a fair protocol?
- Which component causes the gain?
- Does the claimed mechanism hold under intervention or stress?
- Where does it generalize, and where does it fail?
- What does the gain cost in compute, data, memory, or latency?

Recommended order:

1. setup, datasets, metrics, baselines, tuning budget, and uncertainty;
2. main comparison aligned to the central claim;
3. ablations tied one-to-one to method claims;
4. robustness/generalization and sensitivity;
5. efficiency and scaling;
6. qualitative evidence and failure cases.

Write a result paragraph as `observation -> magnitude -> explanation -> scope`.
Name the table cell or trend, quantify it, relate it to the mechanism, and state
where the pattern weakens. Report variability or confidence intervals when the
metric is stochastic. Avoid "clearly" and "significantly" unless visual clarity
or a statistical test justifies the word.

Use strong baselines under comparable data, compute, and tuning. If comparison
conditions differ, surface that difference in the table or prose instead of
hiding it in the appendix.

## 10. Limitations and broader impact

Write causal limitations, not ceremonial disclaimers:

- condition under which the method fails;
- reason or mechanism for the failure;
- practical consequence;
- evidence already observed;
- realistic mitigation or next experiment.

Cover technical scope, data/evaluation scope, compute/deployment cost, and
misuse or affected stakeholders when relevant. Do not claim that future work
will solve an unspecified problem. A limitation that narrows a claim increases
trust when the rest of the paper respects the same boundary.

## 11. Conclusion

Use roughly 160-400 words as a diagnostic range, not a quota. Include:

1. the problem and one-sentence insight;
2. the method or result at the right abstraction level;
3. the strongest evidence;
4. the supported scope and main limitation;
5. one concrete next direction, if useful.

Do not introduce a new method, dataset, theorem, or headline number. Avoid
repeating the abstract sentence by sentence. The conclusion should update the
reader's model of the problem, not simply announce that the paper has ended.

## 12. Figures, tables, captions, and appendix

Use `figure-playbook.md` for the per-figure construction and audit workflow.
Make the first overview figure explain the central mechanism or empirical
contrast, not decorate the page. Write captions that state the takeaway and
define symbols, colors, and protocol needed to interpret the figure without
hunting through the text.

Use table headers to expose fairness conditions such as training data, model
size, compute, supervision, and test protocol. Bold only values that are validly
comparable. Put implementation detail, complete proofs, extended ablations, and
extra qualitative examples in the appendix; keep evidence essential to the main
claim in the main paper.

## 13. Oral/highlight/spotlight compression

Do not imitate a mythical "oral style." The snapshot does not show longer
titles or abstracts for priority papers. In the sample, priority abstracts are
slightly shorter in median length than other posters. Treat this as a prompt to
compress, not as a causal rule.

Strengthen these properties:

- one memorable thesis rather than several loosely related novelties;
- a gap that is visible in a simple counterexample or overview figure;
- a mechanism that explains why the method should work;
- an evidence triangle: main performance, mechanism/ablation, and boundary;
- calibrated claims that survive a skeptical reading;
- result paragraphs that interpret, not merely enumerate tables.

Ask: "What would a reviewer repeat in one sentence during the decision
meeting?" Make that sentence accurate, specific, and supported in the abstract,
introduction, overview figure, and main table.

## 14. Venue adaptation

For CVPR/ICCV/ECCV, prioritize an early visual overview, clear qualitative
comparison, dataset/protocol fairness, and tests of geometric or visual
generalization. Do not let attractive figures replace quantitative evidence.

For ICML/NeurIPS, prioritize a precise problem statement, assumptions,
mechanistic or theoretical justification where relevant, strong empirical
controls, scaling/efficiency, and reproducibility. Do not add theorem-like
notation when the contribution is purely empirical.

Always check the current call for papers, page limit, ethics requirements,
reproducibility checklist, and track-specific rules. Venue conventions change
faster than this playbook.
