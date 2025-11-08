# Business Decisions Course

A comprehensive course on business decision-making presented as Sphinx documentation.

## Overview

This course provides comprehensive coverage of business decision-making processes, analytical frameworks, and practical applications for modern business environments. All content is structured as professional documentation using Sphinx.

## Course Modules

1. **Introduction to Business Decisions** - Foundational concepts and principles
2. **Decision-Making Frameworks** - Structured approaches including SWOT, decision trees, and cost-benefit analysis
3. **Data Analysis for Decisions** - Using data analytics to inform business choices
4. **Risk Management** - Understanding and managing business risks
5. **Case Studies** - Real-world applications and examples

## Building the Documentation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/eisenhauerIO/courses-business-decisions.git
cd courses-business-decisions
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Build the Documentation

To build the HTML documentation:

```bash
make html
```

The generated documentation will be in `docs/build/html/`. Open `docs/build/html/index.html` in your web browser to view the course.

### Other Build Formats

Sphinx supports multiple output formats:

```bash
make latexpdf  # Build PDF documentation (requires LaTeX)
make epub      # Build EPUB documentation
make man       # Build man pages
make text      # Build plain text documentation
```

To see all available build targets:
```bash
make help
```

### Development

To automatically rebuild documentation when files change, you can use sphinx-autobuild:

```bash
pip install sphinx-autobuild
sphinx-autobuild docs/source docs/build/html
```

Then open http://127.0.0.1:8000 in your browser.

## Documentation Structure

```
courses-business-decisions/
├── docs/
│   ├── source/
│   │   ├── conf.py              # Sphinx configuration
│   │   ├── index.rst            # Main documentation entry point
│   │   ├── modules/             # Course modules
│   │   │   ├── introduction.rst
│   │   │   ├── decision_frameworks.rst
│   │   │   ├── data_analysis.rst
│   │   │   ├── risk_management.rst
│   │   │   └── case_studies.rst
│   │   ├── _static/             # Static files (CSS, images)
│   │   └── _templates/          # Custom templates
│   └── build/                   # Generated documentation (gitignored)
├── Makefile                     # Build automation
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Contributing

Contributions to improve the course content are welcome! Please ensure that:

1. Content follows the existing structure and style
2. reStructuredText formatting is correct
3. Documentation builds without errors (`make html`)

## License

This course content is provided for educational purposes.