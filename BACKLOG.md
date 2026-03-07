# Backlog: Impact-Driven Business Decisions

Prioritized work queue for course development and refinement. See DESIGN.md for
architectural context. Granular tasks live in `.claude/docs/backlog.md`
(proposals and actionable items) and `.claude/docs/upgrades.md` (full review
findings).

## Current state

The course is actively taught at the University of Washington. Core content
is in place across five lecture sections:

- Understand Domain: 1 lecture (Catalog AI)
- Measure Impact: 4 lectures (Potential Outcomes, DAGs, Matching, Synthetic Control)
- Evaluate Evidence: 3 lectures (Evaluating Evidence, Agentic Evaluation, Application)
- Allocate Resources: 1 lecture (Portfolio Optimization)
- Build Systems, Software, Course Projects: supporting reference sections

CI (ruff linting) and documentation build (Sphinx + GitHub Pages) are
operational. All notebooks execute successfully during build.

## Phase 0 — Review feedback (high priority)

**Status**: in-progress

Address the high-priority systematic patterns identified in `.claude/docs/upgrades.md`.

- Add `optional` markers to all docstring parameters with defaults (done: 08; remaining: 01, 02, 03, catalog-ai)
- ~~Link Online Retail Simulator on first mention in all measure-impact notebooks~~ ✓
- Add notation tables to Business Context sections (done: 08; remaining: 02, 03)
- Fix import alphabetization (done: 02, catalog-ai; remaining: 01, 03, 08)

## Phase 1 — Review feedback (medium priority)

**Status**: in-progress

Address medium-priority one-off fixes from `.claude/docs/upgrades.md` and
`.claude/docs/backlog.md`.

- Verify `github-workflow` toctree entry resolves Sphinx warning (linked but may not be in toctree)
- Move misplaced `import pandas as pd` in lecture 02
- Add "god's eye view" framing in lecture 02 (done: 08)
- ~~Fix `environment.yml` formatting in `github-workflow.md`~~ ✓
- ~~Standardize catalog-ai code patterns~~ ✓

## Phase 2 — Content proposals

**Status**: planned

Address proposals from `.claude/docs/backlog.md` that require content changes
or narrative decisions.

- Synthetic control lecture: evaluate presentation order (weights vs. unobservables)
- Lecture 08: resolve assignment mechanism narrative vs. simulator behavior mismatch

## Phase 3 — Review feedback (low priority)

**Status**: planned

Polish items from `.claude/docs/upgrades.md` and `.claude/docs/backlog.md`.

- Capitalize/word choice fixes across multiple files
- Bold first concept introductions in catalog-ai
- Add Additional Resources sections where missing
- Add backticks, concept references, and business questions in various cells
- Run a link checker across all documentation

## Phase 4 — Allocate Resources lectures

**Status**: in-progress

Expand the Allocate Resources section. Portfolio Optimization (lecture 01)
is complete. Remaining content TBD.

## Phase 5 — Additional causal methods

**Status**: planned

Expand Measure Impact with additional methods (difference-in-differences,
instrumental variables, regression discontinuity) as the simulator and
impact engine support them.
