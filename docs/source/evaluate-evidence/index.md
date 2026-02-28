# Evaluate Evidence

Not all measurements are equally trustworthy. Before using causal estimates to guide resource allocation, it is essential to assess the quality of the evidence itself. This section teaches how to critically evaluate causal evidence, how to build the agentic systems that automate that assessment, and how to run the full evaluation pipeline end-to-end.

## Causal Evidence

### Evaluating Causal Evidence

We develop the conceptual tools for assessing whether a causal estimate is trustworthy enough to act on. This lecture covers the general principles of internal and external validity, the distinction between statistical and practical significance, and the hierarchy of evidence — which designs provide the most credible identification. We then turn to the diagnostic checks that apply across all causal methods (covariate balance, placebo tests, sensitivity analysis, common support, and pre-treatment trends) and the method-specific diagnostics for experiments, matching, and synthetic control.

```{toctree}
:titlesonly:

01-evaluating-evidence/lecture
```

## Agentic Systems

### Building an Agentic Evaluation System

We examine how the `impact-engine-evaluate` package is built — not how to use it, but what design patterns make it work. The tool implements four patterns that recur across well-engineered agentic systems: registry dispatch (routing inputs to the right handler without hardcoding), prompt engineering as software (versioned YAML templates with knowledge injection), layered specialization (an abstract base class that all reviewers implement), and structured output parsing (constraining and parsing LLM responses into typed objects). Understanding these patterns prepares you to design and extend agentic systems beyond this specific tool.

```{toctree}
:titlesonly:

02-agentic-evaluation-system/lecture
```

## Application

### Automated Evidence Review

We use the `impact-engine-evaluate` package end-to-end, running both evaluation strategies on mock MEASURE output. The deterministic scoring strategy assigns confidence based on the methodology's position in the hierarchy of evidence. The agentic review strategy sends the measurement artifacts to an LLM, which applies the diagnostic framework from the first lecture to score the evidence across five dimensions. Both strategies produce the same 8-key output that the ALLOCATE stage consumes to make confidence-weighted investment decisions.

```{toctree}
:titlesonly:

03-application/lecture
```
