# Review Feedback — Phases 0 & 1

**Status**: complete

## Goal

Close the remaining review feedback items from BACKLOG Phases 0 (high priority)
and 1 (medium priority). These are systematic patterns and one-off fixes
identified during the full course review.

## Scope

**In scope**:
- Add `optional` markers to docstring params with defaults (support.py: 01, 02, 03, catalog-ai)
- Add notation tables to Business Context sections (lectures 02, 03)
- Fix import alphabetization in notebook import cells (lectures 01, 03, 08)
- Verify `github-workflow` toctree entry resolves Sphinx warning
- Move misplaced `import pandas as pd` in lecture 02
- Add "god's eye view" framing in lecture 02

**Out of scope**:
- Phase 2 content proposals (presentation order, narrative changes)
- Phase 3 low-priority polish
- New lecture content
- Changes to `_external/` packages

## Observations

### 1. Docstring `optional` markers

Support modules (01, 02, 03, catalog-ai) have parameters with defaults but no
`, optional` annotation in NumPy-style docstrings.

### 2. Notation tables

Lectures 02 and 03 lack Variable | Notation | Description tables in Business
Context sections, unlike lecture 08 which has one.

### 3. Import alphabetization

Lectures 01, 03, and 08 flagged for potentially unalphabetized imports.

### 4. `github-workflow` toctree

Sphinx warning about orphaned `github-workflow` page in course-projects.

### 5. Misplaced import in lecture 02

`import pandas as pd` appears in cell 40 instead of the main Part II import cell.

### 6. Missing framing in lecture 02

Lecture 02 Part II introduction lacks "god's eye view" language connecting
simulation to potential outcomes framework.

## Decisions

### 1. Docstring `optional` markers

Add `, optional` to all parameters with default values across four support modules.

### 2. Notation tables

Add tables to lectures 02 and 03, using lecture 08 as the reference template.

### 3. Import alphabetization

Verify with `ruff check`; fix only if isort rules are violated.

### 4. `github-workflow` toctree

Add hidden toctree directive to `docs/source/course-projects/index.md`.

### 5. Misplaced import in lecture 02

Move `import pandas as pd` from cell 40 to the main Part II import cell (21).

### 6. Missing framing in lecture 02

Add "god's eye view" language to Part II introduction.

## Plan

1. Add `, optional` to docstring params with defaults in support.py files (01, 02, 03, catalog-ai)
2. Add notation tables to Business Context cells in lectures 02 and 03
3. Verify import order with `ruff check` in lectures 01, 03, 08
4. Add hidden toctree directive for `github-workflow` in course-projects/index.md
5. Move `import pandas as pd` to Part II import cell in lecture 02
6. Add "god's eye view" framing to lecture 02 Part II introduction

## Verification

1. `ruff check .` — pass ✓
2. `ruff format --check .` — pass ✓
3. `hatch run build` — pass ✓

## Files modified

- `docs/source/measure-impact/01-potential-outcomes-model/support.py`
- `docs/source/measure-impact/02-directed-acyclic-graphs/support.py`
- `docs/source/measure-impact/02-directed-acyclic-graphs/lecture.ipynb`
- `docs/source/measure-impact/03-matching-subclassification/support.py`
- `docs/source/measure-impact/03-matching-subclassification/lecture.ipynb`
- `docs/source/measure-impact/08-synthetic-control/lecture.ipynb`
- `docs/source/understand-domain/02-catalog-ai/support.py`
- `docs/source/course-projects/index.md`
