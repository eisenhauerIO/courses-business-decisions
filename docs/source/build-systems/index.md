# Build Systems

Effective decision-making systems require reliable software foundations. This section introduces the core practices needed to implement, operate, and iteratively improve systems for measuring impact and allocating resources. We cover programming with [Python](https://www.python.org/), [Jupyter](https://jupyter.org/) notebooks, and [VS Code](https://code.visualstudio.com/), as well as software engineering practices including version control with [Git](https://git-scm.com/), collaboration on [GitHub](https://github.com/), automated testing and linting, and AI-assisted development with [Kiro](https://kiro.dev/). These skills enable analytical insights to be embedded in durable, extensible software rather than remaining isolated analyses.

## Programming

### Python

Python is the primary programming language for this course. We use it for data analysis, causal inference, simulation, and building decision systems. The language's rich ecosystem of scientific computing libraries—including [pandas](https://pandas.pydata.org/) for data manipulation, [NumPy](https://numpy.org/) for numerical operations, [SciPy](https://scipy.org/) for scientific computing, and [matplotlib](https://matplotlib.org/) for visualization—makes it ideal for translating analytical insights into working code.

**Resources**

- [QuantEcon](https://quantecon.org/) — Open source lectures on quantitative economics with Python
- [Scientific Python Lectures](https://lectures.scientific-python.org/index.html) — Tutorials on the scientific Python ecosystem

### Jupyter

[Jupyter](https://jupyter.org/) notebooks provide an interactive computing environment that combines code, visualizations, and narrative text. This format is ideal for exploratory data analysis, prototyping models, and documenting analytical workflows. Notebooks make it easy to iterate on ideas and share reproducible analyses with collaborators.

**Resources**

- [Jupyter Documentation](https://docs.jupyter.org/) — Official guides and tutorials
- [JupyterLab](https://jupyterlab.readthedocs.io/) — Next-generation notebook interface

### VS Code

[Visual Studio Code](https://code.visualstudio.com/) is a lightweight code editor that serves as the primary development environment for this course. Its rich extension ecosystem supports Python development through the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and integrated Git workflows. It serves as a central hub where coding, Git workflows, and data exploration come together in one interface.

**Resources**

- [VS Code Docs](https://code.visualstudio.com/docs) — Official documentation and tutorials
- [Python in VS Code](https://code.visualstudio.com/docs/languages/python) — Guide for Python development

## Software Engineering

### Git & GitHub

[Git](https://git-scm.com/) is a distributed version control system that tracks changes to code over time, enabling experimentation through branches and reliable rollback when needed. [GitHub](https://github.com/) builds on Git by providing a collaborative platform for hosting repositories, reviewing code through [pull requests](https://docs.github.com/en/pull-requests), and automating workflows with [GitHub Actions](https://docs.github.com/en/actions). Together, they form the backbone of modern software collaboration—ensuring that analytical code remains reproducible, auditable, and easy to extend.

**Resources**

- [GitHub Skills](https://skills.github.com/) — Interactive courses for learning GitHub
- [GitHub Get Started](https://docs.github.com/en/get-started) — Official GitHub documentation

### Code Quality

[Ruff](https://docs.astral.sh/ruff/) enforces consistent style and catches common errors like undefined variables through automated linting and formatting. [pytest](https://docs.pytest.org/) provides a framework for writing tests that verify code behaves as expected and serve as living documentation. Together, these tools help ensure that decision systems remain reliable as they evolve.

**Resources**

- [Ruff Documentation](https://docs.astral.sh/ruff/) — Fast Python linter and formatter
- [pytest Documentation](https://docs.pytest.org/) — Testing framework

### Kiro

[Kiro](https://kiro.dev/) is an AI-powered IDE from Amazon that brings agentic AI capabilities to software development. It uses a spec-driven approach where developers define requirements, design, and tasks in structured documents, and the AI assists with implementation while maintaining context across the project. This workflow aligns well with building decision systems—translating business requirements into working code with AI assistance.

**Resources**

- [Kiro Documentation](https://kiro.dev/docs/) — Official guides and tutorials
