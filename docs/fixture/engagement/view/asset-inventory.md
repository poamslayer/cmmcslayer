> **Generated file. Do not edit.** Rendered by scribe from `ssp/ssp.json`, which is the record. The next change to the SSP overwrites this file; to change what it says, record the change through scribe.

# Asset inventory

## Components

| Component | Type | Category | Description |
|---|---|---|---|
| Access control procedure | policy |  | Northstar's template procedure, policies/access-control-procedure.md. |
| CMM PC | hardware |  | Windows 7 PC running the CMM measurement software. |
| EdgeRouter firewall and VPN | hardware |  | Router and firewall at the internet edge, running the L2TP/IPsec VPN server. |
| Front office MFP | hardware |  | Color multifunction printer near the front office. |
| Haas VF-2 CNC mill | hardware |  | CNC mill with a Haas NextGen control. |
| Incident response plan | plan |  | Northstar's two-page template plan, policies/incident-response-plan.md. |
| Media handling policy | policy |  | One-page policy, policies/media-handling-policy.md. |
| Microsoft 365 commercial tenant | service |  | Microsoft 365 Business Premium commercial tenant: Entra ID, Exchange Online, SharePoint, OneDrive, and Intune. The previous consultant never checked the purchased SKU's FedRAMP status, so it is recorded as neither authorized nor equivalent until the FedRAMP Marketplace listing is verified. |
| Northstar Managed IT | service |  | Managed IT provider. Holds two Global Administrator accounts in Microsoft 365, builds the Windows endpoints, and runs the RMM that reaches them. |
| Personal phones | hardware |  | Staff-owned phones reading company email, with no MDM. |
| SAG-NAS | hardware |  | Network file server holding the Jobs, Quality, and Admin shares. |
| Saguaro operating practices | process-procedure |  | How the company works where the previous consultant described a practice without a written policy or a single component behind it. |
| Saguaro Wi-Fi | hardware |  | Wi-Fi network, SSID Saguaro, on the office LAN. |
| Shop floor PC | hardware |  | Windows 10 Pro desktop at the Haas machine. |
| Windows 11 office endpoints | hardware |  | Windows 11 Pro desktops and laptops, Entra-joined, one per office user. |

## Providers

| Provider | Role | FedRAMP status | Date authorized |
|---|---|---|---|
| Microsoft 365 commercial tenant | CSP | Neither |  |
| Northstar Managed IT | MSP | Not applicable |  |

## Assets by category

### CUI Asset

| Asset | Component | Description | Remarks |
|---|---|---|---|
| ACCT-ROB | Windows 11 office endpoints | Windows 11 Pro, Entra-joined |  |
| ENG-PRIYA | Windows 11 office endpoints | Windows 11 Pro, Entra-joined, CAD/CAM |  |
| Haas VF-2 (NextGen control) | Haas VF-2 CNC mill | CNC machine |  |
| NADIA-LT | Windows 11 office endpoints | Windows 11 Pro, Entra-joined |  |
| OFFICE-DANA | Windows 11 office endpoints | Windows 11 Pro, Entra-joined |  |
| OFFICE-LUIS | Windows 11 office endpoints | Windows 11 Pro, Entra-joined |  |
| PROG-TOM | Windows 11 office endpoints | Windows 11 Pro, Entra-joined |  |
| PURCH-ELLEN | Windows 11 office endpoints | Windows 11 Pro, Entra-joined |  |
| QC-MARIA | Windows 11 office endpoints | Windows 11 Pro, Entra-joined |  |
| SAG-NAS | SAG-NAS | Jobs, Quality, Admin shares |  |
| SHIP-JORDAN | Windows 11 office endpoints | Windows 11 Pro, Entra-joined |  |

### Contractor Risk Managed Asset

| Asset | Component | Description | Remarks |
|---|---|---|---|
| CMM-PC | CMM PC | Windows 7, runs CMM software |  |

### Specialized Asset

| Asset | Component | Kind | Description | Remarks |
|---|---|---|---|---|
| SHOP-PC-01 | Shop floor PC | OT | Windows 10 Pro, shared "shop" login |  |

### Out-of-Scope Asset

| Asset | Component | Description | Justification |
|---|---|---|---|
| MFP-FRONT | Front office MFP | Canon-class color MFP | As left by the previous consultant: policy prohibits scanning CUI. |
| Personal phones (all staff) | Personal phones | Outlook on personal devices | As left by the previous consultant, with no reason recorded beyond the note: Outlook on personal devices. |
