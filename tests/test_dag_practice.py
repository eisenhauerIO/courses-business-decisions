"""Check the answer keys of the DAG practice cards against the backdoor criterion.

Each card states its valid conditioning sets in a "**Valid sets:**" line. These tests recompute the
valid sets from the graph with networkx, so a wrong or mistyped answer key fails the build.
"""

import itertools
import json
import re
from pathlib import Path

import networkx as nx
import pytest

NOTEBOOK = Path(__file__).parents[1] / "docs/source/measure-impact/02-directed-acyclic-graphs/practice.ipynb"

# Card number -> (edges, unobserved nodes); must match the figures in practice/
GRAPHS = {
    1: ([("X", "D"), ("X", "Y"), ("D", "Y")], set()),
    2: ([("D", "M"), ("M", "Y"), ("D", "Y")], set()),
    3: ([("B", "A"), ("A", "D"), ("B", "Y"), ("D", "Y")], set()),
    4: ([("A", "D"), ("A", "C"), ("B", "C"), ("B", "Y"), ("D", "Y")], set()),
    5: ([("X", "D"), ("X", "Y"), ("D", "Y"), ("D", "C"), ("Y", "C")], set()),
    6: ([("U", "X"), ("X", "D"), ("U", "Y"), ("D", "Y")], {"U"}),
    7: ([("A", "D"), ("A", "C"), ("B", "C"), ("B", "Y"), ("C", "D"), ("C", "Y"), ("D", "Y")], set()),
    8: ([("D", "M"), ("M", "Y"), ("D", "Y"), ("U", "M"), ("U", "Y")], {"U"}),
}


def satisfies_backdoor_criterion(graph, z):
    """Return whether *z* satisfies the backdoor criterion for the effect of D on Y."""
    if z & nx.descendants(graph, "D"):
        return False
    backdoor_graph = graph.copy()
    backdoor_graph.remove_edges_from(list(graph.out_edges("D")))
    return nx.is_d_separator(backdoor_graph, {"D"}, {"Y"}, z)


def valid_sets(edges, unobserved):
    """Return every set of observed variables that satisfies the backdoor criterion."""
    graph = nx.DiGraph(edges)
    candidates = sorted(set(graph) - {"D", "Y"} - unobserved)
    subsets = itertools.chain.from_iterable(itertools.combinations(candidates, r) for r in range(len(candidates) + 1))
    return {frozenset(z) for z in subsets if satisfies_backdoor_criterion(graph, set(z))}


def stated_answers():
    """Return the valid sets each card states, keyed by card number."""
    cells = json.loads(NOTEBOOK.read_text())["cells"]
    answers = {}
    for cell in cells:
        text = "".join(cell["source"])
        card = re.match(r"## Card (\d+)", text)
        if card:
            line = re.search(r"\*\*Valid sets:\*\* (.+)", text).group(1)
            answers[int(card.group(1))] = {
                frozenset(m.strip() for m in group.split(",") if m.strip())
                for group in re.findall(r"\{([^}]*)\}", line)
            }
    return answers


def test_every_card_has_a_graph():
    """Guard against cards and graphs drifting apart."""
    assert set(stated_answers()) == set(GRAPHS)


@pytest.mark.parametrize("card", sorted(GRAPHS))
def test_stated_valid_sets_are_correct(card):
    """Each card's stated valid sets match the backdoor criterion."""
    edges, unobserved = GRAPHS[card]
    assert stated_answers()[card] == valid_sets(edges, unobserved)
