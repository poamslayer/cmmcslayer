# Unofficial OSCAL catalogs for SP 800-171 Rev 2: candidate evaluation

Provenance: researched 2026-09-28 for issue #65. Question: the maintainer has decided to adopt an existing unofficial OSCAL catalog for NIST SP 800-171 Rev 2 instead of generating one. Which candidate should it be? This note ranks the candidates and recommends one; the choice stays with the maintainer. It follows `docs/research/oscal-800-171-catalogs.md`, which established that NIST publishes no Rev 2 or 800-171A (2018) OSCAL catalog.

Method. Every repository was cloned at the commit pinned in Sources and the catalog files were read locally. Counts, id checks, and text comparisons were done by script, not by reading. Text was compared against `reference/nist-800-171r2-requirements.json` (built from NIST's CSVs) after normalizing whitespace, a trailing period, and the `; :` and `; and :` list artifacts that file carries. Schema validation used `jsonschema` against the catalog JSON Schema from the `usnistgov/OSCAL` release matching each file's declared `oscal-version`, with `\p{L}` rewritten to `[^\W\d_]` and `\p{N}` to `\d` because Python `re` does not support Unicode property classes. The one XML catalog was validated with `xmllint` against the release XSD. Owner type (company org or individual account) comes from the GitHub search API: organizations do not appear in a user search.

## Answer

- Only one candidate meets every hard requirement (a license that lets us vendor it, 110 requirements, 320 objectives, OSCAL token ids, schema-valid): `khanssen/oscal-nist-800-171r2`. It is recommended, pinned to tag `v2.0-combined.1`, with the caveats in Recommendation. Its main risk is that it is two weeks old, owned by an individual account, and has no track record.
- `FATHOM5CORP/oscal` is the only company-published catalog with full 800-171A coverage and the most permissive license (CC0-1.0), but it fails the OSCAL schema on every id (664 of 664 start with a digit, and 3.2.1 is `" 3.2.1 "` with spaces), 23 single-objective requirements carry truncated prose ("ermine if ..."), and it has not changed since 2022-11-23. Adopting it means rewriting every id, which is close to generating our own.
- CyberESI Consulting Group's catalog is "all rights reserved", so we cannot vendor it. It also has no objectives, and its 3.3.1 to 3.3.6 statements are wrong (they hold IoT device capability names such as "Device Identification").
- The rest either have no objectives, rewrite NIST's text, fail the schema, or are not Rev 2 catalogs at all.

## Comparison

"Objectives" counts leaf objective parts. "Tokens" is whether every `id` matches the OSCAL `TokenDatatype` pattern. "Text" is the result of comparing every requirement statement and every objective against the reference file.

| Candidate | Owner type | License | OSCAL | Reqs | Objectives | Tokens | Schema | Text vs reference | Last commit | Commits, 12 mo |
|---|---|---|---|---|---|---|---|---|---|---|
| `khanssen/oscal-nist-800-171r2` | individual | CC-BY-4.0 | 1.1.2 | 110 | 320 | yes | PASS (0 errors) | 9 objectives carry PDF footer text; 2 statements use CPRT spelling | 2026-09-15 | 11 |
| `FATHOM5CORP/oscal` | company org | CC0-1.0 | 1.0.0 | 110 | 320 (317 distinct ids) | no (664 of 664) | FAIL (672 pattern errors) | 5 statements and 23 objectives differ | 2022-11-23 | 0 |
| CyberESI Consulting Group (website, not GitHub) | company | all rights reserved | 1.1.0 (XML) | 110 | 0 | yes | PASS (XSD) | 7 statements differ, 6 of them replaced by unrelated text | 2023-09-15 (file date) | n/a |
| `sam-aydlette/samaydlette.com` (file in a personal website repo) | individual | MIT | 1.2.2 | 110 | 0 | no (344 of 344) | FAIL (all ids) | 2 statements differ | 2026-06-10 (file) | 563 (whole repo) |
| `tbusillo/nist-800-171-oscal` | individual | MIT | 1.0.0-milestone3 | 109 (3.1.9 missing) | 590 leaves, 305 distinct (duplicated) | no | FAIL (not the 1.0 shape) | 3 statements and 20 objectives differ | 2022-06-21 | 0 |
| `grcwarlock/oscal-catalog-library` (`cmmc-oscal/`) | individual | MIT | 1.1.2 | 110 | 0 | yes | PASS | 107 of 110 statements have added non-NIST sentences | 2026-03-31 | 1 |
| `joserodriguezthe1/cmmc-grc-engineering` (`oscal/catalogs/`) | individual | MIT | 1.1.2 | 110 | 0 | no (234 of 234) | FAIL (234 pattern errors) | 79 of 110 statements are paraphrased summaries | 2026-07-08 | 22 |
| `ceagan/oscal-cmmc` | individual | MIT | 1.1.2 | 1 | 6 | yes | FAIL (empty uuid) | only 3.1.1 present | 2025-08-13 | 0 |
| `openprivacy/cmmc-automation` | individual | AGPL-3.0 | 1.1.2 | 17 (Level 1 only) | 0 | yes | PASS | 17 present match | 2025-07-25 | 0 |
| `daves-sandbox/cmmc-oscal-lite-v2` | individual | none | n/a | 0 | 0 | n/a | n/a | all three files are 0 bytes | 2025-11-07 | 1 |
| `GRCEngClub/claude-grc-engineering` | community org | MIT | n/a | no catalog | n/a | n/a | n/a | CMMC content is skill prose only | 2026-08-18 | 210 |
| `dsolis34/nisp-cmmc-toolkit` | individual | none | n/a | no catalog | n/a | n/a | n/a | its own code calls its export "not a fully schema-valid OSCAL 1.x package" | 2026-07-21 | 2 |
| `cazlo/nist-explorer` | individual | not checked | 1.0.0 | 110 | 320 | no | FAIL | byte-identical copy of the FATHOM5 catalog (same SHA-256) | not checked | not checked |

No candidate links its objectives to its statement part (0 `links` on objective parts in every catalog). For Rev 2 this matters less than for Rev 3, because every Rev 2 requirement has a single statement with no lettered items, so an objective can only belong to that one statement.

## Per-candidate detail

### 1. `khanssen/oscal-nist-800-171r2`

- Repo: https://github.com/khanssen/oscal-nist-800-171r2 . Individual account. Created 2026-09-15; all 11 commits are from that day by one author; 1 star, 0 forks, 0 open issues.
- License: `LICENSE` is CC-BY-4.0. It says the NIST text is public domain and that the OSCAL structure, the combination, the id scheme, and the corrections are copyright Archstone Security LLC under CC BY 4.0. We may vendor it with attribution. The README asks for the attribution line "NIST SP 800-171 Rev 2 Combined OSCAL Catalog, Archstone Security LLC, https://github.com/khanssen/oscal-nist-800-171r2" and reserves two trademarks, which does not affect vendoring the file.
- Files: `catalog/nist-sp-800-171r2-combined-catalog.json` (JSON only; no XML or YAML), plus `nist-sp-800-171r2-profile.json` (added after the release tag). Sources are committed in `sources/`: the CPRT Rev 2 export, the 800-171A PDF, and the text extracted from it.
- Metadata: title "NIST SP 800-171 Rev 2 Combined ... Security Requirements with Assessment Procedures", `version` `2.0-combined.1`, `oscal-version` `1.1.2`, `last-modified` 2026-09-15. No parties, no back-matter.
- Releases: tags `v2.0-combined.1` (commit `291261e2`) and `v2.0-combined.1-rc1`. The catalog file is unchanged between the release tag and `main` (`git diff 291261e HEAD` touches only the workflow, README, and the new profile). The release workflow attaches the JSON and a `SHA256SUMS` and runs `actions/attest-build-provenance`. The releases page returned HTTP 403 through this environment, so the attestation itself was not verified.
- Reproducibility: running `python3 scripts/build.py` on a copy of the clone regenerated the committed catalog byte for byte (`git status` clean afterwards). CI does the same on every push and fails on drift.
- Coverage: 14 groups, 110 controls, 320 objective parts, 320 distinct objective ids. Every requirement's objective count matches 800-171A.
- Shape per control: `statement` part (id), `guidance` part (the Rev 2 discussion, id), one `objective` part per determination statement (id, prose, no props), and one `assessment` part (no id) holding EXAMINE / INTERVIEW / TEST as Markdown-style prose. Group ids are `c-3.1` to `c-3.14`.
- Ids for 3.5.3: control `_03.05.03`, statement `_03.05.03_smt`, objectives `_03.05.03_obj.a` to `_03.05.03_obj.d`. All ids in the file match the token pattern (0 of 664 fail). Snippet (guidance and assessment trimmed):

```json
{
 "id": "_03.05.03",
 "title": "Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.",
 "props": [
  { "name": "label", "value": "3.5.3" },
  { "name": "sort-id", "value": "03.05.03" },
  { "name": "requirement-type", "ns": "https://archstonesecurity.com/ns/oscal", "value": "derived" }
 ],
 "parts": [
  { "id": "_03.05.03_smt", "name": "statement", "prose": "Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts." },
  { "id": "_03.05.03_disc", "name": "guidance", "prose": "Multifactor authentication requires the use of two or more different factors to authenticate. ..." },
  { "id": "_03.05.03_obj.a", "name": "objective", "prose": "privileged accounts are identified." },
  { "id": "_03.05.03_obj.b", "name": "objective", "prose": "multifactor authentication is implemented for local access to privileged accounts." },
  { "id": "_03.05.03_obj.c", "name": "objective", "prose": "multifactor authentication is implemented for network access to privileged accounts." },
  { "id": "_03.05.03_obj.d", "name": "objective", "prose": "multifactor authentication is implemented for network access to non-privileged accounts." },
  { "name": "assessment", "prose": "**EXAMINE:** [SELECT FROM: Identification and authentication policy; ...]" }
 ]
}
```

- Spot check: 3.1.1, 3.5.3, and 3.13.11 statements and all 11 of their objectives match the reference.
- Full sweep: 2 statements and 11 objectives differ from the reference.
  - Statements 3.3.2 (a comma after "those users") and 3.5.4 ("nonprivileged") differ from our CSV-derived reference but match the CPRT Rev 2 export committed in the repo. This is a NIST CSV versus NIST CPRT difference, not a catalog error.
  - 9 objectives end with the 800-171A PDF page footer, "This publication is available free of charge from: https://doi.org/10.6028/NIST.SP.800-171A": 3.1.9[a], 3.1.16[b], 3.3.7[a], 3.3.9[b], 3.5.5[a], 3.8.3[b], 3.13.2[e], 3.13.16[a], 3.14.6[c]. This is an extraction defect and contradicts the README's "verbatim" claim.
  - 3.5.8[a] and 3.11.1[b] differ only because our reference carries artifacts ("specified and", ":the"); the catalog text is correct.
- Schema: PASS against the OSCAL v1.1.2 catalog JSON Schema, 0 errors.
- Other findings:
  - `README.md` on `main` contains an unresolved merge conflict (`<<<<<<< HEAD` ... `>>>>>>> 74f579a`), and its identifier table says groups are `fam-3.1` while the file uses `c-3.1`.
  - Objective parts are named `objective`, not `assessment-objective` as NIST's Rev 3 and 800-53 Rev 5 catalogs name them. Both are legal part names, but tooling that looks for `assessment-objective` will not see them.
  - Objectives carry no `label` prop, so the CONTEXT.md form `3.5.3[a]` has to be derived from the id.
  - The zero-padded id `_03.05.03` reads like Rev 3 numbering (`03.05.03`), though NIST's Rev 3 ids are `SP_800_171_03.05.03`, so there is no collision. The README warns about this.
- Maintenance: 11 commits in the last 12 months (all on one day), 0 open issues, one maintainer.

### 2. `FATHOM5CORP/oscal`

- Repo: https://github.com/FATHOM5CORP/oscal . Company GitHub organization. 18 stars, 5 forks, 0 open issues.
- License: CC0-1.0 (the `LICENSE` file is the Creative Commons CC0 1.0 Universal legal code). No attribution needed.
- Files: `content/SP800-171/oscal-content/catalogs/NIST_SP-800-171_rev2_catalog.json` and `.xml`, plus `profiles/NIST_SP-800-171_rev2_FULL-baseline_profile.json`. Metadata `version` `2.0.0`, `oscal-version` `1.0.0`, `last-modified` 2022-10-01.
- Last commit 2022-11-23 (`66d40d56`), 11 commits total, none in the last 12 months, no tags or releases.
- Coverage: 110 controls and 320 leaf objectives, but only 317 distinct objective ids, because 3.2.1's four objectives all have the id `" 3.2.1 _obj.."`.
- Ids for 3.5.3: control `3.5.3`, statement `3.5.3_smt`, a parent objective `3.5.3_obj` with children `3.5.3_obj.a` to `3.5.3_obj.d`, each with a `label` prop `3.5.3[a]` and so on. None of the 664 ids satisfy the token pattern (they start with a digit). Snippet:

```json
{
 "id": "3.5.3",
 "class": "SP800-171",
 "title": "Use multifactor authentication (MFA) for local and network access to privileged accounts and for network access to non- privileged accounts.",
 "props": [ { "name": "label", "value": "3.5.3" }, { "name": "label", "value": "3.5.3", "class": "sp800-171a" }, { "name": "sort-id", "value": "3.5.3" } ],
 "parts": [
  { "id": "3.5.3_smt", "name": "statement", "prose": "Use multifactor authentication (MFA) for local and network access to privileged accounts and for network access to non- privileged accounts." },
  { "id": "3.5.3_obj", "name": "assessment-objective", "props": [ { "name": "label", "value": "3.5.3", "class": "sp800-171a" } ],
    "parts": [
     { "id": "3.5.3_obj.a", "name": "assessment-objective", "props": [ { "name": "label", "value": "3.5.3[a]", "class": "sp800-171a" } ], "prose": "privileged accounts are identified." },
     { "id": "3.5.3_obj.b", "name": "assessment-objective", "props": [ { "name": "label", "value": "3.5.3[b]", "class": "sp800-171a" } ], "prose": "multifactor authentication is implemented for local access to privileged accounts." }
    ] }
 ]
}
```

- Spot check: 3.1.1 matches. 3.5.3's statement adds "(MFA)" and has a line-break artifact "non- privileged"; its four objectives match. 3.13.11's only objective has id `3.13.11_obj.D` and prose "ermine if FIPS-validated cryptography is employed to protect the confidentiality of CUI."
- Full sweep: 5 statements differ (3.1.6 "non-security", 3.1.15, 3.2.2, and 3.5.10 carry "security- relevant" style line-break hyphens, 3.5.3 as above). 23 single-objective requirements have the `_obj.D` id and the truncated "ermine if" prose: 3.4.4, 3.5.4, 3.5.9, 3.5.11, 3.6.3, 3.7.1, 3.7.3, 3.7.4, 3.7.6, 3.8.2, 3.8.6, 3.8.7, 3.8.8, 3.8.9, 3.9.1, 3.10.4, 3.12.3, 3.13.4, 3.13.7, 3.13.11, 3.13.15, 3.13.16, 3.14.4. Titles hold the statement text instead of a title.
- Schema: FAIL against the OSCAL v1.0.0 catalog JSON Schema: 672 errors, 664 on `id` pattern and 8 on `" 3.2.1 "` prop values.

### 3. CyberESI Consulting Group, OSCAL CPRT Catalog Project

- Source: https://cyberesi-cg.com/oscal-cprt-catalog-project/ , not on GitHub. Company.
- License: the project page says "CyberESI Consulting Group, Incorporated retains the copyright to the content hosted on this page with all rights reserved", citing 2 CFR 200.315(b) (the NIST grant that funded it). That rule gives the federal government a license, not us. We cannot legally vendor it.
- File: `OSCAL_Cat_sp_800_171_2_0_0_230915132251.xml` (XML only), `oscal-version` `1.1.0`, catalog `version` `0.0.1`, `last-modified` 2023-09-15.
- Coverage: 110 controls, 0 objectives (part names are only `statement` and `overview`).
- Ids for 3.5.3: control `_3.5.3`, statement `_3.5.3_stmt`, discussion `_3.5.3_dsc`, no objectives. All 347 ids are valid tokens.

```xml
<control class="requirement" id="_3.5.3">
  <title>3.5.3</title>
  <prop name="marking" class="requirement_type" value="RT_derived"/>
  <part name="statement" id="_3.5.3_stmt">
    <p>Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.</p>
  </part>
  <part name="overview" id="_3.5.3_dsc"> ... </part>
</control>
```

- Text: 3.1.1, 3.5.3, and 3.13.11 match. 3.3.1 to 3.3.6 statements are replaced by "Device Identification", "Device Configuration", "Data Protection", "Logical Access to Interfaces", "Software Update", "Cybersecurity State Awareness" (IoT device capability names), while their discussions are the correct audit text. 3.5.4 uses CPRT's "nonprivileged". Discussion paragraphs are run together without a space ("security.Access").
- Schema: PASS against the OSCAL v1.1.0 complete XSD (`xmllint`).

### 4. `sam-aydlette/samaydlette.com`, `data/catalogs/NIST_SP-800-171_rev2_catalog.json`

- A catalog inside a personal website repository. Individual account. MIT. `oscal-version` `1.2.2`, `version` `Rev 2`, `last-modified` 2026-06-10.
- 110 controls, 0 objectives. Ids `3.5.3` and `3.5.3_smt`; control `title` is just `3.5.3`. 344 of 344 ids fail the token pattern.
- Text: 2 statement differences: 3.3.2 (CPRT comma) and 3.5.3, which ends with footnote markers "[24] [25]." 3.1.1 and 3.13.11 match.
- Schema: FAIL against v1.2.2 (every group and control id fails the pattern; the failures cascade into 14 `additionalProperties` errors on groups).

### 5. `tbusillo/nist-800-171-oscal`

- Individual account. MIT. `dist/nist-800-171-rev2.json`, `oscal-version` `1.0.0-milestone3` (a pre-1.0 draft shape: no `catalog` wrapper, `properties` instead of `props`). Its metadata title says "Revision 1" although the README says Rev 2. Last commit 2022-06-21, 0 open issues.
- 109 controls; 3.1.9 is missing. Objective parts appear twice under each control (590 leaves, 305 distinct ids). Ids for 3.5.3: `3.5.3`, `3.5.3_smt`, parent `3.5.3_obj`, children `3.5.3.a_obj` to `3.5.3.d_obj`, then the same four again. No token-valid ids.
- Text: 3.1.1 reads "(including other system)". 3.12.4 and 3.13.12 carry footnote numbers ("systems.26", "remote activation 27"). 20 single-objective requirements, 3.13.11 among them, prefix the objective with "Determine if".
- Schema: FAIL against v1.0.0 (3 top-level errors: no `catalog` root). The milestone3 schema is not published as a release asset.

### 6. `grcwarlock/oscal-catalog-library`, `cmmc-oscal/catalog/catalog.json`

- Individual account. MIT. `oscal-version` `1.1.2`, title "CMMC Level 2 (NIST SP 800-171 Rev 2)". PASS against v1.1.2.
- 110 controls with CMMC practice ids (`ia-l2-3-5-3`, statement `ia-l2-3-5-3_smt`, label `IA.L2-3.5.3`), 0 objectives.
- Text: 107 of 110 statements append the author's own guidance to NIST's text, for example 3.5.3 adds "Combine two or more factors (something you know, have, or are) to strengthen identity verification." That is not NIST text and would put non-authoritative wording in our `statement` parts.

### 7. `joserodriguezthe1/cmmc-grc-engineering`, `oscal/catalogs/NIST_SP800-171_rev2_catalog.json`

- Individual account. MIT. `oscal-version` `1.1.2`, `version` `rev2-summary-0.1`. 22 commits in 12 months, 2 open issues or PRs.
- 110 controls, 0 objectives. Ids `3.5.3`, `3.5.3_smt` (all 234 fail the token pattern, so despite the repository's "schema-valid OSCAL" description the catalog FAILS v1.1.2 with 234 errors).
- Text: 79 of 110 statements are summaries, for example 3.5.3 is "Use multifactor authentication for privileged and network access".

### Not a Rev 2 catalog

- `ceagan/oscal-cmmc` (MIT): `CMMC_v2_catalog.json` holds one control, `AC.L2-3.1.1`, with 6 objectives. The empty `uuid` fails the v1.1.2 schema.
- `openprivacy/cmmc-automation` (AGPL-3.0): a CMMC Level 1 catalog of 17 controls (ids like `_3.1.1`), no objectives. Schema-valid. AGPL would also be a poor fit for vendoring.
- `daves-sandbox/cmmc-oscal-lite-v2`: no license; `README.md`, `requirements.txt`, and `webapp.py` are all empty files.
- `GRCEngClub/claude-grc-engineering` (MIT, community org, 210 commits in 12 months, 29 open issues or PRs): its CMMC plugin is skills and commands in Markdown. It ships no OSCAL catalog.
- `dsolis34/nisp-cmmc-toolkit`: no license, no catalog file; its `oscal_export.py` states the output is not schema-valid OSCAL.
- `cazlo/nist-explorer`: `db/oscal-content/catalogs/NIST_SP-800-171_rev2_catalog.json` is byte-identical to the FATHOM5 file.

## Recommendation (ranked)

1. **`khanssen/oscal-nist-800-171r2`, pinned to tag `v2.0-combined.1` (commit `291261e2`).** It is the only candidate that is legally vendorable, complete (110 and 320), token-valid, and schema-valid, and its build is reproducible from committed NIST sources. Conditions that would make adoption sound:
   - Vendor the released file with its SHA-256 and the CC BY 4.0 attribution line, and record it in `reference/` with a provenance header and in `reference/authorities.md` at a tier that says "unofficial transform of Tier 1 NIST text". Our own skills should keep citing NIST for what a requirement says.
   - Strip the PDF footer sentence from the 9 objectives listed above, either as a documented local patch or by reporting it upstream and taking the fixed release.
   - Decide whether our tooling reads the part name `objective` as is, or maps it to `assessment-objective` at import.
   - Decide whether our SSP writes `_03.05.03` as `control-id` (the catalog's scheme) or keeps its own scheme with a mapping. Adopting a catalog means adopting its ids; the `sp800-171r2-3.5.3` scheme suggested in the earlier note would no longer apply.
   - Accept the bus-factor risk: one maintainer, two weeks of history, one star. Because the build is reproducible and the sources are committed, we could take over maintenance by forking if the project goes quiet, which reduces that risk.
2. **`FATHOM5CORP/oscal`**, only if a company publisher and CC0 outweigh everything else. It would need every id rewritten to pass the schema, the 3.2.1 id fixed, the 23 truncated objectives rewritten, and 5 statements cleaned. It is useful now as an independent cross-check of the khanssen objective text (a script comparison found they agree on every objective except the defects listed above for each, and 3.2.1, whose broken FATHOM5 id kept it from being matched).
3. **`sam-aydlette/samaydlette.com`**: MIT and close to verbatim, but no objectives and no valid ids. Not adoptable for our purpose.
4. **`grcwarlock/oscal-catalog-library`**: valid and MIT, but no objectives and non-NIST text in the statements.
5. **`tbusillo/nist-800-171-oscal`** and **`joserodriguezthe1/cmmc-grc-engineering`**: pre-1.0 format or paraphrased text, and no valid ids. Not adoptable.
6. **CyberESI**: excluded on license (all rights reserved), and the 3.3.x statements are wrong anyway.

## Open questions

- The khanssen release attestation and `SHA256SUMS` were not checked, because GitHub release pages returned 403 here. Run `gh attestation verify` from a machine with GitHub access before vendoring.
- Where NIST's CSV and CPRT disagree (3.3.2 comma, 3.5.4 "nonprivileged" versus "non-privileged"), which is the text of record? The Rev 2 PDF should decide it. This affects our reference file too.
- `reference/nist-800-171r2-requirements.json` carries list artifacts in its objective text (`; :`, `; and :`, "specified and", ":the"). The comparison normalized them, but they are defects in our own reference.

## Sources

- [S1] `khanssen/oscal-nist-800-171r2` at `d03419f6b2aab60ced57d4a05b487a47d3d73af6` (main, 2026-09-15): https://github.com/khanssen/oscal-nist-800-171r2/tree/d03419f6b2aab60ced57d4a05b487a47d3d73af6 ; catalog: https://github.com/khanssen/oscal-nist-800-171r2/blob/d03419f6b2aab60ced57d4a05b487a47d3d73af6/catalog/nist-sp-800-171r2-combined-catalog.json ; release tag `v2.0-combined.1` at `291261e23b0544a7abf010aa8929ccdce1342561`: https://github.com/khanssen/oscal-nist-800-171r2/tree/291261e23b0544a7abf010aa8929ccdce1342561 ; license: https://github.com/khanssen/oscal-nist-800-171r2/blob/d03419f6b2aab60ced57d4a05b487a47d3d73af6/LICENSE
- [S2] `FATHOM5CORP/oscal` at `66d40d56467d0ad2f00692448ac966750bd816fb`: https://github.com/FATHOM5CORP/oscal/blob/66d40d56467d0ad2f00692448ac966750bd816fb/content/SP800-171/oscal-content/catalogs/NIST_SP-800-171_rev2_catalog.json ; license: https://github.com/FATHOM5CORP/oscal/blob/66d40d56467d0ad2f00692448ac966750bd816fb/LICENSE
- [S3] CyberESI Consulting Group, OSCAL CPRT Catalog Project (copyright notice on the page): https://cyberesi-cg.com/oscal-cprt-catalog-project/ ; Rev 2 catalog: https://cyberesi-cg.com/oscal_catalogs_1c/OSCAL_Cat_sp_800_171_2_0_0_230915132251.xml
- [S4] `sam-aydlette/samaydlette.com` at `7c8b1148ca96de8bb31b83d72da1845dff3163cb`: https://github.com/sam-aydlette/samaydlette.com/blob/7c8b1148ca96de8bb31b83d72da1845dff3163cb/data/catalogs/NIST_SP-800-171_rev2_catalog.json
- [S5] `tbusillo/nist-800-171-oscal` at `5fc2ed3a5af50a12d8435cd649ca7cd7f1395429`: https://github.com/tbusillo/nist-800-171-oscal/blob/5fc2ed3a5af50a12d8435cd649ca7cd7f1395429/dist/nist-800-171-rev2.json
- [S6] `grcwarlock/oscal-catalog-library` at `ea49c4c05c8c62098b3766fd8f26b862fb5181f4`: https://github.com/grcwarlock/oscal-catalog-library/blob/ea49c4c05c8c62098b3766fd8f26b862fb5181f4/cmmc-oscal/catalog/catalog.json
- [S7] `joserodriguezthe1/cmmc-grc-engineering` at `0edc3f188d0afa1164eda3088d81728deb33bba9`: https://github.com/joserodriguezthe1/cmmc-grc-engineering/blob/0edc3f188d0afa1164eda3088d81728deb33bba9/oscal/catalogs/NIST_SP800-171_rev2_catalog.json
- [S8] `ceagan/oscal-cmmc` at `ac0b1a1f1f0c57993373af17b309c63e5d0f2083`: https://github.com/ceagan/oscal-cmmc/blob/ac0b1a1f1f0c57993373af17b309c63e5d0f2083/CMMC_v2_catalog.json
- [S9] `openprivacy/cmmc-automation` at `9a36017f6807e4e7c917de8f48087a1ea95a2974`: https://github.com/openprivacy/cmmc-automation/blob/9a36017f6807e4e7c917de8f48087a1ea95a2974/cmmc-level-1-catalog-generated.json
- [S10] `daves-sandbox/cmmc-oscal-lite-v2` at `0bb48eea65aa78c5a0a5b41156d60634eac9c4cd`: https://github.com/daves-sandbox/cmmc-oscal-lite-v2/tree/0bb48eea65aa78c5a0a5b41156d60634eac9c4cd
- [S11] `GRCEngClub/claude-grc-engineering` at `784fd9ab375c95f867a34d865f0b2b59ac899b73`: https://github.com/GRCEngClub/claude-grc-engineering/tree/784fd9ab375c95f867a34d865f0b2b59ac899b73/plugins/frameworks/cmmc
- [S12] `dsolis34/nisp-cmmc-toolkit` at `6f112d24fb01afd199d6d16e3c30ddd73c173020`: https://github.com/dsolis34/nisp-cmmc-toolkit/blob/6f112d24fb01afd199d6d16e3c30ddd73c173020/src/nisp_cmmc/oscal_export.py
- [S13] `cazlo/nist-explorer` at `543b9c8526b9515a571c15d70fcb8b36d76281fb`: https://github.com/cazlo/nist-explorer/blob/543b9c8526b9515a571c15d70fcb8b36d76281fb/db/oscal-content/catalogs/NIST_SP-800-171_rev2_catalog.json
- [S14] OSCAL catalog JSON Schemas and complete XSD used for validation: https://github.com/usnistgov/OSCAL/releases/download/v1.0.0/oscal_catalog_schema.json , https://github.com/usnistgov/OSCAL/releases/download/v1.1.2/oscal_catalog_schema.json , https://github.com/usnistgov/OSCAL/releases/download/v1.2.2/oscal_catalog_schema.json , https://github.com/usnistgov/OSCAL/releases/download/v1.1.0/oscal_complete_schema.xsd
- [S15] Comparison baseline: `reference/nist-800-171r2-requirements.json` in this repository at `6df7f942b149528c51e82d1727b8f01d16f64724`. Candidate discovery: GitHub repository search for "800-171 oscal" and "cmmc oscal", and code search for Rev 2 catalogs containing `oscal-version`, on 2026-09-28.
