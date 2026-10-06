# Fixture: Saguaro Precision Machining

This folder is a fictional test fixture used to grade the skills in this repository. Nothing here describes a real company, a real person, or a real forum handle, and no text is quoted from any outside source. Every name, part number, and finding below was invented for this fixture.

The fixture has two halves. `company/` is the world an operator would see if they walked into this business: the people, the documents, the network, and a couple of proposed changes and a mock assessment report someone handed them. `engagement/` is the starting state of the client's compliance repository, written the way a previous consultant might have left it: partially done, with realistic gaps and two deliberate plants for the skills under test to catch. Its record is `engagement/ssp/ssp.json`, the OSCAL SSP converted once from the previous consultant's Markdown SSP and asset inventory, mistakes included (`docs/cold-runs/2026-09-28-fixture-ssp-conversion.md`); `engagement/view/` is generated from it. That Markdown has since been retired (`docs/cold-runs/2026-09-29-fixture-markdown-ssp-retired.md`), so the record is the only SSP.

`known-answers.md` is the answer key. It records what each document actually is, how each asset should be categorized, which requirements are NOT MET and why, and how several contested scoping questions should resolve. `grader-rubric.md` explains how a cold run against this fixture is scored.

Do not "fix" the engagement folder in place. Its mistakes are intentional and are listed in `known-answers.md`. A skill under test should always work against a fresh scratch copy, never against this folder directly.

## Folder map

- `company/` - the fictional world: people, documents, IT environment, proposed changes, mock report.
- `engagement/` - the client's compliance repo, starting state. `engagement/ssp/ssp.json` is the record; `engagement/view/` is generated from it.
- `known-answers.md` - the answer key.
- `grader-rubric.md` - how a cold run is scored.
