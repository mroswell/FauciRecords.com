"""Split the source PDF into one PDF per exhibit (the "split by item" deliverable)."""
import os
import subprocess
from config import SOURCE_PDF, DOCS_DIR
from manifest import EXHIBITS


def split():
    os.makedirs(DOCS_DIR, exist_ok=True)
    for ex in EXHIBITS:
        first, last = ex["pages"]
        out = os.path.join(DOCS_DIR, f"{ex['id']}.pdf")
        subprocess.run(
            ["qpdf", SOURCE_PDF, "--pages", SOURCE_PDF, f"{first}-{last}", "--", out],
            check=True,
        )
        print(f"{ex['id']}.pdf  (pages {first}-{last})")


if __name__ == "__main__":
    split()
