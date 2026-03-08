# Offerings page: audience-neutral language and polish

**Status**: complete

## Goal

The new Offerings section uses "course" and "lecture" throughout, which doesn't fit
corporate clients. Neutralize the language so the page works for both university
program directors and corporate technical leadership. Fix formatting and structural
issues identified during review.

## Scope

**In scope**:
- Neutralize "course"/"lecture" language in `offerings/index.md`
- Fix inline formatting (backticks, caps)
- Clarify Iterations intro text to avoid confusion with Offerings
- Fix minor style inconsistencies in `econ-481A-uw-2026.md`

**Out of scope**:
- Content changes to lecture notebooks
- Structural changes to the toctree order
- Changes to `_external/` packages

## Observations

### 1. "Course" language excludes corporate audience

`offerings/index.md` uses "course" 7 times and "lecture" once. For a page that also
targets corporate clients, this reads as university-only.

| Line | Current text | Issue |
|------|-------------|-------|
| 3 | "A course built on..." | Excludes corporate |
| 11 | "This course treats them as one loop" | Same |
| 13 | "This course teaches participants..." | Same |
| 24 | "Every lecture is a Jupyter notebook" | University framing |
| 28 | "Most Gen AI courses teach prompting. This course teaches..." | Two hits |
| 30 | "The course covers four principles" | Same |
| 46 | "The course adapts to different audiences" | Same |

### 2. Formatting issues (GUIDELINES compliance)

- Line 17: `YAML` should be in backticks when referring to the format
- Line 22: `Pydantic` should be in backticks on first mention
- Line 48: "AND" in caps reads as emphasis-via-caps — should be lowercase "and"

### 3. "Proof" header

"Proof" as a section header may overstate — the section provides evidence/track record,
not mathematical proof. Consider "Track record" or keep if boldness is intentional.

### 4. Iterations intro text ambiguity

`iterations/index.md` says "current and upcoming offerings" — now that there's a page
literally called "Offerings," this creates confusion. Reword to differentiate.

### 5. Minor style inconsistencies

- `offerings/index.md` line 5: horizontal rule `---` after subtitle — check consistency
  with other section index pages
- `econ-481A-uw-2026.md` line 5: uses hyphen `-` instead of em-dash `—` before
  "there are no exams"

## Plan

1. Replace "course"/"lecture" with neutral terms in `offerings/index.md`:
   - Line 3: "Built on a production decision system — not slides about one."
   - Line 11: "This material treats them as one loop."
   - Line 13: "Participants learn to close the loop."
   - Line 24: "Every session is a Jupyter notebook..."
   - Line 28: "Most Gen AI programs teach prompting. Participants learn to build..."
   - Line 30: "The material covers four principles..."
   - Line 46: "The material adapts to different audiences..."
2. Fix inline formatting: backtick `YAML`, backtick `Pydantic`, lowercase "and"
3. Decide on "Proof" header — keep or rename to "Track record"
4. Reword `iterations/index.md` intro to avoid "offerings" overlap
5. Fix hyphen → em-dash in `econ-481A-uw-2026.md`
6. Build docs: `hatch run sphinx-build -D nbsphinx_execute=never docs/source docs/build/html`

## Verification

1. `hatch run sphinx-build -D nbsphinx_execute=never docs/source docs/build/html` — pass
2. Read offerings page end-to-end for tone consistency
3. Confirm no "course" or "lecture" remains in `offerings/index.md` (except in Formats
   subsection where "course" is appropriate for the university paragraph)

## Files to modify

- `docs/source/offerings/index.md` — audience-neutral language, formatting fixes
- `docs/source/iterations/index.md` — reword intro
- `docs/source/iterations/econ-481A-uw-2026.md` — hyphen → em-dash
