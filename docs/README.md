# Docs for Business Decisions course

Build locally (pip venv):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r docs/requirements.txt
sphinx-build -b html docs/source docs/_build/html
```

Or using conda (recommended for reproducibility):

```bash
conda env create -f environment.yml
conda activate business-decisions-docs
sphinx-build -b html docs/source docs/_build/html
```

This repo uses `docs/source/conf.py` as the Sphinx configuration. Read the `.readthedocs.yaml` at the repo root for RTD configuration.
