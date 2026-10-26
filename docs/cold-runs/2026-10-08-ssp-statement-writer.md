# Cold run: ssp-statement-writer, destination and mode (#140)

Date: 2026-10-08. Skill under test: `skills/domain/ssp-poam/ssp-statement-writer`, after it began asking for a destination and a drafting mode (ADR-0013) and gained `destinations/scribe.md` and `destinations/intelligrc.md`. Fresh copies made by `python3 scripts/cold_run.py`. The tester got the skill folder, scribe's folder, ADRs 0008, 0010, 0011, 0012 and 0013, the requirements JSON, the scratch engagement, and the fixture company files. The answer key and the rubric were withheld. A second agent graded each run without seeing the skill.

## Prompt

The same as the 2026-09-29 run: "The previous consultant's statement on 3.1.8[a] has a to-be-confirmed in it and I don't trust it. Fix 3.1.8[a] and record it. Nobody at Saguaro can be asked today; don't stop to ask me."

The point of the run was that the default path is unchanged: with no destination recorded and nobody to ask, the skill records through scribe in the as-is mode.

## First run, 9 of 10, pass (2, 2, 2, 2, 1)

Scribe and the as-is mode, chosen for the right reasons. 3.1.8[a] moved to the access control procedure, implemented, the tenant's statement removed, both questions on `scope/open-items.md` under 3.1.8[b].

The miss: the new rule "point a definition objective at its document" produced "The means ... is defined in the Access Control Procedure" on the access control procedure itself. The statement pointed at itself and named its own component, against the 6.14 common row.

**The skill now says** that when the destination attaches the statement to the defining document itself, as scribe does with a policy or procedure component, the statement states the rule with its values instead of pointing. `destinations/scribe.md` repeats it under its rule against naming the component. The example sentence is neutral, not the fixture's values.

## Second run, on the revised skill, 10 of 10, pass (2, 2, 2, 2, 2)

Recorded on 3.1.8[a], access control procedure, implemented: "The means of limiting unsuccessful logon attempts is account lockout: 3 consecutive failed logon attempts within 15 minutes lock the account for 15 minutes." The tenant's statement removed, the 5 and 30 conflict and the SAG-NAS question on the open items list under 3.1.8[b].

The tester noted that step 2 gave no fallback for the mode when nobody can be asked. **The skill now says** to use the default.

## Left as found

- Neither run committed `scope/open-items.md`; the skill does not say whether to.
- The scribe commits in the scratch copy carried the operator's global git identity, while the fixture commit carries the cold-run identity. `cold_run.py` should set a local identity.
- The key's `to-ssp` row says the procedure's values; its `ssp-statement-writer` row only names them in brackets. The two rows could say the same thing.
