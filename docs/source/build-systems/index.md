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
- [Kiro Getting Started](https://kiro.dev/docs/getting-started/installation/) — Installation and setup

## Agentic Systems

### Designing Agentic Systems

Agentic systems use LLMs as reasoning components within a structured software pipeline — not open-ended chat, but constrained evaluation with typed inputs and outputs. The `impact-engine-evaluate` package (used in the [Evaluate Evidence](../evaluate-evidence/index.md) section) is a concrete example: it sends measurement artifacts to an LLM for methodological review, producing structured confidence scores that feed downstream allocation. This tutorial uses that tool to illustrate the core design patterns behind agentic systems.

#### Registry + Dispatch

Rather than hardcoding which reviewer handles which methodology, the system uses a **registry pattern**. Each reviewer registers itself with a decorator, and the registry dispatches at runtime based on the `model_type` field from the manifest:

```python
@MethodReviewerRegistry.register("experiment")
class ExperimentReviewer(MethodReviewer):
    name = "experiment"
    confidence_range = (0.85, 1.0)
    ...
```

The same pattern appears for LLM backends — `BackendRegistry` routes to Anthropic, OpenAI, or LiteLLM based on configuration. This makes it straightforward to add new methods or backends without modifying existing code: implement the interface, register with a decorator, and the system discovers it automatically.

#### Prompt Engineering as Software

In production agentic systems, prompts are not ad-hoc strings — they are **versioned artifacts** managed like any other code. The evaluate tool stores prompts as YAML files with explicit metadata:

```yaml
name: experiment_review
version: "1.0"
dimensions:
  - randomization_integrity
  - specification_adequacy
  - statistical_inference
  - threats_to_validity
  - effect_size_plausibility

system: |
  You are a methodological reviewer specializing in RCTs...
  {{ knowledge_context }}

user: |
  Review the following artifact:
  {{ artifact }}
```

Jinja2 templates separate *what to evaluate* (the artifact) from *how to evaluate* (the instructions and domain knowledge). Knowledge files — markdown documents encoding design principles, common pitfalls, and diagnostic standards — are injected via `{{ knowledge_context }}`, grounding the LLM's assessment in domain expertise rather than relying solely on its training data.

#### Layered Specialization

The system uses an **abstract base class** (`MethodReviewer`) to define the contract that all reviewers must satisfy, while concrete implementations supply method-specific behavior:

| Layer | Responsibility |
|-------|----------------|
| `MethodReviewer` (ABC) | Defines interface: `load_artifact()`, `prompt_template_dir()`, `knowledge_content_dir()`, `confidence_range` |
| `ExperimentReviewer` | Supplies experiment-specific prompt, knowledge files, confidence range (0.85–1.0), and artifact loading |

This layering means adding support for a new methodology (e.g., difference-in-differences) requires implementing one class with the method-specific details — the orchestration logic in `Evaluate` and `ReviewEngine` remains unchanged.

#### Structured Output

LLMs produce free-form text, but downstream systems need typed data. The evaluate tool constrains the LLM's response format and parses it into structured objects:

1. The prompt specifies the exact output format: `DIMENSION: / SCORE: / JUSTIFICATION:` blocks
2. A regex parser extracts per-dimension scores and justifications
3. A JSON fallback handles alternative response formats
4. All scores are clamped to [0.0, 1.0] and assembled into a typed `ReviewResult` with `ReviewDimension` objects

This pattern — **constrain, parse, validate** — is fundamental to agentic systems. The LLM provides reasoning and judgment; the surrounding code ensures the output is reliable and machine-readable.

#### Connecting the Patterns

These patterns compose into the full MEASURE → EVALUATE → ALLOCATE pipeline:

1. **MEASURE** produces a job directory with a manifest and result files
2. **Registry dispatch** selects the right `MethodReviewer` based on `model_type`
3. **Strategy dispatch** routes to score (deterministic) or review (agentic) based on `evaluate_strategy`
4. For agentic review: **prompt templates** + **knowledge injection** produce the LLM prompt, **structured output parsing** converts the response to a typed `ReviewResult`
5. Both paths produce the same 8-key output dict, which **ALLOCATE** consumes to make investment decisions

The key insight is that each pattern handles a specific concern — routing, specialization, prompting, parsing — and they combine cleanly because the interfaces between them are well-defined. This modularity is what makes agentic systems maintainable as they grow.

**Resources**

- [Anthropic: Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Design patterns for LLM-powered systems
- [Anthropic: Claude Agent SDK](https://docs.anthropic.com/en/docs/agents-and-tools/claude-agent-sdk/overview) — SDK for building agents with Claude
