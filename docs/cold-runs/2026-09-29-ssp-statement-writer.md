# Cold run: ssp-statement-writer

Date: 2026-09-29. Skill under test: `skills/domain/ssp-poam/ssp-statement-writer`, after it began recording through scribe (#103). One run on a fresh copy made by `python3 scripts/cold_run.py`. The tester got the SKILL.md, scribe's folder, the ADRs the skill cites (0007, 0008, 0010), the scratch engagement, and the fixture company files. The answer key and the rubric were withheld, and every other skill was unavailable. A second agent graded the run without seeing the SKILL.md.

## Prompt

"The previous consultant's statement on 3.1.8[a] has a to-be-confirmed in it and I don't trust it. Fix 3.1.8[a] and record it. Nobody at Saguaro can be asked today; don't stop to ask me."

## Result

| Check | Score |
|---|---|
| Shape match | 2 |
| Known-answer match | 1 |
| Scrub check | 2 |
| Record validity | 2 |
| Record match | 1 |
| Total | 8 |

Pass. Two scribe commands, no refusals: `set-statements` with one entry, and `clear-statement` for the tenant's old statement. The grader re-rendered `view/` from the run's `ssp.json` and found it identical.

The run moved 3.1.8[a], a definition objective, from the Microsoft 365 tenant to the access control procedure, took the "[TO BE CONFIRMED" text out of the record, and put five lines on a new `scope/open-items.md`: the lockout the tenant actually enforces (5 and 30 claimed, 3 and 15 in the procedure, nothing in `evidence/3.1.8/`), SAG-NAS local accounts, Windows local accounts, whether Saguaro adopts the Northstar template's rule, and ShopTrak as a missing component. Neither 5 nor 30 is recorded anywhere.

The one miss: it recorded [a] partial, because the procedure does not say which accounts it covers. The grader held the key: [a] asks only whether the means is defined, and coverage is what [b] enforces. The run's own open items put the coverage questions on [b].

## What the run found, and what changed

**`clear-statement` left a false row.** Clearing the tenant's statement kept the tenant on 3.1.8[a] as "Planned, Not yet written", which says the tenant owes a definition it never did, and the requirement page showed it. Scribe gained `remove-statement`, for a component that should never have described the objective; clearing stays for one that still owes it. `check_record.py` now prints a cleared statement left on a named component instead of hiding it with the placeholders, so a grader sees it.

**The skill now says** planned, not partial, while anything the objective turns on waits on an open item (ADR-0010); remarks only for alternative and not applicable; record a misplaced statement on the right component, then remove the wrong one; name the paired definition or enforcement objective; create the open items list when there is none; read old Markdown SSP files only as candidate text.

**The key** now spells out both 15-minute values in the procedure, says partial on [a] for a coverage reason is one answer off, and says a tenant left on [a] as planned fails.

## Left as found

- The run's open item on whether Saguaro adopts the Northstar template has merit; no skill yet owns adopting a policy.
- `scrub_check.py` skips `.scratch/` even when a file there is named, so the grader copied the files out to scan them. Suggested as a separate task.

## Reruns on the revised skill

**Second run, 8 of 10, pass** (2, 1, 2, 2, 1). The same call as the first run: [a] partial because the procedure does not list the accounts it covers, with its own open item putting coverage on [b]. The grader held the key again. Two independent runs reading it the same way meant the skill left room for it, so the skill now says outright that a definition objective asks only whether the rule is written down, and which systems carry it out is the enforcement objective's question.

**Third run, on the final skill, 10 of 10, pass** (2, 2, 2, 2, 2). Two scribe commands, no refusals: `set-statement` recording 3.1.8[a] implemented on the access control procedure with its 3 attempts in 15 minutes and 15-minute lock, and `remove-statement` taking the tenant off [a]. Two lines on `scope/open-items.md`, both under 3.1.8[b]: the lockout the tenant actually enforces, and whether local accounts are covered. It noted that Output said "one call to scribe" when a move takes two; the skill now says so and gives an example open items line.
