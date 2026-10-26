# Cold run: ask-poamslayer for a stranger with no engagement repo

Date: 2026-10-26. Skill under test: `skills/flows/ask-poamslayer`. Issue #143.

## Setup

The tester was a fresh agent given only the router and its PHASE-BOUNDARIES.md. It had no engagement repo, no seat and no other skill. Its prompts were ten real opening posts from r/CMMC, taken word for word from a community corpus. They ask about a newcomer's first step, ITAR specs that are not CUI, 7012 with nothing marked, an outside CAD drafter, CUI during quoting, a Level 1 SSP, a GRC tool, the cost of a mock assessment, NCAGE codes in SPRS, and refusing CUI by email. The posts are not reproduced here because they belong to their authors. The tester rated each reply: clear, ambiguous or no route, and whether it helped the stranger take a next step that day.

This run tests the case the 2026-09-14 run did not: a stranger who has not run setup.

## Result

| | Before (main) | After (this branch) |
|---|---|---|
| Sent to setup before any route | 10 of 10 | 0 of 10 |
| Clear route, including an explicit "outside" answer | 1 | 8 |
| Ambiguous | 4, plus 2 partly clear | 2 |
| No route | 3 | 0 |

## What changed

- Routing never waits for setup. Setup is named after the route, and only when the route writes to the engagement repo.
- When no seat is recorded, the wording defaults to OSC.
- The rule from ask-matt: read a skill's SKILL.md before describing it.
- An "Outside what these skills cover" section: Level 1, Level 3, SPRS mechanics, contract vehicles, product and vendor comparisons, prices, careers.
- Five quick routes taken from the posts.

## Caveats

- The router was edited after its author saw these ten posts, so the after column is fitted to them. The next run should use ten fresh posts.
- The tester graded itself. A separate grader was not used.

## Still open

- Setup says "an empty client repo", which means nothing to a non-technical office manager.
- The router does not say whether gate 1 of `significant-change-determination` needs a repo.
- An "unofficial outside assessment" maps to the self-run mock only by inference.
