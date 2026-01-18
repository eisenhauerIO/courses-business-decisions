# Lecture Guidelines

## Purpose
Standards for structuring lecture notebooks across the Business Decisions course.
Each lecture group follows a specific pedagogical pattern.

---

## Measure Impact Lectures

### Reference Header (REQUIRED)
Every measure-impact notebook MUST begin with a reference block:

```markdown
# [Lecture Title]

> **Reference:** *Causal Inference: The Mixtape*, Chapter X: [Chapter Title] (pp. XX-XX)

This lecture introduces [framework/method]. We apply these concepts using
the Online Retail Simulator to answer: **[business question]?**
```

### Source Material

The Mixtape chapters are available at `_external/books-mixtape/`. Use these PDF chapters as the primary source for the theory sections. The theory content should closely follow the book's:
- Notation and terminology
- Order of topic presentation
- Key examples and intuitions
- Mathematical derivations

### Structure Pattern: Theory → Application

**Part I: Theory** (from Mixtape chapter)
- Introduce framework/method with formal definitions
- Present notation (potential outcomes, estimators)
- Explain identification assumptions
- Include key equations and intuition

**Part II: Application** (from understand-domain)
- Frame a business question (e.g., "Does improving product content quality increase sales?")
- Use Online Retail Simulator to generate data with known ground truth
- Demonstrate the method with the running example
- Show what works and what fails (selection bias, etc.)
- Connect results back to theory

### Chapter-to-Lecture Mapping

| Lecture | Mixtape Chapter | Pages | Domain Example |
|---------|-----------------|-------|----------------|
| Potential Outcome Model | Ch 4: Potential Outcomes Causal Model | 119-174 | Product content optimization |
| Causal Graphical Models | Ch 3: Directed Acyclic Graphs | 67-117 | TBD |
| Matching & Propensity | Ch 5: Matching and Subclassification | 175-230 | TBD |
| Regression Discontinuity | Ch 6: Regression Discontinuity | 231-288 | TBD |
| Instrumental Variables | Ch 7: Instrumental Variables | 289-352 | TBD |
| Panel Data | Ch 8: Panel Data | 353-398 | TBD |
| Difference-in-Differences | Ch 9: Difference-in-Differences | 399-468 | TBD |
| Synthetic Control | Ch 10: Synthetic Control | 469-516 | TBD |

**Note:** Generalized Roy Model draws from external sources (Heckman & Vytlacil).

---

## Understand Domain Lectures

Different pattern—introduce tools/systems, not theory-first.

### Structure Pattern: Tool → Exploration
1. Introduce the tool/system and its purpose
2. Show configuration and usage
3. Explore generated data interactively
4. Connect to business questions that motivate later lectures

---

## Cross-References
- **Style:** Use `notebook-review.md` for markdown/code formatting
- **Code:** Use `code-review.md` for Python standards
- **Summaries:** Use `docs-review.md` for index.md lecture summaries

---

## Review Checklist

When reviewing a measure-impact lecture, verify:

**Structure**
- [ ] Reference header present with correct chapter and page numbers
- [ ] Theory section covers Mixtape chapter concepts
- [ ] Application section uses Online Retail Simulator
- [ ] Business question clearly stated

**Content Alignment**
- [ ] Theory matches the referenced Mixtape chapter
- [ ] Application demonstrates the method with simulated data
- [ ] Results connect back to theory (e.g., selection bias shown)

**Completeness**
- [ ] Key definitions and notation introduced
- [ ] Identification assumptions explained
- [ ] At least one worked example with code
- [ ] Interpretation of results discussed
