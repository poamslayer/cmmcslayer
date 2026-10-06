# Cold run: requirement-applicability-matrix

Date: 2026-09-29. Skill under test: `skills/domain/gap/requirement-applicability-matrix`, after it began recording its not applicable and alternative rows through scribe (#103). Two runs, each on a fresh copy made by `python3 scripts/cold_run.py`. Each tester got the SKILL.md, scribe's folder, `reference/`, the scratch engagement, and the fixture company files. The answer key and the rubric were withheld, and every other skill was unavailable. A second agent graded each run without seeing the SKILL.md.

## Prompt

The same for both runs: "Build the applicability matrix for SAG-NAS and the Windows 11 office endpoints and record it. Scope isn't final for the shop floor, the printers, or the providers, so leave those alone; those two components' categories are settled. Don't stop to ask me; record, then show me the tables."

## First run

| Check | Score |
|---|---|
| Shape match | 2 |
| Known-answer match | 1 |
| Scrub check | 2 |
| Record validity | 2 |
| Record match | 2 |
| Total | 9 |

A pass against the key as it then stood, and a failure under the key it led to. Two `set-statements` files recorded 82 not applicable statements on SAG-NAS and 64 on the endpoints, no alternatives, no refusals. The rows the key named were right: 3.2.1 to 3.2.3 and 3.9.1 not applicable, and nothing the devices perform (3.1.1, 3.3.1, 3.5.3, 3.13.11, 3.13.16) touched. The NAS's missing MFA and FIPS validation were kept as gaps, not alternatives, which is the right call.

The rest was not. It recorded all of physical protection (3.10), incident response (3.6), risk and security assessment (3.11, 3.12), and 3.7.6 not applicable "by asset type" on both devices. Those requirements act on the devices and are carried out by the building or a process, so they are inherited. "3.10.1 not applicable to SAG-NAS" reads to an assessor as a claim that nobody limits physical access to it, at a shop whose door code everyone shares. It also recorded 3.10.6 not applicable on a component that includes a laptop. The grader agreed on every point.

**What changed.** The asset-type test now asks whether the requirement is carried out for the component by a facility, a process, or a plan before calling it N/A, and names those families. A mixed component takes the answer of any asset behind it until it is split. The skill also gained partial scope closure for named components, one row per outcome when a requirement's objectives split, an "inherited" outcome in the template, and a rule sending wrong statements on other components to `to-ssp`. The key now fails 3.10.1 or 3.6.1 not applicable, and 3.10.6 not applicable on the endpoints; it allows 3.9.1 as inherited.

## Second run

| Check | Score |
|---|---|
| Shape match | 2 |
| Known-answer match | 2 |
| Scrub check | 2 |
| Record validity | 2 |
| Record match | 2 |
| Total | 10 |

Pass. Four scribe commands, no refusals: `add-component` for "Saguaro office and shop building" (type `physical`) to inherit physical protection from, a `change-component` correcting its description, and two `set-statements` files, 11 statements on the endpoints and 18 on SAG-NAS. Not applicable only for 3.2.1 to 3.2.3 and 3.8.1[a] and [c] on both, and 3.1.19, 3.13.12, and 3.13.14 on the NAS. 3.6, 3.7.6, 3.9, 3.10, 3.11, and 3.12 are inherited in the matrix; 3.10.6 and 3.1.19 apply to the endpoints because of NADIA-LT. The grader re-rendered `view/` and found it identical.

**What the run found: not applicable erased the placeholder.** Scribe dropped an objective's "This System" placeholder at its first statement, whatever its status. After the run, 3.2.1, 3.2.2, 3.2.3, and the others above held only not applicable statements, so the record read as if training applied nowhere, when none has ever been given, and 3.2.1 is a 5-point requirement. Both the tester and the grader reported it. Scribe now keeps the placeholder while every statement on an objective is not applicable, and drops it only when a component records another status (`check_scribe.py` case 24); remove-statement and remove-component bring it back the same way. The fixture's own not applicable objectives (3.1.20[a] and [b], 3.1.22[a]) were written by the previous consultant under the old rule and are left as found, like the rest of its record; the next scribe write on them settles them.

**Also changed:** the step 7 pointer to a pattern the engagement's `CONTEXT.md` does not hold now states the pattern; the template's 3.2.1 row covers [a] to [d] and shows a "gap, nothing compensates" row; the key allows 3.8.1[a] and [c] either way and a facility or process component.

## Left as found

- The endpoints inherit 3.5.1 and 3.5.2 entirely from the tenant while the same matrix treats local administrator accounts as the endpoints' own.
- Whether a laptop is a mobile device for 3.1.18 is not settled by the skill; the run treated it as a mobile computing platform for 3.1.19 only.
- The runs added glossary lines to the engagement `CONTEXT.md`, as the skill says, beside the fixture's stale line that no category decisions are recorded.

## Third run, on the final skill

The reviews and the placeholder rule changed the skill and scribe after the second run, so it was run a third time on a fresh copy, same prompt. **10 of 10, pass** (2, 2, 2, 2, 2). Four scribe commands, no refusals: `add-component` for "Saguaro facility" (`physical`), and three `set-statements` files: 18 statements on SAG-NAS, 11 on the endpoints, and 2 on "Saguaro operating practices" for 3.13.2[b] and [e], not applicable because Saguaro develops no software, recorded on the component that would carry it as step 5 says. The grader found that acceptable though outside the two named components.

Not applicable only for 3.2.1 to 3.2.3 and 3.8.1[a] and [c] on both, and 3.1.19, 3.13.12, and 3.13.14 on the NAS. 3.6, 3.7.6, 3.9.1, 3.10, 3.11, and 3.12 inherited; the NAS's missing MFA and FIPS validation kept as "gap, nothing compensates"; 3.1.18, 3.1.19, 3.8.6, and 3.13.12 applied to the endpoints for NADIA-LT. Every objective holding only not applicable statements kept its "This System" placeholder, planned.

What it changed: the skill listed 3.9.2 as inherited while its account-termination objective is enforced on each component, so 3.9.1 is now the example; a not applicable row never rests on a fact nobody has confirmed; the template's inherited rows are all floor.
