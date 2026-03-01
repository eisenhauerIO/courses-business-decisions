"""Support functions for the Automated Evidence Review notebook."""

# Standard Library
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# Third-party
import matplotlib.pyplot as plt
import numpy as np

# Default p-value used in mock impact results; represents a well-powered experiment
# that clears the conventional 0.05 threshold with room to spare.
DEFAULT_P_VALUE = 0.003

# =============================================================================
# Mock Data Functions
# =============================================================================


def create_mock_job_directory(
    initiative_id="initiative_product_content_experiment",
    model_type="experiment",
    evaluate_strategy="deterministic",
    effect_estimate=150.0,
    ci_lower=80.0,
    ci_upper=220.0,
    sample_size=500,
    cost_to_scale=50000.0,
    diagnostics=None,
):
    """
    Create a temporary job directory with manifest and impact results.

    Simulates the output of the MEASURE stage so that the EVALUATE stage
    can be demonstrated without running the full pipeline.

    Parameters
    ----------
    initiative_id : str
        Identifier for the initiative.
    model_type : str
        Causal method label (must match a registered reviewer).
    evaluate_strategy : str
        Strategy for evaluation: ``"score"`` or ``"review"``.
    effect_estimate : float
        Point estimate of the treatment effect.
    ci_lower : float
        Lower bound of the confidence interval.
    ci_upper : float
        Upper bound of the confidence interval.
    sample_size : int
        Number of observations in the study.
    cost_to_scale : float
        Cost to scale the initiative.
    diagnostics : dict or None
        Diagnostic statistics to embed in the artifact. If ``None``, uses
        defaults representing a clean, well-powered experiment.

    Returns
    -------
    pathlib.Path
        Path to the temporary job directory.
    """
    if diagnostics is None:
        diagnostics = {
            "covariate_balance": {"max_smd": 0.04, "mean_smd": 0.02},
            "attrition_rate": 0.05,
            "compliance_rate": 0.92,
        }

    job_dir = Path(tempfile.mkdtemp(prefix="evaluate_demo_"))

    manifest = {
        "schema_version": "1.0",
        "model_type": model_type,
        "initiative_id": initiative_id,
        "evaluate_strategy": evaluate_strategy,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": {
            "impact_results": {
                "path": "impact_results.json",
                "format": "json",
            }
        },
    }

    # Flat structure matching what load_scorer_event reads
    impact_results = {
        "model_type": model_type,
        "sample_size": sample_size,
        "cost_to_scale": cost_to_scale,
        "effect_estimate": effect_estimate,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "p_value": DEFAULT_P_VALUE,
        "diagnostics": diagnostics,
    }

    (job_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (job_dir / "impact_results.json").write_text(json.dumps(impact_results, indent=2))

    return job_dir


# =============================================================================
# Print Helper Functions
# =============================================================================


def print_evaluate_result(result):
    """
    Print the 8-key output of the EVALUATE stage.

    Parameters
    ----------
    result : dict
        Output dictionary from ``Evaluate.execute()``.
    """
    print("EVALUATE Output")
    print("=" * 50)
    print(f"  Initiative:    {result['initiative_id']}")
    print(f"  Model type:    {result['model_type']}")
    print(f"  Confidence:    {result['confidence']:.3f}")
    print(f"  Sample size:   {result['sample_size']:,}")
    print(f"  Cost:          ${result['cost']:,.0f}")
    print(f"  Return (best): ${result['return_best']:,.0f}")
    print(f"  Return (med):  ${result['return_median']:,.0f}")
    print(f"  Return (worst):${result['return_worst']:,.0f}")


def print_review_result(review_result):
    """
    Print per-dimension scores and justifications from an agentic review.

    Parameters
    ----------
    review_result : ReviewResult
        Result from the agentic review pipeline.
    """
    print("Agentic Review Result")
    print("=" * 60)
    print(f"  Prompt:   {review_result.prompt_name} v{review_result.prompt_version}")
    print(f"  Backend:  {review_result.backend_name} ({review_result.model})")
    print(f"  Overall:  {review_result.overall_score:.2f}")
    print("-" * 60)

    for dim in review_result.dimensions:
        label = dim.name.replace("_", " ").title()
        print(f"\n  {label}: {dim.score:.2f}")
        print(f"    {dim.justification}")


# =============================================================================
# Plotting Functions
# =============================================================================


def plot_confidence_ranges(confidence_map):
    """
    Plot horizontal bars showing confidence ranges by causal method.

    Parameters
    ----------
    confidence_map : dict[str, tuple[float, float]]
        Mapping from method name to ``(lower, upper)`` confidence bounds.
    """
    methods = list(confidence_map.keys())
    lowers = [confidence_map[m][0] for m in methods]
    uppers = [confidence_map[m][1] for m in methods]

    _, ax = plt.subplots(figsize=(8, max(3, len(methods) * 0.8)))

    y_pos = np.arange(len(methods))
    widths = [u - lo for lo, u in zip(lowers, uppers)]

    ax.barh(y_pos, widths, left=lowers, height=0.5, color="#3498db", edgecolor="black", alpha=0.8)

    for i, (lo, hi) in enumerate(zip(lowers, uppers)):
        mid = (lo + hi) / 2
        ax.text(mid, i, f"{lo:.2f}–{hi:.2f}", ha="center", va="center", fontweight="bold", fontsize=10)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([m.replace("_", " ").title() for m in methods])
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("Confidence Range")
    ax.set_title("Methodology-Based Confidence Ranges")
    plt.tight_layout()
    plt.show()


def plot_review_dimensions(review_result):
    """
    Plot a bar chart of per-dimension scores from an agentic review.

    Parameters
    ----------
    review_result : ReviewResult
        Result from the agentic review pipeline.
    """
    names = [d.name.replace("_", " ").title() for d in review_result.dimensions]
    scores = [d.score for d in review_result.dimensions]

    _, ax = plt.subplots(figsize=(8, max(3, len(names) * 0.8)))

    y_pos = np.arange(len(names))
    colors = ["#2ecc71" if s >= 0.8 else "#f39c12" if s >= 0.6 else "#e74c3c" for s in scores]

    ax.barh(y_pos, scores, color=colors, edgecolor="black", alpha=0.8)

    for i, score in enumerate(scores):
        ax.text(score + 0.02, i, f"{score:.2f}", va="center", fontsize=10)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.set_xlim(0, 1.15)
    ax.set_xlabel("Score")
    ax.set_title("Agentic Review: Per-Dimension Scores")
    overall_label = f"Overall: {review_result.overall_score:.2f}"
    ax.axvline(review_result.overall_score, color="black", linestyle="--", linewidth=1.5, label=overall_label)
    ax.legend(loc="lower right")
    plt.tight_layout()
    plt.show()


def plot_score_comparison(result_a, result_b, labels=("A", "B")):
    """
    Compare per-dimension scores from two agentic reviews side by side.

    Useful for validating that the reviewer discriminates between clean and
    flawed measurement artifacts (the Assess mode of the Correctness pillar).

    Parameters
    ----------
    result_a : ReviewResult
        First review result (e.g., a known-clean artifact).
    result_b : ReviewResult
        Second review result (e.g., a known-flaw artifact).
    labels : tuple[str, str]
        Display labels for result_a and result_b respectively.
    """
    dims_a = {d.name: d.score for d in result_a.dimensions}
    dims_b = {d.name: d.score for d in result_b.dimensions}
    dim_names = list(dims_a.keys())

    scores_a = [dims_a[n] for n in dim_names]
    scores_b = [dims_b.get(n, 0.0) for n in dim_names]
    display_names = [n.replace("_", " ").title() for n in dim_names]

    y_pos = np.arange(len(dim_names))
    height = 0.35

    _, ax = plt.subplots(figsize=(9, max(3, len(dim_names) * 1.0)))

    bars_a = ax.barh(
        y_pos + height / 2, scores_a, height, color="#2ecc71", edgecolor="black", alpha=0.85, label=labels[0]
    )
    bars_b = ax.barh(
        y_pos - height / 2, scores_b, height, color="#e74c3c", edgecolor="black", alpha=0.85, label=labels[1]
    )

    for bar, score in zip(bars_a, scores_a):
        ax.text(score + 0.02, bar.get_y() + bar.get_height() / 2, f"{score:.2f}", va="center", fontsize=9)
    for bar, score in zip(bars_b, scores_b):
        ax.text(score + 0.02, bar.get_y() + bar.get_height() / 2, f"{score:.2f}", va="center", fontsize=9)

    ax.axvline(
        result_a.overall_score,
        color="#27ae60",
        linestyle="--",
        linewidth=1.5,
        label=f"{labels[0]} overall: {result_a.overall_score:.2f}",
    )
    ax.axvline(
        result_b.overall_score,
        color="#c0392b",
        linestyle="--",
        linewidth=1.5,
        label=f"{labels[1]} overall: {result_b.overall_score:.2f}",
    )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(display_names)
    ax.set_xlim(0, 1.2)
    ax.set_xlabel("Score")
    ax.set_title("Reviewer Discrimination: Known-Clean vs. Known-Flaw")
    ax.legend(loc="lower right", fontsize=9)
    plt.tight_layout()
    plt.show()
