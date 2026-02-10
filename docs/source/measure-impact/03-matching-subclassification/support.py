"""Support functions for the Matching and Subclassification lecture."""

# Third-party packages
import matplotlib.pyplot as plt
import numpy as np


def create_confounded_treatment_multi(metrics_df, true_effect=0.5, seed=42):
    """
    Create confounded treatment assignment based on multiple continuous covariates.

    Aggregates per-product revenue from metrics and uses a logistic model
    on quality_score, price, and impressions to determine treatment
    probability. Products with lower covariate values are more likely
    to receive content optimization, creating confounding on all three
    dimensions simultaneously.

    Parameters
    ----------
    metrics_df : pandas.DataFrame
        Metrics DataFrame with product_identifier, revenue, quality_score,
        price, and impressions columns.
    true_effect : float
        True proportional causal effect of treatment on revenue.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pandas.DataFrame
        DataFrame with product_identifier, D, Y_observed, Y0, Y1,
        quality_score, price, and impressions columns.
    """
    rng = np.random.default_rng(seed)

    # Aggregate revenue per product (single day, but pattern supports multiple)
    product_revenue = metrics_df.groupby("product_identifier")["revenue"].sum().reset_index()
    product_revenue.columns = ["product_identifier", "baseline_revenue"]

    # Merge continuous covariates from the metrics (one row per product)
    covariates = (
        metrics_df.groupby("product_identifier")[["quality_score", "price", "impressions"]].first().reset_index()
    )
    df = product_revenue.merge(covariates, on="product_identifier")

    # Standardize covariates so each contributes meaningfully
    qs_z = (df["quality_score"] - df["quality_score"].mean()) / df["quality_score"].std()
    price_z = (df["price"] - df["price"].mean()) / df["price"].std()
    imp_z = (df["impressions"] - df["impressions"].mean()) / df["impressions"].std()

    # Treatment probability via logistic model on all three covariates.
    # Negative coefficients: lower covariate values → higher treatment probability
    # (struggling products get content optimization)
    logit = -0.5 * qs_z - 0.8 * price_z - 0.3 * imp_z
    treatment_prob = 1 / (1 + np.exp(-logit))

    df["D"] = (rng.random(len(df)) < treatment_prob).astype(int)

    # Potential outcomes
    df["Y0"] = df["baseline_revenue"]
    df["Y1"] = df["baseline_revenue"] * (1 + true_effect)

    # Observed outcome via switching equation
    df["Y_observed"] = np.where(df["D"] == 1, df["Y1"], df["Y0"])

    return df[["product_identifier", "D", "Y_observed", "Y0", "Y1", "quality_score", "price", "impressions"]]


def compute_ground_truth_att(df):
    """
    Compute the ground truth ATT from potential outcomes.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with D, Y0, and Y1 columns.

    Returns
    -------
    float
        True average treatment effect on the treated.
    """
    treated = df[df["D"] == 1]
    return (treated["Y1"] - treated["Y0"]).mean()


def plot_covariate_imbalance(df, covariates, treatment_col="D"):
    """
    Plot overlapping histograms showing covariate imbalance between groups.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with treatment indicator and covariate columns.
    covariates : list of str
        Covariate column names to plot.
    treatment_col : str
        Name of the binary treatment column.
    """
    treated = df[df[treatment_col] == 1]
    control = df[df[treatment_col] == 0]

    _, axes = plt.subplots(1, len(covariates), figsize=(5 * len(covariates), 4))
    if len(covariates) == 1:
        axes = [axes]

    for ax, cov in zip(axes, covariates):
        ax.hist(control[cov], bins=30, alpha=0.5, color="#3498db", label="Control", density=True)
        ax.hist(treated[cov], bins=30, alpha=0.5, color="#e74c3c", label="Treated", density=True)
        ax.set_xlabel(cov)
        ax.set_ylabel("Density")
        ax.legend()

    plt.suptitle("Covariate Distributions by Treatment Status", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_balance_love_plot(balance_before, balance_after):
    """
    Love plot showing standardized mean differences before and after matching.

    Parameters
    ----------
    balance_before : pandas.DataFrame
        Output of create_table_one() on unmatched data.
        Index includes covariate names; has an 'SMD' column.
    balance_after : pandas.DataFrame
        Output of create_table_one() on matched data.
    """
    # Drop the 'n' row (sample size, not a covariate)
    covariates = [idx for idx in balance_before.index if idx != "n"]

    smd_before = balance_before.loc[covariates, "SMD"].astype(float).abs()
    smd_after = balance_after.loc[covariates, "SMD"].astype(float).abs()

    y_pos = np.arange(len(covariates))

    _, ax = plt.subplots(figsize=(8, max(3, len(covariates) * 0.8)))
    ax.scatter(smd_before, y_pos, marker="o", s=80, color="#e74c3c", label="Before matching", zorder=3)
    ax.scatter(smd_after, y_pos, marker="s", s=80, color="#2ecc71", label="After matching", zorder=3)

    # Connect before/after with lines
    for i in range(len(covariates)):
        ax.plot([smd_before.iloc[i], smd_after.iloc[i]], [y_pos[i], y_pos[i]], color="gray", linewidth=0.8, zorder=2)

    ax.axvline(x=0.1, color="black", linestyle="--", linewidth=1, label="SMD = 0.1 threshold")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(covariates)
    ax.set_xlabel("Absolute Standardized Mean Difference")
    ax.set_title("Covariate Balance: Before vs. After Matching", fontsize=14, fontweight="bold")
    ax.legend(loc="upper right")
    ax.set_xlim(left=0)
    plt.tight_layout()
    plt.show()


def plot_method_comparison(estimates_dict, true_effect):
    """
    Bar chart comparing treatment effect estimates across methods.

    Parameters
    ----------
    estimates_dict : dict
        Mapping of method name to estimated treatment effect (float).
    true_effect : float
        Ground truth ATT for reference line.
    """
    methods = list(estimates_dict.keys())
    estimates = list(estimates_dict.values())

    colors = ["#e74c3c" if abs(e - true_effect) > abs(true_effect) * 0.2 else "#2ecc71" for e in estimates]

    _, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(methods, estimates, color=colors, edgecolor="black", width=0.5)
    ax.axhline(y=true_effect, color="black", linestyle="--", linewidth=2, label=f"True ATT = ${true_effect:,.0f}")

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
