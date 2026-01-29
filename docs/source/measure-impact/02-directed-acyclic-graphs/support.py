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


def create_quality_score(metrics_df, seed=42):
    """
    Create a quality score for each product based on baseline revenue.

    This simulates unobserved product quality that drives both baseline sales
    and the company's decision of which products to optimize.

    Parameters
    ----------
    metrics_df : pandas.DataFrame
        Metrics DataFrame with `product_identifier` and `revenue` columns.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pandas.DataFrame
        DataFrame with `product_identifier` and `quality_score` columns.
    """
    rng = np.random.default_rng(seed)

    # Aggregate revenue by product (in case of multiple dates)
    product_revenue = metrics_df.groupby("product_identifier")["revenue"].sum().reset_index()
    product_revenue.columns = ["product_identifier", "baseline_revenue"]

    # Create quality score: normalized revenue + noise
    # Quality is correlated with revenue but not perfectly
    revenue_min = product_revenue["baseline_revenue"].min()
    revenue_max = product_revenue["baseline_revenue"].max()
    revenue_normalized = (product_revenue["baseline_revenue"] - revenue_min) / (revenue_max - revenue_min + 1e-6)

    # Scale to 1-100 range with noise
    product_revenue["quality_score"] = 10 + 80 * revenue_normalized + rng.normal(0, 10, len(product_revenue))
    product_revenue["quality_score"] = np.clip(product_revenue["quality_score"], 1, 100)

    return product_revenue[["product_identifier", "quality_score", "baseline_revenue"]]


def apply_confounded_treatment(quality_df, treatment_fraction=0.3, quality_effect=-0.02, true_effect=0.5, seed=42):
    """
    Apply treatment assignment that is confounded by quality.

    Struggling products (low quality) are MORE likely to receive content optimization.
    This creates a backdoor path: Quality → Optimization ← (selection) and Quality → Sales.

    Parameters
    ----------
    quality_df : pandas.DataFrame
        DataFrame with `product_identifier`, `quality_score`, and `baseline_revenue`.
    treatment_fraction : float
        Target fraction of products to treat (approximate).
    quality_effect : float
        How quality affects treatment probability (negative = low quality more likely treated).
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

    # Treatment probability inversely related to quality
    # Low quality products are more likely to receive optimization
    quality_centered = df["quality_score"] - df["quality_score"].mean()
    logit = quality_effect * quality_centered
    treatment_prob = 1 / (1 + np.exp(-logit))

    # Scale to achieve target treatment fraction
    treatment_prob = treatment_prob * (treatment_fraction / treatment_prob.mean())
    treatment_prob = np.clip(treatment_prob, 0.05, 0.95)

    # Assign treatment
    df["optimized"] = rng.random(len(df)) < treatment_prob
    df["D"] = df["optimized"].astype(int)

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


def plot_confounding_scatter(df, title=None):
    """
    Plot scatter showing confounding relationship.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with quality_score, D, and Y_observed columns.
    title : str, optional
        Plot title.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: Quality vs Treatment (showing selection bias)
    treated = df[df["D"] == 1]
    control = df[df["D"] == 0]

    axes[0].scatter(
        control["quality_score"],
        control["Y0"],
        alpha=0.5,
        color="#3498db",
        s=40,
        label="Control (not optimized)",
    )
    axes[0].scatter(
        treated["quality_score"],
        treated["Y0"],
        alpha=0.5,
        color="#e74c3c",
        s=40,
        label="Treated (optimized)",
    )
    axes[0].set_xlabel("Quality Score")
    axes[0].set_ylabel("Baseline Revenue ($)")
    axes[0].set_title("Selection into Treatment\n(Low quality products selected for optimization)")
    axes[0].legend()

    # Right: Naive comparison of outcomes
    axes[1].boxplot(
        [control["Y_observed"], treated["Y_observed"]],
        labels=["Control", "Treated"],
        patch_artist=True,
    )
    axes[1].patches[0].set_facecolor("#3498db")
    axes[1].patches[1].set_facecolor("#e74c3c")
    axes[1].set_ylabel("Observed Revenue ($)")
    axes[1].set_title("Observed Outcomes\n(Naive comparison suggests optimization hurts!)")

    naive_diff = treated["Y_observed"].mean() - control["Y_observed"].mean()
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


def plot_dag_application(df, naive_effect, conditioned_effect, true_effect):
    """
    Create summary visualization comparing naive vs conditioned estimates.

    Parameters
    ----------
    df : pandas.DataFrame
        Data with quality_score, D, Y_observed columns.
    naive_effect : float
        Naive estimate (biased).
    conditioned_effect : float
        Estimate after conditioning on quality.
    true_effect : float
        True causal effect (proportional).
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Panel 1: Scatter colored by quality
    scatter = axes[0].scatter(
        df["D"] + np.random.normal(0, 0.05, len(df)),  # Jitter for visibility
        df["Y_observed"],
        c=df["quality_score"],
        cmap="RdYlGn",
        alpha=0.6,
        s=40,
    )
    plt.colorbar(scatter, ax=axes[0], label="Quality Score")
    axes[0].set_xticks([0, 1])
    axes[0].set_xticklabels(["Control", "Treated"])
    axes[0].set_ylabel("Observed Revenue ($)")
    axes[0].set_title("Outcomes by Treatment\n(colored by quality)")

    # Panel 2: Comparison of estimates
    estimates = {
        "Naive": naive_effect,
        "Conditioned\non Quality": conditioned_effect,
    }
    colors = ["#e74c3c" if abs(v) > abs(conditioned_effect) else "#2ecc71" for v in estimates.values()]

    x_pos = np.arange(len(estimates))
    bars = axes[1].bar(x_pos, estimates.values(), color=colors, edgecolor="black", width=0.6)

    # Add value labels
    for bar, val in zip(bars, estimates.values()):
        y_pos = bar.get_height() + (50 if val > 0 else -80)
        axes[1].text(
            bar.get_x() + bar.get_width() / 2, y_pos, f"${val:,.0f}", ha="center", fontsize=11, fontweight="bold"
        )

    axes[1].axhline(0, color="black", linewidth=0.5)
    axes[1].set_xticks(x_pos)
    axes[1].set_xticklabels(estimates.keys())
    axes[1].set_ylabel("Estimated Effect on Revenue ($)")
    axes[1].set_title("Naive vs. Conditioned Estimates")

    # Panel 3: Text summary
    axes[2].axis("off")
    divider = "─" * 30
    summary_text = (
        f"DAG Analysis Summary\n"
        f"{divider}\n\n"
        f"True effect: +{true_effect:.0%} revenue boost\n\n"
        f"Naive estimate: ${naive_effect:,.0f}\n"
        f"  → BIASED (wrong sign!)\n\n"
        f"Conditioned estimate: ${conditioned_effect:,.0f}\n"
        f"  → Closer to true effect\n\n"
        f"{divider}\n"
        f"Backdoor path:\n"
        f"  Quality → Optimization\n"
        f"  Quality → Sales\n\n"
        f"Conditioning on Quality\n"
        f"blocks the backdoor path."
    )
    axes[2].text(
        0.1,
        0.9,
        summary_text,
        transform=axes[2].transAxes,
        fontsize=12,
        verticalalignment="top",
        fontfamily="monospace",
        bbox=dict(boxstyle="round", facecolor="lightgray", alpha=0.3),
    )

    plt.tight_layout()
    plt.show()
