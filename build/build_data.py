"""Assemble the JSON the front end consumes: claims, exhibits, and a search index.

Reads the per-page extracted text produced by extract_text.py and joins it with
the manifest. Also computes reverse links (which claims each exhibit supports).
"""
import os
import re
import json
from config import DATA_DIR, TEXT_DIR, TOTAL_PAGES
from manifest import META, EXHIBITS, CLAIMS
from reflow import reflow_text


def _load_pages():
    path = os.path.join(TEXT_DIR, "_pages.json")
    with open(path) as fh:
        raw = json.load(fh)
    # keys come back as strings from JSON; reflow the raw line-broken text into
    # readable paragraphs for display and search
    pages = {}
    for k, v in raw.items():
        pages[int(k)] = {"text": reflow_text(v["text"]), "ocr": v["ocr"]}
    return pages


def _exhibit_pages(ex, pages):
    first, last = ex["pages"]
    out = []
    for p in range(first, last + 1):
        info = pages.get(p, {"text": "", "ocr": False})
        out.append({
            "page": p,
            "img": f"assets/pages/p{p:02d}.png",
            "thumb": f"assets/pages/p{p:02d}-thumb.png",
            "text": info["text"],
            "ocr": info["ocr"],
        })
    return out


def build():
    os.makedirs(DATA_DIR, exist_ok=True)
    pages = _load_pages()

    # reverse map: exhibit id -> claim numbers it supports
    exhibit_to_claims = {}
    for claim in CLAIMS:
        for fact in claim["facts"]:
            for ex_id in fact["exhibits"]:
                exhibit_to_claims.setdefault(ex_id, set()).add(claim["number"])

    exhibits_out = []
    for ex in EXHIBITS:
        ex_pages = _exhibit_pages(ex, pages)
        exhibits_out.append({
            "id": ex["id"],
            "title": ex["title"],
            "kind": ex["kind"],
            "date": ex["date"],
            "release": ex["release"],
            "summary": ex["summary"],
            "pdf": f"documents/{ex['id']}.pdf",
            "pageRange": ex["pages"],
            "pages": ex_pages,
            "claims": sorted(exhibit_to_claims.get(ex["id"], [])),
            "fullText": "\n\n".join(p["text"] for p in ex_pages),
        })

    with open(os.path.join(DATA_DIR, "exhibits.json"), "w") as fh:
        json.dump({"meta": META, "exhibits": exhibits_out}, fh, indent=2, ensure_ascii=False)

    with open(os.path.join(DATA_DIR, "claims.json"), "w") as fh:
        json.dump({"meta": META, "claims": CLAIMS}, fh, indent=2, ensure_ascii=False)

    # --- search index: flat records the client tokenizes + ranks -----------------
    records = []
    for claim in CLAIMS:
        facts_text = " ".join(f["text"] for f in claim["facts"])
        records.append({
            "ref": claim["id"],
            "kind": "claim",
            "title": f"Claim {claim['number']}: {claim['headline']}",
            "subtitle": "Claim",
            "url": f"index.html#{claim['id']}",
            "text": f"{claim['headline']} {claim['body']} {facts_text}",
        })
    for ex in exhibits_out:
        records.append({
            "ref": ex["id"],
            "kind": "exhibit",
            "title": ex["title"],
            "subtitle": f"{ex['kind'].title()} · {ex['date']}",
            "url": f"exhibit.html?id={ex['id']}",
            "text": f"{ex['title']} {ex['summary']} {ex['fullText']}",
        })
    with open(os.path.join(DATA_DIR, "search-index.json"), "w") as fh:
        json.dump({"records": records}, fh, indent=2, ensure_ascii=False)

    # --- data.js: same data as a JS global so the site works from file:// too ----
    bundle = {
        "meta": META,
        "claims": CLAIMS,
        "exhibits": exhibits_out,
        "search": records,
    }
    with open(os.path.join(DATA_DIR, "data.js"), "w") as fh:
        fh.write("window.__DATA__ = ")
        json.dump(bundle, fh, ensure_ascii=False)
        fh.write(";\n")

    print(f"wrote exhibits.json ({len(exhibits_out)} exhibits), claims.json "
          f"({len(CLAIMS)} claims), search-index.json ({len(records)} records), data.js")

    # sanity: every page 1..TOTAL_PAGES covered by exactly one exhibit
    covered = {}
    for ex in EXHIBITS:
        for p in range(ex["pages"][0], ex["pages"][1] + 1):
            covered[p] = covered.get(p, 0) + 1
    missing = [p for p in range(2, TOTAL_PAGES + 1) if p not in covered]
    dupes = [p for p, c in covered.items() if c > 1]
    if missing:
        print(f"  WARNING: pages not mapped to any exhibit: {missing}")
    if dupes:
        print(f"  WARNING: pages mapped to multiple exhibits: {dupes}")


if __name__ == "__main__":
    build()
