# Autumn 2026 launch

**Status**: executing

## Goal

Prepare the course site and repo for the Autumn 2026 delivery of ECON 481A at the
University of Washington. Related to BACKLOG Phase 0 — Polish.

## Scope

**In scope**:
- Iteration pages: archive Winter 2026, add Autumn 2026
- Pin tool dependencies for the duration of the term
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

Rename to `2026-winter-uw-econ-481A.md` and add `2026-autumn-uw-econ-481A.md` with
the same content and project due date TBD.

### 2. Tool dependencies track `main`

Pin each tool to its current commit SHA for the term.

### 3. Root docs reference a removed layout

Point CLAUDE.md at the workspace `../../tools/` clones, drop subagents, add
`impact-engine-allocate` to CLAUDE.md and DESIGN.md.

### 4. External links unverified since last term

Run the link check from `bdc-review-course` and fix anything broken.

## Plan

1. Rename winter iteration page, add autumn page, update toctree — done
2. Update CLAUDE.md and DESIGN.md — done
3. Pin tool dependencies in `pyproject.toml` to commit SHAs
4. Run link check and fix broken links
5. Set the project due date once known

## Files modified

- `docs/source/iterations/2026-winter-uw-econ-481A.md` — renamed from `econ-481A-uw-2026.md`
- `docs/source/iterations/2026-autumn-uw-econ-481A.md` — new, due date TBD
- `docs/source/iterations/index.md` — toctree
- `CLAUDE.md` — architecture, dependencies, verification, conventions
- `DESIGN.md` — architecture diagram, configuration table

## Verification

1. `hatch run ruff check .` — pass
2. `hatch run build` — pass
3. CI (ci.yml, docs.yml) green on the PR
