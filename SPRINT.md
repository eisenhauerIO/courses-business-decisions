# Autumn 2026 launch

**Status**: complete

## Goal

Prepare the course site and repo for the Autumn 2026 delivery of ECON 481A at the
University of Washington. Related to BACKLOG Phase 0 — Polish.

## Scope

**In scope**:
- Iteration pages: archive Winter 2026, add Autumn 2026
- Catch upstream tool breakage early (tools are developed alongside the course)
- Bring CLAUDE.md and DESIGN.md in line with the current workspace layout
- Check external links on student-facing pages

**Out of scope**:
- Lecture content changes
- Changes to the tool repos
- Phase 1 — Productize

## Observations

### 1. Iteration page still describes Winter 2026

`iterations/econ-481A-uw-2026.md` is the only iteration page and gives a March 20
project deadline.

### 2. Tool dependencies track `main`

All four tools are installed from unpinned GitHub `main`. Any push to a tool repo
can break a lecture on the next site build mid-term.

### 3. Root docs reference a removed layout

CLAUDE.md and DESIGN.md point to `_external/` and `.claude/subagents/`, which no
longer exist, and omit `impact-engine-allocate`.

### 4. External links unverified since last term

The Slack invite, student template repo, and guest links have not been checked
since Winter 2026.

## Decisions

### 1. Iteration page still describes Winter 2026

Keep a single `iterations/index.md` with the current delivery's details (project due
date December 15th) and a table of past iterations. Delete the per-term pages.

### 2. Tool dependencies track `main`

Keep tracking `main`: the tools are developed as the course progresses. Add a nightly
scheduled run of `docs.yml` so a tool change that breaks a lecture fails CI within a
day, even without a course push.

### 3. Root docs reference a removed layout

Point CLAUDE.md at the workspace `../../tools/` clones, drop subagents, add
`impact-engine-allocate` to CLAUDE.md and DESIGN.md.

### 4. External links unverified since last term

Run the link check from `bdc-review-course` and fix anything broken. The paper
link to `eisenhauer.io` (domain gone) points to the public Drive PDF of the paper.

## Plan

1. Collapse iteration pages into `iterations/index.md` with a past-iterations table — done
2. Update CLAUDE.md and DESIGN.md — done
3. Add nightly scheduled docs build — done
4. Run link check and fix broken links — done (Slack invite confirmed by hand)
5. Set the project due date — done (December 15th, 11:59 PM PST)

## Files modified

- `docs/source/iterations/econ-481A-uw-2026.md` — deleted
- `docs/source/iterations/index.md` — current delivery (due December 15th) plus past-iterations table
- `docs/source/allocate-resources/01-portfolio-optimization/lecture.ipynb` — paper link
- `CLAUDE.md` — architecture, dependencies, push-to-main verification, conventions
- `DESIGN.md` — architecture diagram, configuration table, nightly build
- `.github/workflows/docs.yml` — nightly schedule trigger

## Verification

1. `hatch run ruff check .` — pass
2. `hatch run build` — pass
3. CI (ci.yml, docs.yml) green on main
