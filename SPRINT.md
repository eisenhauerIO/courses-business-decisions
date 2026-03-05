# Evaluate Evidence Lecture 03 — Real Agentic Review

**Status**: implemented

## Goal

Rewrite Lecture 03 (Automated Evidence Review) to actually run the `impact_engine_evaluate` pipeline end-to-end with real LLM calls via local Ollama. The current notebook constructs all `ReviewResult` objects by hand with hardcoded scores — the lecture that is supposed to demonstrate the agentic evaluation system never calls it.

## Scope

**In scope**:
- Rewrite Part II of `docs/source/evaluate-evidence/03-application/lecture.ipynb`
- Add helpers to `support.py`, create `review_config.yaml`
- Drop the "From Confidence to Allocation" section (old §4)

**Out of scope**:
- Changes to Lecture 02 or Impact Engine repositories (`_external/`)
- Changes to Sphinx build config (already has `nbsphinx: execute: never`)

## Lecture 03 → Lecture 02 Mapping

| L03 Section | What it does | L02 concept |
|---|---|---|
| §1 Measurement Artifacts | Mock job dir, inspect manifest + results | §1 The Evaluation Task |
| §2 Deterministic Scoring | Confidence map, score strategy | §5 Registry + Dispatch |
| §3 Design Patterns in Practice | Source code of registry, prompts, knowledge, structured output | §2 Four Pillars + §5 Design Patterns |
| §4 Agentic Review | Ollama backend, real `evaluate_confidence()` | §3 Eval Architectures (Judge) + §2 Defensible Confidence |
| §5 Evaluating the Evaluator | Internal + external validity through real pipeline | §4 Evaluation Harness (Assess mode) |

## Plan

### Files to modify

1. `docs/source/evaluate-evidence/03-application/lecture.ipynb` — rewrite Part II
2. `docs/source/evaluate-evidence/03-application/support.py` — add `print_rendered_prompt`, `plot_severity_calibration`
3. `docs/source/evaluate-evidence/03-application/review_config.yaml` — new file, Ollama backend config

### LLM backend

Local Ollama with `llama3.2` (same as catalog-ai lecture). No API key needed.

```yaml
backend:
  model: "ollama_chat/llama3.2"
  temperature: 0.0
  max_tokens: 2048
```

### Notebook structure

**Part I: Theory (keep as-is)**
- Title + intro (update to mention Ollama instead of pre-computed values)
- Pipeline overview, score-vs-review strategy table

**Part II: Application**

**§1. Measurement Artifacts (keep)**
- `create_mock_job_directory()` source, create dir, inspect manifest + impact_results

**§2. Deterministic Scoring (keep)**
- Confidence map, plot, `evaluate_confidence()` with score strategy, `score_confidence()`

**§3. Design Patterns in Practice (NEW)**
- **3.1 Registry + Dispatch** — `MethodReviewerRegistry.available()`, `.create("experiment")`, show `ExperimentReviewer` source. Then `QuasiExperimentalReviewer` to demonstrate **layered specialization**: same base class, different prompt/knowledge/confidence range.
- **3.2 Prompt Engineering as Software** — `list_prompts()`, `list_knowledge_bases()`, load prompt spec, display dimensions + templates, load and show knowledge content.
- **3.3 Rendered Prompt** — create review job dir, load manifest + artifact, render with `render(spec, variables)`, display via `print_rendered_prompt()`.
- **3.4 Structured Output** — show `ReviewResponse` and `DimensionResponse` Pydantic schemas via `inspect.getsource()`.

**§4. Agentic Review (NEW — real LLM call)**
- Load `review_config.yaml`, show config
- `evaluate_confidence(config, str(review_job_dir))` — real Ollama call
- Extract and display `ReviewResult` with `print_review_result()` + `plot_review_dimensions()`
- Compare score vs review confidence side-by-side

**§5. Evaluating the Evaluator (rewrite — real LLM calls)**
- **5.1 Internal Validity — Run-to-Run Stability**: Explain `temperature` — at 0.0 the model samples deterministically (greedy decoding). Call `evaluate_confidence()` twice with temp=0.0, compare scores. Then re-run with temp=0.7 to show stochastic variance. Tests Reproducibility pillar.
- **5.2 Internal Validity — Backend Sensitivity**: Same artifact through `ollama_chat/mistral` (temp=0.0). Compare against llama3.2. Jury framing note: aggregating instead of comparing gives the Jury architecture from L2 §3.
- **5.3 External Validity — Severity Calibration**:
  - **Known-clean**: sample_size=10000, effect=50, ci=[30,70], max_smd=0.02, attrition=0.02, compliance=0.97
  - **Known-medium-flaw**: sample_size=200, effect=180, ci=[40,320], max_smd=0.12, attrition=0.12, compliance=0.82
  - **Known-flaw**: sample_size=80, effect=300, ci=[-5,605], max_smd=0.35, attrition=0.25, compliance=0.68
  - Plot all three with `plot_severity_calibration()`
  - Score ordering (clean > medium > flaw) confirms severity calibration per L2 §4

**§6. Additional resources (keep)**

### support.py additions

- `print_rendered_prompt(messages)` — format system/user messages, truncate at 2000 chars
- `plot_severity_calibration(results, labels)` — 3-way grouped bar chart with overall score lines

### Total LLM calls: 8

main, stability rerun, temp=0.7 run, mistral backend, known-clean, known-medium-flaw, known-flaw

## Verification

1. Start Ollama, ensure `llama3.2` and `mistral` are pulled
2. `hatch run notebook docs/source/evaluate-evidence/03-application/lecture.ipynb`
3. Confirm 8 LLM calls produce valid ReviewResult objects
4. Confirm run-to-run stability at temp=0.0
5. Confirm severity calibration: clean > medium > flaw
6. Run prerequisite lecture to confirm no regressions: `hatch run notebook docs/source/evaluate-evidence/02-agentic-evaluation-system/lecture.ipynb`
7. `ruff check docs/source/evaluate-evidence/03-application/support.py`
8. `hatch run build` — notebook skipped (execute: never), build passes
