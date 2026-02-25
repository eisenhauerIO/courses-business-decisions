"""Support functions for the Synthetic Control lecture."""

# Standard library
import importlib.util
from pathlib import Path

# Third-party packages
import matplotlib.pyplot as plt
import pandas as pd
import yaml

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


def write_sc_config(
    treated_unit, treatment_time, panel_path="panel_data.csv", output_path="config_synthetic_control.yaml"
):
    """Write a synthetic control config YAML for the Impact Engine.

    Parameters
    ----------
    treated_unit : str
        Product identifier of the treated unit.
    treatment_time : str
        Treatment date string (YYYY-MM-DD).
    panel_path : str, optional
        Path to the panel CSV file.
    output_path : str, optional
        Path for the output YAML config file.
    """
    config = {
        "DATA": {
            "SOURCE": {"type": "file", "CONFIG": {"path": panel_path, "date_column": None}},
            "TRANSFORM": {"FUNCTION": "passthrough", "PARAMS": {}},
        },
        "MEASUREMENT": {
            "MODEL": "synthetic_control",
            "PARAMS": {
                "unit_column": "product_identifier",
                "time_column": "date",
                "outcome_column": "revenue",
                "treated_unit": treated_unit,
                "treatment_time": treatment_time,
                "optim_method": "Nelder-Mead",
                "optim_initial": "equal",
            },
        },
    }
    with open(output_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


def build_panel(enriched_metrics, potential_outcomes, treatment_date="2024-11-15", trend_slope=5.0):
    """Build analysis-ready panel from enriched simulator output.

    Aggregates daily revenue per product, adds a common upward time trend
    (so naive before-after estimators are visibly biased), and computes
    counterfactual revenue from the simulator's potential outcomes.

    Parameters
    ----------
    enriched_metrics : pandas.DataFrame
        Enriched metrics from the simulator with product_identifier, date,
        revenue, and enriched columns.
    potential_outcomes : pandas.DataFrame
        Potential outcomes from the simulator with product_identifier, date,
        Y0_revenue, and Y1_revenue columns.
    treatment_date : str, optional
        Date string (YYYY-MM-DD) when the intervention occurs.
    trend_slope : float, optional
        Slope of the common daily time trend added to all products.

    Returns
    -------
    panel : pandas.DataFrame
        Balanced panel with product_identifier, date, revenue, and
        revenue_counterfactual columns.
    treated_products : list of str
        Product identifiers that received treatment.
    control_products : list of str
        Product identifiers in the donor pool.
    """
    # Aggregate revenue per product per date
    daily = enriched_metrics.groupby(["product_identifier", "date"])["revenue"].sum().reset_index()
    daily["date"] = pd.to_datetime(daily["date"])
    daily["product_identifier"] = daily["product_identifier"].astype(str)

    # Aggregate counterfactual revenue (Y0) per product per date
    po = potential_outcomes.copy()
    po["date"] = pd.to_datetime(po["date"])
    po["product_identifier"] = po["product_identifier"].astype(str)
    daily_y0 = po.groupby(["product_identifier", "date"])["Y0_revenue"].sum().reset_index()

    # Merge counterfactual
    daily = daily.merge(daily_y0, on=["product_identifier", "date"], how="left")

    # Build balanced panel (fill missing product-date pairs with 0)
    products = sorted(daily["product_identifier"].unique())
    dates = pd.date_range(daily["date"].min(), daily["date"].max(), freq="D")
    idx = pd.MultiIndex.from_product([products, dates], names=["product_identifier", "date"])
    panel = daily.set_index(["product_identifier", "date"]).reindex(idx, fill_value=0.0).reset_index()

    # Add common time trend (affects all products equally)
    days_since_start = (panel["date"] - panel["date"].min()).dt.days
    panel["revenue"] = panel["revenue"] + trend_slope * days_since_start
    panel["Y0_revenue"] = panel["Y0_revenue"] + trend_slope * days_since_start

    # Counterfactual: Y0 for all products (what revenue would be without treatment)
    panel["revenue_counterfactual"] = panel["Y0_revenue"]

    # Identify treated vs control products
    treated_products = sorted(
        enriched_metrics[enriched_metrics["enriched"]]["product_identifier"].astype(str).unique().tolist()
    )
    control_products = sorted([p for p in products if p not in treated_products])

    panel = panel.drop(columns=["Y0_revenue"])

    return panel, treated_products, control_products


def compute_ground_truth_att(panel, treated_products, treatment_date):
    """Compute the true ATT from known potential outcomes.

    Parameters
    ----------
    panel : pandas.DataFrame
        Panel with revenue and revenue_counterfactual columns.
    treated_products : str or list of str
        Product identifier(s) of the treated unit(s).
    treatment_date : str or pandas.Timestamp
        Treatment date.

    Returns
    -------
    float
        True average treatment effect on the treated in the post period.
    """
    if isinstance(treated_products, str):
        treated_products = [treated_products]
    treatment_date = pd.Timestamp(treatment_date)
    post = panel[(panel["product_identifier"].isin(treated_products)) & (panel["date"] >= treatment_date)]
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
    top_n : int, optional
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


def plot_average_fit(panel, treated_products, control_products, treatment_date):
    """Plot average revenue for treated vs. control groups over time.

    Shows aggregate-level tracking between treated and control products
    before treatment, and divergence after treatment.

    Parameters
    ----------
    panel : pandas.DataFrame
        Panel with product_identifier, date, and revenue columns.
    treated_products : list of str
        Product identifiers of treated units.
    control_products : list of str
        Product identifiers of control units.
    treatment_date : str or pandas.Timestamp
        Treatment date for the vertical line.
    """
    treatment_date = pd.Timestamp(treatment_date)

    treated_avg = (
        panel[panel["product_identifier"].isin(treated_products)].groupby("date")["revenue"].mean().sort_index()
    )
    control_avg = (
        panel[panel["product_identifier"].isin(control_products)].groupby("date")["revenue"].mean().sort_index()
    )

    _, ax = plt.subplots(figsize=(12, 5))
    ax.plot(treated_avg.index, treated_avg.values, color="#e74c3c", linewidth=2, label="Treated (avg)")
    ax.plot(control_avg.index, control_avg.values, color="#3498db", linewidth=2, label="Control (avg)")
    ax.axvline(
        x=treatment_date,
        color="black",
        linestyle=":",
        linewidth=1.5,
        label=f"Treatment ({treatment_date.date()})",
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Average Revenue ($)")
    ax.set_title("Average Revenue: Treated vs. Control Products", fontsize=14, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    plt.show()
