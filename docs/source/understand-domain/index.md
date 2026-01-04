# Understand Domain

Decisions are not made in a vacuum. Causal inference, decision theory, and software systems only create value when tailored to the domain in which real decisions are made. Domain knowledge shapes which questions are meaningful, which signals are trustworthy, which constraints are binding, and which mistakes are costly. Without it, even technically correct analyses can lead to irrelevant conclusions or harmful decisions. This course therefore begins with domain understanding—not as background context, but as a core input to building effective <img src="../_static/learn-decide-repeat.png" alt="LDR" style="height: 1em; vertical-align: middle;"> ***Learn · Decide · Repeat*** systems.

## Improving Product Data Quality

We study the problem of **improving product data quality at scale**. Rather than treating causal inference, decision theory, or software systems in the abstract, the course anchors these ideas in a real operational setting—one where decisions are frequent, uncertainty is pervasive, and mistakes are costly.

The course is grounded in challenges observed in **large-scale generative AI systems operating in production**. In such systems, AI generates vast numbers of potential changes to product data, creating a quality-control problem that cannot be solved through manual review or intuition alone. Ensuring reliability, measuring impact, and deciding which changes to deploy require systematic learning loops that connect evidence to action.

A concrete way to grasp this domain is to look at a real product detail page, such as [*Keurig K-Express Single Serve Coffee Maker*](https://www.amazon.com/Keurig-K-Express-Coffee-Single-Brewer/dp/B09715G57M?th=1) on Amazon. What consumers see as a simple product listing belies a rich set of underlying data decisions: the title, structured attributes, images, pricing context, badges, and descriptive text all shape discovery, interpretation, and trust. In modern e-commerce systems, many of these elements are proposed or modified by AI, and each such change represents a hypothesis about customer behavior that must be evaluated.

```{figure} ../_static/product-data.png
:alt: Product Data Example
:align: center

***Product Data***
```

Improving product data quality at scale therefore means learning not just which changes *seem* better, but which actually improve outcomes, and then deciding which modifications to deploy, which to test further, and which to discard—grounded in evidence rather than intuition.

For a deeper discussion of these issues and how they arise in practice, see [*Addressing Gen AI’s Quality Control Problem*](https://hbr.org/2025/09/addressing-gen-ais-quality-control-problem)
(*Harvard Business Review*, September–October 2025), which examines how organizations confront noise, hallucinations, and scale in AI-driven content systems.

## Simulating Product Data

To study this domain systematically, the course uses the [Online Retail Simulator](https://eisenhauerio.github.io/tools-catalog-generator) as a running example. The simulator generates fully synthetic retail data, enriching product catalogs with AI-generated attributes while supporting controlled treatment effects and known ground truth.

This simulated setting allows us to test causal methods end to end, validate decision rules under uncertainty, and reason explicitly about tradeoffs that affect decision quality—before applying similar approaches to production systems. Throughout the course, the simulator serves as a concrete instantiation of the domain, providing a reproducible environment in which to connect domain knowledge and causal inference to decision-making.
