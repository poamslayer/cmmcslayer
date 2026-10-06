---
name: printer-and-ot-asset-scoping
description: Categorize printers, multifunction devices, print servers, CNC controllers, coordinate measuring machines, and PLCs for the CMMC Assessment Scope. Forces a documented choice among the three contested printer positions, places shop-floor controllers as Specialized Assets with their kind, records each device, its category, and the real attributes it needs in the SSP through scribe, and flags the Rev 3 FIPS problem for networked print devices. Use whenever an operator is categorizing printers, MFPs, or operational technology on a shop floor.
vault_sources:
  - "Printer Scoping"
  - "Machine Shops and CUI"
  - "3.13.8"
  - "3.13.11"
  - "3.13.7"
  - "Rev 2 vs Rev 3 Double Baseline"
  - "Client Onboarding Checklist"
  - "raw/practitioner-community-export-2026-09-02.md"
  - "raw/practitioner-community-export-2026-09-03.md"
public_sources:
  - "CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "32 CFR 170.19 (Specialized Asset definition): https://www.ecfr.gov/current/title-32/section-170.19"
  - "32 CFR 170.4 (definitions, including Test Equipment): https://www.ecfr.gov/current/title-32/section-170.4"
  - "CMMC Level 2 Assessment Guide, DoD CIO, SC.L2-3.13.8: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "CMMC Level 2 Assessment Guide, DoD CIO, SC.L2-3.13.11: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
---

# Printer and OT asset scoping

This skill categorizes the two hardest classes of physical asset in a manufacturing environment: printers and multifunction devices, whose category is unsettled among assessors, and shop-floor operational technology (CNC controllers, coordinate measuring machines, PLCs), whose category is settled but often under-documented. It forces a recorded choice for printers rather than leaving the category implicit, records each device and its category in the engagement's SSP by calling the Skill tool with `scribe`, and flags a forward-looking encryption problem for networked print devices. It does not run the separation test itself (call `logical-separation-test` for that) and it does not write the SSP risk-based management policy the category requires (that belongs to the engagement's SSP-writing skill).

## Inputs

- Every printer, plotter, label printer, and multifunction device (MFP) in the environment, with its network connection type.
- Every CNC controller, coordinate measuring machine (CMM), and programmable logic controller (PLC) on the shop floor.
- The print path from the endpoint that sends the job, through any print server, to the device.
- The engagement's record, `ssp/components/*.md`: the printers and shop-floor devices already recorded, their components, and their categories, so a device is added consistently and a wrong category left by earlier work is found and corrected. Read the files directly; they are the current state. Never read `view/asset-inventory.md`; it is generated for people. The walk, the company's own documents, and the record are the sources.
- `scope/cui-determinations.md`, for which documents are CUI. Whether a device prints, scans, or stores CUI takes that status from the determinations; never infer it yourself from what a file was made from. When an item has no determination, do not decide it here. Place the device on facts that do not depend on it, and put the question on `scope/open-items.md` for `cui-determination-workflow`.
- `scope/network-diagram.drawio` and `scope/network-diagram.md`, and `docs/adr/` for recording the forced printer choice.
- Whether the client is planning a NIST SP 800-171 Revision 3 transition timeline, for the FIPS flag in step 5.

## Method

1. **Force a documented choice among the three printer positions.** No consensus exists on where a printer, multifunction device, or print server belongs, and any assessor may hold any of the three positions:
   - **In scope as a CUI Asset.** A device that prints, scans, or stores CUI processes it, and that is a CUI Asset under the Process/Store/Transmit test, assessed like any other. Take this position when the device can be secured with ordinary IT controls.
   - **In scope as a Specialized Asset, when it cannot be secured.** The printer is treated the same way a CNC controller is: it takes a digital input and produces a physical output, and its firmware resists standard hardening. Under this reading it is documented in the inventory, SSP, and diagram under a risk-based policy but not assessed against the 110 Level 2 requirements directly. Record it with the kind that fits what it is, usually OT, and say in the remarks why it cannot be secured.
   - **Taken off the CUI path.** The device stops touching CUI: CUI printing moves to another device, scan-to-email and network scan destinations for CUI are removed, and the path is closed technically, not by a policy alone. Only then can it be Out-of-Scope, and only if `logical-separation-test` returns isolation, not controlled access. This is the hardest position to defend.

   "Policy prohibits printing or scanning CUI" is none of the three. A device that still can, and does, is a CUI Asset. A device on an open path that nobody uses for CUI is a Contractor Risk Managed Asset (CRMA) only when a written policy and procedure keep CUI off it; with none, it is a CUI Asset.

   Do not leave the category implicit. Name all three positions in the device's remarks and say which one the client chose, and write the rationale in an ADR (see Output). When nobody at the client can be asked, record the device in the category it holds today, which for a device that prints or scans CUI is a CUI Asset, put the choice on `scope/open-items.md`, and write no ADR until the client chooses.

2. **Put every printer on the facility diagram regardless of the category chosen.** Assessors check for printers physically during a walkthrough and compare what they find to the diagram. A printer missing from the diagram is a finding independent of which of the three positions was chosen for it.

3. **Treat CNC controllers, CMMs, and PLCs as Specialized Assets without debate.** Unlike the printer question, this one is settled: shop-floor operational technology that can process, store, or transmit CUI but cannot be fully secured with standard IT controls is a Specialized Asset under 32 CFR 170.19(c). Record its kind: OT for a CNC controller or a PLC, and OT or test equipment for a coordinate measuring machine, whose job is measurement. Document it in the asset inventory, the SSP under a risk-based management policy, and the network and facility diagrams. It is not assessed against the Level 2 requirements directly at a Level 2 assessment.

   **A computer beside a machine is Specialized only when it is part of the machine.** 32 CFR 170.4 defines test equipment as hardware "and/or associated IT components" used in testing, so a PC dedicated to a measuring machine's software, doing nothing else, can be a Specialized Asset (test equipment) with the machine. A PC that holds or saves files to shares, prints, or reaches email as any workstation does is a CUI Asset when it passes the Process/Store/Transmit test, however close it sits to a machine; a general-purpose PC that sends programs to a CNC is an endpoint, and `endpoint-and-vdi-scoping` places it. A PC is never OT, and an old or unpatchable operating system is never the reason for either answer: it is a finding against the requirements (3.14.1, handled as an enduring exception or on a POA&M). Say in the remarks which of the two the PC is and what it does besides serve the machine.

4. **Record the real attributes, not just the device name.** For every printer, multifunction device, plotter, and label printer, capture: the model, whether it carries onboard storage and what is on it, where it can scan a document to (email address, network folder), whether it accepts wireless or cloud-submitted jobs, whether it holds a job until a user badges in to release it, and whether its USB port is enabled. Record who services the device and whether that vendor dials in remotely; a remote-servicing path is its own reachable connection and may need its own row under an MSP or vendor scoping exercise. For every CNC controller, CMM, and PLC: operating system and support status (legacy Windows controllers bolted to CNCs are common), whether it is networked or air-gapped, and how programs reach it (network transfer, USB, or operator entry). The attributes someone has verified go in the device's description and remarks in the record (see Output); an attribute nobody has checked goes on `scope/open-items.md`, with who will check it.

5. **Trace the print path and decide before the assessor asks.** Draw the path from the sending endpoint, through any print server, to the device on the data flow diagram. The category decision in step 1 should already be recorded by the time this trace is complete; do not leave the rationale to be improvised at assessment.

6. **Apply the accepted shop-floor separation pattern between CUI and OT.** Where a CUI-handling workstation sits physically next to a CNC control PC, the accepted pattern is to disable USB storage on the CUI workstation and place it on a different subnet than the OT machine, so that any transfer between the two requires a deliberate, documented path rather than a shared broadcast domain or a thumb drive. Treat a shop that cannot show this separation as carrying an undocumented data flow, not a compliant one.

7. **Flag the Revision 3 FIPS problem for networked print devices, as a forward-looking risk, not a current Rev 2 failure.** Under the current NIST SP 800-171 Revision 2 baseline, 3.13.8 accepts a well-controlled physical environment as a stand-in for encrypting CUI in transit, which is why a networked multifunction device inside a locked facility can print CUI today without a FIPS-validated encryption module. Revision 3 drops that physical-safeguards option entirely, which leaves the FIPS-validated cryptography demanded by 3.13.11 with nothing to fall back on for a networked device that has its own internal storage. Once Revision 3 applies, the options narrow to a FIPS-validated print path or air-gapping the device and printing CUI only over a direct USB connection. Verify any printer's claimed encryption against the CMVP validated modules database before relying on it; a vendor datasheet that says "FIPS compliant" is not evidence of a validated module. Because a separate government-wide rulemaking track can bring Revision 3 forward independent of the CMMC program's own timeline, do not tell a client this problem is years away by default; put it on the roadmap now and take a FIPS-capable printer if one is being purchased anyway for other reasons.

## Output

Record every device in the SSP by calling the Skill tool with `scribe`, one decision per call. Never write the `ssp/` files yourself, and never edit anything under `view/`: the record is the inventory, and scribe renders `view/asset-inventory.md` from it for people. Point the operator at that view when they want to read it.

Tell scribe, in these terms:

1. **The component**: its slug when it is already recorded, or, if it is not, the class of device ("Front office MFP", "Haas CNC mills", "Coordinate measuring machine"), what kind of thing it is (usually a class of hardware), and one line describing it. Give the component a category only when every asset behind it shares that category.
2. **The asset**: its asset id (hostname, asset tag, or a plain name such as "CMM measuring head"), its component, its category, a short description carrying the model and the verified attributes from step 4, and remarks carrying the reason. A printer's remarks name the three positions from step 1 and the one chosen, or say the choice is on the open items list. A Specialized Asset also gets its kind: OT, test equipment, IoT, industrial IoT, government-furnished equipment, or restricted information system. An Out-of-Scope Asset must carry its justification in its `justification` field, naming the technical barrier and the `logical-separation-test` verdict that makes Process/Store/Transmit impossible.
3. **A correction**, when the record already holds a device in a category your method rejects: the new category, and remarks saying why the old one was wrong. Correct it in place, naming the asset by its id; do not remove and re-add it.
4. **A split**, when the devices behind one component fall in different categories, such as a CMM measuring head that is a Specialized Asset and the PC beside it that is a CUI Asset: which assets move to a new component, its title, and, when they share one, its category.

Record only printers, multifunction devices, print servers, and shop-floor equipment, with a PC that is part of a machine. A workstation, server, or other asset you notice on the way is not yours to recategorize, even when its recorded category looks wrong: tell the operator which ones and hand them to `cmmc-scope-boundary`, or to `endpoint-and-vdi-scoping` for a general-purpose PC. A copier vendor's remote-servicing path is a provider question for `esp-and-msp-scoping`; name it in the device's remarks.

Before calling scribe, write the decisions as a table and show it to the operator. Record them once the operator confirms, or straight away if the operator asked you to record without stopping. Scribe gets one row per call:

```markdown
| Asset | Component | Category | Kind (Specialized Asset only) | Attributes (the description) | Reason (the remarks, or the justification of an Out-of-Scope Asset) |
|---|---|---|---|---|---|
| <asset id: hostname, tag, or plain name> | <component slug> | CUI Asset / Security Protection Asset / Contractor Risk Managed Asset / Specialized Asset / Out-of-Scope Asset | <OT / test equipment / IoT / industrial IoT / GFE / restricted information system> | <model, storage, scan destinations, OS and support status, network or air gap, program transfer> | <the P/S/T finding; for a printer, the three positions and the one chosen> |
```

If scribe refuses a change, the refusal is the answer: quote scribe's check line, fix the decision, and ask again. Never work around it. An asset id is unique across the whole SSP, and an asset's category must agree with its component's, so a component whose devices now span categories loses its category or is split.

Write the forced printer choice as an ADR once the client has made it. The ADR holds the reasoning; the record holds the category.

```markdown
# ADR: Printer scoping position for <client / environment>

Date: <date>. Status: proposed.

## Context

<the print path traced in step 5, and the output of logical-separation-test on it>

## Decision

Position chosen: CUI Asset (in scope) / Specialized Asset (cannot be secured) / off the CUI path ("cannot" proven).

## Rationale

<why this position over the other two, referencing the logical-separation-test verdict>

## Consequences

<documentation burden this creates: full assessment, SSP narrative under a risk-based policy, or justification only>
```

Every printer, MFP, and OT asset goes on the network diagram regardless of category: once it is recorded, call the Skill tool with `cmmc-boundary-diagram` to redraw `scope/network-diagram.drawio`. Log the Revision 3 FIPS flag on `scope/open-items.md`, which stays Markdown, with a target date if the client has one.

## Where practitioners disagree

The printer category itself is the open question: some assessors hold that a device on the CUI path is a CUI Asset like any other, others accept the operational-technology Specialized Asset reasoning for a device that cannot be secured, and a minority accept an Out-of-Scope claim once the device is off the CUI path and the underlying separation test genuinely returns isolation. Some also accept a CRMA for a device on an open path that nobody uses for CUI, where a written policy and procedure keep CUI off it. All three positions have been held by assessors in practice. The outcome depends on the assessor, which is exactly why step 1 requires a documented choice rather than a default. The CNC, CMM, and PLC classification as Specialized Assets is not contested in the same way; treat that one as settled.

## Seat notes

**Consultant seat**: raise the printer forced choice explicitly with the client's chosen C3PAO before finalizing the ADR, since the position taken should match what that specific assessor is known to accept. **OSC seat**: walk the facility with the inventory checklist in hand rather than relying on an IT asset list; printers, plotters, and shop-floor controllers are the assets most often missing from a desk-built inventory.

## Sources

- CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (the Specialized Asset category and its treatment).
- 32 CFR 170.19: https://www.ecfr.gov/current/title-32/section-170.19 (the Specialized Asset definition covering operational technology, and the CRMA condition).
- 32 CFR 170.4: https://www.ecfr.gov/current/title-32/section-170.4 (the Test Equipment definition, which reaches associated IT components).
- CMMC Level 2 Assessment Guide, DoD CIO, SC.L2-3.13.8: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (the alternative physical safeguards carve-out that Revision 3 removes).
- CMMC Level 2 Assessment Guide, DoD CIO, SC.L2-3.13.11: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (the FIPS-validated cryptography requirement that has no fallback once the carve-out is gone).
- Practitioner consensus, unattributed, backs the three printer positions in step 1, the shop-floor USB and subnet separation pattern in step 6, and the Revision 3 FIPS risk framing in step 7.
