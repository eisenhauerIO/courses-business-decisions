"""Support functions for the Synthetic Control lecture."""

# Standard library
import importlib.util
from pathlib import Path

# Third-party packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Shared utilities (re-exported so notebooks can import from support)
_shared_path = Path(__file__).resolve().parent.parent / "shared.py"
_spec = importlib.util.spec_from_file_location("shared", _shared_path)
_shared = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_shared)
plot_method_comparison = _shared.plot_method_comparison  # noqa: F811


def _parse_weights(weights_dict):
    """Parse weights from SC result into a clean unit-to-weight mapping.

    The pysyncon library returns weights as a DataFrame; after .to_dict() this
    may be nested ({"col": {"unit": w}}) or flat ({"unit": w}).

    Parameters
    ----------
    weights_dict : dict
        Weights dictionary from sc_result.data["model_summary"]["weights"].

    Returns
    -------
    dict
        Mapping of unit identifier (str) to weight (float).
    """
    parsed = {}
    for key, val in weights_dict.items():
        if isinstance(val, dict):
            for unit, w in val.items():
                parsed[str(unit)] = float(w)
        else:
            parsed[str(key)] = float(val)
    return parsed


def create_synthetic_control_data(metrics_df, treatment_date="2024-11-15", true_effect=50.0, seed=42):
    """Create panel data with a single treated product for synthetic control analysis.

    Aggregates daily revenue per product from the simulator output, selects one
    product as the treated unit, and applies an additive treatment effect from
    treatment_date onward. A common upward time trend is added to all products
    so that naive before-after estimators are visibly biased.

    Parameters
    ----------
    metrics_df : pandas.DataFrame
        Metrics DataFrame from the Online Retail Simulator with
        product_identifier, date, and revenue columns.
    treatment_date : str
        Date string (YYYY-MM-DD) when the intervention occurs.
    true_effect : float
        True additive causal effect on daily revenue from treatment_date onward.
    seed : int
        Random seed for reproducibility of treated product selection.

    Returns
    -------
    panel : pandas.DataFrame
        Balanced panel with product_identifier, date, revenue, and
        revenue_counterfactual columns.
    treated_product : str
        The product_identifier of the treated unit.
    """
    rng = np.random.default_rng(seed)

    # Aggregate revenue per product per date
    daily = metrics_df.groupby(["product_identifier", "date"])["revenue"].sum().reset_index()
    daily["date"] = pd.to_datetime(daily["date"])
    daily["product_identifier"] = daily["product_identifier"].astype(str)

    treatment_date_ts = pd.Timestamp(treatment_date)

    # Build balanced panel (fill missing product-date pairs with 0)
    products = sorted(daily["product_identifier"].unique())
    dates = pd.date_range(daily["date"].min(), daily["date"].max(), freq="D")
    idx = pd.MultiIndex.from_product([products, dates], names=["product_identifier", "date"])
    panel = daily.set_index(["product_identifier", "date"]).reindex(idx, fill_value=0.0).reset_index()

    # Add common time trend (affects all products equally).
    # This makes naive before-after estimators biased upward.
    days_since_start = (panel["date"] - panel["date"].min()).dt.days
    panel["revenue"] = panel["revenue"] + 0.3 * days_since_start

    # Select treated product: pick one with above-median average revenue
    avg_rev = panel.groupby("product_identifier")["revenue"].mean()
    candidates = avg_rev[avg_rev >= avg_rev.median()].index.tolist()
    treated_product = str(rng.choice(candidates))

    # Store counterfactual (true untreated revenue)
    panel["revenue_counterfactual"] = panel["revenue"].copy()

    # Apply additive treatment effect post-treatment
    mask = (panel["product_identifier"] == treated_product) & (panel["date"] >= treatment_date_ts)
    panel.loc[mask, "revenue"] = panel.loc[mask, "revenue"] + true_effect

    return panel, treated_product


def compute_ground_truth_att(panel, treated_product, treatment_date):
    """Compute the true ATT from known potential outcomes.

    Parameters
    ----------
    panel : pandas.DataFrame
        Panel with revenue and revenue_counterfactual columns.
    treated_product : str
        The product_identifier of the treated unit.
    treatment_date : str or pandas.Timestamp
        Treatment date.

    Returns
    -------
    float
        True average treatment effect on the treated in the post period.
    """
    treatment_date = pd.Timestamp(treatment_date)
    post = panel[(panel["product_identifier"] == treated_product) & (panel["date"] >= treatment_date)]
    return (post["revenue"] - post["revenue_counterfactual"]).mean()


def plot_treated_vs_synthetic(panel, treated_product, impact_data, treatment_date):
    """Plot the treated unit's time series against its synthetic control.

    Parameters
    ----------
    panel : pandas.DataFrame
        Panel data with product_identifier, date, and revenue columns.
    treated_product : str
        The product_identifier of the treated unit.
    impact_data : dict
        The ``impact_results["data"]`` dict containing ``model_summary``
        with ``weights``.
    treatment_date : str or pandas.Timestamp
        Treatment date for the vertical line.

    Returns
    -------
    synthetic_ts : pandas.Series
        The synthetic control time series (for use in gap plots).
    """
    treatment_date = pd.Timestamp(treatment_date)

    # Treated unit time series
    treated_ts = panel[panel["product_identifier"] == treated_product].set_index("date")["revenue"].sort_index()

    # Construct synthetic control as weighted average of donor units
    weights = _parse_weights(impact_data["model_summary"]["weights"])
    control_data = panel[panel["product_identifier"] != treated_product]

    synthetic_ts = pd.Series(0.0, index=treated_ts.index)
    for unit, w in weights.items():
        if abs(w) < 1e-6:
            continue
        unit_ts = (
            control_data[control_data["product_identifier"] == unit]
            .set_index("date")["revenue"]
            .reindex(treated_ts.index, fill_value=0.0)
        )
        synthetic_ts = synthetic_ts + w * unit_ts

    _, ax = plt.subplots(figsize=(12, 5))
    ax.plot(
        treated_ts.index,
        treated_ts.values,
        color="#e74c3c",
        linewidth=2,
        label=f"Treated ({treated_product})",
    )
    ax.plot(
        synthetic_ts.index,
        synthetic_ts.values,
        color="#3498db",
        linewidth=2,
        linestyle="--",
        label="Synthetic Control",
    )
    ax.axvline(
        x=treatment_date,
        color="black",
        linestyle=":",
        linewidth=1.5,
        label=f"Treatment ({treatment_date.date()})",
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue ($)")
    ax.set_title("Treated Unit vs. Synthetic Control", fontsize=14, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    plt.show()

    return synthetic_ts


def plot_gap(panel, treated_product, synthetic_ts, treatment_date):
    """Plot the gap (difference) between treated and synthetic control over time.

    Parameters
    ----------
    panel : pandas.DataFrame
        Panel data with product_identifier, date, and revenue columns.
    treated_product : str
        The product_identifier of the treated unit.
    synthetic_ts : pandas.Series
        Synthetic control time series (from plot_treated_vs_synthetic).
    treatment_date : str or pandas.Timestamp
        Treatment date for the vertical line.
    """
    treatment_date = pd.Timestamp(treatment_date)

    treated_ts = panel[panel["product_identifier"] == treated_product].set_index("date")["revenue"].sort_index()

    gap = treated_ts - synthetic_ts

    _, ax = plt.subplots(figsize=(12, 4))
    ax.plot(gap.index, gap.values, color="#2c3e50", linewidth=2)
    ax.axhline(y=0, color="gray", linestyle="-", linewidth=0.8)
    ax.axvline(
        x=treatment_date,
        color="black",
        linestyle=":",
        linewidth=1.5,
        label=f"Treatment ({treatment_date.date()})",
    )
    ax.fill_between(
        gap.index,
        0,
        gap.values,
        where=(gap.index >= treatment_date),
        alpha=0.3,
        color="#e74c3c",
        label="Post-treatment gap",
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue Gap ($)")
    ax.set_title("Gap: Treated \u2212 Synthetic Control", fontsize=14, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_weights(impact_data, top_n=15):
    """Plot donor unit weights as a horizontal bar chart.

    Parameters
    ----------
    impact_data : dict
        The ``impact_results["data"]`` dict containing ``model_summary``
        with ``weights``.
    top_n : int
        Show only the top_n units by weight.
    """
    weights = _parse_weights(impact_data["model_summary"]["weights"])
    weights_series = pd.Series(weights).sort_values(ascending=True)

    # Keep only top_n
    if len(weights_series) > top_n:
        weights_series = weights_series.tail(top_n)

    _, ax = plt.subplots(figsize=(8, max(3, len(weights_series) * 0.4)))
    colors = ["#3498db" if w > 0.01 else "#bdc3c7" for w in weights_series.values]
    ax.barh(
        range(len(weights_series)),
        weights_series.values,
        color=colors,
        edgecolor="black",
        linewidth=0.5,
    )
    ax.set_yticks(range(len(weights_series)))
    ax.set_yticklabels(weights_series.index, fontsize=9)
    ax.set_xlabel("Weight")
    ax.set_title("Donor Unit Weights (Synthetic Control)", fontsize=14, fontweight="bold")
    ax.axvline(x=0, color="black", linewidth=0.5)
    plt.tight_layout()
    plt.show()
