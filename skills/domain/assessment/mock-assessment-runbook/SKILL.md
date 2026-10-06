---
name: mock-assessment-runbook
description: Decide between a gap assessment, a mock assessment, and booking the real certification assessment, gate the choice on prerequisites, and run the mock against all 320 assessment objectives for effectiveness rather than compliance. Use when an organization is choosing its pre-certification assessment path, or asks whether it is ready to book the real one.
vault_sources:
  - "3.12.1"
  - "3.12.3"
  - "Practitioner insights A"
  - "Practitioner insights B"
  - "Client Onboarding Checklist"
  - "Client Onboarding Discovery Checklist"
  - "raw/practitioner-community-export-2026-09-02.md"
  - "raw/public-talk-transcript-M3hoc973lBE.md"
public_sources:
  - "CMMC Level 2 Assessment Guide, DoD CIO, CA.L2-3.12.1, CA.L2-3.12.3: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "32 CFR 170.24(b): https://www.ecfr.gov/current/title-32/section-170.24"
  - "NIST SP 800-171A: https://csrc.nist.gov/pubs/sp/800/171/a/final"
---

# Mock assessment runbook

This skill answers: which pre-certification assessment does this organization need next, and what should the mock actually test once it is warranted? It gates the choice on real prerequisites instead of defaulting to whatever a vendor sells first, and it runs a mock against the full set of assessment objectives, scored for effectiveness rather than a checklist read of the SSP. What this skill cannot give you is a ready-made agenda, an evidence request list, or interview scripts; those do not exist as a packaged artifact here, and the runbook says so rather than inventing them. Call the Skill tool with `control-evidence-lookup` for what counts as acceptable evidence once you know which objectives to test, and `ssp-statement-writer` for the lint pass against supporting documents.

## Inputs

- The SSP, which is the record, `ssp/ssp.json`: call the Skill tool with `scribe` and ask it to show the whole record. It gives the statements and their statuses on every objective, the components, the assets with their categories, and the providers. A record whose objectives are all still planned on "This System" with "Not yet written." is an honest statement that no SSP exists yet. Never read `view/` instead; the view is generated for people and can be stale.
- The network diagram, `scope/network-diagram.drawio` (drawn by `cmmc-boundary-diagram`), beside the assets and categories in the record, to confirm the boundary is actually drawn.
- Any prior gap assessment, POA&M, or self-assessment score already on file.
- The assessment date being targeted, if one is set.

## Method

1. **State the disagreement honestly before choosing a path.** Practitioners disagree sharply on the value of a standalone gap assessment. One position holds that a gap assessment run early, without an SSP and without a drawn boundary, tells the client little beyond what a scope assessment would tell them for less money and more use, because a laundry list of "what's wrong" is not actionable without a scope to hang it on. Another position stresses that outright failure at the real assessment, or being told to come back later, happens more often than certification does, and both outcomes get recorded in eMASS and reflected in the SPRS score, so a mock run first is worth the cost even for an organization that feels ready. Present both positions when advising; do not resolve them for the operator. The outcome depends on the assessor and on how mature the organization already is.

2. **Gate the choice on three prerequisites before recommending anything.** Ask, in order:
   - Does an SSP exist, even a rough one, describing how each requirement is implemented?
   - Is the network actually segmented, or is it one flat network with everything reachable from everywhere?
   - Is the CMMC Assessment Scope drawn, with an asset inventory assigning each asset a category?
   If any answer is no, the recommendation is scoping work first, not a gap assessment and not a mock. Running either exercise against an undocumented, unsegmented, unscoped environment produces a list of problems with no structure to prioritize them, which is close to the least useful version of this exercise.

3. **Route the decision once prerequisites are met.**

   | Situation | Recommended path |
   |---|---|
   | No SSP, no drawn scope, flat network | Scoping and SSP work first; neither a gap nor a mock assessment yet |
   | SSP and scope exist, organization has never had outside eyes on its posture | A scope-focused review, checking the boundary and asset categorization decisions, before a full mock |
   | SSP and scope exist, organization has already validated its scoping decisions | A mock assessment against the full objective set |
   | Organization believes it is ready and wants a final check before booking certification | A mock assessment, run the same way the real assessment will be run |

4. **Run the mock against all 320 assessment objectives, not the 110 requirements.** Scoring at the requirement level hides which specific objective is the actual gap, and the real assessment scores at the objective level. A mock that only checks "is 3.3.3 basically covered" will miss, for example, that the review process exists but was never actually exercised, which is an objective-level failure the requirement-level view cannot see.

5. **Score for effectiveness, not compliance.** The question for each objective is not "does the SSP say we do this," it is "is this an effective way to meet the intent of the requirement." A standard compliance read-through, where the reviewer reads the SSP narrative and confirms the described activity happens, is a materially weaker exercise than one that asks whether the control is actually achieving the risk reduction it is supposed to achieve. Build this distinction into the mock's scoring guide explicitly, or the mock will only catch what a checklist would have caught.

6. **Lint the SSP against its supporting documents before the mock, not during it.** Contradictions between the SSP narrative and the underlying evidence, such as a stated lockout threshold that does not match the actual configuration, are common and easy to find in advance. Many real assessments only permit a small number of document corrections once the assessment has started, so finding and fixing these contradictions before the mock, rather than discovering them live, protects that limited allowance for genuine surprises. Call the Skill tool with `ssp-statement-writer` in lint mode for this pass.

7. **Treat the output as a punch list, not a pass or fail badge.** The mock's value is the list of specific objective-level gaps it produces, each with the evidence or process change needed to close it, not a single readiness score. Feed that list back into `evidence-package-builder` for the artifacts it identifies as missing.

## Output

Write the record to `evidence/mock-assessment/<date>.md`. It is evidence for 3.12.1 as well as a working paper, so it goes in the evidence folder rather than the scratch folder.

```markdown
# Mock assessment record

## Prerequisite gate
- SSP exists: yes/no
- Network segmented: yes/no
- Scope drawn with asset categories: yes/no
- Gate result: proceed to mock | scoping work required first

## Path recommendation
Recommended path: scope review | mock assessment | not ready for either
Rationale: ...

## Objective-level results (320 objectives)
| Requirement | Objective | Evaluated for effectiveness? | Result | Gap, if any |
|---|---|---|---|---|
| 3.12.1 | [a] | | | |
| 3.12.1 | [b] | | | |

## SSP-to-evidence lint findings
| SSP claim | Supporting document says | Contradiction? |
|---|---|---|

## Punch list
- [ ] ...
```

File at `evidence/mock-assessment/<date>.md`, and open a tracked item for each punch-list entry per the existing POA&M or OPA routing rules.

## Where practitioners disagree

- **Whether a standalone gap assessment is worth running.** See the disagreement stated in step 1. Some hold it is low-value without a scope assessment behind it and criticize gap analyses run on a flat, unscoped network. Others treat a mock assessment as close to mandatory before booking certification, because failure at the real thing is common and gets recorded. The outcome depends on the assessor and on the maturity of the organization at the time the question is asked.

## Seat notes

**Consultant seat**: use the prerequisite gate to have the harder conversation early. Selling a gap assessment to a client with no SSP and a flat network produces a report that looks like deliverable work but does not move the client closer to certification; recommend scoping first even when it is the less immediately billable answer. **OSC seat**: if your internal team is running this without outside help, be honest in the gate about whether your network is actually segmented; "we think it's segmented" is not the same as a diagram showing it.

## Sources

- CMMC Level 2 Assessment Guide, DoD CIO, CA.L2-3.12.1, CA.L2-3.12.3: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (the effectiveness-versus-compliance distinction and the periodic-assessment requirement behind the mock).
- 32 CFR 170.24(b): https://www.ecfr.gov/current/title-32/section-170.24 (the three assessment findings and the evidence-in-final-form rule the mock should already be testing against).
- NIST SP 800-171A: https://csrc.nist.gov/pubs/sp/800/171/a/final (the 320 assessment objectives the mock scores against, rather than the 110 requirements).
- Practitioner consensus, unattributed, backs the prerequisite gate in step 2, the routing table in step 3, the effectiveness-scoring rule in step 5, the pre-mock lint recommendation in step 6, and the disagreement recorded above. No packaged mock agenda, evidence request list, or interview script exists in the source material behind this skill; do not present one as though it does.
