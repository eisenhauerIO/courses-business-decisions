"""Support functions for the Matching and Subclassification lecture."""

# Standard library
import logging

# Third-party packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from impact_engine.models.subclassification import SubclassificationAdapter


def create_confounded_treatment_multi(
    metrics_df,
    true_effect=0.5,
    seed=42,
    coef_quality=-0.5,
    coef_price=-0.8,
    coef_impressions=-0.3,
):
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
    coef_quality : float
        Logistic model coefficient for quality_score. Negative values mean
        lower quality increases treatment probability.
    coef_price : float
        Logistic model coefficient for price. Negative values mean lower
        price increases treatment probability.
    coef_impressions : float
        Logistic model coefficient for impressions. Negative values mean
        fewer impressions increases treatment probability.

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

    # Standardize covariates so each contributes on a common scale
    qs_z = (df["quality_score"] - df["quality_score"].mean()) / df["quality_score"].std()
    price_z = (df["price"] - df["price"].mean()) / df["price"].std()
    imp_z = (df["impressions"] - df["impressions"].mean()) / df["impressions"].std()

    # Logistic model: covariates → treatment probability via sigmoid
    logit = coef_quality * qs_z + coef_price * price_z + coef_impressions * imp_z
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


def sweep_strata(confounded_products, strata_values, covariate_columns):
    """
    Sweep across strata counts and collect subclassification ATT estimates.

    Fit the SubclassificationAdapter for each value of K, recording the
    estimated treatment effect and the number of strata used vs. dropped
    due to common support violations.

    Parameters
    ----------
    confounded_products : pandas.DataFrame
        Product-level DataFrame with treatment, outcome, and covariate columns.
    strata_values : list of int
        Values of K (strata per covariate) to sweep over.
    covariate_columns : list of str
        Covariate column names to condition on.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns: n_strata, estimate, n_strata_used, n_strata_dropped.
    """
    records = []

    # Suppress adapter warnings during the sweep
    logger = logging.getLogger("impact_engine")
    original_level = logger.level
    logger.setLevel(logging.ERROR)

    for k in strata_values:
        adapter = SubclassificationAdapter()
        adapter.connect(
            {
                "treatment_column": "D",
                "covariate_columns": covariate_columns,
                "dependent_variable": "Y_observed",
                "n_strata": k,
                "estimand": "att",
            }
        )
        result = adapter.fit(confounded_products)
        records.append(
            {
                "n_strata": k,
                "estimate": result.data["impact_estimates"]["treatment_effect"],
                "n_strata_used": result.data["impact_estimates"]["n_strata"],
                "n_strata_dropped": result.data["impact_estimates"]["n_strata_dropped"],
            }
        )

    logger.setLevel(original_level)

    return pd.DataFrame(records)


def plot_treatment_rates(df, covariates, treatment_col="D", n_bins=5):
    """
    Plot average treatment rate within covariate quintiles.

    Shows how the assignment mechanism maps covariate values to treatment
    probability: each panel bins a covariate into quantiles and displays
    the observed treatment rate per bin.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with treatment indicator and covariate columns.
    covariates : list of str
        Covariate column names to plot.
    treatment_col : str
        Name of the binary treatment column.
    n_bins : int
        Number of quantile bins per covariate.
    """
    _, axes = plt.subplots(1, len(covariates), figsize=(5 * len(covariates), 4))
    if len(covariates) == 1:
        axes = [axes]

    for ax, cov in zip(axes, covariates):
        bins = pd.qcut(df[cov], q=n_bins, duplicates="drop")
        rates = df.groupby(bins, observed=True)[treatment_col].mean()

        labels = [f"Q{i + 1}" for i in range(len(rates))]
        ax.bar(labels, rates, color="#3498db", edgecolor="black", width=0.6)
        ax.set_xlabel(cov)
        ax.set_ylabel("Treatment Rate")
        ax.set_ylim(0, 1)
        ax.axhline(y=df[treatment_col].mean(), color="black", linestyle="--", linewidth=1, label="Overall rate")
        ax.legend(fontsize=9)

    plt.suptitle("Treatment Rate by Covariate Quintile", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


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
    Plot standardized mean differences before and after matching (Love plot).

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


def plot_strata_convergence(results_df, true_att):
    """
    Plot ATT estimates and common support violations as a function of strata count.

    Top panel shows how the ATT estimate converges toward the true effect as the
    number of strata per covariate increases. Bottom panel shows the fraction of
    strata dropped due to common support violations — the curse of dimensionality.

    Parameters
    ----------
    results_df : pandas.DataFrame
        DataFrame with columns: n_strata, estimate, n_strata_used, n_strata_dropped.
    true_att : float
        Ground truth ATT for reference line.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    n = results_df["n_strata"]
    total = results_df["n_strata_used"] + results_df["n_strata_dropped"]
    frac_dropped = results_df["n_strata_dropped"] / total

    # Top panel: ATT estimate convergence
    ax1.plot(n, results_df["estimate"], "o-", color="#3498db", linewidth=2, markersize=7, label="Estimated ATT")
    ax1.axhline(y=true_att, color="black", linestyle="--", linewidth=1.5, label=f"True ATT = ${true_att:,.2f}")
    ax1.set_ylabel("Estimated ATT ($)")
    ax1.set_title("Subclassification: Bias vs. Curse of Dimensionality", fontsize=14, fontweight="bold")
    ax1.legend()

    # Bottom panel: common support violations
    ax2.bar(n, frac_dropped * 100, color="#e74c3c", edgecolor="black", width=0.6)
    ax2.set_xlabel("Number of Strata per Covariate")
    ax2.set_ylabel("Strata Dropped (%)")
    ax2.set_xticks(n)

    # Annotate total strata on bars
    for idx, row in results_df.iterrows():
        pct = frac_dropped.iloc[idx] * 100
        total_k = total.iloc[idx]
        if pct > 0:
            ax2.text(
                row["n_strata"],
                pct + 1.5,
                f"{row['n_strata_dropped']:.0f}/{total_k:.0f}",
                ha="center",
                fontsize=8,
            )

    plt.tight_layout()
    plt.show()


def plot_method_comparison(estimates_dict, true_effect):
    """
    Compare treatment effect estimates across methods in a bar chart.

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
