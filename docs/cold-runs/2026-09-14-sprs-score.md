# Cold run: sprs-score-and-poam-eligibility

Date: 2026-09-14. Skill under test: `skills/domain/gap/sprs-score-and-poam-eligibility`. Tester: a fresh agent given only the SKILL.md and the three reference files it cites. The answer key was withheld.

## Prompt

The fixture's eight NOT MET requirements with their objective letters, including the two adjustable cases described by their actual state rather than by their point value: multifactor authentication covering cloud sign-in and privileged access but not general users reaching a file server, and encryption employed everywhere but without FIPS mode and without a validated module.

## Result

| Check | Score | Evidence |
|---|---|---|
| Shape match | 2 | Worksheet produced in the Output template's shape, one row per requirement with the running score. |
| Known-answer match | 2 | Every answer matched. Score 90 of 110, ratio 0.818, Gate 1 passes. Eligible: 3.1.3, 3.6.3, 3.8.4, 3.13.11. Ineligible: 3.1.1 and 3.3.1 on point value, 3.1.20 as a named exclusion, 3.5.3 because its floor is 3 points and it is not the carve-out. Both adjustable requirements were scored from their described state rather than assumed. |
| Scrub check | 2 | Clean. |

Total 6 of 6. Pass.

## Findings

**The tester reached the right conclusion the skill did not state.** It worked out on its own that a passing score ratio does not make Conditional status reachable, because four of the eight NOT MET requirements can never sit on a POA&M and so must be MET before the assessment. It then said the skill made it derive this by combining three separate steps and gave it nowhere to record it.

That was correct and it was the most important sentence in the output, so the skill now answers it directly. The worksheet carries **Conditional status reachable: YES / NO** as its own line above the score, names the blocking requirements when the answer is no, and tells the operator to lead with it out loud, because "your score is 90" on its own reads as good news.

**Two smaller gaps, left as they are.** The tester noted that the skill does not define whether cloud sign-in always counts as remote access for the multifactor adjustment; that is genuinely environment-dependent and belongs with `endpoint-and-vdi-scoping`, which carries the hops test. It also extended the score budget arithmetic backwards to compute remaining headroom, which the skill did not walk through; the worksheet now carries that as a field.
