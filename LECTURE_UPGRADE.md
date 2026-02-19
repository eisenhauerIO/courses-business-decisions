# Lecture Upgrade Plan: Measure-Impact Compliance

## Context

Three skill reviews (`/author-lecture`, `/review-code`, `/review-writing`) found all three measure-impact lectures non-compliant with the updated skill standards. Lecture 03 is closest; Lecture 01 needs the most work. This plan brings all three into compliance with the 6-step Part II pattern, `support.py` conventions, and cross-lecture notation consistency.

**Key architectural decision:** Lectures 01 and 02 are conceptually different from later lectures — L01 teaches the *problem* (missing counterfactuals), L02 teaches *identification* (DAGs/backdoor criterion). Neither introduces a formal estimation *method* the way L03+ do. The 6-step pattern is followed in spirit, adapting steps 3–4 to each lecture's scope.

---

## Lecture 03 (Matching) — Quick Fixes

Closest to compliance. One remaining edit.

### ~~3A. Fix page range in header~~ DONE

### ~~3B. Add business question to header~~ DONE

### ~~3C. Expose selection coefficients as function arguments~~ DONE

### ~~3D. Rename `df` to `confounded_products`~~ DONE

### ~~3E. Add standalone Diagnostics & Extensions section~~ DONE
Promoted balance diagnostics and Love plot from Section 6 subsection into new `## 8. Diagnostics & Extensions` top-level section. Section 7 (method comparison) stays as validation step.

### ~~3F. Fix import alphabetization~~ DONE
Moved `import pandas as pd` before `from` imports in cell 21 (standard isort ordering).

---

## Lecture 02 (DAGs) — Moderate Changes

### ~~2A. Show `create_confounded_treatment` source via `inspect.getsource()`~~ DONE
Inserted code cell after "Creating the Confounded Treatment Assignment" markdown showing the consolidated function source.

### ~~2B. Consolidate two-step treatment function into one~~ DONE
Created `create_confounded_treatment(metrics_df, ...)` in `support.py` that calls `_create_binary_quality` and `_apply_confounded_treatment` internally. Old functions renamed to private. Notebook updated to use single call.

### ~~2C. Remove summary output (cell 39)~~ DONE
Replaced SUMMARY print block with `pd.DataFrame` comparison table showing Naive vs Conditional estimates, errors, and % errors.

### ~~2D. Remove unused `plt` import~~ DONE
Removed `import matplotlib.pyplot as plt` from notebook imports.

### ~~2E. Rename `confounded_products` variable consistently~~ DONE

---

## Lecture 01 (Potential Outcomes) — Major Restructure

### ~~1A. Create confounded treatment function in `support.py`~~ DONE
Added `create_confounded_treatment(metrics_df, treatment_fraction=0.3, true_effect=0.5, seed=42)` that aggregates revenue, generates quality score, and assigns treatment to bottom fraction by quality (struggling products get optimized).

### ~~1B. Remove dead functions from `support.py`~~ DONE
Deleted: `plot_treatment_parameters`, `plot_bias_decomposition`, `plot_bootstrap_distribution`, `plot_outcome_by_treatment`, `plot_fundamental_problem_table`.

### ~~1C. Restructure Part II notebook cells~~ DONE
Reorganized Part II from 8-section scenario-based layout into 6-step concept-based structure:
1. **Business Context** — content optimization question
2. **Data Generation** — simulate + confounded treatment via `support.py` + `inspect.getsource()`
3. **Naive Comparison** — difference-in-means on confounded data, explain negative selection bias
4. **The Simulator's Advantage** — fundamental problem table, ITE, ATE/ATT/ATC, bias decomposition verification
5. **Randomization Recovers the Truth** — enrichment pipeline, naive estimator unbiased, covariate balance
6. **Diagnostics & Extensions** — Monte Carlo (random vs biased), sample size convergence

### ~~1D. Keep enrichment pipeline for random treatment~~ DONE
The `enrich()` call with `config_enrichment_random.yaml` is present and functional.

---

## Cross-Lecture Notation Standardization

### ~~N1. Independence symbol~~ DONE
L03 already uses `\perp\!\!\!\perp` throughout.

### ~~N2. Treatment effect symbol~~ DONE
Changed `\hat{\tau}_{\text{naive}}` → `\hat{\delta}_{\text{naive}}` and `\hat{\tau}_{\text{conditional}}` → `\hat{\delta}_{\text{conditional}}` in L02 cell 20.

### ~~N3. Part I section numbering~~ DONE
Added numbered headers to L01 Part I sections (1–7), matching L02 and L03 convention.

---

## Execution Order

All items completed:

1. ~~**L03 remaining fixes** (3F)~~ DONE
2. ~~**L02 moderate changes** (2A–2D)~~ DONE
3. ~~**L01 major restructure** (1A–1C)~~ DONE
4. ~~**Cross-lecture notation** (N2–N3)~~ DONE
5. ~~**Verify:** `hatch run pytest` after each lecture~~ DONE

---

## Verification

All checks passed:
```bash
hatch run jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace docs/source/measure-impact/*/lecture.ipynb  # ✓
hatch run ruff format docs/source/measure-impact/*/support.py  # ✓
hatch run ruff check docs/source/measure-impact/*/support.py  # ✓
hatch run pytest  # ✓ 4 passed in 21.26s
```

Success criteria — all met:
- ✓ All 4 notebooks pass `nbmake` tests
- ✓ `ruff format` and `ruff check` clean
- ✓ Each lecture's Part II follows the 6-step pattern (adapted for L01's scope)
- ✓ All `support.py` treatment functions accept `metrics_df`, return `D/Y0/Y1/Y_observed`
- ✓ `inspect.getsource()` used for treatment function in all three lectures
- ✓ Notation consistent: `\perp\!\!\!\perp`, `\hat{\delta}`, numbered Part I headers
