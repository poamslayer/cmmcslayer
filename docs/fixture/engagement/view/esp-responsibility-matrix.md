> **Generated file. Do not edit.** Rendered by scribe from `ssp/ssp.json`, which is the record. The next change to the SSP overwrites this file; to change what it says, record the change through scribe.

# ESP responsibility matrix

## Providers

| Provider | Role | CSP or ESP | FedRAMP status | Date authorized | What it does | Remarks |
|---|---|---|---|---|---|---|
| Microsoft 365 commercial tenant | CSP | CSP | Neither |  | Microsoft 365 Business Premium commercial tenant: Entra ID, Exchange Online, SharePoint, OneDrive, and Intune. The previous consultant never checked the purchased SKU's FedRAMP status, so it is recorded as neither authorized nor equivalent until the FedRAMP Marketplace listing is verified. |  |
| Northstar Managed IT | MSP | ESP | Not applicable |  | Managed IT provider. Holds two Global Administrator accounts in Microsoft 365, builds the Windows endpoints, and runs the RMM that reaches them. |  |

## Provider assets

No provider assets recorded yet.

## Per-requirement responsibility

A statement on a provider's component says how that service meets the objective, including settings the company configures in it; the statement says who performs each part.

### 3.1.1[a]

| Component | Whose component | Status | Statement |
|---|---|---|---|
| Microsoft 365 commercial tenant | Provider's | Implemented | Authorized users are managed in Microsoft Entra ID; the Entra user list is the authorized user list. |

### 3.1.1[c]

| Component | Whose component | Status | Statement |
|---|---|---|---|
| Microsoft 365 commercial tenant | Provider's | Implemented | Devices are authorized by being joined to Entra ID. |

### 3.1.5[a]

| Component | Whose component | Status | Statement |
|---|---|---|---|
| Microsoft 365 commercial tenant | Provider's | Implemented | Only Dana Ortiz and the two Northstar Global Administrator accounts hold administrative rights in Microsoft 365. |

### 3.1.6[b]

| Component | Whose component | Status | Statement |
|---|---|---|---|
| Microsoft 365 commercial tenant | Provider's | Implemented | Staff sign in to their day-to-day work (email, ShopTrak, the SAG-NAS shares) with their own standard Entra account. Nobody uses an administrative account for ordinary work; the two Global Administrator accounts belong to Northstar and are not used by Saguaro staff at all. |

### 3.1.8[a]

| Component | Whose component | Status | Statement |
|---|---|---|---|
| Microsoft 365 commercial tenant | Provider's | Implemented | Accounts are locked after 5 consecutive invalid logon attempts within 15 minutes and remain locked for 30 minutes. [TO BE CONFIRMED: whether this lockout also applies to local accounts on SAG-NAS] |

### 3.1.11[b]

| Component | Whose component | Status | Statement |
|---|---|---|---|
| Microsoft 365 commercial tenant | Provider's | Implemented | Microsoft 365 sign-in sessions expire per the default Entra ID sign-in frequency setting. |
| Windows 11 office endpoints | Company's | Planned | Windows sessions on the endpoints are not automatically terminated; a user who steps away stays signed in until the screen lock engages. |

### 3.1.15[c]

| Component | Whose component | Status | Statement |
|---|---|---|---|
| Northstar Managed IT | Provider's | Planned | Northstar's remote control sessions through the RMM can reach any endpoint without going through the VPN, because the RMM agent runs locally on each machine and calls out to Northstar's cloud service. No Saguaro-side authorization step gates an individual Northstar remote session. |

### 3.3.1[c]

| Component | Whose component | Status | Statement |
|---|---|---|---|
| Microsoft 365 commercial tenant | Provider's | Implemented | The Microsoft 365 unified audit log is enabled by default and records sign-in and administrative activity across Exchange Online, SharePoint, and OneDrive. |
| SAG-NAS | Company's | Planned | SAG-NAS keeps no audit log at all. |
| Shop floor PC | Company's | Planned | SHOP-PC-01 keeps no audit log at all. |
| CMM PC | Company's | Planned | CMM-PC keeps no audit log at all. |

### 3.5.3[c]

| Component | Whose component | Status | Statement |
|---|---|---|---|
| Microsoft 365 commercial tenant | Provider's | Implemented | Northstar's two Global Administrator accounts have MFA enrolled. |

### 3.5.3[d]

| Component | Whose component | Status | Statement |
|---|---|---|---|
| Microsoft 365 commercial tenant | Provider's | Implemented | Multifactor authentication (Microsoft Authenticator) is required by Conditional Access for every user's Microsoft 365 sign-in. |
