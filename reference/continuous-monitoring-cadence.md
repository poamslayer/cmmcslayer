> **Provenance.** Derived from the "Continuous Monitoring Plan" Excel template, version 1.0, dated 2023-02-16, published by Haight Bey & Associates dba Totem Technologies (https://www.totem.tech/) under the MIT License. The 51 monitoring activities, their control mappings, frequencies, and probable responsibility owners are reproduced from the "Monitoring Requirements" sheet without change; the template's organization placeholders and date columns are omitted. The full licence text from the template's "License" sheet is reproduced at the end of this file, as the licence requires.

# Continuous monitoring cadence: 51 recurring activities

Each row is one recurring activity. "Probable responsibility" is the template's suggested owner: OSC (the organization itself), MSP, MSSP, CSP, Other ESP, or Shared. The template marks a subset of rows as CMMC Level 1 requirements; that colour coding is not reproduced here.

| # | Monitoring activity | Control mapping | Description | Frequency | Probable responsibility |
|---|---|---|---|---|---|
| 1 | Information System Monitoring | 3.12.3 | Monitors the system in accordance with 3.12.3 control requirements. | Ongoing | OSC |
| 2 | Analyze Event Logs and SIEM | AU family | Monitor required events | Ongoing | MSSP |
| 3 | Information System Component Inventory | 3.4.1 | Automated or manual detection of new assets | Ongoing | MSP |
| 4 | Incident Response | 3.6.1 | Incident reporting and tracking | Ongoing | Shared |
| 5 | Incident Reporting | 3.6.2 | Incident reporting and tracking | As Required | OSC |
| 6 | Incident Information Storage | DFARS 252.204-7012 | Preserve media images and packet capture / monitoring information related to CUI incidents | As Required | Shared |
| 7 | Vulnerability Scanning | 3.11.2 | Update list of vulnerabilities and execute automated credentialed scans | Monthly | Shared |
| 8 | Network Traffic Analysis and Intrusion Detection | 3.14.6 | Monitors for unauthorized wireless connection points | Weekly | MSSP |
| 9 | Configuration Management | 3.4.1 | Identify and manage configuration items | Ongoing | Shared |
| 10 | Vulnerability Scanning | 3.11.3 | Provide reports to Security Officer showing high-risk vulnerabilities have been mitigated in 30 days and moderate risk-vulnerabilities as soon as possible | Weekly | MSSP |
| 11 | Access Records | 3.10.3; 3.10.4 | Review visitor access records | Monthly | OSC |
| 12 | Least Functionality | 3.4.7 | Identify and eliminate unnecessary functions, ports, protocols, and/or services | 90 Days | MSP |
| 13 | OS and Software Patching | 3.11.3; 3.14.1 | Install security-relevant software and firmware updates within 30 days of the release of the updates. | Monthly | MSP |
| 14 | Component Hardening | 3.4.2 | Automated and/or manual scans for component deviation from security baselines | Annually | MSP |
| 15 | Antimalware scans | 3.14.5 | Perform component antimalware scans | Ongoing | MSP |
| 16 | Antimalware scans -- New/External Removable Media | 3.7.4 | Perform antimalware scan on all new/external removable media (e.g. firmware upgrade USB, diagnostic/maintenance laptop, test tools, DVD supplied by client with files) | As Required | OSC |
| 17 | Account Management | n/a | Automatic termination of temporary and emergency accounts after no more than 30 days. | Monthly | MSP |
| 18 | Plan of Action & Milestones | 3.12.2 | Update as monthly and submit to Security Officer | Monthly | OSC |
| 19 | Monitoring Physical Access | 3.10.4 | Review physical access logs and record date in SSP | Monthly | OSC |
| 20 | Authenticator Management | n/a | Change/refresh passwords | Annually | MSP |
| 21 | Account Management | 3.5.5 | Disable user IDs after 30 days inactivity | Monthly | MSP |
| 22 | Publicly Accessible Content | 3.1.22 | Review content on publicly accessible system and look for non-public information. | 90 Days | OSC |
| 23 | Access Restrictions for Change | 3.1.5; 3.4.5 | Review and reevaluate their information system developer/integrator privileges quarterly. | 90 Days | MSP |
| 24 | Account Management | 3.1.1 | Review and re-authorize user accounts and record date in SSP | Annually | OSC |
| 25 | Auditable Events | 3.3.3 | Review and update auditable events and record changes and date in SSP | Annually | OSC |
| 26 | Security Impact Analysis (SIA) | 3.4.4 | Assess and capture security impact of proposed configuration changes | As Required | OSC |
| 27 | Security Assessments -- Change Management | 3.4.4 | Assess subset of security controls as triggered by SIA | As Required | OSC |
| 28 | Penetration Testing | n/a | Conduct skilled penetration test of organization | Annually | Shared |
| 29 | Baseline Configuration and System Component Inventory | 3.4.1 | Reviews and update baseline configuration annually or during installations and updates | Annually | MSP |
| 30 | Configuration Management Plan | NFO | Review and update | Annually | OSC |
| 31 | Disaster Recovery Plan | n/a | Review and update, including recovery metrics | Annually | OSC |
| 32 | Disaster Recovery Training | n/a | Train personnel in contingency roles and responsibilities and record date in SSP | Annually | OSC |
| 33 | Information System Restoration from Backup | n/a | Test backups to verify integrity and reliability and record date in SSP | Annually | MSP |
| 34 | Incident Response Exercise | 3.6.3 | Conduct incident response training and record date, training materials and participants in SSP | Annually | Shared |
| 35 | Incident Response Plan | 3.6.1 | Review and update, including recovery metrics | Annually | OSC |
| 36 | Physical Access Authorizations | 3.10.1 | Review physical access authorization credential and record date and who performed it in SSP | Annually | OSC |
| 37 | Physical Access Control -- Access Device Inventory | 3.10.5 | Inventory physical access devices annually and record date in SSP | Annually | OSC |
| 38 | Physical Access Control -- Change Combinations and Keys | 3.9.2 | Change combinations and keys when personnel leave and record date and name of responsible person in SSP | As Required | OSC |
| 39 | System Security Plan | 3.12.4 | Review and update | Annually | OSC |
| 40 | External Access and Service Level Agreements | NFO | Review and update and record date in SSP | Annually | OSC |
| 41 | Boundary Protection | 3.13.1; 3.13.6; 3.14.6 | Review firewall rules and remove traffic flow that is no longer supported by business/mission need | Annually | MSP |
| 42 | Security Training -- Annual | AT family | Annual security awareness --including insider threat-- and role-based training | Annually | OSC |
| 43 | Security Training -- On-boarding | AT family | Conduct security awareness  --including insider threat-- and role-based training for new personnel | As Required | OSC |
| 44 | Security Awareness Training Records | AT family | Archive training records | Annually | OSC |
| 45 | Identifier Management | 3.5.5 | Ensure usernames or other identifiers have not been reused | Every Two Years | MSP |
| 46 | Security Control Self-Assessment | 3.12.1 | Conduct annual self-assessment of security controls (CMMC L1-L3) | Annually | OSC |
| 47 | Third-party Security Control Assessment | 3.12.1 | Conduct C3PAO (CMMC L2) or DIBCAC (CMMC L3) re-certification and document in SSP | Every Three Years | OSC |
| 48 | Risk Assessment | 3.11.1 | Review and update risk assessments and record date in SSP, at least annually or as triggered by criteria defined in 3.11.1 | Annually | OSC |
| 49 | Personnel Screening | 3.9.1 | Conduct background checks on all new staff | As Required | Shared |
| 50 | Media Sanitization / Disposal | 3.7.3; 3.8.3 | Sanitize and dispose of media/equipment in accordance with NIST 800-88 | As Required | OSC |
| 51 | Ensure CSP maintain FedRAMP Authorization | DFARS 252.204-7012 | Any CSP that handle your CUI must maintain FedRAMP Moderate authorization or equivalent | Every Three Years | OSC |

Total activities: 51.

## By frequency

- **Ongoing** (6): Information System Monitoring; Analyze Event Logs and SIEM; Information System Component Inventory; Incident Response; Configuration Management; Antimalware scans
- **Weekly** (2): Network Traffic Analysis and Intrusion Detection; Vulnerability Scanning
- **Monthly** (7): Vulnerability Scanning; Access Records; OS and Software Patching; Account Management; Plan of Action & Milestones; Monitoring Physical Access; Account Management
- **90 Days** (3): Least Functionality; Publicly Accessible Content; Access Restrictions for Change
- **Annually** (21): Component Hardening; Authenticator Management; Account Management; Auditable Events; Penetration Testing; Baseline Configuration and System Component Inventory; Configuration Management Plan; Disaster Recovery Plan; Disaster Recovery Training; Information System Restoration from Backup; Incident Response Exercise; Incident Response Plan; Physical Access Authorizations; Physical Access Control -- Access Device Inventory; System Security Plan; External Access and Service Level Agreements; Boundary Protection; Security Training -- Annual; Security Awareness Training Records; Security Control Self-Assessment; Risk Assessment
- **Every Two Years** (1): Identifier Management
- **Every Three Years** (2): Third-party Security Control Assessment; Ensure CSP maintain FedRAMP Authorization
- **As Required** (9): Incident Reporting; Incident Information Storage; Antimalware scans -- New/External Removable Media; Security Impact Analysis (SIA); Security Assessments -- Change Management; Physical Access Control -- Change Combinations and Keys; Security Training -- On-boarding; Personnel Screening; Media Sanitization / Disposal

## Licence (from the template's License sheet)

The MIT License

Continuous Monitoring Plan ©2023 Haight Bey & Associates dba Totem Technologies https://www.totem.tech

Permission is hereby granted, free of charge, to any person obtaining a copy of this document and associated documentation files (the "Document"), to deal in the Document without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Document, and to permit persons to whom the Document is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Document.

THE DOCUMENT IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE DOCUMENT OR THE USE OR OTHER DEALINGS IN THE DOCUMENT.

