# Course Review

Comprehensive validation of course materials. **If any step fails, stop and report findings before proceeding.**

**Exclude:** `_external/` directory.

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
grep -E "from support|from \." docs/source/**/lecture.ipynb
```

For each import like `from support import ...`, verify `support.py` exists in the same directory as the notebook.

#### Check Config File References

```bash
# Find config file references
grep -E 'cat.*\.yaml|\.yaml' docs/source/**/lecture.ipynb
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

## Checklist

- [ ] `hatch run build` completes successfully
- [ ] All external URLs return 200 (or expected 403 for paywalled content)
- [ ] All image files exist at referenced paths
- [ ] All internal notebook references resolve
- [ ] Notation is consistent across all lectures
- [ ] No untracked files that should be committed

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
