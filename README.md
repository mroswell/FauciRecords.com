# The Fauci Records — static archive

A self-contained website presenting the documents released by Chairman Rand Paul
from the July 29, 2026 hearing *"Testimony of Anthony Fauci."* Each of the five
numbered claims links to the primary-source document(s) that support it. Scanned
pages are OCR'd; the original package is split into one PDF per document.

## What's here

```
2026.08.29_Final-Hearing-Document-Release-Package.pdf   # source (unchanged)
build/     # pipeline: PDF -> page images + OCR text + split PDFs + JSON
site/      # the static website (deploy this folder)
```

`site/` is fully static — deploy it to GitHub Pages, Netlify, any web host, or
just open `site/index.html` directly in a browser (`file://` works because the
data is bundled as `site/data/data.js`).

## Rebuilding

Requires the CLI tools `qpdf`, `pdftoppm`, `pdftotext` (poppler), `tesseract`,
and `python3`. Then:

```bash
cd build
./build.sh          # renders pages, OCRs, splits PDFs, writes site/data/*.json
```

The build is idempotent. **`build/manifest.py` is the single source of truth** —
edit it to correct a document boundary, claim wording, or an *Editor's note*, then
re-run `./build.sh`.

## Notes on content

- **Claims** are quoted as stated in the release; the site does not editorialize.
- **Editor's notes** are neutral, dated factual context. They are **hidden by
  default** and shown only when the `show-notes` class is on `<body>` — toggle
  them with the button on the home page, or the deep link `index.html?notes=1`.
  Each note is a discrete `note` field in `manifest.py`, so any note can be
  deleted without affecting anything else.
- **Transcripts** come from OCR on scanned pages (2–20, 32) and text extraction
  on digital pages (21–31). The page scan and downloadable PDF are authoritative.
```
