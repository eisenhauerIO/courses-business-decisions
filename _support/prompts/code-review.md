# Code Review

Review all `*.py` files for quality and correctness.

**Exclude:** `_external/` directory.

## Check For

- **Bugs**: Logic errors, off-by-one, null/None handling, edge cases
- **Clarity**: Unclear variable names, overly complex logic, missing context
- **Style**: Inconsistent formatting, dead code, unused imports, imports not at top of module, premature line breaks (use 120 char limit)
- **Performance**: Unnecessary loops, repeated computations, inefficient patterns
- **Security**: Hardcoded secrets, injection risks, unsafe operations
- **Docstrings**: Missing or incomplete NumPy-style docstrings

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

## Output Format

For each issue found:
1. **File**: path and line number
2. **Issue**: brief description
3. **Suggestion**: how to fix it
