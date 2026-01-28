"""Support functions for the Potential Outcome Model notebook."""

# Third-party packages
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# Print Helper Functions
# =============================================================================


def print_ite_summary(effects):
    """
    Print summary statistics for individual treatment effects.

    Parameters
    ----------
    effects : array-like
        Individual treatment effects.
    """
    print("Individual Treatment Effects:")
    print(f"  Mean: ${np.mean(effects):,.2f}")
    print(f"  Std:  ${np.std(effects):,.2f}")
    print(f"  Min:  ${np.min(effects):,.2f}")
    print(f"  Max:  ${np.max(effects):,.2f}")


def print_naive_estimator(treated_mean, control_mean, true_ate, title="Naive Estimator"):
    """
    Print naive estimator results with comparison to true ATE.

    Parameters
    ----------
    treated_mean : float
        Mean outcome for treated group.
    control_mean : float
        Mean outcome for control group.
    true_ate : float
        True Average Treatment Effect.
    title : str, optional
        Title for the output block.
    """
    estimate = treated_mean - control_mean
    bias = estimate - true_ate

    print(f"{title}:")
    print(f"  E[Y | D=1] = ${treated_mean:,.2f}")
    print(f"  E[Y | D=0] = ${control_mean:,.2f}")
    print(f"  Naive estimate = ${estimate:,.2f}")
    print(f"\nTrue ATE = ${true_ate:,.2f}")
    print(f"Bias = ${bias:,.2f}")


def print_bias_decomposition(baseline_bias, differential_effect_bias, naive_estimate, true_ate):
    """
    Print bias decomposition showing baseline and differential effect components.

    Parameters
    ----------
    baseline_bias : float
        Baseline (selection) bias component.
    differential_effect_bias : float
        Differential treatment effect bias component.
    naive_estimate : float
        Naive difference-in-means estimate.
    true_ate : float
        True Average Treatment Effect.
    """
    total_bias = baseline_bias + differential_effect_bias
    actual_bias = naive_estimate - true_ate

    print("Bias Decomposition:")
    print(f"  Baseline bias:                ${baseline_bias:,.2f}  (treated have higher Y0)")
    print(f"  Differential treatment effect: ${differential_effect_bias:,.2f}")
    print("  " + "─" * 40)
    print(f"  Total bias:                   ${total_bias:,.2f}")
    print(f"\nActual bias (Naive - ATE):      ${actual_bias:,.2f}")


# =============================================================================
# Data Generation Functions
# =============================================================================


def generate_quality_score(revenue, seed=42, noise_std=0.5):
    """
    Generate quality score correlated with revenue.

    Higher revenue products get higher quality scores (realistic assumption:
    good content quality drives higher sales).

    Parameters
    ----------
    revenue : pandas.Series or numpy.ndarray
        Baseline revenue values.
    seed : int, optional
        Random seed for reproducibility. Default is 42.
    noise_std : float, optional
        Standard deviation of noise. Default is 0.5.

    Returns
    -------
    numpy.ndarray
        Quality scores in range [1, 5].
    """
    rng = np.random.default_rng(seed)

    # Normalize revenue to 0-1 range
    revenue_min = revenue.min()
    revenue_max = revenue.max()
    revenue_normalized = (revenue - revenue_min) / (revenue_max - revenue_min + 1e-6)

    # Map to 1-5 scale with noise
    quality = 1 + 4 * revenue_normalized + rng.normal(0, noise_std, len(revenue))

    return np.clip(quality, 1, 5).round(1)


def plot_individual_effects_distribution(effects, true_effect=None, title=None):
    """
    Plot histogram of individual treatment effects.

    Parameters
    ----------
    effects : array-like
        Individual treatment effects.
    true_effect : float, optional
        True effect value to show as vertical line.
    title : str, optional
        Custom title for the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(effects, bins="auto", edgecolor="black", alpha=0.7, color="#3498db")

    if true_effect is not None:
        ax.axvline(true_effect, color="red", linestyle="--", linewidth=2, label=f"True Effect = ${true_effect:,.0f}")

    mean_effect = np.mean(effects)
    ax.axvline(mean_effect, color="orange", linestyle="-", linewidth=2, label=f"Mean Effect = ${mean_effect:,.0f}")

    ax.set_xlabel("Treatment Effect ($)")
    ax.set_ylabel("Number of Products")
    ax.set_title(title or "Distribution of Individual Treatment Effects")
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_treatment_parameters(ate, att, atc, title=None):
    """
    Visualize ATE, ATT, ATC as bar chart.

    Parameters
    ----------
    ate : float
        Average Treatment Effect.
    att : float
        Average Treatment on Treated.
    atc : float
        Average Treatment on Control.
    title : str, optional
        Custom title for the plot.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    params = {"ATE": ate, "ATT": att, "ATC": atc}
    colors = ["#2ecc71", "#e74c3c", "#3498db"]

    bars = ax.bar(params.keys(), params.values(), color=colors, edgecolor="black")

    for bar, value in zip(bars, params.values()):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(params.values()) * 0.02,
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


def plot_bias_decomposition(ate, baseline_bias, naive_estimate, selection_on_gains=None, title=None):
    """
    Create bar chart showing bias decomposition.

    Parameters
    ----------
    ate : float
        True Average Treatment Effect.
    baseline_bias : float
        Baseline (selection) bias component.
    naive_estimate : float
        Naive difference-in-means estimate.
    selection_on_gains : float, optional
        Selection on gains component.
    title : str, optional
        Custom title for the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    if selection_on_gains is not None:
        components = {
            "True ATE": ate,
            "Baseline Bias": baseline_bias,
            "Selection on Gains": selection_on_gains,
            "Naive Estimate": naive_estimate,
        }
        colors = ["#2ecc71", "#e74c3c", "#9b59b6", "#3498db"]
    else:
        components = {
            "True ATE": ate,
            "Baseline Bias": baseline_bias,
            "Naive Estimate": naive_estimate,
        }
        colors = ["#2ecc71", "#e74c3c", "#3498db"]

    x_pos = np.arange(len(components))

    bars = ax.bar(x_pos, components.values(), color=colors, edgecolor="black")

    for bar, (_, value) in zip(bars, components.items()):
        y_offset = max(abs(v) for v in components.values()) * 0.02
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
    ax.set_xticklabels(components.keys())
    ax.set_ylabel("Dollar Amount")
    ax.set_title(title or "Bias Decomposition: Why Naive Estimation Fails")
    ax.axhline(0, color="black", linewidth=0.5)
    plt.tight_layout()
    plt.show()


def plot_randomization_comparison(random_estimates, biased_estimates, true_ate):
    """
    Create side-by-side histograms comparing random vs biased selection.

    Parameters
    ----------
    random_estimates : array-like
        Estimates from random selection simulations.
    biased_estimates : array-like
        Estimates from biased selection simulations.
    true_ate : float
        True Average Treatment Effect.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Random selection (unbiased)
    axes[0].hist(random_estimates, bins=30, alpha=0.7, color="#2ecc71", edgecolor="black")
    axes[0].axvline(true_ate, color="red", linestyle="--", linewidth=2, label=f"True ATE = ${true_ate:,.0f}")
    random_mean = np.mean(random_estimates)
    axes[0].axvline(random_mean, color="blue", linestyle="-", linewidth=2, label=f"Mean = ${random_mean:,.0f}")
    axes[0].set_title("Random Selection (Unbiased)")
    axes[0].set_xlabel("Estimated Treatment Effect ($)")
    axes[0].set_ylabel("Frequency")
    axes[0].legend()

    # Biased selection
    axes[1].hist(biased_estimates, bins=30, alpha=0.7, color="#e74c3c", edgecolor="black")
    axes[1].axvline(true_ate, color="red", linestyle="--", linewidth=2, label=f"True ATE = ${true_ate:,.0f}")
    biased_mean = np.mean(biased_estimates)
    axes[1].axvline(biased_mean, color="blue", linestyle="-", linewidth=2, label=f"Mean = ${biased_mean:,.0f}")
    axes[1].set_title("Selection on Quality (Biased)")
    axes[1].set_xlabel("Estimated Treatment Effect ($)")
    axes[1].set_ylabel("Frequency")
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def plot_bootstrap_distribution(estimates, true_ate=None, title=None):
    """
    Plot bootstrap distribution with confidence interval.

    Parameters
    ----------
    estimates : array-like
        Bootstrap estimates.
    true_ate : float, optional
        True ATE to show as vertical line.
    title : str, optional
        Custom title for the plot.

    Returns
    -------
    tuple
        Lower and upper bounds of 95% confidence interval (ci_low, ci_high).
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(estimates, bins=40, edgecolor="black", alpha=0.7, color="#9b59b6")

    if true_ate is not None:
        ax.axvline(true_ate, color="red", linestyle="--", linewidth=2, label=f"True ATE = ${true_ate:,.0f}")

    mean_est = np.mean(estimates)
    ax.axvline(mean_est, color="blue", linestyle="-", linewidth=2, label=f"Bootstrap Mean = ${mean_est:,.0f}")

    # Confidence interval
    ci_low, ci_high = np.percentile(estimates, [2.5, 97.5])
    ax.axvspan(ci_low, ci_high, alpha=0.2, color="blue", label=f"95% CI: [${ci_low:,.0f}, ${ci_high:,.0f}]")

    ax.set_xlabel("Estimated Treatment Effect ($)")
    ax.set_ylabel("Frequency")
    ax.set_title(title or "Bootstrap Distribution of Treatment Effect Estimate")
    ax.legend()
    plt.tight_layout()
    plt.show()

    return ci_low, ci_high


def plot_outcome_by_treatment(treated_outcomes, control_outcomes, title=None):
    """
    Plot overlapping histograms of outcomes by treatment status.

    Parameters
    ----------
    treated_outcomes : array-like
        Outcomes for treated group.
    control_outcomes : array-like
        Outcomes for control group.
    title : str, optional
        Custom title for the plot.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.hist(
        control_outcomes,
        bins=30,
        alpha=0.6,
        color="#3498db",
        edgecolor="black",
        label=f"Control (n={len(control_outcomes)})",
    )
    ax.hist(
        treated_outcomes,
        bins=30,
        alpha=0.6,
        color="#e74c3c",
        edgecolor="black",
        label=f"Treated (n={len(treated_outcomes)})",
    )

    # Add mean lines
    control_mean, treated_mean = np.mean(control_outcomes), np.mean(treated_outcomes)
    ax.axvline(control_mean, color="#3498db", linestyle="--", linewidth=2, label=f"Control Mean = ${control_mean:,.0f}")
    ax.axvline(treated_mean, color="#e74c3c", linestyle="--", linewidth=2, label=f"Treated Mean = ${treated_mean:,.0f}")

    ax.set_xlabel("Revenue ($)")
    ax.set_ylabel("Number of Products")
    ax.set_title(title or "Distribution of Outcomes by Treatment Status")
    ax.legend()
    ax.set_xlim(0, None)
    plt.tight_layout()
    plt.show()


def plot_balance_check(df, covariates, treatment_col="D", title=None, percentile_clip=95):
    """
    Visualize covariate balance between treatment groups.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with covariates and treatment indicator.
    covariates : list of str
        Column names to check for balance.
    treatment_col : str, optional
        Column name for treatment indicator. Default is 'D'.
    title : str, optional
        Custom title for the plot.
    percentile_clip : int, optional
        Percentile to clip outliers for continuous variables. Default is 95.
    """
    treated = df[df[treatment_col] == 1]
    control = df[df[treatment_col] == 0]

    n_covs = len(covariates)
    fig, axes = plt.subplots(1, n_covs, figsize=(5 * n_covs, 5))

    if n_covs == 1:
        axes = [axes]

    for ax, cov in zip(axes, covariates):
        treated_vals = treated[cov]
        control_vals = control[cov]

        # For continuous variables, use histograms
        if treated_vals.nunique() > 10:
            # Clip outliers for better visualization
            upper_bound = np.percentile(df[cov], percentile_clip)
            treated_clipped = treated_vals.clip(upper=upper_bound)
            control_clipped = control_vals.clip(upper=upper_bound)

            ax.hist(
                control_clipped,
                bins=20,
                alpha=0.6,
                color="#3498db",
                edgecolor="black",
                label="Control",
                density=True,
            )
            ax.hist(
                treated_clipped,
                bins=20,
                alpha=0.6,
                color="#e74c3c",
                edgecolor="black",
                label="Treated",
                density=True,
            )
            ax.set_ylabel("Density")
        else:
            # For categorical/discrete, use bar chart
            x = np.arange(2)
            width = 0.35
            ax.bar(
                x - width / 2,
                [control_vals.mean(), treated_vals.mean()],
                width,
                label="Mean",
                color=["#3498db", "#e74c3c"],
                edgecolor="black",
            )
            ax.set_xticks(x)
            ax.set_xticklabels(["Control", "Treated"])
            ax.set_ylabel("Mean")

        ax.set_title(cov.replace("_", " ").title())
        ax.legend()

    plt.suptitle(title or "Covariate Balance Check", fontsize=14)
    plt.tight_layout()
    plt.show()

    # Also print summary statistics
    print("\nBalance Summary (Mean by Treatment Status):")
    print("-" * 50)
    for cov in covariates:
        ctrl_mean = control[cov].mean()
        treat_mean = treated[cov].mean()
        diff = treat_mean - ctrl_mean
        print(f"{cov:20s}: Control={ctrl_mean:8.2f}, Treated={treat_mean:8.2f}, Diff={diff:+8.2f}")


def plot_sample_size_convergence(sample_sizes, estimates_by_size, true_ate):
    """
    Plot how estimator variance decreases with sample size.

    Parameters
    ----------
    sample_sizes : list
        List of sample sizes used.
    estimates_by_size : dict
        Dictionary mapping sample size to list of estimates.
    true_ate : float
        True Average Treatment Effect.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left panel: distributions at each sample size
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(sample_sizes)))

    for i, (n, color) in enumerate(zip(sample_sizes, colors)):
        estimates = estimates_by_size[n]
        axes[0].hist(
            estimates,
            bins=30,
            alpha=0.5,
            color=color,
            edgecolor="black",
            linewidth=0.5,
            label=f"n = {n}",
        )

    axes[0].axvline(true_ate, color="red", linestyle="--", linewidth=2, label=f"True ATE = ${true_ate:,.0f}")
    axes[0].set_xlabel("Estimated Treatment Effect ($)")
    axes[0].set_ylabel("Frequency")
    axes[0].set_title("Sampling Distributions by Sample Size")
    axes[0].legend()

    # Right panel: standard deviation vs sample size
    std_devs = [np.std(estimates_by_size[n]) for n in sample_sizes]

    axes[1].plot(sample_sizes, std_devs, "o-", color="#3498db", linewidth=2, markersize=8)
    axes[1].set_xlabel("Sample Size (n)")
    axes[1].set_ylabel("Standard Deviation of Estimate ($)")
    axes[1].set_title("Uncertainty Decreases with Sample Size")

    # Add theoretical 1/sqrt(n) reference line
    theoretical = std_devs[0] * np.sqrt(sample_sizes[0]) / np.sqrt(sample_sizes)
    axes[1].plot(sample_sizes, theoretical, "--", color="gray", linewidth=1.5, label=r"$\propto 1/\sqrt{n}$")
    axes[1].legend()

    plt.tight_layout()
    plt.show()


def plot_fundamental_problem_table(df, n_rows=10):
    """
    Display table showing observed/missing potential outcomes.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with columns 'asin', 'D', 'Y', 'Y_1', 'Y_0'.
    n_rows : int, optional
        Number of rows to display. Default is 10.

    Returns
    -------
    pandas.DataFrame
        Styled DataFrame showing the fundamental problem.
    """
    display_df = df[["asin", "D", "Y", "Y_1", "Y_0"]].head(n_rows).copy()

    # Mask counterfactuals
    display_df["Y_1_obs"] = np.where(display_df["D"] == 1, display_df["Y_1"], np.nan)
    display_df["Y_0_obs"] = np.where(display_df["D"] == 0, display_df["Y_0"], np.nan)

    result = display_df[["asin", "D", "Y", "Y_1_obs", "Y_0_obs"]].copy()
    result.columns = ["Product", "D", "Observed (Y)", "Y(1)", "Y(0)"]
    result["D"] = result["D"].map({1: "Treated", 0: "Control"})

    return result
