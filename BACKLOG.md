# Backlog

## Proposals

- [ ] Add Google Analytics to documentation (use `analytics_id` in `html_theme_options` in `conf.py`)
- [ ] Convert `_support/prompts/` templates to Claude Code skills for easier invocation
- [ ] Add short intro paragraphs after each subsection header in `docs/source/measure-impact/index.md` (Foundations, Selection on Observables, Selection on Unobservables)
- [ ] Integrate confounded treatment assignment into Online Retail Simulator (currently manual in lecture 02: `create_binary_quality()` and `apply_confounded_treatment()` in support.py)
- [ ] Add "interface-to-theory mapping" as a review criterion for lectures: when a production tool is introduced, its function interface (parameters/arguments) should be explicitly mapped back to the theoretical concepts from Part I (e.g., via a parameter→concept table followed by annotated `connect()` call). Apply retroactively to existing lectures and enforce in `author-lecture` skill
- [ ] Decide whether confounded treatment assignment should be handled inside the simulator's `enrich` step or via a separate post-simulation function (as currently done in lecture support code)
- [ ] Draft lecture guidelines document, then integrate into `author-lecture` skill. High-level structure for Part II (Application):
  1. **Business Context** — frame the recurring question (consistent across the lecture sequence)
  2. **Data Generation** — config-driven simulation (`simulate()` → `load_job_results()`), then confounded treatment assignment
  3. **Naive Comparison** — show the biased estimate, explain why it's wrong using Part I theory
  4. **Apply the Method** — connect Part I theory to practice; interface-to-theory mapping table when using production tools
  5. **Validation Against Ground Truth** — leverage simulator's full potential outcomes to verify the method works
  6. **Visualization & Comparison** — plots showing bias reduction, balance diagnostics, or method comparison

  Additional guidelines to codify:
  - Standardized import ordering (standard lib → third-party → simulator → support)
  - Progressive covariate complexity across the lecture sequence (binary → continuous → multivariate)
  - When to use impact engine adapters vs. manual implementation (manual demo first, then production tool)
