---
name: review-code
description: Use when reviewing Python code in *.py files and Jupyter notebook code cells. Checks for bugs, clarity, style, performance, security, and docstrings.
---

# Code Review

Review Python code in `*.py` files and Jupyter notebook code cells for quality and correctness.

**Exclude:** `_external/` directory.

---

## Automated Checks

Run these first to catch mechanical issues:

```bash
pre-commit run --all-files   # Formatting, linting, hooks
ruff check .                 # Python linting
```

Report any failures in your review. These are **[BLOCKING]** issues.

---

## Check For

- **Bugs**: Logic errors, off-by-one, null/None handling, edge cases
- **Clarity**: Unclear variable names, overly complex logic, missing context
- **Style**: Inconsistent formatting, dead code, unused imports, imports not at top of module, premature line breaks (use 120 char limit)
- **Performance**: Unnecessary loops, repeated computations, inefficient patterns
- **Security**: Hardcoded secrets, injection risks, unsafe operations
- **Docstrings**: Missing or incomplete NumPy-style docstrings

---

## Import Organization

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
from mypackage import helpers
```

**Rules:**
- Group imports by category with comments
- Alphabetize within groups
- Single import: no parentheses (keep on one line)
- Multiple imports: use parentheses with one per line
- Never use `import *`

**Single Import:**
```python
# Good
from mypackage.submodule import some_function

# Bad - unnecessary parentheses
from mypackage.submodule import (
    some_function,
)
```

**Multiple Imports:**
```python
# Good
from support import (
    helper_one,
    helper_two,
    helper_three,
)

# Bad - too long, hard to read
from support import helper_one, helper_two, helper_three
```

---

## NumPy Docstring Requirements

### Module Level
Every Python file should have a module-level docstring explaining its purpose.

### Functions
All public functions must have docstrings with these sections (as applicable):

```python
def function_name(param1, param2):
    """
    Short one-line summary.

    Longer description if needed.

    Parameters
    ----------
    param1 : type
        Description of param1.
    param2 : type, optional
        Description of param2. Default is X.

    Returns
    -------
    type
        Description of return value.

    Raises
    ------
    ExceptionType
        When and why this exception is raised.
    """
```

### Classes
All classes must have docstrings with Parameters and Attributes sections.

### Style Notes
- Use imperative mood ("Calculate X" not "Calculates X")
- Keep summary line under 79 characters
- Use `optional` for parameters with defaults

---

## Variable Naming

### Use Descriptive Names
```python
# Good
daily_sales = sales.groupby("date").agg({"ordered_units": "sum"})
category_revenue = sales.groupby("category")["revenue"].sum()

# Bad
ds = sales.groupby("date").agg({"ordered_units": "sum"})
cr = sales.groupby("category")["revenue"].sum()
```

### DataFrame Naming Convention
- Raw data: `products`, `sales`, `customers`
- Aggregated: `daily_sales`, `category_revenue`, `product_summary`
- Filtered: `enriched_products`, `high_value_customers`
- Temporary: Use descriptive names, not `df`, `temp`, `data`

### Avoid Reusing Variable Names
```python
# Bad
products = results["products"]
products = products[products["price"] > 100]  # Overwrites original

# Good
products = results["products"]
high_price_products = products[products["price"] > 100]
```

---

## Comments and Documentation

### Comment the WHY, not the WHAT

```python
# Good
# Set seed for reproducible random product selection
random.seed(42)

# Bad
# Set random seed to 42
random.seed(42)
```

---

## Data Operations

### Chain Operations Thoughtfully
```python
# Good (readable chain)
top_products = (
    sales
    .groupby("product_identifier")["revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Bad (too long)
result = sales.groupby("product_identifier")["revenue"].sum().sort_values(ascending=False).head(10).reset_index().merge(products, on="product_identifier")
```

### Explicit Column Selection
```python
# Good
product_cols = ["product_identifier", "category", "price"]
sample_product = products[product_cols].head(1)

# Bad
sample_product = products.head(1)  # What columns are we using?
```

---

## Print Statements and Output

### Formatted Output
```python
# Good
print("=" * 40)
print("DATA SUMMARY")
print("=" * 40)
print(f"Date range:      {sales['date'].min()} to {sales['date'].max()}")
print(f"Categories:      {sales['category'].nunique()}")
print(f"Total revenue:   ${sales['revenue'].sum():,.2f}")
print("=" * 40)

# Bad
print("Date range:", sales['date'].min(), "to", sales['date'].max())
print("Categories:", sales['category'].nunique())
```

### Use f-strings
- `f"Revenue: ${revenue:,.2f}"`
- Not `"Revenue: $" + str(revenue)`
- Not `"Revenue: ${}".format(revenue)`

---

## Anti-Patterns to Avoid

### Mutation Without Clarity
```python
# Bad: Modifying original DataFrame
sales["new_column"] = sales["revenue"] * 1.1

# Good: Make intent clear
sales = sales.copy()  # If mutation intended
# OR
sales_with_adjustment = sales.assign(new_column=lambda x: x["revenue"] * 1.1)
```

### Hardcoded Values
```python
# Bad
high_price = products[products["price"] > 500]

# Good
PRICE_THRESHOLD = 500  # Define at top of cell or notebook
high_price = products[products["price"] > PRICE_THRESHOLD]
```

### Unused Variables
```python
# Bad
results = load_job_results(job_info)
products = results["products"]
sales = results["sales"]
metadata = results["metadata"]  # Never used
```

### Print Debugging Left In
```python
# Bad
print("DEBUG: products shape:", products.shape)  # Remove before committing
```

---

## Reproducibility

### Always Set Seeds
```python
import random
random.seed(42)

import numpy as np
np.random.seed(42)

# For pandas sampling
sample = df.sample(n=100, random_state=42)
```

---

## Notebook-Specific Standards

### One Logical Operation Per Cell
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

### Cell Complexity Limits
- Analysis cells: 5-10 lines
- Data preparation: 10-15 lines
- Complex operations: 15-20 lines (break into helper function if longer)

### Cell Execution Order
- Cells should be executable top-to-bottom in sequence
- No "skip this cell" or "run cell 5 before cell 3" instructions

### Inline Shell Commands

**Use `!cat` for displaying file contents** (config files, prompts, etc.):
```python
# Good - clear and concise for displaying files
! cat "config_simulation.yaml"
! cat prompt_budget.txt
```

**Avoid shell commands when Python equivalents exist:**
```python
# Bad - use Python for file operations
files = ! ls output/

# Good
from pathlib import Path
output_files = list(Path("output").glob("*"))
```

---

## Output Format

Structure your review as:

### Automated Checks
- Pre-commit: Pass/Fail
- Linting: Pass/Fail (X issues)

### Issues

For each issue found:
1. **File**: path and line number
2. **Issue**: brief description
3. **Suggestion**: how to fix it

Use severity tags:
- **[BLOCKING]** Must be fixed before merge
- **[SUGGESTION]** Recommended improvement
- **[NITPICK]** Minor style preference

---

## Checklist

Before finalizing code:

- [ ] Imports organized and grouped by category
- [ ] Single imports: no parentheses; Multiple imports: use parentheses
- [ ] Variable names are descriptive
- [ ] Comments explain WHY, not WHAT
- [ ] Print output is formatted for readability
- [ ] No hardcoded magic numbers
- [ ] Seeds set for reproducibility
- [ ] No unused variables or imports
- [ ] No debug print statements left in
- [ ] DataFrame operations are clear and explicit
- [ ] NumPy-style docstrings on all public functions

---

## Verification

After making changes, always run:

```bash
git status
ruff format .
ruff check .
```

This checks for untracked files, formats code, and checks for linting issues.

**Success criteria:**
- [ ] All new files are under version control
- [ ] `ruff format .` completes without changes
- [ ] `ruff check .` passes with no errors


---

# Course-Specific Code Conventions

## Import Placement in Lecture Notebooks

For lectures that follow the Theory → Application structure, imports should **not** appear at the beginning of the notebook. Instead, place all imports at the start of Part II (Application) to keep Part I (Theory) completely clean of code.

**Exception:** The Directed Acyclic Graphs lecture includes simulation code in Part I (Theory) to demonstrate collider bias with the police force example. This is intentional—the simulation reinforces a key theoretical point that benefits from immediate hands-on demonstration.

```python
# Good - imports at start of Application section
## Part II: Application

# First code cell of Part II
# Standard Library
import inspect

# Third-party packages
import pandas as pd

# Local imports
from online_retail_simulator import simulate
```

```python
# Bad - imports at notebook start pollute Theory section
# Cell 1: Imports (before any theory content)
import pandas as pd
from online_retail_simulator import simulate

# ... Theory section with no code ...
```

**Rationale:** The Theory section should be pure exposition—definitions, notation, and intuition—without any code distractions. Code only enters when we begin the hands-on Application.

---

## Confounded Treatment Functions (`support.py`)

Functions that generate confounded treatment assignment for measure-impact lectures must follow these conventions:

- Accept `metrics_df: pd.DataFrame` as input and return a product-level DataFrame
- Required output columns: `D` (treatment), `Y0`, `Y1`, `Y_observed`, plus covariates
- Parameters (effect size, selection coefficients) should be explicit function arguments, not hardcoded

---

## Support Module Conventions (`support.py`)

Each measure-impact lecture has a `support.py` with these conventions:

**Function categories and naming:**
- Data generation: `create_confounded_treatment*` or `create_*_data` prefix
- Ground truth: `compute_ground_truth_att()` — extracts true ATT from potential outcomes
- Visualization: `plot_` prefix for all plotting functions
- Print helpers: `print_` prefix for formatted output functions
- Private helpers: `_` prefix (e.g., `_create_binary_quality`, `_parse_weights`)

**Module structure:**
- Module-level docstring describing the file's purpose
- Imports grouped by standard library / third-party / local

**Seed handling:**
- Public functions accept a `seed` parameter (default `42`)
- The notebook's import cell sets `np.random.seed(42)` for top-level random operations

---

## Impact Engine Import Convention

Impact Engine lectures add these imports:
```python
from impact_engine_measure import evaluate_impact, load_results
```

Dynamic config generation adds:
```python
import yaml
```

---

## Lecture Self-Containment

Each lecture directory must be fully self-contained — all files required to run the notebook must exist in the same directory.

**Expected structure:**
```
docs/source/<section>/<lecture-name>/
├── lecture.ipynb          # Main notebook
├── support.py             # Local helper functions (if imported)
├── config_*.yaml          # Configuration files (if referenced)
└── output/                # Generated outputs (gitignored)
```

**Checks:**
- For each `from support import ...` in the notebook, verify `support.py` exists in the same directory
- For each `config_*.yaml` referenced (via `! cat` or Python), verify the file exists in the same directory
- No imports from other lecture directories

---

## Course-Specific Checklist

- [ ] Simulation pipeline follows standard sequence: `!cat` config → `simulate()` → `load_job_results()` → print verification
- [ ] `inspect.getsource()` shown before first use of each `support.py` function
- [ ] Impact Engine calls follow: save CSV → display config → `evaluate_impact()` → `load_results()` → extract results
- [ ] `TRUE_EFFECT` defined as a named constant (not inlined in function calls)
- [ ] Ground truth ATT computed and stored before method comparisons
- [ ] Lecture directory is self-contained (all referenced files present)

---

## Verification

After making changes, always run:

```bash
git status
hatch run ruff format .
hatch run ruff check .
hatch run build
```

This checks for untracked files, formats code, checks for linting issues, builds the documentation and executes all notebooks, confirming that code changes don't break anything.

**Success criteria:**
- [ ] All new files are under version control (`git status` shows no untracked files that should be committed)
- [ ] `hatch run ruff format .` completes without changes
- [ ] `hatch run ruff check .` passes with no errors
- [ ] `hatch run build` completes successfully
