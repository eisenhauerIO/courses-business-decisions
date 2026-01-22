"""Support functions for the Generalized Roy Model lecture.

This module provides helper functions for demonstrating essential heterogeneity
using the online retail simulator, focusing on:
- MTE-style analysis using quality as a propensity proxy
- Bias decomposition into baseline and selection-on-gains components
- Comparing treatment parameters (ATE, ATT, ATC)
"""

# Third-party packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def compute_treatment_effects(potential_outcomes_df, treatment_col="D"):
    """Compute treatment effect parameters from potential outcomes data.

    Parameters
    ----------
    potential_outcomes_df : pandas.DataFrame
        DataFrame with columns 'Y0', 'Y1', and treatment indicator.
    treatment_col : str, optional
        Name of treatment indicator column. Default is 'D'.

    Returns
    -------
    dict
        Dictionary with 'ate', 'att', 'atc', 'delta' (individual effects),
        and 'naive_estimate' keys.
    """
    df = potential_outcomes_df.copy()
    is_treated = df[treatment_col] == 1

    # Individual treatment effects
    delta = df["Y1"] - df["Y0"]

    # Population parameters
    ate = delta.mean()
    att = delta[is_treated].mean()
    atc = delta[~is_treated].mean()

    # Naive estimate (what we observe)
    if "Y_observed" in df.columns:
        y_col = "Y_observed"
    elif "Y" in df.columns:
        y_col = "Y"
    else:
        # Compute observed outcome using switching equation
        df["Y_observed"] = np.where(is_treated, df["Y1"], df["Y0"])
        y_col = "Y_observed"

    naive_estimate = df.loc[is_treated, y_col].mean() - df.loc[~is_treated, y_col].mean()

    return {
        "ate": ate,
        "att": att,
        "atc": atc,
        "delta": delta,
        "naive_estimate": naive_estimate,
    }


def compute_bias_decomposition(potential_outcomes_df, treatment_col="D"):
    """Decompose naive estimator bias into baseline and selection-on-gains components.

    The naive estimator can be decomposed as:
        E[Y|D=1] - E[Y|D=0] = ATE + Baseline Bias + Selection on Gains

    Where:
        - Baseline Bias = E[Y0|D=1] - E[Y0|D=0]  (treated have different baseline)
        - Selection on Gains = E[delta|D=1] - E[delta]  (treated benefit more/less)

    Parameters
    ----------
    potential_outcomes_df : pandas.DataFrame
        DataFrame with columns 'Y0', 'Y1', and treatment indicator.
    treatment_col : str, optional
        Name of treatment indicator column. Default is 'D'.

    Returns
    -------
    dict
        Dictionary with 'ate', 'baseline_bias', 'selection_on_gains',
        'total_bias', and 'naive_estimate' keys.
    """
    df = potential_outcomes_df.copy()
    is_treated = df[treatment_col] == 1

    # True ATE
    ate = (df["Y1"] - df["Y0"]).mean()

    # Baseline bias: difference in counterfactual outcomes
    baseline_bias = df.loc[is_treated, "Y0"].mean() - df.loc[~is_treated, "Y0"].mean()

    # Selection on gains: treated have different effects than average
    delta = df["Y1"] - df["Y0"]
    att = delta[is_treated].mean()
    selection_on_gains = att - ate

    # Total bias
    total_bias = baseline_bias + selection_on_gains

    # Naive estimate
    if "Y_observed" in df.columns:
        y_col = "Y_observed"
    else:
        df["Y_observed"] = np.where(is_treated, df["Y1"], df["Y0"])
        y_col = "Y_observed"

    naive_estimate = df.loc[is_treated, y_col].mean() - df.loc[~is_treated, y_col].mean()

    return {
        "ate": ate,
        "baseline_bias": baseline_bias,
        "selection_on_gains": selection_on_gains,
        "total_bias": total_bias,
        "naive_estimate": naive_estimate,
    }


def compute_mte_by_quality(potential_outcomes_df, quality_col="quality_score", treatment_col="D", n_bins=5):
    """Compute marginal treatment effects by quality bins (proxy for propensity).

    This provides an MTE-style analysis where quality score serves as a proxy
    for selection propensity. Products are binned by quality, and the average
    treatment effect is computed within each bin.

    Parameters
    ----------
    potential_outcomes_df : pandas.DataFrame
        DataFrame with columns 'Y0', 'Y1', and quality score.
    quality_col : str, optional
        Name of quality score column. Default is 'quality_score'.
    treatment_col : str, optional
        Name of treatment indicator column. Default is 'D'.
    n_bins : int, optional
        Number of quality bins. Default is 5.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns 'quality_bin', 'quality_midpoint', 'quality_min',
        'quality_max', 'mte', 'mte_std', 'n_products', 'pct_treated'.
    """
    df = potential_outcomes_df.copy()

    # Create quality bins using equal-width bins based on the data range
    # We use pd.cut instead of pd.qcut to avoid collapsing bins when there are
    # many duplicate values (qcut with duplicates="drop" can reduce bin count)
    quality_min = df[quality_col].min()
    quality_max = df[quality_col].max()
    bin_edges = np.linspace(quality_min, quality_max, n_bins + 1)
    df["quality_bin"] = pd.cut(df[quality_col], bins=bin_edges, labels=False, include_lowest=True)

    # Compute MTE within each bin
    results = []
    for bin_idx in sorted(df["quality_bin"].unique()):
        bin_data = df[df["quality_bin"] == bin_idx]

        # Individual effects in this bin
        effects = bin_data["Y1"] - bin_data["Y0"]

        # Treatment rate in this bin
        if treatment_col in df.columns:
            pct_treated = bin_data[treatment_col].mean()
        else:
            pct_treated = np.nan

        results.append(
            {
                "quality_bin": bin_idx,
                "quality_midpoint": bin_data[quality_col].median(),
                "quality_min": bin_data[quality_col].min(),
                "quality_max": bin_data[quality_col].max(),
                "mte": effects.mean(),
                "mte_std": effects.std(),
                "n_products": len(bin_data),
                "pct_treated": pct_treated,
            }
        )

    return pd.DataFrame(results)


def plot_mte_by_quality(mte_df, title=None):
    """Plot MTE curve across quality bins.

    Parameters
    ----------
    mte_df : pandas.DataFrame
        Output from compute_mte_by_quality().
    title : str, optional
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot MTE with error bars
    ax.errorbar(
        mte_df["quality_midpoint"],
        mte_df["mte"],
        yerr=mte_df["mte_std"] / np.sqrt(mte_df["n_products"]),
        fmt="o-",
        capsize=5,
        capthick=2,
        markersize=10,
        linewidth=2,
        color="#2c3e50",
        label="MTE by Quality",
    )

    # Add horizontal line for overall ATE
    overall_ate = (mte_df["mte"] * mte_df["n_products"]).sum() / mte_df["n_products"].sum()
    ax.axhline(overall_ate, color="#e74c3c", linestyle="--", linewidth=2, label=f"Overall ATE = ${overall_ate:,.0f}")

    ax.set_xlabel("Quality Score (Propensity Proxy)", fontsize=12)
    ax.set_ylabel("Marginal Treatment Effect ($)", fontsize=12)
    ax.set_title(title or "MTE by Quality: How Treatment Effects Vary with Selection", fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_treatment_parameters(ate, att, atc, naive=None, title=None):
    """Visualize treatment parameters as bar chart.

    Parameters
    ----------
    ate : float
        Average Treatment Effect.
    att : float
        Average Treatment on Treated.
    atc : float
        Average Treatment on Control.
    naive : float, optional
        Naive estimate to include.
    title : str, optional
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    params = {"ATE": ate, "ATT": att, "ATC": atc}
    colors = ["#2ecc71", "#e74c3c", "#3498db"]

    if naive is not None:
        params["Naive"] = naive
        colors.append("#95a5a6")

    x_pos = np.arange(len(params))
    bars = ax.bar(x_pos, params.values(), color=colors, edgecolor="black", width=0.6)

    # Add value labels
    for bar, (name, value) in zip(bars, params.items()):
        y_offset = max(abs(v) for v in params.values()) * 0.03
        y_pos = bar.get_height() + y_offset if value >= 0 else bar.get_height() - y_offset
        va = "bottom" if value >= 0 else "top"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            y_pos,
            f"${value:,.0f}",
            ha="center",
            va=va,
            fontsize=12,
            fontweight="bold",
        )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(params.keys())
    ax.set_ylabel("Treatment Effect ($)", fontsize=12)
    ax.set_title(title or "Treatment Parameters: Why They Differ Under Essential Heterogeneity", fontsize=14)
    ax.axhline(0, color="black", linewidth=0.5)

    plt.tight_layout()
    return fig


def plot_bias_decomposition(decomposition, title=None):
    """Visualize bias decomposition as stacked bar chart.

    Parameters
    ----------
    decomposition : dict
        Output from compute_bias_decomposition().
    title : str, optional
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Create decomposition visualization
    components = {
        "True ATE": decomposition["ate"],
        "Baseline Bias\n(Selection on Endowments)": decomposition["baseline_bias"],
        "Selection\non Gains": decomposition["selection_on_gains"],
        "Naive Estimate": decomposition["naive_estimate"],
    }
    colors = ["#2ecc71", "#e74c3c", "#9b59b6", "#3498db"]

    x_pos = np.arange(len(components))
    bars = ax.bar(x_pos, components.values(), color=colors, edgecolor="black", width=0.6)

    # Add value labels
    for bar, (name, value) in zip(bars, components.items()):
        y_offset = max(abs(v) for v in components.values()) * 0.03
        y_pos = bar.get_height() + y_offset if value >= 0 else bar.get_height() - y_offset
        va = "bottom" if value >= 0 else "top"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            y_pos,
            f"${value:,.0f}",
            ha="center",
            va=va,
            fontsize=11,
            fontweight="bold",
        )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(components.keys(), fontsize=10)
    ax.set_ylabel("Dollar Amount", fontsize=12)
    ax.set_title(title or "Bias Decomposition: Naive Estimate = ATE + Baseline Bias + Selection on Gains", fontsize=13)
    ax.axhline(0, color="black", linewidth=0.5)

    # Add equation annotation
    ate = decomposition["ate"]
    bb = decomposition["baseline_bias"]
    sg = decomposition["selection_on_gains"]
    naive = decomposition["naive_estimate"]

    equation = f"${naive:,.0f} = ${ate:,.0f} + ${bb:,.0f} + ${sg:,.0f}"
    ax.text(
        0.5,
        0.02,
        equation,
        transform=ax.transAxes,
        ha="center",
        fontsize=11,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    plt.tight_layout()
    return fig


def plot_treatment_effects_distribution(potential_outcomes_df, treatment_col="D", title=None):
    """Plot distribution of individual treatment effects by treatment status.

    Parameters
    ----------
    potential_outcomes_df : pandas.DataFrame
        DataFrame with columns 'Y0', 'Y1', and treatment indicator.
    treatment_col : str, optional
        Name of treatment indicator column. Default is 'D'.
    title : str, optional
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    df = potential_outcomes_df.copy()
    df["delta"] = df["Y1"] - df["Y0"]
    is_treated = df[treatment_col] == 1

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot distributions for treated and control
    sns.kdeplot(df.loc[is_treated, "delta"], ax=ax, color="#e74c3c", fill=True, alpha=0.3, label="Treated", linewidth=2)
    sns.kdeplot(
        df.loc[~is_treated, "delta"], ax=ax, color="#3498db", fill=True, alpha=0.3, label="Control", linewidth=2
    )

    # Add vertical lines for means
    att = df.loc[is_treated, "delta"].mean()
    atc = df.loc[~is_treated, "delta"].mean()
    ate = df["delta"].mean()

    ax.axvline(att, color="#e74c3c", linestyle="--", linewidth=2, label=f"ATT = ${att:,.0f}")
    ax.axvline(atc, color="#3498db", linestyle="--", linewidth=2, label=f"ATC = ${atc:,.0f}")
    ax.axvline(ate, color="#2ecc71", linestyle="-", linewidth=2, label=f"ATE = ${ate:,.0f}")

    ax.set_xlabel("Individual Treatment Effect ($)", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.set_title(
        title or "Distribution of Treatment Effects: Essential Heterogeneity\n(Treated vs Control Groups)", fontsize=13
    )
    ax.legend(fontsize=10)

    plt.tight_layout()
    return fig


def plot_selection_mechanism(potential_outcomes_df, quality_col="quality_score", treatment_col="D", title=None):
    """Visualize how treatment selection relates to quality and potential outcomes.

    Parameters
    ----------
    potential_outcomes_df : pandas.DataFrame
        DataFrame with quality score, treatment indicator, and potential outcomes.
    quality_col : str, optional
        Name of quality score column. Default is 'quality_score'.
    treatment_col : str, optional
        Name of treatment indicator column. Default is 'D'.
    title : str, optional
        Plot title.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    df = potential_outcomes_df.copy()
    df["delta"] = df["Y1"] - df["Y0"]
    is_treated = df[treatment_col] == 1

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Panel 1: Quality vs Treatment (selection mechanism)
    axes[0].scatter(
        df.loc[~is_treated, quality_col],
        df.loc[~is_treated, "Y0"],
        alpha=0.5,
        color="#3498db",
        s=30,
        label="Control",
    )
    axes[0].scatter(
        df.loc[is_treated, quality_col],
        df.loc[is_treated, "Y0"],
        alpha=0.5,
        color="#e74c3c",
        s=30,
        label="Treated",
    )
    axes[0].set_xlabel("Quality Score")
    axes[0].set_ylabel("Baseline Outcome (Y0)")
    axes[0].set_title("Selection into Treatment")
    axes[0].legend()

    # Panel 2: Quality vs Treatment Effect
    axes[1].scatter(df[quality_col], df["delta"], alpha=0.4, color="#2c3e50", s=30)
    z = np.polyfit(df[quality_col], df["delta"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df[quality_col].min(), df[quality_col].max(), 100)
    axes[1].plot(x_line, p(x_line), "r--", linewidth=2, label="Trend")
    axes[1].set_xlabel("Quality Score")
    axes[1].set_ylabel("Treatment Effect (Y1 - Y0)")
    axes[1].set_title("Heterogeneous Effects by Quality")
    axes[1].legend()

    # Panel 3: Summary text
    axes[2].axis("off")

    ate = df["delta"].mean()
    att = df.loc[is_treated, "delta"].mean()
    atc = df.loc[~is_treated, "delta"].mean()
    treated_quality = df.loc[is_treated, quality_col].mean()
    control_quality = df.loc[~is_treated, quality_col].mean()

    summary_text = (
        "Essential Heterogeneity Summary\n"
        "=" * 35 + "\n\n"
        f"Avg Quality (Treated):  {treated_quality:.1f}\n"
        f"Avg Quality (Control):  {control_quality:.1f}\n\n"
        f"ATE:  ${ate:,.0f}\n"
        f"ATT:  ${att:,.0f}\n"
        f"ATC:  ${atc:,.0f}\n\n"
        "=" * 35 + "\n"
        "Key Insight:\n"
        "Treatment selection correlates\n"
        "with treatment response.\n\n"
        "High-quality products:\n"
        "  - Selected for treatment\n"
        "  - Have smaller effects\n\n"
        "This is essential heterogeneity."
    )

    axes[2].text(
        0.1,
        0.9,
        summary_text,
        transform=axes[2].transAxes,
        fontsize=11,
        verticalalignment="top",
        fontfamily="monospace",
        bbox=dict(boxstyle="round", facecolor="lightgray", alpha=0.3),
    )

    plt.suptitle(title or "The Selection-Effect Correlation: Why ATE != ATT != ATC", fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig


def print_essential_heterogeneity_summary(potential_outcomes_df, treatment_col="D"):
    """Print formatted summary of essential heterogeneity analysis.

    Parameters
    ----------
    potential_outcomes_df : pandas.DataFrame
        DataFrame with potential outcomes and treatment indicator.
    treatment_col : str, optional
        Name of treatment indicator column. Default is 'D'.
    """
    effects = compute_treatment_effects(potential_outcomes_df, treatment_col)
    decomp = compute_bias_decomposition(potential_outcomes_df, treatment_col)

    print("=" * 60)
    print("ESSENTIAL HETEROGENEITY ANALYSIS")
    print("=" * 60)
    print()
    print("Treatment Parameters:")
    print(f"  ATE (Average Treatment Effect):     ${effects['ate']:>10,.2f}")
    print(f"  ATT (Treatment on Treated):         ${effects['att']:>10,.2f}")
    print(f"  ATC (Treatment on Control):         ${effects['atc']:>10,.2f}")
    print()
    print("Bias Decomposition:")
    print(f"  Naive Estimate:                     ${decomp['naive_estimate']:>10,.2f}")
    print(f"  True ATE:                           ${decomp['ate']:>10,.2f}")
    print(f"  Baseline Bias (selection on Y0):    ${decomp['baseline_bias']:>10,.2f}")
    print(f"  Selection on Gains (ATT - ATE):     ${decomp['selection_on_gains']:>10,.2f}")
    print(f"  Total Bias:                         ${decomp['total_bias']:>10,.2f}")
    print()
    print("Verification:")
    print("  Naive = ATE + Baseline + SelGains")
    print(
        f"  {decomp['naive_estimate']:.2f} = {decomp['ate']:.2f} + {decomp['baseline_bias']:.2f} + "
        f"{decomp['selection_on_gains']:.2f}"
    )
    print("=" * 60)
