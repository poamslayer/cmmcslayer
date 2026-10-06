# ADR-0011: Scribe's statement operations, and when an objective is unanswered

Date: 2026-09-29. Status: accepted. Issue #103, from its cold runs. Builds on ADR-0007 and ADR-0008. Carried into the Markdown record by ADR-0012: the clear and remove distinction and the placeholder rule stay; `set-statements` is retired.

## Context

Spec #94 gave scribe two statement operations: set a conformity statement on one objective and component, and clear it. Every objective starts planned on the "This System" placeholder, which the first statement replaced. The #103 cold runs of the SSP writers found three gaps in that.

- A pass over a family, or a component's not applicable rows, is dozens of statements, and each set starts oscal-cli, which takes seconds.
- Clearing leaves the component on the objective as planned: right for a component that still owes the objective, wrong for one that never should have described it. The statement writer moved 3.1.8[a] off the tenant and left the tenant showing as owing a definition.
- The applicability matrix recorded not applicable rows on objectives no component had answered. The placeholder went at the first statement, so 3.2.1 read as if training applied nowhere, when none had been given.

## Decision

1. **`set-statements`** records a file of statements as one change: the same rules as `set-statement` per entry, one validation, and nothing recorded if any entry is refused.
2. **`remove-statement`** takes a component off an objective it does not describe. `clear-statement` keeps its meaning: the component still owes the objective.
3. **An objective is unanswered while every statement on it is not applicable.** A not applicable statement says the objective does not bear on one component; it does not answer it for the system. Scribe keeps the "This System" placeholder, planned, beside not applicable statements, and drops it when any component records another status. Removing statements brings it back the same way.

## Consequences

- The fixture's record was written under the old rule, and three of its objectives hold only not applicable statements (3.1.20[a] and [b], 3.1.22[a]). They are left as the previous consultant left them; the next scribe write on each settles it.
- `check_record.py` prints a cleared statement left on a named component, so a grader sees the difference between clearing and removing.
