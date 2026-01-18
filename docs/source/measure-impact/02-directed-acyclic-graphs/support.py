"""Support functions for the Directed Acyclic Graphs notebook."""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import statsmodels.api as sm
import yaml


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


def draw_dag_with_paths(edges, paths, node_labels=None, title=None, figsize=(10, 8)):
    """
    Draw a DAG with multiple paths highlighted in different colors.

    Parameters
    ----------
    edges : list of tuples
        List of (source, target) tuples representing directed edges.
    paths : list of list of tuples
        Each path is a list of edges to highlight.
    node_labels : dict, optional
        Dictionary mapping node names to display labels.
    title : str, optional
        Title for the plot.
    figsize : tuple, optional
        Figure size.
    """
    colors = ["#e74c3c", "#2ecc71", "#9b59b6", "#f39c12", "#1abc9c"]

    G = nx.DiGraph()
    G.add_edges_from(edges)

    fig, ax = plt.subplots(figsize=figsize)

    try:
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    except (ImportError, Exception):
        pos = nx.spring_layout(G, seed=42, k=2)

    # Build edge color map
    edge_color_map = {edge: "#cccccc" for edge in G.edges()}
    for i, path in enumerate(paths):
        color = colors[i % len(colors)]
        for edge in path:
            edge_color_map[edge] = color

    edge_colors = [edge_color_map[edge] for edge in G.edges()]

    nx.draw_networkx_edges(
        G,
        pos,
        edge_color=edge_colors,
        width=2.5,
        arrows=True,
        arrowsize=25,
        connectionstyle="arc3,rad=0.1",
        ax=ax,
    )

    nx.draw_networkx_nodes(G, pos, node_color="#87CEEB", node_size=2000, edgecolors="black", linewidths=2, ax=ax)

    labels = node_labels if node_labels else {n: n for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight="bold", ax=ax)

    ax.set_title(title or "DAG with Paths", fontsize=14, fontweight="bold")
    ax.axis("off")
    plt.tight_layout()
    plt.show()


def load_confounding_config(config_path="config_confounding.yaml"):
    """
    Load confounding configuration from YAML file.

    Parameters
    ----------
    config_path : str
        Path to the YAML configuration file.

    Returns
    -------
    dict
        Configuration dictionary.
    """
    with open(config_path) as f:
        return yaml.safe_load(f)


def simulate_confounded_data(
    n_products=500, quality_effect_marketing=-1.5, quality_effect_sales=10, marketing_effect=2, seed=42
):
    """
    Generate data with confounding structure for marketing-sales analysis.

    The data generation process:
    1. Quality (confounder) is generated from normal distribution
    2. Marketing spend is negatively affected by quality (struggling products get more)
    3. Sales are positively affected by both quality AND marketing

    Parameters
    ----------
    n_products : int
        Number of products to simulate.
    quality_effect_marketing : float
        Effect of quality on marketing spend (should be negative).
    quality_effect_sales : float
        Effect of quality on sales.
    marketing_effect : float
        True causal effect of marketing on sales ($ per $ spent).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    pandas.DataFrame
        DataFrame with columns: quality, marketing_spend, sales, and true_effect.
    """
    rng = np.random.default_rng(seed)

    # Generate quality scores (confounder)
    quality = rng.normal(50, 15, n_products)
    quality = np.clip(quality, 10, 90)

    # Generate marketing spend (inversely related to quality)
    # Low quality products get MORE marketing (rescue marketing)
    marketing_base = 100
    marketing_spend = marketing_base + quality_effect_marketing * quality + rng.normal(0, 20, n_products)
    marketing_spend = np.clip(marketing_spend, 10, 200)

    # Generate sales (positively affected by quality AND marketing)
    sales_base = 500
    sales = (
        sales_base
        + quality_effect_sales * quality
        + marketing_effect * marketing_spend
        + rng.normal(0, 100, n_products)
    )
    sales = np.clip(sales, 50, None)

    df = pd.DataFrame(
        {
            "product_id": [f"P{i:04d}" for i in range(n_products)],
            "quality": quality,
            "marketing_spend": marketing_spend,
            "sales": sales,
            "true_marketing_effect": marketing_effect,
        }
    )

    return df


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


def regression_comparison_table(results_dict, true_effect, effect_var="marketing_spend"):
    """
    Create comparison table of regression estimates vs true effect.

    Parameters
    ----------
    results_dict : dict
        Dictionary mapping model names to statsmodels results objects.
    true_effect : float
        True causal effect value.
    effect_var : str
        Name of the variable whose coefficient to compare.

    Returns
    -------
    pandas.DataFrame
        Comparison table with estimates, SEs, and bias.
    """
    rows = []
    for name, results in results_dict.items():
        coef = results.params[effect_var]
        se = results.bse[effect_var]
        bias = coef - true_effect

        rows.append(
            {
                "Model": name,
                "Estimate": coef,
                "Std Error": se,
                "95% CI Lower": coef - 1.96 * se,
                "95% CI Upper": coef + 1.96 * se,
                "Bias": bias,
                "True Effect": true_effect,
            }
        )

    return pd.DataFrame(rows)


def plot_regression_comparison(comparison_df, title=None):
    """
    Plot regression estimates with confidence intervals.

    Parameters
    ----------
    comparison_df : pandas.DataFrame
        DataFrame from regression_comparison_table.
    title : str, optional
        Plot title.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    y_positions = range(len(comparison_df))

    # Plot estimates with error bars
    ax.errorbar(
        comparison_df["Estimate"],
        y_positions,
        xerr=1.96 * comparison_df["Std Error"],
        fmt="o",
        capsize=5,
        capthick=2,
        markersize=10,
        color="black",
        ecolor="gray",
        elinewidth=2,
    )

    # Color the markers based on bias
    for i, (_, row) in enumerate(comparison_df.iterrows()):
        color = "#e74c3c" if abs(row["Bias"]) > 0.5 else "#2ecc71"
        ax.scatter(row["Estimate"], i, s=150, c=color, zorder=5, edgecolors="black", linewidths=1.5)

    # Add true effect line
    true_effect = comparison_df["True Effect"].iloc[0]
    ax.axvline(true_effect, color="#3498db", linestyle="--", linewidth=2, label=f"True Effect = {true_effect:.2f}")

    ax.set_yticks(y_positions)
    ax.set_yticklabels(comparison_df["Model"])
    ax.set_xlabel("Effect of Marketing on Sales ($ per $ spent)")
    ax.set_title(title or "Regression Estimates: Naive vs. Conditioned")
    ax.legend(loc="upper right")
    ax.grid(axis="x", alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_scatter_comparison(df, x, y, hue=None, title=None):
    """
    Create scatter plot showing relationship between variables.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with data.
    x : str
        X-axis variable name.
    y : str
        Y-axis variable name.
    hue : str, optional
        Variable for color coding points.
    title : str, optional
        Plot title.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    if hue:
        for value in df[hue].unique():
            mask = df[hue] == value
            label = f"{hue}={value}"
            ax.scatter(df.loc[mask, x], df.loc[mask, y], alpha=0.6, label=label, s=50)
        ax.legend()
    else:
        ax.scatter(df[x], df[y], alpha=0.6, color="#3498db", s=50)

    ax.set_xlabel(x.replace("_", " ").title())
    ax.set_ylabel(y.replace("_", " ").title())
    ax.set_title(title or f"{y} vs {x}")

    plt.tight_layout()
    plt.show()


def plot_partial_regression(df, outcome, treatment, confounder, title=None):
    """
    Plot partial regression showing effect after controlling for confounder.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with variables.
    outcome : str
        Outcome variable name.
    treatment : str
        Treatment variable name.
    confounder : str
        Confounder variable name.
    title : str, optional
        Plot title.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Raw scatter
    axes[0].scatter(df[treatment], df[outcome], alpha=0.5, color="#e74c3c", s=40)
    z = np.polyfit(df[treatment], df[outcome], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df[treatment].min(), df[treatment].max(), 100)
    axes[0].plot(x_line, p(x_line), "k--", linewidth=2, label=f"Slope = {z[0]:.2f}")
    axes[0].set_xlabel(treatment.replace("_", " ").title())
    axes[0].set_ylabel(outcome.replace("_", " ").title())
    axes[0].set_title("Raw Relationship (Biased)")
    axes[0].legend()

    # Residualized scatter (controlling for confounder)
    X_conf = sm.add_constant(df[confounder])
    resid_treatment = sm.OLS(df[treatment], X_conf).fit().resid
    resid_outcome = sm.OLS(df[outcome], X_conf).fit().resid

    axes[1].scatter(resid_treatment, resid_outcome, alpha=0.5, color="#2ecc71", s=40)
    z = np.polyfit(resid_treatment, resid_outcome, 1)
    p = np.poly1d(z)
    x_line = np.linspace(resid_treatment.min(), resid_treatment.max(), 100)
    axes[1].plot(x_line, p(x_line), "k--", linewidth=2, label=f"Slope = {z[0]:.2f}")
    axes[1].set_xlabel(f"{treatment} (residualized)")
    axes[1].set_ylabel(f"{outcome} (residualized)")
    axes[1].set_title(f"After Controlling for {confounder.title()}")
    axes[1].legend()

    plt.suptitle(title or "Partial Regression Analysis", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


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


def plot_collider_bias_demo(df, title=None):
    """
    Demonstrate collider bias by showing different estimates.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with marketing_spend, sales, and featured columns.
    title : str, optional
        Plot title.
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    true_effect = df["true_marketing_effect"].iloc[0]

    # Full sample
    axes[0].scatter(df["marketing_spend"], df["sales"], alpha=0.4, color="#3498db", s=30)
    z = np.polyfit(df["marketing_spend"], df["sales"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df["marketing_spend"].min(), df["marketing_spend"].max(), 100)
    axes[0].plot(x_line, p(x_line), "r--", linewidth=2, label=f"Naive slope = {z[0]:.2f}")
    axes[0].axhline(y=0, color="gray", linestyle="-", alpha=0.3)
    axes[0].set_xlabel("Marketing Spend")
    axes[0].set_ylabel("Sales")
    axes[0].set_title("Full Sample (Confounded)")
    axes[0].legend()

    # Conditioned on quality
    results = run_regression(df, "sales", ["marketing_spend", "quality"])
    effect_text = (
        f"Controlling for Quality\n\n"
        f"Marketing Effect: {results.params['marketing_spend']:.2f}\n"
        f"(True Effect: {true_effect:.2f})"
    )
    axes[1].text(
        0.5,
        0.5,
        effect_text,
        ha="center",
        va="center",
        fontsize=14,
        transform=axes[1].transAxes,
        bbox=dict(boxstyle="round", facecolor="#2ecc71", alpha=0.3),
    )
    axes[1].set_title("After Conditioning on Quality")
    axes[1].axis("off")

    # Conditioned on collider (featured)
    featured_df = df[df["featured"]]
    axes[2].scatter(featured_df["marketing_spend"], featured_df["sales"], alpha=0.4, color="#e74c3c", s=30)
    z = np.polyfit(featured_df["marketing_spend"], featured_df["sales"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(featured_df["marketing_spend"].min(), featured_df["marketing_spend"].max(), 100)
    axes[2].plot(x_line, p(x_line), "k--", linewidth=2, label=f"Slope = {z[0]:.2f}")
    axes[2].axhline(y=0, color="gray", linestyle="-", alpha=0.3)
    axes[2].set_xlabel("Marketing Spend")
    axes[2].set_ylabel("Sales")
    axes[2].set_title("Featured Products Only (Collider Bias!)")
    axes[2].legend()

    plt.suptitle(title or "Collider Bias Demonstration", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.show()


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
