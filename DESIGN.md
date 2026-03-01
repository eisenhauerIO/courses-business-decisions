# Design: Impact-Driven Business Decisions Course

## Motivation

Most organizations collect data and generate insights but lack the methods and
systems to connect those insights to decisions. This course addresses that gap
through a single organizing principle — Learn, Decide, Repeat — which structures
every lecture, tool, and assignment around the feedback loop between measurement,
evaluation, and action.

The course is designed as a Sphinx documentation site where every lecture is a
self-contained Jupyter notebook that executes during build. This ensures
reproducibility: all code runs, all outputs are current, and broken notebooks
fail the build.

## Architecture overview

```
┌────────────────────────────────────────────────────────┐
│                  Course Repository                     │
│                                                        │
│  docs/source/                                          │
│  ├── Understand Domain (context + data)                │
│  ├── Measure Impact (causal inference methods)         │
│  ├── Evaluate Evidence (evidence quality assessment)   │
│  ├── Allocate Resources (decision theory)              │
│  └── Build Systems (software engineering)              │
│                                                        │
│  External Tools (pip-installed from GitHub):            │
│  ├── online-retail-simulator (data generation)         │
│  ├── impact-engine-measure (causal estimation)         │
│  └── impact-engine-evaluate (evidence review)          │
│                                                        │
│  Build Pipeline:                                       │
│  hatch run build → Sphinx + nbsphinx → GitHub Pages   │
└────────────────────────────────────────────────────────┘
```

The course follows a domain-driven structure where each top-level section maps
to a stage in the Learn, Decide, Repeat loop. Lectures within each section
progress from foundational theory to applied methods.

## Components

### Lecture notebooks

Each lecture follows a two-part structure:

| Part | Purpose | Typical content |
|------|---------|-----------------|
| **Part I — Theory** | Introduce the method formally | Definitions, assumptions, mathematical framework, worked examples with synthetic data |
| **Part II — Application** | Apply the method to a realistic scenario | Online Retail Simulator data, configuration files, tool integration, results interpretation |

Part II bridges theory to practice through an interface-to-theory mapping table
that links tool configuration parameters back to the formal concepts from Part I.

### Support modules

| File | Scope |
|------|-------|
| `measure-impact/01-potential-outcomes-model/support.py` | POM plotting and confounding helpers |
| `measure-impact/02-directed-acyclic-graphs/support.py` | DAG lecture support functions |
| `measure-impact/03-matching-subclassification/support.py` | Matching and subclassification helpers |
| `measure-impact/08-synthetic-control/support.py` | Synthetic control method helpers |
| `measure-impact/shared.py` | Cross-lecture utilities (e.g., `plot_method_comparison`) |
| `evaluate-evidence/03-application/support.py` | Application lecture helpers |
| `understand-domain/02-catalog-ai/support.py` | Catalog AI lecture support |

### Configuration files

YAML files configure the external tools for each lecture's application section:

| File pattern | Tool | Purpose |
|-------------|------|---------|
| `config_simulation.yaml` | Online Retail Simulator | Product catalog, sales, treatment parameters |
| `config_enrichment*.yaml` | Online Retail Simulator | Content enrichment scenarios |
| `config_matching.yaml` | Impact Engine Measure | Matching estimator settings |
| `config_subclassification.yaml` | Impact Engine Measure | Subclassification estimator settings |
| `config_synthetic_control.yaml` | Impact Engine Measure | Synthetic control estimator settings |
| `config_experiment.yaml` | Impact Engine Measure | Experimental estimator settings |

### CI/CD pipelines

| Workflow | Trigger | Steps |
|----------|---------|-------|
| `ci.yml` | Push/PR to main | Ruff lint + format check |
| `docs.yml` | Push/PR to main | Sphinx build (all notebooks execute), deploy to GitHub Pages on main |

## Data flow

### Build pipeline

```
Author writes lecture.ipynb + support.py + config_*.yaml
        │
        ▼
hatch run build
        │
        ├── Sphinx reads docs/source/**
        ├── nbsphinx executes each .ipynb
        │   ├── Notebook imports from online_retail_simulator, impact_engine
        │   ├── Runs simulation with config_simulation.yaml
        │   ├── Applies causal inference methods
        │   └── Generates plots and tables
        ├── myst-parser renders .md files
        └── Output: docs/build/html/
                │
                ▼
        GitHub Pages (docs.yml deploys on main)
```

### Lecture data flow (within a notebook)

```
config_simulation.yaml → simulate() → DataFrame
        │
        ▼
config_*.yaml → impact_engine method → effect estimates
        │
        ▼
support.py plotting functions → visualizations
```

## Configuration

### Sphinx (`docs/source/conf.py`)

| Setting | Value | Purpose |
|---------|-------|---------|
| `nbsphinx_execute` | `"always"` | Execute all notebooks during build |
| `nbsphinx_allow_errors` | `False` | Fail build on notebook errors |
| `html_theme` | `"sphinx_rtd_theme"` | Read the Docs theme |
| `bibtex_bibfiles` | `["references.bib"]` | Academic citations |
| `todo_include_todos` | Conditional on `SPHINX_PROD` | Show TODOs locally, hide in production |

### Hatch (`pyproject.toml`)

See Common commands in CLAUDE.md. The hatch environment manages all dependencies
including the three GitHub-hosted packages.

### Ruff (`pyproject.toml`)

| Setting | Value |
|---------|-------|
| `line-length` | 120 |
| `select` | D (docstrings), E, F (pyflakes), I (isort) |
| `extend-exclude` | `_external` |
| `*.ipynb` overrides | D, E402, F, I disabled |

## Future directions

- **Allocate Resources lectures**: Decision theory content (currently a placeholder section)
- **Additional causal methods**: Difference-in-differences, instrumental variables, regression discontinuity
- **Interactive elements**: Widgets or Voila dashboards for parameter exploration within notebooks
- **Assessment integration**: Auto-graded assignments using nbgrader or similar
- **Cross-lecture summaries**: Automated method comparison pages generated from lecture outputs
