# Lecture Upgrade Plan: Measure-Impact Compliance

## Context

Three skill reviews (`/author-lecture`, `/review-code`, `/review-writing`) found all three measure-impact lectures non-compliant with the updated skill standards. Lecture 03 is closest; Lecture 01 needs the most work. This plan brings all three into compliance with the 6-step Part II pattern, `support.py` conventions, and cross-lecture notation consistency.

**Key architectural decision:** Lectures 01 and 02 are conceptually different from later lectures — L01 teaches the *problem* (missing counterfactuals), L02 teaches *identification* (DAGs/backdoor criterion). Neither introduces a formal estimation *method* the way L03+ do. The 6-step pattern is followed in spirit, adapting steps 3–4 to each lecture's scope.

---

## Lecture 03 (Matching) — Quick Fixes

Closest to compliance. Four targeted edits, no structural changes.

### 3A. Fix page range in header
**File:** `docs/source/measure-impact/03-matching-subclassification/lecture.ipynb` (cell 0)
- Change `pp. 175-206` → `pp. 175-230`

### 3B. Add business question to header
**File:** same cell 0
- Append to the opening paragraph: `We apply these concepts using the Online Retail Simulator to answer: **Can subclassification and matching recover the true treatment effect when confounding involves multiple continuous covariates?**`

### 3C. Expose selection coefficients as function arguments
**File:** `docs/source/measure-impact/03-matching-subclassification/support.py`
- Add `coef_quality=-0.5, coef_price=-0.8, coef_impressions=-0.3` as explicit keyword arguments to `create_confounded_treatment_multi()`
- Replace hardcoded `COEF_QUALITY`, `COEF_PRICE`, `COEF_IMPRESSIONS` locals with the parameters
- Update the NumPy docstring to document them

### 3D. Rename `df` to `confounded_products`
**File:** `docs/source/measure-impact/03-matching-subclassification/lecture.ipynb`
- Cells 26, 28, 30, 34, 39: replace `df` → `confounded_products` throughout Part II
- Cell 28: `treated = confounded_products[confounded_products["D"] == 1]` etc.

### 3E. Add standalone Diagnostics & Extensions section
**File:** same notebook
- Promote the existing "### Covariate Balance Diagnostics" (cell 40) and Love plot (cells 41-42) out of Section 4 into a new `## 6. Diagnostics & Extensions` section
- Add brief intro markdown: "A key advantage of matching is that we can directly assess covariate balance..."
- Section 5 ("Which Method Best Recovers the True Effect?") stays as the Validation step

### 3F. Fix import alphabetization
**File:** same notebook, cell 21
- Reorder: `impact_engine` imports before `IPython` (case-insensitive sort)

---

## Lecture 02 (DAGs) — Moderate Changes

### 2A. Show `apply_confounded_treatment` source via `inspect.getsource()`
**File:** `docs/source/measure-impact/02-directed-acyclic-graphs/lecture.ipynb`
- After cell 30 ("Creating the Confounded Treatment Assignment" markdown), before cell 31 (the function call), insert a new code cell:
  ```python
  Code(inspect.getsource(apply_confounded_treatment), language="python")
  ```

### 2B. Consolidate two-step treatment function into one
**File:** `docs/source/measure-impact/02-directed-acyclic-graphs/support.py`
- Create `create_confounded_treatment(metrics_df, prob_treat_low=0.6, prob_treat_high=0.2, true_effect=0.5, seed=42)` that:
  1. Aggregates revenue per product (from `create_binary_quality`)
  2. Assigns binary quality High/Low by median split (from `create_binary_quality`)
  3. Assigns confounded treatment (from `apply_confounded_treatment`)
  4. Returns DataFrame with `product_identifier, quality, D, Y0, Y1, Y_observed`
- Keep old functions but mark private (`_create_binary_quality`, `_apply_confounded_treatment`) since `compute_effects` and plotting functions still need the same columns
- Update notebook cell 31 to call the single consolidated function

### 2C. Remove summary output (cell 39)
**File:** same notebook
- Replace the SUMMARY print block in cell 39 with a simple comparison table (like L03's approach in cell 45): a `pd.DataFrame` showing Naive vs Conditional estimates, errors, and % errors
- Remove the "SUMMARY:" header and `=` separators

### 2D. Remove unused `plt` import
**File:** same notebook, cell 21
- Remove `import matplotlib.pyplot as plt` (all plotting goes through `support.py` functions)

### 2E. Rename `confounded_products` variable consistently
**File:** same notebook
- Already uses `confounded_products` — verify consistency across all cells

---

## Lecture 01 (Potential Outcomes) — Major Restructure

### Current structure (cells 9–47):
1. Setup/Imports → 2. Simulate baseline → 3. Enrich (random treatment) → 4. Fundamental problem demo → 5. True parameters (ITE, ATE) → 6. Random assignment validation → 7. Biased selection + bias decomposition → 8. Monte Carlo → 9. Convergence

### Target 6-step structure:
1. **Business Context** — content optimization question (reuse from current)
2. **Data Generation** — simulate + confounded treatment via `support.py` function + `inspect.getsource()`
3. **Naive Comparison** — simple difference-in-means on confounded data; show the biased estimate; explain using Part I's selection bias decomposition
4. **The Simulator's Advantage** — this is L01's unique "method": leverage known potential outcomes (Y0, Y1) to directly compute true ATE, decompose selection bias, and show *why* the naive estimate fails. This replaces "Apply the Method" for L01 since L01's contribution is understanding the problem, not solving it with an estimator.
5. **Validation: Randomization Recovers the Truth** — show that random assignment eliminates selection bias (the naive estimator becomes unbiased under randomization). This is L01's ground-truth validation.
6. **Diagnostics & Extensions** — Monte Carlo simulations (random vs biased), covariate balance under randomization, sample size convergence

### 1A. Create confounded treatment function in `support.py`
**File:** `docs/source/measure-impact/01-potential-outcomes-model/support.py`
- Add `create_confounded_treatment(metrics_df, treatment_fraction=0.3, true_effect=0.5, seed=42)`:
  - Accepts `metrics_df`, aggregates revenue per product
  - Generates `quality_score` via existing `generate_quality_score()`
  - Assigns treatment to top `treatment_fraction` by quality (deterministic selection — struggling products get optimized)
  - Returns DataFrame with `product_identifier, quality_score, D, Y0, Y1, Y_observed`
- This replaces the inline treatment assignment currently in cells 36–37

### 1B. Remove dead functions from `support.py`
**File:** same
- Delete: `plot_treatment_parameters`, `plot_bias_decomposition`, `plot_bootstrap_distribution`, `plot_outcome_by_treatment`
- These are never imported in the notebook

### 1C. Restructure Part II notebook cells
**File:** `docs/source/measure-impact/01-potential-outcomes-model/lecture.ipynb`

Strip outputs first, then restructure Part II into 6 sections:

**Section 1: Business Context** (reuse current cell 9 content)
- "What would be the effect on sales if we improved product content quality?"

**Section 2: Data Generation**
- `simulate()` + `load_job_results()` → baseline metrics
- `Code(inspect.getsource(create_confounded_treatment), language="python")` — show selection mechanism
- Call `create_confounded_treatment(metrics)` → `confounded_products`
- Print treatment/control counts

**Section 3: Naive Comparison**
- Compute `E[Y|D=1] - E[Y|D=0]` on confounded data
- Show biased estimate, note it underestimates (or wrong sign)
- Explain using Part I's selection bias decomposition: $E[Y|D=1] - E[Y|D=0] = \text{ATE} + \text{Selection Bias} + \text{HTE Bias}$

**Section 4: The Simulator's Advantage — Known Potential Outcomes**
- Access `Y0`, `Y1` columns directly (the "god's eye view")
- Compute true ATE, ATT, ATC from potential outcomes
- Numerically verify the bias decomposition formula
- Show fundamental problem table (what we observe vs what's hidden)

**Section 5: Randomization Recovers the Truth**
- Create randomly assigned treatment (use enrichment pipeline or simple random assignment)
- Show naive estimator is now unbiased (E[Y|D=1] - E[Y|D=0] ≈ true ATE)
- Covariate balance check: quality_score distributions equal across groups

**Section 6: Diagnostics & Extensions**
- Monte Carlo: 500 simulations comparing random vs biased assignment distributions
- Sample size convergence: SE ∝ 1/√n demonstration

### 1D. Keep enrichment pipeline for random treatment
- The `enrich()` call with `config_enrichment_random.yaml` stays for Section 5 (randomization)
- It's pedagogically useful to show how the simulator handles random assignment
- Confounded treatment uses the new `support.py` function (Section 2)

---

## Cross-Lecture Notation Standardization

### N1. Independence symbol
- **Standard:** `\perp\!\!\!\perp` for unconditional; `\perp\!\!\!\perp` with `\mid` for conditional
- L01 cell 7: already uses `\perp\!\!\!\perp` — correct
- L03 cell 2: change `\perp` → `\perp\!\!\!\perp` (two occurrences in CIA definition)
- L02: no independence symbols (DAG-only) — no change needed

### N2. Treatment effect symbol
- All three lectures use δ (delta) — **already consistent**
- The earlier review incorrectly flagged τ (tau) in L02; exploration confirmed L02 uses `\hat{\tau}` in cell 20 for the naive/conditional estimators
- **Fix:** L02 cell 20: change `\hat{\tau}_{\text{naive}}` → `\hat{\delta}_{\text{naive}}` and `\hat{\tau}_{\text{conditional}}` → `\hat{\delta}_{\text{conditional}}`

### N3. Part I section numbering
- **Standard:** Numbered headers (`## 1. Title`) — matches L02 and L03 (majority)
- L01 Part I: add numbers to main section headers
  - `## The Potential Outcome Framework` → `## 1. The Potential Outcome Framework`
  - `## The Fundamental Problem of Causal Inference` → `## 2. The Fundamental Problem of Causal Inference`
  - etc. for remaining Part I sections

---

## Execution Order

1. **L03 quick fixes** (3A–3F) — lowest risk, validates the pattern
2. **L02 moderate changes** (2A–2E)
3. **L01 major restructure** (1A–1D)
4. **Cross-lecture notation** (N1–N3) — do last since L01/L02 cells may shift
5. **Verify:** `hatch run pytest` after each lecture

---

## Verification

After all changes:
```bash
hatch run jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace docs/source/measure-impact/*/lecture.ipynb
hatch run ruff format docs/source/measure-impact/*/support.py
hatch run ruff check docs/source/measure-impact/*/support.py
hatch run pytest
```

Success criteria:
- All 4 notebooks pass `nbmake` tests
- `ruff format` and `ruff check` clean
- Each lecture's Part II follows the 6-step pattern (adapted for L01's scope)
- All `support.py` treatment functions accept `metrics_df`, return `D/Y0/Y1/Y_observed`
- `inspect.getsource()` used for treatment function in all three lectures
- Notation consistent: `\perp\!\!\!\perp`, `\hat{\delta}`, numbered Part I headers
