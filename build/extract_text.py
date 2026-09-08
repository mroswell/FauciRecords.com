"""Extract per-page text: pdftotext for real-text pages, Tesseract OCR otherwise.

Auto-detects which pages need OCR by measuring embedded selectable text.
Writes cleaned text (release stamp stripped) to site/data/text/pNN.txt and
returns a dict {page: {"text": str, "ocr": bool}} when called programmatically.
"""
import os
import re
import json
import subprocess
from config import (
    SOURCE_PDF, PAGES_DIR, TEXT_DIR, TOTAL_PAGES, OCR_DPI,
    OCR_CHAR_THRESHOLD, STAMP_PATTERNS,
)


def _pdftotext(page):
    r = subprocess.run(
        ["pdftotext", "-layout", "-f", str(page), "-l", str(page), SOURCE_PDF, "-"],
        capture_output=True, text=True,
    )
    return r.stdout


def _ocr(page):
    """Render the page at OCR_DPI to a temp PNG and OCR it."""
    tmp = os.path.join(TEXT_DIR, f"_ocr_p{page:02d}")
    subprocess.run(
        ["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(OCR_DPI),
         "-png", "-singlefile", SOURCE_PDF, tmp],
        check=True,
    )
    png = tmp + ".png"
    r = subprocess.run(["tesseract", png, "-", "--psm", "6"],
                       capture_output=True, text=True)
    try:
        os.remove(png)
    except OSError:
        pass
    return r.stdout


def _strip_stamp(text):
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            lines.append("")
            continue
        if any(pat in s for pat in STAMP_PATTERNS):
            continue
        # Lone release-number line (e.g. "96") sitting by itself.
        if re.fullmatch(r"\d{1,4}", s):
            continue
        lines.append(line.rstrip())
    # Collapse 3+ blank lines to 1, trim edges.
    out = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    return out


def _nonspace_len(text):
    return len(re.sub(r"\s+", "", text))


def extract():
    os.makedirs(TEXT_DIR, exist_ok=True)
    result = {}
    for p in range(1, TOTAL_PAGES + 1):
        raw = _pdftotext(p)
        needs_ocr = _nonspace_len(_strip_stamp(raw)) < OCR_CHAR_THRESHOLD
        if needs_ocr:
            raw = _ocr(p)
        text = _strip_stamp(raw)
        with open(os.path.join(TEXT_DIR, f"p{p:02d}.txt"), "w") as fh:
            fh.write(text + "\n")
        result[p] = {"text": text, "ocr": needs_ocr}
        print(f"p{p:02d}: {'OCR ' if needs_ocr else 'text'} {_nonspace_len(text):>5} chars")
    with open(os.path.join(TEXT_DIR, "_pages.json"), "w") as fh:
        json.dump(result, fh, indent=2)
    return result


if __name__ == "__main__":
    extract()
