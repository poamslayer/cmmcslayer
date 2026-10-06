---
name: esp-and-msp-scoping
description: Place an MSP, MSSP, RMM, backup provider, SOC, or SaaS vendor in the CMMC Assessment Scope. Runs the account test first, finds the providers behind the provider, scopes remote tooling by feature, applies the CSP versus ESP fork, and records each provider with its role and FedRAMP status, and its tools as assets, in the SSP through scribe, which generates the responsibility matrix. Use whenever an outside party has access to, or holds data from, the environment.
vault_sources:
  - "MSP Scoping and Access Model"
  - "CMMC Scoping"
  - "Remote Maintenance for CUI Systems"
  - "Practitioner insights B"
  - "3.1.20"
  - "3.7.5"
  - "3.7.6"
  - "3.8.9"
  - "raw/CMMC-FAQs-v2.3-May-2026.md"
  - "raw/practitioner-community-export-2026-09-02.md"
public_sources:
  - "CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "32 CFR 170.4 (definitions of ESP, CSP, Security Protection Data): https://www.ecfr.gov/current/title-32/section-170.4"
  - "32 CFR 170.19 (CMMC Assessment Scope): https://www.ecfr.gov/current/title-32/section-170.19"
  - "CMMC FAQs, Section E: https://dodcio.defense.gov/CMMC/FAQ/"
  - "DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012"
  - "DoD CIO FedRAMP Moderate Equivalency memo (December 2023): https://dodcio.defense.gov/Portals/0/Documents/Library/FEDRAMP-EquivalencyCloudServiceProviders.pdf"
  - "CMMC Level 2 Assessment Guide, DoD CIO, MA.L2-3.7.5 and MA.L2-3.7.6: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
---

# ESP and MSP scoping

This skill answers one question: where does an outside provider sit in the CMMC Assessment Scope, and what document proves it? It covers Managed Service Providers (MSPs), Managed Security Service Providers (MSSPs), Remote Monitoring and Management (RMM) tools, backup destinations, Security Operations Center (SOC) services, and Software as a Service (SaaS) vendors. It places the provider, decides whether the provider is a Cloud Service Provider (CSP) or an External Service Provider (ESP) that is not a CSP, and records the provider, its role, its FedRAMP status, and the tools it reaches in with in the engagement's SSP by calling the Skill tool with `scribe`. The responsibility matrix is generated from that record. It does not decide whether the provider's product is acceptable to buy, it does not draw the network diagram, and it does not write SSP conformity statements. For an assessment of a single requirement the provider inherits, call the Skill tool with `control-evidence-lookup`.

## Inputs

- The provider: name, service, contract or statement of work if available.
- How the provider connects: their own accounts on the company's systems, a remote-control tool, an agent that reports out, or nothing but a portal the company logs in to.
- Which data leaves the environment to the provider: CUI, Security Protection Data (logs, alerts, configuration, vulnerability data), or neither.
- The engagement's record, `ssp/components/*.md`: the providers already recorded, each a `service` component with a `provider` block giving its role and FedRAMP status, and the components, assets, and categories they reach. Read the files directly; they are the current state, so a provider already recorded is corrected rather than added twice. Never read anything under `view/`, including `view/esp-responsibility-matrix.md`; it is generated for people. The provider interviews, the contracts, the company's own documents, and the record are the sources.
- `scope/data-flow.md` if it exists, `scope/cui-determinations.md` for which data is CUI, and `CONTEXT.md` for the client's vocabulary. Whether a provider holds CUI takes that status from the determinations; when an item has no determination, place the provider on facts that do not depend on it and put the question on `scope/open-items.md` for `cui-determination-workflow`. Reach into an asset the record already holds as a CUI Asset is such a fact: it is CUI reach whatever the determination later says about any one file, and a tool whose remote control opens or displays that asset's screens or files is a CUI Asset on that fact. Where the record's own category is in doubt, place the tool at the floor the facts support, a Security Protection Asset for admin reach, and put the question on the open items list.
- The seat, from `CONTEXT.md`.

## Method

1. **Run the account test first.** Ask whether provider staff hold their own standing accounts on company systems (local admin, domain admin, global admin in the tenant, an RMM agent with unattended remote control), or whether they can only reach the environment while a company user is logged in and watching. Two outcomes:
   - **Unattended standing accounts or unattended remote control**: the provider's access is in scope. If the accounts reach CUI Assets, the provider's people and tooling can process CUI and are treated as CUI reach: the tool is a Security Protection Asset (SPA) at minimum and, where it can open, move, or display CUI, the path is assessed as a CUI path. Every requirement that touches accounts, remote access, MFA, logging, and nonlocal maintenance applies to that access.
   - **Shadow-only access**: the provider can only join a session a company user started, sees what that user sees, and holds no credentials of its own. Practitioner consensus treats the provider's tooling as a Contractor Risk Managed Asset (CRMA): capable of touching CUI, not intended to, documented in the inventory, SSP, and diagram, and covered by a policy that says why it will not.
   Write the outcome down before anything else. The rest of the method depends on it.

2. **Check what data goes out, separately from access.** An MSSP or SOC that never connects in can still be an ESP because it holds Security Protection Data. 32 CFR 170.4 defines an ESP as an outside organization that processes, stores, or transmits CUI or Security Protection Data, or that provides security protection, within the scope. CMMC FAQ E-Q4 says an MSP and a separate MSSP that receive no CUI are both ESPs and are assessed as part of the company's assessment against the requirements they touch; neither needs its own certification. Record each provider in one of three rows:

   | Provider holds or reaches | Category | Assessed against |
   |---|---|---|
   | CUI (can open, store, or move it) | ESP with CUI; tooling is a CUI Asset or SPA depending on function | Every Level 2 requirement the access or storage touches |
   | Security Protection Data only (logs, alerts, EDR telemetry, configs) | ESP with SPD; tooling is an SPA | Requirements relevant to the capability it provides |
   | Neither, and shadow-only access | CRMA | SSP review; limited checks if the write-up is weak |

3. **Ask the provider who they outsource to.** Many MSPs resell an RMM, EDR, or SOC service from a larger MSP. The second-tier provider watches alerts, reads device inventory, and may issue triage commands. It sees Security Protection Data, so it is an ESP in its own right, even though the company has never heard of it. Ask directly: which vendors sit behind your RMM, EDR, backup, and SOC, and what can each of them see or do? Practitioner consensus is split on whether the second-tier provider gets its own row in the responsibility matrix or is folded into the primary MSP's row; see the disagreement section. Either way, record it (see Output).

4. **Scope the RMM by feature, not by product.** An RMM is several capabilities behind one logo: inventory and patching agents, scripting, and unattended remote control. The remote-control feature is the one that carries CUI screen content off the endpoint and through the vendor's relay, and it is the feature most often not covered by a FedRAMP authorization. Ask which features are enabled, whether the relay is FedRAMP Moderate authorized, and whether remote control can be disabled while patching stays on. A working pattern in practice: keep the RMM for patching and inventory, disable its remote control, and use a FedRAMP-authorized or company-controlled path for hands-on sessions. Record the feature list in the tool's remarks, not just the product name.

5. **Apply the CSP versus ESP fork.** Two different bars apply, and the fork decides which one.
   - **CSP that processes, stores, or transmits CUI**: DFARS 252.204-7012 and FAQ E-Q1 require FedRAMP Moderate authorization or equivalency under the DoD CIO memo. FAQ E-Q2 says encryption does not remove that bar: encrypted CUI at rest in a non-authorized cloud is still a violation. If a vendor claims equivalency, ask for the system security plan and the third-party assessment body of evidence; a claim with no SSP behind it is not defensible (public post: https://reddit.com/r/CMMC/comments/pza6rh/_/hf0odxj/).
   - **ESP that is not a CSP**: an MSP that administers a tenant the company licenses does not become a CSP by reselling it (FAQ E-Q5). It is assessed inside the company's assessment against the requirements it touches (FAQ E-Q3 and E-Q4). No FedRAMP bar applies to it.
   - **Security Protection Data**: the FedRAMP Moderate bar in DFARS 7012 attaches to CUI. It does not attach to an SPA that holds only Security Protection Data (32 CFR 170.19(c)(2) table; public post: https://reddit.com/r/NISTControls/comments/19czouy/_/kj30ida/). Do not force a log platform or EDR console through the CUI bar unless CUI actually lands in it. Note that some companies still drop non-FedRAMP SPAs to reduce argument at assessment; that is a business choice, not a rule.
   - **Where the MSP modifies the cloud service** it contracts for (FAQ E-Q5): it may itself be a CSP, and the FedRAMP bar follows.

6. **Handle nonlocal maintenance as its own path.** A vendor that connects in to troubleshoot an ERP, a CNC controller, or a firewall is doing nonlocal maintenance, whether or not they intend to open CUI. Capability governs, not intent. 3.7.5 requires MFA to establish the session and termination when the work is done; 3.7.6 requires supervision of maintenance personnel who lack access authorization. Two accepted shapes: a supervised, time-boxed, screen-shared session that ends when the ticket closes (the vendor stays outside the pool of authorized CUI users), or a standing privileged path with MFA, a unique named account per technician, a managed access point, and session logging (the vendor is then an ESP with CUI reach). Configuration-management tools that hold a persistent connection to a firewall or switch do not fit the "terminate when complete" wording cleanly; practitioner consensus is to treat the tool as part of the authorization boundary and evidence user-session termination in the tool instead.

7. **Work out the responsibility matrix with each ESP, even when they resist.** The responsibility matrix is the evidence for every requirement the company inherits. Per requirement, establish what the company implements and what the provider implements, and have the provider sign it. Each side of that split is a conformity statement, one on the provider's component and one on the company's, which `to-ssp` writes; scribe renders the matrix from them as `view/esp-responsibility-matrix.md`, and that page is what the provider signs. Providers that push back are usually providers that hold global admin with no written duties; that is exactly the case the assessor will probe. If the provider will not sign, the inheritance claim has no evidence, and the requirement is assessed as the company's alone.

8. **Warn the MSP about liability.** If the MSP was not an equal party when the scope was written, and the scoping documents say something the environment does not do (a separation that does not exist, an out-of-scope claim with no technical bar), the MSP is the party an assessor and a later inquiry will hold to the inaccurate documentation. Say this in the first meeting. Also set the effort expectation: a CUI-scoped device needs the whole managed-service workload, not a small add-on, whatever file-sharing product the client has already bought.

9. **Give the external systems list what it needs.** Every ESP belongs on the 3.1.20 list of approved external connections with its category (CRMA, SPA, CUI Asset), its FedRAMP status and package identifier where one exists, and the approved use. Keep the list to providers that hold CUI or can reach back in; do not list every website. Add each one to `scope/external-systems.md`, a Markdown working note other skills read, and create it if it does not exist: one line per provider or external system with its category, FedRAMP status, and approved use. Put the same facts in the provider's record, the role, the FedRAMP status, what it does, and the approved use in the remarks, because the SSP's statement on 3.1.20[a] is written from the record by `to-ssp`. When nobody has approved the use yet, write the current use, say it is not yet approved, and put the approval on the open items list.

## Output

Record every placement in the SSP by calling the Skill tool with `scribe`, one decision per call. Never write the `ssp/` files yourself, and never edit anything under `view/`: the record holds the inventory and the responsibility matrix, and scribe renders `view/asset-inventory.md` and `view/esp-responsibility-matrix.md` from it for people. Point the operator at those pages when they want to read the providers or the matrix.

Tell scribe, in these terms:

1. **The provider**: its slug when it is already recorded, or its name and service ("Northstar Managed IT", "Microsoft 365 commercial tenant") when it is not, its one role (CSP, MSP, MSSP, SOC, RMM provider, or other ESP), one line on what it does for the organization, and remarks carrying how it was placed: the account test outcome, the data it holds or reaches (CUI, Security Protection Data, or neither), the RMM features enabled, the providers behind it, and the approved use. A provider has exactly one role. A company doing two jobs, such as an MSP that also runs the SOC, is recorded as two providers, one per role, so each carries its own statements. Record a second-tier provider that sees Security Protection Data as a provider of its own, which satisfies both positions in the disagreement below, and name it in the primary provider's remarks too. When you know a second-tier provider exists but not who it is, such as the vendor behind an MSP's RMM, do not invent a name: put the question on `scope/open-items.md` and record the provider once it is named. When the facts leave the account test unanswered, as with a vendor that "dials in" to do something nobody has described, record the provider with its role, say in its remarks that the access model is not confirmed, put the question on the open items list, and record no tool for it until the tool is known. Capability governs, not intent, so an unanswered test is never read as "none".
2. **For a CSP, its FedRAMP status**. A provider whose cloud service carries CUI is recorded with the role CSP, whatever else it does, so its FedRAMP status can be recorded: a third-party RMM whose relay carries CUI screen content is a CSP, with "RMM" in its description. The status: Moderate authorized, with the date authorized from its FedRAMP Marketplace listing; Moderate equivalent, only with the SSP and third-party assessment evidence in hand (step 5); or neither. When nobody has checked the listing for the specific offering purchased, record neither and put the check on `scope/open-items.md`; never record a status nobody verified. An ESP that is not a CSP has no FedRAMP status.
3. **Each tool the provider reaches in with, as an asset** of the provider, named by its asset id: the RMM, an MSSP's own EDR console, the backup agent, the technicians' own devices when they connect in. A provider that reaches in with nothing, such as a SOC that only receives alerts, gets no asset; its record and remarks carry it. Give it its category from steps 1, 2, and 4 (a Security Protection Asset at minimum when it has admin reach, a CUI Asset where it can open, move, or display CUI, a CRMA only for shadow-only tooling covered by a written policy) and remarks naming the features enabled and what decided the category. Devices that cannot be named yet, such as the MSP's technician laptops, may be one asset named for the group, with the count on the open items list. Give the provider's component a category only when every asset behind it shares that category. The organization's own tenant, and the services inside it (identity, endpoint management, endpoint detection bought with the tenant), are assets of the CSP too, but they are not this skill's to add: their categories, and splitting the tenant's component by category, belong to `cmmc-scope-boundary`. Name them for it on the open items list.
4. **A correction**, when the record already holds a provider with the wrong role or FedRAMP status, or a provider's tool in a category your method rejects: the new value, and remarks saying why the old one was wrong. Correct it in place, naming the provider by its slug or the tool by its asset id; do not remove and re-add it, so its statements survive.

Record only providers in use. A provider that is proposed and not yet used, such as a new backup service, is not recorded here: call the Skill tool with `significant-change-determination`, which decides whether it can be used at all. A provider that has no access and holds neither CUI nor Security Protection Data is not an ESP and gets no record. A system the organization reaches out to that is not a provider, such as a customer portal or a personal email account, belongs on the 3.1.20 list in `scope/external-systems.md`; recording one as an other ESP is allowed when it can reach back in. A lower-tier supplier that receives CUI, such as a finisher sent a drawing, is not an ESP either: it is a flowdown question for `flowdown-level-determination` and an information flow under 3.1.3, and it goes on the 3.1.20 list; name it on the open items list and record nothing for it here.

This skill writes no conformity statements. The per-requirement split from step 7, and the SSP's statement of the 3.1.20 list from step 9, are statements that `to-ssp` writes. Until it does, the matrix page lists the providers and their tools and says no statement names a provider yet.

Before calling scribe, write the placements as a table and show it to the operator. Record them once the operator confirms, or straight away if the operator asked you to record without stopping. Scribe gets one row per call:

```markdown
| Provider or tool | Record as | Role (provider) or category (tool) | FedRAMP status (CSP only) | Account test | Data held | Reason (the remarks) |
|---|---|---|---|---|---|---|
| <provider slug or name and service, or tool asset id> | provider / asset of <provider slug> | CSP / MSP / MSSP / SOC / RMM / other ESP; or CUI Asset / Security Protection Asset / Contractor Risk Managed Asset | Moderate authorized, <date> / Moderate equivalent / neither | unattended standing / shadow-only / none | CUI / SPD / none | <what decided it, the features enabled, who sits behind it> |
```

If scribe refuses a change, the refusal is the answer: quote scribe's check line, fix the decision, and ask again. Never work around it. A tool's asset id is unique across the whole SSP, and a tool's category must agree with its provider component's, so a provider whose tools span categories carries no category of its own.

Unconfirmed facts go on `scope/open-items.md`, which stays Markdown, with who will check them, never into a provider's remarks or an SSP statement as if they were settled. Remarks may say that something is not yet confirmed or reviewed, pointing at the open item; they never state the unconfirmed thing as fact. A provider the facts show but do not name, such as "the copier's service vendor", may be recorded under a plain descriptive title and renamed once the name is known. Record the placement decision in `docs/adr/` when the provider is an MSP or holds CUI. When the operator has you record before the provider has reviewed the placement, which the consultant seat note says to insist on, record it, say in the remarks that the provider has not reviewed it, and put the review on the open items list.

## Where practitioners disagree

- **Shadow-only tooling as CRMA.** Some assessors accept that a remote tool which can only join a user-initiated session is a CRMA. Others hold that any tool installed on a CUI Asset with a vendor relay is an SPA and assess it. The outcome depends on the assessor.
- **The second-tier provider.** One position: the sub-MSP is covered by the primary MSP's responsibility matrix and needs no separate row. The other: it holds Security Protection Data on its own systems, so it is a separate ESP and gets its own row. The outcome depends on the assessor.
- **Persistent management connections under 3.7.5.** One reading: a tool that never disconnects cannot satisfy "terminated when complete", so the tool must be redesigned. The other: the tool is inside the authorization boundary and user-session termination is the evidence. The outcome depends on the assessor.
- **Non-FedRAMP SPAs.** The regulation attaches the FedRAMP bar to CUI, not to Security Protection Data. Some assessors still question a non-authorized SIEM or MSSP. The outcome depends on the assessor.

## Seat notes

**Consultant seat**: run step 8 in the first meeting with the client's incumbent MSP, and do not call a scope final until the MSP has reviewed it; when you record before that review, say so as Output describes. Put every contested point above on the pre-assessment question list for `c3pao-selection-vetting`. **OSC seat**: you can run steps 1 through 3 yourself with the MSP contract and a 20-minute call; ask "can your staff log in when none of us is here?" and "who do you buy your RMM, EDR, and SOC from?" and write the answers down verbatim in the open items list.

## Sources

- CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (asset categories, ESP treatment).
- 32 CFR 170.4: https://www.ecfr.gov/current/title-32/section-170.4 (ESP, CSP, Security Protection Data definitions).
- 32 CFR 170.19: https://www.ecfr.gov/current/title-32/section-170.19 (scope and the category table).
- CMMC FAQ E-Q1 through E-Q5: https://dodcio.defense.gov/CMMC/FAQ/.
- DFARS 252.204-7012: https://www.ecfr.gov/current/title-48/chapter-2/subchapter-H/part-252/subpart-252.2/section-252.204-7012.
- DoD CIO FedRAMP Moderate Equivalency memo: https://dodcio.defense.gov/Portals/0/Documents/Library/FEDRAMP-EquivalencyCloudServiceProviders.pdf.
- CMMC Level 2 Assessment Guide, DoD CIO, MA.L2-3.7.5 and MA.L2-3.7.6: https://dodcio.defense.gov/CMMC/Resources-Documentation/.
- Public posts on equivalency evidence and the SPA carve-out: https://reddit.com/r/CMMC/comments/pza6rh/_/hf0odxj/ and https://reddit.com/r/NISTControls/comments/19czouy/_/kj30ida/.
- Practitioner consensus, unattributed, backs the account test in step 1, the sub-provider question in step 3, the RMM feature rule in step 4, the persistent-connection treatment in step 6, and the liability warning in step 8.
