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


def print_balance_summary(df, covariates, treatment_col="D"):
    """
    Print mean covariate values by treatment status.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with covariates and treatment indicator.
    covariates : list of str
        Column names to summarize.
    treatment_col : str, optional
        Column name for treatment indicator. Default is 'D'.
    """
    treated = df[df[treatment_col] == 1]
    control = df[df[treatment_col] == 0]

    print("\nBalance Summary (Mean by Treatment Status):")
    print("-" * 50)
    for cov in covariates:
        ctrl_mean = control[cov].mean()
        treat_mean = treated[cov].mean()
        diff = treat_mean - ctrl_mean
        print(f"{cov:20s}: Control={ctrl_mean:8.2f}, Treated={treat_mean:8.2f}, Diff={diff:+8.2f}")


# =============================================================================
# Data Generation Functions
# =============================================================================


def create_confounded_treatment(metrics_df, treatment_fraction=0.3, true_effect=0.5, seed=42):
    """
    Create confounded treatment assignment from raw simulator metrics.

    Aggregates revenue per product, generates a quality score, then assigns
    treatment deterministically to the lowest-quality products (struggling
    products get optimized). This creates negative selection bias: treated
    products have lower baseline revenue.

    Parameters
    ----------
    metrics_df : pandas.DataFrame
        Metrics DataFrame with ``product_identifier`` and ``revenue`` columns.
    treatment_fraction : float
        Fraction of products to treat (selected from the bottom by quality).
    true_effect : float
        True causal effect of treatment (proportional increase in revenue).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns ``product_identifier``, ``quality_score``,
        ``D``, ``Y0``, ``Y1``, ``Y_observed``.
    """
    product_revenue = metrics_df.groupby("product_identifier")["revenue"].sum().reset_index()
    product_revenue.columns = ["product_identifier", "baseline_revenue"]

    product_revenue["quality_score"] = generate_quality_score(product_revenue["baseline_revenue"], seed=seed)

    # Treat bottom fraction by quality (struggling products get optimized)
    n_treat = int(len(product_revenue) * treatment_fraction)
    treated_ids = set(product_revenue.nsmallest(n_treat, "quality_score")["product_identifier"])
    product_revenue["D"] = product_revenue["product_identifier"].isin(treated_ids).astype(int)

    # Potential outcomes
    product_revenue["Y0"] = product_revenue["baseline_revenue"]
    product_revenue["Y1"] = product_revenue["baseline_revenue"] * (1 + true_effect)
    product_revenue["Y_observed"] = np.where(product_revenue["D"] == 1, product_revenue["Y1"], product_revenue["Y0"])

    return product_revenue[["product_identifier", "quality_score", "D", "Y0", "Y1", "Y_observed"]]


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
    _, ax = plt.subplots(figsize=(10, 6))

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
    _, axes = plt.subplots(1, 2, figsize=(14, 5))

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
    _, axes = plt.subplots(1, n_covs, figsize=(5 * n_covs, 5))

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

    print_balance_summary(df, covariates, treatment_col)


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
    _, axes = plt.subplots(1, 2, figsize=(14, 5))

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
