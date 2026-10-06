---
name: cui-re-use-triage
description: Walk the documents a company creates while using CUI it received, and separate the CUI content each one re-uses from the company's own work, then send every document to `cui-determination-workflow` for its status. Covers any industry, with a build-to-print machine shop as the worked example, the export chain for g-code, and intake and outbound packages to suppliers. Use when a contractor asks whether its own sketches, travelers, inspection reports, NC programs, analysis reports, code, or briefings are CUI because they were made from a customer's CUI.
vault_sources:
  - "Machine Shops and CUI"
  - "How CUI Flows Through a Contractor"
  - "Practitioner insights A"
  - "Supplier CUI Release Procedure"
  - "Data Rights Assertions"
  - "raw/48-cfr-252-227-7013-ecfr-2026-05-14.md"
public_sources:
  - "32 CFR 2002.4 (definitions: (h) CUI, (ee) misuse, (pp) re-use): https://www.ecfr.gov/current/title-32/section-2002.4"
  - "32 CFR 2002.50 (challenges to a designation): https://www.ecfr.gov/current/title-32/section-2002.50"
  - "81 FR 63324, CUI final rule, preamble at 63334: https://www.federalregister.gov/documents/2016/09/14/2016-21665/controlled-unclassified-information"
  - "ISOO, CUI Stakeholders Update Q2 FY2020, slide 8: https://isoo.blogs.archives.gov/2020/02/13/cui-q2-stakeholders-update-slides/"
  - "22 CFR 120.31, unfinished parts: https://www.ecfr.gov/current/title-22/part-120/section-120.31"
  - "22 CFR 120.41, specially designed, with the fastener release at (b)(2): https://www.ecfr.gov/current/title-22/section-120.41"
  - "15 CFR 772.1, EAR definition of specially designed, with the fastener release at (b)(2): https://www.ecfr.gov/current/title-15/section-772.1"
  - "DFARS 252.204-7012, definition of controlled technical information: https://www.ecfr.gov/current/title-48/section-252.204-7012"
  - "IntelliGRC Ep. 11, CUI, Supply Chain Flow-Downs and the Real CMMC Challenges (2026-05-06): https://www.youtube.com/watch?v=PG7aZWUvVvs"
  - "DFARS 252.227-7013, Rights in Technical Data: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.227-7013"
---

# CUI re-use triage

A company that receives CUI creates documents while using it: a machine shop makes sketches, travelers, inspection reports, and g-code from a customer's drawing; an engineering firm writes an analysis report; a software contractor writes code and test data; a services firm builds a briefing. This skill walks those documents one at a time and answers, for each, which parts of it are **re-used CUI** and which parts are the company's own work. It then sends each document to `cui-determination-workflow`, which gives the status.

This skill decides nothing. Call the Skill tool with `cui-determination-workflow` for every status, `export-control-overlay` for ITAR or EAR depth, and `cui-marking-check` for how a document already found to be CUI is marked.

## The rule this skill applies: content, never ancestry

32 CFR 2002.4(pp) defines re-use as "incorporating, restating, or paraphrasing information from its originally designated form into a newly created document", and 2002.4(aa) lists re-using as a form of handling. The preamble to the CUI final rule settles the question this skill exists for: a document derived from CUI is CUI "because it contains controlled information, not simply because it is derived from a document that contains CUI", and a document built only from the non-CUI portions of a source "would not become CUI simply because the information was derived from a CUI document" (81 FR 63324, 63334).

So the question for every created document is **what content does it carry**, not **where did it come from**. The words "derivative CUI", "contaminated", and "inherits the source's status" all describe status travelling by contact, which is how classified information works and not how CUI works. Use **re-used CUI** for the content, and judge the rest of the document on its own (see `CONTEXT.md`).

## Inputs

- What the company received: the documents, their markings, and the contract or order they came under.
- What the company creates from them, one line per document type, and who creates it.
- The end item or service being delivered, and any military or space application.
- Whether the company owns the design or works to a design the customer supplied.
- The engagement repo files: `CONTEXT.md`, `scope/cui-determinations.md`, and any prior `scope/cui-re-use-triage.md` for this client; and the assets in the record, `ssp/ssp.json`, shown by calling the Skill tool with `scribe`. Never read `view/` instead; it is generated for people and can be stale.

## Method

1. **List every document type the company creates from the CUI it received.** Walk the work from receipt to delivery, including the paper that never reaches a server. A machine shop's list starts with the table in step 6. An engineering firm's list includes working calculations, models, analysis reports, and review slides. A software contractor's list includes source code, test data, interface definitions, and tickets. Done when every document type a role interview named is on the list.

2. **Ask the re-use questions of each document, in this order, and write the answers down.**
   1. **Which content on it came from the CUI received?** Name the items: a dimension, a tolerance, a datum scheme, a requirement, an image, a table, a passage of text. "Parts of the drawing" is not an answer.
   2. **Is that content incorporated, restated, or paraphrased?** Any of the three is re-use under 2002.4(pp). Rewriting CUI in your own words, or copying it onto a notepad by hand, is still re-use. A pointer is not: "machine per drawing 4471-003 Rev C" names the source without carrying its content.
   3. **Is the source content itself CUI?** A source can hold CUI and non-CUI portions, and a document built only from the non-CUI portions is not CUI on that account (81 FR 63334). A part number, a material call-out from a public specification, or a quantity is rarely the controlled content of a drawing. Check against the source's own markings and category, through `cui-determination-workflow`.
   4. **Replica or the company's own expression?** Could a reader rebuild the controlled content from this document without the source? A sketch that copies the dimensions and datums is a replica of part of the drawing. A toolpath, a routing, a fixture design, or a test method is the company's own expression of *how* to do the work, even when it was written to meet the customer's *what*.
   5. **What of the company's own is on it?** Methods, process steps, toolpath strategy, routing, scheduling, pricing. That content is Proprietary (own), and it stays the company's whether or not the document also carries re-used CUI.
   6. **Did the contract require this document to be developed and delivered?** If so, the workflow's "specifically for the government" and clause-family tests apply to it as a deliverable. Being made to perform the contract is not enough on its own (the DFARS 252.204-7012 prong (2) bullet in the workflow's step 7).

   Done when every document on the list has an answer to all six, or an answer of "unknown" with what would settle it.

3. **Send each document to `cui-determination-workflow` with those answers, and record the status it returns.** Record the re-used content and the company's own content in separate columns, so a later reader sees that a traveler is CUI because of the three dimensions printed next to the thumbnail, not because it is a traveler. Where the answers leave the status unclear, the workflow's step 8 applies: decide on the evidence, notify the customer with the proposed status and the reasoning, record **potentially CUI, notice sent** while the notice is open, and safeguard the document as CUI meanwhile.

4. **Record what "not CUI" leaves behind.** A document cleared of CUI can still be **Export-controlled**, **Proprietary (own)**, or **FCI**. That is the difference between *regulated* and *controlled*: export law can reach a document the government does not control as CUI, and the obligations differ (see the data categories in `CONTEXT.md`). Label every document with every category that applies, so "not CUI" never reads as "not sensitive".

5. **Hold the company to the check in both directions.** The holder's duty in the workflow's step 8 cuts both ways: a document that re-uses CUI content and is left unmarked is a handling failure, and marking the company's own work as CUI because of its source is misuse (32 CFR 2002.4(ee)). Overmarking has a cost the operator should state out loud to the client. Every asset that stores the overmarked document joins the CUI Asset category and the full set of 110 requirements, so a mislabelled NC program pulls the programming PC, the USB sticks, and the machine controls into scope. And the company's process data is intellectual property: practitioner consensus holds that labelling it the customer's CUI weakens the company's own ownership and data-rights position over it (DFARS 252.227-7013 governs those rights).

6. **Machine shop worked example: the build-to-print document trail.** The shop receives the customer's drawing and machines to it. The shop does not own the design; it does own how it makes the part. Ask the step 2 questions of each row. The right column says where the answer usually turns, not what the answer is.

   | Document | The question that usually decides it |
   |---|---|
   | Customer drawing | The source. Its status comes from its markings and the contract, through the workflow |
   | Shop sketch | Does it copy dimensions, tolerances, or datums from the drawing? A copied datum scheme is a replica of part of the drawing |
   | Traveler or router | Does it print drawing content (a thumbnail, critical dimensions, notes), or only the part number and "per drawing"? The shop's routing is its own either way |
   | Work instruction | Do the drawing's dimensions or requirements sit on the same page as the instruction, or does the reader still need the drawing to act? |
   | Setup sheet | Does it list drawing dimensions, or only the shop's fixturing, tools, and offsets? |
   | Inspection or FAI report | Does it restate the drawing's requirements and results against them? A report that lists every dimension is re-use |
   | G-code / NC program | Run the chain in step 7 |
   | CAD model the shop redraws or imports | A model rebuilt to the drawing's geometry is a replica of the drawing's content. It is the likeliest home of the controlled technical data in the shop |
   | PO for raw material | Does it carry anything beyond stock size, material, and quantity? |
   | PO or package to an outside processor | Split the document from what travels with it (step 9) |
   | Quote, customer PO clause page | Contract paperwork. The workflow usually returns FCI |

   Between the shop's core systems, the ERP is usually the easiest to keep clean, because most of its fields are business data (schedule, cost, quantity); the CAD and PLM systems that hold the models are the hardest, because they hold the geometry itself. A traveler that ERP prints with a drawing thumbnail is the usual way drawing content gets into ERP.

7. **Run the g-code chain. Re-use first, export second.** Two questions, answered in this order. An operator who cannot yet classify the end item can still finish the CUI question.

   **First, re-use.** A toolpath is the shop's own expression of how to cut the part: this tool, this feed, this path. Information a company creates internally and keeps ownership of is not CUI (32 CFR 2002.4(h); ISOO's CUI Stakeholders Update, Q2 FY2020, slide 8), and a new document is CUI only for the CUI content it carries (81 FR 63334). Practitioner consensus applies that to g-code: a coordinate list written to make the part is the shop's method, not the drawing restated, and the CAD model is the usual home of the controlled content. So bring the program to the workflow as a candidate for **not CUI; Proprietary (own)**, and look for what would change it:
   1. **Re-used content in the comments or header.** Drawing notes, tolerances, the customer's requirements, or a title block copied into the program comments are re-used content, and they are what would make the file CUI. A header that only names the part number, revision, and customer is a labelling problem, not re-used technical content: it makes the file look like the customer's document to anyone who opens it. Recommend a shop job number in its place.
   2. **A program the customer supplied or the contract requires to be delivered.** That is not the shop's own expression. Send it to the workflow as a deliverable or as received CUI.
   3. **Genuine doubt.** Where the program embeds enough of the geometry that the shop cannot say it is only its own method, record **potentially CUI, notice sent**, and notify the customer of the status the shop proposes, with the reasoning (the workflow's step 8). Never record "CUI because it came from the drawing": that is ancestry, which step 2 rules out.

   **Second, export.** Run this in order and stop as soon as one step resolves it:
   1. Classify the end item the g-code produces: is it caught by a specific paragraph of the US Munitions List, or by an Export Control Classification Number on the Commerce Control List? A component is not automatically caught because the finished assembly is; read the actual paragraph.
   2. If the end item is caught by neither list, the data describing it is not export-controlled technical data.
   3. If it is caught, check whether the operation produces a part that has reached a stage where it is identifiable as a defense article (22 CFR 120.31). A complex part that takes many setups, each leaving an unrecognizable intermediate shape, can clear this test at each individual g-code file even when the finished part would not.

   **What counts as an answer to the classification question.** An explicit classification from the customer or from a trade compliance review is the strong form; ask for it. Short of that, a customer drawing marked with an export control warning is the customer asserting the item is caught, and that is a usable working answer: proceed on it, and record that it rests on the customer's marking. Do not let an unresolved export question hold up the CUI question, and do not let an export warning answer the CUI question: a program can be Export-controlled and not CUI at the same time. Where the classification matters and is unknown, call the Skill tool with `export-control-overlay` and put the question to the customer in writing.

   **Fastener-only data gets two separate answers.** Fastener-only data describes nothing but a fastener, washer, spacer, bushing, spring, or similar hardware.
   - **Export.** Both lists take fasteners out of their "specially designed" catch-alls "regardless of form or fit" (22 CFR 120.41(b)(2) for the USML, and the definition of "specially designed" at (b)(2) in 15 CFR 772.1 for the CCL). So a fastener is not caught by a catch-all paragraph, and it is caught only if an entry names it directly. Check the entry rather than assume. A fastener that no entry names is usually EAR99. EAR99 is still subject to the EAR, so the end-user and destination screening in `export-control-overlay` still applies.
   - **CUI.** The export answer does not settle whether the data is CTI. DFARS 252.204-7012 defines CTI as technical information with military or space application that is subject to controls on access and dissemination, and the definition does not refer to the export lists. The same definition excludes "information that is lawfully publicly available without restrictions," so data that only restates a published standard fastener specification is not CTI. A customer drawing of a custom fastener that arrives with a CUI banner or a distribution statement is read like any other marked document, through `cui-determination-workflow`.

8. **Run purchasing intake on every incoming package before it reaches the floor.** At quote or purchase-order intake:
   1. A package with only a proprietary legend and an export-control notice, no distribution statement and no CUI banner, goes to `cui-determination-workflow`, whose step 7 reads exactly that case (no statement and no banner from an originator who marks correctly). Record it as Proprietary (third-party), and Export-controlled while the notice stands, and do not leave it as "sensitive". The export notice still needs its own answer from `export-control-overlay`.
   2. Those markings paired with a distribution statement, especially Distribution Statement D, are a strong indicator worth reviewing with the customer for the actual CUI category before proceeding.
   3. When the status is unclear, decide rather than guess, then notify in writing: say the package is sensitively marked but not as CUI, that CUI handling was not flowed down, and how the shop will handle it. The customer can correct it; silence accepts it (the workflow's step 8).
   4. Add quote language stating that the customer is responsible for marking the data it shares. This does not excuse the shop from checking; it records that the shop asked.
   5. Take the package in only through the enclave's intake path, never the general inbox. `enclave-or-enterprise-decision` names that path; intake triage runs on what arrives there.

9. **Triage the outbound package separately, and keep the carrier apart from the cargo.** Purchase orders and packages to an outside processor, finisher, coater, or lab need their own call, in two halves:
   - **The document itself.** A purchase order that names a specification by reference ("anodize per drawing 4471-003 Rev C") and carries no dimensions or geometry does not re-use the drawing's content. The workflow usually returns FCI.
   - **What travels with it.** Attaching the drawing, or putting the printed traveler in the box, is a CUI flow to that supplier. That is a release decision rather than a marking decision. It puts the supplier in scope and needs an approved release path first.

   Keep the two answers in separate columns. "Not CUI, but it transmitted the drawing to a supplier with no release path" tells the client what to fix; "CUI" on the purchase order does not. Call the Skill tool with `supplier-cui-release-procedure` for the path and `flowdown-level-determination` for what the supplier now needs.

10. **Keep an allow-list of what may be copied out.** Redacting controlled documents one at a time does not repeat reliably. Keep one written list, in `scope/extraction-allow-list.md`, of content that may always be copied out of a controlled document into the company's own paperwork, each entry with the reason it is safe: a published standard anyone can buy, a public military specification, a public material specification, or a portion the customer has confirmed in writing is not controlled. This is the preamble's non-CUI portions case: a document built only from them "would not become CUI simply because the information was derived from a CUI document" (81 FR 63334). Three limits:
    - **Each entry gets its status from `cui-determination-workflow`,** recorded once, so the floor can rely on it without asking again.
    - **The list says what is not CUI, not what is not export-controlled.** For an export-controlled part, the dimensions, tolerances, and GD&T are themselves technical data, so the allow-list shrinks what the shop paperwork carries but does not take those items out of the enclave. Call the Skill tool with `export-control-overlay` before adding geometry to the list.
    - **Every entry names its source.** An entry with no reason is a guess, and the shop floor will copy by it for years.

    Practitioners recommend this over redaction: keep customer documents in as few places as possible, and allow-list the public content that is always safe to extract (IntelliGRC Ep. 11, from 53:01: https://www.youtube.com/watch?v=PG7aZWUvVvs).

## Output

Write the triage to `scope/cui-re-use-triage.md`, one row per document type for the job or product line, and append each document's determination to `scope/cui-determinations.md` through `cui-determination-workflow`:

```markdown
# CUI re-use triage: <job or product line>

| Document | Re-used CUI content (what, from which source) | Company's own content | Status (from cui-determination-workflow) | Data categories | Carries CUI with it | Reason |
|---|---|---|---|---|---|---|
| <document type> | <named items, or "none: pointer only"> | <methods, routing, toolpaths, pricing> | CUI / FCI / not CUI and not FCI / potentially CUI, notice sent | <every category that applies> | <what travels attached, or "nothing"> | <the step 2 answers that decided it> |

## Walkthrough questions for the floor and engineering

Use these to confirm the table rather than guess at it: what files can the production user open; can the workstation reach engineering drawings or customer specifications; what do printed packets carry (a CUI banner, a distribution statement, an export notice, a proprietary legend); what is written into program headers and comments; where are test profiles stored and who can edit them; do test profiles or logs carry a customer requirement or numeric limit; are test results a contract deliverable; can the production account reach engineering shares, CAD, PLM, ERP attachments, or MES attachments; and, counting paper, network, and the machine itself, does re-used CUI reach production at all.

## Open items
- <each document recorded as potentially CUI, notice sent: the status proposed, to whom, the date, and when the window closes>
```

**Status** is the document's own status. **Carries CUI with it** is what travels attached to or alongside it, and it is a separate answer: a purchase order that is only FCI still puts a supplier in scope when the drawing is stapled to it. Where the answer is yes, name what travels and route it to `supplier-cui-release-procedure`.

## Where practitioners disagree

- **Whether a toolpath that traces the drawing's geometry is re-use of that geometry.** The majority position: the program is the shop's own expression of how to make the part, and its IP; the CAD model holds the controlled content. The minority position: coordinates that reproduce the drawing's hole pattern and profile are a restatement of the drawing in another notation, so the program is re-used CUI. This skill starts from the majority and records the minority as "potentially CUI, notice sent" where the shop cannot say the program is only its own method. The outcome depends on the assessor and, in the end, on the customer.
- **Whether "derivative CUI" exists at all.** One position: nothing a contractor creates is CUI until the government says so, and only the designating authority can identify CUI. The other: copying CUI into a new document, on a notepad or field by field, obviously keeps it CUI, and denying that invites word games about copying half a document. The regulation reconciles the two on content: the copy is CUI because the content copied is CUI (2002.4(pp); 81 FR 63334), and whatever the company adds of its own is not. The line between restating and expressing your own method is still a matter of degree, which is why an unclear item gets a reasoned status and a written notice to the customer.
- **Whether the line for a work instruction is a bright rule** (drawing content and instruction on the same page) or a judgment the shop has to make consistently across its whole document set. The outcome depends on the assessor.
- **How to treat production test systems** that never show an operator the controlled parameters but store or transmit them behind the scenes. One position: the sanitized operator workflow is out of scope on its own. The other: the test station, application, and log storage stay in scope whatever the operator sees. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: build the triage once per representative product line during onboarding, not once per job, and walk the purchasing team through the intake steps directly, since they run them daily. Say the overmarking cost in step 5 to the owner before anyone starts stamping banners on shop paperwork. **OSC seat**: start with the g-code chain on your highest-volume part number; it usually settles the largest disputed category on the floor and gives the rest of the triage a template.

## Sources

- 32 CFR 2002.4: https://www.ecfr.gov/current/title-32/section-2002.4 ((pp) re-use and (aa) handling for the rule in "Content, never ancestry" and step 2; (h) the exclusion for the company's own information in step 7; (ee) misuse by overmarking in step 5).
- ISOO, CUI Stakeholders Update, Q2 FY2020, slide 8: https://isoo.blogs.archives.gov/2020/02/13/cui-q2-stakeholders-update-slides/ (mirrored at `reference/isoo/cui-stakeholders-update-q2-fy2020.md`; proprietary information a company creates internally and owns is not CUI, step 7).
- 81 FR 63324, the CUI final rule, preamble at 63334: https://www.federalregister.gov/documents/2016/09/14/2016-21665/controlled-unclassified-information (a derived document is CUI because of the controlled information it contains, not because of its source; quoted in `reference/authorities.md`).
- 32 CFR 2002.50: https://www.ecfr.gov/current/title-32/section-2002.50 (the written route for an item whose status is unclear, step 3).
- 22 CFR 120.31: https://www.ecfr.gov/current/title-22/part-120/section-120.31 (unfinished products identifiable as defense articles, step 7).
- 22 CFR 120.41: https://www.ecfr.gov/current/title-22/section-120.41 (the fastener release from "specially designed" at (b)(2), step 7).
- 15 CFR 772.1: https://www.ecfr.gov/current/title-15/section-772.1 (the same release in the EAR definition of "specially designed", step 7).
- DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/section-252.204-7012 (the definition of controlled technical information and its exclusion of lawfully public information, step 7).
- IntelliGRC Ep. 11, "CUI, Supply Chain Flow-Downs and the Real CMMC Challenges" (2026-05-06): https://www.youtube.com/watch?v=PG7aZWUvVvs (paraphrased, not quoted: allow-listing public content instead of redacting, from 53:01; step 10).
- DFARS 252.227-7013, Rights in Technical Data: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.227-7013 (the data-rights basis for a manufacturer's own process data, step 5).
- Practitioner consensus, unattributed, backs the replica question in step 2.4, the overmarking and data-rights cost in step 5, the machine shop table and the ERP-versus-CAD observation in step 6, the application of the ownership exclusion to g-code in step 7, the intake steps in step 8, and the outbound split in step 9. None of it sets a CUI status on its own; every status comes from `cui-determination-workflow`.
