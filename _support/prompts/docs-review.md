# Documentation Review Workflow

Use this file to track systematic documentation reviews. Start a new Claude session and reference this file to continue where you left off.

## How to Use

1. Start a new Claude session
2. Say: "Let's continue the docs review from REVIEW_WORKFLOW.md"
3. Review the next unchecked section together
4. Mark it complete when done

---

## Review Progress

### Section 1: Overview
- **Files:** `docs/source/overview/index.md`, `docs/source/overview/01_fundamental_problem.ipynb`
- **Status:** [x] Completed
- **Notes:** Fixed missing period in index.md; corrected "three" to "four" variables; fixed typos in LaLonde quote (designed, applicants, added articles)

### Section 2: Understand Domain
- **Files:** `docs/source/understand-domain/index.md`
- **Status:** [x] Completed
- **Notes:** No issues found; all links verified working

### Section 3: Measure Impact
- **Files:** `docs/source/measure-impact/index.md`, `docs/source/measure-impact/01_generalized_roy_model.ipynb`
- **Status:** [x] Completed
- **Notes:** Fixed broken link (tools-causal-engine → tools-impact-engine); notebook is placeholder with TBD content; 9 todo blocks for future notebook links

### Section 4: Allocate Resources
- **Files:** `docs/source/allocate-resources/index.md`
- **Status:** [x] Completed
- **Notes:** Placeholder section marked "under construction"; no issues found

### Section 5: Build Systems
- **Files:** `docs/source/build-systems/index.md`
- **Status:** [x] Completed
- **Notes:** Added second Kiro resource link for symmetry; all links verified working

### Section 6: Improve Decisions
- **Files:** `docs/source/improve-decisions/index.md`
- **Status:** [x] Completed
- **Notes:** Placeholder section marked "under construction"; no issues found

### Section 7: Guest Lecturers
- **Files:** `docs/source/guest-lecturers/index.md`
- **Status:** [ ] Not started
- **Notes:**

### Section 8: Software
- **Files:** `docs/source/software/index.md`
- **Status:** [ ] Not started
- **Notes:**

### Section 9: Main Index & References
- **Files:** `docs/source/index.md`, `docs/source/references.md`, `docs/source/references.bib`
- **Status:** [ ] Not started
- **Notes:**

---

## Review Checklist (Per Section)

When reviewing each section, check for:

**Content Accuracy**
- [ ] Technical explanations correct
- [ ] Code examples work
- [ ] Links valid
- [ ] Data/statistics accurate

**Writing Quality**
- [ ] Clear and concise
- [ ] Consistent terminology
- [ ] No grammar/spelling errors
- [ ] Logical flow

**Terminology Conventions**
- [ ] Use "shoppers" (not "customers") when referring to end-users in e-commerce context
- [ ] Verify consistency across all documentation

**Completeness**
- [ ] All topics covered
- [ ] Sufficient depth
- [ ] Examples where needed
- [ ] No unaddressed TODOs

---

## Lecture Summary Guidelines

When writing lecture summaries in index.md files, follow this standardized pattern used in both Understand Domain and Measure Impact sections.

### Standard Format (2-3 Sentences)

**Sentence 1:** We introduce/discuss/present [method/framework/tool] as [its role/purpose].

**Sentence 2:** This section [formalizes/explores/examines/emphasizes] [what problem/concept it addresses].

**Sentence 3 (optional):** The goal is to [learning objective] OR [connection to broader framework].

### Examples

**Potential Outcomes Model:**
```
We introduce the potential outcomes framework as the foundational model for causal inference.
This section formalizes the fundamental problem of causal inference—missing counterfactuals—and
explains why randomization resolves it. The goal is to establish a precise language for defining
causal effects and understanding what can and cannot be identified from data.
```

**Instrumental Variables:**
```
We introduce instrumental variables as a method for causal inference when unobserved confounding
is present. The focus is on identification assumptions, interpretation of local average treatment
effects, and the role of instruments within the Generalized Roy framework.
```

### Key Characteristics

**Tone:**
- Conceptual and framework-focused (not action/implementation-focused)
- Theoretical emphasis on understanding (not building/implementing)

**Content:**
- Emphasize identification assumptions, learning objectives, frameworks
- Connect to broader course context (Generalized Roy Model, business decisions)
- Explain what problem the method solves

**Structure:**
- Always 2-3 sentences (no more, no less)
- Use verbs: introduce, discuss, present, explore, examine (avoid: implement, build, create)
- Focus on "what you understand" not "what you produce"
- Notebook links should be formatted as bullet points below the summary

### Common Patterns

✅ **Do:**
- Start with "We introduce [X] as [purpose]"
- Use "This section formalizes/explores/examines..."
- End with "The goal is to..." or "The focus is on..."
- Mention identification assumptions where relevant
- Connect to Generalized Roy framework (for Measure Impact)
- Emphasize learning objectives
- Format notebook links as: `- [Lecture Title](path/lecture.ipynb)`

❌ **Don't:**
- List technical components without context
- Use action verbs like "implement," "build," "create"
- Write single-sentence summaries
- Focus on tools/outputs instead of concepts/understanding
- Exceed 3 sentences

---

## Session Log

Record completed review sessions here:

| Date | Sections Reviewed | Key Changes |
|------|-------------------|-------------|
| | | |
