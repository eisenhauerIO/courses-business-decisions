# Projects

Course projects provide hands-on experience applying the methods and tools covered in this course to real-world problems. Students work on either replication projects or [Kaggle](https://www.kaggle.com/) competitions, developing practical skills in causal inference, data analysis, and reproducible research. All projects use the [repository template](https://github.com/eisenhauerIO/projects-student-template) which provides the standard project structure, GitHub Actions configuration, and setup instructions.

## Project types

***Replication Projects:*** Students reproduce key results from published research articles, critically assess the quality of the original analysis, and contribute independent extensions such as robustness checks or alternative specifications.

***Kaggle Projects:*** Students participate in data science competitions on Kaggle, document the competition context and evaluation metrics, and develop solution strategies through iterative experimentation and parameter tuning.

## Example project

### Lindo et al. (2010): Academic Probation and Student Outcomes

This replication project by Annica Gehlen replicates {cite:t}`Lindo_2010`, examining the effects of academic probation on student outcomes using a regression discontinuity design. The analysis demonstrates how negative incentives influence performance and dropout decisions at a large Canadian university. The [project notebook](https://ose-course-projects.readthedocs.io/en/latest/projects/Lindo_et_al_2010/project.html) guides the reader through the analysis and reasoning for each step, supported by a clear README and a GitHub Actions workflow that ensures end-to-end reproducibility.

## Frequently asked questions

**Why are the projects public?** Transparency and reproducibility are core values in research and we want to learn from each other.

**What does the typical workflow look like?** See the [GitHub Workflow](github-workflow) guide for the standard workflow from initial setup through submission, including branching, pull requests, and reproducibility requirements.

**What is the scope of replication?** For replication projects, focus on reproducing the core results and main findings of the original paper. You do not need to replicate every table, figure, or robustness check—prioritize the central analyses that support the paper's key conclusions.

**Where can I find research data?** Some journals offer data supplements on their websites. Useful compilations include the [Harvard Dataverse](https://dataverse.harvard.edu/), [MDRC Public-Use Files](https://www.mdrc.org/available-public-use-files), [UC Irvine Machine Learning Repository](https://archive.ics.uci.edu/), and [Google Dataset Search](https://datasetsearch.research.google.com/).

**Do we get to present our projects at the end of the course?** Yes, if you would like feedback on your project, make sure to reach out.

```{toctree}
:hidden:

github-workflow
```
