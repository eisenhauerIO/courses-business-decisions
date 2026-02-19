"""Shared plotting utilities used across multiple lectures."""

import matplotlib.pyplot as plt


def plot_method_comparison(estimates_dict, true_effect):
    """Compare treatment effect estimates across methods in a bar chart.

    Parameters
    ----------
    estimates_dict : dict
        Mapping of method name to estimated treatment effect (float).
    true_effect : float
        Ground truth ATT for reference line.
    """
    methods = list(estimates_dict.keys())
    estimates = list(estimates_dict.values())

    # Color bars red if estimate deviates from truth by more than this fraction
    ERROR_THRESHOLD = 0.2
    colors = ["#e74c3c" if abs(e - true_effect) > abs(true_effect) * ERROR_THRESHOLD else "#2ecc71" for e in estimates]

    _, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(methods, estimates, color=colors, edgecolor="black", width=0.5)
    ax.axhline(
        y=true_effect,
        color="black",
        linestyle="--",
        linewidth=2,
        label=f"True ATT = ${true_effect:,.0f}",
    )

    # Error annotations
    for bar, est in zip(bars, estimates):
        error = est - true_effect
        pct_error = (error / true_effect) * 100
        y_pos = est + (true_effect * 0.03 if est >= 0 else -true_effect * 0.06)
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            y_pos,
            f"${est:,.0f}\n({pct_error:+.1f}%)",
            ha="center",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_ylabel("Estimated Treatment Effect ($)")
    ax.set_title("Method Comparison: Estimated vs. True ATT", fontsize=14, fontweight="bold")
    ax.legend()
    ax.axhline(y=0, color="gray", linewidth=0.5)
    plt.tight_layout()
    plt.show()
