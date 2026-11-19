---
description: Use when performing a comprehensive validation of course materials, or when asked whether a lecture teaches well. Builds docs, checks links, verifies references, validates notation consistency, and reviews teaching quality (accuracy, flow, narrative depth, worked examples, scope).
---

# Course Review

Comprehensive validation of course materials. **If any step fails, stop and report findings before proceeding.**

---

## Steps

### 1. Build Documentation

```bash
hatch run build
```

This executes all notebooks and builds the site. If any notebook fails, stop and report.

---

### 2. Check All Links

#### Find All External URLs

```bash
# In markdown files
grep -rhoE 'https?://[^)>"]+' docs/source/ --include="*.md" | sort -u

# In notebooks (JSON format)
grep -rhoE 'https?://[^)>"\\]+' docs/source/ --include="*.ipynb" | sort -u
```

#### Verify Each URL

For each unique URL, check accessibility:

```bash
curl -s -o /dev/null -w "%{http_code}" "URL"
```

**Expected:** 200 OK
**Flag:** 404 (broken), 403 (restricted), 3xx (redirect)

#### Common Link Categories

| Category | Example Pattern | Notes |
|----------|-----------------|-------|
| Course repo | `github.com/eisenhauerIO/courses-business-decisions` | Should always work |
| Tool repos | `github.com/eisenhauerIO/tools-*` | Verify repo exists |
| API docs | `eisenhauerio.github.io/tools-*/` | Check module paths match |
| External tools | `python.org`, `numpy.org`, etc. | Usually stable |
| Academic | `pubs.aeaweb.org`, journals | May require auth (403 OK) |

---

### 3. Verify Internal References

#### Image Files

```bash
# Find all image references
grep -rhoE '!\[.*\]\([^)]+\)' docs/source/ --include="*.md"
grep -rhoE '"[^"]+\.(png|svg|jpeg|jpg)"' docs/source/ --include="*.ipynb"
```

For each reference, verify the file exists at the expected path.

#### Notebook References

```bash
# Find internal notebook links
grep -rhoE '\]\([^http][^)]+\.ipynb' docs/source/ --include="*.md"
grep -rhoE '\]\([0-9]+-[^)]+/lecture' docs/source/ --include="*.md"
```

---

### 4. Verify Lecture Self-Containment

Each lecture directory should be fully self-contained. All files required to run the notebook must exist in the same directory.

#### Check Local Python Imports

For each lecture notebook, find local imports and verify the files exist:

```bash
# Find local imports in notebooks
grep -rE --include=lecture.ipynb "from support|from \." docs/source
```

For each import like `from support import ...`, verify `support.py` exists in the same directory as the notebook.

#### Check Config File References

```bash
# Find config file references
grep -rE --include=lecture.ipynb 'cat.*\.yaml|\.yaml' docs/source
```

For each config file reference like `config_simulation.yaml`, verify the file exists in the lecture directory.

#### Expected Lecture Directory Structure

```
docs/source/<section>/<lecture-name>/
├── lecture.ipynb          # Main notebook
├── support.py             # Local helper functions (if imported)
├── config_*.yaml          # Configuration files (if referenced)
└── output/                # Generated outputs (gitignored)
```

---

### 5. Check Notation Consistency Across Lectures

Verify that mathematical notation, variable names, and symbols are used consistently across all lectures.

#### Extract Notation Patterns

Review each lecture notebook for:

- **Mathematical symbols**: Greek letters ($\alpha$, $\beta$, $\theta$, etc.)
- **Variable naming**: Treatment indicators ($D$, $T$, $W$), outcomes ($Y$, $Y_0$, $Y_1$), covariates ($X$, $Z$)
- **Function notation**: Expectations ($E[\cdot]$, $\mathbb{E}[\cdot]$), probabilities ($P(\cdot)$, $\Pr(\cdot)$)
- **Subscript/superscript conventions**: Time indices, group indicators, potential outcomes

#### Cross-Reference Check

For each notation element, verify:

1. Same concept uses same symbol across all lectures
2. Same symbol is not used for different concepts
3. Notation introduced in earlier lectures matches usage in later lectures

#### Common Inconsistencies to Flag

| Category | Check For |
|----------|-----------|
| Treatment indicator | $D$ vs $T$ vs $W$ for same concept |
| Potential outcomes | $Y(0), Y(1)$ vs $Y_0, Y_1$ |
| Expectations | $E[\cdot]$ vs $\mathbb{E}[\cdot]$ |
| Probabilities | $P(\cdot)$ vs $\Pr(\cdot)$ vs $p(\cdot)$ |
| Indices | Subscript vs superscript for same meaning |

---

### 6. Check Git Status

```bash
git status
```

Flag any untracked files in `docs/source/` that should be committed.

---

### 7. Review Teaching Quality

The mechanical steps above check that the course builds and links; this one
checks that it teaches. Run it per lecture once steps 1–6 pass. Formatting is
not repeated here: run `bdc-review-writing` for that, with this course's
conventions in `docs/source/GUIDELINES.md`.

#### Content Accuracy
- [ ] Definitions and notation are mathematically correct
- [ ] Equations and derivations are accurate
- [ ] Statistical concepts are properly explained
- [ ] Data/statistics cited are accurate and sourced

#### Structure and Flow
- [ ] Concepts build on each other in a sensible order
- [ ] Prerequisites are introduced before they're needed
- [ ] Transitions between sections are clear
- [ ] The narrative has a clear beginning, middle, and end
- [ ] Theory and application sections are appropriately balanced
- [ ] No section is disproportionately long or short
- [ ] Complex topics get adequate depth; simple topics aren't over-explained

#### Narrative Depth

The reviewable form of `bdc-writing-support`'s three voice habits.

- [ ] Concepts are explained thoroughly with multiple paragraphs, not just stated
- [ ] Mathematical derivations show intermediate steps, not just final results
- [ ] The "why" is explained, not just the "what"
- [ ] Tables organize definitions, parameters, and comparisons
- [ ] Formal definitions use precise LaTeX notation
- [ ] Complex ideas are decomposed into named components

#### Worked Examples
- [ ] At least one complete worked example with code
- [ ] Example is realistic and relatable
- [ ] Steps are explained, not just shown
- [ ] Results are interpreted, not just displayed

#### Engagement and Clarity
- [ ] Technical jargon is explained on first use
- [ ] Assumes appropriate (not excessive) prior knowledge
- [ ] Difficult concepts have intuitive explanations
- [ ] Analogies or visual aids are used where helpful
- [ ] Students can run code and see results
- [ ] Opportunities for exploration or modification exist

#### Completeness and Scope
- [ ] All referenced concepts are defined
- [ ] No "TODO" or placeholder content in final version
- [ ] All code cells are complete and runnable
- [ ] Figures and tables are labeled and explained
- [ ] Covers the topic adequately for the course level
- [ ] Doesn't try to cover too much in one lecture
- [ ] Points to additional resources for deeper exploration

---

## Checklist

- [ ] `hatch run build` completes successfully
- [ ] All external URLs return 200 (or expected 403 for paywalled content)
- [ ] All image files exist at referenced paths
- [ ] All internal notebook references resolve
- [ ] Notation is consistent across all lectures
- [ ] No untracked files that should be committed
- [ ] Each lecture passes the teaching review: concepts build logically, jargon is explained, examples are realistic and explained, results are interpreted, nothing is a placeholder

---

## Output Format

**Link Issues:**
| File | Link | Status | Fix |
|------|------|--------|-----|
| path/to/file.md | URL | 404 | Suggested fix |

**Missing Files:**
| Referenced In | Missing File |
|---------------|--------------|
| path/to/file.md | path/to/image.png |

**Notation Inconsistencies:**
| Concept | Lecture A | Lecture B | Recommended |
|---------|-----------|-----------|-------------|
| Treatment indicator | $D$ | $T$ | Pick one and use consistently |

**Teaching Issues:**
| Lecture | Section | Issue | Suggestion |
|---------|---------|-------|------------|
| path/to/lecture | Worked example | Result shown, not interpreted | State what the estimate means for the business question |
