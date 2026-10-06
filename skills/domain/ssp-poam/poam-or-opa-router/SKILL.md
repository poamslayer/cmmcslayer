---
name: poam-or-opa-router
description: Decide whether a deficiency belongs on a POA&M, on an Operational Plan of Action, in the SSP as an enduring exception, or nowhere at all. Use whenever someone reaches for a tracker after finding a gap.
vault_sources:
  - "3.12.2"
  - "POA&M Eligibility"
  - "CMMC Significant Change Determination"
  - "3.11.3"
  - "3.14.1"
  - "raw/CMMC-FAQs-v2.3-May-2026.md"
public_sources:
  - "32 CFR 170.21: https://www.ecfr.gov/current/title-32/section-170.21"
  - "32 CFR 170.24: https://www.ecfr.gov/current/title-32/section-170.24"
  - "CMMC FAQ C-Q9: https://dodcio.defense.gov/CMMC/FAQ/"
---

# POA&M or OPA

The most common confusion in this area, and an expensive one, because the two instruments score differently. A deficiency on the wrong list either costs points it did not need to cost or claims a MET the assessment will not support.

## Route on the M

You set **milestones** when closing the gap is within your control. That single question separates the two.

| | POA&M | Operational Plan of Action |
|---|---|---|
| What triggers it | A requirement assessed NOT MET during an assessment | A temporary deficiency that arose after the system was already compliant |
| Milestones | You set completion dates, because the fix is yours to make | None, because the timeline is not yours |
| How it scores | NOT MET | MET, under 32 CFR 170.24(b)(1)(ii) |
| Deadline | Hard 180 days from the Conditional CMMC Status Date | None |
| Eligibility limits | Three gates, see below | None |

## Inputs

The deficiency, when it was found, whether the system was compliant before it appeared, and whether the fix is in the organization's hands. If any of those four is unknown, find out before routing; a routing decision made on a guess is the failure this skill exists to prevent.

## Method

1. **Was the system compliant in this respect before the deficiency appeared?**
   - No, it was never compliant: this is a POA&M candidate. Go to step 3.
   - Yes, it was compliant and something changed: go to step 2.

2. **Is closing it within the organization's control?**
   - No, and the deficiency is temporary: **OPA**. A vendor has not yet published a validated cryptographic module, a patch does not exist yet, a provider's authorization is in renewal. It scores MET, so it does not cost points, and it carries no 180-day clock because you cannot commit to a date you do not control.
   - No, and the deficiency is permanent: **enduring exception**, described in the SSP with its mitigations, assessed MET under 32 CFR 170.24(b)(1)(i). A machine that cannot run endpoint protection without failing is the standard case. It belongs in the SSP narrative, never on either list.
   - Yes, it is yours to fix: go to step 3.

3. **Is it worth a tracker entry at all?**
   - One workstation missing one setting, found during routine work: fix it. A tracker entry adds nothing.
   - The same thing happening repeatedly: that is a process deficiency, and the process is what goes on the POA&M, because the root cause is the actual gap.

4. **Run the three POA&M gates before writing anything down.** Call the Skill tool with `sprs-score-and-poam-eligibility`. All three must pass at once:
   - The score is at least 0.8 of the maximum, that is 88 of 110, computed across every NOT MET requirement together.
   - The requirement is worth 1 point, with one exception: 3.13.11 at 3 points, where encryption is employed but is not FIPS validated. At 5 points, meaning no encryption, it is not eligible. 3.5.3 is also scored adjustably, but its floor is 3, so it is never eligible.
   - The requirement is not one of the six named in 32 CFR 170.21(a)(2)(iii): 3.1.20, 3.1.22, 3.10.3, 3.10.4, 3.10.5, and 3.12.4.

5. **If a gate blocks it, say which one, and do not re-route it to an OPA to get around the block.** A requirement that was never implemented is not a temporary deficiency, whatever it would be convenient to call it. It is pre-assessment work: it has to be finished before the assessment, not planned around.

## Output

```markdown
## Routing: <requirement id>

**Route**: POA&M | OPA | enduring exception | fix it now | pre-assessment work

**Why**: <the answers to steps 1 and 2 in one or two sentences>

**Gates** (POA&M only): score ratio <n>; point value <n>; named-six check <pass|fail>.

**Scores as**: NOT MET | MET

**Closeout**: <date, for a POA&M only, being the Conditional CMMC Status Date plus 180 days>
```

`to-poam` writes the ticket from this. This skill decides; it does not publish.

## Common cases

| Situation | Route | Why |
|---|---|---|
| Waiting on a vendor's validated cryptographic module | OPA | Was compliant, timeline is the vendor's |
| No endpoint protection on a machine that cannot run it | Enduring exception in the SSP | Permanent, mitigated, not a plan |
| A rogue remote access path found during assessment | POA&M if the gates pass | Never compliant, yours to fix |
| One workstation missing a setting | Fix it | Not a tracker entry |
| Workstations repeatedly drifting off baseline | POA&M on the process | The gap is the process, not the workstation |
| A 5-point requirement never implemented | Pre-assessment work | Point-value gate blocks a POA&M |
| No SSP | Pre-assessment work, urgently | 3.12.4 is one of the named six, and its absence stops the assessment outright |

## Do not track process improvements here

Putting an improvement that is not a deficiency on a POA&M muddies what is actually non-compliant and pulls an assessor into your project schedule. Keep them somewhere else.

## Where practitioners disagree

How much documentation an OPA needs before an assessor accepts it as MET rather than reading it as a POA&M in disguise is not settled. The defensible version shows the deficiency review, the progress toward correction, and the reason the timeline is not yours. The outcome depends on the assessor.

## Sources

- 32 CFR 170.24(b)(1), the MET treatment of enduring exceptions and temporary deficiencies: `reference/32-cfr-170-24-scoring.md` (also public at https://www.ecfr.gov/current/title-32/section-170.24)
- 32 CFR 170.21, the conditions and the closeout: `reference/32-cfr-170-21-poam-gates.md` (also public at https://www.ecfr.gov/current/title-32/section-170.21)
- The eligible list and the arithmetic behind it: `reference/poam-eligible-46.md` (also public at https://www.ecfr.gov/current/title-32/section-170.21)
- CMMC FAQ C-Q9 on change management and the two instruments: https://dodcio.defense.gov/CMMC/FAQ/
