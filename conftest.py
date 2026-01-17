"""Pytest configuration for notebook testing."""

import pytest

SLOW_NOTEBOOKS = [
    "docs/source/understand-domain/02-catalog-ai/lecture.ipynb",
]


def pytest_collection_modifyitems(config, items):
    """Mark specific notebooks as slow and skip by default."""
    if config.getoption("-m") and "slow" in config.getoption("-m"):
        return

    skip_slow = pytest.mark.skip(reason="slow test, use -m slow to run")
    for item in items:
        if any(nb in str(item.fspath) for nb in SLOW_NOTEBOOKS):
            item.add_marker(skip_slow)
