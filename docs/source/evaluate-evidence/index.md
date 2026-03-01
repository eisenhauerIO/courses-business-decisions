# Evaluate Evidence

With causal estimates produced in the [Measure Impact](../measure-impact/index) stage, the next step is to assess how much to trust them before they can inform the [Allocate Resources](../allocate-resources/index) stage. Structured evaluation of causal evidence is a much younger discipline than causal inference itself, with few textbook treatments and many open questions.

```{figure} ../_static/improve-decisions-framework-evaluate.svg
:figclass: figure-float-right
:width: 400px
```

Every causal estimate carries two kinds of uncertainty. **Statistical uncertainty** — captured in confidence intervals and standard errors — reflects sampling variability and is already part of the measurement output. **Epistemic uncertainty** — design quality, assumption violations, diagnostic failures — is not. Most decision pipelines treat all estimates as equally trustworthy, passing point estimates downstream without any structured assessment of epistemic quality. The consequences compound: when we receive ten initiative-level return estimates, we have no principled way to distinguish a well-powered randomized experiment from a time-series model fit on sparse, noisy data. Resources flow indiscriminately — too much allocated to poorly measured initiatives, too little to well-measured ones.

The material is organized in three parts. We begin with the conceptual toolkit for judging evidence quality — validity, diagnostic checks, and the hierarchy of designs. Because manual review of every estimate does not scale across a portfolio, a dedicated section develops the principles and design patterns for building agentic evaluation systems that produce defensible confidence scores automatically. We then run the full pipeline end-to-end, demonstrating how automated assessment translates measurement output into the confidence-weighted returns that drive resource allocation.

## Evidence Quality

This section develops the diagnostic framework for judging causal evidence. It establishes the vocabulary — internal and external validity, statistical versus practical significance, the hierarchy of designs — and the diagnostic checks that distinguish trustworthy estimates from unreliable ones, whether applied manually or by an automated system.

### Causal Diagnostics

We introduce the conceptual tools for assessing whether a causal estimate is trustworthy enough to act on: validity, significance, and the hierarchy of evidence. We then examine the diagnostic checks that apply across all causal methods and the method-specific tests for experiments, matching, and synthetic control.

```{toctree}
:titlesonly:

01-evaluating-evidence/lecture
```

## Automated Assessment

This section shifts from what to evaluate to how to build systems that evaluate at scale. It develops the principles that make automated confidence scoring defensible — the failure modes of LLM-based assessment, the pillars that address them, the escalation ladder — and then examines the software patterns that instantiate those principles in the `impact-engine-evaluate` package.

### Agentic Evaluation

We develop the principles for trustworthy automated assessment: the four failure modes of LLM-based scoring, the four pillars of defensible confidence, evaluation escalation from Judge through Debate, and the discipline of separating measurement from improvement. We then examine how the `impact-engine-evaluate` package implements these principles through registry dispatch, prompt engineering as software, layered specialization, and structured output parsing.

```{toctree}
:titlesonly:

02-agentic-evaluation-system/lecture
```

## Evaluation Pipeline

This section applies the conceptual and engineering foundations from the preceding parts. It runs the full evaluation pipeline on mock measurement output and validates the system's ability to discriminate between strong and weak evidence.

### Automated Review

We run the `impact-engine-evaluate` package end-to-end, applying both evaluation strategies — deterministic scoring and agentic review — to mock measurement output. The lecture then examines the Correctness pillar directly: by running known-clean and known-flaw artifacts through the reviewer, we demonstrate how an automated assessment system can be validated in practice.

```{toctree}
:titlesonly:

03-application/lecture
```
