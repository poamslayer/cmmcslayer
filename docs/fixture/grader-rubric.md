# Grader Rubric

Every cold run against this fixture is graded on five checks. Each is scored 0, 1, or 2. The total is out of 10. A run passes at 8 or above, with no check scored 0.

Checks 4 and 5 grade the record, `ssp/ssp.json`, which every run leaves whether or not the skill under test writes to it. An SSP that fails oscal-cli scores 0 on check 4, so an invalid record fails the run however good the rest of it is.

## 1. Shape match

Did the skill leave the files or issues the ticket says it should, in the engagement layout, with the sections the skill's own SKILL.md names?

- 2: every artifact is present, in the right place, with the right sections.
- 1: artifacts are present but misplaced, or missing a section.
- 0: an expected artifact is missing.

## 2. Known-answer match

Does the output agree with `known-answers.md` for the question asked, including the reason?

- 2: every checked answer matches, with a correct reason.
- 1: the answers match but a reason is wrong or missing, or exactly one answer differs.
- 0: two or more answers differ from the answer key.

**The answer key is not automatically right.** When a run differs from it, read the reasoning before scoring. A tester that followed the skill correctly and reached a better-supported answer has found a defect in the key, or in the skill, and either way the run has done its job. Correct whichever is wrong, record what changed and why, and re-run. Scoring a run down to protect the key turns the fixture into a thing that agrees with itself.

## 3. Scrub check

Run:

```
python3 scripts/scrub_check.py <output path>
```

- 2: clean.
- 1: warn only.
- 0: any BLOCK or VERBATIM hit.

## 4. Record validity

Run:

```
python3 scripts/check_record.py <scratch copy>
```

It runs oscal-cli on `ssp/ssp.json` with our constraints file, `reference/oscal/cmmc-constraints.xml`.

- 2: the record passes.
- 0: the record is missing, is not JSON, or fails oscal-cli. There is no 1: an SSP is valid or it is not.

A run that edited `ssp.json` by hand, or edited anything under `view/`, scores 0 here too, even if the result validates. The record has one writer, scribe (ADR-0007); `git -C <scratch copy> log -p` shows who wrote what.

## 5. Record match

Run:

```
python3 scripts/check_record.py <scratch copy> --baseline docs/fixture/engagement
```

It prints only what the run changed in the record, as components, assets with their categories, providers with role and FedRAMP status, and statements by objective. Compare that with section 6.14 of `known-answers.md`, which says what each skill's run should leave in the record. A skill 6.14 does not name must leave the record unchanged.

- 2: the record holds what 6.14 says for this skill, and nothing it forbids.
- 1: exactly one expected change is missing or wrong, or the record holds the right answer on the wrong component or objective.
- 0: two or more expected changes are missing or wrong, or a skill that should not touch the record changed it.

The same caution as check 2 applies: a record that departs from the key with better reasoning is a finding about the key.

## Cold-run procedure

a. Copy `docs/fixture/engagement/` to a scratch directory and run `git init` there. Never modify the fixture repository in place.

b. Give a fresh subagent only: the SKILL.md under test, plus any files that SKILL.md itself points to inside its own folder; scribe's folder, when the skill under test records or reads the SSP through scribe, because it cannot write or show the record otherwise; the scratch copy of the engagement repo; the company files under `docs/fixture/company/`; and the exact prompt an operator would type. The subagent gets nothing else. `python3 scripts/cold_run.py --skill <name>` prints this list.

c. The subagent writes its output into the scratch copy.

d. A second subagent grades the scratch copy against `known-answers.md` and this rubric, and writes a short report with the five scores and the evidence for each score. The grader runs `scripts/check_record.py` for checks 4 and 5.

e. Record the result in `docs/cold-runs/<date>-<skill>.md`.

Graders must not be shown the SKILL.md prose. They see only the output and the answer key, so they grade what the operator actually sees.
