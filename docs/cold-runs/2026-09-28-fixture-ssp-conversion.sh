#!/usr/bin/env bash
# The one-time conversion of the fixture engagement's Markdown SSP, asset
# inventory, and responsibility matrix into ssp/ssp.json (#100).
#
# Kept as the record of how the fixture's ssp.json was made; the reasoning is in
# 2026-09-28-fixture-ssp-conversion.md beside it. It was run against a cold-run
# copy, never against docs/fixture/engagement/ (AGENTS.md):
#
#   python3 scripts/cold_run.py --skill fixture-ssp-conversion
#   bash docs/cold-runs/2026-09-28-fixture-ssp-conversion.sh /tmp/poamslayer-cold-runs/<date>-fixture-ssp-conversion
#
# and the resulting ssp/ssp.json, ssp/oscal/, and view/ were reviewed and then
# copied into the fixture. Every change goes through scribe's edit command, so
# every step was validated by oscal-cli with our constraints file.
#
# The record keeps the previous consultant's work as it was left, mistakes
# included: they are the plants the answer key describes. Statement text is
# the Markdown SSP's own sentences, placed on the objective each one speaks to.

set -euo pipefail

ENGAGEMENT="${1:?usage: $0 <cold-run copy of the fixture engagement>}"
REPO="$(cd "$(dirname "$0")/../.." && pwd)"

scribe() {
  python3 "$REPO/skills/flows/scribe/ssp_edit.py" --engagement "$ENGAGEMENT" "$@"
}

scribe create --system-name "Saguaro Precision Machining"

# Components. What the Markdown SSP and the asset inventory name.

scribe add-provider --title "Microsoft 365 commercial tenant" --role csp --fedramp-status none \
  --description "Microsoft 365 Business Premium commercial tenant: Entra ID, Exchange Online, SharePoint, OneDrive, and Intune. The previous consultant never checked the purchased SKU's FedRAMP status, so it is recorded as neither authorized nor equivalent until the FedRAMP Marketplace listing is verified."
scribe add-provider --title "Northstar Managed IT" --role msp \
  --description "Managed IT provider. Holds two Global Administrator accounts in Microsoft 365, builds the Windows endpoints, and runs the RMM that reaches them."
scribe add-component --title "Windows 11 office endpoints" --type hardware \
  --description "Windows 11 Pro desktops and laptops, Entra-joined, one per office user."
scribe add-component --title "Shop floor PC" --type hardware \
  --description "Windows 10 Pro desktop at the Haas machine."
scribe add-component --title "Haas VF-2 CNC mill" --type hardware \
  --description "CNC mill with a Haas NextGen control."
scribe add-component --title "CMM PC" --type hardware \
  --description "Windows 7 PC running the CMM measurement software."
scribe add-component --title "SAG-NAS" --type hardware \
  --description "Network file server holding the Jobs, Quality, and Admin shares."
scribe add-component --title "Front office MFP" --type hardware \
  --description "Color multifunction printer near the front office."
scribe add-component --title "Personal phones" --type hardware \
  --description "Staff-owned phones reading company email, with no MDM."
scribe add-component --title "EdgeRouter firewall and VPN" --type hardware \
  --description "Router and firewall at the internet edge, running the L2TP/IPsec VPN server."
scribe add-component --title "Saguaro Wi-Fi" --type hardware \
  --description "Wi-Fi network, SSID Saguaro, on the office LAN."
scribe add-component --title "Access control procedure" --type policy \
  --description "Northstar's template procedure, policies/access-control-procedure.md."
scribe add-component --title "Media handling policy" --type policy \
  --description "One-page policy, policies/media-handling-policy.md."
scribe add-component --title "Incident response plan" --type plan \
  --description "Northstar's two-page template plan, policies/incident-response-plan.md."
scribe add-component --title "Saguaro operating practices" --type process-procedure \
  --description "How the company works where the previous consultant described a practice without a written policy or a single component behind it."

# Assets. The inventory's rows with the category it was left with. The rows it
# left "not listed" are not recorded: an asset needs a category, and inventing
# one would erase the gap the answer key expects a scoping run to find.

for host in OFFICE-DANA OFFICE-LUIS PROG-TOM QC-MARIA SHIP-JORDAN PURCH-ELLEN ACCT-ROB NADIA-LT; do
  scribe add-asset --name "$host" --component "Windows 11 office endpoints" --category cui-asset \
    --description "Windows 11 Pro, Entra-joined"
done
scribe add-asset --name "ENG-PRIYA" --component "Windows 11 office endpoints" --category cui-asset \
  --description "Windows 11 Pro, Entra-joined, CAD/CAM"
scribe add-asset --name "SHOP-PC-01" --component "Shop floor PC" --category specialized-asset \
  --specialized-type ot --description 'Windows 10 Pro, shared "shop" login'
scribe add-asset --name "Haas VF-2 (NextGen control)" --component "Haas VF-2 CNC mill" --category cui-asset \
  --description "CNC machine"
scribe add-asset --name "CMM-PC" --component "CMM PC" --category contractor-risk-managed-asset \
  --description "Windows 7, runs CMM software"
scribe add-asset --name "SAG-NAS" --component "SAG-NAS" --category cui-asset \
  --description "Jobs, Quality, Admin shares"
scribe add-asset --name "MFP-FRONT" --component "Front office MFP" --category out-of-scope-asset \
  --description "Canon-class color MFP" \
  --remarks "As left by the previous consultant: policy prohibits scanning CUI."
scribe add-asset --name "Personal phones (all staff)" --component "Personal phones" --category out-of-scope-asset \
  --description "Outlook on personal devices" \
  --remarks "As left by the previous consultant, with no reason recorded beyond the note: Outlook on personal devices."

# Statements. One call per objective and component.

st() {
  local objective="$1" component="$2" status="$3" text="$4"
  shift 4
  scribe set-statement --objective "$objective" --component "$component" --status "$status" --statement "$text" "$@"
}

M365="Microsoft 365 commercial tenant"
ENDPOINTS="Windows 11 office endpoints"
PRACTICES="Saguaro operating practices"

# 3.1.1
st "3.1.1[a]" "$M365" implemented "Authorized users are managed in Microsoft Entra ID; the Entra user list is the authorized user list."
st "3.1.1[c]" "$M365" implemented "Devices are authorized by being joined to Entra ID."

# 3.1.2
st "3.1.2[a]" "Access control procedure" implemented "Purchasing and Accounting see their own modules, machinists see the traveler and CAM files relevant to the job in front of them, and Dana Ortiz has full access as owner."
st "3.1.2[b]" "Access control procedure" implemented "Access to ShopTrak, the SAG-NAS shares, and email is limited by job role. SharePoint and OneDrive permissions mirror the same role groups."

# 3.1.3
st "3.1.3[a]" "$PRACTICES" planned "There is no written information flow control policy."
st "3.1.3[b]" "$PRACTICES" planned "No technical control stops CUI from leaving on an email to any external address."
st "3.1.3[c]" "$PRACTICES" implemented "CUI moves from the MeridianLink portal, through Priya Natarajan's engineering package, into the traveler and g-code, out to Sonoran Anodize and Plating by email, and back through Maria Chen's First Article Inspection report."
st "3.1.3[e]" "$PRACTICES" planned "The FAI report has been scanned to a personal Gmail address on at least one occasion, and the drawing is emailed to the finisher as a matter of course."

# 3.1.4
st "3.1.4[b]" "$PRACTICES" implemented "Saguaro is a twelve-person shop with limited separation of duties. Ellen Park issues purchase orders and Rob Castellano pays them; Dana Ortiz personally reviews the bank statement each month, which is the only separation control in place for financial transactions. Engineering (Priya Natarajan), programming (Tom Reyes), and machining (Kevin Marsh, Ana Delgado, Sam Whitfield) are separate people performing separate steps of the same job."

# 3.1.5
st "3.1.5[a]" "$M365" implemented "Only Dana Ortiz and the two Northstar Global Administrator accounts hold administrative rights in Microsoft 365."
st "3.1.5[b]" "$ENDPOINTS" implemented "Local administrator rights on the Windows endpoints belong to Northstar's build account; end users are standard users on their own machines."

# 3.1.6
st "3.1.6[b]" "$M365" implemented "Staff sign in to their day-to-day work (email, ShopTrak, the SAG-NAS shares) with their own standard Entra account. Nobody uses an administrative account for ordinary work; the two Global Administrator accounts belong to Northstar and are not used by Saguaro staff at all."

# 3.1.7
st "3.1.7[c]" "$ENDPOINTS" implemented "Standard users cannot install software or change system settings on their own Windows 11 endpoints; Windows UAC blocks privileged actions and prompts for elevation."
st "3.1.7[d]" "$ENDPOINTS" implemented "Local Windows event logs record UAC elevation attempts, subject to the 20 MB local rollover described under 3.3.1."

# 3.1.8: the lockout values contradict the access control procedure, and the
# open item sits inside the statement. Both are plants (answer key 6.10).
st "3.1.8[a]" "$M365" implemented "Accounts are locked after 5 consecutive invalid logon attempts within 15 minutes and remain locked for 30 minutes. [TO BE CONFIRMED: whether this lockout also applies to local accounts on SAG-NAS]"

# 3.1.9
st "3.1.9[a]" "$ENDPOINTS" planned "No additional CUI-specific privacy or security notice has been drafted or deployed."
st "3.1.9[b]" "$ENDPOINTS" implemented "The Windows sign-in screen on every endpoint displays the standard Microsoft 365 organizational sign-in notice."

# 3.1.10
st "3.1.10[a]" "$ENDPOINTS" implemented "Windows 11 endpoints lock the screen after 10 minutes of inactivity."
st "3.1.10[b]" "$ENDPOINTS" implemented "Windows 11 endpoints lock the screen after 10 minutes of inactivity."
st "3.1.10[b]" "Shop floor PC" planned "SHOP-PC-01 does not have a lock screen policy configured; it relies on the physical layout of the shop floor."
st "3.1.10[b]" "CMM PC" planned "CMM-PC does not have a lock screen policy configured; it relies on the physical layout of the shop floor."
st "3.1.10[c]" "$ENDPOINTS" implemented "The lock screen hides the desktop content."

# 3.1.11
st "3.1.11[b]" "$M365" implemented "Microsoft 365 sign-in sessions expire per the default Entra ID sign-in frequency setting."
st "3.1.11[b]" "$ENDPOINTS" planned "Windows sessions on the endpoints are not automatically terminated; a user who steps away stays signed in until the screen lock engages."

# 3.1.12
st "3.1.12[a]" "EdgeRouter firewall and VPN" implemented "Dana Ortiz's only user remote access path is the EdgeRouter's L2TP/IPsec VPN from her home PC, followed by an RDP session into OFFICE-DANA."
st "3.1.12[b]" "EdgeRouter firewall and VPN" implemented "The VPN is the only remote access method in use by Saguaro staff. Northstar's remote control sessions through the RMM are a separate access path and are treated under 3.1.20 and the ESP scoping decision, not here."

# 3.1.13
st "3.1.13[b]" "EdgeRouter firewall and VPN" implemented "The L2TP/IPsec VPN tunnel that Dana Ortiz uses encrypts traffic between her home PC and the EdgeRouter."
st "3.1.13[b]" "$ENDPOINTS" implemented "The RDP session from Dana Ortiz's home PC into OFFICE-DANA, once inside the tunnel, uses Windows' default RDP encryption."

# 3.1.14
st "3.1.14[a]" "EdgeRouter firewall and VPN" implemented "The only remote access control point is the EdgeRouter's VPN server."
st "3.1.14[b]" "EdgeRouter firewall and VPN" implemented "Every remote session from a Saguaro user passes through the EdgeRouter's VPN server before reaching any endpoint."

# 3.1.15
st "3.1.15[c]" "Northstar Managed IT" planned "Northstar's remote control sessions through the RMM can reach any endpoint without going through the VPN, because the RMM agent runs locally on each machine and calls out to Northstar's cloud service. No Saguaro-side authorization step gates an individual Northstar remote session."

# 3.1.16
st "3.1.16[a]" "Saguaro Wi-Fi" implemented 'The Wi-Fi network "Saguaro" was set up by Northstar when the office was built out.'
st "3.1.16[b]" "Saguaro Wi-Fi" planned "No separate authorization step exists for a new device joining Wi-Fi beyond knowing the WPA2-PSK password on the break room sticky note."

# 3.1.17
st "3.1.17[a]" "Saguaro Wi-Fi" implemented "Wi-Fi uses WPA2-PSK for authentication. The same SSID and password serve staff and guests alike."
st "3.1.17[b]" "Saguaro Wi-Fi" implemented "Wi-Fi uses WPA2-PSK for encryption. The same SSID and password serve staff and guests alike."

# 3.1.18
st "3.1.18[b]" "Personal phones" planned "No mobile device management is deployed. Personal phones connect to Exchange Online through the built-in mail app over the carrier data connection or the office Wi-Fi."

# 3.1.19
st "3.1.19[b]" "Personal phones" partial "CUI is not stored at rest on personal phones as a matter of design, but attachments received in Outlook on a personal phone are not encrypted by any Saguaro-controlled mechanism beyond the phone's own device encryption."

# 3.1.20: the claim the answer key marks wrong (6.3).
st "3.1.20[a]" "$PRACTICES" not-applicable "Saguaro does not connect to external systems." \
  --remarks "As left by the previous consultant, whose SSP gives no reason beyond the claim itself."
st "3.1.20[b]" "$PRACTICES" not-applicable "Saguaro does not connect to external systems." \
  --remarks "As left by the previous consultant, whose SSP gives no reason beyond the claim itself."

# 3.1.21
st "3.1.21[a]" "$PRACTICES" implemented "The USB stick used to carry g-code from PROG-TOM to SHOP-PC-01 is used entirely within the Saguaro network; none of Saguaro's portable storage devices are used with an external system."

# 3.1.22
st "3.1.22[a]" "$PRACTICES" not-applicable "Saguaro does not operate a publicly accessible information system." \
  --remarks "The company website is static marketing content with no CUI and no upload capability."

# 3.3.1
st "3.3.1[c]" "$M365" implemented "The Microsoft 365 unified audit log is enabled by default and records sign-in and administrative activity across Exchange Online, SharePoint, and OneDrive."
st "3.3.1[c]" "SAG-NAS" planned "SAG-NAS keeps no audit log at all."
st "3.3.1[c]" "Shop floor PC" planned "SHOP-PC-01 keeps no audit log at all."
st "3.3.1[c]" "CMM PC" planned "CMM-PC keeps no audit log at all."
st "3.3.1[f]" "$ENDPOINTS" partial "Windows event logs on the eight office endpoints stay local with a 20 MB rollover and are not centrally collected. There is no SIEM and no scheduled log review."

# 3.5.3: the MFA claim that misses SMB access to SAG-NAS (6.3).
st "3.5.3[c]" "$M365" implemented "Northstar's two Global Administrator accounts have MFA enrolled."
st "3.5.3[d]" "$M365" implemented "Multifactor authentication (Microsoft Authenticator) is required by Conditional Access for every user's Microsoft 365 sign-in."

# 3.6.3
st "3.6.3[a]" "Incident response plan" planned "Northstar supplied a two-page incident response plan template, stored at policies/incident-response-plan.md. The plan has never been exercised; no tabletop exercise or test has been scheduled or recorded."

# 3.8.4
st "3.8.4[a]" "Media handling policy" planned 'CUI leaves Saguaro on USB sticks, printed drawings, printed travelers, and the weekly backup drive. None of these carry a CUI marking. policies/media-handling-policy.md says media containing CUI "should be labeled" but gives no procedure for doing so.'
st "3.8.4[b]" "Media handling policy" planned "CUI leaves Saguaro on USB sticks, printed drawings, printed travelers, and the weekly backup drive. None of these carry a distribution limitation."

# 3.12.4
st "3.12.4[b]" "$PRACTICES" implemented "The system boundary for this SSP is the Saguaro office network and Microsoft 365."

# 3.13.11: the FIPS claim the answer key marks wrong (6.3).
st "3.13.11[a]" "$PRACTICES" implemented "All CUI at rest is protected by BitLocker and in transit by TLS."
