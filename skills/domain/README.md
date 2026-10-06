# domain

The judgment layer, derived from a private practitioner wiki under `docs/adr/0001-source-policy.md`. One folder per skill, grouped by engagement phase. Every `SKILL.md` lists `vault_sources` in frontmatter.

| Phase | Skills |
|---|---|
| cui | cui-determination-workflow, cui-re-use-triage, cui-data-flow-mapping, cui-marking-check, export-control-overlay, flowdown-level-determination |
| scoping | cmmc-scope-boundary, logical-separation-test, endpoint-and-vdi-scoping, printer-and-ot-asset-scoping, esp-and-msp-scoping, enclave-or-enterprise-decision, significant-change-determination |
| gap | requirement-applicability-matrix, normative-requirement-test, control-evidence-lookup (plus 110 control files), over-engineering-guard, sprs-score-and-poam-eligibility |
| ssp-poam | ssp-statement-writer, poam-or-opa-router |
| evidence | evidence-package-builder |
| assessment | top-failed-requirements-drill, c3pao-selection-vetting, mock-assessment-runbook |
| m365 | gcc-high-decision, exchange-dlp-enclave-pattern, fips-crypto-scoping |
| policy | policy-after-procedure-sequencing, supplier-cui-release-procedure |
| engagement | cmmc-regulatory-status-brief |
