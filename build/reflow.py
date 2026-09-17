"""Reflow line-broken OCR / pdftotext output into readable paragraphs.

OCR and `pdftotext` emit a hard line break at the end of every *visual* line, so
wrapped sentences look broken. This joins wrapped prose lines back into flowing
paragraphs while preserving the breaks that should stay:

  * email header lines ("From:", "To:", "Subject:", ...) — kept one per line
  * columnar / table rows (two or more runs of 2+ spaces) — the whole table
    block is kept verbatim
  * signature / short list lines — kept one per line, stacked tightly
  * genuine paragraph ends — detected because the last line of a paragraph does
    not reach the right margin (it is shorter than the block's fill width)

Real paragraphs are separated by a blank line; tightly-stacked runs (headers,
signatures, table rows) are not. Hyphenated word-wraps ("inter-\nagency") are
de-hyphenated; hyphens before a digit ("COVID-\n19") keep the hyphen.
"""
import re

# "Label: value" at the very start of a line (email headers, field labels).
HEADER_RE = re.compile(r"^[A-Za-z][\w .\-/]{0,24}:\s")


def _columnar(line):
    """Two or more columns separated by runs of 2+ spaces => tabular row."""
    return len(re.findall(r"\S {2,}", line)) >= 2


def reflow_text(text):
    lines = text.split("\n")

    # fill width is judged from prose lines only, so a wide table can't skew it
    prose_lens = [len(l.rstrip()) for l in lines
                  if l.strip() and not _columnar(l) and not HEADER_RE.match(l)]
    maxlen = max(prose_lens) if prose_lens else 70
    threshold = max(40, min(78, int(maxlen * 0.70)))

    # segments: list of (kind, text); kind in {"para", "short", "verb"}
    segments = []
    cur = []

    def flush():
        if cur:
            joined = " ".join(cur)
            kind = "para" if len(joined) >= threshold else "short"
            segments.append((kind, joined))
            cur[:] = []

    in_table = False
    for raw in lines:
        line = raw.rstrip()
        if line.strip() == "":
            flush()
            in_table = False
            continue

        # once inside a table block, keep every line verbatim until a blank line
        if in_table:
            flush()
            segments.append(("verb", line))
            continue
        if HEADER_RE.match(line):
            flush()
            segments.append(("verb", line))
            continue
        if _columnar(line):
            flush()
            segments.append(("verb", line))
            in_table = True
            continue

        # prose line: join into the current paragraph
        s = line.strip()
        if cur and cur[-1].endswith("-"):
            prev = cur[-1]
            cur[-1] = prev[:-1] + s if s[:1].islower() else prev + s
        else:
            cur.append(s)
        if len(s) < threshold:   # short physical line ends the paragraph
            flush()
    flush()

    # assemble: a blank line only around real paragraphs; structural runs
    # (headers, signatures, table rows, short list lines) stay tightly stacked
    out = []
    prev_kind = None
    for kind, txt in segments:
        if prev_kind is not None and (kind == "para" or prev_kind == "para"):
            out.append("")
        out.append(txt)
        prev_kind = kind

    result = "\n".join(out)
    result = re.sub(r"\n{3,}", "\n\n", result).strip()
    return result


# Terminal punctuation that legitimately ends a paragraph. A trailing hyphen is
# included because reflow keeps "COVID-\n19"-style hyphens, and enumerated list
# items end in ";" — both should stay as separate blocks, not be merged.
_TERMINAL = (".", ";", ":", "!", "?", '"', "”", "’", ")", "]", "-")


def _is_marking(s):
    """A standalone classification marking line (e.g. 'UNCLASSIFIED//FOUO')."""
    return "CLASSIFIED" in s and len(s.split()) <= 3


def repair_paragraphs(text):
    """Heal spurious paragraph breaks left by blank lines in the extracted text.

    `reflow_text` (and pdftotext on double-spaced source pages) can split a single
    paragraph at a stray blank line. This joins two blocks back together ONLY when
    the first ends without terminal punctuation AND the second begins lowercase —
    the reliable signature of a mid-sentence split. It never splits a paragraph,
    and it leaves classification markings, ALL-CAPS headings, and enumerated list
    items (which end in ";") untouched.

    Run this AFTER corrections are applied: some correction strings contain
    intentional blank lines that must still match the reflowed text.
    """
    paras = text.split("\n\n")
    out = []
    for p in paras:
        if out:
            prev = out[-1].rstrip().split("\n")[-1].rstrip()
            first = p.lstrip().split("\n")[0]
            if (prev and first and prev[-1] not in _TERMINAL
                    and re.match(r"[a-z]", first)
                    and not _is_marking(prev) and not _is_marking(first)
                    and not prev.isupper()):
                out[-1] = out[-1].rstrip() + " " + p.lstrip()
                continue
        out.append(p)
    return "\n\n".join(out)
