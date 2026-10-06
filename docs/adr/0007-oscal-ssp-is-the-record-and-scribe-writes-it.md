# ADR-0007: The OSCAL SSP is the record, and only `scribe` writes it

Date: 2026-09-28. Status: superseded by ADR-0012, which keeps the model and the single writer and replaces OSCAL with Markdown and YAML frontmatter. Issue #65. Research in `docs/research/oscal-*.md`.

## Context

Until now the engagement repo held the SSP as one Markdown file per requirement in `ssp/`, and scoping wrote Markdown files in `scope/`. Several skills wrote those files directly. Issue #65 asked for OSCAL components during scoping. The obvious low-cost path was to keep Markdown as the source of truth and export OSCAL from it on request. That path was considered and rejected.

## Decision

1. **Each engagement has one OSCAL SSP, `ssp.json`, and it is the source of truth.** Components, assets, providers, categories, and conformity statements all live there. `setup-poamslayer-skills` creates it with our profile of all 110 requirements and one stub per requirement, so it is valid from the first commit.
2. **`scribe` is the only writer.** Every skill that decides something calls the Skill tool with `scribe` to record it: scoping skills for components, assets, and providers; `to-ssp` and `ssp-statement-writer` for conformity statements. No skill edits `ssp.json` by hand. `scribe` makes the change through a repo edit script, keeps existing UUIDs, runs oscal-cli, undoes the change if validation fails, and re-renders the view.
3. **Skills that read the SSP read `ssp.json`.** The Markdown in `view/` is generated, read-only, and for people. No skill reads it.
4. **Validation is oscal-cli**, pinned to metaschema-framework `oscal-cli` v3.2.0, with our constraints file for our own fields. It runs after every `scribe` write and in `verify.sh`. The web-session hook installs it.
5. **UUIDs are random v4, minted once, and never regenerated** for an existing object. Renames keep the UUID.

## Considered options

- **Markdown stays the source, OSCAL is an export.** Rejected by the maintainer. OSCAL is the direction the record should move in, and an export that nobody edits drifts from what the skills actually decided.
- **Skills write the JSON directly.** Rejected. Ten skills editing one large JSON file would each need to know OSCAL's shape and UUID rules. One writer holds that knowledge once.
- **A custom Python validator instead of oscal-cli.** Considered, then rejected by the maintainer. oscal-cli is the reference tool and runs NIST's Metaschema constraints, including reference checks that a JSON Schema check misses.
- **Split the SSP into per-requirement fragment files.** Rejected. An OSCAL SSP is one document per system; `scribe` and the edit script keep individual changes small instead.
- **Deterministic v5 UUIDs.** Rejected. A rename would change the identity of the object.

## Consequences

- Every skill that writes to `ssp/` or `scope/` today changes to call `scribe`. Every skill that reads the SSP changes to read JSON.
- Java 11 or later is now a dependency wherever the skills run.
- The fixture in `docs/fixture/engagement/` is converted once to an `ssp.json` through a cold-run copy, never in place, and its answer key and grader move to the JSON.
