# Cold run: to-ssp, after the Markdown SSP was retired

Date: 2026-09-29. Skill under test: `skills/flows/to-ssp`, on the fixture with its Markdown SSP, asset inventory, and responsibility matrix stub removed (#105; `2026-09-29-fixture-markdown-ssp-retired.md`). The acceptance check that the writer works when the record is the only SSP. One run on a fresh copy made by `python3 scripts/cold_run.py --skill to-ssp`. The tester got the to-ssp SKILL.md, `ssp-statement-writer`, scribe's folder, ADRs 0007, 0008, and 0010, the scratch engagement, and the fixture company files. The answer key and the rubric were withheld. A second agent graded the run without seeing any SKILL.md.

## Prompt

"Write the SSP statements for 3.1.1, 3.1.8, 3.1.20, and 3.5.3 at Saguaro, from what's in the engagement repo and the company files. Nobody at Saguaro can be asked today. Don't stop between requirements to ask me; record them, then show me the tables."

## Result

| Check | Score |
|---|---|
| Shape match | 2 |
| Known-answer match | 1 |
| Scrub check | 2 |
| Record validity | 2 |
| Record match | 1 |
| Total | 8 |

Pass. Two `set-statements` files, 30 statements for 3.1 and 13 for 3.5, and three `remove-statement` calls taking the tenant off 3.1.1[a], 3.1.1[c], and 3.1.8[a]; no refusals. Against the fixture: 43 statements added, 7 removed, no component, asset, or provider changed. `view/` is exactly what scribe renders. `scope/open-items.md` was created with one line per unconfirmed fact, each naming its objective and who can confirm it. No Markdown SSP file, inventory, or matrix was written, and the tester reported that nothing in the skills asked it to read or write one.

- 3.1.8: [a] implemented on the access control procedure at 3 attempts in 15 minutes, locked 15 minutes; [b] planned on six components; the 5 and 30 claim and the "[TO BE CONFIRMED" text are gone, and both questions are on the open items list.
- 3.1.20: [a] and [b] planned, no longer not applicable, naming the external systems; Sentry SOC on the open items list for `esp-and-msp-scoping`.
- 3.5.3: [d] stays implemented on the tenant, with planned statements on SAG-NAS, the VPN, and Dana's RDP sign-in.
- 3.1.1: [a] and [c] no longer rest on the Entra user list and Entra join; every objective planned or partial except the one miss below.

## The one miss, and a correction to the key

**3.1.1[d] was recorded implemented on the tenant**, on the ground that sign-in needs an enabled account and MFA. The key is better supported: that limits access to account holders, not to authorized users, and the run's own 3.1.1[a] statement says no authorization record exists. Scored 1 on checks 2 and 5. The earlier run on the same prompt (`2026-09-29-to-ssp.md`) kept every 3.1.1 objective planned or partial, and nothing the retirement removed bears on 3.1.1[d], so this is a gap in how the skill treats an enforcement objective whose definition is missing, not something the retirement caused; the tester named it too ("nothing says where an enforcement objective goes when its definition is absent"). Raised as a follow-up rather than changed here.

**3.5.3[c] implemented on the tenant, with planned statements on the RMM, SAG-NAS, the EdgeRouter, and the endpoints.** The common row forbids recording a NOT MET objective implemented, while the 3.5.3 row allowed the same pattern for [d]. The grader found the run's reasoning better supported: the Conditional Access policy does cover the Global Administrators, and the objective fails on the other components. The 3.5.3 row now allows [c] on the tenant on the same terms as [d].

## Left as found

- The fixture's company files say "eight" Windows 11 endpoints and list nine.
- `.scratch/` files were committed in the scratch copy; the cold-run instruction said to add new files, and nothing reaches the record from them.
