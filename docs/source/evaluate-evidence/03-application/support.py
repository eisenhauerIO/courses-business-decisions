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
    evaluate_strategy="score",
    effect_estimate=150.0,
    ci_lower=80.0,
    ci_upper=220.0,
    sample_size=500,
    cost_to_scale=50000.0,
    diagnostics=None,
    *,
    config=None,
):
    """
    Create a temporary job directory with manifest and impact results.

    Simulates the output of the MEASURE stage so that the EVALUATE stage
    can be demonstrated without running the full pipeline.

    Parameters
    ----------
    initiative_id : str, optional
        Identifier for the initiative.
    model_type : str, optional
        Causal method label (must match a registered reviewer).
    evaluate_strategy : str, optional
        Strategy for evaluation: ``"score"`` or ``"review"``.
    effect_estimate : float, optional
        Point estimate of the treatment effect.
    ci_lower : float, optional
        Lower bound of the confidence interval.
    ci_upper : float, optional
        Upper bound of the confidence interval.
    sample_size : int, optional
        Number of observations in the study.
    cost_to_scale : float, optional
        Cost to scale the initiative.
    diagnostics : dict or None, optional
        Diagnostic statistics to embed in the artifact. If ``None``, uses
        defaults representing a clean, well-powered experiment.
    config : dict or None, optional
        Configuration dict that can supply any of the above keys. When
        provided, its values override the corresponding positional defaults.
        Useful for loading artifact specs from YAML files.

    Returns
    -------
    pathlib.Path
        Path to the temporary job directory.
    """
    if config is not None:
        initiative_id = config.get("initiative_id", initiative_id)
        model_type = config.get("model_type", model_type)
        evaluate_strategy = config.get("evaluate_strategy", evaluate_strategy)
        effect_estimate = config.get("effect_estimate", effect_estimate)
        ci_lower = config.get("ci_lower", ci_lower)
        ci_upper = config.get("ci_upper", ci_upper)
        sample_size = config.get("sample_size", sample_size)
        cost_to_scale = config.get("cost_to_scale", cost_to_scale)
        diagnostics = config.get("diagnostics", diagnostics)

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
    Print the output of ``evaluate_confidence``.

    Parameters
    ----------
    result : EvaluateResult
        Output from ``evaluate_confidence()``.
    """
    lo, hi = result.confidence_range
    print("EVALUATE Output")
    print("=" * 50)
    print(f"  Initiative:    {result.initiative_id}")
    print(f"  Strategy:      {result.strategy}")
    print(f"  Confidence:    {result.confidence:.3f}")
    print(f"  Range:         ({lo:.2f}, {hi:.2f})")


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


def plot_severity_calibration(results, labels):
    """
    Plot a grouped bar chart comparing per-dimension scores across severity levels.

    Each result gets a cluster of bars (one per dimension) plus a dashed
    horizontal line at its overall score. Useful for validating that the
    reviewer assigns monotonically decreasing scores as artifact quality
    degrades.

    Parameters
    ----------
    results : list[ReviewResult]
        Review results ordered from cleanest to most flawed.
    labels : list[str]
        Display labels corresponding to each result.
    """
    n_results = len(results)
    dim_names = [d.name for d in results[0].dimensions]
    display_names = [n.replace("_", " ").title() for n in dim_names]
    n_dims = len(dim_names)

    x = np.arange(n_dims)
    width = 0.8 / n_results
    colors = ["#2ecc71", "#f39c12", "#e74c3c"]

    _, ax = plt.subplots(figsize=(10, 5))

    for i, (result, label) in enumerate(zip(results, labels)):
        scores = {d.name: d.score for d in result.dimensions}
        vals = [scores.get(n, 0.0) for n in dim_names]
        offset = (i - n_results / 2 + 0.5) * width
        color = colors[i % len(colors)]
        ax.bar(x + offset, vals, width, label=label, color=color, edgecolor="black", alpha=0.85)
        ax.axhline(result.overall_score, color=color, linestyle="--", linewidth=1.2, alpha=0.7)

    ax.set_xticks(x)
    ax.set_xticklabels(display_names, rotation=30, ha="right")
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Score")
    ax.set_title("Severity Calibration: Known-Clean → Known-Flaw")
    ax.legend(loc="upper right", fontsize=9)
    plt.tight_layout()
    plt.show()
