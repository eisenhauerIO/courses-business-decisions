# Claude Code Project Guidelines

## Environment

Always use the hatch environment for running Python commands. Never use bare `python` or `pip`.

```bash
# Correct — always prefix with hatch run:
hatch run python -c "..."
hatch run jupyter nbconvert ...
hatch run sphinx-build ...

# Wrong — never use bare python/pip:
python -c "..."
pip install ...
```

## Jupyter Notebooks

Before editing a `.ipynb` file, strip its outputs first:

```bash
hatch run jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace path/to/notebook.ipynb
```

This avoids noisy diffs from cell outputs and keeps notebooks clean in version control.

## Project Structure

- Course documentation lives in `docs/source/`
- External dependencies (impact engine, simulator) live in `_external/`
- Both `online_retail_simulator` and `impact_engine` are installed via pip from GitHub (see pyproject.toml)
- Never use `sys.path.insert` — all dependencies should be in pyproject.toml

## Verification

All work happens on a feature branch. Push, wait for CI to pass, then merge to main.

```bash
# 1. Create a feature branch and do all work there
git checkout -b feature/description

# 2. Commit and push
git push -u origin feature/description

# 3. Wait for CI to pass
gh run watch

# 4. Merge to main only after CI passes
git checkout main && git merge feature/description && git push
```
