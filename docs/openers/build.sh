#!/usr/bin/env bash
# Render the lecture-opening slides to PDF with headless Chrome.
set -euo pipefail
cd "$(dirname "$0")"
for name in course-framework lecture-structure product-page; do
  google-chrome --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$PWD/$name.pdf" "file://$PWD/$name.html" 2>/dev/null
done
