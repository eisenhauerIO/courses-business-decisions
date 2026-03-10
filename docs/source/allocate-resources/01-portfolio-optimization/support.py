"""Support functions for the Portfolio Optimization notebook."""

# Third-party
import matplotlib.pyplot as plt
import numpy as np

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
        Five initiatives with costs, scenario returns, and confidence
        scores from Eisenhauer (2025), Table 1.
    """
    return [
        {"id": "TitlesAI", "cost": 4, "R_best": 15, "R_med": 10, "R_worst": 2, "confidence": 0.90},
        {"id": "ImageEnhancer", "cost": 2, "R_best": 12, "R_med": 8, "R_worst": 1, "confidence": 0.60},
        {"id": "PriceOptimizer", "cost": 2, "R_best": 9, "R_med": 6, "R_worst": 2, "confidence": 0.80},
        {"id": "SearchRanker", "cost": 2, "R_best": 7, "R_med": 5, "R_worst": 3, "confidence": 0.40},
        {"id": "BundleEngine", "cost": 4, "R_best": 18, "R_med": 9, "R_worst": 0, "confidence": 0.50},
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
    Plot the return reduction caused by the confidence penalty.

    For each initiative and scenario, shows the drop from baseline to
    effective return as a grouped bar chart, making the cost of weak
    evidence immediately visible.

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
    bar_width = 0.8 / n_scenarios
    colors = ["#3498db", "#2ecc71", "#e74c3c"]

    _, ax = plt.subplots(figsize=(10, 5))

    for j, scenario in enumerate(scenarios):
        base_key = f"R_{scenario}"
        drops = [init[base_key] - init["effective_returns"][scenario] for init in initiatives]
        offset = (j - n_scenarios / 2 + 0.5) * bar_width
        bars = ax.bar(x + offset, drops, bar_width, color=colors[j], edgecolor="black", alpha=0.85, label=scenario)
        for bar, val in zip(bars, drops):
            if val > 0.05:
                ax.text(
                    bar.get_x() + bar.get_width() / 2, val + 0.1, f"{val:.1f}", ha="center", va="bottom", fontsize=8
                )

    ax.set_xticks(x)
    ax.set_xticklabels(ids)
    ax.set_xlabel("Initiative")
    ax.set_ylabel("Return reduction")
    ax.set_title("Confidence Penalty: Return Reduction by Initiative and Scenario")
    ax.legend(loc="upper right")
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


def plot_penalty_curve(initiatives):
    """
    Plot the penalty function gamma = 1 - c with initiatives as labeled points.

    Parameters
    ----------
    initiatives : list[dict]
        Initiatives with ``id`` and ``confidence`` keys.
    """
    c_range = np.linspace(0, 1, 100)
    gamma_range = 1 - c_range

    _, ax = plt.subplots(figsize=(7, 4))
    ax.plot(c_range, gamma_range, color="#2c3e50", linewidth=2, label=r"$\gamma_i = 1 - c_i$")

    colors = ["#3498db", "#2ecc71", "#e74c3c", "#9b59b6", "#f39c12"]
    for i, init in enumerate(initiatives):
        c = init["confidence"]
        gamma = 1 - c
        ax.scatter(c, gamma, color=colors[i % len(colors)], s=120, zorder=5, edgecolor="black")
        ax.annotate(
            init["id"],
            (c, gamma),
            textcoords="offset points",
            xytext=(10, 5),
            fontsize=12,
            fontweight="bold",
        )

    ax.set_xlabel("Confidence score $c_i$")
    ax.set_ylabel("Penalty factor $\\gamma_i$")
    ax.set_title("Confidence Penalty Function")
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_sensitivity_analysis(sensitivity_data, initiative_label="ImageEnhancer"):
    """
    Plot theta* and worst-case return as functions of an initiative's confidence.

    Parameters
    ----------
    sensitivity_data : list[dict]
        List of dicts with keys ``c_e``, ``gamma``, ``theta``, ``worst_return``,
        and ``selected``.
    initiative_label : str
        Display name of the initiative being varied.
    """
    c_vals = [d["c_e"] for d in sensitivity_data]
    theta_vals = [d["theta"] for d in sensitivity_data]
    worst_vals = [d["worst_return"] for d in sensitivity_data]

    fig, ax1 = plt.subplots(figsize=(8, 4.5))

    color1 = "#3498db"
    color2 = "#e74c3c"

    ax1.plot(c_vals, theta_vals, "o-", color=color1, linewidth=2, markersize=8, label=r"$\theta^*$ (max regret)")
    ax1.set_xlabel(f"{initiative_label} confidence ($c$)")
    ax1.set_ylabel(r"Maximum regret $\theta^*$", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2 = ax1.twinx()
    ax2.plot(c_vals, worst_vals, "s--", color=color2, linewidth=2, markersize=8, label="Worst-case return")
    ax2.set_ylabel("Worst-case portfolio return", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="center right")

    ax1.set_title("Incentive Effect: How Evidence Quality Shapes Allocation")
    ax1.grid(True, alpha=0.3)
    fig.tight_layout()
    plt.show()


def plot_scenario_returns_with_regret(result, title):
    """
    Plot portfolio returns by scenario with regret gaps highlighted.

    Like ``plot_scenario_returns`` but adds shaded regret regions and
    annotations between the portfolio return and the optimal benchmark.

    Parameters
    ----------
    result : SolverResult
        Output from a solver call with ``detail.v_j_star`` available.
    title : str
        Plot title.
    """
    scenarios = list(result["total_actual_returns"].keys())
    portfolio_returns = [result["total_actual_returns"][s] for s in scenarios]

    _, ax = plt.subplots(figsize=(7, 5))
    x = np.arange(len(scenarios))

    ax.bar(x, portfolio_returns, color="#3498db", edgecolor="black", alpha=0.85, label="Portfolio return", width=0.5)

    if "v_j_star" in result.get("detail", {}):
        v_star = result["detail"]["v_j_star"]
        v_star_vals = [v_star[s] for s in scenarios]

        ax.scatter(x, v_star_vals, color="#e74c3c", zorder=5, s=120, marker="D", label="$V_j^*$ (optimal)")

        for i, (pret, vret) in enumerate(zip(portfolio_returns, v_star_vals)):
            regret = vret - pret
            if regret > 0:
                ax.annotate(
                    "",
                    xy=(i + 0.3, pret),
                    xytext=(i + 0.3, vret),
                    arrowprops={"arrowstyle": "<->", "color": "#e74c3c", "lw": 2},
                )
                ax.text(
                    i + 0.42,
                    (pret + vret) / 2,
                    f"regret\n= {regret:.1f}",
                    ha="left",
                    va="center",
                    fontsize=9,
                    color="#e74c3c",
                    fontweight="bold",
                )

    for i, val in enumerate(portfolio_returns):
        ax.text(i, val + 0.3, f"{val:.1f}", ha="center", va="bottom", fontsize=10)

    theta = result.get("objective_value")
    if theta is not None:
        ax.axhline(y=0, color="gray", linewidth=0.5)
        ax.text(
            0.98,
            0.02,
            f"$\\theta^* = {theta:.1f}$ (max regret)",
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=10,
            bbox={"boxstyle": "round,pad=0.3", "facecolor": "#fadbd8", "alpha": 0.8},
        )

    ax.set_xticks(x)
    ax.set_xticklabels([s.capitalize() for s in scenarios])
    ax.set_ylabel("Return")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_selection_matrix(all_results, all_initiative_ids):
    """
    Plot a selection matrix showing which initiatives each decision rule picks.

    Parameters
    ----------
    all_results : list[tuple[str, SolverResult]]
        List of ``(rule_name, result)`` pairs.
    all_initiative_ids : list[str]
        Full list of initiative IDs (including excluded ones).
    """
    n_rules = len(all_results)
    n_initiatives = len(all_initiative_ids)

    matrix = np.zeros((n_rules, n_initiatives))
    costs = []

    for i, (_, result) in enumerate(all_results):
        for j, init_id in enumerate(all_initiative_ids):
            if init_id in result["selected_initiatives"]:
                matrix[i, j] = 1
        costs.append(result["total_cost"])

    rule_names = [name for name, _ in all_results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.5), gridspec_kw={"width_ratios": [3, 1.2]})

    cmap = plt.cm.colors.ListedColormap(["#f0f0f0", "#3498db"])
    ax1.imshow(matrix, cmap=cmap, aspect="auto", vmin=0, vmax=1)

    for i in range(n_rules):
        for j in range(n_initiatives):
            symbol = "Selected" if matrix[i, j] == 1 else ""
            color = "white" if matrix[i, j] == 1 else "#aaaaaa"
            ax1.text(j, i, symbol, ha="center", va="center", fontsize=8, color=color, fontweight="bold")

    ax1.set_xticks(np.arange(n_initiatives))
    ax1.set_xticklabels(all_initiative_ids)
    ax1.set_yticks(np.arange(n_rules))
    ax1.set_yticklabels(rule_names, fontsize=9)
    ax1.set_xlabel("Initiative")
    ax1.set_title("Initiative Selection by Decision Rule")

    bars = ax2.barh(np.arange(n_rules), costs, color="#2ecc71", edgecolor="black", alpha=0.85)
    for bar, cost in zip(bars, costs):
        ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2, f"{cost:.0f}", ha="left", va="center")
    ax2.set_yticks(np.arange(n_rules))
    ax2.set_yticklabels([])
    ax2.set_xlabel("Total Cost")
    ax2.set_title("Budget Usage")
    ax2.set_xlim(0, max(costs) * 1.3)

    fig.tight_layout()
    plt.show()


def plot_effective_return_interpolation(initiative, scenarios=None):
    """
    Plot how effective returns interpolate between baseline and worst-case.

    Shows one line per scenario as confidence varies from 0 to 1 for a
    single initiative.

    Parameters
    ----------
    initiative : dict
        A single initiative dict with ``R_best``, ``R_med``, ``R_worst``, and ``id``.
    scenarios : list[str] or None
        Scenario names. Defaults to ``["best", "med", "worst"]``.
    """
    if scenarios is None:
        scenarios = ["best", "med", "worst"]

    r_vals = {s: initiative[f"R_{s}"] for s in scenarios}
    r_min = min(r_vals.values())

    c_range = np.linspace(0, 1, 100)
    colors = {"best": "#3498db", "med": "#2ecc71", "worst": "#e74c3c"}

    _, ax = plt.subplots(figsize=(7, 4.5))

    for s in scenarios:
        r_base = r_vals[s]
        eff_returns = [(1 - (1 - c)) * r_base + (1 - c) * r_min for c in c_range]
        ax.plot(c_range, eff_returns, color=colors[s], linewidth=2, label=f"$\\tilde{{R}}_{{\\mathrm{{{s}}}}}$")

    c_actual = initiative["confidence"]
    ax.axvline(x=c_actual, color="#7f8c8d", linestyle="--", linewidth=1.5, label=f"$c_i = {c_actual}$")

    for s in scenarios:
        r_base = r_vals[s]
        gamma = 1 - c_actual
        eff = (1 - gamma) * r_base + gamma * r_min
        ax.scatter(c_actual, eff, color=colors[s], s=80, zorder=5, edgecolor="black")

    ax.set_xlabel("Confidence score $c_i$")
    ax.set_ylabel("Effective return $\\tilde{R}_{ij}$")
    ax.set_title(f"Initiative {initiative['id']}: Effective Returns as Confidence Varies")
    ax.set_xlim(-0.05, 1.05)
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


