"""Support functions for the Synthetic Control lecture."""

# Third-party packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml


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

    Adds a common upward time trend (so naive before-after estimators are
    visibly biased) and computes counterfactual revenue from the simulator's
    potential outcomes.

    The simulator already produces a balanced panel with one row per product
    per day, so no aggregation or reindexing is needed.

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
        Panel with product_identifier, date, revenue, and
        revenue_counterfactual columns.
    treated_products : list of str
        Product identifiers that received treatment.
    control_products : list of str
        Product identifiers in the donor pool.
    """
    panel = enriched_metrics[["product_identifier", "date", "revenue"]].copy()
    panel["date"] = pd.to_datetime(panel["date"])
    panel["product_identifier"] = panel["product_identifier"].astype(str)

    # Merge counterfactual revenue (Y0) from potential outcomes
    po = potential_outcomes[["product_identifier", "date", "Y0_revenue"]].copy()
    po["date"] = pd.to_datetime(po["date"])
    po["product_identifier"] = po["product_identifier"].astype(str)
    panel = panel.merge(po, on=["product_identifier", "date"], how="left")

    # Add common time trend (affects all products equally)
    days_since_start = (panel["date"] - panel["date"].min()).dt.days
    panel["revenue"] = panel["revenue"] + trend_slope * days_since_start
    panel["Y0_revenue"] = panel["Y0_revenue"] + trend_slope * days_since_start

    # Counterfactual: Y0 for all products (what revenue would be without treatment)
    panel["revenue_counterfactual"] = panel["Y0_revenue"]
    panel = panel.drop(columns=["Y0_revenue"])

    # Identify treated vs control products
    products = sorted(panel["product_identifier"].unique())
    treated_products = sorted(
        enriched_metrics[enriched_metrics["enriched"]]["product_identifier"].astype(str).unique().tolist()
    )
    control_products = sorted([p for p in products if p not in treated_products])

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


def run_placebo_tests(panel, treated_product, control_products, treatment_date, n_placebos=20):
    """Run placebo-in-space tests for synthetic control inference.

    Fits a synthetic control for each placebo unit (pretending it is
    treated) and for the actual treated unit, then computes RMSPE ratios
    to construct a permutation-based p-value.

    Parameters
    ----------
    panel : pandas.DataFrame
        Panel data with product_identifier, date, and revenue columns.
    treated_product : str
        The product_identifier of the actual treated unit.
    control_products : list of str
        Product identifiers in the donor pool.
    treatment_date : str or pandas.Timestamp
        Treatment date.
    n_placebos : int, optional
        Number of placebo units to sample from the donor pool.

    Returns
    -------
    dict
        ``"summary"`` : DataFrame with columns unit, rmspe_pre,
        rmspe_post, ratio, is_treated.
        ``"gaps"`` : dict mapping each unit to its gap Series
        (actual minus synthetic).
    """
    from pysyncon import Dataprep, Synth

    treatment_date = pd.Timestamp(treatment_date)
    rng = np.random.default_rng(42)

    n_sample = min(n_placebos, len(control_products))
    placebo_units = sorted(rng.choice(control_products, size=n_sample, replace=False).tolist())
    units_to_evaluate = placebo_units + [treated_product]

    all_times = sorted(panel["date"].unique())
    pre_times = [t for t in all_times if t < treatment_date]

    rows = []
    gaps = {}

    for i, unit in enumerate(units_to_evaluate, 1):
        is_treated = unit == treated_product
        donors = [p for p in control_products if p != unit]

        df = panel[panel["product_identifier"].isin([unit] + donors)].copy()
        try:
            dataprep = Dataprep(
                foo=df,
                predictors=["revenue"],
                predictors_op="mean",
                dependent="revenue",
                unit_variable="product_identifier",
                time_variable="date",
                treatment_identifier=unit,
                controls_identifier=donors,
                time_predictors_prior=pre_times,
                time_optimize_ssr=pre_times,
            )

            synth = Synth()
            synth.fit(dataprep=dataprep, optim_method="Nelder-Mead", optim_initial="equal")

            rmspe_pre = float(synth.mspe()) ** 0.5

            # Reconstruct synthetic series from weights
            weights = _parse_weights(synth.weights(round=6).to_dict())
            unit_ts = df[df["product_identifier"] == unit].set_index("date")["revenue"].sort_index()
            synthetic_ts = pd.Series(0.0, index=unit_ts.index)
            for donor, w in weights.items():
                if abs(w) < 1e-8:
                    continue
                donor_ts = (
                    df[df["product_identifier"] == donor]
                    .set_index("date")["revenue"]
                    .reindex(unit_ts.index, fill_value=0.0)
                )
                synthetic_ts += w * donor_ts

            gap = unit_ts - synthetic_ts
            gaps[unit] = gap

            post_gap = gap[gap.index >= treatment_date]
            rmspe_post = float((post_gap**2).mean() ** 0.5)
            ratio = rmspe_post / rmspe_pre if rmspe_pre > 1e-10 else float("inf")

            rows.append(
                {
                    "unit": unit,
                    "rmspe_pre": rmspe_pre,
                    "rmspe_post": rmspe_post,
                    "ratio": ratio,
                    "is_treated": is_treated,
                }
            )
            label = " <- treated" if is_treated else ""
            print(f"  [{i}/{len(units_to_evaluate)}] {unit} — ratio: {ratio:.2f}{label}")
        except Exception as e:
            print(f"  [{i}/{len(units_to_evaluate)}] {unit} — FAILED: {e}")

    return {"summary": pd.DataFrame(rows), "gaps": gaps}


def plot_placebo_gaps(placebo_results, treatment_date):
    """Spaghetti plot of placebo and treated unit gaps over time.

    Parameters
    ----------
    placebo_results : dict
        Output from ``run_placebo_tests``.
    treatment_date : str or pandas.Timestamp
        Treatment date for the vertical line.
    """
    treatment_date = pd.Timestamp(treatment_date)
    gaps = placebo_results["gaps"]
    summary = placebo_results["summary"]
    treated_unit = summary.loc[summary["is_treated"], "unit"].iloc[0]

    _, ax = plt.subplots(figsize=(12, 5))

    for unit, gap in gaps.items():
        if unit == treated_unit:
            continue
        ax.plot(gap.index, gap.values, color="#bdc3c7", linewidth=0.8, alpha=0.6)

    # Plot a single gray entry for the legend
    ax.plot([], [], color="#bdc3c7", linewidth=0.8, label="Placebo units")

    if treated_unit in gaps:
        treated_gap = gaps[treated_unit]
        ax.plot(
            treated_gap.index,
            treated_gap.values,
            color="#e74c3c",
            linewidth=2.5,
            label=f"Treated ({treated_unit})",
        )

    ax.axvline(
        x=treatment_date,
        color="black",
        linestyle=":",
        linewidth=1.5,
        label=f"Treatment ({treatment_date.date()})",
    )
    ax.axhline(y=0, color="gray", linestyle="-", linewidth=0.8)
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue Gap ($)")
    ax.set_title("Placebo-in-Space Test: Gap Plots", fontsize=14, fontweight="bold")
    ax.legend()
    plt.tight_layout()
    plt.show()


def plot_rmspe_ratios(placebo_results):
    """Horizontal bar chart of RMSPE ratios with exact p-value.

    Parameters
    ----------
    placebo_results : dict
        Output from ``run_placebo_tests``.
    """
    summary = placebo_results["summary"].sort_values("ratio", ascending=True).reset_index(drop=True)

    colors = ["#e74c3c" if row["is_treated"] else "#bdc3c7" for _, row in summary.iterrows()]

    _, ax = plt.subplots(figsize=(8, max(3, len(summary) * 0.35)))
    ax.barh(range(len(summary)), summary["ratio"].values, color=colors, edgecolor="black", linewidth=0.5)
    ax.set_yticks(range(len(summary)))
    ax.set_yticklabels(summary["unit"].values, fontsize=9)
    ax.set_xlabel("RMSPE Ratio (Post / Pre)")
    ax.set_title("RMSPE Ratio Distribution", fontsize=14, fontweight="bold")

    # Compute and annotate exact p-value
    treated_row = summary[summary["is_treated"]]
    if not treated_row.empty:
        treated_ratio = treated_row["ratio"].iloc[0]
        n_total = len(summary)
        n_extreme = int((summary["ratio"] >= treated_ratio).sum())
        p_value = n_extreme / n_total
        ax.annotate(
            f"p-value = {n_extreme}/{n_total} = {p_value:.3f}",
            xy=(0.95, 0.05),
            xycoords="axes fraction",
            ha="right",
            fontsize=11,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray"),
        )

    plt.tight_layout()
    plt.show()


def plot_method_comparison(estimates_dict, true_effect):
    """Compare treatment effect estimates across methods in a bar chart.

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
    ax.axhline(
        y=true_effect,
        color="black",
        linestyle="--",
        linewidth=2,
        label=f"True ATT = ${true_effect:,.0f}",
    )

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
