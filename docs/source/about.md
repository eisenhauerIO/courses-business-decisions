# Impact-Driven Business Decisions

*A course built on a production decision system — not slides about one.*

---

Organizations spend millions on initiatives without a reliable way to answer three questions: Did it work? How confident are we? Where should we invest next? Most analytics training treats these as separate problems. They aren't. They're stages of one loop — and this course teaches participants to operate it.

The methodology draws on the causal measurement framework behind Amazon Catalog AI, published in Harvard Business Review (2025). This course makes that approach accessible — built on the same design principles, using open-source tools you can run yourself.

## The system behind the course

The course is built on the [Impact Engine](https://eisenhauerio.github.io/tools-impact-engine-website) — an open-source Python ecosystem that runs a complete measurement-to-allocation pipeline in a single call. Four components, each independently tested and deployable:

- **Measure** — Estimate causal impact using rigorous econometric methods (synthetic control, difference-in-differences, causal forests, and more)
- **Evaluate** — Score how much to trust each estimate using an LLM-powered quality assurance system that applies structured diagnostics to measurement artifacts
- **Allocate** — Determine where to invest using portfolio optimization under uncertainty
- **Orchestrate** — Wire the full loop together: config in, decision out

Every lecture is a Jupyter notebook that executes against this infrastructure. Participants run the pipeline on a realistic business problem (product data quality in large-scale online retail) and see how the output of each stage feeds the next.

## Gen AI as quality assurance

Most Gen AI courses teach prompting. This course teaches participants to build production-grade AI systems that do real analytical work.

The Evaluate stage uses LLMs as structured diagnostic aggregators — not chatbots. An agentic review system examines each causal estimate against method-specific criteria (randomization integrity, identification assumptions, threats to validity) and produces a confidence score grounded in concrete evidence. The course covers four principles that make this defensible: Groundedness, Correctness, Traceability, and Reproducibility. Participants learn the design patterns (registry dispatch, prompt engineering as software, structured output via Pydantic) and run a validation harness that tests stability, backend sensitivity, and severity calibration.

The confidence score flows directly into the allocation stage — penalizing return estimates where evidence is weak. This is what it looks like when Gen AI is embedded in a decision system rather than bolted on.

## What makes this different

**One framework, not a toolbox.** The course follows a single principle — *Learn, Decide, Repeat* — that connects every method into an operational loop. The curriculum mirrors the pipeline: Measure, Evaluate, Allocate, repeat. One applied domain throughout, one coherent point of view, no context-switching.

**Everything runs — and it's real.** The Impact Engine isn't courseware. It's a config-driven, CI/CD-tested ecosystem with protocol-based interfaces and pluggable components. Swap an estimation method by changing one YAML line. Add a decision rule by writing one adapter class. Participants experience what production-grade science infrastructure looks like from the inside.

## Delivery

Runs as a full 10-week university course. Adapts to multi-day intensives or focused workshops.

## About the instructor

Philipp Eisenhauer built the causal measurement framework behind Amazon Catalog AI (Harvard Business Review, 2025), co-authored with James Heckman (Journal of Political Economy), and designed the Impact Engine as the productionized version of that methodology. He teaches at the University of Washington.

## Get in touch

Interested in how this material could work for your team or program?

Philipp Eisenhauer — [eisenhauer.io](https://eisenhauer.io)

<div style="margin-top: 50px; padding-top: 30px; border-top: 1px solid #e1e4e5; text-align: center;">
<p style="color: #6c757d; font-size: 14px; margin-bottom: 10px;">Powered by</p>
<a href="https://peisenha.github.io/" style="text-decoration: none; color: #6c757d; font-size: 13px; font-weight: 500;">
Impact Engine
</a>
</div>
