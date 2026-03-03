# Backlog

## Proposals

- [ ] Synthetic control lecture: switch presentation order — present weights first, then the role of unobservables

- [ ] Lecture 08: assignment mechanism narrative claims quality-based selection but simulator uses random selection
  - The notebook says "treated products are selected based on their content quality scores — products with the weakest listings are prioritized"
  - The simulator's `quantity_boost` in `enrichment_library.py` uses `rng.choice()` (uniform random)
  - Either fix the narrative to match the code (random assignment → no selection bias story) or update the simulator to select by quality score

- [ ] Incorporate review feedback
  - **Blocking**
    - Add notation table (Variable | Notation | Description) to Business Context in lectures 02 (DAGs) and 03 (Matching)
    - Add `## Additional resources` section to understand-domain/02-catalog-ai lecture
  - **Notation consistency**
    - Lecture 08: rename $\delta_t$ (common time effect) to $\lambda_t$ or $\gamma_t$ to avoid collision with $\delta$ (treatment effect) in lectures 01–03
    - Lecture 08: add bridging sentences connecting $\alpha \leftrightarrow \delta$ and $Y^N/Y^I \leftrightarrow Y^0/Y^1$ to earlier lecture notation
  - **Writing**
    - Bold first-mention tool links in build-systems/index.md, overview/index.md, course-projects/index.md
    - Verify Slack invite link in iterations/econ-481A-uw-2026.md (may be expired)
    - Add backtick-quotes around `environment.yml` references in course-projects/github-workflow.md
    - Remove re-link of Impact Engine on second mention in measure-impact/index.md
    - Add explicit "god's eye view" language to lecture 03
    - Add dedicated Assignment Mechanism sections (or labels) to lectures 01 and 02
    - Bold Online Retail Simulator link on first mention in lecture 08
    - State selection paradox earlier in lecture 01 Business Context
    - Run a link checker across all documentation
  - **Code**
    - Replace `importlib` dynamic loading of shared.py in lectures 03 and 08 with proper packaging
    - Lecture 02 support.py: pass `true_effect` as parameter instead of storing as DataFrame column
    - Consolidate duplicate imports (inspect, Code) in lecture 02 cells 2/21; move `import pandas as pd` from cell 40 to Part II import cell
    - Remove duplicate `compute_effects()` call in lecture 02 cell 40
    - Consolidate inspect/Code imports into Part II import cell in lecture 08
    - Replace legacy `np.random.seed(42)` with `default_rng` in lectures 01 and 02
    - Add `encoding="utf-8"` to `open()` in lecture 08 support.py
    - Use `_, ax = plt.subplots(...)` for unused fig in catalog-ai support.py
    - Show `inspect.getsource(generate_quality_score)` before first direct use in lecture 01
  - **Build warnings**
    - GUIDELINES.md and github-workflow.md not in any toctree

- [ ] Evaluate Evidence lectures
  - **Landing page (index.md)**
    - Surface four pillar names (groundedness, correctness, traceability, reproducibility) in Automated Assessment and Agentic Evaluation summaries
    - Add caveat about out-of-distribution flaw patterns in Correctness validation framing
    - Preview how confidence scores bridge to resource allocation (one-sentence preview of the functional form)
  - **Lecture 01 (Evaluating Causal Evidence)**
    - Soften "hierarchy of evidence designs" — add sentence that execution quality can invert the hierarchy
    - Add external validity diagnostic subsection (transportability, covariate comparison, heterogeneity analysis)
    - Develop "From Estimate to Evidence" subsection — practical significance example (incremental revenue vs. measurement cost)
    - Add DiD diagnostic table to match the method-specific sections for experiments, matching, and synthetic control
    - Add at least one worked code example (Love plot, placebo distribution, or RMSPE)
  - **Lecture 02 (Agentic Evaluation System)**
    - Map evaluation architectures to pillars (Jury → Reproducibility, Reviewer → Correctness, Debate → Groundedness) in Section 3
    - Add Assess/Improve anti-pattern example ("overfitting the prompt to a specific test case")
    - Add evaluation harness limitation paragraph (cannot test for unconceived failure modes — shared with software testing broadly)
    - Add transition bridge sentence at top of Section 1 connecting from Lecture 01's diagnostic toolkit
  - **Cross-notebook**
    - External validity gap: Lecture 01 defines it but doesn't develop diagnostics; Lecture 02 harness focuses on internal validity of the evaluator — need coherent treatment across both
