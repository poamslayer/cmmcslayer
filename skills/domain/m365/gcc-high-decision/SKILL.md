---
name: gcc-high-decision
description: Decide whether a client needs a GCC High tenant or can stay on Commercial or GCC, and record why. Runs the export-control question first, checks foreign ownership and control, catches the brand-name trap on named vendor products, prices the decision honestly, lists what breaks in GCC High, and applies the FedRAMP Moderate Equivalency test. Use when choosing a Microsoft 365 tenant type, or when a client asks "do we need GCC High."
vault_sources:
  - "Export Controls and CUI"
  - "CRM Systems and CUI"
  - "Client Onboarding Checklist"
  - "Client Onboarding Discovery Checklist"
  - "Practitioner insights A"
  - "Practitioner insights B"
  - "AEC Industry and CMMC"
  - "3.3.1"
  - "3.8.9"
  - "raw/CMMC-FAQs-v2.3-May-2026.md"
public_sources:
  - "CMMC FAQ E-A1, FedRAMP Moderate Equivalency memo, DoD CIO: https://dodcio.defense.gov/Portals/0/Documents/Library/FEDRAMP-EquivalencyCloudServiceProviders.pdf"
  - "CMMC FAQ E-A2: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "reddit.com/r/NISTControls: https://reddit.com/r/NISTControls/comments/pza6rh/_/hf0odxj/"
  - "reddit.com/r/NISTControls: https://reddit.com/r/NISTControls/comments/kf02ft/_/gg5n41f/"
  - "Salesforce FedRAMP Marketplace listing: https://www.fedramp.gov/marketplace/products/FR2003061248/"
  - "Salesforce Compliance, Einstein in Government Cloud: https://help.salesforce.com/apex/HTViewHelpDoc?id=sf.einstein_sales_considerations.htm"
---

# GCC High decision

This skill decides whether a client's Microsoft 365 tenant needs to be GCC High, can stay on GCC, or can stay on Commercial, and it writes down the reasoning so the decision survives staff turnover and a later assessor's questions. It does not configure the tenant and it does not decide CMMC scope on its own; it feeds `enclave-or-enterprise-decision` and the tenant ADR at the scope stage of the main flow, and it starts from the ITAR and EAR answer taken at `find-cui` intake. It refuses to let price open the conversation. Price is a real constraint and this skill prices the decision honestly, but it is never the test that decides the tenant.

## Inputs

- The contract clause list from the client's active contracts (DFARS 252.204-7012, 7019, 7020, 252.204-7021), so the export-control answer can be checked against what the contracts actually say rather than what the client assumes.
- `scope/data-flow.md` if it already exists, since CUI that has not been mapped yet cannot be checked against export-control authorities.
- The client's current vendor and SaaS list, including the exact SKU or plan name for each cloud product that will sit inside the boundary, not just the vendor name.
- Ownership and governance information: who owns the company, whether a foreign parent or foreign investor has a governance role, and who currently administers the M365 tenant.

## Method

1. **Ask the export-control question before recommending anything, and let the answer drive the decision, not price.** Ask two things in the same breath: does the client currently hold ITAR data, EAR data, or any other information that a foreign national cannot see, and is that likely to become true within the planning horizon even if it is not true today. A confirmed or plausible yes is the strongest single signal toward GCC High, because Commercial and GCC tenants cannot solve the deemed-export problem: a foreign-national Microsoft support technician working a ticket on a Commercial tenant is itself a release of ITAR technical data under 22 CFR 120.56. Get this answer in the first meeting, before touching cost, licensing, or vendor conversations. A recommendation built around monthly spend instead of this answer gets the order of operations backward and has to be redone once the export-control fact surfaces later.

2. **Check foreign ownership, control, or influence (FOCI), and who actually administers the tenant.** Ask who owns the company, whether any foreign investor or foreign parent holds governance rights, and whether a foreign-based administrator, reseller, or parent entity currently manages the M365 environment. A foreign-administered commercial tenant surfaces both an export-control problem and a FOCI problem at the same time, and either one can independently push the client toward GCC High or toward a structural fix, such as standing up a US-based subsidiary to hold and administer the authorized tenant.

3. **Apply the brand-name trap test to every vendor product being considered inside the boundary.** A vendor's appearance on the FedRAMP Marketplace certifies one specific cloud offering, not the vendor's whole product line, and not the specific tenant or plan the client already purchased. Verify the exact SKU, not the logo, using this table:

   | Vendor | Commercial or unauthorized offering | Authorized offering to verify | What to check |
   |---|---|---|---|
   | Microsoft | Commercial, GCC | GCC High | Tenant type on the admin center, not the marketing name of the licenses purchased |
   | Salesforce | Commercial Sales Cloud | Government Cloud Plus | FedRAMP Marketplace listing for the specific product, plus whether Einstein or its activity-capture add-on are in use, since neither one runs on either government offering |
   | Autodesk | Commercial cloud products | FedRAMP Moderate authorized products on AWS GovCloud | Which specific products carry the authorization; historically several Autodesk cloud products were feature-reduced relative to commercial, and the authorized set has changed over time, so re-verify rather than relying on a prior engagement's answer |
   | Bluebeam | Commercial cloud | None as of the last check | Confirm current FedRAMP status before assuming a cloud path exists; an on-prem fallback may still be required |

   Never accept "we use [vendor]'s government product" as verified without seeing the tenant, the SKU, or the FedRAMP Marketplace entry yourself. The client's own belief that they bought the authorized offering is not evidence that they did.

4. **Price the decision honestly, and separate the licensing pass-through from the doubled-answering-surface cost.** Two distinct costs stack on a GCC High decision, and both belong in the client conversation, not just the first one:
   - **Licensing pass-through**: GCC High seats and any GCC High-only add-ons typically cost more per user than their Commercial equivalents, and this is a real, recurring number to quote.
   - **The doubled requirement-answering surface**: moving to GCC High does not remove the on-premises environment from scope. Every one of the 110 requirements still has to be answered for whatever stays on-prem, in addition to being answered for the cloud tenant. A client who expects GCC High to shrink their assessment burden to "just the cloud part" has the wrong mental model, and correcting it now avoids a much worse conversation at assessment time.
   Quote both costs together so the client is deciding with the real total, not the license line alone.

5. **Enumerate what breaks or changes in GCC High before the client commits, using the client's actual tool stack.** Known breakage to check against the client's environment:
   - Salesforce's Einstein features, including the add-on that syncs a mailbox into the CRM automatically, do not run on either government offering. A client relying on that automatic sync loses it the moment they move to the authorized instance.
   - Defender/Intune device logs that feed a commercial-tenant Sentinel deployment do not ingest the same way once the tenant moves to GCC High; check the client's SIEM pipeline for a dependency on this path before assuming it carries over unchanged.
   - Native Microsoft 365 Backup availability differs between GCC/GCC High and Commercial; do not assume a backup product the client already uses will be available or licensed the same way post-migration.
   - Several vendors sell a "Federal" or "Government" SKU of a product that never touches CUI. Paying for the federal SKU on a Security Protection Asset that has no CUI exposure is spend without a compliance reason; check each vendor's SKU decision against whether the asset actually needs it.
   Build this list with the client's actual vendor stack in hand, not from memory; the specific breakage changes as vendors update their government offerings.

6. **Apply the FedRAMP Moderate Equivalency test to any cloud product staying off GCC High while still touching CUI.** Under DFARS 252.204-7012, a cloud service provider that processes, stores, or transmits CUI must meet the FedRAMP Moderate baseline, either through FedRAMP Moderate authorization itself or through the DoD's published equivalency path. A vendor's verbal or marketing claim of "FedRAMP Moderate equivalent" is not evidence. Ask for the system security plan behind that claim. In practice this document essentially never materializes; treat "equivalent" claims as unverified until an SSP is actually produced, and plan the architecture as if it will not be. This test also settles encryption questions: a non-FedRAMP-Moderate cloud service cannot store CUI even if the data is encrypted, because the equivalency requirement is not satisfied by encryption alone.

7. **Write the decision down with the export-control finding that drove it, before moving on to configuration.** The tenant decision is not final until it is recorded as an ADR (Output below). Do not let the engagement proceed to Exchange, DLP, or endpoint configuration work on an undocumented tenant decision; a later reviewer, including an assessor, needs to see why GCC High was or was not chosen without having to reconstruct the reasoning from memory.

## Output

Write `docs/adr/<next-number>-tenant-decision.md` in the engagement repo.

```markdown
# ADR-<NNNN>: Microsoft 365 tenant decision for <client>

Date: <date>. Status: accepted.

## Context

<Summary of the client's data, contracts, and current tenant type.>

## Export-control finding

- ITAR or EAR data present or expected: <yes / no / expected within N months>
- Basis: <contract clause review, interview answer, data flow finding>

## Foreign ownership and administration finding

- FOCI present: <yes / no / details>
- Current tenant administrator: <internal / MSP / foreign-based reseller>

## Decision

Tenant type: <Commercial / GCC / GCC High>

Driven by: <export-control finding, FOCI finding, or both>

## Brand-name verification

| Vendor | SKU verified | Evidence |
|---|---|---|
| | | |

## Cost

| Item | Amount |
|---|---|
| Licensing pass-through, annual | |
| Known breakage requiring a workaround or replacement | |

## What breaks and the plan for each

| Capability | Breaks in GCC High? | Client's plan |
|---|---|---|
| | | |

## FedRAMP Moderate Equivalency claims relied on

| Product | Claim | SSP obtained? |
|---|---|---|

## Consequences

<What this locks in, and what it costs to reverse later.>
```

## Where practitioners disagree

- Whether a "nonclave," a CUI-capable environment built small and cheap mainly to produce an SPRS score for a client that does not expect to actually handle CUI, is a defensible strategy or a trap that becomes noncompliant the first time real CUI shows up in the everyday environment instead. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: ask the export-control and FOCI questions in the qualification meeting, before any licensing conversation, so a client cannot anchor the whole engagement on price. Bring the brand-name verification table to every vendor conversation; clients routinely believe they already bought the authorized offering. **OSC seat**: if you are answering these questions internally, get the ITAR/EAR answer from whoever owns contracts or engineering, not from IT, since IT usually does not know the export classification of what the company builds.

## Sources

- CMMC FAQ E-A1, FedRAMP Moderate Equivalency memo, DoD CIO: https://dodcio.defense.gov/Portals/0/Documents/Library/FEDRAMP-EquivalencyCloudServiceProviders.pdf (the equivalency path under DFARS 252.204-7012).
- CMMC FAQ E-A2, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (a non-FedRAMP-Moderate cloud service cannot store CUI even when it is encrypted).
- Reddit, r/NISTControls: https://reddit.com/r/NISTControls/comments/pza6rh/_/hf0odxj/ (FedRAMP Moderate equivalency claims without a produced SSP).
- Reddit, r/NISTControls: https://reddit.com/r/NISTControls/comments/kf02ft/_/gg5n41f/ (GCC High requires answering every requirement for both the cloud tenant and on-premises resources).
- Salesforce FedRAMP Marketplace listing: https://www.fedramp.gov/marketplace/products/FR2003061248/ (the authorized Government Cloud Plus offering, as distinct from commercial Salesforce).
- Salesforce Help, Einstein in Government Cloud: https://help.salesforce.com/apex/HTViewHelpDoc?id=sf.einstein_sales_considerations.htm (Einstein and Einstein Activity Capture unsupported in Government Cloud and Government Cloud Plus).
- Practitioner consensus, unattributed, backs the brand-name trap as a general pattern across vendors beyond Salesforce, the Intune-to-Sentinel ingestion gap in GCC High, the native Microsoft 365 Backup availability difference between tenant types, and the caution against paying for a vendor's federal SKU on an asset that never touches CUI.
