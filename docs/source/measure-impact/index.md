# Measure Impact

Lectures are provided as [Jupyter Notebooks](https://jupyter.org/). Throughout the course, we use the [**Generalized Roy Model**](https://github.com/eisenhauerIO/tools-generalized-roy) as a unifying framework for understanding the statistical assumptions underlying different causal methods and their economic implications. The [**Impact Engine**](https://github.com/eisenhauerIO/tools-impact-engine) allows us then to put these methods into practice.

We follow [Causal Inference: The Mixtape](https://mixtape.scunning.com/) by Scott Cunningham as our foundational reference. The book provides the theoretical baseline, while our lectures apply these concepts to product data and business decision-making contexts.

```{figure} ../_static/mixtape-book.png
:align: center
:width: 150px

***Causal Inference: The Mixtape***
```

The material is organized in three parts. We begin with foundational causal models that clarify what causal effects mean and under which assumptions they are identified. We then study methods that rely on selection on observables, followed by methods designed to address selection on unobservables.

## Foundations

### Potential Outcomes Model

We introduce the potential outcomes framework as the foundational model for causal inference. This section formalizes the fundamental problem of causal inference—missing counterfactuals—and explains why randomization resolves it. The goal is to establish a precise language for defining causal effects and understanding what can and cannot be identified from data.

```{toctree}
:titlesonly:

01-potential-outcome-model/lecture
```

### Causal Graphical Models

We introduce directed acyclic graphs (DAGs) as a complementary representation of causal assumptions. DAGs provide a visual and formal tool for reasoning about identification, making explicit the roles of confounders, mediators, and colliders. This section emphasizes how graphical structure encodes assumptions rather than estimates.

```{toctree}
:titlesonly:

02-directed-acyclic-graphs/lecture
```

### Generalized Roy Model

We introduce the Generalized Roy Model as a unifying framework for causal inference under selection. The model makes selection mechanisms explicit and provides a common structure for understanding treatment effect heterogeneity, self-selection, and policy evaluation. Within this framework, many standard causal methods can be interpreted as imposing different assumptions on potential outcomes and selection rules.

```{toctree}
:titlesonly:

03-generalized-roy-model/lecture
```

## Selection on Observables

### Matching & Propensity Scores

We discuss methods for causal inference when selection into treatment depends only on observed covariates. This section covers matching estimators and propensity score methods, highlighting the conditions under which covariate balance is sufficient for identification.

```{todo}
Add notebook link
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

### Instrumental Variables

We introduce instrumental variables as a method for causal inference when unobserved confounding is present. The focus is on identification assumptions, interpretation of local average treatment effects, and the role of instruments within the Generalized Roy framework.

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
