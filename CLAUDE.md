# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A self-contained static website ("The Fauci Records") presenting the primary-source
documents released by Chairman Rand Paul from the July 29, 2026 HSGAC hearing
*"Testimony of Anthony Fauci."* Five numbered claims each link to the supporting
document(s). Scanned pages are OCR'd; the source packet is split into one PDF per
document.

**Editorial stance is deliberately neutral.** The site presents claims as quoted in
the release and does not editorialize. "Editor's notes" are neutral, dated factual
context, hidden by default. Preserve this stance in any content change.

## Commands

```bash
cd build && ./build.sh          # full rebuild: render → OCR/extract → split → JSON
```

Individual stages (run from `build/`, in this order — each depends on the prior):

```bash
python3 render_pages.py   # PDF pages → assets/pages/pNN.png + thumbnails
python3 extract_text.py   # per-page text (pdftotext, or Tesseract OCR when sparse)
python3 split_pdf.py      # one PDF per exhibit → site/documents/<id>.pdf
python3 build_data.py     # assemble site/data/*.json + data.js (+ mapping sanity check)
```

The build is idempotent. Requires CLI tools: `qpdf`, `pdftoppm`, `pdftotext`
(poppler), `tesseract`, `python3`. No Python package dependencies.

Preview locally: open `site/index.html` directly (`file://` works — data is bundled
as `site/data/data.js`) or serve `site/` over http.

## Architecture

**`build/manifest.py` is the single source of truth.** All content — exhibit
boundaries (1-based PDF page ranges), claim wording, and Editor's notes — lives here.
To correct anything, edit `manifest.py` then re-run `build.sh`. Never hand-edit the
generated files in `site/data/` or `site/documents/`.

Data flow (all paths defined in `build/config.py`):

```
source PDF ──render_pages──▶ site/assets/pages/*.png
           ──extract_text──▶ site/data/text/pNN.txt + _pages.json
           ──split_pdf─────▶ site/documents/<exhibit-id>.pdf
manifest.py + _pages.json ──build_data──▶ site/data/{claims,exhibits,search-index}.json + data.js
```

- `extract_text.py` auto-detects which pages need OCR by measuring embedded
  selectable-text length against `OCR_CHAR_THRESHOLD`, and strips the repeated
  release-stamp boilerplate (`STAMP_PATTERNS` in config).
- `reflow.py` turns OCR/extracted line-broken text into readable paragraphs at
  build_data time (used for both display and search).
- `build_data.py` computes reverse links (exhibit → which claims it supports) and
  emits a warning if any page 2..32 is unmapped or double-mapped by exhibits.

**Frontend is dependency-free vanilla JS.** Every page loads `data/data.js`, which
sets `window.__DATA__` (same content as the JSON files, packaged as a JS global so the
site works from `file://`). `assets/app.js` renders `index.html` (claims + document
grid) and `exhibit.html` (single exhibit via `?id=`); `assets/search.js` powers
`search.html` (client-side tokenize + rank over the search records). There is no build
step for the frontend — edit the HTML/CSS/JS in `site/` directly.

**Editor's notes toggle:** notes render only when `<body>` has the `show-notes` class.
`app.js` reads/writes `localStorage["show-notes"]`; the deep link `?notes=1` / `?notes=0`
forces (and persists) a shareable state. Each note is a discrete `note` field in
`manifest.py`, deletable without side effects.

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which publishes the `site/`
directory to GitHub Pages. Custom domain is `faucirecords.com` (via `site/CNAME`).
`check-domain.sh` is a local-only helper (gitignored) that polls until the domain goes
live.
