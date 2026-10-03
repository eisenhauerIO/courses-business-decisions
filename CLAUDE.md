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
- `hatch run ruff check .` — lint all Python files
- `hatch run ruff format --check .` — check formatting

## Architecture

- `docs/source/` — all course content (Sphinx site root)
  - `conf.py` — Sphinx configuration (nbsphinx, myst-parser, sphinxcontrib-bibtex)
  - `index.md` — landing page with toctree
  - `measure-impact/` — causal inference lectures (potential outcomes, DAGs, matching, synthetic control)
  - `evaluate-evidence/` — evidence quality lectures (evaluation framework, agentic systems, application)
  - `understand-domain/` — domain context lectures (catalog AI)
  - `allocate-resources/` — decision theory lectures (portfolio optimization)
  - `iterations/index.md` — current delivery's details plus a table of past iterations (new term: move the current one into the table)
  - `decision-loop/`, `build-systems/`, `guests/`, `projects/`, `software/` — supporting sections
  - `references.bib` — bibliography
- `docs/source/_static/` — images and SVGs referenced by lectures and index pages
- `../../tools/` — workspace clones of the tool repos (separate projects, do not modify from here)
  - `impact-engine-measure/` — causal estimation source
  - `impact-engine-evaluate/` — evidence review source
  - `impact-engine-allocate/` — resource allocation source
- `.github/workflows/ci.yml` — ruff linting on push/PR
- `.github/workflows/docs.yml` — Sphinx build + GitHub Pages deploy on push to main
- `.claude/skills/` — course-specific skills (bdc-author-lecture, bdc-review-course, and course forks of bdc-review-code and bdc-review-writing); shared skills live in the workspace `.claude/skills/`

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
- `impact-engine-allocate` — portfolio allocation under uncertainty (GitHub)

All installed via pip from GitHub (see pyproject.toml). Never use `sys.path.insert`.

## Verification

Push directly to main; no feature branches or PRs.

1. Lint locally: `hatch run ruff check . && hatch run ruff format --check .`
2. For lecture changes, execute the notebook: `hatch run notebook path/to/lecture.ipynb`
3. Commit and push to main: `git push`
4. Watch CI (ci.yml: linting, docs.yml: Sphinx build + deploy) and fix forward on failure: `gh run watch`

## Key conventions

- Follow writing conventions in `docs/source/GUIDELINES.md` when editing lecture content
- Notebooks execute during Sphinx build (`nbsphinx_execute = "always"`) — all cells must run cleanly
- Part II imports: `from online_retail_simulator import simulate, load_job_results`
- Tool repos under `../../tools/` are separate projects — change them in their own repos, never from here
- Ruff enforces D (docstrings), E, F (pyflakes), I (isort) rules; line length 120
- NumPy-style docstrings for all Python functions
- `print()` is allowed in `support.py` display functions and notebook cells for lecture output; avoid `print()` in library/utility code outside lecture directories
