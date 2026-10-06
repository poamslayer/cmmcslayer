# Cold run: setup-poamslayer-skills

Date: 2026-09-28. Skill under test: `skills/setup/setup-poamslayer-skills`, after it began creating `ssp/ssp.json` through scribe (#99). Tester: a fresh agent given the SKILL.md and the files in its folder, an empty git repo with no remote, and the fixture company files. The answer key and the rubric were withheld. A second agent graded the result without seeing the SKILL.md.

## Prompt

`/setup-poamslayer-skills`, with the operator's answers supplied up front because no operator was live: "I'm the IT manager at the machine shop; the owner asked me to get us ready for CMMC"; local markdown tracker; default triage labels; client name from the company files; drafts approved; create `CLAUDE.md`.

## Result

| Check | Score | Evidence |
|---|---|---|
| Shape match | 2 | Every artifact the ticket names, in place. `ssp/ssp.json` passes oscal-cli with our constraints, imports `oscal/nist-800-171r2-profile.json`, and holds 110 requirements and 320 objectives, all planned. `ssp/oscal/` holds byte-identical copies of the profile and catalog. `view/` holds the asset inventory and 110 requirement pages. The Markdown layout is unchanged: 110 stubs, 110 evidence folders, `CONTEXT.md`, `docs/agents/`. |
| Known-answer match | 2 | The answer key has no entry for setup, so the ticket and the company files were the key. Seat `osc`, correct for the shop's own IT manager. Client name "Saguaro Precision Machining, LLC", from the company files, used as the SSP's system name. The closing summary names `ssp.json` as the record only scribe changes and `view/` as generated and read by no skill. |
| Scrub check | 2 | 231 files, 0 block, 0 warn, 0 verbatim. The verbatim half was skipped because the private wiki was absent. |

Total 6 of 6. Pass.

## What the tester found, and what changed

**The script overwrote a client's `CONTEXT.md`.** The skill said the script never overwrites a file and stops if `CONTEXT.md`, `ssp/`, `scope/`, `evidence/`, or `policies/` exists. The script checked only three of those, and skipped existing files only under `--force`. So a repo holding a `CONTEXT.md`, a `README.md`, or a `.gitignore`, and no `ssp/`, had them silently replaced. The tester proved it in a throwaway folder. Fixed: the guard now covers all five, every write skips an existing file, and `scripts/check_setup.py` holds both cases. `ssp.json` was never at risk, because scribe's create refuses to overwrite.

**The step 3 draft named a `## Terms` section the script does not write.** Corrected to the three sections it does write.

**The seed `docs/agents/domain.md` did not show `ssp.json` or `view/`.** An agent reading it would not learn which file is the record. Its tree now shows both.

## Left as found

- 207 objective lines across 85 Markdown stubs end in a stray " :", carried from the requirements reference into the stub template. The stubs are retired in the contract ticket of #94.
- The requirement view pages are headed with the bare identifier, `# 3.1.1`, without the title. That is scribe's renderer.
- The SKILL.md's layout tree omits a few small files the script writes: `README.md`, `.gitignore`, `scope/interviews/`, and `evidence/continuous-monitoring-calendar.md`.
- The client name rule, "take it from the repo folder name or the remote", has no fallback when neither names the client. The step 3 confirmation caught it here.
