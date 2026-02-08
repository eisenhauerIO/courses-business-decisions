# Course Overview

Businesses face countless decisions with incomplete information. Which initiatives will move the needle? Where should resources go?

Economic thinking provides rigor for decision-making. First, measure impact—use causal inference to establish what is true. Then, evaluate the evidence—assess how reliable each estimate is based on methodology rigor and research design. Then, allocate resources—use decision theory to determine what to do. Done well, measurement, evaluation, and allocation create a learning loop: each action produces new evidence, which updates beliefs and informs the next allocation.

Software engineering enables implementation. You need tools to measure impact reliably and to allocate resources systematically. These tools turn economic thinking into scalable processes rather than one-off analyses.

```{figure} improve-decisions-framework.svg
:alt: Improve Decisions Framework
:align: center

***Course Framework***
```

***Measure Impact.***  What is true? Before allocating resources, you must understand what actually works. This stage teaches causal inference methods—from randomized experiments to observational techniques—that distinguish correlation from causation and establish genuine cause and effect.

***Evaluate Evidence.***  How much should we trust this? Not all measurements are equally reliable. This stage teaches how to assess the quality of causal evidence—examining methodology rigor, identification assumptions, and the strength of the research design—to determine which estimates are trustworthy enough to act on.

***Allocate Resources.***  What should we do? Knowing what works is not enough—you must decide where to invest under constraints and uncertainty. This stage teaches how to allocate resources across initiatives based on measured impact and remaining uncertainty. Better evidence enables better bets.

***Build Systems.***  How do we make this repeatable? Measurement and allocation only matter if they can be executed reliably. This stage teaches software development practices—version control, testing, deployment—that turn methods into durable systems for repeated measurement and decision-making.

***Improve Decisions.*** How does this change outcomes? Evidence, priorities, and systems only matter if they shape real behavior. This stage teaches how to translate insights into decisions that are actually implemented. The goal is not economic thinking or tools in isolation—it is driving sustained business outcomes.

This course teaches you to build and operate <img src="../_static/learn-decide-repeat.png" alt="LDR" style="height: 1em; vertical-align: middle;"> ***Learn · Decide · Repeat*** systems. You will learn causal inference, evidence evaluation, decision theory, software engineering, and implementation strategies that turn analysis into systematically improved decisions.

Throughout the course, we ground these ideas in a single, concrete decision context drawn from large-scale online retail. The problem of improving product data quality at scale provides the domain in which every method, system, and decision is introduced.

```{rubric} Frequently Asked Questions
```

**What software do I need to install?** The [Build Systems](https://eisenhauerio.github.io/courses-business-decisions/build-systems/index.html) page lists the tools we use throughout the course. Start with the essentials: [Python](https://www.python.org/), [VS Code](https://code.visualstudio.com/), and [Git](https://git-scm.com/). You'll also need a [GitHub](https://github.com/) account. For Python libraries, we primarily use [NumPy](https://numpy.org/), [Pandas](https://pandas.pydata.org/), [Matplotlib](https://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/), [SciPy](https://scipy.org/), and [Statsmodels](https://www.statsmodels.org/). We'll introduce additional tools as they become relevant—you don't need everything on day one.

**Where can I find the lecture notebooks?** All lecture notebooks are embedded directly in the [course website](https://eisenhauerio.github.io/courses-business-decisions/) under each topic section (Understand Domain, Measure Impact, etc.). Each lecture has its own self-contained directory in the [course repository](https://github.com/eisenhauerIO/courses-business-decisions)—for example, [docs/source/measure-impact/01-potential-outcomes-model/](https://github.com/eisenhauerIO/courses-business-decisions/tree/main/docs/source/measure-impact/01-potential-outcomes-model) contains the notebook, configuration files, and supporting Python scripts. Alternatively, click "Edit on GitHub" at the top of any lecture page to jump directly to its source.
