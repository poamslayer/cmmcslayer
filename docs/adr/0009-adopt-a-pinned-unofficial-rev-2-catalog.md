# ADR-0009: Adopt a pinned, patched, unofficial OSCAL catalog for 800-171 Rev 2

Date: 2026-09-28. Status: accepted. Issue #65. Evidence in `docs/research/oscal-800-171-catalogs.md` and `docs/research/oscal-rev2-catalog-candidates.md`.

## Context

CMMC Level 2 assesses NIST SP 800-171 Rev 2. NIST publishes an OSCAL catalog only for Rev 3, and none for Rev 2 or for 800-171A (2018). An SSP needs a catalog to reference.

## Decision

1. **We vendor `khanssen/oscal-nist-800-171r2` at tag `v2.0-combined.1`** into `reference/oscal/`. It was the only candidate with a license that allows vendoring (CC-BY-4.0), all 110 requirements and 320 objectives, valid OSCAL ids, and a clean schema pass. Its ids become ours: requirement 3.5.3 is `_03.05.03`, objective 3.5.3[a] is `_03.05.03_obj.a`.
2. **We patch our copy.** Nine objectives end with the 800-171A PDF footer text. A documented patch strips it, and is re-applied if the pin moves. We do not wait for upstream.
3. **We write our own profile** of all 110 requirements, because the upstream profile was added after the pinned tag.
4. **Provenance.** The file carries a provenance header with the pin, the patch, and the CC-BY attribution the license requires. The repository is registered in `reference/authorities.md` as Tier 3. The requirement text it carries is still NIST's, and `reference/nist-800-171r2-requirements.json` remains the check on it.
5. **Our namespace is `https://poamslayer.github.io/ns/cmmc`.** Our fields in the first version: the asset's CMMC category, the kind of specialized asset, the provider role, and the provider's FedRAMP status. They are defined in one constraints file in `reference/oscal/`, which oscal-cli enforces.

## Considered options

- **Generate our own catalog from `reference/nist-800-171r2-requirements.json`.** Recommended during design and not chosen. It would give us ids we control and no outside dependency.
- **The FATHOM5 catalog.** Company-published and CC0, but every id is invalid OSCAL, the 3.2.1 ids collide, and 23 objectives are truncated.
- **NIST's Rev 3 catalog.** Official, but it describes the wrong revision for Level 2.

## Consequences

- The catalog is two weeks old and has one maintainer. Moving the pin is a deliberate change, re-checked against the reference file and re-patched.
- The zero-padded ids read like Rev 3 numbering. NIST's Rev 3 ids are `SP_800_171_03.05.03`, so there is no collision, but skills show people the `3.5.3[a]` form, never the id.
- When CMMC moves to Rev 3, NIST's official catalog replaces this one, and every `control-id` and `statement-id` in every `ssp.json` is remapped.
