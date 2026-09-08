"""Render every PDF page to a display PNG + thumbnail.

Uses poppler's pdftoppm (display images) and produces a downscaled thumbnail
via a second pdftoppm pass at a lower scale. No Python imaging deps required.
"""
import os
import subprocess
from config import SOURCE_PDF, PAGES_DIR, TOTAL_PAGES, RENDER_DPI, THUMB_WIDTH


def render():
    os.makedirs(PAGES_DIR, exist_ok=True)
    for p in range(1, TOTAL_PAGES + 1):
        out = os.path.join(PAGES_DIR, f"p{p:02d}")
        # Full display image at RENDER_DPI.
        subprocess.run(
            ["pdftoppm", "-f", str(p), "-l", str(p), "-r", str(RENDER_DPI),
             "-png", "-singlefile", SOURCE_PDF, out],
            check=True,
        )
        # Thumbnail scaled to fixed pixel width.
        thumb = os.path.join(PAGES_DIR, f"p{p:02d}-thumb")
        subprocess.run(
            ["pdftoppm", "-f", str(p), "-l", str(p), "-scale-to-x", str(THUMB_WIDTH),
             "-scale-to-y", "-1", "-png", "-singlefile", SOURCE_PDF, thumb],
            check=True,
        )
        print(f"rendered p{p:02d}")


if __name__ == "__main__":
    render()
