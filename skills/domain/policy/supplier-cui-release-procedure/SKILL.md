---
name: supplier-cui-release-procedure
description: Decide whether a manufacturer may send a package containing CUI to an outside supplier, finisher, coater, or inspection lab, which of three release paths applies, and what has to be recorded before the package leaves the building. Use this before any outbound shipment or transmittal to a subcontractor that might carry CUI, or when writing the release procedure a supplier-facing policy needs to reference against 3.1.3.
vault_sources:
  - "Supplier CUI Release Procedure"
  - "Machine Shops and CUI"
  - "Paper-Only CUI Environment"
  - "CMMC Flow-Down for Hard-Copy CUI"
  - "CMMC for Subcontractors"
  - "3.1.3"
  - "3.1.20"
  - "3.13.8"
  - "CUI Marking"
  - "raw/AC.L2-3.1.3.md"
  - "raw/SC.L2-3.13.8.md"
  - "raw/CMMC-FAQs-v2.3-May-2026.md"
public_sources:
  - "CMMC Level 2 Assessment Guide, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "CMMC FAQ C-Q11: https://dodcio.defense.gov/CMMC/FAQ/"
  - "DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012"
  - "DFARS 252.204-7021: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7021"
---

# Supplier CUI release procedure

This skill decides whether a package headed to an outside supplier, finisher, coater, or inspection lab may go out, which of three approved release paths applies, and what gets recorded so the company can prove it controlled the flow. It answers a single release decision at a time; it does not run the initial CUI determination on the source document (call `cui-determination-workflow` for that) and it does not decide whether the supplier itself needs a CMMC level (call `flowdown-level-determination`). Use it at the point a job is about to leave the building for outside processing, and reuse its rules when drafting the written release policy that 3.1.3 requires.

## Inputs

- The job or purchase order package headed to the supplier: drawing, model, specification, traveler excerpt, or inspection instruction.
- Any markings already on the source document: proprietary legend, export-control notice, distribution statement, or CUI banner.
- `scope/external-systems.md` (the 3.1.20 list) or an equivalent supplier list, to check whether the receiving supplier already carries a CMMC status or a signed no-digitization commitment.
- `CONTEXT.md` for the client's CUI determinations already on record, so this skill is not re-litigating a status that was already settled.
- The prime or customer's contract flow-down clauses, when available, to check whether a CMMC level was already specified for this data.

## Method

1. **Route the release to one of three approved paths.** Nothing leaves the building outside these three:
   - **Digital CUI path.** The supplier already holds the CMMC level the flowed-down data requires, and the transfer itself uses an approved encrypted channel: a government cloud tenant, DoD SAFE, a prime or customer portal built for this purpose, or an equivalent approved transfer system. Ordinary commercial email does not qualify unless the sending domain is specifically approved and the transmission protection can be shown to be enforced, consistent with the transmission-confidentiality rule at 3.13.8.
   - **Paper-only path.** The supplier receives only hardcopy, signs a written commitment not to scan, photograph, email, upload, key into a system, or otherwise digitize what it receives, and the job owner signs off on that path before anything ships. A supplier who cannot honestly make that commitment does not qualify for this path regardless of how the job is packaged.
   - **No-CUI path.** Purchasing or engineering strips the package down before it goes out, removing controlled drawing content, model geometry, and any other data the supplier does not strictly need, and sends only what is required to quote or perform the work.
   If a job does not cleanly fit one of the three, it does not ship. Get written direction from the CUI owner, the prime, or the customer first; guessing is not a fourth path.

2. **Run four checks before anything is packaged, in order.** Skipping the order produces the same failure every time: someone packages first and asks questions after.
   - Is this actually CUI? Look at everything together rather than any single marking in isolation: what the underlying design or spec document is, the purchase order language, any contract clause that flows requirements downstream, and whatever legend or banner appears on the page. A proprietary stamp or an export-control notice by itself does not settle the question; if the status is unclear, put the question to the customer in writing before treating silence or a guess as a green light.
   - Does the supplier actually need this much? Apply minimum necessary. A finishing house typically needs material, finish spec, tolerance, quantity, and handling instructions, not the full controlled drawing.
   - Is the supplier approved for the specific path chosen? A supplier is not automatically qualified for digital CUI because it is qualified for paper-only, and vice versa; check the path, not just the supplier's general standing.
   - Is the transfer method itself an approved one? Personal email accounts, consumer file-sharing links, and text messages are never approved transfer methods for CUI, regardless of which release path applies.

3. **Record six fields for every release, against 3.1.3.** This is the minimum enforcement record an assessor will ask to see:

   | Field | What goes here |
   |---|---|
   | Job or PO number | Ties the release to a specific order |
   | Supplier | Who is receiving the package |
   | What CUI | Plain description of the data, not just "the drawing" |
   | Release path | Digital CUI, paper-only, or no-CUI |
   | Transfer method | The specific approved channel used |
   | Approver and date | Who signed off and when |

   Whoever holds this authority, typically an operations, quality, or compliance role, should be named on a short internal authorization list rather than left to whoever happens to be at a desk that day.

4. **Use two standing notes rather than drafting language every time.** A paper-only supplier note states, in plain terms, that the package may contain CUI, that use is limited to the named job, that the supplier must not scan, photograph, email, upload, key in, or otherwise digitize it, that it must be stored so only people working the job can reach it, and that it must be returned or destroyed on the company's instruction once the job closes. A customer clarification note asks the customer to confirm, in writing, whether the material being excerpted or attached is CUI, and if so to state the category, the markings that apply, any dissemination limits, and whether a CMMC requirement needs to flow down to the receiving supplier. Keep both as reusable templates rather than freehand emails, so the content does not drift release to release.

5. **Keep five pieces of evidence per release.** A digital-path release needs the supplier's CMMC status or approval record; a paper-only release needs the signed no-digitization commitment; every release needs a copy or accurate description of what actually went out, a record of the transfer method or shipping details, and, when the status was ever unclear, the written customer clarification and its answer. Missing any one of these turns a defensible release into a guess after the fact.

6. **Apply the decision table below to the situations that come up most often.**

   | Situation | Path | Required checks | Notes |
   |---|---|---|---|
   | Supplier already holds the required CMMC status and can receive digitally | Digital CUI | Confirm status still current; confirm transfer channel is approved | Fastest path when it applies |
   | Supplier has no CMMC status and works paper-only | Paper-only | Get the signed no-digitization commitment before shipping | Job owner sign-off is mandatory, not optional |
   | Supplier only needs bid or process information, not the controlled data itself | No-CUI | Strip the package to material, finish, tolerance, quantity, handling | Cheapest and lowest-risk path when the work allows it |
   | Customer markings are missing, inconsistent, or ambiguous | None yet | Send the clarification note; hold the release until answered | Do not release on an assumption |
   | Rush job, no time to vet a new supplier | No-CUI if at all possible | If digital or paper-only is unavoidable, get the fastest path that still meets its own checks | A deadline does not waive any of the four pre-send checks |

7. **Apply two supporting patterns as standing rules, not one-off decisions.** First, when a part physically travels to an outside finisher, coater, or platter along with its paper plans, put the no-scan, no-photograph, no-email commitment and a destroy-on-return instruction into the shipping arrangement itself, the same way a service agreement would bind any other outside vendor; the plans travel with the part and come back or get destroyed, they do not get filed anywhere else. Second, favor physically mailing a paper package over emailing a digital one when the receiving supplier has no realistic path to CMMC capability; a supplier that never receives anything digital never becomes a CUI Asset in the first place. This second point rests on practitioner consensus, unattributed, rather than a written rule in any guide.

## Output

Write the release record to `evidence/supplier-releases/<job-or-po>.md`:

```markdown
# Supplier CUI release: <job or PO number>

## Decision
- Path: <digital CUI | paper-only | no-CUI>
- Reasoning: <why this path fits, referencing the four pre-send checks>

## Approval record
| Field | Value |
|---|---|
| Job/PO number | |
| Supplier | |
| What CUI | |
| Release path | |
| Transfer method | |
| Approver and date | |

## Evidence attached
- [ ] Supplier CMMC status or approval (digital path)
- [ ] Signed no-digitization commitment (paper-only path)
- [ ] Copy or description of what was sent
- [ ] Transfer method or shipping record
- [ ] Customer clarification and answer, if the status was ever unclear

## Open items
- <anything still unresolved, e.g. clarification requested but not yet answered>
```

This file becomes evidence for 3.1.3. If the release also implies a CMMC level requirement on the supplier, hand off to `flowdown-level-determination`.

## Where practitioners disagree

- How much independent judgment a company may exercise when a customer's markings look sensitive but are not explicitly CUI. One position holds that only the customer or CUI owner can make the call, so every ambiguous marking gets a written question and a held release. The other accepts a documented, good-faith interim treatment, applying the markings as received with notice to the customer and an opportunity for the customer to correct it, so work does not stop on every borderline case. The outcome depends on the assessor.
- Whether to flow a CMMC certification requirement down to a paper-only supplier anyway, as a hedge against the supplier eventually digitizing something. Over-flowing costs little and closes a gap; under-flowing keeps a genuinely paper-only, low-capability supplier off the hook it does not need to carry. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: build the two standing notes and the authorization list as part of the engagement's policy package, and walk the buyer or operations lead through one live release before leaving them to run it themselves. **OSC seat**: assign the six-field record and the authorization list to whoever already approves outbound job packages, usually operations or quality, rather than creating a new approval step nobody owns.

## Sources

- CMMC Level 2 Assessment Guide, DoD CIO, AC.L2-3.1.3 and SC.L2-3.13.8: https://dodcio.defense.gov/CMMC/Resources-Documentation/
- CMMC FAQ C-Q11, on paper-only handling and what triggers full assessment scope: https://dodcio.defense.gov/CMMC/FAQ/
- DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012
- DFARS 252.204-7021: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7021
- Practitioner consensus, unattributed, backs the three-path routing structure, the four pre-send checks, the six approval fields, the two standing notes, the five evidence items, the decision table, the finishing-house shipping pattern, and the preference for physical mail over email to keep incapable suppliers out of scope.
