"""Support functions for the Generalized Roy Model lecture.

This module provides helper functions for:
- Treatment effect visualization
- Monte Carlo simulation comparing estimators
- Plotting estimated MTE from grmpy results
- Comparing naive, OLS, and IV estimates
"""

# Third-party packages
import grmpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import norm


def plot_treatment_effects_distribution(delta, ate, tt, tut, effect_est):
    """Plot distribution of treatment effects with vertical lines for parameters.

    Parameters
    ----------
    delta : array-like
        Individual treatment effects (Y1 - Y0).
    ate : float
        Average Treatment Effect.
    tt : float
        Treatment on the Treated.
    tut : float
        Treatment on the Untreated.
    effect_est : float
        Naive effect estimate (mean treated - mean untreated).

    Returns
    -------
    None
        Displays the plot directly.
    """
    plt.figure(figsize=(15, 10))
    plt.ylabel("$f_{Y_1 - Y_0}$", fontsize=20)
    plt.xlabel("$Y_1 - Y_0$", fontsize=20)
    plt.axis([-1, 2, 0.0, 1.31])

    # Plot distribution of individual effects
    sns.kdeplot(delta)

    # Plot average effect parameters
    plt.plot([ate, ate], [0.00, 1.3], label=r"$\Delta^{ATE}$")
    plt.plot([tt, tt], [0.00, 1.3], label=r"$\Delta^{TT}$")
    plt.plot([tut, tut], [0.00, 1.3], label=r"$\Delta^{TUT}$")
    plt.plot([effect_est, effect_est], [0.00, 1.3], label=r"$\hat{\Delta}$")

    plt.legend(prop={"size": 20})
    plt.show()


def plot_joint_distribution(df, title):
    """Plot joint distribution of V and U1 using seaborn jointplot.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with columns 'V' and 'U1'.
    title : str
        Title for the plot.

    Returns
    -------
    seaborn.JointGrid
        The jointplot grid object.
    """
    g = sns.jointplot(x=df["V"], y=df["U1"], height=10)
    g = g.set_axis_labels("$V$", "$U_1$", fontsize=18)
    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle(title, fontsize=22)
    return g


def plot_mte_comparison(configs, quantiles=None):
    """Plot MTE curves comparing with and without essential heterogeneity.

    Parameters
    ----------
    configs : list
        List of grmpy config objects [config_no_eh, config_eh].
    quantiles : array-like, optional
        Quantile grid. Defaults to np.arange(0.01, 1.0, 0.01).

    Returns
    -------
    None
        Displays the plot directly.
    """
    if quantiles is None:
        quantiles = np.arange(0.01, 1.0, 0.01)

    plt.figure(figsize=(15, 10))
    plt.ylabel(r"$\Delta^{MTE}$", fontsize=24)
    plt.xlabel("$u_D$", fontsize=24)

    labels = ["Without essential heterogeneity", "With essential heterogeneity"]
    colors = ["blue", "orange"]

    for counter, config in enumerate(configs):
        sim = config.simulation
        beta1 = np.array(sim.coefficients_treated)
        beta0 = np.array(sim.coefficients_untreated)
        cov = np.array(sim.covariance)
        cov1V = cov[0, 2]
        cov0V = cov[1, 2]

        mte_base = beta1[0] - beta0[0]
        mte = mte_base + (cov1V - cov0V) * norm.ppf(quantiles)

        plt.plot(quantiles, mte, label=labels[counter], color=colors[counter], linewidth=4)

    plt.legend(prop={"size": 20})
    plt.show()


def plot_mte_with_weights(quantiles, mte, omega_tt, omega_tut, omega_ate):
    """Plot MTE curve with treatment effect weights on secondary axis.

    Parameters
    ----------
    quantiles : array-like
        Quantile grid (0 to 1).
    mte : array-like
        Marginal Treatment Effect values.
    omega_tt : array-like
        Weights for Treatment on Treated.
    omega_tut : array-like
        Weights for Treatment on Untreated.
    omega_ate : array-like
        Weights for Average Treatment Effect.

    Returns
    -------
    None
        Displays the plot directly.
    """
    ax1 = plt.figure(figsize=(15, 10)).add_subplot(111)

    plt.ylabel(r"$\Delta^{MTE}$", fontsize=24)
    plt.xlabel("$u_D$", fontsize=24)
    ax1.plot(quantiles, mte, color="blue", label=r" $\Delta^{MTE}$", linewidth=3.0)

    ax2 = ax1.twinx()
    ax2.plot(quantiles, omega_tt, color="red", linestyle="--", label=r" $\omega^{TT}$", linewidth=3.0)
    ax2.plot(quantiles, omega_tut, color="green", linestyle="--", label=r" $\omega^{TUT}$", linewidth=3.0)
    ax2.plot(quantiles, omega_ate, color="orange", linestyle="-.", label=r" $\omega^{ATE}$", linewidth=3.0)

    plt.legend(prop={"size": 20})
    plt.show()


def compute_treatment_effects(df):
    """Compute treatment effect parameters from simulated data.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with columns 'D', 'Y', 'Y1', 'Y0'.

    Returns
    -------
    dict
        Dictionary with 'delta', 'ate', 'tt', 'tut', 'effect_est' keys.
    """
    is_treated = df["D"] == 1
    delta = df["Y1"] - df["Y0"]
    ate = np.mean(df["Y1"] - df["Y0"])
    tt = np.mean(df.loc[is_treated, "Y1"] - df.loc[is_treated, "Y0"])
    tut = np.mean(df.loc[~is_treated, "Y1"] - df.loc[~is_treated, "Y0"])
    effect_est = np.mean(df.loc[is_treated, "Y"]) - np.mean(df.loc[~is_treated, "Y"])

    return {
        "delta": delta,
        "ate": ate,
        "tt": tt,
        "tut": tut,
        "effect_est": effect_est,
    }


def compute_mte_weights(df, quantiles=None):
    """Compute MTE and weights for treatment effect parameters.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with simulated data including 'D' column.
    quantiles : array-like, optional
        Quantile grid. Defaults to np.arange(0.01, 1.0, 0.01).

    Returns
    -------
    dict
        Dictionary with 'omega_tt', 'omega_tut', 'omega_ate' arrays.
    """
    if quantiles is None:
        quantiles = np.arange(0.01, 1.0, 0.01)

    propensity_mean = df["D"].mean()

    omega_tt = np.array([(1 - quantiles[i]) for i in range(len(quantiles))]) / (1 - propensity_mean) * 2
    omega_tut = np.array([quantiles[i] for i in range(len(quantiles))]) / propensity_mean * 2
    omega_ate = np.ones(len(quantiles))

    # Normalize weights
    omega_tt = omega_tt / np.mean(omega_tt)
    omega_tut = omega_tut / np.mean(omega_tut)

    return {
        "omega_tt": omega_tt,
        "omega_tut": omega_tut,
        "omega_ate": omega_ate,
    }


def compute_mte(config, quantiles=None):
    """Compute MTE from grmpy config parameters.

    Parameters
    ----------
    config : Config
        grmpy configuration object.
    quantiles : array-like, optional
        Quantile grid. Defaults to np.arange(0.01, 1.0, 0.01).

    Returns
    -------
    np.ndarray
        MTE values at each quantile.
    """
    if quantiles is None:
        quantiles = np.arange(0.01, 1.0, 0.01)

    sim = config.simulation
    beta1 = np.array(sim.coefficients_treated)
    beta0 = np.array(sim.coefficients_untreated)
    cov = np.array(sim.covariance)
    cov1V = cov[0, 2]
    cov0V = cov[1, 2]

    mte_base = beta1[0] - beta0[0]
    mte = mte_base + (cov1V - cov0V) * norm.ppf(quantiles)

    return mte


def monte_carlo(base_config_path, num_iterations=100, rho_grid=None):
    """Run Monte Carlo comparing OLS, IV, and grmpy estimators across correlation levels.

    Parameters
    ----------
    base_config_path : str
        Path to base configuration file.
    num_iterations : int, optional
        Number of Monte Carlo iterations per correlation level. Default is 100.
    rho_grid : array-like, optional
        Grid of correlation values between U1 and V. Default is np.linspace(0, 0.9, 10).

    Returns
    -------
    dict
        Dictionary with keys 'rho', 'naive_mean', 'naive_std', 'ols_mean', 'ols_std',
        'iv_mean', 'iv_std', 'true_ate' containing arrays of estimates for each
        correlation level.
    """
    if rho_grid is None:
        rho_grid = np.linspace(0, 0.9, 10)

    base_config = grmpy.process_config(base_config_path)
    sim_config = base_config.simulation
    results = _initialize_mc_results(rho_grid)

    for rho in rho_grid:
        iteration_results = _run_mc_iterations(sim_config, rho, num_iterations)
        _append_mc_results(results, iteration_results)

    return results


def _initialize_mc_results(rho_grid):
    """Initialize Monte Carlo results dictionary.

    Parameters
    ----------
    rho_grid : array-like
        Grid of correlation values.

    Returns
    -------
    dict
        Empty results dictionary with initialized keys.
    """
    return {
        "rho": rho_grid,
        "naive_mean": [],
        "naive_std": [],
        "ols_mean": [],
        "ols_std": [],
        "iv_mean": [],
        "iv_std": [],
        "true_ate": [],
    }


def _run_mc_iterations(sim_config, rho, num_iterations):
    """Run all Monte Carlo iterations for a single correlation level.

    Parameters
    ----------
    sim_config : SimulationConfig
        Simulation configuration object.
    rho : float
        Correlation between U1 and V.
    num_iterations : int
        Number of iterations to run.

    Returns
    -------
    dict
        Dictionary with lists of estimates from each iteration.
    """
    naive_estimates = []
    ols_estimates = []
    iv_estimates = []
    true_ate = None

    for _ in range(num_iterations):
        df = _simulate_with_correlation(sim_config, rho)
        true_ate = np.mean(df["Y1"] - df["Y0"])

        # Naive comparison
        treated_mean = df.loc[df["D"] == 1, "Y"].mean()
        untreated_mean = df.loc[df["D"] == 0, "Y"].mean()
        naive_estimates.append(treated_mean - untreated_mean)

        # OLS estimate
        X_ols = sm.add_constant(df["D"])
        ols_model = sm.OLS(df["Y"], X_ols).fit()
        ols_estimates.append(ols_model.params["D"])

        # IV estimate
        iv_estimate = _iv_estimator(df)
        iv_estimates.append(iv_estimate)

    return {
        "naive": naive_estimates,
        "ols": ols_estimates,
        "iv": iv_estimates,
        "true_ate": true_ate,
    }


def _append_mc_results(results, iteration_results):
    """Append iteration results to main results dictionary.

    Parameters
    ----------
    results : dict
        Main results dictionary to update.
    iteration_results : dict
        Results from a single correlation level.

    Returns
    -------
    None
        Updates results in place.
    """
    results["naive_mean"].append(np.mean(iteration_results["naive"]))
    results["naive_std"].append(np.std(iteration_results["naive"]))
    results["ols_mean"].append(np.mean(iteration_results["ols"]))
    results["ols_std"].append(np.std(iteration_results["ols"]))
    results["iv_mean"].append(np.mean(iteration_results["iv"]))
    results["iv_std"].append(np.std(iteration_results["iv"]))
    results["true_ate"].append(iteration_results["true_ate"])


def _simulate_with_correlation(sim_config, rho):
    """Simulate data with a specific correlation between U1 and V.

    Parameters
    ----------
    sim_config : SimulationConfig
        Simulation configuration object.
    rho : float
        Correlation between U1 and V.

    Returns
    -------
    pd.DataFrame
        Simulated data with columns Y, Y1, Y0, D, X0, X1, Z.
    """
    # Get original covariance matrix
    cov = np.array(sim_config.covariance)
    sigma1 = np.sqrt(cov[0, 0])
    sigma_v = np.sqrt(cov[2, 2])

    # Set new covariance with specified rho
    cov_modified = cov.copy()
    cov_1v = rho * sigma1 * sigma_v
    cov_modified[0, 2] = cov_1v
    cov_modified[2, 0] = cov_1v

    # Simulate unobservables
    num_agents = sim_config.agents
    unobservables = np.random.multivariate_normal(np.zeros(3), cov_modified, num_agents)

    # Simulate covariates
    n_treated = len(sim_config.coefficients_treated)
    n_choice = len(sim_config.coefficients_choice)

    # First covariate is intercept
    X = np.ones((num_agents, max(n_treated, n_choice)))
    for i in range(1, max(n_treated, n_choice)):
        X[:, i] = np.random.standard_normal(num_agents)

    # Get coefficients
    beta1 = np.array(sim_config.coefficients_treated)
    beta0 = np.array(sim_config.coefficients_untreated)
    gamma = np.array(sim_config.coefficients_choice)

    # Potential outcomes
    Y1 = X[:, :n_treated] @ beta1 + unobservables[:, 0]
    Y0 = X[:, : len(beta0)] @ beta0 + unobservables[:, 1]

    # Treatment decision
    Z = X[:, :n_choice]
    D = (Z @ gamma > unobservables[:, 2]).astype(float)

    # Observed outcome
    Y = D * Y1 + (1 - D) * Y0

    return pd.DataFrame(
        {
            "Y": Y,
            "Y1": Y1,
            "Y0": Y0,
            "D": D,
            "X0": X[:, 0],
            "X1": X[:, 1] if X.shape[1] > 1 else np.zeros(num_agents),
            "Z": X[:, 2] if X.shape[1] > 2 else np.random.standard_normal(num_agents),
        }
    )


def _iv_estimator(df):
    """Compute IV estimate using two-stage least squares.

    Parameters
    ----------
    df : pd.DataFrame
        Data with columns Y, D, Z.

    Returns
    -------
    float
        IV estimate of treatment effect.
    """
    # First stage: regress D on Z
    Z = sm.add_constant(df[["X0", "X1", "Z"]] if "Z" in df.columns else df[["X0", "X1"]])

    # Check if we have an instrument
    if "Z" not in df.columns:
        Z_cols = [c for c in df.columns if c.startswith("Z")]
        if not Z_cols:
            return np.nan
        Z = sm.add_constant(df[Z_cols])

    first_stage = sm.OLS(df["D"], Z).fit()
    D_hat = first_stage.fittedvalues

    # Second stage: regress Y on fitted D
    X_2sls = sm.add_constant(D_hat)
    second_stage = sm.OLS(df["Y"], X_2sls).fit()

    return second_stage.params.iloc[1]


def plot_monte_carlo_results(results, ax=None):
    """Plot Monte Carlo simulation results.

    Parameters
    ----------
    results : dict
        Results dictionary from monte_carlo function.
    ax : matplotlib.axes.Axes, optional
        Axes to plot on. If None, creates new figure.

    Returns
    -------
    matplotlib.figure.Figure
        The figure object.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))
    else:
        fig = ax.get_figure()

    rho = results["rho"]

    # Plot true ATE
    ax.axhline(
        y=results["true_ate"][0],
        color="black",
        linestyle="--",
        label="True ATE",
        linewidth=2,
    )

    # Plot estimator means with error bands
    ax.plot(rho, results["naive_mean"], "o-", label="Naive", color="red", linewidth=2)
    ax.fill_between(
        rho,
        np.array(results["naive_mean"]) - np.array(results["naive_std"]),
        np.array(results["naive_mean"]) + np.array(results["naive_std"]),
        alpha=0.2,
        color="red",
    )

    ax.plot(rho, results["ols_mean"], "s-", label="OLS", color="blue", linewidth=2)
    ax.fill_between(
        rho,
        np.array(results["ols_mean"]) - np.array(results["ols_std"]),
        np.array(results["ols_mean"]) + np.array(results["ols_std"]),
        alpha=0.2,
        color="blue",
    )

    ax.plot(rho, results["iv_mean"], "^-", label="IV", color="green", linewidth=2)
    ax.fill_between(
        rho,
        np.array(results["iv_mean"]) - np.array(results["iv_std"]),
        np.array(results["iv_mean"]) + np.array(results["iv_std"]),
        alpha=0.2,
        color="green",
    )

    ax.set_xlabel(r"$\rho_{U_1, V}$", fontsize=16)
    ax.set_ylabel("Estimated ATE", fontsize=16)
    ax.set_title("Monte Carlo: Comparison of Estimators", fontsize=18)
    ax.legend(fontsize=14)
    ax.grid(True, alpha=0.3)

    return fig


def plot_est_mte(result, config_path=None, ax=None):
    """Plot estimated MTE from grmpy.estimate() result.

    Parameters
    ----------
    result : EstimationResult
        Result from grmpy.estimate().
    config_path : str, optional
        Path to config file (for true parameter comparison).
    ax : matplotlib.axes.Axes, optional
        Axes to plot on. If None, creates new figure.

    Returns
    -------
    tuple
        (mte array, quantiles array).
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 8))

    quantiles = result.quantiles
    mte = result.mte

    ax.plot(quantiles, mte, label="Estimated MTE", color="blue", linewidth=2)

    # If config provided, plot true MTE for comparison
    if config_path is not None:
        config = grmpy.process_config(config_path)
        sim = config.simulation
        if sim is not None:
            beta1 = np.array(sim.coefficients_treated)
            beta0 = np.array(sim.coefficients_untreated)
            cov = np.array(sim.covariance)
            cov1V = cov[0, 2]
            cov0V = cov[1, 2]

            mte_base = beta1[0] - beta0[0]
            mte_true = mte_base + (cov1V - cov0V) * norm.ppf(quantiles)

            ax.plot(
                quantiles,
                mte_true,
                label="True MTE",
                color="red",
                linestyle="--",
                linewidth=2,
            )

    ax.set_xlabel(r"$u_D$", fontsize=16)
    ax.set_ylabel(r"$\Delta^{MTE}$", fontsize=16)
    ax.set_title("Marginal Treatment Effect", fontsize=18)
    ax.legend(fontsize=14)
    ax.grid(True, alpha=0.3)

    return mte, quantiles


def compare_estimators(df, true_ate=None):
    """Compare Naive, OLS, and IV estimates to true ATE.

    Parameters
    ----------
    df : pd.DataFrame
        Data with columns Y, D, and optionally Y1, Y0.
    true_ate : float, optional
        True ATE. If None, computed from Y1 and Y0 if available.

    Returns
    -------
    pd.DataFrame
        DataFrame with estimator names and their estimates.
    """
    results = []

    # True ATE
    if true_ate is None and "Y1" in df.columns and "Y0" in df.columns:
        true_ate = np.mean(df["Y1"] - df["Y0"])
    if true_ate is not None:
        results.append({"Estimator": "True ATE", "Estimate": true_ate})

    # Naive comparison
    treated_mean = df.loc[df["D"] == 1, "Y"].mean()
    untreated_mean = df.loc[df["D"] == 0, "Y"].mean()
    naive = treated_mean - untreated_mean
    results.append({"Estimator": "Naive", "Estimate": naive})

    # OLS
    X_ols = sm.add_constant(df["D"])
    ols_model = sm.OLS(df["Y"], X_ols).fit()
    results.append({"Estimator": "OLS", "Estimate": ols_model.params["D"]})

    # IV using available instruments
    Z_cols = [c for c in df.columns if c.startswith("Z")]
    if Z_cols:
        Z = sm.add_constant(df[Z_cols])
        first_stage = sm.OLS(df["D"], Z).fit()
        D_hat = first_stage.fittedvalues
        X_2sls = sm.add_constant(D_hat)
        second_stage = sm.OLS(df["Y"], X_2sls).fit()
        results.append({"Estimator": "IV", "Estimate": second_stage.params.iloc[1]})

    return pd.DataFrame(results)
