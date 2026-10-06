# Fixture: Saguaro Precision Machining

This folder is a fictional test fixture used to grade the skills in this repository. Nothing here describes a real company, a real person, or a real forum handle, and no text is quoted from any outside source. Every name, part number, and finding below was invented for this fixture.

The fixture has two halves. `company/` is the world an operator would see if they walked into this business: the people, the documents, the network, and a couple of proposed changes and a mock assessment report someone handed them. `engagement/` is the starting state of the client's compliance repository, written the way a previous consultant might have left it: partially done, with realistic gaps and two deliberate plants for the skills under test to catch. Its record is the SSP under `engagement/ssp/`, in the Markdown and YAML frontmatter of ADR-0012. It was converted once from the previous consultant's Markdown SSP and asset inventory into an OSCAL `ssp.json`, mistakes included (`docs/cold-runs/2026-09-28-fixture-ssp-conversion.md`), and then from `ssp.json` into its present form (`docs/cold-runs/2026-10-05-fixture-markdown-ssp-conversion.md`); `engagement/view/` is generated from it. The previous consultant's Markdown has since been retired (`docs/cold-runs/2026-09-29-fixture-markdown-ssp-retired.md`), so the record is the only SSP.

`known-answers.md` is the answer key. It records what each document actually is, how each asset should be categorized, which requirements are NOT MET and why, and how several contested scoping questions should resolve. `grader-rubric.md` explains how a cold run against this fixture is scored.

Do not "fix" the engagement folder in place. Its mistakes are intentional and are listed in `known-answers.md`. A skill under test should always work against a fresh scratch copy, never against this folder directly.

## Folder map

- `company/` - the fictional world: people, documents, IT environment, proposed changes, mock report.
- `engagement/` - the client's compliance repo, starting state. `engagement/ssp/` is the record, the Markdown SSP (ADR-0012); `engagement/view/` is generated from it.
- `known-answers.md` - the answer key.
- `grader-rubric.md` - how a cold run is scored.
