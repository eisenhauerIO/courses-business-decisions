# Backlog

## Proposals

- [ ] Add Google Analytics to documentation (use `analytics_id` in `html_theme_options` in `conf.py`)
- [ ] Convert `_support/prompts/` templates to Claude Code skills for easier invocation
- [ ] Add short intro paragraphs after each subsection header in `docs/source/measure-impact/index.md` (Foundations, Selection on Observables, Selection on Unobservables)
- [ ] Add "interface-to-theory mapping" as a review criterion for lectures: when a production tool is introduced, its function interface (parameters/arguments) should be explicitly mapped back to the theoretical concepts from Part I (e.g., via a parameter→concept table followed by annotated `connect()` call). Apply retroactively to existing lectures and enforce in `author-lecture` skill
- [ ] Execute lecture upgrade plan (`LECTURE_UPGRADE.md`): bring all measure-impact lectures into compliance with updated skill standards — L03 quick fixes (page range, header, selection coefficients, `df` rename, diagnostics section), L02 moderate changes (`inspect.getsource()`, consolidate treatment function, remove summary output), L01 major restructure (new `support.py` treatment function, 6-step Part II, remove dead code), cross-lecture notation standardization (`⊥⊥`, `δ` not `τ`, numbered Part I headers)
- [ ] Integrate ideas from [`utils-agentic-support`](https://github.com/eisenhauerIO/utils-agentic-support) as a tool for the course
- [ ] Integrate application-workflow SVGs into course documentation: `fork-and-converge.svg` (detailed pipeline showing naive vs. causal fork) into the Measure Impact introduction, `recurring-loop.svg` (compact Frame → Simulate → Measure → Evaluate loop) as a recurring anchor at the start of each application section. Labels align with course sections: Measure = Measure Impact, Evaluate = Evaluate Evidence. Files stored in `docs/source/_static/`
- [ ] Synthetic control lecture: switch presentation order — present weights first, then the role of unobservables
