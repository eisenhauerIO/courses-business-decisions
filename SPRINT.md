# Index file formatting consistency

**Status**: complete

## Goal

Fix formatting inconsistencies across the three section index files (measure-impact,
evaluate-evidence, allocate-resources) identified during the tool introduction work.
Related to BACKLOG Phase 0 — Polish.

## Scope

**In scope**:
- Convert all headers to sentence case per GUIDELINES.md
- Standardize "Impact Engine — Evaluate" naming in evaluate-evidence body text
- Change "parts" to "sections" in measure-impact

**Out of scope**:
- Content changes to lecture notebooks
- Other index files (overview, build-systems, etc.)
- New content or structural changes
- Changes to `_external/` packages

## Observations

### 1. Title case headers

All `##` and `###` headers across all three index files use title case (e.g.,
"Selection on Observables", "Evidence Quality", "Portfolio Optimization") instead
of the sentence case required by GUIDELINES.md (e.g., "Selection on observables").

Affected headers:
- measure-impact: Foundations, Potential Outcomes Model, Causal Graphical Models,
  Selection on Observables, Matching & Subclassification, Selection on Unobservables,
  Synthetic Control
- evaluate-evidence: Evidence Quality, Causal Diagnostics, Automated Assessment,
  Agentic Evaluation, Evaluation Pipeline, Automated Review
- allocate-resources: Portfolio Optimization

### 2. Inconsistent tool name qualifier

evaluate-evidence uses "Impact Engine" without the "— Evaluate" qualifier in three
places (lines 42, 46, 60), while the tool intro paragraph correctly uses
"Impact Engine — Evaluate".

### 3. "Parts" vs "sections"

measure-impact line 40 says "three parts" while evaluate-evidence and
allocate-resources say "sections". The `##` headings are sections, so "sections"
is more accurate and consistent.

### 4. Section intro verbs

measure-impact uses "establishes" for Foundations but "covers" for both Selection
sections. Varied verbs read naturally — forcing uniformity would feel mechanical.

## Decisions

### 1. Title case headers

Convert to sentence case, but treat established causal inference framework names
as proper nouns: Potential Outcomes Model, Causal Graphical Models, Synthetic Control.
Updated GUIDELINES.md exception list to codify this.

Concrete changes:
- measure-impact: "Selection on Observables" → "Selection on observables",
  "Selection on Unobservables" → "Selection on unobservables",
  "Matching & Subclassification" → "Matching & subclassification"
- evaluate-evidence: "Evidence Quality" → "Evidence quality",
  "Causal Diagnostics" → "Causal diagnostics",
  "Automated Assessment" → "Automated assessment",
  "Agentic Evaluation" → "Agentic evaluation",
  "Evaluation Pipeline" → "Evaluation pipeline",
  "Automated Review" → "Automated review"
- allocate-resources: "Portfolio Optimization" → "Portfolio optimization"

Headers that stay capitalized (proper nouns): Foundations, Potential Outcomes Model,
Causal Graphical Models, Synthetic Control.

### 2. Inconsistent tool name qualifier

Add "— Evaluate" to all three body-text references in evaluate-evidence (lines 42, 46, 60).

### 3. "Parts" → "sections"

Change "three parts" to "three sections" in measure-impact.

### 4. Section intro verbs

No change. Varied verbs read naturally.

## Plan

1. Fix headers to sentence case in measure-impact/index.md
2. Fix headers to sentence case in evaluate-evidence/index.md
3. Fix header to sentence case in allocate-resources/index.md
4. Fix "Impact Engine" → "Impact Engine — Evaluate" in evaluate-evidence/index.md (3 occurrences)
5. Fix "parts" → "sections" in measure-impact/index.md
6. Run `hatch run build` to verify

## Verification

1. `ruff check .` — pass
2. `hatch run build` — pass

## Files modified

- `docs/source/measure-impact/index.md` — sentence case headers, "parts" → "sections"
- `docs/source/evaluate-evidence/index.md` — sentence case headers, "Impact Engine" → "Impact Engine — Evaluate" (3×), body text bold references
- `docs/source/allocate-resources/index.md` — sentence case header, body text bold reference
- `docs/source/GUIDELINES.md` — added proper noun examples to exception list
