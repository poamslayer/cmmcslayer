# Domain Docs

How the skills should consume this engagement repo's domain documentation when exploring it.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root: the client glossary, the scope decisions in force, and the `## Seat` line.
- **`docs/adr/`**: read ADRs that touch the area you're about to work in. The enclave or enterprise decision, the GCC High decision, the printer category, and any significant change memo live here.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `domain-modeling` skill (reached via `grill-with-docs` and `find-cui`) creates them lazily when terms or decisions actually get resolved.

## File structure

An engagement repo is always single-context: one glossary, one ADR folder, at the root.

```
/
├── CONTEXT.md                  client glossary, scope decisions, ## Seat
├── docs/adr/
│   ├── 0001-enclave-or-enterprise.md
│   └── 0002-gcc-high.md
├── scope/                      data flow, network diagram, external systems, open items, interviews; the inventory is in ssp.json
├── ssp/
│   ├── ssp.json                the SSP record, one OSCAL document; only scribe changes it
│   └── oscal/                  the profile and catalog ssp.json imports
├── view/                       generated from ssp.json for people; read by no skill, edited by nobody
├── evidence/                   one folder per requirement
└── policies/                   the policy and procedure set
```

## Use the glossary's vocabulary

When your output names a domain concept (in a ticket title, a conformity statement, an audit finding, an ADR), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids. Say requirement and objective, not control or practice; say responsibility matrix, not CRM; keep POA&M, OPA, and enduring exception as three different things.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the engagement doesn't use (reconsider) or there's a real gap (note it for `domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0002 (GCC High), but worth reopening because…_
