# Software

Throughout the course, we ground causal inference and decision-making concepts in a single, concrete decision context drawn from large-scale online retail: improving product data quality at scale. The <img src="../_static/online-retail-simulator.svg" alt="ORS" style="height: 1em; vertical-align: middle;"> **[Online Retail Simulator](https://github.com/eisenhauerIO/tools-catalog-generator)** provides the domain-specific environment in which methods and trade-offs are introduced. The Impact Engine and Portfolio Allocation frameworks then generalize these ideas into reusable systems for measuring impact and allocating resources across decision contexts. The Generalized Roy Model underpins this software stack as the foundational framework for reasoning about selection, heterogeneity, and identification.

## Online Retail Simulator [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg?logo=github)](https://github.com/eisenhauerIO/tools-catalog-generator)

Generates fully synthetic retail data for end-to-end testing of causal inference workflows. Supports controlled treatment effects, enabling validation of estimators and comparison of causal models against known ground truth.

## Causal Engine [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg?logo=github)](https://github.com/eisenhauerIO/tools-causal-engine)

Implements causal inference methods for measuring treatment effects in business decision contexts. Provides a unified interface for estimation, diagnostics, and sensitivity analysis across observational and experimental data.

## Portfolio Allocation [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg?logo=github)](https://github.com/eisenhauerIO/tools-portfolio-allocation)

Optimizes resource allocation across initiatives based on estimated impact and uncertainty. Translates causal effect estimates into actionable investment decisions under constraints.

## Generalized Roy [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue.svg?logo=github)](https://github.com/eisenhauerIO/tools-generalized-roy)

Simulates and estimates the Generalized Roy model for policy evaluation under selection. Provides a unifying framework for understanding treatment effect heterogeneity and identification assumptions.
