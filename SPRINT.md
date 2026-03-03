# Agentic Evaluation System — Lecture Iteration

**Status**: executing

## Goal

Iterate on the "Building an Agentic Evaluation System" lecture
(`docs/source/evaluate-evidence/02-agentic-evaluation-system/lecture.ipynb`).

## Scope

**In scope**:
- Content and structure of the agentic evaluation lecture

**Out of scope**:
- Other evaluate-evidence lectures (01, 03)
- Changes to the Impact Engine codebase

## Observations

### 1. Stage name formatting

The lecture opening uses all-caps `MEASURE` and `ALLOCATE` to reference pipeline
stages. The course convention (see `overview/index.md` and section index pages) is
bold-italic title case: ***Measure Impact***, ***Evaluate Evidence***,
***Allocate Resources***.

### 2. Impact Engine naming convention

The lecture opening uses backtick-quoted `impact-engine-evaluate` in prose. The
course convention (see `measure-impact/index.md` and measure-impact notebooks) is
bold on first mention with a hyperlink — [**Impact Engine**](url) — then plain
**Impact Engine** on subsequent mentions. Package names in backticks are reserved
for code contexts (imports, config references).

### 3. Uneven depth across the four principles

The lecture opening names four principles — failure modes, defensibility pillars,
escalation, and the Assess vs. Improve discipline — but they receive asymmetric
treatment. Escalation (Judge → Debate) and Assess vs. Improve each get multiple
subsections with tables and worked patterns. The Four Pillars get one paragraph
plus an SVG. The LLM-as-Aggregator role gets one paragraph. The lecture needs
more symmetry across these four concepts.

### 4. Section 1 heading: "Trustworthy Automated Assessment" → "Defensible Confidence at Scale"

The current heading "Principles for Trustworthy Automated Assessment" is generic.
"Defensible Confidence at Scale" is specific to the lecture's argument: every
score must be defensible (the four pillars) and the system must produce that
defensibility at scale (the engineering patterns). It also echoes the "Four Pillars
of Defensible Confidence" subheading, creating a tighter conceptual thread.

### 5. Colon-based explanatory patterns → narrative prose

The lecture uses colon-separated definition patterns: "Groundedness is the
precondition: without observable artifacts, there is nothing to be correct about."
This reads like glossary entries rather than flowing narrative. Prefer full
sentences that weave the explanation into the argument. This should be codified
as a project-wide guideline in `docs/source/GUIDELINES.md` (Tone and Voice
section) so it applies to all lectures.

### 6. Escalation framing: prescriptive stories → compositional ingredients

The escalation section (Judge, Jury, Reviewer, Debate) presents each pattern with
a human-intuitive motivation — "a single evaluator might be biased, so add a
second." This reasoning is post-hoc and overly prescriptive. Running two LLMs and
picking the winner at random might outperform a carefully motivated Reviewer
pattern. The real insight is compositional: these are ingredients (single pass,
parallel, sequential, adversarial) that can be combined freely. The eval suite —
not human intuition — determines which composition works. This reinforces the
Assess vs. Improve discipline as the conceptual anchor and makes escalation
just one thing you might learn to do from running evaluations.

### 7. No prescriptive defaults — invest in validation instead

The lecture states "Judge is the right default" and prescribes when to promote
to each pattern. This takes a stand the lecture should not take. Which composition
works is an empirical question answered by the eval suite, not by reasoning about
bias or coverage. The lecture should present all patterns as options without
recommending a default or a promotion ladder. The emphasis belongs on investing in
the ability to validate (Assess vs. Improve), which is what makes any choice
among patterns defensible.

### 8. Introduce "evaluation harness" concept early

The lecture discusses internal/external validity tests and the Assess vs. Improve
discipline but never names the infrastructure that enables systematic evaluation.
Introduce "evaluation harness" early — analogous to a testing harness in software
engineering — as the concrete mechanism that makes compositional pattern selection
empirical rather than prescriptive. The harness is what lets you answer "does
adding a second LLM pass actually improve scores?" instead of assuming it does.

### 9. Merge "Assess vs. Improve" into evaluation harness concept

Assess vs. Improve and the evaluation harness are the same idea from different
angles. Assess mode *is* running the harness; Improve mode *is* acting on what the
harness reveals. Presenting them as separate concepts fragments the argument.
Unify them: the evaluation harness is the infrastructure, Assess vs. Improve is
the discipline for using it. One concept, not two.

### 10. Add a "what we are building" opening section

The lecture jumps into principles without first establishing the concrete goal.
Add an opening section that makes the input/output contract explicit: we receive
measurement artifacts from the ***Measure Impact*** stage, and we want to produce
a confidence assessment — which could be a continuous score, a categorical label
(high / medium / low), or another representation. Fixing this idea early gives
students a concrete anchor before the principles explain *how* to make that
assessment defensible.

### 11. Architecture diagram not centered

The review-engine SVG appears left-aligned despite `margin: 1em auto` in the
`<img>` tag. Root cause: the SVG has a hardcoded `width="602px"` in its root
element, which prevents responsive scaling. The pillars SVG uses only a `viewBox`
(no fixed width) and centers correctly. Fix: remove `width` and `height`
attributes from `review-engine.svg` and rely on `viewBox` alone.

### 12. Separate data flow from implementation patterns

The "From Principles to Patterns" section mixes two concerns in one paragraph:
what happens (measurement results → routing → prompt rendering → LLM call →
structured output) and how it is implemented (Registry + Dispatch, Prompt
Engineering as Software, etc.). Present the data flow first as a pure conceptual
walkthrough — what enters, what transforms, what exits — then separately map each
stage to the design pattern that implements it.

### 13. Additional resources: incomplete reference formatting

The GUIDELINES.md convention is: **Author (Year)**. [Title](url). *Source*,
volume(issue), pages. Several references in the Additional Resources section
are missing source information or use inconsistent formatting:

- Anthropic (2024) — no source type (blog post / technical report)
- Grace & Kwatra (2025), Kwatra et al. (2025) — "OpenAI Cookbook" not italicized
- Zheng et al. (2023) — "NeurIPS 2023" not italicized, missing volume/pages
- Shankar et al. (2024) — no venue/journal at all
- Gamma et al. (1994) — book title should be italicized per convention

## Decisions

### 1. Stage names and Impact Engine formatting (obs #1, #2)

Accept as stated. Replace all-caps stage names with bold-italic title case.
Replace backtick-quoted `impact-engine-evaluate` with [**Impact Engine**](url)
on first mention, **Impact Engine** thereafter.

### 2. Colon patterns → narrative prose (obs #5)

Accept. Rewrite colon-separated definition patterns as flowing narrative
throughout the lecture. Add a guideline to GUIDELINES.md Tone and Voice section:
"Avoid colon-separated definition patterns. Weave explanations into narrative
prose rather than using 'X is Y: explanation' constructions."

### 3. Architecture diagram centering (obs #11)

Accept. Remove hardcoded `width` and `height` from `review-engine.svg`, keep
`viewBox` only.

### 4. Additional resources formatting (obs #13)

Accept. Complete all references per GUIDELINES.md convention: **Author (Year)**.
[Title](url). *Source*, volume(issue), pages.

### 5. Restructure Part I into five sections (obs #3, #4, #6–10, #12)

Replace the current two-section Part I structure with five sections of
balanced depth:

| # | Section | Content | Observations |
|---|---------|---------|-------------|
| 1 | **The Evaluation Task** | Input/output contract: measurement artifacts in, confidence assessment out (score, label, or other representation) | #10 |
| 2 | **Defensible Confidence** | LLM-as-aggregator role, four pillars (groundedness, correctness, traceability, reproducibility) with balanced depth | #3, #4 |
| 3 | **Evaluation Architectures** | Building blocks (single pass, parallel, sequential, adversarial) mapped to named instances (Judge, Jury, Reviewer, Debate). No prescriptive defaults or ladder. Compositions are freely combinable. | #6, #7 |
| 4 | **The Evaluation Harness** | Infrastructure for systematic validation. Unifies Assess vs. Improve as the discipline for using the harness. Internal validity (stability, sensitivity) and external validity (known-flaw, known-clean, calibration). | #8, #9 |
| 5 | **Design Patterns** | Data flow walkthrough first (what enters, transforms, exits), then map each stage to its implementation pattern (Registry + Dispatch, Prompt Engineering as Software, Layered Specialization, Structured Output). | #12 |

## Plan

1. Add narrative prose guideline to `docs/source/GUIDELINES.md`
2. Fix `review-engine.svg` (remove `width`/`height` attributes)
3. Strip notebook outputs
4. Rewrite lecture intro cell (stage names, Impact Engine formatting)
5. Write Section 1: The Evaluation Task
6. Rewrite Section 2: Defensible Confidence (expand pillars, add LLM-as-aggregator depth)
7. Rewrite Section 3: Evaluation Architectures (compositional framing, no defaults)
8. Write Section 4: The Evaluation Harness (merge Assess vs. Improve)
9. Rewrite Section 5: Design Patterns (separate flow from implementation)
10. Fix Additional Resources formatting
11. Update `evaluate-evidence/index.md` if section names changed
12. Run notebook and rebuild docs

## Files modified

- `docs/source/GUIDELINES.md` — add narrative prose guideline
- `docs/source/_static/review-engine.svg` — remove hardcoded dimensions
- `docs/source/evaluate-evidence/02-agentic-evaluation-system/lecture.ipynb` — restructured Part I
- `docs/source/evaluate-evidence/index.md` — update section descriptions if needed

## Verification

1. `ruff check .` passes
2. `hatch run build` succeeds (notebook executes cleanly)
3. `/review-writing` pass on the lecture notebook
