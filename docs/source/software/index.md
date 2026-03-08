# Software

Throughout the material, we ground causal inference and decision-making concepts in a single, concrete decision context drawn from large-scale online retail: improving product data quality at scale. The <img src="../_static/online-retail-simulator.svg" alt="ORS" style="height: 1em; vertical-align: middle;"> **[Online Retail Simulator](https://github.com/eisenhauerIO/tools-catalog-generator)** provides the domain-specific environment in which methods and trade-offs are introduced. The **[Impact Engine](https://eisenhauerio.github.io/tools-impact-engine-website)** then generalizes these ideas into a reusable ecosystem for measuring impact, evaluating evidence quality, and allocating resources across decision contexts.

## Online Retail Simulator [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg?logo=github)](https://github.com/eisenhauerIO/tools-catalog-generator)

Generates fully synthetic retail data for end-to-end testing of causal inference workflows. Supports controlled treatment effects, enabling validation of estimators and comparison of causal models against known ground truth.

## Impact Engine

The Impact Engine is an open-source Python ecosystem that operationalizes the *Learn, Decide, Repeat* loop as a production pipeline. Four independently tested and deployable components map directly to the framework stages:

### Measure [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg?logo=github)](https://github.com/eisenhauerIO/tools-impact-engine-measure)

Estimates causal impact using a unified, config-driven interface. Wraps multiple estimation methods (SARIMAX, synthetic control, difference-in-differences, propensity score matching, causal forests) behind a single `execute()` call. Swap the estimation method by changing one line in a YAML config.

### Evaluate [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg?logo=github)](https://github.com/eisenhauerIO/tools-impact-engine-evaluate)

Scores how much to trust each impact estimate based on its measurement design. Supports both an LLM-powered agentic review mode and a lightweight deterministic scorer. The confidence score directly penalizes return estimates downstream, making the allocator conservative where evidence is weak.

### Allocate [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg?logo=github)](https://github.com/eisenhauerIO/tools-impact-engine-allocate)

Determines where to invest using portfolio optimization under uncertainty. Supports pluggable decision rules (minimax regret, Bayesian weighted-scenario) and respects budget and strategic constraints.

### Orchestrator [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg?logo=github)](https://github.com/eisenhauerIO/tools-impact-engine-orchestrator)

Wires all three components into a single config-driven pipeline. Takes a YAML configuration and runs the full measurement-to-allocation loop: config in, decision out.
