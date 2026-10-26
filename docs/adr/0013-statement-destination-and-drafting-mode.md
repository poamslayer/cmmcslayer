# ADR-0013: Statements can be recorded outside `ssp/`, and can be drafted as if met

Date: 2026-10-08. Status: accepted. Issue #140. Builds on ADR-0008 and ADR-0012. Narrows ADR-0010 for one drafting mode.

## Context

A live engagement keeps its conformity statements in a GRC platform (IntelliGRC), with one text and one status per objective. There, the repo's `ssp/` files hold only the scope. `ssp-statement-writer` could record only through scribe, so the skill's writing rules were followed by hand and the recording step was improvised.

The same engagement asked for statements drafted as the system will stand once the planned work is done. Each statement was written in the present tense, as if the control were in place, while the objective's status was left exactly as it was. The status kept telling the truth, and the text was ready for the day the evidence existed. ADR-0010 forbids this in the default case: an objective waiting on an open item is recorded planned, and its statement says only what is true today.

## Decision

The maintainer decided on 2026-10-08:

1. **The destination is a choice, made once per engagement.** `ssp-statement-writer` records into the `ssp/` files through scribe, into a GRC platform, or into another format the operator names. When the engagement already records where its statements live, the skill uses that. Otherwise it asks. Each destination's mechanics live in their own file in the skill folder, disclosed only when that destination is chosen.
2. **The drafting mode is a choice, made per run.** The default mode is ADR-0010, unchanged. In the **as-if-met** mode, a statement is written as if the control is in place, and the objective's status is never changed by the statement pass. Open items are not written for facts the mode assumes. A contradiction with a documented fact or decision is still raised.
3. **Nothing is recorded before the operator sees it.** The skill shows the full text of each requirement's statements and records only on an explicit instruction.

## Considered options

- **Keep scribe as the only destination.** Rejected. An engagement whose statements live elsewhere would keep a second copy that drifts, which is the reason the engagement split its record in the first place.
- **A separate skill for the GRC platform.** Rejected. The writing rules are the valuable part, and two skills would carry them twice.
- **Let as-if-met text set the status to implemented.** Rejected. The status is what keeps an as-if-met SSP honest.

## Consequences

- In the as-if-met mode, the statement text and the status can disagree on purpose. A reader judges the objective by its status and its evidence, not by its text.
- `to-ssp`, `remediate`, and `ssp-lint` still read and write only `ssp/`. Teaching them another destination, and having setup record the destination in `CONTEXT.md`, are follow-ups.
- The fixture records nothing about a destination and has an `ssp/` record, so a run that cannot ask records through scribe in the default mode, as before.
