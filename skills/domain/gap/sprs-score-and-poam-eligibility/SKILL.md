---
name: sprs-score-and-poam-eligibility
description: Roll 320 assessment objectives up to a 110-requirement SPRS score, apply the 5/3/1 point table and the two adjustable requirements, and decide which NOT MET requirements can sit on a POA&M under the three Level 2 gates. Use whenever computing a score, building a POA&M, or checking whether a Conditional CMMC Status is achievable.
vault_sources:
  - "POA&M Eligibility"
  - "IntelliGRC Assessment Objective Model"
  - "3.12.2"
  - "3.12.4"
  - "3.13.11"
  - "3.5.3"
  - "CMMC Level 1"
public_sources:
  - "32 CFR 170.24, CMMC Scoring Methodology: https://www.ecfr.gov/current/title-32/section-170.24"
  - "32 CFR 170.21, Plan of Action and Milestones requirements: https://www.ecfr.gov/current/title-32/section-170.21"
  - "CMMC FAQs, Office of the DoD CIO, C-Q7 through C-Q10: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "reference/32-cfr-170-24-scoring.md"
  - "reference/32-cfr-170-21-poam-gates.md"
  - "reference/poam-eligible-46.md"
  - "reference/nist-800-171r2-requirements.json"
---

# SPRS score and POA&M eligibility

This skill computes a Level 2 SPRS score from a set of assessed objectives, and for every NOT MET requirement decides whether it can sit on a Plan of Action and Milestones (POA&M) toward a Conditional CMMC Status. It refuses to decide whether a specific piece of evidence is sufficient for a given objective (that is `control-evidence-lookup`) and it refuses to treat a POA&M item as if the requirement were MET, because it is not.

## Inputs

- Per-objective assessment results for all 320 Level 2 objectives, each marked Implemented, Not Implemented, Partially Implemented, or Not Applicable. If results only exist at the 110-requirement level, that is acceptable but coarser.
- The Conditional CMMC Status Date, if a POA&M has already been opened, to compute the 180-day closeout deadline.
- `reference/nist-800-171r2-requirements.json` for the authoritative id, family, and point value of every requirement (also public at https://csrc.nist.gov/pubs/sp/800/171/a/final).

## Method

1. **Roll 320 objectives up to 110 requirements.** Look at every objective under a requirement together: as soon as a single one comes back Not Implemented or only Partially Implemented, the whole requirement is NOT MET. There is no partial credit at the requirement level, with the two adjustable requirements in step 3 as the only exceptions. Pull Not Applicable objectives out of the NOT MET count, but do not silently drop them: surface each one on a separate line with the justification a human wrote, because no automated check can validate an N/A determination.

2. **Score every NOT MET requirement using the point table.** 32 CFR 170.24(c)(2) sets three point values, tied to how much damage an unimplemented requirement could do, not to how hard it is to implement.

   **5-point requirements** (42 total): significant exploitation or CUI exfiltration is possible if not implemented.

   | Family | Requirements |
   |---|---|
   | AC | 3.1.1, 3.1.2, 3.1.12, 3.1.13, 3.1.16, 3.1.17, 3.1.18 |
   | AT | 3.2.1, 3.2.2 |
   | AU | 3.3.1, 3.3.5 |
   | CA | 3.12.1, 3.12.3 |
   | CM | 3.4.1, 3.4.2, 3.4.5, 3.4.6, 3.4.7, 3.4.8 |
   | IA | 3.5.1, 3.5.2, 3.5.10 |
   | IR | 3.6.1, 3.6.2 |
   | MA | 3.7.2, 3.7.5 |
   | MP | 3.8.3, 3.8.7 |
   | PE | 3.10.1, 3.10.2 |
   | PS | 3.9.2 |
   | RA | 3.11.2 |
   | SC | 3.13.1, 3.13.2, 3.13.5, 3.13.6, 3.13.15 |
   | SI | 3.14.1, 3.14.2, 3.14.3, 3.14.4, 3.14.6 |

   **3-point requirements** (14 total): a specific, confined effect on the network or its data if not implemented.

   | Family | Requirements |
   |---|---|
   | AC | 3.1.5, 3.1.19 |
   | AU | 3.3.2 |
   | CA | 3.12.2 |
   | MA | 3.7.1, 3.7.4 |
   | MP | 3.8.1, 3.8.2, 3.8.8 |
   | PS | 3.9.1 |
   | RA | 3.11.1 |
   | SC | 3.13.8 |
   | SI | 3.14.5, 3.14.7 |

   **1-point requirements** (52 total, everything not listed above and not one of the two adjustable requirements below): a limited or indirect effect on the network or its data.

   Full ids for all three tiers are in `reference/32-cfr-170-24-scoring.md` and `reference/nist-800-171r2-requirements.json`; cite those rather than retyping the lists (also public at https://www.ecfr.gov/current/title-32/section-170.24, https://csrc.nist.gov/pubs/sp/800/171/a/final).

3. **Apply the two adjustable requirements.** Two requirements score on a sliding scale instead of a fixed value:

   | Requirement | Full implementation | Partial state | Unimplemented |
   |---|---|---|---|
   | IA.L2-3.5.3, Multifactor Authentication | MET, 0 points | MFA for remote and privileged users only: 3 points | No MFA implemented anywhere: 5 points |
   | SC.L2-3.13.11, CUI Encryption | MET, 0 points | Some encryption is in place, just not a validated module: 3 points | No encryption at all protecting CUI's confidentiality: 5 points |

4. **Sum the score.** Start at 110 (the maximum) and subtract the point value of every NOT MET requirement. The result can go negative if enough high-value requirements are NOT MET; there is no floor at zero.

5. **Check Gate 1: the 0.8 score ratio.** Divide the score by 110. A Conditional Level 2 status of either kind requires a ratio of at least 0.8, which is a score of 88 or higher. Below 88, no POA&M path exists regardless of which specific requirements are NOT MET; the organization must close enough gaps outright to clear the floor first.

6. **Check Gate 2: the point-value ceiling.** Nothing scored above 1 point may sit on a POA&M, with a single named exception: SC.L2-3.13.11 may go on a POA&M only in its 3-point state, where encryption is employed but not FIPS-validated. If 3.13.11 is at 5 points (no encryption at all), it cannot go on a POA&M. IA.L2-3.5.3 has no such exception; at either 3 or 5 points it can never be POA&M'd.

7. **Check Gate 3: the six prohibited requirements.** None of the following may appear on a Level 2 POA&M under any circumstance, regardless of score or point value:

   | Requirement | Name |
   |---|---|
   | AC.L2-3.1.20 | External Connections |
   | AC.L2-3.1.22 | Control Public Information |
   | CA.L2-3.12.4 | System Security Plan |
   | PE.L2-3.10.3 | Escort Visitors |
   | PE.L2-3.10.4 | Physical Access Logs |
   | PE.L2-3.10.5 | Manage Physical Access |

   All six are 1-point requirements; they are named individually because the point-value gate alone would otherwise have let them through. CA.L2-3.12.4 also does a second job on top of being barred from the POA&M: show up to an assessment without a current System Security Plan and the assessment cannot be scored at all, regardless of anything else.

8. **Verify the eligible-46 arithmetic before trusting the list.** Forty-two five-point requirements, plus fourteen three-point requirements, plus the two adjustable requirements, plus fifty-two one-point requirements sums to 110, matching the total requirement count exactly, which confirms every requirement has exactly one point-value assignment. Of the 52 one-point requirements, 6 are barred by Gate 3, leaving 46 eligible. Recompute this arithmetic against `reference/nist-800-171r2-requirements.json` whenever the requirement set changes rather than trusting a cached count (also public at https://csrc.nist.gov/pubs/sp/800/171/a/final).

   The 46 eligible 1-point requirements, by family:

   | Family | Requirements |
   |---|---|
   | AC | 3.1.3, 3.1.4, 3.1.6, 3.1.7, 3.1.8, 3.1.9, 3.1.10, 3.1.11, 3.1.14, 3.1.15, 3.1.21 |
   | AT | 3.2.3 |
   | AU | 3.3.3, 3.3.4, 3.3.6, 3.3.7, 3.3.8, 3.3.9 |
   | CM | 3.4.3, 3.4.4, 3.4.9 |
   | IA | 3.5.4, 3.5.5, 3.5.6, 3.5.7, 3.5.8, 3.5.9, 3.5.11 |
   | IR | 3.6.3 |
   | MA | 3.7.3, 3.7.6 |
   | MP | 3.8.4, 3.8.5, 3.8.6, 3.8.9 |
   | PE | 3.10.6 |
   | RA | 3.11.3 |
   | SC | 3.13.3, 3.13.4, 3.13.7, 3.13.9, 3.13.10, 3.13.12, 3.13.13, 3.13.14, 3.13.16 |

   Plus SC.L2-3.13.11 in its 3-point state only, as the sole requirement above 1 point ever permitted on a POA&M.

9. **Never let a POA&M item read as MET.** A requirement with an open POA&M item is scored NOT MET until the closeout assessment confirms it is fixed. A POA&M is a plan to close a gap, not a substitute for closing it. This differs from how DFARS 252.204-7012 treats an outstanding item, where a documented plan can support a finding of adequate security; CMMC scoring does not extend that same tolerance, and the gap continues to count against the score until it is actually resolved.

10. **Distinguish a POA&M from an Operational Plan of Action (OPA).** A POA&M addresses a requirement assessed NOT MET during the assessment, with milestones the organization controls, and it is subject to every gate above. An OPA addresses a temporary deficiency that arose after the system was already compliant, has no fixed timeline, and is assessed MET rather than NOT MET. Putting a genuinely NOT MET requirement on an OPA instead of a POA&M to dodge the gates is not a legitimate move; the two instruments answer different questions and only one of them is scored as a gap.

11. **Compute the 180-day closeout date.** Add 180 days to the Conditional CMMC Status Date. A closeout assessment must confirm every POA&M'd requirement is now MET before that date. Two distinct ways to miss it: the closeout assessment gets finalized in the CMMC system of record while one or more requirements are still NOT MET, which terminates the Conditional Status immediately and can only happen once before the organization has to start over with a brand-new assessment; or the closeout assessment simply is not finalized in time, in which case the Conditional Status expires automatically on day 181.

12. **Budget the score before building the POA&M, not after.** At the 0.8 floor, the maximum tolerable shortfall from a perfect 110 is 22 points. Since every eligible POA&M item is worth exactly 1 point except the single 3-point 3.13.11 case, a realistic POA&M tops out around 22 one-point requirements, or fewer if any 3-, 5-, or adjustable-point requirements were NOT MET and had to be closed outright before the assessment (since those cannot sit on the POA&M at all). Plan remediation against this budget from the start rather than discovering the ceiling after the assessment.

## Output

Write a score worksheet, one row per NOT MET requirement, to `scope/sprs-score-worksheet.md`.

```markdown
# SPRS score worksheet

Assessed: YYYY-MM-DD
Objectives source: <where the 320 per-objective results came from>

| Requirement | Points | Reason NOT MET | Running score | POA&M eligible? | Gate that blocks it |
|---|---|---|---|---|---|
| 3.5.9 | 1 | ... | 109 | yes | none |
| 3.1.1 | 5 | ... | 104 | no | Gate 2, point value |
| 3.12.4 | 1 | ... | 103 | no | Gate 3, named exclusion |

Final score: <sum> / 110
Score ratio: <score / 110>
Gate 1 (ratio >= 0.8, i.e. score >= 88): PASS / FAIL

**Conditional status reachable: YES / NO**
<When NO, list the requirements that block it and why. These are the ones that must be MET before the assessment, not after.>

Conditional CMMC Status Date: YYYY-MM-DD (if applicable)
POA&M closeout deadline: <status date + 180 days>
Requirements on the POA&M: <list, all Gate-2 and Gate-3 clean>
Points remaining as shortfall while POA&M is open: <count, must stay <= 22 total>
Further 1-point failures the score can still absorb: <22 minus the current shortfall>
```

### Read the two results together, and lead with the second

A passing score ratio does not mean Conditional status is reachable. They are separate questions and the second is the one the operator actually needs.

Gate 1 is about the whole set: is the score at least 88. Gates 2 and 3 are about each requirement: can this particular gap sit on a POA&M at all. A set can clear Gate 1 comfortably and still be nowhere near Conditional status, because every NOT MET requirement that fails Gate 2 or Gate 3 has to be MET by the assessment date. There is no instrument that defers it.

So the worksheet answers **Conditional status reachable** as its own line, before the score. It is YES only when every NOT MET requirement either passes all three gates or has been closed. Otherwise it is NO, and the blocking requirements are named, because those are the real deadline and a report that leads with a comfortable-looking score hides them.

Say it out loud to the operator too. "Your score is 90, which clears the floor, and you cannot be certified conditionally until these four are fixed" is the sentence that changes what they do next. "Your score is 90" on its own reads as good news.

## Where practitioners disagree

- **Whether an organization should self-impose a tighter internal deadline than the regulatory 180 days.** Some practitioners push clients to target closeout well before day 180 to leave room for a failed first attempt at the closeout assessment; others see this as unnecessary caution when the gaps are well understood and the work is already scheduled. The outcome depends on the assessor and on how much slack the organization is comfortable carrying.
- **Whether a Not Applicable determination will be accepted without a supporting mock or documented walk-through.** Some assessors take a written justification at face value; others expect to see the reasoning demonstrated, not just asserted. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: run the score worksheet before the client ever books an assessment, so remediation work targets the requirements that actually move the score and clear the gates, rather than whatever feels most urgent operationally. Flag any 5-point or non-3.13.11-adjustable NOT MET requirement immediately: those cannot be POA&M'd and must be closed before the assessment date, not after it. **OSC seat**: a POA&M buys you 180 days on a limited set of small, 1-point gaps. It does not buy time on anything that could let CUI leak or that the six named requirements cover. Know which bucket each open gap falls into before you assume you have time to fix it.

## Sources

- 32 CFR 170.24, CMMC Scoring Methodology: https://www.ecfr.gov/current/title-32/section-170.24
- 32 CFR 170.21, Plan of Action and Milestones requirements: https://www.ecfr.gov/current/title-32/section-170.21
- CMMC FAQs, Office of the DoD CIO, C-Q7 (requirements barred from POA&M), C-Q8 (closeout failure modes), C-Q9 (POA&M versus OPA): https://dodcio.defense.gov/CMMC/Resources-Documentation/
- `reference/32-cfr-170-24-scoring.md`, `reference/32-cfr-170-21-poam-gates.md`, `reference/poam-eligible-46.md`, `reference/nist-800-171r2-requirements.json` (also public at https://www.ecfr.gov/current/title-32/section-170.24, https://www.ecfr.gov/current/title-32/section-170.21, https://csrc.nist.gov/pubs/sp/800/171/a/final)
