> **Provenance.** `nist-800-171r2-catalog.json` is the NIST SP 800-171 Rev 2 Combined OSCAL Catalog, Archstone Security LLC, https://github.com/khanssen/oscal-nist-800-171r2 , licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), pinned to tag `v2.0-combined.1` (commit `291261e23b0544a7abf010aa8929ccdce1342561`, upstream file `catalog/nist-sp-800-171r2-combined-catalog.json`, SHA-256 `13cf12214e57929f2423b77cff8967f2747b4a606a2838ca48c9df7462dc33c1`), retrieved 2026-09-28, and changed as described under "The patch". The requirement, discussion, objective, and assessment text in it is NIST's, from SP 800-171 Rev 2 and SP 800-171A, a US Government work in the public domain. `nist-800-171r2-profile.json`, `cmmc-constraints.xml`, and this file are this repo's own work, MIT.

# reference/oscal

The OSCAL files every engagement's `ssp.json` stands on. The decisions are ADR-0007 (the OSCAL SSP is the record, and oscal-cli validates it), ADR-0008 (conformity statements attach to objectives), and ADR-0009 (this catalog, the patch, our profile, and our namespace).

| File | What it is |
|---|---|
| `nist-800-171r2-catalog.json` | The pinned Rev 2 catalog with our patch: 110 requirements, 320 objectives. Requirement 3.5.3 is `_03.05.03`; objective 3.5.3[a] is `_03.05.03_obj.a`. Its metadata remarks repeat this provenance. |
| `nist-800-171r2-profile.json` | Our profile: imports the catalog above and selects all 110 requirements by id. Each `ssp.json` imports this. We write our own because the upstream profile was added after the pinned tag. |
| `cmmc-constraints.xml` | The definition of every field in our namespace, `https://poamslayer.github.io/ns/cmmc`, as Metaschema constraints oscal-cli enforces. |

## Attribution

"NIST SP 800-171 Rev 2 Combined OSCAL Catalog, Archstone Security LLC, https://github.com/khanssen/oscal-nist-800-171r2", licensed under CC BY 4.0. Changes were made: see below. Archstone Security LLC does not endorse this repository.

## The patch

`scripts/vendor_oscal_catalog.py` is the patch. It starts from the pinned upstream file, refuses to run if the file's SHA-256 is not the pinned one, and makes exactly these changes:

1. Removes the 800-171A PDF page footer, " This publication is available free of charge from: https://doi.org/10.6028/NIST.SP.800-171A", from the end of nine objectives: 3.1.9[a], 3.1.16[b], 3.3.7[a], 3.3.9[b], 3.5.5[a], 3.8.3[b], 3.13.2[e], 3.13.16[a], 3.14.6[c]. It refuses to run if any of the nine lacks the footer, or if any other objective carries it, because either means the pin moved and the patch needs a person to look again.
2. Replaces the document `uuid` and `last-modified`, because OSCAL expects both to change when the content does.
3. Adds the provenance in `metadata.remarks`.

The same footer also appears at the end of many `assessment` parts (the EXAMINE, INTERVIEW, TEST prose). Those are left as upstream wrote them: statements quote objectives, not assessment prose, and the patch stays as small as the problem.

```sh
python3 scripts/vendor_oscal_catalog.py           # fetch the pin, patch, write
python3 scripts/vendor_oscal_catalog.py --check   # fail if the vendored file differs from pin plus patch
```

Moving the pin is a deliberate change: update the tag, commit, and hash at the top of the script together, re-run it, read the diff, and run `bash scripts/verify.sh`.

## Our fields

Every prop we add carries `ns="https://poamslayer.github.io/ns/cmmc"`. First version, four fields. `cmmc-constraints.xml` is the authority; this table is a summary of it.

| Field | Where it may appear | Values |
|---|---|---|
| `asset-category` | `inventory-item` (exactly one); `component` (at most one, only when every asset behind it shares the category) | `cui-asset`, `security-protection-asset`, `contractor-risk-managed-asset`, `specialized-asset`, `out-of-scope-asset` |
| `specialized-asset-type` | `inventory-item` or `component`, only where `asset-category` is `specialized-asset`; required on such an `inventory-item` | `iot`, `iiot`, `ot`, `gfe`, `restricted-information-system`, `test-equipment` |
| `provider-role` | `component` (at most one). Every value is an ESP; `csp` marks the cloud ones | `csp`, `msp`, `mssp`, `soc`, `rmm`, `other-esp` |
| `fedramp-status` | `component` whose `provider-role` is `csp`, where it is required | `fedramp-moderate-authorized`, `fedramp-moderate-equivalent`, `none` |

Any other name in the namespace fails validation. An Out-of-Scope Asset carries its justification in the inventory item's `remarks`.

```sh
oscal-cli validate ssp.json -c reference/oscal/cmmc-constraints.xml
```

oscal-cli takes the file before `-c`: after `-c` it reads every remaining argument as a constraints file.

## How the files are checked

`bash scripts/verify.sh` runs two checks on this folder:

- `scripts/check_oscal_catalog.py` compares every requirement statement and every objective in the catalog with `reference/nist-800-171r2-requirements.json`, allowing only the four known differences recorded in `docs/research/oscal-rev2-catalog-candidates.md` (3.3.2 and 3.5.4, where NIST's CPRT and CSV spell the statement differently, and 3.5.8[a] and 3.11.1[b], where our reference file carries list artifacts). It also checks that the profile imports this catalog and selects exactly its 110 requirements.
- `scripts/check_oscal_cli.py` runs oscal-cli 3.2.0 on the catalog and the profile, resolves the profile to 110 requirements, and proves the constraints file works: it writes a small SSP to a temporary folder, never to the repository, and requires it to pass with valid values and to fail on every rule when each is broken. Missing Java or oscal-cli is a failure, never a skip. Install oscal-cli with `bash scripts/install_oscal_cli.sh`.
