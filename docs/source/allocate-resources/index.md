# Allocate Resources

With causal estimates from the [Measure Impact](../measure-impact/index) stage and their credibility assessed in the [Evaluate Evidence](../evaluate-evidence/index) stage, the final step is to decide where to invest under uncertainty. Connecting evidence quality to resource allocation is emerging territory, with methods, software patterns, and best practices still being developed.

```{figure} ../_static/improve-decisions-framework-allocate.svg
:align: center
:alt: The Allocate Resources stage in the Learn, Decide, Repeat framework
```

Every initiative arrives at the allocation stage with two numbers: a causal effect estimate from **MEASURE** and a confidence score from **EVALUATE**. The confidence score translates directly into a penalty on projected returns — low-confidence estimates are pulled toward worst-case outcomes, creating a built-in incentive for better measurement. The allocation framework then selects which initiatives to fund subject to budget constraints, using decision rules that handle the remaining uncertainty across plausible scenarios.

The material is organized in one section. **Portfolio Optimization** develops the mathematical framework for selecting initiatives under uncertainty and applies it end-to-end using the [**Impact Engine**](https://eisenhauerio.github.io/tools-impact-engine-allocate/).

## Portfolio Optimization

This section develops the decision-theoretic framework for portfolio selection — confidence penalties, minimax regret, and Bayesian decision rules — and applies it to a mock portfolio using production-grade solvers.

### Portfolio selection under uncertainty

We formalize the resource allocation problem as a binary integer program with confidence-weighted returns, budget constraints, and a downside safeguard. Part I develops the theory following Eisenhauer (2025): scenario-dependent returns, the confidence penalty, minimax regret optimization, and the Bayesian alternative. Part II applies the framework end-to-end on mock portfolio data, verifying results against the paper's simulation example and demonstrating how evidence quality shapes allocation decisions.

```{toctree}
:titlesonly:

01-portfolio-optimization/lecture
```
