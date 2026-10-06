# Cold run: remediate

Date: 2026-09-29. Skill under test: `skills/flows/remediate`, after it began recording the statements it closes through scribe (#103). One run on a fresh copy made by `python3 scripts/cold_run.py`, then seeded (below). The tester got the remediate SKILL.md; the skills it calls on this ticket, `ssp-statement-writer`, `audit`, `control-evidence-lookup` with the 3.6.3 control file only, and `over-engineering-guard`; scribe's folder; ADRs 0007, 0008, and 0010; the scratch engagement; and the fixture company files. That is more than the rubric's usual set, because remediate cannot close a ticket without an audit and a statement. The answer key and the rubric were withheld. A second agent graded the run without seeing any SKILL.md.

## Seed

Committed to the scratch copy as its starting state, never to the fixture:

- `.scratch/poam/3.6.3-ir-test.md`: a POA&M ticket, 3.6.3[a] NOT MET, closeout 2027-03-15.
- `.scratch/audit/3.6.3.md`: the 2026-09-14 audit that produced it.
- `evidence/3.6.3/tabletop-2026-09-28.md`: a signed after-action record of a ransomware tabletop run against the plan, with a completed intake form, a logging check, and change requests CR-01 to CR-03 with owners.

## Prompt

"Work the 3.6.3 ticket in .scratch/poam/. Dana says they ran the tabletop yesterday and Nadia put the after-action record in evidence/3.6.3/. Nobody at Saguaro can be asked today; don't stop to ask me."

## Result

| Check | Score |
|---|---|
| Shape match | 2 |
| Known-answer match | 2 |
| Scrub check | 2 |
| Record validity | 2 |
| Record match | 2 |
| Total | 10 |

Pass. One scribe command, no refusals: `set-statement` replacing 3.6.3[a] on "Incident response plan" with an implemented statement naming the exercise and the evidence file. Its UUID is the one the fixture carried. The grader re-rendered `view/` and found it identical. The run claimed the ticket, re-audited, closed it with the audit table as its closing comment, and routed CR-01 to CR-03 to 3.3.1, 3.6.1, and 3.6.2 rather than treating them as 3.6.3 gaps.

## What the run found, and what changed

**The re-audit was not independent.** The tester could not start a subagent, so it audited its own fix and said so. The skill had no fallback. It now says: if you cannot start a fresh auditor, do not audit your own fix; record the statement, leave the ticket `in-progress`, and tell the operator to run `/audit` in a new session. The key scores a run that closes on its own re-audit, having said so, 1 on check 2, and passes a run that leaves the ticket in progress for that reason.

**A document the fix made wrong.** The plan's Testing section still says it was never exercised. The skill now treats that as a named action with an owner, like a physical one, that does not hold the ticket open unless the objective rests on the document's text.

**No open items list.** Step 5 said to remove settled lines from `scope/open-items.md`; it now says "if the list has any".

## Left as found

- The statement says the plan is tested "at least annually", a period no company document sets; the tabletop record says every six months. Not deducted: the key does not name it.
- Two audits on the same day share `.scratch/audit/<id>-<date>.md`, and the seeded ticket used another name. That is the audit skill's convention, for #104.
- The legacy `ssp/3.6.3.md` still says the plan was never exercised and now contradicts the record. The Markdown SSP is retired in #105.

## Rerun on the revised skill

**10 of 10, pass** (2, 2, 2, 2, 2). One scribe command, no refusals: 3.6.3[a] on "Incident response plan" replaced by an implemented statement, keeping its UUID. The tester again could not start a subagent, and this time did what the revised skill says: it did not audit its own fix, left the ticket `in-progress`, and told the operator to run `/audit` for 3.6.3 in a new session and close on that report. The plan's stale Testing text is a named action that does not hold the ticket open.

What it changed: step 2 asked for a re-audit before any work when the cited report is stale, and here the thing that made it stale was the fix itself, done before the session. The skill now says to record the statement and let the one fresh re-audit in step 6 serve.
