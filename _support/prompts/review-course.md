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

### 4. Check Git Status

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
