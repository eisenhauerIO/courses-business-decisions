"""Support functions for the Catalog AI notebook."""

# Third-party packages
import matplotlib.pyplot as plt
import pandas as pd


def print_product_details(products, label=None):
    """
    Print formatted product details from LLM-generated output.

    Parameters
    ----------
    products : pandas.DataFrame
        DataFrame containing product information with columns 'title',
        'brand', and 'description'.
    label : str, optional
        Header label to display above the product details.
    """
    if label:
        print(f"\n{'=' * 70}")
        print(f"{label.upper()}")
        print(f"{'=' * 70}")
    for _, row in products.iterrows():
        print(f"\n  Title: {row['title']}")
        print(f"  Brand: {row['brand']}")
        print(f"  Description: {row['description']}")


def plot_treatment_effect(metrics, enriched, enrichment_start, figsize=(12, 6)):
    """
    Plot daily revenue comparing original vs enriched data.

    Parameters
    ----------
    metrics : pandas.DataFrame
        Original metrics DataFrame with 'date' and 'revenue' columns.
    enriched : pandas.DataFrame
        Enriched metrics DataFrame with 'date' and 'revenue' columns.
    enrichment_start : str
        Date string (YYYY-MM-DD) when enrichment treatment began.
    figsize : tuple, optional
        Figure size as (width, height) in inches. Default is (12, 6).
    """
    daily_original = metrics.groupby("date")["revenue"].sum().reset_index()
    daily_original["date"] = pd.to_datetime(daily_original["date"])

    daily_enriched = enriched.groupby("date")["revenue"].sum().reset_index()
    daily_enriched["date"] = pd.to_datetime(daily_enriched["date"])

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(
        daily_original["date"],
        daily_original["revenue"],
        marker="o",
        linewidth=2,
        markersize=4,
        label="Original",
        color="#1f77b4",
    )
    ax.plot(
        daily_enriched["date"],
        daily_enriched["revenue"],
        marker="s",
        linewidth=2,
        markersize=4,
        label="Enriched",
        color="#2ca02c",
    )
    ax.axvline(
        pd.to_datetime(enrichment_start),
        color="red",
        linestyle="--",
        alpha=0.7,
        label="Treatment Start",
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue ($)")
    ax.set_title("Treatment Effect: Daily Revenue")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_positioning_comparison(baseline_metrics, budget_enriched, luxury_enriched, treatment_start, figsize=(12, 6)):
    """
    Plot three-way comparison of baseline vs budget vs luxury positioning.

    Parameters
    ----------
    baseline_metrics : pandas.DataFrame
        Original metrics DataFrame (no treatment) with 'date' and 'revenue' columns.
    budget_enriched : pandas.DataFrame
        Budget positioning enriched metrics with 'date' and 'revenue' columns.
    luxury_enriched : pandas.DataFrame
        Luxury positioning enriched metrics with 'date' and 'revenue' columns.
    treatment_start : str
        Date string (YYYY-MM-DD) when treatment began.
    figsize : tuple, optional
        Figure size as (width, height) in inches. Default is (12, 6).

    Returns
    -------
    dict
        Dictionary with lift statistics for each strategy:
        - baseline: {"before": float, "after": float}
        - budget: {"before": float, "after": float, "lift": float}
        - luxury: {"before": float, "after": float, "lift": float}
    """
    # Aggregate revenue by date for all three scenarios
    baseline_daily = baseline_metrics.groupby("date")["revenue"].sum().reset_index()
    baseline_daily["date"] = pd.to_datetime(baseline_daily["date"])
    budget_daily = budget_enriched.groupby("date")["revenue"].sum().reset_index()
    budget_daily["date"] = pd.to_datetime(budget_daily["date"])
    luxury_daily = luxury_enriched.groupby("date")["revenue"].sum().reset_index()
    luxury_daily["date"] = pd.to_datetime(luxury_daily["date"])

    # Create comparison plot
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(
        baseline_daily["date"],
        baseline_daily["revenue"],
        label="Baseline (No Treatment)",
        marker="^",
        linewidth=2,
        linestyle="--",
        alpha=0.7,
        color="gray",
    )
    ax.plot(
        budget_daily["date"],
        budget_daily["revenue"],
        label="Budget Positioning",
        marker="o",
        linewidth=2,
        color="#2ca02c",
    )
    ax.plot(
        luxury_daily["date"],
        luxury_daily["revenue"],
        label="Luxury Positioning",
        marker="s",
        linewidth=2,
        color="#d62728",
    )
    ax.axvline(
        x=pd.to_datetime(treatment_start),
        color="red",
        linestyle=":",
        linewidth=2,
        alpha=0.5,
        label="Treatment Start",
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue ($)")
    ax.set_title("Business Impact Comparison: Budget vs Luxury Positioning")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Calculate lift statistics
    baseline_before = baseline_metrics[baseline_metrics["date"] < treatment_start]["revenue"].mean()
    baseline_after = baseline_metrics[baseline_metrics["date"] >= treatment_start]["revenue"].mean()

    budget_before = budget_enriched[budget_enriched["date"] < treatment_start]["revenue"].mean()
    budget_after = budget_enriched[budget_enriched["date"] >= treatment_start]["revenue"].mean()
    budget_lift = (budget_after - budget_before) / budget_before * 100

    luxury_before = luxury_enriched[luxury_enriched["date"] < treatment_start]["revenue"].mean()
    luxury_after = luxury_enriched[luxury_enriched["date"] >= treatment_start]["revenue"].mean()
    luxury_lift = (luxury_after - luxury_before) / luxury_before * 100

    return {
        "baseline": {"before": baseline_before, "after": baseline_after},
        "budget": {"before": budget_before, "after": budget_after, "lift": budget_lift},
        "luxury": {"before": luxury_before, "after": luxury_after, "lift": luxury_lift},
    }


def _print_scenario_stats(name, before, after, lift=None, is_baseline=False):
    """
    Print formatted statistics for a single scenario.

    Parameters
    ----------
    name : str
        Display name for the scenario (e.g., "Baseline", "Budget Positioning").
    before : float
        Revenue before treatment period.
    after : float
        Revenue after treatment period.
    lift : float, optional
        Lift percentage (for treatment scenarios).
    is_baseline : bool
        If True, show as baseline with change calculation.
    """
    print(f"\n{name}:")
    print(f"  Pre-Treatment Revenue:  ${before:,.2f}")
    print(f"  Post-Treatment Revenue: ${after:,.2f}")

    if is_baseline:
        change = (after - before) / before * 100
        print(f"  Change: {change:.1f}% (should be ~0%)")
    elif lift is not None:
        print(f"  Lift: {lift:.1f}%")


def print_positioning_comparison(stats):
    """
    Print formatted comparison of positioning strategy results.

    Parameters
    ----------
    stats : dict
        Statistics dictionary returned by plot_positioning_comparison().
        Expected structure:
        - baseline: {"before": float, "after": float}
        - budget: {"before": float, "after": float, "lift": float}
        - luxury: {"before": float, "after": float, "lift": float}
    """
    print("\n" + "=" * 70)
    print("BUSINESS IMPACT COMPARISON")
    print("=" * 70)

    # Print each scenario
    _print_scenario_stats(
        "Baseline (No Treatment)", stats["baseline"]["before"], stats["baseline"]["after"], is_baseline=True
    )
    _print_scenario_stats(
        "Budget Positioning", stats["budget"]["before"], stats["budget"]["after"], stats["budget"]["lift"]
    )
    _print_scenario_stats(
        "Luxury Positioning", stats["luxury"]["before"], stats["luxury"]["after"], stats["luxury"]["lift"]
    )

    # Winner
    winner = "Budget" if stats["budget"]["lift"] > stats["luxury"]["lift"] else "Luxury"
    max_lift = max(stats["budget"]["lift"], stats["luxury"]["lift"])
    print(f"\nWinner: {winner} Positioning (+{max_lift:.1f}%)")
    print("=" * 70)
