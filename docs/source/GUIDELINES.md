# Writing Guidelines

This document holds the conventions specific to this course. General formatting
(code elements in backticks, emphasis, numbers, links, header hierarchy and
sentence case, section headers as questions, no summary sections, active voice
and present tense) follows the Billion-Dollar Contributor `bdc-writing-mechanics`
skill, and voice follows `bdc-writing-support`. Where this file and those
skills disagree, this file wins for course material.

---

## Terminology

- Use "shoppers" (not "customers") when referring to end-users in e-commerce context.
- Link a package or tool on its first mention, e.g. `[**Online Retail Simulator**](url)`; plain text afterwards.

---

## Configuration References

### YAML Sections (Top-Level)

Use **BOLD UPPERCASE** in prose:

```markdown
Good: The **PRODUCTS** section generates...
Bad:  The products section generates...
```

### YAML Keys

Use backticks:

```markdown
Good: The `effect_size` parameter controls...
Bad:  The effect_size parameter controls...
```

### Simulation Phases vs YAML Sections

| Context | Format | Example |
|---------|--------|---------|
| Conceptual phase | **bold lowercase** | the **products** phase |
| YAML config section | **BOLD UPPERCASE** | the **PRODUCTS** section |

---

## Headers

Proper nouns of the course's methods keep their capitalization in otherwise
sentence-case headers: "Potential Outcomes Model", "Directed Acyclic Graph",
"Synthetic Control", "Bayesian", "Part I".

---

## Tone and Voice

- **Narrative prose over definition patterns**: Avoid colon-separated definition patterns ("X is Y: explanation"). Weave explanations into flowing narrative rather than glossary-style constructions. Possessive apostrophes are standard usage and not affected by this rule.
- **Separate sentences over semicolons**: Prefer two sentences over a semicolon-joined clause. Semicolons make prose feel academic rather than accessible.

---

## Additional Resources Section

Every lecture ends with an `## Additional resources` section (lowercase "r"). This is the final section of the notebook — nothing follows it.

Format: bullet points with **Author (Year)**. `[Title](url)`. *Journal*, volume(issue), pages.

---

# Measure-Impact Lecture Conventions

The conventions below apply to all lectures under `docs/source/measure-impact/`.

## Lecture Structure

Each lecture follows **Theory (Part I) → Application (Part II)**:

- **Part I** develops the statistical method from the referenced Mixtape chapter
- **Part II** applies the method using the Online Retail Simulator

## Business Context

All measure-impact lectures share the same domain:

- **Treatment**: content optimization campaign on a subset of products
- **Outcome**: revenue
- **Selection**: operates through product characteristics, creating bias in naive estimates

### Notation Table

Every Business Context section includes a notation table:

```markdown
| Variable | Notation | Description |
|----------|----------|-------------|
| ...      | ...      | ...         |
```

## The Selection Paradox Frame

- The true treatment effect is **positive** (content optimization helps)
- The naive estimate is **severely biased** (direction depends on the confounding structure)
- The method studied in the lecture recovers the positive truth
- This paradox should be explicitly stated in the Business Context or Naive Comparison section

## Assignment Mechanism

A dedicated section (or clearly labeled subsection) explains:

- **How** treatment was assigned (the selection rule)
- **Why** the naive comparison fails (what confounding it introduces)
- **Why** the lecture's method works for this specific confounding structure

This section bridges the business context and the methodology.

## Omniscient view language

- The simulator provides both potential outcomes for every unit
- This enables numerical verification of theoretical decompositions
- Use language like "the simulator gives us an omniscient view" or "we observe both potential outcomes"
- Frame this as a pedagogical advantage: "In real data, we would not have this luxury"

## Theory-to-Application Bridge

- The Part II introduction should explicitly connect to Part I concepts
- Name the specific theoretical tools being applied (e.g., "the bias decomposition from Part I", "the CIA from Section 1")

## Interface-to-Theory Mapping

Each Impact Engine method call should include a mapping table connecting YAML config fields to the Part I concepts they implement.

## Source Code Visibility

Use `inspect.getsource()` and `Code()` from `IPython.display` to show key support functions so readers can see how the data pipeline works.

## Source Alignment

- Theory matches the referenced Mixtape chapter
- Key concepts from the chapter are covered
- Notation follows the source material
- No contradictions with established methodology

## Simulation Pipeline

Part II follows a standard sequence: `!cat` the config → `simulate()` → `load_job_results()` → print a verification of what was loaded.

## Ground Truth

- Define the true effect as a named constant, `TRUE_EFFECT`, not inlined in function calls
- Compute and store the ground-truth ATT before any method comparison

## Impact Engine Calls

Lectures that use the Impact Engine import:

```python
from impact_engine_measure import measure_impact, load_results
```

Dynamic config generation adds `import yaml`. Each call follows: save the CSV → display the config → `measure_impact()` → `load_results()` → extract results.

## Support Module (`support.py`)

- Module-level docstring describing the file's purpose; imports grouped standard library / third-party / local
- `plot_` prefix for plotting functions, `print_` prefix for formatted-output functions, `_` prefix for private helpers
- Ground truth: `compute_ground_truth_att()` extracts the true ATT from potential outcomes
- Functions that draw random numbers accept a `seed` parameter (default `42`)
