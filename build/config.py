"""Shared configuration and paths for the build pipeline."""
import os

BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD_DIR)

SOURCE_PDF = os.path.join(ROOT, "2026.08.29_Final-Hearing-Document-Release-Package.pdf")

SITE_DIR = os.path.join(ROOT, "site")
PAGES_DIR = os.path.join(SITE_DIR, "assets", "pages")   # rendered page PNGs
DATA_DIR = os.path.join(SITE_DIR, "data")
TEXT_DIR = os.path.join(DATA_DIR, "text")               # per-page extracted text
DOCS_DIR = os.path.join(SITE_DIR, "documents")          # split per-exhibit PDFs

TOTAL_PAGES = 32

# Render resolution for page images (display) and OCR input.
RENDER_DPI = 150       # display images
OCR_DPI = 220          # higher res improves OCR
THUMB_WIDTH = 240      # thumbnail width in px

# A page is treated as "needs OCR" if its embedded selectable text has fewer
# than this many non-whitespace characters (beyond the repeated release stamp).
OCR_CHAR_THRESHOLD = 300

# Boilerplate stamp lines to strip from extracted text (appear on every page).
STAMP_PATTERNS = [
    "Released by Chairman Rand Paul",
    "Entered into the record by Chairman Rand Paul",
    "at the July 29, 2026 HSGAC Hearing titled,",
    '"Testimony of Anthony Fauci".',
    '"Testimony of Anthony Fauci"',
]
