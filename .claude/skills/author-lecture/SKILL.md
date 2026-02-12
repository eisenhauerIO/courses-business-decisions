---
description: Use when authoring or structuring lecture notebooks. Provides standards for Theory→Application patterns, narrative style, chapter mappings, and lecture summaries.
---

# Lecture Authoring Guide

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

**Part II: Application** (Online Retail Simulator + Impact Engine)

1. **Business Context** — frame the recurring causal question within the business domain (consistent across the lecture sequence)
2. **Data Generation** — two-stage process:
   - **Baseline data:** config-driven simulation (`simulate()` → `load_job_results()`)
   - **Confounded treatment:** self-contained function in `support.py` that takes `metrics_df`
     and returns a product-level DataFrame with columns `D`, `Y0`, `Y1`, `Y_observed`
     (plus covariates).

   *Why not the enrichment pipeline?* The `enrich()` pipeline operates at record-level
   granularity (product × date) for metric mutation (e.g., boosting units sold). Confounded
   treatment assignment operates at product-level granularity for selection bias generation.
   These are different concerns — keeping them separate preserves function readability
   and avoids format conversion boilerplate.
3. **The Assignment Mechanism** — explain the treatment selection process and why it
   creates confounding. This section is the bridge between the business context and the
   estimation methods — it justifies every methodological choice that follows.
   - Describe the business decision: what variables drove treatment selection, and why
   - Introduce the statistical model (e.g., logistic regression) that operationalizes
     the selection process. Provide enough exposition for students to understand the
     functional form and interpret the parameters.
   - Show the `support.py` function source with `inspect.getsource()` so students see
     the selection mechanism explicitly. Selection coefficients should be exposed as
     function arguments (not hardcoded) so they are visible in the signature.
   - Connect to the identifying assumption: if assignment depends only on observed $X$,
     then conditioning on $X$ removes confounding (CIA). State this explicitly.
   - Visualize the assignment mechanism (e.g., treatment rates by covariate quintile)
     so students can see the selection pattern before encountering its consequences.
4. **Naive Comparison** — use the Impact Engine with a naive experimental estimator that ignores the treatment assignment mechanism; show the biased estimate and explain why it's wrong *as a consequence of the assignment mechanism*
5. **Apply the Method** — use the Impact Engine with the lecture's causal method to recover the true effect; include an interface-to-theory mapping table when using production tools. Explain how the method addresses the specific confounding structure created by the assignment mechanism.
6. **Validation Against Ground Truth** — leverage the simulator's full potential outcomes to verify the method works
7. **Diagnostics & Extensions** — method-specific diagnostics, limitations, or deeper exploration (e.g., balance checks, sensitivity analysis, visual comparisons)

### Narrative Style for Theory Sections

Measure Impact Theory sections require detailed, textbook-quality exposition:

**Prose Depth**
- Each concept gets thorough explanation with multiple paragraphs
- Explain the "why" behind each method, not just the "what"
- Build intuition before presenting formal definitions
- Connect new concepts to previously introduced material

**Mathematical Exposition**
- Use LaTeX equations for all mathematical notation
- Show derivations step-by-step, not just final results
- Explain each term in equations when first introduced
- Present formal definitions with precise notation

**Structure**
- Use tables to organize definitions, parameters, and comparisons
- Include worked examples where concepts benefit from concrete illustration
- Decompose complex ideas into named components (e.g., "Baseline Bias", "Differential Treatment Effect Bias")
- Use subsections to break down major concepts into digestible parts

### No Summary Sections

Lectures should focus purely on content. **Do NOT include:**
- "Conclusion" sections
- "Key Takeaways" sections
- "What's Next" sections
- "Summary" sections

Let the content speak for itself. Students absorb concepts through the theory and application—wrap-up sections add length without value.

### Chapter-to-Lecture Mapping (Measure Impact)

The measure-impact lectures each map to a specific Mixtape chapter as their primary source. Other lecture groups draw from numerous sources rather than a single textbook.

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
- **Code:** Use `/review-code` for Python standards
- **Writing:** Use `/review-writing` for prose and formatting

---

## Lecture Summary Guidelines

When writing lecture summaries in index.md files, follow this standardized pattern.

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

### Common Patterns

**Do:**
- Start with "We introduce [X] as [purpose]"
- Use "This section formalizes/explores/examines..."
- End with "The goal is to..." or "The focus is on..."
- Mention identification assumptions where relevant
- Connect to Generalized Roy framework (for Measure Impact)

**Don't:**
- List technical components without context
- Use action verbs like "implement," "build," "create"
- Write single-sentence summaries
- Focus on tools/outputs instead of concepts/understanding
- Exceed 3 sentences

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

**Data Generation**
- [ ] Confounded treatment function in `support.py` with standard output columns (`D`, `Y0`, `Y1`, `Y_observed`)
- [ ] Treatment function source shown via `inspect.getsource()`
