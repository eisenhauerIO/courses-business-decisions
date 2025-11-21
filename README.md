# courses-business-decisions

Course documentation for Business Decisions.

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
