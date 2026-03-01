# Implementation Plan: Impact-Driven Business Decisions

Phased roadmap for course development and refinement. See DESIGN.md for
architectural context. Granular tasks live in `.claude/docs/backlog.md`
(proposals and actionable items) and `.claude/docs/upgrades.md` (full review
findings).

## Current state

The course is actively taught at the University of Washington. Core content
is in place across five lecture sections:

- Understand Domain: 1 lecture (Catalog AI)
- Measure Impact: 4 lectures (Potential Outcomes, DAGs, Matching, Synthetic Control)
- Evaluate Evidence: 3 lectures (Evaluating Evidence, Agentic Evaluation, Application)
- Allocate Resources: placeholder (no lectures yet)
- Build Systems, Software, Course Projects: supporting reference sections

CI (ruff linting) and documentation build (Sphinx + GitHub Pages) are
operational. All notebooks execute successfully during build.

## Phase 0 — Root documentation

**Status**: in-progress

Bring repository root documents into ecosystem schema conformance.

- [x] `README.md` — restructure to schema (h1 before badges, add docs link)
- [x] `CLAUDE.md` — rewrite with all 7 required sections
- [x] `DESIGN.md` — create course design document
- [x] `PLAN.md` — create this implementation roadmap
- [x] `docs/source/index.md` — decouple from README.md, write standalone landing page
- [ ] Verify Sphinx build passes

## Phase 1 — Review feedback (high priority)

**Status**: planned

Address the high-priority systematic patterns identified in `.claude/docs/upgrades.md`.

- Add `optional` markers to all docstring parameters with defaults (15 functions, 5 files)
- Link Online Retail Simulator on first mention in all measure-impact notebooks
- Add notation tables to Business Context sections (lectures 02, 03, 08)
- Fix import alphabetization in 5 notebook import cells

## Phase 2 — Review feedback (medium priority)

**Status**: planned

Address medium-priority one-off fixes from `.claude/docs/upgrades.md` and
`.claude/docs/backlog.md`.

- Add `github-workflow` to toctree (fix Sphinx warning)
- Move misplaced `import pandas as pd` in lecture 02
- Add "god's eye view" framing in lectures 02 and 08
- Fix `environment.yml` formatting in `github-workflow.md`
- Standardize catalog-ai code patterns

## Phase 3 — Content proposals

**Status**: planned

Address proposals from `.claude/docs/backlog.md` that require content changes
or narrative decisions.

- Synthetic control lecture: evaluate presentation order (weights vs. unobservables)
- Lecture 08: resolve assignment mechanism narrative vs. simulator behavior mismatch

## Phase 4 — Review feedback (low priority)

**Status**: planned

Polish items from `.claude/docs/upgrades.md` and `.claude/docs/backlog.md`.

- Capitalize/word choice fixes across multiple files
- Bold first concept introductions in catalog-ai
- Add Additional Resources sections where missing
- Add backticks, concept references, and business questions in various cells
- Run a link checker across all documentation

## Phase 5 — Allocate Resources lectures

**Status**: planned

Create the decision theory lecture series for the Allocate Resources section.
This is the largest remaining content gap in the course.

## Phase 6 — Additional causal methods

**Status**: planned

Expand Measure Impact with additional methods (difference-in-differences,
instrumental variables, regression discontinuity) as the simulator and
impact engine support them.
