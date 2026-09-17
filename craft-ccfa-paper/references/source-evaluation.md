# Upstream landscape and selection rationale

Snapshot date: **2026-08-04**. GitHub stars and repository state change over time. “CCF-A” below means suitable for preparing work aimed at CCF-A-class venues; CCF does not publish an official agent-skill recommendation list.

## Evaluation method

Candidates were found through focused web search, GitHub code/repository search, official project pages, and cross-links from established projects. Each candidate was checked against its repository metadata and primary documentation rather than directory-site descriptions.

Score tools on six questions:

1. Is it an actual reusable skill/workflow, or only a prompt/demo?
2. Does it preserve evidence, citations, and numerical truth?
3. Are figures or slides editable and reproducible?
4. Is there structural and visual QA?
5. Is the repository active and meaningfully adopted?
6. Can its ideas or code be reused under a clear license?

Stars are an adoption signal, not a quality certificate. A large collection may inherit most of its value from upstream projects.

## Primary candidates

| Project | Stars | License signal | Best contribution | Main limitation | Decision |
|---|---:|---|---|---|---|
| [Anthropic Agent Skills](https://github.com/anthropics/skills) | 166,100 | Repository has no detected root license; PPTX skill declares proprietary terms | Most mature general PPTX create/edit/validate/render workflow; native charts and strong file/visual QA | Not academic-specific; reuse restrictions | Use design and QA principles, do not copy proprietary content |
| [K-Dense scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 32,561 | MIT | Broad scientific workflow; strong evidence-first writing and reproducible plotting/export/audit | AI schematics path is raster-only and sends data to external providers | Adopt reproducible plotting and integrity rules; reject raster as formal-diagram default |
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | 14,207 | MIT | End-to-end ML research loop, adversarial review, resumable state, deterministic FigureSpec JSON→SVG, paper-to-talk | Very large and opinionated; cross-model and runtime complexity | Adopt the contract/gate/state pattern and structured vector-diagram principle |
| [Orchestra AI Research SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) | 11,377 | MIT | Wide ML lifecycle coverage, claim-driven experiments, paper/plot/talk skills | Breadth exceeds depth in some areas; several workflows assume external services | Use claim→experiment and lifecycle patterns as secondary evidence |
| [PaperBanana](https://github.com/dwzhu-pku/PaperBanana) | 6,883 | Apache-2.0 | Influential reference-driven multi-agent academic illustration; retriever/planner/stylist/visualizer/critic loop | Official README still lists statistical-plot and diagram-improvement code as TODO; output is image-generation-led | Optional conceptual illustration route only; never numerical or exact-topology default |
| [Master-cai Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | 5,780 | MIT | Concise ML/CV/NLP section patterns, reverse outlining, one-message-per-paragraph, claim-support review | Writing-focused; no complete research/figure/PPT implementation | Adopt clarity and reverse-outline checks |
| [AutoFigure-Edit](https://github.com/ResearAI/AutoFigure-Edit) | 4,057 | MIT | Method text or raster draft → editable SVG plus embedded editor; ICLR 2026 lineage | Heavy SAM/model/API stack; vector reconstruction still needs label/topology verification | Preferred specialized route when generated/raster diagrams must become editable |
| [Paper2Any](https://github.com/OpenDCAI/Paper2Any) | 2,755 | Apache-2.0 | Editable PPT, SVG, draw.io, paper-to-figure/deck/poster/rebuttal breadth | Hosted Studio is not identical to the open-source repository; broad stack and mixed reproducibility | Useful external workbench, not the skill's core dependency |
| [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana) | 2,213 | MIT | Practical extended PaperBanana implementation and slide generation | Still model/API-dependent and primarily raster-generative | Optional experimentation route |
| [K-Dense claude-scientific-writer](https://github.com/K-Dense-AI/claude-scientific-writer) | 2,167 | MIT | Coherent scientific writing/slides/citation collection | Superseded in breadth by scientific-agent-skills | Treat the newer collection as canonical |
| [luwill/research-skills](https://github.com/luwill/research-skills) | 785 | No root license detected by GitHub API; README says MIT | Scholar-slides prioritizes source fidelity, vector equations, grounded numbers, editable PPTX, parity checks | Heavy toolchain; license signal should be clarified before copying | Adopt fidelity-first principle; link rather than vendor |
| [Gabberflast academic-pptx-skill](https://github.com/Gabberflast/academic-pptx-skill) | 734 | Root MIT, but SKILL header observed as proprietary | Strong action-title/ghost-deck academic argument design | License contradiction; depends on a separate PPTX implementation | Use general argument principles only |
| [google-research/papervizagent](https://github.com/google-research/papervizagent) | 474 | Apache-2.0 | Original Google Research release behind PaperBanana/PaperVizAgent | Explicit demonstration-only/non-production disclaimer | Research reference, not production default |
| [siril9 presentation-skill](https://github.com/siril9/presentation-skill) | 35 | MIT | Source-first editable decks, deterministic renderer, geometry/readability/visual QA | Low adoption; large bespoke presentation framework | Useful implementation reference, not a required dependency |

Additional notable project: [Edit-Banana](https://github.com/BIT-DataLab/Edit-Banana) (5,450 stars) reconstructs images into editable draw.io/XML and supports OCR/formulas. GitHub reports AGPL-3.0 while the README badge/text observed during review said Apache-2.0, and the README notes the public repository trails the web service. Treat the root LICENSE as controlling and resolve the discrepancy before reuse.

[davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) (30,093 stars, MIT) is influential as a discovery/packaging layer, but much of the scientific content mirrors or distributes upstream skills. Attribute and evaluate the original skill rather than counting the aggregator as independent evidence.

## Chosen synthesis

The integrated route deliberately combines complementary strengths:

- **Paper reasoning:** local `$write-top-ml-paper` evidence-backed top-venue patterns plus claim/evidence/falsifier contracts from ARIS and Orchestra.
- **Data figures:** K-Dense's reproducibility, integrity, accessibility, vector export, and final-size inspection discipline.
- **Formal diagrams:** ARIS-style structured deterministic source, implemented here as a small standalone JSON→SVG/PPTX renderer.
- **Generated illustrations:** PaperBanana-style plan/critic loop, but only as an optional conceptual route.
- **Raster-to-editable repair:** recommend AutoFigure-Edit or draw.io reconstruction tools, with manual semantic verification.
- **Slides:** Anthropic-style technical QA, scholar-slides fidelity, and academic action-title/ghost-deck narrative checks.
- **Writing clarity:** Master-cai's reverse outline and paragraph-message discipline.

No upstream project is declared “best” in every dimension. The best CCF-A workflow is a source-first composition: evidence and numerical truth first, editable artifacts second, generative aesthetics last.

## Freshness protocol

Before recommending installation or copying code:

1. Recheck repository status, last push, issues, root license, and skill-level license.
2. Read the current README/SKILL file and known limitations.
3. Verify whether hosted features are present in the open-source repository.
4. Run a small local test on the user's actual platform.
5. Record the access date and version/commit in the paper project's provenance manifest.

