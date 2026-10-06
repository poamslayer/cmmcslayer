# OSCAL extensions for CMMC and 800-171 scoping

Provenance: researched 2026-09-28 for issue #65 ("Generate OSCAL components during scoping"). Question: has DoD, The Cyber AB, NIST, FedRAMP, GSA, or anyone else published OSCAL extensions, namespaces, profiles, or property names for CMMC or 800-171 scoping (asset categories, ESP and CSP roles, CMMC levels, POA&M, SPRS), and what conventions should our own namespace follow? Companion to `docs/research/oscal-800-171-catalogs.md`, which covers catalogs and control IDs.

## Answer

- Nobody official has defined OSCAL properties for CMMC. No DoD CIO, DCMA DIBCAC, or Cyber AB document found mentions OSCAL. The CMMC eMASS data standard that C3PAOs must follow is its own JSON format ("the required JSON file format"), not OSCAL, per the CMMC Assessment Process v2.0 (December 2024). The Federal Register and eCFR hold no DoD document that mentions OSCAL. [S16, S19, S20]
- NIST defines no CMMC vocabulary either. The core OSCAL component props cover `asset-type` (hardware and software kinds such as `firewall` or `database`), `implementation-point` (`internal` or `external`), `leveraged-authorization-uuid`, and `inherited-uuid`. None of these expresses a 32 CFR 170.19 asset category. [S2, S3]
- FedRAMP is the reference model for a program namespace: `https://fedramp.gov/ns/oscal`, declared once in a registry file (`FedRAMP_extensions.xml`) that gives each prop a name, description, bindings (where it may appear), a datatype, cardinality, and `allowed-values`. FedRAMP has no asset-category concept. It reuses core `implementation-point` and `leveraged-authorization-uuid` for external and leveraged services, which is the right pattern for our ESP and CSP components. [S11]
- The GSA/fedramp-automation repository no longer resolves (404 from the web, raw, and API endpoints on 2026-09-28; `git ls-remote` asks for credentials). FedRAMP's current repositories label that material "legacy". The files cited here come from a public fork at a pinned commit. The Metaschema external constraints file (`fedramp-external-constraints.xml`) that FedRAMP was building on its `develop` branch could not be retrieved and is unverified. [S10, S11, S12, S13]
- OSCAL's rules: `ns` is an absolute URI used as a name, and it does not have to resolve. Its authority part "must use a value that the organization has control over", typically a DNS domain the organization controls. NIST's own constraints only check props in the NIST namespace, so a prop in a foreign namespace passes NIST validation untouched. A custom name with no `ns` fails, because the component prop-name list has no `allow-other`. [S1, S2, S5, S6, S7]
- Unofficial GitHub projects model 800-171 Rev 2 catalogs and, in one case, SSP and POA&M files under `https://example.com/ns/cmmc`. None models asset categories as props. None is authoritative or widely adopted enough to follow. [S22]
- Recommendation: define our own namespace. Use a URI whose host the project actually controls: `https://poamslayer.github.io/ns/cmmc` today, or a registered project domain if one exists. The URI proposed in earlier notes, `https://poamslayer/ns/cmmc`, has a host with no domain, so it cannot show control and does not follow the OSCAL guidance. Drop the `cmmc-` prefix from prop names because the namespace already carries it. Publish a registry file in the FedRAMP shape. See section 5.

## 1. Official CMMC OSCAL work

What was checked and what was found.

| Publisher | What was checked | Result |
|---|---|---|
| DoD CIO | CMMC Resources and Documentation page; CMMC eMASS introduction PDF | Both return HTTP 403 to scripted requests and to the fetch tool. Unverified. A web search restricted to `dodcio.defense.gov` for "OSCAL" returned no CMMC page that mentions OSCAL. [S17, S18] |
| The Cyber AB | CMMC Assessment Process (CAP) v2.0, December 2024, 29 pages | No occurrence of "OSCAL". The pre-assessment (sections 1.15 to 1.20) and results (sections 3.1 to 3.3) go into CMMC eMASS under "the CMMC eMASS data standard". C3PAOs may use the eMASS Excel templates or "develop or purchase any tool that is compliant with the CMMC eMASS data standard that can generate ... data in the required JSON file format". The standard itself lives in the DoD CMMC eMASS Concept of Operations, which is not public. [S16] |
| CMMC eMASS | Secondary search results name the files `CMMC.PreAssessment.schema.json` and `CMMC.AssessmentResults.schema.json`, hosted on `cmmc.emass.apps.mil` | The names come from a search summary of the DoD CIO eMASS PDF, which was not readable (403). Treat the file names as unverified. Nothing seen suggests they are OSCAL. [S17] |
| DoD in the Federal Register | Federal Register API full-text search for "OSCAL" | Three documents total: a NIST community engagement notice (2024-07-25), a GSA FedRAMP advisory committee meeting notice (2024-12-23), and a NIST ISPAB meeting notice (2022-02-02). No DoD document, no CMMC rule. [S19] |
| 32 CFR (CMMC rule) | eCFR search API for "OSCAL" | Zero results across the CFR. 32 CFR Part 170 does not mention OSCAL. [S20] |
| DCMA DIBCAC, SPRS | Web searches for OSCAL with DIBCAC, SPRS, and eMASS | No primary source found. SPRS takes a score and dates entered through its own interface; no OSCAL import was found. |
| NIST | `usnistgov/oscal-content` at commit `78650f02` | Only 800-171 Rev 3 exists as OSCAL, with no CMMC profile. The Rev 3 catalog uses two NIST namespaces besides the default: `http://csrc.nist.gov/ns/rmf` (281 props, assessment method metadata) and `https://csrc.nist.gov/ns/cprt` (4 props). See the companion note for catalog detail. [S21] |

Conclusion: as of 2026-09-28 there is no official OSCAL namespace, profile, or property list for CMMC, 800-171 Rev 2 scoping, ESP or CSP roles, CMMC levels, POA&M eligibility, or SPRS. The official machine-readable path for CMMC assessment data is the non-OSCAL eMASS JSON standard, which is not published.

## 2. FedRAMP as the reference model

### Where the files are now

`GSA/fedramp-automation` returned 404 on `github.com`, `raw.githubusercontent.com`, and 403 on `api.github.com` on 2026-09-28, and `git ls-remote` asked for credentials, which is what GitHub does for a deleted or private repository. [S10] FedRAMP's current repositories point elsewhere: `FedRAMP/docs` opens with "Historical reference only. This repository is not a source of truth for current FedRAMP rules", and points to `FedRAMP/2026-markdown` and `FedRAMP/rules`. [S13]

A public fork, `oscal-compass-lab/fedramp-automation`, keeps the content. Its `main` branch (commit `76d0473e`, 2026-08-26) carries a "FedRAMP legacy content" banner in its README. Its `legacy` branch (commit `89eddfa2`, 2026-08-14) keeps the older README. Neither branch has the `src/validations/constraints/` directory that holds the Metaschema external constraints, so that file could not be read. A secondary search result claims FedRAMP publishes "fedramp-external-constraints.xml and companions in GSA/fedramp-automation"; that is unverified here. [S11, S12]

### How FedRAMP declares its namespace and props

`dist/content/rev5/resources/xml/FedRAMP_extensions.xml` at the fork's `main` commit: [S11]

- Title "[EXPERIMENTAL] FedRAMP Extensions", version `fedramp2.1.0-oscal1.0.4`, published 2024-09-24.
- One declaration of the namespace: `<extension-namespace ns="https://fedramp.gov/ns/oscal"/>`.
- 92 `<extension>` entries. Each has an `id`, `extension-name` (the prop `name`), `formal-name`, `description`, one or more `binding pattern` XPaths saying where the prop may appear, and a `constraint` with `matches data-type`, `has-cardinality`, and, where the value is a code, `allowed-values` with `allow-other="no"` or `"yes"`. Deprecated entries stay in the file with a "Deprecated." remark and a pointer to the core OSCAL replacement.
- The README of the older branch calls this registry "the authoritative source for all FedRAMP extensions to the OSCAL syntax, FedRAMP-defined identifiers, and accepted values", and names `fedramp_values.xml` as its companion. [S12]

Naming conventions visible in the registry and the SSP template: [S11]

- Names are lowercase, hyphenated tokens: `authorization-type`, `interconnection-data-type`, `scan-type`, `planned-completion-date`, `leveraged-system-identifier`. They are not prefixed with `fedramp-`; the namespace does that job.
- Values are lowercase tokens or typed values (`uuid`, `integer`, `date`).
- Some SSP template props add `class="fedramp"`, for example `<prop ns="https://fedramp.gov/ns/oscal" class="fedramp" name="interconnection-data-type" value="C.3.5.1"/>`.
- The namespace host is a domain FedRAMP controls. `https://fedramp.gov/ns/oscal` does resolve, but only as a redirect (HTTP 301 to `https://www.fedramp.gov/ns/oscal`). It is used as a name, not as a document.

### Asset categories and implementation-point in FedRAMP Rev 5

- FedRAMP has no boundary-category property like CMMC's asset categories. Its `asset-type` extension, bound to `component` and `inventory-item`, lists technology kinds (`os`, `database`, `web-server`, `firewall`, `router`, `switch`, `storage-array`, and so on) with `allow-other="yes"`. That is the same idea as the core OSCAL `asset-type`, not a scoping category. [S11]
- FedRAMP does not define `implementation-point`. It uses the core OSCAL prop. In the Rev 5 SSP template, every component for a leveraged or external service carries `<prop name="implementation-point" value="external"/>` with `leveraged-authorization-uuid` and `inherited-uuid`, all in the default namespace. [S11]
- FedRAMP's `inventory-item-state` extension (`virtual`, `public`, `allows-authenticated-scan`, `is-scanned`) is marked deprecated in favor of the core OSCAL props of the same names. This is FedRAMP's own pattern: when core OSCAL gains a prop, retire the extension. [S11]

### FedRAMP's current direction

FedRAMP's 2026 documentation describes "a transition away from Word and Excel-based templates to simplified JSON documents or (in some cases) optional OSCAL" for Rev 5 providers, and requires agencies to be able to "produce and ingest machine-readable artifacts using formats identified by FedRAMP, including at least" OSCAL and JSON. [S14, S15] So OSCAL is now one accepted format among others at FedRAMP, not the only one. That does not change the value of its registry as a model for our own.

## 3. The OSCAL rules for `ns`

From the metaschema and NIST documentation.

- Definition. In `oscal_metadata_metaschema.xml` (tag `v1.2.3`), the `property` assembly defines `ns` as type `uri` with default `http://csrc.nist.gov/ns/oscal`. Description: "A namespace qualifying the property's name. This allows different organizations to associate distinct semantics with the same name." Remark: "This value must be an absolute URI that serves as a naming system identifier." When `ns` is absent, the name "should be a name defined by the associated OSCAL model." [S1]
- Control of the URI. The OSCAL URI concept page says that for a naming system identifier, "the authority component of the URI must use a value that the organization has control over. Typically, a DNS domain name controlled by the organization is used for this purpose." Its example is `<prop ns="http://example.com/ns/oscal" .../>`. [S5]
- Resolving. The same page says "A URI used only as a name is not required to resolve to a location", and that a URL used consistently as a name may optionally resolve to "information about how to use the URL as a name." [S5] So resolution is optional, and a page that documents the props is a nice extra.
- Why a namespace. The extension tutorial says namespaces let "different organizations ... assign names within their own namespace, without coordinating with other organizations", and that "Using a URI based on a domain name has the advantage of allowing the organization creating a new prop to use something they control as the namespace." [S6]
- How NIST validation treats foreign props. Every NIST prop constraint on components is scoped with `has-oscal-namespace('http://csrc.nist.gov/ns/oscal')`. For example, `oscal-component-prop-name-values` targets `prop[has-oscal-namespace('http://csrc.nist.gov/ns/oscal')]/@name` and has no `allow-other`, so it defaults to `no`. [S2] The Metaschema specification gives `allow-other` a default of `no`. [S7] Two consequences:
  - A prop in our namespace is outside every NIST allowed-values target, so `oscal-cli` and other conformant validators accept any name and value there. Nothing in NIST's constraints checks it. If we want checking, we must ship our own constraints.
  - A custom name with no `ns` (for example `<prop name="asset-category" .../>` on a component) is in the NIST namespace by default and fails `oscal-component-prop-name-values`. So `ns` is mandatory on every prop we invent.
- Extending a NIST prop's values is different. Where NIST sets `allow-other="yes"` (core `asset-type`, for one), a new value may be used in the default namespace. The tutorial shows this with a location `type` of `security-operations-center`. [S3, S6] That route is not available for component prop names.
- Core props we should reuse rather than reinvent: `implementation-point` (`internal` or `external`, "Relative placement of component ... to the system"), `leveraged-authorization-uuid`, `inherited-uuid`, `asset-type`, `public`, `virtual`, `allows-authenticated-scan`. The SSP model also has a `leveraged-authorization` assembly and `inherited` and `satisfied` assemblies for shared responsibility. [S2, S4]
- Pending change. A draft pull request to `usnistgov/OSCAL` (#2267, opened 2026-08-06, still a draft, targeting a feature branch) proposes in-document `prop-definitions` so a document can declare its own prop vocabulary. It admits a breaking change to how an omitted `ns` is read. The `develop` branch (commit `9cea955b`, 2026-09-01) contains no such mechanism. Do not design for it. [S8, S9]

## 4. Unofficial CMMC and 800-171 OSCAL projects on GitHub

All of these are unofficial. None is endorsed by DoD, The Cyber AB, or NIST. Dates are the last commit on the default branch as cloned on 2026-09-28. [S22]

| Repository | Last commit | License | What it models | Namespace |
|---|---|---|---|---|
| `khanssen/oscal-nist-800-171r2` | 2026-09-15 | CC BY 4.0 (copyright held by a security company) | 800-171 Rev 2 catalog with 800-171A objectives, built from CPRT | `https://archstonesecurity.com/ns/oscal` (`requirement-type`, `catalog-uuid`) |
| `joserodriguezthe1/cmmc-grc-engineering` | 2026-07-08 | MIT | Rev 2 catalog, a CMMC L2 SSP, and a POA&M, with Terraform | `https://example.com/ns/cmmc` (`cmmc-id`, `domain`, `implementation-type`, `evidence-source`, `status`, `risk-level`, `owner`, `scheduled-completion`). The SSP has one `this-system` component and no asset-category props. |
| `grcwarlock/oscal-catalog-library` | 2026-03-31 | MIT | Catalogs and profiles for 14 frameworks, including a `cmmc-oscal` folder | none found |
| `ceagan/oscal-cmmc` | 2025-08-13 | MIT | One "CMMCv2" catalog, OSCAL 1.1.2, one group | only NIST `rmf` |
| `openprivacy/cmmc-automation` | 2025-07-25 | AGPL-3.0 | CMMC Level 1 catalog and profile; README says the project moved to GitLab | none |
| `dsolis34/nisp-cmmc-toolkit` | 2026-07-21 | none found | Python gap assessment with "OSCAL-style exports" | not checked in depth |
| `daves-sandbox/cmmc-oscal-lite-v2` | 2025-11-07 | none found | A small web app | none |
| `FATHOM5CORP/oscal` | 2022-11-23 | CC0 1.0 | 800-171 Rev 2 catalog and profile, OSCAL 1.0.x | NIST only |
| `tbusillo/nist-800-171-oscal` | 2022-06-21 | MIT | 800-171 Rev 2 catalog | none |

A search of all their files for "security protection asset", "CRMA", "asset category", and "specialized asset" found those phrases only in prose (catalog text or a skill's Markdown table), never as a prop name or value. No project models ESP or CSP roles, CMMC level, SPRS score, or POA&M eligibility as a namespaced prop, except the one example-domain POA&M above, whose props are generic tracking fields.

One adjacent precedent: MITRE's `hdf-libs` merged an ADR (PR #352, 2026-09-21) that moves every prop its OSCAL exporters invent out of NIST's default namespace into its own namespace. The namespace URI itself was not visible in the fetched page. [S23]

## 5. Recommendation

Define our own namespace. There is nothing official to adopt, and the unofficial namespaces either use a placeholder host (`example.com`) or belong to a third party's domain. Follow the FedRAMP pattern for structure and the OSCAL guidance for the URI.

### Namespace URI

- Use an `https` URI whose host the project controls, with the path shape `/ns/<program>` that NIST (`csrc.nist.gov/ns/oscal`, `/ns/rmf`, `/ns/cprt`) and FedRAMP (`fedramp.gov/ns/oscal`) both use. [S5, S11, S21]
- Proposed: `https://poamslayer.github.io/ns/cmmc`. Only the `poamslayer` GitHub organization can publish under `poamslayer.github.io`, so the host shows control, and a GitHub Pages page at that path can document the props. If the project owns or registers a DNS domain, prefer `https://<that domain>/ns/cmmc` and decide before the first release, because changing a namespace later breaks every document that used it.
- Do not use `https://poamslayer/ns/cmmc`. The host has no domain, so it cannot show control, which the OSCAL URI guidance requires. Do not use a `github.com/poamslayer/...` path either: the authority part would be `github.com`, which the project does not control.
- Version the registry file, not the namespace. FedRAMP keeps one namespace and versions `FedRAMP_extensions.xml`. [S11]

### Property names

Lowercase hyphenated tokens, no `cmmc-` prefix (the namespace carries it), values drawn from the `CONTEXT.md` vocabulary. Every one carries `ns`. This is a proposal for issue #65 to settle, not a finished registry. The "Basis" column names the rule each prop encodes; those citations were not re-read for this note and must go through `reference/authorities.md` before a skill relies on them.

| Prop `name` | Where it binds | Values | Basis |
|---|---|---|---|
| `asset-category` | `component`, `inventory-item` | `cui-asset`, `security-protection-asset`, `contractor-risk-managed-asset`, `specialized-asset`, `out-of-scope-asset`; `allow-other="no"`; cardinality exactly 1 on an in-inventory item | 32 CFR 170.19 asset categories |
| `specialized-asset-type` | same, only where `asset-category` is `specialized-asset` | `iot`, `iiot`, `ot`, `gfe`, `restricted-information-system`, `test-equipment` | the Specialized Asset kinds in 32 CFR 170.19 and `CONTEXT.md` |
| `esp-type` | `component` of type `service` or `organization`-backed service | `csp`, `msp`, `mssp`, `soc`, `other` | ESP and CSP in 32 CFR 170.4 and `CONTEXT.md` |
| `esp-function` | same | `processes-cui`, `security-protection`, `both` | the two ways an ESP enters scope under 32 CFR 170.4 |
| `fedramp-status` | `component` where `esp-type` is `csp` | `fedramp-moderate-authorized`, `fedramp-moderate-equivalent`, `none` | DFARS 252.204-7012(b)(2)(ii)(D) and the DoD CIO equivalency memo (cite through `reference/authorities.md`) |
| `cmmc-level` | `system-characteristics` | `1`, `2`, `3` | 32 CFR 170.14. The prefix is kept here because a bare `level` is ambiguous next to FedRAMP's `impact-level`. |
| `assessment-type` | `system-characteristics` | `self`, `c3pao`, `dibcac` | 32 CFR 170.15 to 170.18 |
| `sprs-score` | `system-characteristics` | integer, -203 to 110 | DoD Assessment Methodology |
| `poam-eligible` | `poam-item` | `yes`, `no` | 32 CFR 170.21 |

Reuse core OSCAL for everything else. ESP and CSP components take `implementation-point="external"`. A FedRAMP-authorized CSP also gets a `leveraged-authorization` entry and `leveraged-authorization-uuid`, as the FedRAMP template does. The responsibility matrix maps to `by-component` with `inherited` and `satisfied`, not to new props. [S2, S4, S11]

### Registry and validation

- Ship one registry file in the repo, modeled on `FedRAMP_extensions.xml`: namespace declared once, then per prop the name, formal name, description, bindings, datatype, cardinality, and allowed values. Write it as a Metaschema external constraints file (the format FedRAMP was moving to, and what `oscal-cli` accepts as extra constraints) so the same file documents and validates. [S7, S11]
- Validation must use our constraints file. NIST's constraints never look at our namespace, so a stock `oscal-cli validate` passes a typo in our values. [S2]
- Publish the registry's human-readable form at the namespace URI when Pages is set up, since OSCAL allows a name URI to resolve to documentation about itself. [S5]
- Before citing any of the 32 CFR, DFARS, or DoD CIO URLs above in a skill, add them to `reference/authorities.md` with their tier, per ADR-0004.

## Open questions

- The CMMC eMASS data standard (`CMMC.PreAssessment.schema.json`, `CMMC.AssessmentResults.schema.json`) is not public. If a C3PAO shares it, map its fields to ours so a later export to eMASS JSON is a transform, not a rewrite. Confirming that the standard is non-OSCAL needs the Concept of Operations or the schemas themselves.
- DoD CIO pages returned 403 to scripted fetches. Someone with a browser should check the CMMC Resources and Documentation page for any OSCAL item added after the CAP v2.0.
- FedRAMP's Metaschema external constraints file (`fedramp-external-constraints.xml`) could not be retrieved because GSA/fedramp-automation is gone and the fork lacks the `develop` branch. If a copy turns up, compare its conventions with the XML registry used here.
- Whether the project will own a domain. That decides between `poamslayer.github.io` and a custom host, and should be settled before any OSCAL file leaves the repo.
- Whether `asset-category` should also be allowed on `system-characteristics` or on `party` (for an ESP as an organization). FedRAMP binds its interconnection props to `component` only; that is the conservative choice.
- Whether draft OSCAL PR #2267 lands. If it does, our registry could also be embedded in each document. Revisit then.

## Sources

- [S1] `usnistgov/OSCAL`, `src/metaschema/oscal_metadata_metaschema.xml`, `property` assembly and its `ns` flag, tag `v1.2.3` (commit `e061961c7702afeabffdf5e59894d35e748dade1`): https://github.com/usnistgov/OSCAL/blob/v1.2.3/src/metaschema/oscal_metadata_metaschema.xml
- [S2] `usnistgov/OSCAL`, `src/metaschema/oscal_implementation-common_metaschema.xml`, component constraints `oscal-component-prop-name-values` and `oscal-component-prop-implementation-point-values`, tag `v1.2.3`: https://github.com/usnistgov/OSCAL/blob/v1.2.3/src/metaschema/oscal_implementation-common_metaschema.xml ; also `oscal_component_metaschema.xml` at the same tag: https://github.com/usnistgov/OSCAL/blob/v1.2.3/src/metaschema/oscal_component_metaschema.xml
- [S3] `usnistgov/OSCAL`, `src/metaschema/shared-constraints/allowed-values-property-name-asset-type-values.ent`, tag `v1.2.3`: https://github.com/usnistgov/OSCAL/blob/v1.2.3/src/metaschema/shared-constraints/allowed-values-property-name-asset-type-values.ent
- [S4] `usnistgov/OSCAL`, `src/metaschema/oscal_ssp_metaschema.xml` (`leveraged-authorization`, `inherited`), tag `v1.2.3`: https://github.com/usnistgov/OSCAL/blob/v1.2.3/src/metaschema/oscal_ssp_metaschema.xml
- [S5] NIST, "URI Usage", OSCAL concepts, last updated March 3, 2025: https://pages.nist.gov/OSCAL/learn/concepts/uri-use/
- [S6] NIST, "Extending Existing OSCAL Models with Props and Links", OSCAL tutorial, last updated November 8, 2023: https://pages.nist.gov/OSCAL/learn/tutorials/general/extension/
- [S7] NIST, Metaschema specification, constraints syntax (`allowed-values`, `allow-other` default `no`, internal and external constraints), last updated August 30, 2024: https://pages.nist.gov/metaschema/specification/syntax/constraints/
- [S8] `usnistgov/OSCAL` pull request #2267, "Add self-contained declared extensions to the control layer", draft, opened 2026-08-06: https://github.com/usnistgov/OSCAL/pull/2267
- [S9] `usnistgov/OSCAL`, `develop` branch at commit `9cea955bcc77a324c817af37fb19cf3b78b09421` (2026-09-01), searched for `extension-definition`: https://github.com/usnistgov/OSCAL/tree/9cea955bcc77a324c817af37fb19cf3b78b09421/src/metaschema
- [S10] `GSA/fedramp-automation`, unreachable on 2026-09-28 (404 web and raw, 403 API, credentials requested by `git ls-remote`): https://github.com/GSA/fedramp-automation
- [S11] `oscal-compass-lab/fedramp-automation` (public fork), `main` at commit `76d0473eafe60676d4acbd6cd76362092c389c46` (2026-08-26). Registry: https://github.com/oscal-compass-lab/fedramp-automation/blob/76d0473eafe60676d4acbd6cd76362092c389c46/dist/content/rev5/resources/xml/FedRAMP_extensions.xml ; values: https://github.com/oscal-compass-lab/fedramp-automation/blob/76d0473eafe60676d4acbd6cd76362092c389c46/dist/content/rev5/resources/xml/fedramp_values.xml ; Rev 5 SSP template: https://github.com/oscal-compass-lab/fedramp-automation/blob/76d0473eafe60676d4acbd6cd76362092c389c46/src/content/rev5/templates/ssp/xml/FedRAMP-SSP-OSCAL-Template.xml ; namespace redirect check: https://fedramp.gov/ns/oscal
- [S12] Same fork, `legacy` branch at commit `89eddfa27da3d3ec8d2b34b61827af40af7169f1` (2026-08-14), README: https://github.com/oscal-compass-lab/fedramp-automation/blob/89eddfa27da3d3ec8d2b34b61827af40af7169f1/README.md
- [S13] `FedRAMP/docs` README at commit `ed5e17f7c69a99a2511a93655353224b23bcf72e`: https://github.com/FedRAMP/docs/blob/ed5e17f7c69a99a2511a93655353224b23bcf72e/README.md
- [S14] `FedRAMP/2026-markdown` at commit `2f81e380a6615d48927a72c5007df785c038f891`: https://github.com/FedRAMP/2026-markdown/blob/2f81e380a6615d48927a72c5007df785c038f891/providers/updating/changes.md ; https://github.com/FedRAMP/2026-markdown/blob/2f81e380a6615d48927a72c5007df785c038f891/agencies/rules/agency-use.md
- [S15] `FedRAMP/rules` at commit `58487bda77d76d9ce334304ec2e779ece7cc7d54`, `fedramp-consolidated-rules.json`: https://github.com/FedRAMP/rules/blob/58487bda77d76d9ce334304ec2e779ece7cc7d54/fedramp-consolidated-rules.json
- [S16] The Cyber AB, CMMC Assessment Process (CAP) v2.0, December 2024: https://cyberab.org/Portals/0/CMMC%20Assessment%20Process%20v2.0.pdf
- [S17] DoD CIO, "Introduction to the CMMC Enterprise Mission Assurance Support Service (eMASS)", HTTP 403, unverified: https://dodcio.defense.gov/Portals/0/Documents/CMMC/CMMC-eMASS.pdf
- [S18] DoD CIO, CMMC Resources and Documentation, HTTP 403, unverified: https://dodcio.defense.gov/CMMC/Resources-Documentation/
- [S19] Federal Register API full-text search for "OSCAL", run 2026-09-28: https://www.federalregister.gov/api/v1/documents.json?conditions%5Bterm%5D=OSCAL ; results: https://www.federalregister.gov/documents/2024/07/25/2024-16381/community-engagement-on-the-open-security-controls-assessment-language-oscal , https://www.federalregister.gov/documents/2024/12/23/2024-30489/federal-secure-cloud-advisory-committee-notification-of-upcoming-meeting , https://www.federalregister.gov/documents/2022/02/02/2022-02064/open-meeting-of-the-information-security-and-privacy-advisory-board
- [S20] eCFR search API for "OSCAL", run 2026-09-28, zero results: https://www.ecfr.gov/api/search/v1/results?query=OSCAL ; 32 CFR Part 170: https://www.ecfr.gov/current/title-32/part-170 ; 170.4: https://www.ecfr.gov/current/title-32/section-170.4 ; 170.19: https://www.ecfr.gov/current/title-32/section-170.19
- [S21] `usnistgov/oscal-content` at commit `78650f02ad9321bb7b817846f8fbd4f2bcd620de` (tag `v1.5.0`), Rev 3 catalog JSON: https://github.com/usnistgov/oscal-content/blob/78650f02ad9321bb7b817846f8fbd4f2bcd620de/nist.gov/SP800-171/rev3/json/NIST_SP800-171_rev3_catalog.json
- [S22] Unofficial repositories, default branch as cloned 2026-09-28: https://github.com/khanssen/oscal-nist-800-171r2 (commit `d03419f`) ; https://github.com/joserodriguezthe1/cmmc-grc-engineering (commit `0edc3f1`) ; https://github.com/grcwarlock/oscal-catalog-library (commit `ea49c4c`) ; https://github.com/ceagan/oscal-cmmc (commit `ac0b1a1`) ; https://github.com/openprivacy/cmmc-automation (commit `9a36017`) ; https://github.com/dsolis34/nisp-cmmc-toolkit (commit `6f112d2`) ; https://github.com/daves-sandbox/cmmc-oscal-lite-v2 (commit `0bb48ee`) ; https://github.com/FATHOM5CORP/oscal (commit `66d40d5`) ; https://github.com/tbusillo/nist-800-171-oscal (commit `5fc2ed3`)
- [S23] `mitre/hdf-libs` pull request #352, "docs(adr): add ADR-0014 OSCAL extension namespace, prose carriage and identity", merged 2026-09-21: https://github.com/mitre/hdf-libs/pull/352
