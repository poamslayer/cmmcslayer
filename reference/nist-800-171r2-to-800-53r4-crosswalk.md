> **Provenance.** NIST SP 800-171 Rev 2, Appendix D, Tables D-1 through D-14 (Mapping Tables), reproduced from the NIST publication at https://csrc.nist.gov/pubs/sp/800/171/r2/upd1/final. Work of the United States Government, public domain (17 U.S.C. 105). Blank cells and asterisks are faithful to the source. Transcribed into Markdown; no content changed.

# NIST 800-171 → 800-53 / ISO 27001 Mapping (Appendix D)

Reproduction of **Appendix D (Tables D-1 through D-14)** of NIST SP 800-171 Rev 2, which maps each of the 110 CUI security requirements to the **NIST SP 800-53 Rev 4** security controls that back it, plus a secondary mapping to **ISO/IEC 27001** Annex A controls.

> [!note] "FedRAMP → 800-171" — what this actually is
> This appendix does **not** map FedRAMP directly. It maps 800-171 requirements to **SP 800-53 Rev 4** controls. The FedRAMP connection is one hop away: FedRAMP baselines (Low/Moderate/High) are themselves selections of 800-53 controls, so the 800-53 column is the bridge between a FedRAMP authorization boundary and an 800-171 requirement.

> [!warning] How to read these tables
> - The mapping is **informational** — per NIST, it imparts no requirements beyond Chapter 3, and only the portion of each 800-53 control relevant to protecting CUI applies.
> - **Blank 800-53 cells are faithful to the source.** Where a requirement's control column shows "—", NIST left it blank in the original table (the neighbouring requirements' controls cover it).
> - Controls are listed against the requirement row where NIST prints the control ID; some control cells visually span adjacent requirements in the PDF.
> - An **asterisk (\*)** on an ISO code means the ISO/IEC control does **not** fully satisfy the intent of the NIST control.
> - 800-53 controls are from **Revision 4** (per NIST's footnote, pending an update to Rev 5 / SP 800-53B).

### Table D-1 — 3.1 Access Control

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.1.1** — Limit system access to authorized users, processes acting on behalf of authorized users, and devices (including other systems). | `AC-2` Account Management | A.9.2.1, A.9.2.2, A.9.2.3, A.9.2.5, A.9.2.6 |
| **3.1.2** — Limit system access to the types of transactions and functions that authorized users are permitted to execute. | `AC-3` Access Enforcement<br>`AC-17` Remote Access | A.6.2.2, A.9.1.2, A.9.4.1, A.9.4.4, A.9.4.5, A.13.1.1, A.14.1.2, A.14.1.3, A.18.1.3, A.6.2.1, A.13.2.1 |
| **3.1.3** — Control the flow of CUI in accordance with approved authorizations. | `AC-4` Information Flow Enforcement | A.13.1.3, A.13.2.1, A.14.1.2, A.14.1.3 |
| **3.1.4** — Separate the duties of individuals to reduce the risk of malevolent activity without collusion. | `AC-5` Separation of Duties | A.6.1.2 |
| **3.1.5** — Employ the principle of least privilege, including for specific security functions and privileged accounts. | `AC-6` Least Privilege<br>`AC-6(1)` Least Privilege Authorize Access to Security Functions<br>`AC-6(5)` Least Privilege Privileged Accounts | A.9.1.2, A.9.2.3, A.9.4.4, A.9.4.5 |
| **3.1.6** — Use non-privileged accounts or roles when accessing nonsecurity functions. | `AC-6(2)` Least Privilege Non-Privileged Access for Nonsecurity Functions | — |
| **3.1.7** — Prevent non-privileged users from executing privileged functions and capture the execution of such functions in audit logs. | `AC-6(9)` Least Privilege Log Use of Privileged Functions<br>`AC-6(10)` Least Privilege Prohibit Non-Privileged Users from Executing Privileged Functions | — |
| **3.1.8** — Limit unsuccessful logon attempts. | `AC-7` Unsuccessful Logon Attempts | A.9.4.2 |
| **3.1.9** — Provide privacy and security notices consistent with applicable CUI rules. | `AC-8` System Use Notification | A.9.4.2 |
| **3.1.10** — Use session lock with pattern-hiding displays to prevent access and viewing of data after a period of inactivity. | `AC-11` Session Lock<br>`AC-11(1)` Session Lock Pattern-Hiding Displays | A.11.2.8, A.11.2.9 |
| **3.1.11** — Terminate (automatically) a user session after a defined condition. | `AC-12` Session Termination | — |
| **3.1.12** — Monitor and control remote access sessions. | `AC-17(1)` Remote Access Automated Monitoring / Control | — |
| **3.1.13** — Employ cryptographic mechanisms to protect the confidentiality of remote access sessions. | `AC-17(2)` Remote Access Protection of Confidentiality / Integrity Using Encryption | — |
| **3.1.14** — Route remote access via managed access control points. | `AC-17(3)` Remote Access Managed Access Control Points | — |
| **3.1.15** — Authorize remote execution of privileged commands and remote access to security-relevant information. | `AC-17(4)` Remote Access Privileged Commands / Access | — |
| **3.1.16** — Authorize wireless access prior to allowing such connections. | `AC-18` Wireless Access | A.6.2.1, A.13.1.1, A.13.2.1 |
| **3.1.17** — Protect wireless access using authentication and encryption. | `AC-18(1)` Wireless Access Authentication and Encryption | — |
| **3.1.18** — Control connection of mobile devices. | `AC-19` Access Control for Mobile Devices | A.6.2.1, A.11.2.6, A.13.2.1 |
| **3.1.19** — Encrypt CUI on mobile devices and mobile computing platforms. | `AC-19(5)` Access Control for Mobile Devices Full Device / Container-Based Encryption | — |
| **3.1.20** — Verify and control/limit connections to and use of external systems. | `AC-20` Use of External Systems<br>`AC-20(1)` Use of External Systems Limits on Authorized Use | A.11.2.6, A.13.1.1, A.13.2.1 |
| **3.1.21** — Limit use of portable storage devices on external systems. | `AC-20(2)` Use of External Systems Portable Storage Devices | — |
| **3.1.22** — Control CUI posted or processed on publicly accessible systems. | `AC-22` Publicly Accessible Content | — |

### Table D-2 — 3.2 Awareness and Training

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.2.1** — Ensure that managers, systems administrators, and users of organizational systems are made aware of the security risks associated with their activities and of the applicable policies, standards, and procedures related to the security of those systems. | `AT-2` Security Awareness Training<br>`AT-3` Role-Based Security Training | A.7.2.2, A.12.2.1, A.7.2.2* |
| **3.2.2** — Ensure that personnel are trained to carry out their assigned information security-related duties and responsibilities. | — | — |
| **3.2.3** — Provide security awareness training on recognizing and reporting potential indicators of insider threat. | `AT-2(2)` Security Awareness Training Insider Threat | — |

### Table D-3 — 3.3 Audit and Accountability

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.3.1** — Create and retain system audit logs and records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity. | `AU-2` Event Logging<br>`AU-3` Content of Audit Records<br>`AU-3(1)` Content of Audit Records Additional Audit | A.12.4.1* |
| **3.3.2** — Ensure that the actions of individual system users can be uniquely traced to those users, so they can be held accountable for their actions. | `AU-6` Audit Record Review, Analysis, and Reporting<br>`AU-11` Audit Record Retention<br>`AU-12` Audit Record Generation | A.12.4.1, A.16.1.2, A.16.1.4, A.12.4.3, A.16.1.7 |
| **3.3.3** — Review and update logged events. | `AU-2(3)` Event Logging Review and Updates | — |
| **3.3.4** — Alert in the event of an audit logging process failure. | `AU-5` Response to Audit Logging Process Failures | — |
| **3.3.5** — Correlate audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity. | `AU-6(3)` Audit Record Review, Analysis, and Reporting Correlate Audit Record Repositories | — |
| **3.3.6** — Provide audit record reduction and report generation to support on-demand analysis and reporting. | `AU-7` Audit Record Reduction and Report Generation | — |
| **3.3.7** — Provide a system capability that compares and synchronizes internal system clocks with an authoritative source to generate time stamps for audit records. | `AU-8` Time Stamps<br>`AU-8(1)` Time Stamps Synchronization with Authoritative Time Source | A.12.4.4 |
| **3.3.8** — Protect audit information and audit logging tools from unauthorized access, modification, and deletion. | `AU-9` Protection of Audit Information | A.12.4.2, A.12.4.3, A.18.1.3 |
| **3.3.9** — Limit management of audit logging functionality to a subset of privileged users. | `AU-9(4)` Protection of Audit Information Access by Subset of Privileged Users | — |

### Table D-4 — 3.4 Configuration Management

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.4.1** — Establish and maintain baseline configurations and inventories of organizational systems (including hardware, software, firmware, and documentation) throughout the respective system development life cycles. | `CM-2` Baseline Configuration<br>`CM-6` Configuration Settings<br>`CM-8` System Component Inventory<br>`CM-8(1)` System Component Inventory Updates During | A.8.1.1, A.8.1.2 |
| **3.4.2** — Establish and enforce security configuration settings for information technology products employed in organizational systems. | — | — |
| **3.4.3** — Track, review, approve or disapprove, and log changes to organizational systems. | `CM-3` Configuration Change Control | A.12.1.2, A.14.2.2, A.14.2.3, A.14.2.4 |
| **3.4.4** — Analyze the security impact of changes prior to implementation. | `CM-4` Security Impact Analysis | A.14.2.3 |
| **3.4.5** — Define, document, approve, and enforce physical and logical access restrictions associated with changes to organizational systems. | `CM-5` Access Restrictions for Change | A.9.2.3, A.9.4.5, A.12.1.2, A.12.1.4, A.12.5.1 |
| **3.4.6** — Employ the principle of least functionality by configuring organizational systems to provide only essential capabilities. | `CM-7` Least Functionality | A.12.5.1* |
| **3.4.7** — Restrict, disable, or prevent the use of nonessential programs, functions, ports, protocols, and services. | `CM-7(1)` Least Functionality Periodic Review<br>`CM-7(2)` Least Functionality Prevent program execution | — |
| **3.4.8** — Apply deny-by-exception (blacklisting) policy to prevent the use of unauthorized software or deny-all, permit-by-exception (whitelisting) policy to allow the execution of authorized software. | `CM-7(4)` Least Functionality Unauthorized Software / Blacklisting<br>`CM-7(5)` Least Functionality Authorized Software / Whitelisting | — |
| **3.4.9** — Control and monitor user-installed software. | `CM-11` User-Installed Software | A.12.5.1, A.12.6.2 |

### Table D-5 — 3.5 Identification and Authentication

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.5.1** — Identify system users, processes acting on behalf of users, and devices. | `IA-2` Identification and Authentication (Organizational Users) | A.9.2.1 |
| **3.5.2** — Authenticate (or verify) the identities of users, processes, or devices, as a prerequisite to allowing access to organizational systems. | `IA-3` Device Identification and Authentication<br>`IA-5` Authenticator Management | A.9.2.1, A.9.2.4, A.9.3.1, A.9.4.3 |
| **3.5.3** — Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts. | `IA-2(1)` Identification and Authentication (Organizational Users) Network Access to Privileged Accounts<br>`IA-2(2)` Identification and Authentication (Organizational Users) Network Access to Non-Privileged Accounts<br>`IA-2(3)` Identification and Authentication (Organizational Users) Local Access to Privileged Accounts | — |
| **3.5.4** — Employ replay-resistant authentication mechanisms for network access to privileged and non-privileged accounts. | `IA-2(8)` Identification and Authentication (Organizational Users) Network Access to Privileged Accounts-Replay Resistant<br>`IA-2(9)` Identification and Authentication (Organizational Users) Network Access to Non-Privileged Accounts-Replay Resistant | — |
| **3.5.5** — Prevent reuse of identifiers for a defined period. | `IA-4` Identifier Management | A.9.2.1 |
| **3.5.6** — Disable identifiers after a defined period of inactivity. | `IA-4` Identifier Management | A.9.2.1 |
| **3.5.7** — Enforce a minimum password complexity and change of characters when new passwords are created. | `IA-5(1)` Authenticator Management Password-Based Authentication | — |
| **3.5.8** — Prohibit password reuse for a specified number of generations. | — | — |
| **3.5.9** — Allow temporary password use for system logons with an immediate change to a permanent password. | — | — |
| **3.5.10** — Store and transmit only cryptographically-protected passwords. | — | — |
| **3.5.11** — Obscure feedback of authentication information. | `IA-6` Authenticator Feedback | A.9.4.2 |

### Table D-6 — 3.6 Incident Response

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.6.1** — Establish an operational incident-handling capability for organizational systems that includes preparation, detection, analysis, containment, recovery, and user response activities. | `IR-2` Incident Response Training<br>`IR-4` Incident Handling | A.7.2.2*, A.16.1.4, A.16.1.5, A.16.1.6 |
| **3.6.2** — Track, document, and report incidents to designated officials and/or authorities both internal and external to the organization. | `IR-5` Incident Monitoring<br>`IR-6` Incident Reporting<br>`IR-7` Incident Response Assistance | A.6.1.3, A.16.1.2 |
| **3.6.3** — Test the organizational incident response capability. | `IR-3` Incident Response Testing | — |

### Table D-7 — 3.7 Maintenance

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.7.1** — Perform maintenance on organizational systems. | `MA-2` Controlled Maintenance | A.11.2.4*, A.11.2.5* |
| **3.7.2** — Provide controls on the tools, techniques, mechanisms, and personnel used to conduct system maintenance. | `MA-3` Maintenance Tools<br>`MA-3(1)` Maintenance Tools Inspect Tools<br>`MA-3(2)` Maintenance Tools Inspect Media | — |
| **3.7.3** — Ensure equipment removed for off-site maintenance is sanitized of any CUI. | `MA-2` Controlled Maintenance | A.11.2.4*, A.11.2.5* |
| **3.7.4** — Check media containing diagnostic and test programs for malicious code before the media are used in organizational systems. | `MA-3(2)` Maintenance Tools Inspect Media | — |
| **3.7.5** — Require multifactor authentication to establish nonlocal maintenance sessions via external network connections and terminate such connections when nonlocal maintenance is complete. | `MA-4` Nonlocal Maintenance | — |
| **3.7.6** — Supervise the maintenance activities of maintenance personnel without required access authorization. | `MA-5` Maintenance Personnel | — |

### Table D-8 — 3.8 Media Protection

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.8.1** — Protect (i.e., physically control and securely store) system media containing CUI, both paper and digital. | `MP-2` Media Access | A.8.2.3, A.8.3.1, A.11.2.9 |
| **3.8.2** — Limit access to CUI on system media to authorized users. | `MP-4` Media Storage | A.8.2.3, A.8.3.1, A.11.2.9 |
| **3.8.3** — Sanitize or destroy system media containing CUI before disposal or release for reuse. | `MP-6` Media Sanitization | A.8.2.3, A.8.3.1, A.8.3.2, A.11.2.7 |
| **3.8.4** — Mark media with necessary CUI markings and distribution limitations. | `MP-3` Media Marking | A.8.2.2 |
| **3.8.5** — Control access to media containing CUI and maintain accountability for media during transport outside of controlled areas. | `MP-5` Media Transport | A.8.2.3, A.8.3.1, A.8.3.3, A.11.2.5, A.11.2.6 |
| **3.8.6** — Implement cryptographic mechanisms to protect the confidentiality of CUI stored on digital media during transport unless otherwise protected by alternative physical safeguards. | `MP-5(4)` Media Transport Cryptographic Protection | — |
| **3.8.7** — Control the use of removable media on system components. | `MP-7` Media Use | A.8.2.3, A.8.3.1 |
| **3.8.8** — Prohibit the use of portable storage devices when such devices have no identifiable owner. | `MP-7(1)` Media Use Prohibit Use Without Owner | — |
| **3.8.9** — Protect the confidentiality of backup CUI at storage locations. | `CP-9` System Backup | A.12.3.1, A.17.1.2, A.18.1.3 |

### Table D-9 — 3.9 Personnel Security

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.9.1** — Screen individuals prior to authorizing access to organizational systems containing CUI. | `PS-3` Personnel Screening<br>`PS-4` Personnel Termination | A.7.1.1, A.7.3.1, A.8.1.4 |
| **3.9.2** — Ensure that organizational systems containing CUI are protected during and after personnel actions such as terminations and transfers. | `PS-5` Personnel Transfer | A.7.3.1, A.8.1.4 |

### Table D-10 — 3.10 Physical Protection

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.10.1** — Limit physical access to organizational systems, equipment, and the respective operating environments to authorized individuals. | `PE-2` Physical Access Authorizations<br>`PE-4` Access Control for Transmission Medium<br>`PE-5` Access Control for | A.11.1.2*, A.11.1.2, A.11.2.3, A.11.1.3 |
| **3.10.2** — Protect and monitor the physical facility and support infrastructure for organizational systems. | `PE-6` Monitoring Physical Access | — |
| **3.10.3** — Escort visitors and monitor visitor activity. | `PE-3` Physical Access Control | A.11.1.1, A.11.1.2, A.11.1.3 |
| **3.10.4** — Maintain audit logs of physical access. | — | — |
| **3.10.5** — Control and manage physical access devices. | — | — |
| **3.10.6** — Enforce safeguarding measures for CUI at alternate work sites. | `PE-17` Alternate Work Site | A.6.2.2, A.11.2.6, A.13.2.1 |

### Table D-11 — 3.11 Risk Assessment

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.11.1** — Periodically assess the risk to organizational operations (including mission, functions, image, or reputation), organizational assets, and individuals, resulting from the operation of organizational systems and the associated processing, storage, or transmission of CUI. | `RA-3` Risk Assessment | A.12.6.1* |
| **3.11.2** — Scan for vulnerabilities in organizational systems and applications periodically and when new vulnerabilities affecting those systems and applications are identified. | `RA-5` Vulnerability Scanning<br>`RA-5(5)` Vulnerability Scanning Privileged Access | A.12.6.1* |
| **3.11.3** — Remediate vulnerabilities in accordance with risk assessments. | `RA-5` Vulnerability Scanning | A.12.6.1* |

### Table D-12 — 3.12 Security Assessment

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.12.1** — Periodically assess the security controls in organizational systems to determine if the controls are effective in their application. | `CA-2` Security Assessments | A.14.2.8, A.18.2.2, A.18.2.3 |
| **3.12.2** — Develop and implement plans of action designed to correct deficiencies and reduce or eliminate vulnerabilities in organizational systems. | `CA-5` Plan of Action and Milestones<br>`CA-7` Continuous Monitoring<br>`PL-2` System Security Plan | A.6.1.2 |
| **3.12.3** — Monitor security controls on an ongoing basis to ensure the continued effectiveness of the controls. | — | — |
| **3.12.4** — Develop, document, and periodically update system security plans that describe system boundaries, system environments of operation, how security requirements are implemented, and the relationships with or connections to other systems. | — | — |

### Table D-13 — 3.13 System and Communications Protection

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.13.1** — Monitor, control, and protect communications (i.e., information transmitted or received by organizational systems) at the external boundaries and key internal boundaries of organizational systems. | `SC-7` Boundary Protection | A.13.1.1, A.13.1.3, A.13.2.1, A.14.1.3 |
| **3.13.2** — Employ architectural designs, software development techniques, and systems engineering principles that promote effective information security within organizational systems. | `SA-8` Security Engineering Principles | A.14.2.5 |
| **3.13.3** — Separate user functionality from system management functionality. | `SC-2` Application Partitioning | — |
| **3.13.4** — Prevent unauthorized and unintended information transfer via shared system resources. | `SC-4` Information in Shared Resources | — |
| **3.13.5** — Implement subnetworks for publicly accessible system components that are physically or logically separated from internal networks. | `SC-7` Boundary Protection | A.13.1.1, A.13.1.3, A.13.2.1, A.14.1.3 |
| **3.13.6** — Deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception). | `SC-7(5)` Boundary Protection Deny by Default / Allow by Exception | — |
| **3.13.7** — Prevent remote devices from simultaneously establishing non-remote connections with organizational systems and communicating via some other connection to resources in external networks (i.e., split tunneling). | `SC-7(7)` Boundary Protection Prevent Split Tunneling for Remote Devices | — |
| **3.13.8** — Implement cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission unless otherwise protected by alternative physical safeguards. | `SC-8` Transmission Confidentiality and Integrity<br>`SC-8(1)` Transmission Confidentiality and Integrity Cryptographic or Alternate Physical Protection | A.8.2.3, A.13.1.1, A.13.2.1, A.13.2.3, A.14.1.2, A.14.1.3 |
| **3.13.9** — Terminate network connections associated with communications sessions at the end of the sessions or after a defined period of inactivity. | `SC-10` Network Disconnect | A.13.1.1 |
| **3.13.10** — Establish and manage cryptographic keys for cryptography employed in organizational systems. | `SC-12` Cryptographic Key Establishment and Management | A.10.1.2 |
| **3.13.11** — Employ FIPS-validated cryptography when used to protect the confidentiality of CUI. | `SC-13` Cryptographic Protection | A.10.1.1, A.14.1.2, A.14.1.3, A.18.1.5 |
| **3.13.12** — Prohibit remote activation of collaborative computing devices and provide indication of devices in use to users present at the device. | `SC-15` Collaborative Computing Devices | A.13.2.1* |
| **3.13.13** — Control and monitor the use of mobile code. | `SC-18` Mobile Code | — |
| **3.13.14** — Control and monitor the use of Voice over Internet Protocol (VoIP) technologies. | `SC-19` Voice over Internet Protocol | — |
| **3.13.15** — Protect the authenticity of communications sessions. | `SC-23` Session Authenticity | — |
| **3.13.16** — Protect the confidentiality of CUI at rest. | `SC-28` Protection of Information at Rest | A.8.2.3* |

### Table D-14 — 3.14 System and Information Integrity

| Requirement | NIST SP 800-53 Rev 4 | ISO/IEC 27001 |
|---|---|---|
| **3.14.1** — Identify, report, and correct system flaws in a timely manner. | `SI-2` Flaw Remediation | A.12.6.1, A.14.2.2, A.14.2.3, A.16.1.3 |
| **3.14.2** — Provide protection from malicious code at designated locations within organizational systems. | — | — |
| **3.14.3** — Monitor system security alerts and advisories and take action in response. | `SI-3` Malicious Code Protection<br>`SI-5` Security Alerts, Advisories, and Directives | A.12.2.1, A.6.1.4* |
| **3.14.4** — Update malicious code protection mechanisms when new releases are available. | `SI-3` Malicious Code Protection | A.12.2.1 |
| **3.14.5** — Perform periodic scans of organizational systems and real-time scans of files from external sources as files are downloaded, opened, or executed. | — | — |
| **3.14.6** — Monitor organizational systems, including inbound and outbound communications traffic, to detect attacks and indicators of potential attacks. | `SI-4` System Monitoring<br>`SI-4(4)` System Monitoring Inbound and Outbound Communications Traffic | — |
| **3.14.7** — Identify unauthorized use of organizational systems. | `SI-4` System Monitoring | — |
---

**Source:** NIST SP 800-171 Rev 2, *Protecting Controlled Unclassified Information in Nonfederal Systems and Organizations*, Appendix D — Mapping Tables (pp. 61–83). DOI: 10.6028/NIST.SP.800-171r2. (Public domain — U.S. Government work.) ISO/IEC 27001 mapping and asterisk convention per that appendix.
