"""Support functions for the Portfolio Optimization notebook."""

# Third-party
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# =============================================================================
# Mock Data Functions
# =============================================================================


def create_mock_portfolio():
    """
    Create a portfolio of five initiatives matching the paper's Table 1.

    Returns a list of initiative dicts with the keys expected by
    ``impact_engine_allocate``: ``id``, ``cost``, ``R_best``, ``R_med``,
    ``R_worst``, and ``confidence``.

    Returns
    -------
    list[dict]
        Five initiatives (A through E) with costs, scenario returns,
        and confidence scores from Eisenhauer (2025), Table 1.
    """
    return [
        {"id": "A", "cost": 4, "R_best": 15, "R_med": 10, "R_worst": 2, "confidence": 0.90},
        {"id": "B", "cost": 2, "R_best": 12, "R_med": 8, "R_worst": 1, "confidence": 0.60},
        {"id": "C", "cost": 2, "R_best": 9, "R_med": 6, "R_worst": 2, "confidence": 0.80},
        {"id": "D", "cost": 2, "R_best": 7, "R_med": 5, "R_worst": 3, "confidence": 0.40},
        {"id": "E", "cost": 4, "R_best": 18, "R_med": 9, "R_worst": 0, "confidence": 0.50},
    ]


# =============================================================================
# Print Helper Functions
# =============================================================================


def display_solver_result(result, rule_name):
    """
    Print a formatted summary of a solver result.

    Parameters
    ----------
    result : SolverResult
        Output from a solver call (minimax regret or Bayesian).
    rule_name : str
        Display name for the decision rule (e.g. ``"Minimax regret"``).
    """
    print(rule_name)
    print("=" * 50)
    print(f"  Status:     {result['status']}")
    print(f"  Selected:   {result['selected_initiatives']}")
    print(f"  Total cost: {result['total_cost']:.1f}")
    if result["objective_value"] is not None:
        print(f"  Objective:  {result['objective_value']:.2f}")
    print()
    print("  Portfolio returns by scenario:")
    for scenario, value in result["total_actual_returns"].items():
        print(f"    {scenario:>5s}: {value:.1f}")


# =============================================================================
# Plotting Functions
# =============================================================================


def plot_confidence_penalty(initiatives):
    """
    Plot base vs effective returns as grouped bars for each initiative.

    For each initiative and scenario, shows the baseline return next to
    the confidence-adjusted effective return, making the penalty visible
    as the gap between bars.

    Parameters
    ----------
    initiatives : list[dict]
        Initiatives with ``effective_returns`` computed (output of
        ``calculate_effective_returns``).
    """
    scenarios = ["best", "med", "worst"]
    ids = [init["id"] for init in initiatives]
    n_initiatives = len(ids)
    n_scenarios = len(scenarios)

    x = np.arange(n_initiatives)
    group_width = 0.8
    bar_width = group_width / (n_scenarios * 2)

    _, ax = plt.subplots(figsize=(10, 5))

    base_colors = ["#3498db", "#2ecc71", "#e74c3c"]
    eff_colors = ["#85c1e9", "#82e0aa", "#f1948a"]

    for j, scenario in enumerate(scenarios):
        base_key = f"R_{scenario}"
        base_vals = [init[base_key] for init in initiatives]
        eff_vals = [init["effective_returns"][scenario] for init in initiatives]

        offset_base = (2 * j) * bar_width - group_width / 2 + bar_width / 2
        offset_eff = (2 * j + 1) * bar_width - group_width / 2 + bar_width / 2

        ax.bar(x + offset_base, base_vals, bar_width, color=base_colors[j], edgecolor="black", alpha=0.85)
        ax.bar(x + offset_eff, eff_vals, bar_width, color=eff_colors[j], edgecolor="black", alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(ids)
    ax.set_xlabel("Initiative")
    ax.set_ylabel("Return")
    ax.set_title("Confidence Penalty: Base vs Effective Returns")

    legend_elements = []
    for j, scenario in enumerate(scenarios):
        legend_elements.append(Patch(facecolor=base_colors[j], edgecolor="black", label=f"{scenario} (base)"))
        legend_elements.append(Patch(facecolor=eff_colors[j], edgecolor="black", label=f"{scenario} (effective)"))
    ax.legend(handles=legend_elements, loc="upper right", fontsize=8, ncol=2)

    plt.tight_layout()
    plt.show()


def plot_effective_returns_heatmap(processed):
    """
    Plot a heatmap of effective returns for preprocessed initiatives.

    Parameters
    ----------
    processed : list[dict]
        Preprocessed initiatives with ``effective_returns`` and ``id`` keys.
    """
    scenarios = ["best", "med", "worst"]
    ids = [init["id"] for init in processed]
    data = np.array([[init["effective_returns"][s] for s in scenarios] for init in processed])

    _, ax = plt.subplots(figsize=(6, max(3, len(ids) * 0.8)))
    im = ax.imshow(data, cmap="YlOrRd", aspect="auto")

    ax.set_xticks(np.arange(len(scenarios)))
    ax.set_xticklabels([s.capitalize() for s in scenarios])
    ax.set_yticks(np.arange(len(ids)))
    ax.set_yticklabels(ids)

    for i in range(len(ids)):
        for j in range(len(scenarios)):
            ax.text(j, i, f"{data[i, j]:.1f}", ha="center", va="center", fontweight="bold", fontsize=11)

    plt.colorbar(im, ax=ax, label="Effective Return")
    ax.set_title("Effective Returns by Initiative and Scenario")
    plt.tight_layout()
    plt.show()


def plot_scenario_returns(result, title):
    """
    Plot portfolio returns by scenario with optimal benchmark overlay.

    Shows a bar for each scenario's portfolio return and a marker for the
    optimal scenario return ``V_j*`` when available in the result detail.

    Parameters
    ----------
    result : SolverResult
        Output from a solver call.
    title : str
        Plot title.
    """
    scenarios = list(result["total_actual_returns"].keys())
    portfolio_returns = [result["total_actual_returns"][s] for s in scenarios]

    _, ax = plt.subplots(figsize=(7, 4))

    x = np.arange(len(scenarios))
    ax.bar(x, portfolio_returns, color="#3498db", edgecolor="black", alpha=0.85, label="Portfolio return")

    if "v_j_star" in result.get("detail", {}):
        v_star = result["detail"]["v_j_star"]
        v_star_vals = [v_star[s] for s in scenarios]
        ax.scatter(x, v_star_vals, color="#e74c3c", zorder=5, s=100, marker="D", label="$V_j^*$ (optimal)")

    for i, val in enumerate(portfolio_returns):
        ax.text(i, val + 0.3, f"{val:.1f}", ha="center", va="bottom", fontsize=10)

    ax.set_xticks(x)
    ax.set_xticklabels([s.capitalize() for s in scenarios])
    ax.set_ylabel("Return")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_portfolio_comparison(all_results):
    """
    Plot a side-by-side comparison of portfolio returns across decision rules.

    Parameters
    ----------
    all_results : list[tuple[str, SolverResult]]
        List of ``(rule_name, result)`` pairs to compare.
    """
    scenarios = list(all_results[0][1]["total_actual_returns"].keys())
    n_rules = len(all_results)
    n_scenarios = len(scenarios)

    x = np.arange(n_scenarios)
    width = 0.8 / n_rules
    colors = ["#3498db", "#2ecc71", "#e74c3c", "#9b59b6"]

    _, ax = plt.subplots(figsize=(9, 5))

    for i, (name, result) in enumerate(all_results):
        vals = [result["total_actual_returns"][s] for s in scenarios]
        offset = (i - n_rules / 2 + 0.5) * width
        bars = ax.bar(x + offset, vals, width, label=name, color=colors[i % len(colors)], edgecolor="black", alpha=0.85)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, val + 0.2, f"{val:.1f}", ha="center", va="bottom", fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels([s.capitalize() for s in scenarios])
    ax.set_ylabel("Portfolio Return")
    ax.set_title("Decision Rule Comparison: Portfolio Returns by Scenario")
    ax.legend(loc="upper right")
    plt.tight_layout()
    plt.show()
