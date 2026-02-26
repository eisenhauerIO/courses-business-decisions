# Measure Impact

Lectures are provided as [Jupyter Notebooks](https://jupyter.org/). We follow [Causal Inference: The Mixtape](https://mixtape.scunning.com/) by Scott Cunningham as our foundational reference. All lectures consist of two parts. First, we cover the theory from the book. Second, we apply these concepts to product data and business decision-making contexts using the [**Online Retail Simulator**](https://github.com/eisenhauerIO/tools-catalog-generator) and the [**Impact Engine**](https://github.com/eisenhauerIO/tools-impact-engine).

Each application lecture follows the same five-step workflow. We frame a causal question in a business context, simulate data with known ground truth using the Online Retail Simulator, measure the treatment effect — first with a naive approach, then with a causal method — using the Impact Engine, evaluate how well each method recovers the truth, and tune the method's parameters to understand how configuration choices affect the reliability of causal estimates.

```{figure} ../_static/lecture-structure.svg
:align: center
:width: 800px

***Lecture Structure***
```

The material is organized in four parts. We begin with foundational causal models that clarify what causal effects mean and under which assumptions they are identified. A dedicated tooling section introduces the software infrastructure that supports the applied work throughout the course. We then study methods that rely on selection on observables, followed by methods designed to address selection on unobservables.

## Foundations

These lectures establish the formal frameworks for defining and reasoning about causal effects. We introduce two complementary perspectives — the potential outcomes model, which provides an algebraic language for causal quantities, and directed acyclic graphs, which encode causal assumptions visually. Together, they supply the conceptual foundation for all identification strategies that follow.

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

## Tooling

This section covers the software tools that support applying causal methods in practice. While the lectures develop theory and walk through worked examples, the tools introduced here provide the infrastructure for moving from method to measurement — configuring estimation strategies, producing standardized results, and simulating data with known ground truth.

### Impact Engine

The [**Impact Engine**](https://github.com/eisenhauerIO/tools-impact-engine) puts the causal inference methods from this course into practice. It provides a unified interface for estimating causal effects — each measurement method is configured through a single YAML file and produces standardized results, so that switching between estimation strategies requires changing one configuration line. Its [documentation](https://eisenhauerio.github.io/tools-impact-engine-measure/) covers usage, configuration, and system design.

## Selection on Observables

```{figure} ../_static/dag-selection-observables.svg
:figclass: figure-float-right
:width: 250px
```

These methods assume that all confounders are observed and measured. As the DAG illustrates, the confounding variables X that jointly influence treatment D and outcome Y are available in the data. Under the conditional independence assumption, conditioning on X is sufficient to identify causal effects. The challenge is how to condition effectively — through stratification, matching, or flexible modeling.

### Matching & Subclassification

We introduce methods for causal inference under selection on observables. This section covers the conditional independence assumption, subclassification, and matching estimators. The focus is on achieving covariate balance to satisfy the backdoor criterion.

```{toctree}
:titlesonly:

03-matching-subclassification/lecture
```

## Selection on Unobservables

```{figure} ../_static/dag-selection-unobservables.svg
:figclass: figure-float-right
:width: 280px
```

These methods address settings where unobserved confounders make the conditional independence assumption untenable. As the DAG shows, even after conditioning on observed confounders X, unobserved confounders U still create a backdoor path between treatment and outcome. Each method below exploits a different source of exogenous variation — an instrument, a threshold, a policy change, or a comparison unit — to identify causal effects despite unmeasured confounding.

### Synthetic Control

We discuss synthetic control methods for comparative case studies with panel data, focusing on transparent construction of counterfactuals and assumptions about factor structures and trends.

```{toctree}
:titlesonly:

08-synthetic-control/lecture
```
