"""Support functions for the Generalized Roy Model lecture."""

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


def plot_treatment_effects_comparison(with_eh=True, without_eh=True):
    """
    Plot treatment effect distributions with and without essential heterogeneity.

    Parameters
    ----------
    with_eh : bool, optional
        Whether to show panel with essential heterogeneity (default: True).
    without_eh : bool, optional
        Whether to show panel without essential heterogeneity (default: True).
    """
    x_axis = np.arange(-2, 4, 0.001)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    configs = [
        ({"TT": 1.3, "TUT": 0.7, "ATE": 1.0}, "With Essential Heterogeneity"),
        ({"TT": 1.0, "TUT": 1.0, "ATE": 1.0}, "Without Essential Heterogeneity"),
    ]

    for ax, (effects, title) in zip(axes, configs):
        ax.plot(x_axis, norm.pdf(x_axis, 1, 1))
        ax.set_xlim(-2, 4)
        ax.set_ylim(0.0, None)
        ax.set_yticks([])
        ax.set_ylabel("$f_{Y_1 - Y_0}$")
        ax.set_xlabel("$Y_1 - Y_0$")
        ax.set_title(title)

        for label, value in effects.items():
            ax.axvline(value, label=label)

        ax.legend(prop={"size": 12})

    plt.tight_layout()
    plt.show()


def plot_marginal_treatment_effect(mte_presence, mte_absence, grid):
    """
    Plot marginal treatment effect with and without essential heterogeneity.

    Parameters
    ----------
    mte_presence : array-like
        MTE values in presence of essential heterogeneity.
    mte_absence : array-like
        MTE values in absence of essential heterogeneity.
    grid : array-like
        Grid of u_S values (0 to 1).
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(grid, mte_presence, label="Presence of EH")
    ax.plot(grid, mte_absence, label="Absence of EH", linestyle="--")

    ax.set_ylabel(r"$B^{MTE}$")
    ax.set_xlabel("$u_S$")
    ax.set_ylim([1.5, 4.5])
    ax.legend()

    plt.tight_layout()
    plt.show()


def plot_weights_marginal_effect(ate_weights, tt_weights, tut_weights, mte, grid):
    """
    Plot weights for treatment parameters alongside the MTE.

    Parameters
    ----------
    ate_weights : array-like
        Weights for Average Treatment Effect.
    tt_weights : array-like
        Weights for Treatment on Treated.
    tut_weights : array-like
        Weights for Treatment on Untreated.
    mte : array-like
        Marginal Treatment Effect values.
    grid : array-like
        Grid of u_S values (0 to 1).
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.set_xlabel(r"$u_S$")
    ax.set_ylabel(r"$\omega(u_S)$")
    ax.set_ylim(0, 4.5)
    ax.set_xlim(0.0, 1.0)

    ax.plot(grid, ate_weights, label=r"$\omega^{ATE}$", linestyle=":")
    ax.plot(grid, tt_weights, label=r"$\omega^{TT}$", linestyle="--")
    ax.plot(grid, tut_weights, label=r"$\omega^{TUT}$", linestyle="-.")
    ax.plot(grid, mte, label="MTE")

    ax.legend()

    ax2 = ax.twinx()
    ax2.set_ylabel("MTE")
    ax2.set_ylim(0, 0.35)

    plt.tight_layout()
    plt.show()


def plot_local_average_treatment(mte, grid):
    """
    Plot local average treatment effect illustration.

    Parameters
    ----------
    mte : array-like
        Marginal Treatment Effect values.
    grid : list
        Grid of u_S values (0 to 1).
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(grid, mte)

    for xtick in [0.2, 0.3, 0.4, 0.6, 0.7, 0.8]:
        index = grid.index(xtick) if isinstance(grid, list) else np.argmin(np.abs(np.array(grid) - xtick))
        height = mte[index]
        ax.plot((xtick, xtick), (0, height), color="grey", alpha=0.7)

    ax.set_xlabel("$u_S$")
    ax.set_ylabel(r"$MTE$")
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_xticklabels([0, "$p_1$", "$p_2$", "$p_3$", "$p_4$", 1])
    ax.set_ylim([1.5, 4.5])

    plt.tight_layout()
    plt.show()
