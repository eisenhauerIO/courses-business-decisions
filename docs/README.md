# Docs for Business Decisions course

This project uses [Hatch](https://hatch.pypa.io/) for environment and dependency management.

## Building Documentation

Build the Sphinx documentation:
```bash
hatch run build
```

The built documentation will be in `docs/build/html/`.

## Serving Documentation Locally

Serve the documentation on `http://localhost:8000`:
```bash
hatch run serve
```

## Cleaning Build Artifacts

Remove the build directory:
```bash
hatch run clean
```

---

This repo uses `docs/source/conf.py` as the Sphinx configuration. Read the `.readthedocs.yaml` at the repo root for RTD configuration.
