# Understand Domain

Decisions are not made in a vacuum. Causal inference, decision theory, and software systems only create value when tailored to the domain in which real decisions are made. Domain knowledge shapes which questions are meaningful, which signals are trustworthy, which constraints are binding, and which mistakes are costly. Without it, even technically correct analyses can lead to irrelevant conclusions or harmful decisions.

## Product Data Improvements

We study the problem of **improving product data quality at scale**. Rather than treating causal inference, decision theory, or software systems in the abstract, the course anchors these ideas in a real operational setting—one where decisions are frequent, uncertainty is pervasive, and mistakes are costly.

The course is grounded in challenges observed in **large-scale generative AI systems operating in production**. In such systems, AI generates vast numbers of potential changes to product data, creating a quality-control problem that cannot be solved through manual review or intuition alone. Ensuring reliability, measuring impact, and deciding which changes to deploy require systematic learning loops that connect evidence to action.

A concrete way to grasp this domain is to look at a real product page, such as [*Keurig K-Express Single Serve Coffee Maker*](https://www.amazon.com/Keurig-K-Express-Coffee-Single-Brewer/dp/B09715G57M?th=1) on Amazon. What consumers see as a simple product listing belies a rich set of underlying data decisions: the title, structured attributes, images, pricing context, badges, and descriptive text all shape discovery, interpretation, and trust. In modern e-commerce systems, many of these elements are proposed or modified by AI, and each such change represents a hypothesis about customer behavior that must be evaluated.

```{figure} product-data.png
:alt: Product Data Example
:align: center

***Product Data***
```

Improving product data quality at scale therefore means learning not just which changes *seem* better, but which actually improve outcomes, and then deciding which modifications to deploy, which to test further, and which to discard—grounded in evidence rather than intuition.

## Online Retail Simulator

We explore the Online Retail Simulator, covering product characteristics simulation, sales metrics with conversion funnels, and treatment effects through enrichment.

[Online Retail Simulator](01-online-retail-simulator/lecture.ipynb)

## AI-Powered Product Catalogs

We implement the Catalog AI system using LLM-generated product details with custom prompts, and visualize causal impact through diverging treatment effect plots.

[AI-Powered Product Catalogs](02-catalog-ai/lecture.ipynb)

```{toctree}
:maxdepth: 2
:hidden:

01-online-retail-simulator/lecture
02-catalog-ai/lecture
```
