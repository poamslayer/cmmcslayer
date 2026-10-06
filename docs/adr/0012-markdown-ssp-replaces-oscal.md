# ADR-0012: The SSP is Markdown with YAML frontmatter, and OSCAL is removed

Date: 2026-10-04. Status: accepted. Supersedes ADR-0007 and ADR-0009.

## Context

ADR-0007 made one OSCAL document, `ssp.json`, the record, validated by oscal-cli. ADR-0009 vendored an unofficial Rev 2 catalog for it to reference, because NIST publishes none for Rev 2. A week of running it showed the cost. Every machine that runs the skills needs Java 11 and a pinned oscal-cli. The edit script grew to 1,400 lines to hold OSCAL's shape and UUID rules. The fixture's record is 5,700 lines of JSON that people read only through a generated view. Nothing an engagement hands over today needs OSCAL: no customer, C3PAO, or eMASS submission in this work has asked for a Rev 2 OSCAL SSP.

The model ADR-0007 brought with OSCAL is worth keeping: components, assets, providers with a role and FedRAMP status, one conformity statement per objective and component, the five statuses, and the "This System" placeholder. Only the container changes.

## Decision

The maintainer decided on 2026-10-03:

1. **The SSP is the `ssp/` folder of the engagement repo**, in Markdown with YAML frontmatter:
   - `ssp/system.md`: system name, CUI information type and impact, status, and users in frontmatter; the authorization boundary as prose in the body.
   - `ssp/components/<slug>.md`: one per component. Frontmatter holds its type, its assets with their CMMC category, and, for an outside provider, its role and FedRAMP status. The body is the description.
   - `ssp/<requirement>.md`: one per requirement, 110 in all. Frontmatter holds every objective and, under each, a list of statements with `component`, `status`, `statement`, and `remarks`. The body carries the requirement and objective text for people and is never parsed.
2. **Statements live in frontmatter, not in headings or tables**, so objective, component, and status are fields a parser reads, not a writing convention (the reason ADR-0008 gave).
3. **Identity is readable.** A component is its filename slug. An asset is the client's own asset id, unique across the SSP. The placeholder is the reserved slug `this-system`, which has no file. Renaming is a scribe operation that renames the file and rewrites every reference. UUIDs are gone.
4. **Scribe stays the only writer.** It edits the files directly, then runs `check_ssp.py` from its own folder. The check enforces that every objective is present, every status is one of the five, every reference resolves, `alternative` and `not applicable` carry a reason, and the ADR-0011 placeholder rule holds. If the check fails, scribe restores the files with git. If it passes, scribe runs `render_view.py`. `ssp_edit.py` is removed.
5. **The view keeps every page**: a prose page per requirement, the asset inventory, and the responsibility matrix. No skill reads it and nobody edits it.
6. **All OSCAL is removed**: `reference/oscal/`, `ssp.json`, oscal-cli, the Java dependency, its install script and session hook step, and the catalog vendoring and checking scripts. Requirement and objective text comes from `reference/nist-800-171r2-requirements.json`, cleaned once of the PDF fragments the patched catalog had stripped.
7. **An OSCAL export is deferred, not designed.** It is built when a customer, a C3PAO, or eMASS asks for one, most likely at Rev 3, when NIST's own catalog exists.
8. **The fixture is converted once** by a converter run in a cold-run copy, reviewed, and copied back. The run and the converter's source are recorded in `docs/cold-runs/`; the converter is not kept in `scripts/`.

## Considered options

- **Keep OSCAL and simplify around it.** Rejected. The cost is the format and its tooling, not how we use it.
- **Simplify the model with the format**, for example statements per requirement. Rejected. Objective-level scoring and the generated responsibility matrix depend on the model.
- **Statements under headings in the body, or in tables.** Rejected. Headings make the structure a convention a stray `###` can break; long statements in table cells are hard to edit and a pipe breaks the row.
- **One file per objective, one per component, or one file for the whole SSP.** Rejected for one file per requirement, which is how an assessor walks the SSP and keeps each change small.
- **Any skill edits the record.** Rejected. The placeholder rules of ADR-0011 belong in one place.
- **A smaller edit script for scribe.** Rejected. With YAML, a direct edit plus a check that enforces the rules is enough.
- **Keep UUIDs in frontmatter.** Rejected. References nobody can read are the cost OSCAL imposed, and slugs make renames a scribe operation instead.

## Consequences

- Java is no longer a dependency. `verify.sh` runs `check_ssp.py` on the fixture in place of oscal-cli.
- Every skill that reads or writes `ssp.json` changes to the `ssp/` files: scribe, `to-ssp`, `remediate`, `setup-poamslayer-skills`, the router, and the check scripts. Setup scaffolds `system.md` and 110 requirement files with every objective planned on `this-system`.
- ADR-0008, ADR-0010, and ADR-0011 keep their decisions. ADR-0011's `set-statements` batch, which existed because each oscal-cli run took seconds, is retired; the clear and remove distinction stays.
- When CMMC moves to Rev 3, requirement files are renamed to Rev 3 ids by a script, not remapped inside a catalog.
