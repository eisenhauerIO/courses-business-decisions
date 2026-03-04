# Evaluate Evidence Lecture 02 — Agentic Evaluation Review

**Status**: executing

## Goal

Review and refine Lecture 02 (Agentic Evaluation System) content. Contributes to
BACKLOG.md Phase 0 (Review feedback — high priority).

## Scope

**In scope**:
- Content and structural review of `docs/source/evaluate-evidence/02-agentic-evaluation-system/lecture.ipynb`

**Out of scope**:
- Changes to other lectures
- Changes to Impact Engine repositories (`_external/`)

## Observations

### 1. Pillar-to-design-pattern mapping table may be forced

The table mapping pipeline stages to design patterns and pillars enforced stretches the
one-to-one correspondence. Layered Specialization → Traceability is the weakest link —
the uniform interface enables audit trails, but the primary value of layered
specialization is correctness through method-specific expertise. Traceability is a side
effect, not the main point.

A tighter mapping would let Correctness appear twice (once for Registry + Dispatch, once
for Layered Specialization) rather than forcing a distinct pillar for each row. The
alternative is to reframe the Layered Specialization description to emphasize the uniform
interface angle more explicitly, but this requires more of a leap for the reader.

### 2. Formulaic "enforces the X pillar" closing sentences

Each design pattern subsection (cells 7–10) ends with a formulaic sentence linking the
pattern to a pillar: "This pattern enforces the Correctness pillar," "This enforces the
Reproducibility pillar," "This enforces the Traceability pillar uniformly," "This cycle
enforces Groundedness at the output level." The table in cell 6 already maps patterns to
pillars explicitly — these closing sentences restate what the table says.

### 3. Remove SUTVA from evaluate-evidence lectures

Lectures 01 and 03 use "Spillover / SUTVA." Remove the "/ SUTVA" abbreviation and keep
just "Spillover." Affects lecture 01 (diagnostic table) and lecture 03 (three mentions in
walkthrough text).

### 4. Hierarchy-of-evidence SVG font sizes too small

In `_static/hierarchy-of-evidence.svg`, the "Tier N" labels (font-size 11), "True Effect"
label (font-size 12), and the side descriptions ("Treatment and control units assigned at
random," etc.) are too small. Increase font sizes so they are readable at the same scale
as the tier names inside the pyramid (currently font-size 14). The side descriptions can
wrap to two lines if needed.

### 5. Stress-tests SVG: "Stable across specifications?" label position

Moved from between the Robustness Checks box and the arrow to the right side. Already
fixed — observation recorded for tracking.

### 6. Evaluate-evidence SVGs need a visual review pass

All SVGs used in the evaluate-evidence lectures need a review for readability, font
sizing, label placement, and overall visual quality. Options A/B/C for a new evaluation
harness diagram will be evaluated during this pass. Candidates:
- `_static/hierarchy-of-evidence.svg` (obs #4)
- `_static/stress-tests.svg` (obs #5)
- `_static/defensible-confidence-pillars.svg`
- `_static/review-engine.svg`
- Any new diagram for Section 4 (The Evaluation Harness)

## Decisions

1. **Table mapping**: Drop forced one-to-one. Let Correctness appear twice (Registry +
   Dispatch, Layered Specialization). Remove Traceability as standalone pillar for Layered
   Specialization.
2. **Formulaic closers**: Remove all four "enforces the X pillar" closing sentences.
3. **SUTVA**: Replace "Spillover / SUTVA" with "Spillover" in lectures 01 and 03.
4. **Hierarchy SVG fonts**: Tier labels 11→14, True Effect 12→14, side descriptions 11→13
   (wrap to two lines as needed).
5. **Stress-tests label**: Already fixed.
6. **SVG review pass**: Separate task after content edits.

## Plan

1. Edit lecture 02 notebook: fix table + remove formulaic closers (obs #1, #2)
2. Edit lectures 01 and 03: remove SUTVA (obs #3)
3. Edit hierarchy-of-evidence SVG: increase font sizes (obs #4)
4. SVG visual review pass (obs #6) — next task

## Files modified

- `docs/source/evaluate-evidence/02-agentic-evaluation-system/lecture.ipynb` — table mapping
  (obs #1), formulaic closers removed (obs #2)
- `docs/source/evaluate-evidence/01-evaluating-evidence/lecture.ipynb` — SUTVA removed (obs #3)
- `docs/source/evaluate-evidence/03-application/lecture.ipynb` — SUTVA removed (obs #3)
- `docs/source/_static/hierarchy-of-evidence.svg` — font sizes increased (obs #4)
- `docs/source/_static/stress-tests.svg` — label repositioned (obs #5, prior session)

## Verification

TBD
