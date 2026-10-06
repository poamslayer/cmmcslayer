---
name: audit
description: Assess one requirement against the current state of the engagement repo and report every NIST SP 800-171A objective as MET or NOT MET with its letter and the missing evidence. Use when the operator asks whether a requirement is met, when remediate needs to know whether a ticket can close, and after every fix.
---

# Audit

The test loop. `remediate` calls it, and the operator calls it directly. For one requirement it reads what the engagement actually has and reports each assessment objective MET or NOT MET, naming the letter and the evidence gap. It does not fix anything, it does not write SSP text, and it does not decide POA&M eligibility.

**This is never deterministic.** There is no script that decides whether an objective is satisfied, because the question is whether a human assessor would accept what is in the repo, and that is a judgment made against what assessors have actually accepted. A pass that greps for file names tells you nothing.

## The unit is the objective, not the requirement

A requirement is MET only when every applicable objective is MET (32 CFR 170.24(b)(1)). One unsatisfied objective makes the whole requirement NOT MET, with no partial credit, and the two adjustable requirements (3.5.3 and 3.13.11) are the only exceptions, and they adjust the score, not the finding. So the report is per objective. "3.1.1 is weak" is not an audit result. "3.1.1[a] NOT MET, no authorization record exists outside the identity provider" is.

## Run it in a subagent

Dispatch a fresh subagent per requirement. It gets a clean window, it does not inherit whatever the operator was arguing about a moment ago, and several requirements can be audited at once. The parent session keeps only the returned report.

Before dispatching, read the SSP from the record, `ssp/ssp.json`: call the Skill tool with `scribe` and ask it to show the record for the requirement. What comes back is the record as it stands now: the components, the assets and their categories, the providers with their roles and remarks, and every statement on each of the requirement's objectives, with its component and status. Never read `view/` instead; the view is generated for people and can be stale, and the record is the SSP.

The subagent gets, and only gets:

- The requirement id.
- `skills/domain/gap/control-evidence-lookup/controls/<id>.md`, the bar.
- Scribe's showing of the record for the requirement, as it came back.
- The engagement's `evidence/<id>/`, `scope/data-flow.md`, `scope/network-diagram.md`, `scope/network-diagram.drawio`, and `scope/open-items.md` where they exist, `CONTEXT.md`, and **every file in `policies/`**, not only the ones the SSP names. A contradiction between a statement and a policy the statement never mentions is exactly the kind an assessor finds, so the policy set has to be in view.
- Any first-hand description of the environment as it actually runs: a site walk, an interview note, a configuration export. **Where this disagrees with the engagement's own scope files, the environment wins and the disagreement is itself a finding**, recorded in Notes. An engagement's inventory is an assertion, and auditing only against the assertion is how a scope error survives all the way to the assessment.
- The instruction below.

Nothing else. A subagent that reads the whole engagement repo starts grading the engagement instead of the requirement.

## Method

1. **Read the control file first, then the engagement.** In that order. Reading the engagement first anchors you to what is there and turns the audit into a search for reasons to pass.

2. **Note the confidence.** A control file marked `confidence: low` cannot carry a confident NOT MET on a judgment call. Report what the Assessment Guide objective plainly requires, and say the bar beyond that is not well established.

3. **Take each objective in letter order.** For each one:
   - State what the objective asks for, in the objective's own terms.
   - Find what the engagement offers: every statement the record holds on that objective, one per component, with its status; the artifacts in the evidence folder; the scope files; the named policy. An objective planned on "This System" with "Not yet written." has no statement at all. A status is the SSP's claim about itself, never evidence that the claim is true.
   - Compare it against the control file's **Sufficient** and **Insufficient** bullets carrying that letter. An engagement answer that matches an Insufficient bullet is NOT MET even when something exists, and that is the most common real finding: evidence is present and it is the wrong evidence.
   - Decide MET, NOT MET, or N/A.

4. **MET needs evidence in final form.** Working papers, drafts, and unapproved policies are not evidence (32 CFR 170.24(b)(1)). An SSP statement on its own is a claim, not evidence; it is MET only when the objective asks for something documented and the document is the evidence. A statement with no artifact behind it, where the objective asks for a practice, is NOT MET.

5. **N/A is a human judgment and is reported separately.** Mark an objective N/A only when the requirement genuinely cannot apply to this scope, and say why in one sentence. Never use N/A to avoid a hard call. An N/A objective counts as MET for scoring but carries a justification a tool cannot validate, so it is surfaced on its own line for a person to confirm.

6. **Name the gap, not the fix.** A NOT MET line says what is missing, in terms of the objective. Suggesting the remedy is `remediate`'s job, and an auditor who designs the fix has stopped auditing it.

7. **Call the over-engineering guard when a fix is on the table.** If the operator or `remediate` proposes a control that goes past what the control file's Sufficient bullets describe, call the Skill tool with `over-engineering-guard` before endorsing it. The loop exists to close objectives, not to spend money.

8. **Contested objectives get both readings.** Where the control file's Edge cases say the outcome depends on the assessor, report the objective as **CONTESTED** with both positions and what the engagement would need for each. Do not silently pick the lenient reading.

   **CONTESTED needs a real dispute, not just an edge case in the file.** The test is whether the engagement has actually done something that a lenient assessor would accept and a strict one would not. An edge case that describes an arrangement this engagement does not have leaves nothing to contest, and the objective is simply NOT MET. Marking every objective whose control file mentions a disagreement as CONTESTED turns the report into mush and hides the gaps that are not in doubt.

## Output

Write the report to `.scratch/audit/<id>-<date>.md` in the engagement repo, in exactly this shape. `to-poam` reads it, so the headings and the table are fixed.

```markdown
# Audit: <id> <title>

Date: <YYYY-MM-DD>. Points: <n>. POA&M eligible: <yes|no>. Control file confidence: <high|medium|low>.

## Finding

<MET | NOT MET>

## Objectives

| Objective | Finding | Evidence seen | Gap |
|---|---|---|---|
| [a] | MET | <artifact or SSP statement> | |
| [b] | NOT MET | <what exists, or "nothing"> | <what the objective asks for that is absent> |
| [c] | N/A | | <why it cannot apply, one sentence> |
| [d] | CONTESTED | <what exists> | <both readings, and what each needs> |

## Notes

<anything the next reader needs: a policy that contradicts the SSP, an artifact that is a draft, an objective that depends on an ESP whose signed responsibility matrix is not in evidence, a problem scribe reported in the record>
```

**The two adjustable requirements need their state named, not just a number.** 3.5.3 and 3.13.11 carry `points: "3 or 5"` because the deduction depends on how far the implementation got. Write the Points field as the value the current state earns, with the state in brackets: `Points: 3 (multifactor authentication for remote and privileged access only)` or `Points: 5 (not implemented)` for 3.5.3; `Points: 3 (encryption employed, not FIPS validated)` or `Points: 5 (encryption not employed)` for 3.13.11. That distinction decides whether 3.13.11 can go on a POA&M at all, so an audit that leaves it as a range hands the next skill a question it cannot answer. The rule is in `reference/32-cfr-170-24-scoring.md` (also public at https://www.ecfr.gov/current/title-32/section-170.24).

A requirement is MET only if every row is MET or N/A. One NOT MET row makes the Finding NOT MET. A CONTESTED row makes the Finding NOT MET until the engagement records which reading it is building to, because an assessor may take either.

## The loop

`remediate` drives it:

1. Audit the requirement. Every objective MET means the ticket closes.
2. Any NOT MET means fix the named gap.
3. Audit again, from a fresh subagent that has not seen the fix being argued for.
4. Repeat until every objective is MET.

The loop closes on its own because the exit condition is the objective table, not anyone's opinion that the work looks done. Do not close a ticket on an audit older than the fix it is meant to verify.

## Seat notes

**OSC seat**: the report is written for the person who has to produce the missing thing, so a gap reads as what is absent rather than as a citation. Keep the objective letters; they are what the assessor will ask about.

**Consultant seat**: the report is the working paper behind the gap assessment, and the CONTESTED rows are the pre-engagement questions for the C3PAO.

## Sources

- 32 CFR 170.24, assessment findings and the evidence finality rule: `reference/32-cfr-170-24-scoring.md` (also public at https://www.ecfr.gov/current/title-32/section-170.24)
- NIST SP 800-171A, the assessment objectives: https://csrc.nist.gov/pubs/sp/800/171/a/final
- CMMC Level 2 Assessment Guide, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/
- The bar per requirement: `skills/domain/gap/control-evidence-lookup/controls/`

Rewritten from `tdd` in mattpocock/skills (MIT, see `skills/flows/LICENSE-mattpocock`). The red-green loop, the one-slice-at-a-time rule, and the refusal to theorise ahead of a failing check are its shape; the seam is an assessment objective and the test is an assessor's judgment.
