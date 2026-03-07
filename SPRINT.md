# Review Feedback — Phases 0 & 1

**Status**: done

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

## Tasks

### 1. Docstring `optional` markers ✓

Added `, optional` to all parameters with default values in NumPy-style docstrings.

Files:
- `docs/source/measure-impact/01-potential-outcomes-model/support.py`
- `docs/source/measure-impact/02-directed-acyclic-graphs/support.py`
- `docs/source/measure-impact/03-matching-subclassification/support.py`
- `docs/source/understand-domain/02-catalog-ai/support.py`

### 2. Notation tables ✓

Added Variable | Notation | Description tables to the Business Context markdown
cells in:
- `docs/source/measure-impact/02-directed-acyclic-graphs/lecture.ipynb`
- `docs/source/measure-impact/03-matching-subclassification/lecture.ipynb`

Used `08-synthetic-control/lecture.ipynb` as the reference template.

### 3. Import alphabetization ✓

Verified imports pass `ruff check` in all three notebooks. No changes needed —
existing order follows isort conventions (bare `import` before `from` imports,
each group alphabetized).

### 4. `github-workflow` toctree ✓

Added hidden toctree directive to `docs/source/course-projects/index.md`
including `github-workflow`.

### 5. Misplaced `import pandas as pd` in lecture 02 ✓

Moved `import pandas as pd` from cell 40 to the main Part II import cell (21)
in `docs/source/measure-impact/02-directed-acyclic-graphs/lecture.ipynb`.

### 6. "God's eye view" framing in lecture 02 ✓

Added "god's eye view" language to the Part II introduction in
`docs/source/measure-impact/02-directed-acyclic-graphs/lecture.ipynb`.

## Verification

1. `ruff check .` — pass ✓
2. `ruff format --check .` — pass ✓
3. `hatch run build` — pending

## Files modified

- `docs/source/measure-impact/01-potential-outcomes-model/support.py`
- `docs/source/measure-impact/02-directed-acyclic-graphs/support.py`
- `docs/source/measure-impact/02-directed-acyclic-graphs/lecture.ipynb`
- `docs/source/measure-impact/03-matching-subclassification/support.py`
- `docs/source/measure-impact/03-matching-subclassification/lecture.ipynb`
- `docs/source/measure-impact/08-synthetic-control/lecture.ipynb`
- `docs/source/understand-domain/02-catalog-ai/support.py`
- `docs/source/course-projects/index.md`
