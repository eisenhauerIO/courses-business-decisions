# CLAUDE.md

## Project overview

Course materials for "Impact-Driven Business Decisions" — a university course that teaches causal inference, evidence evaluation, decision theory, and software engineering through the lens of a single organizing principle: Learn, Decide, Repeat. All lectures are Jupyter notebooks built and deployed as a Sphinx documentation site via GitHub Pages.

## Development setup

All commands use the hatch environment. Never use bare `python` or `pip`.

```bash
pip install hatch "virtualenv<21"
```

Before editing a `.ipynb` file, strip its outputs first:

```bash
hatch run jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace path/to/notebook.ipynb
```

## Common commands

- `hatch run build` — build Sphinx documentation to `docs/build/html`
- `hatch run notebook {path}` — execute a single notebook in place
- `hatch run notebooks` — find and execute all notebooks
- `hatch run slides` — convert lecture notebooks to reveal.js slides
- `ruff check .` — lint all Python files
- `ruff format --check .` — check formatting

## Architecture

- `docs/source/` — all course content (Sphinx site root)
  - `conf.py` — Sphinx configuration (nbsphinx, myst-parser, sphinxcontrib-bibtex)
  - `index.md` — landing page with toctree
  - `measure-impact/` — causal inference lectures (potential outcomes, DAGs, matching, synthetic control)
  - `evaluate-evidence/` — evidence quality lectures (evaluation framework, agentic systems, application)
  - `understand-domain/` — domain context lectures (catalog AI)
  - `overview/`, `build-systems/`, `guest-lecturers/`, `course-projects/`, `software/`, `iterations/`, `allocate-resources/` — supporting sections
  - `references.bib` — bibliography
- `docs/source/_static/` — images and SVGs referenced by lectures and index pages
- `_external/` — local clones of dependency repos (read-only, do not modify)
  - `tools-online-retail-simulator/` — simulator source
  - `tools-impact-engine-measure/` — causal estimation source
  - `tools-impact-engine-evaluate/` — evidence review source
  - `utils-agentic-support/` — shared Claude Code skills and subagents
  - `books-mixtape/` — Causal Inference: The Mixtape reference
- `.github/workflows/ci.yml` — ruff linting on push/PR
- `.github/workflows/docs.yml` — Sphinx build + GitHub Pages deploy on push to main
- `.claude/skills/` — Claude Code skill definitions
- `.claude/subagents/` — symlinked subagent definitions (design-reviewer, doc-generator, test-writer)

### Lecture directory convention

Each measure-impact lecture is a self-contained directory:

```
XX-topic-name/
├── lecture.ipynb           # main notebook (Theory Part I, Application Part II)
├── support.py              # helper functions for the lecture
├── config_simulation.yaml  # simulator configuration
└── config_*.yaml           # additional tool configurations
```

Evaluate-evidence and understand-domain lectures follow the same `lecture.ipynb` pattern but may omit `support.py` or config files when not needed.

### Dependencies

- `online-retail-simulator` — synthetic retail data generation (GitHub)
- `impact-engine-measure` — causal effect estimation (GitHub)
- `impact-engine-evaluate` — LLM-powered evidence review (GitHub)

All installed via pip from GitHub (see pyproject.toml). Never use `sys.path.insert`.

## Verification

All work happens on a feature branch. Push, wait for CI to pass, then merge to main.

```bash
# 1. Create a feature branch and do all work there
git checkout -b feature/description

# 2. Commit and push
git push -u origin feature/description

# 3. Wait for CI to pass (ci.yml: linting, docs.yml: Sphinx build)
gh run watch

# 4. Merge to main only after CI passes
git checkout main && git merge feature/description && git push
```

## Key conventions

- Notebooks execute during Sphinx build (`nbsphinx_execute = "always"`) — all cells must run cleanly
- Lectures follow Theory (Part I) then Application (Part II) structure
- Part II imports: `from online_retail_simulator import simulate, load_job_results`
- Show source code with `inspect.getsource()` + `Code()` from IPython.display
- `_external/` contains reference repos — do not modify
- Ruff enforces D (docstrings), E, F (pyflakes), I (isort) rules; line length 120
- NumPy-style docstrings for all Python functions
- No `print()` statements — use logging or IPython display utilities
