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
    # Claim 2, Doc 1 — CIA/WCPMC memo (memo-wcpmc-fauci); all scan-verified.
    # "SARS COV-2" left as-is: the document's own formatting, not OCR.
    19: [
        ("National institute of Allergy", "National Institute of Allergy"),
        ("Or. Fauci and CIA experts", "Dr. Fauci and CIA experts"),
        ("Or. Fauci expressed concern", "Dr. Fauci expressed concern"),
        ("epidemiclogical", "epidemiological"),
        ("natura! reservoir", "natural reservoir"),
        ("suggested the iC connect", "suggested the IC connect"),
        ("fall of 2019, He encouraged", "fall of 2019. He encouraged"),
        ("COVID-19 Infection", "COVID-19 infection"),
        ("public health channels,", "public health channels."),
    ],
    # Claim 3, Doc 1 — CIA Bioforensics SOW (sow-bioforensics), word-level fixes.
    # Left as original-document typos per user: #1 Biologicial, #2 Centeral, #23 "the the".
    # #8 reflects a redaction; #14 collapses a garbled span. Punctuation (#31-37),
    # stamp fragments (#38-39), and garbled/redacted blocks (#40-43) still pending.
    2: [
        ("To mect the", "To meet the"),                       # #3
        ("scicntific", "scientific"),                          # #4
        ("NLAD", "NIAID"),                                     # #5
        ("cfforts", "efforts"),                                # #6
        ("29 SCOPE", "2.9 SCOPE"),                             # #7 (per user's read of scan)
        ("at thei level", "at the [redacted] level"),          # #8
        ("(ITIC), Currently", "(ITIC). Currently"),            # #31
        ("such technique", "such as technique"),               # #33  (#32 skipped: original)
    ],
    3: [
        ("transfer LAA", "transfer IAA"),                      # #9
        ("mecting", "meeting"),                                # #10
        ("of [AA award", "of IAA award"),                      # #11
        ("shal]", "shall"),                                    # #12
        ("routual", "mutual"),                                 # #13
    ],
    4: [
        ("This task y/\nthis Tepresents", "This task represents"),  # #14
        ("of [AA NIAID", "of IAA NIAID"),                      # #15
        ("goverment", "government"),                           # #16
        ("thesc", "these"),                                    # #17
        ("onc electronic", "one electronic"),                  # #18
        ("shal!", "shall"),                                    # #19 (x2)
        ("shal]", "shall"),                                    # #20
        ("comparisons, Where", "comparisons. Where"),          # #34
        ("questions, This task", "questions. This task"),      # #35
        ("requested, The", "requested. The"),                  # #36
        # #38 remove garbled stamp remnant (the canonical stamp now renders as a header)
        (".- Entered into the record by Chairman Rand\n", ""),
    ],
    5: [
        ("44 Progress", "4.4 Progress"),                       # #21
        ("delieverables", "deliverables"),                     # #22
        ("uscd", "used"),                                      # #24
        ("using CLA funds", "using CIA funds"),                # #25a
        ("of the CLA. NIAID", "of the CIA. NIAID"),            # #25b
        ("inform the CLA of", "inform the CIA of"),            # #25c
        ("under this LAA", "under this IAA"),                  # #26
        ("tegulation", "regulation"),                          # #27
        ("Alj other", "All other"),                            # #28
        ("{government)", "(government)"),                       # #37
        # #39 remove garbled stamp remnant (canonical stamp now renders as a header)
        (". Entered into the record by Chairman Rand\n", ""),
    ],
    6: [
        ("NIAD Points", "NIAID Points"),                       # #29
        ("Infectious Discases", "Infectious Diseases"),        # #30
    ],
    # Claim 3, Doc 2 — Non-disclosure clause (iaa-nondisclosure), p7.
    7: [
        ("of the CLA.", "of the CIA."),                        # #1
        ("\n\n|", ""),                                         # #2 stray page-edge pipe
    ],
    # Claim 3, Doc 3 — D&F Memorandum (df-memo), p8-9. #6-7 skipped: document's own
    # wording ("Finding", "Infectious Disease"). Garbled blocks reconstructed with
    # [signature]/[redacted]; ATP title reconstructed from its own defined acronym.
    8: [
        ("{U)", "(U)"),                                        # #1 brace->paren
        ("[X}", "[X]"),                                        # #2 checkbox
        ("Request Number ——", "Request Number [redacted]"),   # #8
        ("\n\na el", ""),                                      # #9 stray artifact
    ],
    9: [
        ("{] b.", "[ ] b."),                                  # #3 empty checkbox
        ("‘The servicing", "The servicing"),                  # #4 stray quote
        ("[ } c.", "[ ] c."),                                 # #5 checkbox
        ("oe a a 7 Date\nDST/ATP/BTC\n[ee Date OS™\nChief\nDST/ATP Contracts\nirector o rea  echnologies\nand Programs (ATP)",
         "[signature]   Date\nDST/ATP/BTC\n[signature]   Date\nChief, DST/ATP Contracts\nDirector of Advanced Technologies and Programs (ATP)"),  # #10
        ("\nene", ""),                                        # #11 stray footer artifact
    ],
}

# Whole-page text replacements. When a page's OCR is too degraded for surgical
# find/replace (e.g. a scanned data table that OCR turned to noise), map the page
# to replacement text here; it fully replaces the reflowed OCR for that page.
# The page image on the site remains the authoritative record either way.
PAGE_OVERRIDES = {
    # Claim 2, Doc 2 — ODNI email (email-odni-recommendations, p13). Body OCR was
    # clean but the routing headers were badly garbled and partly redacted, and
    # the divider/bullet glyphs became gibberish that can't be safely find/replaced
    # (tokens like "oo"/"ca"/"ee" would match inside other words). Rebuilt by hand
    # from the 300 DPI page image. "[redacted]" marks black-bar addresses;
    # "Kristian Anderson" is left as the document's own spelling (Andersen), not OCR.
    13: (
"""From: Alan S. Macdougall-DNI-
Sent: Monday, July 12, 2021 3:14 PM
To: James Murphy-DNI-; Stuart H. Schwark-DNI-
Cc: Kelly B. Chafin-DNI-; Kathryn H. Brinsfield-DNI-; Terrance H. SHIPPENSBERG-DNI-; James Mcevers-DNI-; Sarah J. Lawrence-DNI-
Subject: FW: Covid origins - Dr. Fauci recommendations
Attachments: Holmes_et_al-preprint_v1.0_converted.pdf
Classification: UNCLASSIFIED//FOUO
============================================================

Murph and Stu,

(U//FOUO) FYSA from last week's IC Weekly Update. We can discuss further based on my chat with Charles.

VR,
Alan

From: Charles E. Luftig-DNI- <[redacted]@dni.ic.gov>
Sent: Monday, July 12, 2021 2:50 PM
To: Alan S. Macdougall-DNI- <[redacted]@dni.ic.gov>
Cc: Morgan Muir-DNI- <[redacted]@dni.ic.gov>; Meghan L. BLIZNIAK-DNI- <[redacted]@dni.ic.gov>
Subject: Covid origins - Dr. Fauci recommendations
Classification: UNCLASSIFIED//FOUO
============================================================

Alan – The article that Dr. Fauci highlighted last week is attached, and the authors whose views he thought were particularly important were:

• Edward Holmes
• Kristian Anderson
• Andrew Rambaut

As discussed, it might be worth considering the article and talking with these individuals in connection with the 90-day study. In addition, the COVID report rollout is scheduled to be discussed on Friday at the IC Weekly. Please provide any materials or information you want the DNI to convey NLT Thursday COB.

Thanks,
Charles

Charles Luftig
Chief of Staff, ODNI"""
    ),
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
