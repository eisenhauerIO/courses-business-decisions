# NumPy Docstring Review

Review all `*.py` files and ensure they have proper NumPy-style docstrings.

**Exclude:** `_external/` directory (third-party code).

## Requirements

### Module Level
Every Python file should have a module-level docstring at the top explaining its purpose.

### Functions
All public functions must have docstrings with these sections (as applicable):

```python
def function_name(param1, param2):
    """
    Short one-line summary.

    Longer description if needed, explaining the function's
    behavior in more detail.

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

    Examples
    --------
    >>> function_name(1, 2)
    3
    """
```

### Classes
All classes must have docstrings with:

```python
class ClassName:
    """
    Short one-line summary.

    Longer description if needed.

    Parameters
    ----------
    param1 : type
        Description of constructor parameter.

    Attributes
    ----------
    attr1 : type
        Description of instance attribute.
    """
```

### Methods
- All public methods need docstrings
- Private methods (`_method`) should have docstrings if logic is non-trivial
- `__init__` parameters documented in class docstring, not method

## Checklist

For each file, verify:
- [ ] Module docstring present
- [ ] All public functions have docstrings
- [ ] All classes have docstrings
- [ ] All public methods have docstrings
- [ ] Parameters section lists all parameters with types
- [ ] Returns section describes return value and type
- [ ] Raises section documents exceptions (if any)
- [ ] Examples provided for complex functions

## Output Format

For each file reviewed, report:
1. **File**: path to file
2. **Missing docstrings**: list functions/classes/methods without docstrings
3. **Incomplete docstrings**: list items missing required sections
4. **Suggested fixes**: provide corrected docstrings

## Style Notes

- Use imperative mood for summary ("Calculate X" not "Calculates X")
- Keep summary line under 79 characters
- Blank line between summary and description
- Align parameter descriptions
- Use `optional` for parameters with defaults
