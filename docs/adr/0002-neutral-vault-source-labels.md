# ADR-0002: Vault sources are named by neutral label, with the real map kept private

Date: 2026-09-14. Status: accepted. Builds on ADR-0001.

## Context

ADR-0001 point 8 requires every domain skill to list the vault pages it derives from, so that a change to a vault page tells the maintainer which skills to re-check. ADR-0001 point 2 forbids naming private individuals.

These collide. Several of the most load-bearing vault pages are titled after the practitioner whose material they digest, and the curated community exports are named after the private community they came from. Writing those titles into `vault_sources` puts a person's name and a community's name into a repo that will be public, inside a field whose only purpose is maintenance.

Three options were considered. Dropping `vault_sources` for those pages loses drift detection exactly where the material is richest. Keeping the real titles and exempting frontmatter from the scrub check publishes the names, which is the thing ADR-0001 exists to prevent. Naming them by neutral label keeps both properties at the cost of one local file.

## Decision

1. **A `vault_sources` entry is a topic title or a neutral label, never a person and never a community.** Topic pages keep their real titles, because a title like `CMMC Scoping` or `3.1.20` identifies a subject, not a person.
2. **Person-titled pages are labelled `Practitioner insights <letter>`.** Community exports are labelled `raw/practitioner-community-export-<date>.md`. The letters and dates are stable, so the label identifies one page for the life of the repo.
3. **The map from label to real title lives in `.vault-map.md`, which is gitignored and never committed.** It exists on the maintainer's machine beside the vault. A contributor without the vault does not need it; the maintainer, who has the vault, is the only person for whom drift detection means anything.
4. **The scrub check enforces this**, because every real name and community name is already on the blocklist and the blocklist applies to frontmatter as it applies to prose.

## Consequences

- Drift detection still works for the maintainer: change a vault page, look it up in `.vault-map.md`, re-check the skills that name its label.
- A reader of the public repo can see that a skill rests on practitioner material without learning whose.
- Losing `.vault-map.md` means rebuilding it by matching skill content back to vault pages. It is a local convenience file, so it is regenerated, not recovered.
