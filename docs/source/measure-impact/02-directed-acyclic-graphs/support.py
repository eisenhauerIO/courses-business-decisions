"""Support functions for the Directed Acyclic Graphs notebook."""

# Third-party packages
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import statsmodels.api as sm


def draw_dag(edges, node_labels=None, title=None, figsize=(8, 6), node_color="#87CEEB", highlight_path=None):
    """
    Draw a directed acyclic graph using networkx and matplotlib.

    Parameters
    ----------
    edges : list of tuples
        List of (source, target) tuples representing directed edges.
    node_labels : dict, optional
        Dictionary mapping node names to display labels.
    title : str, optional
        Title for the plot.
    figsize : tuple, optional
        Figure size. Default is (8, 6).
    node_color : str, optional
        Color for nodes. Default is light blue.
    highlight_path : list of tuples, optional
        List of edges to highlight in red.

    Returns
    -------
    networkx.DiGraph
        The created graph object.
    """
    G = nx.DiGraph()
    G.add_edges_from(edges)

    fig, ax = plt.subplots(figsize=figsize)

    # Use hierarchical layout for DAGs
    try:
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    except (ImportError, Exception):
        pos = nx.spring_layout(G, seed=42, k=2)

    # Draw edges
    edge_colors = []
    edge_widths = []
    for edge in G.edges():
        if highlight_path and edge in highlight_path:
            edge_colors.append("#e74c3c")
            edge_widths.append(3)
        else:
            edge_colors.append("#333333")
            edge_widths.append(2)

    nx.draw_networkx_edges(
        G,
        pos,
        edge_color=edge_colors,
        width=edge_widths,
        arrows=True,
        arrowsize=25,
        connectionstyle="arc3,rad=0.1",
        ax=ax,
    )

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_color, node_size=2000, edgecolors="black", linewidths=2, ax=ax)

    # Draw labels
    labels = node_labels if node_labels else {n: n for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight="bold", ax=ax)

    ax.set_title(title or "Directed Acyclic Graph", fontsize=14, fontweight="bold")
    ax.axis("off")
    plt.tight_layout()
    plt.show()

    return G


def add_collider(df, marketing_pct=70, sales_pct=70, seed=45):
    """
    Add a collider variable (Featured status) to the dataframe.

    Products are featured if they have high marketing spend OR high sales.
    This creates a collider: Marketing -> Featured <- Sales

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with marketing_spend and sales columns.
    marketing_pct : float
        Percentile threshold for marketing spend.
    sales_pct : float
        Percentile threshold for sales.
    seed : int
        Random seed.

    Returns
    -------
    pandas.DataFrame
        DataFrame with added 'featured' column.
    """
    rng = np.random.default_rng(seed)

    marketing_threshold = np.percentile(df["marketing_spend"], marketing_pct)
    sales_threshold = np.percentile(df["sales"], sales_pct)

    # Featured if high marketing OR high sales (with some noise)
    high_marketing = df["marketing_spend"] >= marketing_threshold
    high_sales = df["sales"] >= sales_threshold

    # Base featured on either condition, with some noise
    featured_prob = 0.8 * (high_marketing | high_sales).astype(float) + 0.1
    featured = rng.random(len(df)) < featured_prob

    df = df.copy()
    df["featured"] = featured

    return df


def run_regression(df, outcome, predictors, add_constant=True):
    """
    Run OLS regression and return results.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with variables.
    outcome : str
        Name of outcome variable.
    predictors : list of str
        Names of predictor variables.
    add_constant : bool
        Whether to add a constant term.

    Returns
    -------
    statsmodels.regression.linear_model.RegressionResultsWrapper
        Fitted regression results.
    """
    X = df[predictors].copy()
    if add_constant:
        X = sm.add_constant(X)
    y = df[outcome]

    model = sm.OLS(y, X)
    results = model.fit()

    return results


def print_path_analysis(paths, descriptions):
    """
    Print formatted path analysis.

    Parameters
    ----------
    paths : list of str
        Path representations (e.g., ["D -> Y", "D <- X -> Y"]).
    descriptions : list of str
        Description of each path type.
    """
    print("Path Analysis:")
    print("=" * 60)
    for i, (path, desc) in enumerate(zip(paths, descriptions), 1):
        print(f"\nPath {i}: {path}")
        print(f"  Type: {desc}")
    print("=" * 60)


def draw_movie_star_example(figsize=(12, 5)):
    """
    Draw the classic movie star collider example.

    Shows:
    - Left: Full population (no correlation between talent and beauty)
    - Right: Conditioned on being a movie star (negative correlation appears)
    """
    rng = np.random.default_rng(42)

    n = 1000

    # Generate talent and beauty (independent)
    talent = rng.normal(50, 15, n)
    beauty = rng.normal(50, 15, n)

    # Being a star depends on talent OR beauty (collider)
    star_score = 0.5 * talent + 0.5 * beauty + rng.normal(0, 10, n)
    is_star = star_score > np.percentile(star_score, 90)

    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # Full population
    axes[0].scatter(talent[~is_star], beauty[~is_star], alpha=0.3, color="#3498db", s=20, label="Non-stars")
    axes[0].scatter(talent[is_star], beauty[is_star], alpha=0.8, color="#f39c12", s=50, label="Stars")
    axes[0].set_xlabel("Talent")
    axes[0].set_ylabel("Beauty")
    axes[0].set_title("Full Population")
    corr_full = np.corrcoef(talent, beauty)[0, 1]
    axes[0].text(0.05, 0.95, f"Correlation: {corr_full:.2f}", transform=axes[0].transAxes, va="top", fontsize=11)
    axes[0].legend()

    # Stars only (collider bias)
    axes[1].scatter(talent[is_star], beauty[is_star], alpha=0.8, color="#f39c12", s=50)
    z = np.polyfit(talent[is_star], beauty[is_star], 1)
    p = np.poly1d(z)
    x_line = np.linspace(talent[is_star].min(), talent[is_star].max(), 100)
    axes[1].plot(x_line, p(x_line), "r--", linewidth=2)
    axes[1].set_xlabel("Talent")
    axes[1].set_ylabel("Beauty")
    axes[1].set_title("Movie Stars Only (Collider Bias)")
    corr_stars = np.corrcoef(talent[is_star], beauty[is_star])[0, 1]
    axes[1].text(0.05, 0.95, f"Correlation: {corr_stars:.2f}", transform=axes[1].transAxes, va="top", fontsize=11)

    plt.suptitle("The Movie Star Paradox: Conditioning on a Collider", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()

    print(f"\nIn the full population, talent and beauty are uncorrelated (r = {corr_full:.2f})")
    print(f"Among movie stars, there's a NEGATIVE correlation (r = {corr_stars:.2f})")
    print("\nThis is collider bias: conditioning on Star (which depends on both Talent and Beauty)")
    print("creates a spurious negative association between Talent and Beauty.")


# =============================================================================
# Functions for Online Retail Simulator Integration
# =============================================================================


def create_quality_score(metrics_df, seed=42):
    """
    Create a quality score for each product based on baseline revenue.

    This simulates unobserved product quality that drives both baseline sales
    and the company's decision of which products to optimize.

    Parameters
    ----------
    metrics_df : pandas.DataFrame
        Metrics DataFrame with `product_identifier` and `revenue` columns.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pandas.DataFrame
        DataFrame with `product_identifier` and `quality_score` columns.
    """
    rng = np.random.default_rng(seed)

    # Aggregate revenue by product (in case of multiple dates)
    product_revenue = metrics_df.groupby("product_identifier")["revenue"].sum().reset_index()
    product_revenue.columns = ["product_identifier", "baseline_revenue"]

    # Create quality score: normalized revenue + noise
    # Quality is correlated with revenue but not perfectly
    revenue_min = product_revenue["baseline_revenue"].min()
    revenue_max = product_revenue["baseline_revenue"].max()
    revenue_normalized = (product_revenue["baseline_revenue"] - revenue_min) / (revenue_max - revenue_min + 1e-6)

    # Scale to 1-100 range with noise
    product_revenue["quality_score"] = 10 + 80 * revenue_normalized + rng.normal(0, 10, len(product_revenue))
    product_revenue["quality_score"] = np.clip(product_revenue["quality_score"], 1, 100)

    return product_revenue[["product_identifier", "quality_score", "baseline_revenue"]]


def apply_confounded_treatment(quality_df, treatment_fraction=0.3, quality_effect=-0.02, true_effect=0.5, seed=42):
    """
    Apply treatment assignment that is confounded by quality.

    Struggling products (low quality) are MORE likely to receive content optimization.
    This creates a backdoor path: Quality → Optimization ← (selection) and Quality → Sales.

    Parameters
    ----------
    quality_df : pandas.DataFrame
        DataFrame with `product_identifier`, `quality_score`, and `baseline_revenue`.
    treatment_fraction : float
        Target fraction of products to treat (approximate).
    quality_effect : float
        How quality affects treatment probability (negative = low quality more likely treated).
    true_effect : float
        True causal effect of treatment (proportional increase in revenue).
    seed : int
        Random seed.

    Returns
    -------
    pandas.DataFrame
        DataFrame with treatment assignment and potential outcomes.
    """
    rng = np.random.default_rng(seed)
    df = quality_df.copy()

    # Treatment probability inversely related to quality
    # Low quality products are more likely to receive optimization
    quality_centered = df["quality_score"] - df["quality_score"].mean()
    logit = quality_effect * quality_centered
    treatment_prob = 1 / (1 + np.exp(-logit))

    # Scale to achieve target treatment fraction
    treatment_prob = treatment_prob * (treatment_fraction / treatment_prob.mean())
    treatment_prob = np.clip(treatment_prob, 0.05, 0.95)

    # Assign treatment
    df["optimized"] = rng.random(len(df)) < treatment_prob
    df["D"] = df["optimized"].astype(int)

    # Calculate potential outcomes
    # Y^0: baseline revenue (what would happen without treatment)
    df["Y0"] = df["baseline_revenue"]

    # Y^1: revenue if treated (baseline * (1 + effect))
    df["Y1"] = df["baseline_revenue"] * (1 + true_effect)

    # Observed outcome follows switching equation
    df["Y_observed"] = np.where(df["D"] == 1, df["Y1"], df["Y0"])

    # Store true effect for validation
    df["true_effect"] = true_effect

    return df


def add_collider_variable(df, revenue_col="Y_observed", treatment_col="D", threshold_pct=70, seed=42):
    """
    Add a collider variable: "high_performer" status.

    Products are flagged as high performers if they have:
    - High observed revenue, OR
    - Were selected for optimization (treatment)

    This creates a collider: D → HighPerformer ← Y

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with treatment and outcome columns.
    revenue_col : str
        Column name for revenue.
    treatment_col : str
        Column name for treatment indicator.
    threshold_pct : float
        Percentile threshold for "high" revenue.
    seed : int
        Random seed.

    Returns
    -------
    pandas.DataFrame
        DataFrame with added `high_performer` column.
    """
    rng = np.random.default_rng(seed)
    df = df.copy()

    revenue_threshold = np.percentile(df[revenue_col], threshold_pct)

    # High performer if treated OR high revenue (with some noise)
    high_revenue = df[revenue_col] >= revenue_threshold
    treated = df[treatment_col] == 1

    # Base probability on either condition
    base_prob = 0.8 * (high_revenue | treated).astype(float) + 0.1
    df["high_performer"] = rng.random(len(df)) < base_prob

    return df


def plot_confounding_scatter(df, title=None):
    """
    Plot scatter showing confounding relationship.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with quality_score, D, and Y_observed columns.
    title : str, optional
        Plot title.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: Quality vs Treatment (showing selection bias)
    treated = df[df["D"] == 1]
    control = df[df["D"] == 0]

    axes[0].scatter(
        control["quality_score"],
        control["Y0"],
        alpha=0.5,
        color="#3498db",
        s=40,
        label="Control (not optimized)",
    )
    axes[0].scatter(
        treated["quality_score"],
        treated["Y0"],
        alpha=0.5,
        color="#e74c3c",
        s=40,
        label="Treated (optimized)",
    )
    axes[0].set_xlabel("Quality Score")
    axes[0].set_ylabel("Baseline Revenue ($)")
    axes[0].set_title("Selection into Treatment\n(Low quality products selected for optimization)")
    axes[0].legend()

    # Right: Naive comparison of outcomes
    axes[1].boxplot(
        [control["Y_observed"], treated["Y_observed"]],
        labels=["Control", "Treated"],
        patch_artist=True,
    )
    axes[1].patches[0].set_facecolor("#3498db")
    axes[1].patches[1].set_facecolor("#e74c3c")
    axes[1].set_ylabel("Observed Revenue ($)")
    axes[1].set_title("Observed Outcomes\n(Naive comparison suggests optimization hurts!)")

    naive_diff = treated["Y_observed"].mean() - control["Y_observed"].mean()
    true_effect = df["true_effect"].iloc[0]
    axes[1].text(
        0.5,
        0.02,
        f"Naive diff: ${naive_diff:,.0f}  |  True effect: +{true_effect:.0%}",
        transform=axes[1].transAxes,
        ha="center",
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
    )

    plt.suptitle(title or "Confounding in Content Optimization", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


def plot_estimates_comparison(estimates, title="Three Ways to Estimate the Content Optimization Effect"):
    """
    Plot bar chart comparing different effect estimates.

    Parameters
    ----------
    estimates : dict
        Dictionary mapping estimate names to values.
    title : str, optional
        Plot title.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ["#e74c3c", "#2ecc71", "#f39c12"]
    x_pos = np.arange(len(estimates))

    bars = ax.bar(x_pos, estimates.values(), color=colors[: len(estimates)], edgecolor="black", width=0.6)

    # Add value labels
    for bar, val in zip(bars, estimates.values()):
        y_pos = bar.get_height() + (20 if val > 0 else -40)
        ax.text(bar.get_x() + bar.get_width() / 2, y_pos, f"${val:,.0f}", ha="center", fontsize=12, fontweight="bold")

    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(estimates.keys())
    ax.set_ylabel("Estimated Effect on Revenue ($)")
    ax.set_title(title)
    plt.tight_layout()
    plt.show()


def plot_dag_application(df, naive_effect, conditioned_effect, true_effect):
    """
    Create summary visualization comparing naive vs conditioned estimates.

    Parameters
    ----------
    df : pandas.DataFrame
        Data with quality_score, D, Y_observed columns.
    naive_effect : float
        Naive estimate (biased).
    conditioned_effect : float
        Estimate after conditioning on quality.
    true_effect : float
        True causal effect (proportional).
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Panel 1: Scatter colored by quality
    scatter = axes[0].scatter(
        df["D"] + np.random.normal(0, 0.05, len(df)),  # Jitter for visibility
        df["Y_observed"],
        c=df["quality_score"],
        cmap="RdYlGn",
        alpha=0.6,
        s=40,
    )
    plt.colorbar(scatter, ax=axes[0], label="Quality Score")
    axes[0].set_xticks([0, 1])
    axes[0].set_xticklabels(["Control", "Treated"])
    axes[0].set_ylabel("Observed Revenue ($)")
    axes[0].set_title("Outcomes by Treatment\n(colored by quality)")

    # Panel 2: Comparison of estimates
    estimates = {
        "Naive": naive_effect,
        "Conditioned\non Quality": conditioned_effect,
    }
    colors = ["#e74c3c" if abs(v) > abs(conditioned_effect) else "#2ecc71" for v in estimates.values()]

    x_pos = np.arange(len(estimates))
    bars = axes[1].bar(x_pos, estimates.values(), color=colors, edgecolor="black", width=0.6)

    # Add value labels
    for bar, val in zip(bars, estimates.values()):
        y_pos = bar.get_height() + (50 if val > 0 else -80)
        axes[1].text(
            bar.get_x() + bar.get_width() / 2, y_pos, f"${val:,.0f}", ha="center", fontsize=11, fontweight="bold"
        )

    axes[1].axhline(0, color="black", linewidth=0.5)
    axes[1].set_xticks(x_pos)
    axes[1].set_xticklabels(estimates.keys())
    axes[1].set_ylabel("Estimated Effect on Revenue ($)")
    axes[1].set_title("Naive vs. Conditioned Estimates")

    # Panel 3: Text summary
    axes[2].axis("off")
    summary_text = (
        "DAG Analysis Summary\n"
        "─" * 30 + "\n\n"
        f"True effect: +{true_effect:.0%} revenue boost\n\n"
        f"Naive estimate: ${naive_effect:,.0f}\n"
        "  → BIASED (wrong sign!)\n\n"
        f"Conditioned estimate: ${conditioned_effect:,.0f}\n"
        "  → Closer to true effect\n\n"
        "─" * 30 + "\n"
        "Backdoor path:\n"
        "  Quality → Optimization\n"
        "  Quality → Sales\n\n"
        "Conditioning on Quality\n"
        "blocks the backdoor path."
    )
    axes[2].text(
        0.1,
        0.9,
        summary_text,
        transform=axes[2].transAxes,
        fontsize=12,
        verticalalignment="top",
        fontfamily="monospace",
        bbox=dict(boxstyle="round", facecolor="lightgray", alpha=0.3),
    )

    plt.tight_layout()
    plt.show()
