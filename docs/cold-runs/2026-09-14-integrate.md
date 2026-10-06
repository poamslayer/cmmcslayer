# Integration verification

Date: 2026-09-14. This records the checks ticket 25 asks for, and what each one actually proved.

## Automated checks

`bash scripts/verify.sh --strict` runs five checks. Results at the close of the build:

| Check | Result |
|---|---|
| Skill frontmatter and harness metadata | 51 skills, 0 failing |
| Control file schema and the requirements index | 110 of 110 written, 0 failing |
| Router links, strict | 50 named, 50 written, 0 outstanding, 0 unplanned |
| Scrub check | 0 blocked terms, 0 uncited names, 0 verbatim overlaps |
| Em dashes in prose | none |

The skill validator earned its place immediately: it caught a skill shipped without its Codex metadata, which no other check would have found. The index check was added after a worker reported a mismatch, and it is the reason the requirements file now holds 320 objectives rather than 317.

## Install

`npx skills@latest add poamslayer/nist-800-171-skills --all --agent claude` into an empty repository, verified:

- The skills install into `.agents/skills/` and symlink into `.claude/skills/`.
- Supporting files travel with their skill. `control-evidence-lookup` arrives with `CONTROL-FILE-FORMAT.md` and its whole `controls/` directory, which is the thing that would have been easiest to lose and the thing the skill is worthless without.
- `ask-poamslayer` arrives with its phase boundaries reference.

**One real defect, found here and fixed.** The installer copies each skill folder, not the repository, so `reference/` does not arrive. Skills were citing `reference/32-cfr-170-24-scoring.md` by path, which pointed at nothing in a consuming project. Every such citation now also names the public source it reproduces, so the skill works standalone and the repo path stays a convenience for anyone with the clone.

## Cold runs

Recorded in this directory, one file each.

| Skill | Score | Outcome |
|---|---|---|
| `ask-poamslayer` | 6/6 | Pass. Found a contradiction in the significant-change route, fixed before merge. |
| `control-evidence-lookup` | 6/6 | Pass. Disagreement survived the lookup instead of being resolved. |
| `cui-determination-workflow` and `derivative-cui-triage` | 4/6 then 6/6 | Failed, three defects fixed, re-run passed ten of ten. |
| `sprs-score-and-poam-eligibility` | 6/6 | Pass. Surfaced a missing verdict, added. |
| `audit` | 6/6 | Pass. Four gaps reported and fixed. Corrected the fixture's own answer key. |
| `ssp-lint` | 6/6 | Pass. Caught all three planted defects. Two gaps reported and fixed. |
| `over-engineering-guard` | 6/6 | Pass, on the second attempt after a fixture leak was fixed. Beat the answer key's own argument. Two gaps reported and fixed. |
| `remediate` | 6/6 | Pass. Refused to close a ticket on documentation alone, which is the property the loop exists for. |
| `setup-poamslayer-skills` | deterministic | 232 files, 110 SSP stubs, 110 evidence folders, labels, stale-brief warning. |

## What was not tested, and why

**The full main flow end to end was not run as one sequence.** The flows that start it resolve through live exchange with people: `find-cui` runs training and role interviews, and its determination and mapping steps consume answers that do not exist until someone gives them. An agent that answers its own interview questions has tested nothing. The testable half of `find-cui` is the determination and mapping work, and that is covered by the CUI cold run against the same documents those interviews would surface.

The same applies to `wayfinder`, `grilling`, and `to-questionnaire`.

**`remediate` has now been run**, against a scratch engagement seeded with a real ticket on the local markdown tracker. It claimed the ticket, wrote the policy, the evidence register, and the SSP statement, re-audited, found both objectives still NOT MET because nothing in circulation had actually been marked, and left the ticket open. That is the property the loop exists for: a skill that closes a ticket because a policy now exists converts an open gap into a false claim of compliance.

What remains genuinely unexercised is a fix that lands in a live environment rather than a document, which needs a real tenant and real hardware. No fixture can stand in for that, and no cold run should pretend to. Everything else claimed above was observed.

## Eight cold runs, seven defects, and two wrong fixtures

Of eight skills run cold, one failed outright and five more passed while reporting gaps that were worth fixing. Every one of those defects would have reached an engagement, and none would have been found by reading the skill.

The pattern in all four is the same: the skill was written from the source material, which describes what an experienced person does, and the gap only appeared when something had to follow the text without already knowing the answer. A chain in the wrong order, an output template that could not hold the answer the method demanded, a category never named, a counting unit left implicit. None of these are mistakes about CMMC. They are mistakes about writing something another agent has to execute.

The fixture itself was wrong twice, and that is the most useful result here. Once an answer key listed three failed objectives where six had failed, and the tester's reasoning was better than the key's. Once a company-side file spelled out the correct alternative directly beneath the proposal it was meant to test, handing over the answer. A fixture that is never wrong is a fixture nobody is really running against, so the rubric now says the key is not automatically right and AGENTS.md says the same.

The guard run went further and beat the key's argument rather than merely matching it: where the key said an expensive control was beyond the bar, the tester observed that two of the machines it targets cannot run it at all, which is an objection that survives the client having the money.
