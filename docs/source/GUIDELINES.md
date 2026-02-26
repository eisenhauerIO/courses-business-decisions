# Writing Guidelines

This document defines the formatting, style, and structural conventions for all course documentation. Both human authors and automated reviewers should use this as the single source of truth.

---

## Inline Formatting

### Code Elements

| Element | Format | Example |
|---------|--------|---------|
| Column name | `` `name` `` | `product_identifier` |
| Function | `` `function()` `` | `simulate()` |
| Variable | `` `variable` `` | `job_info` |
| Parameter | `` `parameter` `` | `effect_size` |
| Config file | `` `"file.yaml"` `` | `"config_simulation.yaml"` |
| Object type | `` `Type` `` | `DataFrame` |
| Directory | `` `dir/` `` | `output/` |
| Python module | `` `module` `` | `online_retail_simulator` |

### Emphasis

- **Bold** for concepts on first introduction. Plain text on subsequent mentions.
- *Italics* sparingly, for meta-comments or subtle emphasis.
- Important questions in **bold**.

### Numbers and Values

- Inline numbers in plain text: "Simulate 100 products"
- Parameter values in code formatting: "Set `effect_size: 0.5`"
- String values in backtick-quotes: `"2024-11-01"`

### Links

- Link package/tool names on first mention: `[**Online Retail Simulator**](url)`
- Subsequent mentions: plain bold or plain text. Do not re-link.

---

## Terminology

- Use "shoppers" (not "customers") when referring to end-users in e-commerce context.

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

## Headers and Structure

### Hierarchy

```markdown
# Main Title (once per document)
## Major Section
### Subsection
#### Rare: only for deeply nested content
```

### Headers as Questions

Use question-form headers when exploring data or posing analytical questions:

```markdown
Good: ### How is revenue distributed across categories?
Bad:  ### Revenue Distribution
```

### No Formulaic Summary Sections

Do **not** add structured summary sections at the end of documents. Avoid "Summary", "Key Concepts", "Key Takeaways", "Practical Implications", or "Looking Ahead" sections. Let the material speak for itself.

---

## Tone and Voice

- **Active voice**: "The simulator generates a product catalog" (not passive)
- **Present tense**: "The function writes the DataFrames to disk" (not future)
- **Instructional but not condescending**: "Let's start by simulating 100 products" (not too casual, not too formal)

---

## Additional Resources Section

Every lecture ends with an `## Additional resources` section (lowercase "r"). This is the final section of the notebook — nothing follows it.

Format: bullet points with **Author (Year)**. [Title](url). *Journal*, volume(issue), pages.

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
- **Selection**: operates through product characteristics, creating negative bias

### Notation Table

Every Business Context section includes a notation table:

```markdown
| Variable | Notation | Description |
|----------|----------|-------------|
| ...      | ...      | ...         |
```

## The Selection Paradox Frame

- The true treatment effect is **positive** (content optimization helps)
- The naive estimate is **negative** (or severely biased)
- The method studied in the lecture recovers the positive truth
- This paradox should be explicitly stated in the Business Context or Naive Comparison section

## Assignment Mechanism

A dedicated section (or clearly labeled subsection) explains:

- **How** treatment was assigned (the selection rule)
- **Why** the naive comparison fails (what confounding it introduces)
- **Why** the lecture's method works for this specific confounding structure

This section bridges the business context and the methodology.

## "God's Eye View" Language

- The simulator provides both potential outcomes for every unit
- Use language like "the simulator gives us a god's eye view" or "we observe both potential outcomes"
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
