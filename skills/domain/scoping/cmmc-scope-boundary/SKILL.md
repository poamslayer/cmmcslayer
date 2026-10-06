---
name: cmmc-scope-boundary
description: Discover the assets with a nine-area walk of the site, then decide whether each one sits inside the CMMC Level 2 Assessment Scope, which of the five asset categories it belongs to, and what documentation that category requires, recording every asset and category in the SSP through scribe. Use whenever an operator asks "is this asset in scope", asks what to inventory, or is building the asset inventory and network diagram before an assessment.
vault_sources:
  - "CMMC Scoping"
  - "USG Zones vs CMMC Asset Categories"
  - "USG Nine-Zone Model"
  - "Unified Scoping Guide"
  - "3.4.1"
  - "raw/CMMC Scoping Guide Level 2 v2.13.md"
  - "raw/unified-scoping-guide.pdf"
  - "raw/CMMC-FAQs-v2.3-May-2026.md"
  - "Client Onboarding Checklist"
  - "Client Onboarding Discovery Checklist"
  - "Client Onboarding: Data Flow Mapping First"
  - "MSP Scoping and Access Model"
  - "Printer Scoping"
  - "Machine Shops and CUI"
  - "Export Controls and CUI"
  - "Shadow IT and CUI"
  - "Wireless Network Scoping"
  - "Practitioner insights B"
  - "raw/practitioner-community-export-2026-09-02.md"
public_sources:
  - "CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "32 CFR 170.19 (CMMC Assessment Scope and asset categories): https://www.ecfr.gov/current/title-32/section-170.19"
  - "32 CFR 170.4 (definitions, including Test Equipment): https://www.ecfr.gov/current/title-32/section-170.4"
  - "CMMC FAQs, Section F (Scoping): https://dodcio.defense.gov/CMMC/FAQ/"
  - "CMMC Level 2 Assessment Guide, DoD CIO, CM.L2-3.4.1: https://dodcio.defense.gov/CMMC/Resources-Documentation/"
  - "Unified Scoping Guide, ComplianceForge, CC BY 4.0: https://complianceforge.com/"
---

# CMMC scope boundary

This skill answers one question: does this asset belong inside the CMMC Level 2 Assessment Scope, and if so, as which of the five categories? It starts by finding the assets, with a walk of the site in nine areas, because an asset nobody listed is never placed. It then applies the Process/Store/Transmit test, assigns exactly one category per asset, states the documentation that category requires, rejects the reasoning patterns that have gotten organizations in trouble at assessment, and records each component, asset, and category in the engagement's SSP by calling the Skill tool with `scribe`. It does not decide which of the 110 requirements apply to an in-scope asset once categorized (call the Skill tool with `requirement-applicability-matrix` for that), and it does not judge whether a specific control implementation is sufficient (call `control-evidence-lookup`).

## Inputs

- `scope/data-flow.md`, which the `find-cui` flow leaves; the operator runs it. The discovery walk in step 0 starts from it: assets fall out of the map, never the reverse. When there is no map, tell the operator and recommend running `/find-cui` first. If the operator directs you to go on without one, work from the sources they name, put the missing map on `scope/open-items.md`, and say in your summary that every placement rests on those sources.
- `scope/cui-determinations.md`, for which documents and data are CUI. A placement that rests on whether something is CUI takes that status from the determinations; never infer it yourself from what a file was made from. When an item has no determination, do not decide it here. Place the asset on facts that do not depend on it, and put the question on `scope/open-items.md` for `cui-determination-workflow`.
- A description of the asset: what it is, what touches it, how it connects to the rest of the network, and who administers it.
- The engagement's record, `ssp/ssp.json`: the components, assets, and categories already recorded, so a new asset is added consistently with the ones already placed and a wrong category left by earlier work is found and corrected. Read it by calling the Skill tool with `scribe` and asking it to show the record; that is the current state. Never read `view/asset-inventory.md`; it is generated for people. The walk, the company's own documents, and the record are the sources.
- `scope/network-diagram.md`, the notes file holding any diagram the client handed over, if it exists. Treat an inherited diagram as a claim to check, not a source of categories.
- `CONTEXT.md` for the client's component vocabulary.
- The claimed technical control, if any, that the operator believes removes the asset from scope (a VLAN, a firewall rule, a policy). This skill decides the category; call the Skill tool with `logical-separation-test` first when the claim rests on network segmentation, since that verdict feeds directly into this one.

## Method

0. **Discover the assets before placing any.** On a first pass through an environment, walk the physical site with the data flow map in hand, and pull logs and consoles directly rather than trusting interviews. Nine areas, each a short list of what to pull:

   1. **Identity and people.** Every role touching CUI, temps and the bookkeeping relative included, plus who qualifies for a 3.1.5 carve-out. Foreign nationals, remote-work locations. Admin accounts across domain, firewall, ERP, RMM, watching for shared logins. Identity backbone (local, on-prem AD, or Microsoft Entra ID standalone or hybrid) and how far MFA, conditional access, and local admin rights reach. Last three departures, checked for leftover access. Screening against 3.9.1. Whether MFA lives on a personal phone.
   2. **Endpoints.** OS and support status per device, aging shop-floor Windows especially. Make and model against NDAA Section 889 banned-vendor lists. Government-furnished equipment and its owner. Disk encryption and FIPS validation, EDR versus consumer antivirus, patch method. Written USB/removable-media policy against 3.8.1 and 3.8.7 practice. Personal laptops with RDP into the network. MDM coverage.
   3. **Network.** Firewall brand, model, support status; VLANs or flat. Each SSID, enterprise auth or shared password, guest wifi kept apart from CUI. Remote sites, site-to-site VPN, switch management, DNS filtering. Unclaimed devices: cameras, badge readers, thermostats, HDMI adapters. Domain controllers, license servers, or shares on the general side still queried from the CUI side.
   4. **Shop floor and OT.** Each CNC, CMM, and PLC controller's OS, network status, how a program reaches it. A thumb drive carried to a controller is a data flow, not an exception; check it is on the map. What sits beside what, a CUI workstation next to a CNC especially. Machine-vendor remote access. Layout: entry and exit, bay doors, where paper CUI sits. State plainly: taking CUI off the shop network does not unlock the bay doors when parts are ITAR; the physical controls export law demands still apply.
   5. **Remote access.** VPN product, tunnel type, MFA on it. Anything reachable straight off the internet: exposed RDP, RDWeb, a web app. The RMM in use, which features run, console MFA, FedRAMP standing of its remote-control feature. Any unofficial tool beside the sanctioned one. Whether VDI has clipboard, file transfer, and print redirection off.
   6. **Servers and backups.** Which servers, hypervisor, file shares, and storage hold CUI, and who keys the server room. For backups: product, landing spot, encryption, retention, last proven restore date, delete rights, FedRAMP status of the destination. Backups fail FedRAMP equivalency more often than anything else in the environment, so verify the destination early.
   7. **M365 and cloud.** Tenant tier licensed and what each user got assigned. Which protections actually run, not just licensed: labeling, auto-labeling, loss prevention, external sharing limits. Whether OneDrive syncs to a personal machine, or an inbox rule forwards to a personal address. Whether SPF, DKIM, and DMARC are set, and how CUI actually moves by email today, not what the policy claims.
   8. **SaaS and shadow IT.** Every SaaS in use: ERP/MRP, CAD, PLM, quoting, accounting, payroll/HR, e-signature, file transfer, messaging, video, ticketing. Personal cloud storage, translators, AI assistants. Sign-in and firewall logs pulled directly, not trusted from interviews. Free-text fields in the ERP or CRM quietly collect CUI, the PCI-era card-data trap again. FedRAMP status per CUI-touching SaaS.
   9. **Printers, physical, and logging.** Printer model, storage, scan destination, wireless/cloud printing, secure release, USB state, per device. Copier servicer and remote dial-in. Fax and eFax lines. Shredding and drive disposal. Every printer on the facility diagram regardless of category. Visitor sign-in, badges, escort practice, cameras. Where paper CUI sits day to day, clean-desk honesty, shipping and receiving. Alternate work sites, home offices included (3.10.6). Central log collection, retention, reviewer, time source, and alerting on failed logins and admin changes. Incident plan and prior incidents (3.6.1).

   Then name every outside party able to reach anything the walk found: the MSP and whoever it outsources to, the copier lessor, the backup, ERP, and machine vendors, a colocation facility, and any informal IT help never under contract. Call the Skill tool with `esp-and-msp-scoping` for each; the access model, not the stated intent, decides the category, and that skill records the provider. Until it has, list each outside party on `scope/open-items.md` so none is lost. Printers and shop-floor machines go to `printer-and-ot-asset-scoping`, laptops and remote access to `endpoint-and-vdi-scoping`.

   Anything the walk collected that nobody has verified goes on `scope/open-items.md`, never into an asset's remarks in the record or an SSP conformity statement. An open item closes when someone checks it.

1. **Run the Process/Store/Transmit (P/S/T) test.** Per the CMMC Level 2 Scoping Guide, an asset processes CUI when CUI is used by it (accessed, entered, edited, generated, manipulated, or printed), stores CUI when CUI sits inactive on it (disk, memory, or paper), and transmits CUI when CUI moves through it, physically or digitally. An asset that can do any one of the three is a CUI Asset, unless it qualifies for one of the other four categories below. Physical location does not matter: a cloud service reached only over the internet is still tested by P/S/T, not exempted because it is off the local network.

2. **Assign exactly one of the five categories.** Every asset gets one category, never two:

   | Category | What it is | Assessed against |
   |---|---|---|
   | CUI Asset | Processes, stores, or transmits CUI | Every applicable Level 2 requirement |
   | Security Protection Asset (SPA) | Provides a security function to the scope (identity, logging, endpoint protection, firewalling) whether or not it touches CUI | The requirements relevant to the function it provides |
   | Contractor Risk Managed Asset (CRMA) | Can reach CUI but is not intended to, and is not separated from CUI Assets | SSP review, with limited checks if the write-up is weak |
   | Specialized Asset | Touches CUI as a side effect of its job but resists standard hardening: connected sensors, industrial controllers, shop-floor equipment, government-owned gear, locked-down or restricted systems, test rigs | SSP review under a risk-based policy, not assessed against the 110 at Level 2 |
   | Out-of-Scope Asset | Has no technical path to CUI and offers no protective function for the scope | Not assessed, but the designation must be defensible |

   Four placements this table leaves open, settled:

   - **A computer beside a machine is Specialized only when it is part of the machine.** 32 CFR 170.4 defines test equipment as hardware "and/or associated IT components" used in testing, so a PC dedicated to a measuring machine's software, doing nothing else, can be a Specialized Asset (test equipment) with the machine. A PC used for ordinary work, holding files, printing, or reaching shares and email as any workstation does, is not part of any machine because it sits next to one or sends it programs; it is a CUI Asset when it passes P/S/T. An old or unpatchable operating system is never the reason for either answer: it is a finding against the requirements (3.14.1, handled as an enduring exception or on a POA&M). Say in the remarks which of the two the PC is and what it does besides serve the machine.
   - **CRMA needs a reason CUI is not intended to be there.** An asset qualifies as a CRMA only when a written policy and procedure keep CUI off it. With none, an asset that can reach CUI and has no technical separation from it is a CUI Asset. When nobody has confirmed what the asset's user handles, record the CUI Asset and put the role question on `scope/open-items.md`; a later answer, plus the policy, can move it.
   - **A firewall or VPN device is a Security Protection Asset even though CUI traffic passes through it.** Its protective function decides its category.
   - **A printer or multifunction device on the CUI path has three defensible positions:** in scope as a CUI Asset; in scope as a Specialized Asset when it cannot be secured; or taken off the CUI path so it no longer touches CUI. Name all three in the device's remarks and say which one the client chose. When nobody can be asked, record it as a CUI Asset, the category it holds today, and put the choice on `scope/open-items.md`. `printer-and-ot-asset-scoping` works through the choice.
   - **Removable media that holds CUI at rest is an asset.** A backup drive holding a copy of a CUI share is a CUI Asset. A stick used only to carry a file from one machine to another is a flow on the data flow map, handled under the media requirements (3.8.x), not an inventory row.

   32 CFR 170.19(c) is the authority for this table. reference/usg-zones-to-cmmc-categories.md, drawn from the Unified Scoping Guide (ComplianceForge, CC BY 4.0, https://complianceforge.com/), carries an independent, connectivity-based crosswalk that lands on the same five categories from a different angle; use it as a second lens when a category is not obvious, but score against the table above.

3. **Enforce the documentation matrix.** What a category costs to carry:

   | Category | Asset inventory | SSP treatment | Network diagram |
   |---|---|---|---|
   | CUI Asset | Required | Required, full conformity statements | Required |
   | SPA | Required | Required, scoped to the function | Required |
   | CRMA | Required | Required, narrative explaining why CUI stays off it | Required |
   | Specialized Asset | Required | Required, risk-based management policy | Required |
   | Out-of-Scope | Not required by the Scoping Guide; recorded anyway, with its justification | Skip it | Skip the diagram entry, but keep the written justification |

   The Scoping Guide asks nothing of an Out-of-Scope Asset beyond a justification you can produce. This engagement records it as an asset anyway, with the justification as its remarks, so an assessor reading the record sees the scoping decision and its reason side by side.

   The asset inventory itself satisfies part of CM.L2-3.4.1 (establish and maintain a system inventory covering hardware, software, firmware, and documentation), so build the inventory and the diagram together rather than as separate exercises. In this engagement the inventory is the assets recorded in `ssp/ssp.json`.

4. **Hold the line on "cannot".** The Out-of-Scope definition turns on a single word: the asset must be technically unable to process, store, or transmit CUI. A policy that says users should not put CUI on the asset is not that. An intranet firewall rule that is not deny-by-default is not that either. If you cannot point to a specific technical barrier that makes P/S/T impossible, the asset is not Out-of-Scope. Fall back to CRMA when a written policy and procedure keep CUI off the asset (step 2): it costs an SSP narrative and an inventory row, not an argument you might lose in front of an assessor. With no such policy, it is a CUI Asset. Reserve the Out-of-Scope claim for cases with a real technical bar, such as a thin client configured for keyboard, video, and mouse only (see `endpoint-and-vdi-scoping`), or a network segment with no route at all to a CUI Asset.

5. **Warn on the Level 3 trap.** CRMA is a convenience that is specific to Level 2. Under 32 CFR 170.19(c), a CRMA counts as a full CUI Asset once the boundary is drawn for a Level 3 scope. A company with a Level 3 goal on the roadmap should not lean on the CRMA category the way a Level 2-only shop can; whatever it books as a CRMA now becomes something it has to fully assess later. Raise this during the initial scoping conversation, not after a Level 3 readiness review turns it up.

6. **Reject the five anti-patterns.** Each one has shown up often enough to name:
   - Treating a cloud-hosted SaaS product as out of scope because it is not on the local network. The P/S/T test applies regardless of where the asset physically sits.
   - Reaching for CRMA whenever an asset is inconvenient to test, instead of when the facts actually support it. A thin write-up behind that label invites the assessor to ask why the asset was not simply assessed in full.
   - Calling a laptop out of scope because "policy says no CUI," with no technical control backing the claim. Without a technical barrier, the laptop can still process CUI, so it is at minimum a CRMA.
   - Putting a Security Protection Asset on the out-of-scope side of the diagram. An SPA is in scope by definition; its function is what protects the scope.
   - Mapping one asset to two categories. Every asset gets exactly one; if it seems to need two, split it into the assets that actually differ (for example, a shared server hosting both a CUI file share and an unrelated non-CUI application is two logical assets, not one asset in two categories). A cloud tenant is the common case: its mail and file services hold CUI while its identity and endpoint management services protect the scope, so record the tenant as two assets, one per category, and split its component so each category has its own component (Output, item 4).

7. **Produce the two artifacts an assessor will ask for on day one.** A finished asset inventory and a diagram showing the drawn boundary are things a company must already have before an assessment can begin at all. Walk in without either one and there is nothing yet to assess. The inventory is the record, rendered for people as `view/asset-inventory.md`. The diagram is drawn from the record: once the assets are recorded, call the Skill tool with `cmmc-boundary-diagram`, which writes `scope/network-diagram.drawio`.

## Output

Record every decision in the SSP by calling the Skill tool with `scribe`, one decision per call. Never write `ssp/ssp.json` yourself, and never edit anything under `view/`: the record is the inventory, and scribe renders `view/asset-inventory.md` from it for people. Point the operator at that view when they want to read the inventory.

Tell scribe, in these terms:

1. **The component**, if it is not already recorded: the named part of the system that conformity statements will describe once ("Windows 11 office endpoints", "SAG-NAS", "Microsoft 365 commercial tenant"), what kind of thing it is (a class of hardware, installed software, a cloud service), and one line describing it. Give the component a category only when every asset behind it shares that category. Do not record an outside provider as a new component here; providers and their FedRAMP status belong to `esp-and-msp-scoping`. An asset of a provider, such as the organization's tenant, is recorded against the provider's component like any other asset.
2. **The asset**: its name (hostname, asset tag, or tenant name), the component it is an instance of, its category, a short description, and remarks carrying the reason: the P/S/T finding or the technical control that decided it. A Specialized Asset also gets its kind: IoT, industrial IoT, OT, government-furnished equipment, restricted information system, or test equipment. An Out-of-Scope Asset must carry its justification in the remarks, naming the technical barrier that makes P/S/T impossible; if you cannot name one, it is not Out-of-Scope (step 4).
3. **A correction**, when the record already holds the asset in a category your method rejects: the new category, and remarks saying why the old one was wrong. Correct it in place; do not remove and re-add an asset, so its identity survives.
4. **A split**, when the assets behind one component fall in different categories, or would need different conformity statements: which assets move to a new component, its title, and, when they share one, its category. Engineering laptops that are CUI Assets and front-office laptops of the same model that are CRMAs are two components.

Before calling scribe, write the decisions as a table and show it to the operator. Record them once the operator confirms, or straight away if the operator asked you to record without stopping. Scribe gets one row per call:

```markdown
| Asset | Component | Category | Kind (Specialized Asset only) | Reason (the remarks) |
|---|---|---|---|---|
| <hostname, asset tag, or tenant> | <component title> | CUI Asset / Security Protection Asset / Contractor Risk Managed Asset / Specialized Asset / Out-of-Scope Asset | <IoT / industrial IoT / OT / GFE / restricted information system / test equipment> | <the P/S/T finding or the technical control that decided it> |
```

If scribe refuses a change, the refusal is the answer: read its reason, fix the decision, and ask again. Never work around it. Three refusals are about order and naming rather than the decision: give an asset a name without commas, because a split names the assets it moves as a comma-separated list; change the assets' categories before giving their component one; and split a component before giving either half a category. Splitting a provider's component, such as the tenant, leaves the provider's role and FedRAMP status on both halves; that is expected, since both are the same provider's service.

Things that are not assets get no category and no row: a Wi-Fi network name (SSID) that is simply part of a flat LAN, and paper CUI, which is part of the information flow. Say so in the diagram or the open items instead. The access point that broadcasts the network is hardware and is placed like any other device.

A group of devices that cannot be told apart yet, such as staff personal phones or a rotation of backup drives, may be recorded as one asset named for the group, with the unknown count on the open items list. Record each device separately once it can be named.

A correction can leave conformity statements on a component that no longer fit its assets' new category. Do not change them here: statements belong to `to-ssp` and `ssp-statement-writer`. List each one on the open items list so the next statement pass rewrites it.

Keep `scope/open-items.md` as Markdown alongside the record, one line per unverified fact from the discovery walk, with who will check it.

Do not draw the diagram here. After a pass that records or corrects assets, call the Skill tool with `cmmc-boundary-diagram` so `scope/network-diagram.drawio` matches the record; it draws every asset except a clean Out-of-Scope designation, where the justification in the record stands in for a diagram entry. Record the Level 3 trade-off in an open item when a CRMA designation is chosen and the client has stated a Level 3 goal.

## Where practitioners disagree

Some practitioners argue "cannot" should tolerate a strong compensating control stack (firewall rule plus data loss prevention plus training) even without a hard technical barrier, on the theory that no barrier is ever perfectly unbeatable by an insider anyway. Others hold that any reachable path, however unlikely to be used, means the asset is not technically unable to carry CUI and therefore fails "cannot" outright. The stricter reading is safer to design toward, but the outcome depends on the assessor.

## Seat notes

**Consultant seat**: run this skill once per asset type across the client's whole environment during the discovery phase, and write each asset's remarks well enough that a different C3PAO reading the record two years later can follow the logic. **OSC seat**: run this skill whenever a new device or service is added, not only during the initial scoping pass; a Level 3 trap avoided at purchase time is cheaper than one discovered at assessment.

## Sources

- CMMC Level 2 Scoping Guide v2.13, DoD CIO: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (the P/S/T definitions and the five-category table).
- 32 CFR 170.19: https://www.ecfr.gov/current/title-32/section-170.19 (the category table, the CRMA condition, and the Level 3 CRMA conversion).
- 32 CFR 170.4: https://www.ecfr.gov/current/title-32/section-170.4 (the Test Equipment definition, which reaches associated IT components).
- CMMC FAQs, Section F: https://dodcio.defense.gov/CMMC/FAQ/ (scoping questions and answers).
- CMMC Level 2 Assessment Guide, DoD CIO, CM.L2-3.4.1: https://dodcio.defense.gov/CMMC/Resources-Documentation/ (the system inventory requirement that pairs with the asset inventory artifact).
- reference/usg-zones-to-cmmc-categories.md, derived from the Unified Scoping Guide, ComplianceForge, CC BY 4.0: https://complianceforge.com/ (the independent zone crosswalk used as a cross-check).
- Practitioner consensus, unattributed, backs the nine-area discovery walk and the open-items rule in step 0, the backup, free-text field, and ITAR bay door warnings inside it, the anti-pattern list in step 6, and the "fall back to CRMA" guidance in step 4.
