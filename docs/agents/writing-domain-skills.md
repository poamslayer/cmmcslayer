# Writing a domain skill

Every domain skill under `skills/domain/` is written the same way. This is the brief a worker gets, so it is complete on its own. Read `CONTEXT.md` for the vocabulary and `docs/adr/0001-source-policy.md` for what may and may not be said.

## Shape

One folder per skill: `skills/domain/<phase>/<skill-name>/SKILL.md`, plus `agents/openai.yaml` with `interface.display_name` and `interface.short_description`. Supporting files sit beside `SKILL.md` and are reached by a relative link from it. Nothing links across skill folders; a skill that needs another skill says "call the Skill tool with `<name>`".

Frontmatter:

```yaml
---
name: <skill-name>
description: <model-facing trigger line: what it does and when to reach for it, one or two sentences>
vault_sources:
  - "<wiki page title>"
  - "raw/<file name>"
public_sources:
  - "<title>: <url>"
---
```

`vault_sources` entries name a topic, never a person and never a community. A page titled after a subject keeps its real title (`CMMC Scoping`, `3.1.20`, `Printer Scoping`). A page titled after a practitioner is written as `Practitioner insights A`, `Practitioner insights B`, and so on; a curated community export is written as `raw/practitioner-community-export-<date>.md`. The map back to the real titles lives in `.vault-map.md`, which is gitignored. See `docs/adr/0002-neutral-vault-source-labels.md`. Writing the real title into frontmatter puts a private name in a public repo and the scrub check will reject it.

Add `as_of: YYYY-MM-DD` when the content is perishable (regulatory status) and `confidence: low` when the source was thin. Domain skills are model-invoked: do not set `disable-model-invocation`.

Body, in this order, each as a `##` heading:

1. A one-paragraph statement of what question the skill answers and what it refuses to do.
2. **Inputs**: what the operator or the calling flow must supply (a document, an asset description, a proposed change). Name the engagement repo files it reads (`scope/data-flow.md`, `scope/open-items.md`, `CONTEXT.md`). The SSP, `ssp/ssp.json`, is read by calling the Skill tool with `scribe` and asking it to show the record, and written only through scribe; never name `view/` as an input.
3. **Method**: the rules, tests, and decision tables, as numbered steps. Each step says what to check, what the outcome means, and what to write down. This is where the vault's judgment lives, restated as rules.
4. **Output**: the exact shape of what the skill produces, as a Markdown template in a fenced block, and where it goes in the engagement repo (a file path, an ADR, a `CONTEXT.md` entry, a GitHub issue).
5. **Where practitioners disagree**: each contested point, both positions, and the sentence "the outcome depends on the assessor". Omit the section if nothing is contested.
6. **Seat notes**: one short paragraph each for the consultant seat and the OSC seat, only where the wording or the steps differ. Omit if they do not.
7. **Sources**: the public primary sources, each with a link, and the line "Practitioner consensus, unattributed, backs [which rules]" where that is the only backing.

## Voice

Plain sentences. Second person to the operator. No em dashes; use a comma, colon, or a new sentence. No hedging words that add nothing. Say "assessors have accepted", "assessors have rejected", "the Scoping Guide says", "32 CFR 170.24(c)(2) says". Expand an acronym the first time it appears in the file. Numbers that change what the operator does go in a table.

## What may be said

- Rules, tests, checklists, decision tables, and the reasoning behind them.
- Regulatory and guide text, quoted briefly with the citation.
- "Practitioner consensus" or "assessors have accepted this in practice", with no name and no handle.
- A public person's position, only with a link to where they said it publicly, on the same line.

## What may not be said

- Any handle, any private individual's name, any private community's name, any consulting company's name.
- Any sentence copied from the private wiki. Restate the rule in your own words; the scrub check compares eight-word windows.
- Pricing, competitors, marketing, positioning.
- Anything the vault does not back. If the source is thin, say less and set `confidence: low`.

## Citations

Every URL you cite is in `reference/authorities.md` first. Find the source there, or add it in the right tier, before the skill cites it; `verify.sh` fails otherwise. The tier limits what the source may support: a CUI status rule (whether information is CUI, which category, whether a marking or flowdown makes it CUI) rests on a Tier 1 or Tier 2 entry, and a Tier 3 source supports method only. See `docs/adr/0004-authority-tiers.md`.

Cite `reference/` files by repo-relative path, for example `reference/32-cfr-170-24-scoring.md`, instead of restating tables. Cite the DoD CIO Assessment Guide as "CMMC Level 2 Assessment Guide, DoD CIO, <requirement id>" with the URL `https://dodcio.defense.gov/CMMC/Resources-Documentation/`. Cite the Scoping Guide as "CMMC Level 2 Scoping Guide v2.13, DoD CIO". Cite the eCFR with the section URL. Cite FAQs by question id (for example "CMMC FAQ C-Q9").

## Done when

- The frontmatter validates and names the vault pages the skill came from.
- Every rule in the ticket's description for this skill appears in the Method.
- The Output template exists and names its destination in the engagement repo.
- `python3 scripts/scrub_check.py skills/domain/<phase>/<skill-name>` is clean.
- No em dash anywhere in the folder. `bash scripts/verify.sh` checks this along with everything else.
