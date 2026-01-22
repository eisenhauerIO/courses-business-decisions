# Course Projects

Course projects provide hands-on experience applying the methods and tools covered in this course to real-world problems. Students work on either replication projects or [Kaggle](https://www.kaggle.com/) competitions, developing practical skills in causal inference, data analysis, and reproducible research. All projects use the [repository template](https://github.com/eisenhauerIO/projects-student-template) which provides the standard project structure, GitHub Actions configuration, and setup instructions.

## Project Types

***Replication Projects:*** Students reproduce key results from published research articles, critically assess the quality of the original analysis, and contribute independent extensions such as robustness checks or alternative specifications.

***Kaggle Projects:*** Students participate in data science competitions on Kaggle, document the competition context and evaluation metrics, and develop solution strategies through iterative experimentation and parameter tuning.

## Example Project

### Lindo et al. (2010): Academic Probation and Student Outcomes

This [replication project](https://ose-course-projects.readthedocs.io/en/latest/projects/index.html) by Annica Gehlen replicates {cite:t}`Lindo_2010`, examining the effects of academic probation on student outcomes using a regression discontinuity design. The analysis demonstrates how negative incentives influence performance and dropout decisions at a large Canadian university.

## Frequently Asked Questions

**Why are the projects public?** Transparency and reproducibility are core values in research and we want to learn from each other.

**What are the reproducibility requirements?** All projects must achieve full reproducibility through [GitHub Actions](https://github.com/features/actions) continuous integration. The [repository template](https://github.com/eisenhauerIO/projects-student-template) provides a reference implementation. When code execution spans multiple hours, you can pre-compute results and load them during CI runs—but you must include notebook explanations detailing why this approach is necessary.

**Where can I find research data?** Some journals offer data supplements on their websites. Useful compilations include the [Harvard Dataverse](https://dataverse.harvard.edu/), [MDRC Public-Use Files](https://www.mdrc.org/available-public-use-files), [UC Irvine Machine Learning Repository](https://archive.ics.uci.edu/), and [Google Dataset Search](https://datasetsearch.research.google.com/).

**Do we get to present our projects at the end of the course?** Yes, if you would like feedback on your project, make sure to reach out.
