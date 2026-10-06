> **Provenance.** The nine-zone model, the in-scope matrix, the four out-of-scope tests, and the zone-to-category crosswalk are from the ComplianceForge Unified Scoping Guide (USG), https://complianceforge.com/, licensed under Creative Commons Attribution 4.0 International (CC BY 4.0, https://creativecommons.org/licenses/by/4.0/). Attribution: ComplianceForge. Tables are restated in Markdown; the USG itself calls the crosswalk a generic example, not per-asset guidance. Changes: condensed to the tables and tests; commentary in this file is this repository's.

# USG nine-zone model and the crosswalk to CMMC asset categories

The **USG Nine-Zone Model** is the core mechanism of the Unified Scoping Guide. It sorts every system component into one of nine zones based on how it interacts with sensitive/regulated data, making it "evident which systems, applications and services must be appropriately protected".

## The nine zones

| Zone | Name | What it holds |
|---|---|---|
| **1** | Sensitive Data Assets (SDA) | Systems/apps/services that directly **P/S/T** sensitive/regulated data — the assets the data is trying to protect |
| **2** | Segmenting | Devices that provide segmentation and prevent data "contamination" — firewalls, hypervisors, ACL tools, ZTA micro-segmentation |
| **3** | Security Tools | Systems that impact the security/integrity of Zone 1 & 2 assets — AD/LDAP, DNS, NTP, patch mgmt, antimalware, DLP, VPN, MFA, MDM, SIEM, IDS/IPS |
| **4** | Connected | Any system that can communicate with the SDE (directly or indirectly). If it can impact the security of the data, it is in scope |
| **4A** | Directly Connected | Sits outside the SDE but can communicate with a Zone 1 asset |
| **4B** | Indirectly Connected | No direct SDE access, but can reach Connected/Segmenting systems (e.g., an admin workstation that manages AD or a firewall) |
| **5** | Out-of-Scope | Completely **isolated** from the SDE — no connections whatsoever |
| **6** | Enterprise-Wide | Corporate-wide cyber + physical security program (policies, standards, procedures) |
| **7** | External Service Provider (ESP) | Third parties whose contracts define logical/physical access; "flow-down" of requirements applies |
| **8** | Subcontractor | Third parties party to the contract who may create/access/store/transmit the data |
| **9** | Cloud Service Provider (CSP) | A specialized ESP offering NIST SP 800-145 cloud computing (SaaS/PaaS/IaaS) |

## In-scope matrix

| Zone | Data P/S/T? | In scope? | Segmentation method |
|---|---|---|---|
| 1 Sensitive Data Assets | YES | **YES** | None |
| 2 Segmenting | NO | **YES** | Provides segmentation |
| 3 Security Tools | NO | **YES** | Controlled Access |
| 4 Connected (4A) | NO | **YES** | Controlled Access |
| 4B Indirectly Connected | NO | **YES** | Indirect Access |
| 5 Out-of-Scope | NO | **NO** | Isolated |
| 6 Enterprise-Wide | NO | NO | N/A (whole org) |
| 7 ESPs | MAYBE | **MAYBE** | Must be determined |
| 8 Subcontractors | MAYBE | **MAYBE** | Must be determined |
| 9 CSPs | MAYBE | **MAYBE** | Controlled Access |

Source:

## The four Out-of-Scope (Zone 5) tests

A component is only Zone 5 if **all four** hold:

1. It does not P/S/T sensitive/regulated data;
2. It is not on the same network segment/subnet/VLAN as systems that P/S/T the data;
3. It cannot connect to or access any system in the SDE; and
4. It cannot gain access to the SDE nor impact a security control of an in-scope system via another in-scope system.

## Zone 4 — the "connected" trap

Zone 4 is where scope quietly expands. The guiding rule: *"if something can impact the security of sensitive/regulated data, it is in scope."* An admin's workstation that can grant itself rights into the SDE is Zone 4B and therefore in scope, even though it never touches the data itself. A DLP tool can serve as a compensating control to argue a periodic outbound-only connection out of scope.

The Unified Scoping Guide does **not** replace CMMC's five asset categories — it maps its nine zones onto them so an organization can use one data-centric model across CUI, PCI, and other regimes. The crosswalk below is presented by the USG as a "generic example," not authoritative per-asset guidance.

## The mapping

| USG Zone | CMMC category it typically maps to |
|---|---|
| **Zone 1** Sensitive Data Assets | **CUI Asset** (or Specialized Asset) |
| **Zone 2** Segmenting | **SPA** (Security Protection Asset) |
| **Zone 3** Security Tools | **SPA** |
| **Zone 4** Connected | **CRMA** (or Specialized Asset) |
| **Zone 5** Out-of-Scope | **OOSA** (or Specialized Asset) |
| **Zone 6** Enterprise-Wide | **OOSA** (or Specialized Asset) |
| **Zone 7** ESPs | Possibly CUI Asset / SPA / SA / OOSA |
| **Zone 8** Subcontractors | Possibly CUI Asset / SPA / SA / OOSA |
| **Zone 9** CSPs | Possibly CUI Asset / SPA / SA / OOSA |

Source:

## How the USG explains it

For a generic CMMC Level 2 exercise:

- **CUI Assets** → Sensitive Data Assets (Zone 1).
- **Security Protection Assets (SPA)** → Segmenting (Zone 2) *or* Security Tools (Zone 3), depending on the asset.
- **CRMA** → Connected (Zone 4), because they are *capable* of P/S/T CUI but do not, owing to the OSA's policies/standards/procedures.
- **Specialized Assets (SA)** → can appear in Zones 1, 4, 5, 7, 8, or 9.
- **Out-of-Scope Assets (OOSA)** → Zone 5, but can also live in Zones 6, 7, 8, or 9.

## Why the two models differ

CMMC creates categories (CRMA, Specialized Asset) specifically to *remove* assets from full assessment that the more aggressive PCI DSS model would keep in scope. The USG zones are function/connectivity-based and data-type-agnostic; CMMC's categories layer an assessment-treatment decision on top. See CMMC Scoping for the treatment/documentation requirements per category, and USG Nine-Zone Model for the zone definitions.
