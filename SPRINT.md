# Evaluate Evidence Lectures — Observation Collection

**Status**: executing

## Goal

Collect fresh observations on Evaluate Evidence lectures 01 (Evaluating Causal
Evidence) and 02 (Agentic Evaluation System) to identify improvements in content,
structure, and writing quality.

## Scope

**In scope**:
- Content, structure, and writing of lectures 01 and 02
- Landing page (evaluate-evidence/index.md) as it relates to these lectures

**Out of scope**:
- Code changes to Impact Engine repositories (_external/)

## Observations

### 1. "From Estimate to Evidence" needs a two-stage arc (lecture 01)

The current structure treats stress-testing (robustness, sensitivity, placebo) and
practical significance as separate subsections without an explicit narrative link.
Reframe as two stages: (1) **Is this number reliable?** — stress-test the single
estimate to build confidence that the effect is real; (2) **Does it actually matter?**
— practical significance, cost-benefit analysis, whether the effect is large enough
to justify action. The first stage earns trust in the number; the second stage asks
whether a trusted number warrants a decision. This gives "From Estimate to Evidence"
a clear progression rather than a flat list of checks.

### 2. Hierarchy of evidence: expand with two missing dimensions (lecture 01)

The hierarchy currently uses three tiers (experiments, observational causal studies,
time series) defined by how well each rules out alternative explanations. Two
dimensions are missing:

**(a) Model-based vs. design-based.** Methods that rely on functional form assumptions
(e.g., regression) versus methods that derive credibility from features of the research
design itself (randomization, natural experiments, discontinuities). Design-based
methods are more robust because their validity does not depend on getting the functional
form right. The hierarchy should surface this distinction explicitly.

**(b) Execution quality can invert the hierarchy.** The current framing implies that
higher-tier designs always produce better evidence. That is wrong. A badly executed
experiment — broken randomization, high attrition, non-compliance — can produce worse
evidence than a well-executed time-series analysis with strong pre/post diagnostics.
The hierarchy is a useful prior about *design potential*, not a guarantee. The lecture
should make this explicit: the tier tells you the ceiling, but implementation
determines where you actually land.

### 3. Inconsistent depth in method-specific diagnostics (lecture 01)

Section 2 treats the three methods unevenly. Matching gets two prose paragraphs
(covariate balance, common support) plus a summary table. Experiments and synthetic
control get only a table with one-line descriptions per row — no explanatory prose.
Adopt a hybrid format for all three methods: give the major diagnostics their own
paragraph of explanation, then reference the summary table for the remaining checks.
This provides depth where it matters without expanding every row into a paragraph.

## Decisions

### 1. Two-stage "From Estimate to Evidence" arc (obs #1)

Accept. Restructure the current "Stress-Testing a Single Estimate" and "From Estimate
to Evidence" subsections into a unified two-stage framing: (1) **Is this number
reliable?** — robustness, sensitivity, placebo; (2) **Does it actually matter?** —
practical significance, cost-benefit. Replication stays as a coda after the two stages.

### 2. Hierarchy of evidence: two new dimensions (obs #2)

Accept both. (a) Add model-based vs. design-based distinction to the hierarchy
discussion. (b) Add explicit caveat that execution quality can invert the hierarchy —
the tier is a ceiling, not a guarantee.

### 3. Hybrid format for method-specific diagnostics (obs #3)

Accept. Extend the matching treatment (prose paragraphs for major diagnostics +
summary table for the rest) to experiments and synthetic control. Major diagnostics
to expand: randomization integrity and attrition for experiments; pre-treatment fit
and placebo gaps for synthetic control.

## Plan

1. Strip notebook outputs for lecture 01
2. Rewrite Section 1 "From Estimate to Evidence" with two-stage arc (obs #1)
3. Expand hierarchy of evidence with model-based vs. design-based and execution
   quality caveat (obs #2)
4. Add prose paragraphs for major experiment diagnostics (randomization integrity,
   attrition) in Section 2 (obs #3)
5. Add prose paragraphs for major synthetic control diagnostics (pre-treatment fit,
   placebo gaps) in Section 2 (obs #3)
6. Run `ruff check .` and fix any issues
7. Run `hatch run build` to verify notebook executes cleanly

## Files modified

- `docs/source/evaluate-evidence/01-evaluating-evidence/lecture.ipynb` — restructured
  Section 1 and expanded Section 2 diagnostics
- `docs/source/GUIDELINES.md` — added semicolon rule and possessive apostrophe clarification
- `docs/source/evaluate-evidence/02-agentic-evaluation-system/lecture.ipynb` — fixed colon
  and passive voice violations, removed implementation-specific references from Design
  Patterns subsections (deferred to lecture 03)
- `CLAUDE.md` — added GUIDELINES.md reference, removed duplicated conventions

## Verification

1. `ruff check .` passes
2. `hatch run build` succeeds (all notebooks execute cleanly)
3. CI passes on feature branch before merge
