# OSCAL catalogs for SP 800-171 and 800-171A

Provenance: researched 2026-09-28 for issue #65 ("Generate OSCAL components during scoping"). Question: which official OSCAL catalogs and profiles exist for NIST SP 800-171 Rev 2 and Rev 3 and SP 800-171A, and how do they label requirements, statements, and objectives, so we know what `control-id` and `statement-id` values our SSP would write.

## Answer

- NIST publishes exactly one official OSCAL catalog for 800-171: Rev 3, bundled with 800-171A Rev 3 in the same file, in `usnistgov/oscal-content` under `nist.gov/SP800-171/rev3/` (JSON, minified JSON, XML, YAML). Current release: catalog version `1.1.0`, `oscal-version` `v1.2.2`, published 2026-05-13, repo tag `v1.5.0` (commit `78650f02`). [S1, S2]
- NIST publishes no OSCAL catalog for 800-171 Rev 2 or for 800-171A (June 2018). The CSRC pages for both offer only PDF, CSV, and XLSX. NIST's CPRT tool has JSON exports of both, but those are CPRT's own format, not OSCAL. [S4, S5, S7, S8]
- Rev 3 IDs: control `SP_800_171_03.05.03`; statement part `statement_03.05.03` (or `SR-03.01.01.a` style items when the requirement has lettered parts); assessment objectives are `assessment-objective` parts inside the control, such as `assessment-objective_DS-A.03.05.03.01`. There is no separate 800-171A OSCAL file and no OSCAL profile. [S2]
- No official OSCAL mapping (crosswalk) exists for 800-171 to 800-53 or for Rev 2 to Rev 3. The OSCAL mapping model exists (added in OSCAL v1.2.0), but `oscal-content` ships no mapping instances for 800-171. Rev 3 carries 800-53 Rev 5 references only as `links` to back-matter resources. The Rev 2 to Rev 3 change analysis is an XLSX on CSRC. [S2, S3, S6, S10, S11]
- No official CMMC Level 2 OSCAL catalog or profile was found from DoD CIO or The Cyber AB. Unofficial Rev 2 catalogs exist on GitHub and elsewhere and disagree with each other on IDs. Because CMMC Level 2 is pinned to Rev 2, our skills cannot import an official catalog and must either build their own Rev 2 catalog or adopt an unofficial one. See Recommendation. [S12, S13, S14]

## 1. What NIST publishes

### SP 800-171 Rev 3 and 800-171A Rev 3 (official OSCAL)

`usnistgov/oscal-content` at tag `v1.5.0` (commit `78650f02ad9321bb7b817846f8fbd4f2bcd620de`, 2026-05-13) holds: [S1]

```
nist.gov/SP800-171/rev3/json/NIST_SP800-171_rev3_catalog.json
nist.gov/SP800-171/rev3/json/NIST_SP800-171_rev3_catalog-min.json
nist.gov/SP800-171/rev3/xml/NIST_SP800-171_rev3_catalog.xml
nist.gov/SP800-171/rev3/yaml/NIST_SP800-171_rev3_catalog.yaml
src/nist.gov/SP800-171/rev3/xml/NIST_SP800-171_rev3_catalog.xml   (source; the others are generated)
```

The directory readme says the files carry "the NIST SP 800-171 Rev 3 ... and the NIST SP 800-171A Rev 3 ... in OSCAL formats" and that the published directory holds "the preferred digital reference versions of the SP 800-171 and SP 800-171A bundle." [S1, readme at `nist.gov/SP800-171/rev3/xml/readme.md`]

Metadata of the JSON catalog at that commit: title "Electronic (OSCAL) Version of Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations", `version` `1.1.0`, `oscal-version` `v1.2.2`, `published` `2026-05-13T12:30:00-00:00`. Earlier revisions listed in `metadata.revisions`: `1.0.1` (2026-01-05, "a bug fix for empty statements in security requirements") and `1.0.0` (2025-07-06, OSCAL v1.1.3). Props name the generator as "Cybersecurity And Privacy Open Reference Datasets In OSCAL (CAPORDINO)" and the CPRT framework version `SP_800_171_3_0_0`. [S2]

The catalog is absent from the `v1.3.0` tag tree and present from `v1.4.0` (commit `bc8a528770033611df899b3d52703fb3dc91a20d`, 2025-08-27). [S1]

There is no OSCAL profile for 800-171 in `oscal-content`. The only profiles there are the 800-53 baselines and examples. [S1]

The CSRC Rev 3 publication page itself does not link the OSCAL files. It links a PDF, a Rev 2 to Rev 3 change analysis XLSX, a CUI overlay XLSX, an FAQ, and the CPRT dataset. [S6]

### SP 800-171 Rev 2 (no OSCAL)

The CSRC page for Rev 2 (withdrawn May 14, 2024, superseded by Rev 3) offers the PDF, `sp800-171r2-security-reqs.csv`, `.xlsx`, a CSV readme, and a CSF v1.0 to 800-171 Rev 2 mapping XLSX. No OSCAL. [S4]

The CSV identifies 3.5.3 as `Identifier` `3.5.3`, `Sort-As` `03.05.03`. [S4, CSV]

`oscal-content` has no `rev2` folder under `nist.gov/SP800-171/` on `main`, on tags `v1.3.0`, `v1.4.0`, `v1.5.0`, or on the `prototype-mapping-examples` branch. [S1]

CPRT exports Rev 2 as JSON (`SP_800_171_2_0_0`): 14 families, 110 requirements with ids like `3.5.3`, 110 discussions (`D_3.5.3`), and no assessment objectives and no 800-53 relationships. It is CPRT's own schema, not OSCAL. [S7]

### SP 800-171A (June 2018) (no OSCAL)

The CSRC page (withdrawn May 14, 2024, superseded by 800-171A Rev 3) offers PDF, `sp800-171a-assessment-procedures.csv`, `.xlsx`, and a CSV readme. No OSCAL. [S5]

The CSV rows for 3.5.3: [S5, CSV]

```
Identification and Authentication,3.5.3,03.05.03.0,Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.,Determine if:,...
Identification and Authentication,3.5.3[a],03.05.03.a,,privileged accounts are identified.,,,
Identification and Authentication,3.5.3[b],03.05.03.b,,multifactor authentication is implemented for local access to privileged accounts.,,,
Identification and Authentication,3.5.3[c],03.05.03.c,,multifactor authentication is implemented for network access to privileged accounts.,,,
Identification and Authentication,3.5.3[d],03.05.03.d,,multifactor authentication is implemented for network access to non-privileged accounts.,,,
```

CPRT also exports it as JSON under the identifier `SP_800_171A_1_0_0` (not `SP_800_171_A_...`, which returns an empty response for the old edition). It has 110 requirements, 320 `determination` elements with ids like `DS-3.5.3[a]`, and `E-3.5.3` / `I-3.5.3` / `T-3.5.3` method elements. Its document record has the wrong title ("Assessing Enhanced Security Requirements for Controlled Unclassified Information", which is the 800-172A title). Again CPRT JSON, not OSCAL. [S8]

## 2. ID scheme in the official Rev 3 catalog

Groups are families with ids `SP_800_171_03.01` through `SP_800_171_03.17`. Controls have `class` `requirement` and ids `SP_800_171_03.xx.yy`. The catalog has 130 controls: 97 active and 33 with `props` `status` `withdrawn` and no parts. [S2]

Part naming inside a control: [S2]

| Thing | OSCAL construct | Id pattern |
|---|---|---|
| Requirement | `control` | `SP_800_171_03.05.03` |
| Requirement text, single sentence | part `name: statement`, `class: security_requirement` | `statement_03.05.03` |
| Requirement text, lettered items | part `name: statement` (no id prose) with child parts `name: item` | `SR-03.01.01.a`, `SR-03.01.01.c.01` (label prop repeats the id) |
| Discussion | part `name: guidance` | `guidance_D-03.05.03` |
| 800-171A Rev 3 determination statement | part `name: assessment-objective`, flat, with `links` `rel: assessment-for` to the statement item | `assessment-objective_DS-A.03.05.03.01`, `assessment-objective_DS-A.03.01.01.b.01` |
| Assessment methods | part `name: assessment-method`, prop `method` EXAMINE / INTERVIEW / TEST, child `assessment-objects` | `E-03.05.03_assessment-method_examine` |
| Organization-defined parameter | `params` | `A.03.01.01.ODP.01` (label `A.03.01.01.ODP[01]`) |

Requirement 03.05.03 as published (methods trimmed): [S2]

```json
{
 "id": "SP_800_171_03.05.03",
 "class": "requirement",
 "title": "Multi-Factor Authentication",
 "props": [
  { "name": "sort-id", "value": "03.05.03" },
  { "name": "label", "value": "Multi-Factor Authentication (03.05.03)" }
 ],
 "links": [
  { "href": "#67ce4ecf-5a60-4cfa-8df9-b4eb26bf8e49", "rel": "reference" },
  { "href": "#47920758-65e0-4635-84ee-cab9044da725", "rel": "reference" },
  { "href": "#900b7a48-6d75-4177-aaa6-137d817232c7", "rel": "reference" }
 ],
 "parts": [
  {
   "id": "statement_03.05.03",
   "name": "statement",
   "class": "security_requirement",
   "prose": "Implement multi-factor authentication for access to privileged and non-privileged accounts."
  },
  {
   "id": "guidance_D-03.05.03",
   "name": "guidance",
   "prose": "This requirement applies to user accounts. ..."
  },
  {
   "id": "assessment-objective_DS-A.03.05.03.01",
   "name": "assessment-objective",
   "prose": "multi-factor authentication for access to privileged accounts is implemented.",
   "links": [ { "href": "#SR-03.05.03", "rel": "assessment-for" } ]
  },
  {
   "id": "assessment-objective_DS-A.03.05.03.02",
   "name": "assessment-objective",
   "prose": "multi-factor authentication for access to non-privileged accounts is implemented.",
   "links": [ { "href": "#SR-03.05.03", "rel": "assessment-for" } ]
  },
  { "id": "E-03.05.03_assessment-method_examine", "name": "assessment-method", "...": "..." }
 ]
}
```

The three `reference` links resolve to back-matter resources titled `IA-02(01)`, `IA-02(02)`, and `SP 800-63-3`; the first two carry an `rlink` to the 800-53 Rev 5.1.1 element in CPRT. [S2]

Objective lettering changed between editions. Rev 2 / 800-171A (2018) 3.5.3 has four objectives `[a]` to `[d]`. Rev 3 03.05.03 has two, numbered `[01]` and `[02]` in CPRT (`DS-A.03.05.03[01]`) and `.01` / `.02` in OSCAL ids. [S2, S5, S7c]

### Defects in the Rev 3 catalog to plan around

- Dangling objective links. For the 29 requirements whose statement is one sentence, the `assessment-for` links point to `#SR-03.xx.yy`, but the statement part id is `statement_03.xx.yy`, so no element with that id exists. 03.05.03 is one of them. CPRT uses `SR-03.05.03` for the statement, so the OSCAL converter renamed the part but not the link. Found by resolving every `#` href against every `id` in the JSON at `78650f02`. [S2, S7c]
- Withdrawn requirements link with a bare href. For example `SP_800_171_03.01.21` has `links: [{ "href": "03.01.20", "rel": "incorporated_into" }]`, which is neither a fragment (`#SP_800_171_03.01.20`) nor a URI to a resource. [S2]
- The `alternate` link in `metadata.links` points to the Rev 2 publication page, not to another Rev 3 format. [S2]

## 3. Mappings

- The OSCAL control mapping model (`oscal_mapping_metaschema.xml`) first appears in `usnistgov/OSCAL` at tag `v1.2.0` (commit `8064bf7f`, 2025-12-12) and is absent at `v1.1.3`. Current tag `v1.2.3`. It expresses set-theory relationships (`equivalent-to`, `equal-to`, `subset-of`, `superset-of`, `intersects-with`, `no-relationship`) between a source and target catalog. [S3, S10]
- `oscal-content` at `v1.5.0` contains no file whose path contains "mapping", and the `prototype-mapping-examples` branch adds none for 800-171. No official OSCAL mapping instance for 800-171 to 800-53 or Rev 2 to Rev 3 was found. [S1]
- What exists instead: the Rev 3 catalog's per-requirement `reference` links to 800-53 Rev 5.1.1 controls (above); CPRT's Rev 3 export carries 157 `external_reference` relationships to `SP_800_53_5_1_1`, and the 800-171A Rev 3 export 157 to `SP_800_53_A_5_1_1`; the Rev 2 to Rev 3 change analysis XLSX on CSRC. None is an OSCAL mapping document. [S2, S6, S7b, S7c]
- For Rev 2, the 800-53 relationship lives only in the PDF appendix tables. The Rev 2 CSV has no 800-53 column, and the Rev 2 CPRT export has only internal `projection` relationships. [S4, S7]

## 4. CMMC Level 2 in OSCAL

No official CMMC OSCAL catalog or profile was found. Searches of the DoD CIO site returned the CMMC Assessment Guide and Scoping Guide PDFs and no OSCAL content. The DoD CIO CMMC documentation pages returned HTTP 403 to this environment, so the page listing could not be read directly. That gap is recorded under Open questions. No Cyber AB OSCAL publication was found either; its published process document (CAP) is a PDF. [S12, S13]

Unofficial, not published by NIST, DoD, or The Cyber AB. Each uses a different id scheme for the same requirement:

| Publisher (unofficial) | What | OSCAL version | Id for 3.5.3 | Objectives |
|---|---|---|---|---|
| FATHOM5 (company), `FATHOM5CORP/oscal` | Rev 2 catalog plus a FULL baseline profile, JSON and XML | 1.0.0 | `3.5.3`, statement `3.5.3_smt` | nested `assessment-objective` parts `3.5.3_obj.a` to `.d`, label prop `3.5.3[a]` |
| CyberESI Consulting Group, "OSCAL CPRT Catalog Project" | Rev 2 and Rev 1 catalogs generated from CPRT, plus OSCAL mappings between 800-171 and CSF 1.1, XML | 1.1.0 | `_3.5.3`, statement `_3.5.3_stmt` | none (CPRT Rev 2 export has none) |
| Several individual GitHub accounts | Rev 2 catalogs, some combining 800-171A objectives; CMMC v2 catalogs | 1.0 to 1.1.2 | varies (`3.5.3`, `03.05.03`) | varies |

Sources: [S14, S15, S16]. The FATHOM5 ids `3.5.3` and `3.5.3_smt` start with a digit, which fails the OSCAL `TokenDatatype` pattern `^(\p{L}|_)(\p{L}|\p{N}|[.\-_])*$` from the current catalog JSON schema, so that catalog does not validate against current OSCAL. [S9]

## 5. Recommendation

- There is nothing official to import for Rev 2. Importing the official Rev 3 catalog would be wrong for CMMC Level 2: 32 CFR 170.2 incorporates Rev 2 and 800-171A (2018) (see `reference/authorities.md`), Rev 3 has 97 active requirements in different families (17 groups), and the same number means a different requirement (Rev 2 3.5.3 has four objectives; Rev 3 03.05.03 has two). [S2, S4, S5]
- Build our own Rev 2 plus 800-171A OSCAL catalog in the repo, generated from `reference/nist-800-171r2-requirements.json` (which already came from NIST's CSV), and have the SSP `import-profile` a profile that includes all of it. This keeps provenance at Tier 1 NIST text, avoids a dependency on an unofficial third party, and lets us fix the id scheme.
- Id scheme constraints for our catalog. `control-id` and `statement-id` in the SSP schema are both `TokenDatatype`, so they must start with a letter or underscore and may contain only letters, digits, `.`, `-`, `_`. Bare `3.5.3` and anything with brackets like `3.5.3[a]` are invalid. [S9, S9b]
- Do not reuse NIST's Rev 3 prefix `SP_800_171_03.05.03` for Rev 2 content. It reads as a real NIST Rev 3 id and names a different requirement. Use a prefix that says Rev 2, for example control `sp800-171r2-3.5.3`, statement part `sp800-171r2-3.5.3_smt`, objective parts `sp800-171r2-3.5.3_obj.a` with a `label` prop of `3.5.3[a]` so humans still see the CONTEXT.md form. This is a suggestion for the issue #65 design, not a NIST convention; it probably deserves an ADR.
- Rev 2 requirements have no lettered statement items, so each SSP `implemented-requirement` would carry one `statement` whose `statement-id` is the `_smt` part. If we want per-objective conformity statements (CONTEXT.md makes the objective the unit an SSP statement covers), note that OSCAL `statement-id` is described as a reference to a control statement. Pointing it at `assessment-objective` parts is schema-valid (token only) but outside the documented intent. That trade-off is a decision for issue #65.
- If a Rev 3 path is ever added, import NIST's file pinned to a commit, and work around the dangling `#SR-` links by resolving them to `statement_` ids.

## Open questions

- The DoD CIO CMMC documentation pages returned 403, so the claim "no official CMMC OSCAL" rests on the absence of any hit in searches and on the Cyber AB CAP being PDF. It should be rechecked from a browser.
- Whether NIST plans a Rev 2 OSCAL catalog: none found, and Rev 2 is withdrawn on CSRC, so it looks unlikely, but no NIST statement to that effect was found.
- Whether the dangling `#SR-` links are reported upstream. The `oscal-content` issue tracker was not reachable through this environment's GitHub API access, so this was not checked.
- Which 800-53 revision to cite for Rev 2 crosswalks: Rev 2's own tables map to 800-53 Rev 4. Not re-read from the PDF for this note.

## Sources

- [S1] `usnistgov/oscal-content`, tag `v1.5.0`, commit `78650f02ad9321bb7b817846f8fbd4f2bcd620de`: https://github.com/usnistgov/oscal-content/tree/78650f02ad9321bb7b817846f8fbd4f2bcd620de/nist.gov/SP800-171/rev3 ; readme: https://github.com/usnistgov/oscal-content/blob/78650f02ad9321bb7b817846f8fbd4f2bcd620de/nist.gov/SP800-171/rev3/xml/readme.md ; tag `v1.4.0` commit `bc8a528770033611df899b3d52703fb3dc91a20d`.
- [S2] Rev 3 catalog JSON at the same commit: https://raw.githubusercontent.com/usnistgov/oscal-content/78650f02ad9321bb7b817846f8fbd4f2bcd620de/nist.gov/SP800-171/rev3/json/NIST_SP800-171_rev3_catalog.json
- [S3] `usnistgov/OSCAL`, mapping metaschema at tag `v1.2.3` (commit `e061961c7702afeabffdf5e59894d35e748dade1`): https://github.com/usnistgov/OSCAL/blob/v1.2.3/src/metaschema/oscal_mapping_metaschema.xml ; first present at tag `v1.2.0` (commit `8064bf7f09648505c57c5ca54a1ac409c98f92a0`).
- [S4] SP 800-171 Rev 2 on CSRC: https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final ; CSV: https://csrc.nist.gov/files/pubs/sp/800/171/r2/upd1/final/docs/sp800-171r2-security-reqs.csv
- [S5] SP 800-171A (2018) on CSRC: https://csrc.nist.gov/pubs/sp/800/171/a/final ; CSV: https://csrc.nist.gov/files/pubs/sp/800/171/a/final/docs/sp800-171a-assessment-procedures.csv
- [S6] SP 800-171 Rev 3 on CSRC: https://csrc.nist.gov/pubs/sp/800/171/r3/final ; change analysis: https://csrc.nist.gov/files/pubs/sp/800/171/r3/final/docs/sp800-171r2-to-r3-analysis.xlsx ; 800-171A Rev 3: https://csrc.nist.gov/pubs/sp/800/171/a/r3/final
- [S7] CPRT export, Rev 2: https://csrc.nist.gov/extensions/nudp/services/json/nudp/framework/version/SP_800_171_2_0_0/export/json?element=all ; [S7b] Rev 3: https://csrc.nist.gov/extensions/nudp/services/json/nudp/framework/version/SP_800_171_3_0_0/export/json?element=all ; [S7c] 800-171A Rev 3: https://csrc.nist.gov/extensions/nudp/services/json/nudp/framework/version/SP_800_171_A_3_0_0/export/json?element=all
- [S8] CPRT export, 800-171A (2018): https://csrc.nist.gov/extensions/nudp/services/json/nudp/framework/version/SP_800_171A_1_0_0/export/json?element=all
- [S9] OSCAL v1.2.3 catalog JSON schema (`TokenDatatype`): https://github.com/usnistgov/OSCAL/releases/download/v1.2.3/oscal_catalog_schema.json ; [S9b] SSP JSON schema (`control-id`, `statement-id`): https://github.com/usnistgov/OSCAL/releases/download/v1.2.3/oscal_ssp_schema.json
- [S10] OSCAL control mapping model concepts page: https://pages.nist.gov/OSCAL/learn/concepts/layer/control/mapping/ ; reference: https://pages.nist.gov/OSCAL-Reference/models/latest/mapping/
- [S11] CPRT home: https://csrc.nist.gov/projects/cprt
- [S12] DoD CIO CMMC documentation (403 from this environment): https://dodcio.defense.gov/CMMC/Documentation/ ; CMMC Assessment Guide Level 2 v2.13: https://dodcio.defense.gov/Portals/0/Documents/CMMC/AssessmentGuideL2v2.pdf
- [S13] The Cyber AB, CMMC Assessment Process v2.0 (PDF): https://cyberab.org/Portals/0/CMMC%20Assessment%20Process%20v2.0.pdf
- [S14] Unofficial: FATHOM5, commit `66d40d56467d0ad2f00692448ac966750bd816fb`: https://github.com/FATHOM5CORP/oscal/blob/66d40d56467d0ad2f00692448ac966750bd816fb/content/SP800-171/oscal-content/catalogs/NIST_SP-800-171_rev2_catalog.json
- [S15] Unofficial: CyberESI Consulting Group, OSCAL CPRT Catalog Project: https://cyberesi-cg.com/oscal-cprt-catalog-project/ ; Rev 2 catalog: https://cyberesi-cg.com/oscal_catalogs_1c/OSCAL_Cat_sp_800_171_2_0_0_230915132251.xml
- [S16] Unofficial, individual accounts: found with GitHub repository search for "800-171 oscal" and "cmmc oscal" on 2026-09-28. Repository paths are left out of this file under the house rule on naming private individuals.
