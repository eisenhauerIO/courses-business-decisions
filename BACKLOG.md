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

Part I — Theory

- Define conditioning before section 3: comparing D and Y within groups that
  share a value of Z. Stratifying, matching, filtering the sample, and adding a
  regression control are all forms of conditioning. Within a group Z cannot
  vary, so it cannot drive the D–Y association. The term is used from section 3
  onward but never defined.
- Open section 5 with why the backdoor criterion matters: if Z blocks every
  backdoor path and contains no descendant of D, treatment is as good as random
  within Z, so the within-Z comparison identifies the causal effect. Link back to
  the selection-bias term from the potential outcomes lecture, and forward to the
  conditional independence assumption in the matching lecture.
- Add a clean collider-on-a-backdoor-path example (M-bias):
  D ← A → C ← B → Y, e.g. rewrite ← brand ambition → listing quality ←
  seasonality → sales. C is pre-treatment and looks like a reasonable control,
  but conditioning on it opens the path. This breaks the "control for everything
  pre-treatment" habit.
- Reposition the police use-of-force example. Stop is a descendant of minority
  status: a mediator on minority → stop → force, and a collider on
  minority → stop ← suspicion → force, a non-causal path that leaves D rather
  than a backdoor path. Use it to motivate criterion condition 1 (no
  descendants) and sample selection as conditioning, not as the backdoor
  collider case. Note that conditioning on stop both cuts the mediated path and
  opens the collider path, so the drop from r = 0.22 to r = 0.12 mixes the two.
- Add a short section on reading paths: a variable is a collider on a path only
  if both of that path's arrows point into it; one blocking variable closes the
  whole path; long zig-zag paths are usually closed by colliders, while
  fork-and-chain-only backdoor paths (D ← A → Y, D ← A ← B → Y) stay open. Show
  that conditioning on any one non-collider (A or B) closes the second.
- Define descendant: reachable from D along a directed path (all arrows
  forward); D → A ← B makes A a descendant but not B.
- Part II intro claims Part I formalized d-separation; it does not. Either add
  it (path-blocking rules applied to all paths) or drop the claim.

Part II — Application

- The low-quality bin is all zero revenue (single-day simulation, multiplicative
  effect), so treated and control both show $0.00 and the bin carries no
  information. Simulate 30–60 days, or use an additive effect.
- The weighted conditional estimate ($10.73) misses the true effect ($23.40) by
  54%; the whole gap is in the high-quality bin ($21.46 vs. roughly $47
  expected), likely chance imbalance from skewed revenue and 510 treated
  products. Show the true effect within each bin next to the estimates, and
  verify that the fix recovers the truth.
- Section 6 calls the weighted within-bin estimate "unbiased" two cells before
  it misses by 54%. Reconcile the text with the results.
- The DAG labels quality as unobserved, but Part II conditions on it. Drop the
  label or state that we assume quality is measured.
- Add an M-bias demo: no controls (unbiased), control for C (biased), control
  for C and A (unbiased again).
- Add exercises and a closing summary; the lecture has neither.

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
