# AI-Driven Business Decisions

*From Measurement to Impact*

[![Build Documentation](https://github.com/eisenhauerIO/courses-business-decisions/actions/workflows/docs.yml/badge.svg?branch=main)](https://github.com/eisenhauerIO/courses-business-decisions/actions/workflows/docs.yml)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue.svg?logo=github)](https://github.com/eisenhauerIO/courses-business-decisions)
[![CI](https://github.com/eisenhauerIO/courses-business-decisions/actions/workflows/ci.yml/badge.svg)](https://github.com/eisenhauerIO/courses-business-decisions/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Slack](https://img.shields.io/badge/Slack-Join%20Us-4A154B?logo=slack)](https://join.slack.com/t/eisenhauerioworkspace/shared_invite/zt-3lxtc370j-XLdokfTkno54wfhHVxvEfA)

Welcome to the AI-Driven Business Decisions course. This course explores how to leverage AI and data-driven approaches to make better business decisions.

```{todo}
Add more detailed course overview and learning objectives.
```

## Setup

This project uses [Hatch](https://hatch.pypa.io/) for environment and dependency management.

### Installation

1. Install Hatch:
   ```bash
   pip install --user hatch
   ```

2. Ensure `~/.local/bin` is in your PATH:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

### Building Documentation

Build the Sphinx documentation:
```bash
hatch run build
```

The built documentation will be in `docs/build/html/`.

### Serving Documentation Locally

Serve the documentation on `http://localhost:8000`:
```bash
hatch run serve
```

### Cleaning Build Artifacts

Remove the build directory:
```bash
hatch run clean
```

## Development

The project uses direnv for automatic environment activation. If you have direnv installed, run `direnv allow` in the project directory.

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

This project uses a dual-license approach: **MIT License** for code and **CC BY 4.0** for educational content. See [LICENSE.md](https://github.com/eisenhauerIO/courses-business-decisions/blob/main/LICENSE.md) for details.
