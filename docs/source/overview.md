# Course Overview

Every business decision is a bet made under uncertainty. This course teaches you to improve those odds through a systematic approach.

Every stage exists to drive action and generate learning. First, measure impact—use causal inference to establish what is true. Then, allocate resources—use decision theory to determine what to do. But the process does not end there. Each action produces new evidence, which updates beliefs, which informs the next allocation. What begins as a static decision problem becomes a dynamic loop of learning and acting under uncertainty.

```{figure} _static/drive-action-framework.svg
:alt: Drive Action Framework
:align: center

From Evidence to Action (and back)
```

***Understand Domain.*** Every concept in this course is grounded in a concrete problem: improving product data quality at scale. We use the [Catalog Generator](https://github.com/eisenhauerIO/tools-catalog-generator) as our running example—a system that enriches product catalogs with AI-generated attributes. This setting provides the context for measuring impact, allocating resources, and implementing decisions.

***Measure Impact.*** Correlation is not causation. Before allocating resources, you need to know what actually works. This stage teaches causal inference methods—from randomized experiments to observational techniques—that establish genuine cause and effect. The [Generalized Roy Model](https://github.com/eisenhauerIO/tools-generalized-roy) provides a unified framework that reveals how selection problems arise and which methods address which assumptions. The [Causal Engine](https://github.com/eisenhauerIO/tools-causal-engine) puts these methods into practice.

***Allocate Resources.*** Evidence alone does not make decisions. Once you know what works, you must decide where to invest. This stage teaches how to allocate resources across initiatives based on measured impact and remaining uncertainty. Better evidence enables better bets.

***Build Tools.*** Ideas alone do not ship products. Every stage requires code that runs reliably in production. This stage teaches software development practices—from version control to testing to deployment—that turn analysis into systems. We use [Kiro](https://kiro.dev/) as our AI coding assistant throughout.

***Drive Actions.*** Analysis alone does not drive results. Once you know what works and where to invest, you must act. This stage teaches how to translate insights into decisions that actually get implemented. The goal is not analysis—it is outcomes.
