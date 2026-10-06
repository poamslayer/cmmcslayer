---
name: significant-change-determination
description: Decide whether a proposed change to a certified CMMC environment is a significant change, using four gates, and produce the determination memo and execution checklist the Affirming Official signs. Use before adding, swapping, or migrating any tool, provider, site, operating system, or cloud service in a certified scope.
vault_sources:
  - "CMMC Significant Change Determination"
  - "3.1.20"
  - "POA&M Eligibility"
  - "3.12.2"
  - "CRM Systems and CUI"
  - "raw/practitioner-community-export-2026-05-12a.md"
  - "raw/CMMC-FAQs-v2.3-May-2026.md"
public_sources:
  - "CMMC FAQ C-Q9, C-Q12, F-Q5: https://dodcio.defense.gov/CMMC/FAQ/"
  - "32 CFR 170.21 (POA&M): https://www.ecfr.gov/current/title-32/section-170.21"
  - "32 CFR 170.24 (scoring, OPA treatment): https://www.ecfr.gov/current/title-32/section-170.24"
  - "32 CFR 170.4 (Operational Plan of Action definition): https://www.ecfr.gov/current/title-32/section-170.4"
  - "DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012"
  - "DoD CIO FedRAMP Moderate Equivalency memo: https://dodcio.defense.gov/Portals/0/Documents/Library/FEDRAMP-EquivalencyCloudServiceProviders.pdf"
  - "CMMC Level 2 Assessment Guide, DoD CIO, AC.L2-3.1.20, CM.L2-3.4.3, CM.L2-3.4.4, CA.L2-3.12.2, CA.L2-3.12.4: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
---

# Significant change determination

This skill answers: is this change to a certified environment significant, meaning large enough to require a new assessment, and what has to happen before it is deployed? It walks four gates in order, tells you what the answer means, and produces the memo the Affirming Official signs plus the execution checklist. It does not make the decision. The Affirming Official does, because that person carries the legal and contractual risk of continued compliance (CMMC FAQ C-Q12). It does not decide whether a product is a good buy, and it does not draw the new boundary; call the Skill tool with `cmmc-scope-boundary` or `esp-and-msp-scoping` for the placement work once the gates are answered.

## Inputs

- The proposed change in one paragraph: what is being added, swapped, migrated, or removed, and when.
- The certified state: the SSP as assessed, which is the record, `ssp/ssp.json`, at the commit the assessment was made against, with its components, assets and categories, providers, and statements; the network and data flow diagrams; and `scope/external-systems.md` (the 3.1.20 list). Call the Skill tool with `scribe` and ask it to show the record, once in a checkout of that commit and once as it stands now, so the two can be compared. Never read `view/` instead; it is generated for people and can be stale.
- The certification record: assessment date, C3PAO, any requirement or objective assessed N/A, and the CMMC Status Date.
- For a cloud service: its FedRAMP status or equivalency evidence, and whether it will process, store, or transmit CUI.
- The name of the Affirming Official and the change-control process reference (3.4.3).

## Method

Walk the gates in order. Stop at the first one that ends the question.

1. **Gate 1: can the service be used in scope at all?** If the change is a cloud service that will process, store, or transmit CUI, it needs FedRAMP Moderate authorization or equivalency under the DoD CIO memo (DFARS 252.204-7012; FAQ E-Q1). Encrypting the CUI does not remove that bar (FAQ E-Q2). No authorization and no defensible equivalency evidence means this is not a change question at all; it is a "you cannot use this in scope" answer. Stop, and tell the operator to fix the gating problem first. If the tool touches only Out-of-Scope Assets and can reach no CUI Asset, no SPA, and no CRMA, then no scope event has occurred; record that finding and stop.

2. **Gate 2: was the capability in the assessed environment?** FAQ C-Q12 gives the three cases and the deciding question: does the resulting environment include systems, configurations, or security tools that have never been assessed?

   | Change | Likely answer | Why |
   |---|---|---|
   | Like-for-like swap of an assessed, authorized service for another of the same kind (a FIPS 140-2 firewall for a FIPS 140-3 one, one authorized RMM for another with the same reach) | Not significant, routine configuration management | FAQ C-Q12 case 2 |
   | More of the same: a new building on the same baseline, more endpoints with the same image | Not significant | Nothing new to assess; practitioner consensus |
   | A capability that was assessed N/A and is now used (wireless added to a scope certified without it) | Significant, reassessment required | FAQ C-Q12 case 1 |
   | A new capability that was not in the certified environment (a new SPA with admin reach, a new external system that will hold CUI) | Significant, or at least requires careful evaluation | FAQ C-Q12 case 3 |
   | A new operating system family in scope (macOS or Linux when only Windows was assessed) | Significant | FAQ C-Q12 case 3 example |
   | A new CSP holding CUI, or a migration between fundamentally different environments (one cloud to another, enclave to enterprise) | Significant | The assessed SSP no longer describes the system |
   | A new physical site holding CUI when the assessment was single-site | Significant boundary change | New physical requirements to evidence |
   | Replacing the MSP | Likely significant | New people with admin access, new processes, new evidence sources |
   | Adding a FedRAMP-authorized SaaS tool that will hold CUI, through a mature change process | Contested | See the disagreement section |

3. **Gate 3: which scope artifacts shift?** Check each one and record whether the change alters it materially:
   - Asset inventory: new category or a new kind of asset, not just a count.
   - Network diagram: new components or new flows.
   - Data flow diagram: a new CUI path.
   - Authorization boundary: the line moves.
   - 3.1.20 external systems list: a new entry.
   - Responsibility matrix: a new shared-responsibility surface.
   The plain test: if an assessor walked the floor today holding the assessed SSP, would they find something material the document does not describe? If yes, lean significant.

4. **Gate 4: how many families gain new evidence?** A new component usually creates evidence under Access Control (new accounts and paths), Audit and Accountability (new log source), Configuration Management (baseline change), Identification and Authentication (new MFA point), and System and Communications Protection (new boundary crossing or encryption in transit). Count them. Three or more families with new evidence is almost always significant. One family, with the change absorbed by an assessed process, usually is not. FAQ F-Q5 gives the same signal from the other side: if the security impact analysis under 3.4.4 finds a risk the existing SSP does not address, you probably have a significant change.

5. **State who decides.** Write in the memo, in these words: the Affirming Official decides whether this change is significant enough to require reassessment (FAQ C-Q12). The consultant advises. The C3PAO's view is input, and the C3PAO has a revenue interest in a reassessment, so treat it as data and not as the answer. Nothing at the next triennial assessment enforces a mid-cycle reassessment; what the next assessor will check is whether the change was managed as the SSP says and whether the affected requirements are still MET.

6. **Route any deficiency the change creates.** FAQ C-Q9: a temporary deficiency that arises after the system was compliant goes on an Operational Plan of Action (OPA) and is assessed MET under 32 CFR 170.24(b)(1)(ii); a deficiency found during an assessment and scored NOT MET goes on a POA&M with the 180-day clock (32 CFR 170.21). A deficiency the company can fix on its own schedule is a POA&M item, not an OPA item. Call the Skill tool with `poam-or-opa-router` for the routing.

7. **Run the execution checklist when the answer is significant**, in this order:
   1. Halt deployment until the memo is signed and the SSP is updated.
   2. Affirming Official signs the memo, which carries the date, what changed, the scope impact, the rationale, and the risk accepted.
   3. Change-control package approved under 3.4.3 with the security impact analysis under 3.4.4.
   4. Update the 3.1.20 external systems list; review the responsibility matrix and assign customer responsibilities.
   5. Update the SSP: diagram, inventory, data flow, and every conformity statement the change touches (3.12.4).
   6. Provision accounts with MFA, least privilege, and separation of duties.
   7. Wire the new component's logs into the central log platform.
   8. Notify the C3PAO and agree the delta assessment scope and timing.
   9. File the artifact bundle, so the trail is waiting for whoever assesses next.

8. **When the answer is not significant, still do four things.** Run the change through the existing change-control process, update the SSP and inventory, add the entry to the 3.1.20 list if it is an external system, and have the Affirming Official sign the "not significant" determination, briefly. The signed memo is what the next assessor wants to see; the absence of the paperwork is what draws the finding, not the change itself.

## Output

A determination memo at `docs/adr/NNNN-significant-change-<short-name>.md`:

```markdown
# ADR-NNNN: Significant change determination, <change>

Date: YYYY-MM-DD. Status: proposed | signed.
Affirming Official: <name and title>. Certified scope as of: <assessment date>.

## The change
One paragraph: what, when, who operates it, what it touches.

## Gate 1: usable in scope?
FedRAMP status or equivalency evidence: ... Touches CUI: yes/no. Reaches only Out-of-Scope Assets: yes/no.
Result: proceed | cannot be used in scope | not a scope event

## Gate 2: capability in the assessed environment?
Row from the table: ... Requirements or objectives previously N/A that become applicable: ...
Result: routine CM | significant | requires evaluation

## Gate 3: scope artifacts that shift
| Artifact | Changes materially? | How |
|---|---|---|
| Asset inventory | | |
| Network diagram | | |
| Data flow diagram | | |
| Authorization boundary | | |
| 3.1.20 external systems list | | |
| Responsibility matrix | | |

## Gate 4: families gaining new evidence
| Family | New evidence | 
|---|---|
Count: n. Security impact analysis (3.4.4) found a risk the SSP does not address: yes/no.

## Determination
Significant: yes | no. Rationale: ...
Deficiencies created and their route: OPA | POA&M | none.
The Affirming Official decides (CMMC FAQ C-Q12). Consultant recommendation: ... C3PAO input, if any: ...

## Execution checklist
- [ ] Deployment halted until signed
- [ ] Determination memo signed by the Affirming Official
- [ ] Change-control package approved (3.4.3) with security impact analysis (3.4.4)
- [ ] 3.1.20 list updated; responsibility matrix reviewed
- [ ] SSP updated (3.12.4): diagram, inventory, data flow, conformity statements
- [ ] Accounts provisioned with MFA, least privilege, separation of duties
- [ ] Logging wired to the central log platform
- [ ] C3PAO notified; delta scope and timing agreed
- [ ] Artifact bundle filed at evidence/changes/<short-name>/

Signed: ____________________ Date: __________
```

Reference the memo from the SSP change log and from `CONTEXT.md` if the change introduces a new term. Open a GitHub issue labeled `opa` or `poam` for any deficiency, per step 6.

## Where practitioners disagree

- **Adding an authorized SaaS tool to CUI scope through mature processes.** One position: it is a new external system holding CUI, so FAQ C-Q12 case 3 applies and it is significant. The other: the change-control process, the 3.1.20 approval workflow, and the CUI flow controls were all assessed, so the assessor would only verify the authorization, the responsibility matrix, and that the processes were followed, which is a short delta and not a reassessment. The outcome depends on the assessor.
- **Reassessment scope when a change is significant.** One position: the whole scope is reassessed. The other, drawing on the FedRAMP significant-change model: only the change and the requirements it touches. The outcome depends on the assessor.
- **A new CSP when the organization already had one.** Some treat it as a significant architectural change; others as one more node under a responsibility matrix and existing processes, not a boundary change. The outcome depends on the assessor.
- **Replacing the MSP.** Widely held to be stickier than swapping a cloud service, because people and processes change, but not universally called significant. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: your deliverable is the analysis and the recommendation line; never sign the memo and never let the client believe you decided. Put the contested rows on the C3PAO question list before the delta is scoped. **OSC seat**: the Affirming Official is probably your owner or president; walk them through the four gates in one sitting and get the signature the same day, whichever way the answer goes. An unsigned "not significant" is the finding waiting to happen.

## Sources

- CMMC FAQ C-Q9, C-Q12, F-Q5: https://dodcio.defense.gov/CMMC/FAQ/.
- 32 CFR 170.21: https://www.ecfr.gov/current/title-32/section-170.21 (POA&M gates and the 180-day closeout; see also reference/32-cfr-170-21-poam-gates.md).
- 32 CFR 170.24: https://www.ecfr.gov/current/title-32/section-170.24 (OPA and enduring exceptions assessed MET; see also reference/32-cfr-170-24-scoring.md).
- 32 CFR 170.4: https://www.ecfr.gov/current/title-32/section-170.4.
- DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012.
- DoD CIO FedRAMP Moderate Equivalency memo: https://dodcio.defense.gov/Portals/0/Documents/Library/FEDRAMP-EquivalencyCloudServiceProviders.pdf.
- CMMC Level 2 Assessment Guide, DoD CIO, AC.L2-3.1.20, CM.L2-3.4.3, CM.L2-3.4.4, CA.L2-3.12.2, CA.L2-3.12.4: https://dodcio.defense.gov/CMMC/Resources-Documentation/.
- Practitioner consensus, unattributed, backs the "more of the same" row and the MSP replacement row in Gate 2, the three-family threshold in Gate 4, the C3PAO incentive warning in step 5, and the execution checklist order in step 7.
