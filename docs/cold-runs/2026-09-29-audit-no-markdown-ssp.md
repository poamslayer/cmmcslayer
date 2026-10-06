# Cold run: audit, after the Markdown SSP was retired

Date: 2026-09-29. Skill under test: `skills/flows/audit`, on the fixture with its Markdown SSP, asset inventory, and responsibility matrix stub removed (#105; `2026-09-29-fixture-markdown-ssp-retired.md`). The acceptance check that the reader works when the record is the only SSP. One run on a fresh copy made by `python3 scripts/cold_run.py --skill audit`. The tester got the audit SKILL.md, the 3.5.3 and 3.1.20 control files, `reference/32-cfr-170-24-scoring.md`, scribe's folder, the scratch engagement, and the fixture company files. The answer key and the rubric were withheld. A second agent graded the run without seeing any SKILL.md.

## Prompt

"Audit 3.5.3 and 3.1.20 against the engagement's current state and write the reports where the skill says to."

## Result

| Check | Score |
|---|---|
| Shape match | 2 |
| Known-answer match | 2 |
| Scrub check | 2 |
| Record validity | 2 |
| Record match | 2 |
| Total | 10 |

Pass. Two scribe `show` calls, one per requirement, and two reports under `.scratch/audit/`. 3.5.3 NOT MET on [a] to [d], 3 points with 5 flagged for a person, not eligible; 3.1.20 NOT MET on [a] to [f], the record's not applicable claim rejected as false. Both match 6.3. `check_record.py --baseline` printed 0 lines added and 0 removed. The tester reported that nothing in the skill pointed it at a Markdown SSP file, an inventory, or a matrix, and that it never opened `view/`.

## What the run found

- The fixture's 3.1.20[a] and [b] carry only the not applicable statement on "Saguaro operating practices", with no "This System" planned row, where scribe now keeps the placeholder beside a not applicable statement (#103). The conversion (#100) recorded them before that rule. Left as found; raised as a follow-up, since changing the fixture's starting record is its own reviewed change.
- The 3.5.3 points rule has no case for MFA enforced on one path for every user while remote and local privileged access have none. The run kept 3 and flagged it, as in the earlier run; unchanged.
- The report header asks for POA&M eligibility, which audit does not decide; the run used the control file's `poam_eligible`. Unchanged.
- `scripts/scrub_check.py` still skips `.scratch/`, so the grader scanned a copy.
