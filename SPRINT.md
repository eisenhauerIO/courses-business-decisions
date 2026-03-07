# Allocate Resources — Portfolio Optimization Lecture

**Status**: collecting

## Goal

Author the first lecture in the `allocate-resources/` section: a two-part notebook covering decision theory for portfolio selection (Part I) and an end-to-end application using `impact-engine-allocate` (Part II). This addresses the BACKLOG gap of the empty allocate-resources section.

## Scope

**In scope**:
- Create `01-portfolio-optimization/lecture.ipynb` with Part I (theory) and Part II (application)
- Create `01-portfolio-optimization/support.py` with mock data and visualization helpers
- Create `01-portfolio-optimization/config_allocation.yaml` with budget/constraint parameters
- Update `allocate-resources/index.md` to match measure-impact/evaluate-evidence structure
- Add `impact-engine-allocate` dependency to `pyproject.toml`

**Out of scope**:
- Changes to `_external/` packages
- Additional allocate-resources lectures beyond 01
- Modifications to evaluate-evidence or measure-impact content
- Feature branch / CI workflow

## Observations

### 1. Primary source is Eisenhauer (2025) paper
Part I theory follows the paper's notation (Appendix A1), mathematical formulations (equations 1-6), and simulation example (Tables 1-2). This parallels how measure-impact lectures follow the Mixtape.

### 2. Lecture follows evaluate-evidence 03-application pattern
The closest structural template is `evaluate-evidence/03-application/lecture.ipynb`: Part I develops theory, Part II applies the tool end-to-end on mock data (not the Online Retail Simulator).

### 3. index.md needs full rewrite to match sibling sections
Current `index.md` has only a title, figure, one paragraph, and a warning block. Measure-impact and evaluate-evidence both follow a 7-part structure: title → figure → framing → organizational overview → section header → lecture summary → toctree.

### 4. impact-engine-allocate not yet in pyproject.toml
The package exists in `_external/tools-impact-engine-allocate/` but is not listed as a dependency.

### 5. Mock data should match paper's simulation example
Paper Table 1 defines 5 initiatives (A-E) with exact costs, returns, and confidence values. Using these values enables students to verify Part II results against the paper.

### 6. Paper uses specific notation system
Appendix A1 defines: $I$, $S$, $x_i$, $\mathbf{x}$, $\theta$, $B$, $b_i$, $c_i$, $c_\min$, $\gamma_i$, $R_{ij}$, $R_i^\min$, $\hat{R}_{ij}$, $P_j(\mathbf{x})$, $\hat{V}_j^*$, $\text{Regret}_j(\mathbf{x})$, $R_\min^\text{portfolio}$.

## Decisions

### 1. Use paper as primary theory source
Part I notation, formulations, and worked examples follow Eisenhauer (2025) exactly, just as measure-impact follows the Mixtape.

### 2. Follow evaluate-evidence 03-application structure
Part I: theory sections. Part II: imports → mock data → confidence penalty → preprocessing → theory-to-code mapping → minimax regret → Bayesian → comparison → sensitivity analysis → additional resources.

### 3. Rewrite index.md to match sibling pattern
Full 7-part structure with organizational overview paragraph, section header, lecture summary, and toctree. Remove warning block.

### 4. Add dependency to pyproject.toml
`"impact-engine-allocate @ git+https://github.com/eisenhauerIO/tools-impact-engine-allocate.git"`

### 5. Use paper Table 1 data in mock portfolio
5 initiatives (A-E) with paper's exact values. Budget=10, min_confidence=0.50, min_worst_return=3.

### 6. Use paper notation throughout
All LaTeX in Part I follows Appendix A1 notation.

## Plan

### Phase 1: Infrastructure
1. Add `impact-engine-allocate` to `pyproject.toml`
2. Verify import works: `hatch run python -c "from impact_engine_allocate import solve_minimax_regret"`
3. Create `docs/source/allocate-resources/01-portfolio-optimization/` directory

### Phase 2: Support code
4. Write `support.py` with 6 functions:
   - `create_mock_portfolio()` — 5 initiatives matching paper Table 1
   - `display_solver_result(result, rule_name)` — formatted SolverResult output
   - `plot_confidence_penalty(initiatives)` — base vs effective returns grouped bars
   - `plot_effective_returns_heatmap(processed)` — initiatives × scenarios heatmap
   - `plot_scenario_returns(result, title)` — portfolio scenario returns with V_j* overlay
   - `plot_portfolio_comparison(all_results)` — decision rules side-by-side comparison
5. Write `config_allocation.yaml` (budget=10, min_confidence=0.50, min_worst_return=3)

### Phase 3: Notebook
6. Write `lecture.ipynb` Part I — 5 theory sections using paper notation:
   - §1 The decision problem
   - §2 Scenario-dependent returns
   - §3 The confidence penalty
   - §4 Minimax regret optimization
   - §5 Bayesian decision rule
7. Write `lecture.ipynb` Part II — 9 application sections + Additional resources:
   - §1 Initiative data (mock portfolio from Table 1)
   - §2 Configuration
   - §3 The confidence penalty (verify against Table 2)
   - §4 Preprocessing
   - §5 From theory to code (interface-to-theory mapping table)
   - §6 Minimax regret (verify: selected={A,C,E}, θ*=1.0)
   - §7 Bayesian solver (3 weight profiles)
   - §8 Comparing decision rules
   - §9 How confidence shapes allocation (incentive effect)
   - Additional resources

### Phase 4: index.md
8. Rewrite `allocate-resources/index.md` — full 7-part structure matching siblings

### Phase 5: Verification
9. `hatch run notebook docs/source/allocate-resources/01-portfolio-optimization/lecture.ipynb`
10. `ruff check .` and `ruff format --check .`
11. `/review-writing` on notebook markdown cells
12. `/review-code` on notebook code cells and support.py
13. `hatch run build`

## Files modified

- `pyproject.toml` — add impact-engine-allocate dependency
- `docs/source/allocate-resources/index.md` — rewrite to match sibling structure
- `docs/source/allocate-resources/01-portfolio-optimization/lecture.ipynb` (new)
- `docs/source/allocate-resources/01-portfolio-optimization/support.py` (new)
- `docs/source/allocate-resources/01-portfolio-optimization/config_allocation.yaml` (new)

## Verification

1. `hatch run python -c "from impact_engine_allocate import solve_minimax_regret"` — dependency installed
2. `hatch run notebook docs/source/allocate-resources/01-portfolio-optimization/lecture.ipynb` — all cells execute
3. `ruff check .` — lint passes
4. `ruff format --check .` — format passes
5. `/review-writing` — prose quality, formatting, style checks on notebook markdown cells
6. `/review-code` — Python quality checks on notebook code cells and support.py
7. `hatch run build` — Sphinx builds cleanly
