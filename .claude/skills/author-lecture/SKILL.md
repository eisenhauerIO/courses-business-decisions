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

1. **Business Context** — frame the recurring causal question within the business domain (consistent across the lecture sequence). All measure-impact lectures share a consistent scenario:
   - **Domain**: E-commerce product catalog
   - **Treatment**: Content optimization (better descriptions, images, metadata)
   - **Outcome**: Revenue
   - **Selection mechanism**: Company prioritizes struggling products, creating negative selection bias
   - **The paradox**: True effect is POSITIVE, but naive estimate is NEGATIVE because treated products were already underperforming

   Include a **notation table** mapping variables to mathematical notation:

   | Variable | Notation | Description |
   |----------|----------|-------------|
   | Treatment | $D=1$ | Product receives content optimization |
   | Control | $D=0$ | Product keeps original content |
   | Outcome | $Y$ | Product revenue |

   The simulator provides both potential outcomes ("god's eye view"), enabling numerical verification of theoretical results from Part I. Frame this as a pedagogical advantage: in real data, we would not have this luxury.
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

   The simulation pipeline follows a fixed code sequence across all lectures:

   ```python
   # Cell: display config
   ! cat "config_simulation.yaml"
   ```

   ```python
   # Cell: run simulation and load results
   job_info = simulate("config_simulation.yaml")
   metrics = load_job_results(job_info)["metrics"]

   print(f"Metrics records: {len(metrics)}")
   print(f"Unique products: {metrics['product_identifier'].nunique()}")
   ```
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
   - Define `TRUE_EFFECT` as a named constant (not inlined in function calls) so it is
     visible and reusable for later comparisons.
4. **Naive Comparison** — use the Impact Engine with a naive experimental estimator that ignores the treatment assignment mechanism; show the biased estimate and explain why it's wrong *as a consequence of the assignment mechanism*
5. **Apply the Method** — use the Impact Engine with the lecture's causal method to recover the true effect; include an interface-to-theory mapping table when using production tools. Explain how the method addresses the specific confounding structure created by the assignment mechanism.
6. **Validation Against Ground Truth** — leverage the simulator's full potential outcomes to verify the method works. Compute ground truth ATT from potential outcomes before comparing with method estimates.
7. **Diagnostics & Extensions** — method-specific diagnostics, limitations, or deeper exploration (e.g., balance checks, sensitivity analysis, visual comparisons)

### Section Numbering

Both Part I and Part II use numbered `##` headings:

- Part I: `## 1. Topic`, `## 2. Topic`, etc.
- Part II: `## 1. Business Context`, `## 2. Data Generation`, etc.

Numbering restarts at 1 for Part II. The exact section titles may vary by lecture (e.g., "What Does the Naive Comparison Tell Us?" instead of "Naive Comparison"), but the functional ordering above is fixed.

### Source Code Display Convention

Before calling any `support.py` function for the first time, display its source code so students can see the implementation:

```python
Code(inspect.getsource(function_name), language="python")
```

This applies to all public functions from `support.py` — not just the confounded treatment function. Show the source, then call the function in the next cell.

### Impact Engine Pipeline (Lectures 3+)

Lectures that use the [**Impact Engine**](https://github.com/eisenhauerIO/impact-engine) follow a standard pipeline:

1. **Save data**: `data.to_csv("filename.csv", index=False)` so the YAML config can reference the file
2. **Display config**: `! cat "config_method.yaml"`
3. **Run pipeline**:
   ```python
   job = evaluate_impact("config_method.yaml", storage_url="./output/method_name")
   result = load_results(job)
   ```
4. **Extract and print results** from `result.impact_results["data"]`

When the Impact Engine config depends on runtime values (e.g., a dynamically selected treated unit), generate the config dict in Python and write it to YAML before displaying it:

```python
config = { ... }
with open("config_method.yaml", "w") as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False)
! cat "config_method.yaml"
```

### Interface-to-Theory Mapping Tables

When using the Impact Engine, include a markdown table mapping YAML `MEASUREMENT.PARAMS` fields to their Part I theoretical concepts. Place this table immediately before the config display cell. Example:

| YAML Config Field | Part I Concept |
|-------------------|----------------|
| `treatment_column` | Binary treatment indicator $D$ |
| `covariate_columns` | Conditioning set $X$ from CIA |
| `dependent_variable` | Observed outcome $Y$ |

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

### Additional Resources Section

Every lecture ends with an `## Additional resources` section (lowercase "r"). This is the final section of the notebook — nothing follows it. See `/review-writing` for the citation format standard.

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
- [ ] Simulation pipeline follows standard sequence: `!cat` config → `simulate()` → `load_job_results()` → print verification
- [ ] `inspect.getsource()` shown before first use of each `support.py` function
- [ ] `TRUE_EFFECT` defined as a named constant

**Impact Engine (Lectures 3+)**
- [ ] Data saved to CSV before Impact Engine config references it
- [ ] Interface-to-theory mapping table present before each config display
- [ ] Impact Engine pipeline follows: display config → `evaluate_impact()` → `load_results()` → extract results
- [ ] Ground truth ATT computed before method comparisons

**Narrative**
- [ ] Notation table in Business Context (Variable | Notation | Description)
- [ ] Selection paradox explicit: positive true effect, negative/biased naive estimate
- [ ] "God's eye view" framing used when introducing simulator potential outcomes
- [ ] Part II introduction references specific Part I concepts by name
