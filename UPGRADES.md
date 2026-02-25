# Upgrades

Findings from a full review of all course materials (5 notebooks, 7 `.py` files, 14 `.md` files).

---

## Course Review (Structural Validation)

| Check | Result |
|-------|--------|
| `hatch run build` | **PASS** (1 warning: `github-workflow.md` not in any toctree) |
| External URLs (60+) | **All OK** (403s are expected academic paywalls) |
| Internal references (images, links) | **All OK** |
| Lecture self-containment | **All OK** (all `support.py` and config YAML files present) |
| Notation consistency | **All OK** (differences between lectures 01-03 vs 08 reflect standard conventions per method) |
| Git status (`docs/source/`) | **Clean** |

**One action item:** Add `github-workflow` to a toctree in `docs/source/course-projects/index.md` to fix the Sphinx warning.

---

## Writing Review — 19 issues across 8 files

### Systematic patterns (fix once, apply everywhere)

| Pattern | Count | Where |
|---------|------:|-------|
| Missing link on first mention of Online Retail Simulator | 4 | All measure-impact notebooks (cells 0) |
| Missing notation table in Business Context | 3 | `02-dags`, `03-matching`, `08-synthetic-control` |
| Missing "god's eye view" framing | 2 | `02-dags`, `08-synthetic-control` |
| Bold on first concept introduction | 2 | `02-catalog-ai` ("positioning strategies", "enrichment") |

### One-off issues

| File | Issue |
|------|-------|
| `docs/source/overview/index.md` | Uses "customer" instead of "shoppers" |
| `docs/source/course-projects/github-workflow.md` | `environment.yml` not formatted as `` `"environment.yml"` `` (~9 occurrences) |
| `docs/source/measure-impact/index.md` | "naive experimental comparison" — should be "naive comparison" (it's not experimental) |
| `08-synthetic-control` cell 29 | `## Additional Resources` should be `## Additional resources` (lowercase r) |
| `08-synthetic-control` cell 0 | Missing business question and simulator mention in title cell |
| `03-matching` cell 36 | `MEASUREMENT.PARAMS` missing backticks |
| `02-dags` cell 20 | Part II intro doesn't reference Part I concepts by name |
| `08-synthetic-control` cell 18 | First mention of **Impact Engine** not linked |
| `02-catalog-ai` | No `## Additional resources` section |

---

## Code Review — 33 issues across 12 files

### 0 bugs, 0 security issues

### Docstrings (15 issues) — most pervasive pattern

Missing `optional` markers on parameters with defaults across **all** `support.py` files:

| File | Affected functions |
|------|--------------------|
| `01-potential-outcomes-model/support.py` | `create_confounded_treatment`, `plot_balance_check` |
| `02-directed-acyclic-graphs/support.py` | `simulate_police_force_data`, `draw_police_force_example`, `create_confounded_treatment`, `_apply_confounded_treatment`, `plot_confounding_bar` |
| `03-matching-subclassification/support.py` | `create_confounded_treatment_multi`, `plot_treatment_rates`, `plot_covariate_imbalance` |
| `08-synthetic-control/support.py` | `create_synthetic_control_data`, `plot_weights` |
| `02-catalog-ai/support.py` | `plot_treatment_effect`, `plot_positioning_comparison`, `_print_scenario_stats` |

### Style (14 issues)

| Issue | Where |
|-------|-------|
| Import alphabetization wrong | `01` cell 10, `02` cell 21, `03` cell 21, `08` cell 9, `catalog-ai` cell 6 |
| Misplaced `import pandas as pd` (deep in Part II instead of import cell) | `02-dags` cell 40 |
| Redundant `effects = compute_effects()` recomputation | `02-dags` cell 40 |
| Unused `fig` variable (should be `_`) | `catalog-ai/support.py` lines 51, 121 |
| Unused lambda param (should be `_`) | `catalog-ai/support.py` lines 80, 159 |
| `from online_retail_simulator import simulate, load_job_results, enrich` — 3 imports on one line, should use parens | `catalog-ai` cell 6 |
| Support imports not alphabetized | `catalog-ai` cell 6 |
| Non-standard `itemgetter` pattern for result unpacking | `catalog-ai` cell 11 |
| `! cat config_simulation.yaml` missing quotes | `03-matching` cells 24, 37, 45 |

### Clarity (3 issues)

| Issue | Where |
|-------|-------|
| Cell exceeds 20-line complexity limit | `01` cell 42 (~23 lines), `08` cell 20 (~22 lines) |
| `itemgetter` pattern obscures standard result loading | `catalog-ai` cell 11 |

---

## Priority Summary

### High priority (consistency patterns affecting multiple files)

- [ ] Add `optional` to all docstring params with defaults (15 functions across 5 files)
- [ ] Link Online Retail Simulator on first mention (4 notebooks)
- [ ] Add notation tables to Business Context sections (3 notebooks)
- [ ] Fix import alphabetization (5 notebook import cells)

### Medium priority (one-off fixes)

- [ ] Add `github-workflow` to toctree (Sphinx warning)
- [ ] Move `import pandas as pd` from cell 40 to cell 21 in `02-dags`
- [ ] Add "god's eye view" framing in `02-dags` and `08-synthetic-control`
- [ ] Fix `environment.yml` formatting in `github-workflow.md`
- [ ] Standardize `catalog-ai` patterns (`itemgetter`, unused `fig`, import grouping)

### Low priority (minor polish)

- [ ] Mention and link the Online Retail Simulator on the measure-impact landing page (`docs/source/measure-impact/index.md`) — currently only the Impact Engine is highlighted. **Trade-off:** all measure-impact lectures already use the simulator, so ideally the tooling section (Build Systems or a dedicated tool overview) should be introduced before measure-impact to give students context. Consider whether to restructure section ordering or just add a forward reference.
- [ ] Capitalize/word choice fixes ("Additional Resources" → lowercase, "naive experimental", "customers" → "shoppers")
- [ ] Bold first concept introductions in `02-catalog-ai` ("positioning strategies", "enrichment")
- [ ] Add `## Additional resources` section to `02-catalog-ai`
- [ ] Add backticks to `MEASUREMENT.PARAMS` in `03-matching` cell 36
- [ ] Add Part I concept references to `02-dags` Part II intro
- [ ] Add business question and simulator mention to `08-synthetic-control` title cell
- [ ] Link **Impact Engine** on first mention in `08-synthetic-control`
