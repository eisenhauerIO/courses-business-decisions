# Offerings

*Built on a production decision system — not slides about one.*

---

## The problem

Causal inference methods exist. So do decision frameworks and portfolio optimization theory. But they are taught in isolation — separate courses, separate tools, separate people. The result is a persistent gap between knowing how to estimate an effect and operating a system that turns estimates into decisions.

Three questions sit at the center of every investment decision: Did it work? How confident are we? Where should we invest next? Most organizations and most curricula treat these as separate problems. This material treats them as one loop.

Participants learn to close the loop.

## The system

The [**Impact Engine**](https://eisenhauerio.github.io/tools-impact-engine-website) isn't courseware. It's a config-driven, CI/CD-tested, open-source Python ecosystem that runs a complete measurement-to-allocation pipeline in a single call. One principle — *Learn, Decide, Repeat* — connects four stages into an operational loop:

- **Measure** — Estimate causal impact using rigorous econometric methods (synthetic control, difference-in-differences, causal forests, and more)
- **Evaluate** — Score how much to trust each estimate using an LLM-powered quality assurance system grounded in structured diagnostics
- **Allocate** — Determine where to invest using portfolio optimization under uncertainty
- **Orchestrate** — Wire the full loop together: config in, decision out

Every session is a Jupyter notebook that executes against this infrastructure. Participants run the pipeline on a realistic business problem (product data quality in large-scale online retail) and see how the output of each stage feeds the next. Swap an estimation method by changing one `YAML` line. Add a decision rule by writing one adapter class. Participants see what a production-grade research pipeline looks like from the inside.

## Gen AI as quality assurance

Most Gen AI programs teach prompting. Participants here learn to build production-grade AI systems that do real analytical work.

The Evaluate stage uses LLMs as structured diagnostic aggregators — not chatbots. An agentic review system examines each causal estimate against method-specific criteria (randomization integrity, identification assumptions, threats to validity) and produces a confidence score grounded in concrete evidence. The material covers four principles that make this defensible: Groundedness, Correctness, Traceability, and Reproducibility. Participants learn the design patterns (registry dispatch, prompt engineering as software, structured output via `Pydantic`) and run a validation harness that tests stability, backend sensitivity, and severity calibration.

The confidence score flows directly into the allocation stage — penalizing return estimates where evidence is weak. This is what it looks like when Gen AI is embedded in a decision system rather than bolted on.

## Track record

The methodology draws on the causal measurement framework behind Amazon Catalog AI, published in Harvard Business Review (2025). The Impact Engine is the productionized version of that methodology — built on the same design principles, using open-source tools you can run yourself.

## About the instructor

Philipp Eisenhauer works at the intersection of causal inference research and production decision systems. He holds a PhD from the University of Mannheim and was a postdoctoral researcher with James Heckman at the University of Chicago, where they co-authored work published in the Journal of Political Economy. He is an Affiliate Associate Professor at the University of Washington.

At Amazon, he leads the science behind large-scale causal measurement platforms. The framework behind Amazon Catalog AI was published in Harvard Business Review (2025). The Impact Engine is the open-source productionization of that methodology.

## Formats

The material adapts to different audiences and timeframes. All materials are executable Jupyter notebooks.

**University programs.** A 10-week semester course with a pipeline-aligned curriculum. Each week covers one stage of the measurement-to-allocation loop, building toward a capstone project. Students learn to measure causal effects and ship the measurement system as tested, config-driven code. See [Iterations](../iterations/index) for current offerings with institution-specific details.

**Corporate intensives.** Multi-day intensives covering the full pipeline end-to-end, or focused single-day workshops targeting one stage in depth — causal measurement, LLM-based evaluation, or portfolio allocation. Participants leave with working code and a configured pipeline they can adapt to their own measurement problems.

## Get in touch

Interested in how this material could work for your team or program?

Philipp Eisenhauer — [eisenhauer.io](https://eisenhauer.io)

<div style="margin-top: 50px; padding-top: 30px; border-top: 1px solid #e1e4e5; text-align: center;">
<p style="color: #6c757d; font-size: 14px; margin-bottom: 10px;">Powered by</p>
<a href="https://eisenhauerio.github.io/tools-impact-engine-website">
<img src="https://raw.githubusercontent.com/eisenhauerIO/tools-impact-engine-website/main/img/logo-full-light.svg" alt="Impact Engine" style="height: 60px;">
</a>
</div>
