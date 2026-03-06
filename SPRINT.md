# Lecture 03 Application — Refinements (Round 2)

**Status**: executing

## Goal

Continue refining Lecture 03 (Automated Evidence Review): move severity specs to YAML configs, simplify `create_mock_job_directory()`, make the litellm cell executable, and fix remaining GUIDELINES compliance issues (YAML section refs in prose).

## Scope

**In scope**:
- Move severity calibration specs from Python dicts to YAML config files
- Simplify `create_mock_job_directory()` to accept a config dict
- Make the litellm teaching cell executable (not just a markdown code block)
- Fix YAML section references in prose to use **BOLD UPPERCASE**
- Move `import yaml` to the imports cell
- Add Path-support upstream item to backlog

**Out of scope**:
- Part I theory content
- Changes to `_external/` packages
- Lecture 02 changes
- Sphinx build config

## Observations

### 1. Severity specs are hardcoded Python dicts
The `SEVERITY_SPECS` list in cell 45 defines three artifact configurations as Python dicts. These should live in YAML config files alongside `review_config.yaml`, consistent with how the course handles other configurations.

### 2. Path support needed upstream
`evaluate_confidence()` requires `str(job_dir)` — it should accept `Path` objects natively. This belongs in the `tools-impact-engine-evaluate` backlog, not this sprint.

### 3. Config loading is ad-hoc
Cell 24 has `import yaml` buried mid-notebook. The yaml import should be with the other imports at the top of Part II.

### 4. YAML section refs not capitalized
Prose in cell 21 says "configured backend" — per GUIDELINES, top-level YAML section keys should be referenced as **BACKEND** in prose.

### 5. litellm cell is markdown-only
Cell 21 shows a litellm code example as a markdown code block. Making it executable would let students see the actual output and link to the engine source.

### 6. create_mock_job_directory has too many parameters
The function takes 9 individual parameters. The severity loop has to unpack each spec dict into kwargs. A config-dict interface would simplify both the function and its callers.

## Decisions

### 1. Severity specs → YAML configs
Create `config_severity_clean.yaml`, `config_severity_medium.yaml`, `config_severity_flaw.yaml`. Load them in the severity loop with `yaml.safe_load()`.

### 2. Path support → upstream backlog
Add to `.claude/docs/backlog.md` as an evaluate-evidence item. No code changes in this sprint.

### 3. Move import yaml to imports cell
Add `import yaml` to cell 3 (Part II imports). Remove it from cell 24. Keep cell 24 for config loading and job dir creation.

### 4. YAML section refs → BOLD UPPERCASE
Audit all prose cells. Fix "configured backend" → "configured **BACKEND**" in cell 21 and any other occurrences.

### 5. Make litellm cell executable
Convert the markdown code block in cell 21 to a real code cell with `litellm.completion()`. Add a markdown cell linking to [engine.py L300](https://github.com/eisenhauerIO/tools-impact-engine-evaluate/blob/f108a4289ca1a388e95cd3157eef36445351e67a/impact_engine_evaluate/review/engine.py#L300).

### 6. Simplify create_mock_job_directory()
Add a `config` dict parameter that bundles effect_estimate, ci_lower, ci_upper, sample_size, diagnostics. Individual params remain for backward compatibility but the severity loop can pass YAML-loaded dicts directly.

## Plan

### Phase 1: support.py refactor
1. Refactor `create_mock_job_directory()` — add config dict support

### Phase 2: Notebook changes
2. Create 3 severity YAML config files
3. Move `import yaml` to imports cell
4. Make litellm cell executable + add engine.py link + fix BACKEND ref
5. Update severity loop to load from YAML configs
6. Audit all prose for YAML section ref compliance

### Phase 3: Backlog
7. Add Path-support item to `.claude/docs/backlog.md`

### Phase 4: Verification
8. `hatch run ruff check .` + `hatch run ruff format --check .`
9. `hatch run build`

## Files modified

- `docs/source/evaluate-evidence/03-application/support.py`
- `docs/source/evaluate-evidence/03-application/lecture.ipynb`
- `docs/source/evaluate-evidence/03-application/config_severity_clean.yaml` (new)
- `docs/source/evaluate-evidence/03-application/config_severity_medium.yaml` (new)
- `docs/source/evaluate-evidence/03-application/config_severity_flaw.yaml` (new)
- `.claude/docs/backlog.md`

## Verification

1. `hatch run ruff check .`
2. `hatch run ruff format --check .`
3. `hatch run build` — notebook skipped (execute: never), build passes
4. Start Ollama, run notebook end-to-end: `hatch run notebook docs/source/evaluate-evidence/03-application/lecture.ipynb`
