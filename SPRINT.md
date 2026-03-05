# Lecture 03 Application — Refinements

**Status**: executing

## Goal

Refine Lecture 03 (Automated Evidence Review) for narrative clarity, GUIDELINES compliance, and reduced boilerplate. The previous sprint implemented the real LLM pipeline; this sprint polishes the result.

## Scope

**In scope**:
- Restructure Part II: dissolve §3 Design Patterns, add bridge/orientation section, fold patterns into where they're used
- Add explicit MEASURE→EVALUATE mock framing in §1
- Add litellm/Ollama teaching cell
- Add pipeline flowchart (SVG or ASCII)
- Reduce boilerplate: reuse job dirs, loop over severity artifacts
- GUIDELINES.md compliance pass (header capitalization, YAML section refs, `! cat` for configs)
- Add header capitalization rule to GUIDELINES.md
- Audit `/review-writing` and `/review-code` skills for missing checks
- Remove `print_rendered_prompt` from support.py if no longer needed
- Remove `inspect.getsource(plot_confidence_ranges)` cell (just show the plot)

**Out of scope**:
- Part I theory content
- Changes to `_external/` packages
- Lecture 02 changes
- Sphinx build config

## Observations

### 1. Mock handoff is implicit
§1 says "We use a helper function to create a mock job directory" but doesn't frame *why* — that we're simulating the MEASURE→EVALUATE contract so the lecture stands alone.

### 2. Unnecessary source display for plot helper
Cell 11 shows `inspect.getsource(plot_confidence_ranges)` before calling it. The source code adds no pedagogical value for a plotting utility — just show the plot.

### 3. §3 Design Patterns is a disconnected tour
Four subsections (Registry, Layered Specialization, Prompt Engineering, Structured Output) shown in isolation before any LLM call. Students see machinery without context for why it matters.

### 4. No bridge from L02 theory to L03 code
L02 introduces high-level architecture (registry, four pillars, evaluation harness). L03 jumps straight into code without mapping L02 concepts to the concrete objects students will encounter.

### 5. Raw prompt dump instead of visual pipeline
`print_rendered_prompt()` dumps raw text. A flowchart showing artifact → registry → prompt rendering → LLM → structured output → confidence would orient students better.

### 6. Header capitalization inconsistent
Subsection headers use title case ("Running the Review", "Configuration") with no documented rule. Course convention from other lectures is sentence case.

### 7. Config shown via Python instead of `! cat`
Cell 33 uses `yaml.safe_load()` + `yaml.dump()` instead of the course convention `! cat review_config.yaml`. Prose references "backend" instead of **BACKEND**.

### 8. GUIDELINES gaps not caught by review skills
The `/review-writing` and `/review-code` skills don't check for YAML section capitalization, header case conventions, or `! cat` for config display.

### 9. No litellm/Ollama teaching moment
Students never see the core mechanism — a `litellm.completion()` call with `ollama_chat/model`. The pipeline abstracts it away without first showing what it wraps.

### 10. Redundant job directories
Each subsection in §4 and §5 creates a new `create_mock_job_directory()` with identical parameters. One review job dir can serve all calls (except severity calibration, which needs different artifact data).

### 11. Severity calibration boilerplate
Three near-identical blocks of create-dir → evaluate → extract → print. The repetition obscures the pedagogical point (monotonic score ordering).

## Decisions

### 1. Mock handoff → explicit framing
Add a sentence to §1 intro: we simulate the MEASURE→EVALUATE handoff so the lecture runs standalone without the full pipeline. Frame the mock as intentional pedagogy.

### 2. Drop `plot_confidence_ranges` source display
Delete cell 11 (`inspect.getsource(plot_confidence_ranges)`). Keep cell 12 that calls `plot_confidence_ranges(confidence_map)`.

### 3. Dissolve §3, fold patterns into context
Remove §3 "Design Patterns in Practice" as a standalone section. Move registry + layered specialization into the new bridge section (decision 4). Move prompt engineering, rendered prompt, and structured output into §4 Agentic Review — show each pattern right before it's used.

### 4. Add bridge section after imports
New §3 "From theory to code" that:
- Maps L02 architecture concepts to the concrete objects in the codebase (registry, prompt specs, knowledge bases, structured output)
- Includes the registry + layered specialization demo (moved from old §3)
- Includes a pipeline flowchart (decision 5)
- Introduces litellm/Ollama (decision 9)

### 5. Pipeline flowchart replaces `print_rendered_prompt()`
Create an SVG diagram showing: job directory → manifest dispatch → reviewer → prompt rendering → LLM call → structured output → confidence. Place it in the bridge section. Remove the `print_rendered_prompt()` call and its support.py function.

### 6. Header capitalization → sentence case rule
Add to GUIDELINES.md: all headers use sentence case (capitalize first word and proper nouns only). Fix all L03 headers to comply.

### 7. Config display → `! cat` + **BACKEND**
Replace the Python `yaml.safe_load()` + `yaml.dump()` cell with `! cat review_config.yaml`. Update prose to reference **BACKEND** section per GUIDELINES YAML convention. Remove `yaml` from imports if no longer needed.

### 8. Skill audit for missing GUIDELINES checks
After notebook changes are done, audit `/review-writing` and `/review-code` skills. Add checks for: YAML section capitalization in prose, header sentence case, `! cat` convention for config files.

### 9. litellm/Ollama teaching cell
Add a cell in the bridge section showing a bare `litellm.completion()` call with `ollama_chat/llama3.2`. Link to Ollama docs. Students see the raw mechanism before the pipeline wraps it. Use markdown explanation — no need to execute the cell (the pipeline call in §4 covers that).

### 10. Single review job directory
Create one review job dir at the start of §4 and reuse it for: the main agentic review call, run-to-run stability, temperature=0.7, and mistral backend. Severity calibration keeps its own dirs (different artifact data by design).

### 11. Reduce boilerplate notebook-wide
For severity calibration: define artifact specs as a list of dicts, loop to create dirs and run reviews. For §5 comparison prints: consider a helper or at minimum tighten the repeated blocks. Focus the notebook on results and interpretation, not setup code.

## Plan

### Phase 1: GUIDELINES and skills
1. Add sentence-case header rule to GUIDELINES.md
2. Audit `/review-writing` skill, add missing checks
3. Audit `/review-code` skill, add missing checks

### Phase 2: Notebook restructure
4. Update §1 markdown — add explicit mock framing
5. Delete `inspect.getsource(plot_confidence_ranges)` cell
6. Delete `inspect.getsource(print_evaluate_result)` cell (same pattern)
7. Create pipeline flowchart SVG, add to `docs/source/_static/`
8. Write new §3 "From theory to code" — L02 mapping, registry demo, layered specialization, flowchart, litellm intro
9. Fold prompt engineering + rendered prompt + structured output into §4
10. Replace `yaml.safe_load/dump` with `! cat review_config.yaml`
11. Fix all headers to sentence case
12. Fix all YAML section references to **BOLD UPPERCASE**

### Phase 3: Boilerplate reduction
13. Create single review job dir, reuse across §4 and §5
14. Refactor severity calibration into loop over artifact specs
15. Tighten §5 comparison print blocks
16. Remove `print_rendered_prompt` from support.py
17. Clean up imports (remove `yaml` if unused, remove unused support imports)

### Phase 4: Verification
18. `hatch run ruff check .` + `hatch run ruff format --check .`
19. `hatch run build`
20. Full GUIDELINES compliance check on L03
21. Start Ollama, run notebook end-to-end

## Files modified

- `docs/source/evaluate-evidence/03-application/lecture.ipynb`
- `docs/source/evaluate-evidence/03-application/support.py`
- `docs/source/evaluate-evidence/03-application/review_config.yaml` (possibly unchanged)
- `docs/source/GUIDELINES.md`
- `.claude/skills/review-writing` (skill audit)
- `.claude/skills/review-code` (skill audit)

## Verification

1. `hatch run ruff check .`
2. `hatch run ruff format --check .`
3. `hatch run build` — notebook skipped (execute: never), build passes
4. Full GUIDELINES.md compliance check on L03
5. Start Ollama, run notebook end-to-end: `hatch run notebook docs/source/evaluate-evidence/03-application/lecture.ipynb`
