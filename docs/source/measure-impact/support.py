"""Support functions for the Potential Outcome Model notebook."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_individual_effects_distribution(effects, true_effect=None, title=None):
    """Plot histogram of individual treatment effects.

    Args:
        effects: Array or Series of individual treatment effects
        true_effect: Optional true effect value to show as vertical line
        title: Optional custom title
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(effects, bins=30, edgecolor="black", alpha=0.7, color="#3498db")

    if true_effect is not None:
        ax.axvline(
            true_effect,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"True Effect = {true_effect:.1%}",
        )

    mean_effect = np.mean(effects)
    ax.axvline(
        mean_effect,
        color="orange",
        linestyle="-",
        linewidth=2,
        label=f"Mean Effect = {mean_effect:.1%}",
    )

    ax.set_xlabel("Treatment Effect")
    ax.set_ylabel("Number of Products")
    ax.set_title(title or "Distribution of Individual Treatment Effects")
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_treatment_parameters(ate, att, atc, title=None):
    """Visualize ATE, ATT, ATC as bar chart.

    Args:
        ate: Average Treatment Effect
        att: Average Treatment on Treated
        atc: Average Treatment on Control
        title: Optional custom title
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    params = {"ATE": ate, "ATT": att, "ATC": atc}
    colors = ["#2ecc71", "#e74c3c", "#3498db"]

    bars = ax.bar(params.keys(), params.values(), color=colors, edgecolor="black")

    for bar, value in zip(bars, params.values()):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            f"${value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
        )

    ax.set_ylabel("Treatment Effect ($)")
    ax.set_title(title or "Population-Level Treatment Parameters")
    ax.axhline(0, color="black", linewidth=0.5)
    plt.tight_layout()
    plt.show()


def plot_bias_decomposition(ate, baseline_bias, naive_estimate, title=None):
    """Bar chart showing bias decomposition.

    Args:
        ate: True Average Treatment Effect
        baseline_bias: Baseline (selection) bias component
        naive_estimate: Naive difference-in-means estimate
        title: Optional custom title
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    components = {
        "True ATE": ate,
        "Baseline Bias": baseline_bias,
        "Naive Estimate": naive_estimate,
    }

    colors = ["#2ecc71", "#e74c3c", "#3498db"]
    x_pos = np.arange(len(components))

    bars = ax.bar(x_pos, components.values(), color=colors, edgecolor="black")

    for bar, (name, value) in zip(bars, components.items()):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(components.values()) * 0.02,
            f"${value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )

    ax.set_xticks(x_pos)
    ax.set_xticklabels(components.keys())
    ax.set_ylabel("Dollar Amount")
    ax.set_title(title or "Bias Decomposition: Why Naive Estimation Fails")
    ax.axhline(0, color="black", linewidth=0.5)
    plt.tight_layout()
    plt.show()


def plot_randomization_comparison(random_estimates, biased_estimates, true_ate):
    """Side-by-side histograms comparing random vs biased selection.

    Args:
        random_estimates: Array of estimates from random selection simulations
        biased_estimates: Array of estimates from biased selection simulations
        true_ate: True Average Treatment Effect
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Random selection (unbiased)
    axes[0].hist(
        random_estimates, bins=30, alpha=0.7, color="#2ecc71", edgecolor="black"
    )
    axes[0].axvline(
        true_ate,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"True ATE = ${true_ate:,.0f}",
    )
    axes[0].axvline(
        np.mean(random_estimates),
        color="blue",
        linestyle="-",
        linewidth=2,
        label=f"Mean = ${np.mean(random_estimates):,.0f}",
    )
    axes[0].set_title("Random Selection (Unbiased)")
    axes[0].set_xlabel("Estimated Treatment Effect ($)")
    axes[0].set_ylabel("Frequency")
    axes[0].legend()

    # Biased selection
    axes[1].hist(
        biased_estimates, bins=30, alpha=0.7, color="#e74c3c", edgecolor="black"
    )
    axes[1].axvline(
        true_ate,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"True ATE = ${true_ate:,.0f}",
    )
    axes[1].axvline(
        np.mean(biased_estimates),
        color="blue",
        linestyle="-",
        linewidth=2,
        label=f"Mean = ${np.mean(biased_estimates):,.0f}",
    )
    axes[1].set_title("Selection on Performance (Biased)")
    axes[1].set_xlabel("Estimated Treatment Effect ($)")
    axes[1].set_ylabel("Frequency")
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def plot_time_series_treatment(daily_data, treatment_start, title=None):
    """Plot daily revenue with treatment start line.

    Args:
        daily_data: DataFrame with 'date' and 'revenue' columns
        treatment_start: Treatment start date string (YYYY-MM-DD)
        title: Optional custom title
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    daily_data = daily_data.copy()
    daily_data["date"] = pd.to_datetime(daily_data["date"])

    ax.plot(
        daily_data["date"],
        daily_data["revenue"],
        marker="o",
        linewidth=2,
        markersize=4,
        color="#3498db",
    )
    ax.fill_between(
        daily_data["date"], daily_data["revenue"], alpha=0.3, color="#3498db"
    )

    ax.axvline(
        pd.to_datetime(treatment_start),
        color="red",
        linestyle="--",
        linewidth=2,
        label="Treatment Start",
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue ($)")
    ax.set_title(title or "Daily Revenue with Treatment Period")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_bootstrap_distribution(estimates, true_ate=None, title=None):
    """Plot bootstrap distribution with confidence interval.

    Args:
        estimates: Array of bootstrap estimates
        true_ate: Optional true ATE to show as vertical line
        title: Optional custom title
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(estimates, bins=40, edgecolor="black", alpha=0.7, color="#9b59b6")

    if true_ate is not None:
        ax.axvline(
            true_ate,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"True ATE = ${true_ate:,.0f}",
        )

    mean_est = np.mean(estimates)
    ax.axvline(
        mean_est,
        color="blue",
        linestyle="-",
        linewidth=2,
        label=f"Bootstrap Mean = ${mean_est:,.0f}",
    )

    # Confidence interval
    ci_low, ci_high = np.percentile(estimates, [2.5, 97.5])
    ax.axvspan(
        ci_low,
        ci_high,
        alpha=0.2,
        color="blue",
        label=f"95% CI: [${ci_low:,.0f}, ${ci_high:,.0f}]",
    )

    ax.set_xlabel("Estimated Treatment Effect ($)")
    ax.set_ylabel("Frequency")
    ax.set_title(title or "Bootstrap Distribution of Treatment Effect Estimate")
    ax.legend()
    plt.tight_layout()
    plt.show()

    return ci_low, ci_high


def create_fundamental_problem_table(df, n_rows=10):
    """Display table showing observed/missing potential outcomes.

    Args:
        df: DataFrame with columns 'asin', 'D', 'Y', 'Y_1', 'Y_0'
        n_rows: Number of rows to display

    Returns:
        Styled DataFrame showing the fundamental problem
    """
    display_df = df[["asin", "D", "Y", "Y_1", "Y_0"]].head(n_rows).copy()

    # Format for display
    display_df["D"] = display_df["D"].map({1: "Treated", 0: "Control"})
    display_df["Y"] = display_df["Y"].apply(lambda x: f"${x:,.2f}")
    display_df["Y_1"] = display_df["Y_1"].apply(
        lambda x: f"${x:,.2f}" if pd.notna(x) else "?"
    )
    display_df["Y_0"] = display_df["Y_0"].apply(
        lambda x: f"${x:,.2f}" if pd.notna(x) else "?"
    )

    display_df.columns = ["Product", "Treatment", "Observed", "Y(1)", "Y(0)"]

    return display_df


def compute_bias_components(
    df, treatment_col="D", outcome_col="Y", y1_col="Y_1", y0_col="Y_0"
):
    """Calculate baseline and differential treatment effect bias.

    Args:
        df: DataFrame with potential outcomes
        treatment_col: Column name for treatment indicator
        outcome_col: Column name for observed outcome
        y1_col: Column name for potential outcome under treatment
        y0_col: Column name for potential outcome under control

    Returns:
        Dictionary with ATE, baseline_bias, and naive_estimate
    """
    treated = df[df[treatment_col] == 1]
    control = df[df[treatment_col] == 0]

    # Naive estimate
    naive_estimate = treated[outcome_col].mean() - control[outcome_col].mean()

    # True ATE (requires knowing both potential outcomes)
    if y1_col in df.columns and y0_col in df.columns:
        # Fill in the counterfactuals from the actual data
        df_full = df.copy()
        ate = df_full[y1_col].mean() - df_full[y0_col].mean()

        # Baseline bias: E[Y0|D=1] - E[Y0|D=0]
        # For treated: Y0 is counterfactual, for control: Y0 is observed
        e_y0_d1 = treated[y0_col].mean() if y0_col in treated.columns else None
        e_y0_d0 = (
            control[y0_col].mean()
            if y0_col in control.columns
            else control[outcome_col].mean()
        )

        if e_y0_d1 is not None:
            baseline_bias = e_y0_d1 - e_y0_d0
        else:
            baseline_bias = naive_estimate - ate
    else:
        ate = None
        baseline_bias = None

    return {
        "ate": ate,
        "baseline_bias": baseline_bias,
        "naive_estimate": naive_estimate,
    }
