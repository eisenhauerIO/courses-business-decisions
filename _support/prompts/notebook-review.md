# Notebook Review Guide: Business Decisions Course

## Purpose
This guide defines quality standards for Jupyter notebooks in the Business Decisions course. The goal is **pedagogical clarity**—notebooks should teach effectively through clear code, consistent formatting, and thoughtful structure.

This guide covers both **Python code cells** and **markdown cells**.

---

# Part I: Markdown Cell Standards

## 1. Data Columns and DataFrame Fields

**Use bold code formatting** for column/field names:

```markdown
✅ Each product has a unique `**product_identifier**`, a `**category**`, and a `**price**`.
✅ The `**impressions**` column tracks how many times a product was shown.
❌ Each product has a unique product_identifier (missing formatting)
❌ The **impressions** column (acceptable but less precise)
```

**Why:** Visually distinguishes data fields from regular text.

---

## 2. Code Elements in Markdown

### Functions and Methods
Use backticks with parentheses:

```markdown
✅ `simulate()`
✅ `load_job_results()`
✅ `simulate_characteristics_rule_based()`
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

## 3. File References

### Config Files
Use backticks with quotes:

```markdown
✅ `"config_simulation.yaml"`
✅ `"config_enrichment_mock.yaml"`
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

## 4. Configuration Sections (YAML)

### Top-Level Sections
Use **BOLD UPPERCASE** in prose:

```markdown
✅ The **CHARACTERISTICS** section generates...
✅ The **PARAMS** subsection controls...
✅ The **PRODUCT_DETAILS** section enriches...
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

## 5. Simulation Phases vs YAML Sections

### Conceptual Phases
Use **bold lowercase**:

```markdown
✅ "the **characteristics** phase"
✅ "the **product_details** phase"
✅ "the **metrics** phase"
❌ "the characteristics phase" (not bold)
❌ "the CHARACTERISTICS phase" (wrong case)
```

### YAML Configuration Sections
Use **bold uppercase**:

```markdown
✅ "The **CHARACTERISTICS** section in the YAML config..."
✅ "Configure the **METRICS** section..."
❌ "The characteristics section in the YAML..." (lowercase)
```

**Rule:** Phase names (concepts) = lowercase bold. YAML sections = uppercase bold.

---

## 6. Object Types and Return Values

Use backticks for types:

```markdown
✅ Returns a `JobInfo` object
✅ Returns a `DataFrame`
✅ The `Series` contains...
❌ Returns a JobInfo object
❌ Returns a DataFrame
```

---

## 7. Emphasis and Highlighting

### Bold for Concepts
Use on first introduction:

```markdown
✅ The **conversion funnel** tracks customer behavior. The conversion funnel includes...
✅ We use **vibe coding** to explore data.
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
❌ Does improving product content quality increase sales? (questions can be plain if not major focus)
```

---

## 8. Technical Accuracy

### Data Provenance
Be precise about which phase generates what:

```markdown
✅ Each product starts with core **characteristics** (identifier, category, brand, price)
   which are enriched with **product_details** (title, description, features).

❌ Each product has a category, brand, and price.
   (Doesn't clarify that brand is from characteristics, not product_details)
```

### Field Attribution
**Characteristics phase generates:**
- `**product_identifier**`
- `**category**`
- `**brand**`
- `**price**`

**Product_details phase generates:**
- `**title**`
- `**description**`
- `**features**`

**Metrics phase generates:**
- `**date**`
- `**impressions**`
- `**visits**`
- `**cart_adds**`
- `**ordered_units**`
- `**revenue**`

---

## 9. Numbers and Values

### Inline Numbers
Plain text for readability:

```markdown
✅ Simulate 100 products
✅ A 50% increase
✅ (0.5 = 50% increase)
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

## 10. Links and References

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

### Code References
Link to GitHub source:

```markdown
✅ Browse the source on GitHub ([characteristics](https://github.com/.../characteristics_rule_based.py))
✅ See the API docs ([simulate](https://docs.../simulate.html))
```

---

## 11. Lists and Examples

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
✅ `enrichment_start: "2024-11-15"`
❌ 2024-11-01 (not quoted)
```

---

## 12. Headers and Structure

### Header Hierarchy
```markdown
# Main Title (once per notebook)
## Major Section
### Subsection
#### Rare: only for deeply nested content
```

### Section Headers Should Be Questions (When Appropriate)
```markdown
✅ ## Exploring the Generated Data
✅ ### How is revenue distributed across categories?
✅ ### How do customers move through the purchase journey?

❌ ### Revenue Distribution (less engaging)
❌ ### Customer Journey Analysis (less engaging)
```

**Why:** Questions engage students and frame the analysis purpose.

---

## 13. Tone and Voice

### Active Voice
```markdown
✅ The simulator generates a product catalog
✅ You can explore the source code directly
❌ A product catalog is generated by the simulator
❌ The source code can be explored directly
```

### Present Tense
```markdown
✅ The function writes the DataFrames to disk
✅ The enrichment layer allows you to inject known treatment effects
❌ The function will write the DataFrames to disk
❌ The enrichment layer allowed you to inject effects
```

### Instructional but Not Condescending
```markdown
✅ Let's start by simulating 100 products
✅ The configuration drives a three-phase simulation
❌ Now we're going to simulate some products (too casual)
❌ It is necessary to simulate products (too formal)
```

---

## 14. Common Markdown Patterns

### Introducing Data Output
```markdown
The **[concept]** data [description]. Each record tracks `**column1**`,
`**column2**`, and `**column3**`. This structure [explanation].
```

**Example:**
```markdown
The sales data captures the full customer journey as a conversion funnel.
Each record tracks `**impressions**`, `**visits**`, `**cart_adds**`, and
`**ordered_units**`. This funnel structure reflects real e-commerce behavior
where customers drop off at each stage.
```

### Describing Functions
```markdown
Calling `function_name("config.yaml")` triggers [what it does]. First, it
[step 1], then [step 2]. The function returns a `ObjectType` that [purpose].
```

**Example:**
```markdown
Calling `simulate("config_simulation.yaml")` triggers a three-phase data
generation process. First, it reads and validates the YAML configuration,
then runs the **characteristics** phase to create a product catalog. The
function returns a `JobInfo` object that tracks where results are stored.
```

### Explaining Configuration Sections
```markdown
The **SECTION_NAME** section [purpose]. The `parameter_name` controls
[what it does], and `other_parameter` sets [what it does].
```

**Example:**
```markdown
The **ENRICHMENT** section controls the treatment parameters. The
`effect_size` controls the magnitude of the boost (0.5 = 50% increase),
and `enrichment_fraction` determines what share of products receive
treatment (1.0 = 100%).
```

---

## 15. Markdown Quick Reference

| Element | Format | Example |
|---------|--------|---------|
| Column name | `**name**` | `**product_identifier**` |
| Function | `` `function()` `` | `simulate()` |
| Variable | `` `variable` `` | `job_info` |
| Parameter | `` `parameter` `` | `effect_size` |
| Config file | `` `"file.yaml"` `` | `"config_simulation.yaml"` |
| Phase (concept) | **phase** | **characteristics** |
| YAML section | **SECTION** | **CHARACTERISTICS** |
| Object type | `` `Type` `` | `DataFrame` |
| Directory | `` `dir/` `` | `output/` |

---

# Part II: Python Code Cell Standards

## 16. Code Cell Organization

### Imports
**Structure:**
```python
# Standard Library
import inspect
from pathlib import Path

# Third-party packages
from IPython.display import Code
import pandas as pd
import numpy as np

# Local imports
from online_retail_simulator import simulate, load_job_results
from support import plot_revenue_by_category
```

**Rules:**
- ✅ Group imports by category with comments
- ✅ One import per line for readability
- ✅ Alphabetize within groups
- ❌ Never use `import *`
- ❌ Don't mix standard library and third-party

### One Logical Operation Per Cell
**Good:**
```python
# Cell 1: Run simulation
job_info = simulate("config_simulation.yaml")
```

```python
# Cell 2: Load results
results = load_job_results(job_info)
products = results["products"]
sales = results["sales"]
```

**Bad:**
```python
# Everything crammed together
job_info = simulate("config_simulation.yaml")
results = load_job_results(job_info)
products = results["products"]
sales = results["sales"]
product_count = len(products)
print(f"Loaded {product_count} products")
# ... more unrelated operations
```

**Why:** Students can execute and understand each step independently.

---

## 17. Variable Naming

### Use Descriptive Names
**Good:**
```python
daily_sales = sales.groupby("date").agg({"ordered_units": "sum"})
category_revenue = sales.groupby("category")["revenue"].sum()
enriched_products = products[products["enriched"] == True]
```

**Bad:**
```python
ds = sales.groupby("date").agg({"ordered_units": "sum"})  # Too terse
cr = sales.groupby("category")["revenue"].sum()
ep = products[products["enriched"] == True]
```

### DataFrame Naming Convention
- Raw data: `products`, `sales`, `customers`
- Aggregated: `daily_sales`, `category_revenue`, `product_summary`
- Filtered: `enriched_products`, `high_value_customers`
- Temporary: Use descriptive names, not `df`, `temp`, `data`

### Avoid Reusing Variable Names
**Bad:**
```python
products = results["products"]
# ... later ...
products = products[products["price"] > 100]  # Overwrites original
```

**Good:**
```python
products = results["products"]
# ... later ...
high_price_products = products[products["price"] > 100]
```

---

## 18. Comments and Documentation

### When to Comment
**Comment the WHY, not the WHAT:**

**Good:**
```python
# Set seed for reproducible random product selection
random.seed(42)

# Convert to datetime to enable time-based filtering
daily_sales["date"] = pd.to_datetime(daily_sales["date"])
```

**Bad:**
```python
# Set random seed to 42
random.seed(42)

# Convert date column to datetime
daily_sales["date"] = pd.to_datetime(daily_sales["date"])
```

### Docstrings for Helper Functions
```python
def calculate_conversion_rate(visits, orders):
    """
    Calculate conversion rate from visits to orders.

    Parameters
    ----------
    visits : int
        Number of product visits
    orders : int
        Number of completed orders

    Returns
    -------
    float
        Conversion rate as percentage (0-100)
    """
    if visits == 0:
        return 0.0
    return (orders / visits) * 100
```

### Cell-Level Comments
Use for complex cells:
```python
"""
Create conversion funnel aggregation.

This cell calculates total impressions, visits, cart adds, and orders
across all products to visualize the customer journey.
"""
funnel_data = {
    "Impressions": sales["impressions"].sum(),
    "Visits": sales["visits"].sum(),
    "Cart Adds": sales["cart_adds"].sum(),
    "Orders": sales["ordered_units"].sum(),
}
```

---

## 19. Print Statements and Output

### Formatted Output for Pedagogy
**Good:**
```python
print("=" * 40)
print("DATA SUMMARY")
print("=" * 40)
print(f"Date range:      {sales['date'].min()} to {sales['date'].max()}")
print(f"Categories:      {sales['category'].nunique()}")
print(f"Total revenue:   ${sales['revenue'].sum():,.2f}")
print("=" * 40)
```

**Output:**
```
========================================
DATA SUMMARY
========================================
Date range:      2024-11-01 to 2024-11-30
Categories:      8
Total revenue:   $125,165.32
========================================
```

**Bad:**
```python
print("Date range:", sales['date'].min(), "to", sales['date'].max())
print("Categories:", sales['category'].nunique())
print("Total revenue:", sales['revenue'].sum())
```

### Use f-strings
- ✅ `f"Revenue: ${revenue:,.2f}"`
- ❌ `"Revenue: $" + str(revenue)`
- ❌ `"Revenue: ${}".format(revenue)`

---

## 20. Data Operations

### Chain Operations Thoughtfully
**Good (readable chain):**
```python
top_products = (
    sales
    .groupby("product_identifier")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
```

**Bad (too long):**
```python
result = sales.groupby("product_identifier")["revenue"].sum().sort_values(ascending=False).head(10).reset_index().merge(products, on="product_identifier").sort_values("revenue")
```

**Fix:** Break into multiple cells or steps:
```python
# Aggregate revenue by product
product_revenue = sales.groupby("product_identifier")["revenue"].sum()

# Get top 10 products
top_products = product_revenue.sort_values(ascending=False).head(10)

# Add product details
top_products_with_details = top_products.reset_index().merge(
    products, on="product_identifier"
)
```

### Explicit Column Selection
**Good:**
```python
product_cols = ["product_identifier", "category", "price"]
sample_product = products[product_cols].head(1)
```

**Bad:**
```python
sample_product = products.head(1)  # What columns are we using?
```

---

## 21. Magic Commands and Shell Commands

### Use Sparingly and Explain
**Good:**
```python
# Display the YAML configuration file
! cat "config_simulation.yaml"
```

**Bad:**
```python
! cat "config_simulation.yaml"  # No context
```

### Avoid Inline Shell Commands
**Bad:**
```python
files = ! ls output/
```

**Good:**
```python
from pathlib import Path
output_files = list(Path("output").glob("*"))
```

---

## 22. Visualization Code

### Separate Data Prep from Plotting
**Good:**
```python
# Prepare data for plotting
category_revenue = sales.groupby("category")["revenue"].sum().sort_values()
```

```python
# Visualize revenue by category
plot_revenue_by_category(category_revenue)
```

**Bad:**
```python
# Everything together
plot_revenue_by_category(
    sales.groupby("category")["revenue"].sum().sort_values()
)
```

### Keep Plot Config in Helper Functions
**Move to support.py:**
```python
def plot_revenue_by_category(category_revenue):
    """Plot horizontal bar chart of revenue by category."""
    fig, ax = plt.subplots(figsize=(10, 6))
    category_revenue.plot(
        kind="barh",
        ax=ax,
        color=sns.color_palette("viridis", len(category_revenue))
    )
    ax.set_xlabel("Revenue ($)")
    ax.set_ylabel("Category")
    ax.set_title("Total Revenue by Category")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    plt.tight_layout()
    plt.show()
```

**Why:** Keeps notebook focused on analysis, not plot styling.

---

## 23. Error Handling

### In Notebooks: Fail Loudly
**Good:**
```python
# Let pandas raise KeyError if column doesn't exist
revenue_total = sales["revenue"].sum()
```

**Bad:**
```python
try:
    revenue_total = sales["revenue"].sum()
except KeyError:
    revenue_total = 0  # Silent failure confuses students
```

**Exception:** Use try/except when demonstrating error handling pedagogically:
```python
# Demonstrating validation
try:
    config = yaml.safe_load(config_file)
except yaml.YAMLError as e:
    print(f"Configuration error: {e}")
    raise
```

---

## 24. Code Complexity

### Maximum Lines Per Cell
- **Analysis cells:** 5-10 lines
- **Data preparation:** 10-15 lines
- **Complex operations:** 15-20 lines (break into helper function if longer)

### Cyclomatic Complexity
- Avoid nested if/for statements in notebook cells
- Move complex logic to functions in `support.py`

**Bad:**
```python
for product in products:
    if product["category"] == "Electronics":
        if product["price"] > 100:
            for sale in sales:
                if sale["product_id"] == product["id"]:
                    # ... complex logic
```

**Good:**
```python
# In support.py
def filter_high_value_electronics(products, sales, min_price=100):
    """Filter electronics products above price threshold with sales data."""
    # Complex logic here
    return filtered_results

# In notebook
high_value_products = filter_high_value_electronics(products, sales)
```

---

## 25. Reproducibility

### Always Set Seeds
```python
# For random operations
import random
random.seed(42)

# For numpy
import numpy as np
np.random.seed(42)

# For pandas sampling
sample = df.sample(n=100, random_state=42)
```

### Document Dependencies
Include a cell showing versions:
```python
# Optional: Show package versions for reproducibility
import pandas as pd
import numpy as np
print(f"pandas: {pd.__version__}")
print(f"numpy: {np.__version__}")
```

---

## 26. Code Reuse and DRY Principle

### When to Create a Function
**Repeated more than twice → function:**

**Bad:**
```python
# Cell 1
print("=" * 40)
print("CATEGORY ANALYSIS")
print("=" * 40)

# Cell 5
print("=" * 40)
print("TIME SERIES ANALYSIS")
print("=" * 40)

# Cell 8
print("=" * 40)
print("CONVERSION ANALYSIS")
print("=" * 40)
```

**Good:**
```python
# In support.py
def print_section_header(title):
    """Print formatted section header."""
    print("=" * 40)
    print(title)
    print("=" * 40)

# In notebook
print_section_header("CATEGORY ANALYSIS")
# ... analysis ...
print_section_header("TIME SERIES ANALYSIS")
# ... analysis ...
```

---

## 27. Anti-Patterns to Avoid

### ❌ Mutation Without Clarity
```python
# Bad: Modifying original DataFrame
sales["new_column"] = sales["revenue"] * 1.1

# Good: Make intent clear
sales = sales.copy()  # If mutation intended
# OR
sales_with_adjustment = sales.assign(new_column=lambda x: x["revenue"] * 1.1)
```

### ❌ Hardcoded Values
```python
# Bad
high_price = products[products["price"] > 500]

# Good
PRICE_THRESHOLD = 500  # Define at top of cell or notebook
high_price = products[products["price"] > PRICE_THRESHOLD]
```

### ❌ Unused Variables
```python
# Bad
results = load_job_results(job_info)
products = results["products"]
sales = results["sales"]
metadata = results["metadata"]  # Never used
```

### ❌ Print Debugging Left In
```python
# Bad
print("DEBUG: products shape:", products.shape)  # Remove before committing
revenue = calculate_revenue(products)
print("DEBUG: revenue calculated")  # Remove before committing
```

---

## 28. Notebook-Specific Best Practices

### Cell Execution Order
- Cells should be executable top-to-bottom in sequence
- No "skip this cell" or "run cell 5 before cell 3" instructions
- Use `%reset` to test fresh execution if needed

### State Management
```python
# Good: Clear state at section boundaries
del intermediate_results  # Explicitly clean up

# OR restart kernel and run all cells before finalizing
```

### Display Settings
```python
# Set pandas display options at notebook start
pd.set_option('display.max_columns', None)
pd.set_option('display.precision', 2)
pd.set_option('display.max_rows', 100)
```

---

# Part III: Examples and Checklists

## 29. Example: Good vs Bad Markdown Cell

### ❌ Bad Markdown Cell
```markdown
The products dataframe has columns like product_identifier, category, and
price. It also has brand, title, description, and features. You can use
the simulate function to generate this data. The config file config_simulation.yaml
controls how many products are created.
```

**Problems:**
- No formatting for column names
- Doesn't distinguish characteristics from product_details
- Function name not formatted
- Config file not formatted
- Passive voice ("are created")

### ✅ Good Markdown Cell
```markdown
The products data represents the catalog of items available for sale. Each
product starts with core **characteristics**—a unique `**product_identifier**`,
`**category**`, `**brand**`, and `**price**`—which are then enriched with
**product_details** including `**title**`, `**description**`, and `**features**`.

Calling `simulate("config_simulation.yaml")` generates this data. The
**CHARACTERISTICS** section in the YAML config controls how many products
to create via the `num_products` parameter.
```

**Why Better:**
- Column names properly formatted
- Clear phase separation
- Function name formatted
- Config file formatted
- YAML sections properly referenced
- Active voice
- Clear structure

---

## 30. Example: Good vs Bad Code Cell

### ❌ Bad Cell
```python
# Cell: Analysis
df = pd.read_csv("data.csv")
df["date"] = pd.to_datetime(df["date"])
result = df.groupby("category")["revenue"].sum()
result = result.sort_values(ascending=False)
top = result.head(10)
print(top)
for i, v in top.items():
    print(f"{i}: ${v}")
```

### ✅ Good Cell
```python
"""
Aggregate revenue by category.

Calculates total revenue for each product category and identifies
the top 10 revenue-generating categories.
"""
# Aggregate revenue across all products by category
category_revenue = sales.groupby("category")["revenue"].sum()

# Sort to find highest revenue categories
top_categories = category_revenue.sort_values(ascending=False).head(10)

# Display results
print("=" * 50)
print("TOP 10 CATEGORIES BY REVENUE")
print("=" * 50)
for category, revenue in top_categories.items():
    print(f"{category:<20} ${revenue:>12,.2f}")
print("=" * 50)
```

---

## 31. Markdown Checklist

Before finalizing markdown cells:

- [ ] All column names use `**column_name**` format
- [ ] All functions use `function_name()` format
- [ ] All file references use `"filename.ext"` format
- [ ] Phase names are lowercase bold (**characteristics**)
- [ ] YAML sections are uppercase bold (**CHARACTERISTICS**)
- [ ] Object types use backticks (`DataFrame`, `JobInfo`)
- [ ] First introduction of concepts uses **bold**
- [ ] Brand is listed as a **characteristic**, not product detail
- [ ] Title, description, features are **product_details**
- [ ] Links use meaningful text, not "click here"
- [ ] Headers are questions when exploring data
- [ ] Active voice, present tense throughout

---

## 32. Code Checklist

Before finalizing code cells:

- [ ] Imports organized and grouped by category
- [ ] One logical operation per cell
- [ ] Variable names are descriptive
- [ ] Comments explain WHY, not WHAT
- [ ] Print output is formatted for readability
- [ ] No hardcoded magic numbers
- [ ] Seeds set for reproducibility
- [ ] No unused variables or imports
- [ ] Complex logic moved to helper functions
- [ ] Cells executable in top-to-bottom order
- [ ] No debug print statements left in
- [ ] Visualization code separated from data prep
- [ ] DataFrame operations are clear and explicit

---

## Additional Resources

- [PEP 8](https://peps.python.org/pep-0008/) - Python style guide
- [Pandas best practices](https://pandas.pydata.org/docs/user_guide/style.ipynb)
- [Jupyter notebook best practices](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Working%20With%20Markdown%20Cells.html)

---

## Revision History

- 2026-01-11: Initial version created (merged from code and markdown style guides)
