---
name: review-writing
description: Use when reviewing prose in markdown files and Jupyter notebook markdown cells. Checks formatting, style, clarity, and pedagogical effectiveness.
---

# Writing Review

Review prose in markdown files (`.md`) and Jupyter notebook markdown cells for formatting, style, clarity, and pedagogical effectiveness.

**Exclude:** `_external/` directory.

---

# Step 1: Load Guidelines

Read the project's writing guidelines file at `docs/source/GUIDELINES.md`. This is the single source of truth for all formatting, terminology, and structural conventions. Every check below should be measured against the standards defined there.

If the file does not exist, report this as the first finding.

---

# Step 2: Formatting Audit

Using the inline formatting table and emphasis rules from the guidelines, audit the target file(s):

- [ ] All column names use `` `column_name` `` format
- [ ] All functions use `` `function_name()` `` format
- [ ] All file references use `` `"filename.ext"` `` format
- [ ] Object types use backticks (`` `DataFrame` ``, `` `JobInfo` ``)
- [ ] First introduction of concepts uses **bold**
- [ ] Links use meaningful text, not "click here"
- [ ] Headers are questions when exploring data
- [ ] Active voice, present tense throughout
- [ ] Phase names are lowercase bold (**products**)
- [ ] YAML sections are uppercase bold (**PRODUCTS**)
- [ ] Uses "shoppers" not "customers" for e-commerce end-users
- [ ] Additional resources section uses correct format

---

# Step 3: Structure Compliance

Check that the document follows the structural conventions from the guidelines:

- Do notebooks follow the prescribed structure (Theory → Application, notation tables, assignment mechanism)?
- Are configs named according to convention (`config_*.yaml`)?
- Is the writing style consistent with other lectures?
- Are all config files displayed to the reader (via `! cat`) before use?

---

# Step 4: Check Links and References

## External URLs

Find all external URLs in the target file(s):

```bash
# In markdown files
grep -rhoE 'https?://[^)>"]+' FILE --include="*.md" | sort -u

# In notebooks (JSON format)
grep -rhoE 'https?://[^)>"\\]+' FILE --include="*.ipynb" | sort -u
```

For each unique URL, verify accessibility:

```bash
curl -s -o /dev/null -w "%{http_code}" "URL"
```

**Expected:** 200 OK. **Flag:** 404 (broken), 403 (restricted — OK for paywalled academic content), 3xx (redirect).

## Internal References

Verify that all image and file references resolve:

- Image files referenced via `![](path)` or `<img src="path">` exist at the expected path
- Notebook cross-references (e.g., `toctree` entries, relative links) point to existing files
- SVG/PNG files referenced in `{figure}` directives exist in `_static/`

## Rendered Output

If docs use Sphinx, inspect the built HTML for rendering problems:

- **Anchor-only hrefs**: Search for `href="#` patterns that look like failed relative links
- **Missing formatting**: Verify that inline code, bold, italic, and links render as intended
- **Image/badge rendering**: Confirm diagrams and images load correctly

---

# Step 5: Check Infrastructure

Verify standard docs tooling is in place:

| Check | What to look for |
|-------|-----------------|
| Sphinx builds clean | Run the docs build command, check for warnings |
| nbstripout | Pre-commit hook configured to strip notebook outputs |
| nbmake | Notebooks tested via pytest in pre-commit or CI |
| Matplotlib config | Consistent plot rendering config (matplotlibrc) |
| CI/CD | Docs build workflow in .github/workflows/ |
| Pre-commit | .pre-commit-config.yaml includes docs-related hooks |

---

# Step 6: Pedagogical Clarity

## Content Accuracy

- [ ] Definitions and notation are mathematically correct
- [ ] Equations and derivations are accurate
- [ ] Statistical concepts are properly explained
- [ ] Data/statistics cited are accurate and sourced

## Structure and Flow

- [ ] Concepts build on each other in a sensible order
- [ ] Prerequisites are introduced before they're needed
- [ ] Transitions between sections are clear
- [ ] The narrative has a clear beginning, middle, and end
- [ ] Theory and application sections are appropriately balanced
- [ ] No section is disproportionately long or short

## Narrative Depth

- [ ] Concepts are explained thoroughly with multiple paragraphs, not just stated
- [ ] Mathematical derivations show intermediate steps, not just final results
- [ ] The "why" is explained, not just the "what"
- [ ] Tables organize definitions, parameters, and comparisons
- [ ] Formal definitions use precise LaTeX notation

## Examples and Applications

- [ ] At least one complete worked example with code
- [ ] Example is realistic and relatable
- [ ] Steps are explained, not just shown
- [ ] Results are interpreted, not just displayed

## Engagement and Clarity

- [ ] Technical jargon is explained on first use
- [ ] Assumes appropriate (not excessive) prior knowledge
- [ ] Difficult concepts have intuitive explanations
- [ ] Headers pose questions where appropriate
- [ ] Students can run code and see results

## Completeness

- [ ] All referenced concepts are defined
- [ ] No "TODO" or placeholder content in final version
- [ ] All code cells are complete and runnable
- [ ] Figures and tables are labeled and explained
- [ ] Covers the topic adequately for the course level

---

# Step 7: Measure-Impact Pedagogy Checklist

For lectures under `docs/source/measure-impact/`, also verify:

- [ ] Selection paradox is explicit: true effect is positive, naive estimate is negative/biased
- [ ] Notation table present in Business Context (Variable | Notation | Description)
- [ ] Assignment mechanism section explains WHY naive comparison fails
- [ ] Interface-to-theory mapping table present for each Impact Engine method call
- [ ] "God's eye view" framing used when introducing simulator potential outcomes
- [ ] Part II introduction references specific Part I concepts by name
- [ ] Source code shown via `inspect.getsource()` for key support functions
- [ ] Theory matches the referenced Mixtape chapter

---

# Review Questions

When reviewing, ask yourself:

1. **Would a reader understand this?** Not just follow along, but actually grasp the concept.
2. **Is the "why" explained?** Not just what the method does, but why it works and when to use it.
3. **Are assumptions made explicit?** Readers should know what conditions must hold.
4. **What would confuse someone?** Identify potential stumbling blocks before readers hit them.

---

# Output Format

For each issue found:
1. **Location**: File and line/section reference
2. **Issue**: What's wrong
3. **Suggestion**: How to fix it

---

# Verification

After making changes, always run:

```bash
git status
hatch run ruff format .
hatch run ruff check .
hatch run build
```

**Success criteria:**
- [ ] All new files are under version control
- [ ] `hatch run ruff format .` completes without changes
- [ ] `hatch run ruff check .` passes with no errors
- [ ] `hatch run build` completes successfully
