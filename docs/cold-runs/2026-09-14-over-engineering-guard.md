# Cold run: over-engineering-guard

Date: 2026-09-14. Skill under test: `skills/domain/gap/over-engineering-guard`. Tester: a fresh agent given the SKILL.md, two control files, and the fixture's proposed changes and environment. The answer key was withheld.

## Prompt

The provider has proposed a fix for the device authorization gap. Give your verdict.

## A fixture defect found before the run counted

The first attempt was thrown away. The company-side proposed changes file spelled out the sufficient alternative directly beneath the over-engineered proposal, so a tester reading it as the world it works in was handed the answer it was meant to derive. The company file now carries only what the provider proposed and the justification he gave for it, which is what an operator would actually have in front of them. The verdict stays in the answer key, which the tester never sees.

Worth recording because it is the second time the fixture itself was the thing that was wrong.

## Result

| Check | Score | Evidence |
|---|---|---|
| Shape match | 2 | The output artifact filled in, with both diagnostic questions answered and the sufficient alternative named. |
| Known-answer match | 2 | Matched the key on both halves. 802.1X is optional rather than required, closing a real gap by a form no objective demands; the alternative is address allow-listing plus a periodic scan reconciled against a device roster. Disabling Bluetooth is over-engineering, with blocking the file transfer profile through the endpoint manager already licensed as the cheaper answer. |
| Scrub check | 2 | Clean. |

Total 6 of 6. Pass.

## It beat the answer key

The key argued 802.1X is beyond the bar and expensive. The tester made a better argument: the shop's machine control and its measurement workstation cannot run a certificate supplicant at all, so a certificate rollout across the whole shop would need exceptions for exactly the machines the proposal claims to cover. That is a stronger objection than cost, because it survives the client having the money.

It also caught that the Bluetooth item was sold against the wrong requirement entirely, and said the real risk is not the price but writing it into the SSP as required by a requirement that never asked for it.

## Two gaps reported, both fixed

**The named findings table was being read as keyed to a requirement.** Its 802.1X row is recorded under a different requirement than the one the proposal targeted, and the tester transferred the reasoning but flagged that the skill never says it may. Now stated: the requirement column says where the finding was recorded, not where it applies, and the match is on the shape of the argument. The table narrows where to look; the target requirement's own control file decides.

**Bundled proposals had no rule.** Two controls arrived under one pitch and the output template is written per control. The tester split them, correctly, since the analysis differed completely. Now stated: one verdict per control, never per proposal, because a single verdict on a bundle either buys the control that closes nothing or refuses the one that closes a real gap.

One note was left alone. The tester could not call `normative-requirement-test` because the test denied it every other skill, which is a property of the harness rather than the skill.

## The discarded run found something the clean one did not

The leaked first attempt is not scored, but it is worth reading. Given the same file, it also worked the backup proposal, which cites no requirement at all, and refused to force a verdict: it said the skill's inputs assume a target objective, that this proposal has none, and that guessing one on the vendor's behalf and then grading the guess would be the wrong move.

That is a real hole and it is now filled. A proposal citing no requirement is itself the finding: return **no requirement cited**, say it cannot be judged against a bar nobody has named, and put the question back to whoever proposed it. A proposal that cannot name its objective is discretionary by definition and gets budgeted as discretionary rather than as compliance work.

The same run drew a second distinction the skill had blurred. Whether a cloud service may hold CUI at all is a gate, not excess, and calling an unusable tool over-engineered tells the operator exactly the wrong thing. The skill now routes those questions to the gate skills that own them.

A compromised run still earned its keep, which is an argument for reading a failed test rather than only re-running it.
