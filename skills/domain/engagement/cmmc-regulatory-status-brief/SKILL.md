---
name: cmmc-regulatory-status-brief
description: State what CMMC and NIST SP 800-171 obligations are actually in force today, with an as-of date, so nobody advises a client from a stale picture. Use when a client asks whether CMMC is still happening, which revision applies, or whether to pause an assessment.
as_of: "2026-09-13"
vault_sources:
  - "CMMC Phase II Suspension (July 2026)"
  - "Rev 2 vs Rev 3 Double Baseline"
  - "CMMC Phased Rollout"
  - "CMMC 48 CFR Final Rule"
  - "CMMC Class Deviation"
  - "DFARS 252.204-7021"
  - "Printer Scoping"
  - "raw/practitioner-community-export-2026-09-03.md"
public_sources:
  - "Department of War, suspension of CMMC Phase II requirements, 2026-07-13: https://business.defense.gov/Engage/News/Article/4542563/forging-the-arsenal-of-freedom-department-of-war-suspends-cmmc-phase-ii-require/"
  - "Crowell and Moring client alert on the suspension and the 60-day reform review: https://www.crowell.com/en/insights/client-alerts/department-of-war-immediately-suspends-cmmc-phase-ii-requirements-launches-60-day-reform-review"
  - "Holland and Knight alert: https://www.hklaw.com/en/insights/publications/2026/07/dow-suspends-cmmc-phase-ii-requirements"
  - "Federal News Network coverage: https://federalnewsnetwork.com/cybersecurity/2026/07/pentagon-suspends-cmmc-phase-two-requirements-launches-review-of-program/"
  - "ClearanceJobs on the task force tradeoffs: https://news.clearancejobs.com/2026/08/17/will-cmmc-keep-third-party-audits-pentagon-task-force-weighs-the-tradeoffs/"
  - "32 CFR Part 170: https://www.ecfr.gov/current/title-32/part-170"
  - "DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012"
---

# CMMC regulatory status brief

What is actually in force today, said plainly, with a date on it. Read this before telling any client to speed up, slow down, or sit still.

**This skill goes stale faster than anything else in the repo.** The `as_of` date in its frontmatter is read by `setup-poamslayer-skills`, which warns when it is more than 60 days old. Treat that warning as a hard stop: re-verify against the primary sources below before advising anyone, and update the date and the content together.

## Inputs

- The question, which is usually one of three: is CMMC still happening, which revision of the standard applies to us, or should we pause an assessment we have already booked.
- **Which agencies the client actually holds contracts with.** This is the input that changes the answer and the one nobody volunteers. A supplier working only for the Department of War and a contractor with civilian federal work are in different situations.
- Whether an assessment is booked, and when. The cost of waiting is the assessor backlog, not the regulation.
- The `as_of` date in this skill's own frontmatter. If it is more than 60 days old, refresh before answering. `setup-poamslayer-skills` warns about this at scaffold time; heed it here too.

## Method

1. **Check the date on this file before you open your mouth.** A stale brief delivered confidently is worse than saying you will check, because the client acts on it.
2. **Separate what is in force from what is open.** Those are the two lists below and they are the whole answer. Give the first as fact and the second as an open question with a clock on it.
3. **Ask which agencies they contract with**, then answer the revision question. Do not answer it generically; the double baseline is the part that bites, and it bites only some clients.
4. **Label every forecast as speculation, out loud.** The task force outcome is unknown. Say that in those words rather than hedging your way through a guess that sounds like knowledge.
5. **Answer the pause question on their contracts and their booked slot**, not on a general rule. Practitioners disagree about it and the disagreement is real; see below.
6. **Say what has not changed.** Most clients hear "suspended" and stop everything. The obligations that continue are the part they most need and least expect.

## Output

A short spoken or written brief, carrying four things in this order:

```markdown
## CMMC status, as of <the as_of date on this skill>

**In force today**: <the obligations that have not changed>

**Suspended or open**: <what has stopped, and what is undecided with its clock>

**What this means for you**: <answered against the agencies this client actually contracts with>

**What we do not know**: <labelled as speculation, with the date a decision is expected>
```

Nothing is written to the engagement repo. This skill briefs; it does not decide. Where the answer changes an engagement decision, that decision belongs in an ADR written by the skill that owns it.

## As of 2026-09-13

### Suspended

**CMMC Phase II is suspended.** Two Department of War memoranda on 2026-07-13 suspended it immediately. Phase II was scheduled for 2026-11-10 and would have brought third-party assessment requirements into contracts: C3PAO assessment at Level 2, government-led assessment at Level 3. Solicitations and contracts that already carried those requirements are to be amended to remove them. The stated rationale was compliance cost and burden on small and mid-size contractors.

**It is a suspension, not a repeal.** 32 CFR Part 170 has not been rescinded. The rule, the assessment methodology, the scoring table, and the POA&M conditions all still exist as written.

### Still in force, and this is the part clients get wrong

- **Phase I.** Self-assessment at Levels 1 and 2, posting the resulting score to SPRS, and affirming annually.
- **DFARS 252.204-7012** in full, including the safeguarding obligation and the incident reporting clock.
- **NIST SP 800-171 Rev 2** as the baseline those obligations point at.

Nothing about the July suspension reduces what a contractor holding CUI has to do. It changed who checks.

### Open, with a clock

A **CMMC Reform Task Force** ran a 60-day review with a request for information. Comments closed 2026-08-14. Recommendations were expected to the Department of War CIO around mid-September 2026, and the earliest realistic formal announcement is mid-October 2026, with slippage into late 2026 or 2027 entirely possible. The instrument could be a class deviation, a DFARS rule change, or an amendment to 32 CFR Part 170.

**Anything past this point is speculation and must be labelled as such when you say it out loud.** Practitioner consensus expects a further delay rather than a reinstatement or a cancellation, and expects the assessment requirement to return in some modified form rather than vanish. Nobody knows. Say that.

## The Rev 2 and Rev 3 double baseline

This is the substantive problem the suspension reopened, and it matters more to most clients than the assessment question does.

- **DFARS 252.204-7012 is pinned to Rev 2** by class deviation.
- **Rev 3 is what the proposed FAR CUI rule names.** That rule reaches every federal agency, not the Department of War alone, and it phases in nothing.

Two exits, both uncomfortable:

| Move | Consequence |
|---|---|
| Drop the class deviation | Rev 3 applies to new Department of War contracts immediately, with no transition period |
| Keep the class deviation | A contractor holding both Department of War and civilian federal contracts maintains two baselines at once |

A transition plan for moving from Rev 2 to Rev 3 had been written into the unpublished CMMC 3.0 rule. Shelving Phase II shelved that plan too, along with the assessment requirement, which is why the move is an open question today instead of a scheduled one.

**Advise on this before you advise on assessments.** Ask which agencies the client actually holds contracts with. A pure Department of War supplier and a contractor with civilian agency work are in different situations, and the second one cannot safely assume Rev 2 is the end of the story.

Some Rev 3 deltas already bite in design decisions being made today. The clearest is the loss of the alternative physical safeguards path in 3.13.8, which is what turns networked printing and on-site CUI handling into a spending decision now rather than later.

## What to tell a client

1. **Do not say CMMC is dead.** Self-assessment, SPRS posting, affirmation, 7012, and 800-171 all continue. A client who stands down entirely is accruing risk against obligations that never paused.
2. **Do not say Rev 3 is off the table.** It rides on a separate track, one the Department of War has no power to stop.
3. **Ask which agencies they contract with** before telling them to sit still.
4. **Explain why a certificate still has value.** Primes have consistently run ahead of Department of War deadlines and still have to verify their subcontractors. A certificate is stronger supplier evidence than a self-assessment, and the suspension does not compel any prime to drop an expectation it already set.
5. **Raise the backlog, because it is the real cost of waiting.** Assessor capacity did not grow when demand paused. A client who cancels a booked slot may wait months for the next one, and if requirements return on a deadline, that wait is the exposure.
6. **Label speculation as speculation.** The task force's output is unknown. Say what is in force, say what is open, and keep the two apart.

## How to refresh this skill

When the 60-day warning fires, or whenever something moves:

1. Check the Department of War and Department of War CIO announcements for a task force outcome.
2. Check whether 32 CFR Part 170 has been amended or rescinded on the eCFR.
3. Check whether the class deviation pinning DFARS 252.204-7012 to Rev 2 is still in place.
4. Check the FAR CUI rule's status.
5. Rewrite the "As of" section, update `as_of` in the frontmatter, and note what changed.

Update the date only when you have actually checked. A current date on a stale brief is worse than an old date on an honest one, because the warning that would have caught it no longer fires.

## Where practitioners disagree

Whether a client mid-preparation should pause is contested. One position is that an organization close to ready should finish, because the certificate is the differentiator and the assessor backlog punishes delay. The other is that paying for a third-party assessment nobody currently requires is hard to justify. Both are being argued by people doing this work. The outcome depends on the client's contracts and their appetite for risk, not on a general rule.

## Seat notes

**Consultant seat**: this brief is the first conversation of an engagement and it is where trust is won or lost. A consultant who overstates urgency during a suspension does not get a second engagement.

**OSC seat**: the useful summary is that your self-assessment obligations did not change, the third-party check is paused with an unknown end date, and the revision question depends on who you sell to.

## Sources

Every claim above traces to the public sources in the frontmatter. Practitioner consensus, unattributed, backs the expectation of a further delay and the reading of the double baseline as the more pressing client question; both are labelled as speculation in the text.
