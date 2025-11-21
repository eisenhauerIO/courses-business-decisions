import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# Ensure pandoc is available for nbconvert/nbsphinx conversions.
# If the system pandoc binary is missing, try to download one via pypandoc.
try:
    import pypandoc
    try:
        # Will raise OSError if no pandoc binary is available
        pypandoc.get_pandoc_version()
    except OSError:
        try:
            pypandoc.download_pandoc()
            # Ensure the downloaded pandoc binary is on PATH so nbconvert can find it.
            try:
                pandoc_path = pypandoc.get_pandoc_path()
                pandoc_dir = os.path.dirname(pandoc_path)
                os.environ.setdefault('PYPANDOC_PANDOC', pandoc_path)
                os.environ['PATH'] = pandoc_dir + os.pathsep + os.environ.get('PATH', '')
            except Exception:
                # If we can't determine the downloaded path, continue and allow
                # the later Sphinx build to raise a clear error.
                pass
        except Exception:
            # Fall back to a helpful message during the Sphinx build.
            print("Warning: pandoc not found and automatic download failed.\n"
                  "Install pandoc manually: https://pandoc.org/installing.html")
except Exception:
    # pypandoc isn't installed; the build environment may still provide pandoc.
    # If not, Sphinx will raise an error later; leaving a friendly hint here.
    pass

project = 'Business Decisions — Course'
author = 'eisenhauerIO'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',
    'nbsphinx',
]
templates_path = ['_templates']
exclude_patterns = ['_build']
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
# Do not list `lectures` in `html_extra_path` so notebooks are processed by nbsphinx
# (they will be rendered into HTML). If you also want raw `.ipynb` files copied
# for direct download, add a separate copy step or an alternate path.
html_extra_path = []

# nbsphinx settings: allow notebooks with execution errors to build the docs
nbsphinx_allow_errors = True
