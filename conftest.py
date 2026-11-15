"""Pytest configuration for notebook testing."""

import pytest

# Notebooks that need a local LLM (Ollama); skipped unless run with -m slow
SLOW_NOTEBOOKS = [
    "docs/source/understand-domain/02-catalog-ai/lecture.ipynb",
    "docs/source/evaluate-evidence/03-application/lecture.ipynb",
]


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    """Mark notebooks that need a local LLM as slow, and skip them unless run with -m slow.

    Runs before pytest's own marker selection, so ``-m slow`` sees the marker.
    """
    run_slow = "slow" in (config.getoption("-m") or "")
    skip_slow = pytest.mark.skip(reason="needs a local LLM (Ollama), use -m slow to run")
    for item in items:
        if any(nb in str(item.fspath) for nb in SLOW_NOTEBOOKS):
            item.add_marker(pytest.mark.slow)
            if not run_slow:
                item.add_marker(skip_slow)
