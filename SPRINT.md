# Portfolio optimization lecture — writing and structure

**Status**: verifying

## Goal

Tighten prose and structure in the portfolio optimization lecture
(`allocate-resources/01-portfolio-optimization/`) to comply with GUIDELINES.md.
Related to BACKLOG Phase 0 — Polish.

## Scope

**In scope**:
- Prose quality: active voice, narrative flow, sentence case headers
- GUIDELINES.md compliance: bold on first introduction only, no definition patterns
- Additional resources formatting
- Cell-level structure and transitions

**Out of scope**:
- New theoretical content or sections
- Opening hook or workflow diagram (deferred)
- Changes to `impact_engine_allocate` package
- Changes to `_external/` repos
- Changes to support.py visualizations or code logic
- Other lectures or index files

## Observations

### 1. Definition patterns in Part I

Cells 2–4 use glossary-style "X is Y" definitions: "The **baseline return** $R_{ij}$
is the net return...", "The **penalty factor** $\gamma_i$ is a monotonically
decreasing function...", "The **regret** of portfolio $\mathbf{x}$ under scenario
$s_j$ is the gap...". GUIDELINES.md says to weave explanations into flowing narrative.

### 2. Bold terms not introduced on first mention

Cell 2 introduces "baseline return" and "worst-case return" as key concepts but does
not bold them on first appearance (they appear in plain text before the math definition).

### 3. Additional resources format incomplete

Cell 42 lists references without linked titles or publication metadata. GUIDELINES.md
requires: **Author (Year)**. `[Title](url)`. *Journal*, volume(issue), pages.

### 4. Part II transitions could be tighter

Some Part II markdown cells restate what the reader already knows from Part I rather
than connecting forward. For example, cell 15 ("Before solving, we apply the confidence
penalty from Part I, §3") could be more concise.

### 5. Prose density in intro paragraph

Cell 0 packs three ideas into two sentences (confidence penalty, incentive effect,
Part I/II structure). Could benefit from shorter, punchier sentences.

### 7. Motivating question not highlighted

Cell 0 poses a strong motivating question — "which ones should we fund?" — but it is
not bolded. Other lectures follow a consistent pattern: the central question is bolded
inline (e.g. "We apply these concepts to answer: **What would be the effect on sales
if we improved product content quality?**"). The portfolio lecture should follow the
same convention.

### 8. Effective returns displayed as print loop

Cell 16 shows effective returns with a manual print loop. Cell 10 already uses a
`DataFrame` for the initiative data. The effective returns should also be a DataFrame
for consistency and readability.

### 9. Initiative names not bold in prose

Initiative names (TitlesAI, ImageEnhancer, PriceOptimizer, SearchRanker, BundleEngine)
are program/project names and should be **bold** when referenced in markdown cells.
Currently they appear in plain text (e.g. cell 11: "TitlesAI has the highest
confidence...").

### 6. Config loading is verbose and redundant

Cell 13 shows the raw YAML with `! cat config_allocation.yaml`. Cell 14 then loads the
same file, unpacks three values into separate variables, and prints them — showing the
same information twice. The YAML keys (`budget`, `min_confidence`, `min_worst_return`)
don't match the `solve_minimax_regret()` parameter names (`total_budget`,
`min_confidence_threshold`, `min_portfolio_worst_return`), forcing manual unpacking.
Renaming the YAML keys to match the interface would allow
`solve_minimax_regret(initiatives, **config)` and eliminate the redundant cell.

### 10. Inconsistent solver calling pattern

The notebook uses `solve_minimax_regret()` (convenience wrapper that preprocesses
internally) for minimax, but manually calls `preprocess()` then `BayesianSolver()` for
Bayesian. Both `MinimaxRegretSolver` and `BayesianSolver` are exported at the top level.
The notebook should use the solver classes consistently: preprocess once, then call each
solver with the same pattern. This also removes the need to import
`solve_minimax_regret` and the internal `preprocess` function separately.

## Decisions

### 1. Definition patterns in Part I

Rewrite "X is Y" definitions in cells 2–4 as flowing narrative prose.

### 2. Bold terms not introduced on first mention

Bold **baseline return** and **worst-case return** on first appearance in cell 2.

### 3. Additional resources format incomplete

Add linked titles and publication metadata per GUIDELINES.md format.

### 4. Part II transitions could be tighter

Cut restated Part I content from Part II markdown cells. Keep only forward-pointing
connections.

### 5. Prose density in intro paragraph

Break cell 0 into shorter, punchier sentences.

### 6. Config loading is verbose and redundant

Rename YAML keys to match `solve_minimax_regret()` parameter names
(`total_budget`, `min_confidence_threshold`, `min_portfolio_worst_return`).
Remove the print cell (cell 14). Use `**config` in solver calls.

### 7. Motivating question not highlighted

Bold the central question inline in cell 0, matching the pattern from other lectures.

### 8. Effective returns displayed as print loop

Replace print loop in cell 16 with a `DataFrame` display.

### 9. Initiative names not bold in prose

Bold all initiative names in markdown cells throughout the notebook.

### 10. Inconsistent solver calling pattern

Use `MinimaxRegretSolver` and `BayesianSolver` classes consistently. Preprocess
once with `preprocess()`, then call each solver with the same pattern. Drop
`solve_minimax_regret` from imports.

## Plan

1. Rename YAML keys in `"config_allocation.yaml"` to match interface
2. Update notebook imports: drop `solve_minimax_regret`, keep `MinimaxRegretSolver`
3. Update notebook code cells: use `**config`, `MinimaxRegretSolver()`, remove print cell
4. Replace effective returns print loop with DataFrame
5. Rewrite Part I definition patterns as narrative prose (cells 2–4)
6. Bold key terms on first introduction (cell 2)
7. Bold motivating question in intro (cell 0)
8. Break up dense intro paragraph (cell 0)
9. Bold initiative names in all markdown cells
10. Tighten Part II transitions (cells 15, 22, 27, 29, 32)
11. Fix additional resources formatting (cell 42)
12. Strip outputs, execute notebook, verify clean run
13. Prose review pass against GUIDELINES.md

## Files modified

- `docs/source/allocate-resources/01-portfolio-optimization/lecture.ipynb`
- `docs/source/allocate-resources/01-portfolio-optimization/config_allocation.yaml`

## Verification

1. `ruff check .` — pass
2. `hatch run notebook docs/source/allocate-resources/01-portfolio-optimization/lecture.ipynb` — pass
3. `hatch run build` — pass
