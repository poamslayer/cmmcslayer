---
name: remediate
description: Drive one POA&M or OPA ticket to closure. Make the fix, run the audit, and close the ticket only when every assessment objective for that requirement is MET.
disable-model-invocation: true
---

# Remediate

One ticket, start to finish. Take a ticket off the engagement tracker, close the gap it names, and prove it closed by audit.

Work **one ticket per session** and clear context between tickets. Each ticket is self-contained by construction, so the last one's context is disposable, and carrying it forward is how a fix for one requirement quietly gets justified by an argument made about another.

## Method

1. **Fetch the ticket** by the tracker's convention in `docs/agents/issue-tracker.md`. Read the body and every comment. Claim it by assigning it to yourself before doing any work, so a parallel session skips it.

2. **Read the audit report the ticket cites**, in `.scratch/audit/`. That report names the objective letters and the gap per letter. Those letters are the definition of done. If the report predates the engagement's last changes, re-audit before doing anything: fixing against a stale finding is how work gets done twice. When the change that makes the report stale is the fix itself, done before this session, such as a tabletop someone already ran, do not audit twice: record the statement (step 5) and let the fresh re-audit in step 6 serve.

3. **Read the bar before designing the fix.** Call the Skill tool with `control-evidence-lookup` for this requirement. The Sufficient bullets say what has actually been accepted for the objectives you are closing. Build to that. The Insufficient bullets are worth more attention than the Sufficient ones, because the common failure is that evidence exists and is the wrong evidence.

4. **Check the fix against the guard before building it.** If what you are about to propose goes past the Sufficient bullets, call the Skill tool with `over-engineering-guard`. The question it asks is which assessment objective requires this. If nothing does, the cheaper accepted thing closes the objective and the expensive thing is optional. Record it as optional rather than doing it.

5. **Make the change.** Three kinds of work close a gap, and most tickets need more than one:
   - **A technical change.** Something in the environment changes. Where the change needs a human in a vendor portal, call the Skill tool with `wizard` rather than writing instructions into a comment.
   - **A physical action.** Some fixes are not configuration at all: a label on a drive, a stamp on a printed drawing, a shredder by the copier, a lock on a cabinet. There is no tool for these. Record each one on the ticket as a named action with an owner, in the words the person doing it would use, and treat it as not done until someone confirms it happened. A ticket whose only remaining work is physical is still open, and the re-audit will say so.
   - **An artifact.** The objective asks for something that has to exist: a list, a log, a record, a signed acknowledgement. Produce it and put it in `evidence/<id>/`. Evidence must be in final form; a draft is not evidence (32 CFR 170.24(b)(1)).
   - **A statement.** The SSP has to say what the system now does. For each objective you closed, call the Skill tool with `ssp-statement-writer` to write the statement for every component the fix changed, and record it in the requirement's file, `ssp/<id>.md`, by calling the Skill tool with `scribe`, naming each component by its slug: status implemented, the statement saying how the component now meets the objective and naming the evidence. Replace the statement already on that objective and component rather than adding a second one, and clear a statement the fix made wrong. An objective whose fix is only partly done, or waits on a physical action nobody has confirmed, stays partial or planned, and its statement says what is in place now. Remove the objective's lines from `scope/open-items.md` that the fix settled, if the list has any. A policy or plan whose text the fix made wrong, such as a plan that still says it was never tested, is a named action with an owner, recorded like a physical one; it does not hold the ticket open unless the objective itself rests on that document's text. Never write the `ssp/` files yourself or edit anything under `view/`. A fix that is not written down is a fix the assessor cannot score.

6. **Re-audit from a fresh subagent.** Call `/audit` for the requirement. The subagent must not have seen the fix being argued for, which is the point of running it clean: an auditor who watched you build it will grade the intent instead of the artifact. If you cannot start a fresh subagent, do not audit your own fix: leave the ticket `in-progress`, with the statement recorded, and tell the operator to run `/audit` for the requirement in a new session, then close on that report.

7. **Close only on a clean audit.** Every objective MET or N/A. One NOT MET row means back to step 3 on that letter, and the statement you recorded for it goes back to what is true: call the Skill tool with `ssp-statement-writer` again, and have it record the statement partial or planned through `scribe`. Post the audit report as a closing comment so the closeout assessment can see what was checked and when, then close the ticket.

8. **If the ticket cannot be closed**, say so on the ticket and leave it open. A gap that turns out to need a decision goes to `/wayfinder` or the domain skill that owns it. A gap that turns out to be outside the organization's control is probably an OPA rather than a POA&M: call the Skill tool with `poam-or-opa-router` and re-route it rather than leaving it to rot on the wrong list.

## The loop is the point

Fix, audit, repeat, until the objective table is clean. The exit condition is the table, never anyone's sense that the work looks done. This is the one habit that makes the difference between a repo that says it is compliant and an engagement that survives an assessment.

Do not batch. Closing four tickets and auditing once tells you which requirement passed and nothing about which fix did it.

## Watch the clock

A POA&M ticket carries its closeout date. The 180 days run from the Conditional CMMC Status Date and they are hard (32 CFR 170.21(b)). Two ways to lose: the closeout is finalized with requirements still NOT MET, which can happen exactly once before the whole assessment starts over, or it is not finalized in time and the Conditional status expires on its own. When the remaining time will not cover the remaining tickets, say so to the operator now, not at day 170.

## Seat notes

**OSC seat**: most tickets need someone who is not you. Name the person and what you need from them in the ticket, and use `to-questionnaire` when the answer lives in another department.

**Consultant seat**: the closing comment is the deliverable the client keeps. Write it so a different assessor reading it in a year can tell what was done and what proved it.

## Sources

- 32 CFR 170.24, evidence in final form: `reference/32-cfr-170-24-scoring.md` (also public at https://www.ecfr.gov/current/title-32/section-170.24)
- 32 CFR 170.21, the 180-day closeout: `reference/32-cfr-170-21-poam-gates.md` (also public at https://www.ecfr.gov/current/title-32/section-170.21)
- CMMC FAQ C-Q8, the two closeout failure modes: https://dodcio.defense.gov/CMMC/FAQ/
- ADR-0012, the record and its one writer, and ADR-0010, open items outside the record: `docs/adr/0012-markdown-ssp-replaces-oscal.md`, `docs/adr/0010-open-items-stay-outside-the-record.md`

Rewritten from `implement` in mattpocock/skills (MIT, see `skills/flows/LICENSE-mattpocock`). The shape is kept: drive one ticket, lean on the test loop, review before closing. The test loop is `/audit` and the review is `/ssp-lint`.
