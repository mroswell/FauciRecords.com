"""OCR corrections — source of truth for per-page text fixes.

The OCR/extraction output in site/data/text/ is regenerated (overwritten) by
extract_text.py on every build. This file holds corrections that are applied ON
TOP of that output at build_data time, so they survive every rebuild and are
never clobbered. This is the ONLY place OCR fixes should live — never hand-edit
the generated files in site/data/ or site/documents/.

Format:  CORRECTIONS[page] = [(wrong, right), ...]
  - `page` is the 1-based PDF page number.
  - Each (wrong, right) pair is an exact string replacement applied to the
    reflowed page text (i.e. `wrong` should match what appears on the site).
  - Use enough surrounding context in `wrong` to avoid matching unintended
    occurrences on the same page.

build_data.py warns if any `wrong` string is not found on its page, so stale
corrections (e.g. after an OCR re-run changes the text) surface loudly instead
of silently doing nothing.

Only genuine OCR errors belong here — not the document authors' own typos or
informal spellings, and nothing inside quoted claim text (see the neutral-archive
editorial stance in CLAUDE.md).
"""

CORRECTIONS = {
    # Claim 1, Doc 1 — "If AIDS Went the Way of Smallpox" (email-2009-aids)
    20: [
        ("standpoint, | feel", "standpoint, I feel"),   # pipe misread for "I"
        ("| do not think", "I do not think"),            # pipe misread for "I"
        ("atauci@niaid.nih.gov", "afauci@niaid.nih.gov"),  # "f" misread as "t"
        ("image001 .jpg", "image001.jpg"),               # spurious space
        ("CNE=NIAID", "CN=NIAID"),                       # Exchange address string
    ],
    # Claim 1, Doc 5 — "rand paul tweet" (email-2020-randpaul)
    31: [
        ("he s full of", "he's full of"),               # dropped apostrophe
    ],
}

# Whole-page text replacements. When a page's OCR is too degraded for surgical
# find/replace (e.g. a scanned data table that OCR turned to noise), map the page
# to replacement text here; it fully replaces the reflowed OCR for that page.
# The page image on the site remains the authoritative record either way.
PAGE_OVERRIDES = {
    # Claim 1, Doc 5, p32 — COVID case-count table (Worldometer screenshot in
    # the forwarded email). OCR was unusable; transcribed by hand from the page
    # image at 450 DPI. Country rows are arithmetic-verified (recovered+active+
    # deaths = total cases). Column alignment (2+ spaces) makes the site render
    # each table as a monospace <pre class="tbl"> block.
    32: (
"""USA State   Total Cases      New  Total Deaths   New     Active  Cases/1M  Deaths/1M  Total Tests  Tests/1M
USA Total     3,928,642  +30,092       143,536  +247  1,970,948    11,869        434   48,610,322   146,858
New York        434,633     +469        32,882   +12    156,796    22,342      1,675    5,164,812   265,494
California      391,084                  7,716    +3    278,628     9,898        195    6,286,852   159,112
Florida         360,394  +10,347         5,075   +90    316,879    16,780        236    3,052,106   142,106
Texas           339,210                  4,063          162,211    11,699        140    3,207,857   110,631

 #  Country/Other  Total Cases       New  Total Deaths     New  Recovered     Active  Serious  Cases/1M  Deaths/1M  Total Tests  Tests/1M     Population
    World           14,753,029  +117,477       610,867  +2,298  8,805,686  5,336,476   59,701     1,893       78.4
 1  USA              3,928,642   +30,092       143,536    +247  1,814,158  1,970,948   16,550    11,865        434   48,610,322   146,813    331,102,850
 2  Brazil           2,102,559    +2,663        79,590     +57  1,371,229    651,740    8,318     9,888        374    4,911,063    23,096    212,636,496
 3  India            1,153,824   +35,717        28,099    +596    724,702    401,023    8,944       836         20   14,047,908    10,175  1,380,678,271
 4  Russia             777,486    +5,940        12,427     +85    553,602    211,457    2,300     5,328         85   25,251,614   173,030    145,937,857
 5  South Africa       364,328                   5,033            191,059    168,236      539     6,139         85    2,471,747    41,651     59,344,794
 6  Peru               353,590                  13,187            241,955     98,448    1,293    10,717        400    2,063,240    62,534     32,993,724
 7  Mexico             344,224    +5,311        39,184    +296    217,423     87,617      378     2,668        304      821,922     6,372    128,999,581
 8  Chile              333,029    +2,099         8,633    +130    303,992     20,404    1,764    17,414        451    1,420,390    74,271     19,124,453
 9  Spain              307,335                  28,420                N/A        N/A      617     6,573        608    6,026,446   128,892     46,755,761
10  UK                 295,372      +580        45,312     +12        N/A        N/A      142     4,350        667   13,459,190   198,208     67,904,526
11  Iran               276,202    +2,414        14,405    +217    240,087     21,710    3,583     3,286        171    2,175,217    25,882     84,044,752
12  Pakistan           265,083    +1,587         5,599     +31    205,929     53,555    1,552     1,199         25    1,740,768     7,874    221,084,562
13  Saudi Arabia       253,349    +2,429         2,523     +37    203,259     47,567    2,196     7,272         72    2,728,424    78,315     34,839,236
14  Italy              244,624      +190        35,058     +13    197,162     12,404       47     4,046        580    6,262,302   103,583     60,456,923
"""
    ),
}
