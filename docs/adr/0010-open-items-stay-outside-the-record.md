# ADR-0010: Open items stay Markdown, outside the record

Date: 2026-09-29. Status: accepted. Issue #103, settling the question spec #94 left open. Builds on ADR-0007 and ADR-0008. Carried into the Markdown record by ADR-0012: open items stay outside the `ssp/` files.

## Context

The Markdown SSP gave every requirement file an `## Open items` list: the facts nobody had confirmed yet, each with who could confirm it. Moving the SSP into `ssp.json` (ADR-0007) left the question of where those go. OSCAL has no field for an unverified fact on an objective, so keeping them in the record would mean a custom field in our namespace, a new scribe operation, and a view section, all for text that is working notes rather than a claim about the system.

## Decision

The maintainer decided on 2026-09-28:

1. **Open items stay in one Markdown list in the engagement, `scope/open-items.md`.** They are not recorded in `ssp.json`. Each line names the fact, the requirement or objective it bears on in `3.5.3[a]` form when it bears on one, and who will confirm it.
2. **An objective whose statement waits on an open item is recorded `planned`** for that component. The statement says only what is true today, such as what is not yet documented, never the unconfirmed fact with a caveat attached.
3. **Scribe gains no operation for open items.** `to-poam` and `triage` keep working from the list.

## Considered options

- **Open items as a field on each statement in the record.** Rejected. It puts unverified text inside the document an assessor receives, next to the claims it would undermine, and it needs a custom field with no meaning outside this project.
- **One open items list per requirement, as the Markdown SSP had.** Rejected. The per-requirement files are being retired (#105), and the scoping skills already keep one list at `scope/open-items.md`.

## Consequences

- `to-ssp`, `ssp-statement-writer`, `remediate`, and `requirement-applicability-matrix` write unconfirmed facts to `scope/open-items.md` and record the objective as planned.
- An open item that closes lets the next statement pass set the objective to what the confirmed fact supports.
- Nothing in `ssp.json` says why an objective is planned. A reader who needs the reason reads the open items list.
