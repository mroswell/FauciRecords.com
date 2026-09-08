#!/usr/bin/env bash
# Full build: render pages, extract/OCR text, split PDFs, assemble JSON.
# Idempotent — safe to re-run after editing manifest.py.
set -euo pipefail
cd "$(dirname "$0")"

echo "==> [1/4] Rendering page images"
python3 render_pages.py

echo "==> [2/4] Extracting text (OCR where needed)"
python3 extract_text.py

echo "==> [3/4] Splitting PDF by exhibit"
python3 split_pdf.py

echo "==> [4/4] Building JSON data + search index"
python3 build_data.py

echo "==> Done."
