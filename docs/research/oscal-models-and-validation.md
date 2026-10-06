# OSCAL models, scope, and validation for scoping output

Provenance: researched 2026-09-28 for issue #65 ("Generate OSCAL components during scoping"). Questions: which OSCAL model scoping should produce (component definition or SSP `system-implementation`), where "out of scope" lives, how leveraged authorizations and inheritance are shaped, which serialization to use, which validators this repo can run, and how to keep UUIDs stable when agents regenerate files. Checked against `usnistgov/OSCAL` tag `v1.2.3`. Companion note: `docs/research/oscal-800-171-catalogs.md` covers which catalog the SSP would import.

## Answer

- **Q1, which model.** Scoping should write the SSP's `system-implementation` (components, inventory items, users, leveraged authorizations) plus the boundary text in `system-characteristics`. The component definition model is for vendors, in-house capability owners, and policy owners who publish reusable descriptions of a product or service for many systems to consume [S3]. An SSP cannot import a component definition: the SSP root has `import-profile` and nothing else to import, and `import-component-definitions` exists only inside a component definition [S1a, S1b]. An SSP component points back at its source with a `link` whose `rel` is `imported-from` [S1c], and the component's UUID may be reused ("SSPs may also reference identifiers from a component definitions through its implementation of links") [S5]. One component can back many inventory items: each `inventory-item` lists `implemented-components` by `component-uuid` [S1c]. A small contractor needs only the SSP. A managed service provider serving many contractors is the party that would write a component definition.
- **Q2, out of scope.** OSCAL has no "out of scope" flag. The boundary is prose plus diagrams in `system-characteristics/authorization-boundary` (required), with optional `network-architecture` and `data-flow` [S1a]. A component can carry the OSCAL property `implementation-point` with the closed values `internal` ("implemented within the system boundary") or `external` ("implemented outside the system boundary") [S1c]. External components can be listed; NIST's own leveraging example lists the leveraged IaaS as a `type: system` component with `implementation-point: external` [S14]. A CMMC asset category such as "out of scope" or "Security Protection Asset" needs a property in our own namespace, because OSCAL-namespace property names are a closed list [S1c, S13].
- **Q3, leveraged authorizations.** `system-implementation/leveraged-authorizations[]` records the provider (`title`, `party-uuid`, `date-authorized`, optional link to its SSP). Components tie to it with the props `leveraged-authorization-uuid` and `inherited-uuid`. In `control-implementation`, a `by-component` carries `inherited[]` (with `provided-uuid`) and `satisfied[]` (with `responsibility-uuid`) that point at the provider SSP's `export/provided[]` and `export/responsibilities[]` [S1a, S14]. The `control-origination` prop takes `inherited`, `customer-configured`, `customer-provided`, and others [S1a]. This matches the CMMC ESP/CSP customer responsibility matrix, but the UUID cross-references only resolve if the provider publishes an OSCAL SSP, which a contractor using GCC High will not usually have.
- **Q4, format.** No format is canonical. The Metaschema modules are the single source, and XML, JSON, and YAML schemas and converters are generated from them [S1d, S7]. NIST says valid XML converts "without information loss" to JSON and back [S6]. YAML is validated with the JSON Schema [S8, S9]. Trestle reads and writes JSON and YAML only, not XML [S17]. oscal-cli reads and converts all three [S16]. Recommendation: JSON.
- **Q5, validation.** Three options. (a) The released JSON Schema with Python `jsonschema` checks structure, types, required fields, UUID v4/v5 pattern, and some inline enums. It fails out of the box because the token pattern uses `\p{L}`, which Python `re` rejects. It passes once those two escapes are rewritten. It misses every Metaschema constraint: dangling `component-uuid` references, duplicate UUIDs, and closed values such as `implementation-point` (tested below). (b) `oscal-cli`: Java 11 or newer, public domain (CC0), and the only tool that runs Metaschema constraints, which its own guide calls "experimental" [S16]. The NIST repo stopped at v1.0.3 (2024-02-02, OSCAL 1.1.2). The maintained fork `metaschema-framework/oscal-cli` v3.2.0 (tag commit 2026-05-14) bundles OSCAL 1.2.1 [S15, S16]. (c) `compliance-trestle` v5.1.0 (PyPI, 2026-09-02, Apache-2.0, Python 3.11 or newer, about 20 runtime dependencies) validates through generated pydantic models for OSCAL 1.2.1, plus its own duplicate-UUID, reference, and link checks. It does not run Metaschema constraints [S17].
- **Q6, UUIDs.** The Metaschema `uuid` type is "A version 4 or 5 Universally Unique Identifier", enforced by the pattern `[45]` in the version position, so v1, v7, and v8 fail [S12]. Object UUIDs have "per-subject" consistency: keep them across revisions unless the subject itself changes [S5, S1c]. The document's root UUID is different. NIST's model pages say it must be regenerated every time content changes, and `last-modified` updated with it [S3, S4]. For regenerated files, derive object UUIDs as UUIDv5 from an engagement namespace UUID plus a stable name (for example `component:m365-gcc-high`). RFC 9562 guarantees the same name in the same namespace yields the same UUID [S18]. That practice is this note's inference; NIST does not prescribe v5.

## 1. Component definition versus SSP `system-implementation`

### What each is for, and who writes it

| | Component definition | SSP `system-implementation` |
| --- | --- | --- |
| Root | `component-definition` | inside `system-security-plan` |
| Purpose | "a description of the controls that are supported in a given implementation of a hardware, software, service, policy, process, procedure, or compliance artifact" [S3] | "the system's deployment, including user roles, interconnections, services, and system inventory" [S4] |
| Authors | "Product and Service Vendors, Capability Owners, Policy and Process Owners, Standards Bodies, Validation Bodies" [S3] | "System Owners and System Security Plan Authors" [S4] |
| Consumers | SSP authors, who import "the relevant content into their system security plan" as "a starting point" [S3] | Assessors, authorizing officials, leveraging system owners [S4] |
| Required content | `metadata` only; `components`, `capabilities`, and `control-implementations` are optional [S1b] | `metadata`, `import-profile`, `system-characteristics`, `system-implementation` (at least one `component`), and `control-implementation` (at least one `implemented-requirement`) [S1a] |
| Component `status` | none | required, `state` in `under-development`, `operational`, `disposition`, `other` [S1c] |
| Implementation status per control | none. Trestle stores it in props because "the OSCAL schema doesn't include a form of implementation status for components in the component definition" [S17] | `by-component/implementation-status` [S1a] |
| Extra parts | `capability` groups components that together satisfy a control [S3] | `leveraged-authorizations`, `users`, `inventory-items` [S1a] |

### Can an SSP import a component definition?

No import mechanism exists. The SSP model imports only a profile (`import-profile`, required) [S1a]. `import-component-definition` ("Loads a component definition from another resource") is defined only in the component definition model, so one component definition can pull in another [S1b]. The identifier page lists the five import types (`import`, `import-component-definition`, `import-profile`, `import-ssp`, `import-ap`) [S5].

The SSP keeps lineage with a link instead. The component link `rel` list includes:

> `imported-from`: The hyperlink identifies a URI pointing to the `component` in a `component-definition` that originally defined the `component`. [S1c]

The SSP concept page describes this as "lineage from an SSP's implemented system component back to a relevant source of transferred content", and says referential integrity can be enforced only "if the component definition is resolvable" [S4]. The copy is by value: the SSP author copies the component into `system-implementation/components` and adds the SSP-only fields (`status`, `props` such as `implementation-point`). Trestle's `ssp-generate` and `ssp-assemble` automate this. They take a profile and an optional list of component definitions and build SSP markdown, then the SSP JSON. Without component definitions "the SSP will only have one component: `This System`" [S17].

Component definition UUIDs are declared `per-subject` for components and `change-on-write` for the document root [S1b]. An SSP component copied from a component definition can therefore keep the source component's UUID. NIST's identifier page says SSPs "may also reference identifiers from a component definitions through its implementation of links" [S5]. It does not say the SSP component must reuse the UUID.

### Components and inventory items

A component is a type of thing (a product, a service, a policy). An inventory item is one managed instance. The model says so directly: `inventory-item` is "A single managed inventory item within the system", and its `implemented-components` are "The set of components that are implemented in a given system inventory item" [S1c]. The relation runs from the inventory item to the component, so one component can back many inventory items, and one inventory item can implement several components (NIST's example logging server implements a software component and a policy component) [S14]:

```json
{
  "uuid": "c9c32657-a0eb-4cf2-b5c1-20928983063c",
  "description": "The logging server.",
  "props": [{ "name": "asset-id", "value": "asset-id-logging-server" }],
  "implemented-components": [
    { "component-uuid": "e00acdcf-911b-437d-a42f-b0b558cc4f03" },
    { "component-uuid": "795533ab-9427-4abe-820f-0b571bacfe6d" }
  ]
}
```

This matches the `to-ssp` rule that statements name component types, not machines. The laptop fleet is one component; each laptop, if listed at all, is an inventory item.

### When a small contractor would want which

- **SSP only (the normal case).** The contractor is the system owner. Scoping output feeds `system-characteristics` (boundary, data flow) and `system-implementation`. Later, `to-ssp` fills `control-implementation`.
- **Component definition.** Only when a party describes something reused across systems: an MSP or ESP describing its managed SOC service for all its clients, or a vendor describing a product. The contractor's engagement repo would consume it, not write it.
- **Both.** Only if the engagement wants its policy components (`type: policy`, `process-procedure`, `plan`) reusable across several enclaves of the same company. For one enclave this adds a file without adding information.

One constraint shapes the choice. A standalone SSP is only valid with an `import-profile` and at least one `implemented-requirement` that has a `by-component` [S1a]. A scoping-stage file therefore cannot be a complete, valid SSP on its own. Scoping would write either a fragment (`system-implementation` plus `system-characteristics`) that `to-ssp` merges, or a skeleton SSP whose `control-implementation` holds placeholders. A component definition is valid with metadata and components only [S1b]. That makes it tempting as a scoping container, but it cannot hold inventory items, users, the boundary, or leveraged authorizations.

## 2. Where "out of scope" lives

### Boundary constructs

`system-characteristics` requires `authorization-boundary` and allows `network-architecture` and `data-flow` [S1a]. Each has a required markup `description`, `props`, `links`, and `diagrams` (each diagram has a `caption` and links to an image in back matter). None of them lists components by UUID. The boundary is described in prose and pictures, not as a machine-readable member list.

### `implementation-point`

The component props list includes three names "related to inherited component": `implementation-point`, `leveraged-authorization-uuid`, `inherited-uuid` [S1c]. The values of `implementation-point` are a closed list (no `allow-other`, and the Metaschema default for `allow-other` is `no`) [S1c, S13]:

```xml
<enum value="internal">The component is implemented within the system boundary.</enum>
<enum value="external">The component is implemented outside the system boundary.</enum>
```

### Listing components outside the boundary

This is allowed and expected. The component type list has `system` ("An external system, which may be a leveraged system or the other side of an interconnection") and `interconnection` ("A connection to something outside this system") [S1c]. NIST's leveraging example lists the external IaaS as a component [S14]:

```json
{
  "uuid": "22222222-0000-4000-9001-000000000002",
  "type": "system",
  "title": " **LEVERAGED SYSTEM (IaaS)** ",
  "props": [
    { "name": "implementation-point", "value": "external" },
    { "name": "leveraged-authorization-uuid", "value": "22222222-0000-4000-9000-300000000001" },
    { "name": "inherited-uuid", "value": "11111111-0000-4000-9001-000000000001" }
  ],
  "status": { "state": "operational" }
}
```

`external` means "outside the boundary", not "out of CMMC scope". A GCC High tenant is external and still in scope as an ESP. The CMMC asset categories (CUI asset, Security Protection Asset, Contractor Risk Managed Asset, Specialized Asset, Out-of-Scope) have no OSCAL equivalent. They need a namespaced property. The property model has an optional `ns` ("must be a universal resource identifier") for this purpose [S11]. OSCAL-namespace property names on components are a closed list, so an un-namespaced `asset-category` would fail constraint validation. It still passes JSON Schema, which does not carry that list (see section 5).

The fragment below is this note's illustration, not a NIST example. It passed the v1.2.3 JSON Schema when wrapped in a minimal SSP. The `ns` URI is a placeholder the engagement would own.

```json
{
  "uuid": "61e6b11a-e10e-599b-93ed-9e19ff38813e",
  "type": "network",
  "title": "Shop floor CNC LAN",
  "description": "Air-gapped; no CUI.",
  "status": { "state": "operational" },
  "props": [
    { "name": "implementation-point", "value": "external" },
    { "ns": "https://example.org/ns/cmmc", "name": "asset-category", "value": "out-of-scope" }
  ]
}
```

`network` is in the v1.2.3 shared component type list, along with `region`, `zone`, and `resource-container` [S1c]. When each was added was not checked. The list allows other values (`allow-other="yes"`). NIST's own examples use `process`, `appliance`, and `application` [S14].

### FIPS verdicts

`scope/fips-verdicts.md` maps onto the validation pattern. The product component carries `links: [{rel: "validation", href: "#<uuid>"}]`, and a second component of `type: validation` carries `validation-type` (for example `fips-140-2`), `validation-reference` (the certificate number), and a `validation-details` link to the CMVP certificate [S10]. `validation-type` values are not enumerated in the metaschema [S1c].

## 3. Leveraged authorizations and inheritance

Shape in the leveraging (customer) SSP [S1a]:

- `system-implementation/leveraged-authorizations[]`: `uuid`, `title` (required), `party-uuid` (required, the party that manages the leveraged system), `date-authorized` (required), `props`, `links`, `remarks`. In v1.2.3 the link `rel` list names `system-security-plan` ("A reference to the system security plan for the leveraged authorization"). The href is either `#uuid` into back matter or an absolute URI.
- Components of the leveraged system carry `leveraged-authorization-uuid` (must match a `leveraged-authorization` in this SSP, enforced by an `index-has-key` constraint) and `inherited-uuid` ("UUID of the component as it was assigned in the leveraged system's SSP") [S1a, S1c].
- In `control-implementation/implemented-requirements[]/by-components[]` (or under `statements[]`):
  - `inherited[]`: `uuid`, optional `provided-uuid`, `description`, `responsible-roles`.
  - `satisfied[]`: `uuid`, optional `responsibility-uuid`, `description`, `responsible-roles`.
- `implemented-requirement` props may include `control-origination` with `organization`, `system-specific`, `customer-configured`, `customer-provided`, `inherited` [S1a].

Shape in the leveraged (provider) SSP: each `by-component` may carry one `export` with `provided[]` (what a customer may inherit) and `responsibilities[]` (what the customer must do, optionally tied to a `provided-uuid`). At least one of the two is required [S1a].

From NIST's paired examples [S14], the provider side:

```json
"export": {
  "provided": [{
    "uuid": "11111111-0000-4000-9009-002001001001",
    "description": "Consumer-appropriate description of what a leveraging system may inherit ..."
  }],
  "responsibilities": [{
    "uuid": "11111111-0000-4000-9009-002001001002",
    "provided-uuid": "11111111-0000-4000-9009-002001001001",
    "description": "Leveraging system's responsibilities with respect to inheriting this capability ..."
  }]
}
```

The customer side:

```json
{
  "component-uuid": "22222222-0000-4000-9001-000000000003",
  "uuid": "22222222-0000-4000-9009-002001003000",
  "description": "...",
  "inherited": [{ "uuid": "22222222-0000-4000-9009-002001002002",
                  "provided-uuid": "11111111-0000-4000-9009-002001002001",
                  "description": "Optional description." }],
  "satisfied": [{ "uuid": "22222222-0000-4000-9009-002001002003",
                  "responsibility-uuid": "11111111-0000-4000-9009-002001002002",
                  "description": "Description of how the responsibility was satisfied." }]
}
```

The SSP concept page says `@provided-uuid` must find "a single matching target provided control implementation statement ... in the leveraged SSP" [S4]. The SSP root declares a cross-document index that follows `leveraged-authorization/link[@rel='system-security-plan']/@href` into the leveraged SSP [S1a]. Only a Metaschema constraint engine (oscal-cli) can evaluate that.

**CMMC mapping.** The ESP or CSP maps to the leveraged system. Its customer responsibility matrix rows map to `provided` and `responsibilities`. The contractor's CRM response maps to `inherited` and `satisfied`. In practice the contractor has a PDF or spreadsheet CRM, not the provider's OSCAL SSP, so there are no `provided-uuid` targets to point at. Both `provided-uuid` and `responsibility-uuid` are optional (`required="no"`) [S1a]. The customer SSP can still record `inherited` and `satisfied` statements with descriptions and a link to the CRM document in back matter. What this loses is machine-checkable referential integrity to the provider.

FedRAMP context: the current FedRAMP rules say Rev5 packages are moving "to simplified JSON documents or (in some cases) optional OSCAL" [S19]. Do not assume a CSP will publish an OSCAL SSP for customers to reference. `GSA/fedramp-automation`, named as a source for this note, was not reachable (anonymous git and raw.githubusercontent.com both returned "not found" on 2026-09-28). Its FedRAMP-specific constraints and leveraged-authorization guidance were not checked [S20].

## 4. Format: JSON, YAML, or XML

- All three are first-class. Schemas and converters for every model are generated from the Metaschema sources in the release build [S1d]. The model status table lists XML, JSON, and YAML reference docs and "XML, JSON/YAML" schemas for every released model [S8].
- Round trip: "you have a valid OSCAL XML document, you can convert it without information loss into an equivalent OSCAL JSON document, and vice-versa" [S6]. JSON to YAML "is more straightforward and does not require 'OSCAL-awareness'" [S9]. XML to JSON needs the generated XSLT converters (release assets) or oscal-cli `convert` [S2, S16]. Markup fields (`markup-line`, `markup-multiline`) are Markdown in JSON and YAML and HTML-like elements in XML. That is why the XML to JSON conversion needs the model-aware converter.
- On conversion the document UUID and `last-modified` "should remain the same", so tools can tell the two files are equivalent [S3, S4].
- Tool support: oscal-cli reads, validates, and converts XML, JSON, and YAML [S16]. Trestle "natively supports only `json` and `yaml` formats" and points XML users to NIST's converters [S17]. Python's standard library has JSON built in but no YAML parser.

Recommendation for this repo: JSON. It needs no third-party parser, matches NIST's own `ajv` and JSON Schema path, and trestle and oscal-cli both accept it.

## 5. Validation tooling

### Release assets for v1.2.3

The GitHub release page and REST API were not reachable from this environment. The asset list below comes from the release workflow and Makefile at tag `v1.2.3` [S1d]. Each name was confirmed with an HTTP request to `https://github.com/usnistgov/OSCAL/releases/download/v1.2.3/<name>`, and all returned 200 on 2026-09-28 [S2]. For each model `M` in `assessment-plan`, `assessment-results`, `catalog`, `complete`, `component`, `mapping`, `poam`, `profile`, `ssp`:

- `oscal_M_schema.json` (JSON Schema, `"$schema": "http://json-schema.org/draft-07/schema#"`, `$id` `http://csrc.nist.gov/ns/oscal/1.2.3/oscal-ssp-schema.json` for SSP)
- `oscal_M_schema.xsd`
- `oscal_M_xml-to-json-converter.xsl`, `oscal_M_json-to-xml-converter.xsl`
- `oscal_M_metaschema_RESOLVED.xml`

Also resolved metaschemas for the non-root modules (for example `oscal_metadata_metaschema_RESOLVED.xml` and `oscal_implementation-common_metaschema_RESOLVED.xml`, both confirmed), and the bundles `oscal-1.2.3.zip` and `oscal-1.2.3.tar.bz2`. The workflow uploads `build/generated/oscal*` and creates the release as a draft that a maintainer publishes [S1d]. So the published list could in principle differ from the build output; the names above were all confirmed present. Since v1.1.0, "build artifacts (schemas, converters) are now distributed as part of a release and are no longer tracked within the OSCAL Git repository" [S7].

### Option A: plain Python plus `jsonschema`

Tested on 2026-09-28 with `jsonschema` 4.26.0 on Python 3.11, against `oscal_ssp_schema.json` and `oscal_component_schema.json` from v1.2.3, using NIST's examples [S14] and targeted mutations.

1. **Out of the box it throws.** The schema's token pattern is `^(\p{L}|_)(\p{L}|\p{N}|[.\-_])*$`. Python's `re` rejects `\p` ("bad escape \p at position 2"), so validation of any SSP or component definition raises before reporting anything. Each schema has two `\p{L}` and one `\p{N}`.
2. **Workaround.** Before loading, rewrite `\p{L}` to `[^\W\d_]` and `\p{N}` to `\d`. These are Unicode-aware in Python 3 `str` patterns and are close to, though not exactly, the Unicode categories. After the rewrite, NIST's `ssp-example.json`, both leveraging and leveraged examples, and `example-component-definition.json` validate with zero errors. The third-party `regex` module understands `\p{L}`, but `jsonschema` does not use it by default. Not tested.

   ```python
   text = open("oscal_ssp_schema.json").read()
   text = text.replace(r"\\p{L}", r"[^\\W\\d_]").replace(r"\\p{N}", r"\\d")
   schema = json.loads(text)
   Draft7Validator(schema).iter_errors(doc)
   ```

   Format checks (`date-time`, `uri`, `uri-reference`, `email`) only run when a `FormatChecker` is passed. For `uri` and `date-time`, they also need optional packages installed with `jsonschema`. Without them those formats pass silently. This is `jsonschema` behaviour, not OSCAL's, and was not re-verified here beyond noting that no format errors appeared.

3. **What it catches and misses** (mutations of `ssp-example.json`):

   | Mutation | JSON Schema result | Why |
   | --- | --- | --- |
   | Missing `authorization-boundary` | error | `required` |
   | Unknown property on a component | error | `additionalProperties: false` |
   | Component UUID `...-1000-...` (v1) | error | UUID pattern allows only v4 or v5 |
   | Component `status.state: "done"` | error | inline enum |
   | `by-component.component-uuid` pointing at no component | **passes** | reference integrity is a Metaschema `index-has-key` constraint |
   | Two components with the same UUID | **passes** | `index` / `is-unique` constraint |
   | `implementation-point: "outside"` | **passes** | allowed-values on a prop value, constraint only |
   | Component `type: "laptop"` | passes (correct) | type list has `allow-other="yes"` |
   | `implementation-status.state: "finished"` | passes (correct) | `allow-other="yes"` |

   NIST says the same thing: "Additional constraints are imposed on the OSCAL models that are not representable within the JSON and XML schemas. These constraints can be validated using downstream tools, such as the OSCAL CLI" [S7]. What Option A misses are the checks a generator most often breaks: UUID references, uniqueness, closed prop values, the `leveraged-authorization-uuid` index, and the "at least one `by-component`" cardinality rule [S1a, S1c]. A repo script could add its own checks for the handful that matter to scoping: every `component-uuid` and `leveraged-authorization-uuid` resolves, no duplicate UUIDs, `implementation-point` in {internal, external}. That is a small amount of Python.

### Option B: oscal-cli (Java)

- **NIST repo** `usnistgov/oscal-cli`: last tag `v1.0.3`, commit `5cfe61c`, 2024-02-02. Depends on `liboscal-java` 3.0.3, which pins the OSCAL submodule to `v1.1.2` [S15]. It predates OSCAL 1.2, so any value added to the models after 1.1.2 would be unknown to it. Which v1.2.3 values those are was not checked. NIST's tools page still links this repo and marks "OSCAL Java CLI" as Active [S9].
- **Maintained fork** `metaschema-framework/oscal-cli`: latest tag `v3.2.0`, commit `f0fb6d8`, 2026-05-14. It says it is "maintained to be feature compatible with the NIST v1.0.3 release" and "supports newer releases of the OSCAL models" [S16]. It depends on `liboscal-java` 7.2.0, which pins OSCAL `v1.2.1`, not v1.2.3 [S16]. Install is a zip from Maven Central (`dev.metaschema.oscal:oscal-cli-enhanced`), or `docker pull ghcr.io/metaschema-framework/oscal-cli:latest`. It is built for Java 11 (`maven.compiler.release` 11). License: CC0 public domain dedication [S16].
- **What it checks**: well-formedness, schema compliance, and "Constraint validation: Metaschema-defined validation rules that express business logic beyond basic schema requirements". The guide labels full validation "(experimental)" [S16]. It also bundles extra "OSCAL Enhancements" constraints (unique props, links, and responsible parties per location) [S16]. Exit code 0 on pass, 1 on fail [S16].
- **Footprint for this repo**: a JVM plus a zip, or Docker. It does not fit the repo's "plain Python 3" tooling rule. It could be an optional check, the same way `check_links.py` stays outside `verify.sh`.

### Option C: compliance-trestle (Python)

- Repository moved from `IBM/compliance-trestle` to `oscal-compass/compliance-trestle`. The old URL still resolves. Latest tag `v5.1.0`, commit `94a2caa`, 2026-09-02. PyPI `compliance-trestle` 5.1.0, license `Apache-2.0`, `requires_python >=3.11` [S17].
- Runtime dependencies include `pydantic[email]>=2.11`, `ruamel-yaml`, `cryptography`, `paramiko==5.0.0`, `openpyxl`, `jinja2==3.1.6`, `securesystemslib`, and about a dozen more [S17]. That is heavy for a repo whose checks are standard-library Python.
- OSCAL version: `OSCAL_VERSION = '1.2.1'` in `trestle/oscal/__init__.py` [S17]. Models are generated from the OSCAL JSON Schemas with `datamodel-code-generator` [S17].
- `trestle validate` modes: `duplicates` ("no duplicate uuids and param_ids"), `refs` ("all references in responsible parties are found in roles"), `links` ("uuids in links and prose match resources in backmatter"), `catalog` (unique param ids), `rules`, and `all` [S17]. It does not evaluate Metaschema constraints, so a dangling `by-component.component-uuid` or a bad `implementation-point` value is not among the listed checks. Not tested here.
- Useful beyond validation: `trestle author ssp-generate` / `ssp-assemble` (component definitions plus markdown into an SSP) and `ssp-generate --leveraged-ssp` for an inheritance view [S17].

### Others

- NIST's own guidance validates with `ajv` (Node) for JSON and YAML, and `xmllint` for XML [S7, S1e]. `ajv` supports `\p{L}` through JavaScript Unicode regexes, which is presumably why the schemas use it. That is an inference and was not tested.
- NIST's tools page points to the community list `oscal-club/awesome-oscal` for others [S9]. Not surveyed.

## 6. UUIDs

- **Version.** Metaschema defines `uuid` as "A version 4 or 5 Universally Unique Identifier (UUID) as defined by RFC4122", with JSON pattern `^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[45][0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$` [S12]. The v1.2.3 SSP schema carries the same pattern (confirmed in the downloaded schema). v7 (time-ordered) and v8 UUIDs are rejected. RFC 4122 is obsoleted by RFC 9562 [S18].
- **Object UUIDs are stable.** "Identifier (value) must be managed across revisions of the same document. In general, OSCAL identifiers have per-subject consistency. They should only be changed if the underlying identified subject has changed in a significant way that no longer represents the same identified subject" [S5]. Every component, inventory item, user, leveraged authorization, `by-component`, `inherited`, and `satisfied` UUID carries the same "should be assigned per-subject" text [S1a, S1c].
- **The document UUID changes.** "Every time the content of an OSCAL file changes ... A new UUID value must be generated and assigned to the root element's `uuid`" and `last-modified` must be updated. "This document level UUID is the only UUID in OSCAL associated with version control" [S3, S4]. The component definition metaschema marks its root UUID `identifier-persistence: change-on-write` and component UUIDs `per-subject` [S1b]. See Open questions for a conflict in the SSP metaschema text.
- **Practice for regenerated files.** Two workable approaches:
  1. **Read-back.** Before writing, parse the existing OSCAL file and reuse the UUID of each object matched by a natural key (asset ID, component title slug). Mint v4 only for new objects. Trestle does this with markdown: its `-assemble` tools write only when content changed, and UUIDs are regenerated only on request [S17].
  2. **Name-based v5.** Store one random namespace UUID per engagement (for example in the engagement's `CONTEXT.md` or a small JSON file). Derive each object UUID as `uuid5(namespace, "<kind>:<stable-key>")`. RFC 9562: "UUIDs generated at different times from the same name (using the same canonical format) in the same namespace MUST be equal" [S18]. Python's standard library `uuid.uuid5` does this, and OSCAL accepts v5 [S12]. Example: namespace `6f1c2a9e-3b7d-4e21-9a0c-5d8e7f3b1c42` with name `component:m365-gcc-high` gives `63402ab1-2a3d-55da-b8c6-4cf30584da47` every time.

  Approach 2 suits agents that regenerate a file from Markdown without reading the old JSON. The cost is that the stable key must be really stable: renaming the key mints a new identity, which OSCAL treats as a new subject. RFC 9562 notes that SHA-1 may be disallowed by some policies, and says SHA-256 name-based UUIDs must be v8 [S18]. OSCAL does not accept v8, so v5 is the only name-based option. The document root UUID should still be a fresh v4 on each content change, per [S3, S4].

## Open questions

- **SSP root UUID persistence conflict.** The SSP metaschema's description of `system-security-plan/@uuid` says it "should be assigned per-subject ... consistently used to identify the same subject across revisions" [S1a]. NIST's SSP concept page says the root UUID must change on every content change [S4]. The component definition metaschema resolves this for its own root as `change-on-write` [S1b]. Which rule to follow for the SSP root is not settled by the sources. This note follows the concept page.
- **Which catalog `import-profile` points at.** An SSP must import a profile or catalog. NIST publishes no Rev 2 OSCAL catalog (see `docs/research/oscal-800-171-catalogs.md`). Component definition `control-implementation` also requires a `source` catalog or profile [S1b].
- **Validator OSCAL version lag.** Both maintained validators pin OSCAL 1.2.1 (oscal-cli v3.2.0 through liboscal-java 7.2.0; trestle 5.1.0). The latest release is 1.2.3. Whether they accept `oscal-version: 1.2.3` documents, or 1.2.3-only values, was not tested.
- **oscal-cli constraint coverage.** The guide labels constraint validation experimental [S16]. Whether it evaluates the cross-document index into a leveraged SSP was not tested.
- **FedRAMP sources.** `GSA/fedramp-automation` was unreachable [S20]. FedRAMP's current direction on OSCAL was read only from `FedRAMP/2026-markdown` [S19].
- **GitHub release page.** The asset list is reconstructed from the build files and confirmed by name, not read from the release page, which returned 403 from this environment [S2].
- **Trestle validation depth.** Trestle's validators were read, not run. Whether pydantic model validation enforces the UUID v4/v5 pattern and the inline enums was not confirmed.

## Sources

- [S1] `usnistgov/OSCAL`, tag `v1.2.3` (tag object `a504f40be661d4c1758e753643b0164978a9c2f1`, commit `e061961c7702afeabffdf5e59894d35e748dade1`, 2026-08-06):
  - [S1a] SSP metaschema: https://github.com/usnistgov/OSCAL/blob/v1.2.3/src/metaschema/oscal_ssp_metaschema.xml
  - [S1b] Component definition metaschema: https://github.com/usnistgov/OSCAL/blob/v1.2.3/src/metaschema/oscal_component_metaschema.xml
  - [S1c] Implementation-common metaschema and shared constraints: https://github.com/usnistgov/OSCAL/blob/v1.2.3/src/metaschema/oscal_implementation-common_metaschema.xml ; https://github.com/usnistgov/OSCAL/tree/v1.2.3/src/metaschema/shared-constraints
  - [S1d] Release workflow and build Makefile: https://github.com/usnistgov/OSCAL/blob/v1.2.3/.github/workflows/release.yml ; https://github.com/usnistgov/OSCAL/blob/v1.2.3/build/Makefile
  - [S1e] https://github.com/usnistgov/OSCAL/blob/v1.2.3/README_validations.md
- [S2] OSCAL v1.2.3 release assets (fetched by name): https://github.com/usnistgov/OSCAL/releases/download/v1.2.3/oscal_ssp_schema.json ; https://github.com/usnistgov/OSCAL/releases/download/v1.2.3/oscal_component_schema.json ; https://github.com/usnistgov/OSCAL/releases/download/v1.2.3/oscal-1.2.3.zip ; release page (not reachable here): https://github.com/usnistgov/OSCAL/releases/tag/v1.2.3
- [S3] OSCAL component definition model concepts: https://pages.nist.gov/OSCAL/learn/concepts/layer/implementation/component-definition/
- [S4] OSCAL SSP model concepts: https://pages.nist.gov/OSCAL/learn/concepts/layer/implementation/ssp/
- [S5] Identifier use and UUIDs: https://pages.nist.gov/OSCAL/learn/concepts/identifier-use/
- [S6] Well-formed data formats and valid OSCAL: https://pages.nist.gov/OSCAL/learn/concepts/validation/
- [S7] Testing new OSCAL releases: https://pages.nist.gov/OSCAL/learn/tutorials/general/releases/
- [S8] OSCAL layers and models (status table): https://pages.nist.gov/OSCAL/learn/concepts/layer/
- [S9] OSCAL tools: https://pages.nist.gov/OSCAL/resources/tools/
- [S10] Representing test validation information: https://pages.nist.gov/OSCAL/learn/tutorials/implementation/validation-modeling/
- [S11] Extending OSCAL models with props and links: https://pages.nist.gov/OSCAL/learn/tutorials/general/extension/
- [S12] Metaschema data types (`uuid`): https://pages.nist.gov/metaschema/specification/datatypes/
- [S13] Metaschema constraints (`allowed-values`, `allow-other` default `no`): https://pages.nist.gov/metaschema/specification/syntax/constraints/
- [S14] `usnistgov/oscal-content`, commit `78650f02ad9321bb7b817846f8fbd4f2bcd620de` (2026-05-13): https://github.com/usnistgov/oscal-content/tree/78650f02ad9321bb7b817846f8fbd4f2bcd620de/examples/ssp/json (`ssp-example.json`, `oscal_leveraging-example_ssp.json`, `oscal_leveraged-example_ssp.json`) ; https://github.com/usnistgov/oscal-content/tree/78650f02ad9321bb7b817846f8fbd4f2bcd620de/examples/component-definition/json
- [S15] `usnistgov/oscal-cli`, tag `v1.0.3`, commit `5cfe61c695f598f1b4240aa39313bade4397cbeb` (2024-02-02): https://github.com/usnistgov/oscal-cli/tree/v1.0.3 ; `usnistgov/liboscal-java` tag `v3.0.3` (OSCAL submodule at `4f02dac6f698efda387cc5f55bc99581eaf494b6`, tag `v1.1.2`): https://github.com/usnistgov/liboscal-java/tree/v3.0.3
- [S16] `metaschema-framework/oscal-cli`, tag `v3.2.0`, commit `f0fb6d88aee55eccf1ff6bce5d4f17235aed01a4` (2026-05-14): https://github.com/metaschema-framework/oscal-cli/tree/v3.2.0 ; validation guide: https://github.com/metaschema-framework/oscal-cli/blob/v3.2.0/src/site/markdown/guides/validating-oscal.md.vm ; CLI reference: https://github.com/metaschema-framework/oscal-cli/blob/v3.2.0/src/site/markdown/guides/cli-reference.md.vm ; `metaschema-framework/liboscal-java` tag `v7.2.0` (OSCAL submodule at `26df0501ccbd8cf0dad2a5f06f5f8e6237e2cd94`, tag `v1.2.1`), external constraints: https://github.com/metaschema-framework/liboscal-java/blob/v7.2.0/src/main/metaschema-constraints/oscal-external-constraints.xml ; Maven Central: https://central.sonatype.com/artifact/dev.metaschema.oscal/oscal-cli-enhanced/
- [S17] `oscal-compass/compliance-trestle` (formerly `IBM/compliance-trestle`), tag `v5.1.0`, commit `94a2caaf67568109b0df43a6b7d9c2e7bd9041a8` (2026-09-02): https://github.com/oscal-compass/compliance-trestle/tree/v5.1.0 ; file formats: https://github.com/oscal-compass/compliance-trestle/blob/v5.1.0/docs/index.md ; SSP authoring: https://github.com/oscal-compass/compliance-trestle/blob/v5.1.0/docs/tutorials/Trestle_authoring/ssp_profile_catalog_authoring.md ; validators: https://github.com/oscal-compass/compliance-trestle/tree/v5.1.0/trestle/core ; PyPI metadata: https://pypi.org/pypi/compliance-trestle/json
- [S18] RFC 9562, Universally Unique IDentifiers (obsoletes RFC 4122), sections 5.5 and 6.5: https://www.rfc-editor.org/rfc/rfc9562.txt
- [S19] `FedRAMP/2026-markdown`, commit `2f81e380a6615d48927a72c5007df785c038f891` (2026-09-23): https://github.com/FedRAMP/2026-markdown/blob/2f81e380a6615d48927a72c5007df785c038f891/providers/updating/changes.md ; https://github.com/FedRAMP/2026-markdown/blob/2f81e380a6615d48927a72c5007df785c038f891/agencies/rules/agency-use.md ; `FedRAMP/docs` README (marked "Historical reference only"), commit `ed5e17f7c69a99a2511a93655353224b23bcf72e`: https://github.com/FedRAMP/docs
- [S20] `GSA/fedramp-automation` (not reachable on 2026-09-28; anonymous git asked for credentials and raw.githubusercontent.com returned 404): https://github.com/GSA/fedramp-automation
- [S21] Test harness: `jsonschema` 4.26.0 from PyPI (https://pypi.org/project/jsonschema/), Python 3.11, run in a scratch virtual environment. No repository file was changed.
