"""Support functions for the Directed Acyclic Graphs notebook."""

# Third-party packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def simulate_police_force_data(n_population=5000, discrimination_effect=0.3, seed=42):
    """
    Simulate police stop data with collider bias structure.

    The DAG structure:
        Minority (D) → Stop (M) ← Suspicion (U)
        Minority (D) → Force (Y)
        Suspicion (U) → Force (Y)

    Where Stop (M) is the collider that creates sample selection bias.

    Parameters
    ----------
    n_population : int
        Size of the simulated population.
    discrimination_effect : float
        True causal effect of minority status on force (0 = no discrimination).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns:
        - minority: minority status (0 or 1)
        - suspicion: suspicion scores
        - is_stopped: boolean stop status
        - force_score: force scores
    """
    rng = np.random.default_rng(seed)

    # Minority status (binary treatment)
    minority = rng.choice([0, 1], size=n_population, p=[0.7, 0.3])

    # Suspicion/perceived threat (unobserved confounder)
    suspicion = rng.normal(50, 15, n_population)

    # Stop probability depends on minority status AND suspicion
    # Minorities are more likely to be stopped (D → M)
    # Higher suspicion leads to more stops (U → M)
    stop_score = (
        0.3 * suspicion  # Suspicion affects stops
        + 15 * minority  # Minorities more likely stopped
        + rng.normal(0, 10, n_population)
    )
    is_stopped = stop_score > np.percentile(stop_score, 70)

    # Force depends on suspicion and minority status
    # True discrimination effect is the parameter
    force_score = (
        0.5 * suspicion  # Higher suspicion → more force (U → Y)
        + discrimination_effect * 20 * minority  # True discrimination (D → Y)
        + rng.normal(0, 10, n_population)
    )

    return pd.DataFrame(
        {
            "minority": minority,
            "suspicion": suspicion,
            "is_stopped": is_stopped,
            "force_score": force_score,
        }
    )


def draw_police_force_example(df, figsize=(12, 5)):
    """
    Draw police force collider bias visualization.

    Parameters
    ----------
    df : pandas.DataFrame
        Output from simulate_police_force_data().
    figsize : tuple
        Figure size for the plots.
    """
    minority = df["minority"].values
    is_stopped = df["is_stopped"].values
    force_score = df["force_score"].values

    rng = np.random.default_rng(42)  # For jitter only

    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # Left: Full population
    axes[0].scatter(
        minority[~is_stopped] + rng.normal(0, 0.05, (~is_stopped).sum()),
        force_score[~is_stopped],
        alpha=0.2,
        color="#3498db",
        s=15,
        label="Not stopped",
    )
    axes[0].scatter(
        minority[is_stopped] + rng.normal(0, 0.05, is_stopped.sum()),
        force_score[is_stopped],
        alpha=0.5,
        color="#e74c3c",
        s=30,
        label="Stopped",
    )
    axes[0].set_xticks([0, 1])
    axes[0].set_xticklabels(["Non-minority", "Minority"])
    axes[0].set_xlabel("Minority Status (D)")
    axes[0].set_ylabel("Force Score (Y)")
    axes[0].set_title("Full Population")

    # Correlation in full population
    corr_full = np.corrcoef(minority, force_score)[0, 1]
    axes[0].text(0.05, 0.95, f"Correlation: {corr_full:.2f}", transform=axes[0].transAxes, va="top", fontsize=11)
    axes[0].legend(loc="lower right")

    # Right: Stopped only (collider bias - conditioning on M)
    minority_stopped = minority[is_stopped]
    force_stopped = force_score[is_stopped]

    axes[1].scatter(
        minority_stopped + rng.normal(0, 0.05, len(minority_stopped)),
        force_stopped,
        alpha=0.5,
        color="#e74c3c",
        s=30,
    )

    # Add means for each group
    mean_force_nonmin = force_stopped[minority_stopped == 0].mean()
    mean_force_min = force_stopped[minority_stopped == 1].mean()
    axes[1].hlines(mean_force_nonmin, -0.2, 0.2, colors="#2c3e50", linewidth=3, label="Group mean")
    axes[1].hlines(mean_force_min, 0.8, 1.2, colors="#2c3e50", linewidth=3)

    axes[1].set_xticks([0, 1])
    axes[1].set_xticklabels(["Non-minority", "Minority"])
    axes[1].set_xlabel("Minority Status (D)")
    axes[1].set_ylabel("Force Score (Y)")
    axes[1].set_title("Police Stops Only (Collider Bias)")

    # Correlation among stopped individuals
    corr_stopped = np.corrcoef(minority_stopped, force_stopped)[0, 1]
    axes[1].text(0.05, 0.95, f"Correlation: {corr_stopped:.2f}", transform=axes[1].transAxes, va="top", fontsize=11)
    axes[1].legend(loc="lower right")

    plt.suptitle("Police Use of Force: Sample Selection as Collider Bias", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


# =============================================================================
# Functions for Online Retail Simulator Integration
# =============================================================================


def create_confounded_treatment(metrics_df, prob_treat_low=0.6, prob_treat_high=0.2, true_effect=0.5, seed=42):
    """
    Create confounded treatment assignment from raw simulator metrics.

    Aggregates revenue per product, assigns binary quality (High/Low) by median
    split, then assigns treatment confounded by quality: struggling products
    (low quality) are more likely to receive content optimization.

    Parameters
    ----------
    metrics_df : pandas.DataFrame
        Metrics DataFrame with ``product_identifier`` and ``revenue`` columns.
    prob_treat_low : float
        Probability of treatment for low quality products.
    prob_treat_high : float
        Probability of treatment for high quality products.
    true_effect : float
        True causal effect of treatment (proportional increase in revenue).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns ``product_identifier``, ``quality``,
        ``baseline_revenue``, ``D``, ``Y0``, ``Y1``, ``Y_observed``.
    """
    quality_df = _create_binary_quality(metrics_df)
    return _apply_confounded_treatment(
        quality_df,
        prob_treat_low=prob_treat_low,
        prob_treat_high=prob_treat_high,
        true_effect=true_effect,
        seed=seed,
    )


def _create_binary_quality(metrics_df):
    """
    Create binary quality (High/Low) for each product based on baseline revenue.

    Products in top half by revenue are "High" quality, bottom half are "Low" quality.
    This simulates unobserved product quality that drives both baseline sales
    and the company's decision of which products to optimize.

    Parameters
    ----------
    metrics_df : pandas.DataFrame
        Metrics DataFrame with `product_identifier` and `revenue` columns.

    Returns
    -------
    pandas.DataFrame
        DataFrame with `product_identifier`, `quality`, and `baseline_revenue` columns.
    """
    # Aggregate revenue by product (in case of multiple dates)
    product_revenue = metrics_df.groupby("product_identifier")["revenue"].sum().reset_index()
    product_revenue.columns = ["product_identifier", "baseline_revenue"]

    # Binary quality based on rank (top 50% = High, bottom 50% = Low)
    # Using rank ensures equal split even with ties or skewed distributions
    product_revenue["rank"] = product_revenue["baseline_revenue"].rank(method="first")
    cutoff = len(product_revenue) / 2
    product_revenue["quality"] = np.where(product_revenue["rank"] > cutoff, "High", "Low")

    return product_revenue[["product_identifier", "quality", "baseline_revenue"]]


def _apply_confounded_treatment(quality_df, prob_treat_low=0.6, prob_treat_high=0.2, true_effect=0.5, seed=42):
    """
    Apply treatment assignment that is confounded by binary quality.

    Struggling products (low quality) are MORE likely to receive content optimization.
    This creates a backdoor path: Quality → Optimization and Quality → Sales.

    Parameters
    ----------
    quality_df : pandas.DataFrame
        DataFrame with `product_identifier`, `quality`, and `baseline_revenue`.
    prob_treat_low : float
        Probability of treatment for low quality products.
    prob_treat_high : float
        Probability of treatment for high quality products.
    true_effect : float
        True causal effect of treatment (proportional increase in revenue).
    seed : int
        Random seed.

    Returns
    -------
    pandas.DataFrame
        DataFrame with treatment assignment and potential outcomes.
    """
    rng = np.random.default_rng(seed)
    df = quality_df.copy()

    # Treatment probability depends on quality
    # Low quality products are more likely to receive optimization
    treatment_prob = np.where(df["quality"] == "Low", prob_treat_low, prob_treat_high)

    # Assign treatment
    df["D"] = (rng.random(len(df)) < treatment_prob).astype(int)

    # Calculate potential outcomes
    # Y^0: baseline revenue (what would happen without treatment)
    df["Y0"] = df["baseline_revenue"]

    # Y^1: revenue if treated (baseline * (1 + effect))
    df["Y1"] = df["baseline_revenue"] * (1 + true_effect)

    # Observed outcome follows switching equation
    df["Y_observed"] = np.where(df["D"] == 1, df["Y1"], df["Y0"])

    # Store true effect for validation
    df["true_effect"] = true_effect

    return df


def plot_confounding_bar(df, title=None):
    """
    Plot bar chart showing confounding with binary quality.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with quality, D, and Y_observed columns.
    title : str, optional
        Plot title.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: Treatment rates by quality (showing selection bias)
    low_quality = df[df["quality"] == "Low"]
    high_quality = df[df["quality"] == "High"]
    treat_rate_low = low_quality["D"].mean()
    treat_rate_high = high_quality["D"].mean()

    colors = ["#e74c3c", "#2ecc71"]  # Low=red, High=green
    axes[0].bar(["Low Quality", "High Quality"], [treat_rate_low, treat_rate_high], color=colors)
    axes[0].set_ylabel("Treatment Rate")
    axes[0].set_title("Selection into Treatment\n(Low quality products more likely to be optimized)")
    axes[0].set_ylim(0, 1)
    for i, rate in enumerate([treat_rate_low, treat_rate_high]):
        axes[0].text(i, rate + 0.02, f"{rate:.0%}", ha="center", fontsize=12, fontweight="bold")

    # Right: Naive comparison of outcomes
    treated = df[df["D"] == 1]
    control = df[df["D"] == 0]
    means = [control["Y_observed"].mean(), treated["Y_observed"].mean()]
    axes[1].bar(["Control", "Treated"], means, color=["#3498db", "#e74c3c"])
    axes[1].set_ylabel("Mean Revenue ($)")
    axes[1].set_title("Naive Comparison\n(Suggests optimization hurts sales!)")

    naive_diff = means[1] - means[0]
    true_effect = df["true_effect"].iloc[0]
    axes[1].text(
        0.5,
        0.02,
        f"Naive diff: ${naive_diff:,.0f}  |  True effect: +{true_effect:.0%}",
        transform=axes[1].transAxes,
        ha="center",
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    plt.suptitle(title or "Confounding in Content Optimization", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def compute_effects(df):
    """
    Compute naive and conditional treatment effects from binary quality data.

    Parameters
    ----------
    df : pandas.DataFrame
        Data with quality, D, Y_observed columns.

    Returns
    -------
    dict
        Dictionary with naive_effect, effects by quality bin, and weighted average.
    """
    # Naive effect (unconditional)
    naive_effect = df[df["D"] == 1]["Y_observed"].mean() - df[df["D"] == 0]["Y_observed"].mean()

    # Within-bin effects
    effects = {}
    weights = {}
    for quality in ["Low", "High"]:
        bin_data = df[df["quality"] == quality]
        treated_mean = bin_data[bin_data["D"] == 1]["Y_observed"].mean()
        control_mean = bin_data[bin_data["D"] == 0]["Y_observed"].mean()
        effects[quality] = treated_mean - control_mean
        weights[quality] = len(bin_data) / len(df)

    # Weighted average of within-bin effects
    conditional_effect = sum(effects[q] * weights[q] for q in ["Low", "High"])

    return {
        "naive": naive_effect,
        "by_quality": effects,
        "weights": weights,
        "conditional": conditional_effect,
    }


def plot_conditional_comparison(df):
    """
    Create visualization comparing naive vs conditional estimates with binary quality.

    Parameters
    ----------
    df : pandas.DataFrame
        Data with quality, D, Y_observed columns.
    """
    effects = compute_effects(df)
    true_effect_pct = df["true_effect"].iloc[0]

    _, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Panel 1: Mean outcomes by quality and treatment (2x2 visualization)
    categories = ["Low\nControl", "Low\nTreated", "High\nControl", "High\nTreated"]
    means = []
    colors = []
    for quality in ["Low", "High"]:
        for d in [0, 1]:
            mean_val = df[(df["quality"] == quality) & (df["D"] == d)]["Y_observed"].mean()
            means.append(mean_val)
            colors.append("#3498db" if d == 0 else "#e74c3c")

    bars = axes[0].bar(categories, means, color=colors)
    axes[0].set_ylabel("Mean Revenue ($)")
    axes[0].set_title("Mean Outcomes by Quality × Treatment")
    axes[0].axhline(means[0], color="#3498db", linestyle="--", alpha=0.5, xmin=0, xmax=0.25)
    axes[0].axhline(means[2], color="#3498db", linestyle="--", alpha=0.5, xmin=0.5, xmax=0.75)

    # Add value labels
    for bar, val in zip(bars, means):
        axes[0].text(bar.get_x() + bar.get_width() / 2, val + 20, f"${val:,.0f}", ha="center", fontsize=9)

    # Panel 2: Comparison of effects
    effect_labels = [
        "Naive\n(Biased)",
        "Low Quality\n(Within-bin)",
        "High Quality\n(Within-bin)",
        "Conditional\n(Weighted Avg)",
    ]
    effect_values = [
        effects["naive"],
        effects["by_quality"]["Low"],
        effects["by_quality"]["High"],
        effects["conditional"],
    ]
    bar_colors = ["#e74c3c", "#2ecc71", "#2ecc71", "#2ecc71"]

    bars = axes[1].bar(effect_labels, effect_values, color=bar_colors, edgecolor="black")
    axes[1].axhline(0, color="black", linewidth=0.5)
    axes[1].set_ylabel("Estimated Treatment Effect ($)")
    axes[1].set_title("Naive vs. Conditional Estimates")

    for bar, val in zip(bars, effect_values):
        y_pos = val + (30 if val > 0 else -50)
        axes[1].text(
            bar.get_x() + bar.get_width() / 2, y_pos, f"${val:,.0f}", ha="center", fontsize=10, fontweight="bold"
        )

    # Panel 3: Text summary
    axes[2].axis("off")
    divider = "─" * 35
    summary_text = (
        f"Conditional Comparison Summary\n"
        f"{divider}\n\n"
        f"True effect: +{true_effect_pct:.0%} revenue boost\n\n"
        f"Naive (unconditional):\n"
        f"  E[Y|D=1] - E[Y|D=0] = ${effects['naive']:,.0f}\n"
        f"  → BIASED (wrong sign!)\n\n"
        f"Within Low Quality:\n"
        f"  E[Y|D=1,Q=Low] - E[Y|D=0,Q=Low] = ${effects['by_quality']['Low']:,.0f}\n\n"
        f"Within High Quality:\n"
        f"  E[Y|D=1,Q=High] - E[Y|D=0,Q=High] = ${effects['by_quality']['High']:,.0f}\n\n"
        f"Weighted average: ${effects['conditional']:,.0f}\n"
        f"  → Recovers POSITIVE effect!"
    )
    axes[2].text(
        0.05,
        0.95,
        summary_text,
        transform=axes[2].transAxes,
        fontsize=11,
        verticalalignment="top",
        fontfamily="monospace",
        bbox=dict(boxstyle="round", facecolor="lightgray", alpha=0.3),
    )

    plt.suptitle("Blocking the Backdoor: Conditioning on Quality", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()
