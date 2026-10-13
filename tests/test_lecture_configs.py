"""Validate lecture configs against the installed Online Retail Simulator.

Some lectures (catalog AI) are never executed in CI because they need a local LLM.
These checks catch simulator API changes that would break them, without running them.
"""

from pathlib import Path

import pytest
import yaml
from online_retail_simulator import list_enrichment_functions
from online_retail_simulator.config_processor import process_config

SOURCE = Path(__file__).parents[1] / "docs" / "source"
SIMULATION_CONFIGS = sorted(SOURCE.rglob("config_simulation*.yaml"))
ENRICHMENT_CONFIGS = sorted(SOURCE.rglob("config_enrichment*.yaml"))


def test_configs_found():
    """Guard against the globs silently matching nothing."""
    assert SIMULATION_CONFIGS
    assert ENRICHMENT_CONFIGS


@pytest.mark.parametrize("path", SIMULATION_CONFIGS, ids=lambda p: str(p.relative_to(SOURCE)))
def test_simulation_config_is_valid(path):
    """Each simulation config passes the simulator's own validation."""
    process_config(str(path))


@pytest.mark.parametrize("path", ENRICHMENT_CONFIGS, ids=lambda p: str(p.relative_to(SOURCE)))
def test_enrichment_function_is_registered(path):
    """Each enrichment config names a registered impact function."""
    config = yaml.safe_load(path.read_text())
    assert config["IMPACT"]["FUNCTION"] in list_enrichment_functions()
