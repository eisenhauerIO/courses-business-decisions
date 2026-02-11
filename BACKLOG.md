# Backlog

## Proposals

- [ ] Add Google Analytics to documentation (use `analytics_id` in `html_theme_options` in `conf.py`)
- [ ] Convert `_support/prompts/` templates to Claude Code skills for easier invocation
- [ ] Add short intro paragraphs after each subsection header in `docs/source/measure-impact/index.md` (Foundations, Selection on Observables, Selection on Unobservables)
- [ ] Integrate confounded treatment assignment into Online Retail Simulator (currently manual in lecture 02: `create_binary_quality()` and `apply_confounded_treatment()` in support.py)
- [ ] Add "interface-to-theory mapping" as a review criterion for lectures: when a production tool is introduced, its function interface (parameters/arguments) should be explicitly mapped back to the theoretical concepts from Part I (e.g., via a parameter→concept table followed by annotated `connect()` call). Apply retroactively to existing lectures and enforce in `author-lecture` skill
- [ ] Decide whether confounded treatment assignment should be handled inside the simulator's `enrich` step or via a separate post-simulation function (as currently done in lecture support code)
