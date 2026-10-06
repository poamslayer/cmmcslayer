---
name: cui-marking-check
description: Check a document, email, slide deck, or spreadsheet for correct CUI marking, catch the four wrong banner formats, build a compliant four-line designation block, apply the CTI overlay with the right Distribution Statement, and decide what a subcontractor is allowed to mark on its own output. Use before a marked document leaves the building or when reviewing a document a customer or prime sent in.
vault_sources:
  - "CUI Marking"
  - "Marking CTI"
  - "Distribution Statements"
  - "3.8.4"
  - "Controlled Technical Information"
  - "Practitioner insights B"
  - "raw/dod-cleared-cui-training-aid-markings-2024.md"
  - "raw/dodcui--Distribution-Statements.md"
  - "raw/dodcui--Defense--Controlled-Technical-Information.md"
  - "raw/dodcui--Limited-Dissemination-Controls.md"
  - "raw/dodcui--Home--Marking-Tips-for-CUI-Documents.md"
public_sources:
  - "DoD CUI Program FAQ, Use of Distribution Statements: https://www.dodcui.mil/Frequently-Asked-Questions/Use-of-Distribution-Statements/"
  - "DoDI 5230.24, Distribution Statements on DoD Technical Information, January 10, 2023: https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/523024p.pdf"
  - "DoD CUI marking training aid, December 2024, DoD CIO, cleared for open publication DOPSR 25-P-0275: https://www.dodcui.mil/"
  - "DoD CUI Distribution Statements page: https://www.dodcui.mil/Distribution-Statements/"
  - "DoD CUI Controlled Technical Information category page: https://www.dodcui.mil/Defense/Controlled-Technical-Information/"
  - "DoD CUI Limited Dissemination Controls page: https://www.dodcui.mil/Limited-Dissemination-Controls/"
  - "32 CFR 2002.20 (marking): https://www.ecfr.gov/current/title-32/section-2002.20"
  - "CMMC Level 2 Assessment Guide, DoD CIO, MP.L2-3.8.4: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
---

# CUI marking check

This skill answers: is this document, email, slide deck, or spreadsheet marked the way the DoD CUI program requires, and if not, what is wrong and how do you fix it? It checks the banner, the designation indicator block, the Controlled Technical Information (CTI) overlay, and the format-specific rules for the medium in front of you. It does not decide whether the content is CUI in the first place; that determination happens upstream, before marking. It also does not decide whether export control changes the answer; call the Skill tool with `export-control-overlay` for that.

## Inputs

- The document, email, slide deck, or spreadsheet under review, or a description of it if you cannot paste the content.
- Whether the content is CTI, another CUI category, or the CUI category is not yet known.
- Who produced the document: your company, a customer, or a prime.
- The contract or subcontract clause language governing marking, if you have it.
- `reference/cui-marking-spec.md` for the full training aid text and examples (also public at https://www.dodcui.mil/).

## Method

1. **Check the two mandatory elements first.** Every unclassified document containing CUI needs both: the acronym `CUI`, exactly those three letters and nothing else, repeated on the header and footer of each page, plus a CUI designation indicator block sitting on the cover or first sheet. A document missing either one fails the check regardless of anything else on the page.

2. **Reject these four banners on sight.** The 2024 DoD training aid names these as wrong, and each one is a finding, not a style note:

   | Wrong banner | Why it fails |
   |---|---|
   | `U//CUI` | Do not prefix `CUI` with `UNCLASSIFIED` or `U//` |
   | `CUI//BUDG` (or any category suffix) | The category never goes in the banner; it goes in the designation block |
   | `CONTROLLED` | Not the correct acronym |
   | `CONTROLLED UNCLASSIFIED INFORMATION` | Spelled out is not the correct banner form |

   The only correct top-and-bottom banner text is `CUI`.

3. **Build the four-line designation indicator block.** Place it at the bottom of the first page or cover, never on every page:
   - Line 1, Controlled by: the DoD Component or the producing office. A contractor that is authorized to create CUI documents may list itself as the point of contact here.
   - Line 2, CUI Category: the registry abbreviation or abbreviations, for example `CTI`, `NNPI`, or `BUDG, PSI` when more than one applies.
   - Line 3, LDC or Distribution Statement: the applicable Limited Dissemination Control, or the Distribution Statement letter when the category requires one (see step 4). A document carries one or the other on this line, not usually both, though a `REL TO` control can be appended to a Distribution Statement's full text.
   - Line 4, POC: a name and phone number, a name and email, or an organizational email.

   Never portion-mark the designation block itself. Portion marking on the rest of an unclassified document is optional but recommended; if you use it, apply it to every portion consistently, including titles, paragraphs, bullets, figures, and tables.

4. **Apply the CTI overlay when the category is CTI.** CTI and export-controlled information are the only two CUI categories that require a Distribution Statement, and for CTI the rule is absolute: Distribution Statement B through F, never A. Statement A is reserved for information approved for public release, and CTI by definition is not eligible for public release. Two things must both be true on the document:
   - The letter (B, C, D, E, or F) goes on Line 3 of the designation block.
   - The full text of that statement is written out on the first page of the document, not just abbreviated to the letter.

   When the CTI is also ITAR- or EAR-controlled, which is common, stack an export-control warning on top of the Distribution Statement rather than substituting one for the other; export control and CUI marking are two regimes that happen to land on the same document. A representative warning text: a notice that the document contains technical data whose export is restricted by the Arms Export Control Act or the Export Control Reform Act of 2018, that violations carry severe criminal penalties, and that dissemination follows DoD Directive 5230.25. Call the Skill tool with `export-control-overlay` to work out whether ITAR or EAR actually applies before adding this warning.

   Two incoming patterns to flag rather than fix:
   - **An export warning with no distribution statement and no banner.** Correctly marked CTI and Export Controlled CUI both need a statement B through F, so this is either the originator's own export-controlled data, which is not CUI, or a mismarking. Do not add CUI markings. Raise it with the source in writing and route the status question to `cui-determination-workflow`.
   - **Distribution Statement E with a contractor's proprietary legend and no banner.** A statement is not a CUI determination, and a proprietary legend says who owns the data, not whether the copy you hold is CUI. Read the defense category in the statement: "Controlled Technical Information" means CTI. Any other category leaves it undetermined until you apply that category's test in `reference/dodi-5230-24-defense-categories.md`. No category at all leaves it undetermined. Handle it under NIST SP 800-171 while you ask the source for the CUI category, the controlling DoD office, and whether release to you is authorized. Statement E means "DoD Components only", so a subcontractor holding it needs that authorization in writing.

5. **Apply the format-specific rule for the medium.**

   | Format | Rule |
   |---|---|
   | Text document | Banner top and bottom of every page; designation block bottom of page one |
   | Email carrying CUI in the body | `CUI` as the first and last lines of the body; designation block inline; encrypt when technically feasible |
   | Email that only transmits a CUI attachment, with no CUI in the body | Head and foot of the message read `CUI`; add the line stating the message is unclassified once the enclosure is removed; skip the designation block on the message, since the attachment carries its own |
   | Slide deck | Header and footer marking on the title slide and on every slide that follows; the title slide's marking states the sensitivity of the deck as a whole; pick either that whole-deck convention or a slide-by-slide one for the interior slides and stay consistent |
   | Spreadsheet | Same banner and designation block treatment as a text document |
   | Classified document containing CUI | Banner is the overall classification, for example `SECRET`, never `CUI`; portion marking becomes mandatory rather than optional; put the classification authority block and the CUI block together at the foot of page one; keep CUI category and dissemination information out of the banner line entirely |

6. **Apply the carry-forward rule before you invent a marking.** A subcontractor holds CUI on the government's behalf; it does not get to decide what counts as CUI, and that call belongs to whichever agency first designated it. When a customer or prime hands you a marked document, your job is to carry its existing banner, designation block, and Distribution Statement forward unchanged, not to redesign the marking. Write your own output as CUI only when the contract directs it. A policy sentence that conditions marking on the contract saying so is complete as written; resist the urge to strengthen it into an unconditional instruction to always mark, because that claims a designating authority the contractor does not hold. This is the same logic 3.8.4 applies to physical media: a Distribution Statement already printed on an incoming drawing is enough by itself to meet the distribution-limitation objective, and you do not need to invent a separate marking step to cover it.

7. **Apply the envelope rule.** The shipping container never gets a CUI marking and never gets any sign, label, or note revealing that CUI is inside (32 CFR 2002.20(i)(2)). What goes inside the envelope carries the marking; the envelope stays blank. A transmittal document riding along with the package is treated differently: it needs the word `CONTROLLED` or `CUI` displayed on it, plus a sentence that tells the recipient what the transmittal's status becomes after the enclosure has been taken out.

## Output

A findings table for each document reviewed, written to `evidence/cui-marking/<document-name>.md` or attached to the review thread:

```markdown
# CUI marking check: <document name>

Reviewed: YYYY-MM-DD. Format: text | email | email transmittal | slides | spreadsheet | classified-with-CUI.
CUI category: CTI | other: <category> | not yet determined.

## Findings

| Element | Present or wrong | Fix |
|---|---|---|
| Top/bottom banner | | |
| Designation block, Line 1 (Controlled by) | | |
| Designation block, Line 2 (CUI Category) | | |
| Designation block, Line 3 (LDC or Distribution Statement) | | |
| Designation block, Line 4 (POC) | | |
| Distribution Statement letter (if CTI or export-controlled) | | |
| Distribution Statement full text on page one (if required) | | |
| Export-control warning (if ITAR/EAR applies) | | |
| Format-specific rule for this medium | | |
| Envelope or transmittal treatment (if shipped) | | |

## Carry-forward check
Source of the CUI: own output | customer- or prime-marked, carried forward.
Contract language directing marking, if own output: yes/no, citation: ...

## Result
Clean | needs correction. Corrections required before release: ...
```

## Where practitioners disagree

- **How strictly assessors enforce mechanical marking detail.** One position: every element in this skill's Method is a hard requirement, because the training aid states it as mandatory. The other, drawn from field experience: in practice, few assessors comb through every page looking for a marking defect once the underlying handling process looks sound, so a single file missing a Distribution Statement letter rarely becomes the finding on its own. Treat the mechanical rules as the standard to build toward regardless; the outcome depends on the assessor.
- **Whether to apply your own banner to a document you created that merely re-uses a customer's already-marked content, such as a wrapper memo or a traveler.** One position: mark it, to be consistent and safe. The other: if the constituent customer document already carries its markings, adding a new banner on your own wrapper has you designating CUI on your own output without contract direction, which is the thing the carry-forward rule exists to prevent. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: write the carry-forward and "when required by contract" language into the client's marking policy exactly as this skill states it; a client that over-marks its own IP because a template auto-stamps every document is creating a designation problem for itself, not a safety margin. **OSC seat**: when a document arrives from a prime with markings that look wrong, such as a template Distribution Statement on content that reads like the prime's own IP, do not silently fix it; notify the prime in writing of the category you believe applies and why (`cui-determination-workflow` step 8), and act on any correction.

## Sources

- DoD CUI Program FAQ, Use of Distribution Statements: https://www.dodcui.mil/Frequently-Asked-Questions/Use-of-Distribution-Statements/ (mirrored at `reference/cui-registry/Frequently-Asked-Questions--Use-of-Distribution-Statements.md`).
- DoDI 5230.24, Distribution Statements on DoD Technical Information, January 10, 2023: https://www.esd.whs.mil/Portals/54/Documents/DD/issuances/dodi/523024p.pdf (mirrored at `reference/dod-issuances/dodi-5230-24.md`).
- DoD CUI marking training aid, December 2024, DoD CIO: https://www.dodcui.mil/ (also reference/cui-marking-spec.md).
- DoD CUI Distribution Statements page: https://www.dodcui.mil/Distribution-Statements/.
- DoD CUI Controlled Technical Information category page: https://www.dodcui.mil/Defense/Controlled-Technical-Information/.
- DoD CUI Limited Dissemination Controls page: https://www.dodcui.mil/Limited-Dissemination-Controls/.
- 32 CFR 2002.20: https://www.ecfr.gov/current/title-32/section-2002.20.
- CMMC Level 2 Assessment Guide, DoD CIO, MP.L2-3.8.4: https://dodcio.defense.gov/CMMC/Resources-Documentation/.
- Practitioner consensus, unattributed, backs the carry-forward rule's framing as "authorized holder, not designating agency," the reading of "when required by contract" as correct policy language, and both rows in the disagreement section.
