# Measure Impact

Lectures are provided as [Jupyter Notebooks](https://jupyter.org/). The [**Impact Engine**](https://github.com/eisenhauerIO/tools-impact-engine) allows us to put causal inference methods into practice.

We follow [Causal Inference: The Mixtape](https://mixtape.scunning.com/) by Scott Cunningham as our foundational reference.

```{figure} ../_static/mixtape-book.png
:align: center
:width: 150px

***Causal Inference: The Mixtape***
```

### Lecture Structure

All lectures consist of two parts:

**Part I: Theory** draws directly from the corresponding Mixtape chapter. Each section introduces the method's formal framework, identification assumptions, and key estimators using the book's notation and exposition style.

**Part II: Application** connects theory to practice through a recurring business scenario—product content optimization in an online retail setting. Every application follows a common progression:

1. **Business Context** — frame the causal question within the recurring domain
2. **Data Generation** — use the [Online Retail Simulator](https://github.com/eisenhauerIO/tools-catalog-generator) to produce data with known ground truth via confounded treatment assignment
3. **Naive Comparison** — compute the biased estimate and explain why it fails using Part I theory
4. **Apply the Method** — implement the method using the [Impact Engine](https://github.com/eisenhauerIO/tools-impact-engine-measure), mapping each interface parameter back to its theoretical concept
5. **Validation Against Ground Truth** — compare the estimate to the true effect, which is known because the simulator exposes full potential outcomes
6. **Deep Dive** — explore method-specific diagnostics, limitations, or extensions that deepen understanding beyond the core estimation

### Organization

The material is organized in three parts. We begin with foundational causal models that clarify what causal effects mean and under which assumptions they are identified. We then study methods that rely on selection on observables, followed by methods designed to address selection on unobservables.

## Foundations

These lectures establish the conceptual and formal tools for reasoning about causality. They define what causal effects are, when they can be identified, and how graphical models encode the assumptions that make identification possible.

### Potential Outcomes Model

We introduce the potential outcomes framework as the foundational model for causal inference. This section formalizes the fundamental problem of causal inference—missing counterfactuals—and explains why randomization resolves it. The goal is to establish a precise language for defining causal effects and understanding what can and cannot be identified from data.

```{toctree}
:titlesonly:

01-potential-outcomes-model/lecture
```

### Causal Graphical Models

We introduce directed acyclic graphs (DAGs) as a complementary representation of causal assumptions. DAGs provide a visual and formal tool for reasoning about identification, making explicit the roles of confounders, mediators, and colliders. This section emphasizes how graphical structure encodes assumptions rather than estimates.

```{toctree}
:titlesonly:

02-directed-acyclic-graphs/lecture
```

## Selection on Observables

These methods assume that all confounders are observed and measured. Under the conditional independence assumption, conditioning on observed covariates is sufficient to identify causal effects. The challenge is how to condition effectively—through stratification, matching, or flexible modeling.

### Matching & Subclassification

We introduce methods for causal inference under selection on observables. This section covers the conditional independence assumption, subclassification, and matching estimators. The focus is on achieving covariate balance to satisfy the backdoor criterion.

```{toctree}
:titlesonly:

03-matching-subclassification/lecture
```

### Machine Learning for Causal Inference

We explore how machine learning methods can improve causal inference, focusing on high-dimensional covariate settings. Topics include LASSO-based covariate selection and double machine learning, with an emphasis on separating prediction from causal identification.

```{todo}
Add notebook link
```

### Pooled Ordinary Least Squares (OLS)

We discuss pooled OLS estimation with panel data and clarify the assumptions under which it can be interpreted causally. The section emphasizes when pooled regression is valid and when it fails due to unobserved heterogeneity or dynamic selection.

```{todo}
Add notebook link
```

## Selection on Unobservables

These methods address settings where unobserved confounders make the conditional independence assumption untenable. Each exploits a different source of exogenous variation—an instrument, a threshold, a policy change, or a comparison unit—to identify causal effects despite unmeasured confounding.

### Instrumental Variables

We introduce instrumental variables as a method for causal inference when unobserved confounding is present. The focus is on identification assumptions, interpretation of local average treatment effects, and the role of instruments in causal inference.

```{todo}
Add notebook link
```

### Regression Discontinuity

We discuss regression discontinuity designs that exploit sharp or fuzzy thresholds in treatment assignment. The section emphasizes identification at the cutoff and the interpretation of local causal effects.

```{todo}
Add notebook link
```

### Difference-in-Differences

We present difference-in-differences methods for panel data, including the parallel trends assumption and recent methodological advances. Connections to selection models and potential outcomes are made explicit.

```{todo}
Add notebook link
```

### Synthetic Control

We discuss synthetic control methods for comparative case studies with panel data, focusing on transparent construction of counterfactuals and assumptions about factor structures and trends.

```{todo}
Add notebook link
```
