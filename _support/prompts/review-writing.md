# Writing Review

Review prose in markdown files (`.md`) and Jupyter notebook markdown cells for formatting, style, clarity, and pedagogical effectiveness.

**Exclude:** `_external/` directory.

---

# Part I: Formatting Standards

## Terminology Conventions

- Use "shoppers" (not "customers") when referring to end-users in e-commerce context
- Verify consistency across all documentation

---

## Data Columns and DataFrame Fields

**Use backticks** for column/field names:

```markdown
✅ Each product has a unique `product_identifier`, a `category`, and a `price`.
✅ The `impressions` column tracks how many times a product was shown.
❌ Each product has a unique product_identifier (missing formatting)
❌ The **impressions** column (bold alone - use backticks instead)
```

---

## Code Elements in Markdown

### Functions and Methods
Use backticks with parentheses:

```markdown
✅ `simulate()`
✅ `load_job_results()`
❌ simulate()
❌ simulate
```

### Variables and Objects
Use backticks:

```markdown
✅ The `job_info` object contains...
✅ Pass the `results` to the next function...
❌ The job_info object contains...
```

### Parameters and Arguments
Use backticks:

```markdown
✅ The `effect_size` parameter controls...
✅ Set `num_products` to 100...
❌ The effect_size parameter controls...
```

---

## File References

### Config Files
Use backticks with quotes:

```markdown
✅ `"config_simulation.yaml"`
❌ config_simulation.yaml
❌ "config_simulation.yaml"
```

### Python Modules
Use backticks:

```markdown
✅ `characteristics_rule_based.py`
✅ `online_retail_simulator`
❌ characteristics_rule_based.py
```

### Directories
Use backticks with trailing slash:

```markdown
✅ `output/`
✅ `src/simulate/`
❌ output
```

---

## Configuration Sections (YAML)

### Top-Level Sections
Use **BOLD UPPERCASE** in prose:

```markdown
✅ The **CHARACTERISTICS** section generates...
✅ The **PARAMS** subsection controls...
❌ The CHARACTERISTICS section generates...
❌ The characteristics section generates...
```

### Specific Keys
Use backticks in technical context:

```markdown
✅ The `effect_size` parameter controls...
✅ Set `enrichment_fraction` to 1.0...
❌ The effect_size parameter controls...
```

---

## Simulation Phases vs YAML Sections

### Conceptual Phases
Use **bold lowercase**:

```markdown
✅ "the **characteristics** phase"
✅ "the **product_details** phase"
❌ "the characteristics phase" (not bold)
❌ "the CHARACTERISTICS phase" (wrong case)
```

### YAML Configuration Sections
Use **bold uppercase**:

```markdown
✅ "The **CHARACTERISTICS** section in the YAML config..."
❌ "The characteristics section in the YAML..." (lowercase)
```

**Rule:** Phase names (concepts) = lowercase bold. YAML sections = uppercase bold.

---

## Object Types and Return Values

Use backticks for types:

```markdown
✅ Returns a `JobInfo` object
✅ Returns a `DataFrame`
❌ Returns a JobInfo object
```

---

## Emphasis and Highlighting

### Bold for Concepts
Use on first introduction:

```markdown
✅ The **conversion funnel** tracks customer behavior. The conversion funnel includes...
❌ The conversion funnel tracks... (not bold on first use)
```

### Italics for Subtle Emphasis
Use sparingly for meta-comments:

```markdown
✅ Describe *what* you want in natural language
✅ The goal is not perfectly polished code—it's *rapid insight generation*
```

### Questions as Headers
Format important questions in bold:

```markdown
✅ **Does improving product content quality increase sales?**
✅ How do customers move through the purchase journey?
```

---

## Numbers and Values

### Inline Numbers
Plain text for readability:

```markdown
✅ Simulate 100 products
✅ A 50% increase
❌ Simulate `100` products (over-formatted)
```

### Parameter Values
Use code formatting:

```markdown
✅ Set `effect_size: 0.5`
✅ The default `num_products: 100`
❌ Set effect_size: 0.5 (not formatted)
```

---

## Links and References

### External Links
Format package/tool names with link on first mention:

```markdown
✅ The [**Online Retail Simulator**](https://github.com/eisenhauerIO/tools-catalog-generator)
✅ We use [GitHub Copilot](https://github.com/features/copilot) to generate code.
```

### Subsequent Mentions
Use plain bold or plain text:

```markdown
✅ The **Online Retail Simulator** generates...
✅ The simulator generates...
❌ The [Online Retail Simulator] generates... (over-linked)
```

---

## Lists and Examples

### Parenthetical Examples
Use em-dash for inline examples:

```markdown
✅ `**category**` (such as Electronics, Clothing, or Books)
✅ Brand names get premium suffixes ("Elite", "Pro")
❌ **category** like Electronics, Clothing, or Books
```

### Code Example Values
Use quotes for strings:

```markdown
✅ `"2024-11-01"`
✅ `seed: 42`
❌ 2024-11-01 (not quoted)
```

---

## Headers and Structure

### Header Hierarchy
```markdown
# Main Title (once per notebook - the lecture title only)
## Major Section
### Subsection
#### Rare: only for deeply nested content
```

**Important:** Each lecture notebook should have exactly ONE `#` heading - the lecture title. All other sections should use `##` or lower. This ensures proper document structure and navigation.

### Section Headers Should Be Questions (When Appropriate)
```markdown
✅ ## Exploring the Generated Data
✅ ### How is revenue distributed across categories?
❌ ### Revenue Distribution (less engaging)
```

### No Formulaic Summary Sections

Do **not** add structured summary sections at the end of lectures. Avoid:
- "Summary" with bullet points recapping the lecture
- "Key Concepts" or "Key Takeaways" lists
- "Practical Implications" sections
- "Looking Ahead" or "Next Steps" sections

Lectures should end naturally with the final content. Let the material speak for itself.

---

## Tone and Voice

### Active Voice
```markdown
✅ The simulator generates a product catalog
❌ A product catalog is generated by the simulator
```

### Present Tense
```markdown
✅ The function writes the DataFrames to disk
❌ The function will write the DataFrames to disk
```

### Instructional but Not Condescending
```markdown
✅ Let's start by simulating 100 products
❌ Now we're going to simulate some products (too casual)
❌ It is necessary to simulate products (too formal)
```

---

## Quick Reference

| Element | Format | Example |
|---------|--------|---------|
| Column name | `` `name` `` | `product_identifier` |
| Function | `` `function()` `` | `simulate()` |
| Variable | `` `variable` `` | `job_info` |
| Parameter | `` `parameter` `` | `effect_size` |
| Config file | `` `"file.yaml"` `` | `"config_simulation.yaml"` |
| Phase (concept) | **phase** | **characteristics** |
| YAML section | **SECTION** | **CHARACTERISTICS** |
| Object type | `` `Type` `` | `DataFrame` |
| Directory | `` `dir/` `` | `output/` |

---

# Part II: Pedagogical Clarity

## Content Accuracy

### Technical Correctness
- [ ] Definitions and notation are mathematically correct
- [ ] Equations and derivations are accurate
- [ ] Statistical concepts are properly explained
- [ ] Data/statistics cited are accurate and sourced

### Source Alignment
For Measure Impact lectures:
- [ ] Theory matches the referenced Mixtape chapter
- [ ] Key concepts from the chapter are covered
- [ ] Notation follows the source material
- [ ] No contradictions with established methodology

---

## Structure and Flow

### Logical Progression
- [ ] Concepts build on each other in a sensible order
- [ ] Prerequisites are introduced before they're needed
- [ ] Transitions between sections are clear
- [ ] The narrative has a clear beginning, middle, and end

### Section Balance
- [ ] Theory and application sections are appropriately balanced
- [ ] No section is disproportionately long or short
- [ ] Complex topics get adequate depth
- [ ] Simple topics aren't over-explained

---

## Examples and Applications

### Worked Examples
- [ ] At least one complete worked example with code
- [ ] Example is realistic and relatable
- [ ] Steps are explained, not just shown
- [ ] Results are interpreted, not just displayed

### Business Context (for applied lectures)
- [ ] Business question is clearly stated
- [ ] Data generation connects to the business scenario
- [ ] Results answer the business question
- [ ] Limitations and caveats are discussed

---

## Engagement and Clarity

### Accessibility
- [ ] Technical jargon is explained on first use
- [ ] Assumes appropriate (not excessive) prior knowledge
- [ ] Difficult concepts have intuitive explanations
- [ ] Analogies or visual aids are used where helpful

### Active Learning
- [ ] Headers pose questions where appropriate
- [ ] Students can run code and see results
- [ ] Opportunities for exploration or modification exist

---

## Completeness

### No Missing Pieces
- [ ] All referenced concepts are defined
- [ ] No "TODO" or placeholder content in final version
- [ ] All code cells are complete and runnable
- [ ] Figures and tables are labeled and explained

### Appropriate Scope
- [ ] Covers the topic adequately for the course level
- [ ] Doesn't try to cover too much in one lecture
- [ ] Points to additional resources for deeper exploration

---

# Part III: Checklists

## Formatting Checklist

- [ ] All column names use `` `column_name` `` format
- [ ] All functions use `` `function_name()` `` format
- [ ] All file references use `` `"filename.ext"` `` format
- [ ] Phase names are lowercase bold (**characteristics**)
- [ ] YAML sections are uppercase bold (**CHARACTERISTICS**)
- [ ] Object types use backticks (`` `DataFrame` ``, `` `JobInfo` ``)
- [ ] First introduction of concepts uses **bold**
- [ ] Links use meaningful text, not "click here"
- [ ] Headers are questions when exploring data
- [ ] Active voice, present tense throughout
- [ ] Uses "shoppers" not "customers" for e-commerce end-users

## Pedagogy Checklist

- [ ] Concepts build logically
- [ ] Technical jargon is explained
- [ ] Examples are realistic and explained
- [ ] Results are interpreted, not just shown
- [ ] No placeholder or TODO content

---

## Review Questions

When reviewing, ask yourself:

1. **Would a student understand this?** Not just follow along, but actually grasp the concept.

2. **Is the "why" explained?** Not just what the method does, but why it works and when to use it.

3. **Are assumptions made explicit?** Students should know what conditions must hold.

4. **Is the business relevance clear?** For applied lectures, the connection to decisions should be obvious.

5. **What would confuse someone?** Identify potential stumbling blocks before students hit them.

---

## Verification

After making changes, always run:

```bash
git status
hatch run ruff format .
hatch run ruff check .
hatch run build
```

This checks for untracked files, formats code, checks for linting issues, builds the documentation and executes all notebooks, confirming that changes don't break anything.

**Success criteria:**
- [ ] All new files are under version control (`git status` shows no untracked files that should be committed)
- [ ] `hatch run ruff format .` completes without changes
- [ ] `hatch run ruff check .` passes with no errors
- [ ] `hatch run build` completes successfully

---

## Output Format

For each issue found:
1. **Location**: File and line/section reference
2. **Issue**: What's wrong
3. **Suggestion**: How to fix it
