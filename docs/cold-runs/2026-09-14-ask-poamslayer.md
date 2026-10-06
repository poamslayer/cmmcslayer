# Cold run: ask-poamslayer

Date: 2026-09-14. Skill under test: `skills/flows/ask-poamslayer`. Tester: a fresh agent given only the router, its PHASE-BOUNDARIES.md, the fixture engagement `CONTEXT.md`, and the fixture `company/it-environment.md`. No other file, no writes.

## Prompts

Four operator messages, answered twice, once assuming the seat is `osc` and once assuming `consultant`:

1. "Do we even have CUI?"
2. "We got a mock assessment report from a consultant last spring, what do we do with it?"
3. "Our MSP wants us to add a cloud backup tool, is that okay?"
4. "Where do I start?"

## Result

| Check | Score | Evidence |
|---|---|---|
| Shape match | 2 | The router is answer-only and writes nothing, which is what its skill says. Every answer used the route map and the quick-routes table. |
| Known-answer match | 2 | 1 and 4 routed to `find-cui`, 2 to `triage`, 3 to `significant-change-determination`. Routes matched for both seats. Question 4 was resolved the way the router says, by finding the first main-flow stage whose artifacts are missing, correctly identified as stage 1 because the fixture has no `scope/data-flow.md` and no CUI decisions in `CONTEXT.md`. |
| Scrub check | 2 | No blocked term, no uncited name, no verbatim text in the output. |

Total 6 of 6. Pass.

## Findings

**One contradiction, fixed before merge.** The significant-change on-ramp scoped itself to a certified or assessed environment, while the quick-routes table sent a new SaaS tool there unconditionally. The fixture has nothing assessed, so the skill had no answer for its own question 3. The router now splits the case: gate 1 applies at any stage, because a cloud service that will hold CUI needs FedRAMP Moderate authorization or equivalency whatever the engagement's stage, and everything after gate 1 goes to stage 2 as ordinary scoping.

**The seat precondition works.** The fixture's `CONTEXT.md` has no `## Seat` heading. The tester noted unprompted that a real run should stop and tell the operator to run setup, and proceeded only because the test prompt supplied a seat. That is the behaviour the router asks for.

**Seat wording differs as specified.** The OSC answers stayed in plain language, named the people in the company each step needs, and surfaced none of the consultant-only skills. The consultant answers used artifact filenames, requirement ids, ADRs, and stage numbers.
