import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'Business Decisions — Course'
author = 'eisenhauerIO'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',
    'nbsphinx',
]
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
