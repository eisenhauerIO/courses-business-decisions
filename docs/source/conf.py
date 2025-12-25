import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Business Decisions — Course'
author = 'eisenhauerIO'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.extlinks',
    'myst_parser',
    'nbsphinx',
    'sphinxcontrib.bibtex',
]

# External links shortcuts
extlinks = {
    'repo': ('https://github.com/eisenhauerIO/courses-business-decisions/%s', '%s'),
}

# Show TODO items locally, hide in production builds
todo_include_todos = os.environ.get('SPHINX_PROD', '0') != '1'

# Bibliography configuration
bibtex_bibfiles = ['references.bib']
# Accept Markdown files as source as well as reStructuredText
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
templates_path = ['_templates']
exclude_patterns = ['build']
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
# Do not list `lectures` in `html_extra_path` so notebooks are processed by nbsphinx
# (they will be rendered into HTML). If you also want raw `.ipynb` files copied
# for direct download, add a separate copy step or an alternate path.
html_extra_path = []

# nbsphinx settings: execute notebooks during build
nbsphinx_execute = 'always'
nbsphinx_allow_errors = False

# Add Colab badge to notebooks
nbsphinx_prolog = """
.. raw:: html

    <a href="https://colab.research.google.com/github/eisenhauerIO/courses-business-decisions/blob/main/docs/source/{{ env.doc2path(env.docname, base=None) }}">
        <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
    </a>
"""
