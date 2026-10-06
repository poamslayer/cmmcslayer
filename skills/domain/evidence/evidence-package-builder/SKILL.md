---
name: evidence-package-builder
description: Build the evidence package an assessor will actually check, per assessment objective rather than per requirement, plus the recurring monitoring calendar that keeps that evidence current. Use when preparing for an assessment, or when the operator asks what to show for a requirement.
vault_sources:
  - "3.12.1"
  - "3.12.3"
  - "3.3.3"
  - "3.14.1"
  - "3.8.9"
  - "IntelliGRC Assessment Objective Model"
  - "raw/32-CFR-170.24-CMMC-Scoring-Methodology.md"
public_sources:
  - "32 CFR 170.24(b)(1): https://www.ecfr.gov/current/title-32/section-170.24"
  - "CMMC Level 2 Assessment Guide, DoD CIO, CA.L2-3.12.1, CA.L2-3.12.3, AU.L2-3.3.3, SI.L2-3.14.1, MP.L2-3.8.9: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "reference/continuous-monitoring-cadence.md"
---

# Evidence package builder

This skill answers: what do I hand the assessor, and how do I keep it fresh between assessments? It builds evidence at the unit an assessor actually scores, the assessment objective, and it produces the recurring calendar that turns a one-time evidence pull into something still true a year later. It does not decide whether a requirement is MET; call the Skill tool with `control-evidence-lookup` for the bar and `audit` for the finding. It does not write SSP narrative; call the Skill tool with `ssp-statement-writer` for that.

## Inputs

- The requirement or family you are building evidence for, and the objective letters if you already have them.
- The record, the engagement's `ssp/` folder, for the conformity statements the evidence has to back and the components, assets, and providers behind them, so evidence can be split between what the company produces and what an External Service Provider or Cloud Service Provider produces. Read the files directly: the frontmatter of `ssp/<requirement>.md` lists each objective's statements with their component slug and status, and each `ssp/components/<slug>.md` gives the component's assets and, for a provider, its role and FedRAMP status. An objective whose only entry is `this-system`, planned and "Not yet written.", has no statement for evidence to back yet. Never read `view/` instead; it is generated for people and can be stale.
- Anything already collected in `evidence/`, so the calendar builds on what exists instead of starting over.
- `reference/continuous-monitoring-cadence.md`, the list of 51 recurring monitoring activities this skill schedules against (also public at https://www.totem.tech/).

## Method

1. **Work per objective, not per requirement.** A requirement can carry two to six objectives, and an assessor checks each one on its own. Build one evidence row per objective letter, never one row per requirement number. Call the Skill tool with `control-evidence-lookup` for the accepted-evidence catalogue behind each objective; this skill schedules and packages what that catalogue says is acceptable, it does not decide the bar itself.

2. **Enforce the finality rule before anything else.** Under 32 CFR 170.24(b)(1), an assessment finding of MET requires evidence in final form. A draft, an unapproved policy, or a working paper is not evidence, no matter how complete it looks. Screen every candidate artifact against this before it goes in the package: is it signed, dated, and approved, or is it still in progress?

3. **Build the recurring evidence calendar from the 51-activity cadence.** `reference/continuous-monitoring-cadence.md` lists 51 recurring monitoring activities, each with a control mapping, a frequency (ongoing, weekly, monthly, every 90 days, annually, every two years, every three years, or as required), and a probable owner: the organization itself, an MSP, an MSSP, a CSP, another External Service Provider, or a shared responsibility. Walk that list against the requirements in scope for this engagement and write one calendar row per activity that applies, with the actual owner filled in rather than the template's probable owner. This calendar is what turns "we did this once for the assessment" into evidence an assessor can trust is still true (also public at https://www.totem.tech/).

4. **Pick one of the three artifact patterns that work for a small organization.** Practitioner consensus repeatedly converges on the same three shapes, because they are cheap to produce and easy for an assessor to read:
   - A tracked spreadsheet with a status column, a comments column, a date-of-review column, and a reviewer column.
   - A ticket in whatever system the organization already uses, closed with notes describing what was checked and what was found; the closed ticket with notes is itself the evidence.
   - A screenshot or an exported configuration, paired with the policy or procedure it demonstrates.
   Do not invent a fourth pattern unless the organization already has heavier tooling in place; matching evidence weight to organization size is itself a reviewed decision, not a shortcut.

5. **Solve the single-person IT problem explicitly.** Several requirements, most visibly 3.14.1, ask the organization to identify, report, and correct flaws on a defined timeline. When one person does all three steps, "reporting" has no one to report to. Add a documented reporting step to the process: the same person writes down the list of flaws found before starting remediation, dated and timestamped. That list, reviewed on no one else's schedule but still produced and dated, is the evidence that the organization is reporting on schedule rather than skipping the step because it feels redundant.

6. **Handle inheritance by verifying, not assuming.** When a Cloud Service Provider or another External Service Provider covers part of a requirement, do not write "inherited" and stop. Pull the provider's Customer Responsibility Matrix or Shared Responsibility Matrix, find the specific control it claims to cover, map that provider's control language back to the 800-171 requirement in question, and record what you checked to confirm the mapping actually applies to this environment. The evidence package should show the verification step, not just the claim of inheritance.

7. **Assemble the per-objective table for the requirement in front of you**, using the shape in Output below, and file it under `evidence/<requirement-id>/`.

## Output

Two files land in the engagement repo.

`evidence/continuous-monitoring-calendar.md`, one row per applicable activity from `reference/continuous-monitoring-cadence.md`: (also public at https://www.totem.tech/)

```markdown
# Continuous monitoring calendar

| Activity | Requirement | Frequency | Owner | Last completed | Evidence link |
|---|---|---|---|---|---|
| Security control assessment (annual self-assessment) | 3.12.1 | Annually | OSC | | |
| Information system monitoring | 3.12.3 | Ongoing | OSC | | |
| Review and update logged events | 3.3.3 | Annually | OSC | | |
| Vulnerability scanning | 3.11.2 | Monthly | Shared | | |
| Software flaw identification and correction | 3.14.1 | Monthly | MSP | | |
```

A per-objective evidence table for one requirement, filed at `evidence/<requirement-id>/evidence-table.md`. Example for 3.12.1:

```markdown
# Evidence table: 3.12.1

| Objective | What final-form evidence looks like | Artifact pattern | Status |
|---|---|---|---|
| [a] frequency defined | Written, approved policy stating the review cadence | Policy document, dated and approved | |
| [b] controls assessed at the defined frequency, for effectiveness | A completed review record that answers whether the control is achieving its intent, not only whether the described activity happened | Tracked spreadsheet row, or a closed ticket with notes | |
```

Leave `Status` and the date columns blank until the evidence exists; an empty cell is an open item, never a placeholder claim in the SSP.

## Where practitioners disagree

- **Whether ongoing monitoring has to touch every control, or whether high-priority controls monitored frequently plus one annual full review is enough.** One position: all controls must be hit at some point in the monitoring cycle, because "ongoing" is read as covering the whole set. The other position: watching the higher-risk controls closely, with the annual self-assessment sweeping the rest, still produces a MET finding, since it "mitigates some compliance risk" even if it is not the most complete approach. The outcome depends on the assessor.

## Seat notes

**OSC seat**: build the calendar around whoever is actually available to do the recurring work, not an idealized org chart; if that is one person, step 5's reporting fix is not optional, it is what keeps 3.14.1 out of a finding. **Consultant seat**: when an ESP or CSP is involved, step 6's verification work is the deliverable clients most often skip; do not let "the vendor's CRM says so" stand in for reading that CRM against the specific requirement in front of you.

## Sources

- 32 CFR 170.24(b)(1): https://www.ecfr.gov/current/title-32/section-170.24 (finality rule for MET evidence).
- CMMC Level 2 Assessment Guide, DoD CIO, CA.L2-3.12.1, CA.L2-3.12.3, AU.L2-3.3.3, SI.L2-3.14.1, MP.L2-3.8.9: https://dodcio.defense.gov/CMMC/Resources-Documentation/.
- reference/continuous-monitoring-cadence.md, the 51 recurring monitoring activities, their control mappings, frequencies, and probable owners.
- Practitioner consensus, unattributed, backs the three artifact patterns in step 4, the single-admin reporting fix in step 5, the inheritance-verification approach in step 6, and the disagreement recorded above.
