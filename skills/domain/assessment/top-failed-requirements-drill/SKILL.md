---
name: top-failed-requirements-drill
description: Drill the small set of requirements that most often turn up NOT MET at assessment, with the specific reason each one fails and a scenario-based test for incident response. Use when an OSC is within a few months of an assessment and wants the highest-yield preparation, not a full 110-requirement review.
vault_sources:
  - "3.5.3"
  - "3.14.1"
  - "3.11.2"
  - "3.3.3"
  - "3.3.4"
  - "3.3.5"
  - "3.6.3"
  - "3.12.1"
  - "raw/public-talk-transcript-Oxf-d6yoLsc.md"
  - "raw/public-talk-transcript-39YxwH0BZX4.md"
public_sources:
  - "CMMC Level 2 Assessment Guide, DoD CIO, IA.L2-3.5.3, SI.L2-3.14.1, RA.L2-3.11.2, AU.L2-3.3.3, AU.L2-3.3.4, AU.L2-3.3.5, IR.L2-3.6.3, CA.L2-3.12.1: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "CISA Tabletop Exercise Packages: https://www.cisa.gov/cisa-tabletop-exercise-packages"
  - "NDISAC DIB SCC incident response exercises: https://ndisac.org/dibscc/implementation-and-assessment/incident-response-and-management/exercises/"
  - "Washington State cybersecurity tabletop exercises: https://cybersecurity.wa.gov/tabletop-exercises"
  - "Summit 7, C3PAO Panel: Assessor Perspectives from the Field: https://www.youtube.com/watch?v=Oxf-d6yoLsc"
  - "Summit 7, CMMC Level 2 Assessment: What to Expect: https://www.youtube.com/watch?v=39YxwH0BZX4"
---

# Top failed requirements drill

This skill answers: with limited time before an assessment, which requirements deserve the drill first, and why do they actually fail? It is not a substitute for a full mock assessment; call the Skill tool with `mock-assessment-runbook` for that. It covers seven requirements that recur in practitioner accounts of assessment findings, with the specific misreading or gap behind each one, and it runs the one requirement, incident response testing, as a scenario exercise instead of a checklist item. It does not assign a numeric rank to these seven; where the vault's own ranking claims cannot be traced to a source anyone outside the private community can check, this skill says "commonly failed at assessment" instead of a number.

## Inputs

- The record, `ssp/ssp.json`, for each of the seven requirements below, so the drill can compare what the SSP claims against what the requirement actually demands. Call the Skill tool with `scribe` and ask it to show the record for those requirements: each objective's statements come back with their component and status. Never read `view/` instead; it is generated for people and can be stale.
- `evidence/` for whatever artifacts already exist for these seven.
- The assessment date, so the drill can be scheduled to leave time to fix what it finds.

## Method

Work the seven requirements in this order. For each, the rule is not "do you have a control," it is "which specific misreading causes this control to fail anyway."

1. **3.5.3, multifactor authentication.** Commonly failed at assessment. The recurring misreading is scope: "network access" in the requirement text covers all access to the network, not only remote or internet-facing access. An implementation that covers a VPN and a cloud tenant but leaves the local network login unprotected has not met the requirement. A second recurring gap is enforcement: multifactor authentication configured at account enrollment only, with no re-challenge afterward, or with a password-only fallback still available, does not satisfy the objective even though the feature is technically turned on. A hardware-backed local sign-in (a trusted platform module plus a PIN) is defensible under the underlying NIST authentication guidance, but an assessor who cannot see two distinct factors in the sign-in flow may not accept it without a clear explanation, so document the technical basis before the interview, not during it.

2. **3.14.1, flaw remediation.** Commonly failed at assessment. The requirement has six objectives, and the recurring failure is reading only the last one, correcting flaws within a defined timeframe, while skipping the two objectives that require a defined and demonstrated timeframe for identifying flaws and a defined and demonstrated timeframe for reporting them. An organization can scan regularly and patch quickly and still fail this requirement if it never wrote down, and never evidenced, that it identifies and reports on a schedule. See `evidence-package-builder` for the single-admin fix to the reporting gap.

3. **3.11.2, vulnerability scanning.** Commonly failed at assessment, with a failure pattern connected to scope. Scanning only the assets that hold CUI, or only the systems that are convenient to reach (the office network, not the laptops that travel), leaves the rest of the network boundary unchecked, and the requirement is read by most assessors as boundary-to-boundary, not asset-category-limited. A second failure pattern is substituting patching evidence for scanning evidence: patch records answer 3.14.1, not 3.11.2, and both are separately required. A third is having no evidence of scanning specifically in response to a named, newly disclosed vulnerability, which the requirement calls for as a distinct trigger from the periodic schedule.

4. **3.3.3, review and update logged events.** Commonly failed at assessment. The requirement is not "do you have logs," it is "do you have a defined process for reviewing whether the logs you have are the right ones, and do you update what you log based on that review." Two failures recur: claiming a cloud platform is not applicable because the organization cannot change what the platform logs, and having logging turned on with no defined review process behind it. Neither survives contact with an assessor; the fix in both cases is the same, a documented periodic review, even one that concludes no change is needed, with the review event itself recorded.

5. **3.3.4, alert on audit logging failure.** Commonly failed at assessment. The requirement has three parts, who gets alerted, what failure types trigger the alert, and that the alert actually fires and reaches that person, and having a working alert without the other two documented parts is treated as incomplete. The other recurring gap is passive monitoring: manually checking whether logs came in, instead of an automated notification, does not meet the requirement, because nothing is generated and sent to a responsible person.

6. **3.3.5, correlate audit record review, analysis, and reporting.** Commonly failed at assessment. This one has two legitimate readings, correlating the human processes of review, analysis, and reporting so that suspicious log activity actually triggers an investigation, and correlating the log data itself through a centralized tool. Covering only one reading is a gap; covering both is the safer position. The clearest red flag practitioners point to is a paid third-party monitoring service with a long track record of zero reported incidents, which suggests the review, analysis, and reporting processes are not actually connected to each other, only that logs exist somewhere.

7. **3.6.3, test the incident response capability.** Commonly failed at assessment. The single most common failure is treating a real security incident as a substitute for a planned test, and it is not; a genuine incident can supplement a testing program, but it does not by itself satisfy the requirement. The second is having a written incident response policy that has never been exercised. Run the tabletop scaffold below to fix both.

### The 3.6.3 tabletop scaffold

Run this as a facilitated exercise, not a document review. No specialized personnel are required; the people who would respond to a real incident should run the drill.

1. Write a realistic scenario specific to this organization's environment (a phished credential reaching a CUI file share, a ransomware note on a shop-floor server, a lost unencrypted laptop).
2. Walk the scenario out loud, in order: how is it discovered, how is it documented, who is notified first, how is it contained.
3. As each policy or procedure becomes relevant to the scenario, stop and actually fill out the real incident response form, not a description of what the form would say.
4. Test the ability to reach outside help named in the plan: a retained incident response firm, cyber insurance, the DoD's incident reporting channel, and any customer notification obligation.
5. Check whether the logs the organization actually has would have caught the scenario's activity. If they would not, that is a finding for `top-failed-requirements-drill` item 3 or 4 above, not just this exercise.
6. Capture lessons learned as concrete change requests, not a vague "went well" summary.
7. File the exercise notes, the completed forms, and the change requests as the evidence artifact for this objective.

Run this at least once before the assessment; a quarterly cadence is stronger than an annual one, but no specific frequency is written into the requirement itself, so document whatever cadence the organization commits to and hold it to that.

## Output

Write the drill to `evidence/top-failed-drill.md`. The tabletop exercise it scaffolds produces its own artifact at `evidence/3.6.3/tabletop-<date>.md`, which is the evidence for that requirement and the reason the exercise is worth running rather than just planning.

```markdown
# Top failed requirements drill

| Requirement | Why it fails | SSP claim matches reality? | Fix needed |
|---|---|---|---|
| 3.5.3 | Scope or enforcement misread | | |
| 3.14.1 | Objectives [a]-[e] skipped, only [f] read | | |
| 3.11.2 | Scanning scope too narrow, or scanning conflated with patching | | |
| 3.3.3 | No defined review process | | |
| 3.3.4 | Missing one of the three required parts | | |
| 3.3.5 | Only one of the two readings covered | | |
| 3.6.3 | Real incident treated as a test, or plan never exercised | | |

## 3.6.3 tabletop exercise record
Scenario: ...
Date run: ...
Forms completed: ...
External contacts tested: ...
Log coverage confirmed: yes/no, gap: ...
Lessons learned / change requests: ...
```

File the table at `evidence/top-failed-drill.md` and the tabletop record at `evidence/3.6.3/tabletop-<date>.md`.

## Where practitioners disagree

- **Whether a hardware-backed local sign-in visibly presents as two factors.** One position: a trusted platform module combined with a PIN meets the technical definition of two distinct factors under federal authentication guidance. The other position: even if the technical argument holds, an assessor asking to see the multifactor process in action may not perceive two separate factors during the demonstration, and the burden of explaining the mechanism falls on the organization in the moment. The outcome depends on the assessor.
- **Whether a genuine security incident, well documented, can stand in for a planned incident response test.** One position: nothing in the requirement's discussion explicitly demands a tabletop exercise by name, and a real incident handled with the same rigor as a planned exercise, including a documented after-action review, can reasonably satisfy the intent. The other position: the requirement's own discussion names specific test types, checklists, walk-throughs, tabletop exercises, and simulations, and a real incident should supplement that testing program rather than replace it entirely. The safer posture is to run deliberate tests regardless of what real incidents occur. The outcome depends on the assessor.

## Sources

- CMMC Level 2 Assessment Guide, DoD CIO, IA.L2-3.5.3, SI.L2-3.14.1, RA.L2-3.11.2, AU.L2-3.3.3, AU.L2-3.3.4, AU.L2-3.3.5, IR.L2-3.6.3: https://dodcio.defense.gov/CMMC/Resources-Documentation/.
- CISA Tabletop Exercise Packages: https://www.cisa.gov/cisa-tabletop-exercise-packages.
- NDISAC DIB SCC incident response exercises: https://ndisac.org/dibscc/implementation-and-assessment/incident-response-and-management/exercises/.
- Washington State cybersecurity tabletop exercises: https://cybersecurity.wa.gov/tabletop-exercises.
- Public panel of assessors describing what they see in the field: https://www.youtube.com/watch?v=Oxf-d6yoLsc
- Public talk on what to expect at a Level 2 assessment, drawing on roughly a hundred of them: https://www.youtube.com/watch?v=39YxwH0BZX4
- Practitioner consensus, unattributed, backs every "why it fails" reason above and the recommendation to cover both readings of 3.3.5. No public source states a numeric ranking of these seven requirements against each other, so this skill deliberately omits one.
