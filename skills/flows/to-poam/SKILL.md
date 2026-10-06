---
name: to-poam
description: Turn every NOT MET objective from an audit into a ticket on the engagement tracker, routed to a POA&M or an Operational Plan of Action, gated against the three POA&M conditions and the eligible list before anything is written down.
disable-model-invocation: true
---

# To POA&M

Take the audit reports in the engagement's `.scratch/audit/` and publish one ticket per NOT MET requirement, each routed to the right instrument and each carrying what a closeout assessment will ask for.

The tracker and the label vocabulary should have been provided to you. If `docs/agents/issue-tracker.md` is missing, tell the operator to run `/setup-poamslayer-skills`.

## Refuse to write a POA&M you are not allowed to have

This is the whole reason the skill exists. A gap written onto a POA&M that regulation does not permit there is worse than no plan: the engagement budgets against a Conditional status it cannot be granted. Every candidate passes the gates **before** it becomes a ticket.

Call the Skill tool with `sprs-score-and-poam-eligibility` and give it the full NOT MET set, not one requirement at a time. Two of the three gates are properties of the whole set, not of any single gap:

1. **Score ratio.** The score must be at least 0.8 of the maximum, which is 88 of 110. Compute it across every NOT MET requirement together.
2. **Point value.** Nothing above 1 point may sit on a POA&M, with one exception: 3.13.11 at 3 points, when encryption is employed but not FIPS validated. At 5 points, encryption not employed at all, it is not eligible. 3.5.3 is scored adjustably too but its floor is 3, so it is never eligible.
3. **The named six.** 3.1.20, 3.1.22, 3.10.3, 3.10.4, 3.10.5, and 3.12.4 may never sit on a POA&M, though all six are 1-point requirements (32 CFR 170.21(a)(2)(iii)).

A gap that fails any gate still becomes a ticket. It is just not a POA&M ticket: it is work that has to be finished before the assessment, and the ticket says so in those words with the gate that blocked it. Never quietly downgrade it to a POA&M anyway.

## POA&M or OPA

Route on the M. You set **milestones** when the fix is in your control.

| | POA&M | Operational Plan of Action |
|---|---|---|
| Trigger | Assessed NOT MET during an assessment | A temporary deficiency arising after the system was already compliant |
| Milestones | You set the dates, the gap is yours to close | No remediation timeline, the fix is not in your hands |
| Scored | NOT MET | MET, under 32 CFR 170.24(b)(1)(ii) |
| Clock | Hard 180 days from the Conditional CMMC Status Date | None |

A permanent deviation described in the SSP with its mitigations is an **enduring exception**, assessed MET under 32 CFR 170.24(b)(1)(i). It belongs in the SSP, not on either list. Call the Skill tool with `poam-or-opa-router` for any case that is not obvious, and for every case where the operator reached for a tracker by reflex.

Do not put process improvements on a POA&M. It confuses an assessor about what is actually deficient and drags them into your remediation schedule.

## Method

1. **Gather the audits.** Read every report in `.scratch/audit/`. A requirement with no audit report does not become a ticket; audit it first. Check each report's date against the engagement's last changes, and re-audit anything stale. The SSP is the record, the `ssp/` folder: read the requirement files for the set, `ssp/<id>.md`, directly. Scribe commits every change, so `git log -1 --format=%cs -- ssp/<id>.md` gives the date a requirement's statements last changed, and `git log -1 --format=%cs -- ssp/components/` the date the components did; a statement recorded after the audit, or evidence added after it, makes the audit stale. Never read `view/` for this; the view is generated for people and can be stale.
2. **Build the NOT MET set** as a table: requirement, point value, the NOT MET objective letters, the gap per letter. CONTESTED rows count as NOT MET here, and the ticket says which reading the engagement is building to.
3. **Run the gates over the whole set.** Report the score first, because if the ratio is below 0.8 no POA&M is available at all and every gap is pre-assessment work.
4. **Route each gap** to POA&M, OPA, enduring exception, or just-fix-it. An enduring exception lives in the SSP, so check the statements the requirement file holds for that objective: a deviation the record does not describe, with its mitigations, is not an enduring exception yet, and the ticket is to record it through `ssp-statement-writer`.
5. **Show the operator the routing before publishing.** One table: requirement, points, route, and for anything refused a POA&M, the gate that blocked it. Let them correct it. This is the last cheap moment to catch a wrong call.
6. **Publish**, one ticket per requirement, in requirement order.

## Ticket shape

Title: `<id> <short gap>`, for example `3.1.3 no information flow control between the shop and the finisher`.

Labels: `poam` or `opa`, plus `req:<id>`, plus the triage label `ready-for-agent` since these are agent-grabbable by construction.

```markdown
## Requirement

<id> <title>. Points: <n>. Route: POA&M | OPA | enduring exception | pre-assessment fix.

## NOT MET objectives

| Objective | Gap |
|---|---|
| [b] | <what the objective asks for that is absent> |

## Why this route

<the gate result, in one or two sentences. For a refused POA&M, name the gate: "5-point requirement, ineligible under 32 CFR 170.21(a)(2)(ii)".>

## Closeout date

<for a POA&M only: the Conditional CMMC Status Date plus 180 days, written as a date. If that date is not known yet, write "180 days from the Conditional CMMC Status Date, not yet set" and say so rather than inventing one.>

## Done when

`/audit <id>` reports every objective MET.

## Source

Audit report: `.scratch/audit/<id>-<date>.md`
```

The closeout date is on the ticket because the 180 days are hard (32 CFR 170.21(b)) and a closeout that misses them terminates the Conditional status. A closeout finalized with requirements still NOT MET can only happen once, and then the whole assessment starts again.

## What this skill does not do

It does not fix anything, and it does not close anything. `/remediate` takes one ticket to closure, and it only closes on a clean audit. It does not write SSP text either: a NOT MET objective that turns out to be a documentation gap still becomes a ticket, and `/to-ssp` writes the statement.

## Sources

- 32 CFR 170.21, the POA&M conditions and the 180-day closeout: `reference/32-cfr-170-21-poam-gates.md` (also public at https://www.ecfr.gov/current/title-32/section-170.21)
- 32 CFR 170.24, findings, scoring, and the OPA treatment: `reference/32-cfr-170-24-scoring.md` (also public at https://www.ecfr.gov/current/title-32/section-170.24)
- The derived eligible list with the arithmetic: `reference/poam-eligible-46.md` (also public at https://www.ecfr.gov/current/title-32/section-170.21)
- CMMC FAQ C-Q8 and C-Q9: https://dodcio.defense.gov/CMMC/FAQ/

Rewritten from `to-tickets` in mattpocock/skills (MIT, see `skills/flows/LICENSE-mattpocock`). The vertical slice becomes one requirement, the blocking edges become the gate results, and the quiz-before-publishing step is kept because it is the last cheap moment to catch a wrong route.
