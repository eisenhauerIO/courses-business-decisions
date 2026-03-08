# Measure Impact

The framework begins with measurement — before the [Evaluate Evidence](../evaluate-evidence/index) and [Allocate Resources](../allocate-resources/index) stages can proceed, we need to establish what is true. Causal inference is a well-established field with decades of methodological development, textbooks, and diagnostic tests.

```{figure} ../_static/improve-decisions-framework-measure.svg
:align: center
:alt: The Measure Impact stage in the Learn, Decide, Repeat framework

***Framework — Measure Impact***
```

We follow [Causal Inference: The Mixtape](https://mixtape.scunning.com/) by Scott Cunningham as our foundational reference. All lectures consist of two parts. First, we cover the theory from the book. Second, we apply these concepts to product data and business decision-making contexts.

```{figure} ../_static/mixtape-book.png
:align: center
:width: 150px
```

Each application lecture uses two tools. The [**Online Retail Simulator**](https://eisenhauerio.github.io/tools-online-retail-simulator/) generates fully synthetic retail data where both potential outcomes are observed — an omniscient view that lets us verify whether an estimator recovers the true treatment effect. The [**Impact Engine — Measure**](https://eisenhauerio.github.io/tools-impact-engine-measure/) wraps causal estimation methods behind a single YAML configuration: one call in, one standardized result bundle out.

```{list-table}
:align: center
:header-rows: 1

* - Tool
  - Role
* - [**Online Retail Simulator**](https://eisenhauerio.github.io/tools-online-retail-simulator/)
  - Synthetic data with known ground truth
* - [**Impact Engine — Measure**](https://eisenhauerio.github.io/tools-impact-engine-measure/)
  - Causal effect estimation via YAML config
```

Together, they enable a repeatable five-step workflow that structures every application lecture: frame a business question, simulate data, measure the effect, evaluate performance, and tune parameters.

```{figure} ../_static/lecture-structure.svg
:align: center
:width: 800px

***Lecture Structure***
```

The material is organized in three sections. We begin with foundational causal models that clarify what causal effects mean and under which assumptions they are identified. We then study methods that rely on selection on observables, followed by methods designed to address selection on unobservables.

## Foundations

This section establishes the formal frameworks for defining and reasoning about causal effects. Two complementary perspectives — the potential outcomes model, which provides an algebraic language for causal quantities, and directed acyclic graphs, which encode causal assumptions visually — supply the conceptual foundation for all identification strategies that follow.

### Potential Outcomes Model

We introduce the potential outcomes framework as the foundational model for causal inference. We formalize the fundamental problem — missing counterfactuals — and explain why randomization resolves it. The goal is to establish a precise language for defining causal effects and understanding what can and cannot be identified from data.

```{toctree}
:titlesonly:

01-potential-outcomes-model/lecture
```

### Causal graphical models

We introduce directed acyclic graphs (DAGs) as a complementary representation of causal assumptions. DAGs provide a visual and formal tool for reasoning about identification, making explicit the roles of confounders, mediators, and colliders. We emphasize how graphical structure encodes assumptions rather than estimates.

```{toctree}
:titlesonly:

02-directed-acyclic-graphs/lecture
```

## Selection on observables

```{figure} ../_static/dag-selection-observables.svg
:figclass: figure-float-right
:width: 250px
```

This section covers methods that assume all confounders are observed and measured. As the DAG illustrates, the confounding variables X that jointly influence treatment D and outcome Y are available in the data, so conditioning on X under the conditional independence assumption is sufficient to identify causal effects. The challenge is how to condition effectively — through stratification, matching, or flexible modeling.

### Matching & subclassification

We introduce methods for causal inference under selection on observables. We cover the conditional independence assumption, subclassification, and matching estimators. The focus is on achieving covariate balance to satisfy the backdoor criterion.

```{toctree}
:titlesonly:

03-matching-subclassification/lecture
```

## Selection on unobservables

```{figure} ../_static/dag-selection-unobservables.svg
:figclass: figure-float-right
:width: 280px
```

This section covers methods that address settings where unobserved confounders make the conditional independence assumption untenable. As the DAG shows, even after conditioning on observed confounders X, unobserved confounders U still create a backdoor path between treatment and outcome. Each method exploits a different source of exogenous variation — an instrument, a threshold, a policy change, or a comparison unit — to identify causal effects despite unmeasured confounding.

### Synthetic Control

We discuss synthetic control methods for comparative case studies with panel data. We focus on transparent construction of counterfactuals from comparison units and the assumptions about factor structures and parallel trends that justify identification. The goal is to understand when synthetic control provides a credible strategy for estimating causal effects and how configuration choices affect the resulting estimates.

```{toctree}
:titlesonly:

08-synthetic-control/lecture
```
