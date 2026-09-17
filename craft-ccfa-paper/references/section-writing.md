# Reviewer-facing section writing

Use [the integrated writing route](integrated-writing.md) and the matching [bundled section playbook](../modules/top-ml/references/section-playbook.md). This file remains a compact section audit guide; do not invoke a compatibility entry from here.

## Global writing contract

- One paragraph, one message. Put that message early.
- Each sentence must advance the paragraph by cause, contrast, consequence, refinement, or evidence.
- Define terms before reuse; keep notation and names stable.
- Use claim strength that matches evidence. Replace vague hype with mechanism, scope, or measured effect.
- State uncertainty, exceptions, and negative evidence where they matter.
- Prefer concrete nouns and verbs over generic “framework,” “paradigm,” “significant,” and “comprehensive.”
- Keep claims traceable to claim/evidence IDs until final cleanup.

After drafting a section, write a reverse outline: thesis → paragraph topic sentence → evidence. Revise any paragraph that does not map cleanly.

## Title

Communicate the distinctive contribution and problem/domain. Avoid claims the experiments do not establish, excessive acronyms, and broad “towards” phrasing that hides the object of study.

Audit: Can an informed reader infer what changed and where? Is every comparative/superlative word supportable?

## Abstract

A reliable compact structure:

1. problem/context and why the gap matters;
2. precise limitation of prior approaches;
3. proposed insight/method and what is new;
4. evidence setting: datasets/tasks/baselines/protocol;
5. strongest calibrated result and takeaway;
6. optional boundary/availability statement if space permits.

Write after the main paper stabilizes. Every number and major claim must appear consistently in the results.

## Introduction

Build a causal argument:

1. establish the important problem without a generic history lesson;
2. identify the concrete bottleneck or contradiction;
3. explain why existing approaches do not resolve it;
4. state the key insight;
5. preview the mechanism and decisive evidence;
6. list 2–4 contributions, each distinct and experimentally supported.

Do not use the contribution list to introduce unsupported scope. By its end, the reader should know the what, why, how, evidence, and limitation boundary.

## Related work

Organize by technical assumption, mechanism, supervision, objective, or evaluation regime—not one paragraph per paper. For each cluster:

- summarize the shared approach;
- state its relevant strength and boundary;
- position the current work on a precise axis of difference;
- avoid dismissive language and novelty claims based on incomplete search.

Verify the cited proposition in the primary source. Cite concurrent work fairly even if it weakens the novelty framing.

## Method

Use dependency order:

1. task definition, inputs/outputs, assumptions, notation;
2. overview tied to a method figure;
3. components in the order data/control flows;
4. objective/training/inference algorithm;
5. complexity, implementation choices, and boundary conditions.

Explain the motivation and technical consequence of each design choice. Do not write a chronological lab notebook or disguise a patchwork of heuristics as a single derivation. Separate fixed method definition from tuning and ablation evidence.

## Theory

State assumptions before the result. Distinguish theorem, proposition, lemma, proof sketch, intuition, and empirical observation. Explain what the result does and does not imply for the implemented method. Check symbols, quantifiers, domains, limiting cases, and dependency between results.

## Experiments

Open with the questions/claims being tested, then describe setup before interpreting outcomes. A useful subsection pattern:

1. question or linked claim;
2. setting, baselines, protocol, metric, and uncertainty;
3. observation with exact table/figure reference;
4. interpretation within evidence scope;
5. boundary, failure, or alternative explanation.

Include strong and compute-matched baselines, ablations, tuning protocol, seed/unit-of-replication information, hardware/compute where relevant, and negative results that change interpretation.

## Limitations

State concrete boundaries: data/population, task/domain, scale/compute, assumptions, robustness, evaluation coverage, deployment/ethics, and known failure modes. Explain which central claims remain valid despite each limitation. Do not use generic boilerplate or hide a fatal threat in vague language.

## Conclusion

Restate the contribution at its proven scope, synthesize the decisive evidence, and identify the most justified next step. Do not introduce new results or expand beyond the abstract/introduction claim boundary.

## Caption and table prose

Captions must stand alone and define panels, settings, metrics, uncertainty, units of replication, abbreviations, and takeaway. Table headers include units/direction. Footnotes explain protocol differences rather than burying them in the body.

## De-AI audit

Revise patterns that reduce trust:

- repeated “In this section, we…” meta-prose;
- generic grand claims and landscape openings;
- synonym churn for the same concept;
- excessive triads, em dashes, or uniform paragraph rhythm;
- unsupported adjectives (“significant,” “robust,” “comprehensive”);
- conclusions repeated verbatim across abstract, introduction, and conclusion;
- citations placed as decoration rather than supporting a proposition.

The goal is not to disguise tool use. It is to make every sentence specific, accountable, and useful.

