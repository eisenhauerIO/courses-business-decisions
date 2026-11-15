# Backlog: Impact-Driven Business Decisions

Prioritized work queue for course development and refinement. See DESIGN.md for
architectural context.

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

## Phase 0 — Polish

**Status**: in-progress

### DAG lecture (`measure-impact/02-directed-acyclic-graphs`)

Part I (theory) and the practice cards are done. Part II (application) remains:

- The low-quality bin is all zero revenue (single-day simulation, multiplicative
  effect), so treated and control both show $0.00 and the bin carries no
  information. Simulate 30–60 days, or use an additive effect.
- The weighted conditional estimate ($10.73) misses the true effect ($23.40) by
  54%; the whole gap is in the high-quality bin ($21.46 vs. roughly $47
  expected), likely chance imbalance from skewed revenue and 510 treated
  products. Compute the ground truth per bin before any estimate, show it next
  to the estimates, and verify that the fix recovers the truth.
- Section 6 calls the weighted within-bin estimate "unbiased" before it misses
  by 54%, and the lecture ends on the error table without comment. Reconcile the
  text with the results.
- Quality has three identities: $X$ in the notation table, $Q$ in "Drawing the
  DAG" and the formulas, and labeled unobserved although Part II conditions on
  it. Use one symbol and state that quality is observed.
- Align wording with Part I: quality is a fork on the backdoor path (not a
  "non-collider"), and "From unconditional to conditional comparisons" repeats
  theory before section 1.
- Remove capitals and exclamation marks in markdown and printed output
  ("LOWER", "HURTS", "confounding!", "POSITIVE effect!").
- Add an M-bias demo: no controls (unbiased), control for C (biased), control
  for C and A (unbiased again).

## Phase 1 — Productize

**Status**: planned

Turn the course into a standalone product with a public-facing value proposition.

- Add a landing page with clear value proposition: what the course delivers, who
  it is for, and what makes it different
- Review all materials through the Billion-Dollar Contributor lens: does the
  course position Philipp as the person who connects causal inference, evidence
  evaluation, and decision theory into one operational framework?
- Highlight that the entire course — lectures, tools, and infrastructure — is
  designed and built by Philipp Eisenhauer
- Ensure the narrative arc (Learn, Decide, Repeat) reads as a product story,
  not just a syllabus
