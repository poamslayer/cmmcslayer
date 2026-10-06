> **Provenance.** Written for this repo (MIT). The fields of the engagement's SSP, the Markdown record of ADR-0012, and the values each may take. The asset categories and the kinds of Specialized Asset are the terms of 32 CFR 170.19 (https://www.ecfr.gov/current/title-32/section-170.19); the provider roles and FedRAMP statuses are the glossary's, in `CONTEXT.md`. Nothing here derives from a private source. Scribe's check, `skills/flows/scribe/check_ssp.py`, is the authority; this table is a summary of it, and replaces the field table of the OSCAL record it superseded.

# The SSP's fields

| Field | Where it appears | Values |
|---|---|---|
| `category` | an asset under a component's `assets` (required, unless the component gives one); a component (only when every asset behind it shares the category) | `cui-asset`, `security-protection-asset`, `contractor-risk-managed-asset`, `specialized-asset`, `out-of-scope-asset` |
| `kind` | an asset, required where its category is `specialized-asset` and allowed nowhere else | `iot`, `iiot`, `ot`, `gfe`, `restricted-information-system`, `test-equipment` |
| `justification` | an asset, required where its category is `out-of-scope-asset` and allowed nowhere else | why it cannot process, store, or transmit CUI |
| `provider.role` | a component, once. Every value is an ESP; `csp` marks the cloud ones | `csp`, `msp`, `mssp`, `soc`, `rmm`, `other-esp` |
| `provider.fedramp-status` | a component whose role is `csp`, where it is required | `fedramp-moderate-authorized`, `fedramp-moderate-equivalent`, `none` |
| `provider.date-authorized` | a component whose FedRAMP status is `fedramp-moderate-authorized`, where it is required | the date of its FedRAMP Marketplace listing, `YYYY-MM-DD` |
| `status` | a statement under an objective in `ssp/<requirement>.md` | `implemented`, `partial`, `planned`, `alternative`, `not-applicable` |
| `remarks` | a statement, required where its status is `alternative` or `not-applicable`; also a component or an asset | the reason, or any note |

A statement's `component` is a component's slug, the name of its file under `ssp/components/`, or `this-system`, the placeholder, which is only ever planned with "Not yet written." (ADR-0011).
