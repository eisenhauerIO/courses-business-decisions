# Evaluate Evidence

Every causal estimate carries implicit uncertainty, but most measurement pipelines treat all estimates as equally trustworthy — passing point estimates downstream without any structured assessment of how much faith to place in them. The consequences compound: when an allocator receives ten initiative-level return estimates, it has no principled way to distinguish a well-powered randomized experiment from a time-series model fit on sparse, noisy data. Capital flows indiscriminately — over-invested in poorly measured initiatives, under-invested in well-measured ones.

This section closes that gap. The first lecture builds the conceptual toolkit for judging evidence quality: validity, diagnostic checks, and the hierarchy of designs. The second unpacks how to encode that judgment in a well-engineered agentic system. The third runs the full pipeline end-to-end, producing the confidence scores the ALLOCATE stage needs to weight returns by evidence quality.

## Causal Evidence

### Evaluating Causal Evidence

We introduce the conceptual tools for assessing whether a causal estimate is trustworthy enough to act on: internal and external validity, statistical versus practical significance, and the hierarchy of evidence. We then examine the diagnostic checks that apply across all causal methods and the method-specific tests for experiments, matching, and synthetic control. The lecture closes by exploring what makes automated confidence scoring defensible — the four failure modes of LLM-based assessment and the four pillars that address them.

```{toctree}
:titlesonly:

01-evaluating-evidence/lecture
```

## Agentic Systems

### Building an Agentic Evaluation System

We examine how the `impact-engine-evaluate` package is built — not how to use it, but what design patterns make it work. The lecture explores six patterns spanning construction (registry dispatch, prompt engineering as software, layered specialization, structured output parsing), evaluation escalation (Judge, Jury, Reviewer, Debate), and the discipline of separating measurement from improvement. Understanding these patterns prepares you to design and extend agentic evaluation systems beyond this specific tool.

```{toctree}
:titlesonly:

02-agentic-evaluation-system/lecture
```

## Application

### Automated Evidence Review

We explore the `impact-engine-evaluate` package end-to-end, running both evaluation strategies — deterministic scoring and agentic review — on mock MEASURE output. The lecture then examines the Correctness pillar directly: by running known-clean and known-flaw artifacts through the reviewer, we demonstrate how an automated assessment system can be validated in practice. We discuss what the Assess–Improve cycle looks like when the system fails to discriminate between strong and weak evidence.

```{toctree}
:titlesonly:

03-application/lecture
```
