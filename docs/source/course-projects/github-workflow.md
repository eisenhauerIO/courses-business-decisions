# GitHub Workflow

This guide covers the standard GitHub workflow for course projects, from initial setup through submission.

## Quick Reference

| Action | Command |
|--------|---------|
| Clone repo | `git clone <url>` |
| Create branch | `git checkout -b branch-name` |
| Stage changes | `git add .` |
| Commit | `git commit -m "message"` |
| Push | `git push origin branch-name` |
| Update from main | `git pull origin main` |

---

## Initial Setup

**1. Fork the repository** (if working on a shared project)

Click "Fork" in the top-right of the GitHub repository page. This creates your own copy.

**2. Clone to your machine**

```bash
git clone https://github.com/YOUR-USERNAME/repo-name.git
cd repo-name
```

---

## The Branch Workflow

Never work directly on `main`. Always create a branch for your work.

**1. Create a new branch**

```bash
git checkout -b your-branch-name
```

Use descriptive names that reflect what you're working on:
- `add-impact-analysis`
- `clean-sales-data`
- `update-visualization`
- `draft-findings-section`

**2. Make your changes**

Edit files, run your analysis, update notebooks.

**3. Stage and commit**

```bash
# Stage all changes
git add .

# Or stage specific files
git add analysis/impact_model.py

# Commit with a clear message
git commit -m "Add regression model for impact estimation"
```

**Commit messages should:**
- Start with a verb (Add, Fix, Update, Remove, Clean)
- Be specific about what changed
- Be under 50 characters for the first line

**4. Push to GitHub**

```bash
git push origin your-branch-name
```

---

## Creating a Pull Request

1. Go to your repository on GitHub
2. Click "Compare & pull request" (appears after pushing)
3. Fill in:
   - **Title**: Clear summary of changes
   - **Description**: What you did and why
4. Click "Create pull request"

Your teammates or instructor can now review your work.

---

## Keeping Your Branch Updated

Before submitting, sync with the latest changes from main:

```bash
# Switch to main
git checkout main

# Pull latest changes
git pull origin main

# Switch back to your branch
git checkout your-branch-name

# Merge main into your branch
git merge main
```

Resolve any conflicts, then push again.

---

## Common Scenarios

### "I made changes on main by accident"

```bash
# Create a branch with your changes
git checkout -b my-changes

# Reset main to match remote
git checkout main
git reset --hard origin/main
```

### "I need to undo my last commit"

```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes entirely
git reset --hard HEAD~1
```

### "My branch has conflicts"

1. Pull the latest main: `git pull origin main`
2. Git will mark conflicts in files with `<<<<<<<` markers
3. Edit files to resolve conflicts
4. Stage resolved files: `git add .`
5. Complete the merge: `git commit`

---

## Reproducibility and GitHub Actions

All course projects must achieve full reproducibility through [GitHub Actions](https://github.com/features/actions) continuous integration. The [repository template](https://github.com/eisenhauerIO/projects-student-template) provides a reference implementation with the standard project structure and CI configuration.

### What Happens When You Push

When you push to GitHub or create a pull request, GitHub Actions automatically runs:

1. GitHub detects your push or PR
2. Actions spins up a fresh virtual machine
3. Your `environment.yml` installs all dependencies
4. Automated tests and checks run
5. You see ✅ (pass) or ❌ (fail) on your PR

Check the "Actions" tab in your repository to see run details and debug failures.

### The environment.yml File

This file defines all software dependencies for the project. GitHub Actions uses it to create a consistent environment that ensures your analysis runs identically on any machine.

```yaml
name: course-project
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pandas
  - numpy
  - scikit-learn
  - matplotlib
  - jupyter
  - pip
  - pip:
    - some-pip-package
```

### Setting Up Your Local Environment

To match the GitHub Actions environment locally:

```bash
# Create environment from file
conda env create -f environment.yml

# Activate it
conda activate course-project

# Update if environment.yml changes
conda env update -f environment.yml --prune
```

### Adding New Dependencies

If your code needs a new package:

1. Add it to `environment.yml`
2. Update your local environment: `conda env update -f environment.yml`
3. Test that everything still works
4. Commit the updated `environment.yml` with your code

**Never install packages manually without updating environment.yml** — your code will fail in GitHub Actions if dependencies aren't declared.

### Long-Running Computations

When code execution spans multiple hours, you can pre-compute results and load them during CI runs. If you take this approach, include notebook explanations detailing why pre-computation is necessary and how the results were generated.

---

## Project Submission Checklist

Before creating your pull request:

- [ ] Code runs without errors
- [ ] All notebooks execute top-to-bottom
- [ ] Results are reproducible
- [ ] Commit messages are clear
- [ ] Branch is up-to-date with main
- [ ] GitHub Actions checks pass ✅
- [ ] New dependencies added to `environment.yml`

---

## Useful Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# See what changed
git diff

# Discard local changes to a file
git checkout -- filename

# List branches
git branch -a

# Delete a local branch
git branch -d branch-name
```

---

## Getting Help

- `git help <command>` — Built-in documentation
- [GitHub Docs](https://docs.github.com) — Official guides

**Remember:** Commit early, commit often. Small, focused commits are easier to review and debug than large, sweeping changes.
