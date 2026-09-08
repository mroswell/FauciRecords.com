"""Single source of truth for the site: exhibits, claims, and page mapping.

Edit THIS file to correct any document boundary, claim wording, or context note,
then re-run build/build.sh. Page numbers are 1-based PDF pages. Every claim links
only to documents that are actually present in the released packet.

Text quotes below were verified against the OCR'd / extracted page text.
Context notes (`note`) are neutral, dated, editorial aids. They are hidden on the
site by default and revealed only when the `show-notes` class is present; each is a
discrete field so it can be deleted without touching anything else.
"""

# --- Hearing context (page 1 intro) --------------------------------------------
META = {
    "title": "The Fauci Records",
    "subtitle": "Primary-source documents released by Chairman Rand Paul, M.D.",
    "committee": "U.S. Senate Committee on Homeland Security and Governmental Affairs",
    "source_pdf": "2026.08.29_Final-Hearing-Document-Release-Package.pdf",
    "intro": (
        "On July 29, 2026, Dr. Anthony Fauci appeared before the Committee under subpoena at a "
        "hearing titled “Testimony of Anthony Fauci.” He delivered an opening statement "
        "and then invoked the Fifth Amendment 111 times, refusing to answer the Committee’s "
        "questions. Chairman Paul ruled that the privilege did not apply and ordered him to answer. "
        "He refused again. On August 6, 2026, the Committee voted to hold Dr. Fauci in contempt of "
        "Congress. The records below were released by Chairman Paul. Dr. Fauci refused to answer "
        "questions about them under oath."
    ),
}

# --- Exhibits (split-by-item source documents) ---------------------------------
# id, title, kind, date (display), pages [first, last], release (stamp numbers or None)
EXHIBITS = [
    {
        "id": "sow-bioforensics",
        "title": "CIA Bioforensics R&D Statement of Work",
        "kind": "contract",
        "date": "undated",
        "pages": [2, 6],
        "release": "96–100",
        "summary": (
            "Statement of Work for the CIA's Biological Technology Center (Directorate of Science "
            "and Technology) to fund forensic-microbiology R&D carried out through NIAID's funded "
            "institute (TIGR). Marked UNCLASSIFIED//FOUO."
        ),
    },
    {
        "id": "iaa-nondisclosure",
        "title": "Interagency Agreement — Non-Disclosure Clause",
        "kind": "agreement",
        "date": "undated",
        "pages": [7, 7],
        "release": "101",
        "summary": (
            "Clause stating the CIA considers all technical data developed with funds transferred "
            "to NIAID to be sensitive-but-unclassified, and that it “should not be used, "
            "modified, performed, displayed, released or disclosed … without the CIA’s "
            "permission.”"
        ),
    },
    {
        "id": "df-memo",
        "title": "Determination & Findings Memorandum (NIH/NIAID ACQUIRE)",
        "kind": "memo",
        "date": "undated",
        "pages": [8, 9],
        "release": "102–103",
        "summary": (
            "Memorandum for the record on the Bioforensics R&D funding award the CIA intended to "
            "place with NIH/NIAID, signed by CIA DST/ATP/BTC contracting officials."
        ),
    },
    {
        "id": "minutes-niaid-usamriid",
        "title": "NIAID / USAMRIID Coordinating Meeting Minutes",
        "kind": "minutes",
        "date": "March 11, 2002",
        "pages": [10, 12],
        "release": "104–106",
        "summary": (
            "Minutes of a NIAID–USAMRIID program-manager meeting on bioterrorism-response work, "
            "including a note that USAMRIID would prepare guidelines on accepting funding through "
            "Interagency Agreements."
        ),
    },
    {
        "id": "email-odni-recommendations",
        "title": "ODNI Email — “Covid origins – Dr. Fauci recommendations”",
        "kind": "email",
        "date": "July 12, 2021",
        "pages": [13, 13],
        "release": "107",
        "summary": (
            "ODNI Chief of Staff Charles Luftig writes that the article Dr. Fauci highlighted was "
            "attached, and “the authors whose views he thought were particularly important "
            "were” Edward Holmes, Kristian Andersen, and Andrew Rambaut — suggesting they "
            "be consulted in connection with the 90-day origins study."
        ),
    },
    {
        "id": "bseg-form",
        "title": "BSEG Action Request Form — MERS-CoV Mutation & Human-Passage Risk",
        "kind": "form",
        "date": "September 4, 2015",
        "pages": [14, 16],
        "release": "108–110",
        "summary": (
            "Biological Sciences Experts Group action request from the CIA's Global Health Team, "
            "requesting analysis of the mutation frequency of MERS-CoV and an assessment of "
            "human-passage risk. Approved by the NCPC COTR on September 9, 2015."
        ),
    },
    {
        "id": "exsum-gottlieb",
        "title": "EXSUM — VTC with Dr. Scott Gottlieb (Pfizer board member)",
        "kind": "memo",
        "date": "May 7, 2020",
        "pages": [17, 18],
        "release": "111–112",
        "summary": (
            "Executive summary of a CIA video meeting led by COO Andy Makridis with Dr. Scott "
            "Gottlieb, former FDA commissioner and a member of the agency's External Advisory "
            "Board, on the state of COVID-19 medical countermeasures and vaccine platforms."
        ),
    },
    {
        "id": "memo-wcpmc-fauci",
        "title": "CIA / WCPMC Memo — Meeting with Dr. Fauci on COVID Origins",
        "kind": "memo",
        "date": "June 4 (2021)",
        "pages": [19, 19],
        "release": "113",
        "summary": (
            "Memo recording a WCPMC meeting with Dr. Fauci, who “encouraged CIA to contact” "
            "Robert Garry, directed it to Kristian Andersen, and suggested connecting with Ed "
            "Holmes — “all three of whom have advocated for features of the virus that they "
            "judge to be consistent with a natural origin.”"
        ),
    },
    {
        "id": "email-2009-aids",
        "title": "Email — “If AIDS Went the Way of Smallpox”",
        "kind": "email",
        "date": "September 26, 2009",
        "pages": [20, 22],
        "release": None,
        "summary": (
            "Dr. Fauci forwards a New York Times article to Greg Folkers with his own commentary, "
            "closing: “Please delete this e-mail after you have read it.” The forwarded "
            "article follows."
        ),
    },
    {
        "id": "email-2011-h5n1",
        "title": "Email — “help! H5N1 taskings mishegoss”",
        "kind": "email",
        "date": "December 19, 2011",
        "pages": [23, 25],
        "release": None,
        "summary": (
            "Dr. Fauci to Cliff Lane: “I do not want to put down in an e-mail what I think of "
            "all of this … Please delete e-mail after you read it.” Attachment on dual-use "
            "research funding follows."
        ),
    },
    {
        "id": "email-2012-doomsday",
        "title": "Email — “The Truth About the Doomsday Virus?”",
        "kind": "email",
        "date": "March 4, 2012",
        "pages": [26, 28],
        "release": None,
        "summary": (
            "Dr. Fauci to Cliff Lane about H5N1 transmissibility research, closing: “Please "
            "delete this e-mail and then delete from the deleted file.” The forwarded NYT "
            "editorial follows."
        ),
    },
    {
        "id": "email-2020-ncov",
        "title": "Email — “2019nC-V”",
        "kind": "email",
        "date": "February 2, 2020",
        "pages": [29, 30],
        "release": None,
        "summary": (
            "Dr. Fauci to Francis Collins on a thread with Jeremy Farrar: “Please delete this "
            "e-mail after you read it.”"
        ),
    },
    {
        "id": "email-2020-randpaul",
        "title": "Email — “rand paul tweet”",
        "kind": "email",
        "date": "July 20, 2020",
        "pages": [31, 32],
        "release": None,
        "summary": (
            "Dr. Fauci to Greg Folkers about a Rand Paul tweet on state vs. country death rates, "
            "closing: “… please delete this e-mail after you read it.” A COVID-19 "
            "case-count table follows."
        ),
    },
]

# --- Claims (the 5 numbered items on page 1) -----------------------------------
# Each fact links to specific exhibits. `note` fields are hidden context notes.
CLAIMS = [
    {
        "number": 1,
        "id": "claim-delete-emails",
        "headline": "Fauci repeatedly asked colleagues to delete emails he sent.",
        "body": (
            "Over nearly eleven years, Dr. Fauci closed sensitive emails by telling the recipient to "
            "delete them upon reading. The instructions appear in messages dated September 26, 2009; "
            "December 19, 2011; March 4, 2012; February 2, 2020; and July 20, 2020. In the 2012 email "
            "he asked that the message also be removed from the deleted items folder."
        ),
        "facts": [
            {
                "text": "September 26, 2009 — “Please delete this e-mail after you have read it.” Forwarding a New York Times article to Greg Folkers.",
                "exhibits": ["email-2009-aids"],
            },
            {
                "text": "December 19, 2011 — “Please delete e-mail after you read it.” To Cliff Lane, on H5N1 taskings.",
                "exhibits": ["email-2011-h5n1"],
            },
            {
                "text": "March 4, 2012 — “Please delete this e-mail and then delete from the deleted file.” To Cliff Lane, on the “Doomsday Virus” editorial.",
                "exhibits": ["email-2012-doomsday"],
            },
            {
                "text": "February 2, 2020 — “Please delete this e-mail after you read it.” To Francis Collins, on a thread with Jeremy Farrar.",
                "exhibits": ["email-2020-ncov"],
            },
            {
                "text": "July 20, 2020 — “… please delete this e-mail after you read it.” To Greg Folkers, about a Rand Paul tweet.",
                "exhibits": ["email-2020-randpaul"],
            },
        ],
    },
    {
        "number": 2,
        "id": "claim-conflicted-authors",
        "headline": (
            "Fauci pointed the intelligence community assessing COVID-19’s origin to the "
            "conflicted authors of the Proximal Origin paper."
        ),
        "body": (
            "A CIA memorandum records that Dr. Fauci encouraged the CIA to contact Robert Garry, "
            "Kristian Andersen, and Eddie Holmes. The CIA’s own memo notes the common thread: "
            "“all three of whom have advocated for features of the virus that they judge to be "
            "consistent with a natural origin.” Additionally, a July 12, 2021 email from ODNI "
            "states that Dr. Fauci had highlighted a scientific article and identified “the "
            "authors whose views he thought were particularly important”: Edward Holmes, "
            "Kristian Andersen, and Andrew Rambaut."
        ),
        "note": (
            "“Proximal Origin” refers to the March 2020 Nature Medicine paper "
            "“The proximal origin of SARS-CoV-2,” whose authors included Kristian Andersen, "
            "Edward Holmes, and Andrew Rambaut, and which argued against a laboratory origin."
        ),
        "facts": [
            {
                "text": "CIA/WCPMC memo: Dr. Fauci “encouraged CIA to contact” Robert Garry, directed it to Kristian Andersen, and suggested Ed Holmes — “all three of whom have advocated for features of the virus that they judge to be consistent with a natural origin.”",
                "exhibits": ["memo-wcpmc-fauci"],
            },
            {
                "text": "ODNI email (July 12, 2021): the authors whose views Fauci “thought were particularly important” — Edward Holmes, Kristian Andersen, Andrew Rambaut — suggested for consultation in the 90-day origins study.",
                "exhibits": ["email-odni-recommendations"],
                "note": (
                    "The 90-day study was the Biden administration's May–August 2021 "
                    "intelligence-community review of COVID-19 origins."
                ),
            },
        ],
    },
    {
        "number": 3,
        "id": "claim-cia-niaid-funds",
        "headline": "CIA transferred funds to NIAID for work shielded from public release.",
        "body": (
            "Documents show that the CIA and NIAID had an interagency agreement under which the "
            "transfer of funds and the contractual relationship between the two agencies were "
            "unclassified but restricted from public release. The agreement provided that NIAID "
            "would not disclose the resulting data without the CIA’s permission."
        ),
        "facts": [
            {
                "text": "CIA Bioforensics Statement of Work: forensic-microbiology R&D funded through NIAID's institute (TIGR), marked UNCLASSIFIED//FOUO.",
                "exhibits": ["sow-bioforensics"],
            },
            {
                "text": "Non-disclosure clause: data developed with CIA funds “should not be … released or disclosed … without the CIA’s permission.”",
                "exhibits": ["iaa-nondisclosure"],
            },
            {
                "text": "Determination & Findings Memorandum documenting the CIA's funding award to NIH/NIAID.",
                "exhibits": ["df-memo"],
            },
            {
                "text": "Related record: NIAID–USAMRIID coordinating minutes on funding through Interagency Agreements.",
                "exhibits": ["minutes-niaid-usamriid"],
                "note": (
                    "This record concerns NIAID's relationship with USAMRIID (Department of "
                    "Defense), not the CIA. It is included in the same released set and illustrates "
                    "NIAID's use of interagency agreements."
                ),
            },
        ],
    },
    {
        "number": 4,
        "id": "claim-bseg-mers",
        "headline": (
            "In September 2015, the CIA asked BSEG for information on MERS-CoV mutation frequency "
            "and an assessment of human-passage risk."
        ),
        "body": (
            "A Biological Sciences Experts Group (BSEG) action request form, submitted by the "
            "CIA’s Global Health Team on September 4, 2015, asked “for a paper outlining the "
            "rate of mutation, the number of passages from human to human to lock in these mutations "
            "(or to generate them), and the molecular genetic means through which this is likely to "
            "occur.”"
        ),
        "note": (
            "MERS-CoV is the Middle East Respiratory Syndrome coronavirus. “Passage” means "
            "growing a virus through one host after another — from person to person, animal to "
            "animal, or in lab cell cultures. Each pass gives the virus a chance to pick up "
            "mutations, and repeated passaging can select for versions that spread more easily "
            "among people. So a request for “the number of passages from human to human to "
            "lock in these mutations” is asking how many times a virus must move between "
            "people before it becomes well adapted to spreading among humans."
        ),
        "facts": [
            {
                "text": "BSEG Action Request Form, CIA/Global Health Team, dated September 4, 2015: “Request for Mutation [frequency] of MERS-CoV and Assessment of human passage risk.” Approved by NCPC COTR on September 9, 2015.",
                "exhibits": ["bseg-form"],
            },
        ],
    },
    {
        "number": 5,
        "id": "claim-pfizer-board",
        "headline": "CIA took pandemic advice from a sitting Pfizer board member.",
        "body": (
            "On May 7, 2020, CIA Chief Operating Officer Andy Makridis led a briefing with Dr. Scott "
            "Gottlieb, the former FDA commissioner, in his capacity as a member of the agency’s "
            "External Advisory Board. The agency’s own summary of the meeting identifies Gottlieb "
            "as a member of the Board of Directors of Pfizer. Gottlieb would later also be consulted "
            "by the intelligence community during the Biden Administration’s 90-day study on the "
            "origins of COVID-19."
        ),
        "note": (
            "Scott Gottlieb was FDA Commissioner from 2017 to 2019 and joined Pfizer's board of "
            "directors in June 2019."
        ),
        "facts": [
            {
                "text": "EXSUM of the May 7, 2020 video meeting, led by COO Andy Makridis, with Dr. Scott Gottlieb, External Advisory Board member — covering COVID-19 vaccine platforms (mRNA, adenovirus, recombinant protein).",
                "exhibits": ["exsum-gottlieb"],
            },
        ],
    },
]
